---
title: Opus audio codec version 1.2 released – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2017/06/opus-audio-codec-version-1-2-released/
author: Jean-Marc Valin
published: '2017-06-26'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The [Opus](https://opus-codec.org/) audio codec just got another major upgrade with the release of version 1.2 (see [demo](https://people.xiph.org/~jm/opus/opus-1.2/)). Opus is a totally open, royalty-free, audio codec that can be used for all audio applications, from music streaming and storage to high-quality video-conferencing and VoIP. Its standardization by the Internet Engineering Task Force (IETF) in 2012 (RFC 6716) was a major victory for open standards. Opus is the default codec for WebRTC and is now included in all major web browsers.

This new release brings many speech and music quality improvements, especially at low bitrates. The result is that Opus can now push stereo music bitrates down to 32 kb/s and encode full-band speech down to 14 kb/s. All that is achieved while remaining fully compatible with RFC 6716. The new release also includes optimizations, new options, as well as many bug fixes. [This demo](https://people.xiph.org/~jm/opus/opus-1.2/) shows a few of the upgrades that users and implementers will care about the most, including audio samples. For those who haven’t used Opus yet, now’s a good time to give it a try.

## About
[
Jean-Marc Valin ](https://jmvalin.ca/)

Jean-Marc Valin has a B.S., M.S., and PhD in Electrical Engineering from the University of Sherbrooke. He is the primary author of the Speex codec and one of the main authors of the Opus codec. His expertise includes speech and audio coding, speech recognition, echo cancellation, and other audio-related topics. He is currently employed by Mozilla to work on next-generation multimedia codecs.

## 4 comments

OmegaJune 26th, 2017 at 16:21Jean-Marc ValinJune 26th, 2017 at 21:07voracityJune 30th, 2017 at 22:25Julian LambJune 27th, 2017 at 18:19