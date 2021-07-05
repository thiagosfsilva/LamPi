# from types import TracebackType
import PySimpleGUI as sg  # to create and run the UI
import pickle
from PySimpleGUI.PySimpleGUI import fill_form_with_values  # to save parameters
import shutil  # aslo for file paths
from datetime import datetime  # to get date and time
from gpiozero import CPUTemperature  # to log CPU temperature
import threading
import picamera

##### Define and import functions ######
import lampi_run_threaded as td


def save_params(params):
    pickle.dump(params, open("/home/pi/LamPi/params/params.p", "wb"))

###### UI APP ##########

## UI Elements ##

# Buttons #

# Select pi number
btn_pinum = sg.OptionMenu(
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], key="-PINUM-", default_value=1
)

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
    default_value=(640, 480),
)

# select video framerate
btn_fps = sg.OptionMenu(
    [10, 15, 30, 60], key="-FPS-", default_value=10
    )

# select clip duration
btn_clipdur = sg.OptionMenu(
    [1, 3, 10, 30, 60, 90, 120, 300, 600], key="-CLDUR-", default_value=10
)

# select recording start time
btn_strtime = sg.OptionMenu(
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], key="-STRT-"
    )

# select daytime timelapse interval
btn_timelapse = sg.OptionMenu(
    [1, 2, 5, 10], key="-TLPS-"
    )

# select recording end time
btn_endtime = sg.OptionMenu(
    [1, 3, 10, 30, 60, 90, 120, 300, 600], key="-ENDT-"
    )

# save parameters
btn_save = sg.Button(
    "Save parameters", enable_events=True, key="-SAVE-"
    )

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
out_box = sg.Multiline(
    "Press start...", size=(27, 12), key="-TEXTBOX-"
    )

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
    if event == "-RECMSG-":
        window["-TEXTBOX-"].print(values["-RECMSG-"])
    # Start buttons sets the camera and toggles the recording state
    elif event == "-START-":
        exit_event = threading.Event()
        t1 = threading.Thread(target=td.do_rec, args=(values,window,exit_event), daemon=True)
        t1.start()
        window["-TEXTBOX-"].print("\nRecording Started...:\n")
        window.FindElement("-START-").Update(disabled=True)
        window.FindElement("-STOP-").Update(disabled=False)

    # Stopping rules
    elif event == "-STOP-":
        window["-TEXTBOX-"].print("Stopping...")
        window.FindElement("-START-").Update(disabled=False)
        window.FindElement("-STOP-").Update(disabled=True)
        exit_event.set()
        t1.join()

    elif event == sg.WIN_CLOSED:  # ends program if user closes window
        exit_event.set()
        t1.join()
        break

window.close()

# try:
#     params = pickle.load(open("/home/pi/LamPi/params/params.p", "rb"))
# except:
#     values["-AUTOREC-"] = False

#         save_params(values)
#         window["-TEXTBOX-"].print("\nParameters saved:\n", values)
