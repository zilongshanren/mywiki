---
title: Simonschreibt.
url: https://simonschreibt.de/gat/divine-fire/
author: Simon
published: '2023-05-06'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

This article was updated. Jump to [Update 1](https://simonschreibt.de#update1).

This article is brought to by the year **2017**.

Back then, a very kind Madame J. (part of [Larian Studios](https://fr.wikipedia.org/wiki/Larian_Studios)) was aware of my blog, saw that [Divinity: Original Sins 2](https://store.steampowered.com/app/435150/Divinity_Original_Sin_2__Definitive_Edition) was on my Steam wishlist and mentioned that to the team. Only a bit later, I received a mail from a certain Monsieur G. (also part of Larian) because he gifted me the game. That was very nice!

Fast as I am, it took me only 5 years until I finally played the game and fell in love with it (and its VFX). And so it happened, that today I’d like to present:

In the video below, we can see **two** different ways of using VFX to show that a character burns. The skeletons spawn fire particles at certain bone positions, but my attention was forced to the hot lizard in the center. It looks like the character mesh itself is duplicated and used as foundation for a fire shader. Spoiler: It’s exactly that.

[Divinity: Original Sins 2](https://store.steampowered.com/app/435150/Divinity_Original_Sin_2__Definitive_Edition)

I’ve tried to replicate the shader, but I was never sure if I found the right way. Lucky us: there are **official modding tools** which allow for in-depth inspection!! I’ve watched [this official video](https://www.youtube.com/watch?v=zHf_wNTDNIo) about the installation (super quick & easy) and then I was able to:

- Open Effect Editor
- Select “Shared”
- Search for “burnin” (or “burning” if you’re smarter than me)
- Double-Click
*RS3_FX_GP_ScriptedEvent_ BurningHistorian_Reignite_01* - Press Play

With these tools, we can have a closer look at how the effects are made and watch them from all angles!

[Modding Tools for Divinity: Original Sins 2](https://youtu.be/zHf_wNTDNIo)

I’d like to note some potential issues/details:

- We can see that the (fire) mesh is
**not****only**stretchede upward but also a bit toward the sides (especially visible on the fire starting at the head) - Deforming a mesh like that results usually in strong UV stretching, but the fire texture actually doesn’t look stretched
- There needs to be a soft gradient to make the fire fade out as it raises
- The sides of the (fire) mesh fade out soft as well and are
**not**super harsh

For those who are already experienced, the solutions to these points are: **vertex offset** (based on vertex normal mask), **Fresnel** and **world space based texture mapping**.

*“But Simon, why are you so sure about all of this?”*

Because with the modding tools we can actually look at all the materials as well! In the Effect Editor you can find a so-called “Overlay Material” with the name *RS3_FX_OverlayMaterial_ Burning_01.lsmg*. With this information, you can open the Material Editor, open the material and investigate the whole node system:

For those who can’t wait anymore, here is the complete material (it’s read from right to left, like in the good old [UDK](https://docs.unrealengine.com/udk/Three/DevelopmentKitHome.html) days!). For everyone else, I’ll break it down further below.

## 1. Pushing the Vertices

First, the mesh gets duplicated (Larian calls this “Overlay Material”) and then stretched by offsetting the vertex positions. Of course, we can not just move the hole mesh upward – there needs to be a mask, and in this case it’s the z-Component of the Vertex Normal. Because this value tells us, if a mesh is facing more upward or more downward.

And here you see it in action. Thanks to our mask, faces which point more upward turn more white (meaning a value towards 1.0) while faces pointing side wards or downwards stay dark (towards 0.0) – the values never go into the negative space because of the friendly saturate-node which clamps everything between 0.0 and 1.0. We push the vertices upwards, but this value is multiplied with our gray scale mask which means: where the mask is darker/black, nothing moves:

## 2. Adding Fire

Now it’s time to apply these two textures. The fire is used as the main structure and the noise is there to distort the UVs a bit to add some extra motions to the flames.

Problem: The original mesh UVs are heavily stretched now. Therefore, we use the **World Position** as UVs (known as [Triplanar Mapping](https://youtu.be/sjpszGetM40), but in this case the shader only does Duoplanar Mapping because the top faces are masked out in the next step so the fire is never seen from above anyway).

Now the fire needs to fade out. And we already have a mask for that! Do you remember the grayscale mask based on the z-Component of the Vertex Normal? This can be perfectly used here to subtract values from the fire (this is called [Alpha Erosion](https://realtimevfx.com/t/what-is-your-alpha-opacity-mask-clip-erode-animation-workflow-like/7705)). Add a little bit of Fresnel and it’s perfect.

While it looks very good on organic surfaces like the lizard of the sphere, one might argue that there are some weird flying polygons above the crate. Doesn’t this make this technique useless?

First, let’s check if this issue happens in the real game as well. Yes, it does:

[Divinity: Original Sins 2](https://store.steampowered.com/app/435150/Divinity_Original_Sin_2__Definitive_Edition)

But is this a problem? I’d say: **No**.

First: The game is mostly played in top-down perspective and with that, this artifact isn’t as visible. In addition, if one does not pay close attention, it might not even get noticed. This is a wonderful example where the result is maybe not perfect but absolutely good enough.

For me, finding the right moment where a VFX is good enough is one of the hardest challenges. Sometimes I invest way too much time to find the “perfect” solution only to find out, that all this extra work added only a tiny bit of quality.

By the way, if someone from Larian reads this: Origin Sins is great and Baldur’s Gate is awesome bla bla bla, but I L♥VED the original [Divine Divinity](https://en.wikipedia.org/wiki/Divine_Divinity) soooo much!! So, please… would you kindly make a Divine Divinity Remaster and then Divine Divinity 2? Thank you!

We’re almost at the end, but I wanted to underline that there are **tons** of cool VFX to discover with these mod tools. Here are some examples – maybe they can encourage you to open up the tools and get inspired. :)

[Divinity: Original Sins 2](https://store.steampowered.com/app/435150/Divinity_Original_Sin_2__Definitive_Edition)

That’s it! Thanks for reading, I hope you liked the article and learned something! Let me know!

Have a wonderful day,

Simon ♥

![](../../assets/ba0680151067ebbc.png)

Another thing I really like about those modding tools: They show nicely the different states of an effect. In the timeline on the right, we can see a turquoise bar **“Lead In”** and then a red **“Loop”**-phase which in fact, loops as long until the “Go to next phase”-Button is pressed which jumps to the green **“Lead Out”**-phase.

[Modding Tools for Divinity: Original Sins 2](https://youtu.be/zHf_wNTDNIo)