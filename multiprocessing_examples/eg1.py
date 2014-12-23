#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Fei Gao
# Date: 23/6/14

import multiprocessing as mp


def cube(x):
    return x ** 3


def mp_eg():
    import random
    import string

    # define an output queue
    output = mp.Queue()

    def rand_string(length, pos, output):
        """
        generate a random string of number
        """
        rand_str = ''.join(random.choice(
            string.ascii_lowercase
            + string.ascii_uppercase
            + string.digits) for i in range(length))
        output.put((pos, rand_str))

    # setup a list of processes
    processes = [mp.Process(target=rand_string, args=(5, x, output)) for x in range(4)]

    # run processes
    for p in processes:
        p.start()

    # exit the completed processes
    for p in processes:
        p.join()

    # get process results from output queue
    results = [output.get() for p in processes]

    print(results)


def pool_eg():
    pools = mp.Pool(processes=4)

    print(list(pools.apply(cube, args=(x,)) for x in range(5)))
    print(pools.map(cube, range(5, 10)))

    print([p.get() for p in [pools.apply_async(cube, args=(x,)) for x in range(10)]])
    print(pools.map_async(cube, range(5, 15)).get())
    # pass


if __name__ == '__main__':
    mp_eg()
    pool_eg()
