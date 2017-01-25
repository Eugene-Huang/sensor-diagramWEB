# # -*- coding: utf8 -*-

from flask import render_template, request
from flask_login import login_required
from datetime import datetime
import time
import json
from . import user
from .. import connectDB


current_time = datetime.utcnow()

db = connectDB.ConnectDB()
conn = db.connect()
cur = conn.cursor()


# ========================= 温度显示页面


@user.route('/temperature', methods=['GET', 'POST'])
@login_required
def temperature():
    return render_template('temperature.html', current_time=current_time)


@user.route('/tempview', methods=['GET', 'POST'])
@login_required
def tempView():
    node = request.form.get('node', 1, type=int)
    sql = 'SELECT time, value FROM temperature WHERE node={} LIMIT 20'.format(
        node)
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        data = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
                for item in result]
        return json.dumps(data)
    else:
        return json.dumps([0, 0])

# ---------------------最新一条温度数据


@user.route('/newtemp', methods=['GET', 'POST'])
@login_required
def newTemp():
    node = request.args.get('node', 1, type=int)
    sql = 'SELECT time, value FROM temperature WHERE node={} ORDER BY time LIMIT 1'.format(
        node)
    cur.execute(sql)
    result = cur.fetchone()
    if result:
        data = [time.mktime(result[0].timetuple()) * 1000, result[1]]
        return json.dumps(data)
    else:
        return json.dumps([0, 0])

# ------------------------前一天温度数据


@user.route('/lastdaytemp', methods=['GET', 'POST'])
@login_required
def lastdayTemp():
    node = request.args.get('node', 1, type=int)
    sql = 'SELECT time, value FROM temperature WHERE node={} AND DATE(time) = DATE_SUB(CURDATE(), INTERVAL 1 day)'.format(
        node)
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        data = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
                for item in result]
        return json.dumps(data)
    else:
        return json.dumps([0, 0])

# -------------------上一周温度数据


@user.route('/lastweektemp', methods=['GET', 'POST'])
@login_required
def lastweekTemp():
    minv = []
    maxv = []
    node = request.args.get('node', 1, type=int)
    sql = 'SELECT time, value FROM temperature WHERE node={} AND YEARWEEK(date_format(time, "%Y-%m-%d")) = YEARWEEK(now()) - 1'.format(
        node)
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        mon = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
               for item in result if item[0].isoweekday() == 1]
        tue = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
               for item in result if item[0].isoweekday() == 2]
        wed = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
               for item in result if item[0].isoweekday() == 3]
        thur = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
                for item in result if item[0].isoweekday() == 4]
        fri = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
               for item in result if item[0].isoweekday() == 5]
        sat = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
               for item in result if item[0].isoweekday() == 6]
        sun = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
               for item in result if item[0].isoweekday() == 7]
        for workday in [mon, tue, wed, thur, fri, sat, sun]:
            if len(workday):
                minv.append(min(workday, key=lambda x: x[1]))
                maxv.append(max(workday, key=lambda x: x[1]))
        return json.dumps([minv, maxv])
    else:
        return json.dumps([0, 0])

# ---------------------全部温度数据


@user.route('/alltemp', methods=['GET', 'POST'])
@login_required
def allTemp():
    node = request.args.get('node', 1, type=int)
    sql = 'SELECT time, value FROM temperature WHERE node={}'.format(
        node)
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        data = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
                for item in result]
        return json.dumps(data)
    else:
        return json.dumps([0, 0])

# =========================== 湿度显示页面


@user.route('/humidity', methods=['GET', 'POST'])
@login_required
def humidity():
    return render_template('humidity.html',
                           current_time=current_time)


@user.route('/humview', methods=['GET', 'POST'])
@login_required
def humView(node=1):
    sql = 'SELECT time, value FROM humidity WHERE node={} LIMIT 20'.format(
        node)
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        data = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
                for item in result]
        return json.dumps(data)
    else:
        return json.dumps([0, 0])


# ---------------------最新一条湿度数据


@user.route('/newhum', methods=['GET', 'POST'])
@login_required
def newHum(node=1):
    sql = 'SELECT time, value FROM humidity WHERE node={} ORDER BY time LIMIT 1'.format(
        node)
    cur.execute(sql)
    result = cur.fetchone()
    if result:
        data = [time.mktime(result[0].timetuple()) * 1000, result[1]]
        return json.dumps(data)
    else:
        return json.dumps([0, 0])


# ---------------------上一天湿度数据


@user.route('/lastdayhum', methods=['GET', 'POST'])
@login_required
def lastdayHum(node=1):
    sql = 'SELECT time, value FROM humidity WHERE node={} AND DATE(time) = DATE_SUB(CURDATE(), INTERVAL 1 day)'.format(
        node)
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        data = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
                for item in result]
        return json.dumps(data)
    else:
        return json.dumps([0, 0])

# ---------------------上一周湿度数据


@user.route('/lastweekhum', methods=['GET', 'POST'])
@login_required
def lastweekHum(node=1):
    minv = []
    maxv = []
    sql = 'SELECT time, value FROM humidity WHERE node={} AND YEARWEEK(date_format(time, "%Y-%m-%d")) = YEARWEEK(now()) - 1'.format(
        node)
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        mon = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
               for item in result if item[0].isoweekday() == 1]
        tue = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
               for item in result if item[0].isoweekday() == 2]
        wed = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
               for item in result if item[0].isoweekday() == 3]
        thur = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
                for item in result if item[0].isoweekday() == 4]
        fri = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
               for item in result if item[0].isoweekday() == 5]
        sat = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
               for item in result if item[0].isoweekday() == 6]
        sun = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
               for item in result if item[0].isoweekday() == 7]
        for workday in [mon, tue, wed, thur, fri, sat, sun]:
            if len(workday):
                minv.append(min(workday, key=lambda x: x[1]))
                maxv.append(max(workday, key=lambda x: x[1]))
        return json.dumps([minv, maxv])
    else:
        return json.dumps([0, 0])


@user.route('/allhum', methods=['GET', 'POST'])
@login_required
def allHum(node=1):
    sql = 'SELECT time, value FROM humidity WHERE node={}'.format(
        node)
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        data = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
                for item in result]
        return json.dumps(data)
    else:
        return json.dumps([0, 0])


# ============================ 光照显示页面

@user.route('/lux', methods=['GET', 'POST'])
@login_required
def lux():
    return render_template('light.html',
                           current_time=current_time)


@user.route('/lightview', methods=['GET', 'POST'])
@login_required
def lightView(node=1):
    sql = 'SELECT time, value FROM luminous_intensity WHERE node={} LIMIT 20'.format(
        node)
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        data = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
                for item in result]
        return json.dumps(data)
    else:
        return json.dumps([0, 0])


# ---------------------最新一条光照值数据


@user.route('/newlight', methods=['GET', 'POST'])
@login_required
def newLight(node=1):
    sql = 'SELECT time, value FROM luminous_intensity WHERE node={} ORDER BY time LIMIT 1'.format(
        node)
    cur.execute(sql)
    result = cur.fetchone()
    if result:
        data = [time.mktime(result[0].timetuple()) * 1000, result[1]]
        return json.dumps(data)
    else:
        return json.dumps([0, 0])

# ---------------------上一天光照值数据


@user.route('/lastdaylight', methods=['GET', 'POST'])
@login_required
def lastdayLight(node=1):
    sql = 'SELECT time, value FROM luminous_intensity WHERE node={} AND DATE(time) = DATE_SUB(CURDATE(), INTERVAL 1 day)'.format(
        node)
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        data = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
                for item in result]
        return json.dumps(data)
    else:
        return json.dumps([0, 0])

# ---------------------上一周光照值数据


@user.route('/lastweeklight', methods=['GET', 'POST'])
@login_required
def lastweekLight(node=1):
    minv = []
    maxv = []
    sql = 'SELECT time, value FROM luminous_intensity WHERE node={} AND YEARWEEK(date_format(time, "%Y-%m-%d")) = YEARWEEK(now()) - 1'.format(
        node)
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        mon = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
               for item in result if item[0].isoweekday() == 1]
        tue = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
               for item in result if item[0].isoweekday() == 2]
        wed = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
               for item in result if item[0].isoweekday() == 3]
        thur = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
                for item in result if item[0].isoweekday() == 4]
        fri = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
               for item in result if item[0].isoweekday() == 5]
        sat = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
               for item in result if item[0].isoweekday() == 6]
        sun = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
               for item in result if item[0].isoweekday() == 7]
        for workday in [mon, tue, wed, thur, fri, sat, sun]:
            if len(workday):
                minv.append(min(workday, key=lambda x: x[1]))
                maxv.append(max(workday, key=lambda x: x[1]))
        return json.dumps([minv, maxv])
    else:
        return json.dumps([0, 0])


@user.route('/alllight', methods=['GET', 'POST'])
@login_required
def allLight(node=1):
    sql = 'SELECT time, value FROM luminous_intensity WHERE node={}'.format(
        node)
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        data = [[time.mktime(item[0].timetuple()) * 1000, item[1]]
                for item in result]
        return json.dumps(data)
    else:
        return json.dumps([0, 0])


if __name__ == '__main__':
    pass
