# from crypt import methods
from asyncio import Task, tasks
# import imp
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from website import models
from . import db
import website
from .models import Tasks, User


# inisializing the object instance
views = Blueprint('views',__name__)

# creating a new empty data list
data = []

@views.route('/',methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        task = request.form.get('task')
        if len(name) != 0 and len(task) != 0:
            new_task = Tasks(name=name,task=task,user_id= current_user.id)
            db.session.add(new_task)
            db.session.commit()
            # print("Seession is created")
            return redirect(url_for('views.showlist'))
    return render_template('home.html', user=current_user)


@views.route('/showlist')
@login_required
def showlist():
    # print("the type : ",type(Tasks))
    tasks = Tasks.query.all()
    
    # for item in tasks:
    #     print(item.name)
    return render_template('showlist.html',tasks=tasks, user=current_user)

@views.route('/deleteitem/<int:id>')
@login_required
def deleteitem(id):
    # print("Clickeed")
    tasks = Tasks.query.all()
    # print(len(tasks))
    # print(tasks[id-1])
    items = Tasks.query.get_or_404(id)
    try:
        db.session.delete(items)
        db.session.commit()
        return redirect(url_for('views.showlist'))
    except:
        pass
    return redirect(url_for('views.showlist'))

@views.route('/apidocs')
@login_required
def apidocs():
    return render_template('apidocs.html', user= current_user)

