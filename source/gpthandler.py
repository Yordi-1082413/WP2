from flask import render_template, request, redirect, flash
from lib.testgpt.testgpt import FakeTestGPT
from source.dbconnection import DB_Write, DB_Delete
import sqlite3 as sql
import datetime
from lib.testgpt.testgpt import TestGPT


def gpthandler(note_id):

    if request.method == "POST":
        userquestion = request.form.get("gptquestion")
        title = request.form.get("title")
        note = request.form.get("note")
        category = request.form.get("category")
        ismultiplechoice = request.form.get("multiplechoicecheckbox")
        return gptquestion(userquestion, title, note, category, note_id, ismultiplechoice)

    conn = sql.connect("databases/testgpt.db")
    conn.row_factory = sql.Row
    cursor = conn.cursor()
    note = cursor.execute(f'''
        SELECT notes.note_id, title, note_source, is_public, notes.teacher_id, display_name, notes.category_id, omschrijving, note, notes.date_created
        FROM notes
        INNER JOIN teachers ON notes.teacher_id = teachers.teacher_id
        INNER JOIN categories ON notes.category_id = categories.category_id
        WHERE notes.note_id = {note_id}
        ''')
    note = cursor.fetchall()

    examquestions = cursor.execute(f'''
        SELECT questions.questions_id, exam_question, questions.date_created
        FROM questions
		WHERE questions.note_id = {note_id}
        ''')
    examquestions = cursor.fetchall()

    examawnsers = cursor.execute(f'''
        SELECT questions.note_id, questions.questions_id, exam_question, awnsers.content
        FROM questions
        LEFT JOIN awnsers on questions.questions_id = awnsers.questions_id
        WHERE questions.note_id = {note_id}
        ''')
    examawnsers = cursor.fetchall()


    return render_template("gptform.html", note=note, examquestions=examquestions, examawnsers=examawnsers)


def gptquestion(userquestion, title, note, category, note_id, ismultiplechoice):
    with open(".env") as keyfile:
        key = keyfile.read()
    testgpt = TestGPT(key)


    question = userquestion + title + note

    if ismultiplechoice:
        exam_question = testgpt.generate_multiple_choice_question(question)
    else:
        exam_question = testgpt.generate_open_question(question)


    current_datetime = datetime.datetime.now()
    date_created = current_datetime.date()

    conn = sql.connect("databases/testgpt.db")
    cursor = conn.cursor()
    cursor.execute('''
            INSERT INTO questions ( note_id, exam_question, date_created)
            VALUES (?, ?, ?)
            ''', (note_id, exam_question, date_created))
    conn.commit()
    conn.close()

    flash('Nieuwe vraag toegevoegd', 'success')
    return redirect(request.referrer)


def generate_awnser(question_id):
    with open(".env") as keyfile:
        key = keyfile.read()
    testgpt = TestGPT(key)

#Pulls the exam questions
    conn = sql.connect("databases/testgpt.db")
    cursor = conn.cursor()
    exam_question = cursor.execute(f'''
        SELECT exam_question
        FROM questions
        WHERE questions_id = {question_id}
    ''')
    exam_question = cursor.fetchall()
    question = exam_question[0][0]
    examawnser = testgpt.generate_open_awnser(question)


    current_datetime = datetime.datetime.now()
    date_created = current_datetime.date()


#Writes the newly generated question to the DB
    
    try:
        cursor.execute('''
                INSERT INTO awnsers ( questions_id, content, date_created)
                VALUES (?, ?, ?)
                ''', ( question_id, examawnser, date_created))
        conn.commit()
        flash('Nieuw antwoord toegevoegd', 'success')
    except sql.IntegrityError:
        flash('Er bestaat al een antwoord voor deze vraag', 'error')
    finally:
        conn.close()

    return redirect(request.referrer)



def delete_awnser(examquestionid):
    DB_Delete(f"DELETE FROM questions WHERE questions_id = {examquestionid}")
    flash('Antwoord verwijderd', 'error')
    return redirect(request.referrer)