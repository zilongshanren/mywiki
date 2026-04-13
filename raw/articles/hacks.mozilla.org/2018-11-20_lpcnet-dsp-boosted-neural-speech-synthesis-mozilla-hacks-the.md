---
title: 'LPCNet: DSP-Boosted Neural Speech Synthesis – Mozilla Hacks - the Web developer
  blog'
url: https://hacks.mozilla.org/2018/11/lpcnet-dsp-boosted-neural-speech-synthesis/
author: Jean-Marc Valin
published: '2018-11-20'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

![](https://people.xiph.org/~jm/demo/lpcnet/sampling200.png)


LPCNet is a new project out of Mozilla’s Emerging Technologies group — an efficient neural speech synthesiser with reduced complexity over some of its predecessors. Neural speech synthesis models like [WaveNet](https://deepmind.com/blog/wavenet-generative-model-raw-audio/) have already demonstrated impressive speech synthesis quality, but their computational complexity has made them hard to use in real-time, especially on phones. In a similar fashion to the [RNNoise](https://people.xiph.org/~jm/demo/rnnoise/) project, our solution with LPCNet is to use a combination of deep learning and digital signal processing (DSP) techniques.

LPCNet can help improve the quality of text-to-speech (TTS), low bitrate speech coding, time stretching, and more. You can hear the difference for yourself in our [LPCNet demo page](https://people.xiph.org/~jm/demo/lpcnet/), where LPCNet and WaveNet speech are generated with the same complexity. The demo also explains the motivations for LPCNet, shows what it can achieve, and explores its possible applications.

You can find an in-depth explanation of the algorithm used in LPCNet in [this paper](https://jmvalin.ca/papers/lpcnet_icassp2019.pdf).

## About
[
Jean-Marc Valin ](https://jmvalin.ca/)

Jean-Marc Valin has a B.S., M.S., and PhD in Electrical Engineering from the University of Sherbrooke. He is the primary author of the Speex codec and one of the main authors of the Opus codec. His expertise includes speech and audio coding, speech recognition, echo cancellation, and other audio-related topics. He is currently employed by Mozilla to work on next-generation multimedia codecs.