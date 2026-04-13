---
title: The Linux Graphics Stack
url: https://blog.mecheye.net/2012/06/the-linux-graphics-stack/
author: Jasper St Pierre
published: '2012-06-16'
source_blog: Clean Rinse
source_site: https://blog.mecheye.net
category: graphics
fetched: '2026-04-13'
---

This is an introductory overview post for the Linux Graphics Stack, and how it currently all fits together. I initially wrote it for myself after having conversations with people like Owen Taylor, Ray Strode and Adam Jackson about this stack. I had to go back to them every month or so and learn the stuff from the ground up all over again, as I had forgotten every single piece. I asked them for a good high-level overview document so I could stop bothering them. They didn’t know of any. I started this one. It has been reviewed by Adam Jackson and David Airlie, both of whom work on this exact stack.

Also, I want to point out that a large amount of this stack applies only to the free software drivers. That means that a lot of what you read here may not apply for the AMD Catalyst and NVIDIA proprietary drivers. They may have their own implementations of OpenGL, or an internal fork of Mesa. I’m describing the stack that comes with the free radeon, nouveau and Intel drivers.

If you have any questions, or if at any point things were unclear, or if I’m horribly, horribly wrong about something, or if I just botched a sentence so that it’s incomprehensible, please ask me or let me know in the comments section below.

To start us off, I’m going to paste the entire big stack right here, to let you get a broad overview of where every piece fits in the stack. If you do not understand this right away, don’t be scared. Feel free to refer to this throughout the post. [Here’s a handy link](https://blog.mecheye.net#rendering-stack).

So, to be precise, there are two different paths, depending on the type of rendering you’re doing.

- 3D rendering with OpenGL
-
- Your program starts up, using “OpenGL” to draw.
- A library, “Mesa”, implements the OpenGL API. It uses card-specific drivers to translate the API into a hardware-specific form. If the driver uses Gallium internally, there’s a shared component that turns the OpenGL API into a common intermediate representation, TGSI. The API is passed through Gallium, and all the device-specific driver does is translate from TGSI into hardware commands,
- libdrm uses special secret card-specific
`ioctl`

s to talk to the Linux kernel - The Linux kernel, having special permissions, can allocate memory on and for the card.
- Back out at the Mesa level, Mesa uses DRI2 to talk to Xorg to make sure that buffer flips and window positions, etc. are synchronized.

- 2D rendering with cairo
-
- Your program starts up, using cairo to draw.
- You draw some circles using a gradient. cairo decomposes the circles into trapezoids, and sends these trapezoids and gradients to the X server using the XRender extension. In the case where the X server doesn’t support the XRender extension, cairo draws locally using libpixman, and uses some other method to send the rendered pixmap to the X server.
- The X server acknowledges the XRender request. Xorg can use multiple specialized drivers to do the drawing.
- In a software fallback case, or in the case the graphics driver isn’t up to the task, Xorg will use pixman to do the actual drawing, similar to how cairo does it in its case.
- In a hardware-accelerated case, the Xorg driver will speak libdrm to the kernel, and send textures and commands to the card in the same way.



As to how Xorg gets things on the screen, Xorg itself will set up a framebuffer to draw into using KMS and card-specific drivers.

## X Window System, X11, Xlib, Xorg

X11 isn’t just related to graphics; it has an event delivery system, the concept of properties attached to windows, and more. Lots of other non-graphical things are built on top of it (clipboard, drag and drop). Only listed in here for completeness, and as an introduction. I’ll try and post about the entire X Window System, X11 and all its strange design decisions later.

- X11
- The wire protocol used by the X Window System
- Xlib
- The reference implementation of the client side of the system, and a host of tons of other utilities to manage windows on the X Window System. Used by toolkits with support for X, like GTK+ and Qt. Vanishingly rare to see in applications today.
- XCB
- Sometimes quoted as an alternative to Xlib. It implements a large amount of the X11 protocol. Its API is at a much lower level than Xlib, such that Xlib is actually built on XCB nowadays. Only mentioning it because it’s another acronym.
- Xorg
- The reference implementation of the server side of the system.

X11, the protocol, was designed to be extensible, which means that support for new features can be added without creating a new protocol and breaking existing old clients. As an example, `xeyes`

and `oclock`

get their fancy shapes because of the [Shape Extension](http://www.x.org/releases/X11R7.7/doc/libXext/shapelib.txt), which provide support for non-rectangular windows. If you’re curious how this magic functionality can just appear out of nowhere, the answer is that it doesn’t: support for the extension has to be added to both the server and client before it can be used. There is functionality in the core protocol itself so that clients can ask the server what extensions it has support for, so it knows what functionality it can or cannot use.

X11 was also designed to be “network transparent”. Most importantly it means that we cannot rely on the X server and any X client being on the same machine, so any talking between the two must go over the network. In actuality, a modern desktop environment does not work out of the box in this scenario, as a lot of inter-process communication goes through systems other than X11, like DBus. Over the network, it’s quite chatty, and results in a lot of traffic. When the server and client are on the same machine, instead of going over the network, they’ll go over a UNIX socket, and the kernel doesn’t have to copy data around.

We’ll get back to the X Window System and its numerous extensions in a little bit.

## cairo

**cairo** is a drawing library used either by applications like Firefox directly, or through libraries like GTK+, to draw vector shapes. GTK+3’s drawing model is built entirely on cairo. If you’ve ever used an HTML5 `<canvas>`

, cairo implements practically the same API. Although `<canvas>`

was originally developed by Apple, the vector drawing model is well-known, as it’s the PostScript vector drawing model, which has found support in other vector graphics technologies and standards such as PDF, Flash, SVG, Direct2D, Quartz 2D, OpenVG, and lots more than I can possibly give an exhaustive list for.

cairo has support to draw to X11 surfaces through the [Xlib backend](http://cairographics.org/manual/cairo-XLib-Surfaces.html).

cairo has been used in toolkits like GTK+. Functionality was added in GTK+ 2 to optionally use cairo in GTK+ 2.8. The drawing model in GTK+3 requires cairo.

## XRender Extension

X11 has a special extension, **XRender**, which adds support for anti-aliased drawing primitives (X11’s existing graphics were aliased), gradients, matrix transforms and more. The original intention was that drivers could have specialized accelerated code paths for doing specific drawing. Unfortunately, it seems to be the case that [software rasterization is just as fast](http://ickle.wordpress.com/), for unintuitive reasons. Oh well. XRender deals in aligned trapezoids – rectangles with an optional slant to the left and right edges. Carl Worth and Keith Packard came up with a “fast” software rasterization method for trapezoids. Trapezoids are also super easy to decompose into two triangles, to align ourselves with fast hardware rendering. Cairo includes a wonderful `show-traps`

utility that might give you a bit of insight into the tessellation into trapezoids it does.

Here’s a simple red circle we drew. This is decomposed into two sets of trapezoids – one for the stroke, and one for the fill. Since the diagrams that `show-traps`

gives you by default aren’t very enlightening, I hacked up the utility to give each trapezoid a unique color. Here’s the set of trapezoids for the black stroke.

Psychedelic.

## pixman

Both the X server and cairo need to do pixel level manipulation at some point. cairo and Xorg had separate implementations of things like basic rasterization algorithms, pixel-level access for certain kinds of buffers (ARGB32, RGB24, RGB565), gradients, matrices, and a lot more. Now, both the X server and cairo share a low-level library called **pixman**, which handles these things for it. pixman is not supposed to be a public API, nor is it a drawing API. It’s not really any API at all; it’s just a solution to some code duplication between various parts.

## OpenGL, Mesa, gallium

Now comes the fun part: modern hardware acceleration. I assume everybody already knows what OpenGL is. It’s not a library, there will never be one set of sources to a `libGL.so`

. Each vendor is supposed to provide its own `libGL.so`

. NVIDIA provides its own implementation of OpenGL and ships its own `libGL.so`

, based on its implementations for Windows and OS X.

If you are running open-source drivers, your `libGL.so`

implementation probably comes from **Mesa**. **Mesa** is many things, but one of the major things it provides that it is most famous for is its OpenGL implementation. It is an open-source implementation of the OpenGL API. Mesa itself has multiple backends for which it provides support. It has three CPU-based implementations: swrast (outdated and old, do not use it), softpipe (slow), llvmpipe (potentially fast). Mesa also has hardware-specific drivers. Intel supports Mesa and has built a number of drivers for their chipsets which are shipped inside Mesa. The radeon and nouveau drivers are also supported in Mesa, but are built on a different architecture: gallium.

**gallium** isn’t really anything magical. It’s a set of components to make implementing drivers a lot easier. The idea is that there are state trackers that implement some form of API (OpenGL, GLSL, Direct3D), transform that state to an intermediate representation (known as [Tungsten Graphics Shader Infrastructure, or TGSI](http://people.freedesktop.org/~csimpson/gallium-docs/tgsi.html)), and then the backends take that intermediate representation and convert it to the operations that would be consumed by the hardware itself.

Sadly, the Intel drivers don’t use Gallium. My coworkers tell me it’s because the Intel driver developers do not like having a layer between Mesa and their driver.

## A quick aside: more acronyms

Since there’s a lot of confusing acronyms to cover, and I don’t want to give them each an H3 and write a paragraph for each, I’m just going to list them here. Most of them don’t really matter in today’s world, they’re just an easy reference so you don’t get confused.

- GLES
- OpenGL has several profiles for different form factors.
**GLES**is one of them, standing for “GL Embedded System” or “GL Embedded Subset”, depending on who you ask. It’s the latest approach to target the embedded market. The iPhone supports GLES 2.0. - GLX
- OpenGL has no concept of platform and window systems on its own. Thus, bindings are needed to translate between the differences of OpenGL and something like X11. For instance, putting an OpenGL scene inside an X11 window.
**GLX**is this glue. - WGL
- See above, but replace “X11” with “Windows”, that is, that one Microsoft Operating System.
- EGL
- EGL and GLES are often confused.
**EGL**is a new platform-agnostic API, developed by Khronos Group (the same group that develops and standardizes OpenGL) that provides facilities to get an OpenGL scene up and running on a platform. Like OpenGL, this is vendor-implemented; it’s an alternative to bindings like WGL/GLX and not just a library on top of them, like GLUT. - fglrx
**fglrx**is former name for AMD’s proprietary Xorg OpenGL driver, now known as “Catalyst”. It stands for “FireGL and Radeon for X”. Since it is a proprietary driver, it has its own implementation of`libGL.so`

. I do not know if it is based on Mesa. I’m only mentioning it because it’s sometimes confused with generic technology like AIGLX or GLX, due to the appearance of the letters “GL” and “X”.- DIX, DDX
- The X graphics parts of Xorg is made up of two major parts,
`DIX`

, the “Driver Independent X” subsystem, and`DDX`

, the “Driver Dependent X” subsystem. When we talk about an Xorg driver, the more technically accurate term is a DDX driver.

## Xorg Drivers, DRM, DRI

A little while back I mentioned that Xorg has the ability to do accelerated rendering, based on specific pieces of hardware. I’ll also say that this is not implemented by translating from X11 drawing commands into OpenGL calls. If the drivers are implemented in Mesa land, how can this work without making Xorg dependent on Mesa?

The answer was to create a new piece of infrastructure to be shared between Mesa and Xorg. Mesa implements the OpenGL parts, Xorg implements the X11 drawing parts, and they both convert to a set of card-specific commands. These commands are then uploaded to the kernel, using something called the “Direct Rendering Manager”, or **DRM**. libdrm uses a set of generic, private `ioctl`

s with the kernel to allocate things on the card, and stuffs the commands and textures and things it needs in there. This `ioctl`

interface comes in two forms: Intel’s **GEM**, and Tungsten Graphics’s **TTM**. There is no good distinction between them; they both do the same thing, they’re just different competing implementation. Historically, GEM was designed and proudly announced to be a simpler alternative to TTM, but over time, it has quietly grown to about the same complexity as TTM. Welp.

This means that when you run something like `glxgears`

, it loads Mesa. Mesa itself loads libdrm, and that talks to the kernel driver directly using GEM/TTM. Yes, `glxgears`

talks to the kernel driver directly to show you some spinning gears, and sternly remind you of the benchmarking contents of said utility.

If you poke in `ls /usr/lib64/libdrm_*`

, you’ll note that there are hardware-specific drivers. For cases when GEM/TTM aren’t enough, the Mesa and X server drivers will have a set of private `ioctl`

s to talk to the kernel, which are encapsulated in here. libdrm itself doesn’t actually load these.

The X server needs to know what’s happening here, though, so it can do things like synchronization. This synchronization between your `glxgears`

, the kernel, and the X server is called **DRI**, or more accurately, DRI2. “DRI” stands for “Direct Rendering Infrastructure”, but it’s sort of a strange acronym. “DRI” refers to both the project that glued Mesa and Xorg together (introducing DRM and a bunch of the things I talk about in this article), as well as the DRI protocol and library. DRI 1 wasn’t really that good, so we threw it out and replaced it with DRI 2.

## KMS

As a sort of aside, let’s say you’re working on a new X server, or maybe you want to show graphics on a VT without using an X server. How do you do it? You have to configure the actual hardware to be able to put up graphics. Inside of libdrm and the kernel, there’s a special subsystem that does exactly that, called **KMS**, which stands for “Kernel Mode Setting”. Again, through a set of `ioctl`

s, it’s possible to set up a graphics mode, map a framebuffer, and so on, to display directly on a TTY. Before, there were (and still are) hardware-specific `ioctl`

s, so a shared library called libkms was created to give a shared API. Eventually, there was a new API at the kernel level, literally called the “dumb `ioctl`

s”. With the new dumb `ioctl`

s in place, it is recommended to use those and not libkms.

While it’s very low-level, it’s entirely possible to do. Plymouth, the boot splash screen integrated into modern distributions, is a good example of a very simple application that does this to set up graphics without relying on an X server.

## The “Expose” model, Redirection, TFP, Compositing, AIGLX

I’ve used the term “compositing window manager” without really describing what it means to composite, or what a window manager does. You see, back in the 80s when the X Window System was designed on UNIX systems, a lot of random other companies like HP, Digital Equipment Corp., Sun Microsystems, SGI, were also developing products based on the X Window System. X11 intentionally didn’t mandate any basic policy on how windows were to be controlled, and delegated that responsibility to a separate process called the “window manager”.

As an example, the popular environment at the time, CDE, had a system called “focus follows mouse”, which focused windows when the user moved their mouse over the window itself. This is different from the more popular model that Windows and Mac OS X use by default, “click to focus”.

As window managers started to become more and more complex, [documents](http://tronche.com/gui/x/icccm/) started to [appear](http://standards.freedesktop.org/wm-spec/) describing interoperability between the many different environments. It, too, wouldn’t really mandate any policy either like “Click to Focus” either.

Additionally, back in the 80s, many systems did not have much memory. They could not store the entire pixel contents of all window contents. Windows and X11 solve this issue in the same way: each X11 window should be lossy. Namely, a program will be notified that a window has been “exposed”.

Imagine a set of windows like this. Now let’s say the user drags GIMP away:

The area in the dark gray has been exposed. An `ExposeEvent`

will get sent to the program that owns the window, and it will have to redraw contents. This is why hung programs in versions of Windows or Linux would go blank after you dragged a window over them. Consider the fact that in Windows, the desktop itself is just another program without any special privileges, and can hang like all the others, and you have [one hell of a bug report](http://mrdoob.com/lab/javascript/effects/ie6/).

So, now that machines have as much memory as they do, we have the opportunity to make X11 windows *lossless*, by a mechanism called **redirection**. When we redirect a window, the X server will create backing pixmaps for each window, instead of drawing directly to the backbuffer. This means that the window will be hidden entirely. Something *else* has to take the opportunity to display the pixels in the memory buffer.

The [composite extension](http://www.x.org/releases/X11R7.7/doc/compositeproto/compositeproto.txt) allows a compositing window manager, or “compositor”, to set up something called the **Composite Overlay Window**, or **COW**. The compositor owns the COW, and can paint to it. When you run Compiz or GNOME Shell, these programs are using OpenGL to display the redirected windows on the screen. The X server can give them the window contents by a GL extension, “** Texture from Pixmap**“, or

**TFP**. It lets an OpenGL program use an X11 Pixmap as if it were an OpenGL Texture.

Compositing window managers don’t *have* to use TFP or OpenGL, per se, it’s just the easiest way to do so. They could, if they wanted to, draw the window pixmaps onto the COW normally. I’ve been told that `kwin4`

uses Qt directly to composite windows.

Compositing window managers grab the pixmap from the X server using TFP, and then render it on to the OpenGL scene at just the right place, giving the illusion that the thing that you think you’re clicking on is the actual X11 window. It may sound silly to describe this as an illusion, but play around with GNOME Shell and adjust the size or position of the window actors (Enter `global.get_window_actors().forEach(function(w) { w.scale_x = w.scale_y = 0.5; })`

in the looking glass), and you’ll quickly see the illusion break down in front of you, as you realize that when you click, you’re poking straight through the video player, and to the actual window underneath (Change `0.5`

to `1.0`

in the above snippet to revert the behavior).

With this information, let’s explain one more acronym: **AIGLX**. AIGLX stands for “Accelerated Indirect GLX”. As X11 is a networked protocol, this means that OpenGL should have to work over the network. When OpenGL is being used over the network, this is called an “indirect context”, versus a “direct context” where things are on the same machine. The network protocol used in an “indirect context” is fairly incomplete and unstable.

To understand the design decision behind AIGLX, you have to understand the problem that it was trying to solve: making compositing window managers like Compiz fast. While NVIDIA’s proprietary driver had kernel-level memory management through a custom interface, the open-source stack at this point hadn’t achieved that yet. Pulling a window texture from the X server into the graphics hardware would have meant that it would have to be copied every time the window was updated. Slow. As such, AIGLX was a temporary hack to implement OpenGL in software, preventing the copy into hardware acceleration. As the scene that compositors like Compiz used wasn’t very complex, it worked well enough.

Despite all the fanfare and Phoronix articles, AIGLX hasn’t been used realistically for a while, as we now have the entire DRI stack which can be used to implement TFP without a copy.

As you can imagine, copying (or more accurately, sampling) the window texture contents so that it can be painted as an OpenGL texture requires copying data. As such, most window managers have a feature to turn redirection off for a window that’s full-screen. It may sound a bit silly to describe this as **unredirection**, as that’s the initial state a window is in. But while it may be the initial state for a window, with our modern Linux desktops, it’s hardly the usual state. The logic here is that if a window would be covering the COW anyway and compositing features aren’t necessary, it can safely be unredirected. This feature is designed to give high performance to programs like games, which need to run with high performance at 60 frames per second.

## Wayland

As you can see, we’ve split out quite a large bit of the original infrastructure from X’s initial monolithic behavior. This isn’t the only place where we’ve tore down the monolithic parts of X: a lot of the input device handling has moved into the kernel with evdev, and things like device hotplug support has been moved back into udev.

A large reason that the X Window System stuck around for now was just because it was a lot of effort to replace it. With Xorg stripped down from what it initially was, and with a large amount of functionality required for a modern desktop environment provided solely by extensions, well, how can I say this, [X is overdue](https://www.xkcd.com/963/).

Enter Wayland. Wayland reuses a lot of existing infrastructure that we’ve built up. One of the most controversial things about it is that it lacks any sort of network transparency or drawing protocol. X’s network transparency falls flat in modern times. A large amount of Linux features are hosted in places like DBus, not X, and it’s a shame to see things like Drag and Drop and Clipboard support being by and large hacks with the X Window System solely for network support.

Wayland can use almost the entire stack as detailed above to get a framebuffer on your monitor up and running. Wayland still has a protocol, but it’s based around UNIX sockets and local resources. The biggest drastic change is that there is no `/usr/bin/wayland`

binary running like there is a `/usr/bin/Xorg`

. Instead, Wayland follows the modern desktop’s advice and moves all of this into the window manager process instead. These window managers, more accurately called “compositors” in Wayland terms, are actually in charge of pulling events from the kernel with a system like evdev, setting up a frame buffer using KMS and DRM, and displaying windows on the screen with whatever drawing stack they want, including OpenGL. While this may sound like a lot of code, since these subsystems have moved elsewhere, code to do all of these things would probably be on the order of 2000-3000 SLOC. Consider that the portion of mutter just to implement a sane window focus and stacking policy and synchronize it with the X server is around 4000-5000 SLOC, and maybe you’ll understand my fascination a bit more.

While Wayland does have a library that implementations of both clients and compositors probably should use, it’s simply a reference implementation of the specified Wayland protocol. Somebody could write a Wayland compositor entirely in Python or Ruby and implement the protocol in pure Python, without the help of a libwayland.

Wayland clients talk to the compositor and request a buffer. The compositor will hand them back a buffer that they can draw into, using OpenGL, cairo, or whatever. The compositor is at the discretion to do whatever it wants with that buffer – display it normally because it’s awesome, set it on fire because the application is being annoying, or spin it on a cube because we need more YouTube videos of Linux cube spinning.

The compositor is also in control of input and event handling. If you tried out the thing with setting the scale of the windows in GNOME Shell above, you may have been confused at first, and then figured out that your mouse corresponded to the untransformed window. This is because we weren’t *actually* affecting the X11 window itself, just changing how it gets displayed. The X server keeps track of where windows are, and it’s up to the compositing window manager to display them where the X server thinks it is, otherwise, confusion happens.

Since a Wayland compositor is in charge of reading from evdev and giving windows events, it probably has a much better idea of where a window is, and can do the transformations internally, meaning that not only can we spin windows on a cube temporarily, we will be able to *interact* with windows on a cube.

## Summary

I still hear a lot today that Xorg is very monolithic in its implementation. While this is very true, it’s less true than it was a long while ago. This isn’t due to the incompetence on the part of Xorg developers, a large amount of this is due to baggage that we just have to support, like the hardware-accelerated XRender protocol, or going back even further, non-anti-aliased drawing commands like `XPolyFill`

. While it’s very apparent that X is going to go away in favor of Wayland some time soon, I want to make it clear that a lot of this is happening with the acknowledgement and help of the Xorg and desktop developers. They’re not stubborn, and they’re not incompetent. Hell, for dealing with and implementing a 30-year-old protocol plus history, they’re doing an excellent job, especially with the new architecture.

I also want to give a big shout-out to everybody who worked on the stuff I mentioned in this article, and also want to give my personal thanks to Owen Taylor, Ray Strode and Adam Jackson for being extremely patient and answering all my dumb questions, and to Dave Airlie and Adam Jackson for helping me technically review this article.

While I went into some level of detail in each of these pieces, there’s a lot more here where you could study in a lot more detail if it interests you. To pick just a few examples, you could study the geometry algorithms and theories that cairo exploits to convert arbitrary shapes to trapezoids. Or maybe the fast software rendering algorithm for trapezoids by Carl Worth and Keith Packard and investigate why it’s fast. Consider looking at the design of DRI2, and how it differs from DRI1. Or maybe you’re interested in the hardware itself, and looking at graphics card architecture, and looking at the data sheets to see how you would program one. And if you want to help out in any of these areas, I assume all the projects listed above would be more than happy to have contributions.

I’m planning on writing more of these in the future. A large amount of the stacks used in the Linux and GNOME community today don’t have a good overview document detailing them from a very high level.

This is superb, thank you very much for putting it together.

Just one tiny thing though: trying to run your Looking Glass command on Gnome Shell 3.2 gives a “TypeError: global.window_actors is undefined” exception. Perhaps mention that it only works on 3.4 if that’s the case?

Anyway, thanks again, and well done.

That was my fault. Fixed now.

Pingback: The Linux Graphics Stack | Clean Rinse | G-FX.NET

That was quite educational. I’d been picking up little bits of this from various blogs and mailinglist threads, but I didn’t really see the whole picture until now.

It’s compelling- as a designer it’s exciting to know more about the technology that enables us to share such interesting things with each other.

Thanks for writing this!

Thanks for this.

This filled in a nice bit of knowledge for me.

.

Pingback: Обзор графической подсистемы Linux | UNIXCLUB

Thanks Jasper! Really nice article, I look forward to reading more.

What do you think about server-side decorations, windows info like X atoms, move\resize window in wayland?

I’m on the fence about server-side decorations. krh came to the office a few weeks ago to give an internal demo of Wayland, and I asked him about it. His reasoning was that with thing like rotating and scaling windows, it’s too easy to get a seam between the window and its decorations. That’s a perfectly valid answer, and I’m satisfied with it.

If you’re worried about discontinuity between desktop environments and window toolkits, I wouldn’t be. I expect that we’re going to have a libwayland-decorations which paints (or gives us information to paint) window decorations.

I don’t understand what you mean by the other things, though.

For me, server-side decorations have always meant consistent decoration styling and “internal application behaviour doesn’t affect my ability to move, resize, or minimize/restore/maximize windows” while the only client-side decoration implementation I’ve had experience with (Windows) has lead to applications reveling in custom, inconsistent window borders as well as window management seizing up when an application does.

I’ve heard that the KWin developers plan to force server-side decorations on windows whether they want them or not so, unless my fears of the downsides of client-side decorations can be proven groundless, I may end up using KWin on my LXDE desktop. (And I ditched KDE 4 for repeatedly failing to deliver on their claims of “NOW we’re fast and stable. We promise.”)

Excellent read!! I’ve just recently started dig around Xorg/X11. This has been an amazing read. Great work.

Thank you very much.

Pingback: Voice of reason, quite… | Scali's blog

Pingback: St. Pierre: The Linux Graphics Stack | Linux-Support.com

Awesome work! This graphics world is such spaghetti plate… A good piled-up diagram would be nice to understand how things work. Wayland has a nice collection of them, and it helps understand the interactions happening in the whole stack. BTW, on GNOME 3.4, your command doesn’t work, you need to enter global.get_window_actors().forEach(function(w) { w.scale_x = w.scale_y = 0.5; })

Thanks!

Yeah, that was my fault. I knew I had to correct that before posting it, but forgot about it. Oh well, it’s fixed now!

As for the diagram, I’m going to make one. I’m struggling to make one that’s neat and not a mess, though; there’s lots of different code-paths depending on what libraries you are using, and then there’s things like DRI2, which isn’t a block on its own, but a link layer between two separate blocks.

even with the corrections, I can’t get that command to work, using Fedora 17 (gnome 3.4). I keep getting:

r(digit) = undefined.

each time I run it the digit increments, it started at zero.

That’s what you’re supposed to see. Make sure you’re not in the overview, and that you don’t have any extensions running. The windows should shrink to half size.

Hey magicus,

this is a very nice summary.

Nice writeup and thanks for putting things in perspective. I’d be very interested to see a second part that explains the XVideo acceleration as well. IOW, the part that does colorspace YUV->RGB and scaling conversion…

I don’t know much about XVideo acceleration, but I’m interested in it. When I do learn about it, I’ll be glad to share it with the world.

So, Xv’s like this (focusing on the output side; there’s an input side for video capture too, which works pretty much exactly in reverse). Each X screen has zero or more Xv “adaptors”. There’s two common kinds, overlay and texture. Overlay adaptors are specialized hardware in the GPU to do the colorspace converstion at scanout, texture adaptors are just wired up to the 3D engine.

Each adaptor has:

– one or more ports (simultaneous users)

– a list of supported operations (usually just XvPutImage, which works analogously to XPutImage)

– a list of supported visuals (X11 object model detail, nothing you ever really care about)

– a list of attributes (brightness, contrast, etc)

– a maximum image size

– a list of supported image formats (FOURCC code, bpp, planar or packed, etc)

And that’s pretty much it. Note how this completely omits anything more complicated than colorspace conversion, so all the other decoding work involved in video playback happens on the CPU.

First thanks for this article then my remarks:

– the “Texture from Pixmap“link is broken, could you fix it?

– could you clarify what the COW is, please? You provided a link but I didn’t understand the corresponding text.

-I think that using DRI2, X can be nearly(*) as efficient as Wayland: as with DRI2, it’s also possible to use HW acceleration to draw a buffer in the program, send a reference of the buffer to the display server(compositor), at least that’s what I’ve been told, is-it correct?

*: only nearly because Weston has the compositor, the window manager and the display server in the same process whereas X server implementations put these things into different processes.

Thanks. I fixed the Texture from Pixmap link.

The COW is just a giant window that goes on top of everything else. It’s a bit of magic provided by the X server to make implementing a compositing window manager a lot easier. It will always be the size of the screen, even when you plug in a new monitor. It cannot ever be redirected. When you ask X to give it all the windows on screen, it doesn’t list the COW.

http://cgit.freedesktop.org/xorg/proto/compositeproto/tree/compositeproto.txt#n107

I can’t say anything about efficiency, as I haven’t measured it directly, but yes, the things that you say about Wayland are correct.

Thx for this really nice overview!

Nice overview. As far as I know, there are two things missing in the Linux graphics stack that AmigaOS had 25 years ago.

First, AmigaOS has “lossless” and “lossy” windows mixed into one screen (called SimpleRefresh and SmartRefresh windows). Both of them rendering directly into the screen for maximum performance when the window is in front, but rendering into the backbuffers when they are hidden (for SmartRefresh windows only). This eliminates the constant copying from backbuffers to framebuffers for the common case.

Second, AmigaOS offered API for the vertical blank interrupt, so you could make your rendering 100% smooth, tear-free, and frame-accurate. You could even have your application informed when the beam reached the bottom of your window, so you could start drawing directly into the screen without the user seeing artifacts.

(In case those are implemented in the Linux graphics stack, please provide pointers to API.)

Other than that, I still wonder about performance. I have yet to see my system have full frame rate window management. It might be old and dated, but using mplayer I can play full screen movies (1024×768) with full frame rate (50 fps), so it is not a bandwidth/hardware limitation.

It sounds like AmigaOS has a different model than X. In order to do fancy window transforms like modern compositing managers do, you can’t draw directly to the front-buffer. You have to draw to some kind of buffer in the middle.

The X Expose provides the same functionality, without ever dropping to a back-buffer. In the case where windows are hidden (unmapped), they’re simply not drawn at all. In the cases where partial windows contents are hidden, they’re not drawn either, as X will calculate what area needs to be drawn and clip appropriately when sending an Expose event to the window.

With AmigaOS, it sounds like the application chooses when to paint. In the X model, you are not allowed to paint directly to your window outside of some event from X. To have something like a spinning animation, you tell the X server that some region has been updated, and then X will do the math, see what really needs to be drawn, and then send you an Expose.

Yes, the Amiga was a home/personal computer, and as such, the GUI was aimed purely at rendering local applications, much like early versions of MacOS, Windows etc.

X comes from the world of UNIX and minicomputers, where initially the remote functionality was all-important: there was a single minicomputer on which all users ran their applications, and they each had thin client running the X server which provided the desktop on which the applications would be displayed.

These days however, X is mostly used on PCs as well, running linux, BSD and other *nix-like OSes, but both the X server and the clients run locally, so X now has to serve the same role as Windows/MacOS etc.

Funny enough these other OSes now also have remote desktop functionality.

I have a bunch of linux machines at home and I use X’s networking capability ALL THE TIME to collect windows from different computers onto one screen. I use GLX (OpenGL over the network) as well, though less often. The idea that one should only care about the ability to render to a local computer is still a huge failure to think outside the box. If one can stream video between computers, there’s *plenty* of bandwidth to wrap up an event stream around a remote window. Whether that’s done via GLX style code with graphics primitives, or by just streaming the rendered window (and audio?) and user events over the network doesn’t matter. The point is, it’s an essential part of network-as-the-computer use, and the more computers I have, the more useful it becomes. (Not as useful as being able to make the whole network *behave* as a single united computer, but that’s beyond the scope of the discussion) :-)

So, for a window system to be viable for daily use for me, it needs to have an event stream that can be tunneled between computers on both local and wide networks. Most of us are familiar with the huge win of X over SSH, highlighting that the window system doesn’t have to solve the security issues as well, just allow tunnelling. It would also help to have a way to parallelize requests to reduce latency serialization like XCB . It does NOT have to be intrinsic – since improvements may be easier if it isn’t – but it needs to be either bundled or easily addable, or… it won’t be supplanting X for a bunch of us.

In the end I want to be able to have windows be independent, texture-like, ideally network-transparent constructs to which I can do pretty much anything I want in terms of mapping them onto objects. I need to be able to send events to them that don’t look “fake” like X tries to force (with some cause, and almost no app checks that event flag, but still). I want those textures to be available to various compositing window managers (and without shenanigans like not having rootless X has caused past developers).

Remote desktop functionality is garbage by comparison to the per-window equivalent. Having only remote desktop as an option strikes me as a crufty side effect of minds shaped by root-full X (i.e. being forced to use the entire screen to make events works decently) and the mess that is Windows. Having only this seems to be to be *why* so many people think the local computer is the only objective, since they’ve never been able to work comfortably with windows from dozens of computers sharing their desktop – coincidentally spreading the CPU load as well.

Anyway, sorry for the rant. But I *need* network-transparent graphics, both 2D and 3D. So if Wayland ends up with a module for this (some related commentary is in http://wayland.freedesktop.org/faq.html …) then folks like me can use it *instead* of X, otherwise, no.

I’m not sure how else to tell you this, but with how modern computers work, with how modern GPUs work, the world is moving away from a client/server based graphics model, and more to a compiled-for-local-execution-on-a-GPU graphics model. See: Metal, Vulkan. I do think it’s correct to treat networked operation and display differently from local rendering.

Anyone who argues that network transparency falls flat in the modern world has never used a slowish laptop as a thin client to a remote server.

Yes, VNC sucks. It sucks _royally_. That’s why things like X11 over ethernet are so nice…and you can do that easily and cheaply, _now_. It’s actually very nice that I can run CPU-intensive apps on a dual Xeon box in one room, and not have to deal with the heat or noise while sitting on a recliner in my living room.

Now, X11 over ethernet does have one distinct failing…if applications rasterize client-side, things get _really_ slow if you’re on 100Mb/s ethernet. Try Luminance-HDR; I had a conversation with its developer, and it looks like the problem there sits within Qt. And, here, Wayland is *pushinig* the rasterize-then-send model.

It seems to me that the problem could have been alleviated with a new release of X with an eye toward standardizing coordinate remapping, or even simply passing input events through the window manager/compositor before passing them on to the application.

Now, I’m all for the modularity we’re seeing today. Keeping component operational scope tight is good engineering practice, and splitting the X server and driver architecture into modular layers is a good thing. Wayland, however, is a case of throwing the baby out with the bathwater.

Qt and GTK+ both use XRender, so it’s not the rasterize-and-send model in your case above. It’s just that trapezoids are chatty.

GL applications may work. Or they may not. Indirect contexts in GL are underspecified, and don’t contain any new features beyond GL 1.4.

Besides graphics, basic pieces of functionality will break. Assuming you’re talking about ssh forwarding, copy/paste will work on your local machine, but DBus services will be remote. Drag and drop is even more complicated.

A lot of the problems with VNC are due to the generic nature of it. Something like RDP or SPICE is a lot faster and doesn’t shuttle a drawing protocol over the network. It does this by having a concept of windows down to the basic level, so that if you move a window, it doesn’t have to repaint all other windows; it can instead just use its local backbuffers to repaint the exposed window.

All of your suggestions have been proposed before, but by the end, X will no longer be X. And if we’re replacing X, why not actually replace it instead of using all extensions instead of a core set of functionality?

“Something like RDP or SPICE is a lot faster and doesn’t shuttle a drawing protocol over the network”

Recent versions of RDP support a full composited 2D rendering model as well as remote 3D rendering. See the “Remote Desktop Protocol: Composited Remoting V2 Specification” at MSDN for details.

(Apologies if I started to ramble toward the end. It’s late here.)

I’ve watched TCP flows on a 100Mb/s network while trying to do work with luminance-hdr. It consumes the entire practical bandwidth of the pipe for a few seconds first pushing the data from the client to the server, pulling the data *back* from the server to the client, and then pushing it again. There’s something funky there. (On gigabit, I don’t notice it at all)

I’ve had a lot of good luck with basic GL apps over SSH and over TCP; I can’t complain too much there. I don’t figure on playing 3D games that way, of course.

As for D-Bus, I expect D-Bus tunneling will eventually be included in SSH sessions, as X11 forwarding currently is. This is simply the natural extension of how common D-Bus is becoming, and how dependent on it many things have become. For many users, remote SSH sessions are pragmatically extensions of the current desktop session, so extending desktop communication in this way makes a certain amount of sense.

I’ll agree that RDP works better than VNC. And, certainly, RDP carries with it (at least in the Windows world) the convenience of audio and printer configuration and transport. Still, it doesn’t integrate remote windows into the local desktop anywhere the degree of completeness that X11 does. I’m unfamiliar with SPICE, unless you’re referencing a hardware descriptor language.

Regarding why not completely replace X11, I have several responses. First, building iteratively from an existing, established and stable system maintains the utility of millions of man-hours of experience and knowledge in configuration, application, integration and troubleshooting of the system. With such a system, you can always draw a path between some known and understood historical state and the present state. Wiping out the existing system and replacing it is like telling a Segway user he must now operate a moped. While they serve the same basic need, the techniques of operation, maintenance, troubleshooting and extensibility options are completely different.

Second, consider the ship of Theseus. You can replace and rework every component of the ship until the new thing is very much unlike the old thing, but its crew still knows it just as it always did, and it’s still the same old ship. Completely tearing down X11 and building Wayland is like scuttling Theseus’s ship and erecting a new, different ship and transferring the crew over. They’re both still ships, but everything’s…different.

Third, old code is stable code. There are less likely to be bugs in old code than new code, simply because the old code has been compiled, executed and tested over a far longer period. It’s OK to replace old code with new code where that’s useful, but it makes far more sense to replace it in small chunks and let each chunk go through a burn-in period before you move on to the next chunk. The fewer new lines of code, the easier it will be to isolate the causes of new bug reports.

Finally, (and this ties back to the first and third responses), there’s systemic complexity. Just as new lines of code represent new opportunities for bugs, new arrangements of architecture in a complex system indicate a growth in the presence of systemic bugs. Any time you plug a couple components together, you risk them interacting with each other in unforeseen ways. Old systems and architectures have had the benefit of these interactions being observed and documented. With new systems and systemic components come new opportunities for unforeseen interactions. That means more time spent by developers, technicians and end-users alike in figuring out why this, that or the other thing isn’t working properly.

By all means, if something’s broken, it’s broken. The question is whether you fix it (and deal with new problems in a gradual way) or whether you throw the thing out and try to reinvent it.

I believe more time will be lost reinventing the system than would be lost if people tried to fix the old system first. But nobody wants to be a maintenance programmer; it’s not sexy. And every generation reinvents the wheel.

( If you want to see this in action on a relatively fast timescale, look at the cycle of evolution of programmers. Every generation of language designers thinks they can easily do better than the other guy did two years’ prior. They think, “hey, it doesn’t have to be as complicated as all that”. And then they discover complexities driven by their base assumptions or declarations, or they discover edge cases that the previous system had already had to deal with. (See also: GEM vs TTM in TFA) )

krh worked on the X server for five or six years before starting Wayland.

So? (I’ve got guesses at to ‘what’, but I don’t want to put words in your mouth.)

First there is a lot of issue with old code base. They tend to be hugly and very difficult to change or evolve without breaking a lot of things due to some nasty side effect. It’s all good to be for evolving software, but after more of 20 years, it is understandable that it’s better to start from scratch. We have today much better infrastructure, much better tools and library to write software, at some point the only way to use them at there full capability is by writing a replacement using a full new design.

As for replacing X11, there is a lot of thing that are deap inside it’s protocol that can’t really be fixed without rewritting it from scratch. Redirect input and security are the two main one. Redirect input has been described in this blog already, but security has not. In X world, it is assumed that a running application that access the display can do almost everything it want. From grabbing input, faking them, getting pixel and putting window out of the Composite / Window manager hand.

This is really a bad scenario for any wide use of Linux on a large scale (This basically mean you should never enter your password in a X session if you care about security). We are currently fine, because we trust our code base (mostly free software) and because we have to little users for anyone to care. But if one day we get a bigger user base, that would be a major issue that need to be solved. And Wayland is clearly an opportunity in this case as all input and pixels are managed by one process that can enfore a proper security model.

> Third, old code is stable code

X windows is by far the most unstable part of a linux system — far worse than Windows XP (I use both and have many more crashes with X). I have linux servers which have been running for over 3 years without a reboot or crash. Linux desktops? Not so much. Of course this is due to the added complexity of desktop applications, but the often repeated argument that we shouldn’t mess with X because of how stable it is is ludicrous from an end user’s perspective.

@Michael (and anyone else concerned about losing Millions of X man hours) : The thing is Wayland is really letting your desktop cut out the middle man, simplifying things. They tried many times to improve/extend X, it was always complex and lead to breakages and regressions particularly on less common setups with less usual configuration, obsoleting othwerwise functional hardware. If clients want to talk X protocol in future they can, a slim leaner meaner less buggy X11 server process can simply render into a Wayland window. Since the 80’s and early 90’s when X was a fresh windowing system, the environment has changed an awful lot, X has accumulated more and more cruft, has more and more unused anachronistic features. When the basic model doesn’t fit, you get hard to understand over complicated fragile systems and that’s what has been lived with. There just aren’t the memory and bandwidth constraints, that X was designed to live with. So the X architecture, in having to adapt so much, actually causes many of the bugs, design performance bugs and application complexities. The network transparency, that was a key X bonus, simply doesn’t work like it used to, the modern desktop has side stepped it, by implementing protocols like sftp, ssh, as well web, breaking the Gordian knot, will allow new ways to tackle that problem which integrate far better with modern desktop and hopefully can be properly designed with modern network security requirements in mind, building on modern APIs.

You need a better story on network transparency. Maybe I read it wrong, but it sounds like what you just said is “we already broke it anyway so now we will just throw it away”. This won’t fly.

Use RDP. Network transparency is a dumb, failed idea.

Errrm, developers can and quite often do use XRender for rasterise-and-send based drawing. Remember that blitting a rectangular image to the screen is just a special case of drawing a textured trapezoid to the screen, and in fact many XRender implementations in graphics drivers have a special hardware-accelerated fast path for this case.

One thing in this article caught my eye: “Even basic features and innovations like “Click to Focus” that were in Windows 3.1 for Workgroups hadn’t caught on yet. The popular environment at the time, CDE, had a system called “focus follows mouse”

You’ll have to pry the computer out of my cold, dead hands before I will give up “focus follows mouse”. I certainly hope Wayland allows users to choose their preferred focus model.

It’s up to the compositor to enforce that policy. Given that our customers’ workflows require focus-follows-mouse, I assume it will be working and maintained in GNOME for a long time.

And sorry, it really wasn’t meant to be condescending. It was meant to emphasize that X didn’t specify a policy at all.

cool write up!

minor nitpick: Cairo as the main drawing API was introduced in GTK+ 2.8; not really “at the end of the 2.x cycle”. after 2.8, the X11-based GDK drawing API was considered legacy.

other than that, everything looks great. kudos!

Aha, thanks.

Thanks for writing this! I wish I could read something like this when I was starting with Linux graphics stack 2.5 years ago.

2 fixes:

1) There’s nothing “secret” about libdrm_* ioctls. They are tied to the hardware.

2) GLSL is not an API as implemented by any state tracker. It’s a language in which OpenGL shaders are written.

There are other APIs for which state tracker exists: VDPAU, VA, XVMC, OpenCL (clover). Also worth mentioning is Xorg state tracker, which implements generic DDX.

Martin Peres (Nouveau dev) created nice diagrams explaining how various components interact with each other:

http://fs.mupuf.org/mupuf/nvidia/archi.svg

http://fs.mupuf.org/mupuf/nvidia/mesa.svg

(dotted lines are optional / obsolete)

(don’t be misleaded by word “nvidia” in those links)

1) I was using “secret” as a sort of half-synonym to “internal”, in that you shouldn’t be calling them yourself, and that the ioctl API is in some sense instable. Is that correct?

2) I guess I was confused by the appearance of http://cgit.freedesktop.org/mesa/mesa/tree/src/mesa/state_tracker/st_glsl_to_tgsi.cpp in the state_tracker directory — does GLSL just get directly translated to TGSI, with no intermediate state? I’d certainly like to learn more about the GLSL stack as well.

Thanks for the links to the diagrams. Those are really neat.

1) Well, if you want to write some new piece of software you should NOT use libdrm or libdrm_* directly. Libdrm exposes pretty low level API which is used only by DDX’s and Mesa (and with Xorg state tracker we could get rid of DDX). Libdrm_* libraries exist because hardware differ too much between vendors. They are not internal or unstable (at least they shouldn’t be). They are “driver-specific”.

2) GLSL is also the name of shader intermediate representation (IR). TGSI, Mesa (quite confusing name), LLVM, SM4, NV50_IR, etc. are other IRs. st_glsl_to_tgsi is a translator between GLSL IR and TGSI IR.

For Nouveau translation chain looks like this:

GLSL -> TGSI -> NV50/NVC0 -> NV50/NVC0 binary

GLSL -> TGSI -> NV30 binary

Before st_glsl_to_tgsi was written it looked like this:

GLSL -> Mesa -> TGSI -> NV50/NVC0 -> NV50/NVC0 binary

I’m not sure about these:

For Radeon, I believe it looks like this:

GLSL -> TGSI -> r600 binary

GLSL -> TGSI -> LLVM -> RadeonSI binary

For Intel:

GLSL -> Mesa -> i965 binary

…

What do you recommend instead of libdrm, for something low-level like Plymouth, or a Wayland compositor?

And thanks for clearing up the state tracking confusion.

Wayland uses EGL (provided by Mesa).

Plymouth seems to have very narrow needs and it starts very early in a boot process, so using libdrm directly makes some sense…

Where does Weston boot up EGL? I just see a DRM backend:

http://cgit.freedesktop.org/wayland/weston/tree/src/compositor-drm.c

Superb! Brings a lot of understanding into the mystery of Linux graphics! Thank you!

“I asked them for a good high-level overview document so I could stop bothering them. They didn’t know of any. I started this one.”

Thanks. Reminds me a lot of my attempts to document wayland: http://www.chaosreigns.com/wayland/

“My coworkers tell me it’s because the Intel driver developers do not like having a layer between Mesa and their driver.”

I thought I read it was because they don’t want to rewrite the driver while neglecting the existing driver.

“Driver Dependent X”

Should be “Device” not “Driver”.

“One of the most controversial things about it is that it lacks any sort of network transparency or drawing protocol.”

…

You are not helping.

It only lacks it because it hasn’t been added yet. It is obviously inevitable. https://bugs.freedesktop.org/show_bug.cgi?id=48981

“Wayland clients talk to the compositor and request a buffer.”

I believe the client actually allocates the buffer, without any interaction with the compositor.

“I want to make it clear that a lot of this is happening with the acknowledgement and help of the Xorg and desktop developers.”

You say that like wayland isn’t being created *by* the Xorg developers. I believe AIGLX and DRI2 were largely created by krh.

> I thought I read it was because they don’t want to rewrite the driver while neglecting the existing driver.

When I asked Jerome Glisse, who works on mesa, that’s what he said to me. Feel free to ask the Intel drivers themselves.

> Should be “Device” not “Driver”.

Thanks, fixed.

> You are not helping.

I cannot image how it would work at the Wayland protocol level. As far as I know, there won’t be any drawing protocol built into the system, so we’re stuck with copying bitmaps, like a more advanced VNC. Things like Drag and Drop and Clipboard support are based around FDs; I do not know you could possibly make FDs network transparent, besides some socket magic. Has there been any thought towards remoting with DBus?

Maybe there could be some SPICE integration, which does define some parts of a drawing protocol. But doesn’t really have to do anything with Wayland.

> You say that like wayland isn’t being created *by* the Xorg developers. I believe AIGLX and DRI2 were largely created by krh.

When I was discussing AIGLX with ajax to learn about it, he pointed out that he gave the acroynm its name. Even if krh championed the projects, they’re clearly being supported by the Xorg developers.

> I cannot image how it would work at the Wayland protocol level.

And because you can’t imagine it, you believe it won’t happen?

Maybe read the stuff in the bug about it I gave you a link to? It includes:

well presumably fd passing is not going to be something you can do over a network socket…

right, you need a proxy server that looks like a local wayland server, which then talks spdy (for example) over the internet to the remote server

Honestly, I’m sure I understand the wayland protocol less than you do.

I did read the link. It seemed like a remote display protocol. So, basically, you can see the screen, like VNC. Nothing fancy there. There’s no network transparency, where you can start a client and a compositor on two different machines.

I believe it’s planned to work for individual applications.

As others have said, great article. I do have couple questions/areas I’d like to know more about.

First, what exactly does the window manager do? I would think it would specify the locations of the windows, but you say the X server tells the compositing window manager the locations, not the other way around. Also, what about if the WM and compositor are separate, like xcompmgr?

Second, in order to be fast enough, most of this is built on passing shared memory buffers around. Are some of these buffers in GPU memory, or is all GPU communication done with commands? Do buffers often get rendered in GPU memory and then copied back to system memory? What component decides where to allocate a buffer? Ultimately, the frontbuffer has to get into GPU memory for the RAMDAC to send out to the monitor, right?

These might be too long to answer in a comment, but hopefully a future article will cover them.

First, yeah, I sort of cheated there by merging the compositing manager and window manager into one “compositing window manager”. The window manager has a lot of responsibilities, but the idea is that there’s still this intermediate thing, “X”, between clients and the window manager, and the compositing manager. The window manager has the responsibility to manage regular windows, and place them in positions. It will tell X where it wants to place them. The compositing manager just simply takes positions from X. It does not have the responsibility to move windows.

Second, I don’t understand your question. You say “most of this”. What is “this”? The backbuffer for windows?

“This” is the OpenGL rendering case, the non-XRender 2D case, and everything Wayland does. Anytime the client is rendering into a buffer, passing it to the display server/compositor which renders it into another buffer, which is then flipped to yet another buffer. Each of the rendering steps can happen using the GPU, so I’m wondering how much the stack is able to avoid copying back and forth between video memory and main memory, and which components (kernel, X, compositor, app) manage the buffers.

Does the consolidation of compositor, window manager and the display server into a single process mean a crash in the window-management/compositing code will take down the whole wayland stack and all applications?

Will it still be possible to restart/replace the window-management component without closing all running applications like restarting/replacing a window manager in X11?

> Does the consolidation of compositor, window manager and the display server into a single process mean a crash in the window-management/compositing code will take down the whole wayland stack and all applications?

My guess is yes, but the protocol and implementation is simpler making crashy bugs less likely. I also see something like Xpra in my crystal bowl, or “screen for x” for wayland ;-)

>Will it still be possible to restart/replace the window-management component without closing all running applications like restarting/replacing a window manager in X11?

Still guessing: Possibly. “Window managers” implemented as plugins might be possible to change at run-time – i wouldn’t bet either way at this moment. “Window managers” as alternatives to Weston: probably not without something like screen for wayland

I may have misunderstood but I think an idea floating around was to have a lower level Wayland compositor running, so we could do seamless transition between different compositor (boot compositor, per user compositor) and that could also serve to keep the application runnign in case of crash or during compositor switching transition.

Thank you for this post.

I just wanted to mention that the upcoming Qt 5’s X11 backend is going to use XCB. A supposed benefit of XCB is that it can hide latency via returning futures instead of blocking for a result.

Pingback: Links 23/6/2012: Wine 1.5.7 released, Apple Racism | Techrights

Thank you for this excellent article – I remember having read something similar in quality about the Linux audio stack a while ago. I was missing this one :-)

Excellent job, thanks again.

Fantastic write-up! Well done and Thanks!

Nice!

Btw: The low-level kms from tty (via dumb) is not that hard, i am using it for a my game xizero. For a tutorial see: http://plus.google.com/108656087443346595397/posts/CHNjhmURPm5

This is great work! Thank you for the post!

Far and away the best graphics diagrams I’ve ever seen appear in this SlideShare.net presentation created by the amazing Jim Huang of 0xlabs:

http://www.slideshare.net/jserv/design-and-concepts-of-android-graphics

Some of the content is Android-specific but most of it is not. The combination of Jasper’s wonderful blog entry and Jim Huang’s slides together give a fairly comprehensive view of Linux graphics.

Thanks Jasper for your hard work,

Alison

> X11 isn’t just related to graphics; it has an event delivery system

I would also add that IIRC it’s called “X Server” because it’s a server. It provides resources, such as access to keyboard, video, mouse, etc. And programs using it are X clients, because they connect to server and request some resources there. X server also allows them to communicate to each other, exchange data, request some information, etc.

> a lot of inter-process communication goes through systems other than X11, like DBus.

Yeah. It’s not network-transparent. I don’t really know why. Initially DBUS was based on KDE DCOP, which was built on top of X11 and was “network-transparent”, but DBUS writers had not followed that example. I guess they wanted DBUS to work even without X11. So it’s not X11 to blame, it’s DBUS to blame for that. There’re hacks allowing you to get DBUS across the network anyway.

> it seems to be the case that software rasterization is just as fast, for unintuitive reasons.

It solely depends on the way you draw things. As long as you draw pixel-per-pixel-like (that’s what happens with most current fancy themes) it will definitely be faster to draw it locally and send entire image in one shot to the server than call XPutPixel many times. But as long as you have a rather monotonous images (usually for dark themes and tiling WMs like http://wmfs.info/images/wmfs2_thmb_03.png) drawing it with XRender will need just a few calls, and thus will be faster than putting a lot of pixels by hand. Modern toolkits usually support both ways.

> glxgears loads mesa. mesa itself loads libdrm, and that talks to the kernel driver directly using GEM/TTM.

Isn’t Xserver takes part in that chain? Isn’t mesa talks to the Xserver, while Xserver talks to the kernel directly? What are glXChooseVisual(), glXCreateContext(), glXMakeCurrent() there for then?

> So, now that machines have as much memory as they do, we have the opportunity to make X11 windows lossless

Yeah, “640kb ought to be enough for anybody”. There’re different people, some still prefer to have their windows “lossy” but take less memory. There’s different hardware as well. Doing “lossless windows” on an electronic paper display of eBooks (yes, X works there) is just a waste of its small amount of memory. Also by not “backing pixmaps for each window” on multi-monitor things like http://youtu.be/N6Vf8R_gOec you can save 500MB of RAM just for the desktop and one full screen window on top of it. And the more windows you get, the more RAM it’ll take.

> Wayland follows the modern desktop’s advice and moves all of this into the window manager process instead

Single window manager, no decorators, no light/tiling WMs… Microsoft Windows for Linux? ;)

> X is overdue. Enter Wayland.

X server is so large because it supports every scenario possible. It can work on a low-RAM systems, but can benefit from additional RAM with things like compositing or pixmap caching. It works on black&white displays (ebooks). It can work for different video cards with or without acceleration, or even without video cards at all (sometimes it’s great to be able to run a graphical installer on a server without graphical card). That’s the point of X — support wide range of hardware, allow clients to do things as fast as possible on the current hardware, and still remain backward-compatible, so that applications written 15 years ago work on modern Xservers.

Wayland looks so small, because it cannot do anything. Correct me if I’m wrong, but last time I checked it was missing a lot of features I’m using every day. It not only missed some cool features, like ability to use several keyboards/mouses (see `xinput list`), but was not allowing to do even simple things. I.e. there were no compose-key, no keyboard layouts (xkb), no monitors management (xrandr), no taskbar/dockbar possible (!), no way to change desktop background, even no clipboard/selection, and there were some complexities with keyboard/mouse grabs required for popup-menus to work. Saying that you should throw out Xorg because “X is overdue” is like saying that you must throw out GIMP and use Paint, because GIMP is overdue. Yes, it has a lot of features, that you may not need right now, but when you actually need them — they are there.

If Wayland will have all these features, and have them in a backward-compatible way, won’t it, after years of fixing all the issues, end up being as large as Xorg is now? As you wrote:

> Historically, GEM was designed and proudly announced to be a simpler alternative to TTM, but over time, it has quietly grown to about the same complexity as TTM. Welp.

—

Thank you for a great article.

PS: When it comes to graphics, why do people always compare wayland and Xorg, but never mention directfb? How about writing an article about directfb too?

> I would also add that IIRC it’s called “X Server” because it’s a server. It provides resources, such as access to keyboard, video, mouse, etc. And programs using it are X clients, because they connect to server and request some resources there. X server also allows them to communicate to each other, exchange data, request some information, etc.

I originally had a section about this, but it was quite rant-y. I removed it.

> It solely depends on the way you draw things. As long as you draw pixel-per-pixel-like (that’s what happens with most current fancy themes) it will definitely be faster to draw it locally and send entire image in one shot to the server than call XPutPixel many times. But as long as you have a rather monotonous images (usually for dark themes and tiling WMs like http://wmfs.info/images/wmfs2_thmb_03.png) drawing it with XRender will need just a few calls, and thus will be faster than putting a lot of pixels by hand. Modern toolkits usually support both ways.

No, I mean that software rasterizing can be faster than hardware acceleration, for unintuitive reasons.

> Isn’t Xserver takes part in that chain? Isn’t mesa talks to the Xserver, while Xserver talks to the kernel directly? What are glXChooseVisual(), glXCreateContext(), glXMakeCurrent() there for then?

What makes you think that needs to go through the X server? Direct rendering doesn’t touch the X server at all – that’s the point.

> Single window manager, no decorators, no light/tiling WMs… Microsoft Windows for Linux? ;)

There’s a single compositor, yes. Decorations are done client-side currently. You can make a light/tiling WM for Wayland – it’s perfectly possible.

> Yeah, “640kb ought to be enough for anybody”. There’re different people, some still prefer to have their windows “lossy” but take less memory.

Well yes, I was saying for the general desktop scenario, or any smart phone built in the last five years, that we can support windows that are backed by some sort of memory. Windows does this too, with dwm.exe, it’s “desktop window manager”, which is actually a compositor.

> Wayland looks so small, because it cannot do anything. Correct me if I’m wrong, but last time I checked it was missing a lot of features I’m using every day. It not only missed some cool features, like ability to use several keyboards/mouses (see `xinput list`), but was not allowing to do even simple things. I.e. there were no compose-key, no keyboard layouts (xkb), no monitors management (xrandr), no taskbar/dockbar possible (!), no way to change desktop background, even no clipboard/selection, and there were some complexities with keyboard/mouse grabs required for popup-menus to work. Saying that you should throw out Xorg because “X is overdue” is like saying that you must throw out GIMP and use Paint, because GIMP is overdue. Yes, it has a lot of features, that you may not need right now, but when you actually need them — they are there.

Multiple input devices work as well – the protocol has support for it. XKB is being copied wholesale and put into Wayland for keyboard layouts. Monitors management and a taskbar/dockbar would be done by the compositor, as would desktop background. Since we’re not tied to X’s window tree, it means that we can finally do different backgrounds on different workspaces, too. Clipboard (and DND) is built into the protocol. The popup-menu solution has been fixed with a special window type, and the correct implementation for the compositor is to not send events from the device pair to any other client while one of those windows is up.

> PS: When it comes to graphics, why do people always compare wayland and Xorg, but never mention directfb? How about writing an article about directfb too?

DirectFB isn’t a full solution to replace X11. It’s uninteresting. Nobody cares.

As for why software rendering can be faster than hardware rendering, it is not unintuitive reason at all :-)

When you are writing a software rendering code, you can actually cut out a lot of the screen and only render the needed pixels on screen. You are just checking the limit and don’t paint outside of it. When you are doing hardware rendering, you need to actually send all pixels and the hardware will do the if based on a buffer with the clipping information. A second problem with hardware, but that’s more an issue due to driver, it is not possible to do partial update on rendering, you need to update the full screen every time. In software, you just need to update the area that did change (It can be done for double or triple buffering, by just remembering the change of the last one or two frame and replaying them).

So basically the software engine has a lot more clue and don’t require as much memory and cpu bandwith as the hardware engine require in an average case. Obviously if you always need to rerender a full screen with multiple layout full of alpha, then hardware will beat software because there is no short cut for it.

> So basically the software engine has a lot

> more clue and don’t require as much

> memory and cpu bandwith as the hardware

> engine require in an average case.

You obviously haven’t heard of page-flipping. What you are basically describing above is an implementation of basic old way of copying of data between buffers.

In a page-flip setup (which is pretty common nowadays), the front and back buffer are switched by just changing pointer addresses thereby eliminating the overhead of copying, bandwidth, and partial update shenanigans, down to just a CPU single instruction.

> No, I mean that software rasterizing can be faster than hardware acceleration, for unintuitive reasons.

AFAIK, those were the reasons. :) Software rasterizing is faster if you need too many function calls to make it hardware. In that case overhead of a function call becomes larger than speedup from hardware acceleration.

> What makes you think that needs to go through the X server? Direct rendering doesn’t touch the X server at all – that’s the point.

The fact that glxgears works makes me think that. :) It works locally, it works over `ssh -X`, it also works in Xnest (`apt-get install xnest; Xnest -geometry 800×600 :1 & env DISPLAY=:1 glxgears`). So either it always goes over something like X11 GLX extension, or mesa has some kind of local-display-optimization, and sometimes routes requests directly, but sometimes over X11. In the last case I wonder, how it determines whether it was a local display or not?

> There’s a single compositor, yes. Decorations are done client-side currently.

No emerald with nice decorations for wayland? No global decoration theme possible, every software has to implement its own theme? No stylish linux desktop any more? This really looks like a step back. Maybe it would be better to make decorator a wayland plugin at least? BTW, does every app still have to draw a “shadow” for its window manually? ;)

> You can make a light/tiling WM for Wayland – it’s perfectly possible.

Without being able to disable window decorations it’s really hard to make a tiling WM. Also as a part of wayland compositor, WM won’t be light any more. Currently you need as much as 50 lines of code to write a tiny WM (http://incise.org/tinywm.html), and no more than 2000 lines to write a usable tiling WM (https://en.wikipedia.org/wiki/Dwm). Is that possible for wayland?

> Multiple input devices work as well – the protocol has support for it.

Is there a way to configure them? I.e. can I have separate mouse pointers for my external mouse and touchpad in wayland as I can do in Xorg with `xinput` tool? Or is it up to the compositor?

> Monitors management and a taskbar/dockbar would be done by the compositor, as would desktop background.

You mean no separate tools to configure monitors (xrandr)? And unless compositor explicitly allows me to e.g. rotate the monitor I cannot do that? So now I have to choose among compositor with good WM, compositor supporting several monitors and compositor with a good dockbar… That’s not good. Xorg does not make me to choose, I can use gnome desktop with AWN dockbar and compiz WM and have a comfortable good looking desktop. That’s what makes linux great. Maybe it would be better to make them some sort of plugins for a general compositor?

> Since we’re not tied to X’s window tree, it means that we can finally do different backgrounds on different workspaces, too.

Different backgrounds on different workspaces were working in X for years. I’ve seen it at least since KDE2.

> Clipboard (and DND) is built into the protocol.

Now I can copy a text from browser and it will get pasted in openoffice writer with formatting/hyperlinks preserved but as a plain-text in vim? Great! Does it still support separate clipboard and selection?

> The popup-menu solution has been fixed with a special window type

Waiting to see how it works. Last time I tried gtk popup menu crashed the compositor.

> DirectFB isn’t a full solution to replace X11.

Why not? It has support for keyboard, video, mouse, allows to use hardware acceleration, supports multiple applications and windows (http://directfb.org/index.php?path=Main%2FScreenshots). Debian GTK installer have used directfb for years and nobody have even noticed that it’s not Xorg.

Debian Installer Uses Xorg since squeeze. As far as i know the GTK+ directfb backend was too buggy.

The Guest misses the point with the criticism of Wayland. The first implementations (like Weston) are supposed to be references, not shippable products. In order to keep Wayland small, fast and simple, it’s not meant to include every feature anyone can think of like all the ones X11 has been festooned with and now must support. Wayland is intended to be the basis for a window manager and compositing system, a set of standards almost, and is intended to be skinnable and extensible. The developers don’t object to tiling and window directions, but simple have a full plate already and will be pleased if someone outside contributes support for those extensions.

Regarding mesa talking to X, as I understand it, once GLX or EGL has provided a client with a graphics context, the client essentially owns the memory that is part of the context and can render directly to it. Android uses EGL like Linux and has a similar model.

> The first implementations (like Weston) are supposed to be references, not shippable products.

The problem is not that Weston (as an implementation) does not support some features. The problem is that Wayland (as a protocol) does not support them. And as long as there’s no support in the protocol — any feature can be implemented only as a part of the compositor.

There’s no support for window decorations in the protocol, so every client have to draw its own decoration (with it’s own shadow) manually. It’s not weston making a global window decorator impossible, it’s a protocol.

> The developers don’t object to tiling and window directions

Right. “I don’t object if you write a tiling WM, but it’s not a part of the protocol, so you’ll have to reimplement entire compositor in your tiling WM”. Things like monitor management, input device management, workspaces, taskbar, desktop backgrounds… are either implemented as a part of compositor (weston, or any other) or cannot be implemented at all.

And of course you can forget about tools like xxkb, xbindkeys, xdotool, xvkbd, devilspie, PyTile or tile-windows.

Also, wayland encourages client-side window decorations. So writing a tiling WM is not possible for wayland, until there will be support in the protocol to disable decorations for the window.

To fix all these issues wayland protocol must be fixed, it must include all these features. But if all those features will be actually implemented in wayland protocol, it may become as large as X11 is now.

The alternative is to drop the ideas of reference compositor and client side decorations, and split weston into a set of replaceable plugins (desktop, window manager, decorator, taskbar, etc). In that case it would be possible to allow others to use their favourite WMs/dockbars still having a simple wayland protocol. But simple wayland protocol will be supplemented by a complex wayland API.

> once GLX or EGL has provided a client with a graphics context, the client essentially owns the memory that is part of the context and can render directly to it.

But the very same code also works over `ssh -X`. How? (it’s not irony, I really wonder how it works then, and it’s a good thing to add to this article)

Guest, a lot of the features you want *will* be supported in Wayland. I saw on Phoronix a video of a BoF session featuring Hogsberg where he talked specifically about window decorations, for example. No one pretends Wayland is done, so criticism is a bit premature. Network transparency is definitely not coming, though.

> I saw on Phoronix a video of a BoF session featuring Hogsberg where he talked specifically about window decorations

I believe that most of the dissussions have had wayland developers stating that they are set on using client side window decorations(the applications draw the window decorations as opposed to the server, like they do on windows) to make things simpler and prevent tearing and this is what people object to. Especially the Kde developers, here is a good summary of the objections raised – http://blog.martin-graesslin.com/blog/2010/05/open-letter-the-issues-with-client-side-window-decorations/ . It’s about a fundamental difference of opinion on how things should be implemented. The Wayland developers have responded by saying this could be fixed by using a common library (for theming, behaivor, ect.) and some workaround for the force close problem.

Thanks a lot for writing this! I’ve been wanting to contribute to Mesa and Xorg for a while now, and this really helps in understanding how it all works together.

while linux’s graphic stack make me confuse, the sound stack do it much more

Thank you very much for that!

thanks for the writeup! one bug report though…

you wrote in the Xrender section: “(X11′s existing graphics were aliased)”

this is not a good way to put it (signal processing guys will cringe).

aliasing is an effect that happens when a high frequency signal (let’s say a black dot on a white background is discretized (converted into black and white pixels). this is a natural effect that can always happen when arbitrary graphics is rendered on a screen.

anti-aliasing means low-pass filtering the signal so e.g. sharp white-black edges are smoothed and will look less pixely – very important for text. so anti-aliasing is changing the graphics in order to make the rendering more smooth. you could easily do it without Xrender by doing the filtering yourself, but anti-aliasing support means you just flip a switch and it works.

sorry for being nitpicky.

tl;dr:

just write “X11 itself does not provide anti-aliasing support”

It’s just a colloquially way to put it. You understood what I meant.

Great write up, very informative. Thanks!

Just a typo in the second to last paragraph: “you could study the the geometry algorithms”

Otherwise, awesome article, Looking forward to the same for Gnome, or the Audio stack :)

> Sadly, the Intel drivers don’t use Gallium. My coworkers tell me it’s because the Intel driver developers do not like having a layer between Mesa and their driver.

Not so much “do not like” as “have benchmarked and found significantly slower”.

Gallium provides impressive performance benefits for software rendering and for hardware rendering on older cards, but on most modern graphics hardware it hurts performance.

I’d be very interested in some documentation and numbers on that. From coworkers, they say that Gallium does not affect speed as much as you think it would, and that most of the performance issues are not in the architecture.

Of course, hindsight is 20/20. There certainly could have been issues in Gallium’s architecture at the time.

Very good article, thanks for putting this together!

Nice article, and covering a lot of ground; one possible ‘correction’ is to note.. these are not the two only render paths (cairo and the varios GL options.) ie: “So, to be precise, there are two different paths, depending on the type of rendering you’re doing” is a little too ‘these are your two options”, when it could perhaps be written “So, to be precise, there are two -usual- paths, depending on the type of rendering you’re doing”

One could render direct to framebuffer (open /dev/fb or variations) and draw direct; one could use shared memory extension in X (MITSHM); there are others as well. Consider all those games using SDL, and SDL itself could then be directed to use framebuffer, X11, or other backends.

Most users would use X11 stack, with an optional GL for acceleration, but these are by no means the only methods.

Anyway, a quick nitpick only :)

If we want a hardware accelerated interface, that requires that we have some vendor-implemented interface to agree upon. Right now, OpenGL and X11 drawing are those interfaces, the latter only by necessity.

Still, the article is not ‘correct’ in its assertion of two paths; even with X11.. you coudl just use Xlib, or QT (no cairo), or dozens of other render methods, all hardware accelerated. Cairo is just one option (and a relatively slow one at that, not suitable to many low end devices such as the pile of netbooks, tablets, PDAs, mobiles, etc around..) — so I just think you need to be careful not to assert these are the two only methods, nor even the two most popular.. there are many others :)

ie: 3d rfendering with opengl .. well, most 2d rendering is also opengl these days (just to take advantage of it being hw accelerated, but projecting a purely flat surface.) Likewise.. 2d with cairo? well, you can do 3d with cairo, and 2d without cairo…

Just a small nit, but with just a couple of words, you’re over-asserting, is all.

I documented the XRender path because it’s the more common path in recent times. Raw drawing commands (XDrawLine, XFillPolygon) work in the exact same way, once it hits the server: a hardware-specific piece of code that draws anti-anti-aliased graphics.

I haven’t investigated Qt at all. Does its drawing API use XRender or OpenGL? If they want hardware acceleration, short of writing their own driver-specific code, they’d have to use one of these, so I’m comfortable in saying that the paths are mostly the same for Qt as well.

Jasper,

Thanks for taking the time and effort to put this together. Every time I wanted to get into the Linux graphics stack I would become overwhelmed and give up. You’ve provided an excellent foundation and I feel much more comfortable with my understanding of this topic.

Again, thank you and I can’t wait to read the other documents you whip up on the other stacks.

Thanks! This resolved many questions i had about all of these components, drivers and Xs. I like this kind of overview about… stuff :-)

Great overview, thank you. I tried to get into Linux graphics and/or Mesa development but it was overwhelming trying to understand the big picture. Another resource I found very useful is this book:

http://people.freedesktop.org/~marcheu/linuxgraphicsdrivers.pdf

(which was supposed to be completed during this event: http://www.x.org/wiki/Events/BookSprint2012).

Nice post. Not finished reading yet. Fix: s/to the drawing/to do the drawing/

Thank you very much Jasper. This is a brilliant article.

Thanks for this article, a good one, and saved hours of research and reading. You deserve a medal :)

Warning: I am an experimenter and a newbie so my question may lack quality, also English is not my first language.

I have this idea in my mind of a unified human computer interface. No longer will there be Windows/Unix but a combination of their parts in a single environment.

Now I am intrigued by the current state of control tools for windows applications.

Why can’t I decompose a window into it’s basic elements and then recombine those(still keeping their semantics and the hierarchy = think windows spy++ parent/child relationship) in whatever form I see fit.

Perhaps I want my code editor to auto-browse using Firefox for whatever word I have selected. And I only want the render window from Firefox – not all controls.

To be more specific I am currently looking to send graphics data from my Linux system to my windows desktop. I have seen XMING and I am using it but [ I want something light ].

Can I use XCB and windows graphics to make something like XMING?

Where can I get something like XMING simplified?

Thanks.

No. For Firefox specifically, it paints everything (like the tabs, address bar, what are known as “chrome” widgets) on the same surface as the web-page “content”. There’s no way for any app other than Firefox to know what’s what. Note that this isn’t a misfeature of Firefox; otherwise features such as Tab Candy or some specific types of Firefox Add-Ons wouldn’t be able to work in that situation. The Firefox developers aren’t morons; the web page content rendering system is split out from the rest of the engine (sandboxing and other features require it to be), and you can use the web page rendering system in other applications. Epiphany used to do this before it switched to WebKit.

Windows and OS X and Linux applications won’t ever be able to interact with each other for other, similar technical challenges. The system is structured differently, and applications are unintentionally programmed to those differences.

Paypal?

Wish list?

Your efforts here should not go unrewarded.

I’d consider wayland an interesting proof of concept. Surely you can come up with a X12 on top of it and re-implement nicely at least network transparency. Stopping at wayland seems to me wasteful.

Maybe just dropping what is not useful from the X11, fix some annoying part and keep what is good (and integrate what dbus provides in it somehow), and call X12 wouldn’t be that bad.

That’s precisely what Wayland is: the good parts of X11, plus a bunch of other fun features, in its own new world.

We could call it X12 if we wanted to, but that’s just dumb and misleading.

Little asking. Whats about multimonitor on desktop and on Laptop. Some Programs has at moment big Problems with more then One Monitore. Could Wayland solve this ?

I don’t know the status of an RandR equivalent for Wayland, but they’re working on it, I’m quite sure.

This has been very helpful. Please add a section for Clutter.

Also, it would be nice to have more graphics to show the relationships – at least of major components.

What do you need explained about Clutter? It’s just a toolkit that eventually works its way into OpenGL.

Pingback: Understanding Linux Graphics Stack « Multics69's Blog

Pingback: The open-source radeon(hd) driver and 3D games - Page 2

Thank you so much for taking the time to write this wonderful overview of the Linux graphics stack. This is exactly what I had been looking for. Please write more articles of this kind :)

Pingback: Linux Graphics Stack Questions

Thanks… although I’m using ubuntu for almost two years now, i’ve learned quite a lot here. abstract enough to read through with a comfortable pace (while sipping coffee) and enough details to know where to look for if in need for more information. Nice work!

Pingback: Valve cooking something big.... - Page 3

Pingback: Xplain | Clean Rinse

Pingback: Wayland in 3.12, and beyond | Clean Rinse

Pingback: Xwayland | Clean Rinse

Do you have an opinion on the best way to move the display and interactions of an application running on one machine to another physical machine? As an example, let’s say you have a web browser running on a host. You want to drag that web browser, with its current contents, history, et. al. to another display on another machine and continue using it. I’m not referring to a second monitor, rather another machine all together. It seems that an inelegant (slow) implementation might be to get and share the texture via TFP from the “host” machine to the second one.

“As you can see, we’ve split out quite a large bit of the original infrastructure from X’s initial monolithic behavior. This isn’t the only place where we’ve tore down the monolithic parts of X: a lot of the input device handling has moved into the kernel with evdev, and things like device hotplug support has been moved back into udev.”

I’m guessing by X you mean X11 here?

I actually meant the Xorg server. Nice find, though! Sorry about that.

Hi Jasper, thanks for sharing your knowledge. Being a Linux user I love learning new Linux stuff. Excellent article :-)

This might seem really dumb, but when the developers decided to rewrite X11, how come they didn’t just dump the baggage and rewrite the code, as a thin hardware layer. Sure that might have broken a few existing programs, but wouldn’t that have been easier than just starting from scratch like with wayland.

Because the abstractions that X11 provides are not the abstractions that modern applications want to work with.

Hi,

Thanks for the article. This is really helpful to understand linux graphics.

I have a single doubt not in your article but a related library, DirectFB. I heard that the DirectFB is going to be deprecated and I just can’t point out the place where directFB resided. My understanding is, it is a kind of cairo as a 2d lib, but it also support window system and input system like xorg. Is it okay to understand that the DirectFB is made of graphic lib + window manager? If you know about the deprecation of DirectFB, do you have any insights about why it is being deprecated?

Excellent summary that gives a broad overview of the linux graphics stack ….

Thanks for the great article :)

Thanks for this article and many other (including the Xplain series). I am proud to be this “niche” audience that reads your blog posts. Thanks again and looking forward to more insights from you!

Pingback: Xplain – Explaining X11 for the rest of us | 神刀安全网

Thank you for the good article!

I translated this article into Japanese, so I want to publish it on my blog. Is it OK? And if yes, can I copy the figures in this article to my blog?

Go for it, and I’d love to see the result! And yes, I give you permission to copy the figures as well.

Note that this article is a bit out of date, I might do an improved version at some point.

Thank you! And this is my post of the translation.

http://wagavulin.hatenablog.com/entry/2016/07/19/195955

Pingback: The Linux Graphics Stack – Joe Gardiner

Thanks for good articles!!

I’m looking for the way how to enable 3d acceleration in the guest os running on the virtualbox.

That guest os doesn’t have X-server, instead it has wayland.

And in order to use 3d acceleration in virtualbox, the guest os has ‘vboxvideo’ kernel module.

* https://www.virtualbox.org/manual/ch04.html#guestadd-3d

* https://blogs.oracle.com/fatbloke/entry/3d_acceleration_with_ubuntu_guests

When I tested, although it loaded vboxvideo, it couldn’t use 3d acceleration.

(note) I built mesa with this option ‘libdrm, –with-gallium-drivers=svga”.

I posted a question in the virtualbox forum. But there is only a mention that “the virtualbox doesn’t support 3d acceleration for guest os which doesn’t have X-server”. I thought that 3d acceleration depended on mesa and vboxvideo kernel module.

I don’t understand this, why 3d acceleration is related to X-server.

Very helpful, thanks for taking the time to share that knowledge with us :)

Nice Tutorial, it is helpful to the people like me the newbies. Let me through few question that comes while reading this tutorial targeting fresher.

How do I understand this statement better ? “.. It uses card-specific drivers to translate the API into a hardware-specific form”. could you kindly provide example?

How could I go about replacing X for Wayland? Because for me right now X11 is too slow at rendering stuff and makes everything jittery and lagging all over the place. Can’t watch anstandaed 720p video in Full Screen mode without it lagging frames, another thing to notice is that if I just simply drag a window across the screen while a 720p video is playing it’ll lag so hard you have screen tearing. I’m using NVIDIA’s proprietary drivers, but my CPU also has Intel HD Graphics, and the two don’t work together properly on Linux with Xorg to run as hybrid graphics. Another thing I notice too is that Xorg drains too much memory when running a standard 720p video, like I’ll go from normal RAM usage of around 20% to 98% and I have 8Gb of RAM available, I’ve had to create an additional RAM swapspace by creating a Swapfile on my drive to give me an additional 8GB RAM on top of that, which I really shouldn’t need to do to ensure the system has enough memory to read from. You can find out how to create a Swapfile just by reading it up on ArchLinux Wiki page. X11 is just so stupid and old and very outdated and is just no longer a viable option when I want fast response times in rendering stuff on screen on a 60Hz monitor. The response time of rendering is like 38ms. To top it all off the NVIDIA X Window Settings never stick to the settings that I want them to stay on across reboots and I have to constantly change it to “Prefer Maximum Performance” instead of “Auto”, and have to constantly set the GPU power to “Max Performance” by dragging to slider scale up, and uncheck “Clamping”