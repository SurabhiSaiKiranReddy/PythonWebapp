
from test import app
import unittest



class TestLoginMethods(unittest.TestCase):
    # flask setup correctly
     def test_register(self):
        tester=app.test_client(self)
        response = tester.get('/register', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    #login page loads correctly
     def test_register_required(self):
        tester=app.test_client(self)

        response = tester.get('/register', follow_redirects=True)
        self.assertTrue(b'Register',  response.data)



if __name__ == '__main__':
    app.secret_key='secret123'
    unittest.main()