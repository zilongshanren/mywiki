---
title: Headless Raspberry Pi configuration over Bluetooth – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2017/02/headless-raspberry-pi-configuration-over-bluetooth/
author: Patrick Hundal
published: '2017-02-08'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

With the advent of the newer Raspberry Pi 3 (RPi) with built-in Bluetooth, there are now new options for getting connected to the console of the RPi, without the headache of having to dig up a monitor and keyboard (much less a serial cable with pinouts).

This is especially advantageous when running workshops and hackathons, where connectivity can become problematic. In fact, this specific hack came about from a recent Mozilla hackathon in Berlin, where we realized that we had 10-15 RPi for participants, but not a single monitor, keyboard, serial cable, or other means to connect to the RPis. So it raised the question – why couldn’t we use Bluetooth (BT) as a serial connection to get to the console?

Unlike other tutorials on the web, which assume you already have some console access established, I’ve provided steps which let you do this without any previous connection! To accomplish this, we’ll modify a base image of Raspian-Jesse to allow the RPi to boot into a mode where you can connect via Bluetooth and establish a “virtual” serial connection on startup.

## Why is this awesome?

Lot of reasons:

- No cables, monitors, or keyboards required.
- It lets you work directly on the RPi when resources like wireless access points or wired switches are not available.
- It gives you an easy way to get a second screen for viewing logs when testing the primary networking interfaces.
- Or how about this common problem — you set up wifi for DHCP, but can’t find the machine on your network? Rather than using a tool like
[Pi Finder](https://github.com/adafruit/Adafruit-Pi-Finder)after the fact, you can just use your Bluetooth terminal session to enable wifi and then right after, run an ifconfig to get the IP. - Last but not least, it is great for multi-RPi hackathons — you’ll come across a number of problems in such circumstances, like too many devices with the same hostname, or ssh ports blocked on event space wifi.

It’s brilliant, fast and simple. It is a little insecure, but we’ll also provide some instructions on how to solve this problem near the end of the article.

There are several useful internet resources that helped us in putting this together, but in particular, kudos to Dr. [Rowland for this helpful script](https://github.com/DrRowland/RPi-Bluetooth-Console/blob/master/setup.sh).

## Preparing an RPi image for editing

Here’s how to get started.

- Download the
[latest Raspian Jessie image](https://downloads.raspberrypi.org/raspbian_latest). - Mount the image for editing.

Note: We are after the EXT4 partition, which contains the files we want to edit for startup.

### Mounting on Mac

This proved challenging, as OSX doesn’t support EXT4 natively. This limitation left two options; we felt more compelled to do the second, but the first is probably quicker.

#### 1. Install native Ext4 drivers

This option involves installing EXT4 drivers into OSX (see [https://osxfuse.github.io/](https://osxfuse.github.io/)) and read the .img file natively. These are not recommended for writing to EXT4 partitions, so use with caution.

#### 2. Use a virtual machine

Here we will install Virtual Box, and then create a virtual machine of Linux. We then operate in the VM to natively mount the .img of Raspian-Jessie through a shared folder.

- First, download and install
[VirtualBox](https://www.virtualbox.org/). - Next, download and install
[Mint Linux](https://www.linuxmint.com/)in a virtual machine under Virtual Box: - In the Linux virtual machine, put the image in a shared folder (visible to both the VM and your desktop) and then follow the instructions in the link in the “Mounting on Linux” section below to mount the .img file under Linux and edit the image.

### Mounting on Linux

Mounting EXT4 on Linux is a simple, well-documented process: see [How can I mount a Raspberry Pi Linux distro image?](http://raspberrypi.stackexchange.com/questions/13137/how-can-i-mount-a-raspberry-pi-linux-distro-image)

### Mounting on Windows

This is a fairly simple process, as EXT4 is supported natively by Windows. For a simple guide on how to do this, see [Can I view/copy the contents of an img file from Windows?](https://raspberrypi.stackexchange.com/questions/28457/can-i-view-copy-the-contents-of-an-img-file-from-windows)

## Editing the image

Once you have the image mounted, and you are at the command prompt, you can start editing the configuration files necessary to get us going.

Let’s start by creating the main script that will set up and establish the default Bluetooth services and serial port you will connect to on startup.

You’ll create this file in the /home/pi directory, like so:

`$ sudo nano /home/pi/btserial.sh`


Add the following lines to the script:

```
#!/bin/bash -e
#Edit the display name of the RaspberryPi so you can distinguish
#your unit from others in the Bluetooth console
#(very useful in a class setting)
echo PRETTY_HOSTNAME=raspberrypi > /etc/machine-info
# Edit /lib/systemd/system/bluetooth.service to enable BT services
sudo sed -i: 's|^Exec.*toothd$| \
ExecStart=/usr/lib/bluetooth/bluetoothd -C \
ExecStartPost=/usr/bin/sdptool add SP \
ExecStartPost=/bin/hciconfig hci0 piscan \
|g' /lib/systemd/system/bluetooth.service
# create /etc/systemd/system/rfcomm.service to enable
# the Bluetooth serial port from systemctl
sudo cat <<EOF | sudo tee /etc/systemd/system/rfcomm.service > /dev/null
[Unit]
Description=RFCOMM service
After=bluetooth.service
Requires=bluetooth.service
[Service]
ExecStart=/usr/bin/rfcomm watch hci0 1 getty rfcomm0 115200 vt100 -a pi
[Install]
WantedBy=multi-user.target
EOF
# enable the new rfcomm service
sudo systemctl enable rfcomm
# start the rfcomm service
sudo systemctl restart rfcomm
```


Save the file, and then make it executable by updating its permissions like so:

`$ chmod 755 /home/pi/btserial.sh`


Now you have the basics of the script required to turn on the Bluetooth service and configure it. But to do this 100% headless, you’ll need to run this new script on startup. Let’s edit /etc/rc.local to launch this script automatically.

`$ sudo nano /etc/rc.local`


Add the following lines after the initial comments:

```
#Launch bluetooth service startup script /home/pi/btserial.sh
sudo /home/pi/btserial.sh &
```


Save the rc.local script, unmount the image, and write it to an SD Card using your favorite tool (mine is [ApplePiBaker](https://www.tweaking4all.com/software/macosx-software/macosx-apple-pi-baker/)).

Now you are ready to go. Plug in power to the Rpi and give it 30 seconds or so to startup. Then unplug it, and plug it in again and let it boot up a second time. Restarting the Bluetooth service doesn’t work correctly, so we need to reboot.

Now let’s connect.

## Connecting to your RPi via Bluetooth

On your desktop/laptop, open up your Bluetooth preferences and ensure Bluetooth is enabled.

Select “raspberrypi” (or whatever you have used for PRETTY_HOSTNAME in the btserial.sh script) when it appears and pair with it. It should pair automatically (remember what we said earlier about security issues?)

Open a terminal window on your local machine, and start a screen session to connect via the new Bluetooth serial port created from the RPi connection. First let’s check the name of the serial connection:

`$ ls /dev/cu.*`


This should produce a list of available serial ports, one of which should now be named after your pi. Then we can connect.

`$ screen /dev/cu.raspberrypi-SerialPort 115200`


Give it a second, and you should be at the prompt of the RPi console! Congrats!

## Further tips

Don’t stop reading yet — this section contains some useful tips about using the RPi terminal, including making it more secure.

### Interactive terminal [optional]

After your initial amazement has subsided, you’ll realize your terminal window size isn’t reflected in the output from the serial session. You can adjust this in one of two ways.

#### Manual resizing

Simply note the size of your current terminal window , and enter the command:

`stty rows XX cols YY`


replacing XX and YY with the size of your local terminal window

#### Automatic (dynamic) resizing

If you want your terminal session to be responsive when you change your local terminal window size, you’ll need to do the following:

Start up sshd, which is off by default. From the command prompt, run:

`$ sudo raspi-config`


Now:

- Select “Advanced Config”
- Select “SSH”
- Select “Activate”
- Exit raspi config

With SSH active, you can now enter the following commands:

```
$ su pi -
$ ssh localhost
```


Your terminal window will now resize dynamically.

### Security [optional, but not really…]

If you are on a deserted island, far away from humanity, you can stop now. If not, you should be concerned that this connection is wide open for others to connect to and use. To make this a little more secure, I would recommend turning off Bluetooth discoverability and pairing once you have connected to your RPi.

In the console on the RPi, run the following commands:

```
$sudo bluetoothctl
[bluetooth]#</pre>
Turn off discoverability:
<pre>[bluetooth]#discoverable no
```


Turn off pairing:

`[bluetooth]#pairing no`


And exit bluetoothctl:

```
[bluetooth]#quit
$
```


At this point you should be good to go with at least some small security measures in place. If the machine restarts, you’ll need to follow these security steps again when you reconnect.

## Summary

So there you have it — you should now have set up your own working RPi console over Bluetooth, configured entirely headlessly. You should now be able to go forth and work on your own RPi projects, alongside others, with the minimum of connectivity issues.

If you run into problems getting this to work, or have any tips of your own to share, please do so in the comments.

Special thanks to [Florian Merz](https://twitter.com/fiji_flo) for his technical review of this post.

## About Patrick Hundal

Business Development, Strategic Partnerships at Mozilla.

## One comment

Alex GrandeFebruary 26th, 2017 at 21:27