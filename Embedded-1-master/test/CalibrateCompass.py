import smbus
import time
import math
from statistics import stdev

bus = smbus.SMBus(1)

address = 0x1e

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
    
if __name__ == "__main__":
    write_byte(0x00, 0x70) # Set to 8 samples @ 15Hz - Comp
    write_byte(0x01, 0x20) # 1.3 gain LSb / Gauss 1090 (default) - Comp
    write_byte(0x02, 0x00) # Continuous sampling - Comp

    scale = 0.92
    Bearings = []

    for i in range(0,100):
        time.sleep(0.1)
        x_out = read_word_2c(4,3) * scale
        y_out = read_word_2c(8,7) * scale
        z_out = read_word_2c(6,5) * scale


    
        bearing  = math.atan2(z_out, x_out) 
        if (bearing < 0):
            bearing += 2 * math.pi
        Bearings.append(math.degrees(bearing))
    
    meanPos = sum(Bearings)/float(len(Bearings))
    deviation = stdev(Bearings)

    print("Mean position : " + str(meanPos) + ", standard deviation : " + str(deviation))
