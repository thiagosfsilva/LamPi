import PySimpleGUI as sg  # to create and run the UI
from datetime import datetime, timedelta  # to get date and time
import subprocess, signal, pickle

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

sdt = datetime(1900, 1, 1, 15, 0)
sdt_list = [(sdt + timedelta(minutes=m)).isoformat() for m in range(0, 520, 60)]
st_list = [(datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")).time() for dt in sdt_list]

edt = datetime(1900, 1, 1, 0, 0)
edt_list = [(edt + timedelta(minutes=m)).isoformat() for m in range(0, 520, 60)]
et_list = [(datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")).time() for dt in edt_list]

# select recording start time
btn_strtime = sg.OptionMenu(st_list, key="-STRT-", default_value=st_list[0])

# select recording end time
btn_endtime = sg.OptionMenu(et_list, key="-ENDT-", default_value=et_list[6])

# select daytime timelapse interval
btn_timelapse = sg.OptionMenu([1, 2, 5, 10], key="-TLPS-", default_value=5)

# save parameters
btn_save = sg.Button("Save", enable_events=True, key="-SAVE-")

# start recording
btn_start = sg.Button("Start", enable_events=True, key="-START-", disabled=True)

# stop recording
btn_stop = sg.Button("Stop", enable_events=True, key="-STOP-", disabled=True)

# quit app
btn_quit = sg.Button("Quit", enable_events=True, key="-QUIT-", disabled=False)

## UI Layout and appearance ##

# Set color theme
sg.theme("DarkTanBlue")  # Set colour theme

# Set left (parameter input) column layout
setup_column = [
    [sg.Text("Pi Number"), btn_pinum],
    [sg.Text("Video Resolution"), btn_res],
    [sg.Text("Video frame rate"), btn_fps],
    [sg.Text("Clip Duration (s)"), btn_clipdur],
    [sg.Text("Daytime photo every "), btn_timelapse, sg.Text("sec")],
    [sg.Text("Video Rec Start"), btn_strtime],
    [sg.Text("Video Rec Stop"), btn_endtime],
    [btn_save, btn_start, btn_stop],
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
window = sg.Window(
    "LamPi UI", layout, size=(240, 320), location=(0, 0), font=("Piboto Condensed", 10)
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
            "--geometry=40x24+241+1",
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