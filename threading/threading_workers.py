#!/usr/bin/env python3
# -*- coding: utf8 -*-

# http://eli.thegreenplace.net/2011/12/27/python-threads-communication-and-stopping/

from queue import Queue, Empty
import os

from threading import Thread, Event


class Worker(Thread):
    """ A worker thread that takes directory names from a queue, finds all
        files in them recursively and reports the result.

        Input is done by placing directory names (as strings) into the
        Queue passed in dir_q.

        Output is done by placing tuples into the Queue passed in result_q.
        Each tuple is (thread name, dirname, [list of files]).

        Ask the thread to stop by calling its join() method.
    """

    def __init__(self, in_q, out_q):
        Thread.__init__(self)
        self.in_q = in_q
        self.out_q = out_q
        self.stop_signal = Event()

    def run(self):
        # As long as we weren't asked to stop, try to take new tasks from the
        # queue. The tasks are taken with a blocking 'get', so no CPU
        # cycles are wasted while waiting.
        # Also, 'get' is given a timeout, so stoprequest is always checked,
        # even if there's nothing in the queue.
        while not self.stop_signal.is_set():
            try:
                dirname = self.in_q.get(block=True, timeout=0.1)
                filenames = list(self._files_in_dir(dirname))
                self.out_q.put((self.name, dirname, len(filenames)))
            except Empty:
                continue

    def join(self, timeout=None):
        self.stop_signal.set()
        super(Worker, self).join(timeout)

    def _files_in_dir(self, dirname):
        """ Given a directory name, yields the names of all files (not dirs)
            contained in this directory and its sub-directories.
        """
        for path, dirs, files in os.walk(dirname):
            for file in files:
                yield os.path.join(path, file)


def main(args):
    # create a single input and a single output queue for all threads
    dir_q = Queue()
    result_q = Queue()

    # create "thread pool"
    pool = [Worker(in_q=dir_q, out_q=result_q) for i in range(4)]

    # start all threads
    for thread in pool:
        thread.start()

    # give workers some work to do
    work_count = 0
    for dir in args:
        if os.path.exists(dir):
            work_count += 1
            dir_q.put(dir)

    print('Assigned {} dirs to workers'.format(work_count))

    # now get all results
    while work_count > 0:
        # blocking 'get' from Queue
        result = result_q.get()
        print('From thread {}: {} files found in dir {}'.format(*result))
        work_count -= 1

    # ask threads to die and wait for them to die
    for thread in pool:
        thread.join()


if __name__ == '__main__':
    import sys

    main(sys.argv[1:])