
from test import app
import unittest


class TestLoginMethods(unittest.TestCase):
    # flask setup correctly
     def test_login(self):
        tester=app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    #login page loads correctly
     def test_login_required(self):
        tester=app.test_client(self)

        response = tester.get('/login', follow_redirects=True)
        self.assertTrue(b'Login',  response.data)

    
    # Ensure that posts show up on the main page
     def test_correct_login(self):
        
        tester=app.test_client(self)

        response = tester.post(
            '/login',
            data=dict(username="qwe", password="qwe"),
            follow_redirects=True
        )
        self.assertIn(b'You are now logged in' , response.data)

     def test_incorrect_login(self):
        
        tester=app.test_client(self)

        response = tester.post(
            '/login',
            data=dict(username="wrong", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Username not found' , response.data)



if __name__ == '__main__':
    app.secret_key='secret123'
    unittest.main()