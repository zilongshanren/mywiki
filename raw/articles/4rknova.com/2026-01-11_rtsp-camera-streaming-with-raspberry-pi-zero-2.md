---
title: RTSP camera streaming with Raspberry-Pi Zero 2
url: https://www.4rknova.com/blog/2026/01/11/rtsp-rpi
author: Nikolaos Papadopoulos
published: '2026-01-11'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

This post walks through a clean, reliable way to stream a Raspberry Pi Zero 2 W CSI camera over RTSP on a headless setup. It uses MediaMTX with its built-in rpiCamera source, which avoids V4L2 loopback devices and avoids serving raw video over RTSP. Tested camera: OV5647.

The end goal is:

- A working RTSP stream at rtsp://IP:8554/cam
- Hardware accelerated H.264 encoding
- Reliable playback using RTSP over TCP
- MediaMTX running at startup via systemd

![Raspberry-Pi Zero 2 with camera attached](../../assets/585e4542a49b5689.jpg)

# Step 1: Download the Raspberry Pi OS image

We will use Raspberry Pi OS Lite. Download the 64-bit Lite (arm64) image file:

```
curl -L -o raspios-lite-arm64.img.xz \
https://downloads.raspberrypi.org/raspios_lite_arm64_latest
```


# Step 2: Write the image to the SD card with dd

Find your SD card device:

```
lsblk -p
```


Look for something like /dev/sdX (USB card reader) or /dev/mmcblk0. Unmount any mounted partitions (replace X):

```
sudo umount /dev/sdX* 2>/dev/null || true
```


Write the image. Use the device, not a partition (use /dev/sdX, not /dev/sdX1).

```
xzcat raspios-lite-arm64.img.xz | sudo dd of=/dev/sdX bs=4M status=progress conv=fsync
sync
```


Eject the card safely, then insert it into the Pi Zero 2 W.

# Step 3: First boot and headless login

How you do first login depends on your workflow. Common options:

- Plug in a keyboard and HDMI for one-time setup, then go headless.
- Setup a wifi connection
- Use Ethernet over USB if that is part of your workflow.
- Use your preferred method to get an IP and SSH in.

Most of that can be setup easily via:

```
sudo raspi-config
```


Once you can log in, update the system:

```
sudo apt update
sudo apt full-upgrade -y
sudo reboot
```


# Step 4: Verify the camera works (headless)

On current Raspberry Pi OS, the camera demo apps are named rpicam-*.

Install the tools:

```
sudo apt install -y rpicam-apps
```


List detected cameras:

```
rpicam-hello --list-cameras
```


Optional sanity captures, no display required:

```
rpicam-still -n -o /tmp/test.jpg
rpicam-vid -n -t 3000 --codec h264 -o /tmp/test.h264
ls -lh /tmp/test.jpg /tmp/test.h264
```


If the camera is listed and the files are non-zero, your camera pipeline is working.

# Step 5: Install MediaMTX (tarball)

MediaMTX ships as a single binary plus a YAML config.

Install prerequisites:

```
sudo apt install -y curl tar
```


Download the correct tarball for your OS and CPU from the [MediaMTX GitHub Releases page](https://github.com/bluenviron/mediamtx/releases). Then extract it into a working directory. Example:

```
mkdir -p ~/mediamtx
tar -xzf mediamtx*.tar.gz -C ~/mediamtx
cd ~/mediamtx
ls
```


You should see:

- mediamtx
- mediamtx.yml

# Step 6: Configure MediaMTX

Edit the config file *mediamtx.yml*. Add a path named cam that uses the Pi camera directly. Force RTSP over TCP for reliability and to avoid common H.264 decode errors caused by packet loss.

```
rtspTransports: [tcp]
paths:
cam:
source: rpiCamera
sourceOnDemand: yes
rpiCameraWidth: 1280
rpiCameraHeight: 720
rpiCameraFPS: 30
rpiCameraBitrate: 2000000
rpiCameraCodec: hardwareH264
rpiCameraIDRPeriod: 30
# optional compatibility tweak:
# rpiCameraHardwareH264Profile: baseline
```


| Option | Description |
|---|---|
`hardwareH264` | Uses hardware accelerated H.264 encoding. |
`sourceOnDemand` | Starts the camera only when a client connects. |
`rpiCameraIDRPeriod` | Controls how often keyframes are sent. |

# Step 7: Run MediaMTX and test playback

Start MediaMTX:

```
cd ~/mediamtx
./mediamtx
```


From another machine on the same network, test with TCP:

```
# Any modern media player will do.
# Here are two examples:
mpv --rtsp-transport=tcp rtsp://IP:8554/cam
ffplay -rtsp_transport tcp rtsp://IP:8554/cam
```


If you see video, RTSP is working.

# Step 8: Run MediaMTX at startup with systemd

Move the binary and config to a stable location:

```
sudo mkdir -p /opt/mediamtx
sudo cp ~/mediamtx/mediamtx /opt/mediamtx/
sudo cp ~/mediamtx/mediamtx.yml /opt/mediamtx/
sudo chmod +x /opt/mediamtx/mediamtx
```


Create a dedicated service user:

```
sudo useradd --system --no-create-home --shell /usr/sbin/nologin mediamtx
```


Create the systemd unit:

```
sudo tee /etc/systemd/system/mediamtx.service >/dev/null <<'EOF'
[Unit]
Description=MediaMTX
Wants=network-online.target
After=network-online.target
[Service]
User=mediamtx
WorkingDirectory=/opt/mediamtx
ExecStart=/opt/mediamtx/mediamtx /opt/mediamtx/mediamtx.yml
Restart=on-failure
RestartSec=2
SupplementaryGroups=video
[Install]
WantedBy=multi-user.target
EOF
```


Enable and start:

```
sudo systemctl daemon-reload
sudo systemctl enable --now mediamtx
```


Check status and logs:

```
sudo systemctl status mediamtx --no-pager
sudo journalctl -u mediamtx -f
```


# Step 9: Basic authentication (optional)

If you want to add basic authentication, append this to */opt/mediamtx/mediamtx.yml*:

```
authMethod: internal
authInternalUsers:
- user: user
pass: password
permissions:
- action: read
path: cam
```


Restart:

```
sudo systemctl restart mediamtx
```


Connect:

```
mpv --rtsp-transport=tcp rtsp://user:password@<PI_IP>:8554/cam
```


# Troubleshooting

Here are some issues I came across while working on this and how to work around them.

## RTSP connects but no video / H.264 errors

If you see errors like “non-existing PPS referenced” on the client, do this:

- Use TCP on the client: mpv –rtsp-transport=tcp
- Keep rtspTransports: [tcp] in the MediaMTX config
- Lower bitrate or resolution if WiFi is weak

Try a lighter profile:

```
rpiCameraWidth: 640
rpiCameraHeight: 480
rpiCameraFPS: 15
rpiCameraBitrate: 1000000
rpiCameraIDRPeriod: 15
```


## Camera not detected

- Reseat the CSI ribbon cable and close the latch firmly.
- Re-run: rpicam-hello –list-cameras
- Check logs:

```
dmesg | grep -i -E "camera|unicam|csi|ov|imx" | tail -n 80
```