# Taken from Guido's slides from “Tulip: Async I/O for Python 3” by Guido # van
# Rossum, at LinkedIn, Mountain View, Jan 23, 2014

import asyncio


@coroutine
def fetch(host, port):
    r, w = yield from asyncio.open_connection(host, port)
    w.write(b'GET /HTTP/1.0\r\n\r\n ')
    while (yield from r.readline()).decode('latin-1').strip():
        pass
    body = yield from r.read()
    return body


@coroutine
def start():
    data = yield from fetch('python.org', 80)
    print(data.decode('utf-8'))
