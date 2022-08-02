from pdb import post_mortem
import sqlite3
from wsgiref.validate import validator
from flask import Flask, flash, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#These are for reading from the databases
connection = sqlite3.connect("test.db")
crsruser = connection.cursor()
crsrid = connection.cursor()
crsrreview = connection.cursor()

crsrid = connection.cursor()
crsrname = connection.cursor()
crsrprice = connection.cursor()
    
#User Class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    
    def __init__(self, title, complete):
        self.title = title
        self.complete = complete
    
class reviews_table_test(db.Model):
    review_number = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), db.ForeignKey('user.username'))
    review = db.Column(db.Text)

    def init(self, username, review):
        self.username = username
        self.review = review
             
#this is the database for user reviews
reviews_list = []
crsruser.execute("SELECT username FROM reviews_table_test")
crsrreview.execute("SELECT review FROM reviews_table_test")
rowuser = crsruser.fetchone()
rowreview = crsrreview.fetchone()
while rowreview is not None:
    rowuser = " ".join(str(x) for x in rowuser)
    rowreview = " ".join(str(x) for x in rowreview)
    print(rowuser, rowreview)
    new_review = reviews_table_test(
        username = rowuser,
        review = rowreview)
    reviews_list.append(new_review)   
    rowuser = crsruser.fetchone()
    rowreview = crsrreview.fetchone()
        
    
@app.route('/', methods=['GET', 'POST'])
def home():
    if not session.get('logged_in'):
        return render_template('index.html')
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        try:
            data = User.query.filter_by(username=username, password=password).first()
            if data is not None:
                session["username"] = username
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                session['logged_in'] = False
                return '''
            <html>
            <head> Incorrect Log In </head>
            <a href="/login">
            <button>Go back</button>
            </a>    
            </html
            '''
        except:
            session['logged_in'] = False
            return "Not Logged In"

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = User(
            username=request.form['username'],
            password=request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html')
    return render_template('register.html')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))
   

@app.route("/task")
def task():
    todo_list = Todo.query.all()
    return render_template("task.html", todo_list=todo_list)
 
 
@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("task"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("task"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("task"))

@app.route("/survey", methods=['GET', 'POST'])
def survvey():
    tempUser = session['username']
    if request.method == 'POST':
        new_review = reviews_table_test(
            username = tempUser,
            review = request.form['review'])
        reviews_list.append(new_review)   
        db.session.add(new_review)
        db.session.commit()
    return render_template('survey.html', IdNum = id, review_list = reviews_list)
    

@app.route("/reviews", methods=['GET', 'POST'])
def reviews():
    tempUser = session['username']
    if request.method == 'POST':
        new_review = reviews_table_test(
            username = tempUser,
            review = request.form['review'])
        reviews_list.append(new_review)   
        db.session.add(new_review)
        db.session.commit()
    return render_template('reviews.html', review_list = reviews_list)
 
 
@app.route("/userprofile", methods=['GET', 'POST'])
def accountdetails():
     return render_template('userprofile.html')
 
@app.route("/changepassword", methods=['GET', 'POST'])
def changepassword():
    tempuser = session['username']
    temppuser = User.query.filter_by(username = tempuser).first()
    tempid = temppuser.id
    temppass = temppuser.password
    print(tempuser)
    print(tempid)
    if request.method == 'POST':
        password=request.form['password']
        temppuser.password =request.form['newpassword']
        if password == temppass:
            db.session.commit()
            flash('Your password has been updated!')
            return render_template('index.html')
        else:
            flash('You entered an incorrect password')
            return render_template('changepassword.html')
    return render_template('changepassword.html')
 
 

if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.secret_key = "123"
    app.run(host='0.0.0.0')

