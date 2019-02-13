import time
from API_network import *

def getMsg(n):
    compass = random.randint(1,360)
    acc_x = random.randint(1,50)
    acc_y = random.randint(1,50)
    acc_z = random.randint(1,50)

    payload = {
        "msg no" : str(n),
        "compass" : str(compass),
        "acc" : {
        "acc_x" : str(acc_x),
        "acc_y" : str(acc_y),
        "acc_z" : str(acc_z)
        }
    }

    return payload





client = initSender()
for i in range(100):


    print("sending message ", i)
    message = getMsg(i)
    send(client, message)
    time.sleep(2)

print("all messages have been sent")













