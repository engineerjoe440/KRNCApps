"""
#######################################################################################
Universal Song Barn (USB) Manager - Tkinter App
(c) Stanley Solutions

By: Joe Stanley
#######################################################################################
"""

# Generic Defenitions
bgblue = '#506c91'
fgblue = 'white'
bglblue = '#bdc7e5'
fglblue = 'black'
bggrey = '#c9cdd9'
fggrey = 'black'
mainwidth = 1300
mainheight = 600
tablwidth = 1000
tablheight = mainheight - 5
headers = [
    {'heading': 'File Name',        'width': 000,   'type': 'text'},
    {'heading': 'Audio Filter',     'width': 150,   'type': 'text'},
    {'heading': 'Title',            'width': 200,   'type': 'text'},
    {'heading': 'Artist',           'width': 200,   'type': 'text'},
]
# Evaluate Width of File Name Column
headers[0]['width'] = tablwidth - sum([i['width'] for i in headers]) + 51

# Required Imports
import tkinter as tk
from tkinter.font import Font
from PIL import Image, ImageTk
import time, os, sys
from tabulate import tabulate
from tkintertable import TableCanvas, TableModel

# Prepare Path to Accept Common Imports
curdir = os.getcwd()
parentdir = '/'.join( curdir.split('\\')[:-1] )
sys.path.append(parentdir + '/common')
imagedir = parentdir + '/common/images'

# Import Common Requirements
from tkinterroutines import Splash, ScrollableFrame


class App(tk.Tk):
    def __init__(self):
        # Initialize App, then Withdraw while loading
        tk.Tk.__init__(self)
        self.withdraw()
        self.splash = Splash(   self,
                                text="Welcome Home",
                                width=300,
                                image=imagedir+"/KRNCnegative.png")
        
        # Define Fonts
        self.pt11 = Font(size=11)
        self.pt11B = Font(size=11, weight='bold')

        # Prepare Main App Window
        self.title("KRNC Universal Song Barn (USB) Manager")
        self.configure(background=bgblue)
        self.geometry("{}x{}".format(mainwidth,mainheight))
        self.iconbitmap(imagedir+'/KRNC.ico')
        
        # Generate Table Section
        self.tablFrame = tk.Frame(self, bg=bgblue,width=tablwidth,height=tablheight)
        self.tablFrame.grid(row=0, column=1,sticky="nsew")
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.model = TableModel()
        self.table = TableCanvas(   self.tablFrame, model=self.model,cellbackgr=bglblue,
                                    rowselectedcolor=bgblue,rowheight=25,
                                    thefont=('Segoe UI',9),entrybackgr=bggrey,
                                    selectedcolor=bggrey,multipleselectioncolor=bglblue,)
        self.table.show()
        self.model.addRow()
        for c,column in enumerate(headers):
            name    = column['heading']
            ctype   = column['type']
            width   = column['width']
            self.model.addColumn(colname=name,coltype=ctype)
            self.table.resizeColumn(c,width)
            self.model.setValueAt('',0,c)
        self.table.redraw()
        
        # Generate Options Section
        optsFrame = tk.Frame(self, bg=bgblue)
        optsFrame.grid(row=0, column=2)
        optTitle = tk.Label(optsFrame, text="Barn Options", fg=fgblue, bg=bgblue,
                            font=self.pt11B)
        optTitle.grid(row=1, column=0, pady=5,padx=50)
    
    def center(self):
        # Center Window on Screen
        self.update_idletasks()
        width = self.winfo_width()
        frm_width = self.winfo_rootx() - self.winfo_x()
        self_width = width + 2 * frm_width
        height = self.winfo_height()
        titlebar_height = self.winfo_rooty() - self.winfo_y()
        self_height = height + titlebar_height + frm_width
        x = self.winfo_screenwidth() // 2 - self_width // 2
        y = self.winfo_screenheight() // 2 - self_height // 2
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.deiconify()
    
    def run(self):
        # Finished Loading, Destroy Splash, Display App
        self.splash.destroy()
        self.deiconify()
        self.center()
        # Run Main Loop
        self.mainloop()

if __name__ == "__main__":
    import time
    data = [[ "Joe", "Stanley"],
            [ "FOO", "Bar"],
            [ "Stanley","Solutions"],
            [ "Another","Test"],
            [ "Joe", "Stanley"],
            [ "JoeJoeJoeJoeJoe", "StanleyStanleyStanleyStanley"],]
    app = App()
    time.sleep(2)
    app.run()
# END