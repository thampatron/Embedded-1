import smbus
import time
import math
from API_network import send, initSender
from statistics import stdev


bus = smbus.SMBus(1)

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
            "comp" : [],
            "x" : [],
            "y" : [],
            "z" : [], 
            "temp" : []
        }

        AccAddr = 0x18       # I2C addresses for the sensors
        CompAddr = 0x1E

        scale = 0.92         # Needed to convert compass readings to degrees, comes from the LSB gain

        write_byte(CompAddr, 0x00, 0x70)        # Set frequency to 15 Hz- Compass
        write_byte(CompAddr, 0x01, 0x20)        # 1.3 gain LSb / Gauss 1090 (default) - Compass
        write_byte(CompAddr, 0x02, 0x00)        # Continuous sampling - Compass

        write_byte(AccAddr, 0x20, 0x47)         # Power on, XYZ enabled, 50 Hz - Accelerometer
        write_byte(AccAddr, 0x23, 0x80)         # Continuous update - Accelerometer
        write_byte(AccAddr, 0x1F, 0xC0)         # Enable temperature - Accelerometer
    

        for i in range(0,100):
                time.sleep(0.05)

                # Read Compass
                Comp_X = read_word_2c(CompAddr, 0x04, 0x03) * scale
                Comp_Y = read_word_2c(CompAddr, 0x08, 0x07) * scale
                Comp_Z = read_word_2c(CompAddr, 0x06, 0x05) * scale
                Bearing  = convert_2_bearing(Comp_Z, Comp_X)
                # Read Accelerometer  ----- No need to calibrate Accelerometer, running to ensure door stays static
                Acc_X = read_word_2c(AccAddr, 0x28, 0x29)
                Acc_Y = read_word_2c(AccAddr, 0x2A, 0x2B)
                Acc_Z = read_word_2c(AccAddr, 0x2C, 0x2D)

                # -- Temp needs to calibrate
                temp = read_word_2c(AccAddr, 0x0C, 0x0D)
                temp = temp >> 6


                bearings.append(Bearing)
                X_outs.append(Acc_X)
                Y_outs.append(Acc_Y)
                Z_outs.append(Acc_Z)
                temps.append(temp)

        # Adding the calibration readings to the Readings dict
        
        Readings["comp"].append(sum(bearings)/float(len(bearings)))
        Readings["comp"].append(stdev(bearings))

        Readings["x"].append(sum(X_outs)/float(len(X_outs)))
        Readings["x"].append(stdev(X_outs))

        Readings["y"].append(sum(Y_outs)/float(len(Y_outs)))
        Readings["y"].append(stdev(Y_outs))

        Readings["z"].append(sum(Z_outs)/float(len(Z_outs)))
        Readings["z"].append(stdev(Z_outs))

        Readings["temp"].append(sum(temps)/float(len(temps)))
        Readings["temp"].append(stdev(temps))

        return Readings

def Check(Readings):
        client = initSender("PalomAlert/check")

        # This function checks whether the door was static during calibration

        if (Readings["comp"][1] > 0.5 or Readings["x"][1] > 220) or (Readings["y"][1] > 220 or (Readings["z"][1] > 220 or Readings["temp"][1])) > 1.5:
                send(client, None, "PalomAlert/calibration/retry", qos=2)
                return False
        else:
                send(client, None, "PalomAlert/calibration/ok", qos=2)
                return True 