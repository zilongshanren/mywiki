---
title: Firefox brings you smooth video playback with the world’s fastest AV1 decoder
  – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2019/05/firefox-brings-you-smooth-video-playback-with-the-worlds-fastest-av1-decoder/
author: Nathan Egge
published: '2019-05-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Tuesday’s [release of Firefox 67](https://blog.mozilla.org/blog/2019/05/21/latest-firefox-release-is-faster-than-ever/) brought a number of performance enhancing features that make this our fastest browser ever. Among these is the high performance, royalty free AV1 video decoder [dav1d](https://code.videolan.org/videolan/dav1d), now enabled by default on all desktop platforms (Windows, OSX and Linux) for both 32-bit and 64-bit systems.

With files more than 30% smaller than today’s most popular web codec VP9 [[1](https://code.fb.com/video-engineering/av1-beats-x264-and-libvpx-vp9-in-practical-use-case/)], and nearly 50% smaller than its widely deployed predecessor H.264 [[2](http://www.compression.ru/video/codec_comparison/hevc_2018/pdf/MSU_HEVC_AV1_comparison_2018_P4_HQ_encoders.pdf)], AV1 allows high-quality video experiences with a lot less network usage, and has the potential to transform how and where we watch video on the Internet. However, because AV1 is brand new and more sophisticated, some experts had [predicted](https://www.multichannel.com/news/hardware-support-big-step-ahead-av1) that market adoption would wait until 2020 when high-performance hardware decoders are expected. Dav1d in the browser upends these predictions.

Sponsored by the [Alliance for Open Media](https://aomedia.org), dav1d is a joint effort between the French non-profit VideoLAN and the greater FFmpeg open source audio/video community. Some of the leading minds in open source multimedia joined forces to release the [first](http://www.jbkempf.com/blog/post/2018/First-release-of-dav1d) version of dav1d last fall, already 2x to 5x faster than [libaom](https://aomedia.googlesource.com/aom/), the reference decoder published by AOMedia as part of the AV1 standards effort.

Since then the dav1d developers have squeezed out even more performance by profiling and rewriting critical sections in highly-parallelized SIMD assembly. And this shows in the benchmarks:

Higher performance and greater efficiency means smooth playback of AV1 video in the browser with significantly less CPU utilization.

## AV1 already seeing adoption on the web

Landing dav1d in Firefox could not have happened at a better time. In just the past few months we’ve seen remarkable growth in the use of AV1, with our latest figures showing that 11.8% of video playback in Firefox Beta used AV1, up from 3% in March and 0.85% in February.

Now that desktop Firefox contains dav1d, we expect even more websites will take advantage of this next-generation, royalty-free video codec AV1.

## Mozilla investing in the AV1 future

State-of-the-art decoders like dav1d are great for video playback, but best-in-class, free and open source software *en*coders are equally important to a healthy AV1 community. The AOMedia reference encoder was developed with the goal of creating the AV1 standard, not a production encoder. Thus, Mozilla and Xiph.Org are jointly developing a clean-room encoder named [rav1e](https://github.com/xiph/rav1e) (the Rust AV1 Encoder) to increase encoding gains over the reference encoder and allow software encoding fast enough for real-time applications like WebRTC.

Good encoders make heavy use of psychovisual models to allocate bits for what humans perceive as good visual quality (not [PSNR](https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio)). With rav1e we are applying the perceptual analysis expertise from our earlier [Daala](https://wiki.xiph.org/index.php?title=Daala) and [Theora](https://en.wikipedia.org/wiki/Theora) codec development efforts to add [activity masking](https://people.xiph.org/~jm/daala/pvq_demo/), better [color balancing](https://nbviewer.jupyter.org/gist/barrbrain/9d541d809d1d664460b5ce5c00a57948/Chroma%20quantizer%20balance.ipynb), improved [rate control](https://people.xiph.org/~xiphmont/demo/theora/demo8.html) and perceptual distortion metrics like [CDEF](https://people.xiph.org/~xiphmont/demo/av1/demo2.shtml) that bring new, improved quality to AV1 encoding.

We’re also investing considerable research to improve encoder speed, optimizing new techniques that appear for the first time in AV1. It’s not enough to rewrite existing code from the initial reference encoder in SIMD assembly and make it four times faster. Rav1e is developing ways to make AV1 encoding tools 1000x faster by finding new algorithms rather than simply optimizing existing code.

Rav1e is getting better all the time. Active development continues at a rapid pace, landing major new improvements weekly.

**Join the conversation**

Do you find video compression and related technologies fascinating? Then join us in New York on June 26 for the [Big Apple Video 2019](https://bigapple.video) conference co-hosted by Mozilla and Vimeo. This full day event focuses on cutting edge video technologies and the user experiences they enable. With speakers from Twitch, Cisco, NGCodec, Intel, Wikimedia and other well known companies, this conference is designed for video technology enthusiasts like you!

We’d love to have you with us in New York, but if not you can register to attend remotely and watch our on-line video stream. What else would you expect from a conference on video and related technologies?

**References**

[AV1 beats x264 and libvpx-vp9 in practical use case](https://code.fb.com/video-engineering/av1-beats-x264-and-libvpx-vp9-in-practical-use-case/)– https://code.fb.com/[MSU Codec Comparison 2018](http://www.compression.ru/video/codec_comparison/hevc_2018/pdf/MSU_HEVC_AV1_comparison_2018_P4_HQ_encoders.pdf)– http://www.compression.ru/

## About Nathan Egge

Nathan Egge is a Senior Research Engineer at Mozilla and a member of the non-profit Xiph.Org Foundation. Nathan works on video compression research with the goal of producing best-in-class, royalty-free open standards for media on the Internet. He is a co-author of the AV1 video format from the Alliance for Open Media and contributed to the Daala project before that.

## 3 comments

RobertMay 23rd, 2019 at 14:23Dan CallahanMay 24th, 2019 at 02:04Andrey SitnikMay 24th, 2019 at 06:43