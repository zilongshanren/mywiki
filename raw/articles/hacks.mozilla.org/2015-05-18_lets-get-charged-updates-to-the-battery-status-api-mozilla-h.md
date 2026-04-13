---
title: 'Let’s get charged: Updates to the Battery Status API – Mozilla Hacks - the
  Web developer blog'
url: https://hacks.mozilla.org/2015/05/lets-get-charged-updates-to-the-battery-status-api/
author: Francesco Iovine
published: '2015-05-18'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[Web APIs](https://developer.mozilla.org/en-US/docs/WebAPI) provide a way for Open Web Apps to access device hardware, data and sensors through JavaScript, and open the doors to a number of possibilities especially for mobile devices, TVs, interactive kiosks, and Internet of Things (IoT) applications.

Knowing the battery status of a device can be useful in a number of situations or use cases. Here are some examples:

- Utility apps that collect statistics on battery usage or simply inform the user if the device is charged enough to play a game, watch a movie, or browse the Web.
- High-quality apps that optimize battery consumption: for example, an email client may check the server for new email less frequently if the device is low on battery.
- A word processor could save changes automatically before the battery runs out in order to prevent data loss.
- A system checking if an interactive kiosk or TV installed in a showroom of an event is charging or if something wrong happened with the cables
- A module that checks the battery status of a drone in order to make it come back to the base before it runs out of power.

This article looks at a standardized way to manage energy consumption: The Battery Status API.

**The Battery Status API**

Open Web Apps can retrieve battery status information thanks to the [Battery Status API](https://developer.mozilla.org/en-US/docs/WebAPI/Battery_Status), a [W3C Recommendation](http://www.w3.org/TR/battery-status/) supported by Firefox since version 16. The API is also supported by Firefox OS, and recently by Chrome, Opera, and the Android browser, so now it can be used in production across many major platforms.

Also, the W3C Recommendation has recently been improved, introducing [Promise Objects](https://developer.mozilla.org/en/docs/Web/JavaScript/Reference/Global_Objects/Promise), and the ability to handle multiple batteries installed on the same device.

At the time of writing, [this W3C update](http://www.w3.org/TR/2014/CR-battery-status-20141209/) has not yet been implemented by Firefox: please check the following bugs for implementation updates or in case you want to contribute to Gecko development:

- [
[1050749](https://bugzilla.mozilla.org/show_bug.cgi?id=1050749)] Expose BatteryManager via getBattery() returning a Promise instead of a synchronous accessor (navigator.battery). The[navigator.getBattery()](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/getBattery)method is now available on[Firefox 43](https://developer.mozilla.org/en-US/Firefox/Releases/43). - [
[1050752](https://bugzilla.mozilla.org/show_bug.cgi?id=1050752)] BatteryManager: specify the behavior when a host device has more than one battery.

Below we will look at using the Battery Status API in an instant messaging app running on Firefox OS and all the browsers that currently support the API.

**Demo: Low Energy Messenger**

Low Energy Messenger is an instant messaging demo app that pays close attention to battery status. The app has been built with HTML + CSS + Javascript (no libraries) and uses static data. It does not include web services running on the Internet, but includes real integration with the Battery Status API and has a realistic look & feel.

You’ll find a [working demo of Low Energy Messenger](http://franciov.github.io/low-energy-messenger/), along with [the demo code on Github](https://github.com/franciov/low-energy-messenger/), and an >MDN article called [Retrieving Battery status information](https://developer.mozilla.org/en-US/Apps/Build/gather_and_modify_data/retrieving_battery_status_information) that explains the code step-by-step.

Low Energy Messenger has the following features:

- A battery status bar, containing battery status information.
- A chat section, containing all the messages received or sent.
- An action bar, containing a text field, a button to send a message, a button to take a photo, and a button to install the app on Firefox OS
- In order to preserve battery life when the power level is low, the app doesn’t allow users to take photos when the device is running out of battery.

The visual representation of the battery, in the app’s status bar, changes depending on the charge level. For example:

![13% Discharging: 0:23 remaining](https://mdn.mozillademos.org/files/6713/battery-low.png)


![40% Discharging: 1:19 remaining](https://mdn.mozillademos.org/files/6715/battery-medium.png)


![92% Charging: 0:16 until full](https://mdn.mozillademos.org/files/6711/battery-high.png)


Low Energy Messenger includes a module called [EnergyManager.js](https://github.com/franciov/low-energy-messenger/blob/master/scripts/utils/energy-manager.js) that uses the Battery Status API to get the information displayed above and perform checks.

The battery object, of type [BatteryManager](https://developer.mozilla.org/en-US/docs/Web/API/BatteryManager), is provided by the [ navigator.getBattery](https://developer.mozilla.org/en-US/docs/Web/API/navigator.getBattery) method, using Promises, or by the deprecated [ navigator.battery](https://developer.mozilla.org/en-US/docs/Web/API/navigator.battery) property, part of a previous W3C specification and currently used by Firefox and Firefox OS. As mentioned above, [follow this bug](https://bugzilla.mozilla.org/show_bug.cgi?id=1050749) for implementation updates or if you want to contribute to Gecko development.

The *EnergyManager.js* module eliminates this difference in API implementation in the following way:

```
/* EnergyManager.js */
init: function(callback) {
var _self = this;
```


```
/* Initialize the battery object */
if (navigator.getBattery) {
navigator.getBattery().then(function(battery) {
_self.battery = battery;
callback();
});
} else if (navigator.battery || navigator.mozBattery) { // deprecated battery objects
_self.battery = navigator.battery || navigator.mozBattery;
callback();
}
}
```


The *navigator.getBattery* method returns a battery [promise](https://developer.mozilla.org/en/docs/Web/JavaScript/Reference/Global_Objects/Promise), which is resolved in a BatteryManager object providing events you can handle to monitor the battery status. The deprecated *navigator.battery* attribute returns the *BatteryManager* object directly; the implementation above checks for vendor prefixes as well, for even older, experimental, API implementations carried on by Mozilla in earlier stages of the specification.

Logging into the [Web Console](https://developer.mozilla.org/en/docs/Tools/Web_Console) of a browser is a useful way to understand how the Battery Status API actually works:

`/* EnergyManager.js */`


```
log: function(event) {
if (event) {
console.warn(event);
}
```


```
console.log('battery.level: ' + this.battery.level);
console.log('battery.charging: ' + this.battery.charging);
console.log('battery.chargingTime: ' + this.battery.chargingTime);
console.log('battery.dischargingTime: ' + this.battery.dischargingTime);
}
```


Here is how the logs appear on the Web Console:

![Web Console](https://mdn.mozillademos.org/files/6709/log.png)


Every time an event (*dischargingtimechange*, *levelchange*, etc.) gets fired, the *BatteryManager* object provides updated values that can be used by the application for any purpose.

**Conclusions**

The Battery Status API is a standardized way to access the device hardware and is ready to be used in production, even if at the time of writing some compatibility checks still have to be performed on Firefox. Also, the W3C specification is generic enough to be used in different contexts, thus the API covers a good number of real-world use cases.

## About
[
Francesco Iovine ](http://www.francesco.iovine.name/)

Front-End Software Engineer based in London, passionate about pushing technology forward, with expertise in designing and developing web applications for mobile devices, TVs, interactive kiosks and anywhere the web can reach, using sensors and web APIs. Interested in web standards, contributor to the Open Web as tech writer (@MozDevNet), speaker (http://lanyrd.com/profile/franciov/past/speaking/) and event organiser (@componenthub).