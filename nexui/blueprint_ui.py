import click
from flask import (
    Blueprint,
    request,
    Response,
)
from . import message_queue as m

bp = Blueprint('pay', __name__, url_prefix='/pay')

@bp.route('/display', methods=['GET'])
def handle_display_update():
    if request.headers.get('accept') != 'text/event-stream':
        return Response('This endpoint is meant only for event stream listeners', mimetype='text/plain')

    def get_update_event():
        with m.MessageQueue('/nexoid:v1:display', flags = m.O_CREAT, read = True, write = False) as mq:
            while True:
                (buf, priority) = mq.receive()
                ret = 'data: ' + buf.decode(encoding='UTF-8') + '\n\n'
                click.echo('Forwarding msg with priority: ' + str(priority) + '\n' + ret)
                yield ret

    r = get_update_event()
    return Response(r, mimetype='text/event-stream')
