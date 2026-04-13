---
title: 'Brigade: animation test WIP1'
url: http://raytracey.blogspot.com/2012/04/brigade-animation-test-wip1.html
author: Sam Lapere
published: '2012-04-02'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

FreDre, sure it's possible, but the hardware tesselation in GPUs is useless for ray tracing. Micropolygon ray tracing has been done on the GPU before (see "Micropolygon ray tracing with defocus and motion blur" and "A shading reuse method for efficient micropolygon ray tracing")

Whiskersnout: I could do that, but the geometric complexity of a Doom 3 level (a game from 2004) pales in comparison to current games, so it's not really a challenge. Brigade can do a whole lot more (e.g. the spaceship in the previous post was 850k triangles, and it rendered at 30 fps with real-time photorealistic GI). I'm actually preparing a scene which has more geometric detail per square meter than a level of Crysis 2.

Actually this is from 2007: http://developer.amd.com/sdks/radeon/pages/RadeonSDKSamplesDocuments.aspx#d3d10 Looks like something Humus made. For some reason only runs at 41 fps on my 5870. In order to take the load of the CPU and PCIe bus, for animations with large numbers of dynamic objects, features like GPU skinning and instancing were added. Path tracing uses very different concepts, with BVH update using CPU, it will be hard or even impossible to match this in real time.

It is actually possible to do this in real-time when the acceleration structure is built on the GPU, check the recent work on HLBVH2 (Pantaleoni/Garanzha) and Voxelpipe (Pantaleoni)

## 11 comments:

Looks awesome


Is it possible to add displacement maps or tessellation into models within a path traced engine?

That is so awesome. What's the likelihood that you could recreate or take a room of a Doom 3 map and stick him in there with his texturing?

Thanks.



FreDre, sure it's possible, but the hardware tesselation in GPUs is useless for ray tracing. Micropolygon ray tracing has been done on the GPU before (see "Micropolygon ray tracing with defocus and motion blur" and "A shading reuse method for efficient micropolygon ray tracing")

Whiskersnout: I could do that, but the geometric complexity of a Doom 3 level (a game from 2004) pales in comparison to current games, so it's not really a challenge. Brigade can do a whole lot more (e.g. the spaceship in the previous post was 850k triangles, and it rendered at 30 fps with real-time photorealistic GI). I'm actually preparing a scene which has more geometric detail per square meter than a level of Crysis 2.

What about something like this:

http://www.youtube.com/watch?feature=endscreen&NR=1&v=C9i5HLANhbs

That was 2008.

Actually this is from 2007:

http://developer.amd.com/sdks/radeon/pages/RadeonSDKSamplesDocuments.aspx#d3d10

Looks like something Humus made. For some reason only runs at 41 fps on my 5870.

In order to take the load of the CPU and PCIe bus, for animations with large numbers of dynamic objects, features like GPU skinning and instancing were added.

Path tracing uses very different concepts, with BVH update using CPU, it will be hard or even impossible to match this in real time.

It is actually possible to do this in real-time when the acceleration structure is built on the GPU, check the recent work on HLBVH2 (Pantaleoni/Garanzha) and Voxelpipe (Pantaleoni)

So let's put one of your next challenges an animation of at least 100 detailed models. (fast animation not required)

Sure buddy, if you help me implement HLBVH2 first :)

If OTOY gives me similar conditions as my current employer, I might actually do it.

Sam, David didn't replied you with src code?


Kirill

Hi Kirill,


Nope, I didn't get a reply from him yet.

Post a Comment