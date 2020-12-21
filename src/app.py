#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify,request #Contiene toda la informacion del cliente

#se importan librerias para pagina web
from flask import render_template, redirect, url_for, session, send_from_directory, escape, request, Response

from forms import SignupForm, LoginForm #Publicaciones #PostForm, 
from models import usuario, Planta, Album, ExcGroup
from markupsafe import escape
from werkzeug.utils import secure_filename

import sqlobject as SO

import os
UPLOAD_FOLDER = os.path.abspath("../uploads/") 
ALLOWED_EXTENSIONS = set(["png","jpg","gif", "jpeg"])

app = Flask(__name__, template_folder = '../templates', static_folder='../static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://invitado:invitado@localhost/app_db'
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = 'cualquier cadena aleatoria'



def allow_file(filename):
  return "." in filename and filename.rsplit("." , 1)[1] in ALLOWED_EXTENSIONS


@app.route("/user/", methods=['GET', 'POST'])
def index():
  response = Response()
  response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0') 

  info = ''
  form = LoginForm()
  if form.validate_on_submit():
    name = form.username.data
    passwor = form.password.data
    print(name)
    print(passwor)


    session [ 'username' ] = name


    user1 = usuario.get_user(name)


    if(user1 is None):
      info = 'User not found'
    elif((user1.check_password(passwor) != True)):
      info='Invalid password, retry'
    else:
      user1.login(True)
      route = '/' + form.username.data
      return redirect(route)
  return render_template('ingresar.html', form = form, info = info)  



@app.route('/<name>', methods=['GET', 'POST'])
def profile(name):
    form = LoginForm()
    user1 = usuario.get_user(name)
    print(user1)
    if user1 and user1.get_islogin() and (user1.get_username() == name):
      info = "BIENVENIDO " + name
      #Cargo las tablas en funcion del nombre
      
      #creo las plantas del usuario
      planta = Planta(permiso = 'PRI', especie = "tomate", )
      user1.addPlanta(planta)

      if planta.albumcheck() == None:
        print("El album esta vacio")
      #else:
      #  print(planta.Album.getimage(1))
      return render_template('home.html', form=form, info = info, route = name + "/upload", image_name = "pp.jpeg");
    #con el nombre tengo que saber que imagen tengo cargada, porque te tiene que decir, tengo que ir a la BD  
    return "user not sign in"




@app.route('/<name>/upload', methods=['GET', 'POST'])
def upload(name):
    array = []
    #tengo que pasarle a upload.html el listado de plantas para ese usuario
    #Busco las plantas que tiene el usuario
    user1 = usuario.get_user(name)
    
    i = 0
    for user1.get_id in user1.planta:
      planta = Planta.get_Planta(user1.get_id)
      array.insert(i, planta.especie)
      print(array)


    # ---------------------------------------------------------------------------------
    if request.method == 'POST':      
      
      #Si no existe el input o no tiene la validacion correcta, o el formulario no tiene la parte que corresponde al archivo
      if "ourfile" not in request.files:
        return "the form has no file part"
      f = request.files["ourfile"]
      #Si no se selecciono ningun archivo
      if f.filename == "":
        return "No file selected"
      if f and allow_file(f.filename):
        filename = secure_filename(f.filename) #Cambia todos las barras por _ dentro del archivo
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        print ("Your file has been uploaded " + filename)


        #validacion de existencia de especie de planta
        especieIngresada = request.form['especie_form']
        if especieIngresada not in array:
          return "Especie no encontrada"

        return redirect(url_for("profile", name = session [ 'username' ]))
      return "file not allowed"
    return render_template('upload.html', especie = array, cantidad = len(array))
    


@app.route("/uploads/<filename>")
def get_file(filename):
  album = Album(ruta = UPLOAD_FOLDER, imagename = filename, albumname = "albumname", timestamp = 'HH:MM:SS')
  return send_from_directory(app.config["UPLOAD_FOLDER"], filename)



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
    
    user1 = usuario.get_user(session.pop ( 'username' , None ))
    
    user1.login(False)

    return redirect(url_for('index'))




if __name__ == "__main__":

    connection = SO.connectionForURI("mysql://invitado:invitado@localhost/app_db")
    SO.sqlhub.processConnection = connection
    # connection.debug = True

    # borro las tablas si ya existian
#    Planta.dropTable()
#    ExcGroup.dropTable()
#    Album.dropTable()
#    usuario.dropTable()

    # creo las tablas
 #   usuario.createTable();
 #   Album.createTable()
 #   ExcGroup.createTable();
 #   Planta.createTable();
    

    ExcGroup(planta = "maria")
    #album = Album(title = "empty") #La tabla usuarios no puede referenciar una tabla albums vacia
    
    app.run(debug=True)