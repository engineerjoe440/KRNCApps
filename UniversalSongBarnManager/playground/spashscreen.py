import tkinter as tk
from PIL import Image, ImageTk
import time

class Splash(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.center()
        self.configure(background='#506c91')
        self.overrideredirect(1)
        self.showImg()
        self.showTxt()
        self.update()
    
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
    def showImg(self):
        render = Image.open("C:\\Users\\joestan\Desktop\\KRNCApps\\common\\KRNCnegative.png")
        render = render.resize((150,150), Image.ANTIALIAS)
        photoImg =  ImageTk.PhotoImage(render)
        img = tk.Label(self, image=photoImg, bg='#506c91')
        img.image = photoImg
        img.place(x=22, y=0)
    def showTxt(self):
        txtFrame = tk.Frame(self, bg='#506c91')
        txtFrame.grid(row=0, column=1)
        label1 = tk.Label(txtFrame, text="Welcome Home", fg="white", bg='#506c91')
        label1.grid(row=0, column=0, pady=10)
        txtFrame.update()
        xbias = self.winfo_width() / 2 - txtFrame.winfo_width() / 2
        ybias = (self.winfo_height() / 2- txtFrame.winfo_height() / 2) + 60
        txtFrame.grid(row=0, column=1, pady=ybias, padx=xbias)

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.withdraw()
        splash = Splash(self)

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