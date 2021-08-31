from settings import settings
import logging
from logging.handlers import RotatingFileHandler
import sys


class stdredirector():
    def __init__(self):
        self.data = []

    def write(self, s):
        if len(s) > 1:
            logger.info(s)

    def flush(self):
        pass


logger = logging.getLogger(settings['logging']['logappname'])
logger.setLevel(logging.INFO)
LogFile = RotatingFileHandler(settings['logging']['logfilepath'], maxBytes=1048576, backupCount=5)
formatter = logging.Formatter('%(asctime)s, %(name)s, %(levelname)s : %(message)s')
LogFile.setFormatter(formatter)
logger.addHandler(LogFile)
sys.stdout = x = stdredirector()
print('Logging started')
