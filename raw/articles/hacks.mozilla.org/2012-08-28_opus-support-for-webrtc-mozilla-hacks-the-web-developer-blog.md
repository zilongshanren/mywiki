---
title: Opus Support for WebRTC – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/08/opus-support-for-webrtc/
author: Timothy B Terriberry
published: '2012-08-28'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

As [we announced during the beta cycle](https://hacks.mozilla.org/2012/07/firefox-beta-15-supports-the-new-opus-audio-format/), Firefox now supports the new [Opus audio format](http://opus-codec.org). We expect Opus to be published as RFC 6716 any day now, and we’re starting to see Opus support [pop](http://code.google.com/p/lavfilters/source/detail?r=bacb7df8bc81abcb78dbad164beded3f690b66db) [up](https://projects.savoirfairelinux.com/issues/14602) in [more](http://www.codecguide.com/klcp_beta.htm) and [more](http://www.rockbox.org/mail/archive/rockbox-dev-archive-2012-07/0013.shtml) [places](http://trac.videolan.org/vlc/ticket/7185). Momentum is really building.

### What does this mean for the web?

Keeping the Internet an open platform is part of [Mozilla’s mission](http://www.mozilla.org/about/mission.html). When the technology the Web needs doesn’t exist, we will invest the resources to create it, and release it royalty-free, just as we ask of others. Opus is one of these technologies.

Mozilla employs two of the key authors and developers, and has invested significant legal resources into avoiding known patent thickets. It uses processes and methods that have been long known in the field and which are considered patent-free. As a result, Opus is available on a [royalty-free basis](http://www.opus-codec.org/license/) and can be deployed by anyone, including other open-source projects. Everyone knows this is an incredibly challenging legal environment to operate in, but we think we’ve succeeded.

### Why Opus is important?

The Opus support in the <audio> tag we’re shipping today is great. We think it’s as good or better than all the other codecs people use there, particularly in the voice modes, which people have been [asking for](https://bugzilla.mozilla.org/show_bug.cgi?id=476752) for a long time. But our goals extend far beyond building a great codec for the <audio> tag.

Mozilla is heavily involved in the new [WebRTC](http://webrtc.org/) standards to bring real-time communication to the Web. This is the real reason we made Opus, and why its low-delay features are so important. At the recent [IETF meeting](http://www.ietf.org/meeting/84/) in Vancouver we achieved “[strong consensus](http://jmspeex.livejournal.com/11042.html)” to make Opus Mandatory To Implement (MTI) in WebRTC. Interoperability is even more important here than in the <audio> tag. If two browsers ship without any codecs in common, a website still has the option of encoding their content twice to be compatible with both. But that option isn’t available when the browsers are trying to talk to each other directly. So our success here is a big step in bringing interoperable real-time communication to the Web, using native Web technologies, without plug-ins.

Opus’s flexibility to scale to both very low bitrates and very high quality, and do all of it with very low delay, were instrumental in achieving this consensus. It would take at least six other codecs to satisfy all the use-cases Opus does. So try out Opus today for your podcasts, music broadcasts, games, and more. But look out for Opus in WebRTC [coming soon](https://bugzilla.mozilla.org/show_bug.cgi?id=694810).

## About
[
Timothy B. Terriberry ](http://people.xiph.org/~tterribe/)

Timothy B. Terriberry is a long-time volunteer for the Xiph.Org foundation, working on codecs such as Theora, Vorbis, CELT, and Opus. He has been contributing to Mozilla's media support since 2008 and hacking on WebRTC since 2010.

## 6 comments

BerndAugust 28th, 2012 at 09:31Ralph GilesAugust 28th, 2012 at 10:32njnAugust 28th, 2012 at 21:31FabioAugust 31st, 2012 at 23:22derfSeptember 3rd, 2012 at 00:46pdSeptember 12th, 2012 at 08:42