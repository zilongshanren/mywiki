---
title: Optimizing Software Occlusion Culling – index
url: https://fgiesen.wordpress.com/2013/02/17/optimizing-sw-occlusion-culling-index/
published: '2013-02-17'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Optimizing Software Occlusion Culling – index

In January of 2013, some nice folks at Intel released a [Software Occlusion Culling demo](http://software.intel.com/en-us/vcsource/samples/software-occlusion-culling) with full source code. I spent about two weekends playing around with the code, and after realizing that it made a great example for various things I’d been meaning to write about for a long time, started churning out blog posts about it for the next few weeks. This is the resulting series.

Here’s the list of posts (the series is now finished):

[“Write combining is not your friend”](https://fgiesen.wordpress.com/2013/01/29/write-combining-is-not-your-friend/), on typical write combining issues when writing graphics code.[“A string processing rant”](https://fgiesen.wordpress.com/2013/01/30/a-string-processing-rant/), a slightly over-the-top post that starts with some bad string processing habits and ends in a rant about what a complete minefield the standard C/C++ string processing functions and classes are whenever non-ASCII character sets are involved.[“Cores don’t like to share”](https://fgiesen.wordpress.com/2013/01/31/cores-dont-like-to-share/), on some very common pitfalls when running multiple threads that share memory.[“Fixing cache issues, the lazy way”](https://fgiesen.wordpress.com/2013/02/01/fixing-cache-issues-the-lazy-way/). You could redesign your system to be more cache-friendly – but when you don’t have the time or the energy, you could also just do this.[“Frustum culling: turning the crank”](https://fgiesen.wordpress.com/2013/02/02/frustum-culling-turning-the-crank/)– on the other hand, if you do have the time and energy, might as well do it properly.[“The barycentric conspiracy”](https://fgiesen.wordpress.com/2013/02/06/the-barycentric-conspirac/)is a lead-in to some in-depth posts on the triangle rasterizer that’s at the heart of Intel’s demo. It’s also a gripping tale of triangles, Möbius, and a plot centuries in the making.[“Triangle rasterization in practice”](https://fgiesen.wordpress.com/2013/02/08/triangle-rasterization-in-practice/)– how to build your own precise triangle rasterizer and*not*die trying.[“Optimizing the basic rasterizer”](https://fgiesen.wordpress.com/2013/02/10/optimizing-the-basic-rasterizer/), because this is real time, not amateur hour.[“Depth buffers done quick, part 1”](https://fgiesen.wordpress.com/2013/02/11/depth-buffers-done-quick-part/)– at last, looking at (and optimizing) the depth buffer rasterizer in Intel’s example.[“Depth buffers done quick, part 2”](https://fgiesen.wordpress.com/2013/02/16/depth-buffers-done-quick-part-2/)– optimizing some more![“The care and feeding of worker threads, part 1”](../../assets/09c0483da5eb4cdd.img)– this project uses multi-threading; time to look into what these threads are actually doing.[“The care and feeding of worker threads, part 2”](https://fgiesen.wordpress.com/2013/02/25/the-care-and-feeding-of-worker-threads-part-2/)– more on scheduling.[“Reshaping dataflows”](https://fgiesen.wordpress.com/2013/02/28/reshaping-dataflows/)– using global knowledge to perform local code improvements.[“Speculatively speaking”](https://fgiesen.wordpress.com/2013/03/04/speculatively-speaking/)– on store forwarding and speculative execution, using the triangle binner as an example.[“Mopping up”](https://fgiesen.wordpress.com/2013/03/05/mopping-up/)– a bunch of things that didn’t fit anywhere else.[“The Reckoning”](https://fgiesen.wordpress.com/2013/03/10/optimizing-software-occlusion-culling-the-reckoning/)– in which a lesson is learned, but[the damage is irreversible](http://www.alessonislearned.com/).

All the code is available on [Github](https://github.com/rygorous/intel_occlusion_cull/); there’s various branches corresponding to various (simultaneous) tracks of development, including a lot of experiments that didn’t pan out. The articles all reference the [blog branch](https://github.com/rygorous/intel_occlusion_cull/tree/blog) which contains only the changes I talk about in the posts – i.e. the stuff I judged to be actually useful.

Special thanks to Doug McNabb and Charu Chandrasekaran at Intel for publishing the example with full source code and a permissive license, and for saying “yes” when I asked them whether they were okay with me writing about my findings in this way!


![CC0](../../assets/bc63f301328ae255.png)




To the extent possible under law,


Fabian Giesen

has waived all copyright and related or neighboring rights to

Optimizing Software Occlusion Culling.

This series is great for learning various optimization as well as software rendering techniques which gives me a way better understanding of what actually happens in the hardware. I wonder, however, why Intel guys chose to use a software rasterizer instead of doing the whole thing on the GPU. Do you know if there is a reason for this? (especially with DX11’s compute shader and UAVs it would be way faster, right?)? Thaks.

The whole point is that doing an early conservative occlusion culling pass on the CPU *is* faster than submitting everything to the GPU – as the example shows.

In practice, I wouldn’t be using a full-resolution depth buffer (like the Intel sample uses) for this though. Smaller depth buffer should work just fine and is cheaper to render. You need to be careful with small occluders and make sure your rasterizer is conservative once you do that though.

Thanks a lot for this article series. Learned a lot of details about writing a rasterizer. I have one question though, how do you get around race conditions when writing to the depth buffer using multiple threads? If I’m not mistaken, each thread rasterizes a ‘bin’ and there can be multiple bins per screen space tile. Is it not the case?

No, each tile has one bin. (The tile is the area on the screen, the bin is a data structure containing triangles overlapping the tile.)

I see. Somehow the comments in the code confused me. Thanks for the prompt reply.