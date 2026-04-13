---
title: 'Bytesize Gamedev #1 - Easy Outlines in Shader Graph'
url: https://danielilett.com/2021-06-09-bytesize-1-easy-outlines/
author: Daniel Ilett
published: '2021-06-09'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

There are a lot of approaches you can take to make outlines for 3D objects in Unity. Today, we’re going to explore a time-tested, super easy approach for outlines, translated to Shader Graph!

Bytesize Gamedev is a series of shorter game development tutorials.

Hang out with me and other shader enthusiasts over on [Discord](https://danielilett.com/(https:/discord.gg/tPQEUwPpb3)) and share what you’re working on!

# Easy Outlines

We’ll start by creating a new graph by right-clicking in the Project View and selecting *Create -> Shader -> Universal Render Pipeline -> Unlit Shader Graph* (or *Create -> Shader -> Unlit Graph* on older Unity versions).

![We want an unlit shader because the outline should have a block colour. Create Shader.](../../assets/eb07e73376e4cc52.jpg)

*We want an unlit shader because the outline should have a block colour.*

We can set the output colour to black. Or, you could make this into a property if you want.

![The outline will just be a single colour. Black Main Color.](../../assets/7e690d4af1aa062c.jpg)

*The outline will just be a single colour.*

Then we need to enable double-sided rendering. On older Unity versions, we use the drop-down cog menu on the master node. On newer versions, we just choose the Graph Settings. Either way, tick the “Two Sided” box.

![There's two sides to every story. Two Sided Rendering.](../../assets/ece71ede02209612.jpg)

*There’s two sides to every story.*

Now we’ll disable front-facing triangles so that only back-faces are visible. Add an `Is Front Face`

node, then pass it into the **Predicate** input on a `Branch`

node - the **True** and **False** inputs are 0 and 1 respectively. That gets passed into the **Alpha** field on the Master node, and the **Alpha Clip Threshold** is set to 0.5.

![Pixels with alpha below Alpha Clip Threshold are deleted. Remove Front Faces.](/img/bytesize/part1-remove-front.jpg)

*Pixels with alpha below Alpha Clip Threshold are deleted.*

Now we’ll extend the shape of the mesh along its surface normals. Start by adding an `Outline Thickness`

property - it’s a `Float`

/`Vector1`

.

We’ll take a `Normal Vector`

node - in **Object** space - and `Normalize`

it, so its length is 1. We can `Multiply`

by `Outline Thickness`

, then we’ll `Add`

all this to a `Position`

node in **Object** space. This gives us a new position for the vertex, which gets output to the **Vertex Position** pin on the Master.

![This is normally the easiest way to add outlines. Extend Vertex Normals.](../../assets/211bd6934d21883f.jpg)

*This is normally the easiest way to add outlines.*

Attach a material using this shader to an object - as well as another material using your usual shader for the object - and here’s the result:

![Pikachu looks so happy to be highlighted like this! Completed Material.](../../assets/08cf8be2005fb0f9.jpg)

*Pikachu looks so happy to be highlighted like this!*

Thanks for reading Bytesize Gamedev, where I bring you short game development tips in an easy to digest format!