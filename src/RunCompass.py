import smbus
import time
import math
from API_network import send, initSender

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
    
def convert_2_bearing(North, West):
        bearing  = math.atan2(North, West) 
        if (bearing < 0):
            bearing += 2 * math.pi
        val = math.degrees(bearing)
        return val

def isOutOfRange360(bearing, LThreshold, HThreshold):
        LThreshold = LThreshold % 360
        HThreshold = HThreshold % 360

        if(LThreshold < HThreshold):
                if (LThreshold < bearing and bearing < HThreshold):
                        return False
                else:
                        return True
        else:
                if(HThreshold < bearing and bearing < LThreshold):
                        return True
                else:
                        return  False




def Run(compData):
        mean = compData[0]
        count = 600                                     # Count allows us to send a 'running' message ~1 a minute
        countOpen = 0                                   # Set to alert if door is open for whole minute
        scale = 0.92                                    # Scale needed to convert to degrees
        offset = 0.9
        client = initSender("PalomAlert/comp")
        sendMsg = True                                  # Allow to send message

        while True:

                # Read compass data

                x_out = read_word_2c(4,3) * scale
                y_out = read_word_2c(8,7) * scale       # Read but unused - the sensor stops updating if left unread
                z_out = read_word_2c(6,5) * scale

                bearing  = convert_2_bearing(z_out, x_out)


                # Checking if door is open & a msg hasn't been sent yet or if door has been open for over a minute
                if (isOutOfRange360(bearing, mean - offset, mean + offset) and sendMsg ) or (countOpen>=600):
                        ts = time.time()                 # Get timestamp
                        send(client, ts, "PalomAlert/comp/open", qos=2)
                        time.sleep(3)                   # To ensure messages aren't being sent at too high a frequency
                        sendMsg = False
                        count = 600                     # Ensures 'running' message is sent after the door is closed
                        countOpen = 0           

                # Checking if door has stayed open
                if isOutOfRange360(bearing, mean - offset, mean + offset) and (not sendMsg):
                        countOpen = countOpen + 1       # CountOpen ensures no repeat messages are sent until the door has been open for a minute

                elif (count >= 600):
                        send(client, None, "PalomAlert/comp/running", qos=2)        # Running message indicates to the server that the PalomAlert is live, and there is no intrusion happening
                        count = 0
                        sendMsg = True
                else:
                        count = count + 1
                        countOpen = 0
                        sendMsg = True
                
                time.sleep(0.2)
