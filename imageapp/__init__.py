# __init__.py is the top level file in a Python package.

from quixote.publish import Publisher

# this imports the class RootDirectory from the file 'root.py'
from .root import RootDirectory
from . import html, image

def create_publisher():
     p = Publisher(RootDirectory(), display_exceptions='plain')
     p.is_thread_safe = True
     return p
 
def setup():                            # stuff that should be run once.
    html.init_templates()
    image.initialize()

    filename = "imageapp/dice.png"
    some_data = open(filename, 'rb').read()
    image.add_image(some_data, filename)
    

def teardown():                         # stuff that should be run once.
    pass
