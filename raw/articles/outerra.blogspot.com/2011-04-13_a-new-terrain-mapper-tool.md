---
title: A new terrain mapper tool
url: https://outerra.blogspot.com/2011/04/new-terrain-mapper-tool.html
author: Outerra
published: '2011-04-13'
source_blog: Outerra
source_site: https://outerra.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

What's going on with the tool? Its purpose is to convert terrain data from usual WGS84 projection into a variant of

[quadrilateralized spherical cube](http://en.wikipedia.org/wiki/Quadrilateralized_spherical_cube)projection we are using, along with wavelet-based compression of the data during the process. It takes ~70GB of raw data and processes them into a 14GB datased usable in Outerra, endowing it with ability to be streamed effectively and to provide the needed level of detail.

With the aforementioned defects in mind, and with the need to compile a new dataset with a better detail for northern regions above 60° latitude, we've decided to rework the tool, in order to speed it up and to extend the functionality as well.

I originally planned to implement it using CUDA or OpenCL, but after analyzing it deeper I decided to make it a part of the engine, using OpenGL 3.x shaders for the processing. This will allow for creating an integrated and interactive planet or terrain creator tool later, which is worth it in itself.

The results are surprisingly good. For comparison: to process the data for whole Earth, the old CPU-only tool needed to run continuously for one week (!) on a 4-core processor. The same thing now takes just one hour, using a single CPU core for preparing the data and running bitplane compressor, and a GTX 460 GPU for mapping and computation of wavelet coefficients. In fact the new tool is processing more data, as there are also the northern parts of Scandinavia, Russia and more included in the new dataset.

All in all it represents roughly a

**200X**speedup, which is way more than we expected and hoped for. Although GPU processing plays a significant role in it, without the other improvements it would show much less. The old tool was often bound on I/O transfers - it synchronously processed and streamed the data. The new one does things asynchronously, additionally it now reads the source data directly in packed form, saving the disk I/O bandwidth - it can do the unpacking without losing time because the main load has been moved from CPU to GPU. Another thing that attributed to the speedup is a much better caching mechanism that plays nicely with the GPU job.

There's another interesting piece used in the new tool - unlike the old one, this traverses the terrain using adaptive Hilbert curves.

[Hilbert curve](http://en.wikipedia.org/wiki/Hilbert_curve)is a continuous fractal space-filling curve that has an interesting property - despite being just a line, it can fill a whole enclosed 2D area. Space-filling curves were discovered after mathematician Georg Cantor found out that an infinite number of points in a unit interval has the same cardinality as infinite number of points in a any finitely dimensional enclosed surface (manifold). In other words that there is a 1:1 mapping from points on a line segment into the points of a 2D rectangle.

These functions belong to our beloved family of functions - fractals.

In the mapping tool it's being used in the form of a hierarchical recursive & adaptive Hilbert curve. While any recursive quad-tree traversal method would work effectively, Hilbert curve was used because it preserves locality better (which has a positive effect on cache management), and because it is cool :)

Here is a video showing it in action - the tool shows the progress of data processing on the map:

Apart from the speedup, the new dataset compiled with the tool is also smaller - the size fell down by 2GB to ~12GB, despite containing more detailed terrain for all parts of the world.

I'm not complaining, but I'm not entirely sure why is that. There was one minor optimization in wavelet encoding that can't explain it. The main suspect is that the old tool was encoding wide coastal areas with higher resolution than actually needed.

***

Coming next - a comparison of new and old datasets. Apart from providing a more consistent terrain detail for whole world, the new dataset also comes with enhanced mountain shapes in several places.

## 2 comments:

An impressive feat. Never cease to amaze me at the ruthless efficiency of your methods.

Great job! Waiting for the next post and comparison between the two datasets.

Post a Comment