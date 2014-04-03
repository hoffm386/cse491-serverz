#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse
from StringIO import StringIO
from wsgiref.validate import validator
from sys import stderr
from argparse import ArgumentParser

# app.py
from app import make_app

# Quixote altdemo
import quixote
from quixote.demo.altdemo import create_publisher

# image app
import imageapp

# quotes app
from quotes.apps import QuotesApp

# chat app
from chat.apps import ChatApp

# list of available apps
WSGI_APPS = [          \
        "myapp",       \
        "altdemo",     \
        "image",       \
        "quotes",      \
        "chat",        \
        "default"      \
        ]

#
# "make" functions for various apps
# NOTE: make_app for my app was imported from app.py
#

def make_altdemo():
    create_publisher()
    return quixote.get_wsgi_app()

def make_imageapp():
    imageapp.setup()
    imageapp.create_publisher()
    return quixote.get_wsgi_app()

def make_quotesapp():
    # syntax from @ctb 's quote-server
    return QuotesApp('quotes/quotes.txt', 'quotes/html')

def make_chatapp():
    # syntax from @ctb 's chat-server
    return ChatApp('chat/html')

def select_app(input_str):
    if input_str == "myapp":
        return make_app()
    elif input_str == "altdemo":
        return make_altdemo()
    elif input_str == "image":
        return make_imageapp()
    elif input_str == "quotes":
        return make_quotesapp()
    elif input_str == "chat":
        return make_chatapp()
    else:
        # assume my app by default
        return make_app() 

def parse_commandline_args():
    parser = ArgumentParser(description="Run WSGI app")
    parser.add_argument("-A", default = "default", choices = WSGI_APPS, \
                        help="Which WSGI app to run")
    parser.add_argument("-p", default=0, type=int, \
                        help="Which port number to run the WSGI app on")
    return parser.parse_args()

def handle_connection(conn, port, app=make_app()):

    #
    # Get header stuff from conn, parse header stuff so we know how much content
    # stuff to get from conn, get content stuff from conn
    #

    # loop until we get all of the header stuff
    full_request = conn.recv(1)
    while full_request[-4:] != "\r\n\r\n":
        next_data = conn.recv(1)
        if next_data == "":
            return
        else:
            full_request += next_data

    # split header into first line and everything else
    first_line, request_args = full_request.split("\r\n",1)

    # make dictionary of header stuff
    headers = {}
    for line in request_args.split("\r\n")[:-2]:
        # every time there's a ": ", there's a header key/value pair
        key, value = line.split(": ",1)
        key = key.lower()
        headers[key] = value

    # extract path from first line and use parse_qs to get basic args
    path = urlparse(first_line.split(" ",3)[1])

    # set up "environ" thing for wsgi
    environ = {}
    environ["PATH_INFO"] = path[2]
    environ["QUERY_STRING"] = path[4]
    environ["SCRIPT_NAME"] = ""
    environ["SERVER_NAME"] = socket.getfqdn()
    environ["SERVER_PORT"] = str(port)
    # POST args come after the CRLF (in the message body), so we can't just get
    # the header, we need to grab "content-length" bits overall
    content = ""
    if (first_line.startswith("POST")):
        content_length = int(headers["content-length"])
        while len(content) < content_length:
            content += conn.recv(1)
        environ["REQUEST_METHOD"] = "POST"
        environ["CONTENT_LENGTH"] = str(content_length)
        environ["CONTENT_TYPE"] = headers["content-type"]
        print headers["content-type"]
    else:
        environ["REQUEST_METHOD"] = "GET"
        environ["CONTENT_LENGTH"] = "0"
        environ["CONTENT_TYPE"] = "text/html"
   
    # this function is nested inside handle_connection because I don't know
    # how else to get access to conn without making it a global variable
    def start_response(status, response_headers):
        conn.send('HTTP/1.0 ')
        conn.send(status)
        conn.send('\r\n')
        for pair in response_headers:
            key, header = pair
            conn.send(key + ': ' + header + '\r\n')
        conn.send('\r\n')

    # make content into a mysterious "StringIO" object
    content = StringIO(content)
    environ["wsgi.input"] = content
    environ["wsgi.version"] = (1, 0)
    environ["wsgi.errors"] = stderr
    environ["wsgi.multithread"] = False
    environ["wsgi.multiprocess"] = False
    environ["wsgi.run_once"] = False
    environ["wsgi.url_scheme"] = "http"
    if "cookie" in headers.keys():
        environ["HTTP_COOKIE"] = headers["cookie"]
    else:
        environ["HTTP_COOKIE"] = ""

    # wsgi validation
    the_app = validator(app)

    ret = the_app(environ, start_response)
    if (ret):
        for stuff in ret:
            conn.send(stuff)

    ret.close()
    conn.close()

def main():
    app_choice = parse_commandline_args()
    # the user types "-A appname", hence app_choice.A
    chosen_app = select_app(app_choice.A)
    
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    
    # the user types "-p portnumber", hence app_choice.p
    if app_choice.p == 0:
        #port = random.randint(8000, 9999)
        port = 8501
    else:
        port = app_choice.p
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c, port, chosen_app)

if __name__ == '__main__':
    main()
