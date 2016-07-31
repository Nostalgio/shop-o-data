import socket, http_client
from secret import SSID, SSID_PASSWORD, API_KEY
from wifi import LocalWifi

class Connection:
    """
    Create instance to POST data to Scaphold.io.
    """
    wlan = None
    is_connected = False
    scaphold_host = "api.scaphold.io"

    def __init__(self):
        self.wlan = LocalWifi(ssid=SSID, ssid_password=SSID_PASSWORD)
        self.scaphold_url = "{0}/graphql/{1}".format(
                self.scaphold_host, API_KEY)

    def connect(self):
        try:
            self.wlan.connect()
            self.is_connected = True
        except:
            self.is_connected = False

    def post_to_scaphold(self):
        if not self.is_connected:
            self.connect()
        request = http_client.post(
            'https://api.scaphold.io/graphql/{0}'.format(API_KEY),json={
            "query": "mutation CreateTrafficMut($input: _CreateTrafficInput!) {createTraffic(input: $input) {changedTraffic {id,sensor {id,location}createdAt}}}",
            "variables": {
                "input": {
                    "sensorId": "NTk0ZTVlNzQtNDA1Mi00OWFjLWI0OTMtYmI0NmQ4YTFmMGZkOjAxMGQzOTYzLTZkMzItNDc0Ny04OWVmLTEwMWVkMTg4NmZiOQ=="
                }
            }
        })
        return request

    def send_traffic(self):
        request = self.post_to_scaphold()
        try:
            request.close()
            request = None
            return True
        except:
            return False

