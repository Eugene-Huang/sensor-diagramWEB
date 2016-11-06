# -*- coding: utf8 -*-

# 默认配置文件


class Config(object):
    DEBUG = False
    SECRET_KEY = 'cDCDad5dFee25af54ED3Fd258A77cf2F'
    SQLALCHEMY_DATABASE_URI = 'mysql://zhifeng:zhifengmysql@115.159.190.88/smarthome'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WEB_ADMIN = 'zhifeng523'

# 生产环境下配置


class ProductionConfig(Config):
    DEBUG = False

# 开发环境下配置


class DevelopmentConfig(Config):
    DEBUG = True
