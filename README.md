# BurnBaby Abstract 

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
sudo python3 fire_ultra.py --count 120 --gpio 18 --brightness 160 --fps 60 --audio --audio-min 20 --audio-max 90
```

Notes
- Data pin is set with --gpio. Default 18.
- If rpi_ws281x is missing, script prints SIM output to console.
