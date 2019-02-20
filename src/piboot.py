from API_network import initReceiver

topics = [
    "PalomAlert/run",
    "PalomAlert/halt"
]

print("piBooted \n\n")

initReceiver(topicList=topics ,clientID="piLoma",qos=1) 
