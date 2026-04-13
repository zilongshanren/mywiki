---
title: Publications
url: https://blog.selfshadow.com/publications/
author: Stephen Hill
published: '2026-01-01'
source_blog: Self Shadow
source_site: https://blog.selfshadow.com/
category: graphics
fetched: '2026-04-13'
---

## Courses

[Physically Based Shading in Theory and Practice](https://blog.selfshadow.com/publications/s2025-shading-course/) (SIGGRAPH 2025)

[Physically Based Shading in Theory and Practice](https://blog.selfshadow.com/publications/s2020-shading-course/) (SIGGRAPH 2020)

[Physically Based Shading in Theory and Practice](https://blog.selfshadow.com/publications/s2017-shading-course/) (SIGGRAPH 2017)

[Physically Based Shading in Theory and Practice](https://blog.selfshadow.com/publications/s2016-shading-course/) (SIGGRAPH 2016)

[Physically Based Shading in Theory and Practice](https://blog.selfshadow.com/publications/s2015-shading-course/) (SIGGRAPH 2015)

[Physically Based Shading in Theory and Practice](https://blog.selfshadow.com/publications/s2014-shading-course/) (SIGGRAPH 2014)

[Physically Based Shading in Theory and Practice](https://blog.selfshadow.com/publications/s2013-shading-course/) (SIGGRAPH 2013)

[Practical Physically Based Shading in Film and Game Production](https://blog.selfshadow.com/publications/s2012-shading-course/) (SIGGRAPH 2012)

This SIGGRAPH Course is the spiritual successor to [Physically-Based Shading Models in Film and Game Production](http://renderwonk.com/publications/s2010-shading-course/). It’s a tough act to follow, but [Steve McAuley](http://stevemcauley.com/) and I decided to organise the followup based on strong interest from the game development community, in addition to our own.

We owe a debt of graditude both to Naty Hoffman for putting us in contact with the other speakers, and naturally to the speakers themselves. Not only did they enthusiastically dedicate their time to presenting, but they also produced thoroughly excellent course material that will surely influence and inspire practitioners, just as the 2010 course did.

## Papers

[EON: A practical energy-preserving rough diffuse BRDF](https://jcgt.org/published/0014/01/06/) (JCGT, vol. 14, no. 1, 2025)

[Filtering Distributions of Normals for Shading Antialiasing](https://research.nvidia.com/publication/filtering-distributions-normals-shading-antialiasing) (HPG, 2016. Best paper award)

## Talks

[Real-Time Ray Tracing of Correct* Soft Shadows](http://advances.realtimerendering.com/s2018/index.htm) (Advances in Real-Time Rendering course, SIGGRAPH 2018)

[Real-Time Line- and Disk-Light Shading with Linearly Transformed Cosines](https://blog.selfshadow.com/publications/s2017-shading-course/) (Physically Based Shading course, SIGGRAPH 2017)

[Real-Time Area Lighting: a Journey from Research to Production](https://blog.selfshadow.com/publications/s2016-advances/) (Advances in Real-Time Rendering course, SIGGRAPH 2016)

[Game Rendering: Past, Present… and Future?](https://web.archive.org/web/20160208225541/http://egsr2015.gcc.tu-darmstadt.de/sites/keynote-speakers.html) (Invited Talk, EGSR 2015)

[Rock-Solid Shading: Image Stability Without Sacrificing Detail](http://advances.realtimerendering.com/s2012/index.html) (Advances in Real-Time Rendering course, SIGGRAPH 2012)

Even the best looking games still lack the visual cleanness of animated movies from the mid ’90s, despite exceeding them in level of detail. One reason is the lack of solid anti-aliasing in our shaders. To help redress the balance, Dan Baker and I cover techniques for dealing with different facets of the problem, drawing from recent research and production experience.

[Rendering With Conviction](https://www.selfshadow.com/talks/rwc_gdc2010_v1.pdf) (Gamefest, GDC and GDC Canada, 2010)

For this talk, I decided to focus on two key rendering systems developed for *Splinter Cell: Conviction* that I thought would be interesting to discuss because they were both fairly different from established solutions. The first of these was our GPU-based hierarchical visibility system, which not only gave us great culling at very low cost, but also simplified the renderer design and the lives of our artists. The second was our semi-dynamic Ambient Occlusion solution, that we actually had up and running well in advance of the publication of [Crytek’s SSAO approach](http://www.crytek.com/sites/default/files/Mittring-Finding_NextGen_CryEngine2_Siggraph07.ppt) (SIGGRAPH 2007), but couldn’t talk about until several years later.

## Articles

[Linear-Light Shading with Linearly Transformed Cosines](https://blogs.unity3d.com/2017/04/17/linear-light-shading-with-linearly-transformed-cosines/) (GPU Zen, 2017)

[Blending in Detail](https://blog.selfshadow.com/publications/blending-in-detail/), July 2012

This article, written with [Colin Barré-Brisebois](http://colinbarrebrisebois.com), compares various existing methods of combining normal maps, along with a new technique dubbed *Reoriented Normal Mapping* that Colin developed and I helped to optimise.

[Overdraw in Overdrive](https://blog.selfshadow.com/publications/overdraw-in-overdrive/) (Xbox Developer Journal, 2011)

The genesis of this article was [an appeal](http://twitter.com/#%21/solid_angle/status/5696284937691136) on Twitter from Steve Anichini, asking if it was possible to display, in-engine, the *overshading* of pixel quads, as shown in the recent [ Reducing Shading on GPUs using Quad-Fragment Merging](http://graphics.stanford.edu/papers/fragmerging/) paper. It turns out that there

*is*a way to achieve this efficiently on Xbox 360, leading to a real-time debug view that’s even more accurate than PIX.

[Practical, Dynamic Visibility for Games](https://blog.selfshadow.com/publications/practical-visibility/) (GPU Pro 2, 2011)

I had some great correspondence with various developers following my Gamefest/GDC talk, and it became clear that I really ought to publish a full account of our visibility system, both to clarify a couple of points and to offer a little more implementation advice. I’d also been informed that the game *Warhawk* had taken a somewhat similar approach on PS3 a few years back, albeit via the SPUs and without using a z-pyramid. Unfortunately, details on this are sketchy at best if you’re not a PS3 developer, but I was aware of DICE [doing the same kind of thing](http://www.slideshare.net/repii/the-intersection-of-game-engines-gpus-current-future-presentation/19) for *Battlefield: Bad Company,* and they were happy to share more details. One thing lead to another and I ended up co-authoring a chapter for [ GPU Pro 2](http://downloads.akpeters.com/gpupro/) with Daniel Collin about our respective solutions.

[Hardware Accelerating Art Production](https://web.archive.org/web/20080227065455/http://www.gamasutra.com/view/feature/2042/hardware_accelerating_art_.php) (Gamasutra, 2004)

This was an article that I wrote quite some time ago that helped me gain a proper foothold within the videogame industry. Although certain aspects relating to Shader Model 1.1 hardware are antiquated now, the central idea of using the GPU to speed up Ambient Occlusion baking (or higher order PRT) is still very relevant today. We used an evolution of this technique to generate static AO textures during the production of *Splinter Cell: Conviction*, resulting in rapid iteration times for artists, without compromising fidelity.