# Installation Notes

The Raspberry Pi setup process is always improving and changing, so you may find it takes different steps to get this software working. 

Here are installation instructions from December, 2023. 

## Initial Installation from macOS

Download the Raspberry Pi Imager from <https://www.raspberrypi.com/software/>. 

Using a USB SD card adapter, connect your SD card. You need to connect the adapter directly to your Mac, and then grant it permission. You may have to reboot your Mac if the permission dialog flashes on the screen and disappears. 

Configure the system to your liking, including Wi-Fi and SSH. Then insert the SD card into the Pi and complete the installation. 

Open the Raspberry Pi Configuration tool. I set `Boot` to `To CLI`, enable `Network at Boot`. 

## Disable Audio

If you are hooking the LED strip up to pin `D18`, you must disable audio. 

Per [these instructions](https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage): 
This can be done in /boot/config.txt by changing `dtparam=audio=on` to `dtparam=audio=off` and rebooting.

One symptom of failing to do this is that only a few pixels will light up near the beginning of the strip. 

## Installing GitHub CLI

Follow the instructions at <https://github.com/cli/cli/blob/trunk/docs/install_linux.md> to install `gh`:

```
type -p curl >/dev/null || (sudo apt update && sudo apt install curl -y)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
&& sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
&& sudo apt update \
&& sudo apt install gh -y
```

Then check out the repo:
```
gh auth login
gh repo clone jasonluther/rebar-heart
```

Finally, install the dependencies and systemd scripts:
```
cd rebar-heart/src/orchestration/
./install-systemd-files
```

Start an animation:
```
sudo service heart-rainbow start
```

To troubleshoot, see logs here:
```
tail -f /var/log/daemon.log
```

If you run into problems, refer to <https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage> for updates on how to install and use the Adafruit NeoPixels Python tools. 

