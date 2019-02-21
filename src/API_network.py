import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import os
from API_network_callbacks import *
import ssl

TLS_CERTIFICATE = "./certs/m2mqtt_ca.crt"


def initConnect(client, tls = False):
    # Send messages over HTTPS
    if tls:
        brokerAddr = "ee-estott-octo.ee.ic.ac.uk"
        portNo = 8080
        client.tls_set(TLS_CERTIFICATE, tls_version=ssl.PROTOCOL_TLSv1_2)
        client.tls_insecure_set(True)
        client.connect(brokerAddr, port=portNo)

    # Send messages over MQTT
    else:
        brokerAddr = "broker.hivemq.com"
        portNo = 1883
        client.connect(brokerAddr, port=portNo)

    print("Connected.")
    return client

# API Initialize client for sending
def initSender(clientID = "PalomAlertSend", tls = False):
    client = mqtt.Client(clientID)
    client = initConnect(client, tls)
    return client



# API for sending a message
def send(client, msg, topic="PalomAlert/test", qos=0):
    pLoad = json.dumps(msg)
    client.publish(topic=topic, payload=pLoad, qos=qos)
    client.loop(10,20)




# API initialize client for receiving
# *** PROCESS-BLOCKING FUNCTION ***
def initReceiver(topicList=["PalomAlert/test"], clientID = "PalomAlertReceive", qos=2, tls = False):
    # remove write lock if it was left by past receiver
    if os.path.isfile(LOG_LOCK):
        os.remove(LOG_LOCK)
    if os.path.isfile(STATUS_LOCK):
        os.remove(STATUS_LOCK)
    client = mqtt.Client(clientID)
    # Attach functions to topic-wise callbacks
    client.on_message = on_message
    # connect to broker
    client = initConnect(client, tls)
    # subscribe to topics
    for topic in topicList:
        client.subscribe(topic, qos)

    client.loop_forever()




