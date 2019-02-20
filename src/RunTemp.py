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
        mean = tempData[0] + 10                 # Conversion to celcius
        count = 60
        offset = 4
        client = initSender("PalomAlert/temp")

        while True:
                temp = read_word_2c(0x0C, 0x0D)
                temp = temp >> 6

                temp = temp + 10                # Conversion to celcius


                if ( temp < (mean - offset) or temp > (mean + offset) ):
                        count = 60
                        payload = {
                                "temp" : temp,
                                "ts" : time.time()
                        }
                        send(client, payload, "PalomAlert/temp/change", qos=2)
                        time.sleep(3)           # To ensure messages aren't being sent at too high a frequency
                elif (count >= 60):
                        send(client, str(temp), "PalomAlert/temp/running", qos =2) # Running message indicates to the server that the PalomAlert is live, and there is no intrusion happening
                        count = 0
                else:
                        count = count + 1
                time.sleep(1)
