import firebase_db_connect
import datetime
import queue
db = firebase_db_connect.db()


def IDCheck(ID):
    users_ref = db.collection(u'cguscholar').document(ID)
    doc = users_ref.get()
    if doc.exists:
        checkTemp = doc.to_dict()
        Timestamp = checkTemp['updateTime']
        return Timestamp
    else:
        return ('Not found')


def expiresCheck(last_update, expires):
    if last_update == 'Not found':
        compare = True
    else:
        expires_date = datetime.datetime.strptime(
            last_update, "%Y-%m-%d %H:%M:%S")
        compare_date = expires_date + datetime.timedelta(days=expires)
        current_date = datetime.datetime.now()

        compare = compare_date < current_date
    print(compare)
    return compare  # compare result
    # 過期或Not found為true


def ID_queue(label):
    # 建立佇列
    ID_queue = queue.Queue()

    # 將資料放入佇列
    label_ref = db.collection(u'Label-Domain').document(label)
    docs = label_ref.get()
    IDtemp = docs.to_dict()

    # 取五個過期或為爬過的ID
    number = 5
    ID_count = 0
    while (number != 0):
        expire_time = IDCheck(IDtemp['userID'][ID_count])
        if(expiresCheck(expire_time, 1)):
            print(IDtemp['userID'][ID_count])
            ID_queue.put(IDtemp['userID'][ID_count])
            number = number - 1
        ID_count = ID_count + 1

    return ID_queue
