import os
from gevent import Greenlet, sleep
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket import WebSocketHandler
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

from models import Session




def main():
    WSGIServer(("", 8000), Session, handler_class=WebSocketHandler).serve_forever()

if __name__ == "__main__":
    main()
