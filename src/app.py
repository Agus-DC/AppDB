#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify,request #Contiene toda la informacion del cliente

#se importan librerias para pagina web
from flask import render_template, redirect, url_for, session, send_from_directory, escape, request, Response

from forms import SignupForm, LoginForm #Publicaciones #PostForm, 
from models import usuario, Planta, Album, ExcGroup
from markupsafe import escape
from werkzeug.utils import secure_filename
from datetime import datetime
from bs4 import BeautifulSoup
import time
import requests
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
    array = []
    arrayPlanta = []
    planta1 = []
    album1 = []
    albunesTotales = []
    indice = []
    i = 0
    ii = 0
    j = 0
    k =0
    aux2 = 0
    parameter = 0 
    p = 0

    ownname = session [ 'username' ]
    guestname = name
    
    isOwner =  True if (ownname == guestname) else False
    userOwner = usuario.get_user(ownname)

    print("usuario: ", user1)



    if user1 is not None:

      for b in user1.planta: #planta
        planta = Planta.get_Planta(b) 
        if ExcGroup.accesible(planta, userOwner):
          print(" A esta planta pude acceder: ", planta)
          arrayPlanta.insert(j, planta.especie)  
        else:
          arrayPlanta.insert(j, None)
      
      arrayPlanta.reverse()
      print("Las plantas que hay para el usuario son: ", arrayPlanta)
      cantPlantas = len(arrayPlanta)
      print("cantidad de plantas: ", cantPlantas)


      if (user1.get_username() == name):
        info = ""
        #consulto si el usuario tiene plantas
        if user1.planta:
          print("hay plantas! ")
          print(user1.planta)  #Son todas las plantas
          for z in arrayPlanta:#son solo nombres de plantas
            print("LA PLANTA QUE LE ESTOY PASANDO ES: ", user1.planta[p])
            
            if ExcGroup.accesible(user1.planta[p], userOwner):
              print("Accesible PA",user1.planta[p])
              planta_id_user1 = user1.planta[p].id            #Planta 0 del usuario 1        
              planta1.insert(i, Planta.get_Planta(planta_id_user1))

              print("Paso1")
              print(planta1[i])
          

              album1.insert(i, Album.get_images(planta1[i]))


              print("Paso1.2")


              albunesTotales.insert(i, album1)
            
              number = len(album1[i])
              print("Cantidad de fotos en el album: ")
              print(number)

              print("Albunes totales: ")
              print(album1[i])
              indice.insert(i,number)

              i+=1
              print("Pase render_template")
            p += 1  
        else:
          print("no hay plantas!")







        if request.method == 'POST': 
        #Solo hay que agregar la planta si no esta agregada
          especie =request.form['especie']
          permiso = request.form['seguridad']
          print("---------------------------------------------------------------POST")
          print(request.form.getlist)
          #si se presiona un album
          
          if 'agregar' in request.form:
            print("post especie ", especie)#tengo que poder diferenciar si se agrega nueva planta o se ve el timelapse
            select = request.form.getlist('Usuario')
            

            print("LISTA DE USUARIOS!!",select)
            print(request.form.get('seguridad'))

            ArrayUserSelect = []
            ArrayUserSelect = request.form.getlist('Usuario')


            if(especie != "" and permiso != '0' and ArrayUserSelect != '0' and isOwner):
              
              if((Planta.check_plantaName(especie, user1) == None)):
                planta = Planta(especie = especie, permiso = permiso)
                user1.addPlanta(planta)

                Exc = ExcGroup(planta = planta)

                for u in ArrayUserSelect:
                  print("USUARIO NUmeRO: ",usuario.get_users()[int(u) - 1])
                  Exc.addUsuario(usuario.get_users()[int(u) - 1])         

                info='Planta agregada!'
              


              else:
                info='Planta already added, retry'
              return render_template('home.html', form=form, info = info, route = name + "/upload", images = albunesTotales, numberImage = len(albunesTotales), indice = indice, j=1, myfunction = increment, especies = list(filter(None, arrayPlanta)), ownname = session [ 'username' ], guestname = name, users = usuario.get_users_name())
            else:
              info='No fue posible agregar planta'
              return render_template('home.html', form=form, info = info, route = name + "/upload", images = albunesTotales, numberImage = len(albunesTotales), indice = indice, j=1,myfunction = increment, especies = list(filter(None, arrayPlanta)), ownname = session [ 'username' ], guestname = name, users = usuario.get_users_name())
          
          else:        
            print("post album")
            for ii in arrayPlanta:
              aux = str(aux2) + '.' + 'x'
              if(request.form.getlist(aux)):
                
                print("PRESIONE IMAGEN ", aux)
                #print("De la especie: ", planta1[aux2].get_PlantaName())
                print("Del usuario: ", name)
                break
              aux2 = aux2 + 1
              aux = 0
              #print("EL valor del contador es: ",aux2)
              #print(albunesTotales[aux2][0])
              #print(albunesTotales[aux2][1])
            aux2 = aux2 - 1
            return render_template('timelapse.html', route = name + "/upload", images = albunesTotales[0][aux2], Informacion =planta1[aux2].get_PlantaName() + '/' + str(aux2)  + '/' + name)




        #Al presionar borrar en una imagen
        if (request.method == 'GET' and request.args.get('borrar') != None and isOwner):
          print("---------------------------------------------------------------GET")
          print("TOMATELA", request.args)
          print("De la especie: ", request.args.get('borrar'))
          print("De la info: ", request.args.get('informacion'))

         
          indicePlanta = int(request.args.get('informacion').split('/')[1])
          especie = request.args.get('informacion').split('/')[0]
          usr = request.args.get('informacion').split('/')[2]
   

          if(request.args.get('borrar') != "NaN"):
            indiceImagen = int(request.args.get('borrar').split('/')[0]) - 1
            imagen = request.args.get('borrar').split('/')[2]
          else:
            indiceImagen = 0
            imagen = ""

          print(user1.planta[int(indicePlanta)])

          Album.delete_image(len(album1[indicePlanta]) - 1, indiceImagen, user1.planta[int(indicePlanta)])

          return render_template('timelapse.html', route = name + "/upload", images = albunesTotales[0][indiceImagen], Informacion =request.args.get('informacion'))
          #return redirect(url_for('borrar', name = usr, especie = indicePlanta, indiceimagen = indiceImagen, indicetotal = len(album1[indicePlanta]) - 1))

        if (request.method == 'GET' and request.args.get('insertar') != None and isOwner): 
          print("VIKINGO",request.args.get('insertar'))
          indicePlanta = int(request.args.get('informacion').split('/')[1])
          especie = request.args.get('informacion').split('/')[0]
          usr = request.args.get('informacion').split('/')[2]
          if(request.args.get('insertar') != "NaN"):
            indiceImagen = int(request.args.get('insertar').split('/')[0]) - 1
            imagen = request.args.get('insertar').split('/')[2]
          else:
            indiceImagen = 0
            imagen = ""
          return redirect(url_for('upload', name = usr, especie = indicePlanta, indiceimagen = indiceImagen, indicetotal = len(album1[indicePlanta]) - 1))
        
        return render_template('home.html', form=form, info = info, route = name + "/upload", images = albunesTotales, numberImage = len(albunesTotales), indice = indice, j=1, myfunction = increment, especies = list(filter(None, arrayPlanta)), ownname = session [ 'username' ], guestname = name, users = usuario.get_users_name())
    return "usuario no encontrado"





#def LoadExcUsers(UsersIndex[], Users[]):
  #UsersIndex[] = request.form.getlist('Usuario')
  #Users[] = usuario.get_users()



def increment():
  return(x)

@app.route("/timelapse/")
def timelapse():
  return render_template("timelapse.html", images = images)




@app.route('/<name>/borrar/<especie>/<indiceimagen>/<indicetotal>', methods=['GET', 'POST'])
def borrar(name, especie, indiceimagen, indicetotal):
  array = []
  info = ''
  form = LoginForm()
  #tengo que pasarle a upload.html el listado de plantas para ese usuario
  #Busco las plantas que tiene el usuario
  i = 0
  user1 = usuario.get_user(name)
  ownname = session [ 'username' ]
  guestname = name
  
  isOwner =  True if (ownname == guestname) else False
  
  
  if user1 and isOwner:
    for user1.get_id in user1.planta:
      planta = Planta.get_Planta(user1.get_id)
      array.insert(i, planta.especie)  
    print(array)

    # Para obtener el id de la planta en la cual cargar imagenes
    if user1.planta:
      print("hay plantas! ")
      #print(user1.planta)
      planta_id_user1 = user1.planta[int(especie)].id            #Planta 0 del usuario 1        
      planta1 = Planta.get_Planta(planta_id_user1)

      #Album(planta = planta1 ,ruta = UPLOAD_FOLDER, imagename = filename, albumname = especieIngresada, timestamp = time.ctime(), imageid = int(indiceimagen))
  return render_template('upload.html', especie = array)




@app.route('/<name>/upload/<especie>/<indiceimagen>/<indicetotal>', methods=['GET', 'POST'])
def upload(name, especie, indiceimagen, indicetotal):
  array = []
  info = ''
  form = LoginForm()
  #tengo que pasarle a upload.html el listado de plantas para ese usuario
  #Busco las plantas que tiene el usuario
  user1 = usuario.get_user(name)
  
  i = 0
  if user1 and user1.get_islogin():
    for user1.get_id in user1.planta:
      planta = Planta.get_Planta(user1.get_id)
      array.insert(i, planta.especie)  
    print(array)

    # Para obtener el id de la planta en la cual cargar imagenes
    if user1.planta:
      print("hay plantas! ")
      #print(user1.planta)
      planta_id_user1 = user1.planta[int(especie)].id            #Planta 0 del usuario 1        
      planta1 = Planta.get_Planta(planta_id_user1)
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

        album = Album(planta = planta1 ,ruta = UPLOAD_FOLDER, imagename = filename, albumname = especieIngresada, timestamp = time.ctime(), imageid = Album.insert(int(indicetotal), int(indiceimagen), planta1))

        return redirect(url_for("profile", name = session [ 'username' ]))
      return "file not allowed"
    return render_template('upload.html', especie = array)
  return render_template('ingresar.html', form = form, info = info)





@app.route("/uploads/<filename>")
def get_file(filename):
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
    
    ExcGroup.dropTable()
    Album.dropTable()
    Planta.dropTable()
    usuario.dropTable()

    # creo las tablas
    usuario.createTable();
    Planta.createTable();
    Album.createTable()
    ExcGroup.createTable();
    
    
    ExcGroup()
    Planta(permiso = 'pu')

    #album = Album(title = "empty") #La tabla usuarios no puede referenciar una tabla albums vacia
    
    app.run(debug=True)