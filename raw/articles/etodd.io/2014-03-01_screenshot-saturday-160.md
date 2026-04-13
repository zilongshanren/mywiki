---
title: Screenshot Saturday 160
url: https://etodd.io/2014/03/01/screenshot-saturday-160/
published: '2014-03-01'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Screenshot Saturday 160

This week I finally fixed my water code to allow finite bodies of water like this:

(It's so dark because I still have a pesky rendering bug)

I also realized I accidentally had pre-multiplied alpha turned on for my cloud texture. Here's what it looks like when you use pre-multiplied alpha incorrectly:

And here it is fixed (I also made the clouds fade in over distant objects):

I finally fixed a long-standing bug which caused shadows to get really shaky when the camera was far from the origin due to floating-point errors. I fixed it by rendering everything as if the camera is at the origin. Here it is before:

And after:

(I also switched from back-facing shadow maps to front-facing).

I also did a ton of level design and minor tweaks like making the game pause when you alt-tab away from it, but that's boring stuff. Here's something cool, I totally rewrote the orb enemy to be much scarier.

That's it for this week. Thanks for reading!