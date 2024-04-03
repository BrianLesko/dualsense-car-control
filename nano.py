# Brian Lesko
# Arduino Nano Esp 32 - Micropython
# 12/2023

from machine import Pin, PWM, ADC
import network
import socket
import time

class nano:

    def __init__(self):
        self.log = []
        self.wlan = network.WLAN(network.STA_IF) # Connect to wifi 
        # Networking
        self.IP = None
        self.client_address = None 
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

    def do_connect(self):
        if self.wlan.isconnected() == False:
            self.log_and_serial_send("Attempting to connect to wifi")
            self.wlan.active(True)
            if not self.wlan.isconnected():
                SSID = 'Lesko'
                self.wlan.connect(SSID, '12081999')
                start_time = time.time()  # Record the start time
                timeout = 5  # Set the timeout duration in seconds
                while not self.wlan.isconnected():
                    if time.time() - start_time > timeout:
                        break
            if self.wlan.isconnected():
                self.log_and_serial_send(f'Successfully connected to {SSID}')
                self.IP = str(self.wlan.ifconfig()[0])
                self.server.bind((self.IP, 12345))
                self.log_and_serial_send(f'Successfully Created a server at {self.IP}')
            else:
                self.log_and_serial_send('Failed to connect within the timeout period')
            return 
        if self.wlan.isconnected() == True:
            return
        
    def log_and_serial_send(self, message):
        self.log.append(message)
        self.serial_send(message)
        
    def serial_send(self,message):
        print(message)

nno = nano()
from machine import Pin, PWM, ADC

pwm = PWM(Pin(13))
pwm.freq(1000) # 1000 times a second

while True:
    steps = 0
    nno.do_connect()
    try: 
        data, addr = nno.server.recvfrom(1024) # buffer size is 1024 bytes
        new_data = 1000*int(abs(round(float(data.decode()), 0)))
        print("received: %s" % new_data)
        pwm.duty_u16(new_data)

    except: continue