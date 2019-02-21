import time
import random
from API_network import *

def getMsg(n):
    compass = random.randint(1,360)
    acc_x = random.randint(1,50)
    acc_y = random.randint(1,50)
    acc_z = random.randint(1,50)

    payload = {
        # "compass" : str(compass),
        # "acc" : {
        #     "acc_x" : str(acc_x),
        #     "acc_y" : str(acc_y),
        #     "acc_z" : str(acc_z),
        # }
        "msg no" : str(n)
    }

    return payload





client = initSender(clientID="swag99_send")
for i in range(10000):
    print("sending message ", i)
    message = getMsg(i)
    send(client, message, qos=2)
    time.sleep(0.5)

print("all messages have been sent")













