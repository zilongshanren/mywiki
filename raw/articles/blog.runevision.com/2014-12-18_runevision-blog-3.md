---
title: runevision blog
url: https://blog.runevision.com/2014_12_18_archive.html
published: '2014-12-18'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

The development of my exploration game The Cluster, that I'm creating in my spare time, marches ever onwards, and 2014 saw some nice improvements to it.

Let's have a look back in the form of embedded tweets from throughout the year with added explanations.

### Worlds and world structure

During the end of 2013 I had implemented the concept of huge worlds in the game, and I spent a good part of 2014 beginning to add more structure and purpose to these worlds.

Each world is divided into regions with pathways connecting artefacts, connections to neighbor regions, and the region hub. I used a minimum spanning tree algorithm to find a nice way to determine nicely balanced connections, and tweaking the weights used for the connections to change the overall feel of the structure is always fun.

### New name

In the early 2D iteration of my game, it was called [ Cavex](http://runevision.com/multimedia/cavex/), because it had caves and weird spelling was the thing to do to make names unique. Then since 2010 I used the code name

*EaS*after the still undisclosed names of the protagonists, E. and S. This year I decided to name the game

*The Cluster*as a reference to the place where the game takes place.

### Spherical atmosphere

The game takes place on large (though not planet-sized) floating worlds. Skyboxes with fixed sky gradients don't fit well with this, but finding a good alternative is tricky. I finally managed to produce shaders that create the effect of spherical fog (and atmosphere is like very thin fog), which elegantly solved the problem.

The atmosphere now looks correct (meaning nice, not physically correct) both when inside and when moving outside of it. The shader was a combination of existing work from the community and some extensive tweaks and changes by myself. [I've posted my spherical fog shader here.](http://forum.unity3d.com/threads/spherical-fog-shader-shared-project.269771/)

### Integrating large world structures with terrain

The game world in The Cluster is consists of a large grid of areas, though you wouldn't be able to tell where the cell borders are because it's completely seamless. Still, the background hills used to be controlled by each area individually based solely on whether each of the four corners where inside or outside of the ground. I changed this to be more tightly integrated with the overall shape of the world and some large-scale noise functions.

The new overall shapes of the hills have greater variety and also fit the shape of the world better.

I also re-enabled features of the terrain I had implemented years ago but which had gotten lost in some refactoring at some point. Namely, I have perturbation functions that take a regular smooth noise function and makes it more blocky. I prefer this embracing of block shapes over the smooth but pixelated look of e.g. Minecraft.

### Tubes

As part of creating more structure in the regions, I realized the need to reduce boring backtracking after having reached a remote goal. I implemented tubes that can quickly transport the player back. I may use them for other purposes too. Unlike tubes (pipes) in Mario, these tubes are 100% connected in-world, so are not just magic teleports in tube form.

### What's next?

It's not a secret that most aspects of The Cluster gameplay are only loosely defined despite all good advise of making sure to "find the fun" as early as possible. Being able to ignore sound advice is one of the benefits of a spare time project!

However, after the ground work for fleshing out the structure of the world regions this year, I've gotten some more concrete ideas for how the core of the game is going to function. I won't reveal more here, but stay tuned!