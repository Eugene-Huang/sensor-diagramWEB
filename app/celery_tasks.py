# -*- coding: utf8 -*-

# from flask import current_app
from extensions import celery
from app import connectDB
from app import socketio


# 测试celerty任务
# @celery.task()
# def log(msg):
#     return msg


@celery.task(
    bind=True,
    ignore_result=True,
    default_retry_delay=300,
    max_retries=5
)
def subscribe_start():
    def _on_connect(mqcli):
        """一旦连接上broker则触发此回调函数，随即进行订阅
        """
        mqcli.subscribe()

    def _on_message(mqcli, topic, payload, qos):
        """一接收到消息即触发此回调函数
        """
        print 'received mqtt msg successful'
        # recv_messages = json.dumps(payload)
        # socketio.emit('server_esponse', recv_messages)
        # result = {
        #     'status': 'ok'
        # }
        # return json.dumps(result)

    # # 创建一个应用上下文
    # app = current_app._get_current_object()
    # with app.app_context():
    mqcli = connectDB.PyMQTT()
    mqcli.on_connect = _on_connect
    mqcli.on_message = _on_message
    mqcli.connect()
    mqcli.loop_background()
