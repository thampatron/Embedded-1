#!/usr/bin/python

import smbus
import time
from API_network import send, initSender
from statistics import stdev


bus = smbus.SMBus(1)
client = initSender()
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
    count = 0

    while True:
        for i in range(0,10):
            z_out_L = read_byte(0x2C) 
            z_out_H = read_byte(0x2D)
            z_out = convert_data(z_out_L, z_out_H)

            z_outs.append(z_out)
        deviation = stdev(z_outs)
        z_outs.clear()
        if deviation > 400:
            ts = time.ctime(int(time.time()))           # Get timestamp
            send(client, ts, "PalomAlert/acc/shake")
        if (count == 600):
            send(client, None, "PalomAlert/acc/running", qos =1)
            count = 0
        else:
            count = count + 1
        time.sleep(0.1)
