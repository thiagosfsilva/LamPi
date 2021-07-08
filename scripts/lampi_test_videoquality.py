#!/usr/bin/env python3

import picamera
import os
import shutil
from datetime import datetime
from gpiozero import CPUTemperature

### Set recording parameters here
outDir = '/home/pi/LamPi/sync/videos/'
os.chdir(outDir)

clipDuration = 60 # set clip duration in seconds
camera = picamera.PiCamera() # activate pi camera

# Test 1 - 320 x 
resolutions = res = [(1080, 720)] # set video resolution
framerates = fr = [30] # set video framerate
bitrates = br [1000000]
qualities = ql [5]


# for res in resolutions:
#     for fr in framerates:
#         for br in bitrates:
#             for ql in qualities:
camera.resolution = res # set video resolution
camera.framerate = fr # set video framerate 
outName = f"PiCam_{res[0]}x{res[1]}_fr{fr}_br{br}_ql{ql}.h264"
camera.start_recording(outName, format='h264', bitrate =br, quality=ql)
camera.wait_recording(clipDuration)
camera.stop_recording()
        
