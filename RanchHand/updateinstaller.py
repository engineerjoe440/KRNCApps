"""
#######################################################################################
Ranch Hand - Updater/Installer System
(c) Stanley Solutions

By: Joe Stanley
#######################################################################################
"""

# Capture Version from Service Application
from RanchHandService import get_version, get_service_info, look_up_state, kill_proc
print("Installer Build Version:", get_version())

# Import Required Dependencies
import os
import re
import sys
import csv
import time
import ctypes
import psutil
import zipfile
import requests
import threading
import traceback
import subprocess
import win32com.client
import win32serviceutil
import PySimpleGUI as sg
from pathlib import Path
from alive_progress import alive_bar

print("Executable Location:", sys.executable)

# Define Boolean Control
serviceInstalled = False

# Define Folder Locations
programData  = 'C:/ProgramData/StanleySolutions/KRNC/RanchHand/'
programFiles = 'C:/Program Files (x86)/StanleySolutions/KRNC/RanchHand/images/'
startFolder  = 'C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Stanley Solutions/'

# Define Download Descriptor Location
web_requirements_file = 'https://raw.githubusercontent.com/engineerjoe440/KRNCApps/master/RanchHand/requirements.csv'

# Define Current Python Embeddable Installation Rules
py_embedded_url = "https://www.python.org/ftp/python/3.8.3/python-3.8.3-embed-amd64.zip"
py_local_path = programFiles.replace('images', 'python38') + 'dist.zip'

# Define Service File Location
service_file = programFiles.replace('images/', 'RanchHandService.exe')
servicename = get_service_info()['name']

# Define UAC Elevation Decorator
def elevateUAC( func ):
    """ Simple Wrapper Function to Elevate to Admin with UAC """
    # Define Imports Required for Elevation
    import ctypes, sys
    import time
    # Define Inner Test to Evaluate
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    # Define Inner Wrapper Function
    def inner():
        # Test for Admin Level
        if is_admin():
            # Run the Function at Admin Level
            func()
        else:
            # Re-run the program with admin rights
            command = '"{}" {}'.format(sys.argv[0], " ".join(sys.argv[1:]))
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, 
                                                command, None, 1)
    # Return Inner Function
    return( inner )

# Define Simple Function to Clear Previous Line
def clear_line():
    sys.stdout.write("\033[F") #back to previous line
    sys.stdout.write("\033[K") #clear line

# Define Spinner
class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1: 
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def __enter__(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            return False

# Define Function to Close Active RanchHand App and Stop Windows Service
def close_and_stop():
    global serviceInstalled
    # Close RanchHand App
    for proc in psutil.process_iter():
        if 'RanchHand.exe' == proc.name:
            proc.kill() # Kill the Application
    # Stop Ranch Hand Service
    try:
        serviceSta = win32serviceutil.QueryServiceStatus(servicename)
        serviceInstalled = True
    except:
        print("KRNC Ranch Hand service could not be detected on system.")
        serviceInstalled = False
    else:
        # Look Up Current State from LUT Dictionary
        curState = look_up_state( serviceSta[1] )
        if curState != 'stopped':
            print("Stopping Service...")
            # Stop Service
            try:
                win32serviceutil.StopService(servicename)
                print("Stopped.")
            except:
                print("Failed to stop service. Killing Instead.")
                kill_proc()

# Define Function to Generate Folder Paths
def build_folders():
    # Check for Folder Locations
    if not os.path.exists(programData):
        Path(os.path.dirname(programData)).mkdir(parents=True, exist_ok=True)
    if not os.path.exists(programFiles):
        Path(os.path.dirname(programFiles)).mkdir(parents=True, exist_ok=True)
    if not os.path.exists(startFolder):
        Path(os.path.dirname(startFolder)).mkdir(parents=True, exist_ok=True)

# Define Function to Build Shortcut Link for Application
def make_link():
    # Use Win32com to Build Link
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(startFolder + 'Ranch Hand.lnk')
    shortcut.Targetpath = service_file.replace('Service','')
    shortcut.IconLocation = programFiles.replace('RanchHand/images/', 'KRNC.ico')
    shortcut.WindowStyle = 1 # 7 - Minimized, 3 - Maximized, 1 - Normal
    shortcut.save()

# Define Function to Read Requirements from Web-Based CSV
def read_requirements():
    # Open File from Web to Identify Requirements
    requires = requests.get(web_requirements_file)
    requirements = requires.content.decode('utf-8').split('\n')
    # Build Descriptive Structure
    for ind, row in enumerate(requirements):
        requirements[ind] = row.split(',')
    return(requirements)

# Define Function to Download and "Install" the Requirements
def download_requirement( requirement ):
    # Break Out Constituent Elements
    localPath, url = requirement
    # Open File from Web for Reading
    if (url != 'null') and (localPath != sys.executable):
        resp = requests.get( url )
        with open(localPath, 'wb') as localObj:
            localObj.write( resp.content )
    elif url != 'null':
        print("(w) Unable to locate remote URL for requirement:",
                os.path.basename(localPath))
    else:
        print("Update/Installer already installed. Ignoring.")

# Define Function to "Ask Windows" Where Python Executable Lives
def where_python():
    # "Ask" Windows Where Python Executable Lives
    proc = subprocess.Popen('where python',shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    # Wait for Response
    stdout, stderr = proc.communicate()
    # If Success, Capture Result
    if str(proc.returncode) == '0':
        location = stdout.decode('utf-8').split('\n')[0]
        if location.endswith('python.exe'):
            return(location)

# Define Function to Install Embedded Copy of Python
def install_python():
    # Make the Directory for Embedded Python Dist
    os.mkdir( os.path.dirname(py_local_path) )
    # Download Embedded Python Distribution
    print("Downloading embedded Python distribution...")
    download_requirement( [py_local_path, py_embedded_url] )
    # Unzip Embedded Python Dist
    print("Unzipping embedded Python distribution...")
    with zipfile.ZipFile(py_local_path, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(py_local_path))
    # Add Python to System Path
    print("Adding embedded Python to Windows PATH variable.")
    command = 'setx PATH=%PATH%;"{}"'.format(os.path.dirname(py_local_path))
    retcode = subprocess.call(command, shell=True)
    if retcode:
        print("An error occurred when adding Python to PATH.")
        time.sleep(5)
        sys.exit(1)

# Define Function to Install/Update Windows Service
def windows_service():
    # Manage Windows Service Already Installed
    if serviceInstalled:
        # Update Service
        args = '"{}" update'.format(service_file)
        fail = subprocess.call(args, shell=True)
        if fail:
            print("Failed to update RanchHandService.\n")
            clear_line()
            time.sleep(5)
            sys.exit(1)
        # Start Service
        try:
            win32serviceutil.StartService(servicename)
            print("Started RanchHandService")
        except:
            print("Failed to start RanchHandService.\n")
            clear_line()
            time.sleep(5)
            sys.exit(1)
    # Managed Windows Service Not Already Installed
    else:
        # Check for Valid Python Installation
        pythonLocation = where_python()
        # No Valid Python Installation
        if pythonLocation == None:
            # Install Python
            install_python()
        # Python Installed for User
        elif pythonLocation.find('AppData') != -1:
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
            # Identify Active Username
            username = re.findall(r'C:\\Users\\(.+)\\AppData\\Local',pythonLocation)[0]
            # Prompt for Password from User
            Yn = sg.popup_yes_no(('A user-specific Python installation was detected.'
                                    +' Ranch Hand can use this install, but the '
                                    +'password assocaited with this user is needed.'),
                                ('Would you like to use this installation, or install'
                                    +' Python at a system level? Yes = Use My '
                                    +'Installation; No = Install Python System-Wide'),
                                title='Confirm Use of Current Python Install',
                                icon=programFiles.replace('RanchHand/images/',
                                                            'KRNC.ico'),
                                )
            # Local Installation Accepted
            if Yn.lower() == 'yes':
                # Capture Password
                pswd = sg.popup_get_text(('Please provide the password for the user'
                                            +' "{}".').format(username),
                                        title='Provide User Password',
                                        icon=programFiles.replace('RanchHand/images/',
                                                            'KRNC.ico'),
                                        password_char='*',
                                        )
                # Validate Password
                if pswd == '':
                    clear_line()
                    print("Invalid password provided, aborting.")
                    time.sleep(5)
                    sys.exit(1)
                command = ('{} --username ".\\{}" --password {} --startup '
                            +'auto install'.format(service_file, username, pswd))
                clear_line()
                retcode = subprocess.call(command, shell=True)
                if retcode:
                    clear_line()
                    print("An error occurred while installing service.")
                    time.sleep(5)
                    sys.exit(1)
            else:
                # Install Python
                install_python()
                clear_line()
                command = "{} --startup auto install".format(service_file)
                retcode = subprocess.call(command, shell=True)
                if retcode:
                    clear_line()
                    print("An error occurred while installing service.")
                    time.sleep(5)
                    sys.exit(1)
        


# Define Main Function
@elevateUAC
def main():
    # Start Status Progress Bar
    prog_bar_count = 5
    with alive_bar(prog_bar_count,spinner='classic') as progress_bar:
        # Close and Stop RanchHand App and Service
        progress_bar('stopping service and app')
        close_and_stop()
        # Build Folders
        progress_bar('building folders')
        build_folders()
        # Make Link
        progress_bar('making shortcut link')
        make_link()
        # Identify Requirements
        try:
            progress_bar('identifying required resources')
            requires = read_requirements()
            progress_bar('preparing to download requirements')
        except Exception:
            print("(e) Unable to open web-handle for requirements file.")
            traceback.print_exc()
            time.sleep(5)
            sys.exit(1)
    #clear_line()
    # Manage Resource Download
    with alive_bar(len(requires),spinner='classic') as progress_bar:
        # Download Requirements
        for requirement in requires:
            print("(i) Downloading Requirement:", os.path.basename(requirement[0]))
            try:
                download_requirement( requirement )
                progress_bar()
            except Exception:
                print("(e) Failed to download requirement:",
                        os.path.basename(requirement[0]))
                traceback.print_exc()
    # Install (or update) Windows Service
    with Spinner():
        windows_service()
    clear_line()
    
    # Remark on Completion
    print("\n(i) KRNC RanchHand Installation/Update Complete!")
    input("Press the enter/return key to complete.")



# Create Entrypoint
if __name__ == '__main__':
    time.sleep(1) # Grant time for App to close
    # Call Main Function
    main()


# END
