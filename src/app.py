#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify,request #Contiene toda la informacion del cliente


#se importan librerias para pagina web
from flask import render_template, redirect, url_for, session

from forms import SignupForm #PostForm, LoginForm
from models import usuario, Album

import sqlobject as SO

#from flask_mysqldb import MySQL
#import bcrypt 


app = Flask(__name__, template_folder = '../templates', static_folder='../static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://invitado:invitado@localhost/app_db'
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'


@app.route("/")
def index():
    page = request.args.get('page', 1)
    list = request.args.get('list', 20)
    return render_template('ingresar.html')


#Defino la ruta principal
@app.route('/registro/', methods=['GET', 'POST'])
def log():
  form = SignupForm()
  if form.validate_on_submit():
      name = form.username.data
      email = form.email.data
      passwor = form.password.data
      print(name)
      print(email)
      print(passwor)

      usuario(username = name, email = email, passwo = usuario.set_password(passwor))
      

  return render_template('registro.html', form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))




if __name__ == "__main__":

    connection = SO.connectionForURI("mysql://invitado:invitado@localhost/app_db")
    SO.sqlhub.processConnection = connection
    # connection.debug = True

    # borro las tablas si ya existian
    
    usuario.dropTable(ifExists=True)
    Album.dropTable(ifExists=True)

    # creo las tablas
    Album.createTable()
    usuario.createTable()

    app.run(debug=True)

