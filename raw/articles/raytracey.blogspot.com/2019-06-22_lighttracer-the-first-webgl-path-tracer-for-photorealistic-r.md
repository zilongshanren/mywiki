---
title: LightTracer, the first WebGL path tracer for photorealistic rendering of complex
  scenes in the browser
url: http://raytracey.blogspot.com/2019/06/lighttracer-first-webgl-path-tracer-for.html
author: Sam Lapere
published: '2019-06-22'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

A couple of days ago, Denis Bogolepov sent me a link to LightTracer, a browser based path tracer which he and Danila Ulyanov have developed. I'm quite impressed and excited about LightTracer, as it is the first WebGL based path tracer that can render relatively complex scenes (including textures), which is something I've been waiting to see happen for a while (I tried something similar a few years ago, WebGL still had too many limitations back then).

What makes LightTracer particularly interesting is that it has the potential to bring photoreal interactive 3D to the web, paving the way for online e-commerce stores offering their clients a fully photorealistic preview of an article (be it jewellery, cars, wristwatches, running shoes or handbags).

Up until now, online shops have been trying several ways to offer their clients "photorealistic" previews with the ability to configure the product's materials and colours. These previews were either precomputed 360 degree videos, interactive 3D using WebGL rasterization and even using server-side rendering via cloud based ray tracing streamed to the browser (e.g. Clara.io and Lagoa Render) which requires expensive servers and is tricky to scale.

LightTracer's WebGL ray tracing offers a number of unique selling points:

-

**ease of use**: it's entirely browser based, so nothing needs to be downloaded or installed
-

**intuitive**: since ray tracing follow the physics of light, lights and materials behave just like in the real world, allowing non-rendering-experts to predictably light their scenes
-

**photorealisitic lighting and materials**: as Monte Carlo path tracing solves the full rendering equations without taking shortcuts, this results in truly photoreal scenes
-

**speed**: LightTracer's ray tracing is accelerated by the GPU via WebGL, offering very fast previews. This should get even faster once WebGL will support hardware accelerated ray tracing via Nvidia's RTX technology (and whatever AMD has in the works)
LightTracer is still missing a few features, such as an easy-to-use subsurface scattering shader for realistic skin, hair and waxy materials, and there are plenty of optimisations possible (scene loading speed, UI improvements and presets, etc.) but I think this is the start of something big.

## No comments:

Post a Comment