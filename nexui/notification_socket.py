'''NNG Wrapper for SCAPI Notifications'''
from click import echo
from pynng import Push0

class Socket:
    '''Push0 context manager'''

    def __init__(self, *args, **kwargs):
        self.socket = Push0(*args, **kwargs)
        self.addr = kwargs['dial']
        debug_msg = 'Connected to ' + self.addr
        echo(debug_msg)

    def __enter__(self):
        return self.socket

    def __exit__(self, exception_type, exception_value, traceback):
        debug_msg = 'Disconnected from ' + self.addr + '\n'\
                  + 'type: ' + str(exception_type) + ' ' + str(exception_value)
        echo(debug_msg)
        self.socket.close()
