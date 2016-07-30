from network import WLAN

class LocalWifi:
    """
    Create a local WiFi connection.
    """
    ssid = ''
    auth_mode = WLAN.WPA2
    auth_password = ''
    _wlan = None

    def __init__(self, ssid, ssid_password):
        self.ssid = ssid
        self.auth_password = ssid_password
        self._wlan = WLAN(mode=WLAN.STA)

    def connect(self):
        wlan.scan()
        wlan.connect(ssid=self.ssid, auth=(self.auth_mode, self.auth_password))

        while not wlan.isconnected():
            print('.', end="")
        print("\nConnected to:\n", wlan.ifconfig())
        return True