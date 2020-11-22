"""
#######################################################################################
Universal Song Barn (USB) Manager - Tkinter App (powered by PySimpleGUI)
(c) Stanley Solutions - 2020

By: Joe Stanley
#######################################################################################
"""

# Collect Version
from KrncUsbManager import __version__

# Import Required Dependencies
import os, sys
import PySimpleGUI as sg
from tkinter.font import Font
from PIL import Image, ImageTk
from multiprocessing import Pool
from functools import partial
from importlib.util import spec_from_loader, module_from_spec
from importlib.machinery import SourceFileLoader

# Local Imports
from KrncUsbManager import app
from KrncUsbManager.common import *

# Identify Argument
barnfile = None
cmdargs = sys.argv
for arg in cmdargs:
    if arg.lower().endswith('.barn') :
        # Found Barn Description File
        barnfile = arg
        break

# Define Filter Import Function
def load_filter_driver(name,path=filterpath):
    # Load Module
    if not name.endswith('.filt'):
        name += '.filt'
    spec = spec_from_loader(name, SourceFileLoader(name, path+name))
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    # Return Module Handle
    return(mod)

# Define Filter Implimentation Function
def filter_audio(inputs):
    # Use `filtername` and `filterlist` to Determine Driver Script
    src,dst,filtername = inputs
    # Format src/dst File Paths
    src = repr(src).replace('\\','')
    dst = repr(dst).replace('\\','')
    # Dictionary Structure: {"filtername":<filter_driver>}
    filter_driver = load_filter_driver(filtername)
    # Run Filter
    sta = filter_driver.main(src,dst)

# Define Audio Loader
def audio_loader(audio_files,in_filterslist):
    dataset = []
    # Files List Structure: ["full/path/filename.mp3","filename.mp3"]
    for src,struct in audio_files.items():
        # Decompose Structure
        name = struct['name']
        dstpath = struct['destination']
        dst = dstpath + '/' + name
        filtername = struct['filter']
        # Generate Dataset List
        dataset.append([src,dst,filtername])
    # Iteratively Load Audio and Update Loading Bar
    loader = BlockLoadingBar(text="Filtering and Loading Files")
    step_size = int(min(80,100/len(audio_files.keys()))) # Determine Progress Bar Step
    # Wait for Progress Bar to Initialize
    while True:
        try:
            loader.setValue(step_size)
            break
        except:
            continue
    # Iteratively Filter and Load Audio onto Drive
    with Pool(5) as pool:
        for x in pool.imap_unordered(filter_audio,dataset):
            loader.setValue( loader.getValue() + step_size )
    loader.destroy() # Kill Loading Bar

# Define Pasture Zip Handler:
def pasture_zipper(driveName,zip_files,uzip_files):
    # Perform Operations Required to Zip Files for Pasture
    driveBarn = driveName+barnpath
    # Extract Songs from Pasture
    try:
        with zipfile.ZipFile(driveBarn+'/pasture.zip', 'r') as zipf:
            for file in uzip_files:
                extr_path = (barnpath+'/'+file)[1:]
                zipf.extract(extr_path,driveName)
    except:
        pass
    # Put songs out to Pasture by Zipping their Files
    try:
        with zipfile.ZipFile(driveBarn+'/pasture.zip', 'a') as zipf:
            for file in zip_files:
                zipf.write(  os.path.join(driveBarn,file),
                            compress_type=zipfile.ZIP_DEFLATED )
                os.remove( os.path.join(driveBarn,file) )
    except:
        pass

class application():
    def __init__(self):
        # Throw Splash Screen
        splash = app.SplashScreen()
        time.sleep(3)
        # Prepare Window and Defaults
        self.window = sg.Window(windowTitle, layout=app.window_layout,
            size=app.eval_app_size(splash.window_size()), resizable=True,
            icon=app.app_icon)
        splash.close()
        self.event = None
        self.values = None
    
    def open_barn(self):
        pass

    def close_barn(self):
        pass

    def save_barn(self):
        pass
    
    def run(self):
        # Read/Run Window
        self.event, self.values = self.window.read()
        print(self.event, self.values)
        # Quit When Needed
        if self.event == 'Quit':
            self.close()
        # Detect Closed Window
        elif self.event == None:
            sys.exit(0) # Close gracefully
        else:
            self.run() # Continue Running

    def close(self):
        # Verify Quit if user has selected 'Quit' from menu
        confirm = sg.popup_yes_no('Are you sure you want to quit?',
            title='Quit?', icon=app.app_icon)
        if confirm.lower() == 'no':
            self.run() # Cancel Close Operation
        self.window.close()
        sys.exit(0)

def main():
    # Main Function Entry Point
    # Create Application
    guiApp = application()
    # Barn Description File was Found
    if barnfile != None:
        guiApp.open_barn(barnfile)
    sta = guiApp.run()
    while sta:
        sta = guiApp.run()

if __name__ == "__main__":
    main()


# END