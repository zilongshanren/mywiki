---
title: 'The Rendering of Middle Earth: Shadow of Mordor'
url: https://www.elopezr.com/the-rendering-of-middle-earth-shadow-of-mordor/
author: Redorav
published: '2017-12-27'
source_blog: The Code Corsair
source_site: http://www.elopezr.com
category: game programming
fetched: '2026-04-13'
---

[Middle Earth: Shadow of Mordor](https://en.wikipedia.org/wiki/Middle-earth:_Shadow_of_Mordor) was released in 2014. The game itself was a great surprise, and the fact that it was a spin-off within the storyline of the Lord of the Rings universe was quite unusual and it’s something I enjoyed. The game was a great success, and at the time of writing, [Monolith](https://en.wikipedia.org/wiki/Monolith_Productions) has already released the sequel, Shadow of War. The game’s graphics are beautiful, especially considering it was a cross-generation game and was also released on Xbox 360 and PS3. The PC version is quite polished and features a few extra graphical options and hi-resolution texture packs that make it shine.

The game uses a relatively modern deferred DX11 renderer. I used [Renderdoc](https://github.com/baldurk/renderdoc) to delve into the game’s rendering techniques. I used the highest possible graphical settings (ultra) and enabled all the bells and whistles like order-independent transparency, tessellation, screen-space occlusion and the different motion blurs.

**The Frame**

This is the frame we’ll be analyzing. We’re at the top of a wooden scaffolding in the Udun region. Shadow of Mordor has similar mechanics to games like Assassin’s Creed where you can climb buildings and towers and enjoy some beautiful digital scenery from them.

![](../../assets/47db86111f7fd33b.jpg)


**Depth Prepass**

The first ~140 draw calls perform a quick prepass to render the biggest elements of the terrain and buildings into the depth buffer. Most things don’t end up appearing in this prepass, but it helps when you’ve got a very big number of draw calls and a far range of view. Interestingly the character, who is always in front and takes a decent amount of screen space, does not go into the prepass. As is common for many open world games, the game employs reverse z, a technique that maps the near plane to 1.0 and far plane to 0.0 for increased precision at great distances and to prevent z-fighting. You can read more about z-buffer precision ![](../../assets/e67540ed3ef3b05b.png)


[here](https://developer.nvidia.com/content/depth-precision-visualized).


**G-buffer**

Right after that, the G-Buffer pass begins, with around ~2700 draw calls. If you’ve read my [previous analysis for Castlevania: Lords of Shadow 2](https://www.elopezr.com/castlevania-lords-of-shadow-2-graphics-study/) or have read other similar articles, you’ll be familiar with this pass. Surface properties are written to a set of buffers that are read later on by lighting passes to compute its response to the light. Shadow of Mordor uses a classical deferred renderer, but uses a comparably small amount of G-buffer render targets (3) to achieve its objective. Just for comparison, Unreal Engine uses between 5 and 6 buffers in this pass. The G-buffer layout is as follows:

**Normals Buffer**

R | G | B | A |
Normal.x | Normal.y | Normal.z | ID |

The normals buffer stores the normals in world space, in 8-bit per channel format. This is a little bit tight, sometimes not enough to accurately represent smoothly varying flat surfaces, as can be seen in some puddles throughout the game if paying close attention. The alpha channel is used as an ID that marks different types of objects. Some that I’ve found correspond to a character (255), an animated plant or flag (128), and the sky is marked with ID 1, as it’s later used to filter it out during the bloom phase (it gets its own radial bloom).

**Albedo Buffer**

R | G | B | A |
Albedo.r | Albedo.g | Albedo.b | Cavity Occlusion |

The albedo buffer stores all three albedo components and a small scale occlusion (sometimes called cavity occlusion) that is used to darken small details that no shadow mapping or screen space post effect could really achieve. It’s mainly used for decorative purposes, such as the crevices and wrinkles in clothes, small cracks in wood, the tiny patterns in Talion’s clothes, etc.


The albedo receives special treatment from a blood texture in the shader in the case of enemies (interestingly, Talion never receives any visible wounds). The blood texture is input to this stage when rendering enemies’ clothes and body, but it doesn’t specify the color of the blood, which is input in a constant buffer, instead it specifies blood multipliers/levels to control the amount of blood to show through. The normal orientation is also used to scale the effect, controlling the directionality of the blood splatter. The albedo then effectively gets tinted by the intensity of the wounds the enemy has received and at the location marked by the blood map, while also modifying other surface properties like specular to get a convincing blood effect. I haven’t been able to find the part of the frame where the map gets rendered, but I presume they’re written to right at the beginning of the frame when the sword impact takes place and then used here.



**Specular Buffer**

R | G | B | A |
Roughness | Specular Intensity | Fresnel | Subsurface Scattering |

The specular buffer contains other surface properties you’d expect from many games like roughness (it’s not really roughness but a scaled specular exponent, but can be interpreted as such), a specular intensity which scales the albedo to get an appropriate specular color, a reflectivity factor (typically would be called F0 in graphics literature as it’s the input to the Fresnel specular response) and a subsurface scattering component. This last component is used to light translucent materials such as thin fabric, plants and skin. If we delve into the lighting shader later on we find out that a variation of the [normalized Blinn-Phong](https://seblagarde.wordpress.com/2011/08/17/hello-world/) specular model is in use here.


**Deferred Decals**

As we’ve already seen, Shadow of Mordor goes to great lengths to show blood splatters on damaged characters. The environment also gets its own coating of dark orc blood as Talion swings his sword. However for the surroundings a different technique, [deferred decals](https://mtnphil.wordpress.com/2014/05/24/decals-deferred-rendering/), is used. This technique consists of projecting a set of flat textures onto the surface of whatever has been rendered before, thereby replacing the contents of the G-Buffer with this new content before the lighting pass takes place. For blood a simple blood splatter does the trick, and by rendering many in sequence one can quickly create a pretty grim landscape.


The last thing that gets rendered in the G-buffer pass is the sky, a very high-resolution (8192×2048) sky texture in HDR BC6H format. I’ve had to tonemap it a bit because in HDR all the colors are too dark.

**Tessellation**

A very interesting feature of the game (if enabled) is tessellation. It’s used for many different things, from terrain to character rendering (character props and objects also use it). Tessellation here doesn’t subdivide a low-res mesh, but actually creates polygons from a point cloud, with as much subdivision as necessary depending on level of detail criteria like distance to the camera. An interesting example here is Talion’s cape, which is sent to the GPU as a point cloud (after the physics simulation) and the tessellation shader reconstructs the polygons.

**Order-Independent Transparency**

One of the first things that struck me as odd was the hair pass, as it runs a very complicated special shader. The graphics options mention an OIT option for the hair so this must be it. It first outputs to a separate buffer and counts the total number of overlapping transparent pixels while at the same time storing the properties in a “deep” Gbuffer-like structure. Later on, a different shader properly sorts the individual fragments according to their depth. Arrows seem to be rendered using this as well (I guess those feathers in the back need proper sorting too). It’s a subtle effect and doesn’t add a lot of visual difference but it’s a nice addition nonetheless. As a simple example here’s an image showing the overlapping fragment count (redder is more fragments). Regular transparency is still depth sorted in the CPU and rendered like traditional alpha. Only very specific items get into the OIT pass.![](../../assets/1e63ccc5197c7449.png)



**Shadows of Mordor**

There are many sources of shadow in SoM. Aside from traditional shadow maps for the dynamic lights, SoM uses a two-channel screen-space ambient occlusion, micro-scale occlusion supplied for nearly all objects in the game, and a top-down heightmap-like occlusion texture.


**Screen-space occlusion**

The first pass renders screen-space ambient and specular occlusion using the gbuffer. The shader itself is a massive unrolled loop that samples both the full-size depth map and a previously downsampled averaged depth map looking for neighboring samples in a predefined pattern. It uses a square 4×4 texture to select pseudorandom vectors looking for occluders. It renders a noisy occlusion buffer, which is then smoothed via a simple two-pass blur. The most interesting feature here is that there are two different occlusion channels, one of them applied as specular occlusion, the other as diffuse. Typical SSAO implementations compute a single channel that applies to all baked lighting. Here the SSAO map is also read in the directional light pass and applied there.![](../../assets/feeb10a4b190af09.png)


**Shadow Maps**

The next event is shadow map rendering. Because it’s a mainly outdoors game, most of both the lighting and shadows come from a main directional light. The technique in use here is [Cascaded Shadow Maps](https://msdn.microsoft.com/en-us/library/windows/desktop/ee416307(v=vs.85).aspx) (a variation of which is [Parallel Split Shadow Maps](http://http.developer.nvidia.com/GPUGems3/gpugems3_ch10.html)), a fairly standard long-distance shadowing technique which consists of rendering the same scene from the same point of view of the light for different regions of space. Normally shadow maps further away from the camera span either a larger distance or are lower resolution than the previous ones, effectively trading resolution in regions where the detail isn’t needed anyway due to geometry being far away. In this scene the game is rendering three 4096×4096 shadow cascades (the game actually has space for four), the top cascade being very close to Talion, while the bottom cascade includes mountains and objects far away from the camera. The game’s shadows also use the same reverse z trick as the depth map.

**Shadow Buffer**

The next step is to create a shadowing buffer. This is a 1-channel texture that encodes a [0, 1] shadowing factor based on the occlusion information from the previous shadow maps. To create a bit of softness around the edges the shadow map is sampled 4 times with a special bilinear sampler state which takes 4 samples and compares against a given value (this is called [Percentage Close Filtering](http://http.developer.nvidia.com/GPUGems/gpugems_ch11.html)). Taking several samples and averaging their results is often called [Percentage Closer Soft Shadows](http://developer.download.nvidia.com/shaderlibrary/docs/shadow_PCSS.pdf). In addition to reading from the shadow map, the specular buffer’s last component is also sampled (recall that this is a subsurface scattering factor) and multiplied times a “light bleed factor”, which seems to attempt to remove shadowing from these objects to let a bit more light through.


**Directional Projection Texture**

Another source of light and shadow is a top-down texture that is sampled by the directional light. It’s a color tint to the main directional light’s color plus a global shadowing term that is applied to the directional lighting. Some of it seems to have been hand-authored on top of an automatically generated top-down lightmap of the level. The shadow edges for static geometry seem to have been tweaked by hand (perhaps to avoid conflicts with the actual shadow map) and some parts seem to have been colored in a bit by hand too. The purpose of this texture is probably adding large scale ambient occlusion and faking a bit of global illumination to the directional light in an inexpensive way. The slideshow below shows the color tint, the occlusion, and the product of both factors which gives an idea of what the final color mask looks like.


The result of all the light passes gets saved into an R11G11B10F render target. This is the what the result roughly looks like. I tonemapped the results to make the influence of the directional on the level much more evident.

All the faraway mountains (not shown in the above image) also get lit by directional lights but they’re special cased to be able to control the lighting better. Some are at scale but the ones further away are actually flat textures (impostors) with cleverly authored normal and albedo maps. They have special directional lights affecting just the mountains.

**Static Lighting**

Shadow of Mordor uses a very memory-intensive static lighting solution that involves some very big volume textures. The image below represent the three static light volume textures used for the diffuse lighting of a part of this area. They are each a whopping 512x512x128 BC6H compressed texture, which is to say 32MB per texture or 96MB total (we are playing in high quality settings after all). The Color texture represents an incoming irradiance to a voxel. The other two represent the strength or amount of that irradiance along all six xyz and -xyz directions, with the normal serving as a way to select three components (positive or negative xyz, the ones most aligned with the normal). Once we’ve constructed this vector, we do the dot product of it and the squared normal and this becomes the scale factor for the irradiance. As a formula, this looks like the following:



Static Light Volume Color

Static Light Volume Negative Direction

Static Light Volume Positive Direction

Static Light Volumes also render a cubemap for the specular lighting, which were probably captured at the center of the SLV. Interestingly enough, while the volume textures store HDR values compressed in BC6H, cubemaps are stored in BC3 format (aka as DXT5) which cannot store floating point values. To compensate for this limitation, the alpha channel stores an intensity that is later scaled from 1-10. It’s a bit of an odd decision and to me it looks more like legacy. Remember this game was also released on the previous generation which doesn’t support newer HDR texture formats.

The following sequence shows the before and after, with the actual contribution in the middle image. They have been tonemapped for visualization.


**Atmospheric Fog**

Shadow of Mordor has a weather and time of day system that’ll take Mordor from sunny skies to murky rains as you progress through the game. There are a sum of components that drive this system, fog being one of the most prominent. Shadow of Mordor uses a fairly simple but physically-grounded atmospheric fog model, including a single-scattering simulation of ![](../../assets/d17618029b0da2b6.jpg)


[Rayleigh](https://www.youtube.com/watch?v=twSg2zbjjnA)and Mie scattering.

It starts off by computing the position of the camera from the [center of Earth](https://en.wikipedia.org/wiki/Earth_radius). A few trigonometric calculations end up determining where within the atmosphere the camera is, where the pixel is, and how much of the atmosphere the ray has traveled given a maximum atmospheric height. In this case the atmospheric height is set to 65000 meters above the planet surface. With this information the Rayleigh and Mie coefficients are used to compute both types of fog particle densities and colors. These densities occlude the already shaded pixels by dispersing the light incoming to the camera from the shaded surface and add the contribution of the fog. The radiance and direction of the sun is taken into account to simulate this scattering.


**Exposure and Tonemapping**

Exposure takes on the fairly typical approach of successively downsampling a luminance buffer computed from the main HDR color buffer into a chain of textures, each of which is half the size of the previous texture, starting off with a texture that is 1/3rd of the main framebuffer. This downsampling takes 4 samples that average the neighboring pixels, so after collapsing all the averages into a single texel, the final result is the average luminance. After the texture reaches 16×9 texels, a compute shader is dispatched that adds up all the remaining texels. This value is immediately read in the tonemapping pass to adjust the luminance values.


Tonemapping uses a variation of the Reinhard operator whose optimized formula can be found [here](http://filmicworlds.com/blog/filmic-tonemapping-operators/) and [here](http://duikerresearch.com/2015/09/filmic-tonemapping-for-real-time-rendering/). In hlsl code it would look like the following:

1 2 3 4 | float3 hdrColor = tex2D(HDRTexture, uv.xy); hdrColor *= exposureValue; // This was calculated by the compute shader in the luminance downsampling pass float3 x = max(0.0, hdrColor - 0.004); float3 finalColor = (x * (6.2 * x + 0.5)) / (x * (6.2 * x + 1.7) + 0.06); |

If we plot this curve we can see that this operator pretty much discards 10% of the whites even at an input value of 2.0, while forcing a small part of the bottom range to fully black. This creates a desaturated, dark look.

**Alpha Stage**

The alpha stage is a bit unusual, as it renders objects directly into the LDR buffer. Other games render them into the HDR buffer as well so they can participate in the exposure pass. In any case, the previously computed luminance texture is bound to all the alpha lit objects (in some cases like emissive objects the exposure is performed via shader constants, not a texture lookup) and therefore exposure is automatically applied when drawing instead of as a post process. A very particular case of alpha in this game is when you go into the specter mode in the game (a mode where the spirit of Celebrimbor, who forges the rings of power in the LOTR universe, is rendered on top of you as a means to show that he is always present, although invisible). The game passes a few parameters into both character meshes which control the opacity and allows the game to partially occlude Talion and gradually reveal Celebrimbor. Other objects in the game also render ghost versions on top of the opaque object in specter mode, such as enemies and towers. Here is a different scene midway through the transition to the spectral world.


**Rain**

The main capture we’ve been looking at doesn’t show rain but weather is such an important part of the game I wanted to mention it here. It is generated and simulated in the GPU, and gets rendered right at the end of the alpha stage. A compute shader is dispatched that runs the simulation and writes positions to a buffer. These positions get picked up by another shader that renders as many instances of quads as positions were computed in the previous pass via an instanced indirect call. The vertex shader has a simple quad that gets deformed and oriented towards the camera as necessary. To avoid rain leaking through surfaces, the vertex shader also reads a top-down height map that allows it to discard any drops below an occluding surface. This height map is rendered right at the beginning of the frame. The same vertex shader tells the pixel shader where to sample from a raindrop texture; if the drop is close to a surface it selects a region of the texture that has a splash animation instead. Raindrops also run the fog computation in the pixel shader to blend seamlessly with the rest of the scene. Here’s a screenshot from the same point of view on a rainy day.


While the rain effect is active, the specular buffer is modified globally to produce wet surfaces, and rain waves are rendered into the normals buffer. The animation is tileable so only a single frame of the looping animation is used. The following normals buffer has been modified in order to see the ripples rendered into the buffer.

**Lens Flares and Bloom**

After all alpha has been rendered, lens flares get rendered on top. A series of offset quads are rendered starting at the point where the directional light is coming from (the sun in this case). Immediately after, the bloom pass is performed. This is a fairly standard technique, which consists of a series of downscaled and blurred textures that contain pixels whose luminance is above a certain threshold. There are two bloom passes, a general Gaussian blurred one for the scene and a special radial blur that only applies to the sky. The radiul blur is one use of the special ID in the normal map G-Buffer, since only pixels from the sky are taken into account. As a bonus, this blur samples the depth map and is able to produce some inexpensive [godrays](https://en.wikipedia.org/wiki/Crepuscular_rays). Because the buffer we’re working with at this stage is LDR, the bloom threshold isn’t what you’d expect from an HDR pipeline (values above a threshold, typically 1.0, trigger bloom), which means the amount of bloom you can get from it is a bit limited. It works for the game in any case and here are the results. In the images below the bloom mip colors look weird because every pixel is scaled by the luminance contained in the alpha channel. This luminance had been previously computed in the tonemapping pass. In the final composite the bloom is calculated as **bloom.rgb · bloom.a · bloomScale**



**AA + Depth of Field**

There isn’t much to say about these two as they’re relatively industry standard, a simple FXAA antialiasing pass is run right after bloom is composited onto the LDR image, and depth of field is performed immediately after. For the depth of field the game renders two downscaled blurred versions of the final buffer. Pixel depth is then used to blend between the blurred image and the normal one, giving it the unfocused appearance. I have exaggerated the depth of field for this capture for visualization purposes. The game has an in-game screenshot mode that allows you to very easily tweak these conditions.

**Motion Blur**

Motion blur consists of two passes. First, a fullscreen velocity buffer is populated from the camera’s previous and current orientation, filling the first two channels of the texture with a screen-space velocity. The r channel is how much a pixel has changed in the horizontal dimension of the screen, g channel for the vertical. That’s how you get radial streaks as you move the camera around. The characters are rendered again, this time populating the blue channel as well, using their current and previous poses just like with the camera. The blue channel is used to mark whether a character was rendered or not. The alpha channel is also populated with a constant value (0.0598) but I didn’t really investigate too much what it means or its purpose. The velocity buffer is then downsampled into a very small texture, by averaging a relatively wide neighborhood of velocities in the original texture. This will give each pixel in the final pass a rough idea of how wide the blur radius is going to be in the actual blur pass.

The blur pass then reads both velocity textures, the depth map, the original color buffer and a noise texture, that last one to hide the mirror image effect that can occur when doing this kind of blur with a large radius. The image buffer is then sampled several times in the direction the velocity buffer is pointing to, averaging the colors which ends up blurring the image in the direction of the motion vectors. The effect is also scaled by the frames per second the game is running at. For this capture, I had to cap the game at 30fps, as it was barely noticeable at 60fps+.


**Color Correction**

A final color correction pass is performed using “color cubes”. A color cube is a 3D texture whose rgb components map to the xyz coordinates of the texture. These xyz coordinates contain a color, the color we are going to replace the original color with. In this case the LUT was the neutral one (i.e. the coordinate and the color it contains are the same value) so I’ve modified the same scene with some of the different presets the game comes with in the camera editor.

**Final Frame**

After the main frame has finished, the UI is rendered onto a separate buffer. This guarantees that no matter the resolution you have chosen for the backbuffer in the game, the UI will always render crisp and nice into the native window size, while the game can vary its resolution if needed for performance. At the end, both textures are blended together based on the UI’s alpha channel and rendered into the final framebuffer, ready to be displayed.


I hope you’ve enjoyed reading this analysis, comments or doubts are welcome. I would like to thank [Adrian Courrèges](http://www.adriancourreges.com/) for his amazing work which has inspired this graphics study, and the team at [Monolith](https://www.lith.com/) for this truly memorable game.

Extremely interesting and useful, thanks for doing this!

Very nice work and well presented!

(And thanks for the mention.)

Interesting read!

Very well documented. Thanks for the efforts!

Very nice, and thorough, analysis!!

About the color curve, you say it gives a desaturated look. To be more precise, the steeper it is the more saturated it gets, and vice versa. So it actually saturates the lows and desaturates the highs (converging towards white).

Also, it seems to downscale or blur the image quite a couple of times. Any idea why they didn’t do it once only? For LDR/HDR compatibility?

Hi Beausoleil, It’s been a long time since I wrote this, but let me try my best to answer 🙂

With regards to the color curve you may be right about the lows being more saturated but I think my main point was that the lowest end is being clamped to 0, which can give it a darker look. I think the sRGB curve is embedded here too, so it may not actually be saturating like you think.

With regards to the blurs, different blurs have different purposes. For example a depth of field blur over the entire screen isn’t necessarily useful for bloom (where you may extract just the brightest colors and just blur that). Same applies to the radial blur, etc.

I’m a graphics newbie, so for me this is a massive learning experience as I’m in the process of creating a renderer myself. Just a quick question, if you are still reading comments:

How many times are the world objects rendered (besides from object-specific passes such as motion blur)?

I guess 1 time for gbuffer, and 3 times for shadow maps. But is this a correct assumption?

And again, thank you for doing such a detailed study. I really enjoyed reading this. 🙂

Hi Alexander,

I’m really glad you’re learning from the articles, that’s the point! With respect to your comments,

The number of times an object is rendered depends on the architecture of your engine (forward/deferred/visibility), but it could be rendered in

· Main pass: GBuffer in the deferred case

· Depth Prepass (no need if visibility buffer)

· Once per shadow map (for example 3 cascades as you point out)

For shadow maps and prepass you could be rendering proxies. The prepass is meant to be a cheap pass that later accelerates your rendering (in a forward renderer that isn’t necessarily true). For the shadow pass you could render a convex representation of your mesh or a lower LOD and it would work just as well. Software like Simplygon can do this automatically. What I mean is that an object isn’t necessarily rendered with the same geometry everywhere.

As for motion blur, depending on how you do it you could either render the object again or store motion vectors during the main pass and do it as a postprocess.

Let me know if there’s anything else you want to know.

“The prepass is meant to be a cheap pass that later accelerates your rendering (in a forward renderer that isn’t necessarily true).”

Could you explain further? I always thought the bigger offender in forward renderers was the overdraw?

Hi Beausoleil,

What I meant is that in a forward renderer you’ll typically find that the cost of doing everything in the shader (shadows, lighting, SSAO, GI, etc) is prohibitive, not just because of overdraw, but because of occupancy and shader variation complexity issues as well.

You start pulling features out to run outside the main pass and the easiest stuff is what only depends on depth (shadows, SSAO), so you can end up needing to perform a complete Z-Prepass, which isn’t cheap anymore. Overdraw is definitely an issue in forward renderers, but a full prepass solves it at a relatively large cost.

Hi,

If you are still reading comments here (you were very friendly at writing back last year 🙂 ), I got an idea today and decided to post about it:

https://github.com/KhronosGroup/Vulkan-Docs/issues/2202

Briefly, it’s about an optimized texture format for normal compression

I don’t really know anyone with the expertise to comment on it, and I’m eager to learn! Also, I was motivated to ask you because you explicitly comment on the drawbacks of using 8-bit normal vectors in this article.

Anyways, if you read this, and have the time, I would really love some feedback!

Best,

Alexander

I’ve replied in the Github issue 🙂

Thank you Emilio, I really appreciate it! I’m reading with great interest, though I haven’t really done enough programming with normal blending to really understand the issue with blend+ONV. Maybe I’ll figure it out. 🙂

I’ve seen that reconstruction being used a lot in the past. Remember you’re in texture space, so it makes no sense to point the normal toward the inside of the shape (total opposite of the polygon’s normal).

This means you can forget about your sign bit and simply use a 2×16bit texture format(RG16). This also means you don’t have to do filtering by hand.

But you’d still be using 32bit for the normals. On the other hand, one could probably go 24bit and use the 3rd channel not for the Z but for a scaling value to apply to the XY. I mean, most of the time those are pointing up, so the XY is really small. If we want (cheap) accuracy, we could normalize the XY and store the normal’s length in Z. (similar to what we do with some HDRi formats).

Now I wonder: would that play well when interpolating, or should we use some custom sampling?

I think I may have formulated my line of thinking a bit obscured..

What I meant is to _only_ create a texture format for a gbuffer normal attachment, as I’ve recently learned that RGTC is often used for normal maps (which is reconstruction from 2 compressed channels). So the fragment shader for gbuffer recording would sample the normal for the model’s surface, transform it into world space (or view space), and then store in the r16g15a1 attachment.

And this normal might contain negative values, no?

I just read somewhere that the normal reconstruction is often done manually, and thought a specialized attachment format could help lower memory requirements for gbuffers. At the same time, this new r16g15a1 format could be used side-by-side with r16g16b16 without changing the shader, as the normal reconstruction is handled by the texture sampler.

But I don’t really know if this is a useful thing or not.

Yeah my bad, I misread your post 🙂

In any case, depending on the kind of geometry you’re dealing with, the same rule can apply: front-facing normals might well be culled already. So you can assume the direction of the Z, and go with RG* formats.

As always foliage could be a notable exception, but still, interpreting the normal so it always points the camera is probably what you want. (Otherwise your artist will “double-side” the geometry for the same end-result)