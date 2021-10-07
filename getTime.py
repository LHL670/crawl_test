import datetime


def CurrentTime():
    now = datetime.datetime.now()
    currentTime = now.strftime("%Y-%m-%d %H:%M:%S")
    return currentTime
