"""
#######################################################################################
Universal Song Barn (USB) Manager - Tkinter App (powered by PySimpleGUI)
(c) Stanley Solutions - 2020

By: Joe Stanley
#######################################################################################
"""

# Collect Version
from KrncUsbManager import __version__
from KrncUsbManager.common import *
from KrncUsbManager.images import krnc_splash_b64
from KrncUsbManager.images import icon_b_ico, icon_b_png
from KrncUsbManager.images import icon_w_ico, icon_w_png

# Import Required Dependencies
import os, sys
import PySimpleGUI as sg
from tkinter.font import Font
from PIL import Image, ImageTk

# Set App Icon for Different OS
if os_platform(check_win=True):
    app_icon = icon_b_ico # Windows - Default Light
else:
    app_icon = icon_w_png # Linux

# Define Common Font References
cntl_head_font = ('Bold', 12)

# Define Splash Screen
class SplashScreen():
    def __init__(self, w=275, h=225):
        # Define Layout to be an Image Over Text
        splash_layout = [[
            sg.Column([
                [sg.Image(data=krnc_splash_b64)],
                [sg.Column([
                [
                    sg.Text(''),
                    sg.Text(splashText, text_color='white', justification='center'),
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
    ['Help', ['View Web Docs', 'View License Information']]
]

# Define Table Column
table_layout = [
    [sg.Table([['', '', '']], headings=['File', 'Filter', 'Pastured'],
        size=(tablwidth,tablheight), col_widths=[col1width, col2width, col3width],
        auto_size_columns=False, header_font=table_head_font)]
]

# Define Controls
control_layout = [
    [sg.Text('Filter Selection:', font=cntl_head_font)],
    [sg.Combo(list(available_filters.keys()), size=(cntlwidth, cntl_obj_height),
        readonly=True, key='-filter-select-')],

    [sg.Text('')],
    [sg.Checkbox(' Pastured File', font=cntl_head_font)],

    [sg.Text('\n' + '_'*30 + '\n')], # Horizontal Rule

    [sg.Button('Load Drive',size=(cntlwidth, cntl_obj_height // 7),
        font=('Bold', 14), key='-load-drive-')],
    [sg.ProgressBar(100, size=(cntlwidth, cntl_obj_height), visible=False, key='-progress-')],
    [sg.Text('', key='-status-text-')]
]

# Define Primary Window Layout
window_layout = [
    [sg.MenuBar(menubar_layout)],
    [sg.Column(table_layout), sg.Column(control_layout)]
]

# END