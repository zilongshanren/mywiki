---
title: Rust Game Series - Part 9 - Rust compilation structure
url: https://www.jendrikillner.com/post/rust-game-part-9/
author: Jendrik Illner
published: '2020-04-06'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

The project structure is often neglected when starting on a new project, especially for small projects, but I feel it’s essential. Rust provides two main building blocks:

- Crate
- Module

A Crate is the highest level, and each Crate contains one or more modules.
The details are well explained in the [Rust Book](https://doc.rust-lang.org/1.24.1/book/first-edition/crates-and-modules.html)

Looking at the current state of the game code, we have a few logical blocks:

- Game code
- Window creation logic
- Graphics foundation layer
- Memory management
- Shader interface
- A few extensions to the Rust standard library

The first idea might be to keep everything inside a single `rustmatch3`

Crate and move the other functionality into modules.
This is what I would do for a C++ project of this complexity.

In Rust, I am going to follow a different design and split this code into multiple Crates. The reason for this is the difference in the compilation unit size between Rust and C++.

In C++ each .cpp file is a compilation unit. In Rust, the compilation unit is a Crate.

The compiler is invoked once for each compilation unit. Therefore scaling to multiple cores is trivial for C++ as there are typically more files then there are cores.

The Rust compiler (Rustc) will only be invoked once per Crate. Therefore scaling to multiple cores for a single crate can only be achieved through multithreading within the compiler itself.

To understand how good the Rustc compiler is at using available CPU resources, I ran some tests.

## Rust Compilation - Test Case - Image Rescaler

The following example is taken from one of my smaller Rust based tools. It is a simple tool that rescales images to a resolution suited for publishing on the web.

![Image rescaler compilation timeline Image rescaler compilation timeline](../../assets/d2ecf86860e0df2a.png)


The upper half of this capture shows a timeline of which crates are being compiled. The lower half shows the status of the compilation units and the CPU usage over time.

From these graphs, we can see that the system is fully saturated at the start. Not surprising as the number of active units is always at the maximum value for my machine.

As the number of active units drops, however, so does the system utilization.

Especially insightful is the image crate. It takes around 16s to compile. Out of these, 7 seconds are spent on phase 1 of the compilation, and the rest is spent on phase 2.

The Rust compilation is split into two high-level phases:

- Phase 1: generates metadata (list of types, dependencies, exports)
- Phase 2: code generation

As can be seen from the CPU usage, phase 1 is unable to thoroughly saturate my system. Phase 2, on the other hand, can use my systems resources a lot better.

(the full graph can be found [here](https://www.jendrikillner.com/img/posts/rust-game-part-9/cargo-timing-img_rescaler.html))

## Rust Compilation - Test Case - Rustc

The same behavior can be found in the rustc compiler itself. The capture was published in [Visualizing Rust compilation](https://blog.mozilla.org/nnethercote/2019/10/10/visualizing-rust-compilation/).

![Rustc compilation timeline Rustc compilation timeline](../../assets/e2264503337903fd.png)


It’s a very extreme example as there are more than 20 seconds of compilation where the CPU is pretty much idle! This is caused because the dependent Creates are only able to start compiling after the completion of phase 1.

## Crate heavy architecture

Therefore I am suggesting to prefer a project structure that leans more towards crates with a shallow tree of dependencies. Having dependencies in the middle of the dependency chain can introduce large bubbles, as can be seen in Rustc

The aim should be to allow as many crates as possible to be compiled independently.

Should each file be a separate crate, mimicking the C++ compilation model? No, I don’t think so. There is an overhead to each Crate. There has to be a balance.

The best way is to keep checking the timings to detect if a single crate is starting to become a bottleneck. Once this happens, it’s time to start splitting a single Crate into multiple Crates.

[Visualizing Rust compilation](https://blog.mozilla.org/nnethercote/2019/10/10/visualizing-rust-compilation/) explains the necessary commands. Sadly these are only available on nightly :(

### Game structure

So given all this information, how did I structure this project? For now, I split it into 3 creates

- Window Creation
- Graphics foundation layer + Memory management
- Game + Shader interface

Below is a timing capture of a full rebuild:

![Rust Match3 compilation Rust Match3 compilation](../../assets/fd9e4c6a5836e63a.png)


As you can see most time is actually spend generation the native wrapper to call into Win32 API (Winapi crate) Sadly both the graphics and window creation require Winapi. Is it really needed to take 6 seconds in phase 1 to compile a win32 wrapper? Probably not.

Doing a minimal build with only changes to the game code takes 0.4 seconds. That is good to enough for now :)

## Next Part

In the next part, I will be doing some graphics code again. Time to clean up the rendering interface so that the game doesn’t have to use any unsafe code, and all interactions with D3D11 are hidden inside the Graphics foundation layer.

The code is available on [GitHub](https://github.com/jendrikillner/RustMatch3/releases/tag/rust-game-part-9)