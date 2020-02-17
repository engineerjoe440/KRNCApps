"""
#######################################################################################
Tkinter Routines Support File
(c) Stanley Solutions

By: Joe Stanley
#######################################################################################
"""

# Required Imports
import tkinter as tk
from PIL import Image, ImageTk
import time, os, sys

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
# Scrollable Frame Class
class ScrollableFrame(tk.Frame):
    def __init__(self, container, width, height, bg, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self,width=width,height=height,bg=bg)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas,bg=bg)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        #canvas.pack_propagate(0)
        #scrollbar.pack_propagate(0)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
#######################################################################################

# END