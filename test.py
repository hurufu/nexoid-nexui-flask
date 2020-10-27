import response_socket as rs
import notification_socket as ns
import threading
from time import sleep

def handle_scapi_requests(**kwargs):
    with rs.ResponseSocket(**kwargs) as s:
        while True:
            req = s.recv()
            print('req: ' + req.decode(encoding='UTF-8'))

            rsp = b'<ScapiResponse><ack/></ScapiResponse>'
            s.send(rsp)
            print('rsp: ' + rsp.decode(encoding='UTF-8'))

def start_req_handler():
    req_params = {
        'listen': 'tcp://0.0.0.0:50153'
    }
    req_thread = threading.Thread(target=handle_scapi_requests, name='reqhndlr', daemon=True, kwargs=req_params)
    req_thread.start()

def main():
    start_req_handler()
    with ns.NotificationSocket(listen='tcp://0.0.0.0:50154') as n:
        evt = b'<ScapiNotification><events></events></ScapiNotification>'
        n.send(evt)
        print('ntf: ' + evt.decode(encoding='UTF-8'))

        evt = b'<ScapiNotification><events/></ScapiNotification>'
        n.send(evt)
        print('ntf: ' + evt.decode(encoding='UTF-8'))

        evt = b'<ScapiNotification><events><languageSelection><language>pl</language>'\
              b'</languageSelection><serviceSelection><serviceId><cardValidityCheck/>'\
              b'</serviceId></serviceSelection></events></ScapiNotification>'
        n.send(evt)
        print('ntf: ' + evt.decode(encoding='UTF-8'))

        evt = b'<ScapiNotification><events><manualEntry><pan>4485936516057131</pan>'\
              b'<expirationDate><year>22</year><month>11</month></expirationDate>'\
              b'<cvdData><cvd>123</cvd></cvdData></manualEntry></events></ScapiNotification>'
        n.send(evt)
        print('ntf: ' + evt.decode(encoding='UTF-8'))

        evt = b'<ScapiNotification><events><terminate/></events></ScapiNotification>'
        n.send(evt)
        print('ntf: ' + evt.decode(encoding='UTF-8'))

        sleep(1)

main()
