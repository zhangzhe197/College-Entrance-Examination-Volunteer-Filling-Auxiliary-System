import pandas as pd
import re,random
def get_info(strings):
    p2 = re.compile(r'[(](.*)[)]', re.S)  # 贪婪匹配
    if len(re.findall(p2, strings)) == 0:
        return ''
    else: return '(' + re.findall(p2,strings)[0] + ')'
def delthebrackets(strings):
    a = r'\(.*\)'
    ext = re.sub(a, '', strings)
    return ext
def choosebyhands(lists,row):
    scores = []
    for line in lists:
        scores.append(line[4])
    if max(scores) - min(scores) <= 10:
        return random.choice(lists)
    return ['','']

def makedf(tarlist,templist):
    if templist == ['','']:
        res.loc[len(res)] = tarlist + templist
    else:
        res.loc[len(res)] = tarlist + templist[3:5]
    return
    pass
cnt1,cnt2,cnt3,cnt4 = 0,0,0,0          #cnt1 not found cnt2 muitfound cnt3 match cnt4(maybe) weak found
target_frame = pd.read_excel('res2.xlsx')
sourseframe = pd.read_excel('2020apply.xlsx')
target_frame = target_frame.fillna('')
sourseframe = sourseframe.fillna('')
res = pd.DataFrame(columns=['院校代码','招生院校','专业代码','专业名称','选科要求','计划','学制','学费','专业说明','大学性质','2022计划人数','2022投档数','2022最低分','2022最低位次','2021最低分','2021最低位次','2020最低分','2020最低位次'])
for row in target_frame.itertuples():
    temp = sourseframe[sourseframe['学校代码'] == getattr(row,'院校代码')]
    list_tem = [getattr(row,'院校代码'),getattr(row,'招生院校'),getattr(row,'专业代码'),getattr(row,'专业名称'),
                getattr(row,'选科要求'),getattr(row,'计划'),getattr(row,'学制'),getattr(row,'学费'),
                getattr(row,'专业说明'),getattr(row,'大学性质'),getattr(row,'_12'),
                getattr(row,'_13'),getattr(row,'_14'),getattr(row,'_15'),getattr(row,'_16'),getattr(row,'_17')] #,row[11],row[12],row[13],row[14]
    temp1 = []
    for temp_row in temp.itertuples():
        if getattr(row,'专业名称') == delthebrackets(getattr(temp_row,'专业')) and get_info(getattr(temp_row,'专业')) in getattr(row,'专业说明'):
            temp1.append([getattr(temp_row,'专业代码'),getattr(temp_row,'专业名称'),
                          getattr(temp_row,'投档数'),getattr(temp_row,'最低分'),getattr(temp_row,'最低位次'),
                          getattr(temp_row,'批次')])


    if len(temp1) == 0:
        #print("NOT FOUND the",row[7],row[9])
        for temp_row in temp.itertuples():
            if getattr(row,'专业名称') == delthebrackets(getattr(temp_row, '专业名称')):
                temp1.append(
                    [getattr(temp_row, '专业代码'), getattr(temp_row, '专业名称'),
                     getattr(temp_row, '投档数'), getattr(temp_row, '最低分'), getattr(temp_row, '最低位次'),
                     getattr(temp_row, '批次')])
        if len(temp1) == 1:
            makedf(list_tem,temp1[0])
            cnt3 += 1
        elif len(temp1) > 1:
            makedf(list_tem,choosebyhands(temp1,row))

        else:
            makedf(list_tem,['',''])
            cnt1 += 1
    elif len(temp1) > 1 :
        for line in temp1:
            if line[0] == getattr(row,'专业代码'):
                makedf(list_tem,line)
                cnt3 += 1
                break
        else:
            cnt = 0
            sellist = []
            for line in temp1:
                if line[2] != '':
                    sellist = line
                    cnt += 1
            if cnt == 1:
                makedf(list_tem,sellist)
                cnt3 += 1
            else:
                if len(temp1) == 2 and (temp1[0][-1] != temp1[1][-1]):
                    for line in temp1:
                        if line[-1] == '一段':
                            makedf(list_tem,line)
                            break
                    cnt3 += 1
                else:
                    makedf(list_tem,choosebyhands(temp1,row))
                    cnt2+=1
    else:
        makedf(list_tem,temp1[0])
        cnt3 += 1

        #list_tem += temp.ix[9:13,0].value
     #   print('FOUND')
print('not found{}, weak found{}, find mult{},FOUND{},total{}'.format(cnt1,cnt4,cnt2,cnt3,len(target_frame)))
res.to_excel('res2.xlsx')