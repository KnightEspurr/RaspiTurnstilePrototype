import time
from datetime import datetime, timedelta
import tkinter as tk
from PIL import ImageTk,Image
import threading
from allmyfunctions import *

root = tk.Tk()
root.title('Magic Mirror')
root.geometry("250x250")

#get the 3 images
defaultimg = ImageTk.PhotoImage(Image.open("img/blank.png").resize((175, 175), Image.ANTIALIAS))
successimg = ImageTk.PhotoImage(Image.open("img/proceed.jpg").resize((175, 175), Image.ANTIALIAS))
errorimg = ImageTk.PhotoImage(Image.open("img/red-stop.jpg").resize((175, 175), Image.ANTIALIAS))

#image
imglabel = tk.Label(root, image=defaultimg)
imglabel.pack()

def subscribeVerify2(client: mqtt_client):
    def on_message(client, userdata, msg):
        with open(storage, 'r') as file:
            file_data = json.load(file)
            checkIfExists = len([obj for obj in file_data if (obj['code'] == msg.payload.decode())])
            if checkIfExists == 0:       
                print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

                dictionary = {
                    "code": msg.payload.decode(),
                    "timestamp": str(datetime.now())
                }
                writeJson(dictionary)

                imglabel.config(image=successimg)
                threading.Timer(3, resetImg).start()
            else:
                print(f"{msg.payload.decode()} already scanned")
                imglabel.config(image=errorimg)
                threading.Timer(3, resetImg).start()
    client.subscribe(topic)
    client.on_message = on_message

def resetImg():
    imglabel.config(image=defaultimg)

client = connect_mqtt_receive()
subscribeVerify2(client)
#client.loop_forever()
client.loop_start()

root.mainloop()
