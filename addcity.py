import pandas as pd
import re
df = pd.read_excel('res2.xlsx')
source = pd.read_excel('rating.xlsx',header=1)
schoolattr = pd.read_excel('985211.xlsx',header=1)
pass
#source = source.loc[:, ~source.columns.str.contains('^Unnamed')]
#source= source.rename(columns={'Unnamed:1':'一级学科','Unnamed:2':'等级','Unnamed:3':'院校代码及名称'}   )
df.insert(loc=2,column='所在省区',value='')
df.insert(loc=16,column='judge',value='')
df.insert(loc=10,column='rating',value='')
df.insert(loc=11,column='twotwoone',value='')
df.insert(loc=12,column='C9',value='')
df.insert(loc=13,column='nineeight',value='')
df.insert(loc=14,column='double',value='')
df.fillna('')
def delthebrackets(strings):
    a = r'\(.*\)'
    ext = re.sub(a, '', strings)
    return ext
def getpro(strings):
    return strings[1:3]
def delcode(strings):
    pre = re.compile(u'[\u4e00-\u9fa5]')
    res = re.findall(pre,strings)
    return ''.join(res)
def getrank(num1,num2):
    if num1 != '': return num1
    else: return num2
def getrating(school,subject):
    subframe = source[(source['一级学科'] == subject) & (source['院校代码及名称'] == delthebrackets(school))]
    if len(subframe) == 1:
        return subframe.iloc[[0],[2]].values[0][0]
def schoolattrbuate(school,attr):
    subframe = schoolattr[schoolattr['院校'] == school]
    if len(subframe) == 1:
        if attr == '211':
            return subframe.iloc[[0],[6]].values[0][0]
        elif attr == 'C9':
            return subframe.iloc[[0],[8]].values[0][0]
        elif attr == '985':
            return subframe.iloc[[0],[7]].values[0][0]
        elif attr == 'double':
            return '双一流'

source.一级学科 = source.apply(lambda x:delcode(x.一级学科),axis=1)
source.院校代码及名称 = source.apply(lambda x:delcode(x.院校代码及名称),axis=1)
df.所在省区 = df.apply(lambda x:getpro(x.大学性质),axis=1)
df.rating = df.apply(lambda x:getrating(x.招生院校,x.专业名称),axis=1)
df.judge = df.apply(lambda x:getrank(x.最低位次2022,x.最低位次2021),axis=1)
df.twotwoone = df.apply(lambda x:schoolattrbuate(x.招生院校,'211'),axis=1)
df.nineeight = df.apply(lambda x:schoolattrbuate(x.招生院校,'985'),axis=1)
df.C9 = df.apply(lambda x:schoolattrbuate(x.招生院校,'C9'),axis=1)
df.double = df.apply(lambda x:schoolattrbuate(x.招生院校,'double'),axis=1)
df.to_excel('res3.xlsx')