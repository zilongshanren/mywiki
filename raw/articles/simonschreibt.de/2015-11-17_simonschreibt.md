---
title: Simonschreibt.
url: https://simonschreibt.de/gat/fallout4-wasteland-eyes/
author: Simon
published: '2015-11-17'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

**imploded**head came to me. Only eyes and teeth were left but everything else was fine. Her eyeballs looked great.

![](https://data.simonschreibt.de/gat054/pipBoy_symbol.png)

![](../../assets/43a4ddd526bc21f3.png)

**not**using a full sphere as eyeball you save:

- polygons
- two bones
- and of course the skinning information for the eye

![](../../assets/43a4ddd526bc21f3.png)

[Dr. Med. Schindler](http://gamepat.de/)stated that this technique might be problematic when you want slightly animate the flesh around the eyes when they move.

Normally you would just skin the flesh with a low percentage value to the eye-bones (which we expect to not exist in this case).

But on the other side: Somehow they make it happen to synchronize eye-movement and eye-lid, so maybe even more fleshy-interaction would be possible?

[Prof. Dr. Schaika](http://www.marcelschaika.com/)suspected that there might be bone-limits or other performance-relevant reasons while

[Dr. Dr. Unger](http://polyphobia.de/)mentioned that this technique is very interesting for cartoon-characters where the eyeball can’t be spherical like in this example where the eye is more shaped like a cylinder:

**why**will be a secret.

If you read this diary and originate from the Bethesda-Vault, feel free to take a Brahmin, come over and tell us the whole story about the mysterious eyes of the wasteland.

![](../../assets/43a4ddd526bc21f3.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

I bet the shader just provides jitter as in normal human gaze while still allowing the eye to follow via the bones, which provides a center to return to.

would be awesome if someone of bethesda could explain it :)

The link in Update 2 is wrong (copy-pasting from Update 1? :) ) It should point to Reddit instead.

Oops! I’ve fixed it :) Thank you for the hint!

Super interesting! I can imagine that you set up the animation rig right away with the UV transformation that’s driven by a usual look-at handle. So when exporting … ? You either have a realtime rig and re-do the same ingame. Or you export the UV offset in separate animation channel. Might even be into a value of an unused bone. (we do this for blendshape values)

But actually I suppose they have it combined in some way: have it animated + have realtime influence.

There was a nice assumption in reddit about this: https://www.reddit.com/r/gamedev/comments/3t5swh/i_wrote_a_small_article_about_the_eyes_of_the/cx3pz7e

Would be great to hear from a fo4dev how they did i exactly :D