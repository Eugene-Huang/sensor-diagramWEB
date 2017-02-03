# -*- coding: utf8 -*-

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from sqlalchemy import and_
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
    return json.dumps(data)


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
    return render_template('view_digital.html', current_time=current_time)


# 按节点获取线图数据

@admin.route('/digsensor/line', methods=['GET', 'POST'])
@login_required
@admin_required
def digsenor_line():
    data = []
    node = request.form.get('node', 1, type=int)
    fires = fire.query.filter(fire.node == node).order_by(fire.time).all()
    smokes = smoke.query.filter(smoke.node == node).order_by(smoke.time).all()
    human = humanInfrared.query.filter(
        humanInfrared.node == node).order_by(humanInfrared.time).all()
    fire_data = []
    smoke_data = []
    human_data = []
    # 是否有相应节点数据，没有置0
    if fires:
        for f in fires:
            value = 1 if f.status is True else -1
            fire_data.append([time.mktime((f.time).timetuple()) * 1000, value])
    else:
        fire_data = [0, 0]
    data.append(fire_data)
    if smokes:
        for s in smokes:
            value = 1 if f.status is True else -1
            smoke_data.append(
                [time.mktime((f.time).timetuple()) * 1000, value])
    else:
        smoke_data = [0, 0]
    data.append(smoke_data)
    if human:
        for h in human:
            value = 1 if f.status is True else -1
            human_data.append(
                [time.mktime((f.time).timetuple()) * 1000, value])
    else:
        human_data = [0, 0]
    data.append(human_data)
    return json.dumps(data)

# 按节点获取饼图数据


@admin.route('/digsensor/pie', methods=['GET', 'POST'])
@login_required
@admin_required
def digsensor_pie():
    data = []
    node = request.form.get('node', 1, type=int)
    # 数据库查询
    fire1len = len(fire.query.filter(
        and_(fire.node == node, fire.status == 1)).all())
    fire0len = len(fire.query.filter(
        and_(fire.node == node, fire.status == 0)).all())
    smoke1len = len(smoke.query.filter(
        and_(smoke.node == node, smoke.status == 1)).all())
    smoke0len = len(smoke.query.filter(
        and_(smoke.node == node, smoke.status == 0)).all())
    humanInfrared1len = len(humanInfrared.query.filter(
        and_(humanInfrared.node == node, humanInfrared.status == 1)).all())
    humanInfrared0len = len(humanInfrared.query.filter(
        and_(humanInfrared.node == node, humanInfrared.status == 0)).all())
    # 数据处理
    # 是否有相应节点数据，没有置0
    if fire0len or fire1len:
        fire1percent = (fire1len / float(fire1len + fire0len)) * 100
        fire0percent = (fire0len / float(fire1len + fire0len)) * 100
        fire_data = [['True', fire1percent],
                     ['False', fire0percent]]
    else:
        fire_data = [0, 0]
    data.append(fire_data)

    if smoke0len or smoke1len:
        smoke1percent = (smoke1len / float(smoke0len + smoke1len)) * 100
        smoke0percent = (smoke0len / float(smoke0len + smoke1len)) * 100
        smoke_data = [['True', smoke1percent],
                      ['False', smoke0percent]]
    else:
        smoke_data = [0, 0]
    data.append(smoke_data)

    if humanInfrared0len or humanInfrared1len:
        human1percent = (humanInfrared1len /
                         float(humanInfrared0len + humanInfrared1len)) * 100
        human0percent = (humanInfrared0len /
                         float(humanInfrared0len + humanInfrared1len)) * 100
        human_data = [['True', human1percent],
                      ['False', human0percent]]
    else:
        human_data = [0, 0]
    data.append(human_data)
    return json.dumps(data)
