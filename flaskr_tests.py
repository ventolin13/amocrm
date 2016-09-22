import os
import flaskr
import unittest
import tempfile
import random
import string
import json

class FlaskrTestCase(unittest.TestCase):
	def setUp(self):
		flaskr.app.config['TESTING'] = True
		self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
		self.app = flaskr.app.test_client()

	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(flaskr.app.config['DATABASE'])

	def test_home(self):
		rv = self.app.get('/')
		assert len(rv.data)>550
	
	def test_get_clients(self):
		rv = self.app.get('/contacts')
		assert json.loads(rv.data.decode("utf8"))
		
	def test_sdd_client(self):
		def rndstr(n):
			return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))
		rv =  self.app.post('/contacts', data=dict(
        name="Name%s" % rndstr(10),
        company_name="CN%s" % rndstr(10),
				custom_str=rndstr(10)))
		assert json.loads(rv.data.decode("utf8"))
		
if __name__ == '__main__':
	unittest.main()
