#! /usr/local/bin/python2

from thread import start_new_thread
from time import sleep

def mysqrt(a):
    """Calculate the sqrt of a"""
    print(a)
    eps = 0.000000001
    old = 1
    new = 1
    while True:
        old, new = new, (new + a/new) / 2.0
        # print(old, new)
        if (abs(new-old) < eps):
            break
    return new

def sj(x):
    print(x)
    print("before ")
    sleep(x)
    print("after")

start_new_thread(sj, (3, ))
start_new_thread(sj, (3, ))

print("exit")
c = raw_input('haha')
