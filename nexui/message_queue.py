import posix_ipc

O_CREAT = posix_ipc.O_CREAT

class MessageQueue:

    def __init__(self, *args, **kwargs):
        self.queue = posix_ipc.MessageQueue(*args, **kwargs)

    def __enter__(self):
        return self.queue

    def __exit__(self, type, value, traceback):
        self.queue.close()
