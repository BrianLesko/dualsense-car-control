#!/bin/bash

# Control the mobile robot manually with a dualsense ps5 controller

<<<<<<< HEAD:start.sh
=======
# First we use the default wifi chip in the pi wlan0 to create a hotspot
#sudo nmcli device wifi hotspot ssid lesko-car password 12081999 ifname wlan0 & 

# Next, we host the manual control webpage 
source my_env/bin/activate
python3 car.py & 

#streamlit run instructions.py --server.port 80 


>>>>>>> 8cd146a (start the car file):car.sh
