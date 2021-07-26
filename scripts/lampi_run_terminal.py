#!/usr/bin/env python3
from gpiozero.internal_devices import LoadAverage
import picamera, pickle, os, time as tm
from datetime import datetime, time, timedelta
from gpiozero import CPUTemperature, DiskUsage, LoadAverage
from shutil import disk_usage

# Function to test if current time is in range
def time_in_range():
    global start
    global stop
    global recstatus
    now = datetime.now()
    if now < start:
        recstatus = "wait"
    elif now >= start and now <= stop:
        recstatus = "rec"
    else:
        start = start + timedelta(days=1)
        stop = stop + timedelta(days=1)
        recstatus = "sync"


# Function to everything
def pi_log(logName, outName):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cpuTemp = round(CPUTemperature().temperature, 1)
    diskUsageGb = disk_usage("/")
    diskFree = round(diskUsageGb.free / (1000000000), 2)
    diskUsagePercent = DiskUsage().usage
    loadCPU = LoadAverage(
        min_load_average=0, max_load_average=1, minutes=1
    ).load_average
    outName = os.path.basename(outName)
    logMessage = f"{now}\t{outName}\t{loadCPU}\t{cpuTemp}\t{round(diskUsagePercent,2)}\t{diskFree}\n"
    logFile = open(logName, "a")
    logFile.write(logMessage)
    logFile.close()
    print(f"CPU:{loadCPU}%,{cpuTemp}°C; {diskFree} Gb left")


### Retrieve saved parameters
params = pickle.load(open("/home/pi/LamPi/params/params.p", "rb"))

### Set recording parameters here
camera = picamera.PiCamera()
camera.resolution = params["-RES-"]  # set video resolution
camera.framerate = int(params.get("-FPS-"))  # set video framerate
clipDuration = int(params.get("-CLDUR-"))  # set clip duration in seconds
piNum = params.get("-PINUM-")  # set raspberry pi identifie
start = datetime.combine(datetime.now(), time(params["-STRTHR-"], params["-STRTMIN-"]))
end = timedelta(hours=params["-RECLEN-"])
stop = start + end
recstatus = "wait"

# Start recording logfile
# logName = f"/home/pi/LamPi/sync/logs/flopi{piNum}_rec_log.txt"
# strtTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# logFile = open(logName, "a")
# logFile.write(f"\n Script started on {strtTime}.")
# logFile.close()

# Start pi logfile
logName = f"/home/pi/LamPi/sync/logs/flopi{piNum}_log.txt"
logFile = open(logName, "a")
logHeader = "Time\tFile_name\tCPU_load\tCPU_temp\tPercent_disk_used\tFree_disk_Gb\n"
logFile.write(logHeader)
logFile.close()

# Start recording loop
try:
    while piNum is not None:
        time_in_range()
        if recstatus == "rec":
            sysTime = datetime.now()
            startTime = sysTime.strftime("%Y-%m-%d_%H_%M_%S")
            outName = f"/home/pi/LamPi/sync/videos/lampivid_{piNum}_{startTime}.h264"
            # motionName = f"/home/pi/LamPi/sync/videos/lampivid_{piNum}_{startTime}.mot"
            print(f"{sysTime} is after {start} and before {stop}, so I'm recording")
            # print(f"Recording {os.path.basename(outName)}")
            # print("Click 'Stop'or press Ctrl+C to interrupt execution\n")
            camera.start_recording(
                outName,
                format="h264",
                bitrate=2000000,
                quality=0,  # motion_output=motionName
            )
            camera.wait_recording(clipDuration)
            camera.stop_recording()
            pi_log(logName, outName)

        elif recstatus == "sync":
            sysTime = datetime.now()
            print(
                f"{sysTime} is after {start} and {stop}, so I'm syncing and then waiting until {start}"
            )
            os.system(
                "rclone copy /home/pi/LamPi/sync/ OneDrive:LamPi/test_flopi1 -v --checkers 1 --multi-thread-streams 1 --transfers 1"
            )
            pi_log(logName, "Started Sync")

            # print(f"Syncing finished.\nGoing to sleep now, will start recording again at {start}")
            # print("Zzzzzzzzzz"...")
        elif recstatus == "wait":
            sysTime = datetime.now()
            print(f"{sysTime} is before {start}, so I'm waiting")
            pi_log(logName, "Waiting")
            tm.sleep(60)
        else:
            print("something went wrong")
            break

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
