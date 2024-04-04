# Brian Lesko 
# Run this file on the mobile robot

import arduino as ard
import socket

def main():

    # Set up the serial connection 
    port = '/dev/tty'
    # on mac in terminal: 'ls /dev/tty.*' to find the port manually
    # on linux in terminal: 'ls /dev/tty*' to find the port manually or 'dmesg | grep tty' to find the port manually
    try: 
        BAUD = 9600
        my_arduino = ard.arduino(port,BAUD,.1)
        print(f"Connection to {port} successful")
    except Exception as e:
        print("Could not connect to arduino")

    # Set up the UDP connection
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #self.server.bind((self.IP, 12345))
    #self.log_and_serial_send(f'Successfully Created a server at {self.IP}')

    while True:
        # Receive UDP Signal
        data, addr = my_socket.recvfrom(1024) # buffer size is 1024 bytes
        if data:
            new_data = data.decode("utf-8")
            print("received: %s" % new_data)
        #except Exception as e:
        #    print("Error occurred while receiving the UDP signal.")


        # Send Serial Signal 
        #try:
        #    my_arduino.send('throttle:'+str(power))
        #    my_arduino.send('servo:'+str(angle))
        #except Exception as e:
        #    print("Error occurred while sending the serial signal.")

main()
