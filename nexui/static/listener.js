var socket = io();

socket.on('connect', function() {
    socket.send(null);
});

socket.on('message', function(dt) {
    console.log(dt);
    socket.send('<ScapiResponse><ack/></ScapiResponse>');
});
