import getTime
import datetime


def personalInfoFormat(data):
    # check id format
    personalData = data['personalData']
    if (data['id'][7::] != 'AAAAJ' or data['id'] == ' ' or data['id'] == None):
        return False
    # check personal data format
    if(personalData['name'] == ' ' or personalData['name'] == None):
        return False
    if(personalData['university'] == ' ' or personalData['university'] == '首頁' or personalData['university'] == None):
        data['personalData']['university'] == 'None'

    if(personalData['picture'] == ' ' or personalData['picture'] == None):
        data['personalData']['picture'] == 'None'

    if(len(personalData['label']) == 5):
        data['personalData']['label'] == 'None'
    # check updateTime format
    if(personalData['updateTime'] == '' or personalData['updateTime'] == None):
        data['personalData']['updataTime'] == getTime.CurrentTime()
    try:
        datetime.datetime.strptime(
            personalData['updateTime'], "%Y-%m-%d %H:%M:%S")
    except:
        data['personalData']['updataTime'] == getTime.CurrentTime()
