---
title: WiFi Debugging for Firefox OS – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/04/wifi-debugging-for-firefox-os/
author: J Ryan Stinnett
published: '2015-04-28'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

I am excited to announce that we’re now shipping WiFi debugging for Firefox OS! It’s available in [Firefox OS 3.0 / master](https://developer.mozilla.org/en-US/Firefox_OS/Building) with [Firefox Nightly](https://nightly.mozilla.org/) on desktop.

WiFi debugging allows [WebIDE](https://developer.mozilla.org/docs/Tools/WebIDE) to connect to your Firefox OS device via your local WiFi network instead of a USB cable.

The connection experience is generally more straightforward (especially after connecting to a device the first time) than with USB and also more convenient to use since you’re no longer tied down by a cable.

Since quite early on in the development of Firefox OS, you’ve been able to debug a device over a USB cable. However, this comes with various drawbacks:

- You have to connect a cord whenever debugging is needed
- Drivers are required on some OSes, which causes a lot of confusion
- The cord requirement makes it harder to debug a phone during a user test

The mobile device just generally feels a bit less like itself when it’s tied down with a cord.

We’ve thought about adding some form of WiFi access on the DevTools team for some time. Our key goals were:

- Ease of use
- Secure connection

While we certainly wanted to make this feature available, we wanted to be sure it would be an improvement over the USB method, while also being secure as well. This is important over a shared network like WiFi, since the debugging process by its nature exposes many details of your activity, including potentially private request data. If you’re working at a coffee shop, you don’t want others to have access to this.

When connecting over WiFi, there could be many possible devices to pick from on the same network. To avoid this problem, we use a discovery mechanism, similar to Bonjour or mDNS. When you want to connect, your computer sends a multicast ping to look for nearby devices. If there are any, they’ll reply with their name and what services they support. This allows us to present a simple list of device names, instead of dealing with IP addresses.

The setup process is also nicer than the USB method, which relied on ADB from the Android project. With WiFi debugging, there are no drivers to install on Windows or udev rules to configure on Linux.

A large portion of this project has gone towards making the debugging connection secure, so that you can use it safely on shared network, such as an office or coffee shop.

We use [TLS](https://tools.ietf.org/html/rfc5246) for encryption and authentication. The computer and device both create self-signed certificates. When you connect, a QR code is scanned to verify that the certificates can be trusted. During the connection process, you can choose to remember this information and connect immediately in the future if desired.

You’ll need to assemble the following:

[Firefox 39](https://nightly.mozilla.org/)(2015-03-27 or later)- Firefox OS 3.0 (2015-04-16 or later)

Firefox OS 3.0 is still under heavy development, so it’s not yet available on devices in stores. If you have a Flame device, you can [update your Flame](https://developer.mozilla.org/en-US/Firefox_OS/Phone_guide/Flame/Updating_your_Flame#Updating_your_Flame_to_a_nightly_build) to 3.0 / master using a nightly build. For other devices, you may need to [build for your device](https://developer.mozilla.org/en-US/Firefox_OS/Building) from source to update it.

On Firefox OS, enable WiFi debugging:

- Go to Developer Settings on device (Settings -> Developer)
- Enable DevTools via Wi-Fi
- Edit the device name if desired

![Firefox OS WiFi Debugging Options](../../assets/21595bd3d552a17e.png)


To connect from Firefox Desktop:

- Open WebIDE in Firefox Nightly (Tools -> Web Developer -> WebIDE)
- Click “Select Runtime” to open the runtimes panel
- Your Firefox OS device should show up in the “WiFi Devices” section
- A connection prompt will appear on device, choose “Scan” or “Scan and Remember”
- Scan the QR code displayed in WebIDE

![WebIDE WiFi Runtimes](../../assets/fc2bbcddc4fd55d8.png)


![WebIDE Displays the QR Code](../../assets/4cf77b36ed9e637e.png)


After scanning the QR code, the QR display should disappear and the “device” icon in WebIDE will turn blue for “connected”.

You can then access all of your remote apps and browser tabs just as you can today over USB. All of the Firefox DevTools are available over WiFi to inspect, debug, and explore. This is purely a change in how DevTools packets are exchanged, so there are no limits on what tools you can use.

This feature should be supported on any Firefox OS device. So far, I’ve tested it on the Flame and Nexus 4.

The QR code scanner can be a bit frustrating at the moment, as real devices appear to capture a very low resolution picture. [Bug 1145772](https://bugzil.la/1145772) aims to improve this soon. You should be able to scan with the Flame by trying a few different orientations. I would suggest using “Scan and Remember”, so that scanning is only needed for the first connection.

If you find other issues while testing, please [file bugs](https://bugzilla.mozilla.org/enter_bug.cgi?product=Firefox&component=Developer%20Tools%3A%20WebIDE) or contact me on IRC.

This was quite a complex project, and many people outside of DevTools from teams like Networking and Security provided advice and reviews while working on this feature, including:

- Brian Warner
- Trevor Perrin
- David Keeler
- Honza Bambas
- Patrick McManus
- Jason Duell
- Panos Astithas
- Jan Keromnes
- Alexandre Poirot
- Paul Rouget
- Paul Theriault

I am probably forgetting others as well, so I apologize if you were omitted.

I’d like to add this ability for [Firefox for Android](https://www.mozilla.org/en-US/firefox/android/) next. Thankfully, most of the work done here can be reused there. Additionally, we should update other tools like [node-firefox](https://hacks.mozilla.org/2015/02/introducing-node-firefox/) to use WiFi to connect to devices. We may also leverage some of this work to make the [Browser Toolbox](https://developer.mozilla.org/en-US/docs/Tools/Browser_Toolbox) more secure on Firefox desktop.

If there are features you’d like to see added, [file bugs](https://bugzilla.mozilla.org/enter_bug.cgi?product=Firefox&component=Developer%20Tools%3A%20WebIDE) or contact the team via [various channels](https://wiki.mozilla.org/DevTools/GetInvolved#Communication).

## About
[
J. Ryan Stinnett ](https://convolv.es/)

Staff Engineer working on Firefox DevTools at Mozilla.