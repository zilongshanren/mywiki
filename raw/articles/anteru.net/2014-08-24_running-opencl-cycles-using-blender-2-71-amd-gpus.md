---
title: Running OpenCL Cycles using Blender 2.71 & AMD GPUs
url: https://anteru.net/blog/2014/running-opencl-cycles-using-blender-2-71-amd-gpus
published: '2014-08-24'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

If you are using Blender on AMD, you probably have noticed that Cycles doesn’t support AMD GPUs. However, for some scenes, Cycles is actually working just fine and might be worth a try. Here’s a quick how to guide.

First of all, if you are on Linux, make sure you have the AMD proprietary driver installed. You can grab it from the AMD homepage. Next, you need to set up an environment variable in order to make Cycles “see” the AMD OpenCL device. On Windows, you can open a command window (Shift-Right-Click on your Blender installation folder and use “Open command promp here…”), then type in:

set CYCLES_OPENCL_TEST=all
.\blender.exe

On Linux, you can use:

CYCLES_OPENCL_TEST=all ./blender

After Blender has started, you now have to pick your compute device. Under “User preferences”, “System”, you can find the “Compute device” option. For AMD, pick your GPU code name as the device. The code name for R290 and R9 290X is “Hawaii”, for R9 280, R9 280X, HD 7950 and HD 7970 “Tahiti”. Other codenames are “Pitcairn” and “Bonaire”; these are the GCN based cards – I doubt Cycles will run correctly on older cards.

Anyway, once set up, if everything works right, you’ll get GPU accelerated Cycles!