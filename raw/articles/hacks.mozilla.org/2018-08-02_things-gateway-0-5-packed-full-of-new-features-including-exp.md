---
title: Things Gateway 0.5 packed full of new features, including experimental smart
  assistant – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2018/08/things-gateway-0-5-features-experimental-smart-assistant/
author: Ben Francis
published: '2018-08-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The Things Gateway from Mozilla lets you directly monitor and control your home over the web, without a middleman.

Today the Mozilla IoT team is excited to announce the [0.5 release of the Things Gateway](https://iot.mozilla.org/gateway/), which is packed full of new features including customisable devices, a more powerful rules engine, an interactive floorplan and an experimental smart assistant you can talk to.

## Customisable Things

### Custom Capabilities

A powerful new “capabilities” system means that devices are no longer restricted to a predefined set of Web Thing Types, but can be assembled from an extensible schema-based system of “[capabilities](https://iot.mozilla.org/wot/#context-member)” through our new [schema repository](http://iot.mozilla.org/schemas).

This means that developers have much more flexibility to create weird and wacky devices, and users have more control over how the device is used. So if you have a [door sensor which also happens to be a temperature sensor](https://www.smartthings.com/gb/products/smartthings-multipurpose-sensor), a [smart plug which also has a multi-colour LED ring](https://aeotec.com/z-wave-plug-in-switch), or a [whole bunch of sensors all in one device](https://aeotec.com/z-wave-sensor), you’re not limited by restrictive device types.

This also provides more flexibility to developers who want to build their own web things using the [Things Framework](https://iot.mozilla.org/things/), which now also has support for [Rust](https://github.com/mozilla-iot/webthing-rust), [MicroPython](https://github.com/mozilla-iot/webthing-upy) and [Arduino](https://github.com/mozilla-iot/webthing-arduino).

### Custom Icons

When a user adds a device to the gateway they can now choose what main function they want to use it for and what icon is used to represent it.

You can even upload your own custom icon if you want to.

### Custom Web Interface

In addition to the built-in UI the gateway generates for devices, web things can now provide a link to a custom web interface designed specifically for any given device. This is useful for complex or unusual devices like a robot or a “[pixel wall](https://github.com/RutgersGRID/pixelwall)” where a custom designed UI can be much more user friendly.

### Actions & Events

In addition to properties (like “on/off”, “level” and “color”), the gateway UI can now represent actions like “fade” which are triggered with a button and can accept input via a form.

The UI can also display an event log for a device.

![Screenshot of event log UI](../../assets/c4cd72655198ade6.png)


## Powerful Rules Engine

The rules engine now supports rules with multiple inputs and multiple outputs. Simple rules are still just as easy to create, but more advanced rules can make use of “if”, “while”, “and”, “or” and “equals” operators to create more sophisticated automations through an intuitive drag and drop interface.

It’s also now possible to set colours and strings as outputs.

## Interactive Floorplan

The floorplan view is even more useful now that you can view the status of devices and even control them from directly inside the floorplan. Simply tap things to turn them on and off, or long press to get to their detail view. This provides a helpful visual overview of the status of your whole smart home.

## Smart Assistant Experiment

A feature we’re particularly excited about is a new smart assistant you can talk to via a chat style interface, either by typing or using your voice.

You can give it commands like “Turn the kitchen light on” and it will respond to you to confirm the action. So far it can understand a basic set of commands to turn devices on and off, set levels, set colours and set colour temperatures.

The smart assistant is still very experimental so it’s currently turned off by default, but you can enable it through Settings -> Smart Assistant UI.

## Other Changes

Other new features include developer settings which allow you to view system logs and enable/disable the gateway’s SSH server so you can log in via the command line.

It’s also now much easier to rename devices and you can now also add devices that require a pin number to be entered during pairing.

## How to Get Involved

To try out the latest version of the gateway, [download](https://iot.mozilla.org/gateway/) the software image from our website to use on a Raspberry Pi. If you already have a gateway set up, you should notice it automatically update itself to the 0.5 release.

As always, we welcome your [contributions](https://iot.mozilla.org/contribute/) to our open source project. You can provide feedback and ask questions on [Discourse](https://discourse.mozilla.org/c/iot) and file bugs and send pull requests on [GitHub](https://github.com/mozilla-iot).

Happy hacking!

## About
[
Ben Francis ](http://tola.me.uk)

Former Mozilla Software Engineer. W3C Invited Expert on Web Applications and the Web of Things.

## 5 comments

PrathamAugust 2nd, 2018 at 08:50Ben FrancisAugust 3rd, 2018 at 05:05tapperAugust 2nd, 2018 at 16:18Ben FrancisAugust 3rd, 2018 at 05:16OutpoxAugust 3rd, 2018 at 01:01