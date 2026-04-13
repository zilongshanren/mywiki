---
title: 'Build systems: Conclusion'
url: https://anteru.net/blog/2017/build-systems-conclusion
published: '2017-06-19'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

We’ve made it – the last post in this series! It’s been quite a ride, over the last weeks, we’ve investigated nine different build systems. Let’s summarize what we’ve seen. I’ve broken down the features into a couple of grand categories:

## Overview

**Portable**: Is the build definition portable across different compilers? This requires some kind of abstraction level from the underlying compiler, for instance, include directories being passed through variables, etc.**Modular**: Does the build system scale to larger builds? Can you write parts of the build independently of each other and then combine them into a bigger solution?**Ubiquitous**: Can you expect this build system to be available?**Type**: Does the build tool actually build on its own (in that case, you’ll see “Build” specified), or does it rely on other tools (“Generator”)?

| Tool | Portable | Modular | Ubiquitous | Type |
|---|---|---|---|---|
|

[MSBuild](https://anteru.net/blog/2017/build-systems-msbuild)[SCons](https://anteru.net/blog/2017/build-systems-scons)[Waf](https://anteru.net/blog/2017/build-systems-waf)[FASTbuild](https://anteru.net/blog/2017/build-systems-fastbuild)[Bazel](https://anteru.net/blog/2017/build-systems-bazel)[Buck](https://anteru.net/blog/2017/build-systems-buck)[Premake](https://anteru.net/blog/2017/build-systems-premake)[CMake](https://anteru.net/blog/2017/build-systems-cmake)## Survey results

Last week I’ve also started survey to get a better idea what people are
using out there “in the wild”. From the responses, the most popular
build systems by far are MSBuild (including Visual Studio), followed by
CMake and make. Given over 95% indicated they use Windows, this should
be no surprise, as MSBuild is the default system for the extremely
popular Visual Studio IDE. Still, CMake is showing up as a very strong
competitor, second to MSBuild in both availability *and* usage.

I’ve asked which language is used for the “build system glue” as well, and that answer is interesting as well. 50% use whatever their build system uses, Python, or shell scripts. Combining all shell script languages makes shell the most popular solution for the extra tasks the build systems don’t cover. The interesting bit here is although Python was really popular in this category, Python based build systems don’t seem to be interesting for developers.

## Wrapping up

We’ve looked at various build systems over the last couple of weeks,
and if there’s one thing we’ve learned, then this: There’s no “one
size fits all” solution, and for C++, there might as well never be
until C++ gets a standard ABI which will make library reuse a reality.
CMake has tackled this problem head-on with the “find module” concept
which is in my opinion one of the main reasons for its popularity. It’s
going to be interesting to see if other projects will just embrace
CMake’s approach or just migrate to CMake. Microsoft has heavily
invested in CMake providing a C++ package manager dubbed
[vcpkg](https://github.com/Microsoft/vcpkg/) which is completely based
on CMake. At the same time, large projects like the Unreal Engine 4 use
multiple fully customized build tools like the [Unreal Build
System](https://docs.unrealengine.com/latest/INT/Programming/UnrealBuildSystem/index.html).
I’m personally very curious to see how the ecosystem will evolve going
forward, and what features and concepts future build systems will bring
to the table.

To this end, I hope that you got a good idea of what we have today in
terms of build tools and their concepts, so you’ll be ready for the
future. That’s it for this series, thanks a lot for reading, and I’d
also like to thank my tireless reviewers for their help, in particular,
[Baldur](https://twitter.com/baldurk) and
[Jasper](https://twitter.com/jasperbekkers). Thanks guys!