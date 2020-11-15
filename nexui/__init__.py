'''NEXUI - Demo UI for nexo-in-the-cloud'''
import threading

from flask import (
    Flask,
    redirect,
    url_for,
    request,
)
import click

from timebudget import timebudget
from . import blueprint_ui as ui
from . import request_socket as rq
from . import response_socket as rs
from . import notification_socket as ns

app = Flask(__name__, instance_relative_config=True)
app.register_blueprint(ui.bp)

@app.route('/nexo', methods=['GET'])
def get_scap_notification_form():
    '''Simple redirect to the main page with frames'''
    return redirect(url_for('static', filename='frames.html'))

@app.route('/nexo', methods=['POST'])
def notify_scap():
    '''Forward SCAPI notifications directly to the FAT'''
    with ns.Socket(dial='ipc:///tmp/fatnt') as ntf:
        click.echo(request.data)
        ntf.send(request.data)
    return redirect(url_for('static', filename='notification.xml'))

@app.before_first_request
def start_ui_server():
    '''Lazily starts UI request forwarder'''

    def forward_ui_requests(**kwargs):
        '''Blindly forwards all UI requests to a web browser'''
        with rs.Socket(**kwargs['nexui']) as nexui,\
             rq.Socket(**kwargs['browser']) as browser:
            while True:
                req = nexui.recv()
                with timebudget("Browser roundtrip", quiet=kwargs['quiet_time']):
                    browser.send(req)
                    rsp = browser.recv()
                nexui.send(rsp)

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
            },
            'quiet_time': True,
        }
    }
    threading.Thread(**thread_params).start()
