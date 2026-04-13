---
title: Graphics Programming weekly - Issue 30 — March 11, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-30/
author: Jendrik Illner
published: '2018-03-11'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

[Porting GPU driven occlusion culling to bgfx](https://interplayoflight.wordpress.com/2018/03/05/porting-gpu-driven-occlusion-culling-to-bgfx/) [[wayback-archive]](https://web.archive.org/web/20180312003030/https://interplayoflight.wordpress.com/2018/03/05/porting-gpu-driven-occlusion-culling-to-bgfx/)

- breakdown of how a gpu driven pipeline can be implemented with bgfx
- indirect buffer writing from the CPU not supported so using regular instancing instead

[Breaking down barriers – part 1: what’s a barrier?](https://mynameismjp.wordpress.com/2018/03/06/breaking-down-barriers-part-1-whats-a-barrier/) [[wayback-archive]](https://web.archive.org/web/20180312003104/https://mynameismjp.wordpress.com/2018/03/06/breaking-down-barriers-part-1-whats-a-barrier/)

- look at different meaning of barriers
- on GPUs it includes synchronization, cache management, decompression
- description of how it works on the hardware level

[Hair in In the Valley of Gods](http://blog.camposanto.com/post/171638832704/zora-is-one-of-the-two-main-characters-in-our) [[wayback-archive]](https://web.archive.org/web/20180312102025/http://blog.camposanto.com/post/171638832704/zora-is-one-of-the-two-main-characters-in-our)

- how the stylized hair from Zora is being created
- based on hair cards
- for the trailer the hair was rigged and animated

[Using the GitHub dxcompiler.dll](https://blogs.msdn.microsoft.com/marcelolr/2018/03/06/using-the-github-dxcompiler-dll/) [[wayback-archive]](https://web.archive.org/web/20180312003125/https://blogs.msdn.microsoft.com/marcelolr/2018/03/06/using-the-github-dxcompiler-dll/)

- when using custom dxcompiler.dll to build shaders they will be unsigned
- can only be used when windows developer mode is active and d3d12 experimental mode is enabled
- when the official dxil.dll can be loaded by the compiler the shader will be signed

[Khronos Group Releases Vulkan 1.1](https://www.khronos.org/news/press/khronos-group-releases-vulkan-1-1) [[wayback-archive]](http://web.archive.org/web/20180310010501/https://www.khronos.org/news/press/khronos-group-releases-vulkan-1-1)

- Subgroup Operations: operations that allow communications between parallel gpu work
- extension integrated into 1.1 core specification
- multi-gpu support, cross-api sharing, 16-bit data types, hlsl memory data layout

[Importance Sampling techniques for GGX with Smith Masking-Shadowing: Part 1](https://schuttejoe.github.io/post/ggximportancesamplingpart1/) [[wayback-archive]](https://web.archive.org/web/20180312003155/https://schuttejoe.github.io/post/ggximportancesamplingpart1/)

- mathematical derivation of importance sampling using the CDF (Cumulative Distribution Function)
- including source code

[Importance Sampling techniques for GGX with Smith Masking-Shadowing: Part 2](https://schuttejoe.github.io/post/ggximportancesamplingpart2/) [[wayback-archive]](https://web.archive.org/web/20180312003207/https://schuttejoe.github.io/post/ggximportancesamplingpart2/)

- description of the flaws of solution from part 1
- explanation of a better importance sampling using the distribution of visible normals
- source code included

[Don’t Convert sRGB U8 to Linear U8!](https://blog.demofox.org/2018/03/10/dont-convert-srgb-u8-to-linear-u8/) [[wayback-archive]](https://web.archive.org/web/20180312003224/https://blog.demofox.org/2018/03/10/dont-convert-srgb-u8-to-linear-u8/)

- visualizing loss of precision between storing color data in 8 bits per channel using linear vs sRGB encoding
- difference in lerp behaviour between sRGB and linear color space

[Codegen for fast Vulkan](https://anteru.net/blog/2018/codegen-for-fast-vulkan/) [[wayback-archive]](https://web.archive.org/web/20180312003238/https://anteru.net/blog/2018/codegen-for-fast-vulkan/)

- for better calling performance it’s recommended to query the entry points directly instead of going through the vulkan loader
- article shows how to parse the vulkan xml specification with python to automate the generation of the loading code