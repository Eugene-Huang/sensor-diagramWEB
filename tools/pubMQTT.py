#!/usr/bin/env python
# -*- coding: utf8 -*-


import paho.mqtt.client as mqtt
# from datetime import datetime
import json
import random
import time

MQTT_HOST = "localhost"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_TOPIC = 'SmartLab'


def on_publish(mqttp, userdata, mid):
    print 'Message Published...'


def on_disconnect(mqttc, userdata, rc):
    if rc != 0:
        print 'Unexpected disconnection.'
    else:
        print 'Disconnected-_-|'


mqttp = mqtt.Client()

mqttp.on_publish = on_publish
mqttp.on_disconnect = on_disconnect

mqttp.username_pw_set('zhifeng', password='zhifeng523')
mqttp.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)


def create_sensor():
    '''
    模拟采取传感器数值,随机创造一个传感器及相关数值
    '''
    # received_tiem = datetime.now()
    value = float(format(random.uniform(5, 20), '.1f'))
    sensor_type = random.choice(
        ['temp', 'hum', 'light'])
    sensor_node = random.randint(1, 5)
    return {'type': sensor_type, 'value': value,
            'id': sensor_node}


while True:
    # current_time = datetime.now()
    # 要发布的消息
    msg = {'title': 'test', 'items': [create_sensor(), create_sensor(), create_sensor()]}
    msg = json.dumps(msg)
    try:
        mqttp.publish(MQTT_TOPIC, msg)
        time.sleep(3)
    except KeyboardInterrupt:
        mqttp.disconnect()
        break
