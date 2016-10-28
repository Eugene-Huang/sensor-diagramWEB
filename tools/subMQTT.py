#!/usr/bin/env python
# -*- coding: utf8 -*-


import paho.mqtt.client as mqtt
import json
import sys
import logging
from datetime import datetime

sys.path.append("..")
from app.connect_db import db


logger = logging.getLogger(__name__)

MQTT_HOST = "10.22.85.190"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_TOPIC = 'test/address'
USERNAME = 'test'
PASSWORD = 'fuck'


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


def runMQTT():
    def connected(client, rc):
        print 'Connected to MQTT broker with result code ' + str(rc)
        client.subscribe()

    def message(client, topic, payload, qos):
        '''
        回调函数
        当接收到订阅的主题发布的消息时，触发这个函数
        接受一条消息触发一次
        '''
        # 打印消息
        print 'Topic: ' + str(topic)
        print 'QoS: ' + str(qos)
        print 'Message: ' + str(payload)
        # 反序列化消息和数据
        data = json.loads(payload)
        # =============================
        # 如果是个列表，就迭代一下
        # =============================
        # 解析数据
        TABLE = 'recvmqtt'
        sensor_type = data['sensor_type']
        value = data['value']
        sensor_node = data['sensor_node']
        # 设定接收到消息的时间
        received_time = datetime.now()
        # 插入数据库
        sql = "INSERT INTO {0}(sensor_type, value, sensor_node, recv_time) VALUE(\'{1}\', \'{2}\', \'{3}\', \'{4}\')".format(
            TABLE, sensor_type, value, sensor_node, received_time)
        db.execute_db(sql)

    client = FuckMQTT(USERNAME, PASSWORD, '10.22.85.190')
    client.on_connect = connected
    client.on_message = message

    try:
        client.connect()
        client.loop_blocking()
    except:
        client.disconnect()


if __name__ == '__main__':
    runMQTT()


# ======================================================
# 这是没有打包成类的版本
# ======================================================
# def on_connect(mqttc, userdata, flags, rc):
#     print 'Connected with result code ' + str(rc)
#     mqttc.subscribe(MQTT_TOPIC)


# def on_message(mqttc, userdata, msg):
#     '''
#     回调函数
#     当接收到订阅的主题发布的消息时，触发这个函数
#     接受一条消息触发一次
#     '''
#     # 打印消息
#     print 'Topic: ' + str(msg.topic)
#     print 'QoS: ' + str(msg.qos)
#     print 'Message: ' + str(msg.payload)
#     # 反序列化消息和数据
#     data = json.loads(msg.payload)
#     # 解析数据
#     TABLE = 'recvmqtt'
#     sensor_type = data['sensor_type']
#     value = data['value']
#     sensor_node = data['sensor_node']
#     # 设定接收到消息的时间
#     received_time = datetime.now()
#     # 插入数据库
#     sql = "INSERT INTO {0}(sensor_type, value, sensor_node, recv_time) VALUE(\'{1}\', \'{2}\', \'{3}\', \'{4}\')".format(
#         TABLE, sensor_type, value, sensor_node, received_time)
#     db.execute_db(sql)


# def on_subscribe(mosq, obi, mid, granted_qos):
# print 'Sunscribed to Topic: ' + MQTT_TOPIC + ' with QoS: ' +
# str(granted_qos)


# def on_disconnect(mqttc, userdata, rc):
#     if rc != 0:
#         print 'Unexpected disconnection.'
#     else:
#         print 'Disconnected-_-|'


# mqttc = mqtt.Client()

# mqttc.on_connect = on_connect
# mqttc.on_message = on_message
# mqttc.on_subscribe = on_subscribe
# mqttc.on_disconnect = on_disconnect

# try:
#     mqttc.username_pw_set('test', password='fuck')
#     mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
#     mqttc.loop_forever()
# except KeyboardInterrupt:
#     mqttc.disconnect()
