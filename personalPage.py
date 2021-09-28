import time
import threading
import queue
import firebaseUpdate
import firebase_db_connect
import IDCheck


def userDataList(label):

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
                firebaseUpdate.updatePersonal(userID)

                time.sleep(1)
    work_queue = IDCheck.ID_queue(label)
    # 建立兩個 Worker
    my_worker1 = Worker(work_queue, 1)
    my_worker2 = Worker(work_queue, 2)

    # 讓 Worker 開始處理資料
    my_worker1.start()
    my_worker2.start()

    # 等待所有 Worker 結束
    my_worker1.join()
    my_worker2.join()

    print("Done.")


# 累積到一定得筆數upload firebase
if __name__ == '__main__':
    print('start')
    label = 'causal_inference'
    userDataList(label)
