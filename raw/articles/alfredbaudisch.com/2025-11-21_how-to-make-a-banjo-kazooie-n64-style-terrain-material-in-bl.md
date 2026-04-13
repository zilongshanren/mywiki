---
title: How to make a Banjo Kazooie (N64) style terrain material in Blender (blended
  textures with vertex colors)
url: https://alfredbaudisch.com/experiment-logs/how-to-make-a-banjo-kazooie-n64-style-terrain-material-in-blender-blended-textures-with-vertex-colors/
published: '2025-11-21'
source_blog: Alfred Reinold Baudisch
source_site: https://alfredbaudisch.com
category: game programming
fetched: '2026-04-13'
---

In the first part, [you can see how Banjo-Kazooie from the Nintendo 64 presented its rich environments](https://alfredbaudisch.com/experiment-logs/banjo-kazooie-n64-environments-and-levels-texture-blending-and-vertex-color-usage/), making heavy usage of vertex colors for details, lights and ambient occlusion, and texture blending with vertex color alpha. In this article, let's try to recreate the same style in Blender using the same techniques.

## Initial Material Setup

In Blender, in order to blend two textures using the vertex color alpha, add a "Color Attribute" node and connect it into the "Factor" socket of a "Mix" node. Connect the main texture into "B" and the secondary texture into "A":

If you haven't painted any vertex color information yet, you are going to see the main texture (connected to the "Mix" node "B" socket) covering the whole surface of the mesh:

## How to paint Vertex Color Alpha in Blender?

In Vertex Paint mode, press A to select all vertices, choose the color white and then go to "Paint – Set Vertex Colors" to fill all vertices as white.

Then go to the Brush's blending mode settings and choose either Erase Alpha or Add Alpha, and this is how you can affect the vertex color alpha in Blender.

In our case, if you Erase Alpha, it will cause the surface to blend with texture 2:

After erasing the vertex color alpha from some vertices, you can see texture 2 blending with texture 1, just like [how it happens in Banjo-Kazooie](https://alfredbaudisch.com/experiment-logs/banjo-kazooie-n64-environments-and-levels-texture-blending-and-vertex-color-usage/):

If you want to set selected vertices to specific alpha values, there's a [free add-on for that](https://alfredbaudisch.com/experiment-logs/vertex-alpha-tools-blender-add-on-useful-when-making-n64-and-ps1-graphics/).

## How to visualize Vertex Color Alpha in Blender?

You can use my [free Blender add-on Vertex Alpha Tools](https://alfredbaudisch.com/experiment-logs/vertex-alpha-tools-blender-add-on-useful-when-making-n64-and-ps1-graphics/).

![](../../assets/ae844094b38d61d2.jpeg)


![](../../assets/ae844094b38d61d2.jpeg)

If you don't want to use add-ons, you can connect the Alpha socket of the Color Attribute node onto the Base Color socket:

![](../../assets/10d36e7ef36789dc.png)


![](../../assets/5e51679a6059f1bb.png)


## How to display Vertex Colors alongside texture blending with Vertex Color Alpha?

Can connect the Color Attribute node Color socket onto a Multiply node, and multiply it with the result of the existing Mix node. The result of the Multiply node is the final Base Color:

![](../../assets/3807fd3ee4531ca6.png)


After painting some vertices and adjusting the vertex alpha of others, this is how it looks with the texture blending and the vertex colors, you can see texture 2 blending with texture 1, as well the colors:

## Tips

- In Edit Mode, select all vertices, press "U", then "Reset" to reset the UV on top of the texture.
- Be sure to check the first part:
[Banjo-Kazooie (N64) environments and levels: texture blending and vertex color usage](https://alfredbaudisch.com/experiment-logs/banjo-kazooie-n64-environments-and-levels-texture-blending-and-vertex-color-usage/)