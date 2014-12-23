import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

fh = logging.FileHandler('logging_output.txt')
fh.setLevel(logging.WARNING)
fh.setFormatter(formatter)
logger.addHandler(fh)

sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(formatter)
logger.addHandler(sh)

logger.critical('This is a critical message.')
logger.error('This is an error message.')
logger.warning('This is a warning message.')
logger.info('This is an informative message.')
logger.debug('This is a low-level debug message.')
