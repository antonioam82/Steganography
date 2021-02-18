from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
import tkinter.scrolledtext as sct
import cv2
import os
import numpy as np

class app():
    def __init__(self):
        self.window = Tk()
        self.window.title("Image Steganography")
        self.window.geometry("593x410")
        self.backgr = "gray90"
        #self.window.configure(bg=self.backgr)

        self.imaname = StringVar()
        self.current_dir = StringVar()
        self.mode = StringVar()
        self.mode.set(None)

        self.entryDir = Entry(self.window,width=98,textvariable=self.current_dir)
        self.entryDir.place(x=0,y=0)
        self.textEntry = sct.ScrolledText(self.window,width=70,height=15)
        self.textEntry.place(x=5,y=28)
        self.btnCopy = Button(self.window,text="COPY TEXT",bg=self.backgr)
        self.btnCopy.place(x=5,y=277)
        self.btnClear = Button(self.window,text="CLEAR TEXT",bg=self.backgr)
        self.btnClear.place(x=80,y=277)
        self.rdbEncode = Radiobutton(self.window,text="Encode",variable=self.mode,value="EN",command=self.set_mode)
        self.rdbEncode.place(x=420,y=277)
        self.rdbDecode = Radiobutton(self.window,text="Decode",variable=self.mode,value="DE",command=self.set_mode)
        self.rdbDecode.place(x=506,y=277)
        self.btnSearch = Button(self.window,text="SEARCH",width=20,bg=self.backgr)
        self.btnSearch.place(x=5,y=315)
        self.entImage = Entry(self.window,width=37,font=('arial',14,'bold'),textvariable=self.imaname)
        self.entImage.place(x=167,y=315)
        self.btnStart = Button(self.window,text="START",width=81,bg=self.backgr)
        self.btnStart.place(x=5,y=358)
        

        self.show_dir()

        self.window.mainloop()

    def show_dir(self):
        dirr = os.getcwd()
        self.current_dir.set(dirr)

    def set_mode(self):
        self.btnStart.configure(text="START {}CODING".format(self.mode.get()))

                                    
if __name__=="__main__":
    app()
