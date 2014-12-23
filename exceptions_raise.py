#!/usr/local/bin/python2

class ShortInputException(Exception):
    '''A user-defined exception class.'''
    def __init__(self, length, atleast):
        Exception.__init__(self)
        self.length = length
        self.atleast = atleast

try:
    text = raw_input('Enter something --> ')
    if len(text) < 3:
        raise ShortInputException(len(text), 3)
    # other work can continue as usual here
except EOFError:
    print('why did you do an EOF on me?')
except ShortInputException as ex:
    print('ShortInputException: The input was '+\
            '{0} long, expected as least {1}')\
            .format(ex.length, ex.atleast)
except KeyboardInterrupt:
    print('You cancelled the operation.')
else:
    print('you entered {}'.format(text))
