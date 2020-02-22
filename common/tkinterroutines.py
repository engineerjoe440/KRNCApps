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

# Define Generic Parent-Directory File Retrieval System; EX: `uppath(__file__, 2)`
uppath = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n])


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

# Builtin Test
if __name__ == '__main__':
    import time
    # creating tkinter window 
    root = tk.Tk()
    LB = LoadingBar()
    print("waiting 10")
    time.sleep(10)
    print("stopnow")
    LB.stop()
    root.mainloop()

# END