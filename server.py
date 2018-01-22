from threading import Lock
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

thread = None
thread_lock = Lock()
 


# Thread to keep sending the data upon receiving

def background_thread():
    count = 0
    while True:
        socketio.sleep(1)
        count += 1
        f = open('data.txt', 'r')
    	string = f.read()
    	f.close()
    	print (string)
        socketio.emit('my_response',
                      {'data': string, 'count': count},
                      )

@app.route("/")
def index():
    return render_template('map.html', async_mode=socketio.async_mode)
 

# Various behaviours on the socket in different situations

@socketio.on('my_event')
def test_message(message):
    print (message['data'])


@socketio.on('connect')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)




if __name__ == "__main__":
    socketio.run(app, debug=True)