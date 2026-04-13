---
title: Developing games on and for Linux/SteamOS
url: https://anki3d.org/developing-games-linux-steamos/
author: Panagiotis Christopoulos Charitos
published: '2013-12-23'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

Linux, or GNU/Linux as some people want to call it, was born 20+ years ago as an open source desktop operating system and despite its massive success on super-computers, servers, embedded and mobile devices it didn’t manage to gain the same traction on the space that was bred for, on desktop. Many people gave valid arguments on why desktop is a hard market to conquer but deep down I believe that video games is one of the most commonly desired features of a home computing system. Despite some notable efforts over the years Linux gaming never shared the same love as Windows PC gaming and console gaming but that may come to an end mainly due to Valve’s efforts to steer developers and gamers to Linux. As a Linux (game) developer for the past 6 years I think I can shed some light on the pros and cons of that system and who knows maybe some people will find this reading useful.

To be able to see and understand the big picture of developing on and for Linux we first need to identify the smaller areas that compose it. Things like tools (compilers, debuggers, libraries), hardware abstractions (graphics and sound APIs) and finally maintaining multiplatform capabilities are some key elements of that process. Keeping the multiplatform aspect of things in the back of our head is an interesting and sensible thing to do mainly because with careful planning and not that much effort a Linux application can be ported to other operating systems where the opposite may not be that easy.


## Compilers

Linux has a few notable and high profile compilers, projects with quite amazing quality and in most cases they surpass every closed source solution. The most known compiler is of course **GCC** (actually a number of compilers), a project that is older than Linux kernel and still going strong. The other two alternatives are **clang**, the C/C++ frontend of LLVM project and Intel’s C/C++ compiler.

The good thing about all these compilers is that they keep it close to ISO standards with GCC and clang picking the new specs quickly. Both clang 3.3 and GCC 4.8 support C++11 spec at its fullest. One interesting feature that all three compilers share especially GCC and clang is that they keep a command line compatibility also known as GCC compatibility. That practically means that the same command line arguments work the same for all compilers making them easy to drop and replace. I personally find quite useful switching from GCC to clang just to get some additional warning messages.

Working with all these compilers and even with different versions of the same compiler may prove tricky sometimes. The main problem that often surfaces is what you do with warnings. Some people treat warnings as errors in a way to enforce stricter rules. What happens though is that sometimes a newer version of the same compiler adds new warnings making the application uncompilable. Also clang is quite a warning Nazi. The most sensible thing to do is enable all the possible warnings but never treat them as errors.

All these compilers work on Windows as well as MacOS, clang is also the default compiler for PS4. On Windows however there is another notable C++ compiler from Microsoft, Visual C++. Developers that target Visual C++ first and then trying to port to a GCC compatible may end up being frustrated where the opposite is a bit easier. Microsoft is renowned for not following the standards and creating its own. Also, Visual C++ support of C++11 is also lagging far behind and this is something that needs to be taken under consideration.

## Build systems

The build system is essentially an unavoidable interface that lies between a compiler and the source code. On Windows and Visual Studio there are a number of clicks that set up your project and everything can be done though there but on Linux you will probably need something handwritten. Tools like **CMake, scons, premake** and of course **autotools** are available for that job.

I personally find **CMake** quite good mainly because I haven’t found a single scenario that it is unable to support. You can control compiler flags, you can include different source files depending on the platform you are compiling, you can include external libraries, you can produce executables and/or libraries, you can install and other nice features that I never tried out. One additional and important merit of CMake is its multiplatform nature and by that I mean to be able to produce makefiles for different systems including project files or Visual Studio. The learning curve is somewhat steep and the syntax a bit unconventional but once someone comprehends it CMake can be a very powerful and reliable tool.

## Integrated development environments

For people that come from Windows developing on a new operating system requires an integrated development environment also referred to as editor. To be honest Visual Studio is one of those products Microsoft should be proud of and Linux alternatives are quite difficult to compete. A few notable editors out there are **Eclipse, QtCreator, CodeBlocks, KDevelop, Netbeans** and a few dozen text editors.

**Eclipse** is a huge and very customizable IDE with plugins for almost anything out there. Using its extensive customization options it is possible to use custom makefiles or “connect” it with CMake. Also invoking the debugger from inside the IDE is quite a nice feature that Windows developers always enjoyed but on Linux the editor and the debugger was almost always decoupled.

The second notable IDE is **QtCreator** and it was originally created for writing Qt applications. Fortunately now you can write any C/C++ application you want with it. Compared to Eclipse it is lightweight with less options and emphasis on C/C++ where Eclipse has abstractions over everything. Also it is possible to invoke the debugger in a similar fashion as in Eclipse.

I personally used both Eclipse and QtCreator but at the moment I use something lower level, **VIM** (actually gvim). VIM is probably not something to recommend for every developer and for every project. But when used on a familiar codebase and with the right plugins VIM is a powerful tool. The fact that most Linux developers use either vim or Emacs proves that it can be a very good choice.

## Debuggers

When Valve asked game developers what they would like to see improved on Linux they replied “a nicer debugger”. On Linux and the rest of the Unix systems the de facto debugger is **GDB** (and moving to LLVM’s debugger) and everything interfaces with it including Eclipse and QtCreator. Though, I don’t quite understand why people chose GDB as their top thing that needs improvement (I think there are more pressing matters) but I can give some tips that can make GDB a bit easier to use.

By invoking GDB without extra parameters you will end up in a command line without being able to see your source code without typing some commands. But newer GDB versions have a command line option that splits the screen into two areas, the top with the source code and the bottom with the command line. To do that just add **–tui** to the gdb invocation command line. Even if TUI works fine it gets corrupted when the application prints to stderr or stdout. To reset the view a **CTRL+L** is enough to reset everything to its original state. Long story short, TUI with an occasional CTRL+L can make GDB quite bearable but learning the commands is something that cannot be avoided.

A nice alternative to GDB is a **CGDB**. A command line tool that, as everything else, invokes GDB behind the scenes (or it’s build with it, not quite sure). Compared to GDB+TUI CGDB offers syntax highlighting and some other nice features without being very different.

LLVM project is brewing an alternative debugger but at the moment it’s not 100% usable. LLVM’s debugger is again a command line tool with many similarities to GDB.

## Platform specific code and abstraction layers

Like every other operating system, platform specific code is something unavoidable and Linux is a Posix system and on desktop it is paired with X11 as its display server. Code that utilizes posix and X11 needs to be written but there are some nice libraries that act as an abstraction on top of every operating system that can ease the portability and maintainability.

For Linux the platform specific code consists of interfaces with X11 for displaying and input and with POSIX for threading, counters and filesystem operations etc. If the application is using C++11 the code for threading can be avoided by using the built-in threading library of C++.

One notable library that provides abstraction over platform code is **SDL**. SDL is a quite old project and recently it sees rapid development mainly because of Valve. The good thing about SDL is that it supports most things mentioned above over an easy-to-comprehend API. I’ve been using SDL for years but between version 1.3 and 2.0 it was missing shared OpenGL context support so I wrote my own X11 glue code (to be honest the shared context support is still under-documented and I may have missed it when using 1.3). A few months ago I went back to SDL because the shared context support appears to be implemented and secondly because maintaining cross-platform code for input (keyboard, mouse and controllers) is a huge pain.

## OpenGL and drivers

Most of the problems mentioned above are quite easy to tackle with the biggest pain to be as to how to utilize a GPU and produce the required visual fidelity a game requires. For Linux the one and only hardware accelerated graphics API is **OpenGL**. OpenGL is old, proven, it tries to maintain compatibility, it’s easier to understand, it can be quite fast, it has a nicer spec and it is multiplatform. On the other hand the need for compatibility introduced multiple interfaces for the same thing, conflicting interfaces (for example the texture and the program functions) and finally a quite bloated API (even on GL 4.x core, see texture functions). Also, in the past it used to pick new features either as experimental extensions or after Direct3D. Currently OpenGL 4.4 is on par with the rival Direct3D with a few somewhat small differences.

It is easy for an experienced OpenGL developer to choose the right interface and way for a specific job, the annoyance probably lies in the drivers. The quality of OpenGL drivers is a chicken-egg problem, they are buggy because not many developers use OpenGL and because not many develop with OpenGL the drivers are not tested and developed enough. Excluding mobile GPUs there are three major vendors, nVidia, AMD and Intel. nVidia provides quality Linux OpenGL drivers and at the same time quite fast. nVidia, especially in recent years, supports the new OpenGL versions much faster compared to the competition with beta drivers on every new OpenGL release. After all these years I never faced a problem with nVidia maybe except their over-relaxed compiler and generally their over-relaxed interpretation of the spec. AMD on the other hand tries to follow the spec closely but the quality of their driver is not in par with nVidia. However the two most annoying things with AMD is the fact that they don’t support new features as quickly as their immediate competition and the second is that the performance is significantly lower always compared to nVidia GPUs of the same grade. I haven’t had any experience with Intel GPUs to be honest, the fact that the opensource Mesa drivers pick new features at a slow pace never aligned with the feature-set AnKi required at any specific time.

The main point of friction between OpenGL implementations, and something that Direct3D has already solved, is the differences between GLSL compilers. It is almost certain that shaders that compile in X implementation need changes to work in Y. Khronos group understands that this is a common problem that developers face so it endorses a GLSL parser called **glslang**. At the time of writing glslang is somewhat hidden under Khronos public repositories and not yet advertised. Hopefully that may change in the near future and developers will make use of it. Apart form glslang Mesa’s compiler also got a re-factoring in order be able to work as a standalone executable, decoupled from the rest of Mesa stack.

OpenGL compared to OpenGL ES requires some sort of massaging because it doesn’t expose all functionality in the normal shared-library way but in an extension-like way. By using for example **GLEW** things can become very very easy. Just compile your game with glew.c and include a single .h file and you are good to go.

## CPU profiling

Linux has a wide variety of profiling tools and to be honest I haven’t used every single one of them so this chapter will not present what works best but merely what I used and found good enough. The first tool that, among other cool things, does profiling is **valgrind** plus callgrind plus kcachegrind. After running an application through valgrind/callgrind you get a binary file that can be viewed with the excellent and very usable kcachegrind. Valgrind is not counting by polling the hardware CPU counters but by emulating a CPU, this of course implies that the reported numbers may not represent the reality but experience showed they are close enough. Other tools are perf, oprofile, gperf tools, VTune and other.

## GPU profiling

At this point is where things get really really ugly. There are not many OpenGL profiling tools for Linux and this is something that I don’t see changing dramatically. nVidia always had nice software to offer along with their GPUs but apart from some OpenCL and Cuda tools I haven’t spotted something for OpenGL. AMD seems a bit more serious with its **CodeXL** suite (ex gDebugger) but since I don’t own an AMD GPU is quite difficult to test for myself.

The situation on desktop leaves things to be desired especially compared to what mobile vendors offer for Linux. I often found myself using **ARM’s Mali offline compiler** in order to count shader GPU cycles and despite the fact that this compiler is meant for a mobile GPU architecture it helped me optimize some shaders and eventually increase the FPS.

What I would like to see happening is nVidia moving the same functionality of Windows Nsight to Linux and AMD continuing their good work. Also an offline compiler that counts cycles can be extremely useful.

## Footnote

Working in companies that use Linux internally I often find new colleagues with Windows background accepting and eventually loving the Linux experience. After all, Linux was created by developers with their own needs in mind and this spawned a very developer friendly operating system. All the libraries are precompiled and a few clicks away (using a graphical packet manager) and the shell is a powerful companion tool. The truth is that Linux and it’s tools are somewhat difficult to master but gaining that kind of experience is much more rewarding and in the long run it will lead to increased productivity.

For most scenarios developing using Linux is a fun experience but when it comes to game and graphics development there are things to be desired. Game development always was a Windows affair for a number of reasons but given better drivers and a few profiling tools I strongly believe that Linux can become an experience that will pay of.

That is all from me, for comments, corrections or whatever leave your comments.