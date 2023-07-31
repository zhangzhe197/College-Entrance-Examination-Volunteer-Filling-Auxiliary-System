from flask_migrate import Migrate
from flask import Flask,render_template,jsonify,redirect,url_for,session,request
from exts import mail,db
from flask_mail import Message
from models import EmailCaptchaModel,UserModel
from werkzeug.security import generate_password_hash,check_password_hash
from forms import RegisterForm,LoginForm
import string,random,config

app = Flask(__name__)



if __name__ == '__main__':
    app.run()
