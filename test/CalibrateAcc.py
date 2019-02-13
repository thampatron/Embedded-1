#!/usr/bin/python

import smbus
import time
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
    
if __name__ == "__main__":
        temps = []
        x_outs = []
        y_outs = []
        z_outs = []

        write_byte(0x20, 0x27) # Power on, XYZ enabled
        write_byte(0x23, 0x80) # Continuous update
        write_byte(0x1F, 0xC0) # Enable temperature
    

        for i in range(0,100):
                time.sleep(0.1)

                x_out_L = read_byte(0x28) 
                x_out_H = read_byte(0x29)
                y_out_L = read_byte(0x2A) 
                y_out_H = read_byte(0x2B)
                z_out_L = read_byte(0x2C) 
                z_out_H = read_byte(0x2D)
                temp_L = read_byte(0x0C)
                temp_H = read_byte(0x0D)
    
                x_out = convert_data(x_out_L, x_out_H)
                y_out = convert_data(y_out_L, y_out_H)
                z_out = convert_data(z_out_L, z_out_H)
                temp = convert_data(temp_L, temp_H)
                temp = temp >> 6

                x_outs.append(x_out)
                y_outs.append(y_out)
                z_outs.append(z_out)
                temps.append(temp)
        
        x_out_mean = sum(x_outs)/float(len(x_outs))
        x_out_std = stdev(x_outs)

        y_out_mean = sum(y_outs)/float(len(y_outs))
        y_out_std = stdev(y_outs)

        z_out_mean = sum(z_outs)/float(len(z_outs))
        z_out_std = stdev(z_outs)

        temp_mean = sum(temps)/float(len(temps))
        temp_std = stdev(temps)

        print("X : mean : " + str(x_out_mean) + ", standard deviation : " + str(x_out_std))

        print("Y : mean : " + str(y_out_mean) + ", standard deviation : " + str(y_out_std))

        print("Z : mean : " + str(z_out_mean) + ", standard deviation : " + str(z_out_std))

        print("Temp : mean : " + str(temp_mean) + ", standard deviation : " + str(temp_std))
