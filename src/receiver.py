from API_network import initReceiver

topics = [
    "PalomAlert/test",
    "PalomAlert/acc/shake",
    "PalomAlert/acc/running",
    "PalomAlert/comp/open",
    "PalomAlert/comp/running",
    "PalomAlert/temp/change",
    "PalomAlert/temp/running",
    "PalomAlert/calibration/ok",
    "PalomAlert/calibration/retry"
]

initReceiver(topicList=topics ,clientID="palomalert",qos=2)