---
title: Ambient Light Events and JavaScript detection – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/04/ambient-light-events-and-javascript-detection/
author: Robert Nyman
published: '2013-04-08'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

I think that one of the most interesting things with [all WebAPIs we’re working on](https://hacks.mozilla.org/2013/02/using-webapis-to-make-the-web-layer-more-capable/), is to interact directly with the hardware through JavaScript, but also, as an extension to that, with the environment around us. Enter [Ambient Light Events](http://www.w3.org/TR/ambient-light/).

The idea with an API for ambient light is to be able to detect the light level around the device – especially since there’s a vast difference between being outside in sunlight and sitting in a dim living room – and adapt the user experience based on that.

One use case could be to change the CSS file/values for the page, offering a nicer reading experience under low light conditions, reducing the strong white of a background, and then something with more/better contrast for bright ambient light. Another could be to play certain music depending on the light available.

## Accessing device light

Working with ambient light is quite simple. What you need to do is apply a listener for a `devicelight`

event, and then read out the brightness value.

It comes returned in the lux unity. The lux value ranges between low and high values, but a good point of reference is that dim values are under 30 lux, whereas really bright ones are 10,000 and over.

```
window.addEventListener("devicelight", function (event) {
// Read out the lux value
var lux = event.value;
console.log(lux);
});
```

## Web browser support

Ambient Light Events are currently supported in Firefox on Android, meaning both mobile phones and tablets, and it’s also supported in Firefox OS. On Android devices (the ones I’ve tested), the sensor is located just right to the camera facing the user.

It is also [a W3C Working Draft](http://www.w3.org/TR/ambient-light/), following the type of other similar events, such as [devicemotion](http://dev.w3.org/geo/api/spec-source-orientation.html#devicemotion), so we hope to see more implementations of this soon!

## Demo

Dmitry Dragilev and Tim Wright recently wrote a [blog post about the Ambient Light API](http://www.freshtilledsoil.com/device-api-ambient-light-demo-on-nexus-7/), with this nice demo video:

You can also access the [demo example](http://www.freshtilledsoil.com/the-future-of-web/ambient-light/) directly, and if you test in low light conditions, you’ll get a little music. Remember to try it out on a supported device/web browser.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 13 comments

AlexApril 8th, 2013 at 07:51Robert Nyman [Editor]April 8th, 2013 at 10:25maxw3stApril 8th, 2013 at 10:19Robert Nyman [Editor]April 8th, 2013 at 10:24boblemarinApril 8th, 2013 at 10:24Robert Nyman [Editor]April 8th, 2013 at 10:37Carlos MartinsApril 8th, 2013 at 11:49thinsoldierApril 8th, 2013 at 10:36Robert Nyman [Editor]April 8th, 2013 at 10:39Paul LynchApril 8th, 2013 at 13:14Robert Nyman [Editor]April 8th, 2013 at 23:54LandpaddleApril 9th, 2013 at 03:09Robert Nyman [Editor]April 9th, 2013 at 06:52