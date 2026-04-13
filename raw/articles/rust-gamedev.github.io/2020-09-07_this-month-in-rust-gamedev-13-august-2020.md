---
title: 'This Month in Rust GameDev #13 - August 2020'
url: https://gamedev.rs/news/013/
author: Rust GameDev WG
published: '2020-09-07'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 13th issue of the Rust GameDev Workgroup’s
monthly newsletter.
[Rust](https://rust-lang.org) is a systems language pursuing the trifecta:
safety, concurrency, and speed.
These goals are well-aligned with game development.
We hope to build an inviting ecosystem for anyone wishing
to use Rust in their development process!
Want to get involved? [Join the Rust GameDev working group!](https://github.com/rust-gamedev/wg#join-the-fun)

You can follow the newsletter creation process
by watching [the coordination issues](https://github.com/rust-gamedev/rust-gamedev.github.io/issues?q=label%3Acoordination).
Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).
Feel free to send PRs about your own projects!

Table of contents:

[Rust GameDev Podcast](https://gamedev.rs/news/013/#rust-gamedev-podcast)[Game Updates](https://gamedev.rs/news/013/#game-updates)[Learning Material Updates](https://gamedev.rs/news/013/#learning-material-updates)[Library & Tooling Updates](https://gamedev.rs/news/013/#library-tooling-updates)[Popular Workgroup Issues in GitHub](https://gamedev.rs/news/013/#popular-workgroup-issues-in-github)[Meeting Minutes](https://gamedev.rs/news/013/#meeting-minutes)[Requests for Contribution](https://gamedev.rs/news/013/#requests-for-contribution)

![text logo](../../assets/2e0bb5851103fcb7.jpeg)


This month [Richard @patchfx Patching](https://richardpatching.com) started
[Rust GameDev Podcast](https://rustgamedev.com)!

Over the lockdown period I have been working on a new podcast for Rust game developers. I have been interviewing indie teams and library creators, discussing custom engines, procedural generation, open source and the business of games development.


-
[The first episode](https://rustgamedev.com/episodes/interview-with-team-veloren)is an interview with the team behind Veloren, an open-source multiplayer voxel RPG written in Rust.Find out about the game’s origin, its engine development, pros and cons of a big open-source project, CI and build pipeline, importance of artists, procedural generation, community building, managing players’ expectations, and upcoming developments.

-
[The second episode](https://rustgamedev.com/episodes/interview-with-herbert-wolverson-bracket-lib)is an interview with Herbert Wolverson, creator of[bracket-lib](https://crates.io/crates/bracket-lib)(pka RLTK),[Rust Roguelike Tutorial](http://bfnightly.bracketproductions.com), and[Nox Futura](https://thebracket.itch.io/nox-futura).A very wide-ranging interview covering many interesting topics: where the bracket-lib came from and what the creator is doing now, as well as practical questions and issues discovered in the course of creating their game, [Nox Futura]. Lots of interesting talk about a new Rust games development book Herbert is writing, C++ vs Rust, learning Rust, code architecture and ECS’s in roguelikes, emergent behavior, and hilarious bugs in Dwarf Fortress.


The show has been distributed on most major platforms
for you to listen and subscribe:
[Rust Game Dev Podcast (simplecast)](https://rustgamedev.com/),
[Apple Podcasts](https://podcasts.apple.com/gb/podcast/rust-game-dev/id1526304768),
[Spotify](https://open.spotify.com/show/7HRfGnTcXkLkQd9fxJbDGj),
[RSS Feed](https://feeds.simplecast.com/C6NQglnL),
[Google Podcasts](https://podcasts.google.com/feed/aHR0cHM6Ly9mZWVkcy5zaW1wbGVjYXN0LmNvbS9DNk5RZ2xuTA).

## Game Updates [#](https://gamedev.rs#game-updates)



![Camera debugging in Crate Before Attack](../../assets/64b45bfd3a125945.jpeg)

[Crate Before Attack](https://cratebeforeattack.com) by [koalefant (@CrateAttack)](https://twitter.com/CrateAttack)
is a skill-based multiplayer game where frogs combat their friends
while navigating the landscape with their sticky tongues.

A [playable browser build](https://cratebeforeattack.com/play) can be tried online.

Recent changes are:

- Training mode improvements, including a new map
[Dungeon](https://youtu.be/cukyVXQ0n0c)by[Kesha Astafyev](https://www.behance.net/spoon_tar). [Better camera motion](https://youtu.be/3y7Hfa-v3e8): multiple points of interest are tracked dynamically.- Improved GPU performance by merging multiple render passes into one.
- Added control hints.
- Numerous bugfixes and tweaks.

More details are in [August DevLog-entry](https://cratebeforeattack.com/posts/20200831-august-update/).

![Landscape](../../assets/59ec9dce9bbb43dd.jpeg)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In August, Veloren 0.7 was released! Airshipper, Veloren’s launcher, also got
updated to 0.4.0. Veloren was featured in the inaugural episode of the [Rust
Game Dev Podcast](https://rustgamedev.com/episodes/interview-with-team-veloren). Although the 0.7 release party saw the
largest number of concurrent players at 57, it ran into some significant issues
which you can read about below.

The largest merge in Veloren so far also happened in August. It included monumental changes to lighting and added level of detail functionality to see far-off mountains. Lots of work has been done on the animation, combat, SFX, and UX front. Animations for movement and combat were added and improved. Work continued on particle systems, which have been added to Veloren in places like campfires, fireworks, and weapons.

![Healing sceptre](../../assets/deee380642f6cdff.gif)

You can read more about some specific topics from August:

[Airshipper 0.4.0 Progress](https://veloren.net/devblog-79#airshipper-0-4-progress-by-songtronix)[Animation and Movement Updates](https://veloren.net/devblog-79#animation-and-movement-updates-by-slipped)[Particle Timing](https://veloren.net/devblog-80#particle-timing-by-lobster)- 0.7 Release:
[Party Statistics](https://veloren.net/devblog-81#0-7-release-party-statistics)and[Kick Disaster](https://veloren.net/devblog-81#0-7-release-party-kick-disaster-by-xmac94x) [Lighting and World Changes](https://veloren.net/devblog-81#sharp-s-lighting-and-world-changes-branch)[0.8 Intro Meeting](https://veloren.net/devblog-82#0-8-intro-meeting)[Audio SFX](https://veloren.net/devblog-82#audio-with-ellinia)[Photo Gallery](https://veloren.net/devblog-83#photo-gallery)

August’s full weekly devlogs: “This Week In Veloren…”:
[#79](https://veloren.net/devblog-79),
[#80](https://veloren.net/devblog-80),
[#81](https://veloren.net/devblog-81),
[#82](https://veloren.net/devblog-82),
[#83](https://veloren.net/devblog-83).

In September, work on 0.8 will continue. Some large systems being worked on include networking, improved persistence stability, and player experience. Game design is working on improving the connection between the experience a new player has, and the current game design. The in-progress 0.8 version will likely be completed more quickly than 0.7, as to not include too many changes.

![Two-way cycletracks and shared left-turn lanes](../../assets/307506e9ee1b89f8.png)


[A/B Street](https://abstreet.org) is a traffic simulation game exploring how small changes
to roads affect cyclists, transit users, pedestrians, and drivers. Any city
with OpenStreetMap coverage can be used!

Some of this month’s updates:

- Multiple traffic signals can be edited together.
- An
[API](https://dabreegster.github.io/abstreet/dev/api.html)and tools were added, to control maps and simulation from any language. [Michael Kirk](https://github.com/michaelkirk), a new team member, fixed HiDPI scaling issues in a consistent way.- Many new cities imported, with better support for countries that drive on the left and support for using alternate languages from OpenStreetMap for roads and buildings.
- Backwards compatibility for a player’s edits to the map.
- Two-way cycletracks and roads with multiple direction changes.

![Egregoria buildings screenshot](../../assets/35907fca36e2f7ae.png)


[Egregoria](https://github.com/Uriopass/Egregoria)’s objective is to become a granular society simulation,
filled with fully autonomous agents interacting with their world in real time.
Egregoria was previously known as Scale,
but was renamed to fit the theme better.

The [5th devlog](http://douady.paris/blog/egregoria_5.html) was published, talking about
the renaming, project management, buildings and scripting.

A [Discord](https://discord.gg/CAaZhUJ) server was launched to discuss the project.

*Discussions:
/r/rust_gamedev*

In [Cary](https://specificprotagonist.itch.io/cary) the player has to bring the titular character to the exit by carrying
them or otherwise making sure they don’t – nor the player themselves –
touch any of the traps.
Easier said than done when you have limited stamina and Cary keeps running
into spikes.

Made with hecs and wgpu (no framework), but uses WebGL on the web because of the current implementation status of WebGPU.

Made during the [Extra Credits game jam](https://itch.io/jam/extra-credits-game-jam-6),
it’s a rather small game.
It can be played in the browser or downloaded at [itch.io](https://specificprotagonist.itch.io/cary).



![Anthropic's virtual booth at Play NYC](../../assets/b62cfa37c02d7235.png)

[Play NYC](https://www.play-nyc.com/)

[Way of Rhea](https://store.steampowered.com/app/1110620/Way_of_Rhea/) is a puzzle platformer that takes place in a world where you can
only interact with items that match your current color.

Way of Rhea has a [free Steam demo](https://store.steampowered.com/app/1110620/Way_of_Rhea/) temporarily available as part of
[Play NYC](https://www.play-nyc.com/)!
The new demo includes a level that wasn’t part of the Steam Game Festival,
showing off how circuit puzzles will work in the game. Since Play NYC
couldn’t be in person this year, the devs temporarily themed this level to look
like last year’s Play NYC venue, included placing virtual booths for other games
throughout the level.

Follow [@AnthropicSt](https://twitter.com/anthropicst) or [@masonremaley](https://twitter.com/masonremaley) on Twitter or
[sign up for the mailing list](https://www.anthropicstudios.com/newsletter/signup/tech) for updates.

![vangers-shadow](../../assets/6c59fefbef986986.jpeg)


[vange-rs](https://github.com/kvark/vange-rs) is the project of re-implementing the [Vangers](https://en.wikipedia.org/wiki/Vangers) game (from 1998)
in Rust using modern development practices, parallel computations, and GPU.

This month vange-rs got real-time shadows!
See [video on /r/rust_gamedev](https://reddit.com/r/rust_gamedev/comments/i32p6r/realtime_hybrid_shadows_in_vangers) and technical description
on the [Hybrid Shadows](https://kvark.github.io/vange-rs/2020/08/04/shadows.html) post of the blog.

Another exciting development - the new bruteforce rendering technique allowing
to shift the camera behind the mechos as in 3rd person view.
See [video on /r/rust_gamedev](https://reddit.com/r/rust_gamedev/comments/igejxy/vangers_3rd_person_camera) and technical description on
the [Bar Painting](https://kvark.github.io/vange-rs/2020/08/29/bar-painting.html) post of the blog.

![screenshot: concrete, trees, shadows](../../assets/29a346bd1830e337.jpeg)


[Garden](https://epcc.itch.io/garden) is an upcoming game centered around growing realistic plants.
Some of the updates from [the July & August devlog](https://cyberplant.xyz/posts/july-august/):

- A new player inventory system;
- Better collision detection and camera movement;
- Minimalist, scrollable text-based GUI for choosing which species to plant or the type of material to build with (or destroy) something;
- Plant growth now depends directly on the amount of light every individual leaf receives, calculated on the GPU;
- Variable leaf alignment and ease of creating variety;
- Better bark, detailed trunks, and new species;
- Completely new lighting using GI.

![Chillscapes Main Menu](../../assets/eb7308588a50c9be.png)


[Chillscapes](https://github.com/khonsulabs/chillscapes) is a lo-fi
rhythm experience created for the [NEOC#03 Rhythm Game Jam](https://itch.io/jam/neoc03-rhythm-jam). Using
layerable lo-fi music tracks, the game has you tap with the rhythm of the loops
being added, before changing the music up by adding another loop into the mix.
Last week, [a retrospective update was published](https://community.khonsulabs.com/t/chillscapes-retrospective-and-kludgine-update/28)
reflecting on what the developer’s takeaways were from the experience.

Chillscapes is written using an early-in-development 2d engine,
[Kludgine](https://github.com/khonsulabs/kludgine). For audio playback, rodio was utilized. The source code is
[available on GitHub](https://github.com/khonsulabs/chillscapes).



![Dwarf Seeks Fortune](../../assets/aa104c42c3e13872.png)

[Dwarf Seeks Fortune](https://github.com/amethyst/dwarf_seeks_fortune) is a puzzle-platformer made with the Amethyst game
engine. Its developer, Jazarro, has partnered with the Amethyst organization
to make it an official Amethyst showcase game. It aims to be a learning
resource for anyone looking to get started with Amethyst.

The game currently sports a growing feature set, two playable levels and an
early version of an integrated level editor. It is ready for your
contributions, so if you’re interested, check out the
[contributor’s guide](https://github.com/amethyst/dwarf_seeks_fortune/blob/master/CONTRIBUTING.md) or the [good first issues](https://github.com/amethyst/dwarf_seeks_fortune/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).
If you have any questions, open an issue on GitHub or approach
Jazarro on [the Amethyst discord](https://discord.com/invite/amethyst).

[Akigi](https://akigi.com) is a WIP online multiplayer game.

This month was mostly dedicated to the custom engine’s scenery placement tool
([video demo](https://devjournal.akigi.com/august-2020/082-2020-08-30.html)).
Some of the updates:

[Terrain code refactoring and other required groundwork](https://devjournal.akigi.com/august-2020/080-2020-08-16.html).[Mouse-terrain intersection](https://devjournal.akigi.com/august-2020/082-2020-08-30.html#mouse-terrain-intersection).[Switching between Play and Place modes](https://devjournal.akigi.com/august-2020/082-2020-08-30.html#play-mode-place-mode).[Custom UI system](https://devjournal.akigi.com/august-2020/082-2020-08-30.html#user-interfaces).

Full devlogs:
[#078](https://devjournal.akigi.com/august-2020/078-2020-08-02.html),
[#079](https://devjournal.akigi.com/august-2020/079-2020-08-09.html),
[#080](https://devjournal.akigi.com/august-2020/080-2020-08-16.html),
[#081](https://devjournal.akigi.com/august-2020/081-2020-08-23.html),
[#082](https://devjournal.akigi.com/august-2020/082-2020-08-30.html).



![SIMple Mechanics wave preset](../../assets/e8e54e71f43e7df9.gif)

[SIMple Physics](https://mkhan45.github.io/SIMple-Physics/) by [@mkhan45](https://github.com/mkhan45) is a set of educational physics
simulators meant to help students and teachers conduct labs without expensive equipment
or in person classes. Each simulator uses serializable graphs, object inspection,
Lua scripting, and a few other features to help students learn. Currently, there
is a simulator for mechanics/projectile motion and one for universal gravitation,
but the goal is to include one for electronics/magnetism and one for waves/optics.

Written in Rust using `ggez`

, `specs`

, `imgui-rs`

, and `nphysics`

,
this project’s goals include:
performance, accessibility/portability, ease of use, and extensibility.

To find out more about the project, visit the site [here](https://mkhan45.github.io/SIMple-Physics/),
watch some cool gifs [here](https://mkhan45.github.io/SIMple-Physics/posts/Gifs/), or read the GitHub page
[here](https://mkhan45.github.io/SIMple-Physics/posts/Gifs/).

*Discussions:
/r/rust*

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

![writing nes emulator](../../assets/9618207706d77d8c.png)


“Writing NES Emulator in Rust” is a tutorial by [@bugzmanov](https://twitter.com/bugzmanov) on creating a fully
capable NES/Famicom emulator from scratch in the online book format. It walks
through major steps of emulating NES platform components to run
all-time classics, like Pacman, Donkey Kong, and Super Mario Bros.

It’s a fun way of getting into hardware internals and fundamentals of
computer systems. The tutorial also covers game-dev basics and how to
work with graphics in Rust using [SDL2](https://www.libsdl.org/) library.



![youtube preview](../../assets/c0a3a16e5a601aab.png)

[watch the talk](https://www.youtube.com/watch?v=GFi_EdS_s_c)

Getting started with Rust + gamedev can be intimidating. At
[RustConf 2020](https://rustconf.com), [Micah Tigley](https://twitter.com/micah_tigley) gave a talk about their experience
beginning game development using the [Amethyst](https://amethyst.rs/) game engine and
learning about ECS by implementing examples that aim to be accessible for
beginners.

Supporting blog posts for the talk:

The source code for the [demo can be found here](https://github.com/tigleym/sprite_animations_demo).

![Chargrid Roguelike Tutorial 2020](../../assets/dc56afd034d8aec1.png)


[Chargrid](https://github.com/stevebob/chargrid/) by [@stevebob](https://github.com/stevebob) is a collection of crates for building
applications with text UIs that run in terminals, graphical windows, and web
pages. It was made specifically with roguelike development in mind, though is
general-purpose enough to be used for other applications.

[Chargrid Roguelike Tutorial 2020](https://gridbugs.org/roguelike-tutorial-2020/)
is a tutorial series about making a traditional roguelike from scratch
using chargrid for rendering and input handling. Reference code is available in
[this git repo](https://github.com/stevebob/chargrid-roguelike-tutorial-2020)
organized with one branch for each subsection.

![graph: FileSignal -> AssetSignal -> AssetEvent](../../assets/b569d53cf491914c.png)


[@jojolepro](https://github.com/jojolepro) released a [blog post](https://www.jojolepro.com/blog/2020-08-20_event_chaining/) that provides
an in-depth look at how using events in entity-component-system architectures
can improve system reusability dramatically.

Using events in this way also allows for:

- easier testing,
- additional configurability,
- possible performance improvements,
- higher reusability - especially if using generics.

The blog also has an [RSS feed](https://www.jojolepro.com/blog/blog.xml) and more in-depth posts about
game development are planned.

## Library & Tooling Updates [#](https://gamedev.rs#library-tooling-updates)

![Summary results table](../../assets/f7229dc1b451bc77.png)

[here](https://rust-gamedev.github.io/ecs_bench_suite/target/criterion/report/index.html)

This month [@TomGillen](https://github.com/TomGillen) (author of the [Legion](https://github.com/amethyst/legion) ECS) released
[ecs_bench_suite](https://github.com/rust-gamedev/ecs_bench_suite) - a suite of benchmarks designed to test and compare
Rust ECS library performance across a variety of challenging circumstances.
Later, the project was adopted by the Rust GameDev WG
so that all Rust ECS developers can converge on a neutral,
community-maintained benchmark.

*Discussions:
/r/rust*

[Rapier](https://rapier.rs) is a new set of 2D and 3D physics engines written 100% in Rust.
It is 5 to 10 times faster than [nphysics](https://nphysics.org), close to the performances of the
CPU version of PhysX, and often slightly faster than Box2D.

[For its first release](https://www.dimforge.com/blog/2020/08/25/announcing-the-rapier-physics-engine) Rapier includes:

- rigid-body dynamics;
- colliders and sensors;
- joint constraints;
- optional serialization of the physics state;
- optional cross-platform determinism on IEEE-754 compliant targets;
- optional explicit SIMD and parallelism;
- JavaScript bindings with official NPM packages.

This new physics engine is developed by the recently created [Dimforge](https://dimforge.com)
single-member Open-Source company [replacing](https://www.dimforge.com/blog/2020/08/18/rustsim-becomes-dimforge) the former
Rustsim organization created on GitHub by [@sebcrozet](https://github.com/sebcrozet/).

*Discussions:
/r/rust*

![Jude3D](../../assets/4560ae664b90593f.jpeg)


[Jude3D](https://neocogi.com) is a web based 3D sculpting application.
It’s a WebAssembly application, written in C/C++ and compiled using Emscripten
but after much thinking, the authors decided to move the development to Rust!

Many problems arise when moving existing C/C++/WebAssembly code to Rust. The two most important ones:

- The new code should still interop with the already existing code.
- Payload size matters on the web: your WASM app should be as small as possible.

These led the authors to drop using Rust’s std in favor to their own libs (`!#[no_std]`

),
at least until the std library crates are split up accordingly and stabilized,
for example, the `alloc`

crate.

The good news is that they are
[releasing most of the libraries as they make them as open source](https://github.com/NeoCogi)!
Also, a [WASM glfw3/GLES2 example](https://github.com/NeoCogi/rs-glfw3-gles2-test) that showcases the libs
is included ([live demo](https://neocogi.github.io/rs-glfw3-gles2-test)).

![cute-c2 collision](../../assets/21408a4c3f8cde2b.gif)


cute-c2 is a 2D collision detection library that has had its first release to
[crates.io](https://crates.io/crates/c2). The library is a Rust wrapper around the [c2.h](https://github.com/RandyGaul/cute_headers/blob/master/cute_c2.h) library.

The library can detect collisions between circles, rectangles, capsules and up to eight-sided convex polygons. There are also functions for manifold generation, the GJK algorithm, and ray casting operations. There is an example program in the repository.

[hexasphere](https://crates.io/crates/hexasphere) v1.0 [#](https://gamedev.rs#hexasphere-v1-0)

![hexasphere example gif](../../assets/3b4ef92807079763.gif)


The [hexasphere](https://crates.io/crates/hexasphere) library provides a customizable interface for subdividing 3D
triangle meshes. Custom and stateful interpolation functions can be implemented
as well as per-vertex attributes.

All that’s required to define a base shape are the initial vertices, triangles based on the indices of the vertices in the initial vertices, and numbered edges. As long as the winding of the triangles remains consistent throughout the base mesh, all of the resulting triangles will retain that winding.

This library also provides a few interesting base shapes (which can be used alone if the shape is not subdivided): Icosahedron, Tetrahedron, Cube, Square Plane, Triangle Plane (all of which are pictured above).

[blitz-path](https://github.com/BezPowell/blitz-path) is a new crate providing
an implementation of the [JPS](https://en.wikipedia.org/wiki/Jump_point_search)
pathfinding algorithm.

JPS is an optimization of the A* search algorithm for uniform-cost grids, which are common in games. While fully functional, the code is still in an early state and any suggestions for improvements - especially on how best to integrate it with the existing ecosystem - are greatly appreciated.

[Mun](https://mun-lang.org) is a scripting language for gamedev focused on quick iteration times
that is written in Rust.

[August updates](https://mun-lang.org/blog/2020/08/30/this-month-august/) include:

- compiler support for type aliases;
- shared diagnostics between compiler and language server;
- support for the official
[inkwell](https://crates.io/crates/inkwell)crate; - refactors and quality of life improvements.

![Demo with moving traffic lights](../../assets/8c241873e09206cd.gif)


[inline_tweak](https://crates.io/crates/inline_tweak) by [@Uriopass](https://github.com/Uriopass) is a library that allows you to
tweak at runtime any number literal directly from your code.
It works by parsing the file when a change occurs
(inspired by [this blogpost](http://blog.tuxedolabs.com/2018/03/13/hot-reloading-hardcoded-parameters.html) from Tuxedo labs).
Usage example:

```
use inline_tweak::tweak;
loop {
// Try changing the value while the application is running
println!("{}", tweak!(3.14));
}
```


A `watch!()`

macro that sleeps until the file is modified is also provided.

The library is minimal, only requiring the `lazy_static`

dependency
to hold modified values.
In release mode, the tweaking code is disabled and compiled away.

[yacurses](https://lib.rs/crates/yacurses) by [@Lokathor](https://github.com/Lokathor) is a cross-platform curses bindings crate that’s
small, simple, easy to understand, and most importantly safe to use.
It wraps over `ncurses`

on Unix and a bundled `pdcurses`

on Windows.
If you’re looking to make a terminal-based roguelike
(or any other terminal-based game), give it a try.

[SPIR-Q](https://github.com/PENGUINLIONG/spirq-rs) is a light-weight shader reflection library, which allows you to query
the types, offsets, sizes and even names in your shaders procedurally.

This month v0.4.2..v0.4.6 versions were released. Some of the updates:

- Specialization constants enumeration.
- Dynamically sized multi-binding support.
- Improved entrypoint debug printing.
- Better manifest merging method for pipeline construction.
- Bugfixes and various small API improvements.

*Discussions: /r/rust_gamedev*

![inline-spirv](../../assets/efde982ee85f6ac2.png)


[Inline SPIR-V](https://github.com/PENGUINLIONG/inline-spirv-rs) is a single-crate build-time shader compilation library based on
shaderc which provides procedural macros to help you translate shader sources,
in either GLSL or HLSL, inline or from-file, into SPIR-Vs and embed the SPIR-Vs
right inside your code as `u32`

slices. Despite basic shader compilation,
`inline-spirv`

also support `#include`

directives, macro substitution,
post-compile optimization, as well as descriptor auto-binding.

*Discussions: /r/rust_gamedev*

[rspirv-reflect](https://github.com/Traverse-Research/rspirv-reflect) v0.1 [#](https://gamedev.rs#rspirv-reflect-v0-1)

![Traverse Research banner](../../assets/92386ddafa159988.png)


[Traverse Research](https://traverseresearch.nl) has created the [rspirv-reflect](https://github.com/Traverse-Research/rspirv-reflect) library to replace
their very basic use-case of the existing [spirv-reflect-rs](https://github.com/gwihlidal/spirv-reflect-rs) / [spirv-reflect](https://github.com/KhronosGroup/SPIRV-Reflect)
libraries that are already out there. The current iteration of `rspirv-reflect`

is pretty minimal, but it allows you to extract the binding setup from a SPIR-V
binary. `rspirv-reflect`

supports the latest version of SPIR-V (version 1.5 as
of writing) and it also supports all the new shader stages (both ray tracing
and mesh/task shaders) as well as the existing ones.

Traverse Research wanted to reduce their reliance on C and C++ unsafe
libraries and at the same time they needed to support newer features that were
slow to become available in the existing `spirv-reflect`

library. The primary
use-case for this library is in conjunction with the Rust wrapper around the
DirectX Shader Compiler ([dxc](https://github.com/microsoft/DirectXShaderCompiler)), called [hassle-rs](https://github.com/Traverse-Research/hassle-rs) that Traverse Research
also built.

![wgpu-rs water](../../assets/b41bae3786aa8c43.gif)

[water example](https://github.com/gfx-rs/wgpu-rs/tree/master/examples/water)

gfx-rs project and wgpu ecosystem have observed the release of 0.6 versions! 🎉

Some of the updates:

- Reworked project structure:
`wgpu-core`

- a safe pure-Rust internal API, implementing WebGPU specification;`wgpu-rs`

- the idiomatic Rust wrapper;`wgpu-native`

- the C API wrapper, aiming to be compatible with[Dawn](https://dawn.googlesource.com/dawn);- Gecko and Servo - for implementing WebGPU API in the browsers.

- Ability to record API traces, replay them on a different machine, and run data-driven tests.
`write_buffer`

and`write_texture`

for update the GPU data without intermediate staging buffers or encoders.- A number of powerful native-only extensions, such as descriptor indexing, as well as web-compatible extensions like depth-clamping.
[naga](https://github.com/gfx-rs/naga)v0.2 - an experimental shader translation library.- The
[showcase gallery](https://wgpu.rs/#showcase)was updated.

Read about the details on [gfx-rs blog](https://gfx-rs.github.io/2020/08/18/release-0.6.html).

[@sothr](https://github.com/sothr) has reworked the
[wgpu instancing tutorial](https://sotrh.github.io/learn-wgpu/beginner/tutorial7-instancing/#the-instance-buffer).
See discussion at [/r/rust_gamedev](https://reddit.com/r/rust_gamedev/comments/i8np5v/simplified_instancing_tutorial_learn_wgpu).

![KAS text layout](../../assets/c5915591c5caa26c.png)


[KAS](https://github.com/kas-gui/kas) by [@dhardy](https://github.com/dhardy) is a general purpose UI toolkit; its
initial aim is “old school” desktop apps with a good keyboard and touchscreen
support. Unlike many modern immediate-mode UIs, KAS’s widgets retain state,
allowing minimal per-frame updates. KAS supports embedded WebGPU graphics now,
and will (eventually) support being embedded within other contexts (requiring
only a supply of input events and implementation of some basic graphics routines).

KAS v0.5 switches to a new crate for text layout,
[KAS-text](https://github.com/kas-gui/kas-text). KAS-text is a text layout
engine supporting multi-line editing, shaping and bidirectional text; future
versions will also support formatting. KAS-text is not tied to any particular
raster or render system; its positioned-glyph output is relatively easy to
adapt to crates like `wgpu_glyph`

and `gfx_glyph`

.
For more, see the article [“Why I created KAS-text”](https://kas-gui.github.io/blog/why-kas-text.html).

![Egui](../../assets/ded59839a5e55fc2.png)


[Egui](https://github.com/emilk/egui/) is a highly portable immediate mode GUI library in pure Rust.
Egui can be integrated anywhere you can paint textured triangles.
You can compile Egui to WASM and render it on a web page using [egui_web](https://crates.io/crates/egui_web)
or compile and run natively using [egui_glium](https://crates.io/crates/egui_glium).

Check out the [Egui web demo](https://emilk.github.io/egui/index.html).

Example:

```
Window::new("Debug").show(ui.ctx(), |ui| {
ui.label(format!("Hello, world {}", 123));
if ui.button("Save").clicked {
my_save_function();
}
ui.text_edit(&mut my_string);
ui.add(Slider::f32(&mut value, 0.0..=1.0).text("float"));
});
```


*Discussions:
/r/rust*

![Demo: some terrain painted as grass, snow, dirt, etc](../../assets/5464625d35ec3528.jpeg)


[voxel-mapper](https://github.com/amethyst/voxel-mapper) is a library and in-game editor for voxel maps, smooth or cubey.
The ultimate goal of the project is to make it easy for artists and programmers
alike to generate volumetric game content, either manually or procedurally.
The library’s author [@bonsairobo](https://github.com/bonsairobo) has also written a couple posts:

[“Smooth Voxel Mapping: a Technical Deep Dive on Real-time Surface Nets and Texturing”](https://medium.com/@bonsairobo/smooth-voxel-mapping-a-technical-deep-dive-on-real-time-surface-nets-and-texturing-ef06d0f8ca14)[“A 3rd Person Camera in a Complex Voxel World”](https://medium.com/@bonsairobo/a-3rd-person-camera-in-complex-voxel-world-523944d5335c)

Upcoming on the roadmap are procedural generation algorithms for generating maps, new kinds of voxels, and graphical improvements. Currently, the library and editor depend on the Amethyst engine version 0.15, but there is a desire to make the library engine-agnostic. Contributions are welcome!

[Bevy](https://bevyengine.org) by [@cart](https://github.com/cart) is a brand new, refreshingly simple data-driven
game engine built in Rust. It aims to be:

**Capable**: Offer a complete 2D and 3D feature set.**Simple**: Easy for newbies to pick up, but infinitely flexible for power users.**Data Focused**: Data-oriented architecture using the Entity Component System paradigm.**Modular**: Use only what you need. Replace what you don’t like.**Fast**: App logic should run quickly, and when possible, in parallel.**Productive**: Changes should compile quickly … waiting isn’t fun.

These last few weeks have been big for the Bevy project:

- Bevy was announced and
[open sourced on GitHub](https://bevyengine.org). - Bevy’s features were introduced in the
[“Introducing Bevy”](https://bevyengine.org/news/introducing-bevy)blog post. - Had a staggering number of people join the community.
This required some quick planning to handle the new size,
which they outlined in the
[Scaling Bevy](https://bevyengine.org/news/scaling-bevy)blog post. - Added an official
[awesome-bevy repo](https://github.com/bevyengine/awesome-bevy)with a huge number of community plugins, games, apps, and learning materials. - Rapier, a new pure-rust physics engine,
released an
[official Bevy plugin](https://www.dimforge.com/blog/2020/08/25/announcing-the-rapier-physics-engine/#reaching-out-to-other-communities-bevy-and-javascript). - Thanks to the generosity of individuals and companies, they quickly met
their first two funding goals on @cart’s
[GitHub Sponsors page](https://github.com/sponsors/cart): “sustainable development” and “@cart makes minimum wage working on Bevy”. - Bevy received a glowing review from the Amethyst Engine team and they agreed
to collaborate in certain areas.
See the
[Addressing the Elephant in the Room](https://community.amethyst.rs/t/bevy-engine-addressing-the-elephant-in-the-room)thread on the Amethyst forum for more details.

Bevy users started sharing their work
on the [Bevy Discord showcase channel](https://discord.com/channels/691052431525675048/692648638823923732):

![bevy showcase](../../assets/03755f7fadc99aec.png)


In addition to the initial Bevy GitHub release, 114 pull requests were merged this month. Some highlights:

- A custom
[async task system for Bevy](https://github.com/bevyengine/bevy/pull/384), which significantly improves CPU usage and paves the way for future async work. - Refactored data-driven ECS shader code to make it more maintainable, fix some bugs, and ready to be optimized via the ECS change detection apis.
- Support for “logical or” ECS queries as a compliment to the default “logical and”.
- Numerous CI improvements.
- Use shaderc to compile shaders for iOS builds.
- GLTF loading improvements.

Bevy also made good progress on its three focus areas:

*Discussions:
/r/rust,
hacker news,
twitter,
amethyst forum*

[Minigene](https://www.github.com/jojolepro/minigene) is a tiled and ASCII game engine made by [@jojolepro](https://github.com/jojolepro).
It allows to very simply create complex games running on desktop as well as
in the browser.

While it is still under heavy development, a lot can be done already:

- Easily create ECS systems.
- Create tiled and ASCII entities.
- Create GUI elements.
- Move entities around with A* pathfinding.
- and much more!

### Tetra [#](https://gamedev.rs#tetra)

[Tetra](https://github.com/17cupsofcoffee/tetra) is a simple 2D game framework, inspired by XNA and Raylib. This month,
versions [0.4.1](https://twitter.com/17cupsofcoffee/status/1289857217198317568) and [0.4.2](https://twitter.com/17cupsofcoffee/status/1294316642680426497) were released, featuring:

- Improved Serde support;
- Various fixes and improvements to the built-in
`Camera`

type; - Many documentation improvements, based on user feedback.

In addition, Tetra 0.5 is planned for release in early September. For more
information on the upcoming changes, see the [changelog](https://github.com/17cupsofcoffee/tetra/blob/main/CHANGELOG.md).

![text logo](../../assets/2dfb130310a7896c.png)


[Piston](https://github.com/pistondevelopers/piston) is a modular game engine written in Rust.

A new [Piston Discord Channel](https://discord.gg/TkDnS9x) has been set up
for the Piston project.

Piston consists of a core library “piston” which itself are composed of smaller libraries for abstracting input, window and event loop. This design helps reducing breaking changes in the ecosystem.

The core library `pistoncore-input`

is now stabilized and reached 1.0!
This is the most important core abstraction, because it glues all
libraries that are not independent of the core.

[Dyon](https://github.com/pistondevelopers/dyon) is a rusty dynamically typed scripting language.
It is developed and maintained as part of the Piston project,
but can be used as a standalone library.

Dyon is designed from the bottom up to be a good gamedev scripting language for Rust. It uses a lifetime checker instead of garbage collection, a mutability checker, optional namespaces and ad-hoc types, named argument syntax, 4D vectors and HTML colors, plus a lot more features!

Recently, Dyon got better macro integration for native Rust types
using `#`

as a prefix.
Here is an example of this feature is being tested in
an experimental offline 3D renderer (not open sourced):

```
// Called by `set_simple(scene: _, sdf: _, id: _)`.
dyon_fn!{fn set_simple__scene_sdf_id(
scene: #&mut SimpleScene,
sdf: #&Sdf,
id: f64
) {
scene.sdfs[id as usize] = sdf.clone()
}}
```


To follow updates on Dyon, check out the subreddit [/r/dyon](https://reddit.com/r/dyon/).

[Piston-Graphics](https://github.com/pistondevelopers/graphics) is a library for 2D graphics, written in Rust,
that works with multiple backends.

`Stencil::Increment`

has been added and the ecosystem
has been updated to the latest version.

The research branch of the Piston project, AdvancedResearch,
has released a new ECS library [Nano-ECS](https://github.com/advancedresearch/nano_ecs).

This ECS design stores all components in a single array
and uses bit masks for enabling/disabling components.
An entity can have maximum 64 components and must be initialized
with all components it uses in the future.
Each entity has a slice into the array that stores all components.
The `World`

object, `Component`

and systems are generated using macros.

One research project with Nano-ECS is to prototype a UI framework
for Rust with a UI editor (not open sourced yet).
This project uses Piston-Graphics by default,
but can generate draw commands for processing by other 2D APIs.
It is also possible to override rendering of widgets for
custom looks with Piston-Graphics, which is often useful in gamedev.
Recently, this project has gotten to a place where
[tree-view interaction](https://twitter.com/PistonDeveloper/status/1299840279374110720) is working.

You can follow development at [@PistonDeveloper at Twitter](https://twitter.com/PistonDeveloper).

![logo](../../assets/42e8b028ca04a165.png)


[Amethyst](https://amethyst.rs) is a game engine and tool-set
for ambitious game developers.

This month a [v0.15.1 version was released](https://amethyst.rs/posts/release-0.15.1).
Updates include:

- New book chapters for
[UI](https://book.amethyst.rs/stable/ui.html)and[Tiles](https://book.amethyst.rs/stable/tiles.html); [Updated examples](https://github.com/amethyst/amethyst/tree/v0.15.1/examples), with special attention to the pong example;- Switch to
[GitHub Actions for CI](https://github.com/amethyst/amethyst/blob/v0.15.1/.github/workflows/ci.yml); - Lots of API improvements and bug fixes.

For more details see the [full changelog](https://github.com/amethyst/amethyst/blob/master/docs/CHANGELOG.md#0151---2020-08-14).

v0.16 plans include a full migration to the [Legion ECS](https://github.com/amethyst/legion)
and a big site face lift.

*Discussions:
/r/rust*

![Current state of starframe graphics and physics](../../assets/4b9411ac8dab6d81.gif)


[starframe](https://github.com/m0lentum/starframe) by [@molentum](https://twitter.com/molentum_) is a work-in-progress 2D game engine
for physics-y sidescrolling games. This month it received
[an experimental graph-based entity system](https://molentum.me/blog/starframe-architecture/).

The next area of focus is going to be fleshing out the physics with generalized constraints, which will enable things like friction and joints.

![A running app on a physical device](../../assets/292babdaae570f8d.jpg)


[mochi](https://github.com/richardanaya/mochi) by [@richardanaya](https://github.com/richardanaya) is a game engine oriented toward
low-power mobile Linux phones/tablets.
It’s written in Rust and uses Gtk and Cairo.
All drawing is done with an [Cairo Context](https://gtk-rs.org/docs/cairo/struct.Context.html) that mochi
has extended to do some really [common graphics operations](https://docs.rs/mochi/latest/mochi/trait.MochiCairoExt.html).

This project is super alpha but usable. Current features include: touch, screen rotation, atlases, sounds.

[pinephone-cairo-game-starter](https://github.com/richardanaya/pinephone-cairo-game-starter) is a starter for creating
a Cairo-based game in Rust for [PinePhone](https://en.wikipedia.org/wiki/PinePhone)

*Discussions:
/r/rust_gamedev*

![Puffin flamegraph shown with puffin-imgui](../../assets/13378d04968a5ede.png)


[Puffin](https://github.com/EmbarkStudios/puffin) is a simple instrumentation profiler created by [Embark](https://www.embark-studios.com/)
where you can opt-in to profile parts of your code.

```
fn my_function() {
puffin::profile_function!():
...
if ... {
puffin::profile_scope_data!("load_image", image_name):
...
}
}
```


The collected profile data can be viewed ingame with [imgui-rs](https://github.com/Gekkio/imgui-rs).



![A screenshot from the video](../../assets/b0cf7dee07b26b96.jpg)

[video tutorial / features overview](https://youtube.com/watch?v=p57TV5342fo)

[Optick](https://optick.dev/) by [@bombomby](https://github.com/bombomby) is a lightweight C++ profiler for games
that provides access for all the necessary tools required for
efficient performance analysis and optimization:
instrumentation, switch-contexts, sampling, GPU counters.

This month Rust API for Optick was released: [optick-rs](https://github.com/bombomby/optick-rs).

Also, a set of procedural macros for simplifying the process of code markup
were published: [optick-attr](https://crates.io/crates/optick-attr).

```
// Instrument current function
#[optick_attr::profile]
fn calc() { /* Do some stuff*/ }
// Generate performance capture for function
// to {dir}/capture_name(date-time).opt.
#[optick_attr::capture("capture_name")]
pub fn main() {
calc();
}
```


[wowAddonManager](https://github.com/MR2011/wowAddonManager) v1.0.2 [#](https://gamedev.rs#wowaddonmanager-v1-0-2)

![wowAddonManager Example](../../assets/057044f2c635d7d3.png)


The [wowAddonManager](https://github.com/MR2011/wowAddonManager) is a terminal user interface for managing World of
Warcraft addons on Linux made by [@mreimsbach](https://twitter.com/mreimsbach). It allows installing addons
from [Curseforge](https://www.curseforge.com/wow/addons) for WoW Classic as well as WoW Retail.

The [tui-rs](https://github.com/fdehau/tui-rs) library was used to create the interface and [Termion](https://gitlab.redox-os.org/redox-os/termion) was used to
communicate with the TTY.

[RON](https://github.com/ron-rs/ron) (Rusty Object Notation) is a simple readable data serialization format
that looks similar to Rust syntax and is designed
to support all of [Serde’s data model](https://serde.rs/data-model.html).
RON is relatively popular amongst Rust game developers.

This month [@JonahHenriksson](https://github.com/JonahHenriksson) released [intellij-ron](https://github.com/ron-rs/intellij-ron) - a new plugin
that adds [RON](https://github.com/ron-rs/ron) support to IntelliJ-based IDEs.

*Discussions:
/r/rust*

![sia_viewer demo: A textured model](../../assets/18cc5ff46efab5e6.jpeg)


This month [@Stromberg90](https://github.com/Stromberg90) published [Football Manager Tools](https://github.com/Stromberg90/football-manager-tools) - a set of tools
for working with [Football Manager’s](https://en.wikipedia.org/wiki/Football_Manager) 3D mesh format(.sia).
Amongst them:

`sia_parser`

- a Rust crate for parsing .sia files.`sia_viewer`

- a standalone Mesh(.sia) Viewer.

## Popular Workgroup Issues in GitHub [#](https://gamedev.rs#popular-workgroup-issues-in-github)

## Meeting Minutes [#](https://gamedev.rs#meeting-minutes)

[See all meeting issues](https://github.com/rust-gamedev/wg/issues?q=label%3Ameeting) including full text notes
or [join the next meeting](https://github.com/rust-gamedev/wg#join-the-fun).

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[winit’s “Good first issue” and “help wanted” issues](https://github.com/rust-windowing/winit/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+label%3A%22status%3A+help+wanted%22+label%3A%22Good+first+issue%22).[gfx-rs’s “contributor-friendly” issues](https://github.com/gfx-rs/gfx/issues?q=is%3Aissue+is%3Aopen+label%3Acontributor-friendly).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[A/B Street’s “good first issue” issues](https://github.com/dabreegster/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/good%20first%20issue).

That’s all news for today, thanks for reading!

Subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!