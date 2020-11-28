"""

AUTOR: Juanjo

FECHA DE CREACIÓN: 15/02/2019

"""
import sqlobject as SO
from flask_login import UserMixin #?
from werkzeug.security import generate_password_hash, check_password_hash


class usuario(SO.SQLObject):
    username  = SO.StringCol(length = 25, default=None)
    email     = SO.StringCol(length = 100, default=None)
    passwo  = SO.StringCol(length = 100,  default=None)
    albums = SO.ForeignKey('Album', default=None)

    def set_password(password):
        return generate_password_hash(password)

    def check_password(password_):
        return check_password_hash(password_, password)    

class Album(SO.SQLObject):
    title = SO.StringCol(length=160, varchar=True)
    #usuario = SO.RelatedJoin('usuario')