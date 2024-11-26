import sqlite3 as sql
import csv
from flask import send_file

def export_data(note_id):
   conn = sql.connect("databases/testgpt.db")
   cursor = conn.cursor()
   cursor.execute(f'''
   SELECT exam_question, awnsers.content, questions.date_created
   FROM questions
   LEFT JOIN awnsers on questions.questions_id = awnsers.questions_id
   WHERE questions.note_id = {note_id}
   ''')
   data = cursor.fetchall()

   with open('temp/data.csv', 'w', newline='') as file:
       writer = csv.writer(file)
       writer.writerow(["exam_question", "awnser", "date_created"])
       writer.writerows(data)
   return send_file('temp/data.csv', as_attachment=True)
