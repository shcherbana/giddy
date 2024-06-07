from flask import Blueprint , render_template , request , flash , jsonify
from flask_login import login_required , current_user
from .models import Note
from . import db
import json
import pandas as pd 


views = Blueprint("views" , __name__)

@views.route('/' , methods =['GET' , 'POST'])
@login_required
def home():
    data = pd.read_csv('/Users/artemkrayevskiy/Documents/OP/2семестр_1курс/FilmFinder/website/rotten_tomatoes_movies.csv')
    movie_title = data['movie_title']
    movie_genres = data['genres']
    movie_actors = data['actors']
    movie_directors = data['directors']
    movie_years = data['original_release_date']
    rank_data = data['tomatometer_rating']
    result = []
    for i in range(len(movie_actors)):
        try:
            int(rank_data[i])
            if movie_years[i] != 'nan':
                current_year = str(movie_years[i]).split('-')[0]
            if int(current_year) > 1990 and rank_data[i] != None:
                result.append([movie_title[i] , movie_directors[i] ,rank_data[i] ,i ])
        except:
            print((rank_data[i]))
            continue
            
    result.sort(key = lambda x:int(x[2]))
    result = result[-100:]
    return render_template('home.html' , user=current_user ,films=result)

@views.route('/delete-note' , methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})