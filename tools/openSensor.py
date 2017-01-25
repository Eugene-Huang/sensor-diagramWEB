# -*- coding: UTF-8 -*-
# --------------------------------------
# 模拟传感器采集数据并上传数据库
# 自行设置程序运行的时间（minutes）
# 和插入数据相隔的时间（seconds）
# 多线程，同时模拟六种不同类型传感器
# --------------------------------------

import random
import time
import argparse
import ConfigParser
import MySQLdb
import logging
from subprocess import os
from threading import Thread
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

sh = logging.StreamHandler()
fmt = '%(asctime)s - %(threadName)s - %(levelname)s > %(message)s'
formatter = logging.Formatter(fmt)
sh.setFormatter(formatter)

logger.addHandler(sh)

# 数据库连接


class ConnectDB(object):

    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read(os.path.join(os.path.dirname(os.getcwd()), 'db.conf'))
        self._dbhost = config.get('db', 'DBHOST')
        self._dbname = config.get('db', 'DBNAME')
        self._dbuser = config.get('db', 'DBUSER')
        self._passwd = config.get('db', 'PASSWORD')

    def connect(self):
        try:
            conn = MySQLdb.connect(
                self._dbhost, self._dbuser, self._passwd, self._dbname)
            logger.debug('connect mysql succesfully')
            conn.autocommit(True)
        except MySQLdb.Error as e:
            raise e
        return conn

# command shell arguments


parser = argparse.ArgumentParser()
parser.add_argument('-n', '--node', type=int, default=1,
                    help='Input sensor node number, default is node01')
parser.add_argument('-r', '--run_minute', type=int, default=1,
                    help='Input minutes you want to run this py, default is one miniute')
parser.add_argument('-d', '--delay_seconds', type=int, default=3,
                    help='Input seconds you want to delay process, default is 3 seconds')
args = parser.parse_args()

MINUTES = args.run_minute  # 参数：运行时间
DELAY = args.delay_seconds  # 参数：延迟时长
NODE = args.node

# 建立一个数据库连接并获取游标


def acquire_cursor():
    db = ConnectDB()
    conn = db.connect()
    cursor = conn.cursor()
    return cursor


def open_temperaSensor():
    cur = acquire_cursor()
    # 确定执行多少分钟
    current_time = datetime.now()  # 获取当前时间
    update_time = current_time + timedelta(minutes=MINUTES)  # 截止时间
    insertID = 1
    while current_time < update_time:
        # 插入的数据
        VALUE = float(format(random.uniform(-5, 15), '.1f'))  # 模仿湿度
        ADDRESS = random.choice(
            ['\'C-512\'', '\'C-523\'', '\'C-412\''])  # 模仿位置
        sql = 'INSERT INTO temperature(value, node, address) VALUES({0}, {1}, {2})'.format(
            VALUE, NODE, ADDRESS)
        logger.debug(sql)
        try:
            cur.execute(sql)
            logger.info('Successful [value: {:>5}] [address: {}] [time: {}] [id: {:>3}]'.format(
                VALUE, ADDRESS, current_time, insertID))
        except MySQLdb.Error as e:
            raise e
        time.sleep(DELAY)
        current_time = datetime.now()  # 更新当前时间
        insertID += 1  # 更新insertID


def open_humiditySensor():
    cur = acquire_cursor()
    current_time = datetime.now()
    update_time = current_time + timedelta(minutes=MINUTES)
    insertID = 1
    while current_time < update_time:
        # 插入的数据
        VALUE = float(format(random.uniform(50, 100), '.1f'))
        ADDRESS = random.choice(
            ['\'C-512\'', '\'C-523\'', '\'C-412\''])
        sql = 'INSERT INTO humidity(value, node, address) VALUES({0}, {1}, {2})'.format(
            VALUE, NODE, ADDRESS)
        logger.debug(sql)
        try:
            cur.execute(sql)
            logger.info('Successful [value: {:>5}] [address: {}] [time: {}] [id: {:>3}]'.format(
                VALUE, ADDRESS, current_time, insertID))
        except MySQLdb.Error as e:
            raise e
        time.sleep(DELAY)
        current_time = datetime.now()
        insertID += 1


def open_luxSensor():
    cur = acquire_cursor()
    current_time = datetime.now()
    update_time = current_time + timedelta(minutes=MINUTES)
    insertID = 1
    while current_time < update_time:
        # 插入的数据
        VALUE = random.randint(50, 300)
        ADDRESS = random.choice(
            ['\'C-512\'', '\'C-523\'', '\'C-412\''])
        sql = 'INSERT INTO luminous_intensity(value, node, address) VALUES({0}, {1}, {2})'.format(
            VALUE, NODE, ADDRESS)
        logger.debug(sql)
        try:
            cur.execute(sql)
            logger.info('Successful [value: {:>5}] [address: {}] [time: {}] [id: {:>3}]'.format(
                VALUE, ADDRESS, current_time, insertID))
        except MySQLdb.Error as e:
            raise e
        time.sleep(DELAY)
        current_time = datetime.now()
        insertID += 1


def open_fireSensor():
    cur = acquire_cursor()
    # 确定执行多少分钟
    current_time = datetime.now()  # 获取当前时间
    update_time = current_time + timedelta(minutes=MINUTES)  # 截止时间
    insertID = 1
    while current_time < update_time:
        STATUS = random.choice([True, False])
        ADDRESS = random.choice(['\'C-512\'', '\'C-523\'', '\'C-412\''])
        sql = 'INSERT INTO fire(status, node, address) VALUES({0}, {1}, {2})'.format(
            STATUS, NODE, ADDRESS)
        try:
            cur.execute(sql)
            logger.info('Successful [value: {:>5}] [address: {}] [time: {}] [id: {:>3}]'.format(
                STATUS, ADDRESS, current_time, insertID))
        except MySQLdb.Error as e:
            raise e
        time.sleep(DELAY)
        current_time = datetime.now()  # 更新当前时间
        insertID += 1  # 更新insertID


def open_smokeSensor():
    cur = acquire_cursor()
    current_time = datetime.now()
    update_time = current_time + timedelta(minutes=MINUTES)
    insertID = 1
    while current_time < update_time:
        STATUS = random.choice([True, False])
        ADDRESS = random.choice(['\'C-512\'', '\'C-523\'', '\'C-412\''])
        sql = 'INSERT INTO smoke(status, node, address) VALUES({0}, {1}, {2})'.format(
            STATUS, NODE, ADDRESS)
        try:
            cur.execute(sql)
            logger.info('Successful [value: {:>5}] [address: {}] [time: {}] [id: {:>3}]'.format(
                STATUS, ADDRESS, current_time, insertID))
        except MySQLdb.Error as e:
            raise e
        time.sleep(DELAY)
        current_time = datetime.now()
        insertID += 1


def open_infraredSensor():
    cur = acquire_cursor()
    current_time = datetime.now()
    update_time = current_time + timedelta(minutes=MINUTES)
    insertID = 1
    while current_time < update_time:
        STATUS = random.choice([True, False])
        ADDRESS = random.choice(['\'C-512\'', '\'C-523\'', '\'C-412\''])
        sql = 'INSERT INTO human_infrared(status, node, address) VALUES({0}, {1}, {2})'.format(
            STATUS, NODE, ADDRESS)
        try:
            cur.execute(sql)
            logger.info('Successful [value: {:>5}] [address: {}] [time: {}] [id: {:>3}]'.format(
                STATUS, ADDRESS, current_time, insertID))
        except MySQLdb.Error as e:
            raise e
        time.sleep(DELAY)
        current_time = datetime.now()
        insertID += 1


def main():
    threads = []
    t1 = Thread(target=open_temperaSensor)
    threads.append(t1)
    t2 = Thread(target=open_fireSensor)
    threads.append(t2)
    t3 = Thread(target=open_humiditySensor)
    threads.append(t3)
    t4 = Thread(target=open_luxSensor)
    threads.append(t4)
    t5 = Thread(target=open_smokeSensor)
    threads.append(t5)
    t6 = Thread(target=open_infraredSensor)
    threads.append(t6)
    for t in threads:
        t.setDaemon(True)
        t.start()
    try:
        while t.isAlive():
            pass
    except KeyboardInterrupt:
        logger.info('exit')


if __name__ == '__main__':
    main()
