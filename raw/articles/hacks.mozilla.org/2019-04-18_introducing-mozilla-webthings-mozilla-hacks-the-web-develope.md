---
title: Introducing Mozilla WebThings – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2019/04/introducing-mozilla-webthings/
author: Ben Francis
published: '2019-04-18'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The Mozilla IoT team is excited to announce that after two years of development and seven quarterly software updates that have generated significant interest from the developer & maker community, Project Things is graduating from its early experimental phase and from now on will be known as Mozilla WebThings.

Mozilla’s [mission](https://www.mozilla.org/en-GB/mission/) is to *“ensure the Internet is a global public resource, open and accessible to all. An Internet that truly puts people first, where individuals can shape their own experience and are empowered, safe and independent.”*

The [Mozilla IoT](https://iot.mozilla.org/) team’s mission is to create a [Web of Things](https://en.wikipedia.org/wiki/Web_of_Things) implementation which embodies those values and helps drive IoT standards for security, privacy and interoperability.

[Mozilla WebThings](https://iot.mozilla.org) is an open platform for monitoring and controlling devices over the web, including:

[WebThings Gateway](https://iot.mozilla.org/gateway)– a software distribution for smart home gateways focused on privacy, security and interoperability[WebThings Framework](https://iot.mozilla.org/framework)– a collection of reusable software components to help developers build their own web things


We look forward to a future in which Mozilla WebThings software is installed on commercial products that can provide consumers with a trusted agent for their “smart”, connected home.

# WebThings Gateway 0.8

The WebThings Gateway 0.8 release is available to download from today. If you have an existing Things Gateway it should have automatically updated itself. This latest release includes new features which allow you to privately log data from all your smart home devices, a new alarms capability and a new network settings UI.

## Logs

Have you ever wanted to know how many times the door was opened and closed while you were out? Are you curious about energy consumption of appliances plugged into your smart plugs? With the new logs features you can privately log data from all your smart home devices and visualise that data using interactive graphs.

In order to enable the new logging features go to the main menu ➡ Settings ➡ Experiments and enable the “Logs” option.

You’ll then see the Logs option in the main menu. From there you can click the “+” button to choose a device property to log, including how long to retain the data.

The time series plots can be viewed by hour, day, or week, and a scroll bar lets users scroll back through time. This feature is still experimental, but viewing these logs will help you understand the kinds of data your smart home devices are collecting and think about how much of that data you are comfortable sharing with others via third party services.

Note: If booting WebThings Gateway from an SD card on a Raspberry Pi, please be aware that logging large amounts of data to the SD card may make the card wear out more quickly!

## Alarms

Home safety and security are among the big potential benefits of smart home systems. If one of your “dumb” alarms is triggered while you are at work, how will you know? Even if someone in the vicinity hears it, will they take action? Do they know who to call? WebThings Gateway 0.8 provides a new alarms capability for devices like smoke alarms, carbon monoxide alarms or burglar alarms.

This means you can now check whether an alarm is currently active, and configure rules to notify you if an alarm is triggered while you’re away from home.

## Network Settings

In previous releases, moving your gateway from one wireless network to another when the previous Wi-Fi access point was still active could not be done without console access and command line changes directly on the Raspberry Pi. With the 0.8 release, it is now possible to re-configure your gateway’s network settings from the web interface. These new settings can be found under Settings ➡ Network.

You can either configure the Ethernet port (with a dynamic or static IP address) or re-scan available wireless networks and change the Wi-Fi access point that the gateway is connected to.

# WebThings Gateway for Wireless Routers

We’re also excited to share that we’ve been working on a new [OpenWrt](https://openwrt.org/)-based build of WebThings Gateway, aimed at consumer wireless routers. This version of WebThings Gateway will be able to act as a wifi access point itself, rather than just connect to an existing wireless network as a client.

This is the beginning of a new phase of development of our gateway software, as it evolves into a software distribution for consumer wireless routers. Look out for further announcements in the coming weeks.

# Online Documentation

Along with a refresh of the [Mozilla IoT website](https://iot.mozilla.org/), we have made a start on some online user & developer [documentation](https://iot.mozilla.org/docs/) for the WebThings Gateway and WebThings Framework. If you’d like to contribute to this documentation you can do so via [GitHub](https://github.com/mozilla-iot/docs/).

Thank you for all the contributions we’ve received so far from our wonderful [Mozilla IoT community](https://iot.mozilla.org/community). We look forward to this new and exciting phase of the project!

## About
[
Ben Francis ](http://tola.me.uk)

Former Mozilla Software Engineer. W3C Invited Expert on Web Applications and the Web of Things.

## 33 comments

VladimirApril 18th, 2019 at 16:42Ben FrancisApril 19th, 2019 at 07:36VladimirApril 25th, 2019 at 17:51VladimirApril 18th, 2019 at 16:47Ben FrancisApril 19th, 2019 at 07:37Amitabh OjhaApril 20th, 2019 at 08:16ShaunApril 18th, 2019 at 16:50Ben FrancisApril 19th, 2019 at 07:39blake breadApril 19th, 2019 at 15:46NathanApril 18th, 2019 at 22:04noscripterApril 18th, 2019 at 23:37shivanshu1333April 19th, 2019 at 01:34shivanshu1333April 19th, 2019 at 01:38KenApril 19th, 2019 at 09:23Ben FrancisApril 23rd, 2019 at 05:08Noah ChouApril 19th, 2019 at 10:47NitinsApril 20th, 2019 at 05:23Ben FrancisApril 23rd, 2019 at 05:11BonzadogApril 20th, 2019 at 07:44Le TuApril 20th, 2019 at 18:43Ben FrancisApril 23rd, 2019 at 05:23RyanApril 21st, 2019 at 12:40OlavApril 23rd, 2019 at 01:59Ben FrancisApril 23rd, 2019 at 05:24OlavMay 3rd, 2019 at 10:46JuhuwaApril 23rd, 2019 at 04:37Curious GeorgeApril 24th, 2019 at 00:19Ben FrancisApril 24th, 2019 at 05:41VSApril 30th, 2019 at 01:55Ben FrancisApril 30th, 2019 at 04:08StefanJMay 1st, 2019 at 02:45ANEESH DUAMay 17th, 2019 at 04:04Ben FrancisMay 24th, 2019 at 03:07