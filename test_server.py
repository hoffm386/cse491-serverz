import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

# Test a basic GET call.

def test_handle_index_get():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    header = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n' + \
             '\r\n'
    body = """<html>
    <body>
        <h1>Hello, world.</h1>This is hoffm386's Web server.
        <ul>
            <li><a href='/content'>Content</a></li>
            <li><a href='/file'>File</a></li>
            <li><a href='/image'>Image</a></li>
            <li><a href='/form'>Form</a></li>
        </ul>
    </body>
</html>
"""
    expected_return = header + body
    server.handle_connection(conn, 8500)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_content_get():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    header = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n' + \
             '\r\n'
    body = """<html>
    <body>
        <h1>Content</h1>
        This page will contain "content"
    </body>
</html>"""
    expected_return = header + body
    server.handle_connection(conn, 8500)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_file_get():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    header = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/plain\r\n' + \
             '\r\n'
    expected_return = header
    server.handle_connection(conn, 8500)
    assert conn.sent.startswith(expected_return), 'Got: %s' % (repr(conn.sent),)

def test_handle_image_get():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    header = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: image/jpeg\r\n' + \
             '\r\n'
    expected_return = header
    server.handle_connection(conn, 8500)
    assert conn.sent.startswith(expected_return), 'Got: a long string' 
    #% (repr(conn.sent),)

def test_handle_form_get():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")
    header = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n' + \
             '\r\n'
    body = """<html>
    <body>
        <div>
            <h1>GET form</h1>
            <form action='/submit' method='GET'>
                <input type='text' name='firstname'>
                <input type='text' name='lastname'>
                <input type='submit' value='Submit'>
            </form>
        </div>
        <div>
            <h1>POST form</h1>
            <form action='/submit' method='POST'>
                <input type='text' name='firstname'>
                <input type='text' name='lastname'>
                <input type='submit' value='Submit'>
            </form>
        </div>
    </body>
</html>"""
    expected_return = header + body
    server.handle_connection(conn, 8500)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_404_get():
    conn = FakeConnection("GET /asdf HTTP/1.0\r\n\r\n")
    header = 'HTTP/1.0 404 Not Found\r\n' + \
             'Content-type: text/html\r\n' + \
             '\r\n'
    body = """<html>
    <body>
        <h1>404</h1>
        <p>The page at /asdf could not be found</p>
        <p>To return to the home page, click <a href='/'>here</a></p>
    </body>
</html>"""
    expected_return = header + body
    server.handle_connection(conn, 8500)
    assert conn.sent == expected_return, 'Expected: %s\nGot: %s' % \
                         (repr(expected_return),repr(conn.sent),)

def test_post_urlencoded():
    first = "Erin"
    last = "Hoffman"
    fake_str = "POST /submit HTTP/1.1\r\n" + \
               "Content-Length: 31\r\n" + \
               "Content-Type: application/x-www-form-urlencoded\r\n\r\n" + \
               "firstname={0}&lastname={1}\r\n".format(first, last)
    conn = FakeConnection(fake_str)
    header = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n' + \
             '\r\n'
    body = """<html>
    <body>
        <h1>Form Submission</h1>
        Hello Mr. Erin Hoffman.
    </body>
</html>"""
    expected_return = header + body
    server.handle_connection(conn, 8500)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_submit_post():
    conn_string = "POST /submit HTTP/1.1\r\n" + \
                  "Host: arctic.cse.msu.edu:8987\r\n" + \
                  "Accept: text/html,application/xhtml+xml,application/xml;" +\
                  "q=0.9,*/*;q=0.8\r\n" + \
                  "Referer: http://arctic.cse.msu.edu:8987/form\r\n" + \
                  "Content-Type: application/x-www-form-urlencoded\r\n" + \
                  "Content-Length: 29\r\n\r\n" + \
                  "firstname=John&lastname=Smith"
    conn = FakeConnection(conn_string)
    header = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n' + \
             '\r\n'
    body = """<html>
    <body>
        <h1>Form Submission</h1>
        Hello Mr. John Smith.
    </body>
</html>"""
    expected_return = header + body
    server.handle_connection(conn, 8500)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)


