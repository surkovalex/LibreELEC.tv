import datetime
import xbmcgui
import xbmcaddon
import threading
import time
import sys
import os
import subprocess

addon = xbmcaddon.Addon(id='script.service.m10vfd')

class clockThreadClass(threading.Thread):
    def run(self):
	self.shutdown = False
	while not self.shutdown:
	    if ( not os.path.isfile('/sys/class/net/wlan0/operstate')):
	        subprocess.call("sleep 5", shell=True)
	    spec = 0
	    tm = xbmc.getInfoLabel('System.Time(hh:mm)')
	    play = xbmc.getCondVisibility('Player.Playing')
	    pause = xbmc.getCondVisibility('Player.Paused')
	    lanstate = file('/sys/class/net/eth0/operstate', "rb")
	    lan = lanstate.read()
	    wifistate = file('/sys/class/net/wlan0/operstate', "rb")
	    wifi = wifistate.read()
	    spec = setBit(spec, 1) if (lan.find('up')>=0) else clearBit(spec, 1)
	    spec = setBit(spec, 4) if (wifi.find('up')>=0) else clearBit(spec, 4)
	    now = tm.replace(":", "")
	    spec = setBit(spec, 3)
	    spec = setBit(spec, 5)
	    spec = setBit(spec, 0) if pause else clearBit(spec, 0)
	    spec = setBit(spec, 2) if play else clearBit(spec, 2)
	    now += twoDigitHex(spec)
	    vfd = file('/sys/devices/platform/aml_vfd/led', "wb")
	    vfd.write(now)
	    vfd.flush()
	    time.sleep(0.5)
	    
def setBit(int_type, offset):
    mask = 1 << offset
    return(int_type | mask)

def clearBit(int_type, offset):
    mask = ~(1 << offset)
    return(int_type & mask)

def toggleBit(int_type, offset):
    mask = 1 << offset
    return(int_type ^ mask)

def testBit(int_type, offset):
    mask = 1 << offset
    return(int_type & mask)

def twoDigitHex( number ):
    return '%02x' % number

class ClockDialog: #(xbmc.Monitor):
    def __init__(self):
	self.clockThread = clockThreadClass()
	self.clockThread.start()

dialog = ClockDialog()
del dialog
del addon
