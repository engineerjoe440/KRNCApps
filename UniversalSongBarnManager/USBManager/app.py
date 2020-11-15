"""
#######################################################################################
Universal Song Barn (USB) Manager - Tkinter App (powered by PySimpleGUI)
(c) Stanley Solutions - 2020

By: Joe Stanley
#######################################################################################
"""

# Collect Version
try:
    from .__init__ import __version__
    from .common import *
    from .images import krnc_splash_b64, icon_b, icon_w
except ImportError:
    from __init__ import __version__
    from common import *
    from images import krnc_splash_b64, icon_b, icon_w

# Import Required Dependencies
import os, sys
import PySimpleGUI as sg
from tkinter.font import Font
from PIL import Image, ImageTk

# Define Splash Screen
class SplashScreen():
    def __init__(self, w=250, h=200):
        # Define Layout to be an Image Over Text
        splash_layout = [[
            sg.Column([
                [sg.Image(data=krnc_splash_b64)],
                [sg.Column([
                [
                    sg.Text(''),
                    sg.Text(splashText,text_color='white', justification='center'),
                    sg.Text('')
                ]
                ], justification='center')]
            ], vertical_alignment='center', justification='center',  k='-C-')
        ]]
        # Create Window
        self.window = sg.Window(windowTitle, layout=splash_layout,
            size=(w,h), no_titlebar=True, resizable=True, finalize=True)
        # Apply Centering
        self.window['-C-'].expand(True, True, True)
    
    def window_size(self):
        return self.window.get_screen_size()
    
    def close(self):
        self.window.close()

# Define Simple Function To Evaluate Gui App Size Tuple
def eval_app_size(screen_dims):
    w = int( mainwidth/100 * screen_dims[0] )
    h = int( mainheight/100 * screen_dims[1] )
    return (w,h)

# Define Menu Layout
menubar_layout = [
    ['File', ['&Save Barn', '&Open Barn', 'Close Barn', '&New Barn', '---',
        'Saddle Bag', ['Choose Bag', 'Remove Bag'], '---', '&Quit']],
    ['View', ['Theme', [sg.theme_list()]]],
    ['Help', ['View Web Docs']]
]

# Define Table Column
table_layout = [
    [sg.Table([['', '', '']], headings=['File', 'Filter', 'Pastured'],)]
]

# Define Controls
control_layout = [
    [sg.Text('something')]
]

# Define Primary Window Layout
window_layout = [
    [sg.MenuBar(menubar_layout)],
    [sg.Column(table_layout), sg.Column(control_layout)]
]

# END