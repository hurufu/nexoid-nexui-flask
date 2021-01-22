'''Main entry for standalone server'''
from gevent.pywsgi import WSGIServer
from . import app

http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()
