from functools import wraps
from flask import render_template, session

def check_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['is_admin'] == 0:
            return render_template("landing.html")
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['loggedIn'] == False:
            return render_template("login/login.html")
        return f(*args, **kwargs)
    return decorated_function
