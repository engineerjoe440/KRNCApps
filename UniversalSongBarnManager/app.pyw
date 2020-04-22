"""
#######################################################################################
Universal Song Barn (USB) Manager - Tkinter App
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
barnpath = "/KRNC"
brndpath = "/BRAND"
drivedsc = "krncdrive.barn"
filterpath = utilpath + 'Filters/'
krncbrandp = utilpath + 'KRNCbranding/'

# Define Branding (Imaging) URL
brandurl =  ("https://github.com/engineerjoe440/KRNCApps/blob/master/"+
            "common/branding/KrncBranding.zip?raw=true")

# Required Imports
import tkinter as tk
from tkinter.font import Font
from lib.PIL import Image, ImageTk
import time, os, sys
import lib.requests, zipfile, threading
from multiprocessing import Pool
from functools import partial
from importlib.util import spec_from_loader, module_from_spec
from importlib.machinery import SourceFileLoader
import lib.win32com.client as win32com
from ctypes import windll, WINFUNCTYPE, c_wchar_p, c_int, c_void_p
from pathlib import Path
import requests

# Define Image Path
imagedir = 'images'

# Create Local Paths if Nonexistant
stockpath = stockpath.format(os.getlogin())
musicpath = musicpath.format(os.getlogin())
Path(filterpath).mkdir(parents=True, exist_ok=True)
Path(krncbrandp).mkdir(parents=True, exist_ok=True)
Path(stockpath).mkdir(parents=True, exist_ok=True)

# Import Common Requirements
from lib.tkinterroutines import Splash, LoadingBar, BlockLoadingBar, TableDialog
from lib.tkintertable import TableCanvas, TableModel

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

class App(tk.Tk):
    def __init__(self):
        # Initialize App, then Withdraw while loading
        tk.Tk.__init__(self)
        self.withdraw()
        self.logo = imagedir+"/KRNCnegative.png"
        self.icon = imagedir+'/KRNC.ico'
        self.splash = Splash(   self,
                                text="Welcome Home",
                                width=300,
                                image=self.logo)
        
        # Define Fonts
        self.pt11 = Font(size=11)
        self.pt11B = Font(size=11, weight='bold')
        self.pt16B = Font(size=16, weight='bold')
        
        # Class Variable Declaration
        self.barn = None
        self.lastRow = 0
        self.musicpath = musicpath
        self.blockupdate = False
        self.krncbrand = tk.BooleanVar()
        self.filterVar = tk.StringVar()
        self.pasturVal = tk.StringVar()
        self.driveVal = tk.StringVar()
        self.brandVal = tk.StringVar()
        self.krncbrand.set(True)
        self.filterVar.set("-filter-")
        self.pasturVal.set("-pasture-")
        self.driveVal.set("-usb-drive-")
        self.brandVal.set("StandardCar")
        self.pasturOpt = ['FALSE','TRUE']
        # Find Filter Driver Files (Masked Python Files)
        self.audiofilters = {}
        for file in os.listdir(filterpath):
            if file.endswith('.filt'):
                # Import Module and Manage Handle
                handle = load_filter_driver(file)
                # Generate Look-Up-Dictionary
                self.audiofilters[file[:-5]] = handle
        # Find Available Drives Ignoring C: and any CD-ROM Drives
        self.scanDrives(firstscan=True)

        # Prepare Main App Window
        self.title( "KRNC Universal Song Barn (USB) Manager"+
                    " - Your Music Lives Here.")
        self.configure(background=bgblue)
        self.geometry("{}x{}".format(mainwidth,mainheight))
        self.iconbitmap(self.icon)
        
        # Prepare Menu
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar,tearoff=0)
        self.barnmenu = tk.Menu(self.menubar,tearoff=0)
        self.filtmenu = tk.Menu(self.menubar,tearoff=0)
        self.aboutmenu = tk.Menu(self.menubar,tearoff=0)
        self.filemenu.add_command(  label="New Barn",  command=self.new_barn,
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
        self.barnmenu.add_command( label="Remove Selected",command=self.delete_selcted)
        self.barnmenu.add_separator()
        # Iteratively Generate Filter Submenu
        for filter in self.audiofilters.keys():
            # Add Menu Option for Each Filter
            self.filtmenu.add_command(  label=filter,
                                        command=partial(self.gFilt,filter))
        self.barnmenu.add_cascade(label="Global Filter", menu=self.filtmenu)
        self.barnmenu.add_separator()
        self.barnmenu.add_checkbutton( label="Enable KRNC Branding",var=self.krncbrand)
        self.barnmenu.add_command(  label="Update KRNC Branding",
                                    command=self.update_branding)
        self.aboutmenu.add_command(label="About...", command=self.popupmsg)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_cascade(label="Barn", menu=self.barnmenu)
        self.menubar.add_cascade(label="Help", menu=self.aboutmenu)
        self.config(menu=self.menubar)
        
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
                                    icon=self.icon,read_only=True,)
        self.table.show()
        self.model.addRow()
        self.set_columns(init=True)
        
        # Bind Keys
        self.bind_all("<Control-q>", self.quit)
        self.bind_all("<Control-n>", self.handle_new)
        self.bind_all("<Control-o>", self.handle_open)
        self.bind_all("<Control-s>", self.handle_save)
        self.bind_all("<Control-S>", self.handle_save_as)
        self.bind_all("<Control-a>", self.handle_add)
        self.bind_all("<Delete>",    self.handle_del)
        
        # Generate Options Sections
        optsFrame = tk.Frame(self, bg=bgblue, height=tablheight)
        barnFrame = tk.Frame(optsFrame, bg=bgblue, height=barnheight)
        drivFrame = tk.Frame(optsFrame, bg=bggrey, height=drivheight)
        optsFrame.grid(row=0, column=2, sticky="nsew")
        optsFrame.columnconfigure(0, weight=1)
        optsFrame.rowconfigure(0, weight=10)
        optsFrame.rowconfigure(1, weight=1)
        barnFrame.grid(row=0, column=0, sticky="nsew")
        drivFrame.grid(row=1, column=0, sticky="nsew")
        
        # Generate Barn Frame Information and Controls
        barnTitle = tk.Label(barnFrame, text="Barn Tools", fg=fgblue, bg=bgblue,
                            font=self.pt16B)
        barnTitle.grid(row=0, column=0, pady=5, padx=5)
        filtermenu = tk.OptionMenu(barnFrame,self.filterVar,*self.audiofilters.keys())
        filtermenu.config( width=int((mainwidth-tablwidth)*0.060),background=bglblue)
        filtermenu.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        pasturmenu = tk.OptionMenu(barnFrame,self.pasturVal,*self.pasturOpt)
        pasturmenu.config( width=int((mainwidth-tablwidth)*0.060),background=bglblue)
        pasturmenu.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        lineFrame = tk.Frame(barnFrame,height=1,width=50,bg=bggrey)
        lineFrame.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
        barnTitle = tk.Label(barnFrame, text="Brand Tools", fg=fgblue, bg=bgblue,
                            font=self.pt16B)
        barnTitle.grid(row=4, column=0, pady=5, padx=5)
        brandmenu = tk.OptionMenu(barnFrame,self.brandVal,*self.audiofilters)
        brandmenu.config( width=int((mainwidth-tablwidth)*0.060),background=bglblue)
        brandmenu.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")
        render = Image.open(self.logo)
        render = render.resize((150,150), Image.ANTIALIAS)
        photoImg =  ImageTk.PhotoImage(render)
        brandImag = tk.Label(barnFrame, image=photoImg, bg=bgblue)
        brandImag.image = photoImg
        brandImag.grid(row=6, column=0, padx=5, pady=15)
        
        # Generate Drive Frame Information
        drivTitle = tk.Label(drivFrame, text="Drive Tools", fg=fggrey, bg=bggrey,
                            font=self.pt16B)
        drivTitle.grid(row=0, column=0, pady=5, padx=5, columnspan=2)
        updtBtn = tk.Button(drivFrame, text="Unload Drive", bg=bglblue,
                            command=self.open_from_drive)
        sendBtn = tk.Button(drivFrame, text="Load Drive", bg=bglblue,
                            command=self.load_drive)
        frmtBtn = tk.Button(drivFrame, text="Train (Format) Drive",
                            bg=bglblue, command=self.formatDrive)
        #print(help(tk.OptionMenu))
        self.drivmenu = tk.OptionMenu(drivFrame,self.driveVal,*self.availDrives.keys())
        self.drivmenu.config( width=int((mainwidth-tablwidth)*0.060),background=bglblue)
        updtBtn.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        sendBtn.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        frmtBtn.grid(row=2, column=0, padx=5, pady=5, columnspan=2, sticky="nsew")
        self.drivmenu.grid(row=3, column=0, padx=5, pady=5, columnspan=2, sticky="nsew")
        
    def quit(self, event):
        self.destroy()
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
    
    def set_columns(self,init=False):
        # Format Columns as Necessary
        for c,column in enumerate(headers):
            name    = column['heading']
            ctype   = column['type']
            width   = column['width']
            if init: self.model.addColumn(colname=name,coltype=ctype)
            self.table.resizeColumn(c,width)
            if init: self.model.setValueAt('',0,c)
        self.table.redraw()
    
    # Define Handler Functions
    def handle_add(self,event):
        self.add_songs()
    def handle_del(self,event):
        self.delete_selcted()
    def handle_new(self,event):
        self.new_barn()
    def handle_open(self,event):
        self.open_barn()
    def handle_save(self,event):
        self.save_barn()
    def handle_save_as(self,event):
        self.save_barn_as()
    
    def _update(self):
        if not self.blockupdate:
            try:
                # Capture Current Information
                curFilter = self.filterVar.get()
                curPastur = self.pasturVal.get()
                ROWi = self.table.getSelectedRow()
                filter = self.model.getValueAt(ROWi,1)
                pasture = self.model.getValueAt(ROWi,2)
                # Validate That Same Row Still Selected
                if ROWi == self.lastRow:
                    # Update Filter
                    if (curFilter != "-filter-"):
                        self.model.setValueAt(curFilter,ROWi,1)
                        self.table.redraw()
                    # Update Pasture
                    if (curPastur!="-pasture-") and (pasture!=curPastur):
                        self.model.setValueAt(curPastur,ROWi,2)
                        self.table.redraw()
                else:
                    # Update Filter
                    if (curFilter != "-filter-") and (filter != ''):
                        self.filterVar.set( filter )
                    # Update Pasture
                    if (pasture!=curPastur):
                        self.pasturVal.set( pasture )
                    # Update Check
                    self.lastRow = ROWi
            except:
                pass
        # Set "After" Callback
        self.after(50,self._update)
    
    def scanDrives(self,firstscan=False):
        # Find Available Drives and Names
        strComputer = "." 
        objWMIService = win32com.Dispatch("WbemScripting.SWbemLocator")
        objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
        colItems = objSWbemServices.ExecQuery("Select * from Win32_LogicalDisk")
        # Iteratively Identify Drive Number and Label
        self.availDrives = {}
        for objItem in colItems:
            drvName = objItem.Name
            volName = objItem.VolumeName
            drvDesc = objItem.Description
            # Validate Drive as Potential USB
            if (drvName != 'C:') and (drvDesc.find('CD') == -1):
                drvStr = str(drvName) + '  ' + str(volName)
                self.availDrives[drvStr] = drvName
                if volName == 'KRNC':
                    self.driveVal.set(drvStr)
        if not firstscan:
            # Re-Load Drive Menu
            self.drivmenu['menu'].delete(0, 'end')
            for opt in self.availDrives.keys():
                self.drivmenu['menu'].add_command(  label=opt,
                            command=tk._setit(  self.driveVal, opt))
            # Update Label if Needed
            if self.driveVal.get() not in self.availDrives.keys():
                self.driveVal.set("-usb-drive-")
    
    def formatDrive(self):
        # Capture Selected Drive Letter
        try:
            curDrive = self.availDrives[ self.driveVal.get() ] + '\\'
        except:
            self.scanDrives()
            return
        frmt = 'NTFS'
        name = 'KRNC'
        # Validate Format Operation
        permission = tk.messagebox.askquestion("Format Drive",
                "Formatting will erase all data.\nProceed?",icon='warning',)
        if permission.lower() == 'yes':
            # Define Callback Function
            def fmtCallback(command, modifier, arg):
                return(1)
            # Start Format
            fm = windll.LoadLibrary('fmifs.dll')
            FMT_CB_FUNC = WINFUNCTYPE(c_int, c_int, c_int, c_void_p)
            FMIFS_UNKNOWN = 0
            fm.FormatEx(c_wchar_p(curDrive), FMIFS_UNKNOWN, c_wchar_p(frmt),
                        c_wchar_p(name), True, c_int(0), FMT_CB_FUNC(fmtCallback))
        else:
            self.popupmsg("Drive Format Aborted",button_txt="OK",height=150,width=200)
        # Re-Scan Drives
        self.scanDrives()
        if permission.lower() == 'yes':
            try:
                drive = self.availDrives[ self.driveVal.get() ]
                # Create KRNC Music Folder and Branding (Imaging) Path
                Path( drive + barnpath ).mkdir(parents=True, exist_ok=True)
                Path( drive + brndpath ).mkdir(parents=True, exist_ok=True)
                # Generate USBarn File
                with open(drive+'/'+drivedsc,'w') as t_file:
                    headerstring = ','.join([i['heading'] for i in headers])
                    t_file.write(headerstring+'\n,,\n')
                # Notify Success
                self.popupmsg(  "Drive Format Complete",title='KRNC',
                                button_txt="OK",height=150,width=220)
            except:
                pass
            finally:
                # Re-Scan One More Time
                self.scanDrives()
    
    def gFilt(self,filter):
        # Iteratively Set Filter Column
        for i in range(self.model.getRowCount()):
            self.model.setValueAt(filter,i,1)
        self.table.redraw()
        self.lastRow = -1 # Force Update
    
    def update_branding(self):
        # Use Requests to Download the Imaging
        resp = requests.get( brandurl )
        filepath = krncbrandp+'tempBranding.zip'
        # Start Loading Bar
        self.loader = LoadingBar(   text="Fetching Files.",
                                    width=300,
                                    height=150,
                                )
        # Store Zipped File
        with open(filepath,'wb') as tempZip:
            tempZip.write(resp.content)
        # Extract Zipped Content
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(krncbrandp)
        # Delete Zipped Folder
        os.remove(filepath)
        time.sleep(2)
        # Kill Loading Bar
        self.loader.destroy()
    
    def load_drive(self):
        try:
            # Attempt Loading Barn Description from USB
            driveNm = self.availDrives[ self.driveVal.get() ]
        except:
            # Invalid Drive
            self.popupmsg("An error occurred while loading\nthat USB Drive.",
                            width=300,height=150)
            self.scanDrives()
            return
        usbarn = driveNm + drivedsc
        if not self.validate_barn( usbarn ):
            # Invalid Barn
            self.popupmsg("An error occurred while loading\nthat USBarn description.",
                            width=300,height=150)
            return
        # Barn was validated, read listing
        usb_struct = {}
        with open(usbarn,'r') as t_file:
            t_file.readline()
            for line in t_file:
                # Read Structure
                fpath, filter, pasture = line.split(',')
                t_struct = {'filter':filter,
                            'pasture':pasture.replace('\n',''),
                            'name':os.path.basename(fpath),}
                usb_struct[fpath] = t_struct
        # Read Current Table Information
        tableStruct = list(self.model.getAllCells().values())
        tab_struct = {}
        for row in tableStruct:
            fpath, filter, pasture = row
            t_struct = {'filter':filter,
                        'pasture':pasture.replace('\n',''),
                        'destination':driveNm+barnpath,
                        'name':os.path.basename(fpath),}
            tab_struct[fpath] = t_struct
        # Delete Branding
        for file in  os.listdir( driveNm+brndpath ):
            # If file isn't in listing, delete it
            os.remove( os.path.join( driveNm+brndpath, file ) )
        # Establish Deltas
        to_be_added = list(set(tab_struct.keys()) - set(usb_struct.keys()))
        to_be_remvd = list(set(usb_struct.keys()) - set(tab_struct.keys()))
        # Add Files that Must be Filtered or Zipped
        common_files = list(set(tab_struct.keys()) & set(usb_struct.keys()))
        for file in common_files:
            Lstruct = tab_struct[file]
            Rstruct = usb_struct[file]
            # Compare Filter
            if Lstruct['filter'] != Rstruct['filter']:
                to_be_added.append( file )
        # Find Pastured Files
        zip_files = []
        uzip_files = []
        for Lstruct in tab_struct.values():
            if Lstruct['pasture'] == 'TRUE':
                zip_files.append(Lstruct['name'])
        for Lstruct,Rstruct in zip(tab_struct.values(),usb_struct.values()):
            if (Lstruct['pasture'] == 'FALSE') and (Rstruct['pasture'] == 'TRUE'):
                uzip_files.append(Lstruct['name'])
        # Format for Display
        add_display = [os.path.basename(i) for i in to_be_added]
        rmv_display = [os.path.basename(i) for i in to_be_remvd]
        # Validate Changes Exist
        if max(len(to_be_added),len(to_be_remvd),len(zip_files),len(uzip_files)) == 0:
            # Abort, No Changes to Make!
            self.popupmsg(  "USB Drive Load Aborted\nNo Changes Detected.",
                            button_txt="OK",width=300,height=150)
            return
        # Create Pop-Up Table Describing Delta
        dialog = TableDialog(self,add_display,rmv_display,"USBarn Load - Confirm Load",
                             "To Be Added","To Be Removed",icon=self.icon)
        approval = dialog.wait_for_response()
        # Confirm Approval
        if not approval:
            # Abort
            self.popupmsg(  "USB Drive Load Aborted",button_txt="OK",
                            width=300,height=150)
            return
        # Build Load Structure
        load_struct = {}
        for addObj in to_be_added:
            load_struct[addObj] = tab_struct[addObj]
        # Find all Branding to be Loaded (If Allowed)
        if self.krncbrand.get():
            # Capture Current Branding Filter
            brandFilter = self.brandVal.get()
            # Capture all Branding Files
            for file in os.listdir(krncbrandp):
                if file.endswith('.mp3'):
                    t_struct = {'filter':brandFilter,
                                'pasture':'FALSE',
                                'destination':driveNm+brndpath,
                                'name':file,}
                    load_struct[os.path.join(krncbrandp,file)] = t_struct
        # Start Loading Thread
        if not max(len(to_be_added),len(to_be_remvd)) == 0:
            t = threading.Thread(target=audio_loader,args=(load_struct,self.audiofilters))
            t.start()
            while t.is_alive():
                self.update()
            load_done = False
        # Delete Files not in Barn Listings
        names = [struct['name'] for struct in tab_struct.values()]
        for file in  os.listdir( driveNm+barnpath ):
            # Skip Zipped File
            if file.endswith('.zip'):
                continue
            # If file isn't in listing, delete it
            if not file in names:
                os.remove( os.path.join( driveNm+barnpath, file ) )
        # Operate Zipped Resources
        t = threading.Thread(target=pasture_zipper,args=(driveNm,zip_files,uzip_files))
        t.start()
        while t.is_alive():
            self.update()
        # Prepare to Store *.barn Description on USB
        preBarn = self.barn
        self.save_barn_as( usbarn )
        self.barn = preBarn
        self.popupmsg("Drive Completed!\nWelcome Home.",
                        width=300,height=200)
    
    def delete_selcted(self):
        # Delete Selected Row(s)
        # Start by Getting Selection
        selectionRecords = self.table.get_selectedRecordNames()
        # Iteratively Delete
        for record in selectionRecords:
            self.model.deleteRow(key=record)
        # Update Table
        self.table.redraw()
        # Save and Reload if Possible
        if self.barn != None:
            self.save_barn()
            self.open_barn(self.barn)
    
    def add_songs(self,songlist=[]):
        # Prompt User to Add Songs
        if songlist == []:
            songlist = tk.filedialog.askopenfilenames(  parent=self,
                                                        initialdir=self.musicpath,
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
        if (self.barn == None) and (self.model.getValueAt(0,0) == ''):
            self.model.deleteRows()
        # Add Column Titles
        filekwarg = headers[0]['heading']
        lockkwarg = headers[2]['heading']
        # Clear Filter and Pasture Information
        self.filterVar.set('')
        self.pasturVal.set('FALSE')
        # Add New Rows with Path and Pasture Information
        for song in songlist:
            self.musicpath = os.path.dirname(song)
            self.table.addRow(key=None,**{filekwarg:song,lockkwarg:'FALSE'})
    
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
    
    def open_from_drive(self):
        # Attempt Loading Barn Description from USB
        try:
            usbarn = self.availDrives[ self.driveVal.get() ] + drivedsc
        except:
            self.scanDrives()
            self.popupmsg("No Drive Selected.",button_txt="OK",width=300,height=75)
        if os.path.isfile(usbarn): # Barn Exists!
            # Check if Barn Already Loaded
            if self.barn != None:
                permission = tk.messagebox.askquestion("Close Barn?",
                "Opening from USB will close active Barn.\nProceed?",icon='warning',)
                if permission.lower() != 'yes':
                    # Abort
                    self.popupmsg("USBarn Load Aborted",button_txt="OK")
            # Load Barn
            self.open_barn(usbarn)
        else:
            # No Barn File Found!
            self.popupmsg("We couldn't find a USBarn description.",width=300,height=75)
    
    def validate_barn(self,filepath=''):
        if filepath == '':
            filepath = self.barn
        with open(filepath,'r') as t_file:
            invalidate = False
            # Check for a non-empty file and appropriate data
            i = 0
            names = []
            for i, l in enumerate(t_file):
                l_list = l.split(',')
                if len(l_list) != 3:
                    invalidate = True
                    print(len(l_list))
                    names.append(l_list[0])
            if ((i+1) < 2) or invalidate:
                self.popupmsg("An error occurred while loading\nthat USBarn description."+
                              '\nFailed Lines\n'+'\n'.join(names),
                              width=500,height=150+15*len(names))
                self.barn = None
                return(False)
            return(True)
    
    def open_barn(self,barn=''):
        # Open *.barn Song List File
        # Test if passed as argument
        if barn != '':
            self.barn = barn
        else:
            self.barn = tk.filedialog.askopenfilename(  initialdir=stockpath,
                                                        title="Open Barn Roster",
                                                        filetypes=(
                                                            ("USBarn Desc.",".barn"),
                                                            ("all files","."),
                                                        )
                                                     )
        # Validate Input
        if self.barn == '':
            return
        if not self.validate_barn(self.barn):
            return
        # Input is Valid, Load as CSV, then Reset Table
        self.model.importCSV(filename=self.barn)
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
                                                            ("USBarn Desc.",".barn"),
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
            writtenList = []
            for rowList in cellDict.values():
                # Validate Row as Unique (don't allow duplicates)
                if rowList not in writtenList:
                    row = ','.join(rowList)     # Create CSV Row
                    outputfile.write(row+'\n')  # Write to File
                    writtenList.append(rowList)
    
    def set_about_callback(self,callable,title="KRNC USB Manager Info",bg=bggrey,
                           button_txt="Close",height=150,width=300,*args,**kwargs):
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
        popup.iconbitmap(self.icon)
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
        self.after(50,self._update)
        self.mainloop()

if __name__ == "__main__":
    mainApp = App()
    # Barn Description File was Found
    if barnfile != None:
        mainApp.open_barn(barnfile)
    mainApp.set_about_callback(version)
    time.sleep(3)
    mainApp.run()
# END