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
fggrey = '#506c91'
mainwidth = 1300
mainheight = 600
tablwidth = 1000
tablheight = mainheight - 5
drivheight = 100
barnheight = mainheight - drivheight
headers = [
    {'heading': 'File Name',        'width': 000,   'type': 'text'},
    {'heading': 'Audio Filter',     'width': 200,   'type': 'text'},
    {'heading': 'Pastured',         'width': 150,   'type': 'text'},
]
# Evaluate Width of File Name Column
headers[0]['width'] = tablwidth + 60 - sum([i['width'] for i in headers])

# Define Local Support File Path
utilpath = "C:/ProgramData/StanleySolutions/KRNC/USBManager/"
stockpath = "C:/Users/{}/Music/KRNC/USBManager/"
musicpath = "C:/Users/{}/Music/"
barnpath = "/KRNC/"
filterpath = utilpath + 'Filters/'
krncbrandp = utilpath + 'KRNCbranding/'

# Required Imports
import tkinter as tk
from tkinter.font import Font
from PIL import Image, ImageTk
import time, os, sys
from importlib.util import spec_from_loader, module_from_spec
from importlib.machinery import SourceFileLoader 
from pathlib import Path
from tkintertable import TableCanvas, TableModel

# Prepare Path to Accept Common Imports
curdir = os.getcwd()
parentdir = '/'.join( curdir.split('\\')[:-1] )
sys.path.append(parentdir + '/common')
imagedir = parentdir + '/common/images'

# Create Local Paths if Nonexistant
stockpath = stockpath.format(os.getlogin())
musicpath = musicpath.format(os.getlogin())
Path(filterpath).mkdir(parents=True, exist_ok=True)
Path(krncbrandp).mkdir(parents=True, exist_ok=True)
Path(stockpath).mkdir(parents=True, exist_ok=True)

# Import Common Requirements
from tkinterroutines import Splash, ScrollableFrame

# Define Filter Import Function
def load_filter_driver(name,path=filterpath):
    # Load Module
    spec = spec_from_loader(name, SourceFileLoader(name, path+name))
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    # Return Module Handle
    return(mod)

def donothing():
   x = 0

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
        
        # Class Variable Declaration
        self.barn = None
        self.krncbrand = tk.BooleanVar()
        self.filterVar = tk.StringVar()
        self.pasturVal = tk.StringVar()
        self.krncbrand.set(True)
        self.filterVar.set("-filter-")
        self.pasturVal.set("-pasture-")
        self.pasturOpt = ['FALSE','TRUE']
        # Find Filter Driver Files (Masked Python Files)
        self.audiofilters = {}
        for file in os.listdir(filterpath):
            if file.endswith('.filt'):
                # Import Module and Manage Handle
                handle = load_filter_driver(file)
                # Generate Look-Up-Dictionary
                self.audiofilters[file[:-5]] = handle

        # Prepare Main App Window
        self.title( "KRNC Universal Song Barn (USB) Manager"+
                    " - Your Music Lives Here.")
        self.configure(background=bgblue)
        self.geometry("{}x{}".format(mainwidth,mainheight))
        self.iconbitmap(imagedir+'/KRNC.ico')
        
        # Prepare Menu
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar,tearoff=0)
        self.barnmenu = tk.Menu(self.menubar,tearoff=0)
        self.aboutmenu = tk.Menu(self.menubar,tearoff=0)
        self.filemenu.add_command(  label="New Barn",  command=donothing,
                                    accelerator="Ctrl+N")
        self.filemenu.add_command(  label="Open Barn", command=self.open_barn,
                                    accelerator="Ctrl+O")
        self.filemenu.add_command(  label="Save Barn", command=self.save_barn,
                                    accelerator="Ctrl+S")
        self.filemenu.add_command(  label="Save Barn As", command=self.save_barn_as,
                                    accelerator="Ctrl+Shift+S")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit",command=self.quit,accelerator="Ctrl+Q")
        self.barnmenu.add_command( label="Add Song(s) to Barn",accelerator="Ctrl+A",
                                    command=self.add_songs)
        self.barnmenu.add_command( label="Empty Barn",command=self.empty_barn)
        self.barnmenu.add_separator()
        self.barnmenu.add_checkbutton( label="Enable KRNC Branding",
                                        command=donothing,var=self.krncbrand)
        self.barnmenu.add_separator()
        self.barnmenu.add_command(  label="Update KRNC Branding",
                                    command=donothing)
        self.aboutmenu.add_command(label="About...", command=self.popupmsg)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_cascade(label="Barn", menu=self.barnmenu)
        self.menubar.add_cascade(label="Help", menu=self.aboutmenu)
        self.config(menu=self.menubar)
        
        # Bind Keys
        self.bind_all("<Control-q>", self.quit)
        self.bind_all("<Control-o>", self.handle_open)
        self.bind_all("<Control-s>", self.handle_save)
        self.bind_all("<Control-S>", self.handle_save_as)
        self.bind_all("<Control-a>", self.handle_add)
        
        # Generate Table Section
        self.tablFrame = tk.Frame(self, bg=bgblue,width=tablwidth,height=tablheight)
        self.tablFrame.grid(row=0, column=1,sticky="nsew")
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.model = TableModel()
        self.table = TableCanvas(   self.tablFrame, model=self.model,cellbackgr=bglblue,
                                    rowselectedcolor=bgblue,rowheight=25,
                                    thefont=('Segoe UI',9),entrybackgr=bggrey,
                                    selectedcolor=bggrey,multipleselectioncolor=bglblue,
                                    icon=imagedir+'/KRNC.ico',)
        self.table.show()
        self.model.addRow()
        self.set_columns()
        
        # Generate Options Sections
        optsFrame = tk.Frame(self, bg=bgblue, height=tablheight)
        barnFrame = tk.Frame(optsFrame, bg=bgblue, height=barnheight)
        drivFrame = tk.Frame(optsFrame, bg=bggrey, height=drivheight)
        optsFrame.grid(row=0, column=2, sticky="nsew")
        optsFrame.columnconfigure(0, weight=1)
        optsFrame.rowconfigure(0, weight=6)
        optsFrame.rowconfigure(1, weight=1)
        barnFrame.grid(row=0, column=0, sticky="new")
        drivFrame.grid(row=1, column=0, sticky="nsew")
        
        # Generate Barn Frame Information and Controls
        barnTitle = tk.Label(barnFrame, text="Barn Tools", fg=fgblue, bg=bgblue,
                            font=self.pt11B)
        barnTitle.grid(row=0, column=0, pady=5, padx=50)
        self.filtermenu = tk.OptionMenu(barnFrame,self.filterVar,
                                        *self.audiofilters.keys())
        self.filtermenu.config( width=int((mainwidth-tablwidth)*0.060),
                                background=bglblue)
        self.filtermenu.grid(row=1, column=0, pady=5)
        self.pasturmenu = tk.OptionMenu(barnFrame,self.pasturVal,*self.pasturOpt)
        self.pasturmenu.config( width=int((mainwidth-tablwidth)*0.060),
                                background=bglblue)
        self.pasturmenu.grid(row=2, column=0, pady=5)
        
        # Generate Drive Frame Information
        drivTitle = tk.Label(drivFrame, text="Drive Tools", fg=fggrey, bg=bggrey,
                            font=self.pt11B)
        drivTitle.grid(row=0, column=0, pady=5, padx=50, columnspan=2)
        updtBtn = tk.Button(drivFrame, text="Call Home", bg=bglblue, command=donothing)
        sendBtn = tk.Button(drivFrame, text="Drive Out", bg=bglblue, command=donothing)
        updtBtn.grid(row=1, column=0, padx=5, pady=5)
        sendBtn.grid(row=1, column=1, padx=5, pady=5)
        
    def quit(self, event):
        sys.exit(0)
    
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
    
    def set_columns(self):
        # Format Columns as Necessary
        for c,column in enumerate(headers):
            name    = column['heading']
            ctype   = column['type']
            width   = column['width']
            self.model.addColumn(colname=name,coltype=ctype)
            self.table.resizeColumn(c,width)
            self.model.setValueAt('',0,c)
        self.table.redraw()
    
    # Define Handler Functions
    def handle_add(self,event):
        self.add_songs()
    def handle_open(self,event):
        self.open_barn()
    def handle_save(self,event):
        self.save_barn()
    def handle_save_as(self,event):
        self.save_barn_as()
    
    def update(self):
        # Capture Current Information
        curFilter = self.filterVar.get()
        curPastur = self.pasturVal.get()
        ROWi = self.table.getSelectedRow()
        filter = self.model.getValueAt(ROWi,1)
        pasture = self.model.getValueAt(ROWi,2)
        # Update Filter
        if (curFilter != "-filter-"):
            self.model.setValueAt(curFilter,ROWi,1)
            self.table.redraw()
        # Update Pasture
        if (curPastur!="-pasture-") and (pasture!=curPastur):
            self.model.setValueAt(curPastur,ROWi,2)
            self.table.redraw()
        # Set "After" Callback
        self.after(50,self.update)
    
    def add_songs(self,songlist=[]):
        # Prompt User to Add Songs
        if songlist == []:
            songlist = tk.filedialog.askopenfilenames(  parent=self,
                                                        initialdir=musicpath,
                                                        title="Add Stock to Barn",
                                                        filetypes=(
                                                            ("audio files",
                                                                ".mp3 .wav"),
                                                            ("all files","."),
                                                        ),
                                                        multiple=True,
                                                     )
        # Validate Dataset
        if songlist == []:
            return
        # Remove Dummy Row if No Barn Declared
        if (self.barn == None) and (self.model.getRowCount() == 1):
            self.model.deleteRows()
        # Add new Rows to Table
        filekwarg = headers[0]['heading']
        lockkwarg = headers[2]['heading']
        for song in songlist:
            self.table.addRow(key=None,**{filekwarg:song,lockkwarg:'false'})
    
    def empty_barn(self):
        # Clear Table by Deleting Rows
        self.model.deleteRows()
        self.model.addRow()
        self.set_columns()
    
    def new_barn(self):
        # Clear Barn
        self.empty_barn()
        # Remove Barn Reference
        self.barn = None
    
    def open_barn(self,barn=''):
        # Open *.barn Song List File
        # Test if passed as argument
        if barn != '':
            self.barn = barn
        else:
            self.barn = tk.filedialog.askopenfilename(  initialdir=stockpath,
                                                        title="Open Barn Roster",
                                                        filetypes=(
                                                            ("Song Barn",".barn"),
                                                            ("all files","."),
                                                        )
                                                     )
        # Validate Input
        if self.barn == '':
            return
        # Input is Valid, Load as CSV, then Reset Table
        self.table.importCSV(filename=self.barn)
        self.set_columns()
    
    def save_barn_as(self,barn=''):
        # Clear Stored Barn Name
        self.barn = None
        self.save_barn(barn=barn)
    
    def save_barn(self,barn=''):
        # Save Current Barn
        if barn != '':
            self.barn = barn
        elif self.barn == None:
            self.barn = tk.filedialog.asksaveasfilename(initialdir=stockpath,
                                                        title="Save Barn Roster",
                                                        filetypes=(
                                                            ("Song Barn",".barn"),
                                                            ("all files","."),
                                                        ),
                                                        defaultextension='.barn',
                                                        )
        # Validate Input
        if self.barn == '':
            return
        # Format with file extension
        if not self.barn.endswith('.barn'):
            self.barn += '.barn'
        # File Path is Valid, Store CSV!
        cellDict = self.model.getAllCells()
        with open(self.barn,'w') as outputfile:
            headerstring = ','.join([i['heading'] for i in headers])
            outputfile.write(headerstring+'\n')
            for rowList in cellDict.values():
                row = ','.join(rowList)     # Create CSV Row
                outputfile.write(row+'\n')  # Write to File
    
    def set_about_callback(self,callable,title="KRNC USB Manager Info",bg=bggrey,
                           button_txt="Close",height=100,width=300,*args,**kwargs):
        # Define Callback Methodology to Change The `About` Popup
        def callback():
            self.popupmsg(msg=callable(*args,**kwargs),bg=bg,height=height,
                          width=width,title=title,button_txt=button_txt)
        self.aboutmenu.entryconfig(0,label="About...",command=callback)
    
    def popupmsg(self,msg="--default--",title="KRNC USB Manager Info",
                 button_txt="Close",bg=bggrey,height=200,width=400):
        popup = tk.Tk()
        popup.wm_title(title)
        popup.configure(background=bg)
        popup.geometry("{}x{}".format(width,height))
        popup.iconbitmap(imagedir+'/KRNC.ico')
        label = tk.Label(popup, text=msg, font=self.pt11, bg=bg)
        label.pack(side="top", fill="x", pady=10)
        bFrame = tk.Frame(popup, bg=bg, pady=10)
        bFrame.pack(side="bottom")
        B1 = tk.Button(bFrame, text=button_txt, command = popup.destroy)
        B1.pack(side="bottom")
        popup.mainloop()
    
    def run(self):
        # Finished Loading, Destroy Splash, Display App
        self.splash.destroy()
        self.deiconify()
        self.center()
        # Run Main Loop
        self.after(50,self.update)
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