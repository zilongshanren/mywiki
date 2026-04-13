---
title: Simonschreibt.
url: https://simonschreibt.de/gat/company-of-heroes-shaded-smoke/
author: Simon
published: '2013-08-09'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

When I saw that the smoke is shaded (depending of the angle you look at it) I was impressed but had no idea how it works:

![](../../assets/bea4cdc361ecef35.gif)


Sorry for the stuttering, i had to capture it with [CamStudio](http://camstudio.org/) and rotate the Camera by hand. At first I thought maybe they move a gradient along the particle textures depending on the angle to the sun but later I learned that’s they modified the normals of the particle (see the updates below).

![](../../assets/ba0680151067ebbc.png)

[Eric Chadwick](http://www.polycount.com/forum/showpost.php?p=1896563&postcount=288)mentioned that a similar effect was already used in Shadow of the Colossus. His post

[links to a PDF](http://lukasz.dk/files/making_of_sotc.pdf)where you can find the smoke shading on

**page 16**.

If you’re interested in more thoughts about the issue, feel free to read the comments on [the polycount thread](http://www.polycount.com/forum/showthread.php?p=1897749#post1896557).

![](../../assets/ba0680151067ebbc.png)

[present you this link](http://www.slideshare.net/proyZ/relics-fx-system)which was posted into the comments by a really nice guy (i guess a Relic-Dev, but he wrote it anynom) which talks about the Relic-Fx-System and the also show the smoke particle shading.

![](../../assets/ba0680151067ebbc.png)

I don’t know how Relic did it in CoH, but one way to do this is to only calculate the lighting for the four corners of a particle quad with normals bend away from the particle center and interpolating instead of lighting them per pixel. This is quite a bit cheaper and although it will smooth out the details in the lighting that is often beneficial in the case of smoke.

Two games that use that technique to light their particles are Bioshock and Shadow of the Colossus. If it was even possible on PS2, Relic might have done something similar.

What confuses me is, that not all particles are lit the same way. They all point at you and have more or less the same orientation. But sometimes the “shadow” clearly is stronger on the one side.

Here’s an idea how it might be possible to achieve that effect:

https://dl.dropboxusercontent.com/u/3284052/ParticleShading.jpg

On the left is regular flat particle with normals pointing forward. In the center the normals are bend out from the particle center to achieve the effect I described before. Finally on the right I instead bent the normals away from the particle-systems center. This way you get a more clear light and shadowy side to the whole system. Maybe they did that?

To use the whole particle system is a nice idea! Could be possible. Or, like eRiC said (below) it’s made for every particle and since they overlap, an effect like this would be possible.

Other suggestions can be read in the polycount thread: http://www.polycount.com/forum/showthread.php?t=115889&page=12

Thanks for thinking about this and posting the image from your dropbox :)

the gif is not one sprite only is it? At least 2 I’d think. CryEngine has a similar feature. There you can say hov much a particle sprite bulges towards the cam. works without bumpmap too.

Really? I should work with the CryEngine some times :) Thanks for your comment!

This comment has been removed by the author.

FWIW, we broke the lit quads into 4 triangles (pyramid) and bent the outside normals away. The lighting is a combination of the directional sunlight and an ambient colour. Quite manageable on good hardware in 2006.

If you want to know how the relic fx system works we did a presentation about it at the 2012 Korea Game Conference, you can find the full presentation slides here:

http://www.slideshare.net/proyZ/relics-fx-system

First: Thank you so much for writing the comment! It seems you’re a Relic-Dev and every comment is a honour for me but a Dev-Comment mostly brings a mass of knowledge with it. Really cool!

Second: Thanks for this link! It’s awesome! Really interesting how genius your Fx System is.

Hi, Simon!

Thank you for such a good and informative articles! About this kind of effects you can also check Drew Skillman web site: http://drewskillman.com/vfx.html and their presentation about Brutal Legend VFX: http://drewskillman.com/GDC2010_VFX.pdf

WoW! These links are awesome! Thank you so much for sharing! <3