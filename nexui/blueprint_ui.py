'''SSE UI updates handler
'''
from flask import (
    Blueprint,
    redirect,
    url_for,
)

bp = Blueprint('pay', __name__, url_prefix='/pay')

@bp.route('/display', methods=['GET'])
def handle_display_update():
    '''SocketIO entry point
    '''
    return redirect(url_for('static', filename='display.html'))
