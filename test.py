'''TEST
'''
import threading
from time import sleep

import response_socket as rs
import notification_socket as ns
import request_socket as rq
from scapi_message import (tonexui, fromnexui)

def handle_scapi_requests(**kwargs):
    '''Main request handling function'''
    with rs.ResponseSocket(**kwargs['fat']) as fat,\
         rq.RequestSocket(**kwargs['nexui']) as nexui:
        def fat_recv():
            req = tonexui(fat.recv())
            print('req: ' + req)
            return req.encode('UTF-8')
        def fat_send(rsp):
            rsp_buf = fromnexui(rsp)
            fat.send(rsp_buf)
            print('rsp: ' + rsp_buf.decode(encoding='UTF-8'))

        while True:
            req = fat_recv()
            nexui.send(req)
            rsp = nexui.recv()
            fat_send(rsp)

def start_req_handler():
    '''Starts request handling thread'''
    thread_params = {
        'target': handle_scapi_requests,
        'name': 'reqhndlr',
        'daemon': True,
        'kwargs': {
            'fat': {
                'listen': 'ipc:///tmp/fatrq'
            },
            'nexui': {
                'dial': 'ipc:///tmp/nexui'
            }
        }
    }
    req_thread = threading.Thread(**thread_params)
    req_thread.start()

def main():
    '''Main'''
    start_req_handler()
    with ns.NotificationSocket(listen='ipc:///tmp/fatnt') as ntf:
        evt = b'<ScapiNotification><events></events></ScapiNotification>'
        ntf.send(evt)
        print('ntf: ' + evt.decode(encoding='UTF-8'))

        evt = b'<ScapiNotification><events/></ScapiNotification>'
        ntf.send(evt)
        print('ntf: ' + evt.decode(encoding='UTF-8'))

        evt = b'<ScapiNotification><events><languageSelection><language>pl</language>'\
              b'</languageSelection><serviceSelection><serviceId><cardValidityCheck/>'\
              b'</serviceId></serviceSelection></events></ScapiNotification>'
        ntf.send(evt)
        print('ntf: ' + evt.decode(encoding='UTF-8'))

        evt = b'<ScapiNotification><events><manualEntry><pan>4485936516057131</pan>'\
              b'<expirationDate><year>22</year><month>11</month></expirationDate>'\
              b'<cvdData><cvd>123</cvd></cvdData></manualEntry></events></ScapiNotification>'
        ntf.send(evt)
        print('ntf: ' + evt.decode(encoding='UTF-8'))

        evt = b'<ScapiNotification><events><terminate/></events></ScapiNotification>'
        ntf.send(evt)
        print('ntf: ' + evt.decode(encoding='UTF-8'))

        sleep(100)

main()
