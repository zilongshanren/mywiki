---
title: getUserMedia is ready to roll! – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/07/getusermedia-is-ready-to-roll/
author: Anant Narayanan
published: '2012-07-13'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

We blogged about some of our [WebRTC efforts](https://hacks.mozilla.org/2012/04/webrtc-efforts-underway-at-mozilla/) back in April. Today we have an exciting update for you on that front: *getUserMedia* has landed on mozilla-central! This means you will be able to use the API on the latest [Nightly](http://nightly.mozilla.org) versions of Firefox, and it will eventually make its way to a release build.

*getUserMedia* is a [DOM API](https://developer.mozilla.org/en/DOM/) that allows web pages to obtain video and audio input, for instance, from a webcam or microphone. We hope this will open the possibility of building a whole new class of web pages and applications. This DOM API is one component of the [WebRTC project](https://wiki.mozilla.org/Media/WebRTC), which also includes APIs for peer-to-peer communication channels that will enable exchange of video steams, audio streams and arbitrary data.

We’re still working on the [PeerConnection](http://dev.w3.org/2011/webrtc/editor/webrtc.html) API, but getUserMedia is a great first step in the progression towards full WebRTC support in Firefox! We’ve certainly come a long way since the first image from a webcam [appeared on a web page](https://blog.mozilla.org/labs/2010/10/cloud-meet-rainbow/) via a DOM API. (Not to mention [audio recording support in Jetpack](https://blog.mozilla.org/labs/2009/07/jetpack-0-4-audio-recording-page-mods/) before that.)

![](https://static-ssl-cdn.addons.mozilla.net/img/uploads/previews/full/50/50499.png)


We’ve implemented a prefixed version of the “[Media Capture and Streams](http://dev.w3.org/2011/webrtc/editor/getusermedia.html)” standard being developed at the W3C. Not all portions of the specification have been implemented yet; most notably, we do not support the Constraints API (which allows the caller to request certain types of audio and video based on various parameters).

We have also implemented a Mozilla specific extension to the API: the first argument to mozGetUserMedia is a dictionary that will also accept the property `{picture: true}`

in addition to `{video: true}`

or `{audio: true}`

. The picture API is an experiment to see if there is interest in a dedicated mechanism to obtain a single picture from the user’s camera, without having to set up a video stream. This could be useful in a profile picture upload page, or a photo sharing application, for example.

Without further ado, let’s start with a simple example! Make sure to create a pref named “`media.navigator.enabled`

” and set it to * true* via

`about:config`

first. We’ve put the pref in place because we haven’t implemented a permissions model or any UI for prompting the user to authorize access to the camera or microphone. This release of the API is aimed at developers, and we’ll enable the pref by default after we have a permission model and UI that we’re happy with.%CODEgum%

There’s also a [demo page](https://people.mozilla.com/~anarayanan/gum_test.html) where you can test the audio, video and picture capabilities of the API. Give it a whirl, and let us know what you think! We’re especially interested in feedback from the web developer community about the API and whether it will meet your use cases. You can leave comments on this post, or on the [dev-media](https://groups.google.com/forum/#!forum/mozilla.dev.media) mailing list or newsgroup.

We encourage you to get involved with the project – there’s a lot of information about our ongoing efforts on the [project wiki page](https://wiki.mozilla.org/Media/WebRTC). Posting on the mailing list with your questions, comments and suggestions is great way to get started. We also hang out on the [#media IRC channel](irc://irc.mozilla.org/media), feel free to drop in for an informal chat.

Happy hacking!

## About
[
Anant Narayanan ](http://kix.in/)

[@anantn](http://twitter.com/anantn) is a hacker at [Mozilla Labs](http://mozillalabs.com/) who specializes in generalism. He has previously worked on [Weave](https://wiki.mozilla.org/Labs/Weave), [Jetpack](https://wiki.mozilla.org/Jetpack), [Account Manager](https://wiki.mozilla.org/Labs/Weave/Identity/Account_Manager), and [Rainbow](https://mozillalabs.com/en-US/rainbow/) among other projects. He is currently fiddling with [Open Web Apps](http://apps.mozillalabs.com/) and [Real-time communication for the Web](http://webrtc.org/).

## 40 comments

Anant NarayananJuly 13th, 2012 at 10:41paulo995July 13th, 2012 at 11:17Anant NarayananJuly 13th, 2012 at 11:27AlexandreJuly 13th, 2012 at 14:41Anant NarayananJuly 13th, 2012 at 15:01AlexandreJuly 13th, 2012 at 15:18Anant NarayananJuly 13th, 2012 at 15:22AshleyJuly 13th, 2012 at 15:59Vilson VieiraJuly 15th, 2012 at 22:54Francisco JordanoJuly 14th, 2012 at 12:30KedarJuly 14th, 2012 at 21:41Bryan ClarkJuly 16th, 2012 at 13:37Anant NarayananJuly 16th, 2012 at 13:46thinsoldierJuly 17th, 2012 at 11:56thinsoldierJuly 17th, 2012 at 11:58Anant NarayananJuly 18th, 2012 at 09:37andri iswandiJuly 18th, 2012 at 00:13T-BoneJuly 18th, 2012 at 04:04Anant NarayananJuly 18th, 2012 at 09:39Fabricio C ZuardiJuly 18th, 2012 at 18:42Anant NarayananSeptember 27th, 2012 at 09:54shazJuly 22nd, 2012 at 11:51T-BoneJuly 22nd, 2012 at 14:14ackggJuly 23rd, 2012 at 22:34Anant NarayananSeptember 27th, 2012 at 09:56Vaidik KapoorSeptember 17th, 2012 at 06:52JoaoSeptember 27th, 2012 at 02:37Anant NarayananSeptember 27th, 2012 at 10:02joaoSeptember 27th, 2012 at 10:39MaisondoufOctober 2nd, 2012 at 22:02Prasanna VenkadeshOctober 8th, 2012 at 02:50Anant NarayananOctober 8th, 2012 at 08:34AlexandreOctober 8th, 2012 at 11:23davidOctober 9th, 2012 at 07:08Alexander KarlstadOctober 11th, 2012 at 06:40Laxminarayan KamathDecember 15th, 2012 at 21:58Robert O’CallahanOctober 23rd, 2012 at 15:43Andor SalgaDecember 18th, 2012 at 18:33EibrielJanuary 21st, 2013 at 22:21Robert NymanJanuary 22nd, 2013 at 01:45