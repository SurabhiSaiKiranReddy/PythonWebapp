
  
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

@app.route('/index')
def index():
    return render_template('index.html')

class ProfileForm(Form):
  
    fullname = StringField('Fullname', [validators.DataRequired(),validators.Length(max=50)])
    address1 = TextAreaField("Address1",[validators.DataRequired(),validators.Length(max=100)])
    address2 = TextAreaField("Address2",[validators.Length(max=100)])
    city = StringField('city', [validators.DataRequired(),validators.Length(max=100)])
    state = SelectField('State', choices = [('texas', 'TX'), 
      ('california', 'CA')])
    zipcode = StringField('zipcode', [validators.DataRequired(),validators.Length(min=5,max=9)])

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

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('Your profile is created now ', 'success')

        # return render_template('register.html')
        return redirect(url_for('dashboard'))
    return render_template('profile.html', form=form)

class QuoteForm(Form):
  
    gallons = StringField('gallons', [validators.DataRequired(),validators.Length(max=50)])
  
    deliverydate = DateField('deliverydate', format='%Y-%m-%d')
    # price= DecimalField('price', [validators.DataRequired()])
    # totalamount= DecimalField('amount', [validators.DataRequired()])
   

@app.route('/quote', methods=['GET', 'POST'])
def quote():
    global activeid
    form = QuoteForm(request.form)
    if request.method == 'POST' and form.validate():
        cur = mysql.connection.cursor()
        gallons = form.gallons.data
        
        quoteid=activeid
        global deladdress
        cur.execute("SELECT * FROM profile WHERE pid = %s", [activeid])
        data = cur.fetchone()
        add1 = data['address1']
        add2=data['address2']
        deladdress= add1+add2
        deliverydate= form.deliverydate.data
        # price= form.price.data
        # totalamount= form.totalamount.data
        
        # Create cursor
  

        # Execute query
        cur.execute("INSERT INTO quote( quoteid,gallons, deliverydate,price,totalamount) VALUES(%s, %s,%s,%s,%s)", (quoteid,gallons,deliverydate,'34','34'))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('Your order is placed ', 'success')

        # return render_template('register.html')
        redirect(url_for('dashboard'))
    return render_template('quote.html', form=form,result=deladdress)

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
@app.route('/login', methods=['GET', 'POST'])
def login():
    global activeid
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']
        cur = mysql.connection.cursor()
        
      
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
                    no="n"
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
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/quote_history', methods=['GET', 'POST'])
def quote_history():
   
        # Get Form Fields
       
    cur = mysql.connection.cursor()
        
    cur.execute("SELECT * FROM quote")

    data = cur.fetchall()
    

    mysql.connection.commit()
    cur.close()    
    
   
  

    return render_template("quotehistory.html", data=data)
           
    

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








if __name__ == '__main__':

    app.secret_key='secret123'
    app.run(debug=True)
