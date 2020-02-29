"""
#######################################################################################
Universal Song Barn (USB) Manager System
(c) Stanley Solutions

By: Joe Stanley
#######################################################################################
"""
# Define Version Information
__version__ = 0.1
def version():
    msg  = "UniversalSongBarn Manager Version: {}".format(__version__)
    msg += "\nby Stanley Solutions"
    return(msg)

# Required Imports
import tkinter as tk
from lib.PIL import Image, ImageTk
import time, os, sys
from pathlib import Path

# Import Common Requirements
from lib.tkinterroutines import Splash

# Import Local Requirements
from app import App

# Identify Argument
barnfile = None
cmdargs = sys.argv
for arg in cmdargs:
    if arg.lower().endswith('.barn') :
        # Found Barn Description File
        barnfile = arg
        break

# Run System
mainApp = App()
# Barn Description File was Found
if barnfile != None:
    mainApp.open_barn(barnfile)
mainApp.set_about_callback(version)
time.sleep(3)
mainApp.run()


# END