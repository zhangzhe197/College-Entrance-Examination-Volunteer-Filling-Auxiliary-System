SECRET_KEY = "abcdefghijklmnopqrstuvwxyz"

#数据库配置
HOSTNAME = '127.0.0.1'
PORT     = '3306'
DATABASE = 'test'
USERNAME = 'root'
PASSWORD = 'zhangzhe197'
DB_URI   = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI




#邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "1460345784@qq.com"
MAIL_PASSWORD = "ipdgrlpjrmbqhcjg"
MAIL_DEFAULT_SENDER = "1460345784@qq.com"