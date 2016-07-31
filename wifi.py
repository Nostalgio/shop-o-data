from network import WLAN

class LocalWifi:
    """
    Create a local WiFi connection.
    """
    ssid = ''
    auth_mode = WLAN.WPA2
    auth_password = ''
    wlan = None

    def __init__(self, ssid, ssid_password):
        self.ssid = ssid
        self.auth_password = ssid_password
        self.wlan = WLAN(mode=WLAN.STA)

    def connect(self):
        self.wlan.scan()
        self.wlan.connect(ssid=self.ssid, auth=(self.auth_mode, self.auth_password))

        while not self.wlan.isconnected():
            print('.', end="")
        print("\nConnected to:\n", self.wlan.ifconfig())