import pandas as pd
import sqlalchemy,re,math
from functools import cmp_to_key
import mysql.connector
engine = sqlalchemy.create_engine('mysql+pymysql://root:zhangzhe197@127.0.0.1:3306/test')
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='zhangzhe197',
    
    database='test'
)
mycursor = mydb.cursor()
# ------------------------------------------------------------------------------------------
# 函数名称 id2name
# 函数功能 根据id 返回用户的用户名
# 函数输入参数
#     id
# 返回值 string 用户名
#-------------------------------------------------------------------------------------------
def createuserinfo(user_id, subjects,rank,score):
    sql_checker = "select * from userinfo where user_id={};"
    df = pd.read_sql(sql_checker.format(user_id),engine)
    if len(df) == 0:
        data = {
            'user_id' : [user_id],
            'subject' : [subjects],
            'ranking' : [rank],
            'score' :[score]
        }
        df_temp = pd.DataFrame(data)
        df_temp.to_sql(name='userinfo',con=engine,if_exists='append',index=False)
        print('new user info added')
    else: raise NameError('user data already exist')

def checkuser(user_id):
    sql_checker = "select * from userinfo where user_id={};"
    df = pd.read_sql(sql_checker.format(user_id), engine)
    if len(df) == 0:
        print('user info not found')
        return False
    else:
        print('get userinfo')
        return True

def getusersub(user_id):
    sql = 'select subject from userinfo where user_id ={};'
    df = pd.read_sql(sql.format(user_id),engine)
    return  df.iloc[[0],[0]].values[0][0]

def getuserrank(user_id):
    sql = 'select ranking from userinfo where user_id ={};'
    df = pd.read_sql(sql.format(user_id),engine)
    return df.iloc[[0],[0]].values[0][0]

def getuserscore(user_id):
    sql = 'select score from userinfo where user_id ={};'
    df = pd.read_sql(sql.format(user_id),engine)
    return df.iloc[[0],[0]].values[0][0]

def addmajortodb(user_id, schoolcode, majorcode):
    sql = '''
    INSERT INTO user_major (id,user_id, school_code, major_code, major_sort_order,judge,
    招生院校,专业名称,计划,学制,学费,专业说明,2022计划人数,2022最低分,最低位次2022,2021最低分,最低位次2021,选科要求)
SELECT MAX(id) + 1 ,%s, %s, %s,  COUNT(*) + 1, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
FROM user_major;
'''
    sql1 = 'select judge,招生院校,专业名称,计划,学制,学费,专业说明,2022计划人数,2022最低分,最低位次2022,2021最低分,最低位次2021,选科要求 from test1 where 院校代码 = "{}" and 专业代码 = "{}"'
    sql2 = 'select judge from user_major where school_code = "{}" and major_code = "{}"'
    check_df = pd.read_sql(sql2.format(schoolcode,majorcode),engine)
    if len(check_df) >= 1:
        return
    df = pd.read_sql(sql1.format(schoolcode,majorcode),engine)
    list1 = [user_id,schoolcode,majorcode] + df.values.tolist()[0]
    mycursor.execute(sql,tuple(list1))
    mydb.commit()

def delectmajordb(user_id,schoolcode,majorcode):
    sql = 'DELETE FROM user_major WHERE user_id = %s and school_code = %s and major_code = %s'
    val = (user_id,schoolcode,majorcode)
    mycursor.execute(sql,val)
    mydb.commit()

def changeorder(user_id,schoolcode,majorcode,target):
    sql1 = 'select id, major_sort_order,school_code,major_code from user_major where user_id = {} order by major_sort_order ASC;'
    sql2 = 'update user_major set major_sort_order = %s where id=%s;'
    df = pd.read_sql(sql1.format(user_id),engine)
    try:
        index = df[(df.school_code == schoolcode) & (df.major_code == majorcode)].index.tolist()[0]
    except: raise NameError("wrong target")
    if  0 < target <= len(df) and target != index + 1:
        if target < index + 1:
            for i in range(index - 1, target - 2, -1):
                val = (int(df.iloc[[i+1],[1]].values[0][0]), int(df.iloc[[i],[0]].values[0][0]))
                mycursor.execute(sql2,val)
                mydb.commit()
            val1 = (int(df.iloc[[target - 1],[1]].values[0][0]), int(df.iloc[[index],[0]].values[0][0]))
            mycursor.execute(sql2,val1)
            mydb.commit()
        else:
            for i in range(index + 1, target):
                val = (int(df.iloc[[i-1],[1]].values[0][0]), int(df.iloc[[i],[0]].values[0][0]))
                mycursor.execute(sql2,val)
                mydb.commit()
            val1 = (int(df.iloc[[target - 1],[1]].values[0][0]), int(df.iloc[[index],[0]].values[0][0]))
            mycursor.execute(sql2,val1)
            mydb.commit()
    else: raise NameError('wrong target')

def sort_by_judge(user_id):
    sql = 'select * from user_major where user_id = {} order by judge ASC;'
    sql2 = 'update user_major set major_sort_order = %s where id=%s;'
    df = pd.read_sql(sql.format(user_id),engine)
    if len(df) <= 1 : return
    ordernum = 0
    for row in df.itertuples():
        val = (ordernum,getattr(row,'id'))
        ordernum += 1
        mycursor.execute(sql2,val)
        mydb.commit()

def getmajortable(user_id):
    sql = 'select * from user_major where user_id={} order by major_sort_order ASC'
    df = pd.read_sql(sql.format(user_id),engine)
    list1 = df.fillna('').values.tolist()
    order = 1
    for line in list1:
        line.append(order)
        order += 1
    return list1

def delectmajordball(user_id):
    sql = 'DELETE FROM user_major WHERE user_id = %s'
    val = [user_id]
    mycursor.execute(sql,val)
    mydb.commit()

print(getmajortable(1))