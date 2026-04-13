---
title: HTML5 video 'buffered' property available in Firefox 4 – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2010/08/html5-video-buffered-property-available-in-firefox-4/
author: Chris Pearce
published: '2010-08-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This is a repost from Chris Pearce’s blog.*

Recently I landed support for the [HTML5 video ‘](http://www.whatwg.org/specs/web-apps/current-work/multipage/video.html#dom-media-buffered)[buffered’ ](http://www.whatwg.org/specs/web-apps/current-work/multipage/video.html#dom-media-buffered)[property](http://www.whatwg.org/specs/web-apps/current-work/multipage/video.html#dom-media-buffered) in Firefox. This is cool because we can now accurately determine which time-segments of a video we can play and seek into without needing to pause playback to download more data. Previously you could only get the byte position the download had reached, which often doesn’t map to the time ranges which are playable very well, especially in a variable bit rate video. This also can’t tell you if there are chunks which we skipped downloading before the downloaded byte position. Once the video controls UI is updated, users will be able to know exactly which segments of their video are downloaded and playable and can be seeked into without pausing playback to download more data.

To see this in action, download a current [Firefox nightly build ](http://ftp.mozilla.org/pub/mozilla.org/firefox/nightly/latest-mozilla-central/), and point your browser at my [video ‘buffered’ property demo](http://people.mozilla.com/%7Ecpearce/buffered-demo.html). You’ll see something like the screenshot below, including an extra progress bar (implemented using canvas) showing the time ranges which are buffered.

I’ve implemented the ‘buffered’ property for the Ogg and WAV backends. [Support for the ‘buffered’ property for WebM](https://bugzilla.mozilla.org/show_bug.cgi?id=570904) is being worked on by [Matthew Gregan](http://blog.mjg.im/), and is well underway. At the moment we return empty ranges for the ‘buffered’ property on video elements playing WebM and raw video.

My checkin just missed the cutoff for Firefox 4 Beta 3, so the first beta release that the video ‘buffered’ property will appear in is Firefox 4 Beta 4.

## 19 comments

Richard StallmanAugust 20th, 2010 at 01:07ClerothSeptember 5th, 2010 at 13:31PeterOctober 24th, 2010 at 07:25GuidoOctober 23rd, 2010 at 16:23ChrisNovember 8th, 2010 at 22:27MardegAugust 22nd, 2010 at 14:12NAugust 23rd, 2010 at 11:25FelipeAugust 24th, 2010 at 12:26TsiolkovskyOctober 24th, 2010 at 07:18PeterOctober 24th, 2010 at 07:29DavidOctober 24th, 2010 at 11:05MikeOctober 24th, 2010 at 12:41Karthikeyan A KOctober 24th, 2010 at 18:53MichaelDecember 28th, 2010 at 11:21Brent JApril 6th, 2011 at 11:33ClerothApril 7th, 2011 at 01:19cpearceJune 16th, 2011 at 15:02IanFebruary 11th, 2012 at 18:39hajirMarch 26th, 2012 at 00:32