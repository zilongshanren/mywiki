---
title: 'Shader Showcase Saturday #4: How To Start A Fire With Shaders - Alan Zucconi'
url: https://www.alanzucconi.com/2018/08/05/shader-showcase-saturday-4/
author: Alan Zucconi
published: '2018-08-05'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

In the two previous instalments of **Shader Showcase Saturday**, we have talked about [waterfalls](https://www.alanzucconi.com/?p=9486) and [interactive grass](https://www.alanzucconi.com/?p=9545). Those two subjects sound very different from each other, yet they share something in common: the original phenomenon can be modelled as a fluid simulation. This week’s Shader Showcase Saturday will continue this trend, talking about another effect that involves fluids: **fire**.

With so many games featuring a firearm of some kind, fire and flames are present in the vast majority of FPS and RTS. What we call fire, is nothing more than a mixture of hot gasses moving chaotically. Due to their temperature, these gases glow, producing the typical yellow and red. The colour emitted by a heated gas depends on its temperature. A fireplace burning at 600°C typically gives a yellow light, while a methane cooker which burns at almost 2000°C produces blue flames.

In actuality, the air around is always emitting light due to its temperature, but that glow is outside the **visible spectrum**, hence is *invisible* to us. This also means that fire allows us to see how turbulent the air around is really is, despite looking transparent. If you are interested, there is a special technique, called [Schlieren photography](https://en.wikipedia.org/wiki/Schlieren_photography) which allows seeing those turbulences.

When it comes to games, however, fluid dynamics might not be the most efficient approach to have flames in your game. This is where a good understanding of **shader coding** can be very handy.

There are several techniques that have been used to recreate fire and flames in games, but this week I want to focus on approaches that rely on shaders to simulate the flame behaviour. [Davide Ciacco](https://twitter.com/ciaccodavide) has posted a video showing how the movement of a flame can be recreated just using a quad and a shader.

The main idea is to use some **noise texture** with a gradient texture, and choosing a cut-off value so that all pixels which value is below will not be drawn. If you then scroll the noise texture upward, it will look as is the fire is actually rising. Playing with a colour gradient and another shape for the masking allows creating a variety of very pleasant effects which can be used for everything from flames to magic.

You can see how this effect has been used in [Overland](https://store.steampowered.com/app/355680/Overland/), together with a toon style which keeps the centre of the flame well separated from the rest. In the video below, I suspect each individual flame is done using a different quad. If your game has a fixed camera angle, you can place these quads manually. However, if you move around, you will need to change the shader so that these quads are always facing the camera. This technique is often referred to as **billboarding**.

Overland has a non-photorealistic aesthetic, but if you choose your colours carefully, you can obtain extremely believable results. This is definitely the case [Papetura](https://twitter.com/PapeturaGame), a game currently in development which uses this very technique to create photorealistic flames. *Papetura* mixes real backgrounds with 3D models, so it was essential for the game to have such a high quality effect.

The flame seen above is perfect for a candle. While creating a flame shader is relatively easy, creating such a realistic one takes a lot of effort and time. An asset that might help you is [AAA Candle Flames](https://prf.hn/click/camref:1100l45Ay/destination:https://assetstore.unity.com/packages/vfx/particles/fire-explosions/aaa-candle-flames-79652), which features photorealistic candle flames for an exceptionally low price. If your game has candles, is hard to get something nicer (and cheaper) than that.

For an even more realistic look, it is also possible to animate the meshes where the flames are rendered. This is what VFX Artist [Klemen Lozar](https://twitter.com/klemen_lozar) has done in Unreal (below), where a **vertex function** is used to make the flame move under the effect of wind. This effect has been discussed extensively in the Shader Showcase Saturday dedicated to [Interactive Grass](https://www.alanzucconi.com/?p=9545), where there are all the links necessary to get you started with simulating wind.

While those particular flames look realistic, they cannot be simply reused for *any* fire. Each material produces its own unique flame, from shape to colour. It is important, if your game features many objects engulfed by flames, to spend time making each type of flame unique. If this is your need, my suggestion is to rely on [Ian’s Fire Pack](https://prf.hn/click/camref:1100l45Ay/destination:https://assetstore.unity.com/packages/vfx/particles/fire-explosions/ian-s-fire-pack-69661), which comes with 29 prefabs that are crafted to emulate photorealistic flame for everything from bonfires to burning oil.

One aspect that contributes to the overall realism of a large fire, is obviously smoke. While there will be soon another Shader Showcase Saturday dedicated to smoke, in the meantime you can have a look at [Lit Smoke And Fire 2](https://prf.hn/click/camref:1100l45Ay/destination:https://assetstore.unity.com/packages/vfx/particles/fire-explosions/lit-smoke-and-fire-2-79694), which is hands down the best asset to simulate smoke. What makes it even more interesting is the ability to choose the level of realism you want and, consequently, how heavy the effect is going to be. This feature is really helpful for medium to large words, as you might want to reduce the cost of distant bonfires in the background, while keeping the one nearby as realistic as possible.

## From the Asset Store…


## Leave a Reply Cancel reply