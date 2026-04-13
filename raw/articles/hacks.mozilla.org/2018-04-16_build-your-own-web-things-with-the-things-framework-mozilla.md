---
title: Build your own web things with the Things Framework – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2018/04/build-your-own-web-things-with-the-things-framework/
author: Ben Francis
published: '2018-04-16'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Last year Mozilla started [Project Things](https://iot.mozilla.org) to help developers connect physical “things” to the web in a safe, secure and interoperable way.

In February we [announced](https://hacks.mozilla.org/2018/02/how-to-build-your-own-private-smart-home-with-a-raspberry-pi-and-mozillas-things-gateway/) the 0.3 release of the [Things Gateway](https://iot.mozilla.org/gateway/) which bridges existing smart home devices to the Web of Things. Today we’re excited to tell you about the beginnings of the [Things Framework](https://iot.mozilla.org/things) which aims to help developers build their own “native web things”, and the 0.4 release of the Things Gateway which now supports a wider range of smart home devices.

## Things Framework

The [Things Framework](https://iot.mozilla.org/things) is a collection of reusable software components to help you build your own web things, which directly expose the [Web Thing API](https://iot.mozilla.org/wot/). That means they can be discovered by a Web of Things client or gateway, which can monitor and control them over the web.

A web thing has a [Web Thing Description](https://iot.mozilla.org/wot/#web-thing-description) which describes the device’s capabilities, and exposes a Web Thing [REST API](https://iot.mozilla.org/wot/#web-thing-rest-api) and/or [WebSocket API](https://iot.mozilla.org/wot/#web-thing-websocket-api), so that it can be monitored and controlled. The Thing Description provides machine-readable metadata about a device and its available [properties](https://iot.mozilla.org/wot/#property-object), [actions](https://iot.mozilla.org/wot/#action-object) and [events](https://iot.mozilla.org/wot/#event-object). The Web Thing API lets a client read and write its properties, request actions and subscribe to its events.

You can get started today by turning [Android things](https://developer.android.com/things/index.html) into web things using our [Java web thing library](https://github.com/mozilla-iot/webthing-java), or if you prefer to build things with [Python](https://github.com/mozilla-iot/webthing-python) or [NodeJS](https://github.com/mozilla-iot/webthing-node), we also have you covered there. We have some early examples of how to build web things using WiFi-enabled microcontrollers like the [ESP8266](https://github.com/mozilla-iot/webthing-esp8266), and a [serial gateway adapter](https://github.com/mozilla-iot/serial-adapter) for chipsets with more constrained resources. We’re releasing these libraries at a very early stage of development so that you can [provide us with feedback](https://discourse.mozilla.org/c/iot) and help us to help you build better web things.

In the coming days we’ll be blogging about how to use each of these new web thing libraries, to help you get hands-on building your own devices.

These are still experimental technologies in the process of standardisation [at the W3C](https://www.w3.org/WoT/), but we hope our early open source implementations will help developers try out the Web of Things and help us to improve it.

## Add Web Things

With the 0.4 release of the [Things Gateway](https://iot.mozilla.org/gateway/), you can now add native web things to your gateway, to control them alongside all your other smart home devices. The advantage of native web things is that they don’t need a custom gateway adapter because they follow a common standard using existing web technologies.

Web things can broadcast their web address using [mDNS](https://en.wikipedia.org/wiki/Multicast_DNS) or a Bluetooth beacon so that they can be discovered by the gateway, or they can be manually added by their URL. Simply click on the “+” button in the Things screen of the gateway and either allow it to scan for devices, or manually copy and paste a web thing URL using the “Add by URL…” link.

## New Add-ons

The 0.4 gateway release also comes with a larger selection of add-on adapters which add support for smart home protocols like Apple HomeKit, and devices from LIFX and Broadlink.

You will also notice that, like the gateway itself, add-ons now get automatically updated so you’ll always have the latest version.

## Other Changes

There are a host of other changes in the 0.4 release. You can now create rules based on numerical and color properties, we’ve added support for color temperature light bulbs and there’s a new configuration UI for add-ons. There are new developer features like Windows support, the ability to view and download logs and a new local token service. The local token service provides a simple onboarding experience for people who want to use OAuth to access the gateway’s Web Thing API.

You can see a full changelog for the 0.4 release [here](https://github.com/mozilla-iot/gateway/releases/tag/0.4.0).

We want to say a big thank you to our growing Mozilla IoT community for contributing some of the new add-ons, providing us with feedback, reporting bugs, writing documentation and for generally helping us push Project Things forward. We can’t do this without you!

You can find out more about the Things Framework at [iot.mozilla.org/things](https://iot.mozilla.org/things), and feel free to head over to [Discourse](https://discourse.mozilla.org/c/iot) with any questions and comments.

## About
[
Ben Francis ](http://tola.me.uk)

Former Mozilla Software Engineer. W3C Invited Expert on Web Applications and the Web of Things.

## 12 comments

Attila CsibiApril 17th, 2018 at 02:54Ben FrancisApril 17th, 2018 at 07:50Randy ConstanApril 17th, 2018 at 14:02Ben FrancisApril 18th, 2018 at 07:02Randy ConstanApril 20th, 2018 at 11:07Ben FrancisApril 20th, 2018 at 11:27Randy ConstanApril 23rd, 2018 at 09:41Ben FrancisApril 23rd, 2018 at 10:03AmberApril 19th, 2018 at 07:30Kingsley UchunorApril 30th, 2018 at 10:04L3dMay 11th, 2018 at 01:13RavinderMay 11th, 2018 at 03:38