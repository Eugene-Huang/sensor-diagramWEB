# -*- coding: UTF-8 -*-


import ConfigParser
import MySQLdb
import logging
import json
from subprocess import os
import paho.mqtt.client as mqttc


MQTT_KEEPALIVE_INTERVAL = 60

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

sh = logging.StreamHandler()
fmt = '%(asctime)s - %(threadName)s - %(levelname)s > %(message)s'
formatter = logging.Formatter(fmt)
sh.setFormatter(formatter)

logger.addHandler(sh)


class ConnectDB(object):

    def __init__(self):
        config = ConfigParser.ConfigParser()
        # config.read(os.path.join(os.path.dirname(os.getcwd()), 'db.conf'))
        config.read(os.path.join(os.getcwd(), 'db.conf'))
        # logger.debug(os.path.join(os.getcwd(), 'db.conf'))
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


class PyMQTT(object):

    def __init__(self):
        config = ConfigParser.ConfigParser()
        # config.read(os.path.join(os.getcwd(), 'db.conf'))
        config.read(os.path.join(os.path.dirname(os.getcwd()), 'db.conf'))
        logger.debug(os.path.join(os.path.dirname(os.getcwd()), 'db.conf'))
        self._mqtthost = config.get('mosquitto', 'MQTT_HOST')
        self._mqttport = config.get('mosquitto', 'MQTT_PORT')
        self._mqtttopic = config.get('mosquitto', 'MQTT_TOPIC')
        self._username = config.get('mosquitto', 'USERNAME')
        self._passwd = config.get('mosquitto', 'PASSWORD')
        # Initialize event callbacks to be None so they don't fire
        self.on_connect = None
        self.on_disconnect = None
        self.on_subscribe = None
        self.on_message = None
        # Initialize MQTT client
        self._client = mqttc.Client()
        self._client.username_pw_set(self._username, self._passwd)
        self._client.on_connect = self._mqtt_connect
        self._client.on_disconnect = self._mqtt_disconnect
        self._client.on_subscribe = self._mqtt_subscribe
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
            self.on_connect(self)

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

    def _mqtt_subscribe(self, client, userdata, mid, granted_qos):
        logger.debug('Client on_subscribe called')
        if self.on_subscribe is not None:
            self.on_subscribe(self)

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
        self._client.connect(self._mqtthost, port=self._mqttport,
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
        self._client.subscribe(self._mqtttopic)


if __name__ == '__main__':

    def on_connect(mqcli):
        mqcli.subscribe()

    def on_message(mqcli, topic, payload, qos):
        # 反序列化消息和数据
        recv_messages = json.loads(payload)
        print recv_messages
        return recv_messages

    mqcli = PyMQTT()
    mqcli.on_connect = on_connect
    mqcli.on_message = on_message
    mqcli.connect()
    mqcli.loop_blocking()
