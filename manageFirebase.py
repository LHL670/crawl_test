import firebase_db_connect
import jsonTransfer
db = firebase_db_connect.db()


def updatePersonalData(personalData):
    items = jsonTransfer.jsontransfer(personalData)
    print(items)
    ref = db.collection(u'cguscholar').document((items['id']))
    ref.collection(u'updateTime').document(
        (items['personalData']['updateTime'])).set(items['cited'])
    ref.set(items['personalData'])
