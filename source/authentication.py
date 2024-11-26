from flask import Flask, request, render_template, session, redirect
from flask_bcrypt import Bcrypt
import sqlite3 as sql
app = Flask(__name__)

bcrypt = Bcrypt(app)

def checklogin():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            with sql.connect("databases/testgpt.db") as conn:
                c = conn.cursor()
                c.row_factory = sql.Row
                c.execute("SELECT * from teachers WHERE username=?", (username,))
                rows = c.fetchone()

                if rows and bcrypt.check_password_hash(rows['teacher_password'], password):
                    session['loggedIn'] = True
                    session['teacher_id'] = rows['teacher_id']
                    session['is_admin'] = rows['is_admin']
                    session['teacher_name'] = rows['display_name']
                    conn.close() 
                    return redirect('/home')

        except:
            conn.rollback()

        finally:
            if 'loggedIn' in session:
                conn.close()
                return redirect('/home')
            else:
                conn.close()
                msg = "Wachtwoord of naam incorrect"
                return render_template('login/login.html', msg=msg)      

def logoutsession():
    session.pop('teacher_id', None)
    session['loggedIn'] = False
    return render_template('login/login.html')

