from flask import Blueprint , render_template , request, flash, redirect , url_for
from .models import User , MyFilm
from . import db
import pandas as pd
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import login_user ,login_required , logout_user , current_user 




auth = Blueprint("auth" , __name__)

@auth.route("/login" , methods=['GET' , "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()

        if user:
            if check_password_hash(user.password , password):
                flash("Loged in successfully!" , category = 'success')
                login_user(user , remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password, try again." , category="error")
        else:
            flash('Email does not exitst' , category='error')

    return render_template('login.html' , user = current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/sign-up" , methods=['GET' , "POST"])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email = email).first()

        if user:
            flash("Email alredy exists" , category='error')
        elif len(email) < 5:
            flash('Email must be greater than 5 characters.' ,category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 2 characters.' ,category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.' ,category='error')
        elif len(password1) < 7:
            flash('Password must contain minimum 7 characters.' ,category='error')
        else:
            new_user = User(email=email , first_name=firstName, password =generate_password_hash(password1 , method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user ,remember=True)

            flash('Account created' , category='success')
            return redirect(url_for('views.home'))
        
    return render_template('sign_up.html' , user = current_user)

@auth.route('/finder' , methods = ['GET' , "POST"])
@login_required
def finder():
    if request.method == 'POST':
        min_year = request.form.get('min_year')
        max_year = request.form.get('max_year')
        director = request.form.get('director')
        actor = request.form.get('actor')
        genre = request.form.get('genre')
        films_years = []
        result_list =[]
        if int(min_year) > int(max_year):
            flash("Minimal year is greter than maximal" , category='error')
            return render_template('finder.html' , user = current_user)
        for i in range(int(min_year) , int(max_year) + 1):
            films_years.append(str(i))
        data = pd.read_csv('/Users/artemkrayevskiy/Documents/OP/2семестр_1курс/FilmFinder/website/rotten_tomatoes_movies.csv')
        movie_title = data['movie_title']
        movie_genres = data['genres']
        movie_actors = data['actors']
        movie_directors = data['directors']
        movie_years = data['original_release_date']
        rank_data = data['tomatometer_rating']
        for i in range(len(movie_actors)):
            current_directos =[]
            current_actors = []
            current_genre = []
            current_rank = rank_data[i]
            if movie_years[i] != 'nan':
                current_year = str(movie_years[i]).split('-')[0]
                for k in str(movie_directors[i]).split(','):
                    current_directos.append(k.strip())
                for k in str(movie_actors[i]).split(','):
                    current_actors.append(k.strip())
                for k in str(movie_genres[i]).split(','):
                    current_genre.append(k.strip())
                if current_year in films_years and genre in current_genre and director != '' and actor !='' and director in current_directos and actor in current_actors:
                    result_list.append([movie_title[i] , genre , movie_directors[i] , movie_actors[i] ,current_rank , i] )
                elif current_year in films_years and genre in current_genre and director == '' and actor !='' and actor in current_actors:
                    result_list.append([movie_title[i] , genre , movie_directors[i] , movie_actors[i] , current_rank , i ])
                elif current_year in films_years and genre in current_genre and actor == '' and director !='' and director in current_directos:
                    result_list.append([movie_title[i] , genre , movie_directors[i] , movie_actors[i] , current_rank , i])
                elif current_year in films_years and genre in current_genre and actor == '' and director =='':
                    result_list.append([movie_title[i] , genre , movie_directors[i] , movie_actors[i] , current_rank , i])
        new_result = []
        result_list.sort(key = lambda x:int(x[4]))
        for i in range(len(result_list)-1 , -1 , -1):
            new_result.append(result_list[i])
        return render_template('film_result.html'  , user = current_user ,films = new_result)
    else:
        return render_template('finder.html'  , user = current_user)
    

@auth.route('/finder/<int:id>' , methods = ["POST" , 'GET'])
@login_required
def film_detail(id):
    if request.method == 'GET':
        data = pd.read_csv('/Users/artemkrayevskiy/Documents/OP/2семестр_1курс/FilmFinder/website/rotten_tomatoes_movies.csv')
        movie_title = data['movie_title']
        movie_genres = data['genres']
        movie_actors = data['actors']
        movie_directors = data['directors']
        movie_years = data['original_release_date']
        rank_data = data['tomatometer_rating']
        runtime = data['runtime']
        info = data['movie_info']
        critics_consensus = data['critics_consensus']
        content_rating = data['content_rating']
        authors = data['authors']
        production_company = data['production_company']
        result = [id ,movie_title[id] ,movie_genres[id] , movie_actors[id]  , movie_directors[id] , movie_years[id] ,rank_data[id] , runtime[id] ,info[id],critics_consensus[id] ,content_rating[id] , authors[id] , production_company[id]]
        return render_template('film_details.html' , user = current_user , film = result)
    elif request.method == 'POST':
        data = pd.read_csv('/Users/artemkrayevskiy/Documents/OP/2семестр_1курс/FilmFinder/website/rotten_tomatoes_movies.csv')
        movie_title = data['movie_title']
        movie_genres = data['genres']
        movie_actors = data['actors']
        movie_directors = data['directors']
        movie_years = data['original_release_date']
        rank_data = data['tomatometer_rating']
        runtime = data['runtime']
        info = data['movie_info']
        critics_consensus = data['critics_consensus']
        content_rating = data['content_rating']
        authors = data['authors']
        production_company = data['production_company']
        result = [id , movie_title[id] ,movie_genres[id] , movie_actors[id]  , movie_directors[id] , movie_years[id] ,rank_data[id] , runtime[id] ,info[id],critics_consensus[id] ,content_rating[id] , authors[id] , production_company[id]]
        new_film = MyFilm(title = movie_title[id],genres= movie_genres[id] ,actors =movie_actors[id]  , directors =movie_directors[id]  ,release_date = movie_years[id] , rank =rank_data[id] , runtime = runtime[id], authors = authors[id],info = info[id] ,critics_consensus = critics_consensus[id] , content_rating  = content_rating[id] ,production_company  = production_company[id] , user_id = current_user.id)
        db.session.add(new_film)
        db.session.commit()
        flash('Film added!' , category='success')
        return render_template('film_details.html' , user = current_user , film = result)


@auth.route('/myaccount' , methods = ['GET' , "POST"])
@login_required
def myaccount():
    return render_template('myaccount.html' , user = current_user)

@auth.route('/myaccount/<int:id>' , methods = ['GET' , "POST"])
@login_required
def myaccount_film(id):
    if request.method == "GET":
        film = MyFilm.query.get(id)
        return render_template('myaccount_film.html' , user = current_user  , film = film )
    elif request.method == "POST":
        film = MyFilm.query.get_or_404(id)
        try:
            db.session.delete(film)
            db.session.commit()
            return render_template('myaccount.html' , user = current_user)
        except:
            "An error ocured while deleting this film"

