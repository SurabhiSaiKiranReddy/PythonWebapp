
from test import app
import unittest 
from mock import Mock, patch
from test import login



class TestLoginMethods(unittest.TestCase):

     def setUp(self):
        tester=app.test_client(self)



     def test_customerorders(self):
      
        response = tester.get('/admin_customerorders', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    #login page loads correctly
     def test_customer_orders(self):
        response = tester.get('/admin_customerorders', follow_redirects=True)
        self.assertTrue(b'deliverydate',  response.data)

    
    










    # flask setup correctly
     def test_login(self):
      
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    #login page loads correctly
     def test_login_required(self):
       

        response = tester.get('/login', follow_redirects=True)
        self.assertTrue(b'Login',  response.data)

    
    # Ensure that posts show up on the main page
     def test_correct_admin_login(self):
        
       

        response = tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'Welcome admin' , response.data)
    
     def test_incorrect_admin_login(self):
        
        

        response = tester.post(
            '/login',
            data=dict(username="admin", password="avc"),
            follow_redirects=True
        )
        self.assertIn(b'Username not found' , response.data)
         
     def test_incorrect_admin_login2(self):
        
       

        response = tester.post(
            '/login',
            data=dict(username="abg", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'Username not found' , response.data)
     def test_correct_login(self):
      

        response = tester.post(
            '/login',
            data=dict(username="qwe", password="qwe"),
            follow_redirects=True
        )
        self.assertIn(b'You are now logged in' , response.data)

     def test_incorrect_login(self):
        
      

        response = tester.post(
            '/login',
            data=dict(username="wrong", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Username not found' , response.data)

    #  def test_user_exists_indb(self):
        
    #     user = Mock()

    #     # now set the attributes for the `user` object
    #     user.username = "qwe"
    #     user.password = "qwe"
       
    #     # now we pass the `user` object check for expected result `True`
    #     result = login()
    #     self.assertTrue(result)

    
    #  def not_a_db_hit():
    #     print 'I did not hit the db'
    #  @patch('test.connect_db')
    #  def test_root(self, mock_connect_db):
    #     mock_connect_db.side_effect = not_a_db_hit
    #     response = app.test_client().get('/')
    #     self.assertEqual(response.status_code, 200)

    # REGISTER
     def test_register(self):
        
        response = tester.get('/register', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    #login page loads correctly
     def test_register_required(self):
       

        response = tester.get('/register', follow_redirects=True)
        self.assertTrue(b'Register',  response.data)
   
     def test_correct_register(self):
        
        tester=app.test_client(self)

        response = tester.post(
            '/register',
            data=dict(username="pala1asd", password="pala1sd",confirm="pala1sd"),
            follow_redirects=True
        )
        self.assertIn(b'You are now registered and can log in' , response.data)

     def test_incorrect_register(self):
        
       

        response = tester.post(
            '/register',
            data=dict(username="qwe", password="qwe",confirm="qwe"),
            follow_redirects=True
        )
        self.assertIn(b'username already exists' , response.data)

    # PROFILE

     def test_profile(self):
        
        response = tester.get('/profile', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    #login page loads correctly
     def test_profile_required(self):
        
        response = tester.get('/profile', follow_redirects=True)
        self.assertTrue(b'Profile',  response.data)

    
    # Ensure that posts show up on the main page
     def test_correct_profile(self):
        
         

         response = tester.post(
             '/profile',
             data=dict(fullname="qwe", address1="qwe",address2='',city="hous",state="TX", zipcode="77054"),
             follow_redirects=True
         )
         self.assertIn(b'fullname' , response.data)
    #  def test_correct_inprofile(self):
        
    #      tester=app.test_client(self)

    #      response = tester.post(
    #          '/profile',
    #          data=dict(fullname="qwe", address1="",address2='',city="hous",state="TX", zipcode="77054"),
    #          follow_redirects=True
    #      )
    #      self.assertIn(b'fullname' , response.data)
 # test-quotehistory
     def test_quote_history(self):
       

        response = tester.get('/quote_history', follow_redirects=True)
        self.assertTrue(b'Quote History',  response.data)     
# dashboard
     def test_dashboard(self):
        

        response = tester.get('/dashboard', follow_redirects=True)
        self.assertTrue(b'Dashboard',  response.data)  
# my profile
     def test_myprofile(self):
       

        response = tester.get('/myprofile', follow_redirects=True)
        self.assertTrue(b'My Profile',  response.data)
# logout
     def test_logout(self):

        response = tester.get('/logout', follow_redirects=True)
        self.assertTrue(b'Login',  response.data)  

# QUOTE
     def test_quote(self):
      
        response = tester.get('/quote', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    #login page loads correctly
     def test_quote_required(self):
        
        response = tester.get('/quote', follow_redirects=True)
        self.assertTrue(b'Quote',  response.data)
    

     def test_correct_quote(self):
        
       

        response = tester.post(
            '/quote',
            data=dict(gallons="30",deliverydate="05/12/2019"),
            follow_redirects=True
        )
        self.assertIn(b'Quote' , response.data)

    
     def tearDown(self):
        
    
if __name__ == '__main__':
    app.secret_key='secret123'
    unittest.main()