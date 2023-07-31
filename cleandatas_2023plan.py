import pandas as pd
def getst(sts):
    if sts.find('(') != -1:
        return sts[sts.find('('):]
    else:
        return ''
def getst1(sts):
    if sts.find('(') != -1:
        return sts[:sts.find('(')]
    else:
        return sts
def getst2(sts):
    if sts.find('(') != -1:
        return sts[sts.rfind('('):]
    else:
        return ''
def getst3(sts):
    if sts.find('(') != -1:
        return sts[:sts.rfind('(')]
    else:
        return sts
frame = pd.read_excel('2023plan.xlsx')
frame = frame[frame['批'] == '本科常规批']
frame.reset_index(drop=True)
frame['专业说明'] = None
frame['大学性质'] = None
frame.专业说明 = frame.apply(lambda x: getst(x.专业名称),axis=1)
frame.专业名称 = frame.apply(lambda x: getst1(x.专业名称),axis=1)
frame.大学性质 = frame.apply(lambda x: getst2(x.招生院校),axis=1)
frame.招生院校 = frame.apply(lambda x: getst3(x.招生院校),axis=1)
frame.to_excel('2023palnchanged.xlsx')
print(frame)