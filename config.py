# -*- coding: utf8 -*-

import ConfigParser

config = ConfigParser.ConfigParser()
config.read('db.conf')
dbhost = config.get('db', 'DBHOST')
dbname = config.get('db', 'DBNAME')
dbuser = config.get('db', 'DBUSER')
passwd = config.get('db', 'PASSWORD')

# 默认配置文件


class Config(object):
    DEBUG = False
    SECRET_KEY = 'cDCDad5dFee25af54ED3Fd258A77cf2F'
    SQLALCHEMY_DATABASE_URI = 'mysql://{0}:{1}@{2}/{3}'.format(dbuser, passwd, dbhost, dbname)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WEB_ADMIN = 'zhifeng523'

# 生产环境下配置


class ProductionConfig(Config):
    DEBUG = False

# 开发环境下配置


class DevelopmentConfig(Config):
    DEBUG = True
