---
title: Porting from Windows to Linux, part 3
url: https://anteru.net/blog/2014/porting-from-windows-to-linux-part-3
published: '2014-02-21'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Welcome to the final post of my porting from Windows to Linux series. At this point, I assume you have built your application on Linux. If not, keep on porting :) Otherwise, read on for hints on how to keep your Linux and Windows build working, and how to take advantage of the fact that your code is working on Linux now.

## Code quality tools

Having your code on Linux means you also get access to Linux-specific tools. There are three tools I want to talk about which you should know:

- Clang
- Valgrind
- Address/Thread Sanitizer

Let’s start with [Clang](http://clang.llvm.org/). Clang is a production-quality C++ compiler built on top of the excellent [LLVM](http://llvm.org/) framework. It has full C++ 11 support, provides useful error messages and compiles faster than any other compiler I’m aware of. For portability, it is always useful to check against more than one compiler, and once you have ported over to Linux, using Clang for compiling is trivial. If you use CMake, you can just specify the native compiler to be clang++ instead of g++ and you’re ready to go. You can expect roughly 20-30% faster compile times.

[Valgrind](http://valgrind.org/) is a memory validation tool (it can be also used for profiling.) Basically, Valgrind runs your application and interprets every instruction. At the end, it can report memory leaks, uninitialized memory reads and other memory errors with complete call stacks back to you. The downside is that your code is going to run at least one order of magnitude slower. This makes it not that useful for testing complete applications, but it’s great for your unit and functional test suites! While Valgrind cannot detect all errors, it’s the tool to detect heap memory leaks and other issues.

As said above, Valgrind makes your code at least 10x slower. This has (recently) led to the development of new sanitization tools like the [address sanitizer](http://code.google.com/p/address-sanitizer/wiki/AddressSanitizer). Instead of executing the whole code in a virtual machine, the address sanitizer instruments load/store instructions. The compiler also has to cooperate, but fortunately, both Clang and GCC support the address sanitizer. Due to the instrumented code, the resulting binary is much faster than running it under Valgrind. The only downside is that it needs a recompilation – you’ll basically get a new build configuration for extended debugging. I haven’t used it enough on my code to talk about results yet, but if you ask whether it’s worth it, I’d suggest you look at [the list of bugs found using address sanitizer](http://code.google.com/p/address-sanitizer/wiki/FoundBugs). Similarly, there is also a new thread sanitizer which will hopefully be just as useful for thread synchronization bugs.

## Build automation

If your build is not fully automated, you should be definitely thinking about this now. As mentioned above, Linux provides several great tools which can be used to automatically check your code, but these tools are only useful if they run regularly. Moreover, once you start supporting Clang and GCC on Linux, and MSVC on Windows simultaneously, chances are high that one of the configurations will break at some point.

The way to combat this is to rely on build automation. You might think that you have enough people working on the code to capture all issues, but that’s not enough. With Clang, GCC, MSVC, debug, release, Valgrind and address sanitizers you already have a build matrix consisting of 14 possible configurations – some of which are a pain to work with, like a debug build with Valgrind. Take your time and set up a server which builds all configurations over night. Ideally, your nightly builds will also execute the unit test suite, so you can capture both compile errors as well as runtime errors. If you need a cross-platform build tool, I can recommend [Buildbot](http://buildbot.net/), which does its job and is reasonably easy to configure.

This concludes the porting to Linux series! If you still have questions, feel free to comment and I’ll try my best to address them.