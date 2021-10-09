import getTime
import datetime


def personalInfoFormat(data):
    # check id format
    rewriteData = data
    personalData = data['personalData']
    if (data['id'][7::] != 'AAAAJ' or data['id'] == ' ' or data['id'] == None):
        return False
    # check personal data format
    if(personalData['name'] == ' ' or personalData['name'] == None):
        return False

    if(personalData['university'] == ' ' or personalData['university'] == '首頁' or personalData['university'] == None):
        rewriteData['personalData']['university'] = 'None'

    if(personalData['picture'] == ' ' or personalData['picture'] == None or personalData['picture'] == '/citations/images/avatar_scholar_128.png'):
        rewriteData['personalData']['picture'] = 'https://scholar.google.com.tw/citations/images/avatar_scholar_128.png'

    if(len(personalData['label']) == 0):
        rewriteData['personalData']['label'] = 'None'
    # check updateTime format
    if(personalData['updateTime'] == '' or personalData['updateTime'] == None):
        rewriteData['personalData']['updataTime'] = getTime.currentTime()

    try:
        datetime.datetime.strptime(
            personalData['updateTime'], "%Y-%m-%d %H:%M:%S")
    except:
        rewriteData['personalData']['updataTime'] = getTime.currentTime()
    return rewriteData
