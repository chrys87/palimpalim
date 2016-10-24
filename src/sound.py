#!/bin/python
# -*- coding: utf-8 -*-

# simple beep digitalizing daemon
# By Chrys, Storm Dragon, and contributers.

from core import debug
import subprocess

class driver():
    def __init__(self):
        self.proc = None
        self.volume = 1.0
        self.soundType = ''
        self.soundFileCommand = ''
        self.frequenceCommand = ''
    def initialize(self, environment):
        self.env = environment
        #self.soundFileCommand = self.env['runtime']['settingsManager'].getSetting('sound', 'genericPlayFileCommand')
        #self.frequenceCommand = self.env['runtime']['settingsManager'].getSetting('sound', 'genericFrequencyCommand')
        if self.soundFileCommand == '':
            self.soundFileCommand = 'play -q -v palimpalimVolume palimpalimSoundFile'
        if self.frequenceCommand == '':
            self.frequenceCommand = 'play -q -v palimpalimVolume -n -c1 synth palimpalimDuration sine palimpalimFrequence'
    def shutdown(self):
        self.cancel()
    def playFrequence(self, frequence = 1000, duration = 0.3, adjustVolume = 0):
        if interrupt:
            self.cancel()
        popenFrequenceCommand = self.frequenceCommand.replace('palimpalimVolume', str(self.volume + adjustVolume ))
        popenFrequenceCommand = popenFrequenceCommand.replace('palimpalimFreqDuration', str(duration))
        popenFrequenceCommand = popenFrequenceCommand.replace('palimpalimFrequence', str(frequence))        
        self.proc = subprocess.Popen(popenFrequenceCommand, shell=True)
        self.soundType = 'frequence'
    def playSoundFile(self, filePath, interrupt = True):
        if interrupt:
            self.cancel()
        popenSoundFileCommand = self.soundFileCommand.replace('palimpalimVolume', str(self.volume ))
        popenSoundFileCommand = popenSoundFileCommand.replace('palimpalimSoundFile', filePath)
        self.proc = subprocess.Popen(popenSoundFileCommand, shell=True)
        self.soundType = 'file'
    def cancel(self):
        if self.soundType == '':
            return
        if self.soundType == 'file':
            self.proc.kill()
        if self.soundType == 'frequence':
            self.proc.kill()            
        self.soundType = ''
    def setCallback(self, callback):
        pass
    def setVolume(self, volume):
        self.volume = volume        
