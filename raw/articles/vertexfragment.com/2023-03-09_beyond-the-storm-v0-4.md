---
title: Beyond the Storm - v0.4
url: https://www.vertexfragment.com/ramblings/bts-v04/
author: Steven Sell
published: '2023-03-09'
source_blog: Vertex Fragment
source_site: https://www.vertexfragment.com/
category: graphics
fetched: '2026-04-13'
---

[Performance](https://www.vertexfragment.com#performance)[World Generation](https://www.vertexfragment.com#world-generation)[Terrain and Terraforming](https://www.vertexfragment.com#terrain-and-terraforming)[Ocean Water](https://www.vertexfragment.com#ocean-water)[Other Changes](https://www.vertexfragment.com#other-changes)[Statistics](https://www.vertexfragment.com#statistics)[Next in v0.5](https://www.vertexfragment.com#next-in-v05)[Thanks](https://www.vertexfragment.com#thanks)

The focus for v0.4 of *Beyond the Storm* (BTS) was on the following:

- Performance
- World Generation
- Terrain and Terraforming
- Ocean Water

Of course a host of other features and bug fixes were also touched on in this version.

A lot of effort was put into improving the performance of world generation as well as static data saving. Naturally time was spent on runtime performance, but that mostly came down to tuning world segment streaming distance cutoffs.

Generally, world generation of a 16 km^2 terrain was reduced from several minutes down to less than 20 seconds. Additionally, coming out of v0.3 it took ~30 seconds to save a terrain of that size. It now takes less than 5 seconds for the post-world generation save (*The Big Save*), and a negligible amount of time (no stuttering) during in-game runtime saves.

This was accomplished by lots and lots of profiling, and by parallelizing work where possible, using both a custom thread pool and also by offloading work to the GPU. Performance will always be a concern, especially as world size and complexity continues to grow. But the work done in this version provides a lot more stable platform to build off of.

There was also a huge performance boost to entity streaming during loading, which was a huge relief as it was turning into a large bottleneck that was starting to impact and influence world design due to perceived entity limits. In reality, an intentional stream limiter used during runtime data streaming was in place during game load that shouldn’t have been. During runtime this allocates only 1-2 ms per frame to streaming in entities from new segments, but during loading we don’t want any such limitations. Oops!

![](../../assets/df8033864b317759.png)


World generation was probably *the* focus of this version, and not just in terms of performance. Several new world generation modules were added, and nearly all preexisting ones were updated in some way, whether by creating GPU-based versions of the module or by expanding their functionality.

World generation is now composed of multiple zone generators, instead of a single giant generator. Each zone specifies an area in which it operates and has its own scoped modules that work in isolation. This allows for the generation of terrain/islands using logic and resources completely separate from the rest of the world.

As the game will be island-based this allows for the generation of distinct and interesting island bodies. It also allows for the world to scale up to allow for a large ocean in which the islands exist, without adding additional overhead for empty world segments.

A new heightmap module was added - a GPU-accelarated Diamond-Square implementation. [This implementation is covered in its own ramble.](https://www.vertexfragment.com/ramblings/diamond-square/)

Additionally all FBM-based height modules (simplex, texture, etc.) were enhanced with the introduction of three new noise modifiers: squared, ridges, and valleys. There were plans to implement other modifiers such as distortion but those were not done (yet).

There was a good bit of time spent into optimizing the flow of data between heightmap modules (both generation modules and processing modules such as smoothing) in order to improve performance. This includes more efficient data transfers, as well as being more mindful of module ordering to limit the amount of times data has to be bussed between the CPU and GPU.

This could be lumped in with *Heightmap Generation* but it feels worthy of its own section.

Three algorithms for heightmap erosion were implemented: particle, grid, and river. Each implementation has its pros and cons (and I still want to write a ramble on them), but ultimately river network erosion proved to be the most viable for our use-case.

In addition to heightmap erosion, this also provides a framework for generating actual rivers across the terrain in a future version.

![](../../assets/8a858ef3f12d42a2.png)


In version v0.3 we got rid of the last vestiges of the built-in Unity terrain system. At the time I thought I was done working on terrain, at least for the near future. And I was wrong!

Previously the terrain mesh was thought to be static, once world generation was done.

However this version I unexpectedly implemented terraforming and so changes had to be made to save out terrain changes at runtime in an efficient manner. A new set of internal tools were also introduced to manipulate the mesh, and its heightmaps, during both world generation and runtime.

This one is a really technical detail, but a cool detail (at least to me).

In earlier versions the terrain material used a fairly standard approach to its splatmaps - one or more `RGBA32`

textures. Each channel (R, G, B, A) mapped to a different index into a texture array. The texture array then mapped to the base, low, and high slope textures for a specific region. So for each splat map I could support and blend between 4 distinct texture array indices. This is sufficient for basic test maps, but there has always been a concern about more complex terrains and the relatively low limit of 4 regions per segment (and their 12 terrain textures).

One solution, the common solution, is to add more splat maps. Each additional map means you can support 4 more regions and their associated slope-based textures.

But I never liked that solution for two reasons: it just kept moving the goal posts on the texture limit, and it keeps introducing additional texture samples for blending (even when using ShaderLab features to statically compile out unused code for segments that used less textures).

So I instead opted to use an encoded `RFloat`

splat texture and I redesigned the source texture array. I am sure others have done this before, but to me it was a novel solution to the problem. In brief it allows up to 999 distinct texture splats on each terrain segment mesh while also reducing previous bloat/duplications that was present in the arrays. Neat!

It was always in the plan to have terraforming, as it is pretty much required in order to build larger structures on uneven terrain. However it was not planned to be worked on for at least a couple of more versions. But then I got tired of never having anywhere flat enough to build.

There are 3 terraforming modes, currently accessed through equipping and arming the Shovel:

- Raise - which raises the selected terrain cell by a fixed amount up to a slope limit.
- Lower - which lowers the selected terrain cell by a fixed amount up to a slope limit.
- Flatten - which sets the selected terrain cell y-value to be equal to the y-value of the cell the player is standing on, if its under a slope limit.

The raise/lower amounts and the slope limit are configurable in the item description and can vary between tools.

Originally I had the flatten action affecting a 3x3 square of cells, but it was unintuitive when running into slope limits on corner points. So all actions are on single terrain cells.

![](../../assets/691e238f918a6a49.png)


Water, and buoyancy, were introduced in v0.3 and like other changes in this version I did not plan on revisiting them so soon. To put it mildly, I hate working on water.

However as the world generation moved to a focus on islands, it became imperative to me for the water to look better. It was OK before with its depth gradients, refraction, caustics, etc. but it felt *flat*, especially in open ocean areas.

I went back and looked at some other water implementations and found two things that really helped give height to the water: wave height gradients and surface foam.

The wave height gradient essentially just lightens the wave the taller it is, giving it the appearance of being thinner. In a more sophisticated water simulation we would [have subsurface scattering](https://www.shadertoy.com/view/4tlcWj) lighting up the wave interior. But this is not a sophisticated simulation.

Then the surface foam was added, which I admittedly did not think it would help as much as it did. It really made a world of difference in making the wave peaks pop out.

Once height was added, it needed to be removed so that waves would not pass through the terrain when the surface was near sea level.

This was accomplished by adding a new custom render pass that populated a “World Y” texture. This is another `RFloat`

texture (these are popping up all over the place) that simply records the absolute world-space y value in an area around the main camera. This texture is then sampled to diminish the waves as the y increases and the water becomes shallower.

Obviously I knew this would keep waves from poking through, but like the surface foam I didn’t quite realize how much it helped the feel and look of the ocean along shorelines.

Tessellating the ocean water is an obvious step, and I first did this ~12 years ago. However last version I was tired of water and put it off until the future.

Fortunately adding tessellation was very simple and just a matter of hooking in my existing generic tessellation framework from the terrain grass effect. Naturally this helped the visuals of the ocean water, but moreso it helps to make buoyancy feel better as the visuals now more closesly align with the CPU-side simulation.

![](../../assets/5d8ff170f83d6eee.png)


Those were the big topics that I felt like talking about, but not nearly everything that was done in this version. Below is a list of other changes (some minor, some major) that were done in v0.4.

**Animation**

- Attack/Swing styles.
- Armed and disarmed stances and attach points.
- Fix various animation bugs around water.

**Content**

- New character model.
- Crystals! Shiny and glowy.
- Breakable rocks.
- Pickaxe to break breakable rocks.
- Shovel to dig, and raise, and flatten.
- Mallet to build.
- Clothing equipment (shirt and pants).
- Rigging said clothing equipment.
- The Big Tree of Big Tree Island.
- Portal stones, since swimming between islands takes a long time.
- Finally a “Shabby Wood Foundation” buildable.

**Database (Dynamic Save / Load)**

- Clock time saved to database.
- Wind properties saved to database.
- Door and light state saved to database.
- New database commands.

**Effects and Visuals**

- Thickness texture. Had big plans for it, and then never used it.
- Improved screen shake.
- Shadow tweaks (both cascade cutoffs and appearance).
- Regrowth map to faciliate loss and regrowth of grass in terraformed areas. This is pretty neat.
- Hue variation for grass.

**General Engine**

- Reworked loading addressables.
- Buildables are officially entities, and no longer a hybrid.
- Safety-net to catch entities that fall through the world.

**GUI**

- Reworked input mode switching.
- Terraforming overlay.
- Displaying which equipment is equipped.
- Allowing the equipping of equipment via action bar hotkeys.

**Performance**

- Self-processing thread pool/queue. I really like this thing.
- Tiered entity streaming. (Near/Far)
- Region Tiles

**World Generation**

- Noise-based region modules with cutoff bands.
- Revamped spawn pools, now offer three varieties of spawning logic.
- Subregion generation - absolute, noise, or random.

![](../../assets/fafe8ba0b406564c.png)


Code statistics! *(+/- since last release)*

**Commits in release:**1,435 (*+282*)**Total Git Lines Added:**1,894,400 (*+255,989*)**Total Git Lines Removed:**919,111 (*-128,232*)**C# Files in Release:**702 (*+128*)**Live Lines of C#:**75,680 (*+16,499*)**Largest Files:**`MathUtils.cs`

(*1,084 lines*)`TerrainGrid.cs`

(*1,069 lines*)`WorldGraphSegment.cs`

(*1,051 lines*)

**Smallest Files:**`IAbilityBook.cs`

(*6 lines*)`SystemMenuControlsButtonController`

(*6 lines*)`SystemMenuLoadButtonController`

(*6 lines*)


**Shaders in Release:**71 (*+23*)**Live Lines of Shaders:**11,926 (*+2,991*)**Largest Shaders:**`TerrainImpl.hlsl`

(*917 lines*)`ToonStencilDeferred.shader`

(*675 lines*)`TerrainGrassImpl.hlsl`

(*622 lines*)

**Smallest Shaders:**`DeclareThicknessTexture.hlsl`

(*21 lines*)`DeclareTransparentTexture.hlsl`

(*25 lines*)`OutlineCommon.hlsl`

(*27 lines*)



At this time I am titling v0.5 as *Atmosphere*, and the main focus will be on the following features that will help fill out by the literal and figurative atmosphere.

The current sky features a sun, moon, stars, and day/night transition.

But it is now time to add clouds and a weather system. Additionally I want to add a custom atmospheric fog post-process and stop using the built-in Unity one. Note that this is not *volumetric fog*, which may come in a later version.

There is no sound in BTS currently.

I actually have 0 experience with sound, and have been putting it off and instead working on things I do know how to do. I have kept sound in the back of my head and accounting for it when needed, but now it is time to actually implement it.

- Active Sound: footsteps, collisions, etc.
- Passive Sound: ocean waves, wind, etc.

This will not include music, but simply “world” sound.

Both of these were added in v0.3, but I think it is time to revisit them.

This will include expanding on NPC interactions and also adding in a friendly ocean dweller.

And thanks as always to [Alex B](https://alexthebear.artstation.com/) for providing art, ideas, and feedback during the work on v0.4.