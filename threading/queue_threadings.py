import threading
import queue
import urllib.request
import time

import bs4


class ThUrl(threading.Thread):
    def __init__(self, urls, data):
        threading.Thread.__init__(self)
        self.q_url = urls
        self.q_data = data

    def run(self):
        while True:
            host = self.q_url.get()
            print(self.name, host)
            url = urllib.request.urlopen(host)
            chunk = url.read()
            self.q_data.put(chunk.decode())
            self.q_url.task_done()


class ThMining(threading.Thread):
    def __init__(self, data):
        threading.Thread.__init__(self)
        self.q_data = data

    def run(self):
        while True:
            chunk = self.q_data.get()
            soup = bs4.BeautifulSoup(chunk)
            print(self.name, soup.find_all(['title']))
            self.q_data.task_done()


def main():
    for host in hosts:
        q_url.put(host)

    for i in range(3):
        t = ThUrl(q_url, q_data)
        t.setDaemon(True)
        t.start()

    for i in range(2):
        t = ThMining(q_data)
        t.daemon = True
        t.start()

    print('before join')
    q_url.join()
    q_data.join()
    print('after join')


if __name__ == '__main__':
    hosts = ["http://yahoo.com", "http://google.com", "http://amazon.com",
             "http://ibm.com", "http://apple.com"][:1]

    q_url = queue.Queue()
    q_data = queue.Queue()

    start = time.time()

    main()
    print('times: {}'.format(time.time() - start))
