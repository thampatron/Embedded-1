from API_network import send, initSender


client = initSender("PalomAlert/run")

send(client, None, "PalomAlert/run", qos=2)