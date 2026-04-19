---
title: Rendepth Update, Blog Dark Mode
url: https://cybereality.com/rendepth-update-blog-dark-mode/
author: Cybereality
published: '2024-10-14'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

![](../../assets/61c84fa10155539d.jpg)

Rebooted work on Rendepth, my stereo 3D media player. Decided to go with [SDL3](https://wiki.libsdl.org/SDL3/FrontPage) as the base, as it has a new cross-platform renderer (Vulkan, Metal, DirectX12), which will make things a bit easier. Needed something lightweight, so felt that starting from scratch rather than repurposing Degine code was a better move. I also have an earlier prototype in OpenGL, but I can easily port this code to the project. Already got one of my designers on an app icon, though this is not 100% final.

![](../../assets/595d04c8827182d6.png)

The 2D-to-3D element is almost working, but in a separate Python app. This is based on [Depth Anything V2](https://github.com/DepthAnything/Depth-Anything-V2), which is a pretty sweet ML library for estimating depth from a single color image. After generating a depth map, I use my reprojection shader to simulate stereoscopic 3D. The technique is based on the same method used on the Crysis 2 console release (published in GPU Pro 3), though I’ve made some minor adjustments. The depth estimation portion takes about 2 seconds on the CPU for a single image, and the stereo reprojection is real-time (under 1ms). Hopefully I will be able to speed this up on GPU compute, but we’ll see if total real-time is possible. You can see some of the shots below with the manual processing and my custom anaglyph filter.

Still need some time to figure out how SDL3 works (basically just hacked together one of the example demos) and also port the code from the older two prototypes. Think I can get an early working version in about a month. Also decided to tweak the style on the blog for dark mode to match the new pfp.