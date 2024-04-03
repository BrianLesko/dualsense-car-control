# Brian Lesko 
# Run this file on the mobile robot

import arduino as ard

def main():
    # Set up the serial connection 
    port = '/dev/tty.usbmodem11301'
    try: 
        # on mac in terminal: 'ls /dev/tty.*' to find the port manually
        BAUD = 9600
        my_arduino = ard.arduino(port,BAUD,.1)
        with st.sidebar: st.write(f"Connection to {port} successful")
    except Exception as e:
        print("Could not connect to arduino")

    my_arduino.send(str(0))


    while True:
        # Receive UDP Signal

        # Send Serial Signal 
        try:
            my_arduino.send('throttle:'+str(power))
            my_arduino.send('servo:'+str(angle))
        except Exception as e:
            with Message: 
                print("Error occurred while sending the serial signal.")
