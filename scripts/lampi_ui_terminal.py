import PySimpleGUI as sg  # to create and run the UI
from datetime import datetime, time  # to get date and time
import subprocess, signal, pickle

##### Definefunctions ######
def save_params(params):
    pickle.dump(params, open("/home/pi/LamPi/params/params.p", "wb"))


###### UI APP ##########

## UI Elements ##

# Buttons #

# Select pi number
btn_pinum = sg.Combo(
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    pad=((0, 0), (4, 3)),
    key="-PINUM-",
    size=(8, None),
    default_value=1,
)

# Select video resolution
btn_res = sg.Combo(
    ["640x480", "1296x972", "1640x1232"],
    pad=(0, 3),
    size=(8, None),
    key="-RES-",
    default_value="1296x972",
)

# select video framerate
btn_fps = sg.Combo(
    [15, 20, 25, 30],
    pad=(0, 3),
    size=(8, None),
    key="-FPS-",
    default_value=30,
)

# select clip duration
btn_clipdur = sg.Combo(
    [3, 10, 30, 60, 90, 120],
    pad=(0, 3),
    size=(8, None),
    key="-CLDUR-",
    default_value=60,
)

# sdt = datetime(1900, 1, 1, 15, 0)
# sdt_list = [(sdt + timedelta(minutes=m)).isoformat() for m in range(0, 520, 60)]  # 520
# st_list = [(datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")).time() for dt in sdt_list]

# edt = datetime(1900, 1, 1, 0, 0)
# edt_list = [(edt + timedelta(minutes=m)).isoformat() for m in range(0, 520, 60)]
# et_list = [(datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")).time() for dt in edt_list]

# select recording start time
btn_strt_hr = sg.Combo(
    list(range(0, 23)),
    pad=(0, 3),
    size=(2, None),
    key="-STRTHR-",
    default_value=17,
)

# select recording end time
btn_strt_min = sg.Combo(
    [0, 10, 20, 30, 40, 50],
    pad=(0, 3),
    size=(2, None),
    key="-STRTMIN-",
    default_value=0,
)

btn_length = sg.Combo(
    list(range(0, 23)),
    pad=(0, 3),
    size=(8, None),
    key="-RECLEN-",
    default_value=12,
)

# select daytime timelapse interval
# btn_timelapse = sg.OptionMenu(
#    [0, 1, 2, 3, 5],
#    pad=(0.1, 0.1, 0.1, 0.1),
#    size=(6, 1),
#    key="-TLPS-",
#    default_value=3,
# )

# save parameters
btn_save = sg.Button("Save", enable_events=True, key="-SAVE-")

# start recording
btn_start = sg.Button("Start", enable_events=True, key="-START-", disabled=True)

# stop recording
btn_stop = sg.Button("Stop", enable_events=True, key="-STOP-", disabled=True)

# quit app
# btn_quit = sg.Button("Quit", enable_events=True, key="-QUIT-", disabled=False)

## UI Layout and appearance ##

# Set color theme
sg.theme("DarkTanBlue")  # Set colour theme

# Set left (text) column layout
text_column = [
    [sg.Text("Pi Number")],
    [sg.Text("Video Resolution")],
    [sg.Text("Video frame rate")],
    [sg.Text("Clip Duration (s)")],
    #    [sg.Text("Daytime photo every ")],
    [sg.Text("Start at (HH:MM)")],
    [sg.Text("Record for (hours)")],
]

#  Set right (options) layout
option_column = [
    [btn_pinum],
    [btn_res],
    [btn_fps],
    [btn_clipdur],
    #    [btn_timelapse, sg.Text("s")],
    [btn_strt_hr, sg.Text(":", pad=(0, 0)), btn_strt_min],
    [btn_length],
]

button_row = [[btn_save, btn_start, btn_stop]]

# Set 2-column window layout
layout = [
    [
        sg.Column(
            text_column,
            element_justification="left",
            vertical_alignment="top",
            pad=(0, 1),
        ),
        sg.Column(
            option_column,
            element_justification="center",
            vertical_alignment="top",
            pad=(0, 1),
        ),
    ],
    [
        button_row,
    ],
]

### App execution ###

# Create the Window
window = sg.Window(
    "LamPi UI",
    layout,
    size=(190, 210),
    location=(0, 0),
    margins=(0, 0),
    element_justification="c",
    font=("Piboto Condensed", 10),
)

# Event Loop to process events (get values and run functions)
while True:
    event, values = window.read()
    # Stopping rules
    if (
        event == sg.WIN_CLOSED or event == "-QUIT-"
    ):  # ends program if user closes window
        break
    elif event == "-SAVE-":
        pickle.dump(values, open("/home/pi/LamPi/params/params.p", "wb"))
        window.FindElement("-START-").Update(disabled=False)
    # Start buttons sets the camera and toggles the recording state
    elif event == "-START-":
        command = [
            "lxterminal",
            "--geometry=477x274+4+68",
            "-e",
            "python3",
            "/home/pi/LamPi/scripts/lampi_run_terminal.py",
        ]
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        window.FindElement("-START-").Update(disabled=True)
        window.FindElement("-STOP-").Update(disabled=False)
        window.FindElement("-SAVE-").Update(disabled=True)
    elif event == "-STOP-":
        process.send_signal(signal.SIGINT)
        window.FindElement("-STOP-").Update(disabled=True)
        window.FindElement("-SAVE-").Update(disabled=False)
window.close()

# pid = subprocess.check_output(cm"pgrep -f 'xterm -e bash test.bash'", shell=True)
#        os.kill(pid, signal.SIGINT)
