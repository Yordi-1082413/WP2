from functools import wraps
from flask import Flask, render_template, redirect, session
from source.notespage import notespage
from source.notes import newnote, removenote, editnote, search
from source.gpthandler import gpthandler, generate_awnser, delete_awnser
from source.exportdata import export_data
from source.categories import getcategories, removecategory, categoryform, createcategory, updateform, update
from source.authentication import checklogin, logoutsession
from source.middleware import login_required, check_admin
from source.teachers import getteachers, removeteacher, createteacherform, addteacher, updateformteacher, teacherupdate
app = Flask(__name__)
from datetime import datetime
from flask_breadcrumbs import Breadcrumbs, register_breadcrumb
breadcrumbs = Breadcrumbs()
breadcrumbs.init_app(app)

@app.route('/')
def login():
    session['loggedIn'] = False
    return render_template("login/login.html")

@app.route('/home')
@login_required
@register_breadcrumb(app, '.', 'Home', order=1)
def home():
        teachername = session['teacher_name']
        return render_template("landing.html", teachername=teachername)
#<Note Routes>

#Redirect for ease of use
@app.route('/notes', methods = ['GET', 'POST'])
@login_required
@register_breadcrumb(app, '.notes', 'Notities')
def notes1():
    return redirect('notes/1')

@app.route('/notes/<int:page_id>', methods = ['GET', 'POST'])
@login_required
@register_breadcrumb(app, '.notes/', 'Notities')
def notesroute(page_id):
    return notespage(page_id)

@app.route("/newnote", methods = ['GET', 'POST'])
@login_required
@register_breadcrumb(app, '.notes.newnote', 'Nieuwe notitie', order=3)
def newnoteroute():
    return newnote()

@app.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
@login_required
@register_breadcrumb(app, '.notes.edit_note', 'Edit', order=3)
def edit_note(note_id):
    return editnote(note_id)

@app.route('/delete_note/<int:note_id>', methods=['GET', 'POST'])
@login_required
def delete_note(note_id):
    return removenote(note_id)

@app.route('/searchnotes', methods=['GET','POST'])
@login_required
@register_breadcrumb(app, '.notes.searchnotes', 'Zoeken', order=3)
def searchnotes():
    return search()

@app.route('/gpt/<int:note_id>', methods = ['GET', 'POST'])
@login_required
@register_breadcrumb(app, '.notes.gpt', 'GPT Vragen', order=3)
def gpt(note_id):
    return gpthandler(note_id)
#<Note Routes/>

#<Category Routes>
@app.route('/categories' , methods = ['GET', 'POST'])
@login_required
@register_breadcrumb(app, '.category', 'Categories')
def categories():
    return getcategories()

@app.route('/<int:category_id>/deletecategory',methods=['POST','GET'])  
@login_required 
def deletecategory(category_id):
    return removecategory(category_id)

@app.route('/categoryform')
@login_required
@register_breadcrumb(app, '.category.addcategory', 'Nieuwe categorie')
def new_category():
    return categoryform()

@app.route('/addcategory',methods=['POST','GET'])
@login_required
def addcategory():
    return createcategory()

@app.route('/<int:category_id>/updatecategoryform',methods=['POST','GET'])  
@login_required
@register_breadcrumb(app, '.category.updatecategoryform', 'Update categorie')
def updatecategoryform(category_id):
    return updateform(category_id)


@app.route('/<int:category_id>/update',methods=['POST','GET'])  
@login_required
def updatecategory(category_id):
    return update(category_id)
#<Category Routes/>

#<Login Routes>
@app.route('/authenticate', methods=['POST','GET'])
def authenticate():
    return checklogin()

@app.route('/logout')
def logout():
    return logoutsession()
#<Login Routes/>



#<Data export>

@app.route('/exportdata/<int:note_id>')
@login_required
def exportdata(note_id):
    return export_data(note_id)

#<Data export/>

#<GPT Routes>
@app.route('/generateawnser/<int:examquestion>')
@login_required
def generateawnser(examquestion):
    return generate_awnser(examquestion)

@app.route('/generatemultiawnser/<int:examquestion>')
@login_required
def generatemultiawnser(examquestion):
    return generate_awnser(examquestion, 'multi')

@app.route('/deleteawnser/<int:examquestion>')
@login_required
def deleteawnser(examquestion):
    return delete_awnser(examquestion)
#</GPT Routes/>

#<Teacher routes>
@app.route('/teachers' , methods = ['GET', 'POST'])
@check_admin
@login_required
@register_breadcrumb(app, '.teachers', 'Docenten')
def teachers():
    return getteachers()

@app.route('/<int:teacher_id>/deleteteacher',methods=['POST','GET']) 
@check_admin 
@login_required 
def deleteteacher(teacher_id):
    return removeteacher(teacher_id)

@app.route('/teacherform')
@check_admin
@login_required
@register_breadcrumb(app, '.teachers.teacherform', 'Nieuwe gebruiker')
def teacherform():
    return createteacherform()

@app.route('/createteacher',methods=['POST','GET'])
@check_admin
@login_required
def createteacher():
    return addteacher()

@app.route('/<int:teacher_id>/updateteacherform',methods=['POST','GET'])  
@check_admin
@login_required
@register_breadcrumb(app, '.teachers.updateteacherform', 'Gebruiker aanpassen')
def updateteacherform(teacher_id):
    return updateformteacher(teacher_id)


@app.route('/<int:teacher_id>/updateteacher',methods=['POST','GET'])  
@check_admin
@login_required
def updateteacher(teacher_id):
    return teacherupdate(teacher_id)

#</Teacher routes>



app.secret_key = 'C3CB66935DCFCBAB22EEF491C4593'
if __name__=='__main__':
   app.run(debug=True, host='0.0.0.0', port=8001) 
