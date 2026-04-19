---
title: runevision blog
url: https://blog.runevision.com/2013_09_22_archive.html
published: '2013-09-22'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

One of the problems you'll face when creating an infinite procedurally generated world is that your procedural algorithm is not completely context-free: For example, some block might need to know about neighboring blocks.

![](../../assets/79b677d4fcae98a1.jpg)

To use graphics processing as an example, you might have an initial noise function which is completely context-free, but very often an interesting procedural generation algorithm will also involve a blur filter, or something else where the local result depends on the neighboring data. But since you only have a part of the world loaded/generated at a time, what do you do at the boundaries of the loaded area? The neighboring pixels or data isn't available there since it isn't loaded/generated yet. The layer-based approach I describe in this post and video is a way to address this issue.

I hinted at this layer-based approach in the overview post [Technologies in my Procedural Game The Cluster](http://blog.runevision.com/2013/02/technologies-in-my-procedural-game-eas.html). I have also written a post [Rolling Grids for Infinite Worlds](http://blog.runevision.com/2013/05/rolling-grids-for-infinite-worlds.html) with the source code for the RollingGrid class I use for achieving practically infinite grids; only bounded by the Int32 min and max values.

I use two different layer-based approaches in The Cluster: *Encapsulated layers* and *internal layers*.

*Encapsulated layers* are the most flexible and what I've been using the most. Encapsulated layers can depend on other encapsulated layers, but don't know about their implementation details, and different encapsulated layers can use completely different sizes for the chunks that are loaded. I might go more in details with this some other time.

Recently I implemented the simpler *internal layers*. Internal layers are tightly coupled. They share the same grid, but chunks in the grid can be loaded up to different layer levels. I explain this in more detail in this video below.

That's it for now. You can read [all the posts about The Cluster here](http://blog.runevision.com/search/label/TheCluster).

### 2024 update: LayerProcGen framework released

I've now released a framework called [LayerProcGen](https://github.com/runevision/LayerProcGen) as open source which implements the layer-based procedural generation techniques discussed here.