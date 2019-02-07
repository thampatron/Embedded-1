import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time

brokerAddr = "test.mosquitto.org"
portNo = 1883
topic = "aleSerena/test"

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    # print("\tmessage topic=",message.topic)
    # print("\tmessage qos=",message.qos)
    # print("\tmessage retain flag=",message.retain)




client = mqtt.Client("TestReceive")
client.on_message=on_message        #attach function to callback
client.connect(brokerAddr, port=portNo)
print("connection successful")
client.subscribe(topic, qos=1)
client.loop_start()    #start the loop
time.sleep(1000)
client.loop_stop()