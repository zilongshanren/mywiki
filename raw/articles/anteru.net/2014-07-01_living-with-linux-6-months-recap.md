---
title: Living with Linux - 6 months recap
url: https://anteru.net/blog/2014/living-with-linux-6-months-recap
published: '2014-07-01'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Time flies by – just [a moment ago I switched to Linux](https://anteru.net/blog/2013/taking-linux-seriously) for development, and suddenly half a year has passed. Time to look back!

## Status

I’m running Linux now at work and at home as the primary OS, that is, if I don’t do anything, I end up in Linux, all my e-mails are on Linux, my instant messaging, etc.

At home, Windows is only left for three things: Gaming, photos, and some development. At work, I only boot Windows if I need to run some OpenCL/graphics interop. The vast majority of the time, I’m working on Linux these days.

The Linux I use is Ubuntu 14.04, or to be more specific, the [Kubuntu](http://www.kubuntu.org/) flavour. Let’s take a look at what works and what doesn’t!

### The good

- Graphics driver work better than expected. I’ve followed all beta, intermediate, hot-fix and other releases from AMD from the last few months, and I didn’t brick my machine once. The drivers have gotten also a lot more stable, initially, I couldn’t even boot into the KDE desktop without manual intervention. Today, you can leave an OpenGL application running all weekend long and even remove a monitor and everything will still run. Notice that I was running brand-new hardware on a really recent distribution which was not officially supported. This also improved, for Ubuntu 14.04, AMD had nearly day one support.
[Clang](http://clang.llvm.org/)and[GCC](http://gcc.gnu.org)are seriously faster than Visual Studio. I had to move the build onto a SSD for Visual Studio to get comparable speed to Clang & GCC. Still, running just my unit tests is near instantaneous on Linux, while on Windows, it’s a few seconds just to do a “null” build.- Even though I’m primarily working on Linux now, I don’t break the Visual Studio build too often. On the other hand, working on Visual Studio only, I regularly checked in things which would break the Linux build.
- Accessing a Windows-based network using
[autofs](http://www.autofs.org/),[Samba](http://www.samba.org/)& Co. works reliably. I’ve copied hundreds of gigabytes in a single session from disk to network and back, without so much as a hiccup. Things just work, even if everyone else around you is using Windows. - Performance of most of my tools is a lot better on Linux. I’m not sure whether it’s the compiler or the kernel scheduler, but recently, I’ve been even benchmarking an OpenGL graphics application on Linux because it was simply running faster.
- Installing tools is so much easier it’s no longer funny. Everything you need is in the package manager, and if not, compiling from source is typically trivial.
- Connecting remotely into your machine is so much easier if you end up at a console instead of having to play the RDP game. I also tried remote
[PowerShell](http://en.wikipedia.org/wiki/Windows_PowerShell)for some time, but it’s a far cry from the ease of use of ssh. - Alt+Click for window dragging, how can you live without it?

### The bad

- Debugging with
[Qt Creator](http://en.wikipedia.org/wiki/Qt_Creator)is by far not as comfortable as with Visual Studio. For some reason or another, my code crashes gdb when compiled without any optimization whatsoever, with`-Og`

it works, but the debugging experience is not as good as it should be. The debugger is also way slower than Visual Studio. - Debugging again, I miss the
[Visual Studio visualizers](http://msdn.microsoft.com/en-us/library/zayyhzts.aspx). I did write a few visualizers for Qt Creator, but they[are really painful to write](http://plohrmann.blogspot.de/2013/10/writing-debug-visualizers-for-gdb.html),[don’t integrate well](http://richg42.blogspot.de/2013/10/qtcreators-python-debug-visualizers.html), and debugging them is way harder than with Visual Studio 2013. - I can’t get
[subpixel positioning](http://www.antigrain.com/research/font_rasterization/)to work in Firefox (or anywhere else, for that matter.) While I have proper anti-aliasing, every glyph is rendered exactly the same and the kerning is a bit off. On Windows, I simply force Firefox to use[DirectWrite](http://en.wikipedia.org/wiki/DirectWrite)anti-aliasing for all font sizes and I’m done, but on Linux? Help! Anyone? - I have funny performance problems with scrolling in text editors.
[Sublime Text](http://www.sublimetext.com/)is especially guilty here. Scrolling with a few frames per second is really annoying. - V-Sync on the desktop is broken. I never managed to get my window manager to be V-synced but applications not. I.e. what I want is tear-free dragging of windows, but I want rendering in a window to run as fast as possible. It’s okay if it blits to the window manager ever so often and I only see the sync frames. On Windows, this seems to work without issues, on Linux, I tried to get it running for a few days and I’ve given up. At least with my R9 290X, tearing while moving windows is no longer too noticeable, but video replay is really god awful sometimes. My hope is that Wayland will fix this, but it seems to be quite a few years away still.
- LibreOffice interop is not good enough yet. On its own, it’s excellent and enough for all practical purposes, but at work, I have to use Word, PowerPoint and Excel documents, and for those I typically RDP into a Windows machine and just work from there.

Overall, I’m really pleased with how the Linux experiment turned out so far. For development, it’s pretty slick, except for the annoyances with debuggers. [LLDB](http://lldb.llvm.org/) seems promising in this area – and I already used it a few times where GDB would simply fail – but a good graphical front-end with easy-to-write visualizers is definitely needed.

As a normal desktop, Linux does all right for me, except for the problems with font-rendering and tearing. Sure, this is “just polishing”, but getting font-rendering and v-sync right is what made people really notice even if they can’t pin-point it. Just [look at the efforts mobile vendors go](https://source.android.com/devices/graphics/architecture.html) to provide smooth scrolling and good (high-DPI) font-rendering. I sure hope Wayland will help with the v-sync problems; regarding the fonts, everything is there already ([FreeType](http://www.freetype.org/) can do sub-pixel positioning), but it’ll take time until the UI toolkits will properly support it.

![Image showing various font-rendering problems on Linux.](../../assets/c1dc09a7515b66c1.png)


![Image showing various font-rendering problems on Linux.](../../assets/c1dc09a7515b66c1.png)

That’s it, and as you probably guessed, I’m going to stick with Linux for the foreseeable future :)