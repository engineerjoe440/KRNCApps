"""
#######################################################################################
Universal Song Barn (USB) Manager - Tkinter App (powered by PySimpleGUI)
(c) Stanley Solutions - 2020

By: Joe Stanley
#######################################################################################
"""

# Import Requisites
import win32com.client as win32com
from ctypes import windll, WINFUNCTYPE, c_wchar_p, c_int, c_void_p


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