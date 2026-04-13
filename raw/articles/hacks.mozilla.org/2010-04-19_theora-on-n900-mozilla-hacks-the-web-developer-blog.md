---
title: Theora on N900 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2010/04/theora-on-n900/
author: Christopher Blizzard
published: '2010-04-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This is a re-post from Matthew Gregan’s personal weblog on the work that he’s been doing to bring HTML5 open video to mobile devices. Google recently announced funding for some work to bring Theora to ARM devices via a CPU-driven code path. Mozilla has been funding similar work over the last year or so to do video decoding on DSPs found in mobile devices, leaving the CPU largely idle.*

*We realize this post isn’t strictly web developer-facing, but it’s interesting enough for those who want to know how this stuff works under the covers.*

**Theora on N900: Or, how to play full-screen Theora video on the N900 with 80% idle CPU.**

The C64x+ DSP is often found in systems built upon TI’s OMAP3 SoC, such as the Palm Pre, Motorola Droid, and Nokia N900. Last year, Mozilla funded a port, named Leonora, of Xiph’s Theora video codec to the TI C64x+ DSP. David Schleef conducted the port impressively quickly and [published his results](http://www.schleef.org/blog/2009/11/11/theora-on-ti-c64x-dsp-and-omap3/). The intention of this project was to provide a high quality set of royalty free media codecs for a common mobile computing platform. The initial focus is Firefox Mobile on the N900, so I am working on integrating David’s work into Firefox. To experiment with other facilities Firefox could use to accelerate video playback and test integration, I’ve been hacking on a [branch](http://github.com/kinetiknz/plogg) of a stand-alone Ogg Theora and Vorbis player originally written by Chris Double called [plogg](http://www.bluishcoder.co.nz/2009/06/27/playing-ogg-files-with-audio-and-video.html).

Decoding and playing video can be a CPU intensive process, especially when all of the steps are fighting for time on a single CPU. The expensive parts of the playback process can be broken down into a few coarse pieces, in approximate descending order of cost:

- Video frame decode
- Video colour-space conversion (Y’CbCr to RGB)
- Video frame display
- Audio block decode
- Audio block playback

David’s DSP work enables item 1 to be off-loaded from the CPU completely, effectively providing “hardware accelerated” video decoding. Most devices have some way to off-load items 2 and 3 to the graphics hardware, but it can be difficult to make use of this while integrating with an existing graphics rendering pipeline.

The N900 has a 800×480 pixel display, so my hope was to play a 800×480 video full-screen at 30 frames per second with low CPU use and good battery life.

The ARM CPU in the N900 is quite fast. Doing a pure video-decode-only test, the original Theora library, which currently does not have ARM specific optimizations, is able to decode a 640×360 video at 76 frames per second, and it can even decode an 800×480 video at 32 frames per second. With the [ARM optimized port by Robin Watts](http://google-opensource.blogspot.com/2010/04/interesting-times-for-video-on-web.html), those numbers become 110 FPS and 47 FPS. David’s DSP port produces 78 FPS and 39 FPS, and it leaves the CPU completely idle because the entire decode is off-loaded to the DSP. With these numbers, it’s clear that the N900 is up to the task of playing back video smoothly if we can get the bits on the screen fast enough.

I am using plogg as a basis for experimentation using techniques applicable in the Firefox rendering engine. This requirement immediately excludes some techniques. For example, using hardware Y’CbCr overlays to display the video frames is excluded because it is not possible for Firefox to render arbitrary HTML content over the top of the overlay.

Chris’s original version of plogg used SDL’s Y’CbCr overlay API, which uses a fast direct overlay path on most systems. This provided a baseline for playback performance. Decoding my 800×480 test video with the DSP, it was possible to play back at 33 FPS with around 20% CPU idle. Unlike the decode-only benchmarks mentioned above, the plogg benchmarks are playing both audio and video with correct A/V synchronisation. With 44.1kHz stereo audio, I observed that 10-15% of the device’s CPU is used by PulseAudio. This indicates that audio playback may constitute a significant amount of processor time with some configurations.

Because there was already work underway to provide OpenGL accelerated compositing in Firefox with the newly conceived [Layers API](http://weblogs.mozillazine.org/roc/archives/2010/04/layers.html), it seemed logical to try using a GLSL fragment shader to off-load colour-space conversion to the GPU. This turned out to be too slow to play back a full-screen video.

Looking at the list of vendor-specific OpenGL extensions available on the N900, I discovered the [texture streaming API](http://www.tiexpressdsp.com/index.php/OpenGLES_Texture_Streaming_-_bc-cat_User_Guide). This allows a program to directly map texture memory and copy Y’CbCr data into that memory without having to perform an expensive texture upload or colour-space conversion. The colour-space conversion is off-loaded to dedicated graphics hardware inaccessible via the standard OpenGL APIs. Using this and the modified bc-cat kernel module from the [gst-bc-cat](http://gitorious.org/gst-plugin-bc/gst-plugin-bc/trees/master) project, it’s possible to play back at 26 FPS with 81% CPU idle.

One drawback of the current bc-cat kernel driver is that there is a very limited set of texture formats supported (NV12, UYVY, RGB565, and YUYV), and none of them are the same as what Theora produces. To work around this, a format conversion is required to convert planar Y’CbCr to packed 4:2:2 UYVY. Fortunately, this conversion is much simpler than a full colour-space conversion. Timothy Terriberry sent me a [couple of patches](http://github.com/kinetiknz/plogg/tree/master/patches/) to off-load this conversion work to the DSP. If it’s possible to extend the bc-cat driver to support texture formats compatible with Theora’s output, performance can be further improved.

The test files used for benchmarking were: Big Buck Bunny (video: 640×360 @ 500 kbps 24 FPS, audio: 64 kbps 48kHz stereo, 9m 56s, 40MB) and the movie trailer for 9 (video: 800×480 @ 2 Mbps 23.98 FPS, audio: 44.1kHz stereo, 2m 30s, 30MB). Benchmarks were run with the CPU frequency fixed at 600MHz.

In summary, it’s possible to play full-screen Ogg Theora videos on the N900 at full frame rates with low CPU use by off-loading video decoding to the DSP and colour-space conversion and painting to the GPU. There are opportunities for optimization left, tuning for battery life needs to be investigated, and the integration into Firefox still needs to be done.

*Video decode-only:*

| Decoder | FPS (800×480) | Idle CPU |
|---|---|---|
| libtheora 1.1 | 32 | 0.7% |
| TheorARM 0.04 | 47 | 0.4% |
| leonora (DSP) | 39 | 99.0% |

*Playback (video decode + paint, audio decode + not played). DSP decoding video:*

| Method | FPS (800×480) | Idle CPU |
|---|---|---|
| SDL/overlay | 33 | 20.0% |
| OpenGL/bc-cat | 26 | 81.4% |

## 4 comments

GeorgeApril 28th, 2010 at 16:48rsMay 1st, 2010 at 18:58