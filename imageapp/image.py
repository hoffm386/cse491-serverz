# image handling API
import mimetypes

images = {}
names = {}

def add_image(data, filename = "dice.png"):
    if images:
        image_num = max(images.keys()) + 1
    else:
        image_num = 0
        
    images[image_num] = data
    names[image_num] = filename
    return image_num

def get_image(num):
    return images[num], mimetypes.guess_type(names[num])[0]

def get_latest_image():
    num = max(images.keys())
    return get_image(num)
