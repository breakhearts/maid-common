"""
Logger wrapper
"""
import logging
import logging.handlers
import os
import sys
from utility import wise_mk_dir

class Logger(object):
    def __init__(self, log_root, module):
        log_path = os.path.join(log_root, module)
        if not os.path.exists(log_path):
            wise_mk_dir(log_path)
        get_logger_file_path = lambda x: os.path.join(log_path, x)
        debug_file_handler = logging.handlers.TimedRotatingFileHandler(get_logger_file_path("debug"), when="D", interval=1)
        formatter = logging.Formatter("[%(asctime)s]%(message)s")
        debug_file_handler.setFormatter(formatter)
        error_file_handler = logging.handlers.TimedRotatingFileHandler(get_logger_file_path("error"), when="D", interval=1)
        error_file_handler.setFormatter(formatter)
        exception_file_handler = logging.handlers.TimedRotatingFileHandler(get_logger_file_path("exception"), when="D", interval=1)
        exception_file_handler.setFormatter(formatter)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        self.debug_logger = logging.getLogger("%s" % module)
        self.debug_logger.setLevel(logging.DEBUG)
        self.debug_logger.addHandler(debug_file_handler)
        self.debug_logger.addHandler(console_handler)

        self.error_logger = logging.getLogger("error_%s" % module)
        self.error_logger.setLevel(logging.ERROR)
        self.error_logger.addHandler(error_file_handler)
        self.error_logger.addHandler(console_handler)

        self.exception_logger = logging.getLogger("exception_%s" % module)
        self.exception_logger.setLevel(logging.ERROR)
        self.exception_logger.addHandler(exception_file_handler)
        self.exception_logger.addHandler(console_handler)

    @staticmethod
    def get_head_info():
        try:
            raise Exception
        except:
            f = sys.exc_info()[2].tb_frame.f_back.f_back
            return '%s, %s, ' % (f.f_code.co_name, str(f.f_lineno))

    def debug(self, msg, *args):
        self.debug_logger.debug(msg, *args)

    def debug_fun(self, msg, *args):
        self.debug(Logger.get_head_info() + msg, *args)

    def debug_class_fun(self, cls, msg, *args):
        self.debug(cls + "," + Logger.get_head_info() + msg, *args)

    def error(self, msg, *args):
        self.error_logger.error(msg, *args)

    def exception(self, msg, *args):
        self.exception_logger.exception(msg, *args)

    def traceback(self):
        import traceback
        self.exception(traceback.format_exc())