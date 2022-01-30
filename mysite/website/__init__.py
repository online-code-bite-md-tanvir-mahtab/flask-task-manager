# import imp
import imp
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_restful import Api, Resource, abort, marshal_with, reqparse, fields
from flask_login import login_user, login_required, logout_user, current_user


# creating the instance of the Sqlialchemy
db = SQLAlchemy()


# now i am going to create the
DB_NAME = 'database.db'
def create_app():
    app = Flask(__name__,template_folder='template')
    api = Api(app)
    # secret key
    app.config['SECRET_KEY'] = 'md tanvir'
    
    # configuring with the flask
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    # now i am going to inisialize the app to the database
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    from .api import Task
    
    # now I am going to register the view
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    print(current_user)
    api.add_resource(Task,f'/tasks/<int:u_id>/<int:id>')
    
    # importing the database class
    from .models import Tasks, User
    
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app


def  create_database(app):
    if not path.exists(path='website/' + DB_NAME):
        with app.app_context():
            db.create_all(app= app)
            
        print("Database is created")