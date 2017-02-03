#!/usr/bin/env python
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__, template_folder='./')
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)


@app.route('/socketio')
def websocket():
    return render_template('testsocketio.html')


@socketio.on('client_event')
def client_msg(msg):
    emit('server_response', {'data': msg['data']})


@socketio.on('connect_event')
def connected_msg(msg):
    emit('server_response', {'data': msg['data']})


if __name__ == '__main__':
    socketio.run(app)
