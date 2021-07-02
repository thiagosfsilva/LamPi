#!/usr/bin/env python3

import picamera
import os
import shutil
from datetime import datetime
from gpiozero import CPUTemperature

### Set recording parameters here
whichPi = "Pi_1" # set raspberry pi identifier
outDir = '/home/pi/LamPi/videos'

camera = picamera.PiCamera() # activate pi camera
camera.resolution = (1024, 768) # set video resolution
camera.framerate = 30 # set video framerate 
clipDuration = 5 # set clip duration in seconds

### Start of capture routine

# Set working directory
os.chdir(outDir)

# Test camera output
#camera.start_preview()

# Start logfile
logName = whichPi + 'log.txt'
logFile = open(logName, 'a')
logFile.write('\n Script started on %s ' % datetime.now().strftime("%Y-%m-%d %H:%M:%S") )
logFile.close()
print (r"""
                                  ____________
                                 /       (O)  \
                                / oooooo       \
                  ________     /    _________  /   
          _      /        \   /    /         \/
         / \    /  ____    \_/    /
        //\ \  /  /    \         /
        V  \ \/  /      \       /
            \___/        \_____/
                 _                                      
                | |                                     
                | | __ _ _ __ ___  _ __  _   _ 
                | |/ _` | '_ ` _ \| '_ \| | | |
                | | (_| | | | | | | |_) | |_| |
                |_|\__,_|_| |_| |_| .__/ \__. /
                                  | |    __/ /
                                  |_|   |___/
===============================================================                 
                  """)
print ('Running LamPi script - saving on %s' % outDir)
print('Press Ctrl+C to interrupt execution')
print('\n===============================================================')

# Start recording loop
try:
    while whichPi is not None:
        sysTime = datetime.now()
        startTime = sysTime.strftime("%Y-%m-%d_%H_%M_%S")
        outName = "lampivid_%s_%s.h264" % (whichPi, startTime)
        camera.start_recording(outName)
        camera.wait_recording(clipDuration)
        camera.stop_recording()
        cpuTemp = round(CPUTemperature().temperature,1)
        diskUsage = shutil.disk_usage('/')
        diskFree = round(diskUsage.free / (1000000000),2)
        logOut = "\n\tCPU temp: %s , free disk space: %s Gb, last file: %s" % (cpuTemp, diskFree, outName)
        logFile = open(logName, 'a')
        logFile.write(logOut)
        logFile.close()
except KeyboardInterrupt:
    camera.stop_recording()
    intMsg = "\nInterrupted by user at %s " % datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logFile = open(logName, 'a')
    logFile.write(intMsg)
    logFile.close()
    print(intMsg)
    print("\nYou may now close this window")
    pass  
