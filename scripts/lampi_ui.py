from types import TracebackType
import PySimpleGUI as sg
import os.path

sg.theme('System Default 1')   # Add a touch of color

# Elements

btn_pinum = sg.OptionMenu(
    [1,2,3,4,5,6,7,8,9,10], key='-PINUM-'
)

btn_res = sg.OptionMenu(
    [(640,480), (800,600), (960,720), (1024,768), (1280,960), (1400,1050), (1440,1080)],  key='-RES-'
)

btn_fps = sg.OptionMenu(
    [10,15,30,60],  key='-FPS-'
)

btn_cliplen = sg.OptionMenu(
    [1,3,10,30,60,90,120,300,600], key='-CLEN-'
)

btn_strtime = sg.OptionMenu(
    [1,2,3,4,5,6,7,8,9,10],  key='-STRT-'
)

btn_endtime = sg.OptionMenu(
    [1,3,10,30,60,90,120,300,600],  key='-ENDT-'
)

# Setup column layout
setup_column = [  
    [sg.Text('Pi Number'), btn_pinum],
    [sg.Text('Resolution'), btn_res],
    [sg.Text('FPS'), btn_fps],
    [sg.Text('Duration (s)'), btn_cliplen],
    [sg.Text('Start/End Time'), btn_strtime, btn_endtime],
    [sg.Text('Save path:')],
    [sg.In(size=(25,1), enable_events=True, key='-FOLDER-'), sg.FolderBrowse()]    
]

#  Setup run layout         

run_column = [
    [sg.Button('Start', size=(25,2), enable_events=True,  key='-START-')],
    [sg.Multiline('Select settings and hit "Start"', size=(27,5), key='-TEXTBOX-')]
] 


# Window layout

layout = [
    [sg.Column(setup_column),sg.VSeparator(),sg.Column(run_column)]
]

# Create the Window 
window = sg.Window('LamPi UI', layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    window['-TEXTBOX-'].print('You entered ', values['-CLEN-'])

window.close()