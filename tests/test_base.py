########################################
# create by :ding-PC
# create time :2018-03-07 16:00:00.387201
########################################
import unittest
from app import create_app_swagger, db

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app_swagger('testing').app
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        self.server ='http://localhost:9999/api/v1.0'

    def url_for(self,endpoint):
        return '%s/%s'%(self.server,endpoint)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # def test_hello(self):
    #     response = self.client.get(self.url_for('health'))
    #     self.assertEqual(response.status_code,200)
    #     # self.assertTrue(response.get_data(as_text=True))

    # def test_register(self):
    #     response = self.client.post(url_for('main.register'), data={
    #             'email': '879651072@qq.com',
    #             'name': 'Hyman',
    #             'password1': '123',
    #             'password2': '123'})
    #     self.assertTrue(response.status_code == 302)
        

