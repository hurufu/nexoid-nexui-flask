var sock = new Socket({
    protocol: 'req.sp.nanomsg.org',
    debug: false,
    sendArrayBuffer: true,
    receiveArrayBuffer: true,
});

sock.connect('ws' + '://' + location.hostname + ':' + 51004 + '/');

var dec = new TextDecoder('utf-8');
var enc = new TextEncoder();

var last_msg = null;

function nexui_send(obj) {
    function make_response(obj) {
        function get_header() {
            return Array.from(new Uint8Array(last_msg)).slice(0, 4);
        }
        var txt = Array.from(enc.encode(JSON.stringify(obj)));
        return new Uint8Array(get_header().concat(txt));
    }

    sock.send(make_response(obj));
}

function nexui_ack() {
    nexui_send({ack: null});
}

function nexui_ack_cvdPresence(presence) {
    nexui_send({ackEntry: [{cvdPresence: presence}]});
}

sock.on('data', function(msg) {
    function get_payload() {
        return JSON.parse(dec.decode(msg.slice(4, msg.byteLength)));
    }
    last_msg = msg;
    var req = get_payload();
    req.payload.forEach(function(e) {
        xf_fireEvent("request_log_model", "request_log_event", {source: req.source.type, api: e.api, line: String(e.line)});
    });
});
