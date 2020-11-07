'''NEXUI - Demo UI for nexo-in-the-cloud'''
from flask import Flask
from flask_socketio import SocketIO

from nexui.response_socket import ResponseSocket

app = Flask(__name__, instance_relative_config=True)
socketio = SocketIO(app)

def get_request_generator():
    '''Wait for requests and yield them one by one'''
    with ResponseSocket(listen='ipc:///tmp/nexui') as scap:
        while True:
            browser_response = yield scap.recv().decode(encoding='UTF-8')
            scap.send(browser_response.encode(encoding='UTF-8'))

request_generator = get_request_generator()

@socketio.on('message')
def handle_ready(payload):
    '''Replies back and waits for anouther request'''
    socketio.send(request_generator.send(payload))

if __name__ == '__main__':
    socketio.run(app)
