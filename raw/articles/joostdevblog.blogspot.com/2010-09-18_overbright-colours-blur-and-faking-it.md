---
title: Overbright colours, blur and faking it
url: http://joostdevblog.blogspot.com/2010/09/overbright-colours-blur-and-faking-it.html
author: Joost van Dongen
published: '2010-09-18'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Proun](http://www.proun-game.com). Now let's look at one that is a lot more subtle: blurred HDRI.

In computer games, colours are usually stored with values from 0 to 255, with 0 being black and 255 being white. Few people realise that this introduces some limitations.

The problem is that when an object is lit by a very bright light, its colour might actually have brightness 400 instead of 255. To solve this, graphics cards usually just round this down to 255, since your monitor or television cannot show anything brighter than that anyway.

But what happens when we blur such a bright area with its dark surroundings? Without blur, a white square with value 255 looks the same as one with value 400, because monitors cannot show anything brighter than 255. However, when blurred, there is a big difference, as you can see in this image:

![](../../assets/ea19447e9338ff8f.jpg)

As you can see here, when blurred, really bright objects should look like they grow: they overshine the area around them. Dark details around overbright objects can even totally disappear this way. In Proun, this can be seen clearly in the white boxes at the start of the first track: in the distance, their black outlines disappear. I love to look at this effect:

![](../../assets/90c4d063f1092f9b.jpg)

Allowing colours to go beyond 255 is called HDRI (High Dynamic Range Lighting). On the graphics hardware, to make this happen, you can simply turn this on. (In technical terms: switch the render buffer from 8 bit fixed point per colour channel to 16 bit floating point).

However, that is pretty slow, especially on slightly older videocards. So to save a lot of performance in Proun, I faked the HDRI in a pretty easy way. Objects are simply rendered half as bright as they really are and then after the depth of field blur has been applied, the pixels are made twice as bright again. The end result looks just like HDRI, but without the slowness.

There are two drawbacks to this, though: values cannot go above 511, so there is still some rounding down of the colours going on, and when made more extreme (as is done in the tunnels in Proun), artefacts become visible because everything is made so much brighter. Those artefacts are rarely visible in Proun, but they are in this specific tunnel (still quite subtle, so this may be difficult to see on some monitors):

![](../../assets/031c0801d7a6b8e3.jpg)

An extra benefit of doing HDRI, is that bright colours combine into new colours when blurred. This is kind of a weird side effect, but it looks really cool in the places where the spheres overlap in this image:

![](../../assets/15d5ad499c89954c.jpg)

Which reminds me: I need to do something with explicitly coloured glow in a future game. Maybe have a bright brown object with a green glow or something like that. :)

## No comments:

## Post a Comment