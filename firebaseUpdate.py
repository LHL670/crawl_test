import firebase_db_connect
import jsonTransfer
import userData
db = firebase_db_connect.db()


def updatePersonal(userID):
    items = jsonTransfer.jsontransfer(userData.personalPage(userID))
    print(items)
    ref = db.collection(u'cguscholar').document((items['id']))
    ref.collection(u'updateTime').document(
        (items['personalData']['updateTime'])).set(items['cited'])
    ref.set(items['personalData'])
