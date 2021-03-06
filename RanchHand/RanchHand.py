"""
#######################################################################################
Ranch Hand - Tkinter App
(c) Stanley Solutions

By: Joe Stanley
#######################################################################################
"""

# Capture Version from Service Application
from RanchHandService import get_version, get_service_info, look_up_state
__version__ = get_version()

# Import Required Dependencies
import os
import sys
import time
import PySimpleGUI as sg
import webbrowser
import subprocess
import configparser
import win32serviceutil
from pathlib import Path

# Import Local Dependencies
import vdjsettings as vdj

# Define Generic Parameters
bgblue = '#506c91'
fgblue = 'white'
bglblue = '#bdc7e5'
fglblue = 'black'
bggrey = '#c9cdd9'
fggrey = '#506c91'
slider = '#00A800'
warnred = '#ECC7DB'
descWidth = 20
sepWidth = 23
titleWidth = 74
outputWidth = 140
outputHeight = 7
servicename = get_service_info()['name']
helpdoc = 'https://github.com/engineerjoe440/KRNCApps/blob/master/RanchHand/README.md'
configfile = 'C:\\ProgramData\\StanleySolutions\\KRNC\\RanchHand\\config.ini'
programFile = 'C:\\Program Files (x86)\\StanleySolutions\\KRNC'
updateEXE = '"' + programFile + '\\RanchHand\\updateinstaller.exe"'

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
logo = os.path.join(programFile, "KRNCnegative.png")
icon = os.path.join(programFile, 'KRNC.ico')
help = os.path.join(programFile, 'RanchHand', 'images', "help.png")
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
        sg.ButtonMenu('',['',['Documentation','Update Ranch Hand']], 
            key='help', image_filename=help, image_size=(25, 25), 
            image_subsample=3, border_width=0)],
    [sg.Column(inputsCol), sg.Column(spcrCol), sg.Column(contCol)],
    [sg.Output(size=(outputWidth, outputHeight),font=('TkDefaultFont',8))],
]
#######################################################################################

#######################################################################################
# Construct Window and Start Event Loop
window = sg.Window('KRNC Ranch Hand', mainlayout, icon=icon)
def app():
    global window
    window.finalize()
    # Print KRNC Welcome Message
    print("Welcome Home.")
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
        # "Clean" Input Fields by Default
        window['OneDriveMusic'].update(background_color=bglblue)
        window['OneDriveSettings'].update(background_color=bglblue)
        window['LocalSettings'].update(background_color=bglblue)
        # Manage Events
        if event in (None, 'Exit'):
            break
        # Open Help Page (GitHub Markdown)
        elif event == 'help':
            if values['help'] == 'Documentation':
                webbrowser.open(helpdoc)
            elif values['help'] == 'Update Ranch Hand':
                # Confirm Desire to Update
                response = sg.popup_yes_no('Are you sure you want to update now?',
                                ('Updating now will stopp the application and will'
                                    +' stop any active file synchronization tasks '
                                    +'that are currently active.'),
                                ('It is recommended that VirtualDJ be closed during'
                                    +' Ranch Hand updates.'),
                                title='Confirm Update', icon=icon)
                if response.lower() != 'yes':
                    print("Upgrade Aborted")
                    continue
                # Call Updater in Subproccess
                subprocess.Popen(updateEXE, shell=True)
        # Manage Save/Push/Pull Settings from OneDrive
        elif event in ['save', 'pull', 'push']:
            # Validate all Configuration Before Restarting Service
            if not (window['OneDriveMusic'].get() and
                window['OneDriveSettings'].get() and
                window['LocalSettings'].get()) :
                # Not Valid! Inform User
                print("All fields are required!")
                # Warn for Local Settings Folder Input
                if not window['LocalSettings'].get():
                    window['LocalSettings'].update(background_color=warnred)
                    window['LocalSettings'].SetFocus()
                # Warn for Remote OneDrive Settings
                if not window['OneDriveSettings'].get():
                    window['OneDriveSettings'].update(background_color=warnred)
                    window['OneDriveSettings'].SetFocus()
                # Warn for Remote OneDrive Music Folder
                if not window['OneDriveMusic'].get():
                    window['OneDriveMusic'].update(background_color=warnred)
                    window['OneDriveMusic'].SetFocus()
                # Continue Loop
                continue
            
            else:
                # Capture New Configuration
                config['RanchHand']['OneDriveMusic'] = window['OneDriveMusic'].get()
                config['RanchHand']['OneDriveSettings'] = window['OneDriveSettings'].get()
                config['RanchHand']['LocalSettings'] = window['LocalSettings'].get()
            
            # Manage Save Settings Configuration
            if event == 'save':
                print("Saving...")
                window.Refresh()
                # Validate Storage Location
                if not os.path.exists(os.path.dirname(configfile)):
                    Path(os.path.dirname(configfile)).mkdir(parents=True, exist_ok=True)
                # Store Configuration
                with open(configfile, 'w') as conffile:
                    config.write(conffile)
                # Indicate Success
                print("Successfully updated configuration.")
                window.Refresh()
                # Copy Local Files Over Remote
                try:
                    # Move Folders
                    vdj.modify_move_folders(
                        srcpath = config['RanchHand']['LocalSettings'],
                        dstpath = config['RanchHand']['OneDriveSettings'],
                        srcstring = config['RanchHand']['LocalSettings'],
                        dststring = vdj.generic_path,
                        window = window
                    )
                except Exception as e:
                    print("Attempt to mirror local settings to OneDrive failed.")
                    print(e)
                window.Refresh()
                # Manage the Windows Service
                try:
                    serviceSta = win32serviceutil.QueryServiceStatus(servicename)
                except:
                    print("KRNC Ranch Hand Service is Not Installed!")
                    window.Refresh()
                else:
                    # Look Up Current State from LUT Dictionary
                    curState = look_up_state( serviceSta[1] )
                    print("KRNC Ranch Hand Service is: {}".format(curState.upper()))
                    window.Refresh()
                    if curState != 'stopped':
                        print("Stopping Service...")
                        window.Refresh()
                        # Stop Service
                        try:
                            win32serviceutil.StopService(servicename)
                            print("Stopped.")
                            window.Refresh()
                        except:
                            print("Failed to stop service. Please try again.")
                            continue
                    # Start the Windows Service
                    print("Starting Service...")
                    window.Refresh()
                    try:
                        win32serviceutil.StartService(servicename)
                        print("Started.")
                        window.Refresh()
                    except:
                        print("Failed to start service. Please try again.")
                        continue # in case more code is added later
            # Manage Pull Settings
            elif event == 'pull':
                # Copy Remote Files Over Local
                try:
                    # Move Folders
                    print("Starting Pull...")
                    window.Refresh()
                    vdj.modify_move_folders(
                        srcpath = config['RanchHand']['OneDriveSettings'],
                        dstpath = config['RanchHand']['LocalSettings'],
                        srcstring = vdj.generic_path,
                        mxsrcstring = vdj.generic_mx_path,
                        dststring = config['RanchHand']['LocalSettings'],
                        mxdststring = config['RanchHand']['OneDriveMusic'],
                        window = window,
                    )
                    print("Settings Pull Completed!")
                except Exception as e:
                    print("Attempt to mirror local settings to OneDrive failed.")
                    print(e)
            # Manage Push Settings
            elif event == 'push':
                # Copy Local Files Over Remote
                try:
                    # Move Folders
                    print("Starting Push...")
                    window.Refresh()
                    vdj.modify_move_folders(
                        srcpath = config['RanchHand']['LocalSettings'],
                        dstpath = config['RanchHand']['OneDriveSettings'],
                        srcstring = config['RanchHand']['LocalSettings'],
                        mxsrcstring = config['RanchHand']['OneDriveMusic'],
                        dststring = vdj.generic_path,
                        mxdststring = vdj.generic_mx_path,
                        window = window,
                    )
                    print("Settings Push Completed!")
                except Exception as e:
                    print("Attempt to mirror local settings to OneDrive failed.")
                    print(e)
#######################################################################################    


#######################################################################################
# Run App if Main
if __name__ == '__main__':
    try:
        app()
    except Exception as e:
        print("Exception Occured:", e)
    
    window.close()

# END