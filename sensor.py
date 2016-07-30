from machine import Pin
from time import sleep

pin = Pin('GP10', mode=Pin.IN, pull=None, drive=Pin.MED_POWER)

while True:
    if pin() == 1:
        print("ON")
    else:
        print("...")
    sleep(1)



