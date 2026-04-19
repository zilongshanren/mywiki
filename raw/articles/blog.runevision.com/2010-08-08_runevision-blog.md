---
title: runevision blog
url: https://blog.runevision.com/2010_08_08_archive.html
published: '2010-08-08'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

*This post is about The Cluster, my 2.5D platform game under development with focus on non-linear exploration, set in a big, continuous world. You can read all the posts about The Cluster here.*

I'm taking a break from [pathfinding and AI](http://blog.runevision.com/2010/07/eas-agile-enemies-in-platform-game.html) to go back and talk about the raw level design in The Cluster; More specifically the procedural generation.

The entire world in The Cluster is procedurally generated at runtime, though it is consistent, meaning that the world will be the same every time you play. However, this is strictly a design choice, not a technical limitation, and I'm considering including some kind of bonus areas or similar that will be different every time.

To give you an idea of the current state of the game, here is a simple playable demo (requires Unity plug-in):

Controls: **Arrows** to run, **Ctrl** to jump.

This demo is just a "tech demo" and features no enemies and no way to win. It extends infinitely to the right.

Back in 2007 I [explained the procedural level generation](http://runevision.com/multimedia/cavex/#307) of the game. The game has changed a lot since then - among other things it has turned from a tile based 2D game into a 2.5D game with 3D graphics - but the basic method of generation is still the same.

You can actually see the maze map in-game in the demo above by pressing **2**. Press **1** to hide the world to only see the map. You can zoom a bit out by pressing **Z**, **X** zooms back in, and you can pan around using **WASD**. Press **Esc** to reset the camera.

![](../../assets/2d3f8af1d3cdbecf.png)

A map of the maze that the area is based on.

![](../../assets/a2a90504498e1c58.png)

The map overlayed onto the actual generated area.

![](../../assets/c475f10d5fc9e3d0.png)

The generated area by itself.

One feature not explained in depth on the page linked to above is the placement of locked doors and keys in the game. The game places locked doors and keys in a "perfect way" such that it is always necessary to find all keys and unlock all doors to be able to proceed, and a "deadlock" will never occur, where the key for a door is placed behind that door. The placements are calculated using a simple algorithm I came up with which is based on dividing the area up into a binary tree and then placing keys in leaf nodes and locks in inner nodes in a specific way. Several years after implementing it, I found [this article about "Environment Tree"](http://www.squidi.net/three/entry.php?id=4) at [Squidi.net](http://www.squidi.net/). It's basically the same algorithm, so rather than explaining it myself here, I'll refer to that.

A nice aspect about the algorithm is that it supports placing keys both *sequentially* and *nested*. In the screenshots above, the red door is sequential in the sense that all the following keys and doors are on the far side of the red door, so once you've gone through it, you don't have to go back. The green door, however, is nested. You go through the green door, pick up the blue key, and then go back out the green door in order to proceed. The algorithm doesn't have separate handling of sequential versus nested key and door placements; these are just emergent properties so to speak.

If there's any interest I can cover other aspects of the procedural generation in The Cluster in coming blog posts.