#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse, parse_qs
from cgi import FieldStorage
from StringIO import StringIO
from jinja2 import FileSystemLoader, Environment
from app import make_app

def handle_connection(conn):

    

    #
    # Get header stuff from conn, parse header stuff so we know how much content
    # stuff to get from conn, get content stuff from conn
    #

    # loop until we get all of the header stuff
    full_request = conn.recv(1)
    while full_request[-4:] != "\r\n\r\n":
        full_request += conn.recv(1)

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
     
    # POST args come after the CRLF (in the message body), so we can't just get
    # the header, we need to grab "content-length" bits overall
    content = ""
    if (first_line.startswith("POST")):
        content_length = int(headers["content-length"])
        while len(content) < content_length:
            content += conn.recv(1)
        environ["REQUEST_METHOD"] = "POST"
        environ["CONTENT_LENGTH"] = content_length
        environ["CONTENT_TYPE"] = headers["content-type"]
    else:
        environ["REQUEST_METHOD"] = "GET"
        environ["CONTENT_LENGTH"] = 0
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
    the_app = make_app()
    ret = the_app(environ, start_response)
    for stuff in ret:
        conn.send(stuff)

    conn.close()

def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c)

if __name__ == '__main__':
    main()
