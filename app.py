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
    Incoming = st.empty()
    Status = st.empty()
    RawPower = st.empty()
    Power = st.empty()
    AvgPower = st.empty()

    
    # Setting up the dualsense controller connection
    vendorID, productID = int("0x054C", 16), int("0x0CE6", 16) # these are probably good
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
    IP = '10.42.0.1'  # EDIT THIS 
    Trigger = st.empty()
    window_size = 10  # Number of recent powers to track
    powers = []
    while True:
        with Status: st.write("Reading Controller")
        ds.receive()
        ds.updateTriggers()
        ds.updateThumbsticks()
        ds.updateDpad()

        # Button Control
        power = 0
        if abs(ds.L2) > 1:
            power = -ds.L2 
        if abs(ds.R2) > 1:
            power = ds.R2
            power = int(np.interp(power,[0,255],[0,100])) # calibrated at 

        # Joystick control 
        angle = 95
        if abs(ds.RX) > 0.1:
            with Status: st.write(ds.RX)
            angle = int(np.interp(ds.RX,[-180,180],[45,145]))

        # Boost Button with Dpad up 
        maxpower = 97
        set_throttle = 95.5
        if ds.DpadUp == True: 
            maxpower = 105
            set_throttle = 97

        # Power Calibration
        RawPower.write(f"Normalized Power: {power}")
        normalized_power = power
        power = int(np.interp(power,[0,100],[85,105])) # calibrated at 
        if normalized_power > 0 and normalized_power < 80: 
            # generate a number with a bell curve distribution with mean 90 and std 5
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
        Power.write(f"Sending Power: {power}")
        AvgPower.write(f"Avg Power: {np.mean(powers)}")

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