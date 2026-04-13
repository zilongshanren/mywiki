---
title: Simonschreibt.
url: https://simonschreibt.de/gat/alpha1-top5/
author: Simon
published: '2016-01-22'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

![](https://data.simonschreibt.de/gat058/thumbnail_youtube_01_forward.png)


![](../../assets/3900fdd8a1823a54.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

![](../../assets/c0db1ff9e0dd8298.png)


Alpha1-Materials only support 1 Bit color depth for transparency which means you can either see a pixel or you can not. You can **NOT** have half-transparent pixels like with Materials/Shaders supporting 8 Bit color depth (Alpha8):

Alpha1 vs. Alpha8

So Alpha1 stuff is boring? **Not at all!** OK, most often you’ll see it in cases like here where a tile-able Alpha1-texture of netting wire is mapped on some polygons.

Looks good until you see it from narrow angles where you can notice the actual flatness.

![](../../assets/ebe450f92e093152.png)

For today I collected five **creative** use cases for Alpha1! If you don’t think so or know even more awesome stuff, let me know!

![](../../assets/ed42b20eba66a939.png)


With a second layer in your shader/model you can add crisp detail like here on this Mirelurk:

Or add detail to my beloved stone edges which [I wrote about in the past](http://simonschreibt.de/gat/fallout-3-edges/):

And here is a nice example of a layer on top of the geometry which creates some extra motion (I don’t know exactly how it’s done but it looks at least “Alpha1-ish”):

From what I saw they use a texture for **both**: the base geometry and the moving layer on top (which might be an extra geometry **OR** both could be be mixed in **one** shader):

Interesting: The alpha channel of that texture gets “threshold-ed” (more about this later) and defines which parts of the texture are visible regarding the moving layer. I did a small test with a modified alpha channel like this…

…and this is the result:

You can clearly see that only a small portion of my smooth “blobs” in the alpha channel are actually used. Zooming in you can clearly see hard edges which let me think of a hard Alpha1 cutout:

Like I said: I don’t know if it’s two geometries or just one shader, but here you can see the separate layers:

![](../../assets/064d8159b4dafb9e.png)


We’ve some basic trade-offs in game art when it comes to detail:

**Left:**Modelling all detail costs a lot polygons but looks great**Middle:**Saving polygons is good for the performance but makes stuff look angled**Right:**Using Alpha1-Planes adds great details – until you look from a wrong angle

But by **combining** standard geometry with alpha-planes it’s possible to hide some problem zones. I really like the broken planks on these houses which add a great amount of details:

Unfortunately you can see the “trick” pretty clear by looking at them from above:

**But** it’s still interesting that they stack planes over planes and somehow avoid any z-Fighting:

My guess is that they have priorities assigned to the different materials so that the renderer knows what comes first.

![](../../assets/ebe450f92e093152.png)

**BMP**file format supports an alpha channel!

Now an example which I like even more. Do you see what’s going on here?

They use Alpha1-Planes to make the holes look round **but in addition** add some low-poly geometry to give the object thickness.

Yes, you can see low-poly edges at the backside but the general impression is great in my eyes.

![](../../assets/c4555be8d3dc8307.png)


At a closer look you’ll notice that in most games barrels aren’t perfectly round. This holds true for Fallout 4 (look at the center of the barrel) **but** what’s that? The front looks very round!

They hide the 14-poly-cylinder-angularity with a plane containing a round alpha1-shape. Might not be breathtaking but at least I saw something like this the first time.

Also interesting: They don’t cap the ends like you usually would expect. They use Alpha1-planes which saves some polygons and since all parts use Alpha1-materials (the walls have holes) there’s only **one** material/shader necessary.

I’m not sure if this creates too much overdraw or if you can early discard the fragments for the “invisible” pixels but at least it’s an interesting approach.

![](../../assets/b38d8e604c9e89e6.png)


You may think: If we can only **show** or **don’t show** a pixel with an Alpha1-Shader then there shouldn’t be a need for grey values! That’s **not true** because of **two** reasons.

First let’s look at the alpha channels below which “should” give the same results:

![](../../assets/6192f622b38c347d.png)


From distance they result in very similar outcome:

![](../../assets/0f90da90185e3111.png)


But at a closer look you can see a great difference in quality:

![](../../assets/0b03af7f7987c32f.png)


The reason is the texture filtering which happens on the graphic card. Both textures get up-scaled and filtered when you see them big on your screen:

![](../../assets/c10d63bb58822f00.png)


Then a threshold is used to define which of the grey values will be “completely white” and which “totally black”. As you see, the texture with Anti-Aliasing/grey values is better “smoothed” during the filter process and finally results in a rounder Alpha1 mask:

![](../../assets/09b47b0fc45f168e.png)


That’s why grey values can help even if the texture is only used for “binary” Alpha1.

The second reason is even more interesting because you can use the threshold for creating great effects if you have grey values in your alpha channel!

For example in [Firewatch](http://www.firewatchgame.com/) they use the threshold to make trees in the distance have less details (I strongly recommend to [watch the whole talk](https://www.youtube.com/watch?v=ZYnS3kKTcGg)!):

Here’s another stunning example! This is my texture from earlier and you can see what happens when I manually change the threshold value:

And here you see a particle system doing exactly that (with a different texture). It spawns an particle and **over its lifetime** the threshold is increased:

Isn’t that amazing?? I l❤ve it! Below you can see an example where I **think** (I **don’t** know it for sure) they used similar stuff on the slime and blood:

![](../../assets/90748ac480aed8ab.png)


Let’s get to my favorite. It’s not #1 because of spectacular effects – it’s the other way around: It’s very subtle and I waited a long time to see a solution to this problem and expected it coming from tesselation, parallax occlusion mapping or other fancy techniques.

If you have a delicate structure like this…

…you can’t avoid that it looks **flat** when you look at it from the side. If you would try to do the Fallout-Trick by adding some low-poly geometry you would need to spend a lot polygons because of all the fine detail!

But why does the railing in [Batman](http://rocksteadyltd.com/#arkham-city) **doesn’t** look flat?

It’s not a crazy shader or complex math. It’s very simple:

It’s just two planes with a small offset and the perspective does the rest!! It’s like with many of these tricks: If you know them they don’t seem very spectacular anymore but I never thought about such a **simple** solution!

Yes, it has problems when the planes have too much space or the angle gets too narrow…

…but when you play the game as you should and just walk by, it works perfect! I really like this subtle addition to detail which shows the care of the artists working on the Batman games. Well done! :,)

Thank you for reading until the end! I hope you liked the article and if you know other cool Alpha1-tricks or suggestions feel free to get in touch with me.

Have a nice day!

![](../../assets/ba0680151067ebbc.png)

[Alkemi](http://www.alkemi-games.com/)have a great post about how they used some thresholding in their game

[Drifting Lands](http://www.drifting-lands.com/). Also their way how they create the textures at first place is very interesting.

Read all of it here: [A Game of Tricks III – Particles fun (part1)](http://www.alkemi-games.com/a-game-of-tricks-iii-particles-fun-part1/)

![](../../assets/ba0680151067ebbc.png)

[Wizardry 8](https://en.wikipedia.org/wiki/Wizardry_8)because we saw this and thought:

*“Oh look, a crate!”*:

But when we approached it we were wondering: *“Why does the crate has 5 sides?”*

After two seconds of silence it hit us: *“Ohh…it’s supposed to be a barrel!”*

Maybe it was only funny in that situation but it’s kind of interesting that in on other areas of the game they have barrels with even **seven** sides! Maybe because they’re used in-door?

This goes to [Nuee](https://steamcommunity.com/profiles/76561198022719467): Thank you soooo much for taking the screenshot for me! :) (To the others: I don’t own the game and had trouble finding screenshots showing the barrel from near distance)

![](../../assets/ba0680151067ebbc.png)

Hi,

you’ve already linked to some of our resources earlier but our game Drifting Lands does use 8 bit alpha to create mask animation. You can see a detailed explanation of the mask animation here :

http://www.alkemi-games.com/a-game-of-tricks-iii-particles-fun-part1/

It’s combining this with gradient mapping you were talking about in the mushroom explosion article.

I’ll add that we’re not really converting 8bit alpha to 1bit alpha but we’re just doing a level operation to convert ‘blurry’ animation data to harder edged shapes with still some kind of antialiasing!

Cheers,

– Alain

thanks for the link :) have to read it later because i’ve jump into a train now but i just scrolled over the article and wow … that looks awesome!!

Hey Simon! The lack of z-fighting is easily explained! :D

When rendering hard alpha (alpha1/alpha ref/…) you can actually do z-testing pretty cheap in the shader so it will be sorted on top in the right depth. As it’s a true/false check it still has quite good performance in comparison to soft alpha.

Oh whow! Humus-guy here posted about an interesting alpha-test solution http://humus.name/index.php?page=3D&ID=61 10 years ago! :D

I actually dunno it that’s state of the art right now.

i saw this before and as great their solution is the less i can understand what exactly they’re doing. also other sources don’t explain that very visually :D i’ll see if i can find better explanations.

nice to know :) thank you!

Great stuff as always Simon!

Really neat article on your site as well Alain! Can’t wait for more :D

thank you very much! good to see that there’re other alpha1 fans out there :)

Great examples of using Alpha 1 and an excellent article. I’m looking forward to using this new knowledge in my own projects.

make sure you keep me up to date if you have something to show :)

Will do :)

Thanks for the article!

I’m not sure if it’s alpha 1, but I thought the fur tech of Shadow of the Colossus was pretty neat. (Similar to your last example about railing thickness, but with many more layers for more parallax) It was interesting to see the same technique in Vivisector (but with 8bit alpha or something?), but I guess the technique is depreciated nowadays since fur/hair can be simulated now.

Yeah SotC has so awesome fur! I think it’s still interesting for today’s games because not everyone can simulate the fur/hair like AAA studios can and also sometimes there’s no performance for that (e.g. on smaller mobile devices). This break down is soooo great: http://www.froyok.fr/blog/2012-10-breakdown-shadow-of-the-colossus-pal-ps2

There is no z-fighting in Fallout 4 because they are using so called “Alpha tested shader”. It simply uses alpha channel and threshold value. If alpha is greater (or lower, depending on your code) than threshold, you don’t render the pixels. Such shader can be rendered the same way normal opaque geometry is rendered so you don’t have any z-fighting. Actual code for this is trivial (this is real code snippet!):

if (texture.a < threshold)

discard;

It's called alpha-testing because you usually use texture's alpha channel for cutting out stuff. But you can use any texture channel you want or any data that it suitable (vertex color, position, whatever).

Wow, thank’s for your explanation! Do you know the engine so well because of modding experience?

I don’t know f4 engine but I’m a graphics programmer. Cutout geometry (aka alpha-tested) is a standard rendering technique whitch is shared amongs all directx and opengl engines (and Fallout engine is using one od it for sure).

Got it :) Just was wondering because the threshold sounds like zFighting shouldn’t be an issue with alpha1 but here is an example (again from Fallout4) where some zFighting occurs and I’m not sure why sometimes they make it work perfect and sometimes the don’t :D

https://youtu.be/S2K-GfTZ1Gc