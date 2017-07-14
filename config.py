# coding: utf-8
class Config(object):
    VERSION = "1.0.0"
    DEBUG = False
    SECRET_KEY = 'secret'


class ProdConfig(Config):
    DEBUG = False


class DevConfig(Config):
    DEBUG = True
