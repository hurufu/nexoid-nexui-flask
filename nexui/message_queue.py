'''POSIX IPC wrapper
'''
import posix_ipc
import click

class MessageQueue:
    '''Simple context manager for POSIX MQ
    '''

    def __init__(self, *args, **kwargs):
        self.queue = posix_ipc.MessageQueue(*args, **kwargs)
        self.name = args[0]
        debug_msg = 'Queue "' + self.name + '" opened'
        click.echo(debug_msg)

    def __enter__(self):
        return self.queue

    def __exit__(self, exception_type, exception_value, traceback):
        debug_msg = 'Queue "' + self.name + '" closed, '\
                  + 'type: ' + str(exception_type) + ' ' + str(exception_value)
        click.echo(debug_msg)
        self.queue.close()
        self.queue.unlink()
