'''SSE UI updates handler
'''
import click
from flask import (
    Blueprint,
    request,
    Response,
)
import posix_ipc as ipc
from . import message_queue as m

bp = Blueprint('pay', __name__, url_prefix='/pay')

@bp.route('/display', methods=['GET'])
def handle_display_update():
    '''SSE entry point
    '''
    if request.headers.get('accept') != 'text/event-stream':
        rsp = 'This endpoint is meant only for event stream listeners'
        return Response(rsp, mimetype='text/plain')

    def make_event(data):
        ret = 'data: ' + data.decode(encoding='UTF-8')
        click.echo(ret)
        return ret + '\n\n'

    def get_update_event():
        mqkw = {
            'flags': ipc.O_CREAT,
            'read': True,
            'write': False,
        }
        with m.MessageQueue('/nexoid:v1:display', **mqkw) as msq:
            while True:
                data, _ = msq.receive()
                yield make_event(data=data)

    evt = get_update_event()
    return Response(evt, mimetype='text/event-stream')
