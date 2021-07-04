#!/usr/bin/env python3

import picamera
import shutil
from datetime import datetime
from gpiozero import CPUTemperature


def set_log(piNum):
    logName = f"/home/pi/LamPi/sync/logs/{piNum}_log.txt"
    strtTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logFile = open(logName, "a")
    logFile.write(f"\n Script started on {strtTime}.")
    logFile.close()
    return logName


def do_rec(params, window):
    global camera, logName
    camera = picamera.PiCamera()
    camera.resolution = eval(params["-RES-"])  # set video resolution
    camera.framerate = int(params.get("-FPS-"))  # set video framerate
    clipDuration = int(params.get("-CLDUR-"))  # set clip duration in seconds
    piNum = params.get("-PNUM-")  # set raspberry pi identifier
    logName = set_log(piNum)
    while True:
        sysTime = datetime.now()
        startTime = sysTime.strftime("%Y-%m-%d_%H_%M_%S")
        outName = "/home/pi/LamPi/sync/videos/lampivid_%s_%s.h264" % (piNum, startTime)
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
        window.write_event_value("-RECMSG-", logOut)


def stop_rec(camera, logName):
    intMsg = "\nInterrupted by user at %s " % datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    print(intMsg)
    try:
        camera.stop_recording()
        logFile = open(logName, "a")
        logFile.write(intMsg)
        logFile.close()
    except:
        pass
