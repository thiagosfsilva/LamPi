#!/usr/bin/env python3
import picamera, shutil, pickle
from time import sleep
from datetime import datetime
from gpiozero import CPUTemperature

### Retrieve saved parameters
params = pickle.load(open("/home/pi/LamPi/params/params.p", "rb"))

### Set recording parameters here
camera = picamera.PiCamera()
camera.resolution = eval(params["-RES-"])  # set video resolution
camera.framerate = int(params.get("-FPS-"))  # set video framerate
clipDuration = int(params.get("-CLDUR-"))  # set clip duration in seconds
piNum = params.get("-PINUM-")  # set raspberry pi identifie
strtm = params["-STRT-"]
endtm = params.get("-ENDT-")
strtm = datetime.strptime(strtm, "%H:%M:%S").time()
endtm = datetime.strptime(endtm, "%H:%M:%S").time()
tlps = int(params.get("-TLPS-"))

# Start logfile
logName = f"/home/pi/LamPi/sync/logs/flopi{piNum}_log.txt"
strtTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logFile = open(logName, "a")
logFile.write(f"\n Script started on {strtTime}.")
logFile.close()
# print(
#  r"""
#                                 ____________
#                                /       (O)  \
#                               / oooooo       \
#                 ________     /    _________  /
#         _      /        \   /    /         \/
#        / \    /  ____    \_/    /
#       //\ \  /  /    \         /
#       V  \ \/  /      \       /
#           \___/        \_____/
#                _
#               | |
#               | | __ _ _ __ ___  _ __  _   _
#               | |/ _` | '_ ` _ \| '_ \| | | |
#               | | (_| | | | | | | |_) | |_| |
#               |_|\__,_|_| |_| |_| .__/ \__. /
#                                 | |    __/ /
#                                 |_|   |___/
# ===============================================================
#                 """
# )
print("Running LamPi script \nSaving on /home/pi/LamPi/sync/videos/")
# print("\n===============================================================")

# Start recording loop
try:
    while piNum is not None:
        now = datetime.now().time()
        if now >= strtm and now <= endtm:
            sysTime = datetime.now()
            startTime = sysTime.strftime("%Y-%m-%d_%H_%M_%S")
            outName = f"/home/pi/LamPi/sync/videos/lampivid_{piNum}_{startTime}.h264"
            print("Starting recording of \n" + outName)
            camera.start_recording(outName, format="h264", bitrate=0, quality=20)
            camera.wait_recording(clipDuration)
            camera.stop_recording()
            cpuTemp = round(CPUTemperature().temperature, 1)
            diskUsage = shutil.disk_usage("/")
            diskFree = round(diskUsage.free / (1000000000), 2)
            logOut = "\nCPU temp: %s, free disk space: %s Gb, last file: %s" % (
                cpuTemp,
                diskFree,
                outName,
            )
            logFile = open(logName, "a")
            logFile.write(logOut)
            logFile.close()
            print("Recording finished.  " + " ".join(logOut.split(", ")[:-1]))
            print("Press Ctrl+C to interrupt execution\n")
        else:
            # print(tlps)
            sysTime = datetime.now()
            startTime = sysTime.strftime("%Y-%m-%d_%H_%M_%S")
            outName = f"/home/pi/LamPi/sync/timelapse/lampimage_{piNum}_{startTime}.jpg"
            camera.capture(outName)
            cpuTemp = round(CPUTemperature().temperature, 1)
            diskUsage = shutil.disk_usage("/")
            diskFree = round(diskUsage.free / (1000000000), 2)
            logOut = "\nCPU temp: %s, free disk space: %s Gb, last file: %s" % (
                cpuTemp,
                diskFree,
                outName,
            )
            logFile = open(logName, "a")
            logFile.write(logOut)
            logFile.close()
            print(logOut)
            print("Press Ctrl+C to interrupt execution\n")
            sleep(tlps)
except KeyboardInterrupt:
    try:
        camera.stop_recording()
    except:
        pass
    intMsg = "\nInterrupted by user at %s " % datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    logFile = open(logName, "a")
    logFile.write(intMsg)
    logFile.close()
    print(intMsg)
    print("\nYou may now close this window")
    pass
