---
title: Full WebRTC support is soon coming to a web browser near you! – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2012/09/full-webrtc-support-is-soon-coming-to-a-web-browser-near-you/
author: Robert Nyman
published: '2012-09-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The web is such an integral part of our lives and how we communicate with each other. That’s why we get so excited when we reach evolutionary peaks that take us leaps and bounds forward in offering a better and open game-changing experience for users and web developers alike! We believe [WebRTC](https://developer.mozilla.org/docs/WebRTC) to be one of those steps.

## What is WebRTC?

The RTC in WebRTC stands for Real-Time Communications, offered directly on the web without any need for plugins or third-party software. The idea is to be able to share and stream video, audio and data in the most powerful fashion, directly in a web browser, offering media rich exchanges.

Representatives from Mozilla, Google, Opera and others have been working on WebRTC over a year, and it is on its way to becoming a [W3C recommendation](http://dev.w3.org/2011/webrtc/editor/webrtc.html).

The three corner stones in WebRTC are:

- MediaStream
- Granting web apps/sites access to the camera and microphone on your computer, via the
[getUserMedia API](https://hacks.mozilla.org/2012/07/getusermedia-is-ready-to-roll/). - DataChannel
- Communicating data peer to peer.
- PeerConnection API
- Enabling direct peer to peer connections between two web browsers for audio and video.

## Code simplicity

If you take a look at our work with [WebAPI](https://wiki.mozilla.org/WebAPI), you will see examples of a number of simple and intuitive APIs. We believe it’s important for WebRTC to be as easy-to-use by all web developers, not just the rocket scientists among us (nothing wrong with being one, by the way – it’s just that not everyone is. :-))

To enable this, the web browser handles the real-time media and networking for the web developer, so developers can focus on writing apps that include real-time communication as one of the features. We feel the web itself has in part become an incredibly popular tool for so many developers because it makes it easy to create wonderful things to share with the world.

We believe WebRTC will become successful for the same reason.

For example – and you’ve probably already seen this elsewhere – it is very simple to stream the webcam of your computer directly into a web page (with user-granted access, of course):

```
/*
NOTE: This is meant to show a simplified version,
without prefixes and such that are currently used
for experimental implementations
*/
// Get a reference to an existing video element, set to autoplay
var liveVideo = document.querySelector("#live-video");
/* Request access to the webcam
Note: in current implementations, this has to
be prefixed, and Google Chrome needs a Blob URL
for the MediaStream
*/
navigator.getUserMedia(
{video: true},
function (stream) {
liveVideo.src = stream;
},
function (error) {
console.log("An error occurred: " + error);
}
);
```

If you want to delve more into the code and APIs right now, then [Real-time communication without plugins](http://www.html5rocks.com/en/tutorials/webrtc/basics/) is a good read.

## Coming to a web browser near you!

It is important to note that WebRTC has been planned for a long time, and we are now finally reaching a step where cutting edge web browsers – such as Firefox, Google Chrome and Opera – implement their support and bring WebRTC to the web. With Firefox, our plan is to ship full WebRTC support in Firefox 18, in the beginning of January next year.

Stay tuned, and we’ll keep you up to date on the progress!

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 25 comments

ThijsSeptember 11th, 2012 at 04:35Robert NymanSeptember 11th, 2012 at 04:48Daniel FilhoSeptember 11th, 2012 at 05:37Robert NymanSeptember 11th, 2012 at 05:51ArnoSeptember 11th, 2012 at 07:27Robert NymanSeptember 11th, 2012 at 09:48ShmerlSeptember 11th, 2012 at 11:54Randell JesupSeptember 11th, 2012 at 12:08ShmerlSeptember 11th, 2012 at 12:17rjesupSeptember 11th, 2012 at 13:05ShmerlSeptember 11th, 2012 at 13:28ShmerlSeptember 11th, 2012 at 13:30Peter MoskovitsSeptember 13th, 2012 at 16:09Randell JesupSeptember 14th, 2012 at 02:44ShmerlSeptember 19th, 2012 at 09:05Randell JesupSeptember 19th, 2012 at 09:36ShmerlSeptember 20th, 2012 at 15:44SarajSeptember 14th, 2012 at 16:14Robert NymanSeptember 17th, 2012 at 02:00JimSeptember 18th, 2012 at 21:26Robert NymanSeptember 19th, 2012 at 03:50HaykSeptember 20th, 2012 at 21:57Robert NymanSeptember 21st, 2012 at 01:13AnujOctober 28th, 2012 at 21:54Robert NymanOctober 30th, 2012 at 04:49