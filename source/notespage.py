from flask import Flask, request, render_template
import sqlite3 as sql
import math


def notespage(page_id):

    rows_per_page = 20
    offset = (page_id - 1) * rows_per_page

    conn = sql.connect("databases/testgpt.db")
    cursor = conn.cursor()
    cursor.row_factory = sql.Row
    cursor.execute('''
    SELECT notes.note_id, title, note_source, is_public, notes.teacher_id, display_name, notes.category_id, omschrijving, note, notes.date_created
    FROM notes 
    INNER JOIN teachers ON notes.teacher_id = teachers.teacher_id
    INNER JOIN categories ON notes.category_id = categories.category_id
    LIMIT ? OFFSET ?
    ''', (rows_per_page, offset))

    notes = cursor.fetchall()   
    
    cursor.execute('SELECT COUNT(*) FROM notes')
    total_notes = cursor.fetchone()[0]


    max_pages = math.ceil(total_notes / rows_per_page)
    conn.commit()
    conn.close()



    return render_template("notes/notes.html", notes=notes, page_id=page_id, max_pages=max_pages)
