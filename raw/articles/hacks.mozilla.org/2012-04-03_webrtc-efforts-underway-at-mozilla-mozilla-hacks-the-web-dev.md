---
title: WebRTC efforts underway at Mozilla! – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/04/webrtc-efforts-underway-at-mozilla/
author: Anant Narayanan
published: '2012-04-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Last week, a small team from Mozilla attended [IETF 83](https://www.ietf.org/meeting/83/index.html) in Paris, and we showed an early demo of a simple video call between two [BrowserID](http://browserid.org/)-authenticated parties in a special build of Firefox with [WebRTC](http://webrtc.org/) support. It is still very early days for WebRTC integration in Firefox, but we’re really excited to show you something that works!

At Mozilla Labs, we’ve been experimenting with [integrating social features](https://mozillalabs.com/blog/2012/03/experimenting-with-social-features-in-firefox/) in the browser, and it seemed like a cool idea to combine this with WebRTC to establish a video call between two users who are signed in using BrowserID (now called [Persona](http://mozilla.org/persona/)). The [SocialAPI add-on](https://github.com/mozilla/socialapi-dev), once installed, provides a sidebar where web content from the social service provider is rendered. In our [demo social service](https://github.com/mozilla/mozilla-demo-social-service), we show a “buddy list” of people who are currently signed in using Persona.

The video chat page that is served when the user initiates a video chat uses a custom API intended to simulate the [getUserMedia](http://dev.w3.org/2011/webrtc/editor/getusermedia.html) and [PeerConnection](http://dev.w3.org/2011/webrtc/editor/webrtc.html) APIs currently being standardized at the W3C. A `<canvas>`

is used to render both the remote and local videos, though it is also possible to render them in a `<video>`

. We’re working very quickly to implement the standard APIs, and you can follow our progress on the [tracker bug](https://bugzilla.mozilla.org/show_bug.cgi?id=665909).

A lot of folks burned the midnight oil to get this demo ready before the IETF event, and special thanks are due to [Eric Rescorla](http://www.rtfm.com/), [Michael Hanson](http://www.open-mike.org/), [Suhas Nandakumar](https://github.com/suhasHere), [Enda Mannion](https://github.com/emannion), [Ethan Hugg](https://github.com/ethanhugg), the folks behind [Spacegoo](http://www.spacegoo.com/), and [Randell Jesup](https://plus.google.com/106186763111547737548/posts), in addition to the whole media team here at Mozilla.

Current development is being done on a branch of mozilla-central called [alder](https://hg.mozilla.org/projects/alder). It is going to be an exciting few months ahead as we work towards bringing WebRTC to Firefox. There is a lot of work to do, and if you are interested in contributing, please reach out! [Maire Reavy](http://mozillamediagoddess.org/), our product person and project lead for WebRTC would be happy to help you find ways to contribute. Many of us are also usually available in IRC at [#media](irc://irc.mozilla.org/media), and we have a [mailing list](https://lists.mozilla.org/listinfo/dev-media).

Transcript of screencast:


Hi, I’m Anant from Mozilla Labs and I’m here at IETF where we are demonstrating a simple video call between two BrowserID-authenticated parties, using the new WebRTC APIs that we are working on.

This is a special build of Firefox with WebRTC support, and also has the experimental SocialAPI add-on from Mozilla Labs installed. On the right hand side you can see web content served by demosocialservice.org, to which I will sign with BrowserID. Once I’m signed in, I can see all my online friends on the sidebar. I see my friend Enda is currently online, and so I’m going to click the video chat button to initiate a call.

Here, I see a very early prototype of a video call window served up by our demo social service. Now, I can click the Start Call button to let Enda know that I want to speak with him. Once he accepts the call, a video stream is established between the two parties as you can see. So, that was a video call built entirely using[JavaScript]and[HTML]!

You can check out the source code for this demo, as well as learn how to contribute to the ongoing WebRTC efforts at Mozilla in this blog post. Thanks for watching!

## About
[
Anant Narayanan ](http://kix.in/)

[@anantn](http://twitter.com/anantn) is a hacker at [Mozilla Labs](http://mozillalabs.com/) who specializes in generalism. He has previously worked on [Weave](https://wiki.mozilla.org/Labs/Weave), [Jetpack](https://wiki.mozilla.org/Jetpack), [Account Manager](https://wiki.mozilla.org/Labs/Weave/Identity/Account_Manager), and [Rainbow](https://mozillalabs.com/en-US/rainbow/) among other projects. He is currently fiddling with [Open Web Apps](http://apps.mozillalabs.com/) and [Real-time communication for the Web](http://webrtc.org/).

## 16 comments

Tod RobbinsApril 3rd, 2012 at 09:55Anant NarayananApril 3rd, 2012 at 10:09Forrest O.April 10th, 2012 at 03:07Anant NarayananApril 14th, 2012 at 16:05Caspy7April 5th, 2012 at 10:20CCAC (Collaborative for Communication Access via Captioning)April 9th, 2012 at 00:04StephanApril 9th, 2012 at 07:40Anant NarayananApril 9th, 2012 at 10:11Andrew DuckerApril 9th, 2012 at 10:09Anant NarayananApril 9th, 2012 at 10:16gt2rsApril 14th, 2012 at 15:41YanivJune 5th, 2012 at 01:25DebbraMay 15th, 2012 at 09:12Sam DuttonJuly 12th, 2012 at 07:06majid khosraviAugust 17th, 2012 at 15:55PraveshAugust 18th, 2012 at 03:28