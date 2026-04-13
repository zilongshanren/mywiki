---
title: 'Shader Showcase Saturday #2: Waterfalls - Alan Zucconi'
url: https://www.alanzucconi.com/2018/07/21/shader-showcase-saturday-2/
author: Alan Zucconi
published: '2018-07-21'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

Historically speaking, waterfalls have always had a special place in games. From Super Mario to Tomb Raider, their role has been more than just aesthetic. Often hiding secret caves, waterfalls are now iconic. This is why I believe is important to celebrate some of the most well-crafted waterfalls that have been posted online in the past few months.

I hope this will encourage more readers to try out what shaders can really do, especially when it comes to rivers, lakes and oceans.

## River Shader

This lovely diorama crafted by [Alberto Mastretta](https://twitter.com/SpeedyMastretta) features a stylised waterfall that ends in a small lake. Not much has been shared about the technology behind it, but is likely that the gentle movement of the water is created using a technique called **vertex displacement**. I have covered this topic extensively in an article titled [Surface Shaders in Unity3D](https://www.alanzucconi.com/2015/06/17/surface-shaders-in-unity3d/), where it is applied to make a 3D model skinnier or chubbier. A more sophisticated application of vertex displacement can be found in the [Tentacle Suckers Shader](https://www.alanzucconi.com/2017/06/20/tentacle-suckers-shader/) tutorial.

The reflections that can be seen on the water surface are probably achieved by replacing Unity’s default **lighting model** with a **toon shading**. A primer on both topics can be found in the article about [Physically Based Rendering and Lighting Models](https://www.alanzucconi.com/2015/06/24/physically-based-rendering/) in Unity3D.

The foam lines that appears close to the shores are a pretty common effect that is adopted in most stylised water shaders. It relies on the **depth buffer** to detect when the water surface is “close enough” to another piece of geometry. Game developer Linden Reid wrote a very clear tutorial about foam lines called [Simple Water Shader in Unity](https://lindenreid.wordpress.com/2017/12/15/simple-water-shader-in-unity/).

### Wildbrew

A simpler, yet very effective shader can be seen in the game [Wildbrew](https://twitter.com/wildbrewgame), currently being developed by [Dondragmer](https://twitter.com/dondragmer_). If you want to achieve a similar effect, I highly encourage you to read the full thread. The author is providing insight and images to document how this look was achieved. The water effect is inspired by [this tutorial](https://twitter.com/minionsart/status/925036278005018624) posted by Shader Witch Joyce, better known on Twitter as [MinionsArt](https://twitter.com/minionsart).

### Crystal Waterfall

Most waterfalls that appear in recent indie titles tend to adopt similar techniques and, consequently, to look rather similar. This is not the case for this beautiful waterfall created by [Dan Stockford](https://twitter.com/I_usually_do) for a game currently in development by [Broken Pixel Studios](https://twitter.com/_brokenpixel).

I suspect the foam might be made out of white spheres which have been placed manually, as they don’t seem to appear around every edge like they normally would relying on a depth texture.

The horizontal and vertical parts of the water are most likely different shaders, as they seem to behave quite differently.

### Unlit Waterfall

The last effect I want to talk about in this article is by [Harry Alisavakis](https://twitter.com/HarryAlisavakis). His article [My take on shaders: Unlit waterfall](http://halisavakis.com/my-take-on-shaders-unlit-waterfall-part-1/) has great instructions on how to replicate it, and it could be a good starting point if you want to achieve something similar. It was originally inspired by Reddit’s user AnthemOfDemons earlier post ([here](https://www.reddit.com/r/Unity3D/comments/8fv1t4/finally_got_inspired_enough_by_all_the_shader/)).

Harry is also authoring a series of shaders tutorials which show how he would have re-created certain effects. I have recently discovered his work and I do think that he definitely needs more support. You can find out all of his shaders tutorial [here](http://halisavakis.com/tag/shaders/).

## Leave a Reply Cancel reply