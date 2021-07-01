# Add header info here


### Importing packages
from tkinter import *
from tkinter import ttk
import pickle

### UI Functions
# Function to save the recording parameters
def save_params(params):
    pickle.dump(params, open("params.p", "wb" ))

### Main UI

# root and framne UI definitions
root = Tk()
root.title("Lampi Ui Tk")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

### Define paramter widgets

# Select pi number from dropdown list
piNum = IntVar()
piNumCombobox = ttk.Combobox(mainframe, textvariable=piNum)
piNumCombobox['values'] = (1,2,3,4,5,6,7,8,9,10)
piNumCombobox.state(['readonly'])

# Select video resolution
vidRes = IntVar()
vidResCombobox = ttk.Combobox(mainframe, textvariable=vidRes)
vidResCombobox['values'] = ((640,480), (800,600), (960,720), (1024,768), (1280,960), (1400,1050), (1440,1080))
vidResCombobox.state(['readonly'])

# Select frame rate 
vidFPS = IntVar()
vidFPSCombobox = ttk.Combobox(mainframe, textvariable=vidFPS)
vidFPSCombobox['values'] = (10,15,30,60)
vidFPSCombobox.state(['readonly'])

# Select video duration 
vidDur = IntVar()
vidDurCombobox = ttk.Combobox(mainframe, textvariable=vidDur)
vidDurCombobox['values'] = (1,3,10,30,60,120,300,600)
vidDurCombobox.state(['readonly'])

# Select recording start time  
vidStrt = IntVar()
vidStrtCombobox = ttk.Combobox(mainframe, textvariable=vidStrt)
vidStrtCombobox['values'] = (1,3,10,30,60,120,300)
vidStrtCombobox.state(['readonly'])

# Select recording end time  
vidEnd = IntVar()
vidEndCombobox = ttk.Combobox(mainframe, textvariable=vidEnd)
vidEndCombobox['values'] = (1,3,10,30,60,120,300)
vidEndCombobox.state(['readonly'])

# Select out of hours timelapse timing   
timeLapse = IntVar()
timeLapseCombobox = ttk.Combobox(mainframe, textvariable=timeLapse)
timeLapseCombobox['values'] = (1,3,10,30,60,120,300)
timeLapseCombobox.state(['readonly'])

# Option to restart with saved pameters
reStart = BooleanVar()
reStartCheckbutton = ttk.Checkbutton(mainframe, text='Autostart recording on boot', variable=reStart)
	    

### UI layout

# Left columns (0,1)
ttk.Label(mainframe, text="Pi Number ").grid(column=0, row=1, sticky=W)
piNumCombobox.grid(column=1, row=1, sticky=(W, E))

ttk.Label(mainframe, text="Video resolution ").grid(column=0, row=2, sticky=W)
vidResCombobox.grid(column=1, row=2, sticky=(W, E))

ttk.Label(mainframe, text="Video frame rate ").grid(column=0, row=3, sticky=W)
vidFPSCombobox.grid(column=1, row=3, sticky=(W, E))

ttk.Label(mainframe, text=" Clip duration ").grid(column=2, row=3, sticky=W)
vidDurCombobox.grid(column=3, row=3, sticky=(W, E))

ttk.Label(mainframe, text="Start recording at ").grid(column=0, row=4, sticky=W)
vidStrtCombobox.grid(column=1, row=4, sticky=(W, E))

ttk.Label(mainframe, text=" End at ").grid(column=2, row=4, sticky=W)
vidEndCombobox.grid(column=3, row=4, sticky=(W, E))

ttk.Label(mainframe, text=" Out of hours timelapse rate ").grid(column=0, row=5, sticky=W)
timeLapseCombobox.grid(column=1, row=5, sticky=(W, E))

reStartCheckbutton.grid(column=0, row=6)

root.mainloop()