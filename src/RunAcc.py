#!/usr/bin/python

import smbus
import time
from API_network import send, initSender
from statistics import stdev


bus = smbus.SMBus(1)
address = 0x18

def read_byte(adr):
        return bus.read_byte_data(address, adr)

def read_word(adr):
        high = bus.read_byte_data(address, adr)
        low = bus.read_byte_data(address, adr+1)
        val = (high << 8) + low
        return val

def read_word_2c(adr):
        val = read_word(adr)
        if (val >= 0x8000):
                return -((65535 - val) + 1)
        else:
                return val

def write_byte(adr, value):
        bus.write_byte_data(address, adr, value)

def convert_data( dataL, dataH):
        Acc = dataH*256 + dataL
        if Acc > 32767:
                Acc -= 65536
        return Acc
    
def Run():
    z_outs = []
    count = 50*60                               # Count allows us to send a 'running' message ~1 a minute
    client = initSender("PalomAlert/acc")

    while True:
        for i in range(0,30):                   # The PalomAlert takes the standard deviation over the past 30 readings in order to tell whether the door is being shook - raw readings were too erratic to be used reliably
                z_out_L = read_byte(0x2C) 
                z_out_H = read_byte(0x2D)
                z_out = convert_data(z_out_L, z_out_H)

                z_outs.append(z_out)
        deviation = stdev(z_outs)
        z_outs.clear()                          # Clear the array to ensure next reading is correct

        if (deviation > 1000):
                count = 50*60                   # To indicate door isn't being shook again
                ts = time.time()                # Get timestamp
                send(client, ts, "PalomAlert/acc/shake", qos=2)
                time.sleep(3.5)                  # To ensure messages aren't being sent at too high a frequency

        elif (count >= 50*60):
                send(client, None, "PalomAlert/acc/running", qos =2)   # Running message indicates to the server that the PalomAlert is live, and there is no intrusion happening
                count = 0
        else:
                count = count + 1
        time.sleep(0.02)
