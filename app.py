from flask import Flask,render_template,flash,redirect,url_for,session,request,logging
from flask import MYSQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
app=Flask(__name__)


# @app.route('/')
# def index():
#     return render_template('index.html')



class Login(Form):
    username=StringField('username',[validators.Length(max=50)])
    password=PasswordField('password',[
        validators.DataRequired(),validators.EqualTo('confirm',message='passwords do not match')
    ])
    confirm=PasswordField('confirm password')

@app.route('/login',methods=['POST'])
def login():
    form=Login(request.form)
    if request.method=='POST' and form.validate():
        return render_template('index.html')

    return render_template('index.html',form=form)

if __name__=='__main__':
    app.run(debug=True)
