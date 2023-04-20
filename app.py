from flask import Flask
from flask_socketio import SocketIO, send, join_room, leave_room

import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
# setup a socketio server that only allows requests from the localhost and selected origins
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('join')
def on_join(data):
    room = data.get('user_id')
    join_room(room)

@socketio.on('leave')
def on_leave(data):
    room = data.get('user_id')
    leave_room(room)

@socketio.on('note')
def handle_note(data):
    send({'note':data.get('note')}, broadcast=True, json=True, room=data.get('note').get('creator_id'))

@socketio.on('image')
def handle_note(data):
    send({'image':data.get('image')}, broadcast=True, json=True, room=data.get('creator_id'))

@app.route('/')
def index():
    return {"name":"KlassNaut Socket Server", "version":"0.0.1", "status":"OK"}

if __name__ == '__main__':
    socketio.run(app)