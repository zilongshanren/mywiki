---
title: 'OpenCL & graphics: Are we there yet?'
url: https://anteru.net/blog/2013/opencl-graphics-are-we-there-yet
published: '2013-12-05'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

It’s been a while since my [last blog post on OpenCL and graphics interop](https://anteru.net/blog/2011/12/06/1815/). But before I take a look at the current state of OpenCL and graphics interop, I would like to motivate a bit why I even care about it.

## Compute & graphics

Every time I start talking about OpenCL & graphics interop, the first reaction is basically why don’t you use OpenGL compute shaders or DirectCompute. Well, one part of the answer is that when I started, OpenGL compute shaders weren’t available (and they have been only recently added to the AMD driver), and DirectCompute was horrible as well (compiler took hours to compile a shader), but it turned out, there are reasons which are much more important.

First and most importantly: **I can use the same code with several graphics backends** (D3D9, D3D10, D3D11, OpenGL). Once debugged, I can simply switch the graphics backend and everything remains the same. This is extremely valuable for me as developing OpenCL kernels is still faster than debugging GLSL or HLSL shaders (more on this below.) I don’t see any reason why I would like to develop code that works great in OpenCL twice in HLSL and GLSL and spend money & time on what is basically a source-to-source translation (and spend more money down the road as now I have to maintain duplicated code.)

Second, **I can decide whether to run the code on the GPU or on the CPU**, which neither DirectCompute nor OpenGL compute shaders can provide. Two examples where this is useful:

- My voxel raytracer is limited only by the size of memory on the device, and while my GPU has 4 GiB, my desktop has 24 GiB memory. Once the data set size becomes too large for the GPU, I can transparently switch to the CPU and continue working with the same code (the only difference is that the interop texture is no longer mapped from OpenGL, but it’s an image created on the host instead.) Sure, it runs slower, but customers like it when it still works.
- For iso-surface rendering, I have a pre-process kernel which extracts the surface from a volume. When the data is already present on the GPU, it makes sense to run it there, but when loading from disk, I can run the same code on the CPU to lower the amount of uploaded data. Same kernel, nearly identical host code.

Moreover, **the extension API is well designed and minimal**. All you get is a few functions to enable to access every kind of graphics resource (textures, buffers) and then you can do what you want with them. That means only a few functions to learn, which are also the same for OpenGL and all Direct3D versions (except for the suffix.) If new texture formats or new resource formats are added, there is no need for new APIs. Note *that OpenCL requires no new API functions on the OpenGL/Direct3D side at all*. Interestingly, the API became even smaller with OpenCL 1.2, as there is only one function left for mapping any texture.

Finally, **development is faster & the tooling is better**. Even though I’m still waiting for a good debugger, I’m still more efficient when writing OpenCL code than when working with shaders. Typically, I start by writing OpenCL for the CPU until the code is correct. Once everything works fine, I switch to the GPU and optimize performance. This is much nicer than having to work on the GPU directly where I’m still running into problems which will freeze the machine; this is a no-issue for me when developing on the CPU. This also includes graphics stuff, as I can simply dump the input textures once, debug on CPU, once it works, enable interop again, and I’m done. On the tool side, Intel & AMD provide nice kernel editors; in particular, AMD’s kernel analyzer allows you to immediately see the generated ISA and get statistics on register usage. This comes in very handy when optimizing GPU kernels.

## State of the interop nation

So where are we today, and what has improved since my last post? Let’s take a look:

**Depth buffer access**: This is solved by`cl_khr_depth_images`

, which is unfortunately not implemented by AMD and NVIDIA. It’s a very simple addition to the API which does not introduce any new functions, it just extends the texture mapping to support depth images as well. There’s no corresponding extension for Direct3D though. Basically, everything is specified and done, but the solution hasn’t been shipped yet.**MSAA textures**: Again, solved, by`cl_khr_gl_msaa_sharing`

, but not shipped by neither AMD nor by NVIDIA. This function also doesn’t add new functions, just extends texture mapping support for MSAA images. Again, there is no Direct3D equivalent.**Mip-mapped textures**: Solved in OpenCL 2.0 with`cl_khr_mipmap_image`

. There is even an extension to write to individual mip-map levels. While there is no matching Direct3D extension, it’s pretty easy to image that it’ll be mostly identical.**Offline kernel compiler**: Solved by SPIR, but not shipping yet. Again, a minimal addition to the API, though in this case, the vendors have significant amounts of work to do to actually generate portable SPIR.**Named kernel parameter access**: Not solved yet, but I could work around using OpenCL 1.2 APIs.

To sum it up, 3 out of 5 issues have been solved for OpenCL 1.x but not shipped widely. One can be solved using OpenCL 1.2, but unfortunately, NVIDIA is still shipping OpenCL 1.1 only. In OpenCL 2.0, mip-mapped images also get resolved, bringing it to 4 solved and one that can be worked around – all that we need at this point is the vendors to ship the already specified extensions.

The current verdict is thus a bit better than a year ago, as **we do have the extensions specified now**, but **shipping implementations are still lagging behind the specification**. I still don’t understand why things like MSAA & depth texture sharing are not exposed on AMD & NVIDIA, as this seems to be a minimal addition which would enable extremely efficient graphics interop – finally we could write a full-blown, Battlefield 4 style tiled deferred renderer using OpenCL only and reuse it across AMD, NVIDIA, Intel, OpenGL, Direct3D, and potentially mobile platforms as well (Sony is shipping OpenCL on their mobile phones!) Intel on the other hand is doing good progress on OpenCL, as far as I know, they do expose the depth & MSAA sharing on their integrated graphics processors, and they have also started working on OpenCL libraries like the Intel [Integrated Performance Primitives for OpenCL](http://software.intel.com/en-us/intel-ipp-preview).

**Update**:`cl_khr_mipmap_image`

solves the mip-mapped images problem. I somehow missed that completely when looking into the OpenCL 2.0 spec.