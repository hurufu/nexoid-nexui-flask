import response_socket as rs
import notification_socket as ns

def main():
    with rs.ResponseSocket(listen='tcp://0.0.0.0:50153', recv_timeout=3 * 1000) as s, ns.NotificationSocket(listen='tcp://0.0.0.0:50154') as n:
        evt = b'<ScapiNotification><events><languageSelection><language>pl</language>'\
              b'</languageSelection><serviceSelection><serviceId><cardValidityCheck/>'\
              b'</serviceId></serviceSelection></events></ScapiNotification>'
        print('ntf: ' + evt.decode(encoding='UTF-8'))
        n.send(evt)

        while True:
            req = s.recv()
            print('req: ' + req.decode(encoding='UTF-8'))

            rsp = b'<ScapiResponse><ack/></ScapiResponse>'
            print('rsp: ' + rsp.decode(encoding='UTF-8'))
            s.send(rsp)

main()
