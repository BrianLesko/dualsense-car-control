##################################################################
# Brian Lesko
# 4/3/2024
# Run on your base station. Connect to a dualsense controller and send a UDP Signal to a the Car's IP address

import streamlit as st
import math
import time
import numpy as np
import matplotlib.pyplot as plt
import dualsense # DualSense controller communication
import customize_gui # streamlit GUI modifications
import ethernet as eth # UDP/IP communication
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
    IP = '172.20.10.3'
    Trigger = st.empty()
    while True:
        with Status: st.write("Reading Controller")
        ds.receive()
        ds.updateTriggers()
        ds.updateThumbsticks()

        # Button Control
        power = 90
        if abs(ds.L2) > 1:
            power = -ds.L2 
        if abs(ds.R2) > 1:
            #amplitude = 8
            #offset = 85 + amplitude
            #frequency = 2
            #power = amplitude * math.sin(2 * math.pi * frequency * time.time()) + offset
            power = ds.R2
            with Trigger: st.write(ds.R2)

        # Joystick control 
        angle = 95
        if abs(ds.RX) > 0.1:
            with Status: st.write(ds.RX)
            angle = int(np.interp(ds.RX,[-180,180],[45,145]))

        # Power Calibration
        power = int(np.interp(power,[0,255],[85,105])) # calibrated at 
        with Sending: st.write(f"Sending: {power}")

        throttle = 'throttle:'+str(power)
        steering = 'servo:'+str(angle)
        # Send the command via UDP/IP
        with Message: st.write("Sending UDP Signal")
        try:
            if 'client' not in st.session_state:
                st.session_state.client = eth.ethernet("client", IP, 12345)
            st.session_state.client.s.sendto(throttle.encode(), (IP, 12345))
            st.session_state.client.s.sendto(steering.encode(), (IP, 12345))
        except Exception as e:
            with Message: 
                st.write(e)
                #st.error("Error occurred while sending the UDP signal. Make sure the IP address and port are correctly set in the python script.")

        with Status: st.write("Replotting")
        # Update a plot with the current Input signal, Power.
        with image_spot:
            data.set_data([0], [power])  # Provide sequences for x and y coordinates
            history.append(power)
            ax.set_ylim([55, 125])
            st.pyplot(fig)

main()