Imperial College London
EE3-24 Embedded Systems
Coursework 1

## PALOMALERT ##

Authors:    Alessandro Serena       as6316@ic.ac.uk
            Jordi Laguarta Soler    jl9516@ic.ac.uk
            Mateo Sarjanovic        ms6616@ic.ac.uk

Readme version: 1.4
Date:           20 Feb 2019

#####################################################

# HOW TO RUN THE SYSTEM

(NOTE: all the following instructions have to be followed from within the 'src' directory)

-   RUNNING THE IOT DEVICE
    1.  Power ON the device
    2.  From any other device, run 'python3 palomAlert.py'. This will open the user interface.
    3.	On the UI, indicate that you are not home.
	This will instruct the IoT device to start calibrating itself and sending messages about the system status.
    4.  If the system has not started, ssh into the Pi and run script 'src/TopLevel.py'