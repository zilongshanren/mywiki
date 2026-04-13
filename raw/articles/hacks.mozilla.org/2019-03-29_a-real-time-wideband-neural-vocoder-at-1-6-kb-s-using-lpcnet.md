---
title: A Real-Time Wideband Neural Vocoder at 1.6 kb/s Using LPCNet – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2019/03/a-real-time-wideband-neural-vocoder-at-1-6-kb-s-using-lpcnet/
author: Jean-Marc Valin
published: '2019-03-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/9644fd11c6782deb.jpg)


This is an update on the [LPCNet project](https://people.xiph.org/~jm/demo/lpcnet_codec/), an efficient neural speech synthesizer from Mozilla’s Emerging Technologies group. In an [an earlier demo](https://people.xiph.org/~jm/demo/lpcnet/) from late last year, we showed how LPCNet combines signal processing and deep learning to improve the efficiency of neural speech synthesis.

This time, we turn LPCNet into a very low-bitrate neural speech codec that’s actually usable on current hardware and even on phones ([as described in this paper](https://jmvalin.ca/papers/lpcnet_codec.pdf)). It’s the first time a neural vocoder is able to run in real-time using just one CPU core on a phone (as opposed to a high-end GPU)! The resulting bitrate — just 1.6 kb/s — is about 10 times less than what wideband codecs typically use. The quality is much better than existing very low bitrate vocoders. In fact, it’s comparable to that of more traditional codecs using higher bitrates.

This new codec can be used to improve voice quality in countries with poor network connectivity. It can also be used as redundancy to improve robustness to packet loss for everyone. In storage applications, it can compress an hour-long podcast to just 720 kB (so you’ll still have room left on your floppy disk). With some further work, the technology behind LPCNet could help improve existing codecs at very low bitrates.

Learn more about our ongoing work and check out the ** playable demo in this article**.

## About
[
Jean-Marc Valin ](https://jmvalin.ca/)

Jean-Marc Valin has a B.S., M.S., and PhD in Electrical Engineering from the University of Sherbrooke. He is the primary author of the Speex codec and one of the main authors of the Opus codec. His expertise includes speech and audio coding, speech recognition, echo cancellation, and other audio-related topics. He is currently employed by Mozilla to work on next-generation multimedia codecs.