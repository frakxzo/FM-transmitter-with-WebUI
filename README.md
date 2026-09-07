# 📻 FM-Transmitter with WebUI

> A lightweight, headless ad-hoc RF broadcast and remote command interface built for the Raspberry Pi 3B. It utilizes bare-metal Direct Memory Access (DMA) clock manipulation to transmit FM radio signals, featuring a volatile memory field-notes system, real-time hardware telemetry, and live USB intercom capabilities.
> 
> *Special thanks to **Christophe Jacquet** for building the core transmission engine.*

---

## ⚙️ Hardware Requirements

* **Raspberry Pi 3B** (or compatible SBC)
* **20cm jumper wire** attached to **GPIO 4 (Pin 7)** acting as the antenna
* **USB Microphone** (Required for Live Intercom mode)

---

## 🚀 Fresh Install & Setup

### 1. Install System Dependencies
Ensure the OS has the required audio slicing and encoding tools installed:
```bash
sudo apt update 
sudo apt install python3-flask sox ffmpeg alsa-utils git -y
```

### 2. Install the Hardware Driver

Clone and compile the core FM transmitter dependency:

```bash
git clone https://github.com/ChristopheJacquet/PiFmRds.git
sudo apt-get install libsndfile1-dev
cd PiFmRds/src 
make
mkdir audio_files
```
Save all your .wav files in this directory(audio_files)


### 3. Clone the WebUI (⚠️ CRITICAL PATH REQUIREMENT)

**IMPORTANT:** All Python and HTML files from this repository **MUST** be placed directly inside the `src` folder alongside the compiled `pi_fm_rds` binary. If the pathing is altered, the backend will fail to execute the hardware commands.

Ensure you are still inside the `PiFmRds/src` directory, then clone this repository into it using the trailing dot (`.`):
```bash
git clone https://github.com/frakxzo/FM-transmitter-with-WebUI.git
```


### 4. Execute the Node

The dashboard requires root privileges to bind to the GPIO pins and access system thermal files:

```bash
sudo python3 app.py 
```


Once running, access the tactical UI on your local network via:
```bash
**`http://<PI_IP_ADDRESS>:6767`**
```


## 🏆 Acknowledgments & Credits

* **FM Transmission Core:** The underlying RF modulation driver used in this project is **[PiFmRds](https://github.com/ChristopheJacquet/PiFmRds)**, developed by **Christophe Jacquet**. It handles the bare-metal DMA clock manipulation required to generate the FM carrier wave.

