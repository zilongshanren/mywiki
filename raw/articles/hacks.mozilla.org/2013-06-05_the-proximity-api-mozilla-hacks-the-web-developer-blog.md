---
title: The Proximity API – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/06/the-proximity-api/
author: Robert Nyman
published: '2013-06-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Something that’s very nice with bringing the web to the mobile platform with Firefox OS and [WebAPIs](https://hacks.mozilla.org/2013/02/using-webapis-to-make-the-web-layer-more-capable/) is the ability to connect more into the physical world. One part there is the Proximity API, which is also a [W3C Working Draft – Proximity Events](http://www.w3.org/TR/proximity/).

## What it is

The API is about detecting how close the device is to any other physical object, by accessing the proximity sensor. There are two ways of working with proximity

- Device proximity
- User proximity

From the spec:

The `DeviceProximityEvent`

interface provides web developers information about the distance between the hosting device and a nearby object.

The `UserProximityEvent`

interface provides web developers a user-agent- and platform-specific approximation that the hosting device has sensed a nearby object.

## Using it

Working with proximity is as easy as adding a couple of event handlers, depending on what you want to do. The `deviceproximity`

event works with the metric system, and you will get back the distance in centimeters (these examples take for granted that you have an existing proximityDisplay element to present the values in). You are also able to check the minimum and maximum distance the sensor in your device supports.

![](../../assets/ba015378524cc697.png)


```
window.ondeviceproximity = function (event) {
// Check proximity, in centimeters
var prox = "
```**Proximity: **" + event.value + " cm

";
prox += "**Min value supported: **" + event.min + " cm

";
prox += "**Max value supported: **" + event.max + " cm";
proximityDisplay.innerHTML = prox;
};

It should be noted that the values sensors currently can return a quite small value, ranging from 0 up to 5 or 10 centimeters. In general, I believe the use case has been to detect if the user is holding the device up to the ear or not, but my personal opinion is that this could provide to be even more exciting if it supported, say, up to a meter!

With `userproximity`

, the value you get back is a `near`

property on the `event`

object, which is a boolean returning whether the user is near to the sensor or not.

![](../../assets/c6bb3a9d7390bfa5.png)


```
window.onuserproximity = function (event) {
// Check user proximity
var userProx = "
```**User proximity - near: **" + event.near + "

";
userProximityDisplay.innerHTML = userProx;
};

I’ve also added device and proximity code and testing to the [Firefox OS Boilerplate App](https://github.com/robnyman/Firefox-OS-Boilerplate-App) so feel free to get the latest code there and play around with it.

## Web browser support

The Proximity API is currently supported in:

## Conclusion

Working with proximity is yet another example of crossing the gap between software and real physical context, and showing just how powerful the web can be. We hope to see you creating many interesting things based on it!

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 7 comments

be connectedJune 9th, 2013 at 04:28Robert Nyman [Editor]June 10th, 2013 at 01:40Mathew PorterJune 13th, 2013 at 09:57Robert Nyman [Editor]June 13th, 2013 at 13:34VergorioJune 20th, 2013 at 13:01Caspy7July 3rd, 2013 at 12:28Robert Nyman [Editor]July 3rd, 2013 at 14:11