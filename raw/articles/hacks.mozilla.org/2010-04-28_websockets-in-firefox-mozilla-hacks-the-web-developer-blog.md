---
title: WebSockets in Firefox – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2010/04/websockets-in-firefox/
author: Christopher Blizzard
published: '2010-04-28'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Here’s the pitch for [WebSockets](http://en.wikipedia.org/wiki/Web_Sockets): a low-complexity, low-latency, bi-directional communication system that has a [pretty simple API](http://dev.w3.org/html5/websockets/#websocket) for web developers. Let’s break that down, and then talk about if and when we’re going to include it in Firefox:

**Low-complexity**

The WebSocket protocol, which is started via an HTTP-like handshake, has a relatively simple model for sending text packets back and forth. The complexity of the protocol is quite low. There’s no multiplexing, no support for binary data, and once the data connection is set up, the actual transport is quite cheap.

Note that there are people who feel – possibly correctly – that support for multiplexing and binary data should be added. That would obviously increase the complexity but in some cases might be worth the cost. But more on that later.

**Bi-directional Communication**

One of the key aspects of WebSocket is its support for simple bi-directional communication. Servers can easily send updates to clients and clients can send updates to servers. Many of the [comet-style](http://en.wikipedia.org/wiki/Comet_%28programming%29) applications that people have built will be much simpler and faster with this model because the protocol and API support it directly.

While allowing for bi-directional communication it also is bound by the HTTP same-origin model. That is, it’s doesn’t give the browser the ability to connect to any site on any port it wants to.

So WebSocket is really TCP with the HTTP security model.

**Low-latency**

This is actually the primary value in WebSockets. The key thing is that the cost of sending a small amount of data is also very small. It’s possible to do bi-directional communication today with comet-style applications, but small amounts of data often require a huge amount of overhead to do so.

A second-hand story to give you a sense of scale: Google Wave, which tries to do real-time communication with keystrokes has a several-kilobyte overhead for just about every keystroke because of the TCP startup, teardown and HTTP message headers involved with what should be only a few bytes sent over the wire.

I haven’t tried, but I’m going to guess that if you built [Quake](http://code.google.com/p/quake2-gwt-port/) on top of HTTP comet that the interactive experience would be poor. So this is where WebSockets really shine.

**Simple API**

The [actual API](http://dev.w3.org/html5/websockets/#the-websocket-interface) that a developer sees for WebSocket is relatively simple. You can send messages, you can get messages, you get events when sockets open, close or there’s an error. Additional complexity, which I’m sure others will develop, will happen in JavaScript and backend libraries.

(While this might seem like punting on the issue of complexity, this is actually the model for success we’ve seen for other browser standards: build something relatively simple that others can experiment with. When we understand what’s slow or what’s preventing progress, iterate and improve.)

**When will it be in Firefox?**

We really really want to support WebSockets in the next version of Firefox. And a lot of other people want us to include support too.

[The first set of test patches](https://bugzilla.mozilla.org/show_bug.cgi?id=472529), written by the wonderful Wellington Fernando de Macedo (one of our most excellent contributors!) was first submitted in April of 2009. Since then we’ve been iterating both on the patches themselves and following the spec as it’s changed.

Unfortunately, the spec itself is still under revision. WebSockets did ship in [Chrome](http://blog.chromium.org/2009/12/web-sockets-now-available-in-google.html) with version 4 and I’m told by Chrome developers that it’s going to be included in Chrome 5, without changes. Unfortunately, the [version that Google included in Chrome](http://tools.ietf.org/html/draft-hixie-thewebsocketprotocol-75) doesn’t reflect the [current draft](http://www.whatwg.org/specs/web-socket-protocol/). The handshake for how to start a WebSocket connection has changed, largely to improve security on servers. There’s also a lot of ongoing discussion on the role of [integrated compression](http://www.ietf.org/mail-archive/web/hybi/current/msg01810.html), direct support for binary data (instead of encoding binary data as strings), whether or not the protocol should support multiplexing and a number of other issues.

Since WebSocket isn’t used widely yet, and that Chrome has an uptake rate that’s similar to Firefox, the hope is that once a more recent draft makes it through the process that both Chrome and Firefox can include a more recent version at around the same time.

So in short: we want to ship it because the promise of WebSockets is great, but we’ll have to see if it’s stable and safe enough to do so. Code isn’t the issue – we’ve had that for a while. It’s whether or not there’s consensus on if the protocol is “done enough” to ship it to a few hundred million people.

## 40 comments

John DowdellApril 28th, 2010 at 10:38Su-SheeApril 28th, 2010 at 11:11SchizoDuckieApril 28th, 2010 at 13:59AaronApril 28th, 2010 at 14:12TomerApril 28th, 2010 at 15:42Brendan MillerApril 28th, 2010 at 15:56GeorgeApril 28th, 2010 at 16:38ArunApril 28th, 2010 at 21:10Lars GuntherApril 29th, 2010 at 00:54Simon WillisonApril 29th, 2010 at 04:08Max WilliamsApril 29th, 2010 at 07:22Cyrus OmarApril 30th, 2010 at 11:01Brett ZamirApril 30th, 2010 at 22:48Alexander SchulzeMay 5th, 2010 at 10:41puranMay 5th, 2010 at 12:18Vitaliy KupetsMay 17th, 2010 at 08:51Christopher BlizzardMay 17th, 2010 at 20:13jamesJuly 10th, 2010 at 06:05jamesJuly 10th, 2010 at 06:06Vitaliy KupetsJuly 12th, 2010 at 01:38Vitaliy KupetsJuly 12th, 2010 at 01:39Vitaliy KupetsJuly 12th, 2010 at 01:38Vitaliy KupetsJuly 12th, 2010 at 01:45DerFichtlJuly 12th, 2010 at 02:36JamesJuly 12th, 2010 at 05:19JamesJuly 12th, 2010 at 05:20JamesJuly 12th, 2010 at 05:20JamesJuly 12th, 2010 at 05:21Nathan SweetJuly 29th, 2010 at 11:52John Deer TractorAugust 10th, 2010 at 10:58SebastienAugust 10th, 2010 at 13:54Hector SantosAugust 24th, 2010 at 04:47enderSeptember 10th, 2010 at 18:04Adam RochfordSeptember 22nd, 2010 at 14:53enderSeptember 23rd, 2010 at 00:13