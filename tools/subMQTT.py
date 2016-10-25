#!/usr/bin/env python
# -*- coding: utf8 -*-


import paho.mqtt.client as mqtt
import json
import sys

sys.path.append("../app")
from connect_db import db


MQTT_HOST = "10.22.85.190"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_TOPIC = 'test/temperature'
# MQTT_MSG = ""


def on_connect(mqttc, userdata, flags, rc):
    print 'Connected with result code ' + str(rc)
    mqttc.subscribe(MQTT_TOPIC)


def on_message(mqttc, userdata, msg):
    print 'Topic: ' + str(msg.topic)
    print 'QoS: ' + str(msg.qos)
    print 'Message: ' + str(msg.payload)
    data = json.loads(msg.payload)


def on_subscribe(mosq, obi, mid, granted_qos):
    print 'Sunscribed to Topic: ' + MQTT_TOPIC + ' with QoS: ' + str(granted_qos)


def on_disconnect(mqttc, userdata, rc):
    if rc != 0:
        print 'Unexpected disconnection.'
    else:
        print 'Disconnected-_-|'


mqttc = mqtt.Client()

mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_disconnect = on_disconnect

try:
    mqttc.username_pw_set('test', password='fuck')
    mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
    mqttc.loop_forever()
except KeyboardInterrupt:
    mqttc.disconnect()
