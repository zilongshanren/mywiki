---
title: Using the Vibration API – Part of WebAPI – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2012/01/using-the-vibrator-api-part-of-webapi/
author: Robert Nyman
published: '2012-01-26'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

As part of [Mozillas WebAPI](https://wiki.mozilla.org/WebAPI) effort, we have been working with bringing a Vibration API to all devices that support it.


The idea with the Vibration API is to be able to give the user a notification, in a game or other use case, by telling the device to vibrate. It accesses the native vibrator and tells it how long it should vibrate.

## Examples

The way to do this is quite simple – in this example the parameter is how long it should vibrate, i.e. the number of milliseconds:

`navigator.mozVibrate(1000);`


Another way of controlling vibration is giving a vibration pattern, switching between vibrating and being still. The odd parameters in the list is vibration time, the even ones are pauses:

`navigator.mozVibrate([200, 100, 200, 100]);`


And if you want to stop the vibration, you can simply call the `mozVibrate`

method with an argument of 0 or an empty pattern, like this:

` navigator.mozVibrate(0);`


navigator.mozVibrate([]);

## Try it out!

If you want to try this out right now, you can do so in [Firefox Aurora](http://www.mozilla.org/firefox/channel/), which is planned to become Firefox 11. Currently, it naturally only works on devices that support vibration, which means Firefox on (most) Android phones.

Note: a possbile caveat could be if you have haptic feedback turned on on your Android device, which then might cancel out the vibration.

## Demo

I put together a little demo where you can see the code needed and test it in place. Please play around with this and let us know what you think!

**Edit:** Our temporary implementation name was Vibrator API, but since it gave the wrong impression, we now call it Vibration API – which is also more in line with the [W3C Vibration API draft](http://www.w3.org/TR/vibration/).

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 34 comments

MustafaJanuary 26th, 2012 at 07:32Robert NymanJanuary 26th, 2012 at 12:57DaveCJanuary 26th, 2012 at 07:40Robert NymanJanuary 26th, 2012 at 12:59whyJanuary 26th, 2012 at 07:59Robert NymanJanuary 26th, 2012 at 08:48MeJanuary 26th, 2012 at 08:19Robert NymanJanuary 26th, 2012 at 08:49Justin LebarJanuary 26th, 2012 at 08:34Robert NymanJanuary 26th, 2012 at 08:50Justin LebarJanuary 26th, 2012 at 08:52Robert NymanJanuary 26th, 2012 at 08:56Justin LebarJanuary 26th, 2012 at 09:06Robert NymanJanuary 26th, 2012 at 09:09mike nowakJanuary 26th, 2012 at 09:21Rob HawkesJanuary 26th, 2012 at 10:03PeteJanuary 26th, 2012 at 09:59Robert NymanJanuary 26th, 2012 at 10:01MaxJanuary 27th, 2012 at 01:41Robert NymanJanuary 27th, 2012 at 02:49Justin LebarJanuary 27th, 2012 at 07:39Jonas SickingJanuary 30th, 2012 at 01:31Adrian von GegerfeltJanuary 27th, 2012 at 05:48Justin LebarJanuary 27th, 2012 at 07:38MaxJanuary 27th, 2012 at 07:56Robert NymanJanuary 30th, 2012 at 23:54MaxJanuary 30th, 2012 at 02:43Robert NymanJanuary 30th, 2012 at 23:53Pavel PavlovFebruary 1st, 2012 at 06:27Robert NymanFebruary 1st, 2012 at 06:34Ollie ParsleyFebruary 22nd, 2012 at 14:54Robert NymanFebruary 23rd, 2012 at 02:18Alejandro LechugaJanuary 24th, 2013 at 18:29Robert Nyman [Editor]January 25th, 2013 at 01:55