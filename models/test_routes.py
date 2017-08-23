from flask.testing import FlaskClient # test_client
from application.application import app
import unittest

#paths = ['/register', '/shoppinglists', '/view_list/2', '/logout']
#for path in paths

class RouteTester(unittest.TestCase): 
    
    def setUp(self):
        self.client = FlaskClient(app)

    def test_UI_register_url(self):
        response = self.client.get('/register')
        self.assertEquals(response[1], '200 OK')

    def test_UI_logout_url(self):
        response = self.client.get('/logout')
        self.assertEquals(response[1], '302 FOUND') #returns a redirect to login page

    def test_UI_view_lists_url(self):
        response = self.client.get('/register')
        self.assertEquals(response[1], '200 OK')

    def test_UI_login_url(self):
        response = self.client.get('/')
        self.assertEquals(response[1], '200 OK')

    def test_UI_login_url_success(self):
        response = self.client.post('/')
        print(response)
        self.assertEquals(response[1], '400 BAD REQUEST') #coz malformed/None form is sent,

    ''' requires db to search from
    def test_for_view_single_list_url(self):
        response = self.client.get('/view_list/2')
        print(response[1])
        self.assertEquals(response.status_code[0], 200)
    '''

#==================================================== API Routes ================================================#

    def test_API_get_shopping_lists(self):
        response = self.client.get('/lists')
        self.assertEquals(response[1], '404 NOT FOUND')

    def test_API_get_single_shopping_list_(self):
        response = self.client.get('/lists/9')
        self.assertEquals(response[1], '404 NOT FOUND') #coz no db connection to select list from

    def test_API_post_single_shopping_list(self):
        response = self.client.post('/lists')
        self.assertEquals(response[1], '404 NOT FOUND')

    def test_API_update_shopping_lists(self):
        response = self.client.put('/lists/8')
        self.assertEquals(response[1], '404 NOT FOUND') # naturally

    

