from flask import render_template
from flask import make_response
from flask import Flask, session, redirect, url_for, escape, request
from flask import Mail,Massage
import random

app = Flask(__name__)
app.secret_key = 'thesecretkey'
dic = {}
def getcookie(name):
   strings = ''
   for i in range(10):
       num = random.randint(0,9)
       strings += str(num)
   dic[strings] = name
   return strings
@app.route("/")
def check():
   if 'username' in session:
      return render_template('loggedin.html',str=session['username'] + str(dic))
   else:
      cookie = request.cookies.get('cookie')
      try:
         session['username'] = dic[cookie]
         return render_template('loggedin.html',str=session['username'])
      except:
         return render_template('login.html')
@app.route('/login',methods=['POST'])
def login():
   session['username'] = request.form['nm']
   resp = make_response(redirect(url_for('check')))
   resp.set_cookie('cookie',getcookie(request.form['nm']),max_age=3600)
   return resp
@app.route('/logout')
def logout():
   session.pop('username',None)
   cookie = request.cookies.get('cookie')
   try:
      del dic[cookie]
   except:
      pass
   resp = make_response(redirect((url_for('check'))))
   resp.delete_cookie('cookie')
   return resp
if __name__ == '__main__':
   app.run()