
from flask import Flask, request, render_template, redirect, flash, session
import sqlite3 as sql
import datetime
from source.dbconnection import DB_Delete




#
#
#New note#
#
#
def newnote():
        if request.method == "POST":
            notetitle = request.form.get("notetitle")
            note_source = request.form.get("notesource")
            note_public = request.form.get("is_public")
            notecategory = request.form.get("category")
            notecontent = request.form.get("notecontent") 
            return insertnote(notetitle, notecontent, note_source, notecategory,note_public)
        
        
        conn = sql.connect("databases/testgpt.db")
        cursor = conn.cursor()
        categories = cursor.execute('''
            SELECT omschrijving, category_id FROM categories
        ''')
        categories = cursor.fetchall()

        
        conn.commit()
        conn.close()

        return render_template("notes/createnote.html", categories=categories)

def insertnote(notetitle, notecontent, note_source, notecategory, note_public):


        def insert_note(title, note_source, note_public, teacher_id, category_id, note, date_created):
            conn = sql.connect("databases/testgpt.db")
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO notes ( title, note_source, is_public, teacher_id, category_id, note, date_created)
                VALUES ( ?, ?, ?, ?, ?, ?, ?)
            ''', ( title, note_source, note_public, teacher_id, category_id, note, date_created))
            conn.commit()
            conn.close()

        current_datetime = datetime.datetime.now()
        date_created = current_datetime.strftime("%Y-%m-%d %H:%M")
        teacher_id = session['teacher_id']
        insert_note( notetitle, note_source, note_public, teacher_id, notecategory, notecontent, date_created)

        flash('The note was successfully added.', 'success')
        return redirect("/notes")
    



#
#
#Edit note#
#
#
def editnote(note_id):

    if request.method == "POST":
            title = request.form.get("title")
            note_source = request.form.get("note_source")
            is_public = request.form.get("is_public")
            teacher_id = request.form.get("teacher")
            category_id = request.form.get("category")
            note = request.form.get("note")
            return update_note(title, note_source, is_public, teacher_id, category_id, note, note_id)

    conn = sql.connect("databases/testgpt.db")
    cursor = conn.cursor()
    note = cursor.execute(f'''
    SELECT notes.note_id, title, note_source, is_public, notes.teacher_id, display_name, notes.category_id, omschrijving, note, notes.date_created
    FROM notes
    INNER JOIN teachers ON notes.teacher_id = teachers.teacher_id
    INNER JOIN categories ON notes.category_id = categories.category_id
    WHERE notes.note_id = {note_id}
    ''')
    note = cursor.fetchall()


    categories = cursor.execute('''
            SELECT omschrijving, category_id FROM categories
        ''')
    categories = cursor.fetchall()

    teachers = cursor.execute('''
            SELECT display_name, teacher_id FROM teachers
        ''')
    teachers = cursor.fetchall()

    conn.commit()
    conn.close()


    return render_template("notes/editnote.html", note=note, categories=categories, teachers=teachers)

def update_note(title, note_source, is_public, teacher_id, category_id, note, note_id):
    current_datetime = datetime.datetime.now()
    date_created = current_datetime.strftime("%Y-%m-%d %H:%M")

    conn = sql.connect("databases/testgpt.db")
    cursor = conn.cursor()
    cursor.execute("""
       UPDATE notes
       SET title = ?, note_source = ?, is_public = ?, teacher_id = ?, category_id = ?, note = ?, date_created = ?
       WHERE note_id = ?
     """, (title, note_source, is_public, teacher_id, category_id, note, date_created, note_id))

    conn.commit()
    conn.close()
    
    flash('The note was successfully edited.', 'success')
    return redirect("/notes")

#
#
#Delete note#
#
#
def removenote(note_id):
    DB_Delete(f"DELETE FROM notes WHERE note_id = {note_id}")    
    flash('The note was successfully deleted.', 'error')
    return redirect("/notes")



def search():
    note = request.form['note']
    with sql.connect("databases/testgpt.db") as conn:
            c = conn.cursor()
            c.row_factory = sql.Row
            c.execute("select * from notes where title like ?", ('%'+note+'%',))
            msg = c.fetchall()
            
    return render_template("notes/searchnotes.html",msg=msg) 