---
title: Simonschreibt.
url: https://simonschreibt.de/gat/homeworld-2-backgrounds/
author: Simon
published: '2013-03-15'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

This article was updated. Jump to [Update 0](https://simonschreibt.de#update0). [Update 1](https://simonschreibt.de#update1). [Update 2](https://simonschreibt.de#update2). [Update 3](https://simonschreibt.de#update3).

What you see here![](../../assets/a15003c057865cc1.jpg)


is the stunning background art![](../../assets/6f898269b477bd21.jpg)


of one of the most beautiful sci-fi games.![](../../assets/3ea88f62a464f0ab.jpg)


H o m e w o r l d 2

Thanks for reading.

Just kidding. Of course, I have something to say about this. In the company, we look at the art of [Homeworld](http://en.wikipedia.org/wiki/Homeworld) from time to time and bow to the creators of this masterpiece. Once, we talked about how great the background look and how interesting this sketched style is. There is something…some details seem…special to us:

![](../../assets/2a6a693e05ed5b4a.jpg)

I mentioned, that this looks a bit like… a vertex color gradient. But they wouldn’t paint the background on geometry, right? I mean…that would have to be a highly tessellated sphere.

The discussion was over, but I wasn’t satisfied and wanted to at least see the textures. So I used some [mod tools](http://www.moddb.com/games/homeworld-2/downloads/homeworld-universe-mod-tools) to extract the Homeworld 2 Demo data, but there were no textures. Only some .HOD files. I used Google and found a thread how to generate these .HOD files from a .TGA. It was said:

“…scans every pixel of the image then based on contrast


it decides whether or not to add a new vertex and color…”

What?

Could it really be, that this is vertex color? Luckily you can watch at .HOD file with CFHodEdit. And another tool can force a wireframe mode. And now look what this brought to light:

This is one![](../../assets/305acbdb394597ff.gif)


of the most brave![](../../assets/cce2876359da759f.gif)


solutions for game art i ever saw.![](../../assets/a085c098e72c5c6f.gif)


And here you can see how this influences the sky sphere geometry of the game. Do you see how low the resolution is in the low contrast areas? And how round the sphere is where details were painted?

![](../../assets/72f95c4099a3d830.gif)

I never ever had thought, that this can produce such good results. Oh, and don’t forget that this technique solves two major problems:

- You don’t have any problems with DDS texture compression artifacts.
- More important from composition perspective: since you can’t get too fine detail (it was said in the tutorial that the base TGA shouldn’t contain too sharp details), the background stays where it should:

In the **background**.

Too often, I see games where the background contains so much noise and details, that you can’t really separate fore-/midground from background.

The last time I saw this perfect combination of tech & composition was in Diablo 3. [I talk about the 2.5D tree article](http://simonschreibt.de/gat/diablo-3-trees).

Thanks for reading.

![](../../assets/ba0680151067ebbc.png)

[Russian Version](http://habrahabr.ru/post/250467/) by [Eliiah](https://twitter.com/Quad_Games) | [Korean Version](http://woodorl.tistory.com/36) by Woodorl Kim

Some people asked in the [Polycount thread](http://www.polycount.com/forum/showthread.php?t=115889&page=7) how these Homeworld spheres were created. Let’s do it together! What we’ll use here are modding tools. I have no idea how near these are to the original [Relic](http://www.relic.com/) workflow.

## Download

Download [this mod tool collection](http://www.moddb.com/games/homeworld-2/downloads/homeworld-universe-mod-tools) and use the command line tool “HW2BGBuilder”. There’s also “HW2 – Spookysoft – HOD Tool 1.5.0.1” but it didn’t work out very well for me.

## HOD Viewer

For viewing your .HOD file you should use “CFHodEdit 3.1.5” (open your .HOD, then at the bottom of the program scroll to the lat tab “Miscellaneous” and press “HOD Preview”).

## Let’s go!

Ok, first we create a test .TGA to see what we can expect. I would say, this should work well (1024×512, 24bit):

![](../../assets/c58c8ab04c11db93.jpg)

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

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

[Chris Correia](https://twitter.com/ChrizCorr) works on a space game and asked me about the stars in the Homeworld-Backgrounds because they are super-sharp. I remembered having seen a thread like this a while ago and [here it is](https://forums.gearboxsoftware.com/t/background-star-fields/544377/12)!

In fact, the stars are single textures/billboards:

![](../../assets/ba0680151067ebbc.png)

Possible to post a couple of large image files perhaps?

Thanks for the article. These images would make absolutely awesome multi monitor wallpapers (thinking eyefinity 6000~ x 1024 resolution+), any chance you could provide some really high resolution versions? cheers!

See answer below :D

Hi “-” and “Pete”. Thanks for your comments! I think i’m not the right adress for highres pictures. But i know a place where something like this is the topic: http://deadendthrills.com/

I wrote them an email about your comments and that you would like to see something about Homeworld. With a bit luck we’ll get it :D I would love to have them also.

So this is awesome to find out, I would have never imagined. Not to derail or hijack but since this is Homeworld related and you profess a certain love for the game, I wanted to put this out here. Some guys are working on a kickstarter to try and revive the old homeworlds for digital distribution and touch interface, then move on to make a Homeworld 3. http://www.kickstarter.com/projects/teampix/homeworld-touch-ios-android-and-homeworld-3-pc-mac/

Yeah thanks for the link! But do you think this will be working? I mean buying the license, building the game for only 50.000?

http://www.controlcommandescape.com/articles/beware-the-homeworld-3-kickstarter/

This comment has been removed by a blog administrator.

This guy pulled the backgrounds somehow.

http://walter-nest.deviantart.com/art/Homeworld-2-Space-Backgrounds-200251891

Thank for the hint! I wrote him i message how he did it. I hope he’ll answer. :)

What is even more impressive is that the Spyro Games and Crash Team Racing on play staion One did their bachgrounds that very same way. I guess it saved them memmory back then and they were not so constrained by polycounts, but still a curious and non-intuitive trade-off. CTR even did that for textured surfaces, more specifically, for the Boss Portraits over the boss race door on each world hub in that game, there is a drawing of the boss which if you look at in wireframe, you can verify it uses no texure, but a bunch of gouroud shaded polys.

I noted you comment you maybe i get the chance in the future to look into it. Thx!

Does anybody knows a tool which will do the same with arbitrary models, not with sphere? My idea is to bake lightmaps to vertex colors, and with this kind of tessellation the end result might be almost the same if not better than high-resolution lightmap. Maybe somebody knows games which used this kind of tesselation for lightmapping?

Personally i can’t say anything about this :(

I noticed the same thing on Spyro, and remembered this article.

When you have a big gradient represented by only a few vertices and their interpolated colors, you’re saving all the memory an equivalent texture map would take.

This must’ve been an important optimization for these classic Playstation 1 games.

Super Mario Sunshine for the Gamecube also does vertex color, but for the environment shadows as seen here ( http://blitzbasic.com/Community/posts.php?topic=90523#1029305 ).

Regards.

By the way, the water in SMS looks amazing. I was impressed by that effect and went on to research what kind of technique drives it.

( http://www.gamedev.net/topic/614608-specular-highlights-on-water/#entry4881841 )

Thanks for these links! Really interesting…the shadows and the water look really good. I tried around with MipMaps for water too – to fake the total reflection :)

Thanks for the interesting article! I figure this technique will still be useful on low-end OpenGL ES2 hardware with limited memory bandwidth for textures.

Just for kicks I wrote a Python and OpenGL based viewer for the hod backgrounds, see https://github.com/laanwj/hw2view for the source code.

Wow that’s great! I didn’t have the time to check your tool, but thank you for sharing and mentioning me in your description :) And yes, i think this tech can be really useful. Not only for low-performance but maybe also for art-style. Sometimes restrictions are the source of creativity :)

You’re right. We did something similar for many background elements (and entire backgrounds) in Castle Doombad. The 2D artist drew up whatever he saw fit, then one of the technical artists/animators hand-matched it with geometry. I was amazed how quickly & precisely he pulled it off.

Still, that was with large solid-colored areas and just a few simple gradients. A tool that could automatically generate geometry for arbitrary hand-painted images, like Relic apparently developed for Homeworld 2, would be a great project.

Yeah that’s right. I really nice side-project which surely can still help in modern games. :)

I’ve been working exactly on this automation tool for the past few months! But in my case I’m even working on further compressing down the meshes. Stay tuned!

Does anyone know anything of games or articles related to this topic? Perhaps some that apply this method too, or worked on some automation?

I am doing this project partly for my own interests and for my master thesis research. It isn’t easy finding these pages. Glad I stumbled upon this article, makes for a beautiful reference! :)

Hm … maybe Oskar Stålberg (see Update #1) can help you with that. Or you can find a programmer who worked on the original Homeworld and ask him? Whatever you do, let us know when you’re done! Would be awesome too see what you’re comming up with!