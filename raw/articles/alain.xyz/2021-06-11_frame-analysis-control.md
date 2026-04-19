---
title: Frame Analysis - Control
url: https://alain.xyz/blog/frame-analysis-control
author: Alain Galvan
published: '2021-06-11'
source_blog: Alain Galvan · Ray Tracing Driver Engineer at AMD
source_site: https://alain.xyz/
category: graphics
fetched: '2026-04-19'
---

Control is a metaphysical 3rd person shooter by [Remedy Entertainment](https://www.remedygames.com/games/control/), creators of [Quantum Break](https://www.remedygames.com/games/quantumbreak/) and [Alan Wake](https://www.remedygames.com/games/alan-wake/). You play as **Ms. Jesse Faden**, who finds herself in the *Federal Bureau of Control*, and upon discovering an odd gun and apparent suicide of the previous director, assumes the role of new Director of the FBC by *the Board*, a god-like group reminiscent of the employers from titles like [Valve's Half Life](https://www.half-life.com/en/alyx/). She's tasked to ridding the FBC from a metaphysical force she called the Hiss (which appears to be a force similar to the Dark Presence in Alan Wake) to both please *the Board* and further her own goals.

Control's gameplay loop is similar to that of [From Software's Bloodbore](https://www.playstation.com/en-us/games/bloodborne/) or [Id Software's Doom Eternal](https://bethesda.net/game/doom), with a strong emphasis on moving to dodge your enemies attacks and using abilities granted to you by *objects of power* (or OoPs) to both improve your combat abilities and navigate the world like a *Metroidvania*. Possessed enemies have similar combat abilities that they use to attack and lock off sections of the world.

Visually, the game looks stunning, with *real time ray traced shadows*, *ray traced global illumination*, *ray traced reflections*, *Deep Learning Super Sampling*, volumetric effects, and carefully tuned environmental effects like broken glass, and office debris. Let's analyze exactly what's happening in a single frame of Control, at its highest settings at `4K`

with Deep Learning Super Sampling enabled.

⚠️

Note: This is not an official analysis of theNorthlight Enginerenderer. Please supportControl Ultimate Editionby grabbing a copy of it via Steam, Playstation Store, Xbox Store, or the Nintendo Store, thanks!

We'll be doing a high level analysis of a somewhat still frame mid combat in an area relatively early in the game, with plenty of lights, reflections, and global illumination.

Each frame starts with setting up various data structures. Some early Draw calls build *texture atlases* for various UI elements, generate **Acceleration Data Structures** for the scene and Bounding Volume Hierarchies (BVHs) for lights.

![Shadow Depth Screenshot](../../assets/b4fee025c600e2e4.jpg)


A **light shadow depth pass** renders to a large `16384x2048`

*texture atlas*. Each segment of the atlas is relatively small, about `512x512`

with the smallest being `256x256`

. While it might seem odd that this is here given that ray traced shadows are enabled, both ray traced shadows **and** raster based shadows are used to resolve shadows in Control, with ray traced shadows used for select lights as a means of better resolving contact shadows.

![]() | ![]() |
|---|---|
![]() | ![]() |

The **Prepass** for Control renders *view space normals* with the `b`

channel being used for edge softening/contact edges for corners, and a second render attachment encodes *subsurface data* in the `r`

channel and *roughness* in `g`

.

![Prepass RG channels Screenshot](../../assets/3c7bb9ac263518aa.jpg)


There's a second shadow and prepass step as well for smaller objects as well and to apply beveled edge effects to objects in the environment.

![Velocity Screenshot](../../assets/053ddb07c7b4b469.jpg)


Velocity is encoded in its own separate pass afterwards. This appears to be NDC based velocity, encoded to an `R16G16_FLOAT`

texture.

![Bent Normals Screenshot](../../assets/eb60271adf599afe.jpg)


The **lighting passes** begins with a few `Dispatch`

calls to calculate bent normals, then renders reflections, global illumination, and shadows with `DispatchRays`

.

![Reflection Screenshot](../../assets/acf0bc06e599d1d7.jpg)


**Ray traced reflections** renders at full resolution with samples denoised shortly after rendering. Reflected rays are based on the GGX specular bidirectional reflectance distribution function (BRDF). Control takes advantage of some approximation effects to help reduce the cost of evaluation, by only using reflected rays based on how far they are from the current surface - and that surface's roughness. [[Sjöholm et al. 2021]](https://alain.xyz#ref_mars2021)

![Global Illumination Screenshot](../../assets/0ef99311895ddf44.jpg)


**Ray Traced Global Illumination** renders in a single pass at half the native resolution (so `960x560`

), and is then denoised. Control uses precomputed voxel based global illumination performed with an offline path tracer based on static objects, which helps with resolving global illumination with objects far away. Near field indirect global illumination is used based on an object's BRDF for surfaces relatively close by.

This pass functions as indirect diffuse lighting as well as a kind of ambient occlusion, since the precomputed GI values are used when rays miss.

![Shadow Resolve Screenshot](../../assets/81fef8f57bc5ec9b.jpg)


Finally, **Contact Shadows** are rendered with the red channel representing spotlight index, and the green channel representing the point lights index of the current shadow sample.

All the denoising for these passes use data reprojected from previous frames and blurred with a *bilateral filter*, though each denoising pass is tuned slightly differently. Control uses a variant of the **Spatio-temporal Variance Guided Filter** (SVGF) [[Schied 2017]](https://alain.xyz#ref_schied2017), with a *firefly filter* and *spatial filter* that is based on 4 pixels around a given sample. There's some issues with reprojecting at times, and you can occasionally catch the difference between regions with high accumulation and regions with low. There's also some noise dancing in the end result but it appears really charming and adds to the game's ascetic.

Lighting is then composited to a single render target on a per object basis to overlay material data like albedo, and even volumetric lighting contributions. The image is finally tone mapped.

Control is full of technical art render passes that help it achieve it's overall look.

There's an **enemy pass**, where enemies are overlaid with various effects such as shields, which is also blurred to then give it the appearance of glowing.

| Velocity | Pressure | Divergence |
|---|---|---|
![]() | ![]() | ![]() |

This is followed by a **fluid smoke pass**, probably the highlight of the renderer's technical artistry. There's a feedback loop that uses *view space depth*, a *fluid buffer* that consists of the current frame, a *fluid velocity* buffer that changes over a few `DrawInstanced`

calls, *geometric velocity*, *fluid divergence*, and *fluid pressure* buffers to warp previous and current samples in real time, resulting in a screen space feedback effect that looks like rainbow gas. It's reminiscent of [ShaderToy](https://www.shadertoy.com/view/MdSczK)s that emulate gaseous flow. [[McAloon 2019]](https://alain.xyz#ref_mcaloon2019)

A separate pass uses this fluid warped render pass with a hiss mask to result in a final output image.

![LDSS Screenshot](../../assets/445762c7696c00ca.png)


Deep learning Super Sampling (DLSS) takes in a smaller input image, and upscales it to a target resolution. In this case, it took a `1080p`

input image and upscaled it to `4K`

. This is how the game is able to average above 30 fps at `4K`

on the 2070 Super.

While this screenshot doesn't include it, first a Sobol outline pass is overlaid on top of the final composite for objects that you can control or interact with.

![UI Screenshot](../../assets/ee175feedaf31e59.jpg)


UI particles such as health chips are rendered piecemeal by drawing a billboard, and UI elements such as your health are rendered piecemeal as well in screen space. During my testing I found some of the UIs would draw at the same time, like text elements for your objectives. Given that Control is using [Coherent Labs](https://coherent-labs.com/products/coherent-gameface/)'s HTML5 based **Gameface** Renderer for its user interface this makes sense, as the browser renderer could execute all of those draw calls with the CPU.

Finally the frame is finished and presented to the player.

Control was a really fun game, the *metroidvania style level traversal*, *a variety of unlockables*, and the mysterious, *government controlled setting* made for fun gameplay and a fascinating story. If you have any suggestions for a game to analyze, please let me know in the comments below or via Twitter.

Daniele Giannetti released a [GDC Talk that covers in great detail a single frame of Halo Infinite](https://www.gdcvault.com/play/1027657/One-Frame-in-Halo-Infinite)/

Angelo Pesce ([@kenpex](https://twitter.com/kenpex)) wrote a blog post on [Cyberpunk 2077's Renderer](http://c0de517e.blogspot.com/2020/12/hallucinations-re-rendering-of.html).

Emilio López ([@redorav](https://twitter.com/redorav)) wrote about the new Unreal Engine 5 renderer in his post: [A Macro View of Nanite](http://www.elopezr.com/a-macro-view-of-nanite/).

[Chapter 46 of Ray Tracing Gems 2](https://developer.nvidia.com/ray-tracing-gems-ii) discusses the ray tracer in Control in far more detail, the denoising section is particularly interesting.

NVIDIA has released an SDK to integrate Deep Learning Super Sampling [here](https://developer.nvidia.com/dlss-getting-started). AMD's [Fidelity FX Super resolution](https://github.com/GPUOpen-Effects/FidelityFX-FSR) is also available for developers to integrate into their applications.

I've also released other articles describing the renderers of different titles:

| [Sjöholm et al. 2021] |
| [Schied 2017] |
| [McAloon 2019] |