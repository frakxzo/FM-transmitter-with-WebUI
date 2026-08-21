# FM-transmitter with WebUI

A lightweight, headless ad-hoc RF broadcast and remote command interface built for the Raspberry Pi 3B. It utilizes bare-metal Direct Memory Access (DMA) clock manipulation to transmit FM radio signals, featuring a volatile memory field-notes system, real-time hardware telemetry, and live USB intercom capabilities.
* Special thanks to [Christophe Jacquet](https://github.com/ChristopheJacquet) for Building this amazing project.

## Hardware Requirements
* Raspberry Pi 3B (or compatible SBC)
* 20cm jumper wire attached to GPIO 4 (Pin 7) acting as the antenna
* USB Microphone (for Live Intercom mode)

## Fresh Install & Setup

**1. Install System Dependencies**
Ensure the OS has the required audio slicing and encoding tools:

sudo apt update
sudo apt install python3-flask sox ffmpeg alsa-utils git -y

**2. Install the Hardware Driver**

Clone and compile the core FM transmitter dependency:

git clone [https://github.com/ChristopheJacquet/PiFmRds.git](https://github.com/ChristopheJacquet/PiFmRds.git)
cd PiFmRds/src
make

**3. Clone the WebUI**
Clone this repository directly into the src folder alongside the compiled PiFmRds binary:


git clone https://github.com/frakxzo/FM-transmitter-with-WebUI.git


**4. Execute the Node**
The dashboard requires root privileges to bind to the GPIO pins and access system thermal files:

Bash
sudo python3 app.py
Access the tactical UI via http://<PI_IP_ADDRESS>:6767 on your local network.

**Acknowledgments & Credits**
FM Transmission Core: The underlying RF modulation driver used in this project is PiFmRds, developed by Christophe Jacquet. It handles the bare-metal DMA clock manipulation required to generate the FM carrier wave.
