import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import time
import os

STATUS_FILE = "./status.json"



def read_JSON(filename):

    # check if stats file is there 
    # otherwise copy data from template
    if os.path.isfile(STATUS_FILE):
        #wait for resource to be freed
        while os.path.isfile("./lock.txt"):
            print("lock found")
        # read file
        JSONfile = open(filename, "r+")
        data = json.load(JSONfile)
        JSONfile.close()
        return data
    else:
        with open(TEMPLATE_FILE, 'r') as myfile:
            templateData=myfile.read().replace('\n', '')
        return templateData



def write_JSON(filename, data):
    # add lock
    lock = open("./lock.txt", "w")
    lock.close() 
    while os.path.isfile("./lock.txt") is False:
        pass     
    # write file
    update = json.dumps(data)
    JSONfile = open(filename, "w")
    JSONfile.write(update)
    JSONfile.close()
    # remove lock
    os.remove("./lock.txt")
    while os.path.isfile("./lock.txt"):
        pass



# DEFINE CALLBACK FUNCTIONS FOR RECEIVER

def on_message(client, userdata, message):
    # get current STATUS
    status = read_JSON(STATUS_FILE)
    # decode message payload
    payload = json.loads(str(message.payload.decode("utf-8")))
    currTime = int(time.time())
    # update JSON
    status["lastFileUpdate"] = currTime
    topic = str(message.topic)
    print("Message received. Topic: ", topic)

    if topic == "PalomAlert/test":
        print("Message received: ", payload)
        

    elif topic == "PalomAlert/acc/shake":
        status["accelerometer"]["lastUpdate"] = currTime
        status["accelerometer"]["lastIntrusion"] = payload
        status["accelerometer"]["isShook"] = "yes"

    elif topic == "PalomAlert/acc/running":
        status["accelerometer"]["lastUpdate"] = currTime
        status["accelerometer"]["isShook"] = "no"

    elif topic == "PalomAlert/comp/open":
        status["compass"]["lastUpdate"] = currTime
        status["compass"]["lastIntrusion"] = payload
        status["compass"]["isOpen"] = "yes"

    elif topic == "PalomAlert/comp/running":
        status["compass"]["lastUpdate"] = currTime
        status["compass"]["isOpen"] = "no"

    elif topic == "PalomAlert/temp/change":
        status["thermometer"]["lastUpdate"] = currTime
        status["thermometer"]["lastEmergency"] = payload["ts"]
        status["thermometer"]["temperature"] = payload["temp"]

    elif topic == "PalomAlert/temp/running":
        status["thermometer"]["lastUpdate"] = currTime
        status["thermometer"]["temperature"] = payload

    elif topic == "PalomAlert/calibration/ok":
        status["sensorCalibration"]["lastUpdate"] = currTime
        status["sensorCalibration"]["status"] = "ok"

    elif topic == "PalomAlert/calibration/retry":
        status["sensorCalibration"]["lastUpdate"] = currTime
        status["sensorCalibration"]["status"] = "retrying"
    
    # write JSON
    write_JSON(STATUS_FILE, status)
