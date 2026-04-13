---
title: 'The Rendering of Mafia: Definitive Edition'
url: https://www.elopezr.com/the-rendering-of-mafia-definitive-edition/
author: Redorav
published: '2021-08-23'
source_blog: The Code Corsair
source_site: http://www.elopezr.com
category: game programming
fetched: '2026-04-13'
---

[Mafia: Definitive Edition (2020)](https://en.wikipedia.org/wiki/Mafia:_Definitive_Edition) is a remake of the much-loved gangster classic [Mafia (2002)](https://en.wikipedia.org/wiki/Mafia_(video_game)), originally released for PS2 and Xbox. The game is relatively linear and very story focused, whose narrative I personally found gripping and worthy of being compared to Scarface or Goodfellas. Hangar 13 use their own technology to take on open worlds and stories, previously used for [Mafia III](https://en.wikipedia.org/wiki/Mafia_III), to bring Tommy and the Salieri family to life. It is a DX11 deferred engine on PC, and [RenderDoc 1.13](https://renderdoc.org/) was used to capture and analyze.

**The Frame**

Tommy looks like he means business with his jacket and fedora, and thus our frame analysis begins. I chose a nighttime city scene as I find it more moody and challenging to get right. Let’s dive right in: I’ll make you a rendering offer you can’t refuse.

**Depth Prepass**

As we know, a depth prepass is often a careful balance between the time you spend doing it and the time you save by more effective occlusion. Objects seem to be relatively well selected and sorted with depth and size, as by drawcall 120 we actually have a lot of the biggest content in the depth buffer with very simple shaders. Subsequent drawcalls fail the depth test often after that, avoiding wasted work. There are some odd choices like the electricity wires which I assume have large bounding boxes, but most of it makes sense and probably costs little compared to what it saves.

**GBuffer Pass**

The GBuffer for Mafia packs quite a lot of information. The first texture contains normals and roughness, which is quite standard these days, in 16-bit floating point. While it’s a little large for my taste, normals tend to want as much bit-depth as possible, especially if no [compression schemes](https://aras-p.info/texts/CompactNormalStorage.html) are used.

R16F | G16F | B16F | A16F |
Normal.x | Normal.y | Normal.z | Roughness |


The second texture contains albedo and metalness in an 8-bit normalized format, which is also common for PBR engines and relevant if cars sport very reflective chrome components. As you can see, metallic parts are marked as white whereas mostly everything else is black (i.e. non-metal)

R8 | G8 | B8 | A8 |
Albedo.r | Albedo.g | Albedo.b | Metalness |


The next texture contains packed quantities not easy to decode by inspection. RenderDoc has a neat feature, custom shaders, that will come to our aid. Searching the capture we come across the code for decoding these channels, and after adapting the D3D bytecode back to hlsl, displaying them on screen actually starts to make sense. The first 3 channels are motion vectors (including a z component which I find interesting), and the last channel is the vertex normal encoded in two 8 bit values (z is implicit). It’s interesting to note that vertex normals have only been given 2 bytes as opposed to the 6 bytes assigned to per-pixel normals. Vertex normals are an unusual thing to output, but we’ll soon find out why.

R16U | G16U | B16U | A16U |
MotionVector.x | MotionVector.y | MotionVector.z | Encoded Vertex Normal |


The fourth texture contains miscellaneous quantities such as specular intensity, curvature and profile for subsurface scattering and flags. The G component is set to 0.5 so it may be an unused/spare channel for future usage.

R8 | G8 | B8 | A8 |
Specular Intensity | 0.5 | Curvature or Thickness (for SSS) | SSS Profile |


The last entry in the GBuffer is the emissive lighting, which becomes the main lighting buffer from now on.

R11F | G11F | B10F |
Emissive.r | Emissive.g | Emissive.b |

One interesting performance decision for the GBuffer is not clearing it at the start of the frame. Sometimes clearing a buffer is necessary, but you can avoid the cost if you’re going to overwrite the contents and you know where (by marking it in the stencil). There are other performance penalties involved in clearing depending on platform, so the gist of it is it’s never a bad idea to avoid clearing if you can.

**Downscaled Depth and Normals**

Downscaling depth and normals is a common technique for running expensive effects at lower resolution. As we’ll see later this is put to good use during the global illumination pass. For now we’ll mention that the game creates 3 mipmaps for depth and normals (both vertex and per-pixel). It also creates a downscaled texture containing edge information. These textures are useful for edge preservation when upsampling from a low resolution, which as we’ll see happens often. The edges are cleverly packed into a single R8_UNORM texture, which is very little memory for the information it stores. An implementation of this or a similar scheme is used in [Intel’s Adaptive Screen Space Ambient Occlusion](https://software.intel.com/content/www/us/en/develop/articles/adaptive-screen-space-ambient-occlusion.html).


**Occlusion Culling**

A typical Mafia scene is a relatively dense urban environment, and many objects are occluded by other large objects. Occlusion culling is the family of techniques that avoids processing them. One technique that other engines like UE4 have used to great success is called occlusion queries, and are a way to ask the GPU whether certain geometry is behind the depth buffer, and even how occluded they are as a pixel percentage. A couple of notes on these techniques:

**Small Delay:**Queries happen on the GPU and it takes 2-3 frames for that information to propagate back to the CPU, depending on the implementation. This delay can cause objects to pop on screen if the transition is abrupt**GPU Solution:**Sometimes these queries can be used with a feature called[predicated rendering](https://docs.microsoft.com/en-us/windows/win32/direct3d12/predication), which bypasses those issues but loses visibility on the CPU side**Overhead:**These tests need to be as fast as possible, but even rasterizing just a few hundred boxes isn’t free, so occlusion testing can happen on small conservative depth buffers to make it as cheap as possible

There are drawcalls that look like rooms and big chunks of geometry which suggests that the engine may bucket objects in boxes. Another interesting fact is that queries are also done on the cascades of the shadow map. If objects are occluded from the light’s point of view we can avoid wasting performance.


**Deferred Decals**

Deferred decals is a common technique to add detail or modify material properties on surfaces. It is well suited to a deferred renderer because the pipeline already outputs the necessary quantities. There are many [articles](https://mtnphil.wordpress.com/2014/05/24/decals-deferred-rendering/) and [presentations](https://www.slideshare.net/philiphammer/bindless-deferred-decals-in-the-surge-2) [covering](https://bartwronski.com/2015/03/12/fixing-screen-space-deferred-decals/) [decals](http://broniac.blogspot.com/2011/06/deferred-decals.html). Mafia decals are rasterized, instanced boxes. Certain objects lay down a stencil mask during the GBuffer pass so that decals don’t render on top of them (e.g. the character or the cars)


**Stencil Composite**

A common issue with decals is blending. For one, it sometimes requires equations that the blend unit cannot express (such as for [normal blending](https://blog.selfshadow.com/publications/blending-in-detail/)), but also the alpha channel cannot simultaneously be a blend factor and a blendable quantity. To avoid these issues Mafia uses a clever trick: some decals render into intermediate decal buffers and sample from the original buffer output by the GBuffer pass. After decals have been rendered, a composite pass puts the both buffers back together, using its alpha channel as the blend factor. During rendering decals write a stencil value, to avoid a fullscreen copy and only combine the relevant parts back into the original GBuffer, which makes it a very scalable technique.


**Global Illumination**

One thing the Mafia engine does really well is realtime global illumination. GI is the process of sampling the lighting environment around a given surface and integrating the result (i.e. adding all rays and applying certain weights to each). This is often impractical for realtime, so most solutions distribute rays spatially and/or temporally, and reuse those results by blurring and/or accumulating over time.

**Stochastic Sampling**

This works by randomly distributing vectors around the main normal in a manner consistent with the surface properties and type of illumination. For example, sampling vectors for diffuse illumination look like a noisy version of the original vertex normals, as they are centered around the normal and distributed uniformly around the hemisphere.


For specular, they are centered around the reflection vector produced by the view vector and the per-pixel normal. Specular reflections are more concentrated around the reflection vector for smoother surfaces according to the BRDF. In the extreme (roughness is zero, such as the car) the random vector is the reflection vector.

GI in Mafia is a combination of screen space and “statically” computed lighting. Every ray cast will try to find a source on screen first, and fall back to a volumetric structure. The source for on screen lighting is the previous frame, using the motion vectors for reprojection. For diffuse, the volumetric fallback is a volume structure containing low frequency lighting around the camera. For specular, the fallback is a cascade of cubemaps that has both depth and lighting information and gets raymarched in the same manner as the screen depth buffer.

The process works at 3 resolutions and cleverly upscales in successive iterations to mitigate the cost, and the last step includes temporal accumulation. Both diffuse and specular conceptually work in the same way. A sequence of images is worth more than a lengthy explanation.



**GI Update**

As we have mentioned already, GI works partly in screen space and partly uses fallback structures. A process at the beginning of the frame incrementally updates them. The first step that happens across many frames is cubemap capturing. Cubemaps are captured around the player as they traverse the level, containing both depth and lighting, and there are other textures that provide extra information.

The cubemaps are also preprocessed to produce volume textures that represent what looks like outgoing radiance extracted from those cubemaps and a main direction vector. Other textures look like they might encode some form of light leaking prevention. In any case, it is this volume structure that diffuse rays fall back to when they miss the screen. In the case of specular reflections, the ray is traced directly through the cubemap depth buffer until an intersection is found. For more details on this process, Hangar 13’s Martin Sobek published a detailed [GDC presentation](https://www.gdcvault.com/play/1025467/Real-Time-Reflections-in-Mafia).

**Ambient Occlusion**

**SSAO**

Screen Space Ambient Occlusion is a standard technique so we won’t go into much detail about it. It seems to be used for relatively short range occlusion in general, with the radius constant in screen space (this helps capture detail in the distance even if it looks “larger”)

**Car Occlusion**

It is hard to get ambient occlusion from the underside of things from a screen space technique, so Mafia takes the oldest trick in the book which is to darken the ambient lighting using a texture, in a manner not too dissimilar to decals. It is car-specific and not used for anything else. I have overlaid the wireframe in the shadow shot so you can see clearly how the shadow relates to the car.

**Direct Illumination**

Unlike other games using tiled or clustered lighting, Mafia instead uses classic deferred techniques with some tricks worth mentioning. In both day and night a standard directional light is present.

**Screen Space Contact Shadows**

A known issue with standard shadow mapping is the difficulty to get shadows that perfectly join at the contact point between two surfaces. Typical artifacts in this situation are:

Sometimes developers who add a small bias to avoid shadow self-intersection artifacts will cause another undesired effect where shadows look detached from an object and the object looks like it’s floating[Peter-Panning](https://digitalrune.github.io/DigitalRune-Documentation/html/3f4d959e-9c98-4a97-8d85-7a73c26145d7.htm#PeterPanning):**No Contact:**If the engine has soft shadows, the radius is often applied with no regards to the distance between the occluder and the receiver. Therefore even at the surface boundary the shadow will look soft and not grounded**Shadow Resolution:**If the target performance isn’t reached, developers often compromise on shadow map resolution which of course impact on how crisp the shadow result can be

For these reasons contact shadow techniques were developed. It is yet another screen space raymarching solution where a ray is cast from the depth buffer in the direction of the light until a suitable intersection is reached.

**Parallel Split Shadows**

Parallel split shadows is also fairly standard. Mafia renders several cascades into a 2048×2048 texture array. The cascades are resolved incrementally onto the main shadow mask buffer using stencil and depth trickery to discard pixels outside the cascade range quickly. The closest cascade is sampled with a lot of detail whereas the further cascades are sampled with less detail. The result is combined with the contact shadows.

The typical arsenal of point and spot lights is also available. They are rendered in two ways depending on their screen size:

- For lights that take up a lot of screen real estate, the venerable
[stencil mask technique](https://kayru.org/articles/deferred-stencil/)is used. This technique sets up a stencil mask of the pixels a light touches and then renders the light, writing only to that region taking advantage of early stencil. An extra optimization is that the mask is prepared for several lights up front, then rendered for all those lights - For smaller lights it wasn’t worth the overhead of creating the stencil mask. A quad covering the screen area of the light is used instead. I’m not too sold on this as it feels like many pixels have 0 contribution adding cost to the frame where a tighter shape could have worked better

**Character Shadows**

Characters have their own shadow maps. A custom shader that renders the character geometry and only samples the character shadow map is composited on top of the shadow mask blended with a min operator to add finer detail. Notice the crisp shadows under the hat and the jacket lapels.

**Subsurface Scattering**

After lighting, subsurface scattering kicks in. It’s a subtle effect so we’ll zoom in. The implementation is most likely [SSSSS](http://www.iryoku.com/screen-space-subsurface-scattering) by [Jorge Jiménez](https://twitter.com/iryoku1) which has become pretty standard. It is essentially a bilateral screen-space Gaussian blur with carefully tuned weights derived from skin profiles whose width can vary with thickness/curvature values from the GBuffer. The blur only happens on the diffuse component of the lighting, so diffuse and specular are separated, then composited back.


For optimization a stencil mask is produced so the shader only blurs where strictly necessary and the cost scales. SSS can be more expensive in a cutscene but during gameplay the screen area is tiny and the effect likely has a negligible impact.

![Before image](../../assets/5787ecd7e0a49624.jpg)

![After image](../../assets/fc7f87eb0bf2e4db.jpg)

**Clouds**

Mafia sports an unusual solution for clouds. It starts off by rendering a big dome-shaped object, with depth testing turned on, creating a stencil mask so that the later shader only writes to the visible sky pixels. In that shader, 3 textures are sampled, a couple of 3D textures with 8 slices unwrapped as 2D textures, and an actual 3D noise texture. The choice of 2D textures emulating a 3D texture is a recurring pattern as we’ll see later. One of the 8 slices in the texture is generated every frame to do the cloud simulation, i.e. every 8 frames a cloud cycle is completed.


The three textures are combined to create a fullscreen cloud texture containing a cloud mask for the presence of clouds, plus single scattering and multiscattering in the other two channels. This texture is plugged in later when compositing with the entire sky.


**Atmospheric Sky+ Stars**

Mafia has an atmospheric simulation going on, and can set the environment to different weather and time conditions. One of the first steps uses a series of precomputed inscattering and outscattering textures to produce the [Rayleigh](https://en.wikipedia.org/wiki/Rayleigh_scattering) and [Mie](https://en.wikipedia.org/wiki/Mie_scattering) scattering for the sky, at low resolution.

The sky generation step takes the previous cloud data and blends it with an upsampled version of the Rayleigh and Mie textures depending on the time of day and weather conditions, occluding clouds correctly by fog. This step is also accelerated by the stencil buffer, avoiding computations in the foreground. At nighttime there’s an extra step going on; to render the starfield, stars are rendered as little quads on screen with a small glowing texture applied to them. They are also correctly occluded by the clouds and sky.


**Volumetric Fog**

For volumetric fog, Mafia uses the unwrapped volume texture technique again, although this time there’s an interesting trick taking advantage of it. The idea is to “rasterize” a volumetric shape by slicing it into quads. Each quad renders to a slice in the volume, so e.g. you can split a spotlight into multiple slices and render them in one instanced drawcall. The outputs are both the radiance of the light at a given position and what looks like the position itself from the light’s point of view.![](../../assets/6275a8c54580f4ac.jpg)



As we’ve seen already Mafia loves their stencil buffer so here’s another interesting trick that I think sells this 2D texture emulation on a 3D texture. In a volume texture that is sliced in the depth from the screen, parts of slices are going to be hidden by geometry in front (like the car in this image). By marking occluded pixels we can avoid wasted computations.

This texture is noisy so a post-blur pass is performed on it. This blur helps hide the noise, but also helps with temporal stability, as this volume texture is low resolution compared to the screen (256x192x84). The blur also uses the stencil trickery mentioned above.

The volume texture is then combined with an actual atmospheric fog simulation (bluish color in the image above) and the result overlaid on top of the lit buffer.


**Transparency and Glows**

Transparent objects that need reflections are rendered twice. First they’re output onto an offscreen buffer at half resolution, rendering the closest reflection vectors and depth, which are then used to trace reflections. The resulting reflection texture is later read by the actual full resolution transparency pass and composited back. Smoke and glows are also included in this pass.


**Temporal AA**

Mafia’s antialiasing solution is Temporal AA, which has become relatively standard these days. It has several typical characteristics such as an accumulation buffer and uses motion vectors to access the previous frame’s contents as described [here](http://advances.realtimerendering.com/s2014/#_HIGH-QUALITY_TEMPORAL_SUPERSAMPLING). It creates a disocclusion texture to mitigate trailing and also attempts to remove very bright pixel outliers with a combination of a downscaled HDR texture and the luminance of the scene.


**Post-Processing**

There is a single big shader that composites camera effects such as tonemapping, exposure correction, bloom, film grain, dirt, etc. We’ll go over some but they are fairly standard.

Bloom happens by blurring a thresholded HDR buffer. Instead of concatenating successive blurs and upscaling as other implementations do, each blur is done independently on a downscaled buffer (mips 1-4) and then combined back.


Film grain is not unusual for games that want to have a Hollywood look or imitate older film, and Mafia is a good candidate given its setting. A simple noise texture is applied on top of the entire image and shifted over time, to mimic sensor noise on a dark night. Tonemapping is done using a color cube as we saw in ![](../../assets/4d6b2e90f8e8a649.png)


[Shadow of Mordor](https://www.elopezr.com/the-rendering-of-middle-earth-shadow-of-mordor/), and vignette has an interesting little quirk. Instead of adding a fullscreen pass, it renders a squashed octogon in the middle of the screen with the bounds of the vignette. From there the pixel shader derives the intensity of the effect. I think it’s mainly used when you’re injured, and meant to go dark red representing blood. Screen dirt is added on top as well, and this technically finishes the frame.


### UI

The UI is rendered directly on top of the swapchain at the end of the frame. It’s all pretty standard here except for the rendering of the realtime minimap. As has become a tradition already, stencil is used to mark the region of interest, and then flat geometry is rendered on top representing streets, buildings, routes, etc. After that a series of antialiased borders are rendered to soften the edges and small icons like the car, etc are overlaid on top.![](../../assets/cd7ed00852d80878.jpg)



### Closing Remarks

With this our analysis ends, and hopefully you’ve enjoyed it. Mafia not only is a great game, it also looks really well and we now have a small insight into how it was done. As always, if this leaves you with appetite for more analyses, Adrian Courrèges kindly keeps a [repository](https://www.adriancourreges.com/blog/2020/12/29/graphics-studies-compilation/) of many other game studies.

Well done and very thorough, as always! Keep it up!

Thank you Bo! I always learn a lot making these, hopefully other folks learn from them too

Thanks for your work. I have some question about gi:

1. “Every ray cast will try to find a source on screen first, and fall back to a volumetric structure”, “For diffuse, the volumetric fallback is a volume structure containing low frequency lighting around the camera” How to calculate the volume structure?

2. “The process works at 3 resolutions and cleverly upscales in successive iterations to mitigate the cost, and the last step includes temporal accumulation” process 3 resolution seems to add the additional work, how to mitigate the cost?

Thanks.

Hi ChenA, sorry for the late reply.

1. I’m not entirely sure anymore how the volumetric structure comes about, it’s either derived from the cubemaps which are runtime generated or precalculated.

2. If you did the kind of work this is doing at full resolution it would be impractical from a performance point of view. Doing it at lower resolution means you can take more samples and during the upscale interpolate to a higher resolution. Keeping it only at low resolution would probably not look acceptable, so this combination is needed.

Well done, but why no directx 12 and no rtx features?

Hi Lorenzitto,

A DX12 backend isn’t a trivial win in terms of performance unless you make a large overhaul of the engine, but does become more complicated in terms of management, so it’s a tradeoff.

The main reasons engines move to DX12 is to have more control (which comes at a maintenance cost as mentioned) and features. In this case, Mafia did an impressive job obtaining reflections and GI without the need for raytracing, which would actually probably just slow it all down without much additional gain, and restrict it to few high end platforms.

Another reason I know (from experience) why engines don’t move so quickly to newer APIs is when they’re multiplatform. At Tt Games some games have been released for 7-8 platforms and it was a lot of work for us to maintain and update.

The truth is we were overwhelmed by other things ~like a certain war somewhere~ so unlike at the previous versions DX9 up to 11.0, we didn’t yet have the time to do the same type of parrallel support that we did for the previous ones. We haven’t given up on this, we just had to resolve a few things and we are still in the process of explaining why all of this is very important to the people in charge of budgets.