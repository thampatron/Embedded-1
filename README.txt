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

# GENERAL DESCRIPTION OF SYSTEM

The system is divided into two main components:
1.  IoT device
2.  User interface

The device should start executing as soon as it is turned on.
It will start in 'listening mode' and it will wait to receive a 'run' message in order to start its normal operativity.



# HOW TO RUN THE SYSTEM

(NOTE: all the following instructions have to be followed from within the 'src' directory)

-   RUNNING THE IOT DEVICE
    1.  Power ON the device
    2.  From any other device, run script 'startDevice.py'.
        This will instruct the IoT device to start calibrating itself and sending messages about the system status.
    
-   RUNNING THE USER interface
    1. Execute      python3 palomAlert.py