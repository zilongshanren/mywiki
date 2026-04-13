---
title: My GDC 2014 talk on OpenCL and realtime graphics
url: https://anteru.net/blog/2014/my-gdc-2014-talk-on-opencl-and-realtime-graphics
published: '2014-03-22'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

This post is for everyone who just grabbed the slides of my “[OpenCL for realtime graphics](https://www.khronos.org/assets/uploads/developers/library/2014-gdc/Volumerics-OpenCL-RT-Graphics-GDC-Mar14.pdf)” talk from GDC and wonders where the speaker notes are. So here we go :) Thanks again to Andrew & Neil for inviting me!

## Interop API

Every time I mention OpenCL and graphics, people start by complaining about interop and how much code it is and how slow it is going to be. The truth is, the interop code itself is going to be really small, and there is no good reason why the interop has to be slower than DirectCompute or OpenGL compute shaders (or at least, I’m not aware of a good reason.) In fact, by having to tell the driver early on that you’re going to use a resource later for compute, it can make better decisions than in DirectCompute where it only can identify the dependencies at dispatch call time. The only reason why performance with OpenCL may be worse is due to missing integration of OpenCL with the Direct3D/OpenGL drivers. Fundamentally, there is nothing in the specification or elsewhere which makes OpenCL/graphics interop inefficient.

## Tile based deferred shading

I did that demo back in 2011, so some things may have changed since them – in particular, undefined behaviour is undefined; you’ve been warned. It’s really unfortunate that read/write images didn’t make it into OpenCL 1.x, as they are supported by all Direct3D 11 compliant hardware.

I also mentioned in the slides that you can’t map the depth buffer directly. The reason why you really want to do this is that it allows you to take advantage of the depth buffer compression. As a workaround I simply copied it into a separate texture, which, as far as I know, will trigger a decompression on current hardware. It’s not going to make things horribly slow, but it’s still nicer if you can just directly map the buffers and avoid yet another GPU memory copy.

## Computational graphics

That’s the “serious” compute stuff, where compute is used for large volume data visualization. In this case, the problem you typically run into is that GPU memory is fairly limited compared to CPU memory. The problem that everyone has in mind here is “portable performance”, or basically the question: Can we have stuff which is efficient on both the GPU and CPU?

In my experience, the answer is yes, you can. You might not get the maximum performance on the CPU if you optimize for GPU first, but you’re still going to be reasonably efficient. The 30% compared to ISPC in the slides is just a ballpark number, but what you have to keep in mind is that the ISPC path is using a different traversal code which is more suited for CPUs, and I’ve spent significant amounts of time optimizing it. The CPU OpenCL version in comparison was barely tweaked until it ran “fast enough”. In the future, once CPUs ship with scatter & gather instructions, we can expect the gap to close significantly. Absolute performance will probably still differ, but efficiency on CPUs will go up, and by using OpenCL, your code will be able to take advantage of these improvements immediately without having to do anything on your side.

## Shipping products

The key takeaways here are:

- You can ship software relying on OpenCL/graphics interop now
- You should contact your IHV early

Basically, there’s no real blocker preventing you from shipping applications using OpenCL. People have drivers which support it, compilers are robust enough, and the interop works on Windows & Linux. Sure, there are issues from time to time, but nothing is like horribly broken or cannot be worked around most of the time.

One issue we have been running into regularly is GPU memory management, which is not as robust as we’d like it to be. Graphics developers will be familiar with this problem; for compute, it’s even worse as buffers tend to be larger there.

Regarding the stricter implementation: AMD’s compiler tends to follow the specification very closely, similar to their OpenGL compiler which is also very strict. For instance, it’ll catch implicit double to float conversions, even if you just want to convert 1.0. We typically develop with all warnings turned on and all warnings being treated as errors. You do have to test on different machines regularly though, as even standard-compliant code sometimes results in problems. For example, we ran into issues where one compiler simply would fail on nested loops; in such cases, you have to bite the bullet and restructure your code. That said, these are getting increasing rare.

## Conclusion

To sum it up: OpenCL is ready for graphics, but there are various issues outside of OpenCL which have hindered it success so far. I expect this to change once OpenCL 2.0 is available as it’ll provide capabilities going far beyond OpenGL compute shaders and DirectComput and improve the graphics interop capabilities at the same time. For games, OpenCL 2.0 is likely to be a good target.

However, if you want to use OpenCL for your content creation tools, OpenCL 1.1/1.2 is ready & good to go. For example, I don’t see why you would want to write a ray-tracer for light map baking in DirectCompute if you can get both the interactive version and the offline version for free by using OpenCL. Or write code twice, just because you have to support OpenGL and Direct3D.

So that’s it, I hoped you enjoyed the talk! If you have questions, just use the comment function or contact me directly.