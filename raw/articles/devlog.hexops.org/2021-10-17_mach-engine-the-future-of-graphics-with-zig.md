---
title: 'Mach Engine: The future of graphics (with Zig)'
url: https://devlog.hexops.org/2021/mach-engine-the-future-of-graphics-with-zig/
published: '2021-10-17'
source_blog: Hexops' devlog
source_site: https://devlog.hexops.org/
category: graphics
fetched: '2026-04-19'
---

' devlog

In the coming months, we’ll begin to have truly cross-platform low-level graphics, with the ability to cross compile GPU-accelerated applications written in Zig from any OS and deploy to desktop, mobile, and (in the future) web.

## Mach engine

![Mach: Game engine & graphics toolkit for the future](../../assets/d178db80ae0b5e50.png)

I’ve been working on [Mach Engine](https://github.com/hexops/mach) for about 4 months now, although it as a project is many years in the making, and I believe in the next 4-6 months we’ll have completion of the first key milestone: truly cross platform graphics and seamless cross compilation.

## Vision

Today, I share only the first milestone: Mach engine core. I’ve been working on this for around 1 year now, and we’re close (maybe 4-6 months away) from completion:

## Zero fuss installation & cross compilation

Only `zig`

and `git`

are needed to build from any OS and produce binaries for every OS. You do **not** need any system dependencies, C libraries, SDKs (Xcode, etc.), C compilers or anything else.

We’re able to achieve this thanks to two things:

- Zig has fantastic cross-compilation support, including its own custom linker
`zld`

written by[Jakub Konka](http://www.jakubkonka.com/)which is capable of supporting MacOS cross compilation. - Mach doing the heavy lifting of packaging the required system SDK libraries and C sources for e.g. GLFW so our Zig build scripts can simply
`git clone`

them for you as needed for the target OS you’re building for, completely automagically.

## Truly cross-platform graphics API

### DirectX 12, Metal, Vulkan & OpenGL

Imagine a low-level, little to no overhead graphics API that unifies DirectX, Metal, Vulkan, and OpenGL (if no others are available):

*This isn’t anything new:* all modern engines provide this, Godot has been working towards this for *years* (and still is), and there exist abstraction layers for Vulkan over most of these APIs as well.

### Vendor support

**An API is only as good as the momentum behind it.** What modern API can target the largest array of platforms with the most vendor backing?

**Microsoft sees DirectX as the future, not Vulkan.**(DirectX 13 is coming by the end of 2022.)**Apple sees Metal as the future, not Vulkan.**OpenGL and OpenCL are deprecated, and private legal arguments with Khoronos make it unlikely we’ll ever see OpenGL or Vulkan on Apple hardware ever again.- Google, with their Fuschia OS
[appears to be primarily into Vulkan](https://fuchsia.dev/fuchsia-src/concepts/graphics/magma)from a system-level POV. **NVIDIA, AMD, and Intel generally support as many graphics APIs as possible**, they want to sell hardware.

### One API that Apple, Microsoft, and Google can all agree on

Outside the bounds of traditional graphics APIs there exists an attempt to provide a unified API across all platforms, [WebGPU](https://en.wikipedia.org/wiki/WebGPU) (not to be confused with the much older *WebGL*).

Mozilla, Google, Apple, and Microsoft all got together to build an abstraction layer over the modern graphics APIs - finding the common ground between Direct3D 12, Metal, and Vulkan - plus a safe way to expose that functionality in browsers.

The name *WebGPU* might lead you to believe that this is only for browsers, and that it may not be low-level or fast - but this really couldn’t be further from the truth.

### Apple & Google’s role is what makes WebGPU unique, and why we chose it

What is new about WebGPU in my view is the vendors playing key roles in its development, and the fact that it grew outside the Khronos Group.

Although abstraction layers over modern graphics APIs are nothing new - as Apple, Google, and Microsoft continue to get more into manufacturing their own hardware (it’s clear this is a strategic move for them) we should ask ourselves how this will change the landscape, and WebGPU is the first cross-vendor API to be produced by this new ecosystem.

### WebGPU extended thoughts

## Is WebGPU "native enough"? Yes

For browsers, WebGPU will require sandboxing and validation layers. But in native uses, this can all be turned off, and the WebGPU developers are clearly thinking about this use case:

- Google's implementation of WebGPU,
[Dawn](https://dawn.googlesource.com/dawn), can be configured to effectively turn off all browser sandboxing / validation that could harm performance due to its client/server architecture. - Mozilla / gfx-rs Rust engineers have published articles such as
["The point of WebGPU on native"](http://kvark.github.io/web/gpu/native/2020/05/03/point-of-webgpu-native.html).

As for the quality of implementations, we could compare the amount of resources going into e.g. Google's WebGPU implementation vs. the amount of resources going into Unity/Unreal/MoltenVK/other graphics abstraction layers - but I suspect they're *about equal*.

## Will WebGPU be implemented on GPUs natively? Maybe someday

Not anytime soon. We get some insight into this [via @kvark](https://github.com/gpuweb/gpuweb/issues/847#issuecomment-642883924), a WebGPU developer:

[...] We are not in Khronos, and therefore we have limited participation from IHVs (only Intel and Apple are active). WebGPU was never designed to be implemented by the drivers. I mean, it would totally be rad, in the context of how usable WebGPU

[can be on native], but it couldn't be the requirement from the start.

But as WebGPU usage grows or even becomes prodominate due to it being the most powerful API in browsers, and as Microsoft, Google, and Apple continue to develop their own hardware - I think it's not unreasonable to think that it's possible some day WebGPU will be an even more direct 1:1 mapping between a cross-platform API and low-level APIs, more direct than Vulkan abstraction layers such as MoltenVK (which is required to get Vulkan working on top of MacOS's Metal API) - with the potential that some vendor starts asking "what would a GPU native WebGPU implementation look like?"

## Momentum of WebGPU vs. Vulkan

To [quote](https://news.ycombinator.com/item?id=23090432) [Dzmitry Malyshau / kvark](http://kvark.github.io/about/), a Mozilla engineer working on gfx-rs and WebGPU:

At some point, it comes down to the amount of momentum behind the API. In case of WebGPU, we have strong support from Intel and Apple, which are hardware vendors, as well as Google, who can influence mobile hardware vendors. We are making the specification and have resources to appropriately test it and develop the necessary workarounds. It's the quantity to quality transition that sometimes just needs to cross a certain threshold in order to succeed.


According to some, Nvidia and AMD tend to develop new features with Microsoft as part of DirectX. Only then are they "ported" back to Vulkan and OpenGL. I think that says a lot.

## What progress has been made so far on Mach Engine?

Today, we have cross-compilation of GLFW on all desktop OSs working out of the box with nothing more than `zig`

and `git`

:

This involved:

[Packaging MacOS SDKs](https://github.com/hexops/sdk-macos-11.3)and[Linux system X11/Wayland libraries](https://github.com/hexops/sdk-linux-x86_64)into SDKs, and creating Zig build scripts that could merely`git clone`

them and utilize them for cross-compilation.- Purchasing Apple M1 hardware to test on, and for GitHub Actions as it doesn’t support it.
- Normalizing symlinks in Mac/Linux SDKs everywhere so that Windows users don’t have a hard time with Git symlink management.
- Contributing
[a small fix to the Zig linker](https://github.com/ziglang/zig/pull/9734)

All this to say, we’re really taking a holistic approach to achieve this.

## What’s next? WebGPU

I’m happy to report that a fair amount of progress on this front has been made.

Here is Google’s WebGPU implementation, Dawn, compiled using `zig`

:
![A red triangle in a black window titled 'Dawn Window', the](../../assets/0fe05221aa07695c.png)

![A Zig code file, hello_triangle.zig showing Dawn and WebGPU API usage in Zig](../../assets/6c876dac76ab8835.png)


This includes:

- A ~500 line port of the
`hello_triangle`

example from Dawn to Zig - A ~1200 line
`build.zig`

file which compiles all the Dawn sources using Zig, without using Google’s ninja/etc development tools. - A hack to workaround a bug in Zig where ObjC++
`.mm`

files are not yet recognized. - C shims for the
`dawn_native`

C++ API and utility APIs, which are required in order to bind Dawn to an actual GLFW window.

There are a few weeks of work to do before this can be merged and will be usable by others, please stay tuned for that.

After that will be development of idiomatic Zig bindings to the [WebGPU C API](https://github.com/webgpu-native/webgpu-headers) which is shared between implementations such as Dawn and the Rust’s [gfx-rs/wgpu-native](https://github.com/gfx-rs/wgpu-native) implementation (we could theoretically switch between them at startup in the future, but we’ll probably stick with Dawn as it does not require a separate Rust toolchain and it would prevent out-of-the-box cross compilation.)

## When will there be games, examples, etc.?

It’ll be a while because I am focusing purely on the groundwork first. It’s unlikely you’ll see anything with *real demo value* before later next year.

I’m sure that will be disheartening to hear - and may make you to think there’s nothing of substance here. I totally understand that view, but I hope you’ll stay tuned because I’m in this for the long haul and it’s not my first rodeo (I previously spent 4 years writing [a game engine in Go](https://azul3d.org), and have worked [at a devtools startup for 7 years](https://sourcegraph.com), with my biggest lesson from of those experiences being the importance of demos and examples.

## Follow along

Major developments will be posted here.

You can also follow the project at [github.com/hexops/mach](https://github.com/hexops/mach).

If you like what I’m doing, you can [sponsor me on GitHub](https://github.com/sponsors/emidoots).

Thanks for reading!