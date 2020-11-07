var sock = new Socket({
    protocol: 'req.sp.nanomsg.org',
    debug: false,
    sendArrayBuffer: true,
    receiveArrayBuffer: true,
});

sock.connect('ws' + '://' + location.hostname + ':' + 51004 + '/');

var dec = new TextDecoder('utf-8');
var enc = new TextEncoder();

sock.on('data', function(msg) {
    function make_response(str) {
        var txt = Array.from(enc.encode(str));
        var hdr = Array.from(new Uint8Array(msg)).slice(0, 4);
        var rsp = new Uint8Array(hdr.concat(txt));
        return rsp;
    }
    sock.send(make_response('<ScapiResponse><ack/></ScapiResponse>'));
});
