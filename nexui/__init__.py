'''NEXUI - Demo UI for nexo-in-the-cloud'''
import os
import threading
import subprocess
from logging.config import dictConfig
from logging import (
    info,
    debug,
    warning,
    error,
)
from time import sleep
from contextlib import contextmanager
from traceback import print_exc

from flask import (
    Flask,
    redirect,
    url_for,
    request,
    send_from_directory,
)
import click

import pynng
from timebudget import timebudget
from . import scap4nexui

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname).1s %(threadName)-13s %(message)s',
        }
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': [
            'wsgi'
        ]
    }
})

@contextmanager
def browser_distributor(*args, name='browser_distributor', **kwargs):
    '''Creates a socket for distributing requests to all connected browsers'''
    socket = pynng.Surveyor0(*args, name=name, **kwargs)
    info(f"{socket.protocol_name} '{name}' is listening on {kwargs['listen']}")
    yield socket
    info(f"{socket.protocol_name} '{name}' at {kwargs['listen']} is stopped")
    socket.close()

@contextmanager
def local_ui_requests_gatherer(*args, name='ui_gatherer', **kwargs):
    '''Creates a socket context manager for gathering UI requests from local peers'''
    socket = pynng.Rep0(*args, **kwargs)
    info(f"{socket.protocol_name} '{name}' is listening on {kwargs['listen']}")
    yield socket
    info(f"{socket.protocol_name} '{name}' at {kwargs['listen']} is stopped")
    socket.close()

def notification_socket(*args, name='fat_notifier', **kwargs):
    '''Creates a socket for FAT notifications'''
    socket = pynng.Push0(*args, **kwargs)
    info(f"{socket.protocol_name} '{name}' dialed to {kwargs['dial']}")
    return socket

app = Flask(__name__, instance_relative_config=True)

@app.route('/favicon.ico')
def favicon():
    '''Redirect to favicon'''
    path = os.path.join(app.root_path, 'static')
    return send_from_directory(path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/nexo', methods=['GET'])
def get_scap_notification_form():
    '''Simple redirect to the main page with frames'''
    return redirect(url_for('static', filename='frames.html'))

@app.route('/nexo', methods=['POST'])
def notify_scap():
    '''Forward SCAPI notifications directly to FAT'''
    if notify_scap.ntf is None:
        # Figure out a way to cleanly shutdown SCAP notification socket
        notify_scap.ntf = notification_socket(dial='ipc:///tmp/fatnt')
    notify_scap.ntf.send(request.data)
    debug(f"Sent SCAP notification {request.data}")
    return redirect(url_for('static', filename='notification.xhtml'))

notify_scap.ntf = None

@app.before_first_request
def start_ui_server():
    '''Lazily starts UI request forwarder'''

    def forward_ui_requests(**kwargs):
        '''Blindly forwards all UI requests to a web browser'''
        sleep(15)
        with local_ui_requests_gatherer(**kwargs['nexui']) as nexui,\
             browser_distributor(**kwargs['browser']) as browser:
            sleep(2)
            while True:
                try:
                    req = nexui.recv()
                    debug(f"Received UI request {req}")
                    with timebudget("Browser roundtrip", quiet=kwargs['quiet_time']):
                        browser.send(req)
                        rsp = browser.recv()
                    nexui.send(rsp)
                    debug(f"UI response {rsp}")
                except pynng.exceptions.Timeout:
                    error('Timeout exception suppressed')
                    print_exc()

    def run_external_program(**kwargs):
        sleep(22)
        while True:
            info('Nexoid process started')
            subprocess.run(kwargs['prog'], check=False)
            warning('Nexoid process ended')
            sleep(2)

    def run_scap4nexui():
        sleep(17)
        return scap4nexui.main()

    thread_params = {
        'target': forward_ui_requests,
        'name': 'reqfrwdr',
        'daemon': True,
        'kwargs': {
            'browser': {
                'listen': 'ws://*:51004',
                'survey_time': 1 * 60 * 1000
            },
            'nexui': {
                'listen': 'ipc:///tmp/nexui'
            },
            'quiet_time': True,
        }
    }
    threading.Thread(**thread_params).start()

    scap4nexui_thread_params = {
        'target': run_scap4nexui,
        'name': 'scap4nexui',
        'daemon': True
    }
    threading.Thread(**scap4nexui_thread_params).start()

    nexoid_thread_params = {
        'target': run_external_program,
        'name': 'nexoid_runner',
        'daemon': True,
        'kwargs': {
            'prog': ['nexoid-cpp'],
        }
    }
    threading.Thread(**nexoid_thread_params).start()

    sleep(15)
