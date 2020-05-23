"""
#######################################################################################
Ranch Hand - Windows Service
(c) Stanley Solutions

By: Joe Stanley
#######################################################################################
"""

# Describe Version
__version__ = "0.1"

def get_version():
    return(__version__)

# Describe Service Info
__svc_name__ = 'RanchHand'
__svc_display_name__ = 'KRNC Ranch Hand'
__svc_description__ = 'VirtualDJ Settings Sharing Manager - by StanleySolutions'

def get_service_info():
    return({
        'name'  : __svc_name__,
        'disp'  : __svc_display_name__,
        'desc'  : __svc_description__
    })


# Define Service State Lookup
serviceState = {
    1 : 'stopped',
    2 : 'start-pending',
    3 : 'stop-pending',
    4 : 'running',
    5 : 'continue-pending',
    6 : 'pause-pending',
    7 : 'paused',
}

def look_up_state( enum_state ):
    return( serviceState[ enum_state ] )


# Import Standard Python Dependencies
import os, sys
import re
import psutil
import socket
import subprocess
import win32serviceutil
import win32timezone
import servicemanager
import win32event
import win32service
import win32con
import configparser
import traceback
from logging.handlers import TimedRotatingFileHandler
import logging
import PySimpleGUIQt as sg
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

# Import Local Dependencies
import vdjsettings as vdj

# Define Folder Locations
progFolder = 'C:\\Program Files (x86)\\StanleySolutions\\KRNC\\RanchHand\\'
dataFolder = 'C:\\ProgramData\\StanleySolutions\\KRNC\\RanchHand\\'

# Define File Locations
configfile  = dataFolder + 'config.ini'
iconfile    = progFolder.replace('\\KRNC\\RanchHand\\','KRNC.ico')
iconfileneg = progFolder.replace('\\KRNC\\RanchHand\\','KRNCnegative.ico')
configapp   = progFolder + 'RanchHand.exe'

# Load Default (dev) Icon if `iconfile` Doesn't Exist
if not os.path.exists(iconfile):
    iconfile = ("D:\\Files\\Stanley Solutions\\KRNCApps\\RanchHand\\"+
                "images\\KRNCnegative.ico")

# Define Menu Options
menu_def = ['BLANK', ['Configuration', 'Exit']]

# Start Log if Main
if __name__ == '__main__':
    log_file_path = dataFolder + "service.log"
    logging.basicConfig(
        handlers=[logging.handlers.RotatingFileHandler(
            log_file_path,
            maxBytes=100000,
            backupCount=10
        )],
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s %(message)s'
    )
    logger = logging.getLogger("RanchHandLogger")
    logger.setLevel(logging.DEBUG)
    logger.info("RanchHandService")

# Define Kill Process Function
def kill_proc():
    """ Simple method to kill this process """
    proc = subprocess.Popen('sc queryex {}'.format(__svc_name__),
        stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
    stdout,stderr = proc.communicate()
    # Find PID from STDOUT
    criteria = re.compile(r'PID *: (\d{2,8})')
    try:
        PID = re.findall(criteria, stdout.decode('utf-8'))[0]
        print("Killing RanchHand service with PID: {}".format(PID))
        # Kill PID
        p = psutil.Process( int(PID) )
        p.kill()
    except:
        print("Process Not Running.")
        sys.exit(1)

# Define Primary Windows Service Class
class ConstructorService(win32serviceutil.ServiceFramework):
    '''Base class to create winservice in Python'''

    _svc_name_ = __svc_name__
    _svc_display_name_ = __svc_display_name__
    _svc_description_ = __svc_description__
    
    tray = sg.SystemTray(menu=menu_def, filename=iconfileneg)
    
    ignore_created = []
    ignore_modified = []
    ignore_deleted = []
    ignore_moved = []
    
    kill = False

    @classmethod
    def parse_command_line(cls):
        '''
        ClassMethod to parse the command line
        '''
        logger.info(sys.argv)
        if not 'debug' in sys.argv:
            sys.frozen = 'windows_exe' # Fake py2exe so we can debug
        if (len(sys.argv) == 1):
            logger.info("Bootstrapping Service Start")
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(cls)
            servicemanager.StartServiceCtrlDispatcher()
        else:
            win32serviceutil.HandleCommandLine(cls)
        logger.info("Parsing Command Line Arguments...")

    def __init__(self, args):
        '''
        Constructor of the winservice
        '''
        self.logger = logger
        self.logger.info("attempting to enter __init__...")
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(30)
        self.logger.info("Entered Class __init__")

    def SvcStop(self):
        '''
        Called when the service is asked to stop
        '''
        self.logger.info("RanchHand Service Run Stop.")
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        kill_proc()
        sys.exit(1)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        '''
        Called when the service is asked to start
        '''
        self.logger.info("RanchHand Service Run Start.")
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

#### Define Functions to Manage Files ####################################
    # Define Created Method
    def on_created(self, event):
        # Capture Source Path
        src = event.src_path.replace('\\','/')
        if src in self.ignore_created:
            return
        else:
            try:
                self.ignore_created.remove(src)
            except:
                pass
        print('New File Created:',src)
        # Identify Destination Path
        if self.LOCALFOLDER in src:
            dst = src.replace( self.LOCALFOLDER, self.REMOTEFOLDER )
            srcstr = self.LOCALFOLDER
            mxsrc  = self.ONEDRIVEMX
            dststr = vdj.generic_path
            mxdst  = vdj.generic_mx_path
        else:
            dst = src.replace( self.REMOTEFOLDER, self.LOCALFOLDER )
            srcstr = vdj.generic_path
            mxsrc  = vdj.generic_mx_path
            dststr = self.LOCALFOLDER
            mxdst  = self.ONEDRIVEMX
        # Set Ignore Operator
        self.ignore_created.append(dst)
        # Perform File Management
        self.logger.info(f'Created: {src}')
        vdj.modify_move_file(
            srcfpath=src, dstfpath=dst,
            srcstring=srcstr, dststring=dststr,
            mxsrcstring=mxsrc, mxdststring=mxdst,
        )
    
    # Define Deleted Method
    def on_deleted(self, event):
        # Capture Source Path
        src = event.src_path.replace('\\','/')
        if src in self.ignore_deleted:
            return
        else:
            try:
                self.ignore_deleted.remove(src)
            except:
                pass
        print('Existing File Deleted:',src)
        # Identify Destination Path
        if self.LOCALFOLDER in src:
            return # Don't Delete from One Drive
        else:
            dst = src.replace( self.REMOTEFOLDER, self.LOCALFOLDER )
        # Set Ignore Operator
        self.ignore_deleted.append(dst)
        # Perform File Management
        self.logger.info(f'Deleted: {src}')
        try:
            os.remove(dst)
        except:
            self.logger.warning("A file was deleted in {} that "+
                "could not be deleted in {}.".format(src,dst))
    
    # Define Modified Method
    def on_modified(self, event):
        # Capture Source Path
        src = event.src_path.replace('\\','/')
        if src in self.ignore_modified:
            return
        else:
            try:
                self.ignore_modified.remove(src)
            except:
                pass
        print('Existing File Modified:',src)
        # Identify Destination Path
        if self.LOCALFOLDER in src:
            dst = src.replace( self.LOCALFOLDER, self.REMOTEFOLDER )
            srcstr = self.LOCALFOLDER
            mxsrc  = self.ONEDRIVEMX
            dststr = vdj.generic_path
            mxdst  = vdj.generic_mx_path
        else:
            dst = src.replace( self.REMOTEFOLDER, self.LOCALFOLDER )
            srcstr = vdj.generic_path
            mxsrc  = vdj.generic_mx_path
            dststr = self.LOCALFOLDER
            mxdst  = self.ONEDRIVEMX
        # Set Ignore Operator
        self.ignore_modified.append(dst)
        # Perform File Management
        self.logger.info(f'Modified: {src}')
        vdj.modify_move_file(
            srcfpath=src, dstfpath=dst,
            srcstring=srcstr, dststring=dststr,
            mxsrcstring=mxsrc, mxdststring=mxdst,
        )
    
    # Define Moved Method
    def on_moved(self, event):
        # Capture Source Path
        src = event.src_path.replace('\\','/')
        mvdst = event.dest_path.replace('\\','/')
        if src in self.ignore_moved:
            return
        else:
            try:
                self.ignore_moved.remove(src)
            except:
                pass
        print('Existing File Moved:',src)
        # Identify Destination Path
        if self.LOCALFOLDER in src:
            dst = src.replace( self.LOCALFOLDER, self.REMOTEFOLDER )
            if self.REMOTEFOLDER in mvdst:
                print('Moved to Supported Folder.')
            else:
                print('Moved out of RanchHand Management Scope')
        else:
            dst = src.replace( self.REMOTEFOLDER, self.LOCALFOLDER )
        # Perform File Management
        self.logger.info(f'Moved: {src} to {mvdst}')
    
##########################################################################
    def start(self):
        '''
        Mark internal attribute to allow start of service
        '''
        self.logger.info("Internal Start Method.")
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
        self.LOCALFOLDER = config['RanchHand']['LocalSettings'].replace('\\','/')
        self.REMOTEFOLDER = config['RanchHand']['OneDriveSettings'].replace('\\','/')
        self.ONEDRIVEMX = config['RanchHand']['OneDriveMusic'].replace('\\','/')
        print("Local Folder: {}".format(self.LOCALFOLDER))
        self.logger.info(f'Local VDJ Folder: {self.LOCALFOLDER}')
        print("Remote Folder: {}".format(self.REMOTEFOLDER))
        self.logger.info(f'Remote VDJ Folder: {self.REMOTEFOLDER}')
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
            logger.error("Failed to start!")
            print(e)
        print("Startup Successful.")
        self.logger.info("Startup Successfull")
        self.isrunning = True

    def stop(self):
        '''
        Mark internal attribute to stop service
        '''
        self.logger.info("Internal Stop Method.")
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
            self.logger.info("Internal `main` Method.")
            while not self.kill:
                # Monitor System Tray
                menu_item = self.tray.read()
                if menu_item in [None, '__TIMEOUT__']:
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
    if 'kill' in sys.argv:
        kill_proc()
        logger.info("Killing service")
        sys.exit(0)
    logger.info("Calling Argument Parsing Operation")
    ConstructorService.parse_command_line()

# END