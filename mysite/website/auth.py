# from multiprocessing import AuthenticationError
# import imp
import re
from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, Tasks
from . import db



def is_valide(f_name=None,s_name=None,email=None,password1=None,password2=None):
    if len(email) != 0 or len(email)>6 and len(password1) != 0 or len(password1)>6:
        return True
    elif len(f_name)!=0 or len(f_name)>6 and len(s_name) != 0 or len(s_name)>6 and len(email) != 0 or len(email)>6 and len(password1) != 0 or len(password1)>6 and len(password2) != 0 or len(password2)>6:
        return True
    else:
        return False

auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if is_valide(email=email,password1=password):
            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, request.form.get('password')):
                    login_user(user,remember=False)
                    return redirect(url_for('views.home'))
                else:
                    print("incorrect password")
            else:
                return redirect(url_for('auth.signup'))
        else:
            return redirect(url_for('.auth.login'))
    return render_template('login.html',user=current_user)

@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        f_name = request.form.get('fullname')
        s_name = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password')
        password2  = request.form.get('password2')
        if is_valide(f_name,s_name,email,password1,password2):
            new_user = User(email=email,username=s_name,password=generate_password_hash(password= password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('auth.signup'))
        
    return render_template('signup.html',user=current_user)

@auth.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('auth.login'))