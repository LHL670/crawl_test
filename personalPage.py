import time
import threading
import queue
import userData
import firebase_db_connect


def userDataList(limit):
    userDataList = []
    # 建立佇列
    ID_queue = queue.Queue()

    # 將資料放入佇列
    db = firebase_db_connect.db()
    users_ref = db.collection(u'cguscholar').limit(limit)
    docs = users_ref.get()
    for doc in docs:
        # print(u'{}'.format(doc.id))
        ID_queue.put((doc.id))

    # Worker 類別，負責處理資料
    class Worker(threading.Thread):
        def __init__(self, queue, num):
            threading.Thread.__init__(self)
            self.queue = queue
            self.num = num

        def run(self):
            while self.queue.qsize() > 0:
                # 取得新的資料
                userID = self.queue.get()

                # 處理資料
                #print("Worker %d: %s" % (self.num, userID))
                userDataList.append(userData.personalPage(userID))

                time.sleep(1)

    # 建立兩個 Worker
    my_worker1 = Worker(ID_queue, 1)
    my_worker2 = Worker(ID_queue, 2)

    # 讓 Worker 開始處理資料
    my_worker1.start()
    my_worker2.start()

    # 等待所有 Worker 結束
    my_worker1.join()
    my_worker2.join()

    print("Done.")
    return userDataList


# 累積到一定得筆數upload firebase
if __name__ == '__main__':
    print('start')
    userDataList(3)
