#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify,request #Contiene toda la informacion del cliente


#se importan librerias para pagina web
from flask import render_template, redirect, url_for, session

from forms import SignupForm, LoginForm #PostForm, 
from models import usuario, Album

import sqlobject as SO

#from flask_mysqldb import MySQL
#import bcrypt 


app = Flask(__name__, template_folder = '../templates', static_folder='../static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://invitado:invitado@localhost/app_db'
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

@app.route("/", methods=['GET', 'POST'])
def index():
  info = ''
  form = LoginForm()
  if form.validate_on_submit():
    name = form.username.data
    passwor = form.password.data
    print(name)
    print(passwor)

    user1 = usuario.get_user(name)
    if(user1 is None):
      info = 'User not found'
    elif((user1.check_password(passwor) != True)):
      info='Invalid password, retry'
    else:
      return render_template('home.html', form = form, info = 'BIENVENIDO');
  return render_template('ingresar.html', form = form, info = info)  


#Defino la ruta principal
@app.route('/registro/', methods=['GET', 'POST'])
def log():
  info = ''
  form = SignupForm()
  if form.validate_on_submit():
      name = form.username.data
      email = form.email.data
      passwor = form.password.data
      print(name)
      print(email)
      print(passwor)

      if((usuario.check_user(name) == True) ):
        info='User already in use, retry'
      else:
        user = usuario(username = name, email = email, passwo = usuario.set_password(passwor)) 
        info='User register susessfully, login'

  return render_template('registro.html', form = form, info = info)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))




if __name__ == "__main__":

    connection = SO.connectionForURI("mysql://invitado:invitado@localhost/app_db")
    SO.sqlhub.processConnection = connection
    # connection.debug = True

    # borro las tablas si ya existian
    #usuario.dropTable(ifExists=True)
    #Album.dropTable(ifExists=True)

    # creo las tablas
    #Album.createTable()
    #usuario.createTable()

    app.run(debug=True)

