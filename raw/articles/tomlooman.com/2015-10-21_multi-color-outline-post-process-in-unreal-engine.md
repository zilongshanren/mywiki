---
title: Multi-color Outline Post Process in Unreal Engine
url: https://tomlooman.com/unreal-engine-outline-multi-color-post-process/
author: Tom Looman
published: '2015-10-21'
source_blog: Tom Looman
source_site: https://www.tomlooman.com/
category: unreal engine
fetched: '2026-04-13'
---

With some of the recent changes to Unreal Engine 4, rendering multi-color outlines is now possible! This is done through the use of Custom Stencil, a new buffer similar to Custom Depth - but allowing meshes to render as integer values. This provides us with a 1-255 range of indices that can be used to apply different outline colors to meshes and even combine multiple features such as the decal x-ray shown below by using a different stencil index.

![](../../assets/440be11337aa1cfa.jpg)


## The Original Custom Depth

The original outline material I made last year was based on Custom Depth, before Custom Stencil was available. This meant there was no way to determine the mesh type after it was drawn into the buffer as single channel depth value. More info on the effect and other uses for Custom Depth are available in my of [my earlier posts](https://tomlooman.com/unreal-engine-custom-depth). The original effect uses fewer instructions (97 vs. 144 of the new material) so if you don’t require multiple colors in your game you can consider sticking to the old effect.

The new effect is still using Custom Depth to determine the (optional) occlusion which adds the faint overlay color adjusted by tweaking the *FillAlpha* parameter in the post process. This occlusion can be turned off in the material by unchecking *FillOcclusion* in the material instance.

![](../../assets/ca9afe96700a21e2.jpg)

*The Custom Depth visualizer.*

## Setup Instructions

To enable the outline you need to place a **Post Process Volume**. Make sure you **set it to Unbound** so it’s available regardless whether camera is inside the volume or not. With the post process volume selected, go to **Settings > Blendables** and add the PPI_OutlineColored as the first entry.

## Enabling Custom Stencil

Custom Stencil is disabled by default, to enable go to * Window > Project Settings > Rendering > Post Process > Custom Depth-stencil Pass* and set it to

**Enabled with Stencil**.

Some of the meshes are not visible in the Custom Stencil visualizer in this example, their Stencil value is set to 0 (default), excluding them from this buffer.

![](../../assets/0727f739f5afc1ca.jpg)


To enable this visualizer go to your viewport, look for *Lit > Buffer Visualizer > Custom Stencil*.

You can enable Custom Depth and change the Stencil index through the editor menu of a mesh under the Rendering category.

![](../../assets/7872ae4816e965b7.jpg)


If you’re using C++ you can define the stencil indices in a convenient place in your game code.

```
/* Stencil index mapping to PP_OutlineColored */
#define STENCIL_FRIENDLY_OUTLINE 252;
#define STENCIL_NEUTRAL_OUTLINE 253;
#define STENCIL_ENEMY_OUTLINE 254;
#define STENCIL_ITEMHIGHLIGHT 255;
```


Enabling custom depth and setting the index in C++ is pretty straightforward (Available in Blueprint as well).

```
GetMesh()->SetRenderCustomDepth(true);
GetMesh()->SetCustomDepthStencilValue(255); // assign within 1-255 range.
```


## Download Assets

You can get access to the material files [ here](https://courses.tomlooman.com/p/object-outline-materials-unreal-engine).