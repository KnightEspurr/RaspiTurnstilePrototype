import time
from datetime import datetime, timedelta
import tkinter as tk
from PIL import ImageTk,Image
import threading
from allmyfunctions import *

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
            else:
                print(f"{msg.payload.decode()} already scanned")
    client.subscribe(topic)
    client.on_message = on_message

client = connect_mqtt_receive()
subscribeVerify2(client)
#client.loop_forever()
client.loop_start()
while True:
    print(str(datetime.now()))
    deleteExpiredRecords()
    time.sleep(300)
