import datetime
from flask import Flask, render_template, request, flash, redirect
import sqlite3 as sql
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)

def getteachers():
   database_file = "databases/testgpt.db"
   conn = sql.connect(database_file)
   c = conn.cursor()
   c.row_factory = sql.Row
   c.execute("SELECT * from teachers")
   rows = c.fetchall()
   return render_template("teachers/teachers.html",rows=rows)

def removeteacher(teacher_id):
    with sql.connect("databases/testgpt.db") as conn:
        c = conn.cursor()
        c.execute("delete from teachers where teacher_id=?", (teacher_id,))
        conn.commit()
        flash('Docent verwijderd', 'error')
        return redirect(request.referrer)
    
def createteacherform():
    return render_template('teachers/createteacher.html')

def addteacher():
    if request.method == 'POST':
        try:
          name = request.form['name']
          username = request.form['username']
          teacher_password = request.form['password']
          hashed_password = bcrypt.generate_password_hash(teacher_password)
          current_datetime = datetime.datetime.now()
          date_created = current_datetime.strftime("%Y-%m-%d %H:%M")
          is_admin = 0
          
          with sql.connect("databases/testgpt.db") as conn:
            c = conn.cursor()
            c.execute("INSERT INTO teachers (display_name,username,teacher_password,date_created, is_admin) VALUES (?,?,?,?,?)",(name,username,hashed_password,date_created, is_admin))
            conn.commit()

        except:
           conn.rollback()

        finally:
           flash('Docent toegevoegd', 'success')
           return redirect("../teachers")


def updateformteacher(teacher_id):
      with sql.connect("databases/testgpt.db") as conn:
            c = conn.cursor()
            c.row_factory = sql.Row
            c.execute("SELECT * from teachers where teacher_id=?", (teacher_id,))
            teacher = c.fetchall()
            return render_template('teachers/editteacher.html', teacher=teacher)

def teacherupdate(teacher_id):
    if request.method == 'POST':
        try:
          name = request.form['name']
          username = request.form['username']
          teacher_password = request.form['password']
          hashed_password = bcrypt.generate_password_hash(teacher_password)
          current_datetime = datetime.datetime.now()
          date_created = current_datetime.strftime("%Y-%m-%d %H:%M")
          is_admin = 0
          
          with sql.connect("databases/testgpt.db") as conn:
            c = conn.cursor()
            c.execute("UPDATE teachers SET display_name=?,username=?,teacher_password=?, date_created=?, is_admin=? where teacher_id=?", (name,username,hashed_password, date_created, is_admin, teacher_id))
            conn.commit()

        except:
           conn.rollback()

        finally:
           flash('Docent geüpdate', 'success')
           return redirect("../teachers")
    
      