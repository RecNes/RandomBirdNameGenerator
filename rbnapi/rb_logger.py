# coding: utf-8
import logging
import os
from logging import handlers
from datetime import date
from RandomBirdNameAPI.settings import BASE_DIR

__author__ = 'Sencer Hamarat'


class Loglayici:
    def __init__(self, log_name, level='INFO', log_dir='logs', log_format=None, handler=None):
        """
        log_adi: log_dosya adı
        self.level: log seviyesi. Geçerli seviyeler: CRITICAL, ERROR, WARNING, INFO, DEBUG
        log_dir: log dosyasinin yazilacaği dizin. Ön tanımlı konum <proje_dizini>/log/
        log_format: verilen log formatı kullanılır, aksi halde varsayılan format kullanılır
        handler: TODO
        """
        self.log_name = log_name
        self.loger = None
        self.formatter = None
        self.handler = handler
        self.log_dir = "{}/{}".format(BASE_DIR, log_dir)
        self.log_format = log_format
        self.level = level.upper()
        self.log_format = u"%(asctime)s %(levelname)s %(name)s %(process)d %(threadName)s %(module)s: " \
                          u"%(lineno)d %(funcName)s() %(message)s\r\n"

        self.__set_level()
        self.__set_format()
        self.__setup_handler()

    def __set_level(self):
        if self.level not in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']:
            raise Exception(u"{} is not valid log level".format(self.level))
        self.level = 'DEBUG' if self.level is None else self.level

    def __set_format(self):
        if self.log_format:
            self.log_format = self.log_format
        self.formatter = logging.Formatter(self.log_format)

    def __setup_handler(self):
        if not os.path.exists(self.log_dir):
            os.mkdir(self.log_dir)
        _filename = "{}/{}.log".format(self.log_dir, self.log_name)
        self.handler = handlers.WatchedFileHandler(_filename, mode="a", encoding="utf-8")
        self.handler.setFormatter(self.formatter)

    def make_loger(self):
        _loger = logging.getLogger(self.log_name)
        _loger.setLevel(getattr(logging, self.level))
        _loger.addHandler(self.handler)
        self.loger = _loger
        return _loger


day = date.today().strftime('%d_%m_%Y')
log = Loglayici('RandomBirdNameAPI-%s' % day, ).make_loger()
