import firebase_db_connect
import jsonTransfer
db = firebase_db_connect.db()


def update_PersonalData(personalData):
    items = jsonTransfer.jsontransform(personalData)
    print(items)
    ref = db.collection(u'cguscholar').document((items['id']))
    ref.collection(u'updateTime').document(
        (items['personalData']['updateTime'])).set(items['cited'])
    ref.set(items['personalData'])


def update_Label(item, label):
    items = jsonTransfer.jsontransform(item)
    ref = db.collection(u'Label-Domain').document(label)
    ref.set(items)
