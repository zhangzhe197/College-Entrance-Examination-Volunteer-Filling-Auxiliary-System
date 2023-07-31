import lookupdb,userdb
from dictclass2major import category2major,str2list
from flask_migrate import Migrate
from flask import Flask, render_template, jsonify, redirect, url_for, session, request, make_response
from exts import mail,db
from flask_mail import Message
from models import EmailCaptchaModel,UserModel
from werkzeug.security import generate_password_hash,check_password_hash
from forms import RegisterForm,LoginForm
import string,random,config
import pdfkit
app = Flask(__name__)
#configs = pdfkit.configuration(wkhtmltopdf=r'C:\Users\sweet\PycharmProjects\pythonProject5\wkhtmltopdf\bin\wkhtmltopdf.exe')


app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
migrate = Migrate(app,db)


@app.route("/")
def index():
    return redirect(url_for('mainpage'))


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html',wrong=0)
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("无此用户")
                return render_template('login.html',wrong=1)
            if check_password_hash(user.password,password):
                session['user_id']  = user.id
                if userdb.checkuser(user.id):
                    return redirect(url_for('mainpage'))
                else:
                    return redirect(url_for('fillinfo'))
            else:
                print("password wrong!")
                return render_template('login.html', wrong=1)

        else:
            print(form.errors)
            return redirect(url_for("login"))


@app.route("/register",methods=["GET","POST"])
def register():
    if request.method =='GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.email.data
            password = form.password.data
            user = UserModel(email=email,username=username,password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))
        else:
            print(form.errors)
            return redirect(url_for("register"))

@app.route("/captcha/email")
def get_email_captcha():
    email = request.args.get("email")
    source  = string.digits*4
    captcha = random.sample(source,4)
    captcha = "".join(captcha)
    message = Message(subject="【高考志愿填报系统邮箱验证码】",recipients=[email],body=f"您的验证码是：{captcha}，请勿告诉他人哦")
    mail.send(message)
    email_captcha = EmailCaptchaModel(email=email,captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return jsonify({"code":200,"message": "","data":None})

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('mainpage'))

@app.route('/main')
def mainpage():
    if 'user_id' in session:
        return render_template('main.html',login=1)
    else:
        return render_template('main.html',login=0)
@app.route('/recommenduniv')
def reccomend_univ():
    if not ('user_id' in session) or not userdb.checkuser(session['user_id']):
        return redirect(url_for('login'))
    df = lookupdb.getrecommenduniv(rank=userdb.getuserrank(session['user_id']))
    data_list = df.values.tolist()
    return render_template('recommenduniv.html',data= data_list)

@app.route('/recommendmajor')
def recommend_major():
    if not ('user_id' in session) or not userdb.checkuser(session['user_id']):
        return redirect(url_for('login'))
    major_list = ['计算机科学与技术','电气工程及其自动化','  电子信息工程','临床医学','金融学','法学','软件工程','汉语言文学','通信工程','会计学']
    data = []
    for elements in major_list:
        data.append([elements] + lookupdb.getrecommendmajor(rank=userdb.getuserrank(session['user_id']),
                                                            major=elements))
    return render_template('recommendmajor.html',data = data)

@app.route('/schooldetail/<name>/<pageloc>')
def schooldetail(name,pageloc):
    if not ('user_id' in session):
        return redirect(url_for('login'))
    try: list1, maxpagenum = lookupdb.getinfouniv_major(name,int(pageloc))
    except: return redirect(url_for('notfound',reason='此高校今年在您的地区未招生'))
    info_list = lookupdb.getinfouniv(name)
    return render_template('detail_univinfo.html',majordata = list1,page = int(pageloc),max_page = int(maxpagenum),
                           infolist = info_list)

@app.route('/search',methods=['post'])
def getsearch():
    if not ('user_id' in session):
        return redirect(url_for('login'))
    requ = request.form
    if requ['searchkey'] == '': return redirect(url_for('notfound',reason='搜索内容不能为空'))
    res_list = lookupdb.fuzzy_search(requ['searchkey'])
    if len(res_list) == 0:
        return redirect(url_for('notfound',reason='你所要的页面未找到'))
    elif len(res_list) == 1:
        return redirect(url_for('schooldetail',name=res_list[0][0],pageloc=1))
    else:
        return render_template('search.html',searchdata=res_list)

@app.route('/filter',methods=['GET','post'])
def filter():
    if not ('user_id' in session) or not userdb.checkuser(session['user_id']):
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('filter.html',data = [])
    else :
        form = request.form
        lookupdb.sublist = str2list(userdb.getusersub(session['user_id']))
        print(lookupdb.sublist)
        if form['form_type'] == 'filter':
            try:
                range_st,range_ed = int(form['wc1']), int(form['wc2'])
            except: range_st, range_ed = 1, 500000
            datalist = lookupdb.normalfilter(chosenprov=form.getlist('province'),
                                             chosenmajor=category2major(form['category']),
                                             school_attributes=form.getlist('college_type'),
                                             max_rank=range_st,
                                             min_rank=range_ed)
            return render_template('filter.html',data=datalist)
        else:
            if form['school'] == '' and form['major'] == '':
                return render_template('filter.html',data=[])
            datalist = lookupdb.accuratefilter(form['school'],form['major'])
            return render_template('filter.html',data= datalist)

@app.route('/fillinfo',methods=['GET','POST'])
def fillinfo():
    if request.method == 'GET':
        return render_template('fillinfo.html')
    else:
        if 0 < int(request.form['score']) < 750 and 0 < int(
            request.form['rank']) < 300000 and len(request.form.getlist('kemu')) == 3:
            try:
                userdb.createuserinfo(session['user_id'],str(request.form.getlist('kemu')),
                                  int(request.form['rank']),int(request.form['score']))
                return redirect(url_for('mainpage'))
            except: return redirect(url_for('notfound',reason='您已经填写过您的信息 '))
        else:
            return render_template('fillinfo.html',err = 1)


@app.route('/404/<reason>')
def notfound(reason):
    return render_template('404.html',notice=reason)

@app.route('/addmajor',methods=['POST'])
def addmajor():
    form = request.form
    userdb.addmajortodb(session['user_id'],form['schoolcode'],form['majorcode'])
    return render_template('backpage.html')

@app.route('/majortable',methods=['GET',"POST"])
def majortable():
    if not ('user_id' in session) or not userdb.checkuser(session['user_id']):
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('majortable.html',data=userdb.getmajortable(session['user_id']))
    else:
        form = request.form
        if form['attr'] == 'delete':
            userdb.delectmajordb(session['user_id'],form['schoolcode'],form['majorcode'])
            return render_template('majortable.html',data=userdb.getmajortable(session['user_id']))
        elif form['attr'] == 'adjust':
            try:
                userdb.changeorder(session['user_id'],form['schoolcode'],form['majorcode'],int(form['fname']))
            except: pass
            return render_template('majortable.html',data=userdb.getmajortable(session['user_id']))
        elif form['attr'] == 'deleteall':
            userdb.delectmajordball(session['user_id'])
            return render_template('majortable.html',data=userdb.getmajortable(session['user_id']))
        elif form['attr'] == 'sort':
            userdb.sort_by_judge(session['user_id'])
            return render_template('majortable.html', data=userdb.getmajortable(session['user_id']))
        elif form['attr'] == 'save':
            # pdfkit_option = {'encoding' : 'utf-8'}
            # rendered_html = render_template('html2pdf.html',data=userdb.getmajortable(session['user_id']))
            # pdfkit.from_string(rendered_html, 'output.pdf', configuration=configs,options=pdfkit_option)
            # with open('output.pdf', 'rb') as pdf_file:
            #     pdf_data = pdf_file.read()
            # import os
            # os.remove('output.pdf')
            # response = make_response(pdf_data)
            # response.headers['Content-Type'] = 'application/pdf'
            # response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
            return render_template('majortable.html', data=userdb.getmajortable(session['user_id']))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001)