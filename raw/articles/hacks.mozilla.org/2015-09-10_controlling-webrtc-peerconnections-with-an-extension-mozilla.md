---
title: Controlling WebRTC PeerConnections with an extension – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2015/09/controlling-webrtc-peerconnections-with-an-extension/
author: Philipp Hancke
published: '2015-09-10'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**Author’s note:** Firefox recently added some features (in [Firefox 42](https://developer.mozilla.org/en-US/Firefox/Releases/42)) to allow users to exercise added control over WebRTC `RTCPeerConnections`

, IP address gathering used in connecting them, and what IP addresses are exposed to JS applications. For a detailed explanation of the issues this is addressing and why Firefox is addressing them, please see my [(Maire’s) personal blog post](http://mozillamediagoddess.org/2015/09/10/webrtc-privacy/) about the issue. Discussion of the problems, risks, tradeoffs, and reasoning are best done there. This article is about the new features in the code and how to access them.

Maire Reavy

Engineering Manager, WebRTC


To control IP address exposure and `RTCPeerConnection`

usage, we’ve provided methods to *hook* `createOffer/createAnswer`

and added about:config prefs for controlling which candidates are available during ICE negotiation. Also, some controls already existed in about:config. You can learn more about the controls available on Mozilla’s [wiki page about WebRTC privacy](https://wiki.mozilla.org/Media/WebRTC/Privacy).

The `createOffer/createAnswer`

hooks allow extensions to modify the behaviour of the `PeerConnection`

and, for example, add a door-hanger very similar to the one you get when a site uses the `getUserMedia`

API to access camera and microphone. We have done a [proof of concept extension](https://github.com/fippo/plumber) and this is how it looks for a web site which only uses the `DataChannel`

:

![webrtc-datachannel-doorhanger](../../assets/738472f0f757ae96.png)


From a user interaction perspective, it’s important to ask for access permission in a non-scary way that an end user can understand. For `getUserMedia`

, i.e., access to the user’s camera and microphone, the question asked is:

*Would you like to share your camera and microphone with webrtc.github.io?*

The implications of that are quite clear, as the website can record your voice and video and may send it to someone else.

The sample extension door-hanger pops up in two cases:

- The site uses a receive-only connection, i.e., only receives video — you can test it
[here](https://webrtc.github.io/samples/src/content/peerconnection/trickle-ice/). - The site uses the datachannel without calling getUserMedia as shown with
[this sample](https://webrtc.github.io/samples/src/content/datachannel/basic/).

For the case where the site has permission to access camera and microphone, e.g. [Talky.io](https://talky.io), no additional question is asked. This minimizes the number of questions the user has to answer and retains much of the current behaviour.

For the receive-only case, it is a more awkward question to ask. The use-case here is one-way streaming, e.g., for a webinar. Users don’t expect to be asked for permission here since you don’t need to grant similar permissions to watch a recorded video on YouTube.

For data channels, there are a number of different use cases, ranging from file transfer to gaming to peer-to-peer CDNs. For file transfer, the workflow is rather easy to explain to the user — they select a file, the door-hanger pops up, they allow it, and the file gets transferred. There is a direct connection between the user action and the popup. That applies to gaming as well.

The peer-to-peer CDN use case is harder. You start playing a video and the browser asks for something called DataChannel?! If you are a developer relying on this use-case, we recommend you try [the sample extension](https://github.com/fippo/plumber), and use it to develop a good user experience around that use-case. We’d love to hear your real world feedback.

In the recently reported case of the New York Times’ somewhat [surprising usage of WebRTC](https://webrtchacks.com/dear-ny-times/), the developer cited “fraud detection” as the use case. WebRTC was not built to solve this problem, and there are better tools and technologies for the job. We urge you to put those to use.

If you are an extension developer you can take a look at the [source code of the extension](https://github.com/fippo/plumber) to see what is needed to implement this interaction; you basically need to override the handling of `rtcpeer:Request`

in the `webrtcUI.receiveMessage`

handler. Let us know if you have any questions, either in the comments or open an [issue over at github](https://github.com/fippo/plumber/issues).

## About Philipp Hancke

## About Maire Reavy

Maire is the engineering manager for Mozilla’s WebRTC team.

## 5 comments

RezaSeptember 13th, 2015 at 12:40sofiSeptember 14th, 2015 at 07:58Havi Hoffman [Editor]September 15th, 2015 at 11:54Craig CookSeptember 15th, 2015 at 12:06sofiSeptember 15th, 2015 at 12:28