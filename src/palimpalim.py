#!/bin/python
# -*- coding: utf-8 -*-

# simple daemon that digitalize speaker bells/ beeps (char 7)
# By Chrys, Storm Dragon, and contributers.
import evdev
from evdev import InputDevice
from select import select
#from . import driver

devices = map(evdev.InputDevice, (evdev.list_devices()))
devices = {dev.fd: dev for dev in devices}

for fd in devices:
    for i in devices[fd].capabilities(True):
        print(devices[fd].fn,devices[fd].name,i)

while True:
    r, w, x = select(devices, [], [])
    if r != []:
        for fd in r:
            for event in devices[fd].read():
                print('Devicename:'+ devices[fd].name + '  Devicepath:' + devices[fd].fn + ' | EVENTINFO Type: ' + str(event.type) + '  Code: ' + str(event.code) + '  Value: ' + str(event.value))


