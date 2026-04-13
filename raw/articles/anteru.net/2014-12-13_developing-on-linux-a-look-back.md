---
title: 'Developing on Linux: A look back'
url: https://anteru.net/blog/2014/developing-on-linux-a-look-back
published: '2014-12-13'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Since nearly one year now, I’m using [Linux as my main development environment](https://anteru.net/blog/2014/07/01/2445/). Time to look back at the core development experience, which is quite a bit different than on Windows.

## Build systems

I use [CMake](http://www.cmake.org/) exclusively for all my projects, and this works equally well on Windows an Linux. The build itself is done using [ninja](http://martine.github.io/ninja/), which is quite a bit faster than Visual Studio and has less “dependency hiccups” – that is, situations where an updated file would not result in a correct rebuild. On this side, nothing really interesting, build systems on Linux are just as sophisticated and robust on Windows. A minor advantage for Linux is that CMake finds most libraries automatically, as there are placed in standard directories.

**Update**: Examples why I hate MSBuild:

- A “null” build which just invokes my unit tests takes 4-6 seconds on Windows, 0.5 seconds on Linux (on Linux, all unit tests execute in parallel plus 100ms overhead for the build system.)
- If you have a library everything depends on, MSBuild will build this library with a single thread and not continue building the rest until this one library is built. In general, MSBuild cannot invoke the compiler on C++ files unless the dependencies have been linked.
- Parallelization is split between
`/MP`

(within a project, the compiler will parallelize on its own) and projects (what the build system sees and uses). You can never get 100% perfect core utilization, only severe under- or oversubscription. On Linux, the build system “sees” all individual actions (compile file, link file) and can schedule them perfectly.

## Compilers

I use two compilers on Linux: [GCC](https://gcc.gnu.org/) and [Clang](http://clang.llvm.org/). Both are really robust, produce efficient code and have reasonably good error reporting. Clang still wins by a small margin on the error reporting. Unfortunately, I can’t use Clang as the production compiler as it still lacks OpenMP support, and several of my tools rely on it. However, I keep my projects building with both Clang and GCC to benefit from better error coverage and tooling – more on this below.

Stability wise, I didn’t have a single internal compile error in the last year on Linux, as well as no problems with unsupported C++. In comparison, I did have several issues with Visual C++ not accepting correct C++11 in the same time (mostly related to initializer lists.) Right now, I’m using Visual Studio 2013 as the base feature set, as I have to keep a Windows version working for the graphics stuff, but even the base feature set in Visual Studio 2013 is not as solid as I would hope it to be. At least Microsoft seems to be improving this situation quickly, and with [Visual Studio now free on Windows](http://www.visualstudio.com/products/visual-studio-community-vs), I’ll keep it as a target platform for the foreseeable future.

Performance wise, Linux is a clear winner. This may be related to the kernel, the scheduler, the memory manager or the compiler, I don’t really care, but the final result is my code runs quite a bit faster in general than on Windows. And with quite a bit I mean differences of 30% on exactly the same hardware – which is more than enough reason to port over to Linux. I don’t know where Visual Studio is loosing exactly, but even for simple code with a few structures and stuff, Clang and GCC seem to regularly produce much more efficient binaries than Visual Studio.

One major difference is that the compilers on Linux will embed debug information and symbols by default into the binaries and executables. This is something I don’t like too much. [PDB](http://en.wikipedia.org/wiki/Program_database)s might not be the best solution, but they do work nicely and make it unnecessary to strip binaries before handing them over. Valve described [their approach to set up a symbol server on Linux](http://www.youtube.com/watch?v=xTmAknUbpB0&list=PLckFgM6dUP2hc4iy-IdKFtqR9TeZWMPjm) at the Steam Dev Days, which I haven’t implemented yet – definitely something I want to check out soon. While we’re on debug information …

## Debuggers

This is the really sad part of this blog post. In fact, right now, I have no working debugging environment on Ubuntu 14.10. How did that happen? Well, [GDB](http://www.gnu.org/software/gdb/) is choking while demangling symbols in my framework (see for example [here](https://sourceware.org/bugzilla/show_bug.cgi?id=17708) and [here](https://sourceware.org/bugzilla/show_bug.cgi?id=17157)); while [LLDB](http://lldb.llvm.org/) is plain broken on Ubuntu 14.10 (see [here](https://bugs.launchpad.net/ubuntu/+source/llvm-toolchain-3.5/+bug/1385876) and [here](http://llvm.org/bugs/show_bug.cgi?id=20400#add_comment)).

Demangling seems to be a really popular issue for both debuggers, if you look at the recent entries. This is really surprising for me, as the tools are developed in conjunction with the compiler, and you would expect them to be written in-sync and tested together (i.e. when a new kind of symbol appears with a weird mangling, you would expect a test to be written that the demangler can handle it.) This, together with the fact that the debuggers are often plain unstable (i.e. they simply stop debugging) makes debugging on Linux a real nightmare compared to Windows.

There’s one more nail in the coffin, which is barely functional stepping and variable inspection. Especially GCC seems to aggressively remove variables even in debug builds (or it does not emit the correct debug information to allow GDB to find them) which makes debugging hard; together with instruction reordering, debugging becomes next to impossible. I had multiple occasions where I would step through a program just to jump back and forth through it as instructions were executed in a different order than written in the source code.

Compared to Visual Studio or even [WinDBG](http://en.wikipedia.org/wiki/WinDbg), Linux debugging significantly lacks in two areas: Robustness first and foremost, variable inspection second. Robustness for debuggers is absolutely critical. I had very few occasions on Windows where Visual Studio would not debug correctly, and in those cases, WinDBG would do the job. On Linux, I had countless issues with debuggers ranging from not updated variables to plain crashes, often forcing me to resort to “printf” style debugging to get any work done.

Second, inspecting program state with the current crop of Linux debuggers is really cumbersome. There should be a standard way to format the display of variables. Visual Studio finally got it right with the [native visualizers](http://msdn.microsoft.com/en-us/library/jj620914.aspx); whoever tried to write a visualizer for GDB or LLDB will have noticed this is way harder than it should be. Documentation is less than sparse, and it requires far too much script code to get anything useful. Plus, developing and testing of visualizers is very time consuming.

For me, it’s pretty clear why the debuggers on Linux are still that bad: Writing a debugger is among the least sexy tasks in compiler development. A good debugger requires good compiler support, but nobody goes ahead and brags about how correct the DWARF info generation is; people are much more likely to write about new optimizations or new features (in the last three LLVM developer meetings, there have been only one full talk on debugging, and only very few BoF/Lightning talks.) Second, the compiler must be written with the debugger in mind, which means lots of boring work on the compiler side. Microsoft can just pay developers to buckle down and do it anyway, but getting people motivated in the open source community for this is much more difficult.

## IDEs

I use [Qt Creator](http://en.wikipedia.org/wiki/Qt_Creator) on Linux, which is good enough for most work. On Windows, Visual Studio sets the bar for IDEs, especially for C++. There’s simply nothing getting close. While Qt Creator has a decent programming experience, the weird window layout (no toolbar, no docking windows, etc.), the bad debugger integration (together with the debugger problems mentioned above) and the substandard C++ coding support (IntelliSense is faster and provides help in more areas) needs to get a lot of work to be on-par with Windows. [KDevelop](https://www.kdevelop.org/) shows that the [C++ integration can be much better when Clang is used](http://milianw.de/blog/katekdevelop-sprint-2014-let-there-be-clang), but Qt Creator and Clang is not there yet.

I would also wish Qt Creator would remove the stupid left hand toolbar and replace it with a “normal” toolbar, plus add some docking windows so I can take advantage of two screens while debugging. That said, I’m still productive in Qt Creator, and probably not slower than I’m in Visual Studio. The difference while writing code is really minuscule, and with faster rebuilds, it’s probably even a tiny win for Qt Creator. This all breaks down of course when it comes to debugging, where I’m easily only half as efficient on Linux as on Windows.

## Profilers, validators, etc.

Back to better news. Profiling and validation. For profiling, there is ‘[perf](https://perf.wiki.kernel.org/index.php/Main_Page)‘, which is decent to get a quick idea what is going wrong. For serious profiling, [Intel’s tools](http://en.wikipedia.org/wiki/VTune) are just as good on Linux as their are on Windows. What’s lacking on Linux are good system monitoring tools – these are scattered around in various places. Windows has the [Windows Performance Analysis](http://msdn.microsoft.com/en-us/library/windows/hardware/hh162981.aspx) tools, which group everything under a common UI. On Linux, it’s pretty clear that everything has been developed in isolation and there hasn’t been a guiding hand behind all the stuff which would enforce a common design. This is improving with ‘perf’, which will be hopefully what the WPA toolkit is for Windows. My major gripe with perf is the lack of visualization, which quickly requires to resort [to scripts to get some semi-interactive SVG output](http://www.brendangregg.com/FlameGraphs/cpuflamegraphs.html).

Validation wise though, Linux is a clear winner, with the holy trinity of tools: [Valgrind](http://valgrind.org/), [Address Sanitizer](https://code.google.com/p/address-sanitizer/) and [Clang Static Analyzer](http://clang-analyzer.llvm.org/). Valgrind is basically reason enough to port your work to Linux, and combined with the Address Sanitizer, memory corruption simply becomes a non-issue. There is one small problem with ASAN and Valgrind, which are proprietary tools and libraries – for instance, your good old vendor-provided graphics driver. These can seriously mess up with the analysis (in case of ASAN, it will abort early – usually long before anything interesting in your own code happens.) The only way to solve this is to write long ignore files for Valgrind; for ASAN, you can hope to stub out the offending library or convince the vendor to use it themselves, but that’s it.

The Clang Static Analyzer is similar to the Visual Studio analyzer, but at least in my experience, it finds more issues, at the expense of more false positives.

## Closing remarks

So, looking back on my development experience on Linux, there are two areas where Linux is a clear winner for me: The build system is just so much better than MSBuild that it’s not really funny, and the tool support is just great. I found numerous weird issues on Linux in seconds which would have taken me hours to track down on Windows. I used to fear uninitialized memory issues, but now, with ASAN and Valgrind, they have become a non-issue.

Debugging wise, the situation is really bad though, and while most can be done with command line debugging or printf, I sometimes have to resort to Windows and Visual Studio to get stuff done in reasonable time. This is really not a good situation.

Compilers on Linux are better, but Visual Studio 2013 is sufficiently close that I don’t feel like I’m limited on this front. With [Clang gaining native Windows support](http://clang.llvm.org/docs/MSVCCompatibility.html), the advantage for Linux on this front is going to be zero. Performance is a different story though, with my Linux build regularly outperforming my Windows version by 30% or more.

Overall, the thing I like most on Linux is the instantaneous turnaround with ninja build, which is a real productivity boost. Together with the better net performance I usually get, it’s enough to keep me on Linux, but the bad debugging experience and the lack of a polished IDE are getting increasingly frustrating. The IDE is not the main problem here, but debuggers on Linux are at a point where some bugs are near impossible to track down in a reasonable time – a situation which clearly has to change.