import threading
from time import sleep
import concurrent.futures
from functools import wraps


def spawn(func):
    thread = threading.Thread(target=func)
    thread.start()
    return thread


@spawn
def task2():
    print('my task2')


@spawn
def task1():
    sleep(1)
    print('my task1')

def async(func):
    @wraps(func)
    def spawned(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return spawned

@async
def task3():
    sleep(0.2)
    print('task 3')


def py3():
    executor = concurrent.futures.ThreadPoolExecutor(3)

    @executor.submit
    def future():
        print('future ')


def main():
    task1.join()
    task2.join()
    th = task3()
    th.join()

    py3()
    pass


if __name__ == '__main__':
    main()

