#!/bin/python
# -*- coding: utf-8 -*-

# simple daemon that digitalize speaker bells/ beeps (char 7)
# By Chrys, Storm Dragon, and contributers.
import evdev
from evdev import InputDevice
from select import select
from configparser import ConfigParser
#from . import driver

class palimpalim():
    __init__():
        self._config = None
        self.devices = None
        self.announceLed = False
        self.announeBell = True
        self.loadSettings()
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
    
    def proceed(self):
        while True:
            r, w, x = select(self.devices, [], [])
            if r != []:
                for fd in r:
                    for event in self.devices[fd].read():
                        print('Devicename:'+ self.devices[fd].name + '  Devicepath:' + self.devices[fd].fn + ' | EVENTINFO Type: ' + str(event.type) + '  Code: ' + str(event.code) + '  Value: ' + str(event.value))


