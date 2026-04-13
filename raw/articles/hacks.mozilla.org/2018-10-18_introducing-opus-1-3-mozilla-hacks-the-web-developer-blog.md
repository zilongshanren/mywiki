---
title: Introducing Opus 1.3 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2018/10/introducing-opus-1-3/
author: Jean-Marc Valin
published: '2018-10-18'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The [Opus Audio Codec](https://opus-codec.org/) gets another major update with the release of version 1.3 ([demo](https://people.xiph.org/~jm/opus/opus-1.3/)).

Opus is a totally open, royalty-free audio codec that can be used for all audio applications, from music streaming and storage to high-quality video-conferencing and VoIP. Six years after its standardization by the IETF, Opus is now included in all major browsers and mobile operating systems. It has been adopted for a wide range of applications, and is the default WebRTC codec.

This release brings quality improvements to both speech and music compression, while remaining fully compatible with RFC 6716. Here’s a few of the upgrades that users and implementers will care about the most.

Opus 1.3 includes a brand new speech/music detector. It is based on a [recurrent neural network](https://en.wikipedia.org/wiki/Recurrent_neural_network) and is both simpler and more reliable than the detector that has been used since version 1.1. The new detector should improve the Opus performance on mixed content encoding, especially at bitrates below 48 kb/s.

There are also many improvements for speech encoding at lower bitrates, both for mono and stereo. The demo contains many more details, as well as some audio samples. This new release also includes a cool new feature: [ambisonics](https://en.wikipedia.org/wiki/Ambisonics) support. Ambisonics can be used to encode 3D audio soundtracks for VR and 360 videos.

You can read all the details of [The Release of Opus 1.3](https://people.xiph.org/~jm/opus/opus-1.3/).

## About
[
Jean-Marc Valin ](https://jmvalin.ca/)

Jean-Marc Valin has a B.S., M.S., and PhD in Electrical Engineering from the University of Sherbrooke. He is the primary author of the Speex codec and one of the main authors of the Opus codec. His expertise includes speech and audio coding, speech recognition, echo cancellation, and other audio-related topics. He is currently employed by Mozilla to work on next-generation multimedia codecs.

## One comment

MohorelienNovember 1st, 2018 at 08:38