---
title: Who moved my geolocation? – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/10/who-moved-my-geolocation/
author: Frédéric Harper
published: '2013-10-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

One of the questions we often get when we are talking about Firefox OS is: “What about the GPS on some devices”? You may have noticed that on some devices, the GPS position is not quite accurate or can take a long time to report even when you are outside. Let me start by explaining how it works first. After, we’ll see what the issue is right now, and how we can, as developers, continue to work our magic, and create awesome applications using geolocation.

## How the devices give you geolocation

Most smartphones use two techniques to help you get the longitude and latitude of the phone: the GPS itself, but also something called A-GPS ([Assisted GPS](http://en.wikipedia.org/wiki/Assisted_GPS)) servers. When you are outside, the GPS connects with satellite signals, and gets you the coordinates of the device: latitude and longitude. It works well as long as the GPS can connect with satellites, but it can take some time to achieve this, or to give you something more accurate.

To help the device achieve its goal faster, often you’ll get a location from an A-GPS server: this is why most of the time, you’ll first get a location within maybe 50 meters, and if you wait a little longer, you’ll get something more accurate. It’s also why, when you are using dedicated GPS devices (like the one you use for hiking or geocaching), it takes longer: they just use the GPS, and need to connect to more satellite, no assisted GPS connection.

## What about Firefox OS?

Mozilla doesn’t provide any Firefox OS images; we provide source code to chip manufacturer, and OEMs like Geeksphone. These parties customize various parts and create binary images for devices. The final Firefox OS image is mostly representative of what we have in the public source repositories, but with some modifications. This is an important distinction because the configuration of some parts (like Linux config, device setup, etc.) is not in Mozilla’s hands.

With that in mind, some devices have configuration problems for A-GPS. We are actively working with OEMs to solve that issue, but it’s not something we can fix by ourselves. Once it is fixed for specific devices with A-GPS problems, we’ll let you know about the procedure to fix your device on this blog.

## But I need geolocation for my application

There are many ways to develop applications needing geolocation information even with this little A-GPS issue. First, you can use the simulator to test your application. There is a nice little option right in the simulator to let you emulate any coordinates you need.

![Screenshot of the Firefox OS Simulator](../../assets/98ae7d452ac40709.png)


Of course, while the simulator is perfect for the development part and the first series of tests, you’ll need to test your new masterpiece on a real device. If you are using Linux or OS X (I’m working on a solution for Windows users), our friend, Doug Turner, created a [mock location provider](https://github.com/dougt/b2g-mock-location-provider) which you can install on your (rooted) phone to do some tests. It can hardcode the latitude and longitude that [Firefox OS itself](https://github.com/mozilla-b2g/) returns to your phone. You can change those coordinates by editing `MockGeolocationProvider.js`

file in the `components`

folder of the project. Of course, you could hardcode this yourself in your code, but you won’t be able to see how well your code handles what the device returns to you.

Last but not least, you can also use free services like [freegeoip.net](http://freegeoip.net/). It’s a database that you can use to detect geolocation from IP addresses. It’s not perfect, but it’s a good start to give a more accurate location to the user and a good fallback solution for any applications. You never know when there will be a problem with A-GPS or GPS.

## Best practices for apps using GPS

There are a couple of things you need to keep in mind when you are building an application that needs geolocation. First, you need to think about the accuracy of the result you’ll receive. What you need to know is that using `getCurrentPosition`

tries to return a result as fast as possible: sometimes it means using wifi or the IP address to get the result. When using the GPS device, it may take minutes before it connects to satellites, so in that situation, you have two choices:

- You can get the accuracy of the result, in meters, by getting accuracy for the coordinates returned by
`getCurrentPosition`

(see code below); - Alternatively, you can define a
`HighAccuracy`

option when you call`getCurrentPosition`

(see code below).

```
var options = {
enableHighAccuracy: true,
timeout: 5000,
maximumAge: 0
};
function success(pos) {
var crd = pos.coords;
console.log('Your current position is:');
console.log('Latitude : ' + crd.latitude);
console.log('Longitude: ' + crd.longitude);
console.log('More or less ' + crd.accuracy + ' meters.');
};
function error(err) {
console.warn('ERROR(' + err.code + '): ' + err.message);
};
navigator.geolocation.getCurrentPosition(success, error, options);
```

You also need to think about the fact that the user may move, so you need to re-estimate the user’s coordinates every so often, depending on what you are trying to achieve. You can do this either manually or by using the `watchPosition`

method of the geolocation API in Firefox OS.

```
var watchID = navigator.geolocation.watchPosition(function(position) {
do_something(position.coords.latitude, position.coords.longitude);
});
```

In that situation, if the position changes, either because the devices moves or because more accurate geolocation information arrives, your function will be called, and you’ll be able to handle the new information.

If you want more information about how to use geolocation in your application, you can always check the Mozilla Developer Network documentation on [using geolocation](https://developer.mozilla.org/en-US/docs/WebAPI/Using_geolocation). If you have any questions about using geolocation in your Firefox OS application, please leave a question in the comments’ section.

## About
[
Frédéric Harper ](http://outofcomfortzone.net)

As a Senior Technical Evangelist at Mozilla, Fred shares his passion about the Open Web, and help developers be successful with Firefox OS. Experienced speaker, t-shirts wearer, long-time blogger, passionate hugger, and HTML5 lover, Fred lives in Montréal, and speak Frenglish. Always conscious about the importance of unicorns, and gnomes, you can read about these topics, and other thoughts at outofcomfortzone.net.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 5 comments

nadrimajstorOctober 3rd, 2013 at 17:01nadrimajstorOctober 3rd, 2013 at 17:05Frédéric HarperOctober 9th, 2013 at 06:35servis laptopovaOctober 4th, 2013 at 15:16Frédéric HarperOctober 9th, 2013 at 06:37