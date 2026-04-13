---
title: Home Monitoring with Things Gateway 0.6 – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2018/10/home-monitoring-with-things-gateway-0-6/
author: Ben Francis
published: '2018-10-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

When it comes to smart home devices, protecting the safety and security of your home when you aren’t there is a popular area of adoption. Traditional home security systems are either completely offline (an alarm sounds in the house, but nobody is notified) or professionally monitored (with costly subscription services). Self monitoring of your connected home therefore makes sense, but many current smart home solutions still require ongoing service fees and send your private data to a centralised cloud service.

The latest version of the [Things Gateway](https://iot.mozilla.org/gateway/) rolls out today with new home monitoring features that let you directly monitor your home over the web, without a middleman. That means no monthly fees, your private data stays in your home by default, and you can choose from a variety of sensors from different brands.

Version 0.6 adds support for door sensors, motion sensors and customisable push notifications. Other enhancements include support for push buttons and a wider range of Apple HomeKit devices, as well as general robustness improvements and better error reporting.

### Sensors

The latest update comes with support for door/window sensors and motion sensors, including the [SmartThings Motion Sensor](https://www.smartthings.com/gb/products/smartthings-motion-sensor-2016) and [SmartThings Multipurpose Sensor](https://www.smartthings.com/gb/products/smartthings-multipurpose-sensor-2016).These sensors make great triggers for a home monitoring system and also report temperature, battery level and tamper detection.![An illustration with icons of various sensors used in home monitoring](../../assets/19b3961d2c3a091e.png)


### Push Notifications

You can now create rules which trigger a push notification to your desktop, laptop, tablet or smartphone. An example use case for this is to notify you when a door has been opened or motion is detected in your home, but you can use notifications for whatever you like!

To create a rule which triggers a push notification, simply drag and drop the notification output and customize it with your own message.

Thanks to the power of ![A diagram showing how the Intruder Alarm is triggered by the interaction of the sensors.](../../assets/95b47f3e3ff75f61.png)


[Progressive Web Apps](https://developer.mozilla.org/en-US/docs/Web/Apps/Progressive), if you’ve installed the gateway’s web app on your smartphone or tablet you’ll receive notifications even if the web app is closed.

### Push Buttons

We’ve also added support for push buttons, like the [SmartThings Button](https://www.samsung.com/us/smart-home/smartthings/buttons/samsung-smartthings-button-gp-u999sjvleaa/), which you can program to trigger any action you like using the rules engine. Use a button to simply turn a light on, or set a whole scene with multiple outputs.

### Error Reporting

0.6 also comes with a range of robustness improvements including connection detection and error reporting. That means it will be easier to tell whether you have lost connectivity to the gateway, or one of your devices has dropped offline, and if something goes wrong with an add-on, you’ll be informed about it inside the gateway UI.

If a device has dropped offline, its icon is displayed as translucent until it comes back online. If your web app loses connectivity with the gateway, you’ll see a message appear at the bottom of the screen.![A diagram of all the sensors showing their status.](../../assets/1ca69319149fe3de.png)


### HomeKit

The [HomeKit adapter add-on](https://github.com/mozilla-iot/homekit-adapter) now [supports](https://github.com/mozilla-iot/wiki/wiki/Supported-Hardware) a wider range of Apple HomeKit compatible devices including:

#### Smart plugs

#### Bridges

#### Light bulbs

#### Sensors

These devices use the built-in Bluetooth or WiFi support of your Raspberry Pi-based gateway, so you don’t even need a USB dongle.

### Download

You can [download version 0.6](https://iot.mozilla.org/gateway/) today from the website. If you’ve already built your own Things Gateway with a Raspberry Pi and have it connected to the Internet, it should automatically update itself soon.

We can’t wait to see what creative things you do with all these new features. Be sure to let us know on [Discourse](https://discourse.mozilla.org/c/iot) and [Twitter](https://twitter.com/MozillaIoT)!

## About
[
Ben Francis ](http://tola.me.uk)

Former Mozilla Software Engineer. W3C Invited Expert on Web Applications and the Web of Things.

## 16 comments

EduardoOctober 16th, 2018 at 02:55Ben FrancisOctober 17th, 2018 at 06:58Michael A DravesOctober 18th, 2018 at 10:53WimOctober 25th, 2018 at 00:59Ben FrancisOctober 25th, 2018 at 05:07WimOctober 26th, 2018 at 05:10Ben FrancisOctober 29th, 2018 at 07:21WimNovember 1st, 2018 at 14:32Ben FrancisNovember 2nd, 2018 at 06:32wimNovember 4th, 2018 at 11:36Ben FrancisNovember 5th, 2018 at 05:07Ian ArchbellOctober 27th, 2018 at 11:08Bob NmeetOctober 29th, 2018 at 11:46Ben FrancisOctober 29th, 2018 at 11:55Rahul BhagwatNovember 5th, 2018 at 17:00Ben FrancisNovember 6th, 2018 at 07:03