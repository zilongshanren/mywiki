---
title: Rendepth is Now Feature Complete
url: https://cybereality.com/rendepth-is-now-feature-complete/
author: Cybereality
published: '2025-01-14'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

Pretty sure I actually finished Rendepth, my new 3D media player and 2D-to-3D conversion app. For sure there are tons of features still on the table, but it feels feature complete and stable enough for a launch. The (somewhat long) video above demonstrates most of what’s working. At the moment I’m working on cross-platform stuff and packaging it up. Technically it’s working, but the setup for the dependencies is complex and I need to make this simple to use if you don’t have a Master’s in Computer Science.

Last two days I was working on getting the ML libraries working on the new Intel Arc B580 GPU. It’s sort of working, but performance is not quite stable. One of the issues I ran into was this error, specifically with using the DepthAnything V2 library and PyTorch with the Intel Arc:

Input type (torch.FloatTensor) and weight type (XPUFloatType) should be the same

This happens once you change the selected device according to Intel documentation to use “xpu” (rather than “cuda” or whatever). The line I have looks like this, which works on Nvidia, AMD, Intel (and possibly Apple, need to test that, or falls back to the CPU).

DEVICE = 'cuda' if torch.cuda.is_available() else "xpu" if torch.xpu.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'

This is correct, I believe, but the issue is that the DepthAnything library has similar code inside that predates the new Intel support (as of 2 months ago). If you get the error, you can just use the above version (it’s in the function that moves the image to the tensor). Other than that, it appears to work fine on Intel, just need to do more research on the performance.

Last week I also worked on the graphic design for the website. I did hire a designer for the logo, and I’m using an off-the-shelf WordPress theme, but I customized a lot of the palette design and layout, choice of images, etc. Below is a look at one of the pages. The site itself is mostly functional, just need to fill out some copy in a few places, but it’s pretty close.

![](../../assets/9c74c13d8f1c620a.png)

I also tweaked the “Free View” 3D export for Rendepth to use a 2×2 grid (parallel on top, cross-eye on the bottom). I’d previously experimented with a sort-of obscure 3 view format (left-right-left) but it turns out this is formatted poorly on social media sites, and is almost impossible to view on mobile due to the ultra-widescreen aspect ratio. Below is the newly fixed format.

![](../../assets/c5b8ae132520aa83.jpg)

Other than that, I’ll just be finishing the Windows/Mac ports, and doing more testing and QA with different hardware. I purchased an Nvidia RTX 4060 and an AMD RX 7600, which I’ll be using as the minimum requirements. The app will still work in CPU mode on probably anything that can run a modern API (e.g. DirectX 12 or Vulkan) but will be fairly slow. In my testing so far, if you don’t have an adequate graphics card for the ML stuff, it could take up to 3 seconds for 1 image, while with the GPU acceleration it’s only around 300ms. So a factor of about 10x. After I test more devices, I can see if there is any way to optimize this (for example, running in standard definition in CPU mode) or simply expect users of a software like this own good machines. All in all, I expect probably at least 3 weeks more of development, or likely a bit more, before I’m ready to launch publicly. Stay tuned.