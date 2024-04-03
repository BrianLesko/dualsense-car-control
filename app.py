##################################################################
# Brian Lesko
# 1/29/2024
# Connect to a dualsense controller and send a UDP Signal to a certain IP address

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import dualsense # DualSense controller communication
import customize_gui # streamlit GUI modifications
from ethernet import ethernet as eth # This class contains the methods 
import arduino as ard
DualSense = dualsense.DualSense # this class contains methods to communicate with the DualSense controller
gui = customize_gui.gui() # this class contains methods to modify the streamlit GUI

def main():
    # Set up the app UI
    gui.clean_format(wide=True)
    gui.about(text = "This code implements...")
    st.title("Control Input")
    col1, col2, col3 = st.columns([1,4,1])
    with col2: image_spot = st.empty()
    Message = st.empty()
    Sending = st.empty()
    Incoming = st.empty()
    Status = st.empty()
    
    # Setting up the dualsense controller connection
    vendorID, productID = int("0x054C", 16), int("0x0CE6", 16)
    ds = DualSense(vendorID, productID)
    try: ds.connect()
    except Exception as e:
        st.error("Error occurred while connecting to Dualsense controller. Make sure the controller is wired up and the vendor and product ID's are correctly set in the python script.")

    # Set up the serial connection 
    port = '/dev/tty.usbmodem11301'
    try: 
        # on mac in terminal: 'ls /dev/tty.*' to find the port manually
        BAUD = 9600
        my_arduino = ard.arduino(port,BAUD,.1)
        with st.sidebar: st.write(f"Connection to {port} successful")
    except Exception as e:
        st.write("Could not connect to arduino")

    my_arduino.send(str(0))

    # Set up the plot
    fig, ax = plt.subplots()
    data, = ax.plot([],[],'o')
    ax.xaxis.set_visible(False)
    # Hide all spines in one line
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Control Loop
    history = []
    messages = []
    while True:
        with Status: st.write("Reading Controller")
        ds.receive()
        ds.updateTriggers()
        ds.updateThumbsticks()

        # Button Control
        power = 0
        if abs(ds.L2) > 4:
            power = -ds.L2
        if abs(ds.R2) > 4:
            power = ds.R2

        # Joystick control 
        angle = 95
        if abs(ds.LX) > 0.1:
            with Status: st.write(ds.LX)
            angle = int(np.interp(ds.LX,[-180,180],[55,130]))

        # Power Calibration
        power = int(np.interp(power,[-255,255],[50,120]))+5 # calibrated at 
        with Sending: st.write(f"Sending: {power}")

        # Send the command via serial message 
        #with Status: st.write("Sending Serial")
        try:
            my_arduino.send('throttle:'+str(power))
            my_arduino.send('servo:'+str(angle))
        except Exception as e:
            with Message: 
                st.write("Error occurred while sending the serial signal.")

        #with Status: st.write("Replotting")
        # Update a plot with the current Input signal, Power.
        with image_spot:
            data.set_data([0], [power])  # Provide sequences for x and y coordinates
            history.append(power)
            ax.set_ylim([70, 100])
            st.pyplot(fig)

main()