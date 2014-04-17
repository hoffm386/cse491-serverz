#! /usr/bin/env python
import socket
import random
import argparse

from wsgiref.simple_server import make_server

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=0)
    parser.add_argument('-A', '--app', default='simple')

    args = parser.parse_args()
    port = args.port
    appname = args.app

    ###

    if appname == 'simple':
        from app import make_app
        the_wsgi_app = make_app()
    elif appname == 'imageapp':
        import imageapp, quixote
        imageapp.setup()

        p = imageapp.create_publisher()
        the_wsgi_app = quixote.get_wsgi_app()
    elif appname == 'cookie':
        import cookieapp
        the_wsgi_app = cookieapp.wsgi_app

    host = socket.getfqdn() # Get local machine name
    if port == 0:
        port = random.randint(8000, 9999)
    httpd = make_server('', port, the_wsgi_app)
    print "Serving at http://%s:%d/..." % (host, port,)
    httpd.serve_forever()

if __name__ == '__main__':
    main()
    
