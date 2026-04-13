---
title: GPU Driven rendering experiments at the Digital Dragons conference
url: https://interplayoflight.wordpress.com/2018/05/25/gpu-driven-rendering-experiments-at-the-digital-dragons-conference/
author: Kostas Anagnostou
published: '2018-05-25'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

This week I had the pleasure to present the experiments I’ve doing for the past six months on GPU driven rendering at the Digital Dragons conference in Poland. The event was well organised with lots of interesting talks, and I managed to finally meet many awesome graphics people that I only knew via Twitter.

I have uploaded the presentation slides in [pdf](https://1drv.ms/b/s!AmOPA68QU4JIiNdCIb9Hw4qHyt_cbw) and [pptx](https://1drv.ms/p/s!AmOPA68QU4JIiNdDPUE-3rzn11GehQ) formats with speaker notes in case anyone is interested and also the [modified source code](https://1drv.ms/u/s!AmOPA68QU4JIiNdFImsn-kZVWHx31w) I used for the experiments (I have included an executable, to compile it you will need to download [NvAPI](https://developer.nvidia.com/nvapi)).

The main difference between this and the [previous version](https://interplayoflight.wordpress.com/2018/01/15/experiments-in-gpu-based-occlusion-culling-part-2-multidrawindirect-and-mesh-lodding/) is that this time I pushed the number of instances to 20K (up from 2K) to get some meaningful profiling metrics. This required a change in the way I performed the scan for stream compaction to support more thread groups, as I describe in the presentation. This version also focuses on reducing the memory bandwidth requirements by splitting the instance data into separate streams, using 4×3 matrices for transformations and packing data as much as possible.

These changes dropped the full occlusion pass cost down to 0.25ms (for 20K instances) on a GTX970 and to about a millisecond on a laptop with an HD4000 GPU. Compared to the previous versions, the revised code can process and cull 10 times more instances on the HD4000.

It is only unfortunate that Intel does not support a MultiDraw*Indirect API extension, as performance profiling showed that a large number DrawIndexed*Indirect calls hurt performance on the HD4000.

I am looking forward to an even bigger Digital Dragons conference next year! We need more events like these in Europe.


[…] GPU driven rendering experiments https://interplayoflight.wordpress.com/2018/05/25/gpu-driven-rendering-experiments-at-the-digital-dr… […]