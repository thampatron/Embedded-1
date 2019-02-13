import smbus
import time
import math
from API_network import send, initSender

bus = smbus.SMBus(1)
client = initSender()
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
    mean = tempData[0]
    count = 0
    offset = 8


    while True:
        temp = read_word_2c(0x0C, 0x0D)
        temp = temp >> 6

        if temp < (mean - offset) and temp > (mean + offset):
                
                send(client, temp, "PalomAlert/temp/change")
        if (count == 600):
                send(client, None, "PalomAlert/temp/running", qos =1)
                count = 0
        else:
                count = count + 1

        time.sleep(0.1)
