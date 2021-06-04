from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
import tkinter.scrolledtext as sct
import threading
import pyperclip
import re
import time
import cv2
import os
import numpy as np

class app():
    def __init__(self):
        self.window = Tk()
        self.window.title("Image Steganography")
        self.window.geometry("708x418")
        self.backgr = "gray90"

        self.imaname = StringVar()
        self.current_dir = StringVar()
        self.mode = StringVar()
        self.mode.set("EN")
        self.current_marker = StringVar()
        self.current_marker.set("=====")
        self.spaces = 5
        self.nbytes = IntVar()
        self.file_name = ""
        self.running = False

        self.entryDir = Entry(self.window,width=117,textvariable=self.current_dir)
        self.entryDir.place(x=0,y=0)
        self.textEntry = sct.ScrolledText(self.window,width=85,height=16)
        self.textEntry.place(x=5,y=28)
        Button(self.window,text="COPY TEXT",bg=self.backgr,command=self.init_copy).place(x=5,y=311)
        Button(self.window,text="CLEAR TEXT",bg=self.backgr,command=self.clear).place(x=80,y=311)
        self.rdbEncode = Radiobutton(self.window,text="Encode",variable=self.mode,value="EN",command=self.set_mode)
        self.rdbEncode.place(x=553,y=313)
        self.rdbDecode = Radiobutton(self.window,text="Decode",variable=self.mode,value="DE",command=self.set_mode)
        self.rdbDecode.place(x=629,y=313)
        Button(self.window,text="SEARCH",width=20,bg=self.backgr,command=self.open_file).place(x=5,y=345)
        self.entImage = Entry(self.window,width=49,font=('arial',14),textvariable=self.imaname)
        self.entImage.place(x=156,y=345)
        self.btnStart = Button(self.window,text="START ENCODING",width=76,bg=self.backgr,command=self.init_task)
        self.btnStart.place(x=158,y=379)
        Label(self.window,text="BYTES AVAILABLE:").place(x=167,y=314)
        self.byEnt = Entry(self.window,textvariable=self.nbytes,width=11)
        self.byEnt.place(x=271,y=315)
        Label(self.window,text="MARKER:").place(x=354,y=314)
        self.markerEntry = Entry(self.window,textvariable=self.current_marker)
        self.markerEntry.place(x=410,y=315)
        self.invLabel = Label(self.window,fg="blue",width=98)
        self.invLabel.place(x=6,y=289)
        Button(self.window,text="SAVE DATA",bg=self.backgr,width=20,command=self.save_data).place(x=5,y=379)

        self.show_dir()

        self.window.mainloop()

    def show_dir(self):
        self.current_dir.set(os.getcwd())

    def save_data(self):
        if len(self.textEntry.get('1.0',END)) > 1:
            document = filedialog.asksaveasfilename(initialdir="/",
                       title="Save",defaultextension='.txt')
            if document != "":
                file = open(document,"w",encoding="utf-8")
                line = ""
                content = self.textEntry.get('1.0',END)
                for l in content:
                    line = line+l
                file.write(line)
                file.close()
                messagebox.showinfo("SAVED","Saved document: {}".format(document))
        
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

    def copy_text(self):
        self.textEntry.delete('1.0',END)
        self.ultima_copia = pyperclip.paste().strip()
        while True:
            time.sleep(0.1)
            self.copia = pyperclip.paste().strip()
            if self.copia != self.ultima_copia:
                self.textEntry.insert(END,self.copia)
                self.ultima_copia = self.copia 
                break

    def init_copy(self):
        messagebox.showinfo("IMPORT TEXT","""Select the text, right-click and
select 'copy' to import it.""")
        t1 = threading.Thread(target=self.copy_text)
        t1.start()

    def encode(self):
        secret_data = re.sub("\[\d+\]","",self.textEntry.get('1.0',END))
        if len(secret_data) <= self.n_bytes:
            new_file = filedialog.asksaveasfilename(initialdir="/",filetypes=[('png files','*.PNG'),
                                     ('tiff files','*.TIFF')],title="Save",defaultextension='.png')
            ima_name = (new_file).split("/")[-1]
            if new_file != "":
                secret_data += self.current_marker.get() #"====="
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
            
                cv2.imwrite(new_file,self.image)
                messagebox.showinfo("TASK COMPLETED","Created image: {}".format(ima_name))
        else:
            messagebox.showwarning("NO ESPACE","Insufficient bytes, need bigger image or less data.")
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
            if decoded_data[-(self.spaces):] == self.current_marker.get():#"====="
                break
        self.clear()
        if self.current_marker.get() in decoded_data:
            self.clear()
            self.textEntry.insert(END,decoded_data[:-(self.spaces)])
        else:
            messagebox.showwarning("NO DATA","Data not found.")
        self.invLabel.configure(text="")
        self.running = False

    def init_task(self):
        if self.current_marker.get() != "":
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
        else:
            messagebox.showwarning("NO MARKER","A marker string is required.")
            
                
if __name__=="__main__":
    app()
