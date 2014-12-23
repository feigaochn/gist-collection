from thread import start_new_thread

def worker():
    while 1:
        #print 1
        pass

for it in range(0, 15):
    start_new_thread(worker, ())


raw_input()