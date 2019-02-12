import Calibrate
import RunAcc
import RunCompass
import RunTemp
from thread import start_new_thread
        
def main():

    call = False

    while call == False:
        Readings = Calibrate.Calibrate()
        call = Calibrate.Check(Readings)

    start_new_thread(RunAcc.Run,)
    start_new_thread(RunCompass.Run, (Readings["comp"],))
    start_new_thread(RunTemp.Run, (Readings["temp"],))


if __name__ == "__main__":main()