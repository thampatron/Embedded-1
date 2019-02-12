import smbus
import time
import math
from statistics import stdev


bus = smbus.SMBus(1)

def read_byte(sensorAdr, adr):
        return bus.read_byte_data(sensorAdr, adr)

def read_word(sensorAdr, adrL, adrH):
        high = bus.read_byte_data(sensorAdr, adrH)
        low = bus.read_byte_data(sensorAdr, adrL)
        val = (high << 8) + low
        return val

def read_word_2c(sensorAdr, adrL, adrH):
        val = read_word(sensorAdr, adrL, adrH)
        if (val >= 0x8000):
                return -((65535 - val) + 1)
        else:
                return val

# def read_word_2c(sensorAdr, adrL, adrH = None):
#         val = read_word(sensorAdr, adrL)
#         if adrH is not None: 
#             val_H = read_word(sensorAdr, adrH)
#             val = val + (val_H >> 8)
#         if (val >= 0x8000):
#                 return -((65535 - val) + 1)
#         else:
#                 return val

def write_byte(sensorAdr, adr, value):
        bus.write_byte_data(sensorAdr, adr, value)

def convert_2_bearing(North, West):
        bearing  = math.atan2(North, West) 
        if (bearing < 0):
            bearing += 2 * math.pi
        val = math.degrees(bearing)
        return val
    
def Calibrate():
        bearings = []
        temps = []
        X_outs = []
        Y_outs = []
        Z_outs = []
        Readings = {
            "bearing" : [],
            "x" : [],
            "y" : [],
            "z" : [], 
            "temp" : []
        }
        means = []
        stds = []

        AccAddr = 0x18
        CompAddr = 0x1E
        scale = 0.92

        write_byte(CompAddr, 0x00, 0x70) # Set to 8 samples @ 15Hz - Comp
        write_byte(CompAddr, 0x01, 0x20) # 1.3 gain LSb / Gauss 1090 (default) - Comp
        write_byte(CompAddr, 0x02, 0x00) # Continuous sampling - Comp

        write_byte(AccAddr, 0x20, 0x27) # Power on, XYZ enabled - Acc
        write_byte(AccAddr, 0x23, 0x80) # Continuous update - Acc
        write_byte(AccAddr, 0x1F, 0xC0) # Enable temperature - Acc
    

        for i in range(0,100):
                time.sleep(0.1)

                # Read Compass
                Comp_X = read_word_2c(CompAddr, 0x04, 0x03) * scale
                # Comp_Y = read_word_2c(CompAddr, 0x08, 0x07) * scale
                Comp_Z = read_word_2c(CompAddr, 0x06, 0x05) * scale
                Bearing  = convert_2_bearing(Comp_Z, Comp_X)

                # Read Accelerometer
                Acc_X = read_word_2c(AccAddr, 0x28, 0x29)
                Acc_Y = read_word_2c(AccAddr, 0x2A, 0x2B)
                Acc_Z = read_word_2c(AccAddr, 0x2C, 0x2D)
                temp = read_word_2c(AccAddr, 0x0C, 0x0D)
                temp = temp >> 6


                bearings.append(Bearing)
                X_outs.append(Acc_X)
                Y_outs.append(Acc_Y)
                Z_outs.append(Acc_Z)
                temps.append(temp)
        
        means.append(sum(Readings["bearings"])/float(len(Readings["bearings"])))
        stds.append(stdev(Readings["bearings"]))
        
        means.append(sum(Readings["x"])/float(len(Readings["x"])))
        stds.append(stdev(Readings["x"]))

        means.append(sum(Readings["y"])/float(len(Readings["y"])))
        stds.append(stdev(Readings["y"]))

        means.append(sum(Readings["z"])/float(len(Readings["z"])))
        stds.append(stdev(Readings["z"]))

        means.append(sum(Readings["temp"])/float(len(Readings["temp"])))
        stds.append(stdev(Readings["temp"]))

        # print("Bearing : mean : " + str(Readings["bearings"][0]) + ", standard deviation : " + str(Readings["bearings"][1]))

        # print("X : mean : " + str(Readings["x"][0]) + ", standard deviation : " + str(Readings["x"][1]))

        # print("Y : mean : " + str(Readings["y"][0]) + ", standard deviation : " + str(Readings["y"][1]))

        # print("Z : mean : " + str(Readings["z"][0]) + ", standard deviation : " + str(Readings["z"][1]))
        
        # print("Temp : mean : " + str(Readings["temp"][0]) + ", standard deviation : " + str(Readings["temp"][1]))

        return Readings

def Check(Readings):
    response = 0
    if Readings["bearings"][1] > 0.5: 
        
        if response == "Again":
            return False

    if Readings["x"][1] > 220:
        # Send
        if response == "Again":
            return False

    if Readings["y"][1] > 220:
        # Send
        if response == "Again":
            return False

    if Readings["z"][1] > 220:
        # Send
        if response == "Again":
            return False

    if Readings["temp"][1] > 1.5:
        # Send
        if response == "Again":
            return False
    return True 