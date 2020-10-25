from pynng import Push0

class NotificationSocket:

    def __init__(self, *args, **kwargs):
        self.socket = Push0(*args, **kwargs)

    def __enter__(self):
        return self.socket

    def __exit__(self, type, value, traceback):
        self.socket.close()
