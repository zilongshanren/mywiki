---
title: Mach v0.1 - cross-platform Zig graphics in ~60 seconds
url: https://devlog.hexops.org/2022/mach-v0.1-zig-graphics-in-60s/
published: '2022-03-26'
source_blog: Hexops' devlog
source_site: https://devlog.hexops.org/
category: graphics
fetched: '2026-04-19'
---

' devlog

Five months ago we announced some of our vision for Mach & [the future of graphics with Zig](https://devlog.hexops.org/2021/mach-engine-the-future-of-graphics-with-zig). Today we’ve reached Mach v0.1 with over 1,100 commits.

## Cross-platform graphics in 60 seconds

If you have [Zig v0.10](https://ziglang.org/) you can get started with cross-platform graphics in under 60 seconds, try it for yourself:

```
git clone https://github.com/hexops/mach
cd mach/gpu
zig build run-example
```


(not working? see [known issues](https://github.com/hexops/mach/blob/main/doc/known-issues.md#known-issues))

![](../../assets/3755b780a1247b8f.png)

## All you need is zig, git, and curl.

One key point we’re solving with Mach is the developer experience. We’re tired of people wasting hours and sometimes days getting the right versions of dependencies on their system in order to build projects!

![](../../assets/833b68577b108f65.png)

Our [glfw bindings](https://github.com/hexops/mach-glfw) build GLFW 100% from source using Zig. We even go so far as to build the DirectX Shader Compiler from source via Zig’s build system.

For the few inescapable system dependencies, such as `Metal.framework`

or `libx11`

, we [package them up ourselves](https://github.com/hexops/mach-system-sdk) and our build system knows how to fetch them as needed.

## Effortless cross-compilation

Because of our aggressive approach to solving dependencies, you get effortless cross-compilation to any OS literally at the flip of a switch:

```
$ zig build -Dtarget=x86_64-windows
$ zig build -Dtarget=x86_64-linux
$ zig build -Dtarget=x86_64-macos.12
$ zig build -Dtarget=aarch64-macos.12
```


The binaries you end up with are virtually static.

For Linux, Zig lets you target any glibc version, and musl too, so no more worrying if that binary will run on other machines.

### Unified graphics API (Metal, Vulkan, DirectX 12)

Backed by Metal, Vulkan, DirectX 12 & OpenGL (as a fallback), you get a truly cross-platform graphics API for Windows, Linux, and macOS (Browser and Mobile coming in the future)

![](../../assets/aa1a5bb9586f8b57.png)

### Unified shader language & compute shaders

There’s no need to write shaders for each graphics backend, instead you write shaders in a single modern language (WGSL):

![](../../assets/6ecbed630e5566ed.png)

With compute shaders, you have the ability to leverage computation on the GPU outside of graphical applications (machine learning, physics calculations, etc.) using a straightforward & approachable API that works with every GPU vendor.

### Behind the scenes

![](../../assets/2e80de9444cc0d15.png)

Mach [leverages WebGPU](https://gpuweb.github.io/gpuweb/explainer/), a successor to WebGL. WebGPU is an up and coming graphics API being built by Mozilla, Google, Apple, Microsoft, Intel and others.

Natively, Mach uses Zig as a C/C++ compiler to build [Google Chrome’s native WebGPU implementation](https://github.com/hexops/mach-gpu-dawn) and we use Zig’s build system so you don’t even have to deal with cmake/ninja/gn/etc.

Our infrastructure produces binary releases so you don’t even have to wait the handful of minutes it would take to compile by default. From-source builds are literally at your fingertips, though, just add `-Ddawn-from-source=true`

to your `zig build`

command.

`mach/gpu`

: the GPU interface for Zig

[mach/gpu](https://github.com/hexops/mach/tree/main/gpu) is our Zig interface to WebGPU and comes in at just over 250 commits.

![](../../assets/20bf418ee87b1358.png)

It provides a `gpu.Interface`

, similar to how Zig provides a `std.mem.Allocator`

interface, it’s backed by any implementation:

- A
`NativeInstance`

like Dawn (Google Chrome’s WebGPU implementation.) - (future) A browser implementation when targeting WebAssembly.

Imagine future implementations: maybe a pure-Zig implementation? Maybe a debugger implementation that *wraps an existing one* and streams all API calls to disk so you can replay them later and step through graphics API calls. Lots of possibilities here!

It’s a comprehensive interface, covering the 176 methods, 73 data structures, and 43 enum types that WebGPU exposes today - but there’s still much to do around documentation, fixing bugs, and ensuring we match the browser API nicely. but the foundation is all there!

## Zig ≈ greatness

Zig provides [some excellent runtime safety](https://ziglang.org/learn/overview/#performance-and-safety-choose-two) and catches many of the mistakes people make in C/C++ (memory leaks, integer overflow, index out of bounds, etc.)

In fact, we’ve caught several instances of undefined behavior in GLFW, and even [illegal integer coercion in the DirectX Shader Compiler](https://github.com/microsoft/DirectXShaderCompiler/pull/4178#discussion_r780733405) - all just by compiling C/C++ code using Zig.

The reason we’re *really* ecstatic about Zig, though, are what it promises us in the future:

- Blazing fast compilation, compiling and running a program faster than Python can interpret it - impressive!
[Hot code swapping](http://www.jakubkonka.com/2022/03/16/hcs-zig.html), how cool would it be to edit variables etc. as your game is running?

## Entity Component System

We’re building an Entity Component System [in a blog series](https://devlog.hexops.org/categories/build-an-ecs/) and inspired by:

- Data Oriented Design
- Database design
- Advice from the authors of
[Bevy](https://bevyengine.org)(a very popular ECS)

It’s still early stages, we’ve got some ways to go! But we’re [on our third major revision](https://github.com/hexops/mach/tree/main/ecs) and beginning to face the interesting problems. Keep an eye out for updates on that blog series coming soon.

## Sounds great! What’s the catch?

Mach (and Zig) are still very early stages! APIs are going to change and break. Mach is missing *a lot!*

- Documentation..
- Examples..
- Demos..
- Browser and Mobile support..
- ..Literally everything else that makes a game engine

If you’re looking for cross-platform graphics in Zig, Mach is for you! Otherwise, you’ll probably need to wait a bit.

## Getting started

Check out [the GitHub](https://github.com/hexops/mach) and in particular [this example code](https://github.com/hexops/mach/tree/main/gpu/examples).

There’s a ton of material out there about WebGPU already, check out [this excellent and comprehensive introductory article](https://surma.dev/things/webgpu/) and [these awesome samples](https://github.com/austinEng/webgpu-samples). It should be easy to map any of these to the Mach `gpu.Interface`

since it’s the same API, just Ziggified!

Join our [Matrix chat room](https://matrix.to/#/#hexops:matrix.org) to get help, discuss, etc.

## What’s next?

![](../../assets/5767199957d9890a.png)

My lightning talk in which I’ll be making the case for Mach engine and conveying the vision for where we go from here will be presented at the first-ever European [Zig meetup in Milan, Italy on Apr 9-10](https://zig.news/kristoff/zig-milan-party-2022-final-info-schedule-1jc1).

If like me you are unable to attend in person, the short video will be available afterwards!

## Help us reach Mach v1.0

Consider [sponsoring me on GitHub](https://github.com/sponsors/emidoots) if you like my work, so I can do more of it!

Join our [Matrix chat room](https://matrix.to/#/#hexops:matrix.org) to discuss ideas - collaboration very welcome!

Thanks for coming along in our journey!