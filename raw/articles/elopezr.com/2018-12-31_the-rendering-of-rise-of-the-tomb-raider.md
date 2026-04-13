---
title: The Rendering of Rise of the Tomb Raider
url: https://www.elopezr.com/the-rendering-of-rise-of-the-tomb-raider/
author: Redorav
published: '2018-12-31'
source_blog: The Code Corsair
source_site: http://www.elopezr.com
category: game programming
fetched: '2026-04-13'
---

Rise of the Tomb Raider (2015) is the sequel to the excellent Tomb Raider (2013) reboot. I personally find both refreshing as they move away from the stagnating original series and retell the Croft story. The game is story focused and, like its prequel, offers enjoyable crafting, hunting and climbing/exploring mechanics.

Tomb Raider used the Crystal Engine, developed by Crystal Dynamics also used in [Deus Ex: Human Revolution.](http://www.adriancourreges.com/blog/2015/03/10/deus-ex-human-revolution-graphics-study/) For the sequel a new engine called Foundation was used, previously developed for Lara Croft and the Temple of Osiris (2014). Its rendering can be broadly classified as a tiled light-prepass engine, and we’ll see what that means as we dive in. The engine offers the choice between a DX11 and DX12 renderer; I chose the latter for reasons we’ll see later. I used [Renderdoc ](https://renderdoc.org/)1.2 to capture the frame, on a Geforce 980 Ti, and turned on all the bells and whistles.

**The Frame**

I can safely say without spoilers that in this frame bad guys chase Lara because she’s looking for an artifact they’re looking for too, a conflict of interest that absolutely must be resolved using weapons. Lara is inside the enemy base at nighttime. I chose a frame with atmospheric and contrasty lighting where the engine can show off.

**Depth Prepass**

A customary optimization in many games, a small depth prepass takes place here (~100 draw calls). The game renders the biggest objects (rather the ones that take up the most screen space), to take advantage of the Early-Z capability of GPUs. A concise [article by Intel](https://software.intel.com/en-us/articles/early-z-rejection-sample) explains further. In short, the GPU can avoid running a pixel shader if it can determine it’s occluded behind a previous pixel. It’s a relatively cheap pass that will pre-populate the Z-buffer with depth.

An interesting thing I found is a level of detail (LOD) technique called ‘fizzle’ or ‘checkerboard’. It’s a common way to fade objects in and out at a distance, either to later replace it with a lower quality mesh or to completely make it disappear. Take a look at this truck. It seems to be rendering twice, but in reality it’s rendering a high LOD and a low LOD at the same position, each rendering to the pixels the other is not rendering to. The first LOD is 182226 vertices, whereas the second LOD is 47250. They’re visually indistinguishable at a distance, and yet one is 3 times cheaper. In this frame, LOD 0 has almost disappeared while LOD 1 is almost fully rendered. Once LOD 0 completely disappears, only LOD 1 will render.

![Before image](../../assets/d42f63f2c407c116.png)

![After image](../../assets/e0f4f964adf19913.png)

A pseudorandom texture and a probability factor allow us to discard pixels that don’t pass a threshold. You can see this texture used in ROTR. You might be asking yourself why not use alpha blending. There are many disadvantages to alpha blending over fizzle fading.![](../../assets/44b3c904c79a66b0.png)


**Depth prepass-friendly:**By rendering it like an opaque object and puncturing holes, we can still render into the prepass and take advantage of early-z. Alpha blended objects don’t render into the depth buffer this early due to sorting issues.**Needs extra shader(s)**: If you have a deferred renderer, your opaque shader doesn’t do any lighting. You need a separate variant that does if you’re going to swap an opaque object for a transparent one. Aside from the memory/complexity cost of having at least an extra shader for all opaque objects, they need to be accurate to avoid popping. There are many reasons why this is hard, but it boils down to the fact they’re now rendering through a different code path.**More overdraw**: Alpha blending can produce more overdraw and depending on the complexity of your objects you might find yourself paying a large bandwidth cost for LOD fading.**Z-fighting**: z-fighting is the[flickering effect](https://youtu.be/9AcCrF_nX-I)when two polygons render to a very similar depth such that floating point imprecision causes them to “take turns” to render. If we render two consecutive LODs by fading one out and the next one in, they might z-fight since they’re so close together. There are ways around it like biasing one over the other but it gets tricky.**Z-buffer effects**: Many effects like SSAO rely on the depth buffer. If we render transparent objects at the end of the pipeline when ambient occlusion has run already, we won’t be able to factor them in.

One disadvantage of this technique is that it can look worse than alpha fading, but a good noise pattern, post-fizzle blurring or temporal AA can hide it to a large extent. ROTR doesn’t do anything fancy in this respect.

**Normals Pass**

Crystal Dynamics uses a relatively unusual lighting scheme for its games that we’ll describe in the lighting pass. For now suffice it to say that there is no G-Buffer pass, at least not in the sense that other games have us accustomed to. Instead, the objects in this pass only output depth and normals information. Normals are written to an RGBA16_SNORM render target in world space. As a curiosity, this engine uses Z-up as opposed to Y-up which is what I see more often in other engines/modelling packages. The alpha channel contains glossiness, which will be decompressed later as exp2(glossiness * 12 + 1.0). The glossiness value can actually be negative, as the sign is used as a flag to indicate whether a surface is metallic or not. You can almost spot it yourself, as the darker colors in the alpha channel are all metallic objects.

R | G | B | A |
Normal.x | Normal.y | Normal.z | Glossiness + Metalness |

**Depth Prepass Benefits**

Remember how in the Depth Prepass we talked about saving pixel cost? I’m going to digress a little to illustrate that. Consider the following image. It’s rendering a detailed piece of mountain into the normals buffer. Renderdoc has kindly marked the pixels that pass the depth test as green, and the ones that fail the depth test (don’t render) as red. The total number of pixels this would have rendered without the prepass is ~104518 (counted them in Photoshop). The total number of pixels that actually render is 23858 (calculated by Renderdoc). That’s a ~77% reduction! As you can see, being clever about the prepass can bring in big gains, and all it took was around 100 drawcalls.![](../../assets/10e3f7ae17802869.jpg)


**Multithreaded Command Recording**

One interesting thing worth mentioning and a reason I chose the DX12 renderer is multithreaded command recording. In previous APIs like DX11, rendering typically took place in a single thread. The graphics driver received draw commands from the game and every now and again would kick off a request to the GPU, but the game didn’t know when that was going to happen. This introduces inefficiencies as the driver has to somehow guess what the application is trying to do and doesn’t scale to multiple threads. Newer APIs such as DX12 hand control over to the developer who can decide how to record commands and when to send them off. While Renderdoc can’t show how the recording actually took place, you’ll see there are seven color passes labeled Color Pass #N, and each is wrapped in an ExecuteCommandList: Reset/Close pair. This indicates the beginning and end of a command list. There are somewhere between 100 and 200 drawcalls per list. It doesn’t mean they were recorded using multiple threads, but strongly suggests it.![](../../assets/19ded9ae452bc32e.png)


**Snow Tracks**

If you look around Lara, you’ll see the snow tracks she left while I was moving to position her for the shot. A compute shader is dispatched every frame that records deformation in certain areas and applies them depending on the type and height of the surface. Snow here only has the normal map applied (i.e. the geometry doesn’t change) but in certain areas where the snow thickness is greater, the deformation is actually real! You can also see how the snow “falls” back to its place and fills in the gaps left by Lara. The technique is explained in a lot more detail in [GPU Pro 7](http://gpupro.blogspot.com/2016/01/gpu-pro-7-table-of-content.html). The snow deformation texture is a sort of height map that tracks Lara around, tiling at the edges so that the sampling shader can take advantage of that by wrapping.

**Shadow Atlas**

Shadow mapping takes the relatively common approach of packing as many shadow maps as possible into a single shadow texture. This shadow atlas is, in fact a huge 16384×8196 16-bit texture. This allows for very flexible reuse and resize of shadow maps within the atlas. In this capture there are 8 shadow maps being populated into the atlas. 4 of them belong to the main directional light (the moon, since it’s night time) as they’re using cascading shadow maps, a fairly standard long-distance shadow technique for directional lights which I explained a bit [previously](https://www.elopezr.com/the-rendering-of-middle-earth-shadow-of-mordor#shadows). More interestingly, a few spot and point lights are included in this capture too. The fact there are 8 shadow maps being populated this frame doesn’t mean there are only 8 shadow casting lights. It’s certainly possible the game is caching the shadow results, meaning lights where either the light’s position doesn’t change, or the geometry within its influence hasn’t changed don’t need to update their shadow map.

Shadow map rendering also seems to benefit from multithreaded command list recording, and in this instance a whopping 19 command lists were recorded for shadow map rendering.

**Directional Shadow**

The directional shadow is computed before the lighting pass and sampled later. I’m not sure what would happen if there was more than 1 directional light in the scene.

**Ambient Occlusion**

For ambient occlusion ROTR gives the option of either HBAO or its variant HBAO+, which is a technique originally published by NVIDIA. A few variations of this algorithm exist so I’ll focus on what I found in ROTR. First, the depth buffer is split into 16 textures, each containing 1/16th of the total depth values. The split is done such that every texture contains only one value out of a 4×4 block of the original texture as in the following image. The first texture contains all values marked in red (1), the second values marked in blue (2), etc. If you want more details about this particular technique here’s a [paper](https://developer.nvidia.com/sites/default/files/akamai/gamedev/docs/BAVOIL_ParticleShadowsAndCacheEfficientPost.pdf) by [Louis Bavoil](https://twitter.com/louisbavoil), one of the same authors as HBAO.

The next step computes the ambient occlusion for each texture, giving us 16 ambient AO textures. The way ambient occlusion is generated is to sample the depth buffer multiple times, reconstructing the position and accumulating the result of a calculation for each of the samples. Each ambient occlusion texture is computed using different sampling coordinates, meaning each pixel tells a different part of the story for a 4×4 block of pixels. The reason it’s done this way is performance. Each pixel is already sampling the depth buffer 32 times, the full effect would require 16×32 = 512 samples, which is overkill even for the most powerful of GPUs. They are then recombined into a single fullscreen texture, which is quite noisy so a fullscreen blur pass is performed right after that to smooth the results. We saw a very similar approach in [Shadow of Mordor](https://www.elopezr.com/the-rendering-of-middle-earth-shadow-of-mordor#ssao).


**Tiled Light Prepass**

Light Prepass is a fairly unusual technique. Most development teams go for a combination of traditional deferred + forward (with variations such as tiled, clustered) or fully forward with a few screenspace effects. The light prepass technique is uncommon enough that it warrants an explanation. If the idea behind traditional deferred is to decouple material properties from lighting, the idea behind light prepass is to decouple lighting from material properties. While it may seem a little silly to phrase it like that, the difference is that in traditional deferred, we store all material properties such as albedo, specular color, roughness, metalness, micro-occlusion, emissive, etc. in a fat G-buffer, and use that later as input to subsequent lighting passes. Traditional deferred can get very expensive in terms of bandwidth; the more complex your materials are, the more information and processing you need in your GBuffer. However, in light prepass we first accumulate all the lighting separately using a minimal amount of data, and then apply it onto the materials in subsequent passes. In this case, all the lighting needs is the normal, the roughness and the metalness bit. The shaders (there are two passes) output to three RGBA16F render targets, one containing diffuse lighting, another containing specular lighting and the third containing ambient lighting. All shadowing has been taken into account at this point. As an curiuosity, the first pass (diffuse + specular lighting) uses a two-triangle quad for its fullscreen pass whereas other effects use a single fullscreen triangle (you can read why this matters [here](https://michaldrobot.com/2014/04/01/gcn-execution-patterns-in-full-screen-passes/)). The entire frame is inconsistent in this regard.


**Tiled Optimization**

Tiled lighting is an optimization technique designed to render a large number of lights. ROTR splits the screen into 16×16 tiles and then stores which lights intersect each tile, meaning we only run light calculations for lights that touch the tiles. At the beginning of the frame a sequence of compute shaders were dispatched to determine which lights covered which tiles. During the lighting stage, each pixel will determine which tile they’re in and run a loop through every light in the tile, performing the lighting calculations. If the light assignment to the tiles is good, a lot of math and bandwidth can be saved and performance improved.

**Depth-aware upscaling**

An interesting technique that is relevant both here and in subsequent passes is depth-aware upsampling. Sometimes expensive algorithms can’t be rendered at full resolution, so they’re instead rendered at a lower resolution and upscaled. In this case ambient lighting is computed at half-resolution which means the lighting has to be cleverly reconstructed. In its simplest form it involves looking at 4 low resolution pixels and interpolating to obtain something that resembles the original image. This works for smooth transitions but breaks at surface discontinuities, as we’re now blending unrelated quantities that are contiguous in screen-space but far apart in world space. Solutions typically involve taking multiple depth buffer samples and comparing them to the depth sample that we want to reconstruct. If the sample is too far apart, we don’t consider it for the reconstruction. This works well but it means that the reconstruction shader becomes bandwidth-heavy.

ROTR does something clever using early stencil discard. After the Normals Pass, the depth buffer is fully populated, so they run a fullscreen pass that marks the discontinuous pixels in the stencil buffer. When the time to reconstruct the ambient buffer comes, they use two shaders: a really simple one for the regions with no depth discontinuities, and the more complex one for the pixels with discontinuities. Early stencil will discard the pixels if they don’t belong to the appropriate region, meaning we only pay the cost in the regions where we need to. The following images will clarify a lot more:


After the light prepass, geometry is submitted again into the pipeline, only this time each object samples the light textures, the ambient occlusion texture and the rest of the material properties that we didn’t put in the G-Buffer to begin with. This is good as there was a big bandwidth saving from not having to read a bunch of textures to write them to a fat G-Buffer, to read/decode them back again. The obvious downside is that all geometry needs to be submitted again, and that the light prepass textures are bandwidth-heavy themselves. I was wondering why the light prepass textures aren’t some more lightweight format such as R11G11B10F, but there’s extra information in the alpha channel that doesn’t seem to allow for it. In any case it’s a very interesting technical choice. By this point all opaque geometry has been rendered and lit. Notice how emissive objects such as the sky or the laptop screen are also included.

**Reflections**

This scene isn’t a particularly good example for reflections so I chose another one. The reflections shader is a pretty complicated amalgamation of loops that can be summarized in two parts: one samples cubemaps and the other does SSR, both in the same pass and blended at the end based on a factor that expresses whether the SSR found a reflection or not (possibly not binary but in the [0, 1] range). SSR works as is typical already in many games by repeatedly tracing the depth buffer trying to find the best intersection between the ray reflected at the shaded surface and another surface somewhere in the screen. SSR works with a previously downscaled mipchain of the current HDR buffer, not the full buffer.

There are tweaking factors such as reflection intensity and also a sort of Fresnel texture that was computed before this pass based on normal and roughness. I’m not 100% sure but after looking through the assembly it seems like ROTR can only compute SSR for smooth surfaces. There is no post-SSR blur mipchain like in other [engines](https://www.guerrilla-games.com/read/taking-killzone-shadow-fall-image-quality-into-the-next-generation-1), or even something like tracing the depth buffer using rays that [vary based on roughness](https://www.ea.com/frostbite/news/stochastic-screen-space-reflections). In summary, rougher surfaces will receive reflections from cubemaps or none at all. That said, the quality of the SSR is very good for the cases where it works, and stable given it doesn’t temporally accumulate or blur spatially. Alpha supports SSR as well (you can see some really nice water reflections in some temples) which is a nice addition you don’t see too often.


**Lit Fog**

Fog is not well represented in this scene as it darkens the background and instead is created through particles, so we’ll reuse the reflections capture. Fog is relatively simple but quite effective. There are two modes: a global, uniform fog color, and an inscattering color derived from a cubemap. Maybe the cubemap was repurposed from the reflection cubemaps or perhaps captured specifically. In both modes the attenuation of the fog is derived from a global attenuation texture which packs attenuation curves for several effects. The great thing about about this setup is that it’s really cheap lit fog, i.e. the inscattering varies spatially giving the illusion that fog is interacting with faraway lighting. This approach can also be used to good effect as atmospheric inscattering for skies.![](../../assets/e3f0c1acc0f325fb.jpg)



**Volumetric Lighting**

A few operations happened in preparation for volumetric lighting very early on in the frame. Two buffers were copied from the CPU to the GPU: light indices and light data. Both got read by a compute shader whose output was a 40x23x16 camera-aligned 3D texture where each voxel contains the number of lights that intersect that region. The dimensions of the texture are 40×23 because each tile is 32×32 pixels (1280/32 = 40, 720/32 = 22.5), and 16 is number of pixels in depth. Not all lights are included, only the ones marked as volumetric (three in this scene). There are other fake volumetric effects created with flat textures as we’ll see later. The output texture is higher resolution, 160x90x64. Once the number of lights per tile and their index has been determined, three compute shaders run in sequence performing the following operations:

- A first pass determines the amount of incoming light to a cell inside the frustum-shaped volume. Each cell will accumulate all light influences, as if there were floating particles reacting to the light and returning a fraction towards the camera.
- A second pass will blur the lighting with a small radius. This is probably important to avoid flickering as you move the camera since the resolution is so small.
- The third pass will walk the volume texture front to back, incrementally adding each light contribution and outputting to the final texture. What this effectively does is simulate the total amount of incoming light through a ray up to a given distance. Since at each cell contains the fraction of light bounced towards the camera by particles, at each cell we’ll have the collaborative contribution of all the previously walked cells. This pass also blurs.

Once all this is complete we have a 3D texture that can tell us how much light is incoming for a specific position relative to the camera. All the fullscreen pass needs to do is determine this position, find the corresponding voxel in the texture and add that to the HDR buffer. The actual lighting shader is really simple and about ~16 instructions.


**Hair Rendering**

If PureHair is not enabled, standard layers of hair get rendered on top of each other. This approach still looks great but I want to focus on the bleeding edge. If the feature is enabled, the frame kicks off by simulating Lara’s hair in a sequence of compute shaders. The original Tomb Raider used a technology called TressFX and Crystal Dynamics released the sequel with improved technology. After the initial computation there are an impressive 7 buffers all used to drive Lara’s hair. The process is as follows:

- Dispatch compute shader to calculate motion values using previous positions and current positions (for motion blur)
- Dispatch compute to populate a 1×1 irradiance cubemap from reflection probe and irradiance information (lighting)
- Spawn ~122k vertices in Triangle Strip mode (each strand is a strip) There’s no vertex buffer as you’d expect in typical drawcalls but instead the 7 buffers contain everything needed to build the hair. The pixel shader does manual clipping, if the pixel is outside the window it gets discarded. This pass marks the stencil as ‘contains hair’.
- The lighting/fog pass renders a fullscreen quad with stencil testing enabled, such that only the pixels where hair is actually visible are computed. This will effectively treat hair as opaque and reduce the shading load to just the strands visible on screen.
- There’s also a final pass like 4) that only outputs the hair depth (copies from a “hair depth” texture)

If you’re interested in more details, AMD provides lots of [resources](http://amd-dev.wpengine.netdna-cdn.com/wordpress/media/2012/10/Augmented-Hair-in-Deus-Ex-Universe-Projects-TressFX-3.0.ppsx) and [presentations](http://32ipi028l5q82yhj72224m8j.wpengine.netdna-cdn.com/wp-content/uploads/2017/03/GDC2017-Real-Time-Finite-Element-Method-And-TressFX-4.0.pdf) as this is a [public library](https://gpuopen.com/gaming-product/tressfx/) they provide. One thing that confused me was a step before 1), which is the same drawcall as 3) and says it only renders to depth, but there’s no actual content rendered and I wondered if Renderdoc wasn’t telling me something. I had a suspicion it was maybe trying to do a conditional rendering query, but I can’t see any Predication calls.


#### Tiled Alpha Rendering and Particles

Transparent objects reuse the per-tile light classification computed for the tiled light prepass. Each transparent object computes its own lighting in a single pass, which becomes a pretty scary number of instructions and loops (hence the light prepass approach used for opaque objects). Transparent objects can even do screen-space reflections if enabled! Each object is rendered in back to front sort order directly to the HDR buffer, including glass, flames, water in truck tracks, etc. The alpha pass also renders edge highlights when Lara focuses on some object (like the flammable bottle on the box to her left)

Particles, however, are rendered to a half res buffer to mitigate the huge bandwidth they consume from overdraw, especially if many big, screen-covering particles are used for fog, mist, flames, etc. Therefore the HDR and depth buffers are downscaled to half resolution in each dimension, and particle rendering begins. The overdraw for the particles is massive, with some pixels shading around 40 times each. The heatmap shows what I mean. Since particles have been rendered at half resolution, the same clever upscaling trick that was used for ambient lighting is used here (stencil marks discontinuities, first pass renders to inner pixels, second pass reconstructs edges). You’ll notice particles render before some other alpha like flames, glows, etc. This needs to happen so alpha can sort properly with respect to e.g. smoke. You’ll also notices there’s some “volumetric” light shafts coming from the security lights that have been added here instead of relying on the truly volumetric solution. This is a cheap but convincing way of creating them at a distance.![](../../assets/4ea5819069582f00.jpg)



**Exposure and Tonemapping**

ROTR performs exposure and tonemapping in a single pass. However, while we tend to think of tonemapping as also doing gamma correction, that doesn’t happen here. There are many ways to do exposure, as we’ve seen in [other](https://www.elopezr.com/castlevania-lords-of-shadow-2-graphics-study/) [games](https://www.elopezr.com/the-rendering-of-middle-earth-shadow-of-mordor/). The luminance calculation in ROTR is really interesting and requires almost no intermediate data or passes, so we’ll spend a bit of time explaining the process. The entire screen is divided into 64×64 tiles, and a compute dispatch of (20, 12, 1) groups of 256 threads each is launched to fill the entire screen. Each thread conceptually does the following (pseudocode):

1 2 3 4 5 6 7 8 9 10 | for(int i = 0; i < 16; ++i) { uint2 iCoord = CalculateCoord(threadID, i, j); // Obtain coordinate float3 hdrValue = Load(hdrTexture, iCoord.xyz); // Read HDR float maxHDRValue = max3(hdrValue); // Find max component float minHDRValue = min3(hdrValue); // Find min component float clampedAverage = max(0.0, (maxHDRValue + minHDRValue) / 2.0); float logAverage = log(clampedAverage); // Natural logarithm sumLogAverage += logAverage; } |

Each group will calculate the log sum of all 64 pixels (256 threads each processing 16 values). Instead of storing the average it stores the sum and number of pixels it actually processed (not all groups will process 64×64 pixels e.g. could be beyond the edge of the screen). The shader makes clever use of thread local storage to split the sum; each thread works on 16 horizontal values first, then designated threads add all those values vertically, and finally the orchestrator thread for that group (thread 0) adds the result and stores it all in a buffer. This buffer contains 240 entries, effectively giving us the average luminance for many regions of the screen. A subsequent dispatch will launch 64 threads that will loop through all these values and add them together to get the final screen luminance. It will also undo the logarithm to put back to linear units.

I don’t have a lot of experience with exposure techniques, but reading this [blog post](https://knarkowicz.wordpress.com/2016/01/09/automatic-exposure/) by Krzystof Narkowicz clarified a few things. Storing in the 64-entry array serves the purpose of being able to compute a sort of running average, where they inspect previously computed values and are able to smoothen the exposure curve to avoid very sharp changes in luminance to produce sharp variations in exposure. It’s a very complicated shader and I haven’t decoded all the details, but the end result is an exposure value valid for this frame.

After the adequate exposure values have been found, a single pass will perform the final exposure plus tonemapping. ROTR seems to be using the [Photographic Tonemapping](http://www.cmap.polytechnique.fr/~peyre/cours/x2005signal/hdr_photographic.pdf) which also explains why they’re using log averages as opposed to a simple average. The tonemapping formula in the shader (after exposure) can be expanded as follows:



A concise explanation can be found [here](https://expf.wordpress.com/2010/05/04/reinhards_tone_mapping_operator/). I haven’t been able to determine why there is an extra division by Lm as it would negate the effect of the multiplication. I don’t understand enough to say. In any case whitePoint is 1.0 so the process doesn’t do much this frame, only exposure changes the image. The clamping of values to an LDR range doesn’t even happen here! It happens at color correction time, where the color cube implicitly clamps values greater than 1.0.


**Lens Flares**

Lens Flares are rendered in an interesting way. A small prepass computes a 1xN texture (where N is the total number of flare elements that are going to be rendered as lens flares, 28 in our case). This texture contains the alpha value for the particle and some other unused information, but instead of computing it from a visibility query or something similar, they compute it by analyzing the depth buffer around the particle in a circle. Vertex information is contained in a pixel shader-accessible buffer to allow for this.

Each element is then rendered as a simple screen-aligned planes emitted from lights. If the alpha value is less than 0.01 the position is set to NaN so that the particle doesn’t get rasterized. Thery look a bit like bloom and add to the glow, but the actual effect comes after.


**Bloom**

Bloom takes the standard approach of downsampling the HDR buffer, isolating bright pixels and successively blur-upscaling it to expand the region of influence. The result is upscaled all the way up to screen resolution and composited on top. There are a couple of interesting bits that are worth exploring. The entire process happens using 7 compute shaders: 2 for downsampling, 1 simple blur, 4 to upsample.

- The first downsample from full resolution to half resolution selects pixels brighter than a given threshold and outputs them to a half resolution target (mip 1). It also takes the opportunity to do a small blur as it does this. You’ll notice the first mip becomes only slightly darker, since we’ve discarded pixels with a pretty low threshold of 0.02.
- The next downsample shader takes mip 1 and produces mips 2, 3, 4 and 5 in a single pass.
- The next pass blurs mip 5 in a single pass. There are no separable blurs in the whole process like we sometimes see. All blurs take good advantage of groupshared memory to make sure the shader samples as few samples as possible and reuses from its neighbors.
- The upscale is also interesting. These 3 upscale pass use the same shader, and take two textures, previously blurred mip N and unblurred mip N + 1, blending both together with an externally-provided factor while also blurring them. This helps out bring some finer highlight details to the bloom that can be lost during the blurs.
- The final upscale will upscale mip 1 and adding to the final HDR buffer, multiplying the result by a controllable bloom strength.


One curiosity is that the downscaled textures actually change the aspect ratio. I’ve adjusted it for visualization purposes, I can only guess the reasons but perhaps to make texture sizes nice multiples of 16. Another interesting bit is that since these shaders are pretty bandwidth-bound in general, the values stored in group shared memory are actually converted from float32 to float16! This allows the shader to efficiently trade some math for twice the available memory and bandwidth. The range of values would need to be pretty big for it to become a problem.

**FXAA**

ROTR provides an assortment of antialiasing techniques such as [FXAA](https://developer.download.nvidia.com/assets/gamedev/files/sdk/11/FXAA_WhitePaper.pdf) (Fast Approximate AA) and SSAA (Super Sampling AA). Notably absent is an option to do temporal AA as is becoming customary in most recent AAA games. In any case, FXAA serves its purpose correctly, SSAA works well too, a relatively heavyweight option for those with performance to spare.

**Motion Blur**

Motion blur seems to use a very similar approach to that in [Shadows of Mordor](https://www.elopezr.com/the-rendering-of-middle-earth-shadow-of-mordor#motion_blur). After volumetric rendering, a separate render pass output motion vectors from animated objects into a motion buffer. This buffer is then composited with camera-induced motion, and the final motion buffer is input to a blur pass that’ll blur in the direction indicated by the screen-space motion vectors. To estimate the blur radius, a downscaled version of the motion vector texture is computed in several passes, so each pixel has a rough idea of the motion taking place in a neighborhood around itself. The blur happens in multiple passes at half resolution and is later upscaled in two passes using stencil as we’ve seen before. It does multiple passes for two reasons, the first is to reduce on the number of texture reads needed to produce a blur with a potentially very large radius, and second because it does different blurs depending on whether an animated character was rendered to those pixels.

**Extra Bits and Pieces**

There are a few things that are perhaps worth mentioning but not going too much in depth.

- Camera frost: adds snow flakes and ice streaks to the screen depending on how cold it is
- Camera dirt: Adds dirt to the camera
- Color correction: at the end of the frame there’s a bit of color correction, which uses the relatively standard color cube to perform color correction as was covered before here, while also adding noise to give some scenes a gritty tone

**UI**

The UI is a bit unconventional, as it renders all elements in linear space. Typically, a game has already performed tonemapping and gamma correction by the time the UI starts to render. However, ROTR uses a linear space right up to the very end of the frame. This makes sense, since the game has a 3D-like UI, however it needs to transform sRGB images to linear space before putting them in the HDR buffer, so that the very last thing that happens (gamma correction) doesn’t distort the colors.

**Wrapping up**

I hope you’ve enjoyed reading this analysis as much as I did creating it, I’ve certainly learned a lot. Congratulations are in order to many talented people at [Crystal Dynamics](https://en.wikipedia.org/wiki/Crystal_Dynamics) for the fantastic work that has gone into creating the engine. I would also like to acknowledge Baldur Karlsson for his fantastic work on Renderdoc, whose efforts have made graphics debugging on PC a much better experience. I think the only thing that’s been a bit harder when doing this analysis is inspecting actual shader runs since the feature is unavailable on DX12 as of this write-up. I’m sure it will eventually come though and we’ll all be happy.

Really interesting stuff, thanks for posting this.

I’m glad you like it 🙂

Very enjoyable read, keep up the great work!

Interesting to see how some techniques which were present in DE-HR (like light-prepass) were kept and revamped.

Thanks! Happy to hear you like it as you started this whole thing. I’ll have a re-read of your analysis to compare past vs present, it was a long time ago when I read it for the first time

Thanks for very interesting anylysis!

I’m curious what data contributes to ambient lighting in tiled light prepass. It looks like some form of bounce lighting but of warm tone (with cold direct ‘sun’ in that case). Any details of where it come from?

From what I could see there’s a constant buffer called IrradianceState which seems to hold a spherical harmonic sample in the first 8 components, which is then evaluated using the normal. Presumably this was pre-interpolated on the CPU as you can’t write to constant buffers directly through the GPU as far as I’m aware.

On top of that it seems to loop through a collection of cubemaps which I can only imagine contain specular data for rough materials in the lower mips and is added here. I didn’t look into that last part too much in detail though.

Interesting read!

Would like to see how RTX works.

There is a mod for Quake2 (Q2VKPT iirc) which adds full RTX lightning and eats a ton of resources in the process, but it looks really neat. Would be nice to see how that works (since Q2 renderer is pretty easy to understand, than most of such analysis would be about RTX itself).

Rise of the Tomb Raider is part 2 of the Tomb Raider trilogy; RTX if I’m not mistaken has only appeared in Shadow of the Tomb Raider which I haven’t played yet. I also don’t have an RTX-enabled card although my guess is it would still run (really slowly) on what I have. On top of that though, I’m not sure renderdoc currently supports the RTX extensions.

Have you noticed SDSM for the directional shadow? 😉

Very nice article. Is this analysis for the PC version or Xbox version?

I realize how late it is to reply to this, but it is the PC DX12 version

Please do an analysis for SOTTR (preferably with DX12 and async compute enabled) and you will be surprised.

This post help me a lot