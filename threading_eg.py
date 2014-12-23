#! /usr/local/bin/python3

import time
import threading

def sleeper(i):
    print("thread {} sleeps for 5 seconds".format(i))
    time.sleep(5)
    print("thread %d woke up" % i)

if __name__ == '__main__':
    for i in range(10):
        t = threading.Thread(target=sleeper, args=(i,))
        t.start()
