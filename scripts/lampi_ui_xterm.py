# from types import TracebackType
import PySimpleGUI as sg  # to create and run the UI
import pickle
from PySimpleGUI.PySimpleGUI import fill_form_with_values  # to save parameters
from datetime import datetime, time, timedelta  # to get date and time
import subprocess

##### Definefunctions ######
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
btn_fps = sg.OptionMenu([10, 15, 30, 60], key="-FPS-", default_value=10)

# select clip duration
btn_clipdur = sg.OptionMenu(
    [1, 3, 10, 30, 60, 90, 120, 300, 600], key="-CLDUR-", default_value=10
)

t1 = datetime(1900, 1, 1, 0, 0)
timedate_list = [(t1 + timedelta(minutes=m)).isoformat() for m in range(0, 1440, 60)]
time_list = [
    (datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")).time() for dt in timedate_list
]

# select recording start time
btn_strtime = sg.OptionMenu(time_list, key="-STRT-")

# select recording end time
btn_endtime = sg.OptionMenu(time_list, key="-ENDT-")

# select daytime timelapse interval
btn_timelapse = sg.OptionMenu([1, 2, 5, 10], key="-TLPS-")

# save parameters
btn_save = sg.Button("Save parameters", enable_events=True, key="-SAVE-")

# start recording
btn_start = sg.Button(
    "Start", size=(25, 1), enable_events=True, key="-START-", disabled=True
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
    [sg.Text("Rec Start"), btn_strtime],
    [sg.Text("Rec Stop"), btn_endtime],
    # [chbx_autostart],
    [btn_save, btn_start]
    # [sg.Text("Select folder to save videos:  "), sg.FolderBrowse(key="-FOLDER-")],
]

#  Set right (run app) layout
# run_column = [[btn_start], [btn_stop], [out_box]]

# Set 2-column window layout
layout = [
    [
        sg.Column(setup_column)  # ,  # left column
        # sg.VSeparator(),  # vertical separator (line)
        # sg.Column(run_column),
    ]  # right column
]

### App execution ###

# Create the Window
window = sg.Window("LamPi UI", layout, size=(240, 320), font=("Piboto Condensed", 10))

# Event Loop to process events (get values and run functions)
while True:
    event, values = window.read()
    # Stopping rules
    if event == sg.WIN_CLOSED:  # ends program if user closes window
        break
    elif event == "-SAVE-":
        pickle.dump(values, open("/home/pi/LamPi/params/params.p", "wb"))
        window.FindElement("-START-").Update(disabled=False)
    # Start buttons sets the camera and toggles the recording state
    elif event == "-START-":
        subprocess.run(
            "xterm -geometry 40x24+241+1 -hold -e python3 /home/pi/LamPi/scripts/lampi_run_terminal.py",
            shell=True,
        )

window.close()
