---
title: Mach v0.3 released - Zig game engine & graphics toolkit
url: https://devlog.hexops.org/2024/mach-v0.3-released/
published: '2024-02-02'
source_blog: Hexops' devlog
source_site: https://devlog.hexops.org/
category: graphics
fetched: '2026-04-19'
---

Mach is a Zig game engine & graphics toolkit for building high-performance & modular games, visualizations, and desktop/mobile apps. Learn more

We are working towards Mach 1, and have just released v0.3 which includes 6 months of work - here are the highlights!

Coming soon: intro to 2D gamedev workshop

The first-ever intro to 2D gamedev workshop using Mach will be hosted at the Software You Can Love conference in Milan, Italy, May 14-17. The workshop will use Mach’s currently in-development higher level 2D graphics APIs.

If you’re interested in Zig or Mach, then check out the SYCL conference! It’s an amazing experience, a great opportunity to meet a ton of Zig community members, core team members, as well as enjoy some of the best food that Italy has to offer!

Community highlight: Pixi and Scoop’ems

@foxxne is an early adopter of Mach core, largely pushing it to its limits. They make use of Mach’s new experimental sysgpu graphics API (which we intend to be a successor/descendant of WebGPU), as well as other libraries like flecs and dear-imgui. They’re developing Pixi - a pixel art editor:

@foxxne is making awesome tools and games in Zig, pushing things to their limits, I encourage watching how humble Colton is when speaking about their work. We are very excited to make Mach support foxxne’s projects better in the future, and enable others to build things like this too.

Mach core aims to provide just a window, input, and truly cross-platform graphics API.

We think of it as an alternative/competitor to the classic options of SDL+OpenGL, GLFW+Vulkan, etc. Today, it’s not quite there yet - it uses GLFW behind the scenes for desktop support, and WebGPU as its graphics API, but we’re actively working on making it a genuine competitor written in Zig.

In this release, it saw general bug fixes - as well as some libmach development - which aims to provide a C API to both Mach core and engine APIs.

sysgpu

In Mach v0.2, we announced an experiment - that we were working on a WebGPU implementation written in Zig, as an alternative to using Dawn (Google Chrome’s WebGPU implementation.) In the past 6 months, this experiment saw an immense amount of development and exceeded our expectations!

sysgpu today is a nearly fully-functional WebGPU native implementation (minus browser-level safety checks), thanks to two amazing contributors. It has functional D3D12, Vulkan, Metal, and OpenGL backends. It has it’s own WGSL shader compiler, and nearly all mach-core examples are runnable using it. We’ve even seen real applications (the Pixi pixel editor from foxxne, for example) begin to adopt it.

As we continued development of it over the past six months, we identified key design tradeoffs where we could differ from WebGPU’s API choices and gain a faster, more modern, featureful graphics API. As a result, we’ve come to view sysgpu as a leaner and meaner successor and descendant of WebGPU for native graphics, rather than just another implementation of it. As a result, it builds on the back of WebGPU’s design choices, but ultimately has its own distinct API and will not be ABI-compatible.

We have plans to alleviate some major pain points of WebGPU, specifically around pipeline creation / descriptor boilerplate, supporting push constants when available via a better API design (not as an extension), a more integrated/seamless approach to binding resources to shaders with type-correctness, and more.

We are also evaluating using Zig itself as the shading language, instead of WGSL, and are looking to enable fully offline shader compilation as an optional feature.

sysgpu is still under heavy development, particularly all of the ‘successor/descendant’ API design choices noted above have not been implemented yet. It is disabled in the v0.3 release by default, and after this release we plan to invest more aggressively in it - so expect more details and specifics to come soon.

sysaudio

As a bit of background, mach-sysaudio started out as Zig bindings to Andrew Kelley’s fantastic C library libsoundio, but ultimately it grew to stand on its own two feet - becoming a brand new library written in Zig from first-principles and the ground-up to achieve similar goals: providing just low-level audio input/output, nothing else. It saw a good deal of polish in this iteration:

SIMD sample conversion support - and sample conversion is now explicitly optional (so the default is to work with the driver’s active audio format.)

Major API design improvements

Fixed issues with microphone/input devices, specifically multi-channel devices on macOS with CoreAudio.

As a quick hack project over the holidays, I leveraged Mach’s audio libraries, reading midi input from a piano keyboard, synthesizing audio using Zig code / Mach, and playing it back through digital piano speakers. Here’s a few vertical videos of me being silly & having fun with it (skip to 2:24 to hear how I think a Ziguana might sound!):

Nominated Zig versions

Mach has always needed a sweet-spot between stable Zig and nightly Zig, a better balance of latest-and-greatest features and bug fixes, but less of a moving target than nightly Zig. To address this, we formalized how we nominate Zig versions for use, enabling others to synchronize their Zig version with the one Mach supports more easily.

Mach engine as a standard library of modules

We began documenting how we view Mach engine as a standard library of modules for game development, and how we’ll enable you to use just the parts you wish. This is a small-but-important step in showcasing how the engine’s higher level APIs will be more modular than the monolithic big engines of today.

Entity component system

The Mach entity component system provides a key role in Mach’s modularity, in this iteration it saw numerous polish / bug fix improvements - the ability to actually query entities, a more clear/concise API, etc. It is still under heavy development, however.

mach.math

mach.math was introduced to the Mach standard library: a custom math library tailored towards our graphics API conventions, matrix representations, coordinate systems, etc.

Today it includes many of the basics: vectors, matrices, quaternions - though it is still missing some basic tablestakes. It also has ray-triangle intersection, and we intend to expand it to cover more general collision utilities later.

A new set of math docs were added to the website with some cute diagrams/visualizations.

mach.gfx.Sprite

mach.gfx.Sprite was introduced, which is the start of a 2D sprite-rendering module. It is largely usable, though we anticipate its API to change a fair amount and are looking to add animated sprite support among other key features.

It has been useful in letting us test basic rendering of hundreds of thousands of sprites, each as separate entities with their own transformation matrices calculated CPU-side, and get more of an end-to-end feel for how things are looking with our ECS:

mach.gfx.Text

Development of a basic text rendering module is underway, but not ready for use yet.

Status of ‘simple 2D game’ support

In short, we’re still working on it. More to come soon.

General project maintenance

Two new examples rgb-quad and textured-quad showing off super basic 2D rendering were added.

Began to formulate our hardware support plans, such as when we will target certain SIMD instruction sets.

All of our build.zig scripts went through a great deal of changes and improvements, as Zig’s build system and package manager matured greatly.

I work a normal tech job, and most days after I sign off from work I go online to build Mach, often like working two jobs. I’ve been doing this for a few years now, and dreaming of being able to build Mach for a decade before that.

FOSS is in my roots and I believe we should own our tools, they should empower us-not be part of the ‘open source’ game which is all too prevelant today (even among ‘open source’ engines.) Mach needs to be for people like you and me-it needs to genuinely be software you can love.

My dream is one day to live a simple, modest, future earning a living building Mach for you and creating high-quality games for everyone. Please consider sponsoring my work if you believe in this vision.

Thanks

Immense thank you to all those who helped make this release possible, to those who contribute regularly or in the past, and those who sponsor development. It means the world!