---
title: How to build your own private smart home with a Raspberry Pi and Mozilla’s
  Things Gateway – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2018/02/how-to-build-your-own-private-smart-home-with-a-raspberry-pi-and-mozillas-things-gateway/
author: Ben Francis
published: '2018-02-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Last year we [announced](https://hacks.mozilla.org/2017/06/building-the-web-of-things/) Project Things by Mozilla. Project Things is a framework of software and services that can bridge the communication gap between connected devices by giving “things” URLs on the web.

Today I’m excited to tell you about the latest version of the [Things Gateway](https://iot.mozilla.org/gateway/) and how you can use it to directly monitor and control your home over the web, without a middleman. Instead of installing a different mobile app for every smart home device you buy, you can manage all your devices through a single secure web interface. This blog post will explain how to build your own Web of Things gateway with a Raspberry Pi and use it to connect existing off-the-shelf smart home products from various different brands using the power of the open web.

There are lots of exciting new features in the latest version of the gateway, including a rules engine for setting ‘*if this, then that’* style rules for how things interact, a floorplan view to lay out devices on a map of your home, experimental voice control and support for many new types of “things”. There’s also a brand new add-ons system for adding support for new protocols and devices, and a new way to safely authorise third party applications to access your gateway.

![](../../assets/1d8c88f74b2555e8.png)


## Hardware

The first thing to do is to get your hands on a Raspberry Pi® single board computer. The latest [Raspberry Pi 3](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/) has WiFi and Bluetooth support built in, as well as access to GPIO ports for direct hardware connections. This is not essential as you can use alternative developer boards, or even your laptop or desktop computer, but it currently provides the best experience.

![](../../assets/c6dd4fa195a2b699.png)


If you want to use smart home devices using other protocols like Zigbee or Z-Wave, you will need to invest in USB dongles. For Zigbee we currently support the [Digi XStick](https://www.digi.com/products/xbee-rf-solutions/boxed-rf-modems-adapters/xstick) (ZB mesh version). For Z-Wave you should be able to use any [OpenZWave compatible dongle](https://github.com/OpenZWave/open-zwave/wiki/Controller-Compatibility-List), but so far we have only tested the [Sigma Designs UZB Stick](http://www.vesternet.com/z-wave-sigma-designs-usb-controller) and the [Aeotec Z-Stick](http://aeotec.com/z-wave-usb-stick) (Gen5). Be sure to get the correct device for your region as Z-Wave operating frequencies can vary between countries.

![](../../assets/751d944f26a7384f.png)


You’ll also need a microSD card to flash the software onto! We recommend at least 4GB.

![](../../assets/8a1b90c899eeb07d.png)


Then there’s the “things” themselves. The gateway already supports many different smart plugs, sensors and smart bulbs from lots of different brands using Zigbee, Z-Wave and WiFi. Take a look at the [wiki](https://github.com/mozilla-iot/wiki/wiki/Supported-Hardware) for devices which have already been tested. If you would like to contribute, we are always looking for volunteers to help us test more devices. Let us know what other devices you’d like to see working and consider building your own adapter add-on to make it work! (see later).

If you’re not quite ready to splash out on all this hardware, but you want to try out the gateway software, there’s now a Virtual Things add-on you can install to add virtual things to your gateway.

## Software

Next you’ll need to [download](https://iot.mozilla.org/gateway) the Things Gateway 0.3 software image for the Raspberry Pi and flash it onto your SD card. There are [various ways](https://www.raspberrypi.org/documentation/installation/installing-images/) of doing this but [Etcher](https://etcher.io/) is a graphical application for Windows, Linux and MacOS which makes it easy and safe to do.

![](../../assets/f85ba483199fc3c9.png)


If you want to experiment with the gateway software on your laptop or desktop computer, you can follow the [instructions on GitHub](https://github.com/mozilla-iot/gateway/blob/master/README.md) to download and build it yourself. We also have an experimental OpenWrt package and support for more platforms is coming soon. [Get in touch](https://iot.mozilla.org/contribute/) if you’re targeting a different platform.

## First Time Setup

Before booting up your gateway with the SD card inserted, ensure that any Zigbee or Z-Wave USB dongles are plugged in.

When you first boot the gateway, it acts as a WiFi hotspot broadcasting the network name (SSID) “Mozilla IoT Gateway”. You can connect to that WiFi hotspot with your laptop or smartphone which should automatically direct you to a setup page. Alternatively, you can connect the Raspberry Pi directly to your network using a network cable cable and type **gateway.local** into your browser to begin the setup process.

First, you’re given the option to connect to a WiFi network:


![](../../assets/6c64f25f49013034.png)


If you choose to connect to a WiFi network you’ll be prompted for the WiFi password and then you’ll need to make sure you’re connected to that same network in order to continue setup.

![](../../assets/ce073f01c0941b19.png)


Next, you’ll be asked to choose a unique subdomain for your gateway, which will automatically generate an SSL certificate for you using [LetsEncrypt](https://letsencrypt.org/) and set up a secure tunnel to the Internet so you can access the gateway remotely. You’ll be asked for an email address so you can reclaim your subdomain in future if necessary. You can also choose to use your own domain name if you don’t want to use the tunneling service, but you’ll need to generate your own SSL certificate and configure DNS yourself.

![](../../assets/66698f5a41650fb7.png)


You will then be securely redirected to your new subdomain and you’ll be prompted to create your user account on the gateway.

![](../../assets/26c7eaa05aa4d963.png)


You’ll then automatically be logged into the gateway and will be ready to start adding things. Note that the gateway’s web interface is a Progressive Web App that you can [add to homescreen](https://hacks.mozilla.org/2017/10/progressive-web-apps-firefox-android/) on your smartphone with Firefox.

![](../../assets/34f0e5b2f925d38f.png)


## Adding Things

To add devices to your gateway, click on the “+” icon at the bottom right of the screen. This will put all the attached adapters into pairing mode. Follow the instructions for your individual device to pair it with the gateway (this often involves pressing a button on the device while the gateway is in pairing mode).

Devices that have been successfully paired with the gateway will appear in the add device screen and you can give them a name of your choice before saving them on the gateway.

![](../../assets/fc160d41768fb06e.png)


The devices you’ve added will then appear on the Things screen.

![](../../assets/2cf03a7503b1af46.png)


You can turn things on and off with a single tap, or click on the expand button to go to an expanded view all of all the thing’s properties. For example a smart plug has an on/off switch and reports its current power consumption, voltage, current and frequency.

![](../../assets/0ef4e20609111543.png)


With a dimmable colour light, you can turn the light on and off, set its colour, and set its brightness level.

![](../../assets/65f9e52dc301cba4.png)


## Rules Engine

By clicking on the main menu you can access the rules engine.

![](../../assets/4cf8560b54ca1bc0.png)


The rules engine allows you to set ‘*if this, then that’* style rules for how devices interact with each other. For example, “If Smart Plug A turns on, turn on Smart Plug B”.

To create a rule, first click the “+” button at the bottom right of the rules screen. Then drag and drop things onto the screen and select the properties of the things you wish to connect together.


![](../../assets/186c558d615bb105.png)


You can give your rule a name and then click back to get back to the rules screen where you’ll see your new rule has been added.

![](../../assets/b454d060086654ac.png)


## Floorplan

Clicking on the “floorplan” option from the main menu allows you to arrange devices on a floorplan of your home. Click the edit button at the bottom right of the screen to upload a floorplan image.

![](../../assets/dc5a3f97d37166d5.png)


You’ll need to create the floorplan image yourself. This can be done with an online tool or graphics editor, or you can just scan of a hand drawn map of your home! An SVG file with white lines and a transparent background works best.

You can arrange devices on the floor plan by dragging them around the screen.

![](../../assets/894b5a7f039dbf7a.png)


Just click “save” when you’re done and you’ll see all of your devices laid out. You can click on them to access their expanded view.

![](../../assets/65a0e7e01429229c.png)


## Add-ons

The gateway has an add-ons system so that you can extend its capabilities. It comes with the Zigbee and Z-Wave adapter add-ons installed by default, but you can add support for additional adapters through the add-ons system under “settings” in the main menu.

![](../../assets/51844997b0ecc32e.png)


For example, there is a Virtual Things add-on which allows you to experiment with different types of web things without needing to buy any real hardware. Click the “+” button at the bottom right of the screen to see a list of available add-ons.

![](../../assets/9c97c71d80d583d0.png)


Click the “+ Add” button on any add-ons you want to install. When you navigate back to the add-ons screen you’ll see the list of add-ons that have been installed and you can enable or disable them.

![](../../assets/790182653cd9b76e.png)


In the next blog post, you’ll learn how to create, package, and share your own adapter add-ons in the programming language of your choice (e.g. JavaScript, Python or Rust).

## Voice UI

The gateway also comes with experimental voice controls which are turned off by default. You can enable this feature through “experiments” in settings.

![](../../assets/6b6e408568db39c9.png)


Once the “Speech Commands” experiment is turned on you’ll notice a microphone icon appear at the top right of the things screen.

![](../../assets/79a8e8834088d77e.png)


If the smartphone or PC you’re using has a microphone you can tap the microphone and issue a voice command like “Turn kitchen on” to control devices connected to the gateway.

The voice control is still very experimental and doesn’t yet recognise a very wide range of vocabulary, so it’s best to try to stick to common words like kitchen, balcony, living room, etc. This is an area we’ll be working on improving in future, in collaboration with the [Voice](https://voice.mozilla.org/) team at Mozilla.

## Updates

Your gateway software should automatically keep itself up to date with over-the-air updates from Mozilla. You can see what version of the gateway software you’re running by clicking on “updates” in Settings.

![](../../assets/71b06db82a5a1eee.png)


## What’s Coming Next?

In the next release, the Mozilla IoT team plans to create new gateway adapters to connect more existing smart home devices to the Web of Things. We are also starting work on a collection of software libraries in different programming languages, to help hackers and makers build their own native web things which directly expose the [Web Thing API](https://iot.mozilla.org/wot/), using existing platforms like Arduino and Android Things. You will then be able to add these things to the gateway by their URL.

We will continue to contribute to standardisation of a Web Thing Description format and API via the [W3C Web of Things Interest Group](https://www.w3.org/WoT/). By giving connected devices URLs on the web and using a standard data model and API, we can help create more interoperability on the Internet of Things.

The next blog post will explain how to build, package and share your own adapter add-on using the programming language of your choice, to add new capabilities to the Things Gateway.

## How to Contribute

We need your help! The easiest way to contribute is to [download](https://iot.mozilla.org/gateway/) the Things Gateway software image (0.3 at the time of writing) and test it out for yourself with a Raspberry Pi, to help us find bugs and suggest new features. You can view our [source code](https://github.com/mozilla-iot/gateway) and [file issues](https://github.com/mozilla-iot/gateway) on GitHub. You can also help us fix issues with pull requests and contribute your own adapters for the gateway.

If you want to ask questions, you can find us in #iot on [irc.mozilla.org](https://wiki.mozilla.org/IRC) or the “Mozilla IoT” topic in [Discourse](https://discourse.mozilla.org/c/iot). See [iot.mozilla.org](https://iot.mozilla.org) for more information and follow [@MozillaIoT](https://twitter.com/MozillaIoT) on Twitter if you want to be kept up to date with developments.

Happy hacking!


**Editor’s note:** Want to get started hacking? Here are a couple of projects to get you started:


## About
[
Ben Francis ](http://tola.me.uk)

Former Mozilla Software Engineer. W3C Invited Expert on Web Applications and the Web of Things.

## 75 comments

IlyaFebruary 6th, 2018 at 14:51Mike KienzleFebruary 7th, 2018 at 03:51brentFebruary 8th, 2018 at 18:08laoshawFebruary 6th, 2018 at 15:07Ben FrancisFebruary 6th, 2018 at 15:51PhilFebruary 6th, 2018 at 23:19Ben FrancisFebruary 7th, 2018 at 14:07Brendon KozlowskiFebruary 8th, 2018 at 09:50PatrickFebruary 7th, 2018 at 02:11Ben FrancisFebruary 7th, 2018 at 14:13John DoeFebruary 7th, 2018 at 07:21Ben FrancisFebruary 7th, 2018 at 14:14MartinFebruary 7th, 2018 at 07:48Ben FrancisFebruary 7th, 2018 at 14:17Tomasz WaraksaFebruary 7th, 2018 at 07:50Ben FrancisFebruary 7th, 2018 at 14:19Grand Master PFebruary 7th, 2018 at 12:19Ben FrancisFebruary 7th, 2018 at 14:20LinusFebruary 7th, 2018 at 14:25Ben FrancisFebruary 8th, 2018 at 01:39DanielFebruary 7th, 2018 at 14:35Ben FrancisFebruary 8th, 2018 at 01:42Mike HankeyFebruary 7th, 2018 at 16:16Ben FrancisFebruary 8th, 2018 at 01:51AlexFebruary 7th, 2018 at 17:44Ben FrancisFebruary 8th, 2018 at 01:53NickFebruary 7th, 2018 at 19:22Ben FrancisFebruary 8th, 2018 at 01:55Darryl KFebruary 7th, 2018 at 19:22Ben FrancisFebruary 8th, 2018 at 01:58GarnetFebruary 8th, 2018 at 07:43Ben FrancisFebruary 8th, 2018 at 09:49Trevor OlssonFebruary 8th, 2018 at 08:26Ben FrancisFebruary 8th, 2018 at 09:50James TaylorFebruary 8th, 2018 at 09:02Ben FrancisFebruary 8th, 2018 at 09:54Chase FarmerFebruary 19th, 2018 at 16:59Ben FrancisFebruary 20th, 2018 at 03:26LarsFebruary 8th, 2018 at 09:33Ben FrancisFebruary 8th, 2018 at 09:56Frederick BlaisFebruary 8th, 2018 at 15:10Ben FrancisFebruary 16th, 2018 at 11:30JanFebruary 8th, 2018 at 20:05Ben FrancisFebruary 16th, 2018 at 11:31johnFebruary 9th, 2018 at 03:13Kristian PolsoFebruary 9th, 2018 at 04:49Ben FrancisFebruary 16th, 2018 at 11:32kajmajFebruary 9th, 2018 at 05:14Ben FrancisFebruary 9th, 2018 at 06:37Guy McSwainFebruary 9th, 2018 at 23:10Ben FrancisFebruary 16th, 2018 at 11:36Harvey KingFebruary 11th, 2018 at 21:42Ben FrancisFebruary 16th, 2018 at 11:37MarkusFebruary 12th, 2018 at 01:22tjFebruary 12th, 2018 at 11:35Ben FrancisFebruary 16th, 2018 at 11:38AjayFebruary 12th, 2018 at 12:44Ben FrancisFebruary 16th, 2018 at 11:39robertFebruary 13th, 2018 at 14:02Ben FrancisFebruary 16th, 2018 at 11:40GUY FAUQUEMBERGUEFebruary 15th, 2018 at 06:50Ben FrancisFebruary 16th, 2018 at 11:44BenFebruary 16th, 2018 at 06:09ZanFebruary 16th, 2018 at 10:53Ben FrancisFebruary 16th, 2018 at 11:47FredFebruary 18th, 2018 at 06:40Ben FrancisFebruary 20th, 2018 at 03:04StephFebruary 20th, 2018 at 16:42Ben FrancisFebruary 21st, 2018 at 08:03bobFebruary 22nd, 2018 at 15:12Ben FrancisFebruary 23rd, 2018 at 04:13HarryFebruary 23rd, 2018 at 23:04Ben FrancisFebruary 26th, 2018 at 04:31Camilo MartinFebruary 27th, 2018 at 08:36Ben FrancisFebruary 28th, 2018 at 05:18