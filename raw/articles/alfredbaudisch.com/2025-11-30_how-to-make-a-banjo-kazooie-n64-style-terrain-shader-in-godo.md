---
title: How to make a Banjo Kazooie (N64) style terrain shader in Godot (blended textures
  with vertex colors)
url: https://alfredbaudisch.com/experiment-logs/banjo-kazooie-n64-terrain-in-godot/
published: '2025-11-30'
source_blog: Alfred Reinold Baudisch
source_site: https://alfredbaudisch.com
category: game programming
fetched: '2026-04-13'
---

In this article, I explain how I created a Banjo-Kazooie (Nintendo 64) terrain and level material in Godot, with a Visual Shader, importing the [terrain created in Blender](https://alfredbaudisch.com/experiment-logs/how-to-make-a-banjo-kazooie-n64-style-terrain-material-in-blender-blended-textures-with-vertex-colors/), that makes use of two texture channels and blends them using the vertex color alpha and vertex colors for details and fake lighting and ambient occlusion.

## Prerequisites

Create [the level or terrain in Blender first](https://alfredbaudisch.com/experiment-logs/how-to-make-a-banjo-kazooie-n64-style-terrain-material-in-blender-blended-textures-with-vertex-colors/), blending textures with vertex color alpha and optionally painting vertex colors.

### gLTF Export Setup

In Blender, export the mesh to gLTF to be able to import it into Godot. Make sure "Use Vertex Color: Active" is set (in Data, Mesh, Vertex Colors):

![Blender gLTF export settings showing 'Use Vertex Color: Active' option](../../assets/646e563eab395f14.png)

Why not simply import the `.blend`

file directly into Godot? Because I didn't find a way for it to correctly import the vertex colors.

## Godot Visual Shader

It's a pretty simple shader that mixes two textures, where the mix weight comes from the vertex color alpha. Then the shader multiplies the final color with the vertex colors:

![](../../assets/e59b016d36ea098e.png)


I also disabled specularity:

![](../../assets/1e169dae177c67ab.png)