import socket
from .secret import SSID, SSID_PASSWORD
from .wifi import LocalWifi

class Connection:
    """
    Create instance to POST data to Scaphold.io.
    """
    wlan = None
    is_connected = False

    def __init__(self):
        self.wlan = LocalWifi(ssid=SSID, ssid_password=SSID_PASSWORD)

    def connect(self):
        try:
            self.is_connected = self.wlan.connect()
        except:
            self.is_connected = False

    def test(self):
        if not self.is_connected:
            self.connect()
        addr = socket.getaddrinfo('micropython.org', 80)[0][-1]
        s = socket.socket()
        s.connect(addr)
        s.send(b'GET / HTTP/1.1\r\nHost: micropython.org\r\n\r\n')
        data = s.recv(1000)
        s.close()
        print(data)