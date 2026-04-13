---
title: Stardust Touch-Ups for Brilliant Scenic Demos | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2011/02/stardust-touch-ups-for-brilliant-scenary/
author: Allen Chou
published: '2011-02-26'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

[Wonderfl](http://wonderfl.net/) is a, as its name suggests, wonderful website that provides online ActionScript 3.0 compilation service, where you may post code, share code, and fork code. Recently, I’ve run into two fantastic scenery simulation demos by [Yonatan](http://wonderfl.net/user/yonatan), the [Super Express Desert Sunset](http://wonderfl.net/c/juFu), and [Sea and Clouds](http://wonderfl.net/c/2HBv) demos.

I’ve decided to use [Stardust](https://allenchou.net/code.google.com/p/stardust-particle-engine/) to apply some touch-up to these two demos, in order to see how much I can boost the visual effects with particle effects. And here they are.

**Super Express Desert Sunset (Stardust ver.)**

In this demo, I’ve used simple horizontal rectangles as particles, and used the blur filter to create a motion blur effect. The particles are perturbed by some random drift and are drawn to the left by a uniform gravity field. I really love this train window view of rain (or snow) running by during sunset 🙂

**Sea and Clouds and Fireflies**

Here the water wave reflection effect is pure brilliance. I just can’t help adding some firefly effects to make it even more fantasy-like. The original code draws the entire scene to generate the water reflection, which is quite convenient for me to add particle effects, since the particles are automatically drawn onto the water without extra coding effort.