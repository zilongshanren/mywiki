---
title: JSMad – a JavaScript MP3 decoder – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/06/jsmad-a-javascript-mp3-decoder/
author: Chris Heilmann
published: '2011-06-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

It always amazes me just how fast modern browsers and their JavaScript engines are. And how creative people get when trying to make things work inside a browser instead of relying on a plugin that our end users would have to install (and more importantly constantly keep up to date).

The latest thing that make me go “wow” is [jsmad](http://jsmad.org) ([source on GitHub](https://github.com/nddrylliog/jsmad)) by [Amos Wenger](http://twitter.com/#!/nddrylliog), [Jens Nockert](http://twitter.com/#!/jensnockert) and [Matthias Georgi](http://twitter.com/#!/mgeorgi). JSMad is an MP3 decoder in JavaScript!

“So what”, you say? Well, having JSMad means that now Firefox can play MP3 files without any Flash. It also means that you can listen to MP3 in the browser without the 64bit issues on Linux. With JSMad we can dive deep into the MP3 format and not only play the song but also get information about it. It allows us to build a lot of native dj-mixers, samplers and sequencers in the nearer future.

Right now JSMad works in Firefox 4+ and on Chrome 13.0+, if you enable the Web Audio API in ‘about:flags’.

I remember when MP3 came out and my computer back then was too slow to encode it without locking up in WinAmp. Back then a scene player also helped me out. Now we do the same inside a browser rather than desktop applications.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 25 comments

CAFxXJune 19th, 2011 at 06:22Amos WengerJune 19th, 2011 at 06:30BramJune 19th, 2011 at 07:26Amos WengerJune 19th, 2011 at 08:01MardegJune 19th, 2011 at 06:23xJune 19th, 2011 at 07:18Amos WengerJune 19th, 2011 at 08:07xJune 19th, 2011 at 08:58pdJune 19th, 2011 at 11:20aaJune 19th, 2011 at 13:36Dheeraj YadavJune 20th, 2011 at 05:09GuestJune 20th, 2011 at 06:32BodJune 20th, 2011 at 07:03JaredJune 20th, 2011 at 07:47KissakiJune 25th, 2011 at 10:32KissakiJune 25th, 2011 at 10:31SharonJune 29th, 2011 at 07:11Andres G. AragonesesAugust 14th, 2011 at 06:58Amos WengerAugust 15th, 2011 at 09:46Andres G. AragonesesAugust 16th, 2011 at 10:38danielSeptember 15th, 2011 at 07:59Amos WengerSeptember 16th, 2011 at 00:43trusktrDecember 8th, 2011 at 20:59PithikosMarch 21st, 2012 at 05:33onokOctober 5th, 2012 at 06:30