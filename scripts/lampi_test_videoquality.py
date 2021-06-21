#!/usr/bin/env python3

import picamera
import os
import shutil
from datetime import datetime
from gpiozero import CPUTemperature

### Set recording parameters here
outDir = '/home/pi/LamPi/videos/'
os.chdir(outDir)

clipDuration = 10 # set clip duration in seconds
camera = picamera.PiCamera() # activate pi camera

# Test 1 - 320 x 
resolutions = [(320, 240),(640, 480),(1080, 720)] # set video resolution
framerates = [15, 30, 60] # set video framerate
bitrates = [1000000,5000000,10000000]
qualities = [5,10,20]


for res in resolutions:
    for fr in framerates:
        for br in bitrates:
            for ql in qualities:
                camera.resolution = res # set video resolution
                camera.framerate = fr # set video framerate 
                outName = "PiCam_%sx_%s_fr%s_br%s_ql%s.h264", % (res[0],  res[1], fr, br, ql)
                camera.start_recording(outName, format='h264', bitrate =br, quality=ql)
                camera.wait_recording(clipDuration)
                camera.stop_recording()
        