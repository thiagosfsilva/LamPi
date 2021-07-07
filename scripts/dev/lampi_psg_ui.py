# from types import TracebackType
import PySimpleGUI as sg  # to create and run the UI
import pickle
from PySimpleGUI.PySimpleGUI import fill_form_with_values  # to save parameters
import picamera  # to control the RPi camera
import shutil  # aslo for file paths
from datetime import datetime  # to get date and time
from gpiozero import CPUTemperature  # to log CPU temperature

##### Define  functions ######


def save_params(params):
    pickle.dump(params, open("/home/pi/LamPi/params/params.p", "wb"))


###### UI APP ##########

## UI Elements ##

# Buttons #

# Select pi number
btn_pinum = sg.OptionMenu([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], key="-PINUM-")

# Select video resolution
btn_res = sg.OptionMenu(
    [
        (640, 480),
        (800, 600),
        (960, 720),
        (1024, 768),
        (1280, 960),
        (1400, 1050),
        (1440, 1080),
    ],
    key="-RES-",
)

# select video framerate
btn_fps = sg.OptionMenu([10, 15, 30, 60], key="-FPS-")

# select clip duration
btn_clipdur = sg.OptionMenu([1, 3, 10, 30, 60, 90, 120, 300, 600], key="-CLDUR-")

# select recording start time
btn_strtime = sg.OptionMenu([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], key="-STRT-")

# select daytime timelapse interval
btn_timelapse = sg.OptionMenu([1, 2, 5, 10], key="-TLPS-")

# select recording end time
btn_endtime = sg.OptionMenu([1, 3, 10, 30, 60, 90, 120, 300, 600], key="-ENDT-")

# save parameters
btn_save = sg.Button("Save parameters", enable_events=True, key="-SAVE-")

# start recording
btn_start = sg.Button(
    "Start", size=(25, 1), enable_events=True, key="-START-", disabled=False
)

# stop recording
btn_stop = sg.Button(
    "Stop", size=(25, 1), enable_events=True, key="-STOP-", disabled=True
)

# Checkboxes #
chbx_autostart = sg.Checkbox(
    "Enable recording autostart on boot", default=False, key="-AUTOREC-"
)

# Multiline text box #
out_box = sg.Multiline("Press start...", size=(27, 12), key="-TEXTBOX-")

## UI Layout and appearance ##

# Set color theme
sg.theme("DarkTanBlue")  # Set colour theme

# Set left (parameter input) column layout
setup_column = [
    [sg.Text("Pi Number"), btn_pinum],
    [sg.Text("Video Resolution"), btn_res],
    [sg.Text("Video frame rate"), btn_fps],
    [sg.Text("Clip Duration (s)"), btn_clipdur],
    [sg.Text("Daytime timelapse interval (s)"), btn_timelapse],
    [sg.Text("Rec Start/End"), btn_strtime, btn_endtime],
    [chbx_autostart],
    [btn_save]
    # [sg.Text("Select folder to save videos:  "), sg.FolderBrowse(key="-FOLDER-")],
]

#  Set right (run app) layout
run_column = [[btn_start], [btn_stop], [out_box]]

# Set 2-column window layout
layout = [
    [
        sg.Column(setup_column),  # left column
        sg.VSeparator(),  # vertical separator (line)
        sg.Column(run_column),
    ]  # right column
]

### App execution ###

# Create the Window
window = sg.Window("LamPi UI", layout, size=(480, 320), font=("Piboto Condensed", 10))




# Event Loop to process events (get values and run functions)
while True:
    event, values = window.read()

    # Start buttons sets the camera and toggles the recording state
    if event == "-START-":
        ### Initialise with selected parameters
        params = values
        camera = picamera.PiCamera()
        ## START THREADED  

    # Restart loop if recording has not been started
    if rec_state == False:
        continue

    # Stopping rules
    if event == "-STOP-" or event == sg.WIN_CLOSED:
        if rec_state == True:
            camera.stop_recording()
            logFile = open(logName, "a")
            logFile.write(intMsg)
            logFile.close()
            intMsg = "\nInterrupted by user at %s " % datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            window["-TEXTBOX-"].print(intMsg)
            rec_state = False
            window.FindElement("-START-").Update(disabled=False)
            window.FindElement("-STOP-").Update(disabled=True)
        if event == sg.WIN_CLOSED:  # ends program if user closes window
            break
        else:
            continue

    sysTime = datetime.now()
    startTime = sysTime.strftime("%Y-%m-%d_%H_%M_%S")
    outName = "/home/pi/LamPi/sync/videos/lampivid_%s_%s.h264" % (
        params.get("-PNUM-"),
        startTime,
    )
    camera.start_recording(outName)
    camera.wait_recording(int(params.get("-CLDUR-")))
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
    window["-TEXTBOX-"].print(logOut)

window.close()

# try:
#     params = pickle.load(open("/home/pi/LamPi/params/params.p", "rb"))
# except:
#     values["-AUTOREC-"] = False

#         save_params(values)
#         window["-TEXTBOX-"].print("\nParameters saved:\n", values)
