# main.py -- put your code here!
from machine import Pin
from time import sleep
from scaphold import Connection

pin = Pin('GP10', mode=Pin.IN, pull=None, drive=Pin.MED_POWER)
connection = Connection()

while True:
    if pin() == 1:
        print("ON")
        connection.send_traffic()
    else:
        print("...")
    sleep(3)
