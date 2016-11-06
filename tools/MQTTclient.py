#!/usr/bin/env python
# -*- coding: utf8 -*-

# ---------------------------------
# 订阅MQTT消息，解析数据，插入临时表
# 定时清空临时表
# ---------------------------------

import paho.mqtt.client as mqtt
import MySQLdb
import json
# import sys
import logging
import time
from datetime import datetime
from threading import Thread


# sys.path.append("..")
# from app.connect_db import db


logger = logging.getLogger(__name__)

SERVERHOST = 'localhost'
# MQTT配置
MQTT_HOST = SERVERHOST
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_TOPIC = 'SmartLab'
USERNAME = 'zhifeng'
PASSWORD = 'zhifeng523'

# -----------------------------------------------------
# 连接数据库
try:
    connect = MySQLdb.connect(
        SERVERHOST, 'DBUSERNAME', 'DBPASSWORD', 'DBNAME')
    connect.autocommit(True)
except MySQLdb.Error as e:
    raise e
else:
    print 'Connected to DB successful :)'
    cur = connect.cursor()
# -----------------------------------------------------


def clear_db(interval):
    '''
    定时清空临时mqtt数据库数据
    '''
    RUNSATRT = True
    sql = 'TRUNCATE recvmqtt'
    while RUNSATRT:
        try:
            cur.execute(sql)
            time.sleep(interval)
        except MySQLdb.Error as e:
            raise e


# ---------------------------------------------------------


class FuckMQTT(object):
    """docstring for FuckMQTT"""

    def __init__(self, username, password, host, port=1883):
        self._username = username
        self._password = password
        self._host = host
        self._port = port
        # Initialize event callbacks to be None so theydon't fire
        self.on_connect = None
        self.on_disconnect = None
        self.on_message = None
        # Initialize MQTT client
        self._client = mqtt.Client()
        self._client.username_pw_set(username, password)
        self._client.on_connect = self._mqtt_connect
        self._client.on_disconnect = self._mqtt_disconnect
        self._client.on_message = self._mqtt_message
        self._connected = False

    def _mqtt_connect(self, client, userdata, flags, rc):
        logger.debug('Client on_connect called.')
        if rc == 0:
            self._connected = True
        else:
            raise RuntimeError(
                'Error connecting to MQTT broker with rc: {0}'.format(rc))
        if self.on_connect is not None:
            self.on_connect(self, rc)

    def _mqtt_disconnect(self, client, userdata, rc):
        logger.debug('Client on_disconnect called.')
        self._connected = False
        # If this was an unexpected disconnect (non-zero result code) then just
        # log the RC as an error.  Continue on to call any disconnect handler
        # so clients can potentially recover gracefully.
        if rc != 0:
            logger.debug('Unexpected disconnected with rc: {0}'.format(rc))
        # Call the on_disconnect callback if available.
        if self.on_disconnect is not None:
            self.on_disconnect(self)

    def _mqtt_message(self, client, userdata, msg):
        '''
        回调函数
        当接收到订阅的主题发布的消息时，触发这个函数
        接受一条消息触发一次
        '''
        logger.debug('Client on_message called.')
        # Assumes topic looks like "title/addresss"
        # parsed_topic = msg.topic.split('/')
        if self.on_message is not None:
            topic = '' if msg.topic is None else msg.topic.decode('utf8')
            qos = '' if msg.qos is None else msg.qos
            payload = '' if msg.payload is None else msg.payload.decode('utf8')
            self.on_message(self, topic, payload, qos)

    def connect(self, **kwargs):
        # Skip calling connect if already connected.
        if self._connected:
            return
        # Connect to the Adafruit IO MQTT service.
        self._client.connect(self._host, port=self._port,
                             keepalive=MQTT_KEEPALIVE_INTERVAL, **kwargs)

    def is_connected(self):
        """Returns True if connected to Adafruit.IO and False if not connected.
        """
        return self._connected

    def disconnect(self):
        """Disconnect MQTT client if connected."""
        if self._connected:
            self._client.disconnect()

    def loop_background(self):
        """Starts a background thread to listen for messages from Adafruit.IO
        and call the appropriate callbacks when feed events occur.  Will return
        immediately and will not block execution.  Should only be called once.
        """
        self._client.loop_start()

    def loop_blocking(self):
        self._client.loop_forever()

    def loop(self, timeout_sec=1.0):
        self._client.loop(timeout=timeout_sec)

    def subscribe(self):
        self._client.subscribe(MQTT_TOPIC)
# ------------------------------------------------------------------------------


def runMQTT():
    '''
    1.MQTT订阅，实时接收发布端的消息并解析数据插入到临时数据表，web端查询临时表数据做可视化
    2.定时清空临时表数据
    '''
    def connected(client, rc):
        print 'Connected to MQTT broker with result code ' + str(rc)
        client.subscribe()
        # 开启一条辅助线程
        side_task = Thread(target=clear_db, args=(60,))
        side_task.daemon = True
        side_task.start()

    def message(client, topic, payload, qos):
        '''
        回调函数
        当接收到订阅的主题发布的消息时，触发这个函数
        接受一条消息触发一次
        '''
        # 反序列化消息和数据
        recv_messages = json.loads(payload)
        # 接收到消息的时间
        # received_time = recv_messages['datetime']
        received_time = datetime.now()
        # 打印消息
        # print '----------------------------' * 3
        # print 'Topic: ' + str(topic)
        # print 'QoS: ' + str(qos)
        # print 'Message: ' + str(payload)
        # print 'Received time: ' + str(received_time)
        # print '----------------------------' * 3
        # 插入的数据表
        TABLE = 'recvmqtt'

        # =============================
        # 如果是个列表，就迭代一下
        whole_data = recv_messages['items']
        for data in whole_data:
            sensor_type = data['type']
            value = data['value']
            sensor_node = data['id']
            print sensor_type, value, sensor_node
        # =============================
            # 插入数据库
            sql = "INSERT INTO {0}(sensor_type, value, sensor_node, recv_time) VALUE(\'{1}\', \'{2}\', \'{3}\', \'{4}\')".format(
                TABLE, sensor_type, value, sensor_node, received_time)
            cur.execute(sql)

    client = FuckMQTT(USERNAME, PASSWORD, MQTT_HOST)
    client.on_connect = connected
    client.on_message = message
    try:
        client.connect()
        client.loop_blocking()
    except KeyboardInterrupt:
        client.disconnect()
        print 'Close connect to MQTT broker :('


if __name__ == '__main__':
    runMQTT()
