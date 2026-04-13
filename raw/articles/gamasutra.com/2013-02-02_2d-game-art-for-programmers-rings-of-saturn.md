---
title: 2D Game Art for Programmers - Rings of Saturn
url: https://www.gamedeveloper.com/art/2d-game-art-for-programmers---rings-of-saturn
author: Hans Hildenbrand
published: '2013-02-02'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

So the urge to write the tutorial (and have some fun) wins... and I treat myself to a quick tutorial rather than reply a big backlog of emails (which sadly will have to happen later)...

Note:

The standard beginning of my tutorial seems to be a circle - such a versatile little thing - and then I duplicate and transform it. I am just not sure if I mentioned some quick way to do the duplicate and keep it in place. Duplicate a shape (CTRL-D). Hold CTRL and SHIFT while scaling the object - the scale will keep the proportions and scale based on the pivot point. (Holding just CTRL keeps the proportions and scales based on the lower left corner.)

Let's get started with a simple version of a Saturn style planet with a simple one shape ring around it.

![](../../assets/9daf4eea3782c4f4.jpg)


I added the pattern of the planet (bunch of squashed and slightly differently shaded circles) and the shadow shape (one circle with another circle cutting out the sickle shape via a Path/ Difference) to a mask. I did the same with the shadow of the planet on the ring.

Next up... the same thing with more elaborate rings. Let's face it... it's the same thing... You just take the intial ('unsquashed' ring) and make it more complex by combining several rings of increasing sizes into one object...

![](../../assets/5e9d6d1c48be16f7.jpg)


You can add a more realistic look by adding a circular gradient and more detail patterns to the planet. Breaking the rings apart (Path/Break Apart (SHIFT+CTRL+K)) allows you to assign different colours to different rings and vary the opacity to the rings. I added some small objects and their shadows on the rings for a bit of detail.

I hope you enjoyed this as much as I did and give it a try... as usual it's a lot easier than it looks once you worked out how to do it.