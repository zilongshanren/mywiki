---
title: Themaister's Den
url: https://themaister.net/rsound.html
published: '2011-01-01'
source_blog: Maister's Graphics Adventures
source_site: https://themaister.net/blog
category: graphics
fetched: '2026-04-13'
---

RSound is a portable networked audio system.

It allows you to send audio from an application and transfer it directly to a different computer on your LAN network. It is an audio daemon with a much different focus than most other audio daemons.

The design philosophy is to be as lean as possible, in both protocol and client/server sides, with libraries and protocol being fully documented.

The only purpose in life for RSound is to transfer audio over a network. It does not, by design, attempt to mix and preprocess audio on server side before audio is passed to the speakers.

That is the job of the underlying operating system audio stack after all. It will only process audio if explicitly requested by the user, or the backend drivers requires it, typically resampling.

The implication of this is that RSound is quite portable. It has for example been ported to PlayStation 3 GameOS, and has been implemented into several homebrew emulator projects on the platform. RSound runs and is supported on Linux, Windows, Mac OS X and the BSDs.

Since few applications will support RSound directly, you can emulate most of the popular APIs to let almost any application work seamlessly with RSound:

RSound is designed primarily for audio and video applications, supporting adaptive latency control for video sync with either blocking/polling or callback-based buffering. It is not designed explicitly for low-latency operation, but you can achieve reasonable latencies (~50ms) given decent drivers and network.

The server side of RSound is fully supported by [RoarAudio](http://roaraudio.keep-cool.org/), another audio daemon. It supports far more advanced features under the hood.

RSound is distributed primarily through source.
You can grab the source from GitHub [here](https://github.com/Themaister/RSound).

Copyright (C) Hans-Kristian Arntzen - 2011