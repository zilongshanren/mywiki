---
title: 'This Month in Rust GameDev #19 - February 2021'
url: https://gamedev.rs/news/019/
author: Rust GameDev WG
published: '2021-03-08'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 19th issue of the Rust GameDev Workgroup’s
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

[Game Updates](https://gamedev.rs/news/019/#game-updates)[Learning Material Updates](https://gamedev.rs/news/019/#learning-material-updates)[Engine Updates](https://gamedev.rs/news/019/#engine-updates)[Library & Tooling Updates](https://gamedev.rs/news/019/#library-tooling-updates)[Popular Workgroup Issues in GitHub](https://gamedev.rs/news/019/#popular-workgroup-issues-in-github)[Requests for Contribution](https://gamedev.rs/news/019/#requests-for-contribution)

## Rust GameDev Meetup [#](https://gamedev.rs#rust-gamedev-meetup)

![Gamedev meetup poster](../../assets/71071b7079fb3ca0.png)


The second Rust Gamedev Meetup happened in February. It was an opportunity for
developers to show off what Rust projects they’ve been working on in the game
ecosystem. Developers showed off game engine demos, in-game playthroughs,
tooling, and more. You can watch the recording of the meetup [here on
Youtube](https://www.youtube.com/watch?v=Ea4Wt_FgEEw).

The next meetup will take place on the 13th of March at 16:00 GMT on the [Rust
Gamedev Discord server](https://discord.gg/yNtPTb2), and can also be [streamed on
Twitch](https://www.twitch.tv/rustgamedev). If you would like to show off what you’ve been
working on, fill out [this form](https://forms.gle/BS1zCyZaiUFSUHxe6).

## Game Updates [#](https://gamedev.rs#game-updates)

### Flesh [#](https://gamedev.rs#flesh)

![flesh preview](../../assets/ba106e8582da2f90.gif)

Flesh by [@im_oab](https://twitter.com/im_oab) is a 2D-horizontal shmup game with hand-drawn animation and
organic/fleshy theme. It is implemented using [tetra](https://github.com/17cupsofcoffee/tetra). This month’s updates
include:

- Added title screen
- Support gamepad
- Add new enemy types for first level include mid-boss

![Fishgame gui](../../assets/a8fd084d3ec52d77.gif)

[Fishgame](https://github.com/heroiclabs/fishgame-macroquad) [(web build)](https://fedorgames.itch.io/fish-game?secret=UAVcggHn332a) is an online multiplayer game,
created in a collaboration between [Nakama](https://heroiclabs.com/), an open-source scalable
game server, and the [Macroquad](https://github.com/not-fl3/macroquad/) game
engine.

This month fishgame utilized macroquad’s new UI system to add a title screen and improve the login screen.

![teki preview](../../assets/0ed25a22c1b3ff1d.gif)


[Teki](https://github.com/o2sh/teki) is a free and open-source fangame of the [Tōhō](https://en.wikipedia.org/wiki/Touhou_Project) series using [SDL2](https://github.com/Rust-SDL2/rust-sdl2)
and [Legion](https://crates.io/crates/legion) for ECS. It is aimed to be a shoot ’em up game with “lots of
bullets” a.k.a danmaku 弾幕 - literally “barrage” or “bullet curtain” in
Japanese.

The project is still at a “very” early stage of development (Dec. 2020).

This month’s updates include:

- New enemy type: big fairy
- New special card: Stellar Vortex
- Add yin yang orbs

![harvest hero preview](../../assets/080d54949ba26f58.gif)


[Harvest Hero](https://discord.gg/CJRbxQn3d9) is undergoing a shop system rework. However, new
abilities are still being implemented. You can now use Zhebnog’s Hourglass to
stop time and get weird.

Built on top of [Emerald](https://github.com/Bombfuse/emerald) by [Bombfuse](https://twitter.com/bombfuse_dev).

This month’s updates include:

- Added “Flame Guard” enchantment
- Added “Zhebnog’s Hourglass” ability
- Began work on a new main menu
- Implemented a functional shop system

![Separate cyclepaths in A/B Street](../../assets/c76c02fd368901c9.png)


[A/B Street](https://github.com/a-b-street/abstreet) by [@dabreegster](https://twitter.com/CarlinoDustin) is a traffic simulation game exploring how small
changes to roads affect cyclists, transit users, pedestrians, and drivers, with
support for any city with OpenStreetMap coverage.

In February, [Bruce](https://github.com/BruceBrown) implemented lagging green traffic signals, [Michael](https://github.com/michaelkirk) and
[Yuwen](https://www.yuwen-li.com/) released the new day UI theme. More cycle paths and service roads were
imported for all maps, and we added loads of maps, a new per-country picker UI,
and dynamic font loading. Try out [Taipei](http://abstreet.s3-website.us-east-2.amazonaws.com/dev/game/?--dev&tw/taipei/maps/center.bin) in the web browser to see all of this
in action!

![A brightly colored scene with a grass field, a river, and some happy ducks.](../../assets/b6da2dd2b614200d.jpg)


[Paddlers](https://paddlers.ch) ([GitHub](https://github.com/jakmeier/paddlers-browser-game), [Online Demo](https://demo.paddlers.ch)) by [@jakmeier](https://github.com/jakmeier)
is an experimental MMORTS with the backend and the web client all written in
Rust.

February gave birth to Paddlers release 0.2.1 and a ton of new game mechanics.
It features a skill map, quests, and a refreshed take on the tower defense
aspect of the game. On top of that, the rendering engine (part of the
[Paddle](https://github.com/jakmeier/paddle) framework) has been reworked and now allows for custom shaders.
Read all about this month’s changes in this [article](https://www.jakobmeier.ch/blogging/Paddlers_6.html) released
on the developer’s private website.

### Stellary 2 [#](https://gamedev.rs#stellary-2)



![Stellary 2 Anti-Missile Laser](../../assets/445e56c6487a8bb3.gif)

[watch the full video](https://twitter.com/CoffeJunkStudio/status/1360637714660548618)

Stellary 2 by [@CoffeJunkStudio](https://twitter.com/CoffeJunkStudio) is a 3D real-time space
shooter in which the player has to prevail against enemy space ships.

The latest updates include:

- Players’ space ships
- Prediction of the rocket trajectory
[Energy budget](https://twitter.com/CoffeJunkStudio/status/1360637714660548618)- Weapon enhancements (
[trident laser](https://twitter.com/CoffeJunkStudio/status/1358437135230119936)&[missile splitting](https://twitter.com/CoffeJunkStudio/status/1365666841838952450))



![Homing Missiles](../../assets/4ca6f02b3af3a4fb.gif)

[Theta Wave](https://github.com/amethyst/theta-wave) is a space shooter game by developers [@micah_tigley](https://twitter.com/micah_tigley) and
[@carlosupina](https://twitter.com/carlosupina). It is one of the showcase games for the [Amethyst Engine](https://amethyst.rs/). In
the past month, they have been focusing on refactoring the motion system to make
the code more approachable to other contributors.

Notable changes:

- Missiles now spawn from missile launcher enemies
- Cursed background slowly fades in over the course of the level

![SeniorSKY](../../assets/4943239587a7667a.png)

[SeniorSKY](https://youtube.com/playlist?list=PLMmaJuk-D7iaObZyhyvc83tNwpx3ghzkY) is a flight simulator that uses the Vulkan API, developed by
[@pmathia0](https://twitter.com/pmathia0). As an aerospace engineering student, Peter has always been
interested in how a flight simulator works under the hood. The development of
SeniorSKY started as a hobby project during university studies.

SeniorSKY uses real-world elevation data with 1 arc second precision and can render the whole globe in real dimensions. During the flight, the terrain tiles are loaded dynamically based on real GPS coordinates of airplane, with a decreasing level of detail further from the camera. This is achieved using a combination of a terrain-quad-tree and GPU tessellation.

Notable changes since last month:

- Atmospheric scattering
- Improved fog
- FXAA + HDR tone mapping
- Terrain data preprocessing using compute shaders
- Performance optimizations

Short-term plans:

- replace imgui-rs by egui
- implement sun position based on datetime
- add terrain bump-maps to visualize gravel

![Way of Rhea screenshot](../../assets/be4c93a25526a548.png)


Way of Rhea is a picturesque puzzle game that lets you correct your mistakes. Change your color, teleport past the colored gates, master the color-powered circuits, and befriend the crabs-but don’t let them out!

This month’s major updates include:

- New puzzles
- Support for standard video settings (see
[here](https://www.anthropicstudios.com/2021/02/20/fullscreen-exclusive-is-a-lie/)) - The new promotional art shown above



[gameplay video](https://www.youtube.com/watch?v=cagT0GbiLxY)on YouTube

[Station Iapetus](https://github.com/mrDIMAS/StationIapetus) by [@mrDIMAS](https://github.com/mrDIMAS) is a 3rd person shooter on the
space prison Iapetus near the Saturn.

- New inventory (check the video)
- Ability to throw grenades
- Splash damage
- More textures and materials
- Hitboxes for bots and player
- Better bots navigation
- Laser sight improvements
- Weapon display now shows bullet and grenades count
- Lots of other small fixes and improvements

![Lush forest](../../assets/23d41f412179a7f5.jpg)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In February, lots of work has been done on worldsim, with travelling merchants being worked on. Some experiments have been happening on procedurally generating giant trees. Lots is being done on the combat end, with dual wielding and modular weapons being a big focus. Player trading was also implemented, which allows items to be shared on the server. A large internal shift is being made from diesel to rusqlite.

A rework of attacks was done to allow their effects to be more dynamic. Lots of work has been done on the art team, with new weapon models, new mobs like fish. Some quality of life improvements were added, like humanoids automatically deploying gliders while falling to avoid fall damage. CI changes were made to finally have the GitHub mirror update periodically without error from LFS storage. In March, Veloren will release 0.9.

February’s full weekly devlogs: “This Week In Veloren…”:
[#105](https://veloren.net/devblog-105),
[#106](https://veloren.net/devblog-106),
[#107](https://veloren.net/devblog-107),
[#108](https://veloren.net/devblog-108).

![A screenshot from a game of Project YAWC.](../../assets/7b8197671fa34dc6.png)


[Project YAWC](https://twitter.com/projectyawc) is a turn-based strategy game in development by
junkmail. February saw the release of Alpha 4, bringing special units and
auctions to determine ownership of special units, as well as changes to netcode,
balance, and UI.

Those interested in participating in the alpha test should fill out this
[form](https://forms.gle/tzP6oRaJmApgMyrj7). To learn more, you can follow the new
[@projectyawc](https://twitter.com/projectyawc) Twitter or send an e-mail to projectyawc@gmail.com.

![A player standing in front of a giant crab](../../assets/cd4f992c3ad206f4.jpg)

[Antorum Online](https://ratwizard.dev/dev-log/antorum) is a micro-multiplayer online role-playing game by
[@dooskington](https://twitter.com/dooskington). The game server is written in Rust, and the official client is
being developed in Unity.

The Armorcrafting, Weaponcrafting, and Salvaging skills were implemented this month! Players can now craft gear in town using materials gathered out in the world. They can also break down old or unwanted gear to recycle it.

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

![Way of Rhea's video settings](../../assets/ce6720b80334485f.jpg)

[Way of Rhea](https://store.steampowered.com/app/1110620/Way_of_Rhea/)’s video settings

[Anthropic Studios](https://anthropicstudios.com) has [shared an article](https://www.anthropicstudios.com/2021/02/20/fullscreen-exclusive-is-a-lie/) walking
through what they learned from implementing fullscreen exclusivity in their Rust
game engine and testing the fullscreen exclusive implementation of existing
games on a variety of hardware.

*Discussions:
/r/rust_gamedev*

![Rhythm game demo](../../assets/b18b146a880b2299.gif)

[Rhythm game in Rust using Bevy](https://caballerocoll.com/blog/bevy-rhythm-game/) is an introductory tutorial for Bevy made by
[@guimcaballero](https://twitter.com/GuimCaballero). It guides through how to use Bevy to develop a Rhythm game,
including how to play audio, use GLSL shaders, and make a simple menu screen.

![demo that first show godot’s physics and than switches to rapier](../../assets/6d8932f6546a5fb9.gif)


[godot-vs-rapier](https://github.com/extrawurst/godot-vs-rapier) by [@extrawurst](https://twitter.com/extrawurst) is a project that compares
[Godot](https://godot-rust.github.io)’s built-in physics against [Rapier](https://rapier.rs).

*Discussions:
r/godot*

## Engine Updates [#](https://gamedev.rs#engine-updates)

![macroquad_gui](../../assets/67926887cec77faf.gif)

[macroquad](https://github.com/not-fl3/macroquad) is a cross-platform (Windows/Linux/macOS/Android/iOS/WASM) game
framework built on top of [miniquad](https://github.com/not-fl3/miniquad).

This month biggest update: Macroquad got its own fully skinnable and
customizable immediate mode UI system 🎉.

The new system took its origins from a heavily refactored [megaui](https://github.com/not-fl3/megaui) and supports
custom font sizes, fonts and skins for each UI element.

While work is still in progress, all important decisions were made and
implementation [PR](https://github.com/not-fl3/macroquad/pull/156) got merged.

Minor updates:

[Textures support](https://github.com/not-fl3/macroquad/pull/152)for macroquad materials- Experimental 2D pan/zoom camera
[implementation](https://github.com/not-fl3/macroquad/pull/146)

![Tetra's demo game](../../assets/fcbfad90c1c8ecb8.png)

[Tetra](https://github.com/17cupsofcoffee/tetra) is a simple 2D game framework, inspired by XNA, Love2D, and Raylib. This
month, version 0.6 was released, with some big changes and features:

- A simpler drawing API
- Less global state for mesh drawing
- Multisampled canvases
- Better font rendering

For more details, see the [changelog](https://github.com/17cupsofcoffee/tetra/blob/main/CHANGELOG.md), or [17cupsofcoffee’s
twitter thread](https://twitter.com/17cupsofcoffee/status/1357750836370284544) about the release.



[navmesh agent navigation](https://www.youtube.com/watch?v=tqFdQ5OPB1I)on YouTube

[rg3d](https://github.com/mrDIMAS/rg3d) ([Discord](https://discord.gg/xENF5Uh), [Twitter](https://twitter.com/DmitryNStepanov)) is a game engine that
aims to be easy to use and provide a large set of out-of-box features. Some of
the recent updates:

- Ability to render UI instances in a texture
- FBX name validator
- Fast Approximate Anti-Aliasing (FXAA)
- Integrity checks for resource inheritance
- Nodes now can be tagged
- Animation blending machine now has BlendAnimationsByIndex node
- Multi-directional binding between physics and graph
- SceneDrawingContext improvements: draw_capsule, draw_capsule segment
- Performance statistics for scenes
- ColorGradient improvements
[Path smoothing for navmesh agent](https://www.youtube.com/watch?v=tqFdQ5OPB1I)- Lots of other small fixes and improvements.

![Dotrix Light Demo](../../assets/d64f70dff1ab81f3.png)

[Dotrix](https://github.com/lowenware/dotrix) ([YouTube](https://youtube.com/channel/UCdriNXRizbBFQhqZefaw44A), [Discord](https://discord.com/invite/DrzwBysNRd)) by
[@lowenware](https://twitter.com/lowenware) is an ECS based 3D game engine with renderer built around the
[wgpu-rs](https://github.com/gfx-rs/wgpu-rs).

This month [Dotrix](https://github.com/lowenware/dotrix) 0.3 was released on
[crates.io](https://crates.io/crates/dotrix) with the complete [API
documentation](https://docs.rs/dotrix/0.3.0/dotrix/), major light components
update, wireframes, and mouse ray modules.

## Library & Tooling Updates [#](https://gamedev.rs#library-tooling-updates)

![Screenshot from Rafx Rendering Framework](../../assets/0882b0fbf4024137.png)


Rafx is a multi-backend renderer that optionally integrates with the
[distill](https://github.com/amethyst/distill) asset pipeline. Rafx is divided into three tiers of
functionality:

`rafx-api`

provides a custom GPU API abstraction layer that currently supports
Vulkan and metal. ([API in rust psuedocode](https://github.com/aclysma/rafx/blob/master/docs/api/api_design_in_rust_psuedocode.rs))

`rafx-framework`

builds on the API layer using ideas found in modern shipping
AAA titles. Rendering is pipelined in a separate thread in three phases, using
jobs to extract data from the main thread, process the data on the render
thread, and write the draw calls to command buffers. [[Tatarchuk
2015](http://advances.realtimerendering.com/destiny/gdc_2015/Tatarchuk_GDC_2015__Destiny_Renderer_web.pdf)] A render graph ensures correct synchronization.
[[O’Donnell 2017](https://www.gdcvault.com/play/1024612/FrameGraph-Extensible-Rendering-Architecture-in)] The framework also provides a material
abstraction and shader pipeline.

`rafx-assets`

adds integration with the [distill](https://github.com/amethyst/distill) asset pipeline.
This ensures that when an asset like a mesh is loaded, other related assets like
textures/material/vertex data are loaded. By integrating with Distill, rafx
provides advanced features like streaming live asset updates to remote devices.

More information about rafx:

[GitHub](https://github.com/aclysma/rafx)[Documentation](https://github.com/aclysma/rafx/blob/master/docs/index.md)[Why Rafx?](https://github.com/aclysma/rafx/blob/master/docs/why_rafx.md)(includes similarities/differences with other rust and non-rust alternatives)

![The plot thickens](../../assets/1c04837fcb204b31.gif)


[egui](https://github.com/emilk/egui) by [@emilk](https://twitter.com/ernerfeldt) is an easy-to-use immediate mode GUI library in pure Rust.

This month [versions 0.9 and 0.10](https://github.com/emilk/egui/blob/master/CHANGELOG.md) of egui were released with many improvements
big and small, including a 2D plot, more text styles, disabling widgets and
improved documentation.

You can try out egui in the [online demo](https://emilk.github.io/egui).

[Mun](https://mun-lang.org) is a scripting language for gamedev focused on quick iteration times that
is written in Rust.

It’s been a long time coming, but the Mun Core Team is closing in on the finish
line for Mun v0.3. They are only a couple of pull requests away from locking the
build for bug fixes and documentation. The [February updates](https://mun-lang.org/blog/2021/03/04/this-month-february)
include:

`use`

statements language support;- Incremental file updates for the language server;
- LLVM 11 support;
- Bug fixes and other improvements.

![Graphite GUI](../../assets/e29cf0506411bbae.png)

[Graphite](https://github.com/GraphiteEditor/Graphite) ([GitHub](https://github.com/GraphiteEditor/Graphite), [Discord](https://github.com/GraphiteEditor/Graphite/blob/master/README.md#discord),
[Twitter](https://twitter.com/GraphiteEditor)) is an in-progress vector and
raster graphics editor built on a nondestructive node-based workflow.

Since February’s Rust Gamedev Meetup [which announced](https://www.youtube.com/watch?v=Ea4Wt_FgEEw&t=563s) the
Graphite vision has attracted tremendous interest, community advice has shifted
the development strategy to focus on a 0.1 MVP release ASAP:

- The past year’s in-development custom GUI has been shelved in lieu of an
interim web GUI. Graphite intends to natively support Windows, Mac, Linux, and
Web. This change unblocks core application development but means Graphite is
Web-only until the Rust GUI ecosystem matures. Good progress this month has
been made building the web GUI with
[Vue](https://vuejs.org/). - Graphite 0.1 will now support only vector editing. This defers the large complexity of the graph render engine required for node-based raster editing. It should be less difficult to first focus on building a vector editor that improves upon the UX of Illustrator and Inkscape.

wgpu-rs is a WebGPU implementation and API in Rust.

- “wgpu-core”-0.7.1 was published with fixes
- API updated for blending states, cull faces, vertex formats
- Zero-initialization of buffers upon use
- Validation of texture bindings, index formats for strip topologies
- Binding tracker was rewritten with test-ability in mind, bugs fixed
- The player learned to resize the window properly. API traces can now be replayed on Linux even when swapchain recreation events are present
- SPIRV-Cross was made optional, which was useful for Deno in order to work around the linking conflict with “rusty_v8”

gfx-rs is a portable low-level graphics abstraction layer.

- API got
`PhysicalDeviceProperties`

containing limits and properties of physical devices that are not opt-in. - SPIRV-Cross dependency was made optional, while Naga is required.
- Vulkan backend learned to target Vulkan 1.1 and 1.2 internally.
- DX12 understood more limits.
- GL backend fixed WebGL initialization and EGL library discovery.

naga is the shader translation library/tool.

- Versions 0.3.1 and 0.3.2 were published with fixes
- API: function calls turned into statements, image queries , and stores, understanding of push constants.
- Validation: type validation was re-written and improved, new control flow analysis was added to check for uniformity requirements. In addition, this step now collects the image-sampler pairs used by the module.
- Backends: lots of fixes and filling of the gaps
- Infrastructure:
`convert`

example was removed in favor of the default binary target. The native shaders (produced by the snapshot tests) got validated on CI using platform tools.

Distill is an asset pipeline for games, reading artist-friendly formats from disk, processing them into your engine-ready formats, and delivering them to your game runtime. Distill handles dependencies between assets, import & build caching, cross-device hot reloading during development, packing assets for a shippable game build, and more.

Distill’s design is inspired by Unity’s asset system and [Frostbite’s Scaling
the Pipeline](https://media.contentapi.ea.com/content/dam/eacom/frostbite/files/scaling-the-pipeline.pptx). Distill leverages purity in the
functional-programming sense to deliver a robust and scalable experience for the
asset processing pipeline. With [LMDB](https://symas.com/lmdb/) backing storage of
metadata, Distill is able to avoid blocking asset loading while assets are being
imported which eliminates the most common frustration with existing commercial
offerings. Additionally, Distill is able to provide fully consistent snapshots
of asset metadata to readers over [capnp-rpc](https://github.com/capnproto/capnproto-rust).

`basis-universal`

provides bindings for [Binomial LLC](http://www.binomial.info)’s [Basis
Universal texture codec](https://github.com/BinomialLLC/basis_universal).

Basis Universal is a state-of-the-art
[supercompressed](http://gamma.cs.unc.edu/GST/gst.pdf) texture codec that was
recently [open-sourced](https://opensource.googleblog.com/2019/05/google-and-binomial-partner-to-open.html) by Binomial in partnership
with Google. It was [contributed](https://www.khronos.org/blog/google-and-binomial-contribute-basis-universal-texture-format-to-khronos-gltf-3d-transmission-open-standard) to the
Khronos glTF 3D Transmission Open Standard.

The library has two primary uses:

- Compresses and encode textures “offline” to a custom format
- Transcoding: Unpack the custom format directly to GPU-friendly compressed formats. The final format can be chosen at game runtime to be compatible with available GPU hardware.

Basis universal format can also store mipmapped textures and cubemaps, neither of which is possible with “normal” file formats. Mipmaps can be generated by the library during compression.

Compression is very slow (around 7-10s for a 2k texture) but transcoding is relatively fast (around 5-40ms for a 2k texture depending on quality). Memory savings at runtime are generally >= 75% (depending on the transcode format and quality)

[bevy_egui](https://github.com/mvlabat/bevy_egui) provides a [Egui](https://github.com/emilk/egui) integration
for the [Bevy](https://github.com/bevyengine/bevy) game engine.
It supports [bevy_webgl2](https://github.com/mrk-its/bevy_webgl2) and implements the full set of Egui features
(such as clipboard and opening URLs).

This month versions 0.2 and 0.3 were released, providing an integration with Egui 0.9 and 0.10 respectively.

Try out the [online demo](https://mvlabat.github.io/bevy_egui_web_showcase/index.html).

[rkyv](https://github.com/djkoloski/rkyv) is a zero-copy deserialization framework for Rust. It’s similar to
FlatBuffers and Cap’n Proto and can be used for data storage and messaging.

[Version 0.4](https://github.com/djkoloski/rkyv/releases/tag/v0.4.0) was released this month and brought some big changes
and improvements:

- Major traits have been refactored and renamed to clarify their roles
- Shared pointers (
`Rc`

,`Arc`

,`Weak`

) can now be serialized, deserialized, and validated with correct ownership semantics - Serialization, deserialization, and validation all now support custom contexts
- Greatly improved support for 32- and 64-bit archives by implementing Archive
for
`usize`

and`isize`

- More comprehensive documentation in the
[book](https://djkoloski.github.io/rkyv)

This release completes the project’s initial feature set, and a [request for
feedback](https://github.com/djkoloski/rkyv/issues/67) has been opened to help with future project
planning.

[wasm_plugin](https://github.com/alec-deason/wasm_plugin) is a new low-ish level tool for easily hosting WASM based plugins
for modding or scripting.

It consists of two crates:

[wasm_plugin_host](https://lib.rs/crates/wasm_plugin_host)which wraps a wasmer instance with methods for calling functions on the guest plugin.[wasm_plugin_guest](https://lib.rs/crates/wasm_plugin_guest)which provides an attribute macro to easily export functions to the host.

## Popular Workgroup Issues in GitHub [#](https://gamedev.rs#popular-workgroup-issues-in-github)

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[gfx-rs’s “contributor-friendly” issues](https://github.com/gfx-rs/gfx/issues?q=is%3Aissue+is%3Aopen+label%3Acontributor-friendly).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[A/B Street’s “good first issue” issues](https://github.com/a-b-street/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/good%20first%20issue).

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!