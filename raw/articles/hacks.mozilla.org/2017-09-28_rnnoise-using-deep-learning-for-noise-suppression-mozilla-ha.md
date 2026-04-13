---
title: 'RNNoise: Using Deep Learning for Noise Suppression – Mozilla Hacks - the Web
  developer blog'
url: https://hacks.mozilla.org/2017/09/rnnoise-deep-learning-noise-suppression/
author: Jean-Marc Valin
published: '2017-09-28'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The Mozilla Research [RRNoise project](https://people.xiph.org/~jm/demo/rnnoise/) shows how to apply deep learning to noise suppression. It combines *classic* signal processing with deep learning, but it’s small and **fast**. No expensive GPUs required — it runs easily on a Raspberry Pi. The result is easier to tune and sounds better than traditional noise suppression systems (been there!).

RNNoise will help improve the quality of [WebRTC](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API) calls, especially for multiple speakers in noisy rooms. It is also small enough and fast enough to be executed directly in JavaScript, making it possible for Web developers to embed it directly in Web pages when recording audio.

You can improve RNNoise by [donating your noise to science](https://people.xiph.org/~jm/demo/rnnoise/donate.html). We’re interested in noise from any environment where you might communicate using voice. That can be your office, your car, on the street, or anywhere you might use your phone or computer. The more realistic noise we have, the better the models we can build and the better the output.

Read in depth about the [ RNNoise project](https://people.xiph.org/~jm/demo/rnnoise/).

## About
[
Jean-Marc Valin ](https://jmvalin.ca/)

Jean-Marc Valin has a B.S., M.S., and PhD in Electrical Engineering from the University of Sherbrooke. He is the primary author of the Speex codec and one of the main authors of the Opus codec. His expertise includes speech and audio coding, speech recognition, echo cancellation, and other audio-related topics. He is currently employed by Mozilla to work on next-generation multimedia codecs.

## 3 comments

Jeff hintySeptember 29th, 2017 at 00:13Gustavo GarciaSeptember 29th, 2017 at 12:30Jean-Marc ValinSeptember 29th, 2017 at 12:54