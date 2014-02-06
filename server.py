#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse, parse_qs
from cgi import FieldStorage
from StringIO import StringIO
from jinja2 import FileSystemLoader, Environment

def handle_index_get(conn, environment, args):
    content_type = "text/html"
    conn.send("HTTP/1.0 200 OK\r\nContent-type: "+content_type+"\r\n\r\n")
    template = environment.get_template("index.html")
    conn.send(template.render(args))

def handle_content_get(conn, environment, args):
    content_type = "text/html"
    conn.send("HTTP/1.0 200 OK\r\nContent-type: "+content_type+"\r\n\r\n")
    template = environment.get_template("content.html")
    conn.send(template.render(args))

def handle_file_get(conn, environment, args):
    # once there is actual content here, there might be a type of
    # application/pdf instead of text/html
    content_type = "text/html"
    conn.send("HTTP/1.0 200 OK\r\nContent-type: "+content_type+"\r\n\r\n")
    template = environment.get_template("file.html")
    conn.send(template.render(args))

def handle_image_get(conn, environment, args):
    # once there is actual content here, there might be a type of
    # image/jpeg or image/png
    content_type = "text/html"
    conn.send("HTTP/1.0 200 OK\r\nContent-type: "+content_type+"\r\n\r\n")
    template = environment.get_template("image.html")
    conn.send(template.render(args))

def handle_form_get(conn, environment, args):
    content_type = "text/html"
    conn.send("HTTP/1.0 200 OK\r\nContent-type: "+content_type+"\r\n\r\n")
    template = environment.get_template("form.html")
    conn.send(template.render(args))

def handle_submit(conn, environment, args):
    content_type = "text/html"
    conn.send("HTTP/1.0 200 OK\r\nContent-type: "+content_type+"\r\n\r\n")
    template = environment.get_template("submit.html")
    conn.send(template.render(args))

def handle_404(conn, environment, args):
    conn.send("HTTP/1.0 404 Not Found\r\n\r\n")
    template = environment.get_template("404.html")
    conn.send(template.render(args))

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
    
    # POST args come after the CRLF (in the message body), so we can't just get
    # the header, we need to grab "content-length" bits overall
    content = ""
    if (first_line.startswith("POST")):
        content_length = int(headers["content-length"])
        while len(content) < content_length:
            content += conn.recv(1)
   
    #
    # Now that we have everything we need from conn, start building the response
    # args object
    #

    # make content into a mysterious "StringIO" object
    content = StringIO(content)

    # extract path from first line and use parse_qs to get basic args
    path = urlparse(first_line.split(" ",3)[1])
    args = parse_qs(path[4])

    # use the mysterious "cgi.FieldStorage" module to fill args variable
    # mapping we will use to go from path to  html
    field_storage = FieldStorage(fp=content, headers=headers, \
                                 environ={"REQUEST_METHOD":"POST"})
    for key in field_storage.keys():
        # the value goes into a list because that's what parse_qs does, and it
        # would be silly to have different html pages for GET vs POST form
        # submission
        args.update({key:[field_storage[key].value]})

    #
    # Now that we have our shiny args object, use "jinja2" and map the request
    # path to the right HTML template (or 404 if invalid)
    #

    loader = FileSystemLoader("./templates")
    environment = Environment(loader=loader)

    page = path[2]
    if page == "/":
        handle_index_get(conn, environment, args)
    elif page == "/content":
        handle_content_get(conn, environment, args)
    elif page == "/file":
        handle_file_get(conn, environment, args)
    elif page == "/image":
        handle_image_get(conn, environment, args)
    elif page == "/form":
        handle_form_get(conn, environment, args)
    elif page == "/submit":
        handle_submit(conn, environment, args)
    else:
        args["path"] = page
        handle_404(conn, environment, args)

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
