---
title: Anatomy of a frame in AnKi
url: https://anki3d.org/anatomy-of-a-frame-in-anki/
author: Panagiotis Christopoulos Charitos
published: '2019-07-18'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

This is going to be long so let’s start with the purpose of this article which essentially is to analyze a single frame from the renderer’s point of view. It will briefly describe all the passes and how the data get transformed in order to produce some pretty pixels into the screen.

Some disclaimers before we start:

- It’s not about a perfect renderer. There isn’t such thing. Renderers should adapt to the context (type of game, platforms etc).
- It’s not about a perfect renderer even for my context and standards. I always have ideas for further improvements and I have kept postponing this article until they get materialized. But then new ideas come up and I felt I shouldn’t wait any longer.
- It’s
**not**about a mobile (GPU) friendly renderer. It’s a desktop oriented one. - It doesn’t reflect how the renderer will look like in a month from now. I tweak it almost daily.

These are some terms used throughout this article:

- Graphics pass: A series of drawcalls that affect the same output. In Vulkan terminology it’s a VkRenderPass pass with a single subpass.
- Compute pass: A compute job or a series of compute jobs that affect the same output.
- Render target: Part of the output of a graphics render pass.
- Texture: A sampled image that is used as input in compute or graphics passes. Some render targets may be used as textures later on.
- GI: Global illumination.

## Cluster binning

AnKi’s renderer is using clustered deferred shading so one of the first steps is to bin various primitives into a number of clusters. This step happens in the CPU and this is the list with the primitives that take part in the binning process:

- Point lights
- Spot lights
- Decals
- Fog density probes
- Reflection probes
- Diffuse GI probes

I won’t go into details on how binning works or what kind of data structures are populated. Just wanted to list the primitives since this information is relevant later on.

## Generic compute (GPU particles)

The first pass that will run is a series of compute jobs requested by the scene-graph. At the moment its primary consumer is GPU particle simulations.

Every (visible) GPU particle emitter will invoke a compute job that will perform the particle simulation. The simulation will use the previous frame’s depth buffer (actually a down-scaled version of it. See the *Depth downscaling* stage described bellow) for collision detection. If the particle’s new position falls behind the depth buffer then we assume that it collided with some surface.

The depth buffer will also be used to calculate the normal at the point of impact. The normal is then used by the simulation to bounce the particles against the surface.

![](../../assets/8b50fd25049f846b.png)

## GBuffer pass

Naturally, in deferred shading one of the first passes that run is the population of some sort of GBuffer.

At the beginning of this graphics pass we perform a light **depth pre-pass** where some of the most important visible objects are drawn with a simplified fragment (pixel) shader.

In AnKi’s case the **GBuffer** consists of 4 render targets plus depth. The first render target is a R8G8B8A8_UNORM and it contains the diffuse color and a subsurface term (more on that later).

![](../../assets/8e32720b40b32493.png)

The 2nd render target is a R8G8B8A8_UNORM as well and it contains the roughness, metallic and Fresnel terms. The last component contains some sort of scale for the emission.

![](../../assets/c4b1941affeaba58.png)

The 3rd render target is a A2B10G10R10_UNORM_PACK32 and it encodes the normal (in world space) in the G, B and A components. The two bits of A component hold the sign of the normal’s Z.

The R component holds another part of the emission. You may wonder if that makes sense. Firstly, the emission is not float and secondly it’s not a 3 component value. I’ve decided to cheat a bit so the stored term is multiplied by a max value and then with the diffuse term. That will give the actual emission to be used.

```
actual_emission = gbuffer.diffuse
* (gbuffer.emissionScale * ABSOLUTE_MAX_EMISSION * gbuffer.emission)
```

![](../../assets/c29a6fb7f5594bf9.png)

The last render target holds the velocity in a R16G16_SNORM texture.

![](../../assets/b4e7ca2639dd685c.png)

## Deferred decals

Once the GBuffer is populated there will be an additional graphics pass that will apply the decals into some of GBuffer’s render targets. We want the depth buffer to be available that’s why this pass is separate from the GBuffer pass.

The decal textures are all stored into a couple atlases. The first atlas contains the diffuse term and the second the metallic factor and roughness. The decals are binned into clusters as we already mentioned. This pass draws a single fullscreen triangle and appends to GBuffer using blending. Discard is being used to minimize unnecessary blending.

## Depth downscaling

The depth buffer will be downscaled up to a certain size. This is a series of compute passes that read some input and compute the max depth (in AnKi the depth is 0.0 near the camera and 1.0 far of the camera). This stage is like a fancy mipmaping but each compute job will populate 2 mipmap levels at once.

The final compute job will also output the depth values into a host visible storage buffer. These values will be used by the scene’s visibility tests a few frames down the line (C-buffer technique [Kasyan 2011]).

Another reason for this downscaling is that some of the following passes (and some of the previous as we’ve seen) require the depth buffer in order to reconstruct the world position or normal or whatever. So, instead of providing the actual depth buffer we use a downscalled version of it in order to save some bandwidth.

## Shadows

The renderer is being given a list of lights that cast a shadow. Those can be a single directional light (sun) with a variable number of cascades, a number of spot lights and maybe a few point lights. The final result is generated in two separate passes. The first goes through the lights and populates a scratch depth buffer and the second one takes that scratch depth buffer, linearizes the depth, does some blurring and populates another image (a texture atlas). The linearization and the blurring is because AnKi is using **exponential shadow mapping** (ESM). So, let’s name the first pass *scratch* and the second *ESM resolve*.

The first step of the shadow generation happens in the CPU. This is a complex process where the renderer goes through the (visible) lights that cast shadow, determines whether they need re-rendering and allocates tiles into the scratch and ESM atlas textures.

The renderer has a cache for the lights it encounters across frames. This caching system is based on timestamps and UUIDs (a unique uint64 number). Every light should have its own UUID and if that cache encounters a new UUID then it knows that this light is new and that its shadows need to be re-rendered. If the light’s UUID is in the cache the renderer checks the light’s timestamp against the cache’s timestamp. If the cache has an outdated version of the shadows then the the shadows will be re-rendered. If the cache is full then it will kick some lights that weren’t visible for a few frames. It’s a complex system and one paragraph is not enough to describe it but you get the idea.

After the CPU work is done the *scratch* pass will render what’s visible from the lights’ PoV and populate the temporary scratch atlas. The scratch atlas is divided into tiles and the tiles into subtiles and the subtiles into sub-subtiles. Shadows that need higher detail are rendered into the higher levels of this hierarchy. For example the first 2 cascades of the directional light are rendered into 512×512 tiles and the rest in 256×256. Distant point lights will use the small tiles. So the hierarchy level that will be chosen depends on the light distance from the camera, the size of the light and its type. This is quite flexible.

![](../../assets/dbeb93c6be8479cc.png)

The next step reads the scratch depth buffer, linearizes the depth and does a 9-tap blur before it outputs it to a larger atlas. This is the atlas that will be used by the following passes.

![](../../assets/f9586eca100ce0d7.png)

## Screen space ambient occlusion

SSAO is being done in two compute passes and in 1/4 of the resolution. The first pass:

- Has access to the depth buffer only (actually a mipmap level that the
*Depth downscaling*stage produced). - It doesn’t read the normal buffer.
- Computes the view space normal and the view space position from the downscaled depth buffer.
- Uses “Alchemy screen-space ambient obscurance” to calculate the SSAO term [McGuire2011].
- Does a coarse blur.

The second compute pass does some additional blurring.

There are a few reasons for not reading the GBuffer to get the normal:

- The GBuffer’s normal has finer detail and that makes it more noisy. That implies more denoising (blurring) of the SSAO output.
- No need for temporal accumulation between frames to remove the noise.
- Saves bandwidth since we read one texture less.
- This pass can be moved to async compute since we won’t have to transfer ownership of the normal buffer between the queues. We can just mark the downscalled depth buffer as VK_SHARING_MODE_CONCURRENT and move on.

![](../../assets/e3044c7f2ea0e711.png)

## Diffuse global illumination

OK this will be tricky to explain. The input to the GI stage is a list of visible GI probes and the output is a series of 3D textures containing “GI values”. There is one 3D texture per probe. The probes are placed by the artists inside the level and they are axis aligned bounding boxes (AABBs). Every probe is divided into a 3D grid, and the size of the cells is something also set by the artists. Every cell inside the grid owns a few texels inside the 3D texture.

The renderer will compute the GI term of a single cell per frame. The population of whole probe might take quite a few frames to complete. Just like shadows there is a caching system that tracks new probes, changes to already cached probes and also tracks the cell that will get updated next frame.

Populating a single cell involves a mini renderer by itself. The first thing that happens is a graphics pass that populates a 6 part GBuffer. And yes I am aware that populating the a 3rd render target is an overkill. I’m planning to fix that in the future.

If the scene has a directional light then there will be a super shadow pass as well. This light can only have one cascade.

![](../../assets/94bba85d6d4360b3.png)

Next there is the usual light shading. That graphics pass is not using clustered or tilled shading since the resolution is too low. The light shading is being done using traditional deferred shading where the shapes of the visible lights are drawn with additive blending. Only the directional light can have shadows.

![](../../assets/ee2b10732a7141d0.png)

The next step is the integration of the light buffers in order to compute the irradiance. This compute job reads the output of the light shading as a cube map. It integrates once for every direction of the cube. The integration for each direction samples only the face the direction points to and not the whole hemisphere as it should. After that step we have the irradiance per direction. But we are not done just yet. The compute job then applies the GI back to the light shading result and integrates again to compute the second bounce. This compute job is not extremely efficient but it’s pretty neat the way it works.

The final thing that will happen is to store the irradiance for all faces (6 rgb32f values) to a 3D texture. So let’s talk a bit about this 3D texture.

If the probe’s grid is 128*128*128 (random example) then this 3D texture will be sized 768*128*128. The X direction encodes the 6 directions of the ambient dice.

![](../../assets/8e1d9d99bfa89443.png)

## Volumetric lighting accumulation

As we mentioned above the frustum is divided into clusters and each cluster holds a list of some primitives. This pass is a compute job that calculates the lighting for each cell and the fog density as well.

Every compute invocation operates on a single cluster. For every invocation a random point inside the cluster will be chosen and the lighting of each light will be accumulated to compute the final result. The shadows are taken into account and that’s the reason why this pass will run after the shadow passes. The diffuse GI computed in the *Diffuse global illumination* stage will also be used.

One thing mentioned in the *Cluster binning* section is that AnKi has fog probes. These probes can be spheres or AABBs and the are associated with a single value which is the fog density. So, in addition to lighting each compute invocation of this pass will iterate the fog probes to compute the total fog density of each cluster.

One thing to note is that this pass is temporal. The position that is chosen to compute the lighting (and fog density) is jittered every frame. The result of the previous frame will be merged with the current result.

The final result is stored into a 3D texture.

![](../../assets/6894b91a1c6106ef.png)

## Volumetric fog

This technique is based on the one that was described by Bart Wronski [Wronski 2014]. For each cluster, the 3D texture computed by *Volumetric lighting accumulation* will be sampled to compute the fog. The fog density of the *Volumetric lighting accumulation* will be added to a global fog density term in order to compute the final fog density.

The result will be stored in a 3D texture as well.

![](../../assets/ce4cd74da1b9859d.png)

## Cube reflections

Artists can place some probes inside the scene and its purpose is to capture the specular GI term. The probes’ shape can only be an AABB at the moment. Their generation is somewhat similar to how the diffuse GI is produced. Once again it involves a cache and a mini renderer.

The idea is to populate a cubemap from the center of the probe. The renderer handles a single probe per frame and the result will be cached.

The first pass is the GBuffer generation. Nothing special.

Shadowmapping for the directional light as well.

![](../../assets/94bba85d6d4360b3.png)

The next pass does light shading using traditional deferred shading just like in diffuse GI.

![](../../assets/7b51273aff9d2847.png)

But that is not all. A compute pass will integrate the cubemap to compute the diffuse GI for each face direction. The diffuse GI is applied back to the cube map.

![](../../assets/346625d6748d6bc1.png)

The reflection generation is not using information from the diffuse GI pass because it’s a pain to synchronize those two stages. At the same time the probe types involved are different and figuring out who overlaps with whom is a pain.

## Screen space reflections

Nothing spectacular here or something that you haven’t seen before. One detail is that this is a compute pass that populates an image in a checkerboard manner. Every frame will write into a different texel.

There are no HiZ optimizations at the moment. Initially the ray marching starts with a big step and if there is a hit the step will decrease.

Once the raymarching finds a hit the light buffer will be sampled. This is the light buffer of the previous frame and it’s mipmaped (it’s generated by the *Downscale and average luminance* stage described later). The more rough the surface is the higher mipmap level will be used and the opposite.

If the raymarching failed to find a valid sample then it will output zero color with a factor indicating that failure.

![](../../assets/28259260f79327b8.png)

## Light shading, forward shading and fog

The next step is to gather all the results of the previous passes and finally perform the light shading. This is a graphics pass.

The first thing that happens is to compute the light shading. This is a fullscreen (triangle) draw that unpacks the GBuffer and iterates the lights of the affected cluster. The GBuffer’s diffuse term will be multiplied by the SSAO term. This drawcall will also sample the screen space reflections to compute the indirect specular term. If the SSR is missing information then the cubemaps will be used instead.

One last thing that happens in that fullscreen drawcall is to apply the diffuse GI. This will also iterate the GI probes of the cluster to find some blending factors (between GI probes) and sample from the correct 3D texture.

After the light pass there is a fullscreen draw that applies the fog by sampling the 3D texture computed by the the *volumetric fog* pass.

Then there is a series of drawcalls for transparent objects, particles etc. Those drawcalls have full access to the clusters and to the *light accumulation buffer* (produced by *Volumetric lighting accumulation*) so they can compute accurate or less accurate lighting. The particles for example use the *light accumulation buffer* in order to get some rough lighting that includes shadows as well.

And with that the light shading is complete and the HDR light buffer is populated.

As we mentioned before, the GBuffer contains a subsurface term. This is actually used in light shading to change the lambert term of light equations a bit.

`const F32 lambert = max(gbuffer.m_subsurface, dot(l, gbuffer.m_normal));`


This is obviously quite fake but at the same time it’s not that computationally taxing.

## Temporal AA

The GBuffer was populated with some offset in the projection matrix (jitter). So now it’s time to clean that up. This compute pass takes the light buffer of the current frame and the previous frame and performs the temporal AA that we all love.

The temporal AA used is more or less what I described here [https://community.arm.com/developer/tools-software/graphics/b/blog/posts/temporal-anti-aliasing](https://community.arm.com/developer/tools-software/graphics/b/blog/posts/temporal-anti-aliasing). It’s using variance clipping [Salvi16] and some luminance modulation for jitter removal [Lottes12].

As you might have noticed the input of this pass is an HDR render target but the *luminance based jitter removal* normally operates using LDR input. For this reason the HDR image goes through some cheap tonemapping using the previous frame’s average luminance.

The unprojection of the previous frame data is using the velocity information from the GBuffer as well.

![](../../assets/3a3a3e4c8b1c4038.png)

## Downscale and average luminance

This is a series of compute passes that downscale the output of the temporal AA in order to populate an HDR mippmaped image. Every downscale step will apply some blurring before it outputs the result into a mipmap level. This is heavily inspired by the Kawase blur. Pretty standard stuff.

The compute pass before the last will also calculate the average luminance. It’s the “one before the last” and not the last because this compute pass will run in parallel with the last downscale since they don’t have a dependency between them. Check out the render graph later in the article.

## Bloom and screen space lens flares

This is a compute pass with a single compute job that computes the bloom and also does some sort of screen space lens flares. The input is the mipmap chain produced by the *downscale* passes.

![](../../assets/5bc15525095e620d.png)

## Final composite & UI

This is a single graphics pass that will produce the final result. This is it, end of the road.

The first drawcall is the actual final composite and it’s a fullscreen (triangle) draw that:

- Does motion blur
- Does tonemapping
- Does color grading using a LUT texture

After that is done there is a series of drawcalls that apply the UI on top of that. This is the reason why this is a graphics and not a compute pass.

![](../../assets/c515daf161b5c1ae.png)

## Bonus: Render graph

AnKi features a (complex) system that automates some of the duties of the renderer. Its main purpose is to identify the dependencies between the various passes and to provide the renderer with the order those passes should run. This is a must for engines that are written using low level APIs such as Vulkan or DX12. I won’t go into details on how the render graph works and the dozen of its extra features but I’ll focus on the way it resolves dependencies between passes.

Every pass will inform about the resources it will consume and produce. After all passes have added their information the render graph will inspect the dependencies in order to find the order the passes. Rendergraph’s main goal is to batch as many passes as it can together in order to minimize the pipeline barriers. That means that the stages will ultimately be re-ordered.

TL;DR: passes and their dependencies enter the rendergraph and pass batches with pipeline barriers come out (more or less).

![](../../assets/bf9d2c5b849af4c7.png)

Rendergraph spaghetti (click for full size)

The picture above is produced by the debug capabilities of the render graph. The dotted squares are compute passes and the solid squares are graphics passes. The squares with the same color and in the same horizontal line are part of the same batch. There is a pipeline barrier after each batch so 14 barriers in total. The arrows indicate dependencies. **Please note that this graph is the worst case scenario**. After the initial warmup frames, the cube reflections and the GI volume textures will be in their respective caches and the related passes will disappear.

As you can see, in some cases we can have up to 8 graphics passes with 2 compute jobs running in “parallel”. Pretty neat.

## Closing comments

Tried to keep this article a bit high level in order to avoid loosing the reader from boredom. For more technical details or comments use the comment section bellow.

Very nice. You are certainly utilizing vulkan in a novel way. I assume you are using a topological sort on the graph and is it being called per frame? I would love to see some benchmarking stats of the various stages.

Glad you liked the breakdown. Yes there is a topological sort per frame but it does more than sorting. It also tries to batch passes together.

It’s being done per frame for a few reasons:

– Some probes may require an update and that implies additional passes

– The resources that define the pass dependencies change from this frame to the next and since the rendergraph will also perform VkLayout transitions it’s more convenient to rebuild it.

– Some passes (like shadows) don’t always run.

Benchmarking a frame sounds like an interesting followup to this article. I’ll try to make this happen!