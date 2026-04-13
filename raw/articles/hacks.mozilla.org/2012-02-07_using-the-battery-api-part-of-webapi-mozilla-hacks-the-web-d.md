---
title: Using the Battery API – Part of WebAPI – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2012/02/using-the-battery-api-part-of-webapi/
author: Robert Nyman
published: '2012-02-07'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Detecting battery level in a device or computer can help you inform the user of the current status. Within [Mozilla’s WebAPI](https://wiki.mozilla.org/WebAPI), we have the [Battery API](https://wiki.mozilla.org/WebAPI/BatteryAPI) to offer that possibility.


## Accessing the battery

First, it’s a matter of accessing the battery object:

`var battery = navigator.mozBattery;`


## Properties

There are a few properties offered to detect the charging level of the battery in the device:

- Battery level
- Check the currenty battery level. Returns a value between 0 and 1.
- Battery charging
- A boolean, returning if the device/computer is currently being charged.
- Battery chargingTime
- Time left in seconds until it is fully charged. Available when charging.
- Battery dischargingTime
- Time left in seconds until it is discharged. Available when not charging.

`// Get battery level in percentage`


var batteryLevel = battery.level * 100 + "%";

// Get whether device is charging or not

var chargingStatus = battery.charging;

// Time until the device is fully charged

var batteryCharged = battery.chargingTime;

// Time until the device is discharged

var batteryDischarged = battery.dischargingTime;


## Events

There are four events available for detecting changes to the battery’s status:

- levelchange
- If the battery level changes.
- chargingchange
- Detect if the device went from being charged to unplugged, or vice versa.
- chargingtimechange
- When the device’s charging time changes (when plugged in)
- dischargingtimechange
- When the device’s discharging time changed (when unplugged)

```
battery.addEventLister("levelchange", function () {
// Device's battery level changed
}, false);
battery.addEventListener("chargingchange", function () {
// Device got plugged in to power, or unplugged
}, false);
battery.addEventListener("chargingtimechange", function () {
// Device's charging time changed
}, false);
battery.addEventListener("dischargingtimechange", function () {
// Device's discharging time changed
}, false);
```


## Device support

Battery API is supported in [Firefox Beta](http://www.mozilla.org/firefox/beta/) on:

- Android (
[Firefox Aurora](http://www.mozilla.org/firefox/aurora/)only, for now) - Windows
- Linux (for those distros that have
[UPower](http://upower.freedesktop.org/)installed – bundled with most nowadays)

Right now we don’t have anyone working on the Mac OS X implemementation, so if you have the skills, [we’d love to see you contribute](https://bugzilla.mozilla.org/show_bug.cgi?id=696045)!

## Demo and code

I’ve put together a basic [demo of the Battery API](http://robnyman.github.com/battery/) and code is also available in the [Battery API repository on GitHub](https://github.com/robnyman/robnyman.github.com/tree/master/battery).

If you don’t experience the expected results on your device, please [file a bug](https://bugzilla.mozilla.org/enter_bug.cgi) and we can look into it. This feature is experimental at this time, and may not be ready for production use just yet.

### Update: September 26th, 2012

Since this post was published, [this API has now been unprefixed](https://hacks.mozilla.org/2012/02/using-the-battery-api-part-of-webapi/comment-page-1/#comment-1809129) and support in Mac OS X has been added.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 16 comments

Gervase MarkhamFebruary 7th, 2012 at 07:14Robert NymanFebruary 8th, 2012 at 01:11David MulderFebruary 8th, 2012 at 01:21Robert NymanFebruary 8th, 2012 at 01:42Scott MattocksFebruary 8th, 2012 at 14:23Robert NymanFebruary 8th, 2012 at 14:45louisremiFebruary 8th, 2012 at 04:30Robert NymanFebruary 8th, 2012 at 14:46PierreFebruary 9th, 2012 at 08:59Robert NymanFebruary 9th, 2012 at 10:11Tim McCormackSeptember 6th, 2012 at 13:05Robert NymanSeptember 7th, 2012 at 00:15Reuben MoraisSeptember 25th, 2012 at 07:28Robert NymanSeptember 26th, 2012 at 00:59Patrick StadlerNovember 12th, 2012 at 00:52Robert NymanNovember 12th, 2012 at 06:01