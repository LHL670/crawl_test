import time
import threading
import queue
import manageFirebase
import CGUScholarCrawl
import checkDataformat
import getIDQueue

# Worker 類別，負責處理資料


class CGUScholar(threading.Thread):
    def __init__(self, queue, num):
        threading.Thread.__init__(self)
        self.queue = queue
        self.num = num

    def run(self):
        while self.queue.qsize() > 0:
            userID = self.queue.get()
            personalData = CGUScholarCrawl.get_PersonalPage(userID)
            checkpersonalfFormat = checkDataformat.personalInfoFormat(
                personalData)

            if(checkpersonalfFormat != False):
                manageFirebase.update_PersonalData(personalData)
            else:
                rewriteData = checkpersonalfFormat
                manageFirebase.update_PersonalData(rewriteData)
            time.sleep(1)


def CGUCrawlWorker(label):
    work_queue = getIDQueue.get_IDQueue(label)
    # 建立兩個 Worker
    CGUWorker1 = CGUScholar(work_queue, 1)
    CGUWorker2 = CGUScholar(work_queue, 2)

    # 讓 Worker 開始處理資料
    CGUWorker1.start()
    CGUWorker2.start()

    # 等待所有 Worker 結束
    CGUWorker1.join()
    CGUWorker2.join()

    print("Done.")


# 累積到一定得筆數upload firebase
if __name__ == '__main__':
    print('start')
    label = 'causal_inference'
    CGUCrawlWorker(label)
