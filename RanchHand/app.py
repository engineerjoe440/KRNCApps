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
import configparser

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
configfile = 'C:\\ProgramData\\StanleySolutions\\KRNC\\RanchHand\\config.ini'

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
# Read Configuration File
config = configparser.ConfigParser()
config.read(configfile)
#######################################################################################

#######################################################################################
# Build Window Layout
inputsCol = [
    [sg.Text('OneDrive Audio Folder',size=(descWidth,1)),
        sg.In(key='OneDriveMusic'),sg.FolderBrowse(target='OneDriveMusic')],
    [sg.Text('OneDrive VirtualDJ Folder',size=(descWidth,1)),
        sg.In(key='OneDriveSettings'),sg.FolderBrowse(target='OneDriveSettings')],
    [sg.Text('Local VirtualDJ Folder',size=(descWidth,1)),
        sg.In(key='LocalSettings'),sg.FolderBrowse(target='LocalSettings')],
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
    # Test for Valid Configuration File
    if not config.sections():
        print("No valid Ranch Hand configuration file...",
            "New configuration file will be generated.")
        # Build Default Configuration
        config['RanchHand'] = {
            "OneDriveMusic" : "",
            "OneDriveSettings" : "",
            "LocalSettings" : "",
        }
    # Load Configuration Strings
    window['OneDriveMusic'].update(value=config['RanchHand']['OneDriveMusic'])
    window['OneDriveSettings'].update(value=config['RanchHand']['OneDriveSettings'])
    window['LocalSettings'].update(value=config['RanchHand']['LocalSettings'])
    # Run Event Loop
    while True:
        # Capture Values from Window Event
        event, values = window.read()
        # Manage Events
        if event in (None, 'Exit'):
            break
        # Open Help Page (GitHub Markdown)
        elif event == 'help':
            webbrowser.open(helpdoc)
        # Manage Save Settings Configuration
        elif event == 'save':
            # Capture New Configuration
            config['RanchHand']['OneDriveMusic'] = window['OneDriveMusic'].get()
            config['RanchHand']['OneDriveSettings'] = window['OneDriveSettings'].get()
            config['RanchHand']['LocalSettings'] = window['LocalSettings'].get()
            # Store Configuration
            with open(configfile, 'w') as conffile:
                config.write(conffile)
            # Indicate Success
            print("Successfully updated configuration.")
#######################################################################################    


#######################################################################################
# Run App if Main
if __name__ == '__main__':
    app()
    
window.close()

# END