"""
#######################################################################################
Ranch Hand - Windows Service
(c) Stanley Solutions

By: Joe Stanley
#######################################################################################
"""

# Import Standard Python Dependencies
import os
import socket
import subprocess
import win32serviceutil
import servicemanager
import win32event
import win32service
import win32file
import win32con
import configparser
import PySimpleGUIQt as sg

# Import Local Dependencies
import vdjsettings

# Define File Locations
configfile = 'C:\\ProgramData\\StanleySolutions\\KRNC\\RanchHand\\config.ini'
iconfile = 'C:\\Program Files (x86)\\StanleySolutions\\KRNC\\RanchHand\\images\\KRNCnegative.ico'
configapp = 'C:\\Program Files (x86)\\StanleySolutions\\KRNC\\RanchHand\\RanchHand.exe'

# Load Default Icon if `iconfile` Doesn't Exist
if not os.path.exists(iconfile):
    iconfile = ("D:\\Files\\Stanley Solutions\\KRNCApps\\RanchHand\\"+
                "images\\KRNCnegative.ico")

# Define Menu Options
menu_def = ['BLANK', ['Configuration', 'Exit']]

# Define Primary Windows Service Class
class ConstructorService(win32serviceutil.ServiceFramework):
    '''Base class to create winservice in Python'''

    _svc_name_ = 'RanchHand'
    _svc_display_name_ = 'KRNC Ranch Hand'
    _svc_description_ = 'VirtualDJ Settings Sharing Manager - by StanleySolutions'
    
    tray = sg.SystemTray(menu=menu_def, filename=iconfile)
    
    ACTIONS = {
      1 : "Created",
      2 : "Deleted",
      3 : "Updated",
      4 : "Renamed",
      5 : "Renamed"
    }
    FILE_LIST_DIRECTORY = 0x0001

    @classmethod
    def parse_command_line(cls):
        '''
        ClassMethod to parse the command line
        '''
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        '''
        Constructor of the winservice
        '''
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        '''
        Called when the service is asked to stop
        '''
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        '''
        Called when the service is asked to start
        '''
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def start(self):
        '''
        Mark internal attribute to allow start of service
        '''
        # Read Configuration File
        config = configparser.ConfigParser()
        config.read(configfile)
        # Test for Invalid Config File
        if not config.sections():
            self.kill = True
        # Load Folder Descriptions
        self.LOCALFOLDER = config['RanchHand']['LocalSettings']
        self.REMOTEFOLDER = config['RanchHand']['OneDriveSettings']
        self.ONEDRIVEMX = config['RanchHand']['OneDriveMusic']
        # Build Directory Handles
        self._localDirHandle = win32file.CreateFile (
          self.LOCALFOLDER,
          FILE_LIST_DIRECTORY,
          win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
          None,
          win32con.OPEN_EXISTING,
          win32con.FILE_FLAG_BACKUP_SEMANTICS,
          None
        )
        self._remoteDirHandle = win32file.CreateFile (
          self.REMOTEFOLDER,
          FILE_LIST_DIRECTORY,
          win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
          None,
          win32con.OPEN_EXISTING,
          win32con.FILE_FLAG_BACKUP_SEMANTICS,
          None
        )

    def stop(self):
        '''
        Mark internal attribute to stop service
        '''
        self.kill = True

    def main(self):
        '''
        Main body method called when started
        '''
##########################################################################
        while not self.kill:
            # Monitor System Tray
            menu_item = self.tray.read()
            print(menu_item)
            if menu_item == 'Exit':
                self.kill = True
            elif menu_item in ['Open','__ACTIVATED__']:
                # Start Configuration App
                subprocess.call([configapp])
            # Manage File Moves from Local to Remote
            ##############################################################
            # Monitor Directory Every Scan
            results = win32file.ReadDirectoryChangesW (
                self._localDirHandle,
                1024,
                True,
                win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                 win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                 win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                 win32con.FILE_NOTIFY_CHANGE_SIZE |
                 win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                 win32con.FILE_NOTIFY_CHANGE_SECURITY,
                None,
                None
            )
            # Iterate Over Results to Perform Necessary Actions
            for action, file in results:
                full_filename = os.path.join(self.MONFOLDER, file)
                print(full_filename, self.ACTIONS.get(action, "Unknown"))
##########################################################################
            # Manage File Moves from Remote to Local
            ##############################################################
            # Monitor Directory Every Scan
            results = win32file.ReadDirectoryChangesW (
                self._remoteDirHandle,
                1024,
                True,
                win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                 win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                 win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                 win32con.FILE_NOTIFY_CHANGE_SIZE |
                 win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                 win32con.FILE_NOTIFY_CHANGE_SECURITY,
                None,
                None
            )
            # Iterate Over Results to Perform Necessary Actions
            for action, file in results:
                full_filename = os.path.join(self.MONFOLDER, file)
                print(full_filename, self.ACTIONS.get(action, "Unknown"))
##########################################################################

# Service Routine Entry Point
if __name__ == '__main__':
    ConstructorService.parse_command_line()

# END