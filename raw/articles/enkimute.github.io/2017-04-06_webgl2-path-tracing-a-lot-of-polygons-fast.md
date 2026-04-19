---
title: webGl2 - Path tracing a lot of polygons - fast.
url: https://enkimute.github.io/webgl2PathTracing.js/
author: Enki's blog
published: '2017-04-06'
source_blog: Enki's blog – Math, Graphics, Programming.
source_site: https://enkimute.github.io/
category: graphics
fetched: '2026-04-19'
---

GIT

![view on github](../../assets/cb9f317b98c6b74a.png)

# webGl2 - Path tracing a lot of polygons - fast.

please wait .. loading ..

Left click to rotate - Right Click to zoom ..

## WebGL2 - Path tracing.

Since webCL seems to be stuck in limbo, I was pretty excited about webGL2 making it to the major browsers - both on desktop and mobile. Sure - we don’t get compute shaders yet, but the glsl is bumped to version 3.00, removing the branching restrictions. Texture and renderbuffers in floating point are default features, and texture arrays provide a way around the limited texture resources of webGL1.

To get a better feel for the new features and the performance to expect I decided to see how webGL2 holds up against a compute heavy problem like path tracing. The results are quite impressive and show how even compute heavy problems can be tackled on todays web platform.

## Features in the demo.

- 150k+ polygons.
- Grid Based acceleration structure augmented with a distance field.
- Hammersley low discrepancy sampler.
- Importance sampling.
- Full anti-aliasing

The rendering speeds achieved greatly surpass those of common comercial CPU pathtracers (e.g. arnold), and approach those of current GPU implementations (e.g. octane). The lack of compute shaders and scattered write is a handicap, but the extra power provided by webGL2 truely unlocks a whole range of applications that used to be out of reach for the web ..

Source code of the demo above (350 lines) is available on GIT.

## Textures ? Materials ? Lens effects ? IBL ? PBR ? Direct Lighting ?

An extended version of this path tracer is implemented in my JimmyRig tool. Below are some screenshots that are all rendered in the browser (and all in seconds ..)

#### Textures, PBR materials, IBL lighting, Thin lens camera model

![](../../assets/f466b11aba5bc082.png)


#### Nested dielectrics, frosted glass.

![](../../assets/3096d9df78e169eb.png)


#### PBR Materials (metalness/roughness chart), IBL lighting, Direct Lighting Kernel

![](../../assets/6c09be5fb9b8145e.png)


#### High poly, IBL

![](../../assets/e84d4cfbb48e1dd7.png)