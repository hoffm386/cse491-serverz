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
    if os.path.exists(IMAGE_DB_FILE):
        db = sqlite3.connect(IMAGE_DB_FILE)
        db.text_factory = bytes
        c = db.cursor()

        c.execute('SELECT i, image FROM image_store ORDER BY i DESC')

        results = c.fetchall()

        for num, image in results:
            images[num] = image

def save(data, image_num):
    # connect to existing database
    db = sqlite3.connect(IMAGE_DB_FILE)
    # configure to allow binary insertions
    db.text_factory = bytes

    db.execute('INSERT INTO image_store (i, image) VALUES (?,?)', \
            (image_num, data,))
    db.commit()

def add_image(data, filename="dice.png"):
    if images:
        image_num = max(images.keys()) + 1
    else:
        image_num = 0
        
    images[image_num] = data
    names[image_num] = filename

    save(data, image_num)

    return image_num

def get_image(num):
    return images[num], mimetypes.guess_type(names[num])[0]

def get_latest_image():
    num = max(images.keys())
    return get_image(num)
