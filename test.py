'''TEST
'''
import threading
from time import sleep

import response_socket as rs
import notification_socket as ns
import message_queue as mq

def handle_scapi_requests(**kwargs):
    '''Main request handling function
    '''
    with rs.ResponseSocket(**kwargs) as sock,\
         mq.MessageQueue('/nexoid:v1:display', read = False) as queue:
        while True:
            sleep(1)

            req = sock.recv()
            print('req: ' + req.decode(encoding='UTF-8'))

            queue.send(req)

            rsp = b'<ScapiResponse><ack/></ScapiResponse>'
            sock.send(rsp)
            print('rsp: ' + rsp.decode(encoding='UTF-8'))

def start_req_handler():
    '''Starts request handling thread'''
    thread_params = {
        'target': handle_scapi_requests,
        'name': 'reqhndlr',
        'daemon': True,
        'kwargs': {
            'listen': 'tcp://0.0.0.0:50153'
        }
    }
    req_thread = threading.Thread(**thread_params)
    req_thread.start()

def main():
    '''Main'''
    start_req_handler()
    with ns.NotificationSocket(listen='tcp://0.0.0.0:50154') as ntf:
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
