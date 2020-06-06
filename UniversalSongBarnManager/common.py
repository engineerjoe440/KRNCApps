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
import win32com.client as win32com
import requests, zipfile, threading
from ctypes import windll, WINFUNCTYPE, c_wchar_p, c_int, c_void_p

# Generic Defenitions
bgblue = '#506c91'
fgblue = 'white'
bglblue = '#bdc7e5'
fglblue = 'black'
bggrey = '#c9cdd9'
fggrey = '#506c91'
mainwidth = 1300
mainheight = 600
tablwidth = 1000
tablheight = mainheight - 5
drivheight = 100
barnheight = mainheight - drivheight
headers = [
    {'heading': 'File Name',        'width': 000,   'type': 'text'},
    {'heading': 'Audio Filter',     'width': 200,   'type': 'text'},
    {'heading': 'Pastured',         'width': 150,   'type': 'text'},
]
# Evaluate Width of File Name Column
headers[0]['width'] = tablwidth + 60 - sum([i['width'] for i in headers])

# Define Local Support File Path
utilpath   = "C:/ProgramData/StanleySolutions/KRNC/USBManager/"
stockpath  = "C:/Users/{}/Music/KRNC/USBManager/"
musicpath  = "C:/Users/{}/Music/"
barnpath   = "/KRNC"
brndpath   = "/BRAND"
imagedir   = 'images'
drivedsc   = "krncdrive.barn"
filterpath = os.path.join(utilpath, 'Filters/')
krncbrandp = os.path.join(utilpath, 'KRNCbranding/')

# Define Branding (Imaging) URL
brandurl = ("https://github.com/engineerjoe440/KRNCApps/blob/master/"+
            "common/branding/KrncBranding.zip?raw=true")


# Define Function to Update KRNC Branding from Web
def update_branding():
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

# Define Function to Scan for Available Drives
def scanDrives():
    # Find Available Drives and Names
    strComputer = "." 
    objWMIService = win32com.Dispatch("WbemScripting.SWbemLocator")
    objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
    colItems = objSWbemServices.ExecQuery("Select * from Win32_LogicalDisk")
    # Iteratively Identify Drive Number and Label
    availDrives = {}
    driveVal = '-usb-drive-'
    for objItem in colItems:
        drvName = objItem.Name
        volName = objItem.VolumeName
        drvDesc = objItem.Description
        # Validate Drive as Potential USB
        if (drvName != 'C:') and (drvDesc.find('CD') == -1):
            drvStr = str(drvName) + '  ' + str(volName)
            availDrives[drvStr] = drvName
            if volName == 'KRNC':
                driveVal = drvStr
    return( driveVal, availDrives )

# Define Function to Format a Drive
def formatDrive(curDrive):
    # Define Callback Function
    def fmtCallback(command, modifier, arg):
        return(1)
    # Start Format
    fm = windll.LoadLibrary('fmifs.dll')
    FMT_CB_FUNC = WINFUNCTYPE(c_int, c_int, c_int, c_void_p)
    FMIFS_UNKNOWN = 0
    fm.FormatEx(c_wchar_p(curDrive), FMIFS_UNKNOWN, c_wchar_p(frmt),
                c_wchar_p(name), True, c_int(0), FMT_CB_FUNC(fmtCallback))
    # Re-Scan Drives
    driveVal, availDrives = scanDrives()
    try:
        # Create KRNC Music Folder and Branding (Imaging) Path
        Path( curDrive + barnpath ).mkdir(parents=True, exist_ok=True)
        Path( curDrive + brndpath ).mkdir(parents=True, exist_ok=True)
        # Generate USBarn File
        with open(curDrive+'/'+drivedsc,'w') as t_file:
            headerstring = ','.join([i['heading'] for i in headers])
            t_file.write(headerstring+'\n,,\n')
        # Notify Success
        self.popupmsg(  "Drive Format Complete",title='KRNC',
                        button_txt="OK",height=150,width=220)
    except:
        pass
    finally:
        # Re-Scan One More Time
        driveVal, availDrives = scanDrives()
    return( driveVal, availDrives )



# END