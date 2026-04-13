---
title: Thoughts on the knowledge of an up-to-date Graphics Programmer
url: http://diaryofagraphicsprogrammer.blogspot.com/2011/03/thoughts-on-knowledge-of-up-to-date.html
author: Wolfgang Engel
published: '2011-03-15'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

There are certainly more pieces that you could talk about, I just picked the ones I believe can easily be separated from the renderer or the ones that I would consider are more important features of a renderer. Here is the list of the last class:

- DirectX 11 API
- Deferred Lighting / MSAA and more
- Order-Independent Transparency
- Shadows: Cascaded, Cube, Soft Shadows and more
- PostFX: HDR, Depth of Field, Motion Blur, Color Filters and more
- GPU Particle System
- Real-Time Dynamic Global Illumination - several techniques
- CUDA, DirectCompute

**DirectX 11 API**

I am totally agnostic to any graphics API. I don't care which API I am using as long as the API exposes all the hardware features. In fact in the last two years I worked more with OpenGL ES 2.0 on mobile devices (that unfortunately doesn't expose many hardware features) than with DirectX 11. My students at UCSD prefer OpenGL. The reason why I expose them in one session to DirectX 11 is that this API currently exposes more features than OpenGL (although OpenGL catches up ... fortunately). On Windows platforms DirectX has better driver support, while on Apple, you want to prefer using OpenGL. As far as I know Apple is beta testing OpenGL 3.2 and is otherwise still on 2.0.

I am trying to teach the Direct3D API by highlighting the concepts and not talking too much about API calls and parameters. Having learned one API should enable anyone to use any other graphics API on his own, because all the underlying principles are the same. Graphics API's are not that different anymore; just the amount of hardware functionality they expose is different.

One thing that is remarkable is that there is no good Direct3D 11 book available. Together with others I published a short Direct3D 10 book that was mostly written about 3 - 4 years ago at [

[Direct3D10](http://wiki.gamedev.net/index.php/D3DBook:Book_Cover)]. There is a book by A.K. Peters coming out on

[Direct3D 11](http://diaryofagraphicsprogrammer.blogspot.com/Practical Rendering and Computation With Direct3d 11), several of the authors that worked on the Direct3D 10 book worked on this one too and it looks promising.

**Deferred Lighting / MSAA / Order-Independent Transparency**

Nowadays, it is easy to say that Deferred Lighting is a standard setup for a rendering system. Using Deferred Lighting in a rendering system streamlines your renderer design in a certain direction, so you have to be fully aware of the side effects of Deferred Lighting.

Currently we still differ between rendering opaque and transparent objects. Only opaque objects get the Deferred Lighting treatment and transparent objects -that can't be rendered into the depth buffer- require a simplified lighting model, that is only applied to transparent objects.

If we want to reach CG movie lighting and shadows, we need 1000's of lights and 100's of shadows. I think we can render on most hardware now for objects that are in the depth buffer 1000's of lights, the shadows are harder to achieve. Unfortunately there is no generic solution for rendering shadows on transparent objects either.

Designing a renderer so that it supports Order-Independent Transparency (OIT) might help here, although currently available techniques running on average hardware are still too expensive.

Following the development of OIT is certainly of great interest to graphics programmers, so I added this topic to the curriculum of my class.

MSAA is expensive when used with Deferred Lighting (commonly only used by running the lighting/shadow shader per-sample on edges of objects and per-pixel everywhere else). MLAA doesn't cover moving objects very well although it is a good replacement for everything else.

**Shadows: Cascaded, Cube, Soft Shadows and more**

Shadows are still expensive because they consume lots of vertex /geometry shader cycles and/or are memory bandwidth hungry. For cube shadow maps, my last article on a typical Ellipsoid Light Shadow setup can be found

[here](http://altdevblogaday.com/2011/02/28/shadows-thoughts-on-ellipsoid-light-shadow-rendering/).

Cascaded Shadow maps and the future development for outdoor shadows represent a natural Level-of-Shadow (LOS) system. With each cascade, the distribution of shadow resolution is lower and therefore the shadow map area to on-screen pixel ratio is already part of the approach, with future approaches probably offering a more detailed LOS system. The expectation is that the "Multi-Frustum Shadow" approach taken with Cascaded Shadow Maps will be brought to the next level with finer granularity and better LOS.

Cube shadow maps can cover many different light types. Like with Cascaded Shadow Maps, the culling of objects and therefore the amount of geometry rendered into those maps is a challenge. Their error distribution compared to their next competitor Dual-Paraboloid Shadow maps is better and therefore they are favorable to those.

Soft Shadows are a refinement that will be available in more and more games. Rendering perceptually correct shadows that show a softer penumbra based on the distance of the occluder to the shadow receiver is a nice looking feature that should be widely available soon.

**PostFX: HDR, Depth of Field, Motion Blur, Color Filters and more**

Different parts of a modern PostFX pipeline full-fill very different tasks in a rendering system. Many of them are dealing with color quality in general, like HDR rendering and tone mapping. Others mimic real-world camera systems so that the player -who is expected to be accustomed to all the errors camera lenses introduce- feels comfortable while playing a game.

Depth of Field and motion blur are quite often used to get over Level-of-Detail (LOD)rendering shortcomings. In an open world game Depth of Field can be used to hide the fact that the buildings 200 meters away from the camera use a lower LOD level. Motion blur is usually used to offer the sense of speed.

In recent development, very nice looking Depth of Field with Bokeh is used to guide the attention of the user to certain parts of the screen. Those effects are more expensive, although you can also run them on an integrated GPU -like Intel's Sandy Bridge- [

[RawK](http://www.confettispecialfx.com/rawk®-graphics-demo-for-sandy-bridge)].

**GPU Particle System**

Modern particle systems are used to cover much more than just explosion effects. They can represent liquid or small objects that are flocking, cast light and shadows and expose many other behavior patterns like collision response, flight physics or for example leaf, trash or grass behavior.

Mimicking those systems is now part of a graphics sub-system that runs favorably on the GPU, to achieve large numbers of particles. As long as all the memory access is happening on the GPU in "streaming" patterns, those systems can simulate very high numbers of particles.

With a full-featured list of requirements for a next-gen particle system, it should be easy to define the position of one or more programmers who deal only with this system.

A GPU Particle System is a "mini" game engine with all the features of a game engine like drawing, simulation, collision detection, collision response, audio support, networking etc.. It demonstrates the GPU usage patterns of next-gen engines.

**Real-Time Dynamic Global Illumination - several techniques**

It looks like the next level of detail in lighting is expected to be -what is commonly named- Global Illumination. Everything said about Deferred Lighting and shadows applies also to Global Illumination. So shadows are more difficult and transparent objects are challenging.

Whatever the Global Illumination technique of choice is, the most critical aspect is that it is fully dynamic and does not occupy much memory. A typical system based on a Light Propagation Volume approach consumes about 1.5 to 2.5 Mb of memory and extends the shadow map already used, following the Reflective shadow map idea developed by Carsten Dachsbacher et. all.

Looking at it from a birds eye of view, Reflective shadow maps seem to be a good starting point for any development in the area. Collecting the bouncing diffuse, specular light and occlusion "somewhere" and then re-applying the light data to a scene is difficult, while balancing quality and performance [Dachsbacher], [DachsbacherSii], [Kaplanyan].

As usual I keep stressing the fact that whatever we do should be as "dynamic" as possible without the usage of look-up textures or light maps. That especially applies to Global Illumination.

**CUDA, DirectCompute**

Another important topic for a graphics programmer are the new "General Programming" interfaces that allow to program the GPU more like a CPU. That means that algorithms that didn't fit well into the rasterized graphics pipeline assumed by most GPUs nowadays, can be implemented easier; as long as the data set is suitable for GPU usage.

CUDA represents a good entry level knowledge here. It gives a very good overview on how NVIDIA GPUs actually work, how different types of memories need to be involved and how code is executed on those GPUs.

DirectCompute and OpenCL are more abstract and hide some of the valuable knowledge required for CUDA programming. Although both are expected to work on all GPUs and are therefore easier portable.

All this being said, what will my future list for the class look like?

- Direct3D X API
- CUDA, DirectCompute
- Deferred Lighting / MSAA and more
- Order-Independent Transparency
- Shadows: Cascaded, Cube, Soft Shadows and more
- PostFX: HDR, Depth of Field, Motion Blur, Color Filters and more
- GPU Particle System
- Real-Time Dynamic Global Illumination - several techniques

**References**

[Dachsbacher] Carsten Dachsbacher, Marc Stamminger, “Reflective Shadow Maps”,

[http://www.vis.uni-stuttgart.de/~dachsbcn/download/rsm.pdf](http://www.vis.uni-stuttgart.de/~dachsbcn/download/rsm.pdf)

[http://www.vis.uni-stuttgart.de/~dachsbcn/publications.html](http://www.vis.uni-stuttgart.de/~dachsbcn/publications.html)

[[DachsbacherSii] Carsten Dachsbacher, Marc Stamminger, “Splatting Indirect Illumination”,](http://www.vis.uni-stuttgart.de/~dachsbcn/publications.html)

[http://www.vis.uni-stuttgart.de/~dachsbcn/download/sii.pdf](http://www.vis.uni-stuttgart.de/~dachsbcn/download/sii.pdf)

[[Kaplanyan] Anton Kaplanyan, Wolfgang Engel, Carsten Dachsbacher,](http://www.vis.uni-stuttgart.de/~dachsbcn/download/sii.pdf)

“Diffuse Global Illumination with Temporally Coherent Light Propagation Volumes”, GPU Pro 2,

pp 185 – 203, AK Peters, 2011

## 2 comments:

Is it possible to attend your course online?

No, there is no online-class in the moment. I teach this at UCSD.

Post a Comment