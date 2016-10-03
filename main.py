from flask import Flask, request, render_template, redirect
from urllib.parse import urlencode
import re
import requests
import mongoengine as me

try:
	import simplejson as json
except ImportError:
	import json


AMO_URL = "https://new57dfff397ffd3.amocrm.ru"
AMO_LOGIN = "venya1178@gmail.com"
AMO_KEY = "380d97e3b222b0259695e097db5ee3a2"
CUSTOM_FIELDS = {
	'companies': [
			{
			'enums': {'2478932': 'WORKDD', '2478938': 'HOME', '2478934': 'MOB', '2478936': 'FAX', '2478940': 'OTHER', '2478930': 'WORK'},
			'name': 'Телефон',
			'code': 'PHONE',
			'multiple': 'Y',
			'sort': 4,
			'disabled': '0',
			'type_id': '8',
			'id': '1026278'
		},{
			'enums': {'2478946': 'OTHER', '2478942': 'WORK', '2478944': 'PRIV'},
			'name': 'Email',
			'code': 'EMAIL',
			'multiple': 'Y',
			'sort': 6,
			'disabled': '0',
			'type_id': '8',
			'id': '1026280'
		},{
			'name': 'Web',
			'code': 'WEB',
			'multiple': 'N',
			'sort': 8,
			'disabled': '0',
			'type_id': '7',
			'id': '1026282'
		},{
			'name': 'Адрес',
			'code': 'ADDRESS',
			'multiple': 'N',
			'sort': 12,
			'disabled': '0',
			'type_id': '9',
			'id': '1026286'
		}
	], 
	'contacts': [
			{
			'name': 'Должность',
			'code': 'POSITION',
			'multiple': 'N',
			'sort': 2,
			'disabled': '0',
			'type_id': '1',
			'id': '1026276'
		},{
			'enums':{'2478932': 'WORKDD', '2478938': 'HOME', '2478934': 'MOB', '2478936': 'FAX', '2478940': 'OTHER', '2478930': 'WORK'},
			'name': 'Телефон',
			'code': 'PHONE',
			'multiple': 'Y',
			'sort': 4,
			'disabled': '0',
			'type_id': '8',
			'id': '1026278'
		},{
			'enums': {'2478946': 'OTHER', '2478942': 'WORK', '2478944': 'PRIV'},
			'name': 'Email',
			'code': 'EMAIL',
			'multiple': 'Y',
			'sort': 6,
			'disabled': '0',
			'type_id': '8',
			'id': '1026280'
		},{
			'enums': {'2478950': 'ICQ', '2478954': 'GTALK', '2478952': 'JABBER', '2478956': 'MSN', '2478958': 'OTHER', '2478948': 'SKYPE'},
			'name': 'Мгн. сообщения',
			'code': 'IM',
			'multiple': 'Y',
			'sort': 10,
			'disabled': '0',
			'type_id': '8',
			'id': '1026284'
		}
	]
}

CUSTOM_COMPANIES_IDS = {
	'PHONE' : 1026278, 
	'EMAIL' : 1026280,
	'WEB' : 1026282,
	'ADDRESS' : 1026286,
}

CUSTOM_CONTACTS_IDS = {
	'POSITION' : 1026276,
	'PHONE' : 1026278, 
	'EMAIL' : 1026280, 
	'IM' : 1026284,
}

app = Flask(__name__)

from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)

app.debug = True

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
	app.logger.info(request.__dict__)
	ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
	return json.dumps({'ip': str(ip)}), 200

@app.route('/')
def home():
	app.logger.info(request.__dict__)
	return render_template('home.html', CUSTOM_CONTACTS_IDS=CUSTOM_CONTACTS_IDS)
	
@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
	params = {"USER_LOGIN" : AMO_LOGIN,
						"USER_HASH" : AMO_KEY, 
						"type" : "json",
	}
	if request.method == 'POST':
		name = request.form["name"]
		company_name = request.form["company_name"]
		custom_id = request.form["custom_id"]
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
					"id" : CUSTOM_CONTACTS_IDS[custom_id],
					"values" : [
						{
						"value" : custom_str, 
						"enum" : "OTHER"
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
