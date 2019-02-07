import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time

brokerAddr = "test.mosquitto.org"
portNo = 1883
topic = "aleSerena/test"

client = mqtt.Client("TestSend")
client.connect(brokerAddr, port=portNo)

print("connection successful")

print("starting to send messages")
for i in range(100):
    print("sending message ", i)
    msg = "msg no. " + str(i) + " - " + str(time.time())
    client.publish(topic=topic, payload=msg, qos=0)
    # mqttLoop(2,10)
    time.sleep(2)

print("all messages have been sent")