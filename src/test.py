from API_network import send, initSender
import time


client = initSender("PalomAlert/run")

send(client, None, "PalomAlert/run", qos=2)

time.sleep(20)

send(client, None, "PalomAlert/halt", qos=2)

print("The test is complete!")