---
title: Simonschreibt.
url: https://simonschreibt.de/gat/bioshock-glossiness/
author: Simon
published: '2013-04-19'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

You see that i run out of topics by talking about tricks which aren’t existing. Do you know that, if a game looks better in your imagination than it actual does? I had a nice detail in my mind which i saw in Bioshock. So i revisited the game and…it *wasn’t* made how i thought. :(

So what now? Forget about it or mention it anyway? Maybe someone could use at least the idea…let’s see:

When i saw this door in [Biohock](http://www.bioshockgame.com/) for the first time, i immediatelly noticed: the reflections are well done. And today i think: they still are! Look how great the wood differs from the glass. And how the two structures of the glass pop out. ♥ But i had something different in my memory…

*intensity*of the specular, but

*not*the size of the spot. The smoother a surface, the smaller the light source reflection. If a surface is rough, you get a bigger and smoother reflection. Below you find a link to a

[polycount thread](http://www.polycount.com/forum/showthread.php?t=76839)with a link to the

[Valve Wiki](https://developer.valvesoftware.com/wiki/Main_Page)for more information.

*only*control the specular strength but also the size of the spot (smaller on the glass, bigger on the wood). But after short look into the game and their textures it was clear: they don’t (there was no extra control texture).

- Maybe i could inspire you to think about the specular issue in general. It’s very interesting how light works and how we try to press this complex phenomenon in game engines.
- I think even with a standard specular map, the door is a really great example how well specular can (and should) be used for different materials.
- Something which speaks against the idea of controlling the reflection size (besides of the setup effort): You have to store the information somewhere. Regardless if you do it per vertex color, in a texture mask, in a color channel or per object: you need extra resources.

I would love to hear your opinion about this article. Because it’s not about an awesome trick but on the other hand it *is* definitely a great example. So feel free to contact me and tell me your opinion!

Actually you don’t need to separate specular intensity and size of the specular spot. This is related values because the energy conservation law.

For example see slides 35 and 37

http://renderwonk.com/publications/s2010-shading-course/snow/sigg2010_physhadcourse_ILM_slides.compressed.pdf

So programmers can write shader and use single texture for specular intensity and specular spot size, this is called normalized specular.

Thanks a lot for this link! Very interesting! I guess we control size and intensity separately because the calculation isn’t very accurate in some games and this is the only way to tweak it out, would be my thought…

But you need to abstract away from microfacets in CG, so only having intensity and deriving gloss from that is a really limited and strange way of working.

Same method as in terminator salvation also used in many modern games.

Here link for some gamedev papers

http://renderwonk.com/publications/s2010-shading-course/hoffman/s2010_physically_based_shading_hoffman_b_notes.pdf

http://www.rorydriscoll.com/2009/01/25/energy-conservation-in-games/

That’s certainly the way one should go about it, but I fail to see how this removes the need for a gloss map?

Really interesting links! Thank you for sharing! As more a i read about it, i wonder why this isn’t standard implementation for the specular :D

I spotted a cool trick in Doom3. Doom3 has a fixed gloss falloff which was fairly wide. But they managed to have sharp speculars on fleshy bits by simply having very tight highlights painted into the specular maps. That’s totally unrealistic, but it looked perfectly convincing. They cheated the trick even further in Rage by prebaking static specular highlights into stuff (!!) and it didn’t look wrong at all. They also did the same thing with really wide specular reflections in some spots. There’s something interesting at work… It seems if you make speculars really sharp or really wide you can get away with a lot.

That reminds me of an old not well known trick by 2D animators called the ‘scribble cell’; you scribble some random lines and use those as a mask for a second drawing with white dots, which pan across the scene. Through the gliding in and out of existance due to the scribble mask it looks like tight specular reflections on water.

About Doom 3: I checked out the ID DevNet but only found textures from Quake 4. There i couldn’t see the white spots in the specular (only some in the diffuse) but maybe that because they didn’t do it like you said in Q4 or the resolution of the texture in the article i too low. I have to checkout the D3 textures…sounds interesting! Here’s the link to the dev net (textures in the lower part of the article):

http://www.iddevnet.com/quake4/ArtReference_CreatingModels

Here’s an explanation of the scribble cell thing, seems i got it backwards, it’s the dots that are static.

http://www.newgrounds.com/bbs/topic/550605

Wow, this cell trick is awesome! I think this is worth a small article here on the blog…i really like this trick, even maybe i’m the only person which didn’t know it :D awesome! It look so great…to be honest, exactly this is something i thought about sometimes in the past…how to get these nice animated sparkles into water. :)

We did something similar to this for specular in The Chronicles of Spellborn. I’m not in touch with the technical artist/programmer anymore or I’d ask him how it was done, but basically: our specular texture masked a small scribbly texture that moved somehow (with the camera vector?) so you got some quite convincing motion within the specular highlights. We’d really only have thin highlights painted into the specular texture, never large areas.

It worked really well on dark metals like gold!

Sad that the game isn’t playable anymore :,( Would love to check it out in the game…