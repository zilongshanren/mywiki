---
title: A look at how Campo Santo created convincing water for a (cut) game trailer
  scene
url: https://www.gamedeveloper.com/art/a-look-at-how-campo-santo-created-convincing-water-for-a-cut-game-trailer-scene
author: Alissa McAloon
published: '2018-03-16'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

"To bring the scene to life, we’d need nice-looking water, which wouldn’t be convincing if it didn’t react to the motion of the characters and surrounding geometry.”


- Matt Wilde explains how and why he endeavored for realistic-looking water in the trailer.

Campo Santo’s Matt Wilde has [shared an interesting and in-depth blog post](http://blog.camposanto.com/post/171934927979/hi-im-matt-wilde-an-old-man-from-the-north-of) about the months-long process of creating realistic water for the In the Valley of Gods’ announcement trailer that is well worth a look if you’re in the VFX business.

Wilde, somewhat of a self-proclaimed near-expert on animating blood, magic, and urine, explains how he and graphics programmer Pete Demoreuille combined their efforts to create water that would react convincingly to the environment around it.

First up, Demoreuille created a GPU-based simulation using a shallow-water approximation, which resulted in multiple dynamic textures to be fed into the shader for the water surface’s height, normal map, velocity, and distance from any partially submerged obstructions.

“It’s a little more accurate than traditional video game techniques, as it accounts for the water’s depth and computes its horizontal velocity along with height,” explains Wilde. “For collision with the characters and the world, a ‘signed distance field’ can be precomputed for the static environment, and characters are added in per-frame by attaching primitives (capsules, in this case) to bones in their rigs.”

From there, Wilde took the reigns, first creating a flow mapping texture and eventually working toward a more water-like shader through the addition of normal mapping, depth-based transparent, causing lighting effects and more.

![](https://media.giphy.com/media/uVQLquUKfpcFsRrJeQ/giphy.gif?width=342&auto=webp&quality=80&disable=upscale)


The end result is the gorgeous water found in a clip on Wilde’s full blog post. Unfortunately, it seems the insightful blog post itself is the only fruit of the duo’s labor; Wilde says that, after a few months work, the scene in question was ultimately cut from the bit In the Valley of Gods reveal.

Of course, Wilde describes the entire process in vivid detail and offers a number of gifs and videos to illustrate his progress through the creation process in the full post, so be sure to [check out the Campo Santo blog](http://blog.camposanto.com/post/171934927979/hi-im-matt-wilde-an-old-man-from-the-north-of) for the complete breakdown.