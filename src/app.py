#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify,request #Contiene toda la informacion del cliente
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
app.config['SECRET KEY'] = '966a98e7b6fd851217f6f90db9f0e1da'

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



#Defino la ruta principal
@app.route('/registro', methods=['GET', 'POST'])
def log():
    if request.method == 'POST':
      name = request.form['username']
      email = request.form['password']
      password = request.form['email']
      print(name)
      print(email)
      print(password)
    return render_template('registro.html')#, form = Form)



if __name__ == "__main__":
    app.run(debug=True)