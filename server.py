#!/usr/bin/env python
import random
import socket
import time

s = socket.socket()         # Create a socket object
host = socket.getfqdn()     # Get local machine name
port = random.randint(8000, 9999)
s.bind((host, port))        # Bind to the port

print 'Starting server on', host, port
print 'The Web server URL for this would be http://%s:%d/' % (host, port)

s.listen(5)                 # Now wait for client connection.

print 'Entering infinite loop; hit CTRL-C to exit'
while True:
    # Establish connection with client.    
    c, (client_host, client_port) = s.accept()
    print c.recv(1000)
    print 'Got connection from', client_host, client_port
    c.send("HTTP/1.0 200 OK \r")
    c.send("Content-type: text/html\n\n")
    # @comment these lines are VERY long..try triple-quote strings instead?
    # e.g. content = '''
    # <html>
    #   <body>
    #     <h1>Howdy World</h1>
    #     <p>This is YourBestFriend's Web Server!</p>
    #     <script></script>
    #   </body>
    # </html>
    # '''
    # c.send(content)
    c.send("<html style='background-color: black;'>\n")
    c.send("<body style='border: 5px solid brown; border-radius: 500px; background-color: tan; font-style: italic; padding: 50px; display: inline-block; position: absolute; left: 25%; top: 25%;'>\n\n")
    c.send("<h1 id='header' style='color: black; opacity: .5;'>Howdy World ^_^</h1>\n")
    c.send("<p style='color: dimgray;'>This here is YourBestFriend's Web server!!!</p>\n")
    
    c.send("<script type='text/javascript'>\n")
    c.send("window.setInterval(function(){ changeColor(); }, 75);")
    c.send("var colour = 'red';")
    # @comment spelling nitpick: choose "colour" or "color", not both
    c.send("function changeColor(){ document.getElementById('header').style.color= colour; newColour();}")
    c.send("function newColour(){   if(colour == 'red'){colour = 'darkorange';} else if(colour == 'darkorange'){colour = 'yellow';} else if(colour == 'yellow'){colour = 'chartreuse';} else if(colour == 'chartreuse'){colour = 'cyan';} else if(colour == 'cyan'){colour = 'indigo';} else if(colour == 'indigo'){colour = 'red';}   }")
    c.send("</script>")

    c.send("</body>\n\n")
    c.send("</html>\n\n")
    c.close()
