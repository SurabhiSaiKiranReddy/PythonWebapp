
from datetime import datetime  
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators,SelectField,DecimalField,IntegerField
from passlib.hash import sha256_crypt
from functools import wraps
from wtforms.fields.html5 import DateField
from flask_table import Table, Col

app = Flask(__name__)
activeid=0
# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'webapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL

mysql = MySQL(app)
deladdress=''
price=''
totalamount=''

class ChangePrice(Form):
  
    price = DecimalField('price',places=2)
  
    

@app.route('/changeprice', methods=['GET', 'POST'])
def changeprice():
    form = ChangePrice(request.form)
    if request.method == 'POST' and form.validate():
       
        price = form.price.data
       
        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        pri=float(price)
        cur.execute("update price set price=%s where price_id=%s",(pri,'1'))
        mysql.connection.commit()
        # Commit to DB
        # Close connection
        cur.close()



        flash('The price is updated', 'success')

        # return render_template('register.html')
        
    return render_template('price.html', form=form)


class ProfileForm(Form):
  
    fullname = StringField('Fullname', [validators.DataRequired(),validators.Length(max=50)])
    address1 = TextAreaField("Address1",[validators.DataRequired(),validators.Length(max=100)])
    address2 = TextAreaField("Address2",[validators.Length(max=100)])
    city = StringField('city', [validators.DataRequired(),validators.Length(max=100)])
    state = SelectField(u'State', choices = [('AL','AL'),('AK','AK'),('AZ','AZ'),('AR','AR'),('CA','CA'),('CO','CO'),('CT','CT'),('DE','DE'),('DC','DC'),('FL','FL'),('GA','GA'),('HI','HI'),('ID','ID'),('IL','IL'),('IN','IN'),('IA','IA'),('KS','KS'),('KY','KY'),('LA','LA'),('ME','ME'),('MD','MD'),('MA','MA'),('MI','MI'),('MN','MN'),('MS','MS'),('MO','MO'),('MT','MT'),('NE','NE'),('NV','NV'),('NH','NH'),('NJ','NJ'),('NM','NM'),('NY','NY'),('NC','NC'),('ND','ND'),('OH','OH'),('OK','OK'),('OR','OR'),('PA','PA'),('RI','RI'),('SC','SC'),('SD','SD'),('TN','TN'),('TX','TX'),('UT','UT'),('VT','VT'),('VA','VA'),('WA','WA'),('WV','WV'),('WI','WI'),('WY','WY'),])
    zipcode = IntegerField('zipcode', [validators.NumberRange(min=10000,max=999999999,message="zipcode should be 5 to 9 characters")])

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ProfileForm(request.form)
    if request.method == 'POST' and form.validate():
        global activeid
        pid=activeid
        print(pid)
        fullname = form.fullname.data
        
        address1= form.address1.data
        address2= form.address2.data
        city= form.city.data
        state= form.state.data
        zipcode= form.zipcode.data
        # Create cursor
        cur = mysql.connection.cursor()
        # Execute query
        cur.execute("INSERT INTO profile(pid,fullname, address1,address2,city,state,zipcode) VALUES(%s,%s, %s,%s,%s,%s,%s)", (pid,fullname,address1,address2,city,state,zipcode))
        # cur.execute("select * from register where id=%s",activeid)
        no="n"
        cur.execute("UPDATE register set isfirstlogin = %s WHERE id=%s",(no,pid))
        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()

        flash('Your profile is created now ', 'success')

        # return render_template('register.html')
        return redirect(url_for('dashboard'))
    return render_template('profile.html', form=form)

class QuoteForm(Form):
  
    gallons = IntegerField('gallons', [validators.NumberRange(min=1,max=9999999999999,message="Enter a number")])
    deliverydate = DateField('deliverydate', format='%Y-%m-%d')
   
   

@app.route('/quote', methods=['GET', 'POST'])
def quote():
    global activeid
    global deladdress
    global price
    global totalamount
    form = QuoteForm(request.form)
    if request.method == 'POST' and form.validate() and request.form['submit button']=='place order':
        cur = mysql.connection.cursor()
        gallons = form.gallons.data
        
        quoteid=activeid
        deladdress=''
        cur.execute("SELECT * FROM profile WHERE pid = %s", [activeid])
        data = cur.fetchone()
        add1 = data['address1']
        add2=data['address2']
        deladdress= add1+add2        
        
        deliverydate= form.deliverydate.data        
        # Create cursor
        # Execute query
        cur.execute("SELECT state FROM profile WHERE pid = %s", [activeid])
        loc = cur.fetchone() 
        his=cur.execute("SELECT * FROM quote WHERE quoteid = %s", [activeid]) 
        cur.execute("SELECT price FROM price where price_id=%s",('1'))
        current= cur.fetchone()
        current_price=current['price']
        #print(current_price)         
        price=current_price+pricing_module(loc['state'],his,gallons,deliverydate.month,current_price)
        totalamount=float(gallons)*price   

        cur.execute("INSERT INTO quote( quoteid,gallons, deliverydate,price,totalamount) VALUES(%s, %s,%s,%s,%s)", (quoteid,gallons,deliverydate,price,totalamount))
        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        flash('Your order is placed ', 'success')

        # return render_template('register.html')
        # form.gallons.data=''
        # form.deliverydate.data=''
        
        return render_template('quote.html', form=form,result=deladdress)
    
    if request.method == 'POST' and form.validate() and request.form['submit button']=='get price':
        cur = mysql.connection.cursor()
        gallons = form.gallons.data
        deliverydate= form.deliverydate.data        
        quoteid=activeid
        deladdress=''
        price=''
        cur.execute("SELECT * FROM profile WHERE pid = %s", [activeid])
        data = cur.fetchone()
        add1 = data['address1']
        add2=data['address2']
        cur.execute("SELECT state FROM profile WHERE pid = %s", [activeid])
        loc = cur.fetchone() 
        cur.execute("SELECT price FROM price where price_id=%s",('1'))
        current= cur.fetchone()
        current_price=current['price']       
        # if loc['state']=="texas":
        #     location=0.02
        # else:
        #     location=0.04
        # print(location)
        his=cur.execute("SELECT * FROM quote WHERE quoteid = %s", [activeid])        
        # if his>0:
        #     rate_history_factor=0.01
        # else:
        #     rate_history_factor=0
        # print(rate_history_factor)
        # if gallons>1000:
        #     gallons_requested_factor=0.02
        # else:
        #     gallons_requested_factor=0.03
        # print(deliverydate.month)
        # if (deliverydate.month)==6 or (deliverydate.month)==7 or (deliverydate.month)==8:
        #     rate_fluctuation=0.04
        # else:
        #     rate_fluctuation=0.03
        # print(rate_fluctuation)
        # print(deliverydate.month)
        deladdress= add1+add2
        cur.execute("SELECT price FROM price where price_id=%s",('1'))
        current= cur.fetchone()
        current_price=current['price']
        #print(current_price)       
        # current_price=1.50
        #margin=current_price*(location-rate_history_factor+gallons_requested_factor+0.01+rate_fluctuation)
        price=current_price+pricing_module(loc['state'],his,gallons,deliverydate.month,current_price)
        totalamount=float(gallons)*price               
        # Create cursor
        # Execute query
        # Commit to DB
        
        mysql.connection.commit()
        # Close connection
        cur.close()
        # return render_template('register.html')       
        return render_template('quote.html', form=form,result=deladdress,price=price,amount=totalamount)
    return render_template('quote.html',form=form,result=deladdress)

def pricing_module(location,history,gallons,deliverymonth,current_price):
    if location=="TX":
        loc=0.02
    else:
        loc=0.04
    if history>0:
        rate_history_factor=0.01
    else:
        rate_history_factor=0
    if gallons>1000:
        gallons_requested_factor=0.02
    else:
        gallons_requested_factor=0.03
    if (deliverymonth)==6 or (deliverymonth)==7 or (deliverymonth)==8:
        rate_fluctuation=0.04
    else:
        rate_fluctuation=0.03
    margin=current_price*(loc-rate_history_factor+gallons_requested_factor+0.1+rate_fluctuation)
    return margin

    # cur = mysql.connection.cursor()
    # cur.execute("select * from profile where pid=%s",[activeid])
    # data = cur.fetchone()
    #     # address1= data['address1']
    #     # address2=data['address2']
    # cur.close()
    #     # deliveryaddress=address1+address2
    #     # print(deli)
    # return render_template('quote.html', result=data)
# Register Form Class
class RegisterForm(Form):
  
    username = StringField('Username', [validators.Length(min=1, max=50)])
   
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():      
        username = form.username.data
        password = form.password.data
        # Create cursor
        cur = mysql.connection.cursor()
        # Execute query
        try:
            cur.execute("INSERT INTO register(username, password, isfirstlogin) VALUES(%s, %s,%s)", (username, password,'y'))
            mysql.connection.commit()
        except:
            error = 'username already exists'
            return render_template('register.html', error=error,form=form)
        # Commit to DB
        # Close connection
        cur.close()
        flash('You are now registered and can log in', 'success')
        # return render_template('register.html')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)



@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# User login
@app.route('/', methods=['GET', 'POST'])
def main1():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    global activeid
    session['logged_in'] = False
    session['admin_logged_in']=False
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']
        cur = mysql.connection.cursor()      
        if username=="admin" and password_candidate=="admin":
            session['admin_logged_in'] = True
            session['username'] = username
            session['logged_in'] = False
            return redirect(url_for('dashboard'))
        # Create cursor
        # Get user by username
        result = cur.execute("SELECT * FROM register WHERE username = %s", [username])
        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']
            firstlogin=data['isfirstlogin']
            # Compare Passwords
            if password_candidate==password:
                # Passed
                session['logged_in'] = True
                session['username'] = username
                if firstlogin=="y":
                    no="y"
                    cur.execute("UPDATE register set isfirstlogin = %s WHERE username=%s",(no,username))
                    mysql.connection.commit()
                    cur.execute("SELECT id FROM register WHERE username = %s", [username])
                    userid=cur.fetchone()
                    activeid=userid['id']
                    cur.close()
                    flash('You are now logged in.Please complete your profile', 'success')
                    return redirect(url_for('profile'))
                else:
                    userid = cur.execute("SELECT id FROM register WHERE username = %s", [username])
                    userid=cur.fetchone()
                    activeid=userid['id']
                    flash('You are now logged in', 'success')
                    return redirect(url_for('dashboard'))
            else:
                error = 'Password does not match'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/quote_history', methods=['GET', 'POST'])
def quote_history():   
    global activeid
        # Get Form Fields
    cur = mysql.connection.cursor()
    val=1
    x=cur.execute("SELECT deliverydate,gallons,price,totalamount FROM quote where quoteid=%s",[activeid])
    data = cur.fetchall()
    if(x==0):
        return render_template("quotehistory.html",val=0)
    mysql.connection.commit()
    cur.close()    
    
   
  

    return render_template("quotehistory.html", data=data)
 # Check if user logged in
def is_admin_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            return f(*args, **kwargs)
        # else:
        #     flash('Not the admin, Please login', 'danger')
        #     return redirect(url_for('login'))
    return wrap
           

# Check if user logged in




def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap




@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))  

@app.route('/myprofile', methods=['GET', 'POST'])
def myprofile():
   
        # Get Form Fields       
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM profile where pid=%s",[activeid])
    data = cur.fetchall()
    # print(data)
    mysql.connection.commit()
    cur.close()    
    
   
  

    return render_template("myprofile.html", data=data)
           


#admin

@app.route('/admin_customerorders', methods=['GET', 'POST'])
def admincustomerorders():

        # Get Form Fields
       
    cur = mysql.connection.cursor()
    cur.execute("SELECT  register.username,quote.deliverydate, quote.gallons,quote.price,quote.totalamount FROM quote INNER JOIN register ON quote.quoteid=register.id")
    data = cur.fetchall()
    mysql.connection.commit()
    cur.close()    
    
   
  

    return render_template("admincustomerorders.html", data=data)


if __name__ == '__main__':

    app.secret_key='secret123'
    # app.run(threaded=True)
    app.run(host='0.0.0.0',posrt=80,threaded=True)
