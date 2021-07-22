#!/usr/bin/env python3
from gpiozero.internal_devices import LoadAverage
import picamera, pickle, os, time as tm
from datetime import datetime, time
from gpiozero import CPUTemperature, DiskUsage, LoadAverage
from shutil import disk_usage

# Function to test if current time is in range
def time_in_range(start, end):
    now = datetime.now().time()
    preMidnight = time(23, 59, 59)
    midnight = time(0, 0, 0)
    if (start <= preMidnight) and (end <= preMidnight):
        if (now >= start and now <= end):
            return True
    elif 
        return False


# Function to everything
def pi_log(logName, outName):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cpuTemp = round(CPUTemperature().temperature, 1)
    diskUsageGb = disk_usage("/")
    diskFree = round(diskUsageGb.free / (1000000000), 2)
    diskUsagePercent = DiskUsage()
    loadCPU = LoadAverage(min_load_average=0, max_load_average=1, minutes=1)
    outName = os.path.basename(outName)
    logMessage = f"{now}\tTest\t{loadCPU}\t{cpuTemp}\t{round(diskUsagePercent.usage,2)}\t{diskFree}\n"
    logFile = open(logName, "a")
    logFile.write(logMessage)
    logFile.close()
    print(logMessage)


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

# Start recording logfile
# logName = f"/home/pi/LamPi/sync/logs/flopi{piNum}_rec_log.txt"
# strtTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# logFile = open(logName, "a")
# logFile.write(f"\n Script started on {strtTime}.")
# logFile.close()

# Start pi logfile
logName = f"/home/pi/LamPi/sync/logs/flopi{piNum}_log.txt"
logFile = open(logName, "a")
logHeader = "Time\tFile_name\tCPU_load\tCPU_temp\tPercent_disk_used\tFree_disk_Gb"
logFile.write(logHeader)
logFile.close()

sync_flag = 0

# Start recording loop
try:
    while piNum is not None:
        now = datetime.now()
        if time_in_range(strtm, endtm):
            sysTime = datetime.now()
            startTime = sysTime.strftime("%Y-%m-%d_%H_%M_%S")
            outName = f"/home/pi/LamPi/sync/videos/lampivid_{piNum}_{startTime}.h264"
            motionName = f"/home/pi/LamPi/sync/videos/lampivid_{piNum}_{startTime}.mot"

            # print(f"Recording {os.path.basename(outName)}")
            # print("Click 'Stop'or press Ctrl+C to interrupt execution\n")
            camera.start_recording(
                outName, format="h264", bitrate=0, quality=25, motion_output=motionName
            )
            camera.wait_recording(clipDuration)
            camera.stop_recording()
            pi_log(logName, outName)
            sync_flag = 0

        else:
            if sync_flag == 0:
                os.system(
                    "rclone copy /home/pi/LamPi/sync/ OneDrive:LamPi/test_flopi1 -q"
                )
                pi_log(logName, "Rclone started")
                sync_flag = 1
            else:
                pi_log(logName, "Sleeping")
                tm.sleep(60)


except KeyboardInterrupt:
    try:
        camera.stop_recording()
    except:
        pass
    intMsg = "\nInterrupted by user at %s " % datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    # logFile = open(logName, "a")
    # logFile.write(intMsg)
    # logFile.close()
    print(intMsg)
    # print("\nYou may now close this window")
    pass
