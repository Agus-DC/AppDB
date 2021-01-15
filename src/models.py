"""

AUTOR: DECA

FECHA DE CREACIÓN: 15/02/2019

"""

import sqlobject as SO
from flask_login import UserMixin #?
from werkzeug.security import generate_password_hash, check_password_hash


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

    def check_plantaName(especie):
        for a in Planta.selectBy(especie=especie):
            print(a.especie)
            return (a.especie != '')     

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
    #imageid   = SO.StringCol(length=10, varchar=True)
    ruta      = SO.StringCol(length=100,varchar=True)
    timestamp = SO.StringCol(length=50, varchar=True)
    planta    = SO.ForeignKey('Planta', default=None)


    #def asignId(planta):
    #    i = 0
    #    for j in Album.select(Album.q.planta==planta):
    #        j.imageid += 1
    #    return ""    


    def delete_image(inx, planta):
        i = 1
        array = []
        for j in Album.select(Album.q.planta==planta):
            #print(i)
            #print(j)
            #print('\t{}) {}'.format(i, j.imagename))
            #print(planta.especie)
            #print(j.albumname)
            
            if (planta.especie == j.albumname):
                array.insert(i, j.imagename)
                i += 1
            


            #    print("ENTRO")
        print(inx)
        print(array[inx])      
        print("AYYYYYYYYYYYYYYYYYY>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<")

        return ""
        #for planta in self.select(self.planta==planta):



    def get_images(planta):
        i = 1
        array = []
        for j in Album.select(Album.q.planta==planta):
            #print(i)
            #print(j)
            #print('\t{}) {}'.format(i, j.imagename))
            #print(planta.especie)
            #print(j.albumname)
            if (planta.especie == j.albumname):
                array.insert(i, j.imagename)
                i += 1
            #    print("ENTRO")
        #print(array)        
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
