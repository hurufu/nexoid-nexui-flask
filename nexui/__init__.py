'''NEXUI - Demo UI for nexo-in-the-cloud'''
import threading

from flask import Flask
import click

from . import blueprint_ui as ui
from . import request_socket as rq
from . import response_socket as rs

app = Flask(__name__, instance_relative_config=True)
app.register_blueprint(ui.bp)

@app.before_first_request
def start_ui_server():
    '''Lazily starts UI request forwarder'''

    def forward_ui_requests(**kwargs):
        '''Blindly forwards all UI requests to a web browser'''
        with rs.Socket(**kwargs['nexui']) as nexui,\
             rq.Socket(**kwargs['browser']) as browser:
            while True:
                browser.send(nexui.recv())
                nexui.send(browser.recv())

    thread_params = {
        'target': forward_ui_requests,
        'name': 'reqfrwdr',
        'daemon': True,
        'kwargs': {
            'browser': {
                'listen': 'ws://*:51004'
            },
            'nexui': {
                'listen': 'ipc:///tmp/nexui'
            }
        }
    }
    threading.Thread(**thread_params).start()
