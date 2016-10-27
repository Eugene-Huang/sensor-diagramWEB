#!/usr/bin/env python
# -*- coding: utf8 -*-


import paho.mqtt.client as mqtt
from datetime import datetime
import json
import random
import time

MQTT_HOST = "10.22.85.190"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_TOPIC = 'test/address'


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

mqttp.username_pw_set('test', password='fuck')
mqttp.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)


while True:
    current_time = datetime.now()
    value = float(format(random.uniform(5, 20), '.1f'))
    sensor_type = random.choice(
        ['temperature', 'humidity', 'light'])
    sensor_node = random.randint(1, 5)
    msg = {'sensor_type': sensor_type, 'value': value,
           'sensor_node': sensor_node}
    msg = json.dumps(msg)
    try:
        mqttp.publish(MQTT_TOPIC, msg)
        time.sleep(2)
    except KeyboardInterrupt:
        mqttp.disconnect()
        break
