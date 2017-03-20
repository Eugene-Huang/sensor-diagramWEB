# -*- coding: utf8 -*-

from extensions import celery
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO

# import sys
# sys.path.append('../')
# from config import BaseConfig

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
socketio = SocketIO()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
# 登录视图
# 未登录的用户尝试访问一个login_required 装饰的视图，
# 闪现一条消息， 重定向到此
# login_manager.login_view = 'main.login' # 不设置则默认返回401错误
# 自定义闪现消息，default = 'Please log in to acsess this page'
login_manager.login_message = u'Please log in first'
# 设置闪现错误消息的类别
login_manager.login_message_category = 'info'


def creat_app(config_name):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config_name)  # 从config.py读取配置文件

    flask_app.secret_key = flask_app.config['SECRET_KEY']
    flask_app.config['SQLALCHEMY_DATABASE_URI']  # 连接数据库
    flask_app.config['CELERY_IMPORTS'] = ('app.celery_tasks',)  # 手动注册celery任务
    flask_app.config['CELERY_BROKER_URL']  # celery中间人配置
    flask_app.config['CELERY_RESULT_BACKEND']

    bootstrap.init_app(flask_app)
    moment.init_app(flask_app)
    db.init_app(flask_app)
    login_manager.init_app(flask_app)
    socketio.init_app(flask_app)
    celery.init_app(flask_app)

    from .main import main as main_blueprint  # 注册蓝图
    flask_app.register_blueprint(main_blueprint)

    from .admin import admin as admin_blueprint
    flask_app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .user import user as user_blueprint
    flask_app.register_blueprint(user_blueprint, url_prefix='/user')

    return flask_app
