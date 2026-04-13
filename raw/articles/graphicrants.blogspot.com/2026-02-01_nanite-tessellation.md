---
title: Nanite Tessellation
url: http://graphicrants.blogspot.com/2026/02/nanite-tessellation.html
author: Brian Karis
published: '2026-02-01'
source_blog: Graphic Rants
source_site: http://graphicrants.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

List of posts:

[Intro](https://graphicrants.blogspot.com/2026/02/nanite-tessellation.html)[Possible approaches](https://graphicrants.blogspot.com/2026/02/possible-approaches-for-tessellation.html)[How to tessellate](https://graphicrants.blogspot.com/2026/02/how-to-tessellate.html)[Nanite + Reyes](https://graphicrants.blogspot.com/2026/02/nanite-reyes.html)[Variable sized work](https://graphicrants.blogspot.com/2026/03/variable-sized-work.html)- Vertex deduplication / Post transform cache (coming soon)
- VisBuffer / Deferred materials
- Wrapping up

### What is Nanite Tessellation?

A system for dynamically tessellating meshes and displacing them. The displacement comes from a shader graph, authored in UE’s material editor. This tessellation is in addition to what Nanite already provides.Tessellation demoed at GDC in Marvel 1943: Rise of Hydra


Patches


Diced triangles


Final pixels

## Why?

Why is geometry amplification needed when we have Nanite?

[I’ve argued in the past](https://www.youtube.com/watch?v=NRnj_lnpORU)that amplification approaches to the virtualized geometry problem were not good enough, so why would I start working on it now? Have I changed my mind? No. My argument was that amplification approaches are not a general purpose solution to the virtualized geometry problem. They do not solve all cases. They can’t change the genus of a surface. A simplification approach would always be needed. If you have that it could also solve amplification in a way. A mesh could always be synthesized, subdivided, tessellated, and/or displaced offline. Then simplification can reduce it down. This ignores the data storage implications but it does show that it is the more general purpose solution to that problem.

So we have that now. It’s called

[Nanite](https://www.youtube.com/watch?v=eviSykqSUUw)and is pretty cool. It was the right thing to work on first. But just because this solution is general purpose enough that it can be used for these other cases does not mean it is ideal for them. Storing full topology of an irregular mesh covers all cases but is expensive. Storing every position on the surface as a full 3d point with a complete set of attributes is expensive. We do our best to compress that data but nothing beats not having that data at all.

### Compression

Scalar displacement fields, whether they are artist authored maps or captured through projection of a detailed surface to a simpler one, are much less data. 1 value compared to 5+. Compression of regular 2D data, ie images, in relation to human perception is vastly more researched and well understood.


Comparison of disk size for high poly vs low poly with normal and displacement maps

Even better data compression than that are procedural texturing approaches. What do I mean by procedural texturing? I don’t just mean mathematical functions like Perlin noise. I might be pushing the definition a bit but even simple texture tiling in a way is a form of procedural texturing. But certainly once shaders are involved where multiple textures are mixed and modified we are in the realm of procedural. The simplest form of this is detail texturing. A much higher frequency signal can be represented than stored explicitly. Viewed statically like this, the compression ratio can be far higher than is achievable through any other means.### Authoring

But beyond data compression, procedural content generation can be an incredibly effective time saver for an artist. It also can be reusable, dynamic, and animatable. By reusable I mean that a base material type, like snow, can be authored once and applied to many surfaces. By dynamic I mean the same asset can accumulate snow over time by changing the shader parameters, all the way to full animation like a moving lava field flow.Displacement maps are extremely common in film and the primary reason for their use is not data compression. A good bit of it is tooling and while I could say that should be improved and is someone else’s responsibility to keep up with Nanite’s capabilities, the fact of the matter is I can’t snap my fingers and change all the DCCs. Even if every application were all optimized to better work with high poly meshes there is always something inherently simpler with 2d textures, and displacement maps are no different.

Displacement’s use in film also helps animation. For a character the base cage can be rigged and deformed. The deformed cage can then be smoothly subdivided and displaced to get the final detail. This simplifies the rigger’s and animator’s concerns and separates them to an extent from the sculptor who might carve out individual dragon scales.

The last use case is specific to games. Scalability is an important consideration for Fortnite as well as other games that still need to support lower end platforms that aren’t powerful enough to run the Nanite pipeline. We can easily generate low poly fallback meshes through the same mesh simplification algorithm that Nanite uses, but what is fine for the distance isn’t necessarily good enough for up close. The art of low poly modelling is often a matter of abstraction of shape and artists are much more picky about the results. They will also move detail between domains, from mesh to texture, that requires involvement of other assets that is difficult or impossible to automatically do reliably. For these reasons, when a large scalability range is required, like with Fortnite, our art teams have been more comfortable authoring for low or mid in the scalability range and amplifying up rather than authoring for high and simplifying down.