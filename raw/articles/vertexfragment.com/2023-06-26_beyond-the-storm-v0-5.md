---
title: Beyond the Storm - v0.5
url: https://www.vertexfragment.com/ramblings/bts-v05/
author: Steven Sell
published: '2023-06-26'
source_blog: Vertex Fragment
source_site: https://www.vertexfragment.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/cb4078f07843961d.png)


The very first commit to the *Beyond the Storm* project was on 2021-06-27. Two years and 1,643 commits later, we now have v0.5 of the project. It is my third longest running project after [ Realms](https://www.vertexfragment.com/projects/#realms-2018---2021) (which lasted 2.5 years) and

[(which was on-and-off for 4 years), and it is still going strong.](https://www.vertexfragment.com/projects/#ocular-engine-2014---2018)

*Ocular Engine*As declared in [the v0.4 update](https://www.vertexfragment.com/ramblings/bts-v04/), this release was titled *Atmosphere*. This encompassed both the literal and figurative atmosphere of the game and brought along both challenges and triumphs.

![](../../assets/5c555b6fe86c5f2f.png)


Coming into this version I knew that clouds would be my biggest challenge. And I was right.

For several years part of my job was providing support to a Clouds/Weather SDK as well as implementing it in a proprietary engine. Additionally I took stabs at doing volumetric clouds in a few different ShaderToys. Those experiences left me with a feeling of general dislike towards clouds.

But coming out of the other side of it (and several rewrites), I am very pleased with how they turned out in *Beyond the Storm*. They look decent, stylistically match, and are *somewhat* performant. The high quality clouds do cause my computer to dip below 60 FPS, but that is what graphics options are for! Plus I realized the other day that my computer is 9 years old now.

Some features include:

- Real-time volumetric clouds (buzzwords!)
- Dynamic day/night light transitions
- Shadows and reflections
- Occupy world space

That last point may need some explanation.

As the name may suggest, storms are an integral part to *Beyond the Storm*. Because of this it is important that storms follow a predictable and controllable pattern and that the weather system occupies the entire map.

In most games (*Elder Scrolls*, *Zelda*, etc.) weather tends to affect the local area around the player. Weather between zones and regions may be completely disconnected. In a relatively few games (*Sea of Thieves*) the storms occupy the entire world space and you can see and navigate around advancing storms, etc. *Beyond the Storm* is one of these latter games.

Being able to see an approaching storm while sailing on the seas was an important part in my envisioning of the game. And it was one of the more challenging parts to get right as we tend to forget that clouds are *huge*. And the systems they are in are even larger. A lot of time was spent tweaking and finessing the cloud generation to get this right, as real-world values do not map to game values as even the largest of games tend to be small compared to real-life geography.

But without going into too much detail, which may end up being a future spoiler, everything eventually lined up just right.

![](../../assets/9ac174f854a38739.png)

![](../../assets/d1711420d2aca0c8.png)

Unity has built-in fog. Built-in fog does not affect skyboxes.

It is hard to have a convincing storm without blending the world and skybox together with fog. And thus I added in volumetric fog. In addition to being able to blend together the world and the sky, creating my own volumetric fog provides the following advantages:

- More control over the fog gradients, with separate gradients for world and skybox.
- Adjusting gradient colors and settings based on:
- Time-of-day
- Proximity to sun and moon
- Weather conditions

- Illuminating the fog around configured point light sources.

The fog system also allows for multiple fog volumes to support things such as heavy ground fog and mist.

![](../../assets/6d42a34390224c37.png)

![](../../assets/2164145ea15f2602.png)

There were many approaches to weather that I had in mind before starting on it, and what I finally settled on was a *storm intensity* value. This intensity is the primary driver of selecting the appropriate weather profile (clear, cloudy, stormy, etc.) that should be active around the player.

The *storm intensity* is calculated via an algorithm implemented both on the CPU and GPU to allow the logic to sync up with various visuals. It is also calculated in such a way that, as mentioned previously, storms occur at a regular and predictable cadence which will play an important part in the game.

But like clouds, the weather occupies the world-space. It may be storming at point A but at the same time it is clear at point B, and then at point C you can see the storm approaching. So to simulate local weather effects, a local weather grid is employed. This simply samples the storm intensity in a large area around the player, selects the appropriate weather profile (which may also be affected by region), and then creates an average local weather profile.

A weather profile defines a long list of atmospheric conditions:

- Ambient light gradient
- Sun light and surface color and intensity curves
- Moon light and surface color and intensity curves
- Sky color gradients
- Wind speed and strength
- Wind trail effects
- Cloud color gradients
- Fog intensity and falloffs
- Fog color gradients
- Fog noise intensity
- Precipitation styles, intensity, and angles
- Thunder frequency and intensity
- Water color gradients
- Water wave height

*Whew.*

![](../../assets/a79e781730fb8591.png)


Entering into v0.5 there was absolutely no sound, and it was something I kept intentionally putting off.

In fact, aside from a brief foray into [FMOD](https://www.fmod.com/) at a previous job some *~checks repository dates~* 11 years ago (!), I have never done anything with audio. So unlike most things that I work on these days, I had no previous foundational knowledge to work off of. So I began by trying to categorize audio in games and I came up with this: Ambient and Triggered audio.

These are sounds that just happen, without any direct interaction from the player. They can be looped or single-shot clips and fall into two subcategories:

- Weather-based
- Region-based

Weather-based audio is fairly obvious: wind, rain, thunder, etc. These are what Unity (everyone?) calls 2D audio in that they do not fall off based on distance from the audio source. Intensity of these is controlled by the local weather profile. And eventually weather-based sounds should be diminished or muffled if the player is inside a structure, but that is a future problem for future me.

The most obvious example of region-based audio is perhaps waves. Unlike weather, region audio is 3D and needs to fall off based on distance from the region that is playing the sound. This was a little tricky (and fun) as regions within the game are just logical constructs post-world generation. So a way was devised to query local region influences as well as vectors to those regions. This enables playing audio in one ear while walking along a beach, and then diminishing the sound of the waves as you move inland (or upwards).

These are sounds that occur because something did something. At this point there are the following subcategories:

- Character audio, controlled by a
`CharacterAudioMap`

on the entity. Includes: footsteps, unarmed combat, etc. - Weapon audio, controlled by a
`WeaponAudioMap`

on the item. Includes: swings, strikes, blocks, etc. - Interface audio, which includes: button hover, press, item pickup, item equip, etc.
- General audio, which is triggered by specific logic.

Let’s follow through with an example, labelling each audio triggered by their list number:

The player turns off the light (4), walks to the door (1), opens the door (4), closes the door (4). They then walk to nearest tree (1), swings at it (2), hits it (2), swings at it again (2), hits again (2), the tree falls (4), the tree hits the ground (4), player picks up wood (3).


Going through the process of adding in audio really makes you realize all of the wonderful sounds you have been taking for granted in movies and games.

![](../../assets/6c9267ec059429ee.png)


Visual effects are something I don’t have a lot of experience with as my career and hobbies have generally either been focused at a lower level (buffers and meshes and culling and …) or on larger visual systems (terrain and water and clouds and …). However it is something I really look forward to doing more of, and I wanted to make sure I got to work on a few effects this version.

While working on a [Ludum Dare](https://ludumdare.com/) jam, a friend mentioned three key components to sell a scene: light, audio, and movement. And its something thats been in the back of my head ever since.

Two effects were added to help sell the movement and presence of the wind (aside from the new clouds): wind trails and grass motes. The trails are curvy streaks in the sky, that generally follow the direction of the wind. The motes appear in grass or forest regions and are similar to those seen in games such as *Breath of the Wild*.

Unfortunately since they are made to show *movement* they don’t look as good in *still* screenshots.

Resource gathering will be a decent part of the game, and wood will be a common resource. As such lots of trees will be cut down (I know, I know, its revolutionary gameplay). And since it will happen a lot, it should look and feel good.

In addition to audio triggers, the following improvements were made to tree cutting:

- Trees show where they were cut.
- Felled trees break apart further when they hit the ground.
- Feedback (screen shake) when a tree hits the ground nearby.
[Improved puff particles when a tree crashes or is destroyed.](https://www.vertexfragment.com/ramblings/stylized-puff-particles/)

Those were the big topics that I felt like talking about, but not nearly everything that was done in this version. Below is a list of other changes (some minor, some major) that were done in v0.5.

**Content**

- Updated Pine Tree model.
- Updated Bare Pine Tree model.
- Added 38 audio resources composed of 63 audio clips.
- General reorginzation of entities.

**Effects and Visuals**

- Improved reflection probes.
- Transparent depth capture pass.
- Lots of tweaks to night lighting.
- Increased grass and tree wind bending.
- Increased grass growback duration after terraforming.

**General Engine**

- Resource error handling.
- Fixed weapon blade rigidbody.
- Generalized surface info queries.

**GUI**

- Numerous GUI bug fixes.
- Corrected paper doll alignment.

**Math**

- Worley Noise.
- Worley-Simplex Noise.
- Tileable noise implementations.

![](../../assets/501b3e0633cf682b.png)


Code statistics! *(+/- since last release)*

**Commits in release:**1,644 (*+209*)**Total Git Lines Added:**2,116,774 (*+222,374*)**Total Git Lines Removed:**1,040,796 (*-121,685*)**C# Files in Release:**702 (*+128*)**Live Lines of C#:**88,426 (*+12,746*)**Largest Files:**`MathUtils.cs`

(*1,342 lines*)`TerrainGrid.cs`

(*1,069 lines*)`WorldGraphSegment.cs`

(*1,051 lines*)

**Smallest Files:**`IAbilityBook.cs`

(*6 lines*)`SystemMenuControlsButtonController`

(*6 lines*)`SystemMenuLoadButtonController`

(*6 lines*)


**Shaders in Release:**90 (*+19*)**Live Lines of Shaders:**14,633 (*+2,707*)**Largest Shaders:**`TerrainImpl.hlsl`

(*916 lines*)`Common.hlsl`

(*895 lines*)`ToonStencilDeferred.shader`

(*675 lines*)

**Smallest Shaders:**`DeclareThicknessTexture.hlsl`

(*21 lines*)`DeclareLightSourcesTexture.hlsl`

(*22 lines*)`DeclareTransparentTexture.hlsl`

(*25 lines*)



Seeing as I gave v0.5 a name it is only appropriate that v0.6 receives on as well, *Life and Death*.

*Beyond the Storm* is a game with a world, but without much life. After two years there is still no concept of health, combat, etc. The next version will be focused on bringing in those mechanics.

Basic animation was added during v0.1 and incrementally updated as needed. However many actions feel constrained by the current animation setup and a second pass is sorely needed to achieve natural and more fluid feeling interactions.

There is a reason that combat has not yet been added in - it is not envisioned to be a primary focus of the game. This does not mean it is not important, but *Beyond the Storm* will be more focused on exploration and is not a Soulslike game.

With that said, combat must still feel smooth and well implemented with a lot of time spent on tweaking and tuning it.

This was originally a goal for v0.5 but ran out of time and scope to address it.

This will be needed doubly so with the addition of combat.

The first pass of buoyancy was added in v0.2 (along with water) a year ago and has not been touched since then.

It’s current state is *acceptable* but being only acceptable is not acceptable. Especially since a good portion of the game will be sailing between islands.