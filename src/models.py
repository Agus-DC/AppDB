"""

AUTOR: DECA

FECHA DE CREACIÓN: 15/02/2019

"""

import sqlobject as SO
from flask_login import UserMixin #?
from werkzeug.security import generate_password_hash, check_password_hash
import json




class PlantPlot(SO.SQLObject):

    temperature = SO.StringCol(length = 25, default=None)
    humidity    = SO.StringCol(length = 25, default=None)
    ph          = SO.StringCol(length = 25, default=None)
    elect       = SO.StringCol(length = 25, default=None)
    lumens      = SO.StringCol(length = 25, default=None)
    growthStage = SO.StringCol(length = 25, default=None)
    username    = SO.StringCol(length = 25, default=None)
    plantname   = SO.StringCol(length = 25, default=None)
    plant       = SO.ForeignKey('Planta', default=None)

    def get_data(plant):
        data = []
        index = 0
        for j in PlantPlot.select(PlantPlot.q.plant==plant):
            data.insert(index, j)
            index+=1
        return data


        #print(users)    


class usuario(SO.SQLObject):

    username   = SO.StringCol(length = 25, default=None)
    email      = SO.StringCol(length = 100, default=None)
    passwo     = SO.StringCol(length = 100,  default=None)
    planta     = SO.RelatedJoin('Planta')
    status     = False

    def get_id(self):
        return (self.id)

    def login(self, status):
        self.status = status
        return True

    def get_islogin(self):
        return self.status

    def getname_userlogin(self):
        if (self.satus == True):
            return self.username
        else:
            return None   

    def get_username(self):
        return self.username

    def set_password(password):
        return generate_password_hash(password)

    def check_password(self, password_):
        return check_password_hash(self.passwo, password_)    

    def get_user(name):
        for a in usuario.selectBy(username=name):
            return a

    def get_users():
        users = []
        index = 0
        for a in usuario.select():
            users.insert(index, a)
            index+=1
        #print(users)    
        return users

    def get_users_name():
        users = []
        index = 0
        for a in usuario.select():
            users.insert(index, a.username)
            index+=1
        #print(users)    
        return users

    def check_user(name):
        for a in usuario.selectBy(username=name):
            print(a.username)
            return (a.username != '')
            
    def check_email(email):
        for a in usuario.selectBy(email=email):
            print(a.email)
            return (a.email != '')            



class Planta(SO.SQLObject):
    permiso    = SO.StringCol(length=10, varchar=True)
    especie    = SO.StringCol(length=25, default=None)
    usuario    = SO.RelatedJoin('usuario')

    def check_plantaName(especie, usr):
        for a in Planta.selectBy(especie=especie):
            if(a.usuario[0] == usr):
                print(a.especie)
                return ''
        return None   

    def get_plantaByNameAndUser(especie, usr):
        for a in Planta.selectBy(especie=especie):
            #print("ANTES DE ENCONTRE",a.usuario[0].username)
            if(a.usuario[0].username == usr):
                #print("ENCONTRE",a)
                return a
        return None   


    def get_id(self):
        return (self.id)

    def get_Planta(id):
        for a in Planta.selectBy(id=id):
            print ("[/Models]", a.especie)
            return a

    def get_PlantaName(self):
        return self.especie    

    def albumcheck(self):
        return self.album

    #busco el numero de plantas de cada usuario entrando por usuario
    def listadoPlantas(self, usuario):
        for usuario in self.select(orderBy=self.id):
            return print(self.especie + ':')


class Album(SO.SQLObject):
    albumname = SO.StringCol(length=50, varchar=True)
    imagename = SO.StringCol(length=50, varchar=True)
    imageid   = SO.IntCol()
    ruta      = SO.StringCol(length=100,varchar=True)
    timestamp = SO.StringCol(length=50, varchar=True)
    planta    = SO.ForeignKey('Planta', default=None)

    def insert(indicetotal, indiceImagen, planta):
        vector = []
        flag = 0
        inx = 0
        #print("----------------INSERT------------")
        if (indiceImagen >= 1):    
            for j in Album.select(orderBy = Album.q.imageid):
                if(Album.q.planta==planta):
                    if(flag == 1):
                        j.imageid += 1
                    if(j.imageid == (indiceImagen)):
                        if(indiceImagen != indicetotal):
                            j.imageid += 1
                        else:
                            indiceImagen+=1
                        flag = 1
        else:
            return indicetotal + 1      
        return (indiceImagen)    

    def asignId(planta):
        i = 0
        aux = 0
        print("[/asignId]")

        for j in Album.select(Album.q.planta==planta):
            j.imageid += 1
            print("[/Album]")
            print (j.imageid) 
            aux = j.imageid
        return aux


    def delete_image(indicetotal, indiceImagen, planta):
        vector = []
        flag = 0
        idaux = 0
        inx = 0
        print("----------------borrar imagen------------")

        for j in Album.select(orderBy = Album.q.imageid):
            if(j.q.planta==planta and j.albumname==planta.especie):
                if(idaux):
                    j.imageid -= 1
                elif(j.imageid == (indiceImagen)):
                    print("indiceImagen, indicetotal, j.imageid: ",indiceImagen, indicetotal, j.imageid)
                    if(indiceImagen == 0 and indicetotal >= 1 and j.imageid == 0): #condicion de ultima imagen, solo puedo borrarla cuando sea la ultima
                        return (indiceImagen)    
                    else:
                       idaux = j.imageid
                       j.delete(j.id) 
        return (indiceImagen)    



    def get_images(planta):
        i = 1
        array = []


        for j in Album.select(orderBy = Album.q.imageid):
            print(j.planta.usuario[0])
            print(planta.usuario[0])
            if(Album.q.planta==planta and j.albumname == planta.especie and j.planta.usuario[0] == planta.usuario[0]):
                array.insert(i, j.imagename)
                i += 1
        print(array)        
        return array



    def get_imageCount(self, planta):
        for planta in self.select(orderBy=self.q.albumname):
   
            print("Estoy por imprimir planta")
            print(planta)
            
            print("Estoy por imprimir planta self")
            print(self.planta)
            
            for planta in self.select(orderBy=self.q.albumname):
                print("Estoy por imprimir cantidad")
                return ("{}".format(self.select(SO.AND(self.q.planta == planta, self.planta.especie == 'tomate')).count()))
    





    def Album():
        return Album



class ExcGroup(SO.SQLObject):
    imagenesUnlock      = SO.StringCol(length = 5, default=None)
    condicionessUnlock  = SO.StringCol(length = 5, default=None)
    planta              = SO.ForeignKey('Planta', default=None) #va a ser el numero de planta, en default habia un 1
    usuario             = SO.RelatedJoin('usuario')

    def accesible(planta, user):
        flag = False
     
        for j in ExcGroup.select():
            #print("Encontre oro puro1 (*) ",j.usuario)
            if ((planta.permiso == '1') or (j.planta == planta and j.usuario[0] == user and planta.permiso == '3')):
                print("Encontre oro puro2 (*) ",j.usuario)
                flag = True
        return flag    