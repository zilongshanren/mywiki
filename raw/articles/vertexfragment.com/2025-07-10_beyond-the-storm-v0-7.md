---
title: Beyond the Storm - v0.7
url: https://www.vertexfragment.com/ramblings/bts-v07/
author: Steven Sell
published: '2025-07-10'
source_blog: Vertex Fragment
source_site: https://www.vertexfragment.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/8c2d45e984b54741.png)

![](../../assets/eb07958dd0e15eca.png)

After a year long break from working on *Beyond the Storm*, during which I created [Ponder](https://pondertcg.com/), I am back to give a rather unique update as it moves to v0.7.0. Unique in that this is the first version of BTS that [is publicly available](https://github.com/ssell/BTS-Public) and also likely the last update for the game in its current state.

Long story short: BTS, as-is, is likely too ambitious for me to complete on my own in any sort of timely manner. This is a side effect from me always wanting things to be *big*. The games I played had to be large and open, and even the books I read had to be door stoppers. However life changes, and as I found my freetime dwindling I have discovered a renewed appreciation for smaller experiences.

As such, moving forward there will be a refocusing of BTS and a great trimming down of features and scope. What was to be an extremely large and varied open world, will instead be reconstructed into a short (2-3 hour) experience. This means that some features that I spent a good deal of time on, such as building and terraforming, may eventually be cut to fit the new slimmed down vision. But perhaps some day I may have the resources needed to revisit the original loftier vision of BTS. For now, however, I believe it is better to get something finished as opposed to toiling on an endless project.

With all that said, below are the highlights of v0.7.0. Likely the smallest of the numbered versions, but that is to be expected given the circumstances.

![](../../assets/69ca9f059072dce2.png)


Prior to this version, all grass was rendered as quads more-or-less as described in the [Unity Deferred Grass Rendering](https://www.vertexfragment.com/ramblings/unity-deferred-grass-rendering/) ramble. While this approach has some pros, primarily the ease of which to change the appearance of the grass via using different textures, it comes with some cons.

In v0.7 the grass was switched to a bladed version, where each individual grass blade is drawn. This fixed some artifacts present in the quad-based grass present at high view angles, low density, or near boundaries of regions that don’t have grass. The biggest visual improvements resulting from the transition are wind effects and the ability to add custom meshes to the blade tips to create flowers.

This is seen in-game where the grasslands region has purple flowers and the forest regions have no flowers.

Additionally, updates were made to both the grass and terrain layer systems to allow better blending of grass heights and terrain textures based on slopes and regional settings. In forest regions the grass is no longer as tall and there are areas of dirt to add more visual variety. Previously the same uniform carpet of grass that ran through the grasslands region also filled the forest.

![](../../assets/f22f8c367fa5b94a.png)


While not present in the released demo, the volumetric fog was also completely rewritten in v0.7. It is absent due to not getting around to working it into the world generation and/or weather systems in time.

However, the implementation follows what is shown in the [Rendering Volumetric Fog Using Custom URP Render Pass](https://www.vertexfragment.com/ramblings/urp-volumetric-fog/) ramble.

A basic water trail effect was added to entities as they walk and swim through water.

Like I found with the boat wake trails, working with displaced water surfaces is a lot more challenging than a flat surface. However the effort was worth it, as it is another small effect that helps to bring the world together.

![](../../assets/befc1ea124970d68.png)


Ever since clouds were first implemented in [v0.5](https://www.vertexfragment.com/ramblings/bts-v05/) I had not been completely satisfied with their performance. Yes, they could render at runtime however there a was noticable FPS dip as the clouds were being re-rendered.

This is because the approach I took to optimizing cloud rendering at the time was to render them once every 0.25 seconds and simply interpolate between them. I was never happy with that solution but it was *good enough* and I moved on to other more pressing needs. However, following the release of [v0.6](https://www.vertexfragment.com/ramblings/bts-v06/) I had enough of the performance spikes.

A good deal of time was spent figuring out a final solution, but eventually I was successful in rendering them in real-time. Those efforts are captured in the [Upsampling to Improve Volumetric Cloud Render Performance](https://www.vertexfragment.com/ramblings/volumetric-cloud-upsampling/) ramble.

Code statistics! *(+/- since last release)*

**Commits in release:**2,096 (*+175*)**Total Git Lines Added:**2,424,200 (*+107,179*)**Total Git Lines Removed:**1,561,424 (*-49,348*)**C# Files in Release:**975 (*+32*)**Live Lines of C#:**112,094 (*+3,429*)**Largest Files:**`MathUtils.cs`

(*1,615 lines*)`TextureUtils.cs`

(1,079 lines)`TerrainGrid.cs`

(*1,069 lines*)

**Smallest Files:**`IAbilityBook.cs`

(*6 lines*)`SystemMenuControlsButtonController`

(*6 lines*)`SystemMenuLoadButtonController`

(*6 lines*)


**Shaders in Release:**110 (*+13*)**Live Lines of Shaders:**18,352 (*+2,915*)**Largest Shaders:**`Common.hlsl`

(*1,069 lines*)`TerrainImpl.hlsl`

(*943 lines*)`TerrainBladedGrassImpl.hlsl`

(*690 lines*)

**Smallest Shaders:**`DeclareThicknessTexture.hlsl`

(*21 lines*)`DeclareLightSourcesTexture.hlsl`

(*22 lines*)`DeclareTransparentTexture.hlsl`

(*25 lines*)