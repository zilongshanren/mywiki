---
title: Using the GPU for precomputing GI in game development
url: http://raytracey.blogspot.com/2010/06/using-gpu-for-precomputing-gi-in-game.html
author: Sam Lapere
published: '2010-06-18'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I just read on the


I also read that Bungie uses a GPU-accelerated photon mapping technique from the Siggraph 2009 paper "An Efficient GPU-based Approach for Interactive Global Illumination" by Rui Wang et al. to precompute GI in some of the Halo games (ODST?, Reach?).


It's nice to see that GPUs are actually used for precomputating lighting in games and movies (e.g. PantaRay in Avatar) and I believe this is a very interesting trend. On a PC stuffed with multiple Fermi's, some of these techniques might be close to real-time and achieve very high quality. With the latest breakthroughs in GPU-accelerated GI algorithms (path tracing, bidirectional path tracing (Brigade), soon realtime MLT?, (image space) GPU photon mapping, sppm) it should be possible to have movie-quality real-time GI on the next generation of consoles coming in 2012 (at the earliest). Or maybe not on consoles, but definitely on GPU clouds. :-).

[Real-Time Rendering blog](http://www.realtimerendering.com/blog), that Ubi Montreal used GPUs to precompute ambient occlusion for Splinter Cell Conviction. The technique used was invented by Toshiya Hachisuka and described in GPU Gems 2 in the chapter "High-Quality Global Illumination Rendering Using Rasterization".I also read that Bungie uses a GPU-accelerated photon mapping technique from the Siggraph 2009 paper "An Efficient GPU-based Approach for Interactive Global Illumination" by Rui Wang et al. to precompute GI in some of the Halo games (ODST?, Reach?).

It's nice to see that GPUs are actually used for precomputating lighting in games and movies (e.g. PantaRay in Avatar) and I believe this is a very interesting trend. On a PC stuffed with multiple Fermi's, some of these techniques might be close to real-time and achieve very high quality. With the latest breakthroughs in GPU-accelerated GI algorithms (path tracing, bidirectional path tracing (Brigade), soon realtime MLT?, (image space) GPU photon mapping, sppm) it should be possible to have movie-quality real-time GI on the next generation of consoles coming in 2012 (at the earliest). Or maybe not on consoles, but definitely on GPU clouds. :-).

## No comments:

Post a Comment