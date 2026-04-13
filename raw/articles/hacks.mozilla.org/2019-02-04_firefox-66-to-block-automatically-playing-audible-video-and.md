---
title: Firefox 66 to block automatically playing audible video and audio – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2019/02/firefox-66-to-block-automatically-playing-audible-video-and-audio/
author: Chris Pearce
published: '2019-02-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Isn’t it annoying when you click on a link or open a new browser tab and audible video or audio starts playing automatically?

We know that unsolicited volume can be a great source of distraction and frustration for users of the web. So we are making changes to how Firefox handles playing media with sound. We want to make sure web developers are aware of this new *autoplay blocking* feature in Firefox.

Starting with the release of Firefox 66 for desktop and Firefox for Android, Firefox will block audible audio and video by default. We only allow a site to play audio or video aloud via the `HTMLMediaElement`

API once a web page has had user interaction to initiate the audio, such as the user clicking on a “play” button.

Any playback that happens before the user has interacted with a page via a mouse click, printable key press, or touch event, is deemed to be *autoplay* and will be blocked if it is potentially audible.

Muted autoplay is still allowed. So script can set the “muted” attribute on `HTMLMediaElement`

to true, and autoplay will work.

We expect to roll out audible autoplay blocking enabled by default, in Firefox 66, scheduled for [general release](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox#Firefox_channels) on 19 March 2019. In Firefox for Android, this will replace the existing block autoplay implementation with the same behavior we’ll be using in Firefox on desktop.

There are some sites on which users want audible autoplay audio and video to be allowed. When Firefox for Desktop blocks autoplay audio or video, an icon appears in the URL bar. Users can click on the icon to access the site information panel, where they can change the “Autoplay sound” permission for that site from the default setting of “Block” to “Allow”. Firefox will then allow that site to autoplay audibly. This allows users to easily curate their own whitelist of sites that they trust to autoplay audibly.

![](../../assets/97033a9118b5b0f0.png)


![](../../assets/97033a9118b5b0f0.png)

Firefox expresses a blocked `play()`

call to JavaScript by rejecting the promise returned by `HTMLMediaElement.play()`

with a `NotAllowedError`

. All major browsers which block autoplay express a blocked play via this mechanism. In general, the advice for web authors when calling `HTMLMediaElement.play()`

, is to *not assume* that calls to `play()`

will always succeed, and to always handle the promise returned by `play()`

being rejected.

If you want to avoid having your audible playback blocked, you should only play media inside a click or [keyboard event](https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent) handler, or on mobile in a [touchend event](https://developer.mozilla.org/en-US/docs/Web/Events/touchend). Another strategy to consider for video is to autoplay muted, and present an “unmute” button to your users. Note that muted autoplay is also currently allowed by default in all major browsers which block autoplay media.

We are also allowing sites to autoplay audibly if the user has previously granted them camera/microphone permission, so that sites which have explicit user permission to run WebRTC should continue to work as they do today.

At this time, we’re also working on blocking autoplay for [Web Audio](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Using_Web_Audio_API) content, but have not yet finalized our implementation. We expect to ship with autoplay Web Audio content blocking enabled by default sometime in 2019. We’ll let you know!

## 34 comments

SamFebruary 4th, 2019 at 10:50Ravan AsterisFebruary 4th, 2019 at 11:12jasperFebruary 4th, 2019 at 12:17bahadir balbanFebruary 4th, 2019 at 14:04Chris PearceFebruary 6th, 2019 at 13:11Tony DFebruary 4th, 2019 at 16:32Chris PearceFebruary 6th, 2019 at 13:09Geoff HartFebruary 6th, 2019 at 16:05Chris PearceFebruary 12th, 2019 at 15:50EloiseFebruary 5th, 2019 at 03:16Chris PearceFebruary 12th, 2019 at 15:52NoNameFebruary 5th, 2019 at 08:29Chris PearceFebruary 6th, 2019 at 11:14Win LoganFebruary 5th, 2019 at 15:05Painful InsightFebruary 5th, 2019 at 19:02Chris PearceFebruary 6th, 2019 at 11:10Andrew InggsFebruary 6th, 2019 at 11:10Chris PearceFebruary 6th, 2019 at 13:16Norbert SüleMarch 3rd, 2019 at 06:43Chris PearceMarch 6th, 2019 at 13:31Lucs LucsFebruary 7th, 2019 at 06:44Dan HyattFebruary 7th, 2019 at 08:12Chris PearceFebruary 12th, 2019 at 15:59RowFebruary 7th, 2019 at 18:17Paul PolsonFebruary 8th, 2019 at 06:45J RedheadFebruary 10th, 2019 at 14:11Chris PearceFebruary 10th, 2019 at 17:00Adam ChaceFebruary 12th, 2019 at 10:09Chris PearceFebruary 12th, 2019 at 15:42BanananaFebruary 28th, 2019 at 08:50Chris PearceFebruary 28th, 2019 at 12:17BanananaFebruary 28th, 2019 at 22:37EricMarch 6th, 2019 at 06:30Chris PearceMarch 6th, 2019 at 13:30