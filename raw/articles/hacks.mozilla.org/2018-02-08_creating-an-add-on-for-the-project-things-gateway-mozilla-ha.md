---
title: Creating an Add-on for the Project Things Gateway – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2018/02/creating-an-add-on-for-the-project-things-gateway/
author: James Hobin
published: '2018-02-08'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The [Project Things Gateway](https://iot.mozilla.org/gateway/) exists as a platform to bring all of your IoT devices together under a unified umbrella, using a standardized HTTP-based API. Currently, the platform only has support for a limited number of devices, and we need your help expanding our reach! It is fairly straightforward to add support for new devices, and we will walk you through how to do so. The best part: you can use whatever programming language you’d like!

## High-Level Concepts

### Add-on

An *Add-on* is a collection of code that the Gateway runs to gain a new features, usually a new adapter. This is loosely modeled after the [add-on system](https://developer.mozilla.org/en-US/Add-ons) in Firefox where each add-on adds to the functionality of your Gateway in new and exciting ways.

### Adapter

An *Adapter* is an object that manages communication with a device or set of devices. This could be very granular, such as one adapter object communicating with one GPIO pin, or it could be much more broad, such as one adapter communicating with any number of devices over WiFi. You decide!

### Device

A *Device* is just that, a hardware device, such as a smart plug, light bulb, or temperature sensor.

### Property

A *Property* is an individual property of a device, such as its on/off state, its energy usage, or its color.

## Supported Languages

Add-ons have been written in Node.js, Python, and Rust so far, and official JavaScript and Python bindings are available on the gateway platform. If you want to skip ahead, you can check out the [list of examples](https://hacks.mozilla.org#examples) now. However, you are free to develop an add-on in whatever language you choose, provided the following:

- Your add-on is
[properly packaged](https://github.com/mozilla-iot/wiki/wiki/Add-On-System-Design). - Your add-on package bundles all required dependencies that do not already exist on the gateway platform.
- If your package contains any compiled binaries, they must be compiled for the armv6l architecture.
[All Raspberry Pi families](https://elinux.org/RPi_Hardware#Raspberry_Pi_Hardware_History)are compatible with this architecture. The easiest way to do this would be to build your package on a Raspberry Pi 1/2/Zero.

## Implementation: The Nitty Gritty

### Evaluate Your Target Device

First, you need to think about the device(s) you’re trying to target.

- Will your add-on be communicating with one or many devices?
- How will the add-on communicate with the device(s)? Is a separate hardware dongle required?
- For example, the Zigbee and Z-Wave adapters require a separate USB dongle to communicate with devices.

- What properties do these devices have?
- Is there an existing Thing type that you can advertise?
- Are there existing libraries you can use to talk to your device?
- You’d be surprised by how many NPM modules, Python modules, C/C++ libraries, etc. exist for communicating with IoT devices.


The key here is to gain a strong understanding of the devices you’re trying to support.

### Start from an Example

The easiest way to start development is to start with one of the [existing add-ons](https://hacks.mozilla.org#examples) (listed further down). You can download, copy and paste, or git clone one of them into:

`/home/pi/.mozilla-iot/addons/`


Alternatively, you can do your development on a different machine. Just make sure you test on the Raspberry Pi.

After doing so, you should edit the `package.json` file as appropriate. In particular, the name field needs to match the name of the directory you just created.

Next, begin to edit the code. The key parts of the add-on lifecycle are device creation and property updates. Device creation typically happens as part of a discovery process, whether that’s through [SSDP](https://en.wikipedia.org/wiki/Simple_Service_Discovery_Protocol), probing serial devices, or something else. After discovering devices, you need to build up their property lists, and make sure you handle property changes (that could be through events you get, or you may have to poll your devices). You also need to handle property updates from the user.

Restart the gateway process to test your changes:

`$ sudo systemctl restart mozilla-iot-gateway.service`


Test your add-on thoroughly. You can enable it through the *Settings->Add-ons* menu in the UI.

### Get Your Add-on Published!

Run `./package.sh` or whatever else you have to do to package up your add-on. Host the package somewhere, i.e. on Github as a release. Then, submit a pull request or issues to the addon-list repository.

### Notes

- Your add-on will run in a separate process and communicate with the gateway process via nanomsg IPC. That should hopefully be irrelevant to you.
- If your add-on process dies, it will automatically be restarted.

## Examples

The Project Things team has built several add-ons that can serve as a good starting point and reference.

Node.js:

- Example adapter:
[https://github.com/mozilla-iot/example-adapter](https://github.com/mozilla-iot/example-adapter) - Virtual things adapter:
[https://github.com/mozilla-iot/virtual-things-adapter](https://github.com/mozilla-iot/virtual-things-adapter) - Zigbee adapter:
[https://github.com/mozilla-iot/zigbee-adapter](https://github.com/mozilla-iot/zigbee-adapter) - Z-Wave adapter:
[https://github.com/mozilla-iot/zwave-adapter](https://github.com/mozilla-iot/zwave-adapter) - Philips Hue adapter:
[https://github.com/mozilla-iot/philips-hue-adapter](https://github.com/mozilla-iot/philips-hue-adapter) - GPIO adapter:
[https://github.com/mozilla-iot/gpio-adapter](https://github.com/mozilla-iot/gpio-adapter)

Python:

- TP-Link adapter:
[https://github.com/mozilla-iot/tplink-adapter](https://github.com/mozilla-iot/tplink-adapter)

Rust:

- MQTT adapter (in progress):
[https://github.com/hobinjk/mqtt-adapter](https://github.com/hobinjk/mqtt-adapter)

## References

Additional documentation, API references, etc., can be found here:

- Web Thing API specification:
[https://iot.mozilla.org/wot/](https://iot.mozilla.org/wot/) - Node.js adapter API:
[https://github.com/mozilla-iot/wiki/wiki/Adapter-API](https://github.com/mozilla-iot/wiki/wiki/Adapter-API) - Adapter IPC API:
[https://github.com/mozilla-iot/wiki/wiki/Adapter-IPC](https://github.com/mozilla-iot/wiki/wiki/Adapter-IPC) - Add-on packaging:
[https://github.com/mozilla-iot/wiki/wiki/Add-On-System-Design](https://github.com/mozilla-iot/wiki/wiki/Add-On-System-Design) - Python add-on bindings:
[https://github.com/mozilla-iot/gateway-addon-python](https://github.com/mozilla-iot/gateway-addon-python) - Add-on list:
[https://github.com/mozilla-iot/addon-list](https://github.com/mozilla-iot/addon-list)

Find a bug in some of our software? Let us know! We’d love to have issues, or better yet, pull requests, filed to the appropriate Github repo.

## About
[
James Hobin ](https://hobinjk.github.io/)

Level 25 Computer Wizard on a quest to keep the Internet of Things free and open.

## About
[
Michael Stegeman ](https://github.com/mrstegeman)

Michael is a software engineer at Mozilla working on WebThings.

## 4 comments

voracityFebruary 10th, 2018 at 03:09James HobinFebruary 12th, 2018 at 08:00Wim HaanstraFebruary 20th, 2018 at 13:11James HobinFebruary 20th, 2018 at 13:30