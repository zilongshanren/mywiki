---
title: Graphics Programming weekly - Issue 31 — March 18, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-31/
author: Jendrik Illner
published: '2018-03-18'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

This week I am at GDC, therefore there will be no newsletter at the end of the week. If you would like to meet during the week, send me an email or message me on twitter. DMs are open.

The series will return on April 2nd.

- dynamically loads vulkan entry points, bypassing the vulkan loader for increased calling performance

[Good Vulkan Binding](https://timothylottes.github.io/20180316.html) [[wayback-archive]](https://web.archive.org/web/20180319143646/https://timothylottes.github.io/20180316.html)

- suggests using dynamic SSBO on AMD
- on NVidia: data smaller then 64 KiB use UBO, otherwise SSBO
- then alias use binding aliasing to access as different types

[A Look Inside Farpoint’s Rendering Techniques for VR](https://www.impulsegear.com/a-look-inside-farpoints-rendering-techniques-for-vr) [[wayback-archive]](https://web.archive.org/web/20180319143709/https://www.impulsegear.com/a-look-inside-farpoints-rendering-techniques-for-vr)

- MSAA didn’t give the image quality required
- used oculus UE4 renderer with dynamic resolution to enable super sampling when possible
- occlusion query is done using a merged depth buffer from the left and right eye
- applies a mip bias based on the distance to the center of the screen
- experiment with world space cone tracing

[Performance Profiling](https://medium.com/@jcowles/performance-profiling-d5f44b4b6f33) [[wayback-archive]](http://web.archive.org/web/20180319120354/https://medium.com/@jcowles/performance-profiling-d5f44b4b6f33)

- what to optimize for, selecting appropriate metrics
- tips on how to make tests reproduceable
- considerations for data recording to validate assumptions
- what data to record and how to present the results

[Vulkan Subgroup Tutorial](https://www.khronos.org/blog/vulkan-subgroup-tutorial) [[wayback-archive]](https://web.archive.org/web/20180319144416/https://www.khronos.org/blog/vulkan-subgroup-tutorial)

- what subgroups are
- how to use subgroup operations efficiently
- examples of use-cases

- screen space indirect lighting technique
- based on the ideas of horizon based ambient occlusion (HBAO)
- discussion of improvements to HBAO
- how to integrate it into a rendering pipeline

[ A dive into the making of Immersion ](http://www.ctrl-alt-test.fr/?p=463) [[wayback-archive]](http://web.archive.org/web/20180319131928/http://www.ctrl-alt-test.fr/?p=463)

- water reflection ( planar reflection with blur )
- volumetric lighting
- algithmn description including light absorption

- vegetation and particles

[valley of gods - water](http://blog.camposanto.com/post/171934927979/hi-im-matt-wilde-an-old-man-from-the-north-of) [[wayback-archive]](http://web.archive.org/web/20180317211428/http://blog.camposanto.com/post/171934927979/hi-im-matt-wilde-an-old-man-from-the-north-of)

- GPU based shallow water simulation
- signed distance field for collision with the geometry
- breakdown of the different visual components

[ Estimated Cost of Per Atom Function in Real-time Shaders on the GPU ](http://blog.ruofeidu.com/estimated-cost-per-atom-function-real-time-shaders-gpu/) [[wayback-archive]](https://web.archive.org/web/20180319143954/http://blog.ruofeidu.com/estimated-cost-per-atom-function-real-time-shaders-gpu/)

- gives rough estimates of how expensive GPU instructions are relative to each other

[Unreal Engine 4.19 Released!](https://www.unrealengine.com/en-US/blog/unreal-engine-4-19-released) [[wayback-archive]](https://web.archive.org/web/20180319143610/https://www.unrealengine.com/en-US/blog/unreal-engine-4-19-released)

- new temporal up sampling method
- dynamic resolution
- all lights use physically based units
- terrain LOD selection is now screen size based instead of distance based

[The High Definition Render Pipeline: Focused on visual quality](https://blogs.unity3d.com/2018/03/16/the-high-definition-render-pipeline-focused-on-visual-quality/) [[wayback-archive]](https://web.archive.org/web/20180319144158/https://blogs.unity3d.com/2018/03/16/the-high-definition-render-pipeline-focused-on-visual-quality/)

- unified lighting across all render passes (deferred, forward, ….)
- build for high end PCs and consoles
- new area lights, sun based on physical units
- overview of new BRDF
- decals on opaque and transparent objects
- many new debug features
- volume based system for scene settings such as sky, shadows, …