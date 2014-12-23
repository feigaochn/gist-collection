import logging

logging.basicConfig(filename='logging_output.txt', level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s]: %(message)s')
logging.debug('This is a log.')
