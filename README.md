# PiRadio
This is a Raspberry Pi based Internet Radio based on MPD.

## Hardware
 - Raspberry Pi Zero W
 - 20x4 LCD
 - USB Soundcard

## Requirements
 - Linux distro
 - Python3
 - git

## Setup

### System Dependencies

On Raspbian:
``` bash
  sudo apt install python3-pip git mpd
```

### Python Dependencies

``` bash
  pip3 install RPi.GPIO musicpd
```

### Installation
Clone this Git repo into `/home/pi/piradio`:
``` bash
pi@piradio:~ $ git clone https://github.com/nold360/piradio /home/pi/piradio
```

This script will setup & update everything from git:
``` bash
sudo ./setupdate.sh
```


### ALSA Equalizer
The `mpd.conf` referes to a alsaequal Equalizer device. Use `conf/asound.conf` as `/etc/asource.conf`.

#### Installation
`sudo apt install libasound2-plugin-equal`

#### Configuration
`sudo -u mpd alsamixer -D equal`
