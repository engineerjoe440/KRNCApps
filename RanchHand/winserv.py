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
import win32con
import configparser
import traceback
import PySimpleGUIQt as sg
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

# Import Local Dependencies
#import vdjsettings

# Define Folder Locations
progFolder = 'C:\\Program Files (x86)\\StanleySolutions\\KRNC\\RanchHand\\'
dataFolder = 'C:\\ProgramData\\StanleySolutions\\KRNC\\RanchHand\\'

# Define File Locations
configfile  = dataFolder + 'config.ini'
iconfile    = progFolder + 'images\\KRNC.ico'
iconfileneg = progFolder + 'images\\KRNCnegative.ico'
configapp   = progFolder + 'RanchHand.exe'

# Load Default (dev) Icon if `iconfile` Doesn't Exist
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
    
    tray = sg.SystemTray(menu=menu_def, filename=iconfileneg)
    
    kill = False

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

#### Define Functions to Manage Files ####################################
    # Define Created Method
    def on_created(event):
        # Capture Source Path
        src = event.src_path
        # Identify Destination Path
        if self.LOCALFOLDER in src:
            dst = src.replace( self.LOCALFOLDER, self.REMOTEFOLDER )
        else:
            dst = src.replace( self.REMOTEFOLDER, self.LOCALFOLDER )
        # Perform File Management
        with open('C:\\Users\\Joe Stanley\\Desktop\\file.txt','w') as fob:
            fob.write('Created:\n')
            fob.write(src)
    
    # Define Deleted Method
    def on_deleted(event):
        # Capture Source Path
        src = event.src_path
        # Identify Destination Path
        if self.LOCALFOLDER in src:
            dst = src.replace( self.LOCALFOLDER, self.REMOTEFOLDER )
        else:
            dst = src.replace( self.REMOTEFOLDER, self.LOCALFOLDER )
        # Perform File Management
        with open('C:\\Users\\Joe Stanley\\Desktop\\file.txt','w') as fob:
            fob.write('Deleted:\n')
            fob.write(src)
    
    # Define Modified Method
    def on_modified(event):
        # Capture Source Path
        src = event.src_path
        # Identify Destination Path
        if self.LOCALFOLDER in src:
            dst = src.replace( self.LOCALFOLDER, self.REMOTEFOLDER )
        else:
            dst = src.replace( self.REMOTEFOLDER, self.LOCALFOLDER )
        # Perform File Management
        with open('C:\\Users\\Joe Stanley\\Desktop\\file.txt','w') as fob:
            fob.write('Modified:\n')
            fob.write(src)
    
    # Define Moved Method
    def on_moved(event):
        # Capture Source Path
        src = event.src_path
        # Identify Destination Path
        if self.LOCALFOLDER in src:
            dst = src.replace( self.LOCALFOLDER, self.REMOTEFOLDER )
        else:
            dst = src.replace( self.REMOTEFOLDER, self.LOCALFOLDER )
        # Perform File Management
        mvdst = event.dest_path
        with open('C:\\Users\\Joe Stanley\\Desktop\\file.txt','w') as fob:
            fob.write('Moved:\n')
            fob.write(src)
    
##########################################################################
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
        # Prepare Observer Settings
        patterns = '*'
        ignore_patterns = ''
        ignore_directories = False
        case_sensitive = True
        observe_recursive = True
        # Prepare Event Handlers
        self.local_event_handler = PatternMatchingEventHandler(
                                    patterns,
                                    ignore_patterns,
                                    ignore_directories,
                                    case_sensitive
                            )
        self.remote_event_handler = PatternMatchingEventHandler(
                                    patterns,
                                    ignore_patterns,
                                    ignore_directories,
                                    case_sensitive
                            )
        # Set Handler Functions
        self.local_event_handler.on_created = self.on_created
        self.local_event_handler.on_deleted = self.on_deleted
        self.local_event_handler.on_modified = self.on_modified
        self.local_event_handler.on_moved = self.on_moved
        self.remote_event_handler.on_created = self.on_created
        self.remote_event_handler.on_deleted = self.on_deleted
        self.remote_event_handler.on_modified = self.on_modified
        self.remote_event_handler.on_moved = self.on_moved
        # Prepare Observers
        self.local_observer = Observer()
        self.remote_observer = Observer()
        # Load Folder Descriptions
        self.LOCALFOLDER = config['RanchHand']['LocalSettings']
        self.REMOTEFOLDER = config['RanchHand']['OneDriveSettings']
        self.ONEDRIVEMX = config['RanchHand']['OneDriveMusic']
        print("Local Folder: {}".format(self.LOCALFOLDER))
        print("Remote Folder: {}".format(self.REMOTEFOLDER))
        # Build Directory Handles
        try:
            # Schedule Observers
            self.local_observer.schedule(   
                                            self.local_event_handler,
                                            self.LOCALFOLDER,
                                            recursive=observe_recursive
                                        )
            self.remote_observer.schedule(
                                            self.remote_event_handler,
                                            self.REMOTEFOLDER,
                                            recursive=observe_recursive
                                        )
            # Start Observers
            self.local_observer.start()
            self.remote_observer.start()
        except Exception as e:
            print("Failure!")
            print(e)
        print("Startup Successful.")
        self.isrunning = True

    def stop(self):
        '''
        Mark internal attribute to stop service
        '''
        self.kill = True
        self.isrunning = False
        self.local_observer.stop()
        self.remote_observer.stop()

##########################################################################
    def main(self):
        '''
        Main body method called when started
        '''
        try:
            while not self.kill:
                # Monitor System Tray
                menu_item = self.tray.read()
                print(menu_item)
                if menu_item == '__TIMEOUT__':
                    pass
                elif menu_item == 'Exit':
                    self.kill = True
                elif menu_item in ['Open','__ACTIVATED__']:
                    # Start Configuration App
                    try:
                        subprocess.call([configapp])
                    except:
                        print("Unable to start RanchManager App.")
                        sg.popup_error("Unable to start RanchManager App.",
                            icon=iconfile, background_color='#506c91')
        except Exception as e:
            print("An Error Occurred and Service Died.")
            print(e)
##########################################################################

# Service Routine Entry Point
if __name__ == '__main__':
    ConstructorService.parse_command_line()

# END