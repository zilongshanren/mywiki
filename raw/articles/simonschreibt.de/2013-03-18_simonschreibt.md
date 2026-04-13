---
title: Simonschreibt.
url: https://simonschreibt.de/gat/homeworld-2-backgrounds-tech/
author: Simon
published: '2013-03-18'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

Some people asked in the [Polycount thread](http://www.polycount.com/forum/showthread.php?t=115889&page=7) how these Homeworld spheres ([see this Article](http://simonschreibt.de/gat/homeworld-2-backgrounds/)) were created. Let’s do it together! What we’ll use here are modding tools. I have no idea how near these are to the original [Relic](http://www.relic.com/) workflow.

## Download

Download [this mod tool collection](http://www.moddb.com/games/homeworld-2/downloads/homeworld-universe-mod-tools) and use the command line tool “HW2BGBuilder”. There’s also “HW2 – Spookysoft – HOD Tool 1.5.0.1” but it didn’t work out very well for me.

## HOD Viewer

For viewing your .HOD file you should use “CFHodEdit 3.1.5” (open your .HOD, then at the bottom of the program scroll to the lat tab “Miscellaneous” and press “HOD Preview”).

## Let’s go!

Ok, first we create a test .TGA to see what we can expect. I would say, this should work well (1024×512, 24bit):

![](https://data.simonschreibt.de/gat026/blog_testtexture.jpg)

Create a shortcut to the HW2BGBuilder.exe and drag & drop your texture on it. Let it calculate some stuff and then hit “Space” to start the process and feel like a Matrix hacker while numbers run down the command line.

![](../../assets/ff84e3790f478e54.gif)

And this is how it looks in “CFHodEdit”. You can clearly see the UV layout of the sphere. Now we know three things:

- Don’t add detail at the top/bottom of the texture because it gets stretched a lot.
- The left/right side of the texture has to fit to each other to avoid a visible seem.
- The colors are brighter than in the original texture, more about this later.

![](../../assets/5082080a11201d7b.gif)

![](../../assets/9a745f0ff9d7bdf0.jpg)

Regarding the last point: in Homeworld they painted only smooth gradients where the poles of the sphere are and avoid any visible stretching. Also, the vertices are pretty rare in these areas, which leads to smooth vertex color gradients. Take a look at the geometry around the pole:

I think this is just awesome. Because of the limitation to use detail only on the horizontal areas, you achieve that the player (hopefully) never looses his orientation.

Now, let’s use a “real” texture. But before that, we have to decrease the output level from 255 to 128 (Photoshop > Image > Adjustments > Levels).

![](../../assets/47937eb552ef1147.jpg)

**255**

![](../../assets/760b1c0b0bb4b799.jpg)

**128**


After the creation process you’ll find a “_ref.TGA” which is an edge map the program uses for the sphere creation. I think this looks fascinating. I think the quads are the parts which the program calculates after each other.

![](../../assets/a35923a36ea4cb7d.jpg)

And this is how it looks in the viewer. Especially at the top of the big mountain you can see some color bleeding. I didn’t play around with the settings of the “HW2BGBuilder”. Maybe there’s space for improvements, but in general I think the result is pretty good.

![](../../assets/f535c36cf36fc43a.gif)

The resolution of your source texture has an impact on the sphere intersections and on the course of the polycount.

![](../../assets/e5ef6f9f9da8edbb.jpg)

![](../../assets/b384766a443f4da5.jpg)


My last point will be a bit technical. Please correct me if I’m explaining it wrong. There is a good point why I said “Bye” to mathematics and went the way of graphics. :)

- 1 Pixel needs 24 Bit/3 Bytes to be saved (RGB, every channel has 8 Bit)
- 1 Vertex needs a position (XYZ)
*and*a vertex color (RGB)

This means, if your source texture contains too massive contrast and detail everywhere, you would get more data than when you use a texture. But the Homeworld backgrounds consist mostly of colors and gradients, and only **sometimes** more detail. So for this purpose, this optimization is awesome.

While writing this article, there were discussions going on how to achieve this poly reduction in zBrush:

[Computron](http://www.polycount.com/forum/member.php?u=44049)posted his results[here](http://www.polycount.com/forum/showpost.php?p=1798325&postcount=163).- And
[poopinmymouth](http://www.polycount.com/forum/member.php?u=13622)posted a[great link](http://forums.relicnews.com/showthread.php?148734-Homeworld2-Background-Builder-v1-3)where the creator tool is explained with all its parameters.

Love this blog! Keep it up :)

Thanks man :) Glad to hear this!

Thanks! I was able to run the tools on mac with wine! So happy it just worked

Nice to hear! Don’t hesitate to show us you test results :)

On the 3rd to last image, the way you where rotating the camera “by mouse” looked a bit like you were free falling, surrounded by mountains!

I remember feeling like the cleverest little five year old when I noticed the sky in the early Spyro games seemed to be doing something with triangles, but at the time I would have no idea what it was I was looking at!

I wonder what the advantages and disadvantages of an animated vertex coloured skydome would be…

You noticed it when you were 5 years old? Wow…that’s incredible :) When i was that old i didn’t noticed pixels at all and never thought about bad graphic or something like that. Just enjoyed Colonization in 320×340 :D

Do you know of a good tool to convert cube map backgrounds to the spherical ones HW2BGBuilder requires?

Unfortunately no :,( I think you would have to convert your cubemap by hand…

This pretty smart!! Especially with most pixels ending up at the top and bottom of the sphere, where you just don’t look.

I wonder how many other has used similar techniques…