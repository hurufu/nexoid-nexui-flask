from pynng import Req0

class RequestSocket:

    def __init__(self, *args, **kwargs):
        self.socket = Req0(*args, **kwargs)

    def __enter__(self):
        return self.socket

    def __exit__(self, type, value, traceback):
        self.socket.close()
