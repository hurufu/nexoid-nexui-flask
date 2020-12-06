'''Basic SCAP Application'''

import response_socket as rs
import request_socket as rq
from scapi_message import (tonexui, fromnexui)

def handle_scapi_requests():
    '''Main request handling function'''
    with rs.ResponseSocket(listen='ipc:///tmp/fatrq') as fat,\
         rq.RequestSocket(dial='ipc:///tmp/nexui') as nexui:
        def fat_recv():
            req = tonexui(fat.recv())
            print('req: ' + req)
            return req.encode('UTF-8')
        def fat_send(rsp):
            rsp_buf = fromnexui(rsp)
            fat.send(rsp_buf)
            print('rsp: ' + rsp_buf.decode(encoding='UTF-8'))

        while True:
            nexui.send(fat_recv())
            fat_send(nexui.recv())

handle_scapi_requests()
