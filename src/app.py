#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlobject as SO
from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow

#se importan librerias para pagina web
from flask import render_template, redirect, url_for, session
#from flask_mysqldb import MySQL
import bcrypt 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://invitado:invitado@localhost/app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

ma = Marshmallow(app)

class PlantPlot(SO.SQLObject):
    growthStage = SO.StringCol(length = 25, default=None)
    temperature = SO.StringCol(length = 25, default=None)
    humidity    = SO.StringCol(length = 25, default=None)
    ph          = SO.StringCol(length = 25, default=None)
    elect       = SO.StringCol(length = 25, default=None)
    lumens      = SO.StringCol(length = 25, default=None)
    username    = SO.StringCol(length = 25, default=None)
#    def __init__(self, title, description):
#        self.title = title
#        self.description = description


class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'growthStage', 'temperature', 'humidity','ph','elect','lumens', 'username')

task_schema = TaskSchema()



@app.route('/tasks', methods=['Post'])
def create_PlantPlot():
  growthStage = request.json['growthStage']
  temperature = request.json['temperature']
  humidity    = request.json['humidity']
  ph          = request.json['ph']
  elect       = request.json['elect']
  lumens      = request.json['lumens']
  username    = request.json['username']

  new_PlantPlot= PlantPlot(growthStage = growthStage, 
          temperature = temperature,
          humidity = humidity,
          ph = ph,
          elect = elect,
          lumens = lumens,
          username = username)

  return task_schema.jsonify(new_PlantPlot)



@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to my API'})



if __name__ == "__main__":

    connection = SO.connectionForURI("mysql://invitado:invitado@localhost/app")
    SO.sqlhub.processConnection = connection

    PlantPlot.createTable();

    app.run(debug=True)