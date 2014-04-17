# image handling API
import mimetypes
import sqlite3
import os

IMAGE_DB_FILE = 'images.sqlite'

images = {}
names = {}

def initialize():
    load()

def load():
    global images
    global names

    # Create database file if nonexistent
    if os.path.exists(IMAGE_DB_FILE) == False:
        print 'DB doesn\'t exist...creating at', IMAGE_DB_FILE
        db = sqlite3.connect(IMAGE_DB_FILE)
        create_str = 'CREATE TABLE image_store (' + \
                     'i INTEGER PRIMARY KEY,' + \
                     'filename TEXT,' + \
                     'image BLOB' + \
                     ')'
        db.execute(create_str)
        db.commit()
        db.close()

    # open existing database
    db = sqlite3.connect(IMAGE_DB_FILE)
    db.text_factory = bytes
    c = db.cursor()

    c.execute('SELECT i, filename, image FROM image_store')

    results = c.fetchall()

    for i, filename, image in results:
        images[i] = image
        names[i] = filename
    print names

def save(data, filename, image_num):
    # connect to existing database
    db = sqlite3.connect(IMAGE_DB_FILE)
    # configure to allow binary insertions
    db.text_factory = bytes

    insert_str = 'INSERT INTO image_store (' + \
                 'i, '                       + \
                 'filename, '                + \
                 'image '                    + \
                 ')'                         + \
                 'VALUES ('                  + \
                 '?, '                       + \
                 '?, '                       + \
                 '?'                         + \
                 ')'
    db.execute(insert_str,(image_num, filename, data,))   
    db.commit()

def add_image(data, filename="dice.png"):
    # determine key value based on existing keys
    if images:
        image_num = max(images.keys()) + 1
    else:
        image_num = 0

    print "New image num is %d" % image_num
    
    # save to database
    save(data, filename, image_num)
    print images
    
    # update in local data structure
    images[image_num] = data
    names[image_num] = filename


    return image_num

def get_image(num):
    return images[num], mimetypes.guess_type(names[num])[0]

def get_latest_image():
    num = max(images.keys())
    return get_image(num)
