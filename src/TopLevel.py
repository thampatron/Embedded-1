#!/usr/bin/python

import Calibrate
import RunAcc
import RunCompass
import RunTemp
from threading import Thread
from API_network_callbacks import awayFromHome


        
def main():
    global awayFromHome
    awayFromHome = False
    print("Top Level running")
    threads = []
    calibrated = False


    # Calibration Loop
    
    while calibrated == False:
        Readings = Calibrate.Calibrate()
        calibrated = Calibrate.Check(Readings)


    # Once calibrated, a thread is generated for each component

    threadComp = Thread(target=RunCompass.Run, args=(Readings["comp"],))
    threadAcc = Thread(target=RunAcc.Run)
    threadTemp = Thread(target=RunTemp.Run, args=(Readings["temp"],))

    threadComp.daemon = True    # Setting daemon flag to True forces the threads 
    threadAcc.daemon = True     # to terminate once the main program does
    threadTemp.daemon = True

    threads.append(threadComp)
    threads.append(threadAcc)
    threads.append(threadTemp)

    # Run the threads

    threadComp.start()
    threadAcc.start()
    threadTemp.start()

    # Keep the program running as to not terminate the daemonic threads
    while True:
        pass

if __name__ == "__main__":
    main()