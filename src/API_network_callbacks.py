import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import time
import signal
import subprocess
import os

STATUS_FILE = "./status.json"
STATUS_LOCK = "./lock_status.txt"
LOG_FILE = "./log.txt"
LOG_LOCK = "./lock_log.txt"
TEMPLATE_FILE = "./template.json"
awayFromHome = False

def update_log(status, topic):
    # prepare data
    data = {}
    data["timeStamp"] = time.ctime(status["lastFileUpdate"])
    data["topic"] = topic
    data["status"] = status
    # wait for resource to be freed
    while os.path.isfile(LOG_LOCK):
        pass
    # add lock
    lock = open(LOG_LOCK, "w")
    lock.close()
    while os.path.isfile(LOG_LOCK) is False:
        pass
    # append data to log
    update = json.dumps(data)
    JSONfile = open(LOG_FILE, "a")
    JSONfile.write(update)
    JSONfile.write("\n")
    JSONfile.close()
    # remove lock
    os.remove(LOG_LOCK)
    while os.path.isfile(LOG_LOCK):
        pass  


def read_JSON(filename):
    # check if stats file is there 
    if os.path.isfile(filename):
        #wait for resource to be freed
        while os.path.isfile(STATUS_LOCK):
            pass
        # read file
        JSONfile = open(filename, "r+")
        data = json.load(JSONfile)
        JSONfile.close()
        return data
    # otherwise copy data from template
    else:
        with open(TEMPLATE_FILE, 'r') as myfile:
            templateData=myfile.read().replace('\n', '')
        return templateData



def write_JSON(filename, data):
    # add lock
    lock = open(STATUS_LOCK, "w")
    lock.close() 
    while os.path.isfile(STATUS_LOCK) is False:
        pass     
    # write file
    update = json.dumps(data)
    JSONfile = open(filename, "w")
    JSONfile.write(update)
    JSONfile.close()
    # remove lock
    os.remove(STATUS_LOCK)
    while os.path.isfile(STATUS_LOCK):
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
        update_log(status, topic)

    elif topic == "PalomAlert/acc/running":
        status["accelerometer"]["lastUpdate"] = currTime
        status["accelerometer"]["isShook"] = "no"

    elif topic == "PalomAlert/comp/open":
        status["compass"]["lastUpdate"] = currTime
        status["compass"]["lastIntrusion"] = payload
        status["compass"]["isOpen"] = "yes"
        update_log(status, topic)

    elif topic == "PalomAlert/comp/running":
        status["compass"]["lastUpdate"] = currTime
        status["compass"]["isOpen"] = "no"

    elif topic == "PalomAlert/temp/change":
        status["thermometer"]["lastUpdate"] = currTime
        status["thermometer"]["lastEmergency"] = payload["ts"]
        status["thermometer"]["temperature"] = payload["temp"]
        update_log(status, topic)

    elif topic == "PalomAlert/temp/running":
        status["thermometer"]["lastUpdate"] = currTime
        status["thermometer"]["temperature"] = payload

    elif topic == "PalomAlert/calibration/ok":
        status["sensorCalibration"]["lastUpdate"] = currTime
        status["sensorCalibration"]["status"] = "ok"

    elif topic == "PalomAlert/calibration/retry":
        status["sensorCalibration"]["lastUpdate"] = currTime
        status["sensorCalibration"]["status"] = "retrying"

    elif topic == "PalomAlert/run":
        process = subprocess.Popen("python3 TopLevel.py", stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid)        # Run the PalomAlert as parent of a process group

    elif topic == "PalomAlert/halt":
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)  # Send the signal to kill the whole process group
    
    # write JSON
    write_JSON(STATUS_FILE, status)
