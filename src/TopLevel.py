#!/usr/bin/python

import Calibrate
import RunAcc
import RunCompass
import RunTemp
from threading import Thread

awayFromHome = False
        
def main():
    print("Top Level running")
    threads = []
    calibrated = False
    
    while calibrated == False:
        Readings = Calibrate.Calibrate()
        calibrated = Calibrate.Check(Readings)

    threadComp = Thread(target=RunCompass.Run, args=(Readings["comp"],))
    threadAcc = Thread(target=RunAcc.Run)
    threadTemp = Thread(target=RunTemp.Run, args=(Readings["temp"],))

    threadComp.daemon = True    # Setting daemon flag to True forces the threads 
    threadAcc.daemon = True     # to terminate once the main program does
    threadTemp.daemon = True

    threads.append(threadComp)
    threads.append(threadAcc)
    threads.append(threadTemp)

    threadComp.start()
    threadAcc.start()
    threadTemp.start()

    while not awayFromHome:
        print("Pass")
        pass
    
    print("Exiting Top Level")
    return

if __name__ == "__main__":
    main()