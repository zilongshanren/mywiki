---
title: Build engineering
url: https://anteru.net/blog/2010/build-engineering
published: '2010-07-19'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Do you have one-click-builds for your whole project? That’s a good question (so good that[ you should ask it before you get employed](http://joelonsoftware.com/articles/fog0000000043.html)), but if the answer is no, chances are high that your team has not dedicated enough time to build engineering.

So what’s that, build engineering: My take on it is that it’s basically everything until you can actually start working on your code. That’s a quite weird definition, so let’s give me an example: A build engineer should take care of the SCM solution, track all dependencies, write docs, write all build-related tools and make sure that any developer can get up & running very quickly. Moreover, the build engineer should take care that it is easy for developers to add new tests and files to the current project without having to synchronise anything.

Interestingly, most teams don’t seem to consider this too important. Running a test requires this huge command line, so what? Adding a new file means editing the Makefile and the Visual Studio project, breaking Linux half of the time … and similar issues. Bigger problems crop up as well, like project 23 being compiled with slightly different compiler settings, causing weird runtime bugs. Worst of all, the time to get up and started from scratch is measured in hours, as you need to set up huge amounts of dependencies and/or system settings (environment variables, anyone?) In this post, I’ll describe my take on build engineering, and how I cope with typical problems.

## SCM and dependencies

The first thing you need is a good SCM solution. I’m using [Bazaar](http://bazaar.canonical.com/) for this, which is easy to learn, fully distributed and comes with nice UI tools. At work, I’m stuck with SVN for some projects, which is decent, but I really like [the new features that distributed SCM provide](https://anteru.net/blog/2010/03/08/634/). All of the source code of the project is available from a single repository, so this is what every developer has to check out. However, I have not checked in all dependencies into the SCM: For Boost and Qt, developers have to build it on their machines. In order to make this as simple as possible, I’ve documented the exact build command lines on our local knowledge base. There’s always a trade-off here; what might be useful is support for external repositories (basically, they seem to be part of the repository, but are stored elsewhere.) Both Boost and Qt compile to huge amounts of binaries, so I think this is a reasonable trade-off here.

However, there are still some dependencies left; for instance, in one project we use [Cg](http://developer.nvidia.com/object/cg_toolkit.html), which comes as binary-only. Checking in the binaries is possible, but I wouldn’t recommend this, especially for DVCS systems where each client will have to store the fully history of each binary … so we’re using a lightweight tool which fetches the binaries off our server. They’re packaged manually into a compressed file, downloaded during the build (if they’re not already installed on the target machine) and cached on each developer’s machine. All other dependencies (zlib, etc.) have been integrated into the source tree. On Linux, the system libraries are also ignored to avoid version mismatches.

## Build system

I’m using [CMake](http://cmake.org/) as my build system everywhere now. If I get legacy code with another build system, I convert it to CMake right away. To make this simpler, I typically keep some “sample” projects around and copy new projects into it (for instance, I have a very simple DirectX 10 app from which I derive the CMakeLists for new DirectX applications.) CMake has one major advantage over competing systems: It allows you to use your normal IDE without problems. You can still use Visual Studio 2010, with IntelliSense and debugging working, which is typically a large hassle with other build tools.

## Glue

No matter how great your build system is, at some point you’re going to run into cases where you have to extend it to get some functionality. For instance, I have one case where I need to scan `.cpp`

files for `TEST()`

macros and generate a test registry from that. This is where the build “glue” comes into play.

I used to have the “glue” tools written in C#, but I’ve totally switched to [Python](http://python.org)-based scripts now. Having the tools in C# has the nice advantage that development time is pretty low (after all, you can use the full .NET framework as well as Visual Studio), but I had to check in binaries at the end so the user didn’t have to fire up Visual Studio first, then CMake, then Visual Studio again … and despite Mono being available on Linux, I ran into quite a few issues where something wasn’t supported or required a newer Mono build.

Switching to Python turned out to be a good decision here, and I even believe now that there isn’t too much difference in development time between C# and Python. For command-line tools, I would even argue that Python is easier – for instance, there’s a built-in option parser in Python, but none in C#. I’m also using Python for code generation using a small custom template engine (I hope to find time to get the source code public some day.) There’s also a bunch of helper tools which are not directly invoked during the build, but still useful (for instance, I have a small tool to generate a header/source file skeleton) – all of them are in Python as well. For the record, I’m using Python 3.1, so the build tools should continue to work for the next few years at least ;)

## Closing thoughts

Never underestimate how much plumbing your build process will need. Over time, your build requirements will grow, as your project(s) becomes bigger, and the more tools and utilities you can re-use, the easier it’ll be. Ideally, you should have at least on dedicated engineer on your team who is responsible for building, and who keeps track of everything necessary to get started. Most developers should have only very small parts of the build system which they modify (i.e., add source files to a project), while the rest should be managed by a dedicated group. This way, you can usually avoid the situations where an innocent looking modification to a high-level build script breaks someone else’s work.