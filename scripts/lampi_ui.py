# from types import TracebackType
import PySimpleGUI as sg  # to create and run the UI
import os.path  # to handle file paths
import pickle  # to save parameters

##### Define / Import functions ######


def save_params(params):
    pickle.dump(params, open("params.p", "wb"))


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
# select clip length
btn_cliplen = sg.OptionMenu([1, 3, 10, 30, 60, 90, 120, 300, 600], key="-CLEN-")

# select recording start time
btn_strtime = sg.OptionMenu([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], key="-STRT-")

# select recording end time
btn_endtime = sg.OptionMenu([1, 3, 10, 30, 60, 90, 120, 300, 600], key="-ENDT-")

# save parameters
btn_save = sg.Button("Save", enable_events=True, key="-SAVE-")

# start recording
btn_start = sg.Button("Start", size=(25, 1), enable_events=True, key="-START-")

# Checkboxes #

chbx_daytime = sg.Checkbox(
    "Enable 2sec timelapse outside recording hours?", default=False, key="-DTLPS-"
)

# Multiline text box #

out_box = sg.Multiline(
    """1) Select settings
    2) Save settings
    3) Click 'Start' """,
    size=(27, 8),
    key="-TEXTBOX-",
)


## UI Layout and appearabnce ##

sg.theme("System Default 1")  # Set colour theme

# Set left (parameter input ) column layout
setup_column = [
    [sg.Text("Pi Number"), btn_pinum],
    [sg.Text("Video Resolution"), btn_res],
    [sg.Text("Video frame rate"), btn_fps, sg.Text("Duration (s)"), btn_cliplen],
    [sg.Text("Start recording at: "), btn_strtime, sg.Text(" End at: "), btn_endtime],
    [sg.Text("Save path:"), sg.In(size=(25, 1), key="-FOLDER-"), sg.FolderBrowse()],
    [chbx_daytime, btn_save],
]

#  Set right (run app) layout
run_column = [[btn_start], [out_box]]

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
window = sg.Window("LamPi UI", layout)

# Event Loop to process events (get values and run functions)
while True:
    event, values = window.read()
    if event == "-SAVE-":
        save_params(values)
        window["-TEXTBOX-"].print("\nParameters saved:\n", values)
    if event == sg.WIN_CLOSED:  # ends program if user closes window
        break

window.close()
