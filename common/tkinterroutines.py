"""
#######################################################################################
Tkinter Routines Support File
(c) Stanley Solutions

By: Joe Stanley
#######################################################################################
"""

# Required Imports
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import time, os, sys
import threading
from tkintertable import TableCanvas, TableModel

# Define Generic Parent-Directory File Retrieval System; EX: `uppath(__file__, 2)`
uppath = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n])

# Declare Space for Progress Handle
gProgHandle = None

#######################################################################################
# Splash Screen Class
"""
EXAMPLE:
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.withdraw()
        splash = Splash(self,text="Welcome Home",width=300,
            image=uppath(__file__, 3)+"\\common\\KRNCnegative.png")

        ## setup stuff goes here
        self.title("Main Window")
        ## simulate a delay while loading
        time.sleep(6)

        ## finished loading so destroy splash
        splash.destroy()

        ## show selfdow again
        self.deiconify()

if __name__ == "__main__":
    app = App()
    app.mainloop()
"""

# Define Class
class Splash(tk.Toplevel):
    # Initialization Method
    def __init__(self,parent,fg='white',bg='#506c91',imgw=150,imgh=150,
                 width=200,height=200,image=None,text=''):
        tk.Toplevel.__init__(self, parent)
        self.center()
        self.geometry("{}x{}".format(width,height))
        self.configure(background=bg)
        self.overrideredirect(1)
        if image != None:
            self.showImg(image=image,bg=bg,w=imgw,h=imgh)
        else:
            imgh = 0
        if text != '':
            self.showTxt(text=text,fg=fg,bg=bg,imgh=imgh)
        self.update()
    # Center, Show Image, and Show Text Methods
    def center(self):
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
    def showImg(self,image,bg,w,h):
        render = Image.open(image)
        render = render.resize((w,h), Image.ANTIALIAS)
        photoImg =  ImageTk.PhotoImage(render)
        imgFrame = tk.Frame(self, bg=bg)
        imgFrame.grid(row=0, column=1)
        img = tk.Label(imgFrame, image=photoImg, bg=bg)
        img.image = photoImg
        img.place(x=22, y=0)
        img.grid(row=0, column=0, pady=0)
        imgFrame.update()
        xbias = self.winfo_width() / 2 - imgFrame.winfo_width() / 2
        ybias = 5
        imgFrame.grid(row=0, column=1, pady=ybias, padx=xbias)
    def showTxt(self,text,fg,bg,imgh=0):
        txtFrame = tk.Frame(self, bg=bg)
        txtFrame.grid(row=1, column=1)
        label1 = tk.Label(txtFrame, text=text, fg=fg, bg=bg)
        label1.grid(row=1, column=0, pady=0)
        txtFrame.update()
        xbias = self.winfo_width() / 2 - txtFrame.winfo_width() / 2
        ybias = self.winfo_height() - (txtFrame.winfo_height() + 25 + imgh)
        txtFrame.grid(row=1, column=1, pady=ybias, padx=xbias)
#######################################################################################

#######################################################################################
# Indeterminite Tkinter Loading Bar
class LoadingBar(tk.Toplevel):
    # Initialization Method
    def __init__(self,fg='white',bg='#506c91',width=200,height=100,text=''):
        self.width = width
        self.height = height
        self.text = text
        self.bg = bg
        self.fg = fg
        self.t = threading.Thread()
        self.t.__init__(target = self.run, args = ())
        self.t.start()
    # Center and Update Methods
    def center(self):
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
        self.parent = tk.Tk()
        self.parent.withdraw()
        tk.Toplevel.__init__(self, self.parent)
        self.center()
        self.geometry("{}x{}".format(self.width,self.height))
        self.configure(background=self.bg)
        self.overrideredirect(1)
        self.label = tk.Label(self, text=self.text, bg=self.bg, fg=self.fg)
        self.rowconfigure(0, weight=15)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.label.grid(row=0,column=0,pady=5,padx=5, sticky="nsew")
        self.progress = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=50,
                                        mode='indeterminate' )
        self.progress.grid(row=1,column=0,pady=5,padx=5, sticky="ew")
        self.t1 = threading.Thread()
        self.t1.__init__(target = self.progress.start, args = ())
        self.t1.start()
        self.parent.mainloop()
    def stop(self):
        if self.t1.is_alive() == False:
            self.progress.stop()
            self.t1.join()
#######################################################################################

#######################################################################################
# Indeterminite Tkinter Loading Bar
class BlockLoadingBar(tk.Toplevel):
    # Initialization Method
    def __init__(self,fg='white',bg='#506c91',width=200,height=150,text=''):
        self.width = width
        self.height = height
        self.text = text
        self.bg = bg
        self.fg = fg
        self.t = threading.Thread()
        self.t.__init__(target = self.run, args = ())
        self.t.start()
    # Center and Update Methods
    def center(self):
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
    def setValue(self,value):
        global gProgHandle
        gProgHandle['value'] = int(value)
    def getValue(self):
        global gProgHandle
        return(gProgHandle['value'])
    def run(self):
        global gProgHandle
        self.parent = tk.Tk()
        self.parent.withdraw()
        tk.Toplevel.__init__(self, self.parent)
        self.center()
        self.geometry("{}x{}".format(self.width,self.height))
        self.configure(background=self.bg)
        self.overrideredirect(1)
        self.label = tk.Label(self, text=self.text, bg=self.bg, fg=self.fg)
        self.rowconfigure(0, weight=15)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.label.grid(row=0,column=0,pady=5,padx=5, sticky="nsew")
        self.progress = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=50,
                                        mode='indeterminate' )
        self.gprogress = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=50,
                                        mode='determinate' )
        self.progress.grid(row=1,column=0,pady=5,padx=5, sticky="ew")
        self.gprogress.grid(row=2,column=0,pady=5,padx=5, sticky="ew")
        gProgHandle = self.gprogress
        self.t1 = threading.Thread()
        self.t1.__init__(target = self.progress.start, args = ())
        self.t1.start()
        self.gprogress['value'] = 20
        self.parent.mainloop()
    def stop(self):
        if self.t1.is_alive() == False:
            self.progress.stop()
            self.gprogress.stop()
            self.t1.join()
            self.t2.join()
#######################################################################################

#######################################################################################
class TableDialog(tk.Toplevel):
    def __init__(   self,parent,column1,column2,title='',column1txt='',column2txt='',
                    fg='white',bg='#506c91',tablecellbg='#bdc7e5',tablebg='#c9cdd9',
                    width=620,height=290,icon=None):
        self.dataObj = None
        self.top = tk.Toplevel(parent)
        self.top.wm_title(title)
        self.top.configure(background=bg)
        self.top.geometry("{}x{}".format(width,height))
        if icon != None:
            self.top.iconbitmap(icon)
        self.top.rowconfigure(0,weight=1)
        tablFrame = tk.Frame(self.top, bg=bg,width=int(width-50),height=height)
        tablFrame.grid(row=0, column=0,sticky="nsew")
        tablFrame.columnconfigure(0, weight=1)
        tablFrame.rowconfigure(0, weight=1)
        btnFrame = tk.Frame(self.top, bg=bg,width=50,height=height)
        btnFrame.grid(row=0, column=1,sticky="nsew")
        btnFrame.columnconfigure(0, weight=1)
        popmodel = TableModel()
        poptable = TableCanvas( tablFrame, model=popmodel,cellbackgr=tablecellbg,
                                rowselectedcolor=bg,rowheight=25,icon=icon,
                                thefont=('Segoe UI',8),entrybackgr=tablebg,
                                selectedcolor=tablebg,multipleselectioncolor=tablecellbg,)
        okBtn = tk.Button(btnFrame,text="OK",bg=tablecellbg)
        cancelBtn = tk.Button(btnFrame,text="CANCEL",bg=tablecellbg)
        okBtn['command'] = lambda: self.declare_response(True)
        cancelBtn['command'] = lambda: self.declare_response(False)
        okBtn.grid(row=0,column=0,padx=5,pady=5,sticky="ew")
        cancelBtn.grid(row=1,column=0,padx=5,pady=5,sticky="ew")
        poptable.show()
        popmodel.addColumn(column1txt)
        popmodel.addColumn(column2txt)
        poptable.resizeColumn(0,250)
        poptable.resizeColumn(1,250)
        # Add Empty Rows For Table, Minimum of One Row Required
        for ROWi in range(max(len(column1),len(column2),1)):
            popmodel.addRow()
        # Load Rows with Data
        for ROWi, entry in enumerate(column1):
            popmodel.setValueAt(entry,ROWi,0)
        for ROWi, entry in enumerate(column2):
            popmodel.setValueAt(entry,ROWi,1)
        poptable.redraw()
    
    def declare_response(self,response=None):
        self.dataObj = response
        self.top.destroy()
    
    def wait_for_response(self):
        while self.dataObj not in [True, False]:
            self.top.update()
        return(self.dataObj)
#######################################################################################

# Builtin Test
if __name__ == '__main__':
    import time
    # creating tkinter window 
    root = tk.Tk()
    LB = BlockLoadingBar()
    print("waiting 10")
    time.sleep(2)
    LB.setValue(40)
    time.sleep(3)
    LB.setValue(80)
    time.sleep(5)
    print("stopnow")
    LB.destroy()
    root.mainloop()

# END