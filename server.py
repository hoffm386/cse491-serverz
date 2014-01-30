#!/usr/bin/env python
import random
import socket
import time
import urlparse

def handle_index_get(conn, args):
    content_type = "text/html"
    body = """
    <h1>Hello, world.</h1>This is hoffm386's Web server.
    <ul>
        <li><a href='/content'>Content</a></li>
        <li><a href='/file'>File</a></li>
        <li><a href='/image'>Image</a></li>
        <li><a href='/form'>Form</a></li>
    </ul>
    """   
    conn.send("HTTP/1.0 200 OK\r\n")
    conn.send("Content-type: "+content_type+"\r\n\r\n")
    conn.send(body)

def handle_content_get(conn, args):
    content_type = "text/html"
    body = """
    <h1>Content</h1>
    This page will contain "content"
    """
    conn.send("HTTP/1.0 200 OK\r\n")
    conn.send("Content-type: "+content_type+"\r\n\r\n")
    conn.send(body)

def handle_file_get(conn, args):
    # once there is actual content here, there might be a type of
    # application/pdf instead of text/html
    content_type = "text/html"
    body = """
    <h1>File</h1>
    This page will contain "file"
    """
    conn.send("HTTP/1.0 200 OK\r\n")
    conn.send("Content-type: "+content_type+"\r\n\r\n")
    conn.send(body)

def handle_image_get(conn, args):
    # once there is actual content here, there might be a type of
    # image/jpeg or image/png
    content_type = "text/html"
    body = """
    <h1>Image</h1>
    This page will contain an "image"
    """
    conn.send("HTTP/1.0 200 OK\r\n")
    conn.send("Content-type: "+content_type+"\r\n\r\n")
    conn.send(body)

def handle_form_get(conn, args):
    content_type = "text/html"
    body = """
    <div>
        <h1>GET form</h1>
        <form action='/submit' method='GET'>
            <input type='text' name='firstname'>
            <input type='text' name='lastname'>
            <input type='submit' value='Submit'>
        </form>
    </div>
    <div>
        <h1>POST form</h1>
        <form action='/submit' method='POST'>
            <input type='text' name='firstname'>
            <input type='text' name='lastname'>
            <input type='submit' value='Submit'>
        </form>
    </div>
    """
    conn.send("HTTP/1.0 200 OK\r\n")
    conn.send("Content-type: "+content_type+"\r\n\r\n")
    conn.send(body)

def handle_submit(conn, args):
    first_name = args['firstname'][0]
    last_name = args['lastname'][0]
    content_type = "text/html"
    body = """
    <h1>Form Submission</h1>
    Hello Mr. %s %s.
    """ % (first_name, last_name)
    conn.send("HTTP/1.0 200 OK\r\n")
    conn.send("Content-type: "+content_type+"\r\n\r\n")
    conn.send(body)

def handle_post(conn, args):
    content_type = "text/html"
    body = """
    <h1>Post Request without args</h1>
    This is not actually what a post request should do, but I have received
    a post request
    """
    conn.send("HTTP/1.0 200 OK\r\n")
    conn.send("Content-type: "+content_type+"\r\n\r\n")
    conn.send(body)

# handles all HTTP GET requests
def handle_get_request(conn, path, args):
    if (path == "/"):
        handle_index_get(conn, args)
    elif (path == "/content"):
        handle_content_get(conn, args)
    elif (path == "/file"):
        handle_file_get(conn, args)
    elif (path == "/image"):
        handle_image_get(conn, args)
    elif (path == "/form"):
        handle_form_get(conn, args) 
    elif (path == "/submit"):
        handle_submit(conn, args)

# handles all HTTP POST requests
def handle_post_request(conn, path, args):
    if (path == "/"):
        handle_post(conn, args)
    elif (path == "/submit"):
        handle_submit(conn, args) 

# determines if connection is GET or POST and parses out path
def handle_connection(conn):
    request = conn.recv(1000)
    request_type = request.split(" ")[0]
    if (request_type == "GET"):
        # GET args come after the ? in the path
        path_and_args = request.split(" ")[1].split("?")
        path = path_and_args[0]
        # if args exist, send them, otherwise send empty dictionary
        if (len(path_and_args)>1):
            args = urlparse.parse_qs(path_and_args[1])
        else:
            args = {}
        handle_get_request(conn, path, args)
    elif (request_type == "POST"):
        # POST args come after the CRLF (in the message body)
        path = request.split(" ")[1]
        header_and_content = request.split("\r\n\r\n")
        # if args exist, send them, otherwise send emtpy dictionary
        if (len(header_and_content)>1):
            args = urlparse.parse_qs(header_and_content[-1])
        else:
            args = {}
        handle_post_request(conn, path, args)
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
