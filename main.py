from flask import Flask, request, render_template, redirect
from httplib2 import Http
from urllib.parse import urlencode
import re
import requests

try:
	import json
except ImportError:
	import simplejson as json


AMO_URL = "https://new57dfff397ffd3.amocrm.ru"
AMO_LOGIN = "venya1178@gmail.com"
AMO_KEY = "380d97e3b222b0259695e097db5ee3a2"
app = Flask(__name__)
app.debug = True

@app.route('/')
def home():
	return render_template('home.html')
	
@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
	params = {"USER_LOGIN" : AMO_LOGIN,
						"USER_HASH" : AMO_KEY, 
						"type" : "json",
	}
	if request.method == 'POST':
		name = request.form["name"]
		company_name = request.form["company_name"]
		custom_str = request.form["custom_str"]
		
		s = requests.session()
		try:
			a = s.get("%s/private/api/auth.php" % AMO_URL, params=params)
		except Exception as msg:
			app.logger.error(repr(msg))
			return {"response":{"contacts":[], "error_code":"404","error":"Неизвестная ошибка"}}
		try:
			jj = json.loads(a.text)
		except Exception as msg:
			app.logger.error(repr(msg))
			return {"response":{"contacts":[], "error_code":"401","error":"Ошибка сервера"}}
		
		try:
			id = jj["response"]["accounts"][0]["id"]
		except Exception as msg:
			app.logger.error(repr(msg))
			return {"response":{"contacts":[], "error_code":"401","error":"Ошибка авторизации"}}
		
		c = {"responsible_user_id" : id,
			"name" : name,
			"company_name" : company_name, 
			"custom_fields" : [
				{
					"id" : 45860529,
					"values" : [
						{
						"value" : 55555, 
						}
					]			
				},
			]
		}
		params = {"request" : {
			"contacts" : {
			"add" : [c]
				}
			}
		}
		try:
			r = s.post("%s/private/api/v2/json/contacts/set" % AMO_URL, data=json.dumps(params))
		except Exception as msg:
			app.logger.error(repr(msg))
			return {"response":{"contacts":[], "error_code":"404","error":"Неизвестная ошибка"}}
		return r.text
	else:
		s = requests.session()
		try:
			a = s.get("%s/private/api/auth.php" % AMO_URL, params=params)
			r = s.get("%s/private/api/v2/json/contacts/list" % AMO_URL)
		except Exception as msg:
			app.logger.error(repr(msg))
			return {"response":{"contacts":[], "error_code":"404","error":"Неизвестная ошибка"}}
		app.logger.debug(r.text)
		return r.text

if __name__ == '__main__':
    app.run()
