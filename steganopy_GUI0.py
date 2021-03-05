from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
import tkinter.scrolledtext as sct
import threading
import time
import re
import cv2
import os
import numpy as np

class app():
    def __init__(self):
        self.window = Tk()
        self.window.title("Image Steganography")
        self.window.geometry("593x402")
        self.backgr = "gray90"

        self.imaname = StringVar()
        self.current_dir = StringVar()
        self.mode = StringVar()
        self.mode.set("EN")
        self.nbytes = IntVar()
        self.file_name = ""
        self.running = False

        self.entryDir = Entry(self.window,width=98,textvariable=self.current_dir)
        self.entryDir.place(x=0,y=0)
        self.textEntry = sct.ScrolledText(self.window,width=70,height=15)
        self.textEntry.place(x=5,y=28)
        self.btnClear = Button(self.window,text="CLEAR TEXT",width=20,bg=self.backgr,command=self.clear)
        self.btnClear.place(x=5,y=277)
        self.rdbEncode = Radiobutton(self.window,text="Encode",variable=self.mode,value="EN",command=self.set_mode)
        self.rdbEncode.place(x=420,y=277)
        self.rdbDecode = Radiobutton(self.window,text="Decode",variable=self.mode,value="DE",command=self.set_mode)
        self.rdbDecode.place(x=506,y=277)
        self.btnSearch = Button(self.window,text="SEARCH",width=20,bg=self.backgr,command=self.open_file)
        self.btnSearch.place(x=5,y=315)
        self.entImage = Entry(self.window,width=37,font=('arial',14),textvariable=self.imaname)
        self.entImage.place(x=167,y=315)
        self.btnStart = Button(self.window,text="START ENCODING",width=81,bg=self.backgr,command=self.init_task)
        self.btnStart.place(x=5,y=353)
        self.bylab = Label(self.window,text="BYTES AVAILABLE:")
        self.bylab.place(x=167,y=280)
        self.byEnt = Entry(self.window,textvariable=self.nbytes,width=17)
        self.byEnt.place(x=275,y=281)
        self.invLabel = Label(self.window,text="",fg="blue",width=83)
        self.invLabel.place(x=3,y=380)
        

        self.show_dir()

        self.window.mainloop()

    def show_dir(self):
        self.current_dir.set(os.getcwd())

    def set_mode(self):
        self.btnStart.configure(text="START {}CODING".format(self.mode.get()))

    def open_file(self):
        file = filedialog.askopenfilename(initialdir="/",title="SELECT FILE",
               filetypes =(("PNG files","*.PNG") ,("TIFF files","*.TIFF")))
        if file != "":
            self.file_name = file.split("/")[-1]
            os.chdir(("/").join(file.split("/")[:-1]))
            self.show_dir()
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
        #secret_data = self.textEntry.get('1.0',END)
        secret_data = re.sub("\[\d+\]","",self.textEntry.get('1.0',END))
        if len(secret_data) <= self.n_bytes:
            secret_data += "====="
            data_index = 0
            binary_secret_data = self.to_bin(secret_data)
            data_len = len(binary_secret_data)
            for row in self.image:
                for pixel in row:
                    r, g, b = self.to_bin(pixel)
                    if data_index < data_len:
                        pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
                        data_index += 1
                    if data_index < data_len:
                        pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
                        data_index += 1
                    if data_index < data_len:
                        pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2)
                        data_index += 1
                    if data_index >= data_len:
                        break
            ima_name = "encoded_"+self.file_name
            cv2.imwrite(ima_name,self.image)
            messagebox.showinfo("TASK COMPLETED","Created image: {}".format(ima_name))
        else:
            messagebox.showwarning("ERROR","Insufficient bytes, need bigger image or less data.")
        self.invLabel.configure(text="")
        self.running = False
                    
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
        if "=====" in decoded_data:
            self.clear()
            self.textEntry.insert(END,decoded_data[:-5])
        else:
            messagebox.showwarning("NO DATA","No data encoded.")
        self.invLabel.configure(text="")
        self.running = False

    def init_task(self):
        if self.file_name != "":
            if self.mode.get()=="EN" and len(self.textEntry.get('1.0',END))>1 and self.running==False:
                self.running = True
                self.invLabel.configure(text="ENCODING...")
                t = threading.Thread(target=self.encode)
                t.start()
            elif self.mode.get()=="DE" and self.running==False:
                self.running = True
                self.invLabel.configure(text="DECODING...")
                t = threading.Thread(target=self.decode)
                t.start()
        else:
            messagebox.showwarning("NO FILE","Select image file.")
            
                
if __name__=="__main__":
    app()
