# -*- coding: UTF-8 -*-

import json
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from datetime import datetime
from sqlalchemy import desc
from . import main
# from .. import db
from ..models import User, Role, temperature, humidity

current_time = datetime.utcnow()


# redirect to home page
@main.route('/')
def index():
    return redirect(url_for('.welcome'))


# Welcome
@main.route('/welcome')
def welcome():
    return render_template('index.html',
                           current_time=current_time)


# Home page
@main.route('/home')
def home():
    return render_template('home.html',
                           current_time=current_time)

# Page about contact us


@main.route('/contact')
def contact():
    return render_template('contact.html',
                           current_time=current_time)


# login
@main.route('/login', methods=['GET', 'POST'])
def login():
    # 前端模版上获取用户输入数据
    if request.method == 'POST':
        uname = request.form['username']
        passwd = request.form['password']
        # 在数据库中查找用户对象
        user = User.query.filter_by(username=uname).first()
        if user is None:
            flash(u'Incorrect username', 'failed')
        elif user.verify_password(passwd) is None:
            flash(u'Incorrect password', 'failed')
        else:
            login_user(user)  # 用户登录
            flash(u'You are logged in, Welcome, {0}'.format(
                user.username), 'sucessed')
            # 管理员角色对象
            admin = Role.query.filter_by(name='Admin').first()
            if user.role_id == admin.id:  # 管理员用户登录即转到控制台页面
                return redirect(request.args.get('next') or
                                url_for('admin.dashboard'))
            # 普通账户转到图表页面
            return redirect(request.args.get('next') or
                            url_for('user.tempView'))
    return render_template('login.html',
                           current_time=current_time)

# logout


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'You were logged out', 'sucessed')
    return redirect(url_for('.login'))

# 首页温湿度显示


@main.route('/indexdata', methods=['GET'])
def indexData():
    temp = temperature.query.order_by(
        desc(temperature.time)).filter_by(node=1).first()
    humi = humidity.query.order_by(
        desc(humidity.time)).filter_by(node=1).first()
    if temp and humi:
        data = [temp.value, humi.value]
    elif temp is not None and humi is None:
        data = [temp.value, 00.0]
    elif humi is not None and temp is None:
        data = [00.0, humi.value]
    else:
        data = [00.0, 00.0]
    return json.dumps(data)


if __name__ == '__main__':
    main.run(debug=True)
