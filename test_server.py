
from server import app,QuoteForm
import unittest 
from mock import Mock, patch
from server import login
from werkzeug import ImmutableMultiDict
from flask import Flask, request
import pytest
from server import pricing_module,QuoteForm


class TestLoginMethods(unittest.TestCase):
     
     def test_customerorders(self):
        tester=app.test_client(self)
        response = tester.get('/admin_customerorders', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    #login page loads correctly
     def test_customer_orders(self):
        tester=app.test_client(self)
        response = tester.get('/admin_customerorders', follow_redirects=True)
        self.assertTrue(b'deliverydate',  response.data)

    

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
     def test_correct_admin_login(self):
        
        tester=app.test_client(self)

        response = tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'Welcome admin' , response.data)
     
     def test_change_price(self):
        
        tester=app.test_client(self)

        response = tester.post(
            '/changeprice',
            data=dict(price="21"),
            follow_redirects=False
        )
        self.assertIn(b'The price is updated' , response.data)

     def test_incorrect_admin_login(self):
        
        
        tester=app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username="admin", password="avc"),
            follow_redirects=True
        )
        self.assertIn(b'Username not found' , response.data)
         
     def test_incorrect_admin_login2(self):
        
       
        tester=app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username="abg", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'Username not found' , response.data)

      
   
     def test_profile_login(self):
        tester=app.test_client(self)

        response = tester.post(
            '/login',
            data=dict(username="test3", password="test3"),
            follow_redirects=True
        )
        self.assertIn(b'You are now logged in.Please complete your profile' , response.data)
      
     def test_no_login(self):
        tester=app.test_client(self)

        response = tester.post(
            '/login',
            data=dict(username="", password=""),
            follow_redirects=True
        )
        self.assertIn(b'Username not found' , response.data)


     def test_incorrect_login(self):
        
        tester=app.test_client(self)

        response = tester.post(
            '/login',
            data=dict(username="wrong", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Username not found' , response.data)
     def test_incorrect_password_login(self):
        
        tester=app.test_client(self)
         # password1='bun'
        response = tester.post(
            '/login',
            data=dict(username="bun", password="xyz"),
            follow_redirects=True
        )
        self.assertIn(b'Password does not match' , response.data)
     

    # REGISTER
     def test_register(self):
        tester=app.test_client(self)  
        response = tester.get('/register', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    #login page loads correctly
     def test_register_required(self):
        tester=app.test_client(self)

        response = tester.get('/register', follow_redirects=True)
        self.assertTrue(b'Register',  response.data)
#    needed
    #  def test_correct_register(self):
        
    #     tester=app.test_client(self)

    #     response = tester.post(
    #         '/register',
    #         data=dict(username="test3", password="test3",confirm="test3"),
    #         follow_redirects=True
    #     )
    #     self.assertIn(b'You are now registered' , response.data)



     def test_incorrect_password(self):
        
        tester=app.test_client(self)

        response = tester.post(
            '/register',
            data=dict(username="klopn", password="klopn",confirm="kanbv"),
            follow_redirects=True
        )
        self.assertIn(b'Passwords do not match' , response.data)
     def test_incorrect_register(self):
        
        tester=app.test_client(self) 

        response = tester.post(
            '/register',
            data=dict(username="qwe", password="qwe",confirm="qwe"),
            follow_redirects=True
        )
        self.assertIn(b'username already exists' , response.data)

    # PROFILE

     def test_profile(self):
        tester=app.test_client(self)  
        response = tester.get('/profile', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    #login page loads correctly
     def test_profile_required(self):
        tester=app.test_client(self) 
        response = tester.get('/profile', follow_redirects=True)
        self.assertTrue(b'Profile',  response.data)
   
     def test_profile_asser(self):
        tester=app.test_client(self) 
        pid1=2 
        response = tester.get('/profile', content_type='html/text')
        self.assertEqual(2, pid1)

        
    #  def test_data_injection(self):
    #     tester=app.test_client(self)  
    #     response = tester.get('/profile')
        
        
    #     inject_data = {'Fullname':'qwe', 'Address1':'qwe','Address2':'ass','city':'hous','State':'TX', 'zipcode':'77054'}
    #     response = response.post(tester, data=inject_data)
    #     assert 'Your profile is created now' in response.data
    # Ensure that posts show up on the main page
     def test_correct_profile(self):
         tester=app.test_client(self)  
         
         pid=150
         response = tester.post(
             '/profile',
             data=dict(fullname="qwe", address1="qwe",address2='ass',city="hous",state="TX", zipcode="77054"),
             follow_redirects=True        
         )
        #  response = tester.get('/dashboard', content_type='html/text')
         self.assertIn(b'Your profile is created now' , response.data)
     def test_incorrect_profile(self):
        
         tester=app.test_client(self)

         response = tester.post(
             '/profile',
             data=dict(fullname="qwe",city="hous",state="TX", zipcode="77054"),
             follow_redirects=True
         )
         self.assertIn(b'fullname' , response.data)
 # test-quotehistory
     def test_quote_history(self):
        tester=app.test_client(self) 

        response = tester.get('/quote_history', follow_redirects=True)
        self.assertTrue(b'Quote History',  response.data)     
# dashboard
     def test_dashboard(self):
        tester=app.test_client(self)  

        response = tester.get('/dashboard', follow_redirects=True)
        self.assertTrue(b'Dashboard',  response.data)  
# my profile
     def test_myprofile(self):
       
        tester=app.test_client(self)
        response = tester.get('/myprofile', follow_redirects=True)
        self.assertTrue(b'My Profile',  response.data)
# logout
     def test_logout(self):
        tester=app.test_client(self)
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'Login',  response.data)  

# QUOTE
     def test_quote(self):
        tester=app.test_client(self)
        response = tester.get('/quote', content_type='html/text')
        self.assertEqual(response.status_code, 200)
     def test_pricing_module(self):
        assert pricing_module("TX",1,900,6,1) == 0.09
     def test_pricing_module2(self):
        # print(pricing_module("CA",0,2000,5,1))
        assert pricing_module("TX",0,2000,5,1) == 0.08
     
    # def test_pricing_module(self):
    #     tester=app.test_client(self)
    #login page loads correctly
     
    #  def test_quote_two(self):
    #     tester=app.test_client(self)    
    #     response = tester.post(
    #     '/quote',
    #     data=dict(gallons="10",deliverydate="05/12/2019"),
    #     follow_redirects=True
    #     )
    #     self.assertIn(b'Your order is placed' , response.data)
            
    #  def test_sample_form_validate(self):
    #     tester=app.test_client(self)

    #     abc = Flask(__name__)
    #     form = QuoteForm(request.form)
    #     response = tester.post(
    #          '/quote',
    #          data=dict(gallons="10",deliverydate="05/12/2019"),
    #          follow_redirects=True
    #             )
    #     if request.form['submit button']=='place order':
    #         self.assertIn(b'Your order is placed' , response.data)

    #     # with app.test_request_context('/quote'):
    #     #     request.form = ImmutableMultiDict([('btn', 'place order')])
    #         # response = tester.post(
    #         #  '/quote',
    #         #  data=dict(gallons="10",deliverydate="05/12/2019"),
    #         #  follow_redirects=True
    #         #     )
    #         # self.assertIn(b'Your order is placed' , response.data) # Prints 'Saving...'
    #         request.form = ImmutableMultiDict([('btn', 'get price')])
    #         response = tester.post(
    #          '/quote',
    #          data=dict(gallons="10",deliverydate="05/12/2019"),
    #          follow_redirects=True
    #             )
    #         self.assertIn(b'Price per gallon' , response.data) # Prints 'Updating

     def test_quote_required(self):
        tester=app.test_client(self)  
        response = tester.get('/quote', follow_redirects=True)
        self.assertTrue(b'Quote',  response.data)

     def test_address_quote(self):
        
         tester=app.test_client(self)

         response = tester.post(
             '/quote',
             data=dict(gallons="10",deliverydate="05/12/2019"),
             follow_redirects=True
         )
         self.assertIn(b'Price per gallon' , response.data)
    
     def test_price_quote(self):
        
         tester=app.test_client(self)

         response = tester.post(
             '/quote',
             data=dict(gallons="10",deliverydate="04/10/2019"),
             follow_redirects=False
         )
         self.assertIn(b'Quote' , response.data) 
         
     def test_correct_quote(self):
        
        tester=app.test_client(self) 

        response = tester.post(
            '/quote',
            data=dict(gallons="30",deliverydate="05/12/2019"),
            follow_redirects=True
        )
        self.assertIn(b'Quote' , response.data)
     def test_incorrect_quote(self):
        
        tester=app.test_client(self) 

        response = tester.post(
            '/quote',
            data=dict(gallons="",deliverydate="05/12/2019"),
            follow_redirects=True
        )
        self.assertIn(b'Quote' , response.data)
     def test_correct_login(self):
        tester=app.test_client(self)

        response = tester.post(
            '/login',
            data=dict(username="bun", password="bun"),
            follow_redirects=True
        )
        self.assertIn(b'You are now logged in' , response.data)
   

        
    
if __name__ == '__main__':
    app.secret_key='secret123'
    unittest.main()