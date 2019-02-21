from API_network import initReceiver

topics = [
    "PalomAlert/run",
    "PalomAlert/halt"
]

initReceiver(topicList=topics ,clientID="piLoma",qos=2) 
