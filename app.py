#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse, parse_qs
from cgi import FieldStorage
from StringIO import StringIO
from jinja2 import FileSystemLoader, Environment
from wsgiref.util import setup_testing_defaults

"""
A relatively simple WSGI application.
 1) Parses environ dictionary into args dictionary
 -  args is in the appropriate format for jinja
 2) Uses jinja2 to render the HTML templates
 -  Creates jinja environment variable pointing at the templates folder
 -  The relevant handler function uses this variable to get the appropriate
    status, response headers, and response content
 3) Passes status and response headers to start_response function
 4) Returns response content
 @param environ A dictionary of information in WSGI format
 @param start_response A function which begins the server response
 @returns The response body (HTML, image, or plain text)
"""
def simple_app(environ, start_response):

    # Use urlparse module to create args dictionary from environ
    args = dict()
    qs = parse_qs(environ["QUERY_STRING"])
    for key, value in qs.iteritems():
        args[key] = value
    args["path"] = environ["PATH_INFO"]

    # POST args are more complicated
    if environ['REQUEST_METHOD'] == 'POST':
        # Create request headers dictionary out of environ data
        # This will be used by the cgi module to update args
        headers = dict()
        for key, value in environ.iteritems():
            if key.startswith("HTTP"):
                environ_key_string = key[5:]
                # environ keys look like "CONTENT_TYPE", while header keys look
                # like "content-type", hence this reformatting
                lowercase_key_string = environ_key_string.lower()
                header_key_string = lowercase_key_string.replace("_","-")
                headers[header_key_string] = value

        headers['content-type'] = environ['CONTENT_TYPE']
        headers['content-length'] = environ['CONTENT_LENGTH']
        
        fp = environ["wsgi.input"]
        
        # In POST, overwrite what parse_qs put into args with values from
        # the cgi module's FieldStorage
        field_storage = FieldStorage(fp=fp, headers=headers, environ=environ)
        for key in field_storage.keys():
            args.update({key:field_storage[key].value})

    # Create a jinja2 environment pointing at the templates folder
    loader = FileSystemLoader("./templates")
    j_environ = Environment(loader=loader)
    
    # Pass jinja2 environment and args dictionary to the relevant function based
    # on the request path
    page = args["path"]
    if page == "/":
        status, content, response_headers = handle_index_get(j_environ, args)
    elif page == "/content":
        status, content, response_headers = handle_content_get(j_environ, args)
    elif page == "/file":
        status, content, response_headers = handle_file_get(j_environ, args)
    elif page == "/image":
        status, content, response_headers = handle_image_get(j_environ, args)
    elif page == "/form":
        status, content, response_headers = handle_form_get(j_environ, args)
    elif page == "/submit":
        status, content, response_headers = handle_submit(j_environ, args)
    else:
        args["path"] = page
        status, content, response_headers = handle_404(j_environ, args)

    # Call start_reponse function (which was passed in as a parameter) with
    # the status and response headers returned by handling function
    start_response(status, response_headers)

    # Return content returned by handling function
    return content

"""
I'm not entirely sure why, but wsgi needs to call this function to access the
main app function
"""
def make_app():
    return simple_app

"""
Index handler
@param environment The jinja2 environment
@param args The args dictionary jinja2 needs to render the template
@returns "200 OK" (the request was successful)
         HTML of index page
         Headers indicating type text/html
"""
def handle_index_get(environment, args):
    status = "200 OK"
    template = environment.get_template("index.html")
    response_headers = []
    response_headers.append(('Content-type', 'text/html'))
    return status, template.render(args), response_headers

def handle_content_get(environment, args):
    status = "200 OK"
    template = environment.get_template("content.html")
    response_headers = []
    response_headers.append(('Content-type', 'text/html'))
    return status, template.render(args), response_headers

def handle_file_get(environment, args):
    status = "200 OK"
    # once there is actual content here, there might be a type of
    # application/pdf instead of text/html
    text_file = open_file("files/city_all.txt")
    response_headers = []
    response_headers.append(('Content-type', 'text/html'))
    return status, text_file, response_headers

def handle_image_get(environment, args):
    status = "200 OK"
    # once there is actual content here, there might be a type of
    # image/jpeg or image/png
    image = open_file("img/galaxy.jpg")
    response_headers = []
    response_headers.append(('Content-type', 'image/jpeg'))
    return status, image, response_headers

def handle_form_get(environment, args):
    status = "200 OK"
    template = environment.get_template("form.html")
    response_headers = []
    response_headers.append(('Content-type', 'text/html'))
    return status, template.render(args), response_headers

def handle_submit(environment, args):
    status = "200 OK"
    template = environment.get_template("submit.html")
    response_headers = []
    response_headers.append(('Content-type', 'text/html'))
    return status, template.render(args), response_headers

def handle_404(environment, args):
    status = "404 Not Found"
    template = environment.get_template("404.html")
    response_headers = []
    return status, template.render(args), response_headers

def open_file(filename):
    fp = open(filename, "rb")
    data = fp.read()
    fp.close()
    return data

