---
title: ImagePeeker.
url: https://c0de517e.com/020_imgpeek.htm
author: Angelo Pesce
published: '2025-03-27'
source_blog: 'c0de517e''s weblore: Main Entrance.'
source_site: https://c0de517e.com/
category: graphics
fetched: '2026-04-19'
---

An

[old tool](https://c0de517e.blogspot.com/2013/05/peeknpoke.html) of mine that I recently brushed up and updated. The idea here is to "peek" process memory, continously, and interpret/display it as a 2d image.

The usage is simple: you put a breakpoint somewhere in the app you want to debug, take the pointer address of the image you're interested in, and pass it to imgpeek along with the app process name.

![](../../assets/b7b3a6fec16b5c0c.png)

The tool supports a large number of pixel formats, including HDR, it can deswizzle 4x4 block-swizzled images, do basic channel operations, easily launch multiple instances and do image comparisons.

I love to work visually, and over the years I've developed a bunch of little tools to "spy" on running applications, to efficiently write out traces/logs, and to re-import them back.

Some examples from my old blog:

[datavis 101](https://c0de517e.blogspot.com/2014/06/stuff-that-every-programmer-should-know.html),

[datalog](https://c0de517e.blogspot.com/2017/11/datalog.html),

[nvgprint](https://c0de517e.blogspot.com/2019/03/gdc-2019-everyday-shallow-ml.html) (similar to

[this](https://www.billbaxter.com/projects/imdebug/), but better),

[GPU printf](https://c0de517e.blogspot.com/2013/07/dx11-gpu-printf.html) (directX 11, but the concept obviously can be ported anywhere).

I use everything, from python to js, Mathematica, processing, ctoy/tcc and a lot of different little engines and frameworks I've built over the years. And still to this day I'm upset that we have not seen this idea, that visualization and program tracing is key, materialize in better native debuggers.

Yes, there are some extensions for specific in-memory data visualization, for example

[this one for VisualStudio seems neat](https://github.com/awulkiew/graphical-debugging), but they are all limited, they over-rely on things like "natvis" and/or

[specific formats](https://marketplace.visualstudio.com/items?itemName=VisualCPPTeam.ImageWatchForVisualStudio2022) that they expect the data to be in, and nothing (to my knowledge) explores the problem of dynamic visualization/program tracing, outside academic experiments (mostly done in managed/VM languages) or

[abandoned](https://www.gnu.org/software/ddd/) [prototypes](https://github.com/meeloo/xspray).

There are even

[conferences on software visualization](https://vissoft.io/), and yet for the poor C/C++ programmer, the debugging experience never

**fundamentally** changed in the past couple of decades.

Anyhow! Here is the code, I hope it can be useful to you. It's a single C# file, it's trivial to create a project to build it:

[imgpeek.cs](020_imgpeek/imgpeek.cs).

P.S. Making tiny, crappy tools like this, is IMHO a superpower (just don't fall in love with them beyond their utility for the job at hand, remember, it's about saving time now, not creating a tool...). You can get in a few lines of code more "power" than "real", productized tools, just by riding the good part of the 80/20 split, writing stuff from scratch, not having to care about legacy codebases and integration and all the problems that make software engineering hard. For production code that would be obnoxious cowboy coding and a borderline fireable offense, but for your own tooling... YOLO! Vibecode that!