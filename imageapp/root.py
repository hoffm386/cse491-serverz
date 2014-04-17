import quixote
from quixote.directory import Directory, export, subdir
from quixote.util import StaticDirectory
import os

from . import html, image

class RootDirectory(Directory):
    _q_exports = ['static']
    static = StaticDirectory(os.path.join(os.path.dirname(__file__),'static'))

    @export(name='')                    # this makes it public.
    def index(self):
        return html.render('index.html')

    @export(name='jquery')
    def jquery(self):
        return open('jquery-1.3.2.min.js').read()

    @export(name='upload')
    def upload(self):
        return html.render('upload.html')

    @export(name='upload_receive')
    def upload_receive(self):
        request = quixote.get_request()
        print request.form.keys()

        the_file = request.form['file']
        print dir(the_file)
        print 'received file with name:', the_file.base_filename
        data = the_file.read(int(1e9))

        image.add_image(data, the_file.base_filename)

        return quixote.redirect('./')

    @export(name='upload2')
    def upload2(self):
        return html.render('upload2.html')

    @export(name='upload2_receive')
    def upload2_receive(self):
        request = quixote.get_request()
        print request.form.keys()

        the_file = request.form['file']
        print dir(the_file)
        print 'received file with name:', the_file.base_filename
        data = the_file.read(int(1e9))

        image.add_image(data)

        return html.render('upload2_received.html')

    @export(name='image')
    def image(self):
        return html.render('image.html')

    @export(name='image_list')
    def image_list(self):
        image_num = image.get_image_num()
        info = {'num_images': image_num}
        return html.render('image_list.html', info)

    @export(name='image_raw')
    def image_raw(self):
        response = quixote.get_response()
        request = quixote.get_request()

        # if the user is requesting a particular image, serve it
        if 'num' in request.form.keys():
            try:
                image_num = int(request.form['num'].encode('ascii'))
            except:
                print "parsing error.  showing latest image"
                image_num = image.get_image_num()

            image_count = image.get_image_num()

            # instead of error message-ing for too high or low, just reset
            # to min or max
            if image_num < 0:
                image_num = 0
            if image_num > image_count:
                image_num = image_count

            img, content_type = image.get_image(image_num)
        # otherwise, serve the latest image
        else:
            img, content_type = image.get_latest_image()
        
        response.set_content_type(content_type)
        return img
