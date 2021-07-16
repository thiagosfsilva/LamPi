#!/usr/bin/env python3
import picamera, shutil, pickle
from time import sleep
from datetime import datetime, time, timedelta
from gpiozero import CPUTemperature

# Function to test if current time is in range
def time_in_range(start, end, x):
    today = datetime.now().date()
    if start < end:
        strt = datetime.combine(today, start)
        endt = datetime.combine(today, end)
    elif end < start:
        strt = datetime.combine(today, start)
        endt = datetime.combine(today + timedelta(days=1), end)
    result = x >= strt and x <= endt
    return result


### Retrieve saved parameters
params = pickle.load(open("/home/pi/LamPi/params/params.p", "rb"))

### Set recording parameters here
camera = picamera.PiCamera()
camera.resolution = eval(params["-RES-"])  # set video resolution
camera.framerate = int(params.get("-FPS-"))  # set video framerate
clipDuration = int(params.get("-CLDUR-"))  # set clip duration in seconds
piNum = params.get("-PINUM-")  # set raspberry pi identifie
strtm = datetime.strptime(params["-STRT-"], "%H:%M:%S").time()
endtm = datetime.strptime(params["-ENDT-"], "%H:%M:%S").time()
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
        now = datetime.now()
        if time_in_range(strtm, endtm, now):
            sysTime = datetime.now()
            startTime = sysTime.strftime("%Y-%m-%d_%H_%M_%S")
            outName = f"/home/pi/LamPi/sync/videos/lampivid_{piNum}_{startTime}.h264"
            print("Recording videos")
            camera.start_recording(outName, format="h264", bitrate=0, quality=25)
            camera.wait_recording(clipDuration)
            camera.stop_recording()
            cpuTemp = round(CPUTemperature().temperature, 1)
            diskUsage = shutil.disk_usage("/")
            diskFree = round(diskUsage.free / (1000000000), 2)
            logOut = f"\nCPU temp: {cpuTemp}\n Free disk space: {diskFree} Gb\n Last file saved:\n {outName}"
            logFile = open(logName, "a")
            logFile.write(logOut)
            logFile.close()
            print(logOut)
            print("Click 'Stop'or press Ctrl+C to interrupt execution\n")
        else:
            # print(tlps)
            sysTime = datetime.now()
            startTime = sysTime.strftime("%Y-%m-%d_%H_%M_%S")
            outName = f"/home/pi/LamPi/sync/timelapse/lampimage_{piNum}_{startTime}.jpg"
            print("Recording timelapses")
            camera.capture(outName)
            cpuTemp = round(CPUTemperature().temperature, 1)
            diskUsage = shutil.disk_usage("/")
            diskFree = round(diskUsage.free / (1000000000), 2)
            logOut = f"\nCPU temp: {cpuTemp}\n Free disk space: {diskFree} Gb\n Last file saved:\n {outName}"
            logFile = open(logName, "a")
            logFile.write(logOut)
            logFile.close()
            print(logOut)
            print("Click 'Stop'or press Ctrl+C to interrupt execution\n")
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
