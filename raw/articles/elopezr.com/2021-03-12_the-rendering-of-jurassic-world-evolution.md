---
title: 'The Rendering of Jurassic World: Evolution'
url: https://www.elopezr.com/the-rendering-of-jurassic-world-evolution/
author: Redorav
published: '2021-03-12'
source_blog: The Code Corsair
source_site: http://www.elopezr.com
category: game programming
fetched: '2026-04-13'
---

Jurassic World: Evolution is the kind of game many kids (and adult-kids) dreamed of for a long time. What’s not to like about a game that gives you the reins of a park where the main attractions are 65-million-year-old colossal beasts? This isn’t the first successful amusement park game by [Frontier Developments](https://en.wikipedia.org/wiki/Frontier_Developments), but it’s certainly not your typical one. Frontier is a proud developer of their Cobra technology, which [has been evolving](https://www.frontier.co.uk/node/639) since 1988. For JWE in particular it is a DX11 tiled forward renderer. For the analysis I used [Renderdoc](https://renderdoc.org/) and turned on all the graphics bells and whistles. Welcome… to Jurassic Park.

**The Frame**

It’s hard to decide what to present as a frame for this game, because free navigation and dynamic time of day means you have limitless possibilities. I chose a moody, rainy intermediate view that captures the dark essence of the original movies taking advantage of the Capture Mode.

**Compute Shaders**

The first thing to notice about the frame is that it is very compute-heavy. In the absence of markers, Renderdoc splits rendering into passes if there are more than one Draw or Dispatch commands targeting the same output buffers. According to the capture there are 15 compute vs 18 color/depth passes, i.e. it is broadly split into half compute, half draw techniques. Compute can be more flexible than draw (and, if done correctly, faster) but a lot of time has to be spent fine-tuning and balancing performance. Frontier clearly spared no expense developing the technology to get there, however this also means that analyzing a frame is a bit harder.![](../../assets/7947106a6f3da1f8.png)


**Grass Displacement**

A big component of JWE is foliage and its interaction with cars, dinosaurs, wind, etc. To animate the grass, one of the very first processes populates a top-down texture that contains grass displacement information. This grass displacement texture is later read in the vertex shader of all the grass in the game, and the information used to modify the position of the vertices of each blade of grass. The texture wraps around as the camera moves and fills in the new regions that appear at the edges. This means that the texture doesn’t necessarily look like a top-down snapshot of the scene, but will typically be split into 4 quadrants. The process involves these steps:

- Render dinosaurs and cars, probably other objects such as the gyrospheres. This doesn’t need an accurate version of the geometry, e.g. cars only render wheels and part of the chassis, which is in contact with grass. The result is a top down depth buffer (leftmost image). If you squint you’ll see the profile of an ankylosaurus. The other dinosaurs aren’t rendered here, perhaps the engine knows they aren’t stepping on grass and optimizes them out.
- Take this depth buffer and a heightmap of the scene (center image), and output three quantities: a mask to tell whether the depth of the object was above/below the terrain, the difference in depth between them, and the actual depth and pack them in a 3-channel texture (rightmost image)

An additional process simulates wind. In this particular scene there is a general breeze from the storm plus a helicopter, both producing currents that displace grass. This is a top down texture similar to the one before containing motion vectors in 2D. The motion for the wind is an undulating texture meant to mimic wind waves which seems to have been computed on the CPU, and the influence of the helicopter is cleverly done blending a stream of particles on top of the first texture. You can see it in the image as streams pulling outward. Dinosaur and car motion is also blended here. I’m not entirely sure what the purpose of the repeating texture is (you can see the same objects repeated multiple times).![](../../assets/be9e124ff1e5b10d.png)


**Tiled Forward Lighting**

One thing to explain before we get to the geometry prepass is tiled forward lighting. We talked about tiled in [Rise of the Tomb Raider](https://www.elopezr.com/the-rendering-of-rise-of-the-tomb-raider/) but there’s some differences. Tiled lighting in JWE splits the screen into 8×8 pixel tiles extruded towards the far plane to create subfrustums. A compute shader is dispatched per tile, which reads a big buffer with data for all lights. Intersecting each light against the subfrustum of a tile gives you a list of lights for that tile. In the lighting pass, each pixel reads the tile it belongs to and processes each light. Reducing the number of lights per tile is very important in a forward engine, where calculations happen as geometry is rendered and decisions per object would be too coarse and greatly impact performance. It’s worth mentioning that tiled lighting is particularly effective when there are many small lights, rather than a few big ones. JWE is full of small lights which makes it a suitable technique.

An additional consideration is that tiles in screen space extend from the camera to the far plane. We know lights may be occluded by opaque objects, so JWE uses the information from the depth buffer to reduce the range to the regions it cares about. To that end it creates a min-max depth buffer that we’ll explain later. A lot has been written about this so I’ll throw a couple of extra links [here](https://wickedengine.net/2018/01/10/optimizing-tile-based-light-culling/) and [here](https://leifnode.com/2015/05/tiled-deferred-shading/).

**Depth Prepass**

As is customary in many games, a depth prepass is performed on the main geometry. All geometry is submitted at this point in the frame, in contrast to other engines where simpler geometry (or none at all) can be submitted. It outputs some stencil values too, for many things in fact: to mark dinosaurs, foliage, buildings, terrain, every type of object seems to have its own id. As it effectively submits geometry more than once for processing, there must be good reasons for it.


- Tiled rendering splits the screen into small equally-sized tiles and assigns lights to each tile. As well as splitting in screen space, tiles have a depth range (to avoid processing lights), and to obtain this range the depth buffer is used. Minimum and maximum values per tile are computed to determine the range
- Even though the previous point says that full depth information is necessary, in a deferred lighting engine that wouldn’t strictly be true. Tile classification could still happen after the GBuffer has been rendered, where all the depth content would be available. However, forward lighting happens when we render the object in the main lighting pass, and by that point we need to have done tile classification already
- A depth prepass helps with a GPU optimization called Early Z. For a forward engine this pass is actually quite important as the pixel cost of the main lighting pass is very high. Early Z helps the GPU avoid overdraw during the lighting pass by using the information from the pre-populated depth buffer to discard pixels behind other surfaces

One way to compute the minimum and maximum for a tile is what is called a Min-Max Depth Buffer. This is essentially two buffers, one containing the closest depth for a region of the screen, the other containing the maximum. A straightforward way of doing this is to compute mips in succession, i.e. Mip 0 -> Mip 1, then Mip 1 -> Mip 2, etc. It’s very interesting to see what this process does to the birdcage: the closest depth (top) makes the birdcage look solid, whereas the furthest depth (bottom) makes the birdcage disappear completely! Intuitively this makes sense, and you can now see what each tile represents. Note that JWE uses [reverse depth](https://developer.nvidia.com/content/depth-precision-visualized), where the closest depth is represented by a 1, and the furthest by a 0. This distributes depth values better and helps avoid z-fighting at far distances.

**Thin GBuffer**

The game renders the geometry again, after the depth prepass, outputting pixel normals + roughness in one texture and motion vectors in another. The main reason to have to do this is so that we can compute effects like SSAO, SSR, Temporal AA and other postprocesses that need these quantities. It’s a tradeoff that forward rendering engines have to do to be able to offload some of the work outside the main shader and compute fullscreen effects. Rendering the geometry again is a high price to pay but necessary, an alternative would be to output these quantities in the depth prepass.


**Atmospheric Simulation and Fog**

JWE has a realistic atmospheric simulation to go with its weather system that runs in several steps. One of the first is to compute a transmittance look up table (LUT). Transmittance is a way of expressing how dense the atmosphere is, and can be modeled as a function of height from the surface of the earth, and elevation angle, hence a 2D texture.

There are some nice God Rays/light shafts caused by mountains, and the solution is actually tailored to them. A pass renders only the mountain meshes to a custom depth buffer. This depth buffer is split into 4 sections, and each frame only one of those sections is rendered, distributing work across frames. It is processed and produces a single orange looking texture. This texture stores the first two moments of a shadow map, essentially the depth value and the depth squared. These two quantities are blurred, giving it that fuzzy look. This is very typical of a family of techniques that precompute blurred shadows, such as [variance mapping](https://graphics.stanford.edu/~mdfisher/Shadows.html) and [moment shadow mapping](https://cg.cs.uni-bonn.de/en/publications/paper-details/peters-2015-msm/). It’s an interesting approach because the rest of the shadows do not use it. Typically you’ll go with pre-blurring shadows if a raymarching pass is going to happen as it adds stability.

This is used in conjunction with the transmittance texture to compute fog both for reflection/diffuse cubemaps and for the entire scene at low resolution, upscaled later to fullscreen. Low resolution saves bandwidth and is suitable because fog is generally low frequency. Note the screen space fog texture has content from previous frames. This is an optimization if you can get away with it because you don’t need to clear the texture, clawing back precious fractions of millisecond. The texture is RGBA16F and includes inscattering (the “fog color”) in rgb and outscattering (the “fog amount”) in the alpha channel, and is read in the main lighting pass to composite with opaque geometry.


**Reflections**

There are three systems to produce reflections in JWE: cubemaps, screen-space reflections and planar reflections. We’re going to go through them in sequence and see how they all fit together.

**Cubemap Generation**

One of the first color passes to happen in the frame is a cubemap face rendering. In my capture, one face of two different cubemaps is rendered (both of them include depth + lighting). Interestingly, the sky is colored ff00ff pink in some of the faces, as it turns out cubemaps are blended later based on this mask and only one final cubemap is ever used. Because rendering of these cubemaps is expensive, the cost is amortized across frames and each frame only a subset of the full cubemap is produced. The cubemaps also aren’t very detailed: they include the sky (produced by a compute shader we’ll mention in a moment), low poly landscape/foliage and lights.


Cubemaps are used for two purposes: one is to generate reflection captures (for specular lighting), the other is to generate ambient lighting (a process called irradiance cubemaps, for diffuse lighting). The image sequence shows the blending of two different cubemaps which is not correct but illustrates the purpose (keep in mind one of them is still being processed!). The last sequence is irradiance generation which is used to integrate the lighting coming from multiple directions. A different process also downsamples the cubemaps, this time to approximate a rough specular response, using the split sum approximation described by [Brian Karis](https://twitter.com/briankaris) in [Real Shading in Unreal Engine 4](https://cdn2.unrealengine.com/Resources/files/2013SiggraphPresentationsNotes-26915738.pdf).

**Screen-Space Reflections**

One of the most popular ways of doing reflections these days, SSR is present in many games. The particular approach JWE has taken I have seen used for games like Killzone Shadow Fall and Assassin’s Creed Black Flag, but people have used this technique in different ways. An initial compute pass takes in the pixel normals and depth buffer, as well as a small randomization texture, and outputs the UV of the reflection, reflection depth and a confidence value to a half resolution RGB10A2 texture. The confidence value is binary, and measures how sure we are that we have found a valid reflection. Invalid reflections can happen for a multitude of reasons, either because the ray went off screen, reflections are blocked by an object, or even if we’ve decided some surfaces aren’t worthy of reflections.


One valid question to ask is: what do we use as the source of reflections? In a deferred engine, there is some hope to compute many parts of the lighting equation before SSR happens, but in a forward engine that would be very hard. The answer here is that we sample last frame’s lighting buffer. It has all the lighting, including transparent objects, fog, etc. The main caveat is that when the camera moves, the current pixel shouldn’t sample last frame’s buffer directly, but needs to go through a process called [reprojection](http://s3.amazonaws.com/arena-attachments/655504/c5c71c5507f0f8bf344252958254fb7d.pdf?1468341463). We know where the camera was last frame so we can modify the UV we use to sample it. For moving objects, one would normally use motion vectors as well to do the reprojection, but JWE doesn’t do this. Once we have all the information, there is a dilation/blurring process for the highest mip available, and a mipchain generation to simulate roughness.


**Planar Reflections**

There is a lot of water in JWE (dinosaurs need somewhere to drink and swim). It turns out water uses a pretty classic, but effective, technique: planar reflections. The first step renders a full resolution depth pre-pass where objects that need to be reflected are rendered “upside down” from the point of view of an imaginary camera that is below the reflection plane looking upwards. The objects rendered here are lower quality: for example, trees are plain alpha tested quads that read from a tree atlas, and dinosaurs are low poly. In the same spirit as tiled lighting, a step computes the min and max depth buffer, for the tiled light classification. The first object is a fullscreen quad for the sky, which takes a 128×128 cubemap as input with the sky, sun and low resolution clouds. It takes advantage of the prepass to only render where there are no opaque objects occluding it. The lighting pass happens in a similar way as the main pass.


**Shadow Mapping**

JWE takes the fairly standard cascaded shadow mapping approach for its main directional light, of which there’s only ever one. There’s plenty of point lights around for the security fences and spotlights for the car headlights, but none of them are shadowed. It would probably be quite taxing to render that many shadowed lights, especially considering how geometry-heavy this game is. The cascades for the directional light are contained in a 2D texture array that contains 4 slices, and use reverse depth for rendering (1 is near plane, 0 is far plane). The capture I’m presenting is not very exciting as the directional light is fully occluded, so here’s what it looks like in another sunny capture.

As you can see, there are a lot of black regions where no geometry has been rendered. I think these regions are overlaps between cascades where it would make no sense to render, plus some form of exclusion outside the frustum.

**Shadow Mask**

This shadow map isn’t used directly during the lighting pass. A fullscreen pass that produces a shadow mask is used instead. This helps reduces the computational load on an already packed main lighting pass. The shadow mask is produced using a compute shader that takes in the depth buffer and the shadow cascades, to produce an image similar to this. Again this shadow mask is not the same as our original capture as the rainy scene has no direct shadows.

**Ambient Occlusion**

JWE takes the same approach as Rise of the Tomb Raider for its highest quality ambient occlusion, HBAO, so I will only touch on it briefly here. The screen is divided into 16 textures, and each computes ambient occlusion using a fixed set of random directions. The texture is then combined back and blurred. Many games use this technique as [NVIDIA](https://www.nvidia.com/en-gb/geforce/technologies/hbao-plus/technology/) popularized it and even provide source code and ease of integration for its licensees. At lower qualities the ambient occlusion uses a slightly different multipass technique that struck me as similar to one developed by [Intel](https://software.intel.com/content/www/us/en/develop/articles/adaptive-screen-space-ambient-occlusion.html) although I cannot say for certain. The ambient occlusion is packed alongside the shadow mask so that the main shader samples the texture once.

**Main Pass: Opaque + Transparent**

Opaque objects are rendered first, where the early Z technique we mentioned earlier kicks in. The rasterizer state can actually be set to Equal, i.e. pixels whose depth is equal to the one already present in the depth buffer are rendered, otherwise discarded. This cuts pixel shader cost to only the visible pixels.


**Bug alert!** Car headlights are supposed to have a neat volumetric effect applied to them. However, for some weird reason, they are rendered **before** all the opaque objects in the frame so they end up completely occluded! Look carefully at the carousel above to see this in action. This highlights the importance of proper ordering in the frame. The transparent pass comes right after that and conceptually is not very different, other than the blend modes change to mimic glass and they are sorted back to front. I hacked a quick composite to show what the car headlights should have looked like.

Forward rendering can be powerful in terms of shader flexibility: since everything happens inside the main pass, every attribute of the material is present, and lots of possibilities in terms of lighting models (hair, cloth) and material variety come more naturally than in a deferred pipeline. This flexibility comes with a few performance implications: expensive geometry passes and feature coupling: everything from material evaluation to lighting, reflections, global illumination, sampling fullscreen textures like ambient occlusion, SSR, shadows, etc. is packed in a single, enormous, shader.

In terms of performance, a relatively straightforward lighting pass shader in JWE has around ~600 instructions, while for comparison a fairly average GBuffer shader in Ryse: Son of Rome is ~70 instructions. Very long shaders tend to suffer from a GPU phenomenon called low occupancy, where the GPU is blocked due to resource contention. In general, low occupancy is not a good thing to have, although reality is always more complex. You can read more [here](https://www.eecis.udel.edu/~cavazos/cisc879/Lecture-10.pdf). To alleviate this, forward engines tend to pull features out of the main pass. As we saw, to implement SSAO and SSR, normals and roughness were output in an extra pass, duplicating vertex and pixel work.

**Rain**

Rain is an important part of the weather system, where a series of processes work together to give a convincing illusion.

**Rain Ripples**

A compute shader calculates rain textures later applied as normal maps e.g. on the landscape. The source for the rain is a couple of ripple textures containing the height of the rain waves created by the impact of a rain drop. From a height map it is straightforward to derive a normal map, which then gets blended with that of the target. The texture is tileable so it can be repeated many times across a given surface. The reason they come in pairs is because they are consecutive frames in an animation loop and they are being blended for a smoother animation. A series of compute shaders produces the mipmap chain for those textures.

**Rain Drops and Splashes**

There are several rain layers that are all rendered as camera facing rectangles with rain textures in them that simulate falling rain. A rain generation compute pass drives the number of rain drops depending on how intense the rainfall is.


I call rain puffs the very light cloud of rain you get when rain is decomposed into multiple droplets and almost floats after impacting. The texture for these looks like fireworks, it’s an interesting take on it. I also call rain sheet a very large polygon that has a multitude of rain drops in it simply scrolling downwards.

The source textures for each of these stages are relatively straightforward. However there is an interesting twist on the rain splash texture, where it uses a clever lighting technique to give it more volume. It is essentially a 3 channel texture where each channel gives some information on what the drop looks like lit from the left, from the middle, and from the right. Remember we’re rendering a flat quad! During rendering, we know where the light source is with respect to the normal vector of the quad, and based on this we can blend the channels appropriately, giving more weight to the channel that more accurately matches the light direction. See below to see it in action. All we’re doing is blending 3 images, and already it looks like a light is moving left and right.


Splashes are also animated when they impact, its animation sourced from a big spritesheet that contains variations for 8 rain splash types and is composed of 8 frames, an example of which is shown below.

**Temporal AA**

JWE uses Temporal AA as its antialiasing technique. Aliasing produced by foliage, small geometry, thin cables, and small lights is very hard for the alternatives to reduce in the general case. TAA belongs to a family of techniques called [temporal supersampling](https://bartwronski.com/2014/03/15/temporal-supersampling-and-antialiasing/). These distribute computations across multiple frames and bring those results together to improve quality. For TAA this means the camera is constantly jittering, producing a slightly different image every frame and revealing detail that isn’t present in others. Accumulating these results gives a better image.


There are a few edge cases we need to consider:

- If the camera moves, we blend two unrelated images introducing ghosting. We can fix this using motion vectors, output during the thin gbuffer pass. They are an offset in screen UV space that tells us where in the previous frame a pixel was
- If objects are occluding something one frame but not the next. This is called disocclusion
- If an object’s previous position is outside the screen
- Jittering can flicker in static images, caused by very thin geometry or high frequency normal maps

All these questions are answered differently in different engines. Despite all its imperfections, TAA creates a much better resulting image than the alternatives. The before and after results speak for themselves.

**Bloom, Lens Dirt and Tonemapping**

Bloom uses the very classical but no less mesmerizing technique of downscale + upscale, the original implementation of which is often credited to [Masaki Kawase in 2003](http://genderi.org/frame-buffer-postprocessing-effects-in-double-s-t-e-a-l-wreckl.html) and henceforth called [Kawase Blur](https://software.intel.com/content/www/us/en/develop/videos/improving-real-time-gpu-based-image-blur-algorithms-kawase-blur-and-moving-box-averages.html). The way it works is it creates an image by thresholding the main lighting buffer (e.g. take all values above 1) and successively blurs + downscales that texture until it gets to an unrecognizable blob. From there it starts upscaling each mip while blending with the previous one. It does this all the way up to Mip 1 and finally composites it with a texture containing camera imperfections and applies tonemapping.


We’ve seen color cubes in the past in [Shadow of Mordor](https://www.elopezr.com/the-rendering-of-middle-earth-shadow-of-mordor/), in this case tonemapping is packed in a cube instead of executed via a formula, which gives it a peculiar saturated orange/green color. There’s another color correction pass right after, but the concept is similar. With this, the frame essentially has ended.

**Blur and UI**

The main screenshot has no UI as I hid it for the beauty shot, but there is one during gameplay and it’s actually quite nice. One of the last steps produces a blurred downscaled copy of the lighting buffer later used in the UI to give it a frosted, translucent look.

**Top-down Color Map**

A very interesting process happens at the end of the frame. A top-down “color” map is produced from the contents of the lighting and depth buffers. The breakdown is:

- Dispatch 240×136 threads. Each thread expands to one of every 8 pixels in the depth buffer
- Read depth, and reconstruct the world position of the pixel
- Read the lighting buffer, compute the luminance and manipulate the color based on some formulas
- Read stencil and based on some criteria, output the values. The criteria seems to be if the object is static, and the depth is not too far away or something similar
- The output color is current color plus the difference between the new and old, and the last channel is luminance

The essence of this algorithm, as far as I can tell, is to build a color map based on what you are seeing at the moment! As you move around the world, the top-down content slowly gets populated. I’m not sure where this is used (maybe next frame? maybe bounced lighting?) as it’s done at the very end and not used again. I guess code, uh, finds a way.

With this we end our analysis, we’ve covered a lot and I hope you enjoyed it and perhaps even learned something. I’d like to thank the team at Frontier for their excellent games, and as always mention [Adrian Courrèges](http://www.adriancourreges.com/), who first inspired me to write these with his own, as well as hosts a [neat page](https://www.adriancourreges.com/blog/2020/12/29/graphics-studies-compilation/) where he keeps all the different studies from other people.

Wouldn’t it be faster to combine depth prepass and thin gbuffer passes? I know that then depth prepass is no more depth-only and loses some of its perf benefits, but on the other side rendering geometry in THREE passes sounds insane.

Hey WSte, thanks for your comment.

I agree and I think 3 geometry passes are way too many. For me it’s either a clever depth prepass with conservative geometry + a gbuffer geometry pass, or go full visibility buffer. Maybe they ended up changing that in JWE2 and it was a transitional thing. Changing an old forward engine to be fully deferred is a very complicated task so they might have taken it in steps. It would be an interesting experiment to put JWE2 through Renderdoc