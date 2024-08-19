import streamlit as st

col1, col2, col3 = st.columns([1,2,1])
col2.Title("My first robot!")
col2.caption("This robot is built off a four wheel drive RC car, modified to have four wheel steering")

col2.write("First, connect to the robot over its wifi network, and then go to your browser and type in the IP address of the robot. Since its the host, the IP address will be the first in the IP range")
col2.write("Next, you can ssh into the robot by typing in the terminal: ssh <hostname>@<IP address>")

