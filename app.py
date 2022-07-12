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
   
if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.secret_key = "123"
    app.run(host='0.0.0.0')

