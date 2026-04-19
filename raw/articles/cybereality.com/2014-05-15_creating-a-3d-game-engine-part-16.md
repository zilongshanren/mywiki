---
title: Creating a 3D Game Engine (Part 16)
url: https://cybereality.com/creating-a-3d-game-engine-part-16/
author: Cybereality
published: '2014-05-15'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

After some more testing, it looks like OGRE is not the savior it seemed like yesterday. While the static geometry boosted frame-rates greatly, it’s only useful for, well, static objects. Meaning the models can’t move or animate. I did find another option, instancing, which initially looked promising. It allows rendering of large amounts of identical objects faster than just having them be individual. Sounds good.

The implementation seemed complex at first, but then I found the InstanceManager which simplified things a whole lot. However, after getting it working, I wasn’t as impressed with the performance. Just rendering the same 13k still cubes I was getting a little over 100 fps. Then when adding rotation animation to the cubes, the speed dropped down to around 33 fps. Certainly this is still better than the naive implementation, however still nowhere close to where I want.

To be completely upfront, my computer is not a power-house. I’m still running a Core 2 Duo @ 3GHz and GTX 470’s in SLI. Getting a little old, I know, but still can play modern games like Titanfall or whatever. Maybe I’m expecting too much, don’t know at this point. I think I will just go back to development on my engine and worry about performance optimization later. Even so, this was still an interesting investigation at least.