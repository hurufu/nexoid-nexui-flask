# Nexo-in-the-cloud demo web application 

See [live demo](https://nexoweb.online/nexo) now!

## Building

Given `$DSTDIR` is your Python prefix, just do:

```sh
python setup.py build
python setup.py install -O1 --root=$DSTDIR --skip-build
```

Then run it:

```sh
python -m nexui
```

It will listen on port 5000 for incomming, connection. Actuall deployment is
up to you, in the live instance I have `nginx` listtening on port 80 and proxying
requests to that python module while serving all static files:

```
 server {
	location /static {
		alias $DSTDIR/nexui/static;
		expires 3d;
		add_header Cache-Control "public";
	}

	location /ws {
		proxy_pass http://localhost:51004/;
		proxy_http_version 1.1;
		proxy_set_header Upgrade $http_upgrade;
		proxy_set_header Connection "Upgrade";
		proxy_set_header Host $host;
	}

    location / {
		proxy_pass http://localhost:5000;
		proxy_http_version 1.1;
		proxy_set_header Connection "";
		proxy_set_header Host $host;
    }
}
```
## Architecture

It uses [XForms](https://github.com/AlainCouthures/declarative4all) framework,
and is very basic from the GUI perspective. Single XML to send an event to SCAP,
and display all interactions that SCAP is requesting.

Back-end is responsible to spawning `nexoid-cpp` to process transaction and then
actual SCAP is implemented in Python - it translates messages and just sends
them to the front-end for a display. Very basic stuff, useful for debugging and
testing though.
