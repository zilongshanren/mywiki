---
title: 3D artist explains how water is animated in games such as Uncharted 4, Subnautica
url: https://www.eurogamer.net/3d-artist-explains-how-water-is-animated-in-games-such-as-uncharted-4-subnautica
author: Victoria Phillips Kennedy
published: '2023-05-15'
source_blog: Eurogamer.net
source_site: https://www.eurogamer.net/
category: graphics
fetched: '2026-04-19'
---

Water features a lot in video games - [Bertie even ran a Five of the Best supporter's piece](https://www.eurogamer.net/five-of-the-best-water) on it earlier this year. But how do developers actually make it look so, well, water-like?

According to 3D artist Thomas of Twitter account Stylized Station, there is a lot involved to get it just right. It takes "a ton of smoke and mirrors in the background, without anyone ever realising it," they explained in a very thorough Twitter thread, noting "creating real-time simulated water is still really hard to do".

Thomas stated that most developers use a variety of "cheats" and techniques that see things such as textures, VFX sprites, normal maps, and basic geometry "smashed together" in order to give the "illusion of flowing water".

[Watch on YouTube](https://www.youtube.com/watch?v=pd_MbDzn0bI)

Thomas shared examples from [Uncharted 4: A Thief's End](https://www.eurogamer.net/games/uncharted-4-thiefs-end) (pictured above), and [Far Cry 5](https://www.eurogamer.net/games/far-cry-5). According to their thread, both of these games trick the eye by layering moving textures over simple geometry.

"These normal maps do a great job of faking the micro details of waves and ripples you see on a large body of water without having to simulate anything; it's just moving two simple textures over a plane. Our monkey brains fill in the rest of the details for us," they explained.

Thomas goes on to discuss water's caustics in games, or in their words "those shimmering patterns of light you see on the bottom of a pool" and "the strange light images created when light shines through a glass of water".

According to Thomas, to create this effect in a game "all you have to do is pan an emissive texture on the bottom of your water floor" and then "add a simple distortion and dissolve effect" to simulate the caustics. Here, the artist used both Bioshock and [Subnautica](https://www.eurogamer.net/games/subnautica) as examples, stating that while it may seem like a small detail, we would miss it if it wasn't there.

When it comes to games with more "dynamic" areas of water, meanwhile, Thomas explained developers will often use a method called "Vertex displacement".

This "allows controlling the positions of a mesh's vertices via a shader", and "can be applied to the actual geometry of the water". This means that instead of having a flat plane, "you can have moving, flowing geometry".

Thomas also shed more light (and praise) on [Sea of Thieves](https://www.eurogamer.net/games/sea-of-thieves), which they say the developer took "to the next level" when it came to water design.

"Rare recognised early on in the development of Sea of Thieves that most players will be staring at the sky and the water most of the time in-game, so they paid extra attention to these areas, by creating a water system that was dynamic, and had character and personality," they wrote.

"On the open water, you have these massive crashing waves that can be seen for miles. These waves are procedurally created and are synched to every player out on the ocean."

You can read Thomas' full and incredibly interesting thread all about water in video games by [following this link here](https://twitter.com/StylizedStation/status/1657401347539361794).