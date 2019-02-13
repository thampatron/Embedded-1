import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import os
from API_network_callbacks import *



# API Initialize client for sending
def initSender(clientID = "PalomAlertSend"):
    # brokerAddr = "test.mosquitto.org"
    brokerAddr = "broker.hivemq.com"
    client = mqtt.Client(clientID)
    portNo = 1883 ######## NO TLS --> TODO
    client.connect(brokerAddr, port=portNo)
    return client



# API for sending a message
def send(client, msg, topic="PalomAlert/test", qos=0):
    pLoad = json.dumps(msg)
    client.publish(topic=topic, payload=pLoad, qos=qos)
    client.loop(10,20)




# API initialize client for receiving
# *** PROCESS-BLOCKING FUNCTION ***
def initReceiver(topicList=["PalomAlert/test"], clientID = "PalomAlertReceive", qos=1):
    # remove write lock if it was left by past receiver
    if os.path.isfile("./lock.txt"):
        os.remove("./lock.txt")
    # brokerAddr = "test.mosquitto.org"
    client = mqtt.Client(clientID)
    # Attach functions to topic-wise callbacks
    client.on_message = on_message
    # connect to broker
    brokerAddr = "broker.hivemq.com"
    portNo = 1883 ######## NO TLS --> TODO
    client.connect(brokerAddr, port=portNo)
    # subscribe to topics
    for topic in topicList:
        client.subscribe(topic, qos)

    client.loop_forever()




