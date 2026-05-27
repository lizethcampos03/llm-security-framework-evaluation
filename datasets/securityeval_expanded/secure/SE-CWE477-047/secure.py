import time


def currentTime():
    '''
    Print the current processor time in seconds.
    '''
    pro_time = time.process_time()
    print("Current processor time (in seconds):", pro_time)