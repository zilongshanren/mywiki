---
title: My wish list for 2014
url: https://anteru.net/blog/2013/my-wish-list-for-2014
published: '2013-12-30'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

I’m sometimes a hopeless optimist, especially when it comes to hardware and software releases. But sometimes, [I wish for something like a Javascript based, declarative UI in 2008](https://anteru.net/blog/2008/10/20/298/), and [it becomes reality in 2010](https://en.wikipedia.org/wiki/Qt_Quick), so let’s try again for this year ;)

## AMD driver fixes

AMD’s Direct3D & OpenGL driver works just as expected, but sadly, everything else could use some love. For example:

- OpenGL/OpenCL interop is broken
*since several months*on Windows and Linux. - Using Direct3D, I get a “hitch” every 3-4 seconds in a few applications (the hitch is a frame which takes nearly 1 second; AMD is aware of the issue and told me it’s a driver bug … months ago.)
- On Windows, my machine still “looses” a DisplayPort-connected screen occasionally when waking up from stand-by.
- On Linux, after enabling a tear-free desktop, I get
*machine lock-ups*during booting when I don’t switch fast enough to a text console. - Power usage is still high when two or three different monitors are hooked up.
- The latest Linux driver
*refuses to install*due to a missing patch in the kernel module.

I assume that the AMD driver team is busy working on the PS4, XBox One and Mantle, but I do hope once they get those things shipped, they will go back and fix all the small things which make the difference between having a working driver and a good driver. I also hope that AMD gets up some proper continuous integration solution to avoid regressions like breaking OpenCL/OpenGL interop or releasing drivers which don’t install. This kind of things seems to be something that you can completely avoid with automation. NVIDIA did this investment quite some time ago (see this [blog post about their Moscow-based testing team](http://blogs.nvidia.com/blog/2012/03/06/nvidia-moscow-a-gamers-destination/))

**Wish for 2014**: AMD moves focus back to their Linux/Windows drivers.

## Micro-server CPUs

For a home-server, a AMD’s 4-core Opteron X2150 or the 4-core Avaton Atoms is the perfect CPU. With ECC support and low-power usage, it allows you to build a real home-server which can work as a NAS and DNLA server. Unfortunately, even though AMD [announced the X2150 in May 2013](http://www.amd.com/us/products/server/processors/2100seriesplatform/Pages/x2150seriesprocessors.aspx), as of December, there is still *not a single board available* in retail with it. In the meantime, AMD stopped shipping low-power Athlons with ECC support. Intel is a bit faster, but currently, there is only one 4-core Atom board available in Europe. I know of a few people waiting to build their own home-server who don’t want a closed NAS-black-box, and we’re all twiddling our thumbs while we wait for AMD and Intel to ship their stuff.

**Wish for 2014**: AMD and Intel ship affordable micro-server CPUs in retail!

## Widespread OpenCL 1.2 and SPIR support

OpenCL 1.2 provides a few nice additions over 1.1, in particular: * SPIR, allowing you to pre-compile kernels * Easier image creation, both for interop and in normal API usage * Buffer & image filling without having to run a kernel

SPIR is the biggest and most important addition which is enabled by OpenCL 1.2. Strictly speaking, you could do SPIR and OpenCL 1.1, but the official SPIR specification is written against OpenCL 1.2. With SPIR, it becomes easier to ship large OpenCL applications, as we no longer have to pay with long start-up times on the client. It also becomes possible to compile other languages down to SPIR. Finally, SPIR frees us from problems with compilers; it’s not uncommon that one driver version chokes on a particular kernel. With SPIR, we can compile once in advance and rest assured that it’ll work on all clients supporting SPIR, as loading SPIR has a lower chance to fail load than compiling OpenCL C. There’s not much you can do wrong when starting from SPIR :)

The other two changes are nice API improvements. In particular, buffer & image filling is something which can be implemented extremely efficiently in the driver but emulation is tricky (for example, instead of zeroing out a buffer, the driver can simply give you “fresh” memory.)

The only vendor not implementing OpenCL 1.2 is NVIDIA. Even though implementing the OpenCL 1.2 API is a rather small task, I have doubts that NVIDIA will do it unless Adobe or Autodesk will require it. On the SPIR side, things are looking even worse. As far as I know, only Intel ships SPIR support.

**Wish for 2014**: AMD ships SPIR, NVIDIA updates to OpenCL 1.2 & SPIR.

## 24”, 4k monitors

High-resolution displays are great, not because you can suddenly run games at insane resolutions, but because font rendering improves dramatically. Everyone who has a mobile phone knows how good fonts look on really high-resolution screens. While anti-aliasing can help, higher resolution is the “correct” solution. You can try for yourself if you have an Retina Mac Book Pro – just turn off font anti-aliasing, and what happens? You still get gorgeous looking text. As a programmer, reading and writing text is my daily job. Unfortunately, while mobile and to some degree notebooks went to 150 dpi and beyond, we’re stuck with at most 2560x1600 on 27” in the desktop market with a pretty embarrassing 110 dpi or so.

Just recently however, [Dell announced a 24”, 3840x2160](http://www.dell.com/learn/us/en/uscorp1/secure/2013-12-2-dell-ultrasharp-ultra-hd-monitors) screen, and I can’t really wait for them to appear in retail. The reason why I’m very interested in a 4k screen is cause I believe it’s going to close to being good enough that further improvements won’t matter. While I can clearly see the difference between 100 and 200 dpi text, 200 and 400 is much harder to spot, and anything beyond is probably no longer useful. What this means is that once we get 8k 24” screens, we’ll be practically done unless we get better eyes :)

**Wish for 2014**: EIZO ships an affordable 4k, 24” screen.