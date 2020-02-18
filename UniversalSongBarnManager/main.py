"""
#######################################################################################
Universal Song Barn (USB) Manager System
(c) Stanley Solutions

By: Joe Stanley
#######################################################################################
"""

# Required Imports
import tkinter as tk
from PIL import Image, ImageTk
import time, os, sys
from pathlib import Path

# Prepare Path to Accept Common Imports
curdir = os.getcwd()
parentdir = '/'.join( curdir.split('\\')[:-1] )
sys.path.append(parentdir + '/common')

# Import Common Requirements
from tkinterroutines import Splash

# Import Local Requirements
from app import App

# Define Local Support File Path
stockpath = "C:/ProgramData/StanleySolutions/KRNC/USBManager/"
barnpath = "/KRNC/"

# Create Local Path if Nonexistant
Path(stockpath).mkdir(parents=True, exist_ok=True)

# Run System
mainApp = App()
time.sleep(3)
mainApp.run()


# END