#!/usr/bin/python

import smbus
import time

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
        write_byte(0x20, 0x27) # Power on, XYZ enabled
        write_byte(0x23, 0x80) # Continuous update
        write_byte(0x1F, 0x60) # Enable temperature
    
        time.sleep(1)

        x_out_L = read_byte(0x28) 
        x_out_H = read_byte(0x29)
        y_out_L = read_byte(0x2A) 
        y_out_H = read_byte(0x2B)
        z_out_L = read_byte(0x2C) 
        z_out_H = read_byte(0x2D)
    
        x_out = convert_data(x_out_L, x_out_H)
        y_out = convert_data(y_out_L, y_out_H)
        z_out = convert_data(z_out_L, z_out_H)

        temp_stat = read_byte(0x07)
        temp_L = read_byte(0x0C)
        temp_H = read_byte(0x0D)
        temp = convert_data(temp_L, temp_H)
        
        print('Sweet bruhh : ' + str(x_out) + ' , y : ' + str(y_out) + ' , z :' + str(z_out))
        print('Is it cold? ' + str(temp_stat))