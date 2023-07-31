import numpy
import pandas as pd
from sqlalchemy import Column, String, create_engine
import mysql,pymysql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
df = pd.read_excel('res4.xlsx')
engine = create_engine('mysql+pymysql://root:zhangzhe197@127.0.0.1:3306/test')
#
# def fun(judge,school):
#     if pd.isnull(judge):
#         df_temp = pd.read_sql('select judge from test1 where 招生院校 = "{}" ORDER BY judge ASC'.format(school),engine)
#         df_temp = df_temp.sort_values(by = ['judge'],na_position='last')
#        # print(df_temp.iloc[[0],[0]].values[0][0])
#         return df_temp.iloc[[0],[0]].values[0][0]
#     else: return judge
# df.judge = df.apply(lambda x:fun(x.judge,x.招生院校),axis=1)
# print(df)
# df.to_excel('res4.xlsx')
df.to_sql(name='test1',
          con=engine,
          if_exists='replace',
          index=False
            )