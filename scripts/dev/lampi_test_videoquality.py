import picamera
import os

### Set recording parameters here
outDir = "/home/pi/LamPi/sync/videos/"
os.chdir(outDir)

# set clip duration in seconds
camera = picamera.PiCamera()  # activate pi camera
camera.resolution = (1640, 1232)  # set video resolution
camera.framerate = 30  # set video framerate
br = 0
ql = 10
dur = 10
outName = (
    f"PiCam_{camera.resolution}_fr{camera.framerate}_br{br/1000000}M_ql{ql}_{dur}s.h264"
)
camera.start_recording(outName, format="h264", bitrate=br, quality=ql)
camera.wait_recording(dur)
camera.stop_recording()

size_mb = os.path.getsize(outName) / 1000000
size_mb_hour = size_mb * (60 / dur)
size_gb_day = size_mb_hour * 24 / 1000
sd_capacity = 32 / size_gb_day
print(outName)
print(
    f"At these settings, each 60s file will be {round(size_mb,2)} Mb\nIt will record {round(size_mb_hour, 2)}Mb in one hour\nIt will record {round(size_gb_day,2)}Gb per day.\nA 32Gb card will be able to hold {round(sd_capacity,2)} days of recording."
)
