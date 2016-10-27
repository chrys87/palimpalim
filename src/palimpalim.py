#!/bin/python
# -*- coding: utf-8 -*-

# simple daemon that digitalize speaker bells/ beeps (char 7)
# By Chrys, Storm Dragon, and contributers.
import evdev
from evdev import InputDevice
from select import select
import time, os
from configparser import ConfigParser
#from . import driver

class palimpalim():
    def __init__(self):
        self._config = None
        self.devices = None
        self.debug = True
        self.announceLed = False
        self.announeBell = True
        self.loadDevices()
        self.loadSettings()
        if self.announceLed:
            self.currNumlock = self.getLedState()
            self.currShift = self.getLedState(1) 
            self.currScrolllock = self.getLedState(2)
    def loadSettings(self, settingConfigPath ='/etc/palim/settings.conf'):
        if not os.path.exists(settingConfigPath):
            return
        self._config = ConfigParser()
        self._config.read(settingConfigPath)
        try:
            self.announceLed = bool(self.getSetting(self, 'general', 'announceLed'))
        except:
            print('announceLed has to be True/False in configfile')
        try:
            self.announeBell = bool(self.getSetting(self, 'general', 'announeBell'))
        except:
            print('announeBell has to be True/False in configfile')
    
    def getSetting(self, section, setting):
        value = ''
        try:
            value = self._config.get(section, setting)
        except Exception as e:
            print(e)
        return value
    
    def loadDevices(self):
        self.devices = map(evdev.InputDevice, (evdev.list_devices()))
        self.devices = {dev.fd: dev for dev in self.devices}

        for fd in self.devices:
            for i in self.devices[fd].capabilities(True):
                print(self.devices[fd].fn,self.devices[fd].name,i)

    def getLedState(self, led = 0):
        # 0 = Numlock
        # 1 = Capslock
        # 2 = Rollen
        if self.devices == None:
            return False
        if self.devices == {}:
            return False                   
        for fd, dev in self.devices.items():
            return led in dev.leds()
        return False 
                
    def proceed(self):
        while True:
            r, w, x = select(self.devices, [], [])
            # wait until all events reach it destination and did what they shouldwitch LEDs and so on)
            time.sleep(0.15)
            if r != []:
                for fd in r:
                    for event in self.devices[fd].read():
                        if event.type == 11: #EV_LED
                            if self.announceLed:
                                if self.currNumlock != self.getLedState():
                                    if self.debug:
                                        print('numlock',self.getLedState())
                                    self.currNumlock = self.getLedState()
                                if self.currShift != self.getLedState(1):
                                    if self.debug:
                                        print('shift',self.getLedState(1))
                                    self.currShift = self.getLedState(1) 
                                if self.currScrolllock != self.getLedState(2):
                                    if self.debug:
                                        print('scrolllock',self.getLedState(2))
                                    self.currScrolllock = self.getLedState(2)
                        if self.announeBell:
                            if event.type == 12: #EV_SND
                                if self.debug:
                                    print('bell')
                        if self.debug:
                            if event.type == 12 or event.type == 17:
                                print('Devicename:'+ self.devices[fd].name + '  Devicepath:' + self.devices[fd].fn + ' | EVENTINFO Type: ' + str(event.type) + '  Code: ' + str(event.code) + '  Value: ' + str(event.value))


