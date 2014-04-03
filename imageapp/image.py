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
    #if os.path.exists(IMAGE_DB_FILE):
    if True:
        print 'DB exists'

        db = sqlite3.connect(IMAGE_DB_FILE)
        db.text_factory = bytes
        c = db.cursor()

        c.execute('SELECT i, filename, image FROM image_store ORDER BY i DESC')

        print 'First result from selection:\n'
        print c.fetchone()
        results = c.fetchall()
        print results

        for num, name, image in results:
            images[num] = image
            names[num] = name
    print names
def save(data, filename, image_num):
    # connect to existing database
    db = sqlite3.connect(IMAGE_DB_FILE)
    # configure to allow binary insertions
    db.text_factory = bytes

    insert_str = 'INSERT INTO image_store (' + \
                 'i, '                       + \
                 'filename, '                + \
                 'image, '                   + \
                 ')'                         + \
                 'VALUES ('                  + \
                 '?, '                       + \
                 '?, '                       + \
                 '?'                         + \
                 ')'
    db.execute(insert_str, ( \
                image_num,   \
                filename,    \
                data,        \
                )            \
              )   
    db.commit()

def add_image(data, filename="dice.png"):
    if images:
        image_num = max(images.keys()) + 1
    else:
        image_num = 0

    print "New image num is %d" % image_num
    print images
    images[image_num] = data
    names[image_num] = filename

    save(data, filename, image_num)

    return image_num

def get_image(num):
    return images[num], mimetypes.guess_type(names[num])[0]

def get_latest_image():
    load()
    num = max(images.keys())
    return get_image(num)
