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
    passwo     = SO.StringCol(length = 15,  default=None)
    albums     = SO.RelatedJoin('Album')
    status     = False

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
            #<span style="color: red;">{{ error }}</span>

            #Si el usuario coincide tengo que ingresar, sino tengo que mostrar datos erroneos y reintentar
        


        #print("{}: {}".format(usuario.username, usuario.select(usuario.q.username==name)))
        #nombre = usuario.select(usuario.q.username==name)
        #print(usuario.username)
        #for name in usuario.select(orderBy=usuario.q.username, limit=10):
        #    print(usuario.username)
#            i = 1
#            for album in Album.select(Album.q.artist == artist):
#                print('\t{}) {}'.format(i, album.title))
#                i += 1
#            print()

class Album(SO.SQLObject):
    title = SO.StringCol(length=160, varchar=True)
    usuario = SO.RelatedJoin('usuario')