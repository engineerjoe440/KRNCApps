"""
#######################################################################################
Ranch Hand - Tkinter App
(c) Stanley Solutions

By: Joe Stanley
#######################################################################################
"""

# Import Required Dependencies
import os
import time
import PySimpleGUI as sg
import webbrowser

# Define Generic Parameters
bgblue = '#506c91'
fgblue = 'white'
bglblue = '#bdc7e5'
fglblue = 'black'
bggrey = '#c9cdd9'
fggrey = '#506c91'
slider = '#00A800'
descWidth = 20
sepWidth = 23
titleWidth = 74
outputWidth = 120
outputHeight = 7
helpdoc = 'https://github.com/engineerjoe440/KRNCApps/blob/master/RanchHand/README.md'

#######################################################################################
# Add Custom Theme in-line with KRNC Coloring
sg.LOOK_AND_FEEL_TABLE['KrncTheme'] = {
    'BACKGROUND': bgblue,
    'TEXT': fgblue,
    'INPUT': bglblue,
    'TEXT_INPUT': fglblue,
    'SCROLL': '#c7e78b',
    'BUTTON': (fglblue, bglblue),
    'PROGRESS': (bggrey, slider),
    'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
}
# Set Theme Accordingly
sg.theme('KrncTheme')

# Define Image Path
imagedir = 'images'
logo = imagedir+"/KRNCnegative.png"
help = imagedir+"/help.png"
icon = imagedir+'/KRNC.ico'
#######################################################################################

#######################################################################################
# Build Window Layout
inputsCol = [
    [sg.Text('OneDrive Audio Folder',size=(descWidth,1)),
        sg.In(key='onedriveaudio'),sg.FolderBrowse(target='onedriveaudio')],
    [sg.Text('OneDrive VirtualDJ Folder',size=(descWidth,1)),
        sg.In(key='onedrivesettings'),sg.FolderBrowse(target='onedrivesettings')],
    [sg.Text('Local VirtualDJ Folder',size=(descWidth,1)),
        sg.In(key='localsettings'),sg.FolderBrowse(target='localsettings')],
]
contCol = [
    [sg.Button('Save Configuration',key='save',size=(descWidth,1))],
    [sg.Button('Push VDJ Settings Now',key='push',size=(descWidth,1))],
    [sg.Button('Pull VDJ Settings Now',key='pull',size=(descWidth,1))],
]
spcrCol = [[sg.Text(' '*sepWidth)]]
mainlayout = [
    [sg.Text('Ranch Hand - A VirtualDJ Shared Settings Manager',
        font=('TkDefaultFont',14),size=(titleWidth,1)),
        sg.Button('',key='help',image_filename=help,image_size=(25, 25),
            image_subsample=85, border_width=0)],
    [sg.Column(inputsCol), sg.Column(spcrCol), sg.Column(contCol)],
    [sg.Output(size=(outputWidth, outputHeight))],
]
#######################################################################################

#######################################################################################
# Construct Window and Start Event Loop
window = sg.Window('KRNC Ranch Hand', mainlayout, icon=icon)
def app():
    global window
    window.finalize()
    # Run Event Loop
    while True:
        # Capture Values from Window Event
        event, values = window.read()
        # Manage Events
        if event in (None, 'Exit'):
            break
        # Open Help Page (GitHub Markdown)
        if event == 'help':
            webbrowser.open(helpdoc)
#######################################################################################    


#######################################################################################
# Run App if Main
if __name__ == '__main__':
    app()
    
window.close()

# END