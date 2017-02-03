#!/url/bin/env/python
# -*- coding: utf8 -*-

from flask import current_app
# from celery.util.log import get_task_log
from app import connectDB
from app import celery
from app import socketio
import json


# logger = get_task_log(__name__)


@celery.task
def block_sub():
    app = current_app._get_current_object()
    # 创建一个应用上下文
    with app.app_context():
        mqcli = connectDB.PyMQTT()
        mqcli.on_connect = on_connect
        mqcli.on_message = on_message
        mqcli.connect()
        mqcli.loop_background()


def on_connect(mqcli):
    """一旦连接上broker则触发此回调函数，随即进行订阅
    """
    mqcli.subscribe()


def on_message(mqcli, topic, payload, qos):
    # 反序列化消息和数据
    recv_messages = json.dumps(payload)
    socketio.emit('server_esponse', recv_messages)
    # result = {
    #     'status': 'ok'
    # }
    # return json.dumps(result)
