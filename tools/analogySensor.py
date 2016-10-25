# -*- coding: UTF-8 -*-
# --------------------------------------
# 模拟传感器采集数据并上传数据库
# 自行设置程序运行的时间（minutes）
# 和插入数据相隔的时间（seconds）
# --------------------------------------

import MySQLdb
import random
import time
import sys
import argparse
from threading import Thread
from datetime import datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

sys.path.append("..")  # 为了导入上级目录中的模块
from app import models


app = Flask(__name__)

# 连接数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/smarthome'
# 禁止显示傻逼sqlalchemy warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

# command shell arguments
parser = argparse.ArgumentParser()
parser.add_argument('sensor_type', help='Input sensor type,\
                    "temp => temperature | "humi" => humidity\
                    | "lumi" => luminousIntensity | "fire" | \
                    "smoke" | "human" ==> human infrared | all')
parser.add_argument('-r', '--run_minute', type=int, default=1,
                    help='Input minutes you want to run this py')
parser.add_argument('-d', '--delay_seconds', type=int, default=2,
                    help='Input seconds you want to delay process')
args = parser.parse_args()

MINS = args.run_minute  # 参数：运行时间
DELAY = args.delay_seconds  # 参数：延迟时长
SENSOR = args.sensor_type  # 传感器类型


# 模型实例
humidity = models.humidity
temperature = models.temperature
luminousIntensity = models.luminousIntensity
fire = models.fire
smoke = models.smoke
human_infrared = models.humanInfrared


def insert_huimidity():
    # 确定执行多少分钟
    current_time = datetime.now()  # 获取当前时间
    update_time = current_time + timedelta(minutes=MINS)  # 截止时间
    insertID = 1
    while current_time < update_time:
        # 插入的数据
        VALUE = float(format(random.uniform(60, 90), '.1f'))  # 模仿湿度
        UNIT = '%'
        # NODE = int(format(random.randint(1, 20), '03'))  # 模仿传感器节点
        NODE = 1
        ADDRESS = random.choice(['home', 'school'])  # 模仿位置

        Humi = humidity(value=VALUE, unit=UNIT, node=NODE,
                        address=ADDRESS)
        try:
            db.session.add(Humi)
            db.session.commit()
            print 'Insert successful  [', current_time, '] [', insertID, ']'
        except MySQLdb.Error as e:
            raise e

        time.sleep(DELAY)  # delay one seconds
        current_time = datetime.now()  # 更新当前时间
        insertID += 1  # 更新insertID


def insert_temperature():
    # 确定执行多少分钟
    current_time = datetime.now()  # 获取当前时间
    update_time = current_time + timedelta(minutes=MINS)  # 截止时间
    insertID = 1
    while current_time < update_time:
        # 插入的数据
        VALUE = float(format(random.uniform(20, 35), '.1f'))  # 模仿湿度
        UNIT = 'ºC'
        # NODE = int(format(random.randint(1, 20), '03'))  # 模仿传感器节点
        NODE = 1
        ADDRESS = random.choice(['home', 'school'])  # 模仿位置

        Temp = temperature(value=VALUE, unit=UNIT, node=NODE,
                           address=ADDRESS)
        try:
            db.session.add(Temp)
            db.session.commit()
            print 'Insert successful  [', current_time, '] [', insertID, ']'
        except MySQLdb.Error as e:
            raise e

        time.sleep(DELAY)  # delay one seconds
        current_time = datetime.now()  # 更新当前时间
        insertID += 1  # 更新insertID


def insert_luminous_Intensity():
    # 确定执行多少分钟
    current_time = datetime.now()  # 获取当前时间
    update_time = current_time + timedelta(minutes=MINS)  # 截止时间
    insertID = 1
    while current_time < update_time:
        # 插入的数据
        VALUE = float(format(random.uniform(200, 1000), '.1f'))  # 模仿湿度
        UNIT = 'Lux'
        NODE = 1  # 模仿传感器节点
        ADDRESS = random.choice(['home', 'school'])  # 模仿位置

        Lumi = luminousIntensity(value=VALUE, unit=UNIT, node=NODE,
                                 address=ADDRESS)
        try:
            db.session.add(Lumi)
            db.session.commit()
            print 'Insert successful  [', current_time, '] [', insertID, ']'
        except MySQLdb.Error as e:
            raise e

        time.sleep(DELAY)  # delay one seconds
        current_time = datetime.now()  # 更新当前时间
        insertID += 1  # 更新insertID


def insert_fire():
    # 确定执行多少分钟
    current_time = datetime.now()  # 获取当前时间
    update_time = current_time + timedelta(minutes=MINS)  # 截止时间
    insertID = 1
    while current_time < update_time:
        STATUS = random.choice([True, False])
        ADDRESS = random.choice(['home', 'school'])
        NODE = int(format(random.randint(1, 5), '03'))
        Fire = fire(status=STATUS, node=NODE, address=ADDRESS)
        try:
            db.session.add(Fire)
            db.session.commit()
            print 'Insert successful  [', current_time, '] [', insertID, ']'
        except MySQLdb.Error as e:
            raise e
        time.sleep(DELAY)  # delay one seconds
        current_time = datetime.now()  # 更新当前时间
        insertID += 1  # 更新insertID


def insert_smoke():
    insertID = 1
    current_time = datetime.now()  # 获取当前时间
    update_time = current_time + timedelta(minutes=MINS)  # 截止时间
    while current_time < update_time:
        STATUS = random.choice([True, False])
        ADDRESS = random.choice(['home', 'school'])
        NODE = int(format(random.randint(1, 5), '03'))
        Smoke = smoke(status=STATUS, node=NODE, address=ADDRESS)
        try:
            db.session.add(Smoke)
            db.session.commit()
            print 'Insert successful  [', current_time, '] [', insertID, ']'
            # NODE += 1
        except MySQLdb.Error as e:
            raise e
        time.sleep(DELAY)  # delay one seconds
        current_time = datetime.now()  # 更新当前时间
        insertID += 1


def insert_human_infrared():
    insertID = 1
    current_time = datetime.now()  # 获取当前时间
    update_time = current_time + timedelta(minutes=MINS)  # 截止时间
    while current_time < update_time:
        STATUS = random.choice([True, False])
        ADDRESS = random.choice(['home', 'school'])
        NODE = int(format(random.randint(1, 5), '03'))
        HI = human_infrared(status=STATUS, node=NODE, address=ADDRESS)
        try:
            db.session.add(HI)
            db.session.commit()
            print 'Insert successful  [', current_time, '] [', insertID, ']'
            # NODE += 1
        except MySQLdb.Error as e:
            raise e
        time.sleep(DELAY)  # delay one seconds
        current_time = datetime.now()  # 更新当前时间
        insertID += 1


def main():
    thread1 = Thread(target=insert_temperature)
    thread2 = Thread(target=insert_huimidity)
    thread3 = Thread(target=insert_luminous_Intensity)
    thread4 = Thread(target=insert_fire)
    thread5 = Thread(target=insert_smoke)
    thread6 = Thread(target=insert_human_infrared)
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()


if __name__ == '__main__':
    try:
        if SENSOR == 'temp':
            insert_temperature()
            sys.exit(0)
        if SENSOR == 'humi':
            insert_huimidity()
            sys.exit(0)
        if SENSOR == 'lumi':
            insert_luminous_Intensity()
            sys.exit(0)
        if SENSOR == 'fire':
            insert_fire()
            sys.exit(0)
        if SENSOR == 'smoke':
            insert_smoke()
            sys.exit(0)
        if SENSOR == 'human':
            insert_human_infrared()
            sys.exit(0)
        if SENSOR == 'all':
            main()
        else:
            print '\n\t[Error]: Pelase input correct argument\n\tType "-h" or "--help" for help\n'
    except KeyboardInterrupt:
        print '\n[Exit]: Stopped inserting data '
