---
title: WebRTC comes to Firefox – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/06/webrtc-comes-to-firefox/
author: Maire Reavy
published: '2013-06-25'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

As we mentioned in the [Hacks blog back in April](https://hacks.mozilla.org/2013/04/webrtc-update-our-first-implementation-will-be-in-release-soon-welcome-to-the-party-but-please-watch-your-head/) , WebRTC will be on by default in Firefox 22. [getUserMedia (gUM) has been on by default since Firefox 20](https://blog.mozilla.org/futurereleases/2013/01/12/capture-local-camera-and-microphone-streams-with-getusermedia-now-enabled-in-firefox/). PeerConnection and DataChannel, which enable video/audio calling and peer-to-peer data sharing, are what’s new in Firefox 22 (due to be released today).

WebRTC brings real-time communication to the web for the first time ever, and we’re excited to get this new technology into the hands of developers. We believe the industry has only scratched the surface of what’s possible with WebRTC, and only by getting it into the hands of developers and early adopters will we see this technology’s true potential.

## Known issues/limitations

There are a few known issues/limitations in the early releases:

- We are initially focused on getting 1:1 calling working well. We’ve done nothing to prevent conference or mesh calling, but depending on the capabilities of your device, video calls with multiple participants may be sluggish. We will be improving multi-person calling in future releases. Our roadmap includes full support for multi-person/conference/mesh calling and we expect to improve the experience in future releases.
- You may hear echo on calls when you or the party you’re talking to is playing sound over your computer speakers. We’re working on improving echo cancellation but for the time being, try wearing headphones if you experience this problem.
- On some systems, you may experience audio delay relative to the video. We’ve isolated the problem and are working on a fix for a near-term Firefox release.
- If you are behind a particularly restrictive NAT or firewall, you may have trouble connecting. We are adding support for media relaying (
[TURN](http://en.wikipedia.org/wiki/Traversal_Using_Relay_NAT)) in Firefox 23, so you should find this improving soon.

## Trying WebRTC support today

If you’d like to try out Firefox’s WebRTC support today, here are some sites that support WebRTC calling:

![](../../assets/60f3280ef6c11ebb.png)


**NOTE**: most of these sites support 3 or more callers. We expect basic 1:1 (2-person) calling to perform well enough for developer and early adopter use. As mentioned above, you may find that your mileage may vary with 3-or-more person calling using the current release.

If you’re a developer interested in [embedding WebRTC video chat into your website](https://hacks.mozilla.org/2013/05/embedding-webrtc-video-chat-right-into-your-website/), please check out article on that.

![](../../assets/465646ba647be1ca.png)


## Testing DataChannels

You can also try out DataChannels in Firefox, which is the first browser to launch a spec-compliant implementation of DataChannels to the market. Some sites and projects that use DataChannels:

[BananaBread game](https://developer.mozilla.org/en-US/demos/detail/bananabread)project. Our[WebRTC Data Channels for Great Multiplayer post](https://hacks.mozilla.org/2013/03/webrtc-data-channels-for-great-multiplayer/)explains how BananaBread uses DataChannels.[TowTruck](https://towtruck.mozillalabs.com/)project[Sharefest](http://www.sharefest.me/)– transfers files using DataChannels)[PeerCDN](https://peercdn.com/)– browser-based peer-to-peer CDN using DataChannels

## Using Firefox Nightly to test the latest

I still encourage developers to use [Firefox Nightly](http://nightly.mozilla.org/) because it has the latest and greatest code and improvements, and we will be continuing to improve existing features and add new ones as we get feedback from developers and users and as the WebRTC standard itself evolves.

## Rapid progress!

We expect new WebRTC sites, supporting PeerConnection and DataChannels, to come online rapidly over the next several months. We’ll keep you updated on our progress and on WebRTC’s progress here on Mozilla Hacks.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 33 comments

Jan KrupaJune 25th, 2013 at 08:27Robert Nyman [Editor]June 25th, 2013 at 12:37DennisJune 25th, 2013 at 08:39Robert Nyman [Editor]June 25th, 2013 at 12:38barduJune 25th, 2013 at 11:38Robert Nyman [Editor]June 25th, 2013 at 12:40Maire ReavyJune 26th, 2013 at 07:19Isaque GaldinoJune 25th, 2013 at 14:04Robert Nyman [Editor]June 25th, 2013 at 14:12LukeJune 25th, 2013 at 22:56AndyJune 25th, 2013 at 14:55Robert Nyman [Editor]June 25th, 2013 at 15:04Maire ReavyJune 26th, 2013 at 07:34JimJune 25th, 2013 at 17:20HankJune 26th, 2013 at 00:15Robert Nyman [Editor]June 26th, 2013 at 03:14Jaydson GomesJune 25th, 2013 at 19:30Robert Nyman [Editor]June 26th, 2013 at 03:15Jaydson GomesJune 25th, 2013 at 20:36Robert Nyman [Editor]June 26th, 2013 at 03:17Uwe RauschenbachJune 26th, 2013 at 03:56Robert Nyman [Editor]June 26th, 2013 at 06:00Maire ReavyJune 27th, 2013 at 17:34rehbJune 26th, 2013 at 05:50GerardoJune 26th, 2013 at 07:22vince dobbsJune 26th, 2013 at 08:56Robert Nyman [Editor]June 26th, 2013 at 09:29Mathew PorterJune 26th, 2013 at 14:08Eugene KrevenetsJune 27th, 2013 at 09:10Robert Nyman [Editor]June 27th, 2013 at 13:37AlexeyJuly 11th, 2013 at 09:12Robert Nyman [Editor]July 11th, 2013 at 09:21AlexeyJuly 11th, 2013 at 09:26