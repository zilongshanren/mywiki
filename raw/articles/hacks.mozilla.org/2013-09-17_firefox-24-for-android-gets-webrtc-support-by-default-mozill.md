---
title: Firefox 24 for Android gets WebRTC support by default – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2013/09/firefox-24-for-android-gets-webrtc-support-by-default/
author: Maire Reavy
published: '2013-09-17'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

WebRTC is now on [Firefox for Android](https://play.google.com/store/apps/details?id=org.mozilla.firefox) as well as Firefox Desktop! Firefox 24 for Android now supports mozGetUserMedia, mozRTCPeerConnection, and DataChannels by default. mozGetUserMedia has been in desktop releases since Firefox 20, and mozPeerConnection and DataChannels since Firefox 22, and we’re excited that Android is now joining Desktop releases in supporting these cool new features!

## What you can do

With WebRTC enabled, developers can:

- Capture camera or microphone streams directly from Firefox Android using only JavaScript (a feature we know developers have been wanting for a while!),
- Make browser to browser calls (audio and/or video) which you can test with sites like appspot.apprtc.com, and
- Share data (no server in the middle) to enable peer-to-peer apps (e.g. text chat, gaming, image sharing especially during calls)

![](../../assets/95f068a1713cbb91.jpg)


We’re eager to see the ideas developers come up with!

## For early adopters and feedback

Our support is still largely intended for developers and for early adopters at this stage to give us feedback. The working group specs are not complete, and we still have more features to implement and quality improvements to make. We are also primarily focused now on making 1:1 (person-to-person) calling solid — in contrast to multi-person calling, which we’ll focus on later. We welcome your testing and experimentation. Please give us feedback, file bug reports and start building new applications based on these new abilities.

If you’re not sure where to start, please start by reading some of the [ WebRTC articles on Hacks that have already been published](https://hacks.mozilla.org/category/webrtc/). In particular, please check out [WebRTC and the Early API](https://hacks.mozilla.org/2013/07/webrtc-and-the-early-api/), [The Making of Face to GIF](https://hacks.mozilla.org/2013/07/the-making-of-face-to-gif/), and [PeerSquared](https://hacks.mozilla.org/2013/07/peersquared-one-on-one-online-teaching-with-webrtc/) as well as [An AR Game](https://developer.mozilla.org/demos/detail/an-ar-game) (which won our getUserMedia Dev Derby) and [WebRTC Experiments & Demos](https://www.webrtc-experiment.com/).

![](../../assets/bac2f7790c23824c.jpg)


An example of simple video frame capture (which will capture new images at approximately 15fps):

```
navigator.getUserMedia({video: true, audio: false}, yes, no);
video.src = URL.createObjectURL(stream);
setInterval(function () {
context.drawImage(video, 0,0, width,height);
frames.push(context.getImageData(0,0, width,height));
}, 67);
```

Snippet of code taken from “Multi-person video chat” on nightly-gupshup (you can try it in the [WebRTC Test Landing Page](http://mozilla.github.io/webrtc-landing/) — full code is [on GitHub](https://github.com/jesup/nightly-gupshup.git))

```
function acceptCall(offer) {
log("Incoming call with offer " + offer);
navigator.mozGetUserMedia({video:true, audio:true}, function(stream) {
document.getElementById("localvideo").mozSrcObject = stream;
document.getElementById("localvideo").play();
document.getElementById("localvideo").muted = true;
var pc = new mozRTCPeerConnection();
pc.addStream(stream);
pc.onaddstream = function(obj) {
document.getElementById("remotevideo").mozSrcObject = obj.stream;
document.getElementById("remotevideo").play();
};
pc.setRemoteDescription(new mozRTCSessionDescription(JSON.parse(offer.offer)), function() {
log("setRemoteDescription, creating answer");
pc.createAnswer(function(answer) {
pc.setLocalDescription(answer, function() {
// Send answer to remote end.
log("created Answer and setLocalDescription " + JSON.stringify(answer));
peerc = pc;
jQuery.post(
"answer", {
to: offer.from,
from: offer.to,
answer: JSON.stringify(answer)
},
function() { console.log("Answer sent!"); }
).error(error);
}, error);
}, error);
}, error);
}, error);
}
function initiateCall(user) {
navigator.mozGetUserMedia({video:true, audio:true}, function(stream) {
document.getElementById("localvideo").mozSrcObject = stream;
document.getElementById("localvideo").play();
document.getElementById("localvideo").muted = true;
var pc = new mozRTCPeerConnection();
pc.addStream(stream);
pc.onaddstream = function(obj) {
log("Got onaddstream of type " + obj.type);
document.getElementById("remotevideo").mozSrcObject = obj.stream;
document.getElementById("remotevideo").play();
};
pc.createOffer(function(offer) {
log("Created offer" + JSON.stringify(offer));
pc.setLocalDescription(offer, function() {
// Send offer to remote end.
log("setLocalDescription, sending to remote");
peerc = pc;
jQuery.post(
"offer", {
to: user,
from: document.getElementById("user").innerHTML,
offer: JSON.stringify(offer)
},
function() { console.log("Offer sent!"); }
).error(error);
}, error);
}, error);
}, error);
}
```

Any code that runs on Desktop should run on Android. (Ah, the beauty of HTML5!) However, you may want to optimize for Android knowing that it could now be used on a smaller screen device and even rotated.

This is still a [hard-hat area](https://hacks.mozilla.org/2013/04/webrtc-update-our-first-implementation-will-be-in-release-soon-welcome-to-the-party-but-please-watch-your-head/), especially for mobile. We’ve tested our Android support of 1:1 calling with a number of major WebRTC sites, including [talky.io](https://talky.io), [apprtc.appspot.com](https://apprtc.appspot.com), and [codeshare.io](http://codeshare.io).

## Known issues

- Echo cancellation needs improvement; for calls we suggest a headset (
[Bug 916331](https://bugzilla.mozilla.org/show_bug.cgi?id=916331)) - Occasionally there are audio/video sync issues or excessive audio delay. We already have a fix in Firefox 25 that will improve delay (
[Bug 884365](https://bugzilla.mozilla.org/show_bug.cgi?id=884365)). - On some devices there are intermittent video-capture crashes; we’re actively investigating (
[Bug 902431](https://bugzilla.mozilla.org/show_bug.cgi?id=902431)). - Lower-end devices or devices with poor connectivity may have problems decoding or sending higher-resolution video at good frame rates.

![](../../assets/f70e25f9e3ab120c.jpg)


Please help us bring real-time communications to the web: build your apps, give us your feedback, report bugs, and help us test and develop. With your help, your ideas, and your enthusiasm, we will rock the web to a whole new level.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 13 comments

tumiraSeptember 17th, 2013 at 08:06Robert Nyman [Editor]September 17th, 2013 at 10:10Laura ForrestSeptember 17th, 2013 at 10:18AdrianSeptember 17th, 2013 at 14:36TumiraSeptember 17th, 2013 at 17:24PrykaSeptember 18th, 2013 at 06:56song zhengSeptember 18th, 2013 at 14:06GalaxySeptember 19th, 2013 at 00:32Kataskeui Istoselidon ThessalonikiSeptember 22nd, 2013 at 06:14IanSeptember 25th, 2013 at 14:44Robert Nyman [Editor]September 26th, 2013 at 01:27dobberxOctober 4th, 2013 at 07:14Bashir AhmedOctober 5th, 2013 at 19:40