# in here we are going to crete all the data here
import email
from time import timezone
from . import db
from sqlalchemy import func
from flask_login import UserMixin



class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    task = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default= func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150),unique=True)
    username = db.Column(db.String(150))
    password = db.Column(db.String(150))
    tasks = db.relationship('Tasks')