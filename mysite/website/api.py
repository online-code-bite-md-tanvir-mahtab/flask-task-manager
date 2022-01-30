from email import message
from flask_login import current_user
from flask_restful import Api, Resource, abort, marshal_with, reqparse, fields
from .models import *
from . import db


how_the_will_look = {
    'id':fields.Integer,
    'name':fields.String,
    'task':fields.String,
    'date':fields.DateTime,
}
video_put_args = reqparse.RequestParser()
video_put_args.add_argument('name',type=str,help='Name field is required to fill',required=True)
video_put_args.add_argument('task',type=int,help='Views field is required',required=True)
video_put_args.add_argument('date',type=int,help='Likes field also required')
class Task(Resource):
    
    @marshal_with(how_the_will_look)
    def get(self,u_id,id):
        user = User.query.filter_by(id= u_id).first()
        print(user.username)
        if user.id == current_user.id:
            task = Tasks.query.filter_by(id= id).first()
            return task
        else:
            abort(404,message="Could not found")
    @marshal_with(how_the_will_look)
    def post(self, u_id,id):
        user = User.query.filter_by(id= u_id).first()
        if user.id == current_user.id:
            args = video_put_args.parse_args()
            result = Tasks.query.filter_by(id= id).first()
            if result:
                abort(400,"Task already taken")
            task = Tasks(id= id,name=args['name'],task=args['task'])
            db.session.add(task)
            db.session.commit()
            return task, 201
        else:
            abort(501,"Server problem Can't access")
