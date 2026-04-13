---
title: Tools of the trade
url: https://interplayoflight.wordpress.com/2013/01/12/tools-of-the-trade/
author: Kostas Anagnostou
published: '2013-01-12'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

A large part of a graphics programmer’s work revolves around the tools that allow her to create, edit and customise shaders, which in turn define the look of a 3D environment.

Over the years I’ve used many different tools ranging from a simple text editor and a command line compiler to a fully fledged shader graph editor with drag and drop functionality. Which tools will actually be used for a graphics project depends a lot on personal preference, development platform and/or ease (and cost) of development.

For experimentation on new graphics techniques I use whatever seems reasonable each time, and depends on how simple or involved what I plan to develop is. I used to be a great fan of XNA game studio for example, due to its content pipeline as well as ease of use. Regrettably, it hasn’t been updated since Direct3D 9 and Microsoft does not seem so keen to upgrade it any more. Still, there are other C# based frameworks that support D3D11 nowadays (for a comparison check [this post](http://www.popekim.com/2013/01/goodbye-xna-hello-sharpdx.html)) which I didn’t have the chance to try yet.

To quickly write a shader to try a graphics effect or lighting model etc, I often use [FX Composer](https://developer.nvidia.com/fx-composer). It is a great tool although unfortunately it only supports up to D3D10 and not 11. nVidia is apparently not supporting it any longer. [RenderMonkey](http://developer.amd.com/resources/archive/archived-tools/gpu-tools-archive/rendermonkey-toolsuite/), a similar tool created by AMD/ATI, is no longer supported as well but is still useful.

In cases where I want to develop something more involved, that requires the use of a rendering engine, I resort to the open source [Hieroglyph](http://hieroglyph3.codeplex.com/) engine. It is a thin layer over D3D11 and supports forward and deferred rendering as well. I don’t know of that many open source D3D11 engines, I used to develop my own for D3D9, but I still haven’t found the time to upgrade it to the latest graphics API.

Complementary to the graphics development tools and equally important are the graphics debugging/profiling tools. Again which one to use depends on the platform, the availability and cost. Personally, one of the best debugging tools I’ve ever used is PIX for Xbox/Xbox360. PIX for Windows does not even come close, but it still is useful. nVidia’s [Parallel NSight](https://developer.nvidia.com/nvidia-nsight-visual-studio-edition) is possibly the closest to Pix for XBox you can find on Windows and its integration with Visual Studio is very useful. It even supports shader debugging although you will need a separate slave machine for that. AMD provides [ ](http://developer.amd.com/tools/graphics-development/gpu-perfstudio-2/)[GPU PerfStudio](http://developer.amd.com/tools/graphics-development/gpu-perfstudio-2/) but I haven’t evaluated it extensively. [Intel’s GPA](http://software.intel.com/en-us/vcsource/tools/intel-gpa) is quite useful as well for Intel and non-Intel GPUs, although it does not support shader debugging. Finally Microsoft has added a graphics debugger/profiler to the professional edition of Visual Studio 2012, which I haven’t tried yet.

In cases we don’t have any available tool, we also have the option for manual debugging and performance profiling, and in some cases it is easier to get results faster with it, but this is too large a topic to discuss here.

I mentioned Direct3D mainly in this post, but most of the above tools support both D3D and the OpenGL API. Which one to use for graphics programming does not matter that much in my opinion (at least nowadays), and it depends mainly on the development platform. What matters though is the version of the API to use, as later APIs such as Direct3D11 and OpenGL 4.0+ offer a wealth of new functionality such as tessellation, geometry and compute shaders, as well as different and more flexible ways to read from and write data to the GPU which makes a whole new class of graphics techniques possible.

A final note on the development platform, most of the above tools support PC/Windows, which I believe is the most suitable environment for general graphics development/experimentation/learning. If you develop for a more “closed” platform you will have to use the APIs and tools provided by the manufacturer, be it Microsoft, Sony, Nintendo, Apple etc. Quite often, especially for the current generation of consoles and on mobile, these APIs are not as fully featured as on PC.

These are some of the tools one can use to develop and experiment on graphics techniques. If you think I have missed anything important please add it to the comments.