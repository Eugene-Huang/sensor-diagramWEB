# -*- coding: utf8 -*-

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from datetime import datetime
import json
import time
from ..decorators import admin_required
from . import admin
from .. import db
from app.models import User, Role, fire, smoke, humanInfrared
from .forms import AddUserForm

current_time = datetime.utcnow()

# 控制台界面


@admin.route('/dashboard', methods=['GET', 'POST'])
@login_required
@admin_required
def dashboard():
    return render_template('dashboard.html',
                           current_time=current_time)

# 数字量传感器数据表格显示


@admin.route('/sensordata', methods=['GET', 'POST'])
@login_required
@admin_required
def sensorData():
    data = []
    fires = fire.query.group_by(fire.node).all()
    smokes = smoke.query.group_by(smoke.node).all()
    human = humanInfrared.query.group_by(humanInfrared.node).all()
    for f in fires:
        sensor = '火焰'
        row = {"sensor": sensor, "status": f.status,
               "node": f.node, "address": f.address}
        data.append(row)
    for s in smokes:
        sensor = '烟雾'
        row = {"sensor": sensor, "status": s.status,
               "node": s.node, "address": s.address}
        data.append(row)
    for h in human:
        sensor = '人体红外'
        row = {"sensor": sensor, "status": h.status,
               "node": h.node, "address": h.address}
    data = json.dumps(data)
    return data


# 用户管理

# 添加用户


@admin.route('/usermanage', methods=['GET', 'POST'])
@login_required
@admin_required
def userManage():
    form = AddUserForm()
    if form.validate_on_submit():
        role = form.role.data
        uid = Role.query.filter_by(name=role).first().id
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    role_id=uid)
        try:
            db.session.add(user)
            db.session.commit()
            flash('You have added a new user')
            return redirect(url_for('admin.userManage'))
        except:
            flash('Sorry, add failed')
    return render_template('usermanagement.html',
                           form=form, current_time=current_time)

# user info


@admin.route('/userinfo', methods=['GET', 'POST'])
@login_required
@admin_required
def userInfo():
    data = []
    users = User.query.all()
    for u in users:
        role = Role.query.filter(u.role_id == Role.id).first().name
        # row = [u.id, role, u.username, u.email]  # 数组
        row = {"id": u.id, "role": role,
               "username": u.username, "email": u.email}  # 对象
        data.append(row)
    data = json.dumps(data)
    return data

# 用户饼状图统计


@admin.route('/userchart', methods=['GET', 'POST'])
@login_required
@admin_required
def userChart():
    admin_list = []
    student_list = []
    teacher_list = []
    users = User.query.all()
    for u in users:
        role = Role.query.filter(u.role_id == Role.id).first().name
        if role == "Admin":
            admin_list.append(role)
        if role == "Student":
            student_list.append(role)
        if role == "Teacher":
            teacher_list.append(role)
    admin_length = float(len(admin_list))
    student_length = float(len(student_list))
    teacher_length = float(len(teacher_list))
    total = admin_length + student_length + teacher_length
    admin_percent = (admin_length / total) * 100
    student_percent = (student_length / total) * 100
    teacher_percent = (teacher_length / total) * 100

    chart_data = [["Admin", admin_percent], ["Student",
                                             student_percent], ["Teacher", teacher_percent]]
    return json.dumps(chart_data)

# 图表化显示数字量传感器数据


@admin.route('/viewdigital', methods=['GET', 'POST'])
@login_required
@admin_required
def viewDigital():
    if request.method == "POST":
        node = request.form['search']
        # 输入的节点号必须是整数
        try:
            int(node)
        except:
            flash(u'节点号必须是整数')

        data = json.dumps([getPieData(node), getLineData(node)])
        return render_template('view_digital.html', data=data, current_time=current_time)
    else:
        flash(u'没有数据可以显示，请搜索节点数据')
        return render_template('view_digital.html', current_time=current_time)


# @admin.route('/dgpie', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def getDgPie():
#     if request.method == "POST":
#         node = request.form['search']
#         return getPieData(node)
#     else:
#         return getPieData(1)


# @admin.route('/dgline', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def getDgLine():
#     if request.method == "POST":
#         node = request.form['search']
#         return getLineData(node)
#     else:
#         return getLineData(1)


# 按节点获取线图数据


def getLineData(node):
    data = []
    # 数据库查询
    fires = fire.query.filter(fire.node == node).order_by(fire.time).all()
    smokes = smoke.query.filter(smoke.node == node).order_by(smoke.time).all()
    human = humanInfrared.query.filter(
        humanInfrared.node == node).order_by(humanInfrared.time).all()
    fire_data = []
    smoke_data = []
    human_data = []
    # 处理火焰数据
    if fires:  # 是否有相应节点数据，没有置0
        for f in fires:
            if f.status is True:
                value = 1
            if f.status is False:
                value = -1
            tim = time.mktime((f.time).timetuple()) * 1000
            fire_data.append([tim, value])
    else:
        fire_data = 0
    data.append(fire_data)
    # 处理烟雾数据
    if smokes:
        for s in smokes:
            if s.status is True:
                value = 1
            if s.status is False:
                value = -1
            tim = time.mktime((f.time).timetuple()) * 1000
            smoke_data.append([value, tim])
    else:
        smoke_data = 0
    data.append(smoke_data)
    # 处理人体红外数据
    if human:
        for h in human:
            if h.status is True:
                value = 1
            if h.status is False:
                value = -1
            tim = time.mktime((f.time).timetuple()) * 1000
            human_data.append([value, tim])
    else:
        human_data = 0
    data.append(human_data)
    # 返回json
    return data

# 按节点获取饼图数据


def getPieData(node):
    data = []
    fire_true_list = []
    fire_false_list = []
    smoke_true_list = []
    smoke_false_list = []
    human_true_list = []
    human_false_list = []
    # 数据库查询
    fires = fire.query.filter(fire.node == node).all()
    smokes = smoke.query.filter(smoke.node == node).all()
    human = humanInfrared.query.filter(humanInfrared.node == node).all()
    # 数据处理
    if fires:  # 是否有相应节点数据，没有置0
        for f in fires:
            if f.status is True:
                fire_true_list.append(True)
            if f.status is False:
                fire_false_list.append(False)
        fire_true_length = float(len(fire_true_list))
        fire_false_length = float(len(fire_false_list))
        total = fire_true_length + fire_false_length
        fire_true_percent = (fire_true_length / total) * 100
        fire_false_percent = (fire_false_length / total) * 100
        fire_data = [['True', fire_true_percent],
                     ['False', fire_false_percent]]
    else:
        fire_data = 0
    data.append(fire_data)

    if smokes:
        for s in smokes:
            if s.status is True:
                smoke_true_list.append(True)
            if s.status is False:
                smoke_false_list.append(False)
        smoke_true_length = float(len(smoke_true_list))
        smoke_false_length = float(len(smoke_false_list))
        total = smoke_true_length + smoke_false_length
        smoke_true_percent = (smoke_true_length / total) * 100
        smoke_false_percent = (smoke_false_length / total) * 100
        smoke_data = [['True', smoke_true_percent],
                      ['False', smoke_false_percent]]
    else:
        smoke_data = 0
    data.append(smoke_data)

    if human:
        for h in human:
            if h.status is True:
                human_true_list.append(True)
            if h.status is False:
                human_false_list.append(False)
        human_true_length = float(len(human_true_list))
        human_false_length = float(len(human_false_list))
        total = human_true_length + human_false_length
        human_true_percent = (human_true_length / total) * 100
        human_false_percent = (human_false_length / total) * 100
        human_data = [['True', human_true_percent],
                      ['False', human_false_percent]]
    else:
        human_data = 0
    data.append(human_data)
    return data
