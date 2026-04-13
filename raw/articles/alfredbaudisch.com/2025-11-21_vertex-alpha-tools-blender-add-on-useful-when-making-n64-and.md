---
title: 'Vertex Alpha Tools: Blender add-on useful when making N64 and PS1 graphics'
url: https://alfredbaudisch.com/experiment-logs/vertex-alpha-tools-blender-add-on-useful-when-making-n64-and-ps1-graphics/
published: '2025-11-21'
source_blog: Alfred Reinold Baudisch
source_site: https://alfredbaudisch.com
category: game programming
fetched: '2026-04-13'
---

I have [previously shown how to make Banjo-Kazooie](https://alfredbaudisch.com/experiment-logs/how-to-make-a-banjo-kazooie-n64-style-terrain-material-in-blender-blended-textures-with-vertex-colors/) (from the Nintendo 64) stylized terrain and environments with vertex colors and vertex color alpha.

But, there are a few annoyances and small roadblocks in that workflow:

- Painting the vertex color alpha to specific values can be difficult.
- It's very hard to replicate the same vertex color alpha value in different parts of the mesh (for example, in case you want to equally blend another texture in various sections of the mesh).
- It's cumbersome to visualize the vertex alpha itself.
- There's no way to know the exact value of the vertex alpha from a specific vertex.

To solve issue number 2 I found the free "[VertexAlphaSetter](https://github.com/Desayuno64/VertexAlphaSetter)" Blender add-on by [Desayuno64](https://github.com/Desayuno64/). This add-on lets you set specific alpha values to selected vertices.

But then I still had all the other 3 issues pending. For that, I created my own solution, "Vertex Alpha Tools" (free, [available on Github)](https://github.com/alfredbaudisch/VertexAlphaTools), with the following features:

![](../../assets/a1dc44dacf18ef6c.png)


- Toggle vertex color alpha as a material overlay.
- Visualize the specific vertex alpha values as 3D labels on top of each vertex.
- And I unified the original "VertexAlphaSetter" add-on onto my add-on.

![](../../assets/c6f46d29c8d99a8c.jpeg)


![](../../assets/c6f46d29c8d99a8c.jpeg)

![](../../assets/ae844094b38d61d2.jpeg)


![](../../assets/ae844094b38d61d2.jpeg)

This is useful when making both PlayStation 1 (PS1) and Nintendo 64 (N64) stylized graphics with Blender.