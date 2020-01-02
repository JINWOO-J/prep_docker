#!/usr/bin/env python3.6

import threading
import time
import sys
import os
import requests,json

try:
    # Python 2.x
    from SocketServer import ThreadingMixIn
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from BaseHTTPServer import HTTPServer
except ImportError:
    # Python 3.x
    from socketserver import ThreadingMixIn
    from http.server import SimpleHTTPRequestHandler, HTTPServer

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

class MyRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/check':
            # Create the response
            self.response = {
                "result": "OK"
            }
            self.protocol_version = 'HTTP/1.1'
            self.send_response(200, 'OK')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # self.wfile.write(bytes(json.dumps(self.response)))
            self.wfile.write(bytes(json.dumps(self.response), "utf-8"))
            # self.path = '/'
            return
            # return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

class ThreadingChecker(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, ipaddr=None, port=None, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
        self.ipaddr = ipaddr
        self.port = port
        self.count = 0
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            check_url = f"http://{self.ipaddr}:{self.port}/check"
            print(f'[{self.count}] Trying connect to {check_url}')
            self.count += 1
            time.sleep(self.interval)
            try:
                response = requests.get(f"{check_url}", verify=False, timeout=2)
                res_json = response.json().get("result","")
            except Exception as e:
                res_json = "FAIL"
                print(f"[FAIL] Cant accessible - {self.ipaddr}:{self.port} -> {e}")
            if res_json == "OK":
                print(f"[OK] Accessible - {self.ipaddr}:{self.port}")
                os._exit(0)

def getExtIPaddr():
    url = "https://ipinfo.io/"
    try:
        r = requests.get(url,verify=False)
    except:
        print("error while querying info...")
        sys.exit()
    data = json.loads(r.text)
    return data.get("ip", "[NO DATA]")


if sys.argv[1:]:
    address = sys.argv[1]
    if (':' in address):
        interface = address.split(':')[0]
        port = int(address.split(':')[1])
    else:
        interface = '0.0.0.0'
        port = int(address)
else:
    port = 8000
    interface = '0.0.0.0'

if sys.argv[2:]:
    os.chdir(sys.argv[2])

print('Started HTTP server on ' + interface + ':' + str(port))
SimpleHTTPRequestHandler = MyRequestHandler
server = ThreadingSimpleServer((interface, port), SimpleHTTPRequestHandler)

if interface == "0.0.0.0":
    check_ip = getExtIPaddr()
    print( "Your externel IP : " + check_ip)
else:
    check_ip = interface

checker = ThreadingChecker(ipaddr=check_ip, port=port)

try:
    while 1:
        # print("start")
        sys.stdout.flush()
        server.handle_request()

except KeyboardInterrupt:
    print(' Finished.')
