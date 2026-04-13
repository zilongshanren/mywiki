---
title: Smart Screen-Space Blurring for Shadows
url: https://theinstructionlimit.com/smart-screen-space-blurring-for-shadows
author: Author Renaud Bédard
published: '2010-03-16'
source_blog: The Instruction Limit
source_site: https://theinstructionlimit.com
category: graphics
fetched: '2026-04-13'
---

I’ve been working on a screen-space solution for blurring shadows that has the following features :

- Variable-sized kernel based on surface distance and view angle
- Rejection of samples if they lie on a non-contiguous surface, by identifying depth and normal discontinuities
- Bilateral, two-pass blur filter to maximize the possible kernel size
- Vertex and pixel shader 3.0, so no worry about 64 instructions in the PS

…but also works with the following constraints, to simplify matters :

- Flat surfaces only, no curves! (to simplify the sample rejection process)
- Full control over the rendering pipeline, so the “main render” pass can output weird values in order to be properly blurred

I quickly realized that it’s very hard or impossible to do a variable-sized Gaussian filter in real-time. If you change the kernel size, you change the standard deviation, and you need to recalculate the weights… this is too heavy for a pixel shader. So I chose to use a box filter with uniformly-spaced samples.

I totally would’ve liked to use Poisson-Disk distribution, but it’s not doable in a two-pass bilateral scenario. And you can’t achieve big kernels in real-time without separating the process in two passes.

My XNA3 implementation currently uses no additional render targets (!) but just a “resolve texture”, and resolves from the main buffer quite a lot. A R32F (Single) render target is used for the shadowmapping process itself, but otherwise everything’s done with a A8R8G8B8 (Color) main buffer.

The shadowmapping solution is standard orthographic/directional depth testing, but I’m using Exponential Shadow Maps (ESM) to simplify the depth biasing problems. I could never get my hands on a really good way to do Slope-Scale Biasing for standard depth testing, so ESM saves the day here. Otherwise, there’s no fancy cascading, splitting or projection tricks.

Here’s how it looks at different distances. The blur kernel stays approximately the same size in world-space even if the whole process is screen-space!

![d0](../../assets/94b83e261ff346a6.png)

![d1](../../assets/0a83dc2f9ca75aad.png)


![d2](../../assets/6db2c9e73966f4b6.png)

![d3](../../assets/64ae18e2ea78a225.png)


I’ll keep working on a clean sample to show, and I’ll definitely release the HLSL code if I can’t release the source to the whole thing. Stay tuned!

Looks really cool… i look forward to seeing a demo/video/source.

Seconded!. Waiting for it too.

“I quickly realized that it’s very hard or impossible to do a variable-sized Gaussian filter in real-time.”

I think you can. Just reduce the Gaussian to the terms you need g(x)=e^-(dx*dx)

Use e^-((dX^2)/K). Where K=falloff term. This should reduce to

g(x) = exp( -((x1-x0)^2 * 1/K) );

WeightSum += g(x);

Scale your total by 1/WeightSum to renomalize. If you plot that function you’ll see you get a Gaussian curve with normalized weights just like before. No need for the other terms in the Gaussian Blur(PI,sqrt,etc); which are just a normalization factor anyway. Adding in bilateral term you just need to add another delta

g(x) = exp( -( dx^2 + dh^2) * 1/K));

dH might be you depth scaled to something. Remember you want to keep dH approx =0 for things you don’t want falloff for. Scale your heights to that range. Remember

dx*dx + dh*dh is just a dot product so you can calc them in one function.

The above code should be easy to run in a pixel shader and you can adjust K based on whatever you’d like. You can also adjust you tap radius as well since you can calc deltaX on the fly. Say scale your tap radius by depth; so you blur shadow in the depth less.

Hope you release the code. Like to see what you’ve come up with. I’m working on something similar

Thanks for sharing I learned a lot from your site, wikipedia and my bud LLCoolJay

Very impresive, could you please share the demo? Thanks!

I kinda forgot about it, sorry! I’m working on finishing it up now. One big downside is that it’ll be in XNA3.1 and I can’t install version 4 on my machine, but at least the shaders will be usable.

You should definitely release the HLSL! :D