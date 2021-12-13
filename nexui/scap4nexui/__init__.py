'''Basic SCAP Application'''

from contextlib import contextmanager
from logging import (
    info,
    debug,
)

from pynng import (Req0, Rep0)
from . import scapi_message as sm

@contextmanager
def ui_socket(*args, name='ui_req_from_scap', **kwargs):
    '''Creates UI socket for forwarding converted SCAPI requests'''
    socket = Req0(*args, **kwargs)
    info(f"{socket.protocol_name} '{name}' dialed to {kwargs['dial']}")
    yield socket
    info(f"{socket.protocol_name} '{name}' dropped connection to {kwargs['dial']}")
    socket.close()

@contextmanager
def scapi_endpoint(*args, name='scapi_endpoint', **kwargs):
    '''Creates SCAPI endpoint socket'''
    socket = Rep0(*args, **kwargs)
    info(f"{socket.protocol_name} '{name}' is listening on {kwargs['listen']}")
    yield socket
    info(f"{socket.protocol_name} '{name}' at {kwargs['listen']} is stopped")
    socket.close()

def main():
    '''Main request forwarding loop'''
    with scapi_endpoint(listen='ipc:///tmp/fatrq') as fat,\
         ui_socket(dial='ipc:///tmp/nexui') as nexui:
        def exchange_messages():
            req = fat.recv()
            debug(f"Received SCAPI request {req}")
            sm.append_to_event_log('ScapiNngRequest', req)
            nexui.send(sm.tonexui(req))
            rsp = sm.fromnexui(nexui.recv())
            fat.send(rsp)
            debug(f"SCAPI response {rsp}")
            sm.append_to_event_log('ScapiNngResponse', rsp)

        while True:
            exchange_messages()

if __name__ == '__main__':
    main()
