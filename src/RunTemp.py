import smbus
import time
import math
from API_network import send, initSender

bus = smbus.SMBus(1)
address = 0x18

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adrL, adrH):
        high = bus.read_byte_data(address, adrH)
        low = bus.read_byte_data(address, adrL)
        val = (high << 8) + low
        return val

def read_word_2c(adrL, adrH):
        val = read_word(adrL, adrH)
        if (val >= 0x8000):
                return -((65535 - val) + 1)
        else:
                return val

def write_byte(adr, value):
    bus.write_byte_data(address, adr, value)
    
def Run(tempData):
        offset = 10                             # Offset neeeded to convert temperatures to celcius
        mean = tempData[0] + offset                 # Conversion to celcius
        count = 60                              # Count allows us to send a 'running' message ~1 a minute
        tolerance = 10                           # Tolerance, the variation of temperature before a message is sent
        client = initSender("PalomAlert/temp")
        sendMsg = True                          # Allow to send message
        countChange = 0

        while True:

                # Reading temperature and converting to celcius
                temp = read_word_2c(0x0C, 0x0D)
                temp = temp >> 6
                temp = temp + offset              


                if ((temp < (mean - tolerance/2) or temp > (mean + tolerance)) and sendMsg) or countChange>=60:
                        count = 60              # Ensures 'running' message is sent after the temperature returns to normal
                        countChange = 0
                        sendMsg = False

                        payload = {
                                "temp" : temp,
                                "ts" : time.time()       # Send timestamp and current temperature
                        }
                        send(client, payload, "PalomAlert/temp/change", qos=2)
                        time.sleep(3)           # To ensure messages aren't being sent at too high a frequency

                # Checking if temperature has stayed outside of range
                if (temp < (mean - tolerance/2) or temp > (mean + tolerance)) and (not sendMsg):
                        countChange = countChange + 1       # CountOpen ensures no repeat messages are sent until temperature remains changed for a minute

                elif (count >= 60):
                        send(client, str(temp), "PalomAlert/temp/running", qos =2) # Running message indicates to the server that the PalomAlert is live, and there is no intrusion happening
                        count = 0
                        sendMsg = True
                else:
                        countChange = 0
                        count = count + 1
                        sendMsg = True
                time.sleep(1)
