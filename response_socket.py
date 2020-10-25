from pynng import Rep0

class ResponseSocket:

    def __init__(self, *args, **kwargs):
        self.socket = Rep0(*args, **kwargs)

    def __enter__(self):
        return self.socket

    def __exit__(self, type, value, traceback):
        self.socket.close()
