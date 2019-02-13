import smbus
import time
import math
from API_network import send, initSender

bus = smbus.SMBus(1)
client = initSender()

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
    
def Run(compData):
    mean = compData[0]
    stddev = compData[1]
    count = 0
    scale = 0.92
    offset = 4 * stddev

    x_out = read_word_2c(4,3) * scale
    z_out = read_word_2c(6,5) * scale

    bearing  = math.atan2(z_out, x_out) 
    if (bearing < 0):
        bearing += 2 * math.pi
    bearing = math.degrees(bearing)

    while True:
        x_out = read_word_2c(4,3) * scale
        z_out = read_word_2c(6,5) * scale

        bearing  = math.atan2(z_out, x_out) 
        if (bearing < 0):
            bearing += 2 * math.pi
        bearing = math.degrees(bearing)

        if bearing < (mean - offset) and bearing > (mean + offset):
            ts = time.ctime(int(time.time()))                   # Get timestamp
            send(client, ts, "PalomAlert/comp/open")
        if (count == 600):
            send(client, None, "PalomAlert/comp/running", qos =1)
            count = 0
        else:
            count = count + 1



        time.sleep(0.1)
