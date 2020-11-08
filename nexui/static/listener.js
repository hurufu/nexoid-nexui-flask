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
    function make_id() {
        return get_header().map(function(x){return x.toString(16);}).join('');
    }
    function make_response(str) {
        var txt = Array.from(enc.encode(str));
        return new Uint8Array(get_header().concat(txt));
    }
    xf_fireEvent("request_log_model", "ui_request", {id: make_id()});
    sock.send(make_response('<ScapiResponse><ack/></ScapiResponse>'));
});
