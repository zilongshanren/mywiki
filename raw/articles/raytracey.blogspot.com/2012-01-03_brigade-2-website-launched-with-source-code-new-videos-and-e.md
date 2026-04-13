---
title: Brigade 2 website launched with source code + new videos and exe's
url: http://raytracey.blogspot.com/2012/01/brigade-2-website-launched-with-source.html
author: Sam Lapere
published: '2012-01-03'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Great news today: the website for the Brigade 2 path tracer has been launched and includes the source code so anyone can make their own real-time path traced game. The path tracing kernels are still closed source and precompiled in a library.

I have also developed two small demos showing real-time path traced interior scenes with animation. The first one is a simple study room like scene, in which the ceiling and back walls are removed to let more light enter the scene (there is a problem with the normals from the chair):

The second one is a more complex bedroom scene (180k triangles). The scene is a free 3ds max model from

[http://www.3dmodelfree.com](http://www.3dmodelfree.com/), which was tweaked a little bit (I took out the ceiling, two walls and the curtains). The scene came without textures, so I had to set every material manually in the mtl file. Some screens:
Diffuse(.1,.1,.1) and spec(.9) for bedframe and closet:

Two videos showing real-time material tweaking and animation with physics:

The executable demo can be downloaded at

(all CUDA architectures supported)

Expect many more demos made with the Brigade 2 path tracer in the coming weeks and months. Brigade is also going to be ported to OpenCL soon. 2012 is going to be a breakthrough year for real-time GPGPU path tracing.

## 3 comments:

Something is really odd about the shading of the materials, let's see what it looks like with Lambertian Matte Material.

True, it's a problem with normals, which is most apparent on glossy surfaces.

Somewhere along the export/import process of obj models from Max to Maya/Blender and into Brigade, the normals get screwed up. I will have to take a closer look at this. I think I am not loading the models in Brigade correctly. Should be easy to solve.

I found out what the problem was: turning off "smooth groups" in 3dsmax when exporting the obj solved the normals issue. The shading looks right now.

Post a Comment