#!/usr/bin/env python3
# -*- coding: utf8 -*-


import os
import sqlite3
from functools import wraps
import time

import pandas as pd
import numpy as np


def timing(f) -> callable:
    """

    :rtype : callable
    """

    @wraps(f)
    def timed(*args, **kwargs):
        ts = time.time()
        result = f(*args, **kwargs)
        te = time.time()
        print('func: {}:\n\ttime: {} sec'.format(f.__name__, te - ts))
        return result

    return timed


def getpath(fn):
    return os.path.join(os.path.expanduser('~/Downloads'), fn)


df = pd.DataFrame(np.random.randn(10 ** 6, 2), columns=list('AB'))


@timing
def test_sqlite_write(df: pd.DataFrame):
    fn = getpath('test.sqlite')
    if os.path.exists(fn):
        os.remove(fn)
    sqlite_db = sqlite3.connect(fn)
    df.to_sql(name='test_table', con=sqlite_db)
    sqlite_db.close()


@timing
def test_sqlite_read():
    fn = getpath('test.sqlite')
    sqlite_db = sqlite3.connect(fn)
    pd.read_sql_query('select * from test_table', sqlite_db)
    sqlite_db.close()


@timing
def test_hdf_fixed_write(df):
    df.to_hdf(getpath('test_fixed.hdf'), 'test', mode='w')


@timing
def test_hdf_fixed_read():
    pd.read_hdf(getpath('test_fixed.hdf'), 'test')


@timing
def test_hdf_fixed_write_compress(df):
    df.to_hdf(getpath('test_fixed_compress.hdf'), 'test', mode='w', complib='blosc')


@timing
def test_hdf_fixed_read_compress():
    pd.read_hdf(getpath('test_fixed_compress.hdf'), 'test')


@timing
def test_hdf_table_write(df):
    df.to_hdf(getpath('test_table.hdf'), 'test', mode='w', format='table')


@timing
def test_hdf_table_read():
    pd.read_hdf(getpath('test_table.hdf'), 'test')


@timing
def test_hdf_table_write_compress(df):
    df.to_hdf(getpath('test_table_compress.hdf'), 'test', mode='w', complib='blosc', format='table')


@timing
def test_hdf_table_read_compress():
    pd.read_hdf(getpath('test_table_compress.hdf'), 'test')


@timing
def test_csv_write(df):
    df.to_csv(getpath('test.csv'), mode='w')


@timing
def test_csv_read():
    pd.read_csv(getpath('test.csv'), index_col=0)


def main():
    test_sqlite_write(df)
    test_sqlite_read()

    test_hdf_fixed_write(df)
    test_hdf_fixed_read()

    test_hdf_fixed_write_compress(df)
    test_hdf_fixed_read_compress()

    test_csv_write(df)
    test_csv_read()


if __name__ == '__main__':
    main()