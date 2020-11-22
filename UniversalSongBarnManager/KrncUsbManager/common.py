"""
#######################################################################################
Universal Song Barn (USB) Manager - Tkinter App (powered by PySimpleGUI)
(c) Stanley Solutions - 2020

By: Joe Stanley
#######################################################################################
"""

# Import Requirements
import os, sys
import time
import requests
from pathlib import Path
import requests, zipfile, threading

# Filter imports
from KrncUsbManager.filters import filter_lookup as available_filters

# Attempt Windows/Linux Imports
try:
    from KrncUsbManager.windowsutil import *
    __platform__ = 'WINDOWS'
    # If Windows, Set Path
    utilbase = 'C:/ProgramData'
except ImportError:
    from KrncUsbManager.linuxutil import *
    # If Linux, Set Path
    utilbase = os.path.join(os.path.expanduser('~'), '.config')
    __platform__ = 'LINUX'

# Generic Defenitions
bgblue = '#506c91'
fgblue = 'white'
bglblue = '#bdc7e5'
fglblue = 'black'
bggrey = '#c9cdd9'
fggrey = '#506c91'
mainwidth = 80 # % of screen
mainheight = 70 # % of screen
col1width  = 55
col2width  = 20
col3width  = 15
tablwidth  = 1000
tablheight = 40
cntlwidth  = 200
cntl_obj_height = 15
drivheight = 100

# Define Fonts
table_head_font = ('Helvetica', 12)
table_body_font = ('Helvetica', 10)

# Define Standard Text Messages
splashText  = 'Welcome Home.'
windowTitle = 'Universal Song Barn Manager - Your Music Lives Here'

# Define OS Type Lookup
def os_platform(check_win=False, check_lin=False):
    """ Check for the operating platform """
    if check_lin and check_win:
        raise ValueError("Inputs are exclusive; choose one, not both.")
    if check_win and __platform__ == 'WINDOWS':
        return True
    elif check_win:
        return False # Not Running Windows
    elif check_lin and __platform__ == 'LINUX':
        return True
    elif check_lin:
        return False
    else:
        return __platform__

# Define Local Support File Path
userpath   = os.path.expanduser('~')
utilpath   = os.path.join(utilbase, "StanleySolutions/KRNC/USBManager/")
stockpath  = os.path.join(userpath, "Music/KRNC/USBManager/")
musicpath  = os.path.join(userpath, "Music/")
barnpath   = "/KRNC"
brndpath   = "/BRAND"
imagedir   = 'images'
drivedsc   = "krncdrive.barn"
filterpath = os.path.join(utilpath, 'Filters/')
krncbrandp = os.path.join(utilpath, 'KRNCbranding/')

# Create Local Paths if Nonexistent
Path(filterpath).mkdir(parents=True, exist_ok=True)
Path(krncbrandp).mkdir(parents=True, exist_ok=True)
Path(stockpath).mkdir(parents=True, exist_ok=True)

# Define Branding (Imaging) URL
brandurl = ("https://github.com/engineerjoe440/KRNCApps/blob/master/"+
            "common/branding/KrncBranding.zip?raw=true")


# Define Function to Update KRNC Branding from Web
def pull_new_krnc_branding_files():
    # Use Requests to Download the Imaging
    resp = requests.get( brandurl )
    filepath = krncbrandp+'tempBranding.zip'
    # Start Loading Bar
    self.loader = LoadingBar(   text="Fetching Files.",
                                width=300,
                                height=150,
                            )
    # Store Zipped File
    with open(filepath,'wb') as tempZip:
        tempZip.write(resp.content)
    # Extract Zipped Content
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(krncbrandp)
    # Delete Zipped Folder
    os.remove(filepath)
    time.sleep(2)
    # Kill Loading Bar
    self.loader.destroy()


# END