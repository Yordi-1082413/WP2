import datetime
from flask import Flask, render_template, request, session, redirect, flash
app = Flask(__name__)
import sqlite3 as sql

def getcategories():
   database_file = "databases/testgpt.db"
   conn = sql.connect(database_file)
   c = conn.cursor()
   c.row_factory = sql.Row
   c.execute("SELECT * from categories")
   rows = c.fetchall()
   return render_template("categories/categories.html",rows=rows)

def removecategory(category_id):
    with sql.connect("databases/testgpt.db") as conn:
        c = conn.cursor()
        c.execute("delete from categories where category_id=?", (category_id,))
        conn.commit()
        flash('Categorie verwijderd', 'error')
        return redirect(request.referrer)

def createcategory():
    if request.method == 'POST':
        try:
          category = request.form['category']
          current_datetime = datetime.datetime.now()
          date_created = current_datetime.strftime("%Y-%m-%d %H:%M")
          
          with sql.connect("databases/testgpt.db") as conn:
            c = conn.cursor()
            c.execute("INSERT INTO categories (omschrijving,date_created) VALUES (?,?)",(category,date_created))
            conn.commit()

        except:
           conn.rollback()

        finally:
           conn.close()
           flash('Nieuwe categorie toegevoegd', 'success')
           return redirect('categories')

def categoryform():
    return render_template('categories/createcategory.html')

def updateform(category_id):
      with sql.connect("databases/testgpt.db") as conn:
            c = conn.cursor()
            c.row_factory = sql.Row
            c.execute("SELECT * from categories where category_id=?", (category_id,))
            category = c.fetchall()
            return render_template('categories/editcategory.html', category=category)
      
def update(category_id):
    if request.method == 'POST':
        try:
          category = request.form['category']
          current_datetime = datetime.datetime.now()
          date_created = current_datetime.strftime("%Y-%m-%d %H:%M")
          
          with sql.connect("databases/testgpt.db") as conn:
            c = conn.cursor()
            c.execute("UPDATE categories SET omschrijving=?, date_created=? where category_id=?", (category, date_created, category_id))
            conn.commit()

        except:
           conn.rollback()

        finally:
            conn.close() 
            flash('Categorie aangepast', 'success')
            return redirect('../categories')
            

if __name__ == '__main__':
    app.run(debug=True, port=8001) 