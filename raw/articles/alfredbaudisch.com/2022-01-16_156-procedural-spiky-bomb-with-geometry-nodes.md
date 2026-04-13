---
title: '156: Procedural Spiky Bomb with Geometry Nodes'
url: https://alfredbaudisch.com/experiments/3d-art/156-procedural-spiky-bomb-with-geometry-nodes/
published: '2022-01-16'
source_blog: Alfred Reinold Baudisch
source_site: https://alfredbaudisch.com
category: game programming
fetched: '2026-04-13'
---

I'm still very newbie when it comes to Geometry Nodes, so as a challenge, I tried to do something by my own, to test my newly acquired knowledge. This has been done 100% by me, without following tutorials.

It took me almost 4 hours, mostly because I was trying to understand how to evenly space the spikes.

![](../../assets/6472203901046d69.png)


## Problem

- I wanted to create a UV Sphere with spikes (cones), where spikes are aligned to the UV Sphere's faces normals. I want the spikes to be alternated/ping-ponged: one spike, an empty spot, so on and so forth.
- I tried to alternate the spikes by using the faces indexes, if the index is even, show spike, otherwise, hide it. The problem is that the faces' indexes are not linear.
- I also tried by comparing normals or comparing indexes that already have the "spike", but I don't know how to compare with previous iterations using Geo Nodes (i.e. if spike has already been shown at this normal/or this index, do not show it now, like storing a temporary variable – this is so simple with coding).

This is the ball full of spikes:

When I tried to alternate the face's indexes using a Math – Modules node %2:

Desired output:

## Proposed Solutions

**Ginyumbi** from [Erindale's Discord](https://discord.gg/9WP7MS6nCg) proposed using an odd number of segments and it worked immediatelly. But the problem is that at the last row of faces there would always be two spikes side by side:

Then Salami in the same Discord came to the rescue, by suggesting: "if the segment is even, simply offset the index by 1 if the row is even".

And it worked! I then changed it in a way that at the top there's a unique bigger spike. And that's it.