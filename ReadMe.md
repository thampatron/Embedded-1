# PalomAlert

Imperial College London  
EE3-24 Embedded Systems  
Coursework 1  

Authors:&nbsp;&nbsp;&nbsp;&nbsp;Jordi Laguarta Soler    jl9516@ic.ac.uk  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Mateo Sarjanovic        ms6616@ic.ac.uk  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Alessandro Serena       as6316@ic.ac.uk  
Website: https://jordilaguartasoler.wixsite.com/website  
Readme version: 1.5  
Date:           21 Feb 2019  

# How to run the system

(NOTE: all the following instructions have to be followed from within the 'src' directory)

-   Running the IoT device
    1.  Power ON the Raspberry Pi


-   Running the user interface
    1.  From any other device, run 'python3 palomAlert.py'. This will open the user interface.
    2.	On the UI, indicate that you are not home.
	    This will instruct the IoT device to start calibrating itself and sending messages about the system status.
    3.  If the UI does not say 'Connected', ssh into the Raspberry Pi and run script 'TopLevel.py'