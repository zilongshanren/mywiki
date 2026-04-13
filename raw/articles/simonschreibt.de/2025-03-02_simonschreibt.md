---
title: Simonschreibt.
url: https://simonschreibt.de/gat/infinity-nikki-shadow/
author: Simon
published: '2025-03-02'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

Hey sunshine! 🌞

I f*ckd up. This is how I originally planned this article: It should be **short**, contain 1-2 videos and express the following:

“Look! In

[Infinity Nikki]the character has a “real” shadow, but the developers fade it out while jumping to make space for a blob shadow (which helps to navigate while jumping/gliding).”

[Infinity Nikki](https://store.epicgames.com/en-US/p/infinity-nikki-71fc64?lang=en-US)

But the more I looked into the subject, the more observations I made, the more people got involved (to give me advice), and the article grew longer and longer. I’m sorry.

Unfortunately, none of the usual profilers attaches to the game (I tried [Renderdoc](https://renderdoc.org/), [Nsight](https://developer.nvidia.com/nsight-systems) & [GPA](https://www.intel.com/content/www/us/en/developer/tools/graphics-performance-analyzers/overview.html)). So **I can only assume**, and there’s **no proof** of anything!

💘💘💘 Huge thanks to [Nemi](https://nemi.artstation.com/), [Ben Golus](https://bsky.app/profile/did:plc:oonxdlrixnlefvtahyk7io6q) & [Froyok](https://bsky.app/profile/froyok.fr) for helping with this article. 💘💘💘

# Table of Content

[Shadow Map](https://simonschreibt.de#shadowmap) | [Blob Shadow](https://simonschreibt.de#blob) | [Blob vs Decal](https://simonschreibt.de#blob-vs-decal) | [Ambient Occlusion](https://simonschreibt.de#ao) | [Bonus Observations](https://simonschreibt.de#bonus) | [Summary](https://simonschreibt.de#summary) | [Bonus Links](https://simonschreibt.de#bonus-links)

# Overview

I have the impression, that there are 3 different types of shadows at play:

**Ambient Occlusion Blob**: Subtle. Grounds characters in the world.**Blob Shadow + Blue Ring**: Appears while jumping/gliding. Serves as landing guide.**Realistic Shadow**: Made with[shadow mapping](https://en.wikipedia.org/wiki/Shadow_mapping). Fades out while jumping/gliding.

# Shadow Map: Selective Fading

As you saw in the first video, while jumping, a blob shadow is fading **in**, while the “realistic” shadow fades **out**. This avoids having two shadows (realistic shadow map & blob shadow) at the same time. BUT, for some reason, it’s **still visible** on other characters!

[Infinity Nikki](https://store.epicgames.com/en-US/p/infinity-nikki-71fc64?lang=en-US)

### Why is the shadow still visible on NPCs?

There might be a **separate** shadow pass just for **self-shadowing** of characters. This pass seems to contain Nikki’s shadow (next to all characters) and is not modified at all. A custom technology for the self-shadowing was mentioned in their [behind the scenes article](https://www.unrealengine.com/en-US/developer-interviews/behind-the-scenes-of-infinity-nikki-tracing-a-glamorous-turn-to-an-unreal-open-world):

“For character lighting, we developed high-quality shadows specifically for characters to achieve detailed self-shadowing.”


### How can they make Nikki’s shadow fade independently of all other shadows?

Nikki’s shadow seems to render in a **separate** shadow pass, which allows rendering it with different translucency.

In summary, if the theory is correct, we have **three** shadow passes: One for all objects and NPCs, one for Nikki (can fade in/out) and one for character self-shadowing including Nikki and all NPCs.

A crude version of this (using dithering for the fading) is possible in Unreal by using the [Shadow Pass Switch](https://unrealdirective.com/tips/shadow-pass-switch)-Node. Here is an example where I fade a selected cube:

In both cases, dithering is at work. With classic **low resolution** shadow maps, it isn’t as obvious (because everything looks a bit blurrier), but with the virtual shadow maps (which allow for sharper shadows), we can see the dithering noise very clearly.

Just for your information, this is the material of the center cube:

![](../../assets/4098b1c46dafe88f.png)


![](../../assets/4098b1c46dafe88f.png)

A capture of the frame shows how it works. For calculating a shadow map, we need a depth buffer that contains the scene from the camera’s point of view and another one from the light source’s point of view (they get compared [with code magic](https://youtu.be/kCCsko29pv0) to give us the shadow information). The first one looks like expected (it contains the floor and our three boxes). The latter, on the other hand, contains our center box as a **dithered version** and thus generates the dithered shadow:

FYI: Found this article [The Case of the Disappearing Shadow: Gradual Shadow Fading](https://stephenverderame.github.io/blog/oort-shadows/) about selective fading by using a separate depth buffer.

## History Lesson

Older games didn’t have this “double shadow” problem because shadow mapping was too expensive back then. So, in Super Mario 64 there is **just** a blob shadow. I really like that it gets smaller when Mario is further away from the ground – nice detail! 👍

[Let’s Play Super Mario 64](https://youtu.be/MNSZUvhnWM4)

Jump & Run games usually rely on having such a blob shadow to show the players where they land. As soon as “real” shadows (shadow mapping) are added, developers have to decide how to deal with the “double shadow” issue.

As already mentioned, in Infinity Nikki, the “real” shadow is replaced by a blob shadow while jumping. But here are two more solutions:

### 💡 Alternative Solution 1: Top-Down Shadow

In Super Mario Odyssey, Mario’s shadow is **different** from that of the NPCs. While theirs is projected from the **sun direction**, Mario’s is always projected from the **top**, and no extra blob shadow is needed (according to [this post](https://forums.tigsource.com/index.php?topic=67055.0), Mario uses a stencil shadow):

### 💡 Alternative Solution 2: Just show both

Yooka-Laylee (and [this Raytracing version](https://www.youtube.com/watch?v=ChqP2ecA8qE) from Super Mario 64) simply allows **both** shadows to exist at the same time:

[Yooka-Laylee](https://store.steampowered.com/app/360830/YookaLaylee/)

By the way, Yooka-Laylee has a nice trick on defining **when** the blob shadow should become visible! Instead of a distance-based calculation between character and floor, they put a decal projection several centimeters **below** the feet. It’s **always** there, like this edge case reveals:

[Yooka-Laylee](https://store.steampowered.com/app/360830/YookaLaylee/)

As soon as the player jumps, the decal projection will be raised above the ground and suddenly draw a pleasant blob on the floor.

Speaking of…

# Blob Shadow

Classic blob shadows are simple quads with a radial gradient texture. They are placed close to the floor and **align to it**.

Unfortunately, when the ground is **uneven**, the illusion breaks quickly. Here we see how the quad penetrates the surface before getting re-aligned:

[Let’s Play Super Mario 64](https://youtu.be/MNSZUvhnWM4)

Keep this artifact in mind! We’ll see it later in Infinity Nikki as well when we talk about blob shadows on water!

A more modern approach would be to **project** a texture onto the floor (as Yooka-Laylee does it) instead of using a floating plane. This is usually called “decal”:

You may think, that such a projected decal is way cooler than a stinky old plane. But there is a case where projections usually don’t work: **Water**! 💧

# Blob Shadow vs Decal

A plane can easily be placed **above** water. Here you can observe that the blob shadow switches from being below or above water, depending on Mario’s vertical position:

[Let’s Play Super Mario 64](https://youtu.be/MNSZUvhnWM4)

[Yooka-Laylee](https://store.steampowered.com/app/360830/YookaLaylee/) on the other hand, uses a projected decal for the drop shadow. Problem: It’s **not** working on translucent surfaces!

Look how the drop shadow is only rendered **below** the water surface and becomes almost invisible:

[Yooka-Laylee](https://store.steampowered.com/app/360830/YookaLaylee/)

That’s a common issue, since the decal projection relies on the depth buffer and water doesn’t get written into it.

While a plane may be a better option in this case, it comes with another disadvantage (apart from intersecting with uneven terrain): It is a bit “jumpy” when moving along an environment with height differences.

Mario’s shadow plane **suddenly changes** its height position. It’s only visible **either** on the floor **or** the ceiling:

[Let’s Play Super Mario 64](https://youtu.be/MNSZUvhnWM4)

A projection has the advantage, that it can be seen at different heights at the same time. Here, for example, it’s visible on the floor **and** the platform:

[Super Mario 3D World](https://youtu.be/FG2GPN7LJIk)

But even here, the lower shadow suddenly disappears! I assume that when Peaches pivot point is above the platform, the projection distance is updated and now too short to reach the floor. This might be a workaround to avoid seeing the shadow on the platform **and** the floor at all times.

This behavior can be observed in Yooka-Laylee. Here the blob shadow is projected on the planks and the floor below:

[Yooka-Laylee](https://store.steampowered.com/app/360830/YookaLaylee/)

Another potential small visual issue with projections: they may result in very long shadows on verticals surfaces:

[Super Mario 3D World](https://youtu.be/FG2GPN7LJIk)

We’ll talk later about a method to prevent this from happening.

Let’s go back to Nikki. How did they make the blob shadow? Is it a plane **or** a decal?

I assume: It’s **two** planes **and** one decal! *mic drop*

While gliding, it’s easy to observe that there is a plane that aligns to the underlaying surface. At least the blue ring is a plane:

[Infinity Nikki](https://store.epicgames.com/en-US/p/infinity-nikki-71fc64?lang=en-US)

What about the blob shadow? Well…remember the Mario 64 example, where the plane would be only visible at **one** height position at a time?

Here, on the other hand, we can see that the shadow is visible at the floor **and** the tent for some time (like in the example with Peaches platform):

[Infinity Nikki](https://store.epicgames.com/en-US/p/infinity-nikki-71fc64?lang=en-US)

And here it’s even more obvious, that our drop shadow is projected at different heights at the same time. So we can assume: The blob shadow is a decal projection!

[Infinity Nikki](https://store.epicgames.com/en-US/p/infinity-nikki-71fc64?lang=en-US)

It is an interesting detail, that the projection on the floor fades out with a small delay in comparison to the others … no idea what’s going on there.

*“But Simon, why then we don’t see this strong vertical shadow like in the example with Peach?”*

I think they just mask the projection based on the normal orientation of the environment. Here is a demo ([and I made a tutorial](https://youtu.be/6pGLl7uuMXc)):

*“But Simon, you said decals can’t be projected on the water surface! Why do we see it in Nikki?!”*

[Infinity Nikki](https://store.epicgames.com/en-US/p/infinity-nikki-71fc64?lang=en-US)

This is where the **second** plane comes into play! I think they always place a blob shadow plane slightly above the water surface **in addition** to the decal projection for the blob shadow and the blue ring plane. Here you can see all three elements working together:

[Infinity Nikki](https://store.epicgames.com/en-US/p/infinity-nikki-71fc64?lang=en-US)

Although, I would expect to see the blob shadow projection on the floor **below** the water like in Yooka-Laylee… no idea why it’s not appearing. Maybe the projection distance is limited so that it never goes deeper than the water surface?

Here is a collection of examples where we can observe two more behaviors:

[Infinity Nikki](https://store.epicgames.com/en-US/p/infinity-nikki-71fc64?lang=en-US)

- The “water plane” always stays at the water height and does
**not**align to any surface below, which makes it sometimes intersect with the environment (like the Mario 64 example from above). - Sometimes, we can see the
**projected**blob shadow and the surface-aligned blue circle on top of the intersecting “water plane”:

Thought we’re done? No! Turns out, in caves, Nikki’s “real” shadow is **not** faded away (and maybe they are using [capsule shadows](https://dev.epicgames.com/documentation/en-us/unreal-engine/capsule-shadows-overview-in-unreal-engine) since they don’t need so much accuracy?):

[Infinity Nikki](https://store.epicgames.com/en-US/p/infinity-nikki-71fc64?lang=en-US)

Another detail: The “water plane”, which is usually seen above the water, suddenly disappears while jumping from one side to the other – but does **not** reappear, when jumping back. (o.O)

[Infinity Nikki](https://store.epicgames.com/en-US/p/infinity-nikki-71fc64?lang=en-US)

Quite a lot of food for thought, isn’t it? Did you expect such a long part about simple blob shadows? I certainly did not ! :)

Now that we thought a lot about the blob shadow, let’s have a short look at the subtle ambient occlusion.

# Ambient Occlusion: Decal or Plane?

I think that the AO in Infinity Nikki is another decal projection because when standing on an edge, you can see it reach 1 meter downward “into the ground”:

[Infinity Nikki](https://store.epicgames.com/en-US/p/infinity-nikki-71fc64?lang=en-US)

Here is another example. I hope you can see well how the AO decal is projected onto the ground and draws a nice subtle AO blob:

[Infinity Nikki](https://store.epicgames.com/en-US/p/infinity-nikki-71fc64?lang=en-US)

That’s basically all I wanted to share, but while recording all those videos, I made some more observations.

# Bonus Observations

## Shadow on Water

I’m always delighted to see when games render shadows on the water surface. It’s not well visible in this video, but yes, the stone also casts shadows on the water surface:

[Infinity Nikki](https://store.epicgames.com/en-US/p/infinity-nikki-71fc64?lang=en-US)

There are methods to replicate this in Unreal. For example, a **translucent** material with lighting mode **Surface Forward Shading** or the [Single Layer Water](https://dev.epicgames.com/documentation/en-us/unreal-engine/single-layer-water-shading-model-in-unreal-engine) shading model:

![](../../assets/6a989dd66361521e.jpg)


![](../../assets/6a989dd66361521e.jpg)

Also, when you create a **new** Unreal 5.5 project with a quality preset set to **maximum**, it should work with all other material lighting modes as well! For some reason, I didn’t get this working in my project, which I created in 4.x, but with a fresh 5.5 project it worked out of the box (because the directional light has **Cast Volumentric Shadow** enabled by default):

Important note from [the docs](https://dev.epicgames.com/documentation/en-us/unreal-engine/lit-translucency-in-unreal-engine#translucentsurfaces): *“r.TranslucencyLightingVolumeDim, which defaults to 64. Raising this by a factor of 2 increases the cost to light volume by a factor of 8.”*

## Item Shadows

Items can have unique shadows that do **not** belong to the shadow map. We can notice this because:

- Item shadows always are always cast from
**above**, while environment shadows are cast from the sun direction. - Item shadows darken
**already shadowed**areas even more.

[Infinity Nikki](https://store.epicgames.com/en-US/p/infinity-nikki-71fc64?lang=en-US)

The item shadows use decal projections **and** planes (to show up on water). Here is an example for a **projection**:

[Infinity Nikki](https://store.epicgames.com/en-US/p/infinity-nikki-71fc64?lang=en-US)

And here is an example where we can see how a plane is used as a shadow on the water (and how it intersects with the incoming barrel):

[Infinity Nikki](https://store.epicgames.com/en-US/p/infinity-nikki-71fc64?lang=en-US)

Interesting detail: When items are created “on the fly” they do **not** have shadows:

[Infinity Nikki](https://store.epicgames.com/en-US/p/infinity-nikki-71fc64?lang=en-US)

And this might be the proof that the item shadows are just rotating decals with **pre-made** textures, because here we can clearly see, that the mesh shape does not match the shadow (Bonus: We can see a soft fade in when Nikki comes closer to the decal).

[Infinity Nikki](https://store.epicgames.com/en-US/p/infinity-nikki-71fc64?lang=en-US)

In the video above, several decals seem to overlap each other, and that’s why they appear so dark. Here is another capture of how decals overlap sometimes:

## What is this?

Here, I do not have ANY idea what’s happening. For some reason, when you walk below such a launch pad, there appears a blob shadow **above** Nikki!?

[Infinity Nikki](https://store.epicgames.com/en-US/p/infinity-nikki-71fc64?lang=en-US)

Here is a closer look:

[Infinity Nikki](https://store.epicgames.com/en-US/p/infinity-nikki-71fc64?lang=en-US)

What is this?! Why is it appearing above Nikki?!

# Summary

Again, everything in this article is **guesswork**! Here is a little recap:

### 🌞 The game uses shadow maps for beauty

- One pass for everything
**except**Nikki - One pass for Nikki (to fade out her shadow independently while jumping/gliding) –
**except**while being in a cave! - One pass for character self-shadowing (that’s why we see Nikki’s shadow on other characters while jumping/gliding)

### 🕊️ The game uses a blob shadow to help with navigation while gliding

This blob shadow consists of:

- Two decal projections (blob & ambient occlusion)
- The blob shadow seems to be masked by the surface normal

- Two planes (blue circle & blob shadow)
- The blue circle aligns to the surface below
- The blob is always placed slightly above the water and does not align to any surface


### ⭐ Items may have shadows as well (except the items spawn on the fly)

This shadow consists of:

- A (sometimes rotating) decal projection using pre-made textures
- A plane using a pre-made texture for showing the shadow above the water surface

Thanks for reading the article! If you have more theories about the rendering techniques, let me know!

*Simon*

# Bonus Links

[Infinity Nikki](https://store.epicgames.com/de/p/infinity-nikki-71fc64) is a fantastic game, very optimized and the developers extended the Unreal Engine with amazing custom tech like Order-Independent Transparency (OIT), custom particle collision, custom fur and multi layer cloth collision. Read more about it in [this official Epic article](https://www.unrealengine.com/en-US/developer-interviews/behind-the-scenes-of-infinity-nikki-tracing-a-glamorous-turn-to-an-unreal-open-world).

If you can’t hear enough about shadows, there is this awesome [article explaining different old school shadow rendering techniques](https://30fps.net/pages/videogame-shadows/).

[Classic 3D videogame shadow techniques](https://30fps.net/pages/videogame-shadows/)

Here is [a great paper](http://www.diva-portal.org/smash/get/diva2:1441836/FULLTEXT01.pdf) about the difference in perception of blob shadow vs shadow map.

You want even more old school? Then check out [my old article](https://simonschreibt.de/gat/1943-retro-shadows/) about how “transparent” shadows were done in 1987.

![](../../assets/fb2d5f42630df9d3.gif)

Regarding the shadow appearing above the character near the end, this is likely because the decal node is present at all times. It has upper and lower fade properties and while in most scenarios, you only care about the lower fade property for a blob shadow, the upper fade property will kick in when you walk under a low ceiling with a floor above.

This is probably best fixed by reducing the decal’s vertical extents and making the upper fade more aggressive.

PS: Casting decals onto transparent surfaces is something that happens automatically in Godot (thanks to forward rendering), so you don’t need to do anything specific like a dedicated plane for water shadows. :)

Thank you for your comment!

I had the same idea about the decal, but I could not see the same “shadow blob above my head” behavior when I stand below a tent or wooden structure. So there seems to be some special case when it comes to those jump pads.