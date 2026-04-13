---
title: Shadow mapping basics
url: https://anteru.net/blog/2015/shadow-mapping-basics
published: '2015-08-06'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Welcome to a different kind of blog post! This time, I’ll be writing an educational piece about shadow mapping for all of you who are just getting started with real-time graphics and shader programming. If you want to see the implementation, please follow the [OctoAwesome](http://wiki.octoawesome.net) live-coding project where this will be included over time.

## Shadows

Let’s start right away by trying to define what problem we want to solve. As of today, OctoAwesome is an outdoor game without any kind of shadows but with some kind of fixed-function illumination. For every pixel that is shaded, the lighting is evaluated even if the point is occluded by some geometry. What we want to add is the ability for a point to query whether it is occluded or not.

Some of you might shout **ray-tracing**. And you’re absolutely right, we will use this as our mental model to derive shadow mapping! So how would the lighting code work? If we had something like a `shadow()`

API call in the shader, we could use that to trace a ray from the point being shaded to the light source. `shadow()`

returns a boolean, which indicates whether the path is clear or not.

The problem here is how to implement the `shadow()`

call. For efficient ray-tracing, we’re going to need some kind of acceleration structure and then a rather involved kernel to do the real tracing. In the case of OctoAwesome, we would probably want to trace a binary volume for maximum efficiency. We’d also need some special way to handle transparent blocks like the trees and animated objects. Not impossible but a lot of work.

We’ll notice pretty quickly that for each frame, we have to trace a lot of rays and that gets expensive due to the traversal. It’s even worse as we trace the same rays over and over, at least as long the light source and the camera is not moving. This is surely not the most efficient way; it feels as if we should be able to store and reuse the results of the `shadow()`

calls somehow.

## Caching

And indeed, there is a way to reuse `shadow()`

calls. The key insight is that we can store one value per ray to resolve the `shadow()`

query for **all points** along the ray. The value we store is the distance to the closest hit, and our new `shadow()`

call now just checks the distance of the query point against the closest point. If further away, it is in shadow.

Now the only problem is how to store the “per-ray” data, which are now cast from arbitrary points. For a distant light source, imagine we place a grid orthogonal to the light direction and quantize rays into small “cells”. That is, all rays which are emitted “nearby” will go into the same cell. This introduces a bit of error, depending on how big our cells are and other factors, but in general it’s quite acceptable.

## Implementation

What we need to do now is to **produce a grid of distance values** from the light source, **store** this somehow, and during shading, **project the points into that grid** and **compare the values**. Turns out the GPU is **perfectly** suited for this. Producing distance values is exactly what we do when writing into the depth buffer. Storing is equally easy, we can re-use a depth buffer as a texture. The only remaining problem is to project the points into the shadow map and compare the values.

Let’s tackle the problems one-by-one. First of all, we need a new camera, which captures the scene **as seen from the light** into a depth map. This means we need to create a new render target, which has only a depth buffer bound. We also need to set up the camera correctly: It should cover the complete view frustum and nothing else, to maximize the effective resolution. Finally, when rendering, we should turn off all pixel shaders to improve performance. Of course, for alpha-tested geometry, we need the shaders, but if possible we should use a simplified version which only calls `discard()`

while generating the shadow map.

The next step is the normal render pass in which we need to implement the `shadow()`

call. For this to work, we have to project the point being shaded into the shadow map, that is, it has to go from world-space into the light-space using the same projection as we used to generate the shadow map. This means we need to pass-through the world-space position somehow through the vertex shader, the easiest way is to simply forward it and then multiply with the light projection in the pixel shader. One division, one adjustment for the -1..1 to 0..1 coordinate system difference, and a comparison later and we know if the point is in shadow!

## Details

The solution above will work in practice but result in quite ugly, blocky shadows. We can achieve higher quality by using a [comparison sampler](https://msdn.microsoft.com/en-us/library/windows/desktop/bb509696%28v=vs.85%29.aspx) and linear filtering, which will enable hardware-accelerated [percentage closer filtering](http://www.eng.utah.edu/~cs5610/handouts/reeves87.pdf).

I’ve also omitted lots of other problems we’re going to run into. For instance, the shadow map resolution should be improved by using cascaded shadow maps, we should use some kind of contact hardening shadows to make the shadows softer further away, and so on. Good shadow mapping is actually really hard to implement, due to the fixed precision and resolution of shadow maps, but right now, it’s the best we can do until the hardware becomes fast enough to trace soft-shadows in real-time. This will be hopefully the topic of a future blog post :)