# -*- coding: utf8 -*-

import ConfigParser

config = ConfigParser.ConfigParser()
config.read('db.conf')
dbhost = config.get('db', 'DBHOST')
dbname = config.get('db', 'DBNAME')
dbuser = config.get('db', 'DBUSER')
passwd = config.get('db', 'PASSWORD')
rdhost = config.get('celery_redis', 'REDIS_HOST')
rdport = config.get('celery_redis', 'REDIS_PORT')
rdb = config.get('celery_redis', 'REDIS_DB')

# 默认配置文件


class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'cDCDad5dFee25af54ED3Fd258A77cf2F'
    SQLALCHEMY_DATABASE_URI = 'mysql://{0}:{1}@{2}/{3}'.format(dbuser, passwd, dbhost, dbname)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WEB_ADMIN = 'zhifeng523'
    CELERY_BROKER_URL = 'redis://{}:{}/{}'.format(rdhost, rdport, rdb)
    CELERY_RESULT_BACKEND = 'redis://{}:{}/{}'.format(rdhost, rdport, rdb)
    CELERY_TASK_SERIALIZER = 'json'

# 生产环境下配置


class ProductionConfig(BaseConfig):
    DEBUG = False

# 开发环境下配置


class DevelopmentConfig(BaseConfig):
    DEBUG = True
