import time
from datetime import datetime, timedelta
import tkinter as tk
from PIL import ImageTk,Image
import threading
from allmyfunctions import *
import serial

# for raspberry pi only, serial linakge to the relay
usb = serial.Serial("/dev/ttyUSB0",9600)
# codes for tun on and turn off relay
turnOn = b'\xA0\x01\x01\xA2'
turnOff = b'\xA0\x01\x00\xA1'

root = tk.Tk()
root.title('MM Exit')
root.geometry("250x250")
#get the 3 images
defaultimg = ImageTk.PhotoImage(Image.open("img/blank.png").resize((175, 175), Image.ANTIALIAS))
successimg = ImageTk.PhotoImage(Image.open("img/proceed.jpg").resize((175, 175), Image.ANTIALIAS))
errorimg = ImageTk.PhotoImage(Image.open("img/red-stop.jpg").resize((175, 175), Image.ANTIALIAS))

def openthegates():
    if usb.is_open:
        usb.write(turnOn)
        time.sleep(1)
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
        resultlbl.config(text = 'Welcome ' + inp)
        imglabel.config(image=successimg)
        openthegates()
    else:
        resultlbl.config(text = 'No entry found for ' + inp)
        imglabel.config(image=errorimg)

    threading.Timer(3, clearFields).start()

def clearFields():
    resultlbl.config(text = "")
    imglabel.config(image=defaultimg)
    inputtxt.focus()

#bind the enter key to the function
root.bind('<Return>', printInput)

#greeting to tell you which page you're on
greeting = tk.Label(root, text = "Magic Mirror Exit")
greeting.pack()

#enter the card no here
inputtxt = tk.Text(root,height = 1,width = 20)
inputtxt.pack()
inputtxt.focus()
#message
resultlbl = tk.Label(root, text = "")
resultlbl.pack()

#image
imglabel = tk.Label(root, image=defaultimg)
imglabel.pack()

root.mainloop()

