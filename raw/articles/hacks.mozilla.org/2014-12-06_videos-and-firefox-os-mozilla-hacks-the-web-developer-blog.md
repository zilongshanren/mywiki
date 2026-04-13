---
title: Videos and Firefox OS – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/12/videos-and-firefox-os/
author: Mark Wheeler
published: '2014-12-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## Before HTML5

Before HTML5, displaying video on the Web required [browser plugins](https://developer.apple.com/library/mac/documentation/quicktime/Conceptual/QTScripting_HTML/QTScripting_HTML_Document/ScriptingHTML.html) and [Flash](http://www.adobe.com/products/flash.html).

Luckily, Firefox OS supports HTML5 video so we don’t need to support these older formats.

## Video support on the Web

Even though modern browsers support HTML5, the video formats they support vary:

In summary, to support the most browsers with the fewest formats you need the **MP4** and **WebM** video formats (Firefox prefers WebM).

## Multiple sizes

Now that you have seen what formats you can use, you need to decide on video resolutions, as desktop users on high speed wifi will expect better quality videos than mobile users on 3G.

At [Rormix](http://rormix.com) we decided on 720p for desktop, 360p for mobile connections, and 180p specially for Firefox OS to reduce the cost in countries with high data charges.

There are no hard and fast rules — it depends on who your market audience is.

### Streaming?

The best streaming solution would be to automatically serve the user different videos sizes depending on their connection status ([adaptive streaming](http://en.wikipedia.org/wiki/Adaptive_bitrate_streaming)) but support for this technology [is poor](http://www.jwplayer.com/html5/#html5_adaptivestreaming).

[HTTP live streaming](http://en.wikipedia.org/wiki/HTTP_Live_Streaming) works well on Apple devices, but has [poor support on Android](http://www.jwplayer.com/blog/the-pain-of-live-streaming-on-android/).

At the time of writing, the most promising technology is [MPEG DASH](http://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP), which is an international standard.

In summary, we are going to have to wait before we get an adaptive streaming technology that is widely accepted (Firefox does not support HLS or MPEG DASH).

### DIY Adaptive streaming

In the absence of adaptive streaming we need to try to work out the best video quality to load at the outset. The following is a quick guide to help you decide:

### Wifi or 3G

Using a [certified](https://developer.mozilla.org/en-US/Firefox_OS/Security/Application_security) Firefox OS app you can check to see if the user is on wifi or not.

```
var lock = navigator.mozSettings.createLock();
var setting = lock.get('wifi.enabled');
setting.onsuccess = function () {
console.log('wifi.enabled: ' + setting.result);
}
setting.onerror = function () {
console.warn('An error occured: ' + setting.error);
}
```

There is some more information at the [W3C Device API](http://www.w3.org/2009/dap/).

### Detecting screen size

There is no point sending a 720p video to a user with a screen smaller than 720p. There are many ways to get the different bounds of a user’s screen; [innerWidth](https://developer.mozilla.org/en-US/docs/Web/API/Window.innerWidth) and [width](https://developer.mozilla.org/en-US/docs/Web/API/Screen.width) allow you to get a good idea:

```
function getVidSize()
{
//Get the width of the phone (rotation independent)
var min = Math.min($(window).innerHeight(),$(window).innerWidth());
//Return a video size we have
if(min < 320) return '180';
else if(min < 550) return '360';
else return '720';
}
```

### Determining internet speed

It is difficult to get an accurate read of a user's internet speed using web technologies — usually they involve loading a large image onto the user's device and timing it. This has the disadvantage of having to send more data to the user. Some services such as: [http://speedof.me/api.html](http://speedof.me/api.html) exist, but still require data downloads to the user's device. ([Stackoverflow](http://stackoverflow.com/questions/5529718/how-to-detect-internet-speed-in-javascript) has some more options.)

You can be slightly more clever by using HTML5, and checking the time it takes between the user starting the video and a set amount of the video loading. This way we do not need to load any extra data on the user's device. A quick [VideoJS](http://www.videojs.com) example follows:

```
var global_speedcount = 0;
var global_video = null;
global_video = videojs("video", {}, function(){
//Set up video sources
});
global_video.on('play',function(){
//User has clicked play
global_speedcount = new Date().getTime();
});
function timer()
{
var diff = new Date().getTime() - global_speedcount;
//Remove this handler as it is run multiple times per second!
global_video.off('timeupdate',timer);
}
global_video.on('timeupdate',timer);
```

This code starts timing when the user clicks play, and when the browser starts to play the video it sends timing information to `timeupdate`

. You can also use this function to detect if lots of buffering is happening.

## Detect high resolution devices

One final thing to determine is whether or not a user has a high pixel density screen. In this case even if they have a small screen it can still have a large number of pixels (and therefore require a higher resolution video).

[Modernizr](https://github.com/benlister/utilities/tree/master/Modernizr%20Retina%20:%20HiDPI%20test) has a plugin for detecting hi-res screens.

```
if (Modernizr.highresdisplay)
{
alert('Your device has a high resolution screen');
}
```

## WebP Thumbnails

Not to get embroiled in an argument, but at [Rormix](http://rormix.com) we have seen an average decrease of 30% in file size (WebP vs JPEG) with no loss of quality (in some cases up to 50% less). And in countries with expensive data plans, the less data the better.

We encode all of our thumbnails in multiple resolutions of WebP and send them to every device that supports them to reduce the amount of data being sent to the user.

## Mobile considerations

If you are playing HTML5 videos on mobile devices, their behavior differs. On iOS it automatically goes to full screen on iPhones/iPods, but not on tablets.

Some libraries such as VideoJS have [removed the controls from mobile devices](https://github.com/videojs/video.js/blob/32519181c8ffacbc2b322e42958a2db4a5fb4d3c/src/js/player.js#L27-36) until their stability increases.

## Useful libraries

There are a few useful HTML5 video libraries:

## Mozilla links

Mozilla has some great articles on web video:

[Live streaming web audio and video](https://developer.mozilla.org/en-US/Apps/Build/Audio_and_video_delivery/Live_streaming_web_audio_and_video)[Setting up adaptive streaming media sources](https://developer.mozilla.org/en-US/Apps/Build/Audio_and_video_delivery/Setting_up_adaptive_streaming_media_sources)[Audio and video delivery](https://developer.mozilla.org/en-US/Apps/Build/Audio_and_video_delivery)[Cross browser video player](https://developer.mozilla.org/en-US/Apps/Build/Audio_and_video_delivery/cross_browser_video_player)

## Other useful Links

## About
[
Mark Wheeler ](http://pixelcode.co.uk)

CTO at Rormix - Music worth watching

## 6 comments

Daniel DavisDecember 6th, 2014 at 00:38Mark WheelerDecember 8th, 2014 at 20:33Daniel DavisDecember 9th, 2014 at 07:11Benergy SamDecember 9th, 2014 at 10:47ShmerlJanuary 1st, 2015 at 19:29ShmerlJanuary 1st, 2015 at 19:31