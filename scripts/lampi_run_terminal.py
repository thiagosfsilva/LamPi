#!/usr/bin/env python3
import picamera, shutil, pickle, os, time as tm
from datetime import datetime, time
from gpiozero import CPUTemperature

# Function to test if current time is in range
def time_in_range(start, end):
    now = datetime.now().time()
    preMidnight = time(23, 59, 59)
    midnight = time(0, 0, 0)
    if (now >= start and now <= preMidnight) or (now >= midnight and now <= end):
        return True
    else:
        return False


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

# Start logfile
logName = f"/home/pi/LamPi/sync/logs/flopi{piNum}_log.txt"
strtTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logFile = open(logName, "a")
logFile.write(f"\n Script started on {strtTime}.")
logFile.close()
#
# Start recording loop
try:
    while piNum is not None:
        now = datetime.now()
        if time_in_range(strtm, endtm):
            sysTime = datetime.now()
            startTime = sysTime.strftime("%Y-%m-%d_%H_%M_%S")
            outName = f"/home/pi/LamPi/sync/videos/lampivid_{piNum}_{startTime}.h264"
            print(f"Recording {os.path.basename(outName)}")
            print("Click 'Stop'or press Ctrl+C to interrupt execution\n")
            camera.start_recording(outName, format="h264", bitrate=0, quality=25)
            camera.wait_recording(clipDuration)
            camera.stop_recording()
            cpuTemp = round(CPUTemperature().temperature, 1)
            diskUsage = shutil.disk_usage("/")
            diskFree = round(diskUsage.free / (1000000000), 2)
            logOut = f"Finished recording\n{outName}\nCPU temp: {cpuTemp}\nFree disk space: {diskFree}Gb"
            logFile = open(logName, "a")
            logFile.write(logOut)
            logFile.close()
            print(logOut)            
        else:
            sleepTime = (datetime.combine(datetime.now().date(), strtm) - datetime.now()).total_seconds()
            #print(sleepTime)
            logFile = open(logName, "a")
            logFile.write("Stopped recording at {datetime.now()}")
            logFile.close()
            print(
                f"Starting rclone cloud syncing - will get back to recording at {strtm}"
            )
            os.system("rclone copy /home/pi/LamPi/sync/ OneDrive:LamPi -v")
            tm.sleep(sleepTime)

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
