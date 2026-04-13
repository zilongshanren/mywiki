---
title: Simonschreibt.
url: https://simonschreibt.de/gat/teleglitch-rgb-flickering/
author: Simon
published: '2013-01-21'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

If you use a teleporter in [Teleglitch](http://teleglitch.com/), there appears a really nice effect. After having a closer look i noticed, that they distort the three channels R,G and B indifferent ways. I really like this “Hardware is a bit f*cked up” – effect.

[Deadlight](http://www.deadlightgame.com/). I think they also did some stuff with the different RGB channels. You can see this pretty good at the top right corner at the water tank. Unfortunately i can’t say more about this, because they didn’t spoke about this in their

[The Art of Deadlight](http://www.youtube.com/watch?v=b0Huw18GsUY)video.

![](https://data.simonschreibt.de/assets/icon_update_01.png)

![](../../assets/ba0680151067ebbc.png)

This effect is commonly referred to as “Chromatic Abberation”. It can sometimes be used to simulate old cameras with bad lenses. It is also used in engine Crytek (their water shader uses it to simulate seperation of light), and in the mod Black Mesa as a damage indicator.

Chromatic abberations are optical effects and tend to be yellow against cyan, green against purple.

But RGB distortion is very digital, and reminds much more of an old out of sync video tape.

Im the author of that post process ^^

So glad that a dev is raising his hand. Cool to hear! If you want to explain it into a way an artist can understand, i would love to add this to the article. I tried to explain it but maybe i missed something.

Oh, I didnt know “Teleglitch”. Its a pretty easy effect, just to distort each color channel independently.

Oh I’m sorry! You worked on Deadlight as i saw. Really nice looking game! But the RGB-Fx is not just distorted equally, right? It looks like its stronger in the outer parts of the image, right?

Yep, its stronger as pixels gets closer to borders. You need a gradient from screen centre to screen borders that will modulate distortion offset.

Good to see you here again :)