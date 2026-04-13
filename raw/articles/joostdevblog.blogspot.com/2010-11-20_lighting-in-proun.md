---
title: Lighting in Proun
url: http://joostdevblog.blogspot.com/2010/11/lighting-in-proun.html
author: Joost van Dongen
published: '2010-11-20'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Proun](http://www.proun-game.com)is getting a lot of very positive responses to how it looks. Most people seem to think that the depth of field blur is the core reason for this, but the game still looks pretty good when that is turned off. What really makes the biggest difference, is the careful lighting.

Since most of Proun's environments are static, the lighting is calculated beforehand and stored in lightmaps. Calculating lighting beforehand is called

*baking*.

*Baking*should not be confused with

*cooking*, which stands for saving memory directly to disc (this is used to speed-up loading times, because you don't have to parse cooked data). Interestingly, I have heard rumours that the terms

*baking*and

*cooking*are also sometimes used for certain algorithms that are used in kitchens, but I don't know anything about that.

Lightmaps take up a lot of space (one third of Proun's total size), but they have some big benefits. Because lighting is calculated beforehand on the developer's computer, it doesn't matter if it takes a lot of time. This means that much more complex lighting can be used than when it is calculated in real-time. In Proun, I use this a lot. I think calculating all the lightmaps for just the second track cost my laptop about 30 hours!

![](../../assets/a083a3f84196140b.jpg)

The further a shadow is from the object that casts it, the blurrier is gets, especially if the light source is large. Lights that cast shadows that get blurrier with distance are usually called

*area lights*. In practice, it is hardly ever possible to calculate this in real-time, so most games have either fully sharp shadows (as if the light source is infinitely small), or a fixed blur that ignores distance.

![](../../assets/b1a80424bbff12dd.jpg)

![](../../assets/818de14527e782ec.jpg)

(On a sidenote: as soon as Proun is finished, I am going to implement a technique that I have come up with that makes it possible to render real-time area light shadows in games with a Diablo-like perspective.)

In the real world, a lot of light does not come directly from the sun: part of the light is scattered by the atmosphere and comes from all directions. Such light from all directions is called

*skylight*. Skylight makes shadows less deep and add a lot of subtle shadow effects to the world.

![](../../assets/c1da9ac8181c7c75.jpg)

Objects reflect light. So if light falls on a red object, then this object will reflect a little bit of red light onto the objects around it. This is called

*global illumination*. This is a very subtle effect, but because of Proun's bright colours it is clearly visible in a couple of places.

![](../../assets/819f757116d5e898.jpg)

All of these things are only possible because in Proun, lights don't move and almost all objects are static. I could not have used lightmaps otherwise. The levels are also small enough to store high quality lightmaps of all objects.

The things I discussed here today are pretty technical. In a future blogpost I will talk a bit about the artistic side of Proun's lighting: crazy light colours.

Very interesting to see the subtle effects of the lighting. It is actually more noticeable in such an abstract environment than it would be in a realistic environment.

ReplyDeleteI wonder how long it takes until such effects can be achieved efficiently in real-time (if ever). I'm looking forward to learn more about your real-time area light shadow technique!

Lots of these effects are getting approximated better and better. I think lighting with this amount of precision in real-time may be ten to twenty years away, but for example, Nvidia's Mad Mod Mike demo already contained a pretty sweet trick to fake real-time global illumination on the main character. :)

ReplyDeleteHow do you calculate lightmaps? Do you use Blender for that, any other software or you have made your own?

ReplyDeleteVRay in 3D Studio MAX. I made custom plugins for 3dsmax to turn it into my level editing tool, including a script to automatically call unwrap on all the models and then let VRay render the lightmaps. :)


ReplyDeleteMy 3dsmax plugins are released with the game, so if you download the beta, you can make your own levels. ^-^

Ha! 2010! I was a fool to believe this kind of tech wasn't going to be on hardware from only 3 years from now.

ReplyDeleteLol! :) Pre-rendered lighting like this has been in games for something like ten years already, I think.

Delete