import pandas as pd
import sqlalchemy,re,math
from functools import cmp_to_key
engine = sqlalchemy.create_engine('mysql+pymysql://root:zhangzhe197@127.0.0.1:3306/test')
sublist = ['物理','化学','生物']


def delthebrackets(strings):
    return strings[1:len(strings) - 1]

def get_re(list1):
    strprov = ''
    for i in range(len(list1)):
        if i != len(list1) - 1:
            strprov += list1[i] + '|'
        else:
            strprov += list1[i]
    return "'" + strprov + "'"


# ------------------------------------------------------------------------------------------
# 函数名称 getsubjectorder
# 函数功能 根据输入的科目输出筛选科目的MySQL命令
# 函数输入参数
#    list1 考生的选科的列表
# 返回值 string 格式的命令
#-------------------------------------------------------------------------------------------

def getsubjectorder(list1):
    def getsulistsortedcmp(str1, str2):
        dic1 = {'物理': 0, '思想政治': 1, '历史': 2, '地理': 3, '化学': 4, '生物': 5}
        if dic1[str1] < dic1[str2]:
            return -1
        elif dic1[str1] > dic1[str2]:
            return 1
        else:
            return 0
    list2 = sorted(list1,key=cmp_to_key(getsulistsortedcmp))
    order = " and ((选科要求 = '不限' or 选科要求= '{}' or 选科要求= '{}' or 选科要求= '{}')  or ((选科要求 REGEXP '或') and (选科要求 REGEXP '{}' or 选科要求 REGEXP '{}' or 选科要求 REGEXP '{}')) or (选科要求 REGEXP '和' and 选科要求 IN ('{}','{}','{}','{}')))"
    return order.format(list2[0],list2[1],list2[2],list2[0],list2[1],list2[2],list2[0] + '和' + list2[1],
                        list2[0] + '和' + list2[2],list2[1] + '和' + list2[2],list2[0]+'和'+list2[1]+'和'+list2[2])
# ------------------------------------------------------------------------------------------
# 函数名称 normalfilter
# 函数功能 访问数据库 并给出符合条件的内容
# 函数输入参数
#     chosenprov 选择的省份,列表形式输入,不选默认为全部省份
#     chosenmajor 选择的省份,不选默认为全部
#     max_rank & min_rank 最低和最高排名,不选默认为全部
#     school_attributes 办学属性/ 公办,民办,独立学院,中外合作办学,港澳台地区合作办学
#     restrictsub = True 考虑考生的选课要求
# 返回值 Dataframe 筛选出的内容
#-------------------------------------------------------------------------------------------

def normalfilter(chosenprov=None, chosenmajor = [], school_attributes=None, max_rank = 1, min_rank = 500000, restrictsub = True):
    if school_attributes is None:
        school_attributes = ['公办', '民办', '独立学院', '中外合作办学', '港澳台地区合作办学']
    if chosenprov is None:
        chosenprov = ['河北', '山西', '黑龙江', '吉林', '辽宁', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南',
                      '湖北', '湖南', '广东', '海南',
                      '四川', '贵州', '云南', '陕西', '甘肃', '青海', '台湾', '内蒙', '广西', '西藏', '宁夏', '新疆',
                      '北京', '天津', '上海', '重庆', '香港', '澳门']
    sql = '''
    select  院校代码,招生院校,专业代码,专业名称,计划,学制,学费,专业说明,rating,twotwoone,nineeight,双一流,2022计划人数,2022最低分,最低位次2022,2021最低分,最低位次2021,选科要求  from test1 where (judge BETWEEN {} and {}) and (大学性质 REGEXP {}) and (大学性质 REGEXP {}) 
    '''
    if len(chosenmajor) == 0:   sql1 = sql.format(max_rank,min_rank,get_re(chosenprov),get_re(school_attributes))
    else:
        strings = get_re(chosenmajor)
        sql1 = sql.format(max_rank,min_rank,get_re(chosenprov),get_re(school_attributes)) + \
               'and (专业名称 REGEXP {} or 专业说明 REGEXP {})'.format(strings,strings)
    if restrictsub == True:
        df = pd.read_sql(sql1 + getsubjectorder(sublist) + 'ORDER BY judge ASC;', engine)
    else:
        df = pd.read_sql(sql1 + ';',engine)

    if len(df) > 1000:
        return df.fillna('').values.tolist()[:1000]
    return df.fillna('').values.tolist()
# ------------------------------------------------------------------------------------------
# 函数名称 accuratefilter
# 函数功能 实现精准搜索
# 函数输入参数
#     school_name 搜索的学校名称
#     major_name 搜索的专业名称
#     restrictsub = True 考虑考生的选课要求
# 返回值 Dataframe 筛选出的内容
#-------------------------------------------------------------------------------------------


def accuratefilter(school_name,major_name,restrictsub = True):
    sql_acc = """
    select 院校代码,招生院校,专业代码,专业名称,计划,学制,学费,专业说明,rating,twotwoone,nineeight,双一流,2022计划人数,2022最低分,最低位次2022,2021最低分,最低位次2021,选科要求 from test1 where """
    order1 = '(招生院校 REGEXP "{}" or 招生院校 = "{}")'
    order2 = '(专业名称 REGEXP "{}" or 专业说明 REGEXP "{}")'
    if major_name == '':
        sql_acc1 = sql_acc + order1.format(school_name,school_name)
    elif school_name == '':
        sql_acc1 = sql_acc + order2.format(major_name,major_name)
    else:
        sql_acc1 = sql_acc + order1.format(school_name,school_name) +' and ' + order2.format(major_name,major_name)
    if restrictsub == True:
        df = pd.read_sql(sql_acc1 + getsubjectorder(sublist) + 'ORDER BY judge ASC;', engine)
    else:
        df = pd.read_sql(sql_acc1 + ';',engine)
    print(df,sql_acc1 + getsubjectorder(sublist) + 'ORDER BY judge ASC;')
    print(df.values.tolist())

    if len(df) > 1000:
        return df.fillna('').values.tolist()[:1000]
    return df.fillna('').values.tolist()
# ------------------------------------------------------------------------------------------
# 函数名称 getrecommenduniv
# 函数功能 获取推荐的大学
# 函数输入参数
#     rank 考生的排名信息
# 返回值 推荐的大学index,招生院校,twotwoone,C9,nineeight,双一流,major1,major2,major3
#-------------------------------------------------------------------------------------------
def getrecommenduniv(rank):
    sql_rec = 'select distinct 招生院校,twotwoone,C9,nineeight,双一流,大学性质 from test1 where judge between {} and {};'
    sql_get = 'select 招生院校,专业名称 from test1 where (judge between {} and {}) and (招生院校="{}") ORDER BY judge ASC LIMIT 3;'
    df = pd.read_sql(sql_rec.format(max(rank - 3000,0),rank + 1000),engine).fillna('')
    try: df = df.sample(n=10).reset_index()
    except: df = df.reset_index()
    df.大学性质 = df.apply(lambda x: delthebrackets(x.大学性质),axis=1)
    print(df)
    for i in range(1,4):
        df.insert(df.shape[1],column='major' + str(i),value='')
    for i in range(10):
        dftemp = pd.read_sql(sql_get.format(max(rank - 3000, 0), rank + 1000,df.iloc[i].at['招生院校']), engine)
        for j in range(len(dftemp)):
            try:
                 df.iloc[i,j + 7] = dftemp.at[j,'专业名称']
            except: pass
    return df

# ------------------------------------------------------------------------------------------
# 函数名称 getrecommendmajor
# 函数功能 在推荐的专业上显示特定的大学
# 函数输入参数
#     rank 考生的排名信息
# 返回值 包含三个招生院校的列表
#-------------------------------------------------------------------------------------------
def getrecommendmajor(rank,major):
    sql_maj = 'select 招生院校,judge from test1 where judge >= {} and (专业名称 REGEXP "{}" or 专业说明 REGEXP "{}") ORDER BY judge ASC LIMIT 3'
    df = pd.read_sql(sql_maj.format(rank,major,major),engine)
    res = []
    for line in range(len(df)):
        res.append(df.iloc[line].at['招生院校'])
    while 1:
        if len(res) < 3: res.append('')
        else: break
    return res
# ------------------------------------------------------------------------------------------
# 函数名称 getinfouniv
# 函数功能 返回特定高校的详情信息,用于显示在详情页
# 函数输入参数
#     school 学校的名称
# 返回值 一个列表,包括学校的一些信息
#-------------------------------------------------------------------------------------------
def getinfouniv(school):
    sql = 'select 中文名字,英文名字,所在省份,所在城区,女生比例,学校类型,所属机构,是否985,是否211,描述,官网 from univinfo where 中文名字="{}";'
    df = pd.read_sql(sql.format(school),engine).fillna('')
    if len(df) == 0:
        sql_fuzz = 'select 中文名字,英文名字,所在省份,所在城区,女生比例,学校类型,所属机构,是否985,是否211,描述,官网 from univinfo where 中文名字 REGEXP "{}";'
        df = pd.read_sql(sql_fuzz.format(school),engine).fillna('')
    list1 = df.values.tolist()[0]
    list1[9] = list1[9].split('_x000D_',1)[0]
    return list1
# ------------------------------------------------------------------------------------------
# 函数名称 getinfouniv_major
# 函数功能 返回特定高校的当年招生信息,用于显示在详情页
# 函数输入参数
#     school 学校的名称
# 返回值 一个列表,包括学校的招生信息和检索到的信息条数
#-------------------------------------------------------------------------------------------
def getinfouniv_major(school,page = 1,cap = 8):
    sql = 'select 专业名称,选科要求,计划,学费,专业说明,rating,judge from test1 where 招生院校 = "{}" ORDER BY judge ASC;'
    df = pd.read_sql(sql.format(school),engine).fillna('').reset_index()
    if len(df) == 0:
        if '中国人民解放军' in school:
            df = pd.read_sql(sql.format(school.replace('中国人民解放军','')),engine).fillna('').reset_index()
    lineselected = df.shape[0]
    if math.ceil(df.shape[0] / cap) < page:
        raise NameError('page out of range')
    else:
        df = df.loc[(page - 1) * cap:min(page * cap - 1, len(df)), :]
    return df.values.tolist(),math.ceil(lineselected / cap)

# ------------------------------------------------------------------------------------------
# 函数名称 fuzzy_search
# 函数功能 返回特定高校的当年招生信息,用于显示在详情页
# 函数输入参数
#     关键词
# 返回值 一个列表,包括大学名称,学校简介缩减版
#-------------------------------------------------------------------------------------------
def fuzzy_search(keyword):
    sql= 'select 中文名字,描述 from univinfo where 中文名字 REGEXP "{}"'
    df = pd.read_sql(sql.format(keyword),engine)
    list1 = df.values.tolist()
    for line in list1:
        line[1] = line[1][:150] + '...'
    print(list1)
    return list1