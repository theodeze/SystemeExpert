import logging
import sys
import tempfile
import os
from logging.handlers import RotatingFileHandler

class Log:

    @staticmethod
    def init():
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        file_handler = RotatingFileHandler(tempfile.gettempdir() + '/se.log', 'a')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s'))
        logger.addHandler(file_handler)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)
        logger.addHandler(stream_handler)

        Log.debug("Initialisation")

    @staticmethod
    def print():
        with open(tempfile.gettempdir() + '/se.log', "r") as log:
            print(log.read(), end='')

    @staticmethod
    def remove_log():
        os.remove(tempfile.gettempdir() + '/se.log')

    @staticmethod
    def debug(chaine):
        logger = logging.getLogger()
        logger.debug(chaine)

    @staticmethod
    def info(chaine):
        logger = logging.getLogger()
        logger.info(chaine)

    @staticmethod
    def warning(chaine):
        logger = logging.getLogger()
        logger.warning(chaine)

    @staticmethod
    def error(chaine):
        logger = logging.getLogger()
        logger.error(chaine)

    @staticmethod
    def critical(chaine):
        logger = logging.getLogger()
        logger.critical(chaine)