# -*- coding: utf8 -*-

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from . import models
# from . import connectDB


bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
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
    app = Flask(__name__)
    app.config.from_object(config_name)  # 从config.py读取配置文件

    app.secret_key = app.config['SECRET_KEY']
    app.config['SQLALCHEMY_DATABASE_URI']  # 连接数据库

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint  # 注册蓝图
    app.register_blueprint(main_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')

    return app
