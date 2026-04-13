---
title: Games | Shaders | Tutorials
url: https://danielilett.com/page2/
author: Daniel Ilett
published: '2024-04-10'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

[
](https://danielilett.com/2024-04-10-tut7-10-terastal-effect/)

Pokémon's Terastallize Effect in Shader Graph

![Pokémon's Terastallize Effect in Shader Graph](../../assets/34a9c7867ecc978a.jpg)

Turn any mesh into dazzling crystal by triangulating the mesh and using random vectors for lighting calculations.

Turn any mesh into dazzling crystal by triangulating the mesh and using random vectors for lighting calculations.

Distort the view behind a mesh with the Scene Color node and tint it green for an easy Metal Gear-style stealth camo effect. It was my destiny to be here... in this article!

With physically based rendering (PBR), we describe the physical properties of a surface, such as albedo color, normals, smoothness, metallic, and light emission.

Along with coloring pixels, we can modify the vertices of a mesh in-shader to create wave displacement effects, amongst other things.

Godot is the hottest scrappy little game engine on the block these days, so I decided to create a handful of shaders to test it out.

To render an image properly, Unity writes extra information to the depth buffer. We can read that data to make a silhouette effect.

Transparent objects are drawn after opaque objects in a back-to-front order, and alpha clipping can remove pixels based on alpha (transparency) values.

We use textures to apply base color information to the surface of an object, which requires texture coordinates (UVs) to map the texture onto the mesh.

Shader Graph is Unity's node-based editor for making shaders - small programs that modify the appearance of objects.

Voronoi noise patterns look like random organic cells. This custom Voronoi code makes it easier to find cell edges to make a rocky lava surface.

With Renderer Features, we can create an efficient two-pass Gaussian blur with configurable kernel size.

This quick-fire article will blast through ten effects, from inverted hull outlines and silhouettes to vertex displacement waves and 2D swirling vortices.

Modern stealth games feature x-ray vision, which helps to track hidden enemies and other points of interest. Render Objects helps us to draw objects through walls.

With the Fullscreen Shader Graph type, we can draw outlines by finding changes in color across nearby pixels.

Holograms help make your game feel more futuristic, like this flexible and feature-packed reactive shield effect.