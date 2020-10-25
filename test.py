import response_socket as rs
import notification_socket as ns

with rs.ResponseSocket(listen='tcp://0.0.0.0:50153') as s:
    with ns.NotificationSocket(listen='tcp://0.0.0.0:50154') as n:
        req = s.recv()
        print('> ' + req.decode(encoding='UTF-8'))

        rsp = b'<ScapiResponse><ack/></ScapiResponse>'
        print('< ' + rsp.decode(encoding='UTF-8'))
        s.send(rsp)

        req = s.recv()
        print('> ' + req.decode(encoding='UTF-8'))

        rsp = b'<ScapiResponse><ack/></ScapiResponse>'
        print('< ' + rsp.decode(encoding='UTF-8'))
        s.send(rsp)

        evt = b'<ScapiNotification><events><languageSelection><language>pl</language>'\
              b'</languageSelection><serviceSelection><serviceId><cardValidityCheck/>'\
              b'</serviceId></serviceSelection></events></ScapiNotification>'
        print('< ' + evt.decode(encoding='UTF-8'))
        n.send(evt)

        req = s.recv()
        print('> ' + req.decode(encoding='UTF-8'))

        rsp = b'<ScapiResponse><ack/></ScapiResponse>'
        print('< ' + rsp.decode(encoding='UTF-8'))
        s.send(rsp)

        req = s.recv()
        print('> ' + req.decode(encoding='UTF-8'))

        rsp = b'<ScapiResponse><ack/></ScapiResponse>'
        print('< ' + rsp.decode(encoding='UTF-8'))
        s.send(rsp)
