from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class MyFilm(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(10000))
    genres = db.Column(db.String(10000))
    actors = db.Column(db.String(10000))
    directors = db.Column(db.String(10000))
    release_date = db.Column(db.String(10000))
    rank = db.Column(db.String(10000))
    runtime = db.Column(db.String(10000))
    authors = db.Column(db.String(10000))
    info = db.Column(db.Text)
    critics_consensus = db.Column(db.Text)
    content_rating = db.Column(db.String(10000))
    production_company = db.Column(db.String(10000))
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'))

class Note(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone = True) , default =func.now())
    user_id = db.Column(db.Integer , db.ForeignKey('user.id')) 

class User(db.Model , UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(150) , unique = True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    films = db.relationship('MyFilm')
