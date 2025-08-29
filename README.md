# BurnBaby 

One wire WS281x on GPIO 18 by default.
optional random audio playback
Runs on a Raspberry Pi.

## Install

```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev
pip3 install -r requirements.txt
```
## Run

```bash
mkdir -p audio
# put mp3 or wav in ./audio if using --audio
sudo python3 burnBaby.py --count 120 --gpio 18 --brightness 160 --fps 60 --audio --audio-min 20 --audio-max 90
```
--count = number of LEDs in your strip
--gpio = GPIO pin for the data line (default 18)
--brightness = brightness 0–255
--fps = frames per second (default 60)
--audio = enable audio playback (looks in ./audio folder)
--audio-min / --audio-max = random time between sounds in seconds

Notes
- Data pin is set with --gpio. Default 18.
- If rpi_ws281x is missing, script prints SIM output to console.
