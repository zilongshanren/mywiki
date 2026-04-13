---
title: 'Deus Ex: Human Revolution - Graphics Study - Adrian Courrèges'
url: http://www.adriancourreges.com/blog/2015/03/10/deus-ex-human-revolution-graphics-study/
author: Adrian Courrèges
published: '2015-03-10'
source_blog: Adrian Courrèges
source_site: http://www.adriancourreges.com/
category: graphics
fetched: '2026-04-13'
---

** 2015/03/12: **

*Back online after*[Reddit](http://www.reddit.com/r/programming/comments/2yo9qa/deus_ex_human_revolution_graphics_study/)and

[Slashdot](http://games.slashdot.org/story/15/03/12/2227239/rendering-a-frame-of-deus-ex-human-revolution)killed my bandwidth with 30,000 visits in the last hours. Followed by[HN](https://news.ycombinator.com/item?id=9565891).

*2015/03/11:**Update with comments from*

[Matthijs De Smedt](https://mastodon.social/@anji).![](../../assets/2c1245cb7fd30e4e.jpg)


The original [Deus Ex](https://en.wikipedia.org/wiki/Deus_Ex) is among the most critically acclaimed PC games of its time and I spent countless hours helping JC Denton fend off the conspiracies of UNATCO or the Illuminati.

I never had the chance to play the second opus “[Invisible War](https://en.wikipedia.org/wiki/Deus_Ex:_Invisible_War)”, but I gave a shot to “[Human Revolution](https://en.wikipedia.org/wiki/Deus_Ex:_Invisible_War)” when it was released.
All I can say is: it lived up to the expectations!

Deus Ex: Human Revolution is a game released in 2011 by Square Enix, and developed by Eidos Montréal and Nixxes for the PC version.
It uses a modified version of the Crystal engine made by [Crystal Dynamics](http://www.crystald.com/) and was one of the earliest games to support DirectX 11.

It featured great graphics at the time (still looks good!), and it was as beautiful as light-weight: even low-budget video cards could run the game smoothly.

I was curious about the rendering process, so I spent a few hours reverse-engineering the game, playing with [Renderdoc](https://github.com/baldurk/renderdoc).

Here are the results of my investigation.

# How a Frame is Rendered

Below is the scene we’ll consider. This is an actual screenshot of the game: the final image presented on the player’s monitor.

![](../../assets/5456dd6d69071450.jpg)

At first glance, Deus Ex HR seems to use an approach similar to the [forward+ rendering](http://www.slideshare.net/takahiroharada/forward-34779335) technique.

Except that the game was developed years before forward+ became popular, actually it uses a precursor technique: the [“light pre-pass”](https://diaryofagraphicsprogrammer.blogspot.com/2008/03/light-pre-pass-renderer.html) approach.

### Normal + Depth Pre-Pass

The game renders all the visible objects, outputting only a [normal map](https://en.wikipedia.org/wiki/Normal_mapping) and a [depth map](https://en.wikipedia.org/wiki/Depth_map).

Transparent objects are not rendered.

Depending on the mesh, each triangle will be rendered as a flat surface (same normal for all the fragments of the triangle),
or can also be modulated by its own normal map.
For example, the hand sculpture has its own normal map modulating the final normals rendered to the buffer.

![](../../assets/f14e2ef4b654fd97.jpg)

![](../../assets/1741e53a8b0ba9c9.jpg)

![](../../assets/1b01417343b4aac7.jpg)

![](../../assets/9722f52e53b0e6c5.jpg)

While the normal map is being created, each draw call also generates at the same time the depth map:

![](../../assets/fc69db9bfd16e154.jpg)

This step is achieved in 166 draw calls.

### Shadow Maps

Shadows are generated through the [PSSM](https://developer.nvidia.com/gpugems/gpugems3/part-ii-light-and-shadows/chapter-10-parallel-split-shadow-maps-programmable-gpus) technique.

In short, the scene is rendered once for each light able to cast a shadow. In our case there are 2 light
sources: one in the small office behind the glass window on the right, and one on the top of the hand sculpture.

![](../../assets/2de53da1e77f4c92.jpg)

Each shadow map corresponds to a 1024x1024 square inside a 4096x3072 texture.

This pass is done in only 52 draw calls, much less than when rendering the full scene.

This is achieved by marking only the biggest objects as shadow-casters, skipping the smaller ones;
plus some frustrum culling is probably used to render only the objects visible from the light source.

After the different shadow maps are generated, the depth map and the shadow maps are combined to produce a shadow mask texture.

![](../../assets/f373ac5ae21259d7.jpg)

Each texel of the depth map is read, and its visibility is calculated for each light source.

The final result is outputted to an RGBA 8-bit texture which acts like a mask:

the default value is white `(1, 1, 1, 1)`

which means the texel is not shadowed by anything.
If a texel is in the shadow of a certain light source, a byte corresponding to this light source is set
to 0.

The shadow seen under the sculpture fingers is produced only by the light above them, not the office light,
which is why they appear blue-ish: RGBA of `(0, 1, 1, 1)`

.

This approach is able to handle 4 light sources at the same time, more if bit-masks are used instead of byte-masks.

Some small visible artifacts are typical of a PCF filtering technique.

** Update: ** Matthijs De Smedt

[pointed out](https://twitter.com/anji_nl/status/575392391550500864)that each channel for a light source does not only store 0 or 1 (it would be a waste to use 8 bits for this): during this pass the PCF of the pixel is also computed and stored inside these 8 bits.

Strictly speaking it is not really a mask: we have a value of 1 if fully lit, a value of 0 if fully occluded (in the middle of the shadow), and a value between 0 and 1 around the edges of the shadow (to give smoother borders).

### Screen Space Ambient Occlusion

By sampling the depth buffer, the [SSAO](https://en.wikipedia.org/wiki/Screen_space_ambient_occlusion) map is created.
A first “noisy” result is obtained through a pixel shader.
Then on DirectX 11 compatible cards, a compute shader is used to apply a blur with a 19x19 kernel and smooth the result.

On older cards, the blur is done with a pixel shader.

![](../../assets/188e933a924d5060.jpg)

![](../../assets/8e441705e973702f.jpg)

After the SSAO texture is generated its value is stored within the alpha channel of the normal map.

![](../../assets/9722f52e53b0e6c5.jpg)

Alpha: Ambient Occlusion

### Light Pre-Pass

Each point-light of the scene is rendered one by one.

The only inputs are the Normal+SSAO map and the depth buffer. The pixels affected by a light depends only
on the light radius and intensity.

![](../../assets/396f6c52e6aa07db.jpg)

![](../../assets/21db9cd3d8ed4703.jpg)

![](../../assets/dcdae6b32bd2015f.jpg)

![](../../assets/e8fd7ab78e615671.jpg)

The material reflecting the light is not important at this point yet, the information stored in the light
map is simply how much light is potentially reflected (and its color) for each pixel of the scene.

Later, this irradiance information will be useful to calculate how much light is actually reflected depending
on the mesh material and its specular property.

This scene uses 45 point-lights.

### Forward-Rendering of Opaque Objects

This is where the “actual” rendering finally happens.

Every single mesh of the scene is drawn to the screen. The final color of the pixel is calculated from:

- the Normal+SSAO map, the shadow-maps and mask, the light map
- the object’s own textures / material properties
- sometimes, a fake environment map (128x128 texture cube) to enhance reflections of the mesh

First, all the opaque objects are rendered:

![]() Normal+SSAO
|
![]() Depth
|
![]() Shadow
|
![]() Light
|
![]() Mesh textures and env map.
|

![](../../assets/3e73717d21c76e9c.png)


![](../../assets/cfbe3d24b07f60ac.jpg)

![](../../assets/d29f18462834c637.jpg)

![](../../assets/c81320cdca64a9f7.jpg)

![](../../assets/e510d27c22f289b4.jpg)

Notice that during this rendering step, the depth test function is set to `COMPARISON_EQUAL`

and not `COMPARISON_LESS`

.

Also, even if the depth test is enabled, depth-writing is disabled.

This is a trick to increase performance: remember that we already generated the scene depth buffer during the normal map creation.
So we already know exactly the final depth value a pixel is supposed to have. By discarding any fragment with the wrong depth,
we avoid heavy shading calculations which will just go to waste when a new fragment, closer to the camera, overrides with its own value.

This effectively achieves a rendering **with 0 overdraw**.

### Transparent Objects

This step renders decals (like signs on the wall, bullet impacts), transparent objects (like window glasses), or fake volumetric-lights (halo of spot-lights).

![](../../assets/e510d27c22f289b4.jpg)

![](../../assets/691610126e854850.jpg)

![](../../assets/3ee9b127080850e0.jpg)

The depth function is of course turned back to `COMPARISON_LESS_EQUAL`

because we don’t have yet any information about the position
of transparent objects at this point. The depth-write stays disabled, to make sure a transparent mesh close to the camera does not cancel
the rendering of another transparent mesh further behind.

The volumetric-lights look very nice: these are simply a group of “sprites” rendered in 3D in the scene at the good position.
They are not single-sprite-billboards always facing the camera like you could expect, they’re actually [icosahedrons](https://en.wikipedia.org/wiki/Icosahedron) 3D meshes scaled correctly to represent the light halo.
The choice of icosahedrons is a compromise: approximating a sphere with as little geometry as possible.

Also these meshes don’t rely on any texture: the “halo” is calculated 100% procedurally. The pixel shader, by sampling the depth map,
can know how far the current pixel is located from the light source, and compute the final color
value based on this distance.

Here is a wireframe representation of the meshes used to create the effect:

![](../../assets/5cf6e1c6c7b77bb0.jpg)

For reference the rendering of opaque and transparent objects is done in 253 draw calls.

### Light Bloom

To apply a [bloom effect](https://en.wikipedia.org/wiki/Bloom_%28shader_effect%29), we need to know the set of pixels with a very strong light intensity.

Deus Ex HR uses a simple LDR workflow, there is no HDR buffer on which we could apply a bright-pass filter.

But actually, while performing the previous pass, for each mesh an extra information was being outputted to the alpha channel: the emissive intensity of the mesh.

![](../../assets/ab9c5a5ed089ec17.jpg)

This is enough to create a bloom layer: the idea is to simply apply a [Gaussian blur](https://en.wikipedia.org/wiki/Gaussian_blur) with a large radius.

The image is first downscaled to half, then one-fourth of the original size (to make blurring more efficient) and finally blurred.

![]() Scale x0.25
|
![]() Apply blur |
![]() |

After we obtain the blur of the bright areas, we simply need to blend it on the top of the original scene. The blending is additive, because we only want to add brightness to some areas, never darken anything.

![](../../assets/5590d91197abdb96.jpg)

![](../../assets/7699a001a99c55fa.jpg)

### Anti-Aliasing

To smooth-out the jagged lines on the edge of the meshes, Deus Ex HR supports different techniques of anti-aliasing like DLAA, MLAA, FXAA…

Here’s an overview of the correction when using [FXAA](https://en.wikipedia.org/wiki/Fast_approximate_anti-aliasing):

![]() FXAA Off
|
![]() |
![]() FXAA On
|

### Color Correction

We’re almost done for the scene, it’s already looking pretty good.

The last touch is a bit of color correction: [gamma correction](https://en.wikipedia.org/wiki/Gamma_correction) is applied and then a special pixel shader
is used to give a yellowish tone to the scene.

The yellow tint, sometimes referred to as “gold filter”, is a bit like the trademark of the game.

For those who don’t like it, [some mod](https://kotaku.com/5843146/deus-ex-mod-removes-gold-filter-game-suddenly-looks-even-better/) exists to disable it.

![](../../assets/7699a001a99c55fa.jpg)

![](../../assets/539edd55fee89b52.jpg)

### User Interface

The final step is to render the UI on the top of the view. This is done in 317 draw calls.

![](../../assets/539edd55fee89b52.jpg)

![](../../assets/5456dd6d69071450.jpg)

And we’re done! The texture is finally copied to the back-buffer and presented to the user.

### Timeline

Just to give a rough idea of the cost of each step of the process, here is a quick comparison of the time required to process the steps.

![](../../assets/088f52dcb8e02e64.png)


# Bonus Notes

### Depth Of Field

I don’t think the [DoF](https://en.wikipedia.org/wiki/Depth_of_field) effect is ever used during the gameplay phases, but it is always present during the cinematics or the dialogs.
The technique used in Deus Ex HR is the most basic you could think about: a 2-layer DoF, using Gaussian blur.

![]() Original Scene
Downscale and blur
![]() |
|
![]() #1: Scale x0.5
![]() #2: Horizontal Blur
![]() #3: Vertical Blur
|

After we obtain 2 versions of the scene: the original crisp one and a blurred out-of-focus version, a pixel shader will [lerp](https://en.wikipedia.org/wiki/Linear_interpolation)
between the 2 layers, depending on the pixel depth.

Too near or too close, the shader will use the blurred image; but at the right in-focus distance, the shader will use the original image.

![]() Original
|
![]() Blur
|
![]() Depth
|

![](../../assets/3e73717d21c76e9c.png)


![](../../assets/ede890a542d2658b.jpg)

![](../../assets/5de2d34213c4d4cf.jpg)

The Gaussian blur can be performed on compute shaders on compatible hardware, with a fallback to pixel shaders.

### Silhouette Effect

![](../../assets/b60bcb45b3aed36f.jpg)


In some games, the effect is very basic: sometimes the mesh is simply drawn at a bigger scale outputting a constant color; sometimes after the whole scene is rendered the relevant mesh is drawn again with some color and alpha modulation on the top of the final image.

But in Deus Ex HR the silhouette effect is perfectly integrated: any occluder in front the interactable mesh affects the final silhouette. Note how the shiny outline does not only follow the shape of the container but also the one of the policeman in front of it.

So how is such effect achieved?

It’s a very simple trick. Remember the light map containing all the irradiance information for each pixel of the scene?
We only need the RGB channels to store the irradiance, the alpha channel is not used. And this is precisely in the alpha channel
that the game stores information about pixels belonging to an interactable object.

![](../../assets/500e736314a53cdb.jpg)

![](../../assets/23258774e746651a.jpg)

Well this is the only information we need to draw the silhouette: after the scene is rendered, but before the bloom, an extra pass occurs.
This pass draws an overlay on the top of the scene: the pixels marked as interactive are rendered with a yellow tint modulated by a texture with some triangles-pattern,
finally a [Sobel](https://en.wikipedia.org/wiki/Sobel_operator)-like edge-detection operator is used to draw the silhouette.
Drawing the silhouette also outputs to the alpha channel of the render target: this is where the
information about the brightness is located. The bloom effect will then make the silhouette shine.

![](../../assets/b9b08abfb11655c5.jpg)

![](../../assets/b60bcb45b3aed36f.jpg)

# Further Readings

There are still many things that could be said about Deus Ex HR, if you want to know more you can check out some of the links below.

[Deus Ex is in the Details](http://twvideo01.ubm-us.net/o1/vault/gdc2012/slides/Programming%20Track/DeSmedt_Matthijs_Deus%20Ex%20Is.pdf) – GDC 2012 presentation by [Matthijs De Smedt](https://twitter.com/anji_nl).

[The Design Challenges of Deus Ex: Human Revolution](http://gdcvault.com/play/1015489/Reimagining-a-Classic-The-Design) – GDC 2012 presentation by François Lapikas.

[Building the Story-driven Experience of Deus Ex: Human Revolution](http://www.gdcvault.com/play/1015027/Building-the-Story-driven-Experience) – GDC 2011 presentation by Mary DeMarle.

More discussion on this very topic: [Slashdot](http://games.slashdot.org/story/15/03/12/2227239/rendering-a-frame-of-deus-ex-human-revolution),
[Hacker News](https://news.ycombinator.com/item?id=9565891),
[Reddit](http://www.reddit.com/r/programming/comments/2yo9qa/deus_ex_human_revolution_graphics_study/).