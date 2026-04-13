---
title: Firefox OS Simulator – previewing version 3.0 – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/03/firefox-os-simulator-previewing-version-3-0/
author: Robert Nyman
published: '2013-03-13'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Three months ago we were proud to release the [1.0 version of the Firefox OS Simulator](https://hacks.mozilla.org/2012/12/firefox-os-simulator-1-0-is-here/). We’ve made a lot of progress since, and version 2.0 came out about a month ago ([latest official version](https://addons.mozilla.org/en-US/firefox/addon/firefox-os-simulator/)). Now, moving forward, we’d like to present and introduce you to a preview of the upcoming 3.0 version!

We discussed whether we should talk about this new version yet, since it’s a bit rough around the edges, but we decided to give it a go for two reasons:

- We’re Mozilla. We do things in the open, and we share our progress. Because we want you to know what’s going on and to be able to come along with us in the process
- It gives you an unique opportunity to test it out, give feedback, contribute and much more before it’s released

## New features in the preview

We’ve listened to the feedback and have tried to target the most common features being requested and well-needed. New features include:

- Push to Device
- Rotation simulation
- Basic geolocation API simulation
- Manifest validation
- Stability fixes for installation and updates to apps
- Newer versions of the Firefox rendering engine and Gaia (the UI for Firefox OS)

### Push to Device

This means that if you have an existing device supporting Firefox OS, connected via USB, you will be able to push apps installed in the Firefox OS Simulator directly to that device.

Please note:

- Remote debugging has to be enabled on the device, via
`Settings > Device information > More Information > Developer > Remote debugging`

- On Linux (at least Ubuntu), you must create the file
`/etc/udev/rules.d/51-android.rules`

as root and then add a manufacturer-specific entry for the device as described by[Android’s Setting up a Device for Development](http://developer.android.com/tools/device.html#setting-up). Example for one of our test devices:entry:

`SUBSYSTEM=="usb", ATTR{idVendor}==" 19d2", MODE="0666", GROUP="plugdev"`

- Not complete Windows support yet. Planned to make it into the final release.
- Make sure you have the latest version of Firefox OS on your device (especially due to recent fixes like
[bug 842725](https://bugzilla.mozilla.org/show_bug.cgi?id=842725))

![image](../../assets/ce96e9fbdab60963.png)


### Rotation simulation

There’s now a feature to rotate the simulator, get events and more, to adapt your contents to both portrait and landscape. Supports the `mozorientationchange`

event.

![image](../../assets/18f84d0105d92d09.png)


### Basic geolocation API simulation

The simulator now also supports geolocation, so you can test it in your app, and read out longitude and latitude values.

Coming soon: an enhancement that lets you specify the geolocation to provide!

### Manifest validation

When you add an app to the Firefox OS Simulator, it also does a quick validation of your manifest file for errors and warnings, including problems that prevent installing the app in the Simulator, usage of APIs that the Simulator doesn’t yet simulate (not all APIs in there yet), and missing properties that are required by the Marketplace or devices.

![image](../../assets/2cefc3b9bfa8039f.png)


## Downloading the preview

We have all the [versions of the Firefox OS Simulator on our FTP server](https://ftp.mozilla.org/pub/mozilla.org/labs/r2d2b2g/), under its working name r2d2b2g. Here are the direct links to the installation files (installs as an extension in Firefox)

[Firefox OS Simulator Preview for Windows](https://ftp.mozilla.org/pub/mozilla.org/labs/r2d2b2g/r2d2b2g-windows.xpi)[Firefox OS Simulator Preview for Mac](https://ftp.mozilla.org/pub/mozilla.org/labs/r2d2b2g/r2d2b2g-mac.xpi)[Firefox OS Simulator Preview for Linux](https://ftp.mozilla.org/pub/mozilla.org/labs/r2d2b2g/r2d2b2g-linux.xpi)

Once installed, it will be available in Firefox in the Tools > Web Developer menu:

![image](../../assets/543038381053ea15.png)


## Give us feedback!

Please let us know in the comments here or [by filing a bug](https://github.com/mozilla/r2d2b2g/issues?state=open). Hopefully you will like the improvements and they will benefit you with developing apps!

## Getting started with Firefox OS & building Open Web Apps

To get started, we have had a number of articles here on Mozilla Hacks previously:

[Getting started with Open Web Apps – why and how](https://hacks.mozilla.org/2013/02/getting-started-with-open-web-apps-why-and-how/)[Using WebAPIs to make the web layer more capable](https://hacks.mozilla.org/2013/02/using-webapis-to-make-the-web-layer-more-capable/)[Introducing the Firefox OS Boilerplate App](https://hacks.mozilla.org/2013/01/introducing-the-firefox-os-boilerplate-app/)[Introducing Web Activities](https://hacks.mozilla.org/2013/01/introducing-web-activities/)

Additionally we have some other resources:

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 61 comments

x I’m tcMarch 13th, 2013 at 09:20VincentMarch 13th, 2013 at 11:28Robert Nyman [Editor]March 13th, 2013 at 12:11SankalpMarch 13th, 2013 at 13:36Robert Nyman [Editor]March 13th, 2013 at 17:01Igor CostaMarch 13th, 2013 at 18:13Robert Nyman [Editor]March 14th, 2013 at 02:10FlakiMarch 14th, 2013 at 04:50Robert Nyman [Editor]March 14th, 2013 at 05:42crayMarch 14th, 2013 at 05:05Myk MelezMarch 18th, 2013 at 23:55Gsbriele VidaliMarch 14th, 2013 at 06:48Robert Nyman [Editor]March 14th, 2013 at 08:48Philip CaseyMarch 14th, 2013 at 17:05Robert Nyman [Editor]March 15th, 2013 at 02:38nishanMarch 16th, 2013 at 07:58Robert Nyman [Editor]March 18th, 2013 at 02:57Ken SaundersMarch 17th, 2013 at 00:48Robert Nyman [Editor]March 18th, 2013 at 02:54ZakirMarch 18th, 2013 at 19:06Robert Nyman [Editor]March 19th, 2013 at 01:06CarterMarch 19th, 2013 at 15:15Robert Nyman [Editor]March 19th, 2013 at 16:23DeanMarch 19th, 2013 at 15:29Robert Nyman [Editor]March 19th, 2013 at 16:24gabrieleMarch 20th, 2013 at 03:52Robert Nyman [Editor]March 20th, 2013 at 06:05CarterMarch 19th, 2013 at 15:39Robert Nyman [Editor]March 19th, 2013 at 16:25monster1612March 19th, 2013 at 16:08Robert Nyman [Editor]March 19th, 2013 at 16:25ZakirMarch 20th, 2013 at 07:44DanielMarch 20th, 2013 at 08:29Robert Nyman [Editor]March 20th, 2013 at 13:26zakirMarch 21st, 2013 at 17:28Robert Nyman [Editor]March 22nd, 2013 at 02:40GabrieleMarch 22nd, 2013 at 02:59Robert Nyman [Editor]March 22nd, 2013 at 03:58GabrieleMarch 22nd, 2013 at 04:06GabrieleMarch 22nd, 2013 at 02:55Variya Soft SolutionsMarch 24th, 2013 at 09:57viswaprasathMarch 25th, 2013 at 09:08llageMarch 29th, 2013 at 08:49Robert Nyman [Editor]April 1st, 2013 at 01:04AnirudhaMarch 30th, 2013 at 21:05Robert Nyman [Editor]April 1st, 2013 at 01:05numMarch 30th, 2013 at 21:50Robert Nyman [Editor]April 1st, 2013 at 01:05andresApril 3rd, 2013 at 09:48Robert Nyman [Editor]April 4th, 2013 at 02:28GabrieleApril 4th, 2013 at 04:07Robert Nyman [Editor]April 5th, 2013 at 01:25gabriele vidaliApril 5th, 2013 at 01:44Robert Nyman [Editor]April 5th, 2013 at 02:20andresApril 10th, 2013 at 17:12Gabriele VidaliApril 21st, 2013 at 16:52Caspy7April 20th, 2013 at 13:38Myk MelezApril 22nd, 2013 at 11:38Caspy7April 22nd, 2013 at 20:16Robert Nyman [Editor]April 22nd, 2013 at 02:09Robert Nyman [Editor]April 22nd, 2013 at 02:09