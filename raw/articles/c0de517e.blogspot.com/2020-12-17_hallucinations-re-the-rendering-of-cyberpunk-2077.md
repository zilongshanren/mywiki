---
title: 'Hallucinations re: the rendering of Cyberpunk 2077'
url: https://c0de517e.blogspot.com/2020/12/hallucinations-re-rendering-of.html
published: '2020-12-17'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

**Introduction**

Two curses befall rendering engineers. First, we lose the ability to look at reality without being constantly reminded of how fascinatingly hard it is to solve light transport and model materials.

Second, when you start playing any game, you cannot refrain from trying to reverse its rendering technology (which is particularly infuriating for multiplayer titles - stop shooting at me, I'm just here to look how rocks cast shadows!).

So when I bought Cyberpunk 2077 I had to look at how it renders a frame. It's very simple to take RenderDoc captures of it, so I had really no excuse.

The following are speculations on its rendering techniques, observations made while skimming captures, and playing a few hours.

It's by no means a serious attempt at reverse engineering. For that, I lack both the time and the talent. I also rationalize doing a bad job at this by the following excuse: it's actually better this way.

I think it's better to dream about how rendering (or anything really) could be, just with some degree of inspiration from external sources (in this case, RenderDoc captures), rather than exactly knowing what is going on.

If we know, we know, there's no mystery anymore. It's what we do not know that makes us think, and sometimes we exactly guess what's going on, but other times we do one better, we hallucinate something new... Isn't that wonderful?

The following is mostly a read-through of a single capture. I did open a second one to try to fill some blanks, but so far, that's all.

|

I made the captures at high settings, without RTX or DLSS as RenderDoc does not allow these (yet?). I disabled motionblur and other uninteresting post-fx and made sure I was moving in all captures to be able to tell a bit better when passes access previous frame(s) data.

I am also not relying on insider information for this. Makes everything easier and more fun.

**The basics**

At a glance, it doesn't take long to describe the core of Cyberpunk 2077 rendering.

It's a classic deferred renderer, with a fairly vanilla g-buffer layout. We don't see the crazy amount of buffers of say, Suckerpunch's PS4 launch Infamous:Second Son, nor complex bit-packing and re-interpretation of channels.

![]() |

- 10.10.10.2 Normals, with the 2-bit alpha reserved to mark hair
- 10.10.10.2 Albedo. Not clear what the alpha is doing here, it seems to just be set to one for everything drawn, but it might be only the captures I got
- 8.8.8.8 Metalness, Roughness, Translucency and Emissive, in this order (RGBA)
- Z-buffer and Stencil. The latter seems to isolate object/material types. Moving objects are tagged. Skin. Cars. Vegetation. Hair. Roads. Hard to tell / would take time to identify the meaning of each bit, but you get the gist...

If we look at the frame chronologically, it starts with a bunch of UI draws (that I didn't investigate further), a bunch of copies from a CPU buffer into VS constants, then a shadowmap update (more on this later), and finally a depth pre-pass.

![]() |

This depth pre-pass is partial (not drawing the entire scene) and is only used to reduce the overdraw in the subsequent g-buffer pass.

Basically, all the geometry draws are using instancing and some form of bindless textures. I'd imagine this was a big part of updating the engine from The Witcher 3 to contemporary hardware.

Bindless also makes it quite annoying to look at the capture in renderDoc unfortunately - by spot-checking I could not see too many different shaders in the g-buffer pass - perhaps a sign of not having allowed artists to make shaders via visual graphs?

Other wild guesses: I don't see any front-to-back sorting in the g-buffer, and the depth prepass renders all kinds of geometries, not just walls, so it would seem that there is no special authoring for these (brushes, forming a BSP) - nor artists have hand-tagged objects for the prepass, as some relatively "bad" occluders make the cut. I imagine that after culling a list of objects is sorted by shader and from there instanced draws are dynamically formed on the CPU.

The opening credits do not mention Umbra (which was used in The Witcher 3) - so I guess CDPr rolled out their own visibility solution. Its effectiveness is really hard to gauge, as visibility is a GPU/CPU balance problem, but there seem to be quite a few draws that do not contribute to the image, for what's worth. It also looks like that at times the rendering can display "hidden" rooms, so it looks like it's not a cell and portal system - I am guessing that for such large worlds it's impractical to ask artists to do lots of manual work for visibility.
![]() |

Looks like some non-visible rooms are drawn then covered by the floor - which might hint at culling done without old-school brushes/BSP/cell&portals?

Lastly, I didn't see any culling done GPU side, with depth pyramids and so on, no per-triangle or cluster culling or predicated draws, so I guess all frustum and occlusion culling is CPU-side.

*Note: people are asking if "bad" culling is the reason for the current performance issues, I guess meaning on ps4/xb1. This inference cannot be done, nor the visibility system can be called "bad" - as I wrote already. FWIW - it seems mostly that consoles struggle with memory and streaming more than anything else. Who knows...*

Let's keep going... After the main g-buffer pass (which seems to be always split in two - not sure if there's a rendering reason or perhaps these are two command buffers done on different threads), there are other passes for moving objects (which write motion vectors - the motion vector buffer is first initialized with camera motion).

This pass includes avatars, and the shaders for these objects do not use bindless (perhaps that's used only for world geometry) - so it's much easier to see what's going on there if one wants to.

Finally, we're done with the main g-buffer passes, depth-writes are turned off and there is a final pass for decals. Surprisingly these are pretty "vanilla" as well, most of them being mesh decals.

Mesh decals bind as inputs (a copy of) the normal buffer, which is interesting as one might imagine the 10.10.10 format was chosen to allow for easy hardware blending, but it seems that some custom blend math is used as well - something important enough to pay for the price of making a copy (on PC at least).

![]() |

It looks like only triangles carrying decals are rendered, using special decal meshes, but other than that everything is remarkably simple. It's not bindless either (only the main static geometry g-buffer pass seems to be), so it's easier to see what's going on here.

At the end of the decal pass we see sometimes projected decals as well, I haven't investigated dynamic ones created by weapons, but the static ones on the levels are just applied with tight boxes around geometry, I guess hand-made, without any stencil-marking technique (which would probably not help in this case) to try to minimize the shaded pixels.

Projected decals do bind depth-stencil as input as well, obviously as they need the scene depth, to reconstruct world-space surface position and do the texture projection, but probably also to read stencil and avoid applying these decals on objects tagged as moving.

![]() |

As for the main g-buffer draws, many of the decals might end up not contributing at all to the image, and I don't see much evidence of decal culling (as some tiny ones are draws) - but it also might depend on my chosen settings.

The g-buffer pass is quite heavy, but it has lots of detail and it's of course the only pass that depends on scene geometry, a fraction of the overall frame time. E.g. look at the normals on the ground, pushed beyond the point of aliasing. At least on this PC capture, textures seem even biased towards aliasing, perhaps knowing that temporal will resolve them later (which absolutely does in practice, rotating the camera often reveals texture aliasing that immediately gets resolved when stopped - not a bad idea, especially as noise during view rotation can be masked by motion blur).

|

**A note re:Deferred vs Forward+**

Most state-of-the-art engines are deferred nowadays. Frostbite, Guerrilla's Decima, Call of Duty BO3/4/CW, Red Dead Redemption 2, Naughty Dog's Uncharted/TLOU and so on.

On the other hand, the amount of advanced trickery that Forward+ allows you is unparalleled, and it has been adopted by a few to do truly incredible rendering, see for example the latest Doom games or have a look at the mind-blowing tricks behind Call of Duty: Modern Warfare / Warzone (and the previous Infinity Warfare which was the first time that COD line moved from being a crazy complex forward renderer to a crazy complex forward+).

I think the jury is still out on all this, and as most thing rendering (or well, coding!) we don't know anything about what's optimal, we just make/inherit choices and optimize around them.

That said, I'd wager this was a great idea for CP2077 - and I'm not surprised at all to see this setup. As we'll see in the following, CP2077 does not seem to have baked lighting, relying instead on a few magic tricks, most of which operating in screen-space.

For these to work, you need before lighting to know material and normals, so you need to write a g-buffer anyways. Also you need temporal reprojection, so you want motion vectors and to compute lighting effects in separate passes (that you can then appropriately reproject, filter and composite).

I would venture to say also that this was done not because of the need for dynamic GI - there's very little from what I've seen in terms of moving lights and geometry is not destructible. I imagine instead, this is because the storage and runtime memory costs of baked lighting would be too big. Plus, it's easier to make lighting interactive for artists in such a system, rather than trying to write a realtime path-tracer that accurately simulates what your baking system results would be...

**Lighting part 1: Analytic lights**

Obviously, no deferred rendering analysis can stop at the g-buffer, we split shading in two, and we have now to look at the second half, how lighting is done.

Here things become a bit dicier, as in the modern age of compute shaders, everything gets packed into structures that we cannot easily see. Even textures can be hard to read when they do not carry continuous data but pack who-knows-what into integers.

![]() |

|

Also, note that this happens after hair rendering - which we didn't cover.

It first packs normal and roughness into a RGBA8 using Crytek's lookup-based best-fit normal encoding, then it creates a min-max mip pyramid of depth values.

The pyramid is then used to create what looks like a volumetric texture for clustered lighting.

The clusters seem to be 32x32 pixels in screen-space (froxels), with 64 z-slices. The lighting though seems to be done at a 16x16 tile granularity, all via compute shader indirect dispatches.

I would venture this is because CS are specialized by both the materials and lights present in a tile, and then dispatched accordingly - a common setup in contemporary deferred rendering systems (e.g. see Call of Duty Black Ops 3 and Uncharted 4 presentations on the topic).

Analytic lighting pass outputs two RGBA16 buffers, which seems to be diffuse and specular contributions. Regarding the options for scene lights, I would not be surprised if all we have are spot/point/sphere lights and line/capsule lights. Most of Cyberpunk's lights are neons, so definitely line light support is a must.

You'll also notice that a lot of the lighting is unshadowed, and I don't think I ever noticed multiple shadows under a single object/avatar. I'm sure that the engine does not have limitations in that aspect, but all this points at lighting that is heavily "authored" with artists carefully placing shadow-casting lights. I would also not be surprised if the lights have manually assigned bounding volumes to avoid leaks.

![]() |

**Lighting part 2: Shadows**

But what we just saw does not mean that shadows are unsophisticated in Cyberpunk 2077, quite the contrary, there are definitely a number of tricks that have been employed, most of them not at all easy to reverse!

First of all, before the depth-prepass, there are always a bunch of draws into what looks like a shadowmap. I suspect this is a CSM, but in the capture I have looked at, I have never seen it used, only rendered into. This points to a system that updates shadowmaps over many frames, likely with only static objects?

![]() |

These multi-frame effects are complicated to capture, so I can't say if there are further caching systems (e.g. see the quadtree compressed shadows of Black Ops 3) at play.

One thing that looks interesting is that if you travel fast enough through a level (e.g. in a car) you can see that the shadows take some time to "catch up" and they fade in incrementally in a peculiar fashion. It almost appears like there is a depth offset applied from the sun point of view, that over time gets reduced. Interesting!

![]() |

There's surely a lot to reverse-engineer here if one was inclined to do the work!

All other shadows in the scene are some form of VSMs, computed again incrementally over time. I've seen 512x512 and 256x256 used, and in my captures, I can see five shadowmaps rendered per frame, but I'm guessing this depends on settings. Most of these seem only bound as render targets, so again it might be that it takes multiple frames to finish rendering them. One gets blurred (VSM) into a slice of a texture array - I've seen some with 10 slices and others with 20.

Finally, we have what the game settings call "contact shadows" - which are screen-space, short-range raymarched shadows. These seem to be computed by the lighting compute shaders themselves, which would make sense as these know about lights and their directions...

Overall, shadows are both simple and complex. The setup, with CSMs, VSMs, and optionally raymarching is not overly surprising, but I'm sure the devil is in the detail of how all these are generated and faded in. It's rare to see obvious artifacts, so the entire system has to be praised, especially in an open-world game!

**Lighting part III: All the rest...**

Since booting the game for the first time I had the distinct sense that most lighting is actually not in the form of analytic lights - and indeed looking at the captures this seems to not be unfounded. At the same time, there are no lightmaps, and I doubt there's anything pre-baked at all. This is perhaps one of the most fascinating parts of the rendering.

![]() |

It looks like it's computing bent normals and aperture cones - impossible to tell the exact technique, but it's definitely doing a great job, probably something along the lines of HBAO-GTAO. First, depth, normal/roughness, and motion vectors are all downsampled to half-res. Then a pass computes current-frame AO, and subsequent ones do bilateral filtering and temporal reprojection. The dithering pattern is also quite regular if I had to guess, probably Jorge's Gradient noise?

It's easy to guess that the separate diffuse-specular emitted from the lighting pass is there to make it easier to occlude both more correctly with the cone information.

![]() |

Second, we have to look at indirect lighting. After the light clustering pass there are a bunch of draws that update a texture array of what appear to be spherically (or dual paraboloid?) unwrapped probes. Again, this is distributed across frames, not all slices of this array are updated per frame. It's not hard to see in captures that some part of the probe array gets updated with new probes, generating on the fly mipmaps, presumably GGX-prefiltered.

![]() |

The source of the probe data is harder to find though, but in the main capture I'm using there seems to be something that looks like a specular cubemap relighting happening, it's not obvious to me if this is a different probe from the ones in the array or the source for the array data later on.

Also, it's hard to say whether or not these probes are hand placed in the level, if the relighting assumption is true, then I'd imagine that the locations are fixed, and perhaps artist placed volumes or planes to define the influence area of each probe / avoid leaks.

![]() |

We have your "standard" volumetric lighting, computed in a 3d texture, with both temporal reprojection. The raymarching is clamped using the scene depth, presumably to save performance, but this, in turn, can lead to leaks and reprojection artifacts at times. Not too evident though in most cases.

![]() |

Now, things get very interesting again. First, we have an is an amazing Screen-Space Reflection pass, which again uses the packed normal/roughness buffer and thus supports blurry reflections, and at least at my rendering settings, is done at full resolution.

It uses previous-frame color data, before UI compositing for the reflection (using motion vectors to reproject). And it's quite a lot of noise, even if it employs a blue-noise texture for dithering!

![]() |

Then, a indirect diffuse/ambient GI. Binds the g-buffer and a bunch of 64x64x64 volume textures that are hard to decode. From the inputs and outputs one can guess the volume is centered around the camera and contains indices to some sort of computed irradiance, maybe spherical harmonics or such.

The lighting is very soft/low-frequency and indirect shadows are not really visible in this pass. This might even by dynamic GI!

Certainly is volumetric, which has the advantage of being "uniform" across all objects, moving or not, and this coherence shows in the final game.

![]() |

And here is where we can see what I said at the beginning. Most lighting is not from analytic lights! We don't see the usual tricks of the trade, with a lot of "fill" lights added by artists (albeit the light design is definitely very careful), instead indirect lighting is what makes most of the scene. This indirect lighting is not as "precise" as engines that rely more heavily on GI bakes and complicated encodings, but it is very uniform and regains high-frequency effects via the two very high-quality screen-space passes, the AO and reflection ones.

The screen-space passes are quite noisy, which in turn makes temporal reprojection really fundamental, and this is another extremely interesting aspect of this engine. Traditional wisdom says that reprojection does not work in games that have lots of transparent surfaces. The sci-fi worlds of Cyberpunk definitely qualify for this, but the engineers here did not get the news and made things work anyway!

And yes, sometimes it's possible to see reprojection artifact, and the entire shading can have a bit of "swimming" in motion, but in general, it's solid and coherent, qualities that even many engines using lightmaps cannot claim to have. Light leaks are not common, silhouettes are usually well shaded, properly occluded.

**All the rest**

There are lots of other effects in the engine we won't cover - for brevity and to keep my sanity. Hair is very interesting, appearing to render multiple depth slices and inject itself partially in the g-buffer with some pre-lighting and weird normal (fake anisotropic?) effect. Translucency/skin shading is surely another important effect I won't dissect.

![]() |

Before the frame is over though, we have to mention transparencies - as more magic is going on here for sure. First, there is a pass that seems to compute a light chart, I think for all transparencies, not just particles.

Glass can blur whatever is behind them, and this is done with a specialized pass, first rendering transparent geometry in a buffer that accumulates the blur amount, then a series of compute shaders end up creating three mips of the screen, and finally everything is composited back in the scene.

After the "glass blur", transparencies are rendered again, together with particles, using the lighting information computed in the chart. At least at my rendering settings, everything here is done at full resolution.

|

Finally, the all-mighty temporal reprojection. I would really like to see the game without this, the difference before and after the temporal reprojection is quite amazing. There is some sort of dilated mask magic going on, but to be honest, I can't see anything too bizarre going on, it's astonishing how well it works.

Perhaps there are some very complicated secret recipes lurking somewhere in the shaders or beyond my ability to understand the capture.

|

|

I wrote "finally" because I won't look further, i.e. the details of the post-effect stack, things here are not too surprising. Bloom is a big part of it, of course, almost adding another layer of indirect lighting, and it's top-notch as expected, stable, and wide.

Depth of field, of course, tone-mapping and auto-exposure... There are of course all the image-degradation fixings you'd expect and probably want to disable: film grain, lens flares, motion blur, chromatic aberration... Even the UI compositing is non-trivial, all done in compute, but who has the time... Now that I got all this off my chest, I can finally try to go and enjoy the game! Bye!

## 13 comments:

Please, write more on the topic! I am curious how many things you'd be able to pick :-D Gj so far ;)

Great research.

One issue I see is that post pictures are lowres.

GI: A bunch of volume textures centered on the camera with hard to decode contents that only seems to do low frequency diffuse and no indirect shadows...


Seems like cascaded light propagation volumes (Crytek) to me .

"The raymarching is clamped using the scene depth, presumably to save performance"

Do you mean it's culled or clamped like:

z = min( z, depthZ)

?

If later, how is this optimization? Cache?

The hair rendering with depth slices is most likely Deep Opacity Maps (or some similar technique). For those interested: http://www.cemyuksel.com/research/deepopacity. It's used for "blending" semi-transparent strands of hair in the correct order. @C0DE517E: were you able to figure out how many such depth slices they are doing per hair style?

Anonymous #1 - I don't think it's LPV, these would be easier to "see" in RenderDoc as they store color-ish stuff. Also I don't see any voxelization of the scene. I also did not see anything destructible in the world, so I would not be surprised if some for of visibility for GI is baked in the level data.



Anonymous #2 - I mean the volumetric lighting & its raymarching stop when a surface is "hit" - the process does not go beyond visible surfaces - using the scene z-buffer to stop the volumetric marching. This allows you at a given point to stop processing froxels far away, but it also means you will see disocclusions which can be quite evident as now you have a very low-res buffer (froxels are big on the screen). Note that the main reason for computing volumetrics in a volume texture is to make temporal reprojection easier, otherwise you can just raymarch in screenspace in a low-res 2d buffer (well, another advantage is that you can then also do volumetrics correctly on transparencies, but you can hack that in 2d too - e.g. that's how COD:BO3 works, emitting 4 layers out of the 2d marching).

Erik - I really didn't spend time there - imagining it is indeed one of the "known" techniques - but in all these things the devil is in the details, details that I do not really want to go and reverse... FWIW, hair looks really good - e.g. in the character creator.

The analysis of obsolete, broken-by-design rasterization renderer.

This is very interesting, thank you. I think people are interested in explanation of why the hell it is so slow and why settings don't really affect FPS. Why is it only the resolution that matters, and why FPS stays low even in closed rooms without complex geometry. Would it be possible for devs to fix that?

Mikhail - I cannot say much about any of that because it's hard to profile stuff from a capture, and even then you only have the picture from the GPU point of view, know nothing about CPU.








We can try to reason though around what you told me.

If you say that in your or many cases resolution is the thing that affects framerate most then it should follow that you are GPU-bound, not CPU-bound, which in a way is great, as at least with GPUs you can always find ways to scale, while CPU issues in many cases really require to wait for engineers to change code.

As for why performance does not seem to depend on the scene, well you said that resolution is the main thing that changes performance, which seems to point that the problem is not how many objects you're drawing or how many vertices, so it is not surprising that it's less affected by the scene.

Deferred engines tend to look like this a bit more than forward engines, by design. If they are not CPU-bound, then the only pass that depends on objects and vertices is the g-buffer pass, all the rest of rendering works in screen-space and it is completely independent from what geometry you have, once the g-buffer is done, it doesn't matter if it contained 10 objects of 1000000. This is good, in general, a desired characteristic.

Why other settings affect FPS less? Well, not sure, but consider that resolution is a very powerful lever. If you, say, try to do half of the work per pixel in a given effect, say the awesome SSAO or SSR they have, then at best you're saving half of the time, but in practice often it's less as there are other costs to pay to move memory around and so on, that do not depend on the work you're doing per-pixel.

If you drop the amount of pixels you render on the other hand, you're for sure eliminating that work completely. And many effects cannot do "less work" at all, they do not have quality controls. Dropping resolution affects absolutely everything, not just a few things developers found the way to expose in settings...

Lastly, resolution is quadratic, e.g. going from 4k to 1080p gives you 4 times less work, not 2 times...

You should load up nsight to profile the RTX and DLSS. I might do that tonight or tomorrow.

>quadtree compressed shadows of Black Ops 3

Could you please give paper name or some link?

Thanks.

Anonymous: https://research.activision.com/publications/archives/sparse-shadow-trees


In general, all ATVI R&D stuff, from either studios or central technology, should be on research.activision.com, so it's not hard to find :)

This is so interesting!

One thing I am really curious about is how the shadows on particle billboards were handled, for smoke and dust effects for example. Depending on the amount of particles, this seems to approximate volumetric shadows quite well. Are they CSMs projected onto the animated smoke? I'm having a hard time understanding how this was handled when the light is incoming from the opposite side of the particle.

Post a Comment