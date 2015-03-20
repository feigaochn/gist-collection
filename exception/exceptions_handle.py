#!/usr/local/bin/python2

try:
    text = raw_input('Enter something --> ')
except EOFError:
    print('why did you do an EOF on me?')
except KeyboardInterrupt:
    print('You cancelled the operation.')
else:
    print('you entered {}'.format(text))
