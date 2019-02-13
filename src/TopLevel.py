#!/usr/bin/python

import Calibrate
import RunAcc
import RunCompass
import RunTemp
from threading import Thread
        
def main():
    threads = []
    calibrated = False

    while calibrated == False:
        Readings = Calibrate.Calibrate()
        calibrated = Calibrate.Check(Readings)

    threadComp = Thread(target=RunCompass.Run, args=Readings["comp"])
    threadAcc = Thread(target=RunAcc.Run)
    threadTemp = Thread(target=RunTemp.Run, args=Readings["temp"])

    threads.append(threadComp)
    threads.append(threadAcc)
    threads.append(threadTemp)

    threadComp.start()
    threadAcc.start()
    threadTemp.start()

if __name__ == "__main__":
    main()