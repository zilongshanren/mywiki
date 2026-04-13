---
title: Progress update on WebRTC for Firefox on desktop – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2012/11/progress-update-on-webrtc-for-firefox-on-desktop/
author: Maire Reavy
published: '2012-11-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

WebRTC for desktop is now in [Firefox Nightly](http://nightly.mozilla.org/) and is also in [Firefox Aurora](http://www.mozilla.org/firefox/aurora/), though Nightly has the hottest up-to-date fixes.

We support `mozGetUserMedia`

, `mozRTCPeerConnection`

and `DataChannels`

. We have a basic UI for `mozGetUserMedia`

which we expect to be updating in the

coming weeks.

## Enabling WebRTC in Firefox

The code is behind a pref for now, pending more testing. To enable our WebRTC code in Firefox’s Nightly desktop build, browse to [about:config](about:config)

and change the `media.peerconnection.enabled`

preference to `true`

.

Here are the 3 relevant prefs to `getUserMedia()`

and `mozRTCPeerConnection()`

:

`media.navigator.enabled`

enables calls to`mozGetUserMedia()`

only`media.navigator.permission.disabled`

automatically gives permission to access the camera/microphone and bypasses the permission/selection dialog`media.peerconnection.enabled`

enables use of`mozRTCPeerConnection()`


*Note: media.peerconnection.enabled implies media.navigator.enabled has been set to true.*



## Demos & upcoming changes

There’s a lot you can do with these APIs, even today. For examples, check out our [test landing page on GitHub](http://mozilla.github.com/webrtc-landing). We’ll try and put up notices if you’re running an out-of-date browser — as well as news updates about important bug fixes and API changes there!

Upcoming changes include:

- Support for constraints (to getUserMedia and createOffer/Answer)
- Control of bandwidth, resolution, echo cancellation, etc.
- Statistics
- TURN support (to allow connections between devices behind symmetric NATs)
- Fixes for audio drift (progressive loss of A/V sync)
- Trickle ICE, rtcp-mux and BUNDLE support
- getUserMedia() UI updates
- And many bugfixes

To give you an idea of the power of these APIs, in a couple of days our team whipped up a [Social API integration demo](http://github.com/anantn/socialapi-demo) that allows you to video +

text chat with your friends, drag-and-drop files to each other, drop links, tabs, etc, all making simple use of the DataChannel API.

The DataChannel API is quite simple on the surface, and has an API very similar to [WebSockets](https://developer.mozilla.org/en-US/docs/WebSockets). A quick example:



```
/**
* Assume we've connected a PeerConnection with a friend - usually with audio
* and/or video. For the time being, always at least include a 'fake' audio
* stream - this will be fixed soon.
*
* connectDataConnection is a temporary function that will soon disappear.
* The two sides need to use inverted copies of the two numbers (eg. 5000, 5001
* on one side, 5001, 5000 on the other)
*/
pc.connectDataConnection(5001, 5000);
function handle_new(channel) {
channel.binaryType = "blob";
channel.onmessage = function(evt) {
if (evt.data instanceof Blob) {
console.log("I received a blob");
// assign data to an image, save in a file, etc
} else {
console.log("I got a message: " + evt.data);
}
};
channel.onopen = function() {
// We can now send, like WebSockets
channel.send("The channel is open!");
};
channel.onclose = function() {
console.log("pc1 onclose fired");
};
};
/* For when the other side creates a channel */
pc.onDataChannel = handle_new;
channel = pc.createDataChannel("My Datastream",{});
if (channel) {
handle_new(channel);
}
```

## Filing bugs & moving forward

Progress on WebRTC (and bug-fixing) is rapid, and we encourage you to try it out and submit bugs. (We have plenty! But we’re nailing them as fast as we can, so make sure you’re on nightly and update regularly.)

Bug reports are highly appreciated. Please file them on

[Bugzilla](https://bugzilla.mozilla.org/enter_bug.cgi?product=Core&component=WebRTC) under “Product:Core”, “Component:WebRTC”.

The team is both excited by all the progress, and exhausted. The work so far represents tons of hours of work from so many people on the Firefox team (too many people to name — especially because we don’t want to forget

someone — but you know who you are!). Thank you to everyone who helped us land this “747″ on the flight deck.

We’ll continue to blog regularly on our progress as we work to make this a great product feature for Firefox and the web.

## About
[
Anant Narayanan ](http://kix.in/)

[@anantn](http://twitter.com/anantn) is a hacker at [Mozilla Labs](http://mozillalabs.com/) who specializes in generalism. He has previously worked on [Weave](https://wiki.mozilla.org/Labs/Weave), [Jetpack](https://wiki.mozilla.org/Jetpack), [Account Manager](https://wiki.mozilla.org/Labs/Weave/Identity/Account_Manager), and [Rainbow](https://mozillalabs.com/en-US/rainbow/) among other projects. He is currently fiddling with [Open Web Apps](http://apps.mozillalabs.com/) and [Real-time communication for the Web](http://webrtc.org/).

## About
[
Robin Hawkes ](http://rawkes.com)

Robin thrives on solving problems through code. He's a Digital Tinkerer, Head of Developer Relations at Pusher, former Evangelist at Mozilla, book author, and a Brit.

## 40 comments

Pascal RettigNovember 5th, 2012 at 08:09Anant NarayananNovember 5th, 2012 at 08:22DrazickNovember 5th, 2012 at 09:00Robert NymanNovember 5th, 2012 at 09:18Felipe ReyesNovember 5th, 2012 at 09:25Robert NymanNovember 5th, 2012 at 09:48TomNovember 5th, 2012 at 12:43Robert NymanNovember 5th, 2012 at 15:41TomNovember 5th, 2012 at 16:52Sam DuttonNovember 7th, 2012 at 04:13Robert NymanNovember 7th, 2012 at 06:48MarkNovember 7th, 2012 at 22:45Robert NymanNovember 8th, 2012 at 01:39Maire ReavyNovember 8th, 2012 at 02:06Gonzalo GascaNovember 9th, 2012 at 10:59Anant NarayananNovember 9th, 2012 at 14:59Robert NymanNovember 9th, 2012 at 15:04Hadar WeissNovember 11th, 2012 at 19:49Robert NymanNovember 12th, 2012 at 06:00Scott WhartonNovember 20th, 2012 at 20:36Robert NymanNovember 21st, 2012 at 03:10Jonathan ChetwyndNovember 23rd, 2012 at 12:42Robert NymanNovember 24th, 2012 at 04:01Randell JesupNovember 24th, 2012 at 05:43Jonathan ChetwyndNovember 24th, 2012 at 10:25Randell JesupNovember 24th, 2012 at 10:30Derick EppendahlDecember 3rd, 2012 at 03:38RodDecember 10th, 2012 at 19:31Robert NymanDecember 11th, 2012 at 03:20David GausmannDecember 12th, 2012 at 12:07Robert NymanDecember 12th, 2012 at 12:54CooperDecember 18th, 2012 at 18:13Michael AdeyeyeDecember 14th, 2012 at 09:45MisterXYZJanuary 13th, 2013 at 11:55Andre NatalFebruary 1st, 2013 at 08:33Robert Nyman [Editor]February 4th, 2013 at 02:56Appie MastenrbroekFebruary 5th, 2013 at 11:04Robert Nyman [Editor]February 5th, 2013 at 13:08ScottFebruary 18th, 2013 at 21:23Robert Nyman [Editor]February 19th, 2013 at 01:54