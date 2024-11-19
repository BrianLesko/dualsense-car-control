# Brian Lesko 
# Run this file on the mobile robot, it will relay the UDP signal to the arduino over the serial USB connection

import arduino as ard
import socket
from get_ip import get_ip_address
from dualsense import wirelessDualSense
import numpy as np

def main():

    # Set up the serial connection 
    port = '/dev/ttyACM0'
    # on mac in terminal: 'ls /dev/tty.*' to find the port manually
    # on linux in terminal: 'ls /dev/tty*' to find the port manually or 'dmesg | grep tty' to find the port manually
    try: 
        BAUD = 9600
        my_arduino = ard.arduino(port,BAUD,.1)
        print(f"Connection to {port} successful")
    except Exception as e:
        print("Could not connect to arduino")
    ds = wirelessDualSense(1356, 3302)
    print(f"Waiting for control signal...")

    powers = []
    window_size = 10
    while True:
        ds.receive()
        ds.updateThumbsticks()
        ds.updateTriggers()

        # Button Control
        power = 0
        if abs(ds.L2) > 1:
            power = -ds.L2 
        if abs(ds.R2) > 1:
            power = int(np.interp(ds.R2,[0,255],[0,100])) # calibrated at 

        # Joystick control 
        angle = 95
        if abs(ds.RX) > 0.1:
            angle = int(np.interp(ds.RX,[-180,180],[45,145]))

        # Boost Button with Dpad up 
        maxpower = 97
        set_throttle = 95.5
        if ds.DpadUp == True: 
            maxpower = 105
            set_throttle = 97

        # Power Calibration, accounds for the ESC being terrible at low speeds.
        normalized_power = power
        #power = int(np.interp(power,[0,100],[85,105])) # calibrated at 
        if normalized_power > 0 and normalized_power < 80: 
            count_94 = sum(1 for x in powers if x == set_throttle)
            max_94_count = int(window_size * (max(normalized_power,20) / 100))
            if count_94 < max_94_count:
                power = set_throttle
            else:
                power = 80
        else:
            power = int(np.interp(normalized_power,[0,100],[90,maxpower]))
        powers.append(power)
        if len(powers) > 9: powers.pop(0) 

        throttle = 'throttle:'+str(power)
        steering = 'servo:'+str(angle)
        # Send the command via serial
        try:
            my_arduino.send(throttle.encode())
            my_arduino.send(steering.encode())
        except Exception as e:
            print("Error occurred while sending the serial signal.")

main()
