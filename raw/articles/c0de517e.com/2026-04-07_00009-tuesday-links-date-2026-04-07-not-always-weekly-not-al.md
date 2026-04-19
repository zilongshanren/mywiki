---
title: '00009: Tuesday links!Date:2026-04-07. Not always weekly. Not always on Tuesday.'
url: https://c0de517e.com/LINKS/00009.htm
author: Angelo Pesce
published: '2026-04-07'
source_blog: 'c0de517e''s weblore: Main Entrance.'
source_site: https://c0de517e.com/
category: graphics
fetched: '2026-04-19'
---

Legend:

‼️ = Must read!

🧐 = Interesting, curio.

**Real-Time Rendering.**
-

[Vulkanized 2026.](https://vulkan.org/user/pages/09.events/vulkanised-2026/1445-John-Talley-Samsung.pptx.pdf)
Some interesting stuff - main link is a presentation about the correlation of index/vertex buffer layout and (black box) BVH performance in RTRT APIs. But there are quite a few other interesting ones, for example: https://vulkan.org/user/pages/09.events/vulkanised-2026/0900-Reiner-Dolp-KIT.pdf on autotuning (which is a topic I'm always interested in) and https://vulkan.org/user/pages/09.events/vulkanised-2026/1415-Lucas-Silva-DevshGraphicsProgramming.pptx.pdf on GPU driven rendering on mobile.

-

[Zenteon Reshade SSGI.](https://github.com/Zenteon/ZenteonFX)
ReShade seems to be a fun framework to do little graphic experiments. This guy has a collection of shaders, and a youtube channel where they explain the development - e.g. https://www.youtube.com/watch?v=dmdyqzelBIY

-

[TexelSplatting "pixel" art.](https://dylanebert.com/texel-splatting/)
Cue old man yelling at the clouds. Pixel art is about pixels! Like people who say "dithering" when they mean "stippling" - here the "pixel art" is really a sort of high-resolution voxel thing. But still, it's cute. And our GPUs are way too powerful :)

**'AI' - Machine learning, deep or not.**
-

[PowerInfer. 🧐](https://github.com/Tiiny-AI/PowerInfer)
Made by people who are selling a "personal" HW accelerator for AI (which I don't find yet too compelling - things are moving too fast IMHO to invest in personal HW) - it's an inference runtime that claims some quite compelling speedups. There is likely a ton more to uncover in terms of inference optimization.

-

[Depth Anything 3. ‼️](https://depth-anything-3.github.io/)
Pretty impressive transformed-based video 2 depth (or GS etc) pipeline. Has sourcecode, ComfyUI plugins etc etc. Very cool. See also: https://rollingdepth.github.io/ (Marigold)

-

[A theory of creativity in diffusion models.](https://arxiv.org/pdf/2412.20292)
Work in interpreting what deep models do is always fascinating to me. In the end the findings of this paper are perhaps not surprising - but having them formulated as an analytic theory is interesting.

**Retrocomputing (might contain emulation).**
-

[Tie Fighter totalconversion.](https://sites.google.com/view/tie-fighter-total-conversion/)
One of the best games ever!

-

[Voodoo graphics re-created in FPGA.](https://github.com/fayalalebrun/SpinalVoodoo)
Unfortunately - not (yet?) something that can be plugged in MisterFPGA ao486 etc (in fact, IIRC the ao486 core is already at the limits of what that FPGA can fit).

-

[More PC emulators.](https://github.com/electricbolt/XT)
As I'm building something of my own... Found a few interesting projects on Vogons. The one above aims to run PC dos commands "natively" in a terminal. Of course, it only supports commandline dos stuff, by intercepting some DOS interrupts - e.g. no direct writes to the screen, not even in textmode... Some other cute stuff: https://github.com/petr-to/pico-286-waveshare/ https://github.com/adriancable/8086tiny https://github.com/hchunhui/tiny386 https://bitbucket.org/superfury/unipcemu

-

[Back to PET demo.](https://www.youtube.com/watch?v=IXoZoogMsXA)
Cute demo (not new) - the video is about how to hack it to loop.

-

[How I Built an Open-World Engine for the N64. 🧐](https://www.youtube.com/watch?v=lXxmIw9axWw)
Quite fun! Seems that the N64 can be a decent platform for retro development today - not as arcane as the ps1/ps2, but still very quirky and limited.

-

[Adventures in reverse-eng. a 16bit dos game.](https://cybersmash.github.io/night-raid/)
Ghidra can still decompile 16 bit dos, in fact, there are also plugins to work together with dosbox. FWIW - Ghidra is a java application, you can run it "portably" by downloading a compatible version of OpenJDK portable (you need the jdk, not just the runtime) and then pointing the JAVA_HOME env var to it before starting Ghidra.

-

[Shimming DOS with C#. 🧐](https://github.com/OpenRakis/Cryogenic)
"The game is fully playable with sound and music through hybrid ASM/.NET execution." Crazy, reminds me of how (fast) Windows games emulation on Android works - replace, when you can, emulated calls with native ad-hoc code. Leverages Spice86 - A PC emulator for real mode reverse engineering.

-

[How emm386 extended DOS life.](https://www.os2museum.com/wp/the-importance-of-emm386/)
Again, recently due to... things I'm playing with, I had the re-learn some stuff - specifically around emm386. This article is a fascinating tidbit of history, all stuff I did not know/realize back when I was actually a kid using these things...

**Miscellanea.**
-

[Win9x styled website.](https://leikareipa.github.io)
Just cool.

-

[Hacking the Xbox One. 🧐](https://www.youtube.com/watch?v=FTFn4UZsA5U)
I can barely understand any of this - but fascinating nonetheless.

-

[Handy system tools.](https://systeminformer.sourceforge.io/)
I probably should add a #tools tag to my links system and then I can search these tags to update my https://c0de517e.com/016_tools_that_I_use.htm page... Note to self! See also https://apphousekitchen.com/aldente-overview/ AlDente battery optimizer for Macs - I hate though that the non-free version is a subscription :/