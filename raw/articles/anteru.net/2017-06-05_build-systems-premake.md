---
title: 'Build systems: Premake'
url: https://anteru.net/blog/2017/build-systems-premake
published: '2017-06-05'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Welcome back to another post in the build system series! So far, we’ve looked at many different build systems, but all of them had one thing in common: They did build the project all by themselves, no other tool was required. I’ve hinted a bit at generating build files in the [Make](https://anteru.net/blog/2017/build-systems-make) entry, and today, we’re going to look at a build tool which is actually a “meta” build tool – all it does is generate build files for other build tools. I’ve picked [Premake](https://premake.github.io/) to showcase this new concept, as it’s literally the name of the game here ☺

## Build generators?

It might seem a bit weird at first to build a build tool which then requires another build tool to be invoked, but if we look a bit closer, there are good reasons for this separation. As I mentioned in the [intro](https://anteru.net/blog/2017/build-systems-intro), the goal of a build system is to transform some data using some commands. We saw how [Make](https://anteru.net/blog/2017/build-systems-make) and [MSBuild](https://anteru.net/blog/2017/build-systems-msbuild) focus on implementing that goal and not much else. By separating the build execution from the build script generation, we can have two focused tools, instead of mixing high- and low-level concepts together. The other build tools we looked at all have some task and dependency engine *somewhere*, but it might not be directly accessible, making it hard to understand what exactly is being executed in the end.

There are various advantage of going “meta”, one being *portability* between systems. On Linux, Make is super popular, on Windows, MSBuild is the default, and if you want to target both, it makes sense to generate the files from a single source. Especially once it comes to supporting multiple versions of the same tool – Visual Studio 2013, 2015, 2017, for example – being able to just generate the files reduces the maintenance burden a lot.

Another major advantage of splitting the generation from the execution is performance. We already saw build systems splitting the initial configuration into a separate step from the actual build when we looked at [Waf](https://anteru.net/blog/2017/build-systems-waf). In general, the build description will change only rarely, and by making the build description minimal, we can improve the daily build experience. In fact, this very idea is what lead to the development of [Ninja](https://ninja-build.org/), a super low-level tool similar to Make, which is *designed* to execute machine generated build scripts.

## Sample project

Let’s see how Premake differs from the other tools we’ve used so far. On the build file side, Premake uses a scripting language to allow for easy high-level customization. Here, it’s Lua, and the build files are actually Lua scripts which are interpreted at generation time. After generation, Premake writes a build file for the tool you’ve selected, which then needs to build once more. One feature of Premake is that it writes *portable* build files, so you can use it as a generator for build files which are then shipped, removing the need to invoke Premake on the developer’s machine. Next week, we’ll see a different approach to build files where they are treated as an intermediate output only.

The actual build description looks very similar to what we’ve seen before. As usual, we’ll start with the static library here:

```
project "statlib"
kind "StaticLib"
language "C++"
```


We tell Premake we’re building a static library in C++, nothing special so far. Next up, we define the source files:

```
files {"StaticLibrarySource.cpp", "%{cfg.buildtarget.directory}/table.cpp"}
```


He we have our generated file, specified just “as if” it already exists. We don’t specify the actual generation script for it, instead, we use a “pre-build” command which will be executed before the build runs to generate this file. This way, we side-step the issue of specifying build-time dependencies inside Premake. Premake will write a build description which assumes the file to exist, and ask the underlying build system to produce it in a pre-build step, but Premake is not going to provide the actual dependency to the build system. This means that it will get rebuilt no matter what. This can be also seen from how we specify this:

```
p = path.getabsolute (os.getcwd ())
prebuildcommands { ""C:\\Program Files\\Python36\\python.exe" " .. p .. "/tablegen.py > %{cfg.buildtarget.directory}/table.cpp" }
```


We invoke Lua to get the current working directory, so we can run the Python executable with the correct path. We don’t tell Premake about what is required to build the table, and what outputs it produces, we just pass on the raw command line and ask Premake to execute it.

That’s it for the static library – unsurprisingly, Premake requires just as much information as any other tool we looked at to generate correct build files. That’s it for Premake, the reminder of the build description will look very familiar to you if you’ve been following this series so far. As always, head to the [sample repository](https://github.com/Anteru/build-systems/tree/master/premake) for the build definition.

With this, what is left in terms of build systems? There’s still one problem we had in all the systems so far, which is finding binaries and dependencies, that none of the build systems have tackled so far. Next week, we’re going to investigate this issue in a lot of detail – stay tuned!