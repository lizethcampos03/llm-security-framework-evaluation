import threading
import time


def getData(dataStart, dataLimit, thread):
    '''
    Check if the dataStart is less than or equal to dataLimit.
    If so, acquire a thread lock, increase the dataStart by 1 by, and then unlock the thread.
    Print which thread is currently accessing the data
    '''
    lock = threading.Lock()

    lock.acquire()
    try:
        if dataStart <= dataLimit:
            dataStart += 1
    finally:
        lock.release()

    print("data from A :: " + str(dataStart) + " Accessor thread :: " + str(threading.get_ident()))
    time.sleep(0.5)