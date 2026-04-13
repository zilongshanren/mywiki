---
title: Graphics Programming weekly - Issue 14 — October 29, 2017
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-14/
author: Jendrik Illner
published: '2017-10-29'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

[OpenCl -> Vulkan: A Porting Guide](http://www.duskborn.com/wp-content/uploads/2015/03/OpenCL-to-Vulkan-A-Porting-Guide.pdf) [[wayback-archive]](https://web.archive.org/web/20171030125257/http://www.duskborn.com/wp-content/uploads/2015/03/OpenCL-to-Vulkan-A-Porting-Guide.pdf)

- why?
- better cross-platforms support
- more frequent driver updates
- more tools
- less driver overhead, up to 3x less

- shows differences between the APIs
[clspv](https://github.com/google/clspv)a tool to compile openCL shaders to SPIRV

[Bringing Galaxy on Fire 3 to Vulkan: Stats & Summary](https://www.gamasutra.com/blogs/JohannesKuhlmann/20171023/308101/Bringing_Galaxy_on_Fire_3_to_Vulkan_Stats__Summary.php) [[wayback-archive]](http://web.archive.org/web/20171024235621/https://www.gamasutra.com/blogs/JohannesKuhlmann/20171023/308101/Bringing_Galaxy_on_Fire_3_to_Vulkan_Stats__Summary.php)

- vulkan, 40% more code
- between 2.7x to 4x faster then OpenGL ES across devices (CPU performance)

[NanoGL : a crafted WebGL(2) microframework](https://m.makemepulse.com/nanogl-a-crafted-webgl-2-microframework-39837889f6a4) [[wayback-archive]](https://web.archive.org/web/20171026183150/https://m.makemepulse.com/nanogl-a-crafted-webgl-2-microframework-39837889f6a4?gi=2adb2e42d0c0)

- light-weight helpers wrapping the WebGL2 API
- separate modules
- Draco compressed models
- GPU textures + high MIP streaming
- LOD system
- PBR
- Post effects

- nice videos showing the features

[How Unreal Renders a Frame](https://interplayoflight.wordpress.com/2017/10/25/how-unreal-renders-a-frame/amp/) [[wayback-archive]](https://web.archive.org/web/20171026183459/https://interplayoflight.wordpress.com/2017/10/25/how-unreal-renders-a-frame/amp/)

- breakdown and high-level look at how UE4 rendering works
- small explanations about how each stages works and some implementation details

[High-Performance GPU Computing in the Julia Programming Language](https://devblogs.nvidia.com/parallelforall/gpu-computing-julia-programming-language/) [[wayback-archive]](http://web.archive.org/web/20171027160029/https://devblogs.nvidia.com/parallelforall/gpu-computing-julia-programming-language/)

- work-in-progress support
- same high-level language on CPU and GPU (some limitation)
- written inline with CPU code

[Transmuting White Noise To Blue, Red, Green, Purple](https://blog.demofox.org/2017/10/25/transmuting-white-noise-to-blue-red-green-purple/amp/) [[wayback-archive]](https://web.archive.org/web/20171026182513/https://blog.demofox.org/2017/10/25/transmuting-white-noise-to-blue-red-green-purple/amp/)

- how to turn white noise into different kinds of noise
- done by filtering white noise to only include the desired frequencies

[The Gauss-Seidel and Jacobi Methods for Solving Linear Systems](https://erkaman.github.io/posts/jacobi_and_gauss_seidel.html) [[wayback-archive]](https://web.archive.org/web/20171030124639/https://erkaman.github.io/posts/jacobi_and_gauss_seidel.html)

- explanation of the Jacobi Method and Gauss-Seidel method, both are very similar
- but Gauss-Seidel converges a lot quicker

- 12-bit, full-frame wavelet compression video codec
- constant quality, bit-rates will vary as needed
- decoder, encoder, test applicatiom open source

[sRGB versus Linear Colour Space](http://thelittleengineerthatcould.blogspot.ca/2017/10/srgb-versus-linear-colour-space.html?m=1) [[wayback-archive]](https://web.archive.org/web/20171027170258/http://thelittleengineerthatcould.blogspot.ca/2017/10/srgb-versus-linear-colour-space.html?m=1)

- sRGB backbuffer handling in SDL / OpenGl

[sRGB Colour Space - Part Deux](http://thelittleengineerthatcould.blogspot.ca/2017/10/srgb-colour-space-part-deux.html?m=1) [[wayback-archive]](https://web.archive.org/web/20171027170743/http://thelittleengineerthatcould.blogspot.ca/2017/10/srgb-colour-space-part-deux.html?m=1)

- how to use hardware sRGB -> linear conversion with OpenGL for textures