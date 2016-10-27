# -*- coding: UTF-8 -*-

from connect_db import db  # model about connect db
import MySQLdb
import json
import time
from datetime import datetime


TABLE = 'recvmqtt'  # 查询的表
ITEM = 'value, insert_time'  # 查询的值
FILTER = ''            # 过滤器

current_time = datetime.now()

# 框架


def get_mqtt(sensor):
    FILTER = 'WHERE sensor_type = \'{0}\' ORDER BY insert_time DESC LIMIT 1'.format(sensor)
    sql = 'SELECT {0} FROM {1} '.format(ITEM, TABLE) + FILTER
    try:
        db.execute_db(sql)
        # db.conn.commit() # 如果没有设置自动提交事务 autocommit(True)
        # 手动提交事务
    except MySQLdb.Error as e:
        raise e
    else:
        row = db.cur.fetchone()  # fetchone()!!!才能把实时数据显示到前端图表
        if row:
            # js中时间戳为毫秒数，需* 1000
            # 查询出的时间戳转换为json格式
            # datetime.datime() -> 时间元组 -> float类型时间值
            data = [row[0], time.mktime(row[1].timetuple()) * 1000]
            data.reverse()  # 反转时间和温度值
        else:
            data = [0, time.mktime(current_time.timetuple()) * 1000]
            data.reverse()  # 反转时间和温度值
    return json.dumps(data)


def get_mqtttemp():
    return get_mqtt('temperature')


def get_mqtthumidity():
    return get_mqtt('humidity')


def get_mqttlight():
    return get_mqtt('light')


if __name__ == '__main__':
    print get_mqtttemp()
    print get_mqtthumidity()
