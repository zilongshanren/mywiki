---
title: Deconstructing the water effect in Super Mario Sunshine
url: https://blog.mecheye.net/2018/03/deconstructing-the-water-effect-in-super-mario-sunshine/
author: Jasper St Pierre
published: '2018-03-03'
source_blog: Clean Rinse
source_site: https://blog.mecheye.net
category: graphics
fetched: '2026-04-13'
---

**Note:** The demos below require [WebGL2 support](http://webglreport.com/?v=2). If you are running a browser without WebGL 2 support, user “petercooper” on Hacker News has helpfully recorded [a video](http://funny.computer/cloud/SunshineSea/mariowater.mp4) and [GIFs](http://funny.computer/cloud/SunshineSea/) and for me.

One of my hobbies is writing model viewers and graphics toys for games. It’s a good mix of my interests in graphics and rendering, in reverse engineering complex engines, and nostalgia for old video games.

I recently extended my [WebGL-based game model viewer](https://magcius.github.io/model-viewer/) to add support for some of Nintendo’s GameCube games, including The Legend of Zelda: The Wind Waker and Super Mario Sunshine. The GameCube, for those unaware, had a novel, almost-programmable, but fixed-function GPU. Instead of developers writing shaders, they programmed in a set of texture combiners similar to the methods used in [glTexEnv](https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/glTexEnv.xml) pipelines, but taken to the extreme. For those used to modern programmable GPUs, it can be quite the mindbending experience to think that complex effects can be done with this thing. And yet, 2002 saw the release of Super Mario Sunshine with some really good looking water for its time. Replicated in WebGL below:

This water effect is loaded into your browser directly from the original game files for Delfino Plaza and placed onto a plane. Let’s take a deeper dive into how this was done, shall we?

## Texturing the plane

Believe it or not, the effect actually starts out like this:

The effect can be seen as a fairly complex variant on something super old: “texture scrolling”. It’s a bit more complicated than what’s displayed here, but the fundamentals remain the same. Our plane starts life as this scrolling wave-y texture, which provides us some interesting noise to work with. This is then combined with a second layer of the same texture, but this time only scrolling in one dimension.

This gives us an interesting moire pattern which is the basis for how the water appears to bubble and shift around so naturally. You might even notice some “ghostly”-looking alignment when the two textures meet up. This artifact is visible in the original material, but it appears more like an intentional sunbeam or a ray of light scanning across the water. Hiding artifacts like this with clever material design is a large part of game graphics techniques.

Obviously, the texture isn’t black. Instead of the colors being black and white, they’re blended in with the background, giving us something that looks more transparent.

Now we’re getting somewhere. At this point, the second texture layer is also added in twice as much as the first, which makes it looks especially bright, almost “blooming”. This feature will come in handy later to define highlights in our water.

Going back to the original material, it’s a lot more “dynamic”. That is, as we move the camera around, zoom in and out, the texture seems to morph with it. It’s clear when it’s near us, and also fades out in the distance. Now, in a traditional fixed-function pipeline, this sort of effect is impossible. There’s no possible way this material can know the distance from the camera! However, Nintendo uses a clever abuse of a more traditional feature to implement this sort of thing. Let’s talk about what I like to call “mip trick”.

## Building a square mip out of a round hole

[Mip-mapping](https://en.wikipedia.org/wiki/Mipmap) is a traditional graphics optimization. You see, when GPUs apply textures, they want the resulting image to be as smooth as possible, and they want to to be as fast as possible. The texture we’re sampling from here is actually only 64×64 pixels in size (yes, it’s true!), and our browser windows tend to be a lot bigger than that. If you zoom in, especially in our last demo, you can “see the pixels”, and also how they blend together and fade in and out, but keep in mind that GPUs have to compute that for every pixel in the *resulting* image. Looking from above, in this case the texture is magnified, but when looking at it at an angle, as the plane becomes more squashed from perspective in the distance, and the texture on the screen drops to less than 64×64 in size.

When this happens, the texture is said to be “minified”, and the GPU has to read a lot more pixels in our texture to make the resulting image smooth. This is expensive — the GPU wants to read as *few* pixels as possible. For this reason, we invented “mip-maps”, which are precomputed smaller versions of each image. The GPU can use these images instead when the texture is minified. So, we have 32×32 versions of our texture, and 16×16 versions of our texture, and the GPU can select which one it wants, and even blend across two versions to get the best image quality. Mipmaps are an excellent example of a time/space tradeoff, and an example of build-time content optimizations.

However, you might have noticed, “as the texture becomes minified”. That happens when it becomes smaller on the screen, which… tends to happen when the texture is… *farther away*. Are you picking up on the hint here? It’s a way to pick out distance from the camera!

What if, instead of using smaller versions of the *same* texture, we instead use different textures? Nintendo had the same idea. This is what I call the “mip trick”. The wave texture I showed you above isn’t the full story. In practice, here’s the full wave texture, with all of its mipmap levels shown.

![](../../assets/30edf888cf9b34df.png)


In the largest mipmap level (where the texture is closest to the camera), we don’t have any pixels. This basically removes the water effect in a small radius around the camera — letting the water be clear. This both prevents the water material from getting too repetitive, and also helps during gameplay by showing the player the stuff underwater that is closest to them. Clever! The second mipmap level is actually the texture I’ve been using in the demo up until now, and is “medium-strength”.

The third mipmap level is the brightest, which corresponds to that “band” of bright shininess in the middle. This band, I believe, is a clever way of faking enviornment reflections. At that camera distance, you can imagine we’d mostly being the reflection from our skybox when at a 20 degree angle looking into the water, like our clouds. In [Sirena Beach](https://magcius.github.io/model-viewer/#j3d/data/j3d/sirena0.szs), this band is tinted yellow to give the level a beautiful yellow glow that matches the evening sunset.

Let’s try uploading all of these mipmaps now into our demo.

That’s getting us a lot closer! We’re almost there.

As a quick aside, since the algorithm choosing of which mipmap to use for the texture is hardcoded into the GPU, it does mean it isn’t necessarily portable. The GameCube renders in a resolution 640×548, and the mipmaps here are designed for that size. The Dolphin developers noticed this as well — since Dolphin can render in higher resolutions than what the GameCube can handle, [this trick can break](https://dolphin-emu.org/blog/2017/11/03/dolphin-progress-report-october-2017/#50-5745-add-heuristic-for-detecting-custom-mipmaps-by-tomcc) unless you are careful about it. Thankfully, modern graphics APIs have ways of applying a bias to the mipmap selection. Using your screen resolution and the knowledge of the original 640×548 design of the GameCube, we can calculate this bias and then use that while sampling.

With that out of the way, it’s time for the final touch. Again, believe it or not, there’s only one thing left to turn our last demo into the final product. A simple function (known as the alpha test) tests “how bright” the resulting pixel is, and if it’s between a certain threshold, the pixel is kicked out entirely. In our case, any pixels between 0.13 and 0.92 are simply dropped on the floor.

This gives us the unique “seran wrap” look for the outer bands of the effect, and in the middle, the water is mostly composed of these brighter pixels, and so the higher threshold lets only the really bright pixels shine through, giving us that empty band and those wonderful highlights!

## Forgotten Lore

In today’s days of programmable shaders, PBR pipelines, and increased art budgets, these tricks are becoming more and more like forgotten knowledge. Nintendo’s GameCube-era games have, in my admittedly-biased mind, some of the best artwork done in this era. Even though I mentioned “GameCube”, the Wii was effectively the same hardware, and so these same tricks can be found in the Mario Galaxy games, Super Smash Bros. Brawl, and even The Legend of Zelda: Skyward Sword. It’s impressive that GPU technology from 2001 carried Nintendo all the way through 2012, when the Wii U was released.

Good art direction, a liberal amount of creative design, and intricate knowledge of the hardware can make for some fantastic effects under such constraints. For more fun, try figuring out the glass pane effects in [Delfino Hotel](https://magcius.github.io/model-viewer/#j3d/data/j3d/delfino0.szs) or the improvements upon the technique used in [Super Mario Galaxy](https://magcius.github.io/model-viewer/#j3d/data/j3d/PeachCastleGardenPlanet.arc).

The code used for every one of these demos is open-source and [available on GitHub](https://github.com/magcius/model-viewer). Obviously, all credits for the original artwork go to the incredibly talented artists at Nintendo. Huge special thanks to all of my friends working on the [Dolphin](https://dolphin-emu.org/) team.

Thanks for taking the time to figure this out, and for taking the time to write it up – very interesting and much appreciated!

Very interesting, love this kind of articles, so much knowledge which has to be preserved and passed on!

coooooool!

Brilliant! Thanks for taking the time to explain it to us!

Saw this on Hacker News and it was a great read! The webviewer is really cool tech too!

Really fascinating article.. Thank you. Bookmarked your site for more!

I’m still impressed by how good the water looks in that game. Very interesting!

Self imposed limits mean I can’t post on HN for a few days but you might find this useful

https://github.com/greggman/oes-vertex-array-object-polyfill

BTW: It looks like WebGL2 is never coming to Safari. If you look at the webkit repo there has been no significant WebGL2 work in over a year

https://trac.webkit.org/log/webkit/trunk/Source/WebCore/html/canvas/WebGL2RenderingContext.cpp?rev=223501

Maybe out of scope for this post but it seems that there’s no mention of what appears to be actual water geometry in the area immediately surrounding Mario in-game? This doesn’t appear in the model viewer and unless I’m not viewing it correctly there seems to be larger waves that move Mario up-and-down such as in the beginning of this video: https://www.youtube.com/watch?v=xeQFDNdSltI

It feels like this is in addition to the texture highlights present in this post, but perhaps there’s another explanation. These larger close-range waves feel like a large part of why this effect is successful in the final product

Good eye! I was kind of hoping nobody would catch me on this. This works by having a small “wave” mesh which surrounds the player with a more rough texture (stored in the game files as “wave.bti”), using a variant effect of what’s done here. The mesh itself is generated procedurally by the engine at runtime, and the material (as far as I know) is just hardcoded into the engine. Keep in mind this works by having a fairly small mesh surround the player character with a separate effect — the traditional water effect is still there underneath.

amazing water

Pingback: How Nintendo Did The Water Effects In Super Mario Sunshine | Kotaku Australia

Oh wow, this is a seriously awesome writeup. I always wondered as a kid how they managed to make the water look so good. Thanks a lot for sharing! :D

Thanks for taking the time to enlighten us. Really appreciate your efforts.

Is the grayscale layer technically acting as a grayscale bumpmap texture?

No. There is no bump mapping in this material.

Looks like your embeds are broken?

I renamed the GitHub repo and didn’t expect the links to 404. Fixed now, thanks for the report!

Chromium on Linux, Intel integrated graphics (i5-6200U). It seems that anything past “white” wraps around to “blue” and begins reaching for white again. This is most visible in “Let’s try uploading all of these mipmaps now”.

Late reply but this is actually intentional — the recorded videos were taken on an older version of the site that doesn’t have the overflow. This has been double-checked against hardware so I know the new style is correct.

It seems like the examples are broken, I can only see the skybox and a blue water color.

This should be fixed. Sorry!

It seems that all examples are broken. Show only black and console spams 404 errors

Should be fixed now.