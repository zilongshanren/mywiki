---
title: A simple trick for fast high quality bokeh on lights in Cello Fortress
url: http://joostdevblog.blogspot.com/2014/08/a-simple-trick-for-fast-high-quality.html
author: Joost van Dongen
published: '2014-08-29'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Cello Fortress](http://www.cellofortress.com)I came up with a simplified version of bokeh that looks really high quality, is very fast to render and even very easy to implement. My implementation also has some severe limitations, but I think it can work really well for many games.

Bokeh is a part of focal blur, which is also known as depth of field blur or DoF. DoF is the effect that only objects at a certain distance are sharp, while everything closer and further away is blurred. This is an effect that every lens has, and the larger the lens is, the stronger the blur is. Focal blur has been done in many games for quite a while now, but with the normal DoF rendering techniques the bokeh effect is usually lost. Bokeh means that extremely bright spots grow with the blur and appear as clearly recognisable circles (or hexagons or other shapes, depending on the shape of the lens).

![](../../assets/75ec3595b79338e4.jpg)

*Image from*

[HDWallSource.com](http://hdwallsource.com/bokeh-23995.html).The problem with rendering bokeh in games is that a naive implementation requires high dynamic range (HDR) rendering and an extremely large amount of blur samples. HDR has become quite common in games by now, but taking enough samples to get good sharp bokeh is impractical. For bokeh as large as in the image above, you would probably need many hundreds of samples to get it look smooth. I actually tried that exact thing in

[Proun](http://www.proun-game.com)two years ago, as a fun little experiment.

Proun already had really high quality DoF (as I described in

[this blogpost](http://joostdevblog.blogspot.nl/2010/09/depth-of-field-blur-in-proun.html)). I added bokeh by simply making some pixels extremely bright. This is a quick dirty trick that was needed because Proun only has limited fake HDR, but the effect looks pretty convincing, as you can see below on the left image. However, if the blur is increased the bokeh becomes extremely noisy, as you can see on the right. It looks noisy despite that it already uses a quite insane 128 samples per pixel! You can find more images of this approach in

[this blogpost](http://joostdevblog.blogspot.nl/2012/04/fun-bokeh-experiment-in-proun.html).

![](http://www.proun-game.com/Oogst3D/BLOG/Bokeh%20trick%20-%20Proun.jpg)

This makes this naive approach unusable if strong blur is wanted. We need something smarter. The most common approach in current games seems to be to render actual polygons with a bokeh circle texture on them. To do so we need to find all the bright pixels in the image and then generate a quad for each one.

According to

[this article](http://bartwronski.com/2014/04/07/bokeh-depth-of-field-going-insane-part-1/)The Witcher 2 was ahead of its time by having bokeh all the way back in 2011. The Witcher 2 did this by generating a quad for

*every*pixel and then discarding the ones that are not blurred enough. That's a whole lot of sprites to render! Needless to see this only worked in real-time on the very fastest PC videocards.

Most games that have bokeh these days seem to use a smarter approach, using newer shader models: first they look for all the pixels that are so bright that they would get a clear bokeh circle, and then they generate quads for this. An example of this approach can be found

[here](http://mynameismjp.wordpress.com/2011/02/28/bokeh/). Unlike The Witcher 2's technique this creates only the bokeh itself, not the general focal blur, so with this technique the depth of field blur needs to be done separately.

Even with this clever technique the performance hit is still heavy. It requires analysing all the pixels on the screen to find the ones that are much brighter than the ones next to it. It also produces temporal artefacts: if the source of the bokeh is really small it will flicker because it is smaller than a pixel. Normally this is not that much of a problem because it is only a pixel, but if a big bokeh sprite flickers on and off this becomes much more noticeable. These temporal artefacts might already show with slight camera movements. I don't know what technique Star Citizen uses, but the kind of flickering this would result in can clearly be seen in

[this video](http://youtu.be/hgjMOeq--1A?t=1m17s)in the bright spots in the background.

Now that we roughly know how bokeh is usually rendered, let's look at that simple and fast trick that I use in Cello Fortress. My idea comes from that the most pronounced bokeh is often from actual lights, not just random bright pixels. If you are looking directly at a light, but the light is in the blurred background, then it will generate a very clear bokeh circle. In general a game engine already knows where all the lights are, so this means that we can

**skip the searching for bright pixels entirely and directly create one screen-space quad for every light**. To do so I first render the scene, then apply normal depth of field blur, and finally render the bokeh sprites on top of that.

Not only does this method skip the expensive step of finding the bright pixels that need bokeh, it also fixes all the issues with temporal artefacts. We always know exactly where the lights are so no matter how small they are, the bokeh will never flicker when the camera moves. It just moves along with the light correctly.

![](../../assets/4295ed0a14fa0a63.jpg)

To get a good-looking effect I scale the bokeh with how blurred the light should be. This can simply be calculated based on the focal settings of the camera and the distance to the camera. I also fade out the bokeh sprite a bit as it gets larger, since the larger the blur, the less bright the bokeh circle should be (unless the light is infinitely bright). Here is a video that shows the bokeh in action in Cello Fortress. The bokeh is mostly visible at the bottom of the screen.

An important part of bokeh is the actual shape of the bokeh effect. This shape is created by the shape of the lens. I often like hexagonal bokeh best, but I recently discovered that in photography this is generally considered ugly. When reading reviews of a new camera lens I wanted to buy I learned that the more expensive lenses have circular bokeh while cheaper lenses have hexagons. Still, in the end the only thing that matters is what looks good aesthetically in your game. Since most bokeh rendering techniques use those textured sprites the bokeh shape can be modified really simply by using a different texture.

![](../../assets/85e8b014e119d60c.jpg)

Note that this all does not look as good as it can yet because I have so far spent too little time on the actual visual design of Cello Fortress. I mostly focussed on the gameplay and some cool shaders. Once I start working on proper graphics I should also tweak the brightness, size and colour of the bokeh to make it look better. I should probably also try adding a bit of chromatic aberration to the bokeh texture then.

My bokeh technique does not solve occlusion at the moment. If a light disappears behind an object then it should not still get a bokeh sprite. I didn't solve this yet because it does not occur in the current version of Cello Fortress. However, several solutions can be implemented easily. For example, I already have a depth texture for the depth of field blur, so I can do a look-up in that on the screen position of the light to see whether there is an object in front of it.

The big downside of my method for rendering bokeh is that you need to know where the bokeh will appear beforehand. This means that more subtle bokeh sources like reflections and strong speculars are not practically doable. I can imagine some tricks to get for example bokeh in planar reflections working (if you know where the reflecting planes are), but beyond that it quickly becomes infeasible. The standard technique of searching for the bokeh pixels of the image handles this much better, so if you really need bokeh on speculars, then you will probably need to resort to such techniques.

![](../../assets/79e8a41b852a96ab.jpg)

*Image from*

[this article](http://mynameismjp.wordpress.com/2011/02/28/bokeh/)by MJPI looked up a bunch of articles on bokeh implementations and couldn't find any mention of something similar to what I am doing. This surprises me because the idea is so simple and obvious. If anyone knows of any articles or games that already do this, then please let me know so that I can add a link.

That's it! My bokeh technique is simpler and much faster than most commonly used methods of rendering bokeh and it even fixes problems with temporal artefacts. It is also a limited technique that does not handle all bokeh effects, but in many cases it will probably be good enough. It definitely is for Cello Fortress!

This sounds a lot like lens flare effect, but with blurred sprite.





ReplyDeleteAt least, similar to how lens flares are implemented in my dayjob render, when they aren't assigned only to the sun, but to any light source and only one sprite is used with zero offset towards screen centre rather than a line of multihued spots.

We have the same limitations with regards to reflections, and we use an occlusion query to check if a light is visible and dim the flare sprite if it's partially obscured.

We use a setup like that to make brighter halos around lamps.

I like how your idea of bokeh is actually usable on low-end devices.

Good point, it is indeed very similar to a simplified lens flare. :)

Delete