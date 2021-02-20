from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
import tkinter.scrolledtext as sct
import threading
import cv2
import os

import numpy as np

class app():
    def __init__(self):
        self.window = Tk()
        self.window.title("Image Steganography")
        self.window.geometry("593x405")
        self.backgr = "gray90"
        #self.window.configure(bg=self.backgr)

        self.imaname = StringVar()
        self.current_dir = StringVar()
        self.mode = StringVar()
        self.mode.set("EN")
        self.nbytes = IntVar()

        self.entryDir = Entry(self.window,width=98,textvariable=self.current_dir)
        self.entryDir.place(x=0,y=0)
        self.textEntry = sct.ScrolledText(self.window,width=70,height=15)
        self.textEntry.place(x=5,y=28)
        self.btnCopy = Button(self.window,text="COPY TEXT",bg=self.backgr)
        self.btnCopy.place(x=5,y=277)
        self.btnClear = Button(self.window,text="CLEAR TEXT",bg=self.backgr,command=self.clear)
        self.btnClear.place(x=80,y=277)
        self.rdbEncode = Radiobutton(self.window,text="Encode",variable=self.mode,value="EN",command=self.set_mode)
        self.rdbEncode.place(x=420,y=277)
        self.rdbDecode = Radiobutton(self.window,text="Decode",variable=self.mode,value="DE",command=self.set_mode)
        self.rdbDecode.place(x=506,y=277)
        self.btnSearch = Button(self.window,text="SEARCH",width=20,bg=self.backgr,command=self.open_file)
        self.btnSearch.place(x=5,y=315)
        self.entImage = Entry(self.window,width=37,font=('arial',14),textvariable=self.imaname)
        self.entImage.place(x=167,y=315)
        self.btnStart = Button(self.window,text="START ENCODING",width=81,bg=self.backgr,command=self.init_task)
        self.btnStart.place(x=5,y=358)
        self.bylab = Label(self.window,text="BYTES AVAILABLE:")
        self.bylab.place(x=167,y=280)
        self.byEnt = Entry(self.window,textvariable=self.nbytes,width=17)
        self.byEnt.place(x=275,y=281)
        

        self.show_dir()

        self.window.mainloop()

    def show_dir(self):
        dirr = os.getcwd()
        self.current_dir.set(dirr)

    def set_mode(self):
        self.btnStart.configure(text="START {}CODING".format(self.mode.get()))

    def open_file(self):
        file = filedialog.askopenfilename(initialdir="/",title="SELECCIONAR ARCHIVO",
               filetypes =(("PNG files","*.PNG") ,("TIFF files","*.TIFF")))
        if file != "":
            self.file_name = file.split("/")[-1]
            self.imaname.set(self.file_name)
            try:
                self.image = cv2.imread(file)
                self.n_bytes = self.image.shape[0] * self.image.shape[1] * 3 // 8
                self.nbytes.set(self.n_bytes)
            except:
                messagebox.showwarning("ERROR","Can't open the file.")

    def clear(self):
        self.textEntry.delete('1.0',END)

    def to_bin(self,data):
        if isinstance(data, str):
            return ''.join([ format(ord(i), "08b") for i in data ])
        elif isinstance(data, bytes) or isinstance(data, np.ndarray):
            return [ format(i, "08b") for i in data ]
        elif isinstance(data, int) or isinstance(data, np.uint8):
            return format(data, "08b")
        else:
            raise TypeError("Type not supported.")

    def encode(self):
        print("Nothing yet :P")

    def decode(self):
        binary_data = ""
        for row in self.image:
            for pixel in row:
                r, g, b = self.to_bin(pixel)
                binary_data += r[-1]
                binary_data += g[-1]
                binary_data += b[-1]
        all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data[-5:] == "=====":
                break
        self.clear()
        if not "ÿ" in decoded_data[:-5]:
            self.textEntry.insert(END,decoded_data[:-5])
        else:
            print(":P")

    def init_task(self):
        if self.mode.get()=="EN":
            t = threading.Thread(target=self.encode)
        else:
            t = threading.Thread(target=self.decode)
        t.start()
                
if __name__=="__main__":
    app()
