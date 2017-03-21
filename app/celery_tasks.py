# -*- coding: utf8 -*-

from flask import current_app
from extensions import celery
from app import connectDB
import urllib
import urllib2
import json

# 测试celerty任务
# @celery.task()
# def log(msg):
#     return msg


@celery.task()
def task_subscribe():
    def _data_cleaning(data):
        '''订阅的数据格式：
        data = {
            "temperature": {"node": 01, "value": 12, address": "class01"},
            "humidity": {"node": 01, "value": 12, address": "class01"},
            "light": {"node": 01, "value": 12, address": "class01"}
        }
        '''
        data = json.loads(data)
        result = data['temperature']
        return {"temperature": result}

    def _on_connect(mqcli):
        """一旦连接上broker则触发此回调函数，随即进行订阅
        """
        mqcli.subscribe()

    def _on_message(mqcli, topic, payload, qos):
        """一接收到消息即触发此回调函数
        """
        # 提交一个post请求触发websocket事件
        url = 'http://127.0.0.1:8000/uptemperature'
        data = urllib.urlencode(_data_cleaning(payload))
        request = urllib2.Request(url, data)
        urllib2.urlopen(request)
        # print 'received mqtt msg successful # ' + data

    # 创建一个应用上下文
    app = current_app._get_current_object()
    with app.app_context():
        mqcli = connectDB.PyMQTT()
        mqcli.on_connect = _on_connect
        mqcli.on_message = _on_message
        mqcli.connect()
        mqcli.loop_background()
