# -*- coding: utf8 -*-

from sqlalchemy.types import TIMESTAMP
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app
from . import db, login_manager

# 模型

# 权限等级


class Permission:
    COMMONUSER = 0x01
    ADMINISTER = 0x02
    ROOT = 0x04


# 用户数据表


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    # 插入角色

    @staticmethod
    def insert_roles():
        roles = {
            'Student': Permission.COMMONUSER,
            'Teacher': Permission.COMMONUSER,
            'Admin': Permission.ADMINISTER,
            'Root': Permission.ROOT
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r> % self.name'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property  # 设定名为password的只写属性，读取值则报错
    def password(self, password):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):  # 转换为hash
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):  # 验证hash密码
        return check_password_hash(self.password_hash, password)

    def __init__(self, **kwargs):

        super(User, self).__init__(**kwargs)
        # 初始化时默认定义root角色
        if self.role is None:
            if self.username == current_app.config['WEB_ADMIN']:
                self.role = Role.query.filter_by(permissions=0x04).first()
        # 检查用户是否具有指定的权限

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def is_root(self):
        return self.can(Permission.ROOT)

    @staticmethod
    def insert_users():
        admin_user = User(email='admin@test.com', username='admin01',
                          password='testadmin', role=Role.query.filter_by(name='Admin').first())
        student_user = User(email='student@test.com', username='student01',
                            password='teststudent', role=Role.query.filter_by(name='Student').first())
        teacher_user = User(email='teacher@test.com', username='teacher01',
                            password='testteacher', role=Role.query.filter_by(name='Teacher').first())
        db.session.add_all([admin_user, student_user, teacher_user])
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.username


# 加载用户的回调函数


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# MQTT


class recvmqtt(db.Model):
    __tablename__ = 'recvmqtt'
    id = db.Column(db.Integer, primary_key=True)
    sensor_type = db.Column(db.String(20))
    value = db.Column(db.Float)
    sensor_node = db.Column(db.String(20))
    recv_time = db.Column(db.DateTime)
    insert_time = db.Column(TIMESTAMP, server_default=func.now())


# 温度


class temperature(db.Model):
    __tablename__ = 'temperature'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    unit = db.Column(db.String(10))
    node = db.Column(db.String(20))
    time = db.Column(TIMESTAMP, server_default=func.now())
    address = db.Column(db.String(80))

# 湿度


class humidity(db.Model):
    __tablename__ = 'humidity'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    unit = db.Column(db.String(10))
    node = db.Column(db.String(20))
    time = db.Column(TIMESTAMP, server_default=func.now())
    address = db.Column(db.String(80))

# 光照值


class luminousIntensity(db.Model):
    __tablename__ = 'luminous_intensity'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    unit = db.Column(db.String(10))
    node = db.Column(db.String(20))
    time = db.Column(TIMESTAMP, server_default=func.now())
    address = db.Column(db.String(80))

# #数字量

# 人体红外


class humanInfrared(db.Model):
    __tablename__ = 'human_infrared'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean)
    node = db.Column(db.String(20))
    time = db.Column(TIMESTAMP, server_default=func.now())
    address = db.Column(db.String(80))

# 火焰


class fire(db.Model):
    __tablename__ = 'fire'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean)
    node = db.Column(db.String(20))
    time = db.Column(TIMESTAMP, server_default=func.now())
    address = db.Column(db.String(80))

# 烟雾


class smoke(db.Model):
    __tablename__ = 'smoke'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean)
    node = db.Column(db.String(20))
    time = db.Column(TIMESTAMP, server_default=func.now())
    address = db.Column(db.String(80))
