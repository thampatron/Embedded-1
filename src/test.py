from API_network import send, initSender
import time


client = initSender("PalomAlert/run")

send(client, None, "PalomAlert/run", qos=1)

time.sleep(20)

send(client, None, "PalomAlert/halt", qos=1)

print("The test is complete!")