---
title: Raytracing, a 4 year retrospective
url: https://interplayoflight.wordpress.com/2022/04/09/raytracing-a-4-year-retrospective/
author: Kostas Anagnostou
published: '2022-04-09'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Recently I got access to a GPU that supports accelerated raytracing and the temptation to tinker with DXR is too strong. This means that I will steer away from compute shader raytracing for the foreseeable future. It is a good opportunity though to do a quick retrospective of the past few years of experimenting with “software” raytracing.

It all started about 4 years ago, when DXR was released and the first GPUs that supported it came out. My lowly Intel HD4000 laptop didn’t support DXR of course but not wanting to miss out on all the fun I decided to implement my own raytracing solution based on compute shaders. I was quite ambitious at the time, choosing to implement both [raytraced shadows and reflections](https://interplayoflight.wordpress.com/2018/07/04/hybrid-raytraced-shadows-and-reflections/), which was a huge learning step having to manage not just BVH creation/traversal and collisions but material sampling, hit point lighting and closest hits as well. I also got a first feel of the impact of ray divergence.

The first attempt at raytracing was decent but quite naive. For example I stopped the BVH build at model level, which meant that I had to iterate over each meshes triangles, in a loop, to determine ray-triangle collisions. That sort of worked for the simple spheres and cubes I was using but would never scale. [In my second attempt](https://interplayoflight.wordpress.com/2018/09/04/hybrid-raytraced-shadows-part-2-performance-improvements/) I improved BVH generation to include all triangles which improved the time to find ray collisions a lot. I also started exploring better BVH generation techniques like Surface Area Heuristic which accelerated traversal massively (left is number of steps to find a collision without SAH, right with SAH).

![](../../assets/5452699348eb8f57.png)

![](../../assets/5b75bb5e623add00.png)

BVH traversal is memory intensive operation as well which highlighted how important it is to choose the best buffer type for the target platform (for eg Intel GPUs seem to prefer ByteAddressBuffers).

This work coincided with an invitation from [Wolfgang Engel](http://diaryofagraphicsprogrammer.blogspot.com/2018/09/ray-tracing-without-ray-tracing-api.html) to write a hybrid raytraced shadows sample for [The Forge](https://github.com/ConfettiFX/The-Forge), so my experiments end up there, running on DX12, Vulkan and iOS, which was great.

Another technique that was gradually gaining traction was mixing screen space with raytracing techniques and for my next experiment I focused on [hybrid raytraced reflections](https://interplayoflight.wordpress.com/2019/09/07/hybrid-screen-space-reflections/). The idea behind this is to raymarch screen space reflections as normal but for those rays that fail to find a collision in screenspace let raytracing pick them up and find the geometry collisions.

![](../../assets/25a141ee76a4e1d5.png)


![](../../assets/25a141ee76a4e1d5.png)

This experiment also gave me the opportunity to directly compare SSR and raytraced reflections and highlight their differences, especially in terms of specular lighting of the hitpoints (left SSR, right raytraced)

![](../../assets/07e14dc2fdb5303c.png)

![](../../assets/5175c2003ecfcd26.png)

At some point I came across Intel’s Embree library and realised that I can use it [to generate the BVH trees that I use for raytracing](https://interplayoflight.wordpress.com/2020/07/21/using-embree-generated-bvh-trees-for-gpu-raytracing/) in my toy engine. I made some comparisons in terms of memory and traversal costs, there where mixed results depending on the scene (“reference” was my BVH generation code).


![](../../assets/5ad70370f85dc8ca.png)

Embree offers options to balance generation time and BVH traversal time which is very useful in cases you generate BVHs in the runtime. It was an overall better option and I am using this to generate my BVH trees since.

Up to that point, I was using a single BVH to bake the whole scene in. This in general produces a higher quality tree but it can be wasteful when trying to trace local rays (imagine local light shadows), or if we need to stream in and update the BVH with new models. For this reason [I added a two level BVH hierarchy](https://interplayoflight.wordpress.com/2020/11/01/adding-support-for-two-level-acceleration-for-raytracing/), with one BVH storing a single model (BLAS in DXR’s lingo) and another BVH for all the model instances’ BVHs (aka TLAS). Embree’s fast BVH tree generation was ideal for something that needed per frame generation like the TLAS. This opened to the door to raytraced shadows for animated models for example.

I next revisited hybrid raytracing, mixing raytracing with traditional techniques, this time to explore options to[ combine shadowmap and raytraced shadows](https://interplayoflight.wordpress.com/2021/05/15/experiments-in-hybrid-raytraced-shadows/). The idea here is that the requirement of high quality shadows (where raytracing shines) is along the boundary of shadowed and lit areas, so using shadowmaps for the bulk of the shadowed pixels and raytracing for the edges should help reduce the cost (left hybrid shadows, right fully raytraced)

![](../../assets/2f5238dd09b4c46c.png)

![](../../assets/5613f8c212adaf06.png)

Over the years I also performed a number of [smaller scale experiments](https://interplayoflight.wordpress.com/2021/07/10/raytracing-tidbits/) like exploiting the ray coherence between neighbouring pixels and caching hit triangle index to test before kicking off a full BVH traversal (a big advantage of having full control over the BVH traversal).

![](../../assets/7f76177ade5e33d3.jpg)

I also explored the impact of ray divergence on wave size, using shadowmaps to occlude lighting for hit point lighting and second bounce lighting

![](../../assets/252a012f79e52603.png)

![](../../assets/2d8d4516c2483f77.png)

Initially [I did some comparisons](https://twitter.com/KostasAAA/status/1362454532903550978?s=20&t=4aeGzC9qnKwI7o9-JPq--g) between my implementation and Mitsuba to validate GI intensity (left in engine, right Mitsuba).

![](../../assets/3037036e16da6c2e.jpg)

![](../../assets/34eb36cf3b32e1de.jpg)

I also started dabbling with [denoising](https://twitter.com/KostasAAA/status/1401234175135526912?s=20&t=4aeGzC9qnKwI7o9-JPq--g), using blue noise and temporal refinement to improve resolution of the GI and blurring to suppress the spatial noise.

![](../../assets/91e81611e2bb774d.jpg)

![](../../assets/d439a90aea9d585f.jpg)

Having support for raytraced GI,[ I made a few investigations on indirect lighting directionality](https://interplayoflight.wordpress.com/2021/12/28/notes-on-occlusion-and-directionality-in-image-based-lighting/), comparing raytraced GI to screen space AO + irradiance cubemaps (left raytraced, right SSAO).

![](../../assets/345e26359871ebf2.png)

![](../../assets/25b619f9bc2cae41.png)

Some more pretty images of raytraced cubemaps [here](https://twitter.com/KostasAAA/status/1470058520234102784?s=20&t=4aeGzC9qnKwI7o9-JPq--g).

Continuing on the theme of GI, I later added a path tracer to the toy engine to further validate the raytraced GI output. I did help me[ fix some issues](https://twitter.com/KostasAAA/status/1420483948841476099?s=20&t=4aeGzC9qnKwI7o9-JPq--g) with the noise I use to generate the rays.

![](../../assets/b3cb1e50d91c3716.jpg)


![](../../assets/b3cb1e50d91c3716.jpg)

Later I revisited denoising to [implement Metro: Exodus RTGI denoising](https://interplayoflight.wordpress.com/2022/03/26/raytraced-global-illumination-denoising/) (this game has been a great source of inspiration to me), which improved noise in GI significantly.

![](../../assets/0d9674187ca97d71.png)

![](../../assets/fddac36340ded969.png)

More recently I have [started experimenting with software VRS](https://twitter.com/KostasAAA/status/1510353051034566676?s=20&t=4aeGzC9qnKwI7o9-JPq--g) to reduce RTGI cost, which shows promise, but this is a story for another day.

![](../../assets/a8b7bdc835a75763.png)

![](../../assets/69804100c4c7ee35.jpg)

So what is next? More of the same of course but with a heavier focus on DXR. There are some many things to explore with raytracing, the journey is just beginning!

As ever, thank you for sharing your knowledge! As an ex graphics programmer I am living somewhat vicariously through your wonderful experiments :)

This blog is a constant inspiration of mine. Thank you for documenting your journey!

Hello. Love your writeups. Out of curiousity, what was the motivation behind programming with a laptop with only a hd4000?

Thank you! That was what I had available at the time. Also I love a challenge! :-)