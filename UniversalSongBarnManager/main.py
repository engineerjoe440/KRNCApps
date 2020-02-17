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

# Prepare Path to Accept Common Imports
curdir = os.getcwd()
parentdir = '/'.join( curdir.split('\\')[:-1] )
sys.path.append(parentdir + '/common')

# Import Common Requirements
from tkinterroutines import Splash

# Import Local Requirements
from app import App


# Run System
mainApp = App()
time.sleep(1)
mainApp.run()


# END