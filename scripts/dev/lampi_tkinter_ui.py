# Add header info here


### Importing packages
from tkinter import *
from tkinter import ttk
import pickle

### UI Functions
# Function to save the recording parameters
def save_params(params):
    pickle.dump(params, open("params.p", "wb"))


### Main UI

# root window and framne UI definitions
root = Tk()
root.title("Lampi Ui Tk")
root.geometry("480x320+5+5")

# mainframe = ttk.Frame(root, padding="3 3 3 3")
# mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.columnconfigure(4, weight=1)
root.columnconfigure(5, weight=4)

### Define paramter widgets

# Select pi number from dropdown list
piNum = IntVar()
piNumCombobox = ttk.Combobox(root, textvariable=piNum)
piNumCombobox["values"] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
piNumCombobox.state(["readonly"])

# Select video resolution
vidRes = IntVar()
vidResCombobox = ttk.Combobox(root, textvariable=vidRes)
vidResCombobox["values"] = (
    (640, 480),
    (800, 600),
    (960, 720),
    (1024, 768),
    (1280, 960),
    (1400, 1050),
    (1440, 1080),
)
vidResCombobox.state(["readonly"])

# Select frame rate
vidFPS = IntVar()
vidFPSCombobox = ttk.Combobox(root, width=2, textvariable=vidFPS)
vidFPSCombobox["values"] = (10, 15, 30, 60)
vidFPSCombobox.state(["readonly"])

# Select video duration
vidDur = IntVar()
vidDurCombobox = ttk.Combobox(root, width=3, textvariable=vidDur)
vidDurCombobox["values"] = (1, 3, 10, 30, 60, 120, 300, 600)
vidDurCombobox.state(["readonly"])

# Select recording start time
vidStrt = IntVar()
vidStrtCombobox = ttk.Combobox(root, width=3, textvariable=vidStrt)
vidStrtCombobox["values"] = (1, 3, 10, 30, 60, 120, 300)
vidStrtCombobox.state(["readonly"])

# Select recording end time
vidEnd = IntVar()
vidEndCombobox = ttk.Combobox(root, width=3, textvariable=vidEnd)
vidEndCombobox["values"] = (1, 3, 10, 30, 60, 120, 300)
vidEndCombobox.state(["readonly"])

# Select out of hours timelapse timing
timeLapse = IntVar()
timeLapseCombobox = ttk.Combobox(root, width=3, textvariable=timeLapse)
timeLapseCombobox["values"] = (1, 3, 10, 30, 60, 120, 300)
timeLapseCombobox.state(["readonly"])

# Option to restart with saved pameters
reStart = BooleanVar()
reStartCheckbutton = ttk.Checkbutton(
    root, text="Autostart recording on boot", variable=reStart
)


### UI layout

# Left columns (0,1)
ttk.Label(root, text="Pi Number ").grid(column=1, row=1, sticky=W)
piNumCombobox.grid(column=2, row=1, sticky=(W, E))

ttk.Label(root, text="Video resolution ").grid(column=1, row=2, sticky=W)
vidResCombobox.grid(column=2, row=2, sticky=(W, E))

ttk.Label(root, text="Video frame rate ").grid(column=1, row=3, sticky=W)
vidFPSCombobox.grid(column=2, row=3, sticky=(W, E))
ttk.Label(root, text=" Clip duration ").grid(column=3, row=3, sticky=W)
vidDurCombobox.grid(column=4, row=3, sticky=(W, E))

ttk.Label(root, text="Start recording at ").grid(column=1, row=4, sticky=W)
vidStrtCombobox.grid(column=2, row=4, sticky=(W, E))
ttk.Label(root, text=" End at ").grid(column=3, row=4, sticky=W)
vidEndCombobox.grid(column=4, row=4, sticky=(W, E))

ttk.Label(root, text=" Out of hours timelapse rate ").grid(column=1, row=5, sticky=W)
timeLapseCombobox.grid(column=2, row=5, sticky=(W, E))

reStartCheckbutton.grid(column=1, row=6)

root.mainloop()
