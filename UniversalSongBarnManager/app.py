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

# Required Imports
import tkinter as tk
from tkinter.font import Font
from PIL import Image, ImageTk
import time, os, sys
from tabulate import tabulate

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
        self.consolas11 = Font(family="Consolas", size=11)
        self.consolas11B = Font(family="Consolas", size=11, weight='bold')

        # Prepare Main App Window
        self.title("KRNC Universal Song Barn (USB) Manager")
        self.configure(background=bgblue)
        self.geometry("{}x{}".format(mainwidth,mainheight))
        self.iconbitmap(imagedir+'/KRNC.ico')
        
        # Generate Table Section
        self.tablFrame = ScrollableFrame(   self,width=tablwidth,
                                            height=tablheight,bg=bglblue)
        self.tablFrame.grid(row=0, column=1)
        #self.fill_table()
        
        # Generate Options Section
        optsFrame = tk.Frame(self, bg=bgblue)
        optsFrame.grid(row=0, column=2)
        optTitle = tk.Label(optsFrame, text="File Parameters", fg=fgblue, bg=bgblue)
        optTitle.grid(row=1, column=0, pady=5,padx=50)
    
    def run(self):
        # Finished Loading, Destroy Splash, Display App
        self.splash.destroy()
        self.deiconify()
        # Run Main Loop
        self.mainloop()
    
    def fill_table(self,datarows,headers=()):
        # Format and Validate Data and Headers
        tablerows = tabulate(datarows,headers,tablefmt="plain",stralign='right')
        tablerows = tablerows.split('\n')
        if len(headers) > 0:
            row = tablerows[0]
            tk.Label(   self.tablFrame.scrollable_frame, text=row,
                        font=self.consolas11B, bg=bgblue, fg=fgblue ).pack()
            tablerows = tablerows[1:]
        for i,row in enumerate(tablerows):
            if (i%2) == 1:
                bg = bggrey
                fg = fggrey
            else:
                bg = bglblue
                fg = fglblue
            tk.Label(   self.tablFrame.scrollable_frame, text=row,
                        font=self.consolas11, bg=bg, fg=fg ).pack()

if __name__ == "__main__":
    import time
    data = [[ "Joe", "Stanley"],
            [ "FOO", "Bar"],
            [ "Stanley","Solutions"],
            [ "Another","Test"],
            [ "Joe", "Stanley"],
            [ "JoeJoeJoeJoeJoe", "StanleyStanleyStanleyStanley"],]
    app = App()
    app.fill_table(data,["TEST","DATA"])
    time.sleep(2)
    app.run()
# END