
# Mobile robot
All the code needed to manually control my second mobile robot, using a PS5 remote. 

&nbsp;

<div align="center"><img src="docs/preview.gif" width="800"></div>

&nbsp;

## Dependencies

This code uses the following libraries:
- `streamlit`: for building the user interface.
- `numpy`: for creating arrays.
- `matplotlib`: for plotting the stepper motor visualization
- `hidapi`: for accessing usb connections on the host device

&nbsp;

## Usage
1. clone this repository
```
git clone 
```
2. change the wifi SSID and password as well as the PS5 remote vendorID and productID in 'app.py'
4. Run the arduino nano.py file on an arduino nano esp32 running mircopython
5. run the streamlit app with the following command in your terminal
```
Streamlit run app.py
```

This will start the local Streamlit server, and you can access the interface by opening a web browser and navigating to `http://localhost:8501`.

&nbsp;

## How it Works

The app as follows:
1. The hidapi library is used to initiate a connection to the PS5 controller
2. The dualsense class is used to decode the received bytes
4. the matplotlib library is used to create a visualization of the received signal from the triggers
3. Streamlit is used to display the figure
4. The ethernet class and UDP Socket communication is used to send the bytes to an IP address
5. The app loops indefinitely until quit
6. The Arduino connects to the internet, then receives the UDP signal and decodes it, then sets its PWM pin appropriately. 

&nbsp;

## Repository Structure
```
repository/
├── app.py # the code and UI integrated together live here
├── customize_gui # class for adding gui elements
├── dualsense.py # The class used to decode received bytes from the wired controller
├── requirements.txt # the python packages needed to run locally
├── .gitignore # includes the local virtual environment named my_env
├── ethernet.py
├── robot.py
└── docs/
    └── preview.png # preview photo for Github
```

&nbsp;

## Topics 
```
Python | Streamlit | Git | Low Code UI
Sketchpad | HIDapi | decode bytes | PS5 | Sony | Dualsense | external device | communication 
custom classes
Self taught coding | Mechanical engineer | Robotics engineer
```
&nbsp;

<hr>

&nbsp;

<div align="center">



╭━━╮╭━━━┳━━┳━━━┳━╮╱╭╮        ╭╮╱╱╭━━━┳━━━┳╮╭━┳━━━╮
┃╭╮┃┃╭━╮┣┫┣┫╭━╮┃┃╰╮┃┃        ┃┃╱╱┃╭━━┫╭━╮┃┃┃╭┫╭━╮┃
┃╰╯╰┫╰━╯┃┃┃┃┃╱┃┃╭╮╰╯┃        ┃┃╱╱┃╰━━┫╰━━┫╰╯╯┃┃╱┃┃
┃╭━╮┃╭╮╭╯┃┃┃╰━╯┃┃╰╮┃┃        ┃┃╱╭┫╭━━┻━━╮┃╭╮┃┃┃╱┃┃
┃╰━╯┃┃┃╰┳┫┣┫╭━╮┃┃╱┃┃┃        ┃╰━╯┃╰━━┫╰━╯┃┃┃╰┫╰━╯┃
╰━━━┻╯╰━┻━━┻╯╱╰┻╯╱╰━╯        ╰━━━┻━━━┻━━━┻╯╰━┻━━━╯
  


&nbsp;


<a href="https://twitter.com/BrianJosephLeko"><img src="https://raw.githubusercontent.com/BrianLesko/BrianLesko/f7be693250033b9d28c2224c9c1042bb6859bfe9/.socials/svg-white/x-logo-white.svg" width="30" alt="X Logo"></a> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <a href="https://github.com/BrianLesko"><img src="https://raw.githubusercontent.com/BrianLesko/BrianLesko/f7be693250033b9d28c2224c9c1042bb6859bfe9/.socials/svg-white/github-mark-white.svg" width="30" alt="GitHub"></a> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <a href="https://www.linkedin.com/in/brianlesko/"><img src="https://raw.githubusercontent.com/BrianLesko/BrianLesko/f7be693250033b9d28c2224c9c1042bb6859bfe9/.socials/svg-white/linkedin-icon-white.svg" width="30" alt="LinkedIn"></a>

follow all of these for pizza :)

</div>


&nbsp;


