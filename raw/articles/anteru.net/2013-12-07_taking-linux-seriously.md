---
title: Taking Linux seriously
url: https://anteru.net/blog/2013/taking-linux-seriously
published: '2013-12-07'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

During my last vacation, I did a small experiment at home: I installed Linux, copied all my stuff from Windows over that I use daily (e-mails, bookmarks, code, IM settings, etc.) and forced myself to use Linux for two weeks straight for everything. The last time I used Linux for a longer time was during my [assisted texture assignment project](https://anteru.net/blog/2009/09/14/604/) while I was at INRIA. Back then, the choice of using Linux was mostly a pragmatic solution to work around the fact that I had a hard time to get my hands on a recent Windows with a recent Visual Studio. This time however I’ve been evaluating Linux as a serious alternative to Windows. That is, I wanted to understand whether I can get work done on Linux (so I can develop productively at home on Linux) and whether Linux works fine for everyday usage.

Another reason to try switching completely is the fact that for a lot of computation tasks, I already use a Linux-based server machine at work, which outperforms my Windows-based desktop by ~30% (when I normalize for CPU count/speed.) Over the last weeks, I also spent a lot of time at work on my OpenGL back-end so I could test new graphics hardware features on Windows, bringing it up to feature parity with Direct3D. This would allow me to also properly evaluate the “work side”, assuming that OpenGL would work fine on Linux.

## Setting up

To ensure a fair comparison, I bought a new SSD and started the Linux experiment using Ubuntu 13.10. Installation went fine out-of-the-box and all my hardware was working right away, but I hit two annoying problems immediately:

- I could only change my audio volume using alsamixer, but not using the UI
- There was no way to set a per-monitor wallpaper with Unity

As I’m not too religious about my window manager, I simply switched to KDE which solves these problems. However, installing KDE over an existing Ubuntu installation leaves you with a monster with lots of packages that don’t make much sense, so I had to do a clean installation with KDE.

Once set up, the first thing that I noticed was that the default font rendering in KDE sucks. While Unity has a very nice anti-aliasing set up by default, KDE used some stupid defaults. Luckily, it’s easy to switch. By enabling sub-pixel anti-aliasing and setting the hinting mode to “slight” you basically get DirectWrite/OSX quality text in Linux as well.

Some minor issues with the default colour scheme and window decoration were fixed in no time. All that was left was to install the AMD binary drivers. The Ubuntu package management doesn’t provide beta drivers, so I had to do this manually. This works just fine, but there is one minor caveat: To get the drivers to install OpenCL, you must not run the installer, but instead use it to generate packages for your distribution and install all three of them.

## Developing

So let’s get started with developing. I use CMake everywhere, so the first step was to get and build CMake from source to get the latest version. That worked right away, including the Qt UI. For the IDE, I’m using Qt Creator as well as Sublime Text. Funnily, this is pretty similar to what I use on Windows; debugging and building in Visual Studio, but some typing does happen in Sublime Text. Here’s also where I hit the first major problem: On Ubuntu, debugging with Qt Creator does not work (the local variables window just remains empty), as the system gdb is linked with Python 3, but Qt Creator expects a “stock” gdb with Python 2. That’s easy enough to solve (get gdb, build from source) once you know it, but figuring this out took me a while as there is no error message at all that the system GDB is not compatible.

On the compiler side, I decided to go ahead and set up builds with both GCC and Clang. Ubuntu comes with recent versions, and as I was already building the code with GCC on Linux and Clang on Mac OS X, I was set up in no time. Build times are also better than on Windows, more so with Clang, which is roughly 30% faster than GCC in my testing.

Unfortunately, I quickly ran into another issue with debugging with GDB: Stepping into a dynamic library sometimes takes several minutes. LLDB doesn’t have this problem, so I hope that either GDB gets fixed or Qt Creator gets support for LLDB, as I do have to sometimes switch to LLDB just to get the debugging done.

Let’s move on the graphics and OpenCL part: I’m using an AMD HD 7970 card at home, so I was prepared for the worst, but surprisingly, all of my OpenGL stuff worked right away. That is, it worked as long as I was using only OpenGL, as I can’t get the OpenCL interop to work. I can create an interop context jus fine, but mapping a texture or a buffer produces an invalid memory object while returning `CL_SUCCESS`

at the same time. Unfortunately, I have similar trouble on Windows with AMD, OpenCL/OpenGL interop and the latest drivers, so I assume that something got broken in the 13.9/13.11 beta drivers. On Windows, the 13.4 drivers seem fine and the FirePro drivers are working as well.

![The voxel rasterizer from the niven research framework running Linux.](../../assets/0f4dbda7c39a8e77.png)

However, graphics on Linux is still no on par with Windows. Basically, the Linux OpenGL drivers didn’t get the love that the the Windows Direct3D drivers got. Performance is simply worse, and I also have problems with extreme frame time variance which I don’t have on Windows. That said, at least correctness seems fine, as all of my OpenGL code that works on Windows also works on Linux.

For profiling, I used the built-in Linux [perf](http://en.wikipedia.org/wiki/Perf_%28Linux%29) commands and Code XL, and both get the job done. In particular, setting up perf is a no-brainer, and you can get useful data from it very quickly. Not sure how good it’ll work to profile multi-threaded applications. Unfortunately, GPUPerfStudio2 doesn’t work on Linux; for graphics profiling and debugging I’m using [apitrace](http://apitrace.github.io) right now.

Development itself isn’t much different. One thing that is faster on Linux though is looking up the system API, as I’m much faster at typing `man 2 open`

than switching to my browser, typing in `CreateFile msdn`

, and waiting for the page to load.

## Gaming, entertainment, and other stuff

If it would be just for work, I’d be done here, but I’m using my machine at home for some occasional gaming, movie watching, photo work, office use and of course for browsing & e-mail. Let’s start with what doesn’t work: Gaming. While DOTA 2 runs on Linux, it runs slowly, it lags, audio stutters, and overall it’s just a bad experience. It’s worse than when I tried on Mac OS X. Nearly all games I have don’t support Linux at all. The notable exception besides DOTA was Metro: Last Light, which does work and looks just as good on Windows, but is completely unplayable, as it slows down to a crawl every few seconds.

Movie watching (using Lovefilm) works surprisingly well if you like inception: There’s a package which [installs a specially packaged Wine with Firefox in order to run Silverlight](https://launchpad.net/~ehoover/+archive/compholio/). Energy efficiency looks differently, but heck, it does work.

For photo retouching, [Lightroom](http://www.adobe.com/products/photoshop-lightroom.html) is still king, and Lightroom doesn’t work on Linux. No idea why an application written primarily in Lua is so difficult to port, but for the better or worse, I still have to boot Windows to develop my images. There are [Linux alternatives](http://www.darktable.org/), but they still lack the speed of Lightroom as well as its camera profiles. While [lensfun](http://lensfun.berlios.de/index.html) does support [an impressive list of lenses for distortion correction](http://lensfun.berlios.de/lenslist/), vignetting is basically left to the user. Sure, this is not so important when working on a single image, but if you’re bulk-correcting an import, these things do matter.

Everything else: It just works. There’s nothing I really miss from Windows. I’m actually surprised how little difference there is for “normal” use. If I wouldn’t do gaming and graphics development, all I would notice from switching to Linux is that the default fonts look different and that the start button has a different icon.

## The verdict

I’m** going to stick with Linux** at home and try to get the issues with OpenCL/OpenGL interop sorted out. Either AMD will fix them, or I’ll have to get an NVIDIA card again and check there, but I do believe that this is just a minor obstacle. For gaming I will still have to boot into Windows occasionally, but for everything else, Linux it is. The only downside is that I can’t go right ahead and port everything to use the latest C++ 11 features as I can’t kill of Windows support in my research framework, at least not until graphics performance is the same or better on Linux. Oh and before you ask, yes, this blog post was written 100% on Linux already :)