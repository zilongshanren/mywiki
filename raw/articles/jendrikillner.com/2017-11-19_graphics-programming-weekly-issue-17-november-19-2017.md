---
title: Graphics Programming weekly - Issue 17 — November 19, 2017
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-17/
author: Jendrik Illner
published: '2017-11-19'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

[Last Week on DirectX Shader Compiler (2017-11-14)](https://blogs.msdn.microsoft.com/marcelolr/2017/11/14/last-week-on-directx-shader-compiler-2017-11-14/) [[wayback-archive]](https://web.archive.org/web/20171114212438/https://blogs.msdn.microsoft.com/marcelolr/2017/11/14/last-week-on-directx-shader-compiler-2017-11-14/)

- support for explicitly sized types 16 to 64 bits
- spir-v improvements

- Improved performance of occlusion ray packets by up to 50%

[Experiments in GPU-based occlusion culling](https://interplayoflight.wordpress.com/2017/11/15/experiments-in-gpu-based-occlusion-culling/) [[wayback-archive]](https://web.archive.org/web/20171118150728/https://interplayoflight.wordpress.com/2017/11/15/experiments-in-gpu-based-occlusion-culling/)

- An GPU occlusion system that does not require mayor changes to existing D3D11 based engines
- render occluders to depth buffer
- mip chain generation
- world transform + aabb (axis aligned bounding box) in structured buffer
- if visible write the transform to an AppendBuffer
- DrawIndexedInstancedIndirect for drawing the models
- index count is pre-filled by the CPU when creating the buffer
- only the number of instances needs to be atomically incremented on the GPU

- expand to support multiple mesh types culling in one pass
- remove use of AppendBuffer
- removing invisible instances with parallel prefix scan for stream compaction


[Updated Crunch texture compression library](https://blogs.unity3d.com/2017/11/15/updated-crunch-texture-compression-library/) [[wayback-archive]](https://web.archive.org/web/20171120023303/https://blogs.unity3d.com/2017/11/15/updated-crunch-texture-compression-library/)

- compress DXT textures up to 2.5 times faster
- latest github version up to 5x faster

- 10% better compression ratio
- added support for ETC_RGB4 and ETC2_RGBA8
- commits have very detailed commit messages to follow the progress along
[github](https://github.com/Unity-Technologies/crunch/commits/unity?after=c1d8e8da7145c90198d3035344dadc474fd176b3+34)

[Mud and Water of Spintires: MudRunner](https://www.gamasutra.com/blogs/PavelZagrebelnyy/20171116/309626/Mud_and_Water_of_SpintiresMudRunner.php) [[wayback-archive]](http://web.archive.org/web/20171116120223/https://www.gamasutra.com/blogs/PavelZagrebelnyy/20171116/309626/Mud_and_Water_of_SpintiresMudRunner.php)

- visual aspects driven via textures
- dynamically updated through rendering of particles into textures

- projection of meshes
- heavy use of decals

- mud system
- mud displacement
- wheel tracks
- mud particles

- water system
- water simulation
- geometric water waves


[Biome Painter: Populating Massive Worlds](https://www.gamasutra.com/blogs/KrzysztofNarkowicz/20171116/309724/) [[wayback-archive]](https://web.archive.org/web/20171117004625/https://www.gamasutra.com/blogs/KrzysztofNarkowicz/20171116/309724/)

generate terrain textures and entity placement from the same system

- biome type and lushness in color maps

spawns entities on pre-calculated spawn points

- entities spawned at runtime
- following rules based on terrain information

Biome LOD

- based on distance spawn only larger objects
- small object just close to the player

splines are used for roads/rivers

- automatically adjusts the maps to adjust for it

biome blockers

- simple shapes that reduce or remove biomes where placed


[Technology Sneak Peek: Python in Unreal Engine](https://www.unrealengine.com/en-US/blog/technology-sneak-peek-python-in-unreal-engine) [[wayback-archive]](https://web.archive.org/web/20171120023559/https://www.unrealengine.com/en-US/blog/technology-sneak-peek-python-in-unreal-engine)

- automated non destructive workflow processing
- replace materials/combine models/ remove detailts etc…
- can be python or visual scripting (blueprint)

[Gpufit: An open-source toolkit for GPU-accelerated curve fitting](https://www.nature.com/articles/s41598-017-15313-9) [[wayback-archive]](https://web.archive.org/web/20171120023718/https://www.nature.com/articles/s41598-017-15313-9)

- GPU-accelerated , open-source library for curve fitting
- using the Levenberg-Marquardt algorithm