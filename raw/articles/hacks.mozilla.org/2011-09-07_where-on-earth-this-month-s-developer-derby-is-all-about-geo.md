---
title: Where on earth? This month's Developer Derby is all about geolocation. – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/09/where-on-earth-this-months-developer-derby-is-all-about-geolocation/
author: Chris Heilmann
published: '2011-09-07'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Another month, another [Developer Derby](https://developer.mozilla.org/en-US/demos/devderby). This month we want you to play with something that is [not part of the HTML5 stack](http://isgeolocationpartofhtml5.com/) and we feel it doesn’t get the love it deserves from developers: the geolocation API. Firefox has supported this API for a long time and you can do some pretty cool things with it.

So, what is the Geolocation API? In essence it allows you to detect where the user of your product is at the moment. The location data is found by different means: GPS location, mobile phone masts or wireless hub location. If you turn off wireless on your laptop and you have no 3G connectivity, the API will not be able to get any data.

Using geolocation is incredibly simple. You ask the browser to tell you what the current location is with a method on the `navigator.geolocation`

object:

```
navigator.geolocation.getCurrentPosition(
success,
failure,
{ parameters }
);
```

Where *success* is the function that is called when the browser found a location, *failure* is the function called when there was an error and properties is an object that can contain a few parameters. The parameters are the Boolean `enableHighAccuracy`

, the `maximumAge`

of the location before the browser should ask for a new one and the `timeout`

in milliseconds after which the browser should stop trying to find a location.

Each function (success and failure) get a parameter with which to do your coding magic. The success function will get a location object when everything went well. This location object has the following properties: A timestamp telling you when the reading was done and a coordinates object with the following properties: `accuracy`

, `altitude`

, `altitudeAccuracy`

, `heading`

, `latitude`

, `longitude`

and `speed`

.

Some of these are dependent on having more than one reading as for example heading and speed are calculated from the distance in latitude and longitude from reading to reading.

On Firefox you have an extra object called address which is the result of reverse geocoding the latitude and longitude. Reverse geocoding is normally done with an API but in the case of Firefox we have it baked in. When I currently do a call to `getCurrentPosition`

I [get the following result on Firefox](http://isithackday.com/hacks/geo/check/):

Timestamp: 1315378919289 Coordinates: Accuracy: 18000 Altitude: 0 AltitudeAccuracy: 0 Heading: NaN Latitude: 50.06465 Longitude: 19.94498 Speed: NaN Address: City: Kraków Country: Poland CountryCode: PL County: Kraków County Postal Code: null Premises: null Street: Lubicz Street Number: 1

You can [Run this test for yourself](http://isithackday.com/hacks/geo/check/) and see the code [here on JSFiddle](http://jsfiddle.net/codepo8/Un8na/):

The failure function gets an error object with a `code`

property. This property can have three values: 1 is a permission denied error, 2 is a position unavailable error and 3 is a timeout.

In addition to the `getCurrentPosition`

method you also have a `watchPosition`

method which keeps firing when a new location was found. The parameters are the same and when you keep reading (for example on a mobile device) then you will get values for the `heading`

and the `speed`

. You can stop watching the position change using the `clearWatch`

method.

Using `watchPosition`

is very cool when you are on the go. Check the [Geolocation demo page](http://isithackday.com/hacks/geo/check/) and turn the watch position on and off with the button on the bottom.

In essence, this is what the map app on your mobile phone does.

## What can you do with this?

Well, what you get is a latitude and longitude of your end user. This can be used with all kind of geo platforms like for example [GeoNames](http://www.geonames.org/) to find places of interest around you.

You could also allow people to set markers for their friends on a map, collaboratively paint with them, find photos, tweets or foursquare checkins around you – a lot is possible when you come from lat/lon.

## Resources

[Geo API Specification of the W3C](http://dev.w3.org/geo/api/spec-source.html)[Geo API on MDN]- Another
[simple Geo Demo](http://html5demos.com/geo)by Remy Sharp [Geolocation in Firefox](http://www.mozilla.org/en-US/firefox/geolocation/)[Using geolocation on MDN](https://developer.mozilla.org/en/Using_geolocation)

We will also soon run a webinar on geolocation, stay tuned!

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!