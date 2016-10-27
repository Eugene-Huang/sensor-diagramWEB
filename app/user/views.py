# -*- coding: utf8 -*-

from flask import render_template
from flask_login import login_required
from datetime import datetime
from ..fetch_temp import view_temp_data, get_latesttemp, get_lastdaytemp, get_lastweektemp, get_alltemp
from ..fetch_humidity import view_humidity_data, get_latesthumidity, get_lastdayhumidity, get_lastweekhumidity, get_allhumidity
from ..fetch_light import view_light_data, get_latestlight, get_lastdaylight, get_lastweeklight, get_alllight
from ..fetch_mqtt import get_mqtttemp, get_mqtthumidity, get_mqttlight
from . import user


current_time = datetime.utcnow()

# 温度

# 温度监控，可视化数据


@user.route('/tempview', methods=['GET', 'POST'])
@login_required
def tempView():
    data = view_temp_data()
    return render_template('temperature.html', data=data, current_time=current_time)

# get the latest data use ajax


@user.route('/newtemp', methods=['GET'])
@login_required
def newTemp():
    # data = get_latesttemp()
    data = get_mqtttemp()
    return data

# 前一天数据


@user.route('/lastdaytemp', methods=['GET'])
@login_required
def lastdayTemp():
    data = get_lastdaytemp()
    return data

# 上一周数据


@user.route('/lastweektemp', methods=['GET'])
@login_required
def lastweekTemp():
    data = get_lastweektemp()
    return data


@user.route('/alltemp', methods=['GET'])
@login_required
def allTemp():
    data = get_alltemp()
    return data

# # 湿度


@user.route('/humview', methods=['GET', 'POST'])
@login_required
def humView():
    data = view_humidity_data()
    return render_template('humidity.html', data=data, current_time=current_time)


@user.route('/newhum', methods=['GET'])
@login_required
def newHum():
    # data = get_latesthumidity()
    data = get_mqtthumidity()
    return data


@user.route('/lastdayhum', methods=['GET'])
@login_required
def lastdayHum():
    data = get_lastdayhumidity()
    return data


@user.route('/lastweekhum', methods=['GET'])
@login_required
def lastweekHum():
    data = get_lastweekhumidity()
    return data


@user.route('/allhum', methods=['GET'])
@login_required
def allHum():
    data = get_allhumidity()
    return data


# # 光照值


@user.route('/lightview', methods=['GET', 'POST'])
@login_required
def lightView():
    data = view_light_data()
    return render_template('light.html', data=data, current_time=current_time)


@user.route('/newlight', methods=['GET'])
@login_required
def newLight():
    # data = get_latestlight()
    data = get_mqttlight()
    return data


@user.route('/lastdaylight', methods=['GET'])
@login_required
def lastdayLight():
    data = get_lastdaylight()
    return data


@user.route('/lastweeklight', methods=['GET'])
@login_required
def lastweekLight():
    data = get_lastweeklight()
    return data


@user.route('/alllight', methods=['GET'])
@login_required
def allLight():
    data = get_alllight()
    return data
