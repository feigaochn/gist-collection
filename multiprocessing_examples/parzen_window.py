#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Fei Gao
# Date: 23/6/14

import multiprocessing as mp

import numpy as np


def parzen_estimation(x_samples, point_x, h):
    """
    Implementation of a hypercube kernel for Parzen-window estimation.

    :param x_samples: training sample, 'd x 1'-dim numpy array
    :param point_x: point for density estimation, 'd x 1'-dim numpy array
    :param h: window width
    :return: the predicted pdf as float
    """
    k_n = 0
    for row in x_samples:
        x_i = (point_x - row[:, np.newaxis]) / (h)
        for row in x_i:
            if np.abs(row) > (1 / 2):
                break
        else:
            k_n += 1
    return h, (k_n / len(x_samples)) / (h ** point_x.shape[1])


def parzenwindow_eg():
    """
    An example of Parzen Window method.

    >>> parzenwindow_eg()
    p(x) = (1, 0.3)
    """
    # samples within the cube
    X_inside = np.array([[0, 0, 0], [0.2, 0.2, 0.2], [0.1, -0.1, -0.3]])

    X_outside = np.array([[-1.2, 0.3, -0.3], [0.8, -0.82, -0.9], [1, 0.6, -0.7],
                          [0.8, 0.7, 0.2], [0.7, -0.8, -0.45], [-0.3, 0.6, 0.9],
                          [0.7, -0.6, -0.8]])

    point_x = np.array([[0], [0], [0]])
    X_all = np.vstack((X_inside, X_outside))

    print('p(x) =', parzen_estimation(X_all, point_x, h=1))


def serial(samples, x, widths):
    return [parzen_estimation(samples, x, w) for w in widths]


def multiprocess(processes, samples, x, widths):
    pool = mp.Pool(processes=processes)
    results = [pool.apply_async(parzen_estimation, args=(samples, x, w)) for w in widths]
    results = [p.get() for p in results]
    results.sort()  # to sort the results by input window width
    return results


np.random.seed(123)

# Generate random 2D-patterns
mu_vec = np.array([0, 0])
cov_mat = np.array([[1, 0], [0, 1]])
x_2Dgauss = np.random.multivariate_normal(mu_vec, cov_mat, 10000)

from scipy.stats import multivariate_normal

var = multivariate_normal(mean=[0, 0], cov=[[1, 0], [0, 1]])
print('actual probability density:', var.pdf([0, 0]))

widths = np.arange(0.1, 1.3, 0.1)
point_x = np.array([[0], [0]])

results = multiprocess(4, x_2Dgauss, point_x, widths)
for r in results:
    print('h = %s, p(x) = %s' % (r[0], r[1]))

# Based on the results, we can say that the best window-width
# would be h=1.1, since the estimated result is close to the
# actual result ~0.15915.

widths = np.linspace(1.0, 1.2, 100)


# def benchmark():

import timeit

print('begin benchmark')

benchmarks = list()

benchmarks.append(timeit.Timer('serial(x_2Dgauss, point_x, widths)',
                               'from __main__ import serial, x_2Dgauss, point_x, widths').timeit(number=1))
print('benchmark #1')

benchmarks.append(timeit.Timer('multiprocess(2, x_2Dgauss, point_x, widths)',
                               'from __main__ import multiprocess, x_2Dgauss, point_x, widths').timeit(number=1))
print('benchmark #2')

benchmarks.append(timeit.Timer('multiprocess(3, x_2Dgauss, point_x, widths)',
                               'from __main__ import multiprocess, x_2Dgauss, point_x, widths').timeit(number=1))
print('benchmark #3')

benchmarks.append(timeit.Timer('multiprocess(4, x_2Dgauss, point_x, widths)',
                               'from __main__ import multiprocess, x_2Dgauss, point_x, widths').timeit(number=1))
print('benchmark #4')

benchmarks.append(timeit.Timer('multiprocess(6, x_2Dgauss, point_x, widths)',
                               'from __main__ import multiprocess, x_2Dgauss, point_x, widths').timeit(number=1))
print('benchmark #5')

print('end benchmark')


def print_sysinfo():
    import platform

    print('\nPython version  :', platform.python_version())
    print('compiler        :', platform.python_compiler())

    print('\nsystem     :', platform.system())
    print('release    :', platform.release())
    print('machine    :', platform.machine())
    print('processor  :', platform.processor())
    print('CPU count  :', mp.cpu_count())
    print('interpreter:', platform.architecture()[0])
    print('\n\n')


def plot_results():
    from matplotlib import pyplot as plt

    global benchmarks

    n = 10000

    bar_labels = ['serial', '2', '3', '4', '6']

    fig = plt.figure(figsize=(10, 8))

    # plot bars
    y_pos = np.arange(len(benchmarks))
    plt.yticks(y_pos, bar_labels, fontsize=16)
    bars = plt.barh(y_pos, benchmarks,
                    align='center', alpha=0.4, color='g')

    # annotation and labels

    for ba, be in zip(bars, benchmarks):
        plt.text(ba.get_width() + 1.4, ba.get_y() + ba.get_height() / 2,
                 '{0:.2%}'.format(benchmarks[0] / be),
                 ha='center', va='bottom', fontsize=11)

    plt.xlabel('time in seconds for n=%s' % n, fontsize=14)
    plt.ylabel('number of processes', fontsize=14)
    t = plt.title('Serial vs. Multiprocessing via Parzen-window estimation', fontsize=18)
    plt.ylim([-1, len(benchmarks) + 0.5])
    plt.xlim([0, max(benchmarks) * 1.1])
    plt.vlines(benchmarks[0], -1, len(benchmarks) + 0.5, linestyles='dashed')
    plt.grid()

    plt.show()


print_sysinfo()
# plot_results()
