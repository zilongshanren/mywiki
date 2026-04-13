---
title: 'GM Shaders: Voxels 2'
url: https://mini.gmshaders.com/p/voxels2
author: Xor
published: '2024-08-25'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Voxels 2

### Creating editable voxel maps with 2D textures

Hi everyone!

Previously, I wrote about voxel raytracing using the “DDA” algorithm:

Today, we’re going to continue from there and get into actually implementing this in a game engine. So far, we can render blocks however we need, but we have no way of interacting with them and our map is generated on the fly. If we wanted a more complex scene, the formula could get big and expensive. We need a way of pre-generating our map so that we don’t have to every frame, and so we can edit it during runtime. Let’s start by generating a map.

This tutorial comes with a [full GameMaker demo](https://github.com/XorDev/GM_Voxels).

# Map Storage

We need an efficient way to pass lots of voxel map data to the GPU. Since I’m using GameMaker for this demo, so we don’t yet have access to Shader Storage Buffer Objects or 3D textures, but we have a backup plan: Every engine has 2D textures!

If you’re implementing this in an engine that supports 3D textures, you can skip this step, but for the rest of us, let’s look at 3D Look-Up-Tables:

For our purposes, LUTs are just textures used to store data in a structured way. In a regular 2D texture, you read from a specific x and y coordinate, and you get the RGBA values back. This could work for a simple height map where at any give x and y coordinate, you get the terrain height and material data (using different color channels). For some purposes, this would be fine, but here we want to be able to have caves and to be able to stack different materials on top of each other and for that we need to add “z” layers to our texture.

The easiest way is to put all the layers on one texture, with each layer side by side. So if we have a 64x64x64 world, we could use a texture that is 64*64x64 (or 4096x64).

Then, when we need to read the texture, we add the z-layer coordinate times 64 to the x coordinate. The biggest texture we can do is 16k, which means we would only be able to go as large as 256 pixel wide cells with 64 layers unless we stack layers in the y-axis too.

You can see in the LUT above, we have 8x8 cells of 64x64 pixels. To read the z layers, you start from the top-left and go right, row by row, like reading a book. Notice the blue channel becomes brighter as you go down. We can do the same for our 3D world, and this allows us to support much larger map/chunk sizes (theoretically up to 1024x1024x256 by using splitting 16 layers vertically and horizontally). This can actually be thought of as a 4D data structure because it requires 4 resolution values (cell width, cell height, horizontal cell count, vertical cell count).

Here are the functions I’ve written to go from UV coordinates (0 to 1) to 3D voxel coordinates and back :

```
vec3 uv_to_block(vec2 uv)
{
//Convert uv coordinates to pixel coordinates
vec2 p = floor(uv * RES.xy * RES.zw);
//Get the subcell x and y coordinates
vec2 xy = mod(p, RES.xy);
//Compute cell coordinates
vec2 zw = mod((p-xy) / RES.xy, RES.zw);
//Calculate the z value from xy cell position
float z = dot(zw, vec2(1, RES.z));
return vec3(xy,z);
}
vec2 block_to_uv(vec3 b)
{
//Clamp the z to the map height range
b.z = clamp(b.z, 0.0, RES.z * RES.w-1.0);
//Compute subcell coordinates
vec2 sub_cell = fract(b.xy / RES.xy) / RES.zw;
//Compute cell coordinates
vec2 cell = fract(floor(b.z / vec2(1,RES.z)) / RES.zw);
return sub_cell + cell;
}
```