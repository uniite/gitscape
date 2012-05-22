import os
from gevent import Greenlet, sleep
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket import WebSocketHandler
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import json
import git

from struct import pack, unpack
import traceback

import controllers
import settings




def pack_data(data):
    return pack("!I", len(data)) + data

class Session(object):
    def __init__(self, environ, start_response):
        websocket = environ.get("wsgi.websocket")
        self.repo_list = [x.strip() for x in
                          open(settings.config_path("repos.lst"), "r").read().splitlines()
                          if x.strip()]
        self.repo = git.Repo(self.repo_list[0])
        if websocket is None:
            return None
        try:
            print "Got WebSocket connection"
            while True:
                request = websocket.receive()
                if request is None:
                    break
                else:
                    result = self.handle_request(json.loads(request))
                    if result:
                        websocket.send(json.dumps(result))
        except WebSocketError, ex:
            print "%s: %s" % (ex.__class__.__name__, ex)
        finally:
            websocket.close()


    def handle_request(self, request):
        print "Parsing request: %s" % request
        try:
            controller = getattr(controllers, request["controller"])
            action = getattr(controller, request["action"])
            args = request["args"] or []
            if "kwargs" in request:
                kwargs = request["kwargs"]
            else:
                kwargs = {}
            print "%s#%s => %s, %s" % (controller, action, args, kwargs)
        except AttributeError, e:
            print "Bad Request (AttributeError: %s)" % e.args
            return False
        except KeyError, e:
            print "Bad Request (KeyError: %s)" % e.args
            return False

        return action(self, *args, **kwargs)


    def send_obj(self, obj):
        try:
            self.socket.send(
                pack_data(obj.__class__.__name__) +
                pack_data(JSONEncoder().encode(obj)))
            print "Sent %s" % JSONEncoder().encode(obj)
            return True
        except Exception:
            print "Send error!"
            print traceback.format_exc()
            return False
