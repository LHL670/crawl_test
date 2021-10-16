import time
import threading
import queue
import manageFirebase
import CGUScholarCrawl
import checkdataformat
import getIDQueue
import CGUScholarLabel

# Worker 類別，負責處理資料


class CGUScholar(threading.Thread):
    def __init__(self, queue, num):
        threading.Thread.__init__(self)
        self.queue = queue
        self.num = num

    def run(self):
        while self.queue.qsize() > 0:
            userid = self.queue.get()
            personalinfo = CGUScholarCrawl.get_PersonalPage(userid)
            check_personalformat = checkdataformat.personalInfoFormat(
                personalinfo)

            # ID或name為空時回傳False,格式錯誤修正後回傳rewriteInfo
            if(check_personalformat != False):
                manageFirebase.update_PersonalData(personalinfo)
                manageFirebase.update_LabelDomain(
                    personalinfo['personalData']['label'])
            else:
                rewritePersonalInfo = check_personalformat
                manageFirebase.update_PersonalData(rewritePersonalInfo)
                manageFirebase.update_LabelDomain(
                    rewritePersonalInfo['personalData']['label'])

            time.sleep(1)


def LabelCrawl():
    label = manageFirebase.get_LastUpdateLabel(1)  # limit
    labelList = CGUScholarLabel.get_LabelIDList(label[0])
    check_LabelFormat = checkdataformat.labelInfoFormat(labelList)

    # label list 為空時回傳False,格式錯誤修正後回傳rewriteInfo
    if(check_LabelFormat != False):
        manageFirebase.update_LabelInfo(labelList)
    else:
        rewriteLabelInfo = check_LabelFormat
        manageFirebase.update_LabelInfo(rewriteLabelInfo, label)


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
    label = 'rf_systems'
    CGUCrawlWorker(label)
    LabelCrawl()
