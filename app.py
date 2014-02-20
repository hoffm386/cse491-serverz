#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse, parse_qs
from cgi import FieldStorage
from StringIO import StringIO
from jinja2 import FileSystemLoader, Environment
from wsgiref.util import setup_testing_defaults

# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults
def simple_app(environ, start_response):
    iter_items = parse_qs(environ["QUERY_STRING"]).iteritems()
    args = {key:value[0] for key, value in iter_items}
    args["path"] = environ["PATH_INFO"]

    # Grab POST args if there are any
    if environ['REQUEST_METHOD'] == 'POST':
        headers = dict()

        for key, value in environ.iteritems():
            if key.startswith("HTTP"):
                header_key_string = key[5:]
                # environ keys look like "CONTENT_TYPE", while header keys look
                # like "content-type", hence this reformatting
                header_key_string = header_key_string.lower()
                header_key_string = header_key_string.replace("_","-")
                headers[header_key_string] = value

        headers['content-type'] = environ['CONTENT_TYPE']
        headers['content-length'] = environ['CONTENT_LENGTH']
        
        # use the mysterious "cgi.FieldStorage" module to fill args variable
        # mapping we will use to go from path to  html
        field_storage = FieldStorage(fp=environ['wsgi.input'], \
                                     headers=headers, environ=environ)
        for key in field_storage.keys():
            # the value goes into a list because that's what parse_qs does, and
            # it would be silly to have different html pages for GET vs POST form
            # submission
            args.update({key:[field_storage[key].value]})

    #
    # Now that we have our shiny args object, use "jinja2" and map the request
    # path to the right HTML template (or 404 if invalid)
    #

    loader = FileSystemLoader("./templates")
    environment = Environment(loader=loader)
    response_headers = [('Content-type', 'text/html')]
    

    page = environ["PATH_INFO"]
    if page == "/":
        status, template = handle_index_get(environment)
    elif page == "/content":
        status, template = handle_content_get(environment)
    elif page == "/file":
        status, template = handle_file_get(environment)
    elif page == "/image":
        status, template = handle_image_get(environment)
    elif page == "/form":
        status, template = handle_form_get(environment)
    elif page == "/submit":
        status, template = handle_submit(environment)
    else:
        args["path"] = page
        status, template = handle_404(environment)

    start_response(status, response_headers)

    return template.render(args)

##    ret = ["%s: %s\n" % (key, value)
##           for key, value in environ.iteritems()]
##    ret.insert(0, "This is your environ.  Hello, world!\n\n")
##
##    return ret

def make_app():
    return simple_app

def handle_index_get(environment):
    status = "200 OK"
    template = environment.get_template("index.html")
    return status, template

def handle_content_get(environment):
    status = "200 OK"
    template = environment.get_template("content.html")
    return status, template

def handle_file_get(environment):
    status = "200 OK"
    # once there is actual content here, there might be a type of
    # application/pdf instead of text/html
    template = environment.get_template("file.html")
    return status, template

def handle_image_get(environment):
    status = "200 OK"
    # once there is actual content here, there might be a type of
    # image/jpeg or image/png
    template = environment.get_template("image.html")
    return status, template

def handle_form_get(environment):
    status = "200 OK"
    template = environment.get_template("form.html")
    return status, template

def handle_submit(environment):
    status = "200 OK"
    template = environment.get_template("submit.html")
    return status, template

def handle_404(environment):
    status = "404 Not Found"
    template = environment.get_template("404.html")
    return status, template

