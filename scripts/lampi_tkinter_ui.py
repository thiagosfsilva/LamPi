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
root.title("Feet to Meters")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

### Define paramter widgets

# Select p number from dropdown list
piNum = IntVar()
piNumCombobox = ttk.Combobox(mainframe, textvariable=piNum)
piNumCombobox['values'] = (1,2,3,4,5,6,7,8,9,10)
piNumCombobox.state(['readonly'])



### UI layout
piNumCombobox.grid(column=1, row=1, sticky=(W, E))

root.mainloop()