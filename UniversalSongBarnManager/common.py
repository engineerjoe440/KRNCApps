"""
#######################################################################################
Universal Song Barn (USB) Manager - Tkinter App (powered by PySimpleGUI)
(c) Stanley Solutions - 2020

By: Joe Stanley
#######################################################################################
"""

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
filterpath = utilpath + 'Filters/'
krncbrandp = utilpath + 'KRNCbranding/'

# Define Branding (Imaging) URL
brandurl = ("https://github.com/engineerjoe440/KRNCApps/blob/master/"+
            "common/branding/KrncBranding.zip?raw=true")


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



# END