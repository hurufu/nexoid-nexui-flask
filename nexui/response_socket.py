'''NNG Wrapper'''
import click
from pynng import Rep0

class ResponseSocket:
    '''Rep0 context manager'''

    def __init__(self, *args, **kwargs):
        self.socket = Rep0(*args, **kwargs)
        self.addr = kwargs['listen']
        debug_msg = 'Listening on ' + self.addr
        click.echo(debug_msg)

    def __enter__(self):
        return self.socket

    def __exit__(self, exception_type, exception_value, traceback):
        debug_msg = 'Stopped to listen on ' + self.addr + '\n'\
                  + 'type: ' + str(exception_type) + ' ' + str(exception_value)
        click.echo(debug_msg)
        self.socket.close()
