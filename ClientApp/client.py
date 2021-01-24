
import requests
import time
from flask import Flask, jsonify, json
from random import randint

app = Flask(__name__)

_users = ['Juan', 'Pepe', 'Carla', 'Valeria']
_growthStage = ['Germinacion', 'Crecimiento', 'Floracion']





with app.app_context():
	
	url = "http://127.0.0.1:5000/tasks"

	i = 0

	while True:
		#value = randint(0, 10)
		#print(value)	
		
		userslen = randint(0, len(_users) - 1)
		growthStagelen = randint(0, len(_growthStage) - 1)
		_temperature = str(randint(20, 35))
		_humidity = str(randint(50,99))
		_ph = str(randint(0,14))
		_elect = str(randint(0,3))
		_lumens = str(randint(0,1000))

		payload = {
		    "growthStage" : _growthStage[growthStagelen], 
          	"temperature" : _temperature,
          	"humidity" : _humidity,
          	"ph" : _ph,
          	"elect" : _elect,
          	"lumens" : _lumens,
          	"username": _users[userslen]
		}


		print("Esto es un descontrol1",payload)
		print("Esto es un descontrol2",json.dumps(payload))

		headers = {'Content-Type': 'application/json'}

		response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

		print(response.text)

		time.sleep(1)

