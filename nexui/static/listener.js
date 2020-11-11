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
    function get_header() {
        return Array.from(new Uint8Array(msg)).slice(0, 4);
    }
    function get_payload() {
        return JSON.parse(dec.decode(msg.slice(4, msg.byteLength)));
    }
    function make_response(obj) {
        var txt = Array.from(enc.encode(JSON.stringify(obj)));
        return new Uint8Array(get_header().concat(txt));
    }
    xf_fireEvent("request_log_model", "request_log_event", get_payload());
    sock.send(make_response({ack: {}}));
});
