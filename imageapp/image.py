# image handling API
import mimetypes
import cPickle
import os

IMAGE_DB_FILE = 'images.db'

images = {}
names = {}

def initialize():
    load()

def load():
    global images
    if os.path.exists(IMAGE_DB_FILE):
        fp = open(IMAGE_DB_FILE, 'rb')
        images = cPickle.load(fp)
        fp.close()

        print 'Loaded: %d images' % (len(images))

def save():
    fp = open(IMAGE_DB_FILE, 'wb')
    cPickle.dump(images, fp)
    fp.close()

def add_image(data, filename="dice.png"):
    if images:
        image_num = max(images.keys()) + 1
    else:
        image_num = 0
        
    images[image_num] = data
    names[image_num] = filename

    save()
    
    return image_num

def get_image(num):
    return images[num], mimetypes.guess_type(names[num])[0]

def get_latest_image():
    num = max(images.keys())
    return get_image(num)
