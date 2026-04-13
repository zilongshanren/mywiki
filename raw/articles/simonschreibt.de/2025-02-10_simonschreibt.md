---
title: Simonschreibt.
url: https://simonschreibt.de/gat/cyberpunk-broken-edges/
author: Simon
published: '2025-02-10'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

This article was updated. Jump to [Update 1](https://simonschreibt.de#update1).

This post extends my [Fallout 3 – Edges](https://simonschreibt.de/gat/fallout-3-edges/) article.

While the decal in Fallout “only” added detail to the surface but didn’t change the silhouette, we can see a beautiful breakup of the straight concrete wall in [Cyberpunk 2077: Phantom Liberty](https://www.gog.com/en/game/cyberpunk_2077_phantom_liberty):

[Cyberpunk 2077: Phantom Liberty](https://www.gog.com/en/game/cyberpunk_2077_phantom_liberty)

To me, this looks so good, that I would not be surprised if it would be a custom mesh with unique texture.

**But it is not!**

It all starts with a simple box as wall (with chamfered/beveled edges) and a detailed mesh which is stuck into the wall as overlap (there are 3 steps of fade-in for the wireframe because this mesh uses 3 different materials and therefore renders in 3 separate draw calls).

[Cyberpunk 2077: Phantom Liberty](https://www.gog.com/en/game/cyberpunk_2077_phantom_liberty)

Sticking a mesh into another looks a bit ugly, though, as we can clear see where both geometries intersect. The Cyber-Artists of CDPR try to cover this up by placing a decal on top of both geometry, but the intersection is still quite visible:

[Cyberpunk 2077: Phantom Liberty](https://www.gog.com/en/game/cyberpunk_2077_phantom_liberty)

The magic happens now, when **another** layer of decals comes on top!

[Cyberpunk 2077: Phantom Liberty](https://www.gog.com/en/game/cyberpunk_2077_phantom_liberty)

Here are the textures for this decal, and I must admit: I love those stone structures, the sharpness and the cracks! 💘💘💘

The small grayscale texture is a height map for the wonderful [parallax occlusion mapping (POM)](https://youtu.be/jrJP__JRjEY?si=5MW48VG2EN5JiJN0), which adds all the depth to it. Here is a quick example with their texture but displayed in Unreal:

There is a weird behavior thought, and I’m not sure why it happens. Here you can clearly see how the depth of the POM changes depending on the distance so that parts of it get pushed downward?

[Cyberpunk 2077: Phantom Liberty](https://www.gog.com/en/game/cyberpunk_2077_phantom_liberty)

I did a test in Unreal, but I could not reproduce the issue. Maybe it’s related to my very low settings in the Cyberpunk game, because I only use a GTX 1080. What I can rule out: There is no tessellation happening, and increasing anisotropic filtering also doesn’t change anything.

Anyway, I love how these POM decals blend both geometries so perfectly into each other! I hope you like it as much as I do and if you have any idea what this odd behavior, let me know in the comments!

![](../../assets/ba0680151067ebbc.png)

[Oskar Świerad](https://bsky.app/profile/techartaid.com) gave us some info what the issue could be in his [reply on bluesky](https://bsky.app/profile/techartaid.com/post/3leujhcjbns2b):

“We made the number of steps dependent on the angle. What you see here is probably an artifact of that (or interpolation)”


The depth changing over the distance might be an optimization of the POM. The technique works by ray-marching the depth texture with a variable amount of steps and step size. I bet the step size is increased, and the step count reduced with distance for better performance.

Yes, I had the pleasure of getting a reply from one of the developers: “We made the number of steps dependent on the angle. What you see here is probably an artifact of that (or interpolation)”

Looks to me like they cancel the POM effect when the angle gets to extreme to avoid POM swimming effect.