---
title: Simultaneous Mipmap Level Generation
url: http://hacksoflife.blogspot.com/2016/05/simultaneous-mipmap-level-generation.html
author: Benjamin Supnik
published: '2016-05-07'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

*The novel trick deep in this post is the use of morton-number pixel addressing to generate mipmaps in parallel; I was surprised to not see anyone doing this so I figured I'd write it up. It is quite possible that no one does this because it's totally stupid, but the initial results looked promising under a narrow set of circumstances.*

I was looking at CPU-based generation of mipmaps the other day. The traditional way to do this is with recursion: you calculate mip level 1 (quarter size of the original image) from the original image, then you calculate mip map level 2 from mip map level 1, again cutting down by a factor of four, and on and on.

This "recursive down-size" algorithm has a nice property: the total number of pixels read in the filtering operations is very low - about 33% more than the size of the original image. (We get this "efficiency" even though we are producing several new images because most of the mips are reading from

*much*smaller images than the original.)

But recursively down-sizing has one hidden problem: the smaller mips are

*not*actually computed from the original image! If you have a 256x256 image, that last pixel is computed from data that has been re-sampled seven time! Your lower mips are on the wrong end of a game of telephone.

Does this matter? That all depends on what your filtering algorithm is. If you are doing a simple box filter average, then it almost certainly doesn't matter - the limits of that filter are a lot worse than the recursive error.

But there are algorithms that make

*approximate*mipmaps. A common trick these days in physically based rendering engines is to

[increase the roughness](http://blog.selfshadow.com/2011/07/22/specular-showdown/)of lower mips based on the divergence of normals in the higher mips. The idea is that at lower mips our normals (pointing in all different directions) should be scattering light, but they've averaged out. We increase roughness to say "some scattering happened under this pixel that you can't see any more."

The problem is that this roughness increase is very much an approximation; the last thing we want to do is approximate an approximation over and over by recursively down-sizing. Whatever the problems of the algorithm, let's limit ourselves to absorbing the error once by always working from the highest level mipmap.

### Two Ways To Sample

A naive way to compute these mipmaps is to compute each mip level from the original image, with each higher number (and smaller) mip level sampling more source pixels for each destination pixel. This solves our quality problem, but it's slow - for a 256 x 256 image, we're going to do*eight*full passes over the source image - each time we make the source image twice as big, we eat another pass. This is way worse than 33% more samples that we had in the recursive algorithm.

(Quick side note: note that overflow must be re-examined. Recursive mipmaps sample at most four source pixels for each destination, so for example we could use a short to accumulate unsigned bytes. The "use the source" image might sample 1M pixels to build the last mip, overflowing accumulation data types.)

I then got an idea: what if we could build

*all*of the mipmaps at once in a single iteration? The algorithm would go something like this:

- For each mip level we will compute, start a "bucket" to accumulate pixels.
- For each pixel in the source image, read that pixel and accumulate it into each bucket.
- For each of those buckets,
*if*it is full (that is, if it has accumulated enough samples to be done), compute the destination pixel and reset the bucket.

In order to make this work, we have to use a very particular iteration order: we have to cover all four pixels under the first pixel of the first mip before we can go on to the fifth pixel - this applies at all mip levels. It turns out that this is done by -interleaving- the digits of our pixel address in binary.

(If you are familiar with tiling and GPU hardware this is totally unsurprising in any way.)

In other words, if we are doing the 87th pixel of a 256 x 256 image, that pixel number is 01010111 in binary. We split the digits to get an X address of 1111 and a Y address of 001, that is, this is the 15th X pixel and 1st Y pixel. The first 64 pixels are in the lower left 8x8 of the image - they must be because we have to read those first 64 pixels to compute the 3rd mip-level's first pixel. We then move to the right by 8 pixels - the next 16 pixels are used for the next 4x4, so we move four more to the right. The next four pixels are the next 2x2, leaving 3 pixels left at 14,0 - in that 2x2 we are in the upper right, giving us an address of 15,1.

(Note: if your image is not square, all bits to the left of the number of bits needed to compute an NxN square, where N is the

*shorter*dimension, must be applied only to the longer dimension.)

There is one problem with this algorithm: it is

*really, really, really*cache unfriendly. The reason it is so cache unfriendly is that our image is stored in linear order, not tiled order, so all of those Y hops are jumping way forward and backward and all over the place in memory. Our images are too big to just sit in cache (e.g. 4 MB) but in our old algorithms we just read through them in perfect order. That meant that that for each cache line fetched, we used the whole thing, and more importantly, our access order was so bleeding obvious that the hardware prefetcher could know exactly what was going on and have the next bytes ready.

To performance test this, I put my down-sampling algorithms into traits classes and wrote templated down-samplers for recursive, linear, and parallel mipmap generation. To test, I used two down-sampling algorithms:

- "Raw" down-sampling simply averaged pixel values, as integers.
- "sRGB" down-sampling converted the pixels to floating-point linear space, averaged in linear space, and then converted to sRGB. The sRGB conversion is a correct conversion (e.g. linear at the bottom, 2.4 power on the top) in floating point, rather than a table lookup or approximation.

Raw sRGB

Recursive 18.4 374

Sequential 72.1 2732

Parallel 124.9 392

As you can see, recursive is always fastest, and parallel is worse than sequential for purely data-movement workflows like "raw". But when we go to the sRGB work-flow, parallel is

*much*faster than sequential, and almost as good as recursive.

Why? I think the answer is that the conversion from 8-bit sRGB to floating point linear is expensive - there's branching, power functions and data unpacking in that conversion. And the parallel algorithm absolutely minimizes this work - every source pixel is decoded exactly once - that's even 33% less than the recursive algorithm. (Every algorithm has to

*write*the same number of pixels in the end, so there's no change in absolute work then.)

My gut feeling is that this "win" isn't as good as it looks - the more data limited and the less CPU limited our algorithm, the more like 'raw' and the less like 'sRGB' we are. In other words, there's no real replacement for recursion if you can afford it, and they wouldn't look close if I spent some time tuning my sRGB conversion.* And if there's any long term trend, it's code becoming more input data limited and less ALU bound.

### You Know We Have GPUs, Right??

At this point you should have only one question: Ben, why in the hell are you not using the GPU to compute your mipmaps???

There are a few conditions particular to the X-Plane engine that make on-CPU mipmapping interesting in X-Plane.

- Most of our mipmaps are precomputed in DDS files. Therefore most of the time, our interaction with the driver is to feed the entire mip pyramid to the driver from the CPU side. By computing mipmaps for PNG files on the CPU, we ensure that every one of our textures goes into the driver in the same way.
- Since we are OpenGL based, the driver needs to manage residency of textures; if the driver decides to prioritize PNG files because they are more expensive to swap off the GPU because the mipmaps aren't already resident in system memory too, that's not good for us.
- Some day when we use a lower level API,
*we*will need to manage residency, and it will be easier to have only code flow (system-pool for all resources, page them to the GPU when they are in the working set) for all textures. - Disk-texture upload is done entirely in background threads - the sim never waits, and pre-loading is N-way threaded during load, so the cost of CPU time is actually pretty cheap in a multicore world.

* I did not try a table-based sRGB sRGB decode, which would be an interesting comparison - I'll have to try that on another day. I did try

[RYG's SSE + table-based](https://gist.github.com/rygorous/2203834)re-encode, and it does speed things up compared to a non-SSE implementation. I was able to modify it for alpha support but haven't had time to write a matched decoder. (I didn't see any back story to the post, so I don't know if decode should always just be table-based.)

I believe that the cache misses caused by following the space-filling curve are totally unnecessary, as well as the complexity of just following the curve.





ReplyDeleteYou could just start on the top left (or bottom, if your rows are flipped) of the image and scan across horizontally, tallying up your pixels into corresponding mip buckets just as with the Morton curve, but way more cache-friendly! When you hit the 2nd row of pixels now every 2 pixels you will have completed another 2x2 bucket for the 1st mip level.. Once you hit the 4th row of input image pixels, every 4 pixels of that row you will be completing 4x4 buckets for the 2nd mip level, and two 2x2 buckets on the 2nd row of 1st mip level (with the original image being the 0th level).

Writing to buckets in horizontal order might add a little speed boost too.

The big different here is that with the Morton curve you're ticking off 4 1st level buckets for every 2nd level bucket (and on and on up the levels) while scanning horizontally you've got a whole row of buckets for every mip level simultaneously until they each get filled up with their last pixel. You'd either sum the integer values and divide at the very end by the miplevel's total added pixels, or you could just sum floating point channel values that are pre-divided (or inverse-multiplied) to save the final division on the completion of the bucket, and just convert to the final channel data format (i.e. 8 bits). There's a good chance this would all be virtually free in the face of the cache misses being practically obliterated.

I dunno, maybe I'm missing something. I think it's at least worth investigating.