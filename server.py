#!/usr/bin/env python
import random
import socket
import time

# handles all HTTP GET requests
def handle_get_request(conn, path):
    content_type = ""
    body = ""
    if (path == "/"):
        content_type = "text/html"
        body = """
        <h1>Hello, world.</h1>This is hoffm386's Web server.
        <ul>
          <li><a href='/content'>Content</a></li>
          <li><a href='/file'>File</a></li>
          <li><a href='/image'>Image</a></li>
        </ul>
        """   
    elif (path == "/content"):
        content_type = "text/html"
        body = """
        <h1>Content</h1>
        This page will contain "content"
        """
    elif (path == "/file"):
        # once there is actual content here, there might be a type of
        # application/pdf instead of text/html
        content_type = "text/html"
        body = """
        <h1>File</h1>
        This page will contain "file"
        """
    elif (path == "/image"):
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

# handles all HTTP POST requests
def handle_post_request(conn, path):
    conn.send("HTTP/1.0 200 OK\r\n")
    conn.send("Content-type: text/html\r\n\r\n")
    body = """
    <h1>Post Request</h1>
    This is not actually what a post request will do, but I have received
    a post request
    """
    conn.send(body)

# determines if connection is GET or POST and parses out path
def handle_connection(conn):
    request = conn.recv(1000)
    request_type = request.split(" ")[0]
    path = request.split(" ")[1]
    if (request_type == "GET"):
        handle_get_request(conn, path)
    elif (request_type == "POST"):
        handle_post_request(conn, path)
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
