#dump all functions here

from datetime import datetime, timedelta
import time
import random
import json
from paho.mqtt import client as mqtt_client
import itertools as it
import tkinter as tk
from PIL import ImageTk,Image
import os

broker = 'broker.emqx.io'
port = 1883
topic = "magicmirror"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'emqx'
password = 'public'
storage = 'storage.json'
interval = 900

# make connection for mqtt
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker! Entry service activated")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

# use this one for the receiver
def connect_mqtt_receive() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker! Storage service activated")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
    while True:
        insert = input()
        result = client.publish(topic, insert)
        status = result[0]
        if status == 0:
            print(f"Send `{insert}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

def publishFromTK(client,insert):
    #before you do anything, validate that this value does not exist in the log
    with open(storage, 'r') as file:
        file_data = json.load(file)
        checkIfExists = len([obj for obj in file_data if (obj['code'] == insert)])
        if checkIfExists == 0:
            result = client.publish(topic, insert)
            status = result[0]
            if status == 0:
                print(f"Send `{insert}` to topic `{topic}`")
                return("True")
            else:
                print(f"Failed to send message to topic {topic}")
                return("Fail")
        else:
            print(f"Already logged")
            return("Exists")

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        dictionary = {
            "code": msg.payload.decode(),
            "timestamp": str(datetime.now())
        }
        writeJson(dictionary)

    client.subscribe(topic)
    client.on_message = on_message

def writeJson(entry):
    with open(storage, 'r+') as file:
    #with open(storage + "tmp.json", 'r+') as file:
        file_data = json.load(file)
        file_data.append(entry)
        file.seek(0)
        json.dump(file_data, file)
    #os.rename(storage + "tmp.json",storage)

#unused
def readJson():
    with open(storage, 'r') as file:
        file_data = json.load(file)
        for x in range(len(file_data)):
            print(file_data[x]["code"])

#unused
def deleteFromJson():
    while True:
        insert = input()
        print(insert)
        with open(storage, 'r') as file:
            file_data = json.load(file)
            checkIfExists = len([obj for obj in file_data if (obj['code'] == insert)])
            print('Found ' + str(checkIfExists))
            if checkIfExists == 1:
                filtered_data = [obj for obj in file_data if (obj['code'] != insert)]
                with open(storage, 'w') as file:
                    json.dump(filtered_data, file)
                    print('Welcome ' + str(insert))
            elif checkIfExists == 0:
                print('No entry found for ' + str(insert) + '. Please check in at the Magic Mirror first')

#using tkinter input
def deleteFromJsonUsingInput(insert):
    print(insert)
    while True:
        with open(storage, 'r') as file:
            file_data = json.load(file)
            checkIfExists = len([obj for obj in file_data if (obj['code'] == insert)])
            print('Found ' + str(checkIfExists))
            if checkIfExists == 1:
                filtered_data = [obj for obj in file_data if (obj['code'] != insert)]
                with open(storage + "tmp", 'w') as file:
                # with open(storage, 'w') as file:
                    json.dump(filtered_data, file)
                    # return(True) #moved out
                os.rename(storage + "tmp",storage)
                return(True)
            elif checkIfExists == 0:
                return(False)

# keep file_data as the one to be edited, but iterate through a cloned list
def deleteExpiredRecords():
    numdeleted = 0
    with open(storage, 'r') as file:
        file_data = json.load(file)

    with open(storage, 'r') as file:
        clone_data = json.load(file)
        for x in range(len(clone_data)):
            codeobj = clone_data[x]["code"]
            datetimeobj = clone_data[x]["timestamp"]
            properdtobj = datetime.strptime(datetimeobj, '%Y-%m-%d %H:%M:%S.%f')
            timeBetweenEntry = (datetime.now() - properdtobj)

            if timeBetweenEntry.total_seconds() > interval:
                file_data = [obj for obj in file_data if (obj['code'] != codeobj)]
                numdeleted += 1

    # with open(storage, 'w') as file:
    with open(storage + "tmp", 'w') as file:
        json.dump(file_data, file)
        print("Number of entries deleted: " + str(numdeleted)) #debug
    os.rename(storage + "tmp",storage)
