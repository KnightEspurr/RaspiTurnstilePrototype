import time
import subprocess
from datetime import datetime, timedelta
import tkinter as tk
from PIL import ImageTk,Image
import threading
from threading import Thread
from allmyfunctions import *
import serial
from itertools import count, cycle

class ImageLabel(tk.Label):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im).resize((700,480),Image.ANTIALIAS)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = 100
        except:
            self.delay = 10

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)

# for raspberry pi only, serial linakge to the relay
usb = serial.Serial("/dev/ttyUSB0",9600)
# codes for tun on and turn off relay
turnOn = b'\xA0\x01\x01\xA2'
turnOff = b'\xA0\x01\x00\xA1'

root = tk.Tk()
root.title('MM Exit')
root.attributes("-fullscreen",True)
root.configure(bg="black")
root.bind("<Escape>",quit)
#root.geometry("250x250")
#get the 3 images
successimg = "gifs/SAFE Green.jpg"
errorimg = "gifs/SAFE Red.jpg"
justgif = "gifs/SAFE Screen.jpg"

def openthegates():
    if usb.is_open:
        usb.write(turnOn)
        time.sleep(6)
        usb.write(turnOff)
        time.sleep(1)

#function to print the code scanned / keyed in into label
#clear the inputs so can scan again
def printInput(event):
    inp = inputtxt.get(1.0, "end-1c").strip() #strip the whitespace because the enter key press counts
    inputtxt.delete('1.0', tk.END)

    #run the delete function
    attempt = deleteFromJsonUsingInput(inp)
    if attempt == True:
        #imglabel.load(successimg)
        #openthegates()
        a = Thread(target = imglabel.load(successimg))
        b = Thread(target = openthegates)
        a.start()
        b.start()
    else:
        imglabel.load(errorimg)

    threading.Timer(6, clearFields).start()

def clearFields():
    imglabel.load(justgif)
    inputtxt.focus()

#bind the enter key to the function
root.bind('<Return>', printInput)

#enter the card no here
inputtxt = tk.Text(root,height = 1,width = 20)
inputtxt.pack()
inputtxt.focus()

#image
imglabel = ImageLabel(root)
imglabel.pack()
imglabel.load(justgif)

root.mainloop()

