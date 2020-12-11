'''Basic SCAP Application'''

from contextlib import contextmanager
from pynng import (Req0, Rep0)
from scapi_message import (tonexui, fromnexui)

@contextmanager
def request_socket(*args, **kwargs):
    '''NNG Req0 context manager'''
    socket = Req0(*args, **kwargs)
    yield socket
    socket.close()

@contextmanager
def response_socket(*args, **kwargs):
    '''NNG Rep0 context manager'''
    socket = Rep0(*args, **kwargs)
    yield socket
    socket.close()

def main():
    '''Main request forwarding loop'''
    with response_socket(listen='ipc:///tmp/fatrq') as fat,\
         request_socket(dial='ipc:///tmp/nexui') as nexui:
        def exchange_messages():
            req = tonexui(fat.recv())
            nexui.send(req)
            print('req: ' + req.decode('UTF-8'))
            rsp = nexui.recv()
            fat.send(fromnexui(rsp))
            print('rsp: ' + rsp.decode('UTF-8'))

        while True:
            exchange_messages()

main()
