import datetime
import xbmcgui
import xbmcaddon
import threading
import time
import sys
import subprocess

addon = xbmcaddon.Addon(id='script.service.vfd')

class clockThreadClass(threading.Thread):
    def run(self):
	self.shutdown = False
	while not self.shutdown:
	    spec = 0
	    tm = xbmc.getInfoLabel('System.Time(hh:mm)')
	    usb_state = usb = ''
	    p = subprocess.Popen('blkid /dev/sd*', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	    for line in p.stdout.readlines():
		usb_state += line
	    retval = p.wait()
	    if len(usb_state) > 0: usb = 'c'
	    else: usb = 'C'
	    sd_state = sd = ''
	    p = subprocess.Popen('blkid /dev/mmcblk* | grep " UUID"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	    for line in p.stdout.readlines():
		sd_state += line
	    retval = p.wait()
	    if len(sd_state) > 0: sd = 'd'
	    else: sd = 'D'
	    hpd_state = file('/sys/class/amhdmitx/amhdmitx0/hpd_state', "rb")
	    hpdstate = hpd_state.read()
	    if (hpdstate == '1'): hpd = "eF"
	    else: hpd = "Ef"
	    vfdset = tm + hpd + usb + sd
	    vfdset = str(vfdset).rjust(9,'0')
	    vfd = file('/sys/devices/m1-vfd.26/led', "wb")
	    vfd.write(vfdset)
	    vfd.flush()
	    time.sleep(0.5)

class ClockDialog: #(xbmc.Monitor):
    def __init__(self):
	self.clockThread = clockThreadClass()
	self.clockThread.start()

dialog = ClockDialog()
del dialog
del addon
