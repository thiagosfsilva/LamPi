#!/usr/bin/env python3

import picamera
import shutil
from datetime import datetime
from gpiozero import CPUTemperature


def do_rec(params, window, exit_event):
    # global stop_threads
    camera = picamera.PiCamera()
    camera.resolution = eval(params["-RES-"])  # set video resolution
    camera.framerate = int(params.get("-FPS-"))  # set video framerate
    clipDuration = int(params.get("-CLDUR-"))  # set clip duration in seconds
    piNum = params.get("-PINUM-")  # set raspberry pi identifier
    logName = f"/home/pi/LamPi/sync/logs/flopi{piNum}_log.txt"
    strtTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logFile = open(logName, "a")
    logFile.write(f"\n Script started on {strtTime}.")
    logFile.close()
    while True:
        sysTime = datetime.now()
        startTime = sysTime.strftime("%Y-%m-%d_%H_%M_%S")
        outName = f"/home/pi/LamPi/sync/videos/lampivid_{piNum}_{startTime}.h264"
        camera.start_recording(outName)
        camera.wait_recording(clipDuration)
        camera.stop_recording()
        cpuTemp = round(CPUTemperature().temperature, 1)
        diskUsage = shutil.disk_usage("/")
        diskFree = round(diskUsage.free / (1000000000), 2)
        logOut = f"\n\tCPU temp: {cpuTemp} , \n\tfree disk space: {diskFree} Gb, \n\tlast file: {outName}"
        logFile = open(logName, "a")
        logFile.write(logOut)
        logFile.close()
        window.write_event_value("-RECMSG-", outName)

        if exit_event.is_set():
            getTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            intMsg = f"\nInterrupted by user at {getTime}"
            camera.stop_recording()
            logFile = open(logName, "a")
            logFile.write(intMsg)
            logFile.close()
            window.write_event_value("-RECMSG-", "Recording stopped successfully.")
            break
