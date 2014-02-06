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
    body = """
    <h1>Hello, world.</h1>This is hoffm386's Web server.
    <ul>
        <li><a href='/content'>Content</a></li>
        <li><a href='/file'>File</a></li>
        <li><a href='/image'>Image</a></li>
        <li><a href='/form'>Form</a></li>
    </ul>
    """
    expected_return = header + body
    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_content_get():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    header = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n' + \
             '\r\n'
    body = """
    <h1>Content</h1>
    This page will contain "content"
    """
    expected_return = header + body
    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_file_get():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    header = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n' + \
             '\r\n'
    body = """
    <h1>File</h1>
    This page will contain "file"
    """
    expected_return = header + body
    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_image_get():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    header = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n' + \
             '\r\n'
    body = """
    <h1>Image</h1>
    This page will contain an "image"
    """
    expected_return = header + body
    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_form_get():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")
    header = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n' + \
             '\r\n'
    body = """
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
    """
    expected_return = header + body
    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_post():
    conn = FakeConnection("POST / HTTP/1.1\r\n\r\n")
    header = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n' + \
             '\r\n'
    body = """
    <h1>Post Request without args</h1>
    This is not actually what a post request should do, but I have received
    a post request
    """
    expected_return = header + body
    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_submit_get():
    get_args = "?firstname=John&lastname=Smith"
    conn = FakeConnection("GET /submit%s HTTP/1.1\r\n\r\n" % (get_args))
    header = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n' + \
             '\r\n'
    body = """
        <h1>Form Submission</h1>
        Hello Mr. John Smith.
        """
    expected_return = header + body
    server.handle_connection(conn)
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
    body = """
        <h1>Form Submission</h1>
        Hello Mr. John Smith.
        """
    expected_return = header + body
    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_submit_post_no_args():
    conn_string = "POST /submit HTTP/1.1\r\n" + \
                  "Host: arctic.cse.msu.edu:8987\r\n" + \
                  "Accept: text/html,application/xhtml+xml,application/xml;" +\
                  "q=0.9,*/*;q=0.8\r\n" + \
                  "Referer: http://arctic.cse.msu.edu:8987/form\r\n" + \
                  "Content-Type: application/x-www-form-urlencoded\r\n" + \
                  "Content-Length: 29\r\n\r\n"
    conn = FakeConnection(conn_string)
    header = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n' + \
             '\r\n'
    body = """
        <h1>Form Submission</h1>
        Hello, you didn't submit any data.
        """
    expected_return = header + body
    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

