import usocket
import ujson
try:
    import ussl
    SUPPORT_SSL = True
except ImportError:
    ussl = None
    SUPPORT_SSL = False

SUPPORT_TIMEOUT = hasattr(usocket.socket, 'settimeout')
CONTENT_TYPE_JSON = 'application/json'


class Response(object):
    def __init__(self, status_code, raw):
        self.status_code = status_code
        self.raw = raw
        self._content = False
        self.encoding = 'utf-8'

    @property
    def content(self):
        if self._content is False:
            self._content = self.raw.read()
            self.raw.close()
            self.raw = None

        return self._content

    @property
    def text(self):
        content = self.content

        return str(content, self.encoding) if content else ''

    def close(self):
        if self.raw is not None:
            self._content = None
            self.raw.close()
            self.raw = None

    def json(self):
        return ujson.loads(self.text)

    def raise_for_status(self):
        if 400 <= self.status_code < 500:
            raise OSError('Client error: %s' % self.status_code)
        if 500 <= self.status_code < 600:
            raise OSError('Server error: %s' % self.status_code)


# Adapted from upip
def request(method, url, json=None, timeout=None, headers=None):
    urlparts = url.split('/', 3)
    proto = urlparts[0]
    host = urlparts[2]
    urlpath = '' if len(urlparts) < 4 else urlparts[3]

    if proto == 'http:':
        port = 80
    elif proto == 'https:':
        port = 443
    else:
        raise OSError('Unsupported protocol: %s' % proto[:-1])

    if ':' in host:
        host, port = host.split(':')
        port = int(port)

    if json is not None:
        content = ujson.dumps(json)
        content_type = CONTENT_TYPE_JSON
    else:
        content = None

    ai = usocket.getaddrinfo(host, port)
    addr = ai[0][-1]

    sock = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM, usocket.IPPROTO_SEC)

    if timeout is not None:
        assert SUPPORT_TIMEOUT, 'Socket does not support timeout'
        sock.settimeout(timeout)

    if proto == 'https:':
        assert SUPPORT_SSL, 'HTTPS not supported: could not find ussl'
        sock = ussl.wrap_socket(sock)

    sock.connect(addr)

    sock.write('%s /%s HTTP/1.1\r\nHost: %s\r\n' % (method, urlpath, host))

    if headers is not None:
        for header in headers.items():
            sock.write('%s: %s\r\n' % header)

    if content is not None:
        # sock.write('authorization: %s\r\n' % 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3NjYXBob2xkLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1NzkwNGRlY2NjZjI5ZjAyMmQwZTk0MTEiLCJhdWQiOiJKdGdmeVpJUTJwSmo5ckk4RTllNjE3aFFjazBSbnhBbiIsImV4cCI6MTQ3MTY2NjkyNSwiaWF0IjoxNDY5MDc0OTI1fQ.WQiyNMzkL7djIj8g2-LgrWIsut68pbGp1c9dJ7i_JPc')
        sock.write('content-length: %s\r\n' % len(content))
        sock.write('content-type: %s\r\n' % content_type)
        sock.write('\r\n')
        sock.write(content)
    else:
        sock.write('\r\n')

    l = sock.readline()
    protover, status, msg = l.split(None, 2)

    # Skip headers
    while sock.readline() != b'\r\n':
        pass

    return Response(int(status), sock)


def get(url, **kwargs):
    return request('GET', url, **kwargs)


def post(url, **kwargs):
    return request('POST', url, **kwargs)