#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify,request #Contiene toda la informacion del cliente
from forms import SignupForm
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


#se importan librerias para pagina web
from flask import render_template, redirect, url_for, session


#from flask_wtf import FlaskForm
#from wtforms import Form, BooleanField, StringField, PasswordField, validators, SubmitField
#from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

#from flask_mysqldb import MySQL
import bcrypt 


app = Flask(__name__, template_folder = '../templates', static_folder='../static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://invitado:invitado@localhost/app_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

db = SQLAlchemy(app)
ma = Marshmallow(app)

#Semilla para encriptamiento
semilla = bcrypt.gensalt()

class Task(db.Model):
    id        = db.Column(db.Integer    , primary_key=True)
    username  = db.Column(db.String(26) , unique=True, nullable=False)
    email     = db.Column(db.String(100), unique=True, nullable=False)
    password  = db.Column(db.String(60) , nullable=False)
#    def __init__(self, title, description):
#        self.title = title
#        self.description = description

db.create_all()

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password')


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)




@app.route("/")
def index():
    page = request.args.get('page', 1)
    list = request.args.get('list', 20)
    return render_template('ingresar.html')


#Defino la ruta principal
@app.route('/registro/', methods=['GET', 'POST'])
def log():
#    if request.method == 'POST':
#      name = request.form['username']
#      email = request.form['password']
#      password = request.form['email']
  form = SignupForm()
  if form.validate_on_submit():
      name = form.username.data
      email = form.email.data
      password = form.password.data
      print(name)
      print(email)
      print(password)
  return render_template('registro.html', form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)


#Tengo que hacer algo si los datos no son validos
#Tengo que agregar vistas de una misma pagina
