from API_network import send, initSender


client = initSender("PalomAlert/halt")

send(client, None, "PalomAlert/halt", qos=2)