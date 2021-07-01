# from types import TracebackType
import PySimpleGUI as sg  # to create and run the UI
import os.path  # to handle file paths
import pickle  # to save parameters


##### Define / Import functions ######


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
# btn_ok = sg.Button("OK", enable_events=True, key="-OK-")

# start recording
btn_start = sg.Button("Start", size=(25, 1), enable_events=True, key="-START-")

# stop recording
btn_stop = sg.Button("Stop", size=(25, 1), enable_events=True, key="-STOP-")

# Checkboxes #

chbx_autostart = sg.Checkbox(
    "Enable recording autostart on boot", default=False, key="-AUTOREC-"
)

# Multiline text box #

out_box = sg.Multiline(
    """1) Select settings
    2) Save settings
    3) Click 'Start' """,
    size=(27, 12),
    key="-TEXTBOX-",
)


## UI Layout and appearabnce ##

sg.theme("DarkTanBlue")  # Set colour theme

# Set left (parameter input ) column layout
setup_column = [
    [sg.Text("Pi Number"), btn_pinum],
    [sg.Text("Video Resolution"), btn_res],
    [sg.Text("Video frame rate"), btn_fps],
    [sg.Text("Clip Duration (s)"), btn_clipdur],
    [sg.Text("Daytime timelapse interval (s)"), btn_timelapse],
    [sg.Text("Rec Start/End"), btn_strtime, btn_endtime],
    [chbx_autostart],
    [sg.Text("Select folder to save videos:  "), sg.FolderBrowse(key="-FOLDER-")],
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
    if event == "-START-":
        save_params(values)
        start_log("-FOLDER-")
        start_rec(values)
        window["-TEXTBOX-"].print("\nParameters saved:\n", values)
    if event == sg.WIN_CLOSED:  # ends program if user closes window
        break

window.close()
