#!/usr/bin/env python3

import picamera
import os
import shutil
from datetime import datetime
from gpiozero import CPUTemperature
import pickle

### Retrieve recording parameters

params = pickle.load("/home/pi/LamPi/params/params.p")


def start_rec(params):
    camera = picamera.PiCamera()  # activate pi camera
    camera.resolution = params.get("-RES-")  # set video resolution
    camera.framerate = params.get("-FPS-")  # set video framerate
    clipDuration = params.get("-CLDUR-")  # set clip duration in seconds
    piNum = params.get("-PNUM-")  # set raspberry pi identifier
    outDir = params.get("-FOLDER-")

    ### Start of capture routine

    #    Set working directory
    os.chdir(outDir)

    # Start logfile
    logName = "/home/pi/LamPi/sync/logs/PI%s_log.txt" % piNum
    logFile = open(logName, "a")
    logFile.write(
        "\n Script started on %s " % datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    logFile.close()

    # Start recording loop
    try:
        while whichPi is not None:
            sysTime = datetime.now()
            startTime = sysTime.strftime("%Y-%m-%d_%H_%M_%S")
            outName = "lampivid_%s_%s.h264" % (whichPi, startTime)
            camera.start_recording(outName)
            camera.wait_recording(clipDuration)
            camera.stop_recording()
            cpuTemp = round(CPUTemperature().temperature, 1)
            diskUsage = shutil.disk_usage("/")
            diskFree = round(diskUsage.free / (1000000000), 2)
            logOut = "\n\tCPU temp: %s , free disk space: %s Gb, last file: %s" % (
                cpuTemp,
                diskFree,
                outName,
            )
            logFile = open(logName, "a")
            logFile.write(logOut)
            logFile.close()
    except KeyboardInterrupt:
        camera.stop_recording()
        intMsg = "\nInterrupted by user at %s " % datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        logFile = open(logName, "a")
        logFile.write(intMsg)
        logFile.close()
        # print(intMsg)
        # print("\nYou may now close this window")
        pass
