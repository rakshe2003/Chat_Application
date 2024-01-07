# app.py

from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Dictionary to store chat rooms and messages
chat_rooms = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    socketio.emit('message', {'msg': f'{username} has joined the room'}, room=room)

@socketio.on('leave')
def handle_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    socketio.emit('message', {'msg': f'{username} has left the room'}, room=room)

@socketio.on('message')
def handle_message(data):
    username = data['username']
    room = data['room']
    message = data['message']
    socketio.emit('message', {'msg': f'{username}: {message}'}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
