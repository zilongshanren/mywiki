---
title: 'Robust OpenCL initialization, part #2 (Optimus & friends)'
url: https://anteru.net/blog/2014/robust-opencl-initialization-part-2-optimus-friends
published: '2014-04-28'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

I totally forgot it, but there is one thing related to robust OpenCL initialization which is difficult to impossible to solve robustly, and that is handling hybrid graphics. This blog post is NVIDIA/Intel specific, which is a very common configuration these days, and it will only affect you if you want to use graphics & compute interop.

The problem that you will run into is easy to explain:

- The D3D device is created on the Intel integrated chip (device #0 if you enumerate them), which is (potentially) re-routed to the NVIDIA driver due to Optimus
- OpenCL interop will not be aware of this, so the Intel OpenCL runtime will try to interop with a hijacked Intel driver, and fail

If Optimus is disabled (i.e. there is no NVIDIA graphics adapter), everything will work fine. Similarly, it’ll just work if you have the integrated chip disabled. The problems only crop up if both devices are active and available.

Unfortunately, I don’t have a good solutions for this problem. The most robust way seems to be to enumerate all devices and prefer NVIDIA over Intel, which may not be what you want (especially if the user asked for the integrated device.) Ideally, you’d like some query to check if Optimus is present and if it should be used for your application, and only then, use NVIDIA, but so far, I haven’t found a way to do this (if you know a solution, please drop a line in the comments!)

I’m not sure what happens with AMD’s equivalent (Enduro), but I would assume that it’ll be similarly complicated. If you know it, please tell me so I can update this post accordingly!