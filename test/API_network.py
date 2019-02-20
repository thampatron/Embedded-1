import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import random



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




# API initialize client for receiving
# *** PROCESS-BLOCKING FUNCTION ***
def initReceiver(topic="PalomAlert/test", clientID = "PalomAlertReceive"):
    # brokerAddr = "test.mosquitto.org"
    brokerAddr = "broker.hivemq.com"
    client = mqtt.Client(clientID)
    client.on_message=on_message        #attach function to callback
    # CONSIDER IMPLEMENTING
    # message_callback_add(sub, callback)
    # sub
    #     the subscription filter to match against for this callback. Only one callback may be defined per literal sub string
    # callback
    #     the callback to be used. Takes the same form as the on_message callback.
    # 
    # 
    portNo = 1883 ######## NO TLS --> TODO
    client.connect(brokerAddr, port=portNo)
    client.subscribe(topic, qos=1)
    client.loop_forever()




def on_message(client, userdata, message):
    json_in = str(message.payload.decode("utf-8"))
    print("message received ")
    print(json.loads(json_in))
    # print("\tmessage topic=",message.topic)
    # print("\tmessage qos=",message.qos)
    # print("\tmessage retain flag=",message.retain)
