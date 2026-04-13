---
title: Simonschreibt.
url: https://simonschreibt.de/gat/gta-v-wormy-fountain/
author: Simon
published: '2020-03-21'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

This article was updated. Jump to [Update 1](https://simonschreibt.de#update1). [Update 2](https://simonschreibt.de#update2). [Update 3](https://simonschreibt.de#update3). [Update 4](https://simonschreibt.de#update4). [Update 5](https://simonschreibt.de#update5).

![](https://data.simonschreibt.de/gat070/thumbnail_youtube_01_forward.png)


![](../../assets/1468142abc4eae51.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

[Grand Theft Auto V](https://www.rockstargames.com/V) has some nice fountains which I would like to present you – but sometimes it’s a bit hard to admire them in the game :,(

It can be equally hard to put nice water effects into a game. One reason for this is, that water has an **always-changing surface-topology**.

While the polycount for e.g. a cloth-simulation stays **consistent** (and the vertices “just” need to be moved around) **every frame** of a water-simulation has a different amount of polygons/vertices:

It’s possible to use **newer** techniques like [Vertex Animation Textures](https://www.sidefx.com/tutorials/game-tools-vertex-animation-textures/) or [“Geometry Flipbooks” á la Alembic](https://www.youtube.com/watch?v=YTDEdZovHbw) but what I saw in GTA was **simpler** – that’s why I would like to show it to you.

Here is the first one. As it looks a bit like a worm, let’s call it:

# Wormy Fountain

In case you think: *“Well … that’s water, so what?”* I would like to underline, that having a nice **volume** and/or **silhouette** for the water is not that easy – and in the example above we have a both! <3 :)

To illustrate the problem: For water-effects often a water-texture is moved along a **flat** surface which **sometimes** works very well. Here, is a great example which we shall name:

# Wedding Cake Fountain

**But **if try to mimic the **“Wormy Fountain”** by running a texture along a **static** geometry (like it was done for the “Wedding Cake Fountain”), the trick gets very obvious when looking at it from the **side**:

Of course, you could use a geometry with some **volume** instead of a flat plane. Luckily, GTA offers an example for that as well. I’m introducing to you – last but not least:

# Tongue Fountain

Here we have a geometry which some volume which works perfectly fine from any angle but there is a “but”.

Here comes the “but”.**But** the **silhouette** is very **static** and not as dynamic as we saw it on the “Wormy Fountain”. Let’s look at the effect again:

Looks very good from all angles **and** has a nice dynamic silhouette, doesn’t it?

# The Secret

The secret behind this water-stream is called: **Spline with camera-facing quads**.

The polygon-ribbon is re-orienting itself **toward the camera** and with that you’ll never see, that it’s actually a **flat** polygon-stripe. Only when you look at it from very **extreme angles**, you might see some artifacts:

You may have seen similar techniques in other areas for example on the [Home World Trails](https://simonschreibt.de/gat/homeworld-2-engines/) or from the [Company of Heroes flame thrower](https://simonschreibt.de/gat/company-of-heroes-flamethrower/) (see image below), but I thought making a fountain with that is very creative so I had to share it with you guys. :)

# By the way #1

Here is the texture which was used in GTA:

# By the way #2

I have no idea what these smaller geometries are for … they are not visible in the game:

# By the way #3

This effect inspired me (together with other influences like this great talk about [loopable liquids in Mortal Kombat](https://youtu.be/k8_6PmSKF2U?t=836) – **careful**, the talk also features many **blood** effects!) an idea in my mind: If a simple moving texture on a polygon-trail/spline already looks so nice, could this work even better with a **tileable mesh moving along a spline**?

To test this, I made a small side-project:

It uses two **tileable** meshes (generated in Houdini) and 5 instances of each run along a spline. If you want to see the **full breakdown**, I put everything together on my [Artstation post](https://www.artstation.com/artwork/BmN5G6). **Thanks for reading my article. <3 ****I hope you’ll like it! **

And never forget:

![](../../assets/ba0680151067ebbc.png)

[Smou](https://twitter.com/Smou_) and [DrWDSo](https://twitter.com/DrWDSo) told me that there is actually a name for the “water without turbulence” I was so amazed by (you can see it in the [youtube video I recorded](https://youtu.be/axqzP69GSsE)): “Laminar Flow”. And both linked me to this amazing video you should watch. Right. Now! :)

![](../../assets/ba0680151067ebbc.png)

[Wyvery](https://twitter.com/niels_dewitte) and [Luos](https://twitter.com/Luos_83) just mentioned that it’s **not** really a trail but more a spline with **camera-facing quads**. Thank you for the hint! :)

In Unreal there is a [“Spline Thicken”-Node](https://docs.unrealengine.com/en-US/Engine/Rendering/Materials/Functions/Reference/WorldPositionOffset/index.html#splinethicken) to use this technique e.g. for cables but Luos also told me that he likes to use it for his [soul coasters](https://realtimevfx.com/t/vfx-basics-mesh-soulercoasters/1987).

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

[Bananaft](https://twitter.com/Bananaft) sent us a small video showing a guy who suddenly loses a big red sausage. This sausage is actually a trail-geometry between particles and those particles can collide with the level geometry. Another very creative use for those kind of geometries. :)

![](../../assets/ba0680151067ebbc.png)

[Taras Tereshchenko](https://www.linkedin.com/posts/teres4enko_the-use-of-expensive-and-complex-solutions-activity-7306292571142565889-bXb7) shares a very cool **opaque** fountain. The meshes are animated by World Position Offset (not Vertex Animation Textures) and the translucency is the result of using (custom?) dithering.

“I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.”

You forgot the last video, “Update 1”.

Fixed. Thanks for the hint!

Post-FX quality of GTA V at productscrack also has a big impact on performance. This includes things like bloom, HDR lighting, thermal shimmer, and other special effects. Grass and shade can put a heavy strain on your system. Given the size of the in-game world, loading times can get quite long. If you have a large enough SSD, pushing it open might be a good idea. For some reason, MSAA has a massive negative impact on performance. It can therefore make sense to switch to FXAA or to switch off anti-aliasing completely.

That green goo stream in By The Way #3 is really cool. Nice work :)