---
title: 'This Month in Rust GameDev #43 - February 2023'
url: https://gamedev.rs/news/043/
author: Rust GameDev WG
published: '2023-03-08'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 43rd issue of the Rust GameDev Workgroup’s
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

[Announcements](https://gamedev.rs/news/043/#announcements)[Game Updates](https://gamedev.rs/news/043/#game-updates)[Engine Updates](https://gamedev.rs/news/043/#engine-updates)[Learning Material Updates](https://gamedev.rs/news/043/#learning-material-updates)[Tooling Updates](https://gamedev.rs/news/043/#tooling-updates)[Library Updates](https://gamedev.rs/news/043/#library-updates)[Other News](https://gamedev.rs/news/043/#other-news)[Discussions](https://gamedev.rs/news/043/#discussions)[Requests for Contribution](https://gamedev.rs/news/043/#requests-for-contribution)

## Announcements [#](https://gamedev.rs#announcements)

### Rust GameDev Meetup [#](https://gamedev.rs#rust-gamedev-meetup)

![Gamedev meetup poster](../../assets/6cd0b5ad7265b2c9.png)


The 24th Rust Gamedev Meetup took place in February. You can watch the recording
of the meetup [here on Youtube](https://youtu.be/HTxX-Wm-3R8). Here was the schedule
from the meetup:

- Micro Game Engine -
[@AngelOnFira](https://twitter.com/AngelOnFira) - Graphite -
[@GraphiteEditor](https://twitter.com/GraphiteEditor)

The meetups take place on the second Saturday of every month via the [Rust
Gamedev Discord server](https://discord.gg/yNtPTb2) and are also [streamed on
Twitch](https://twitch.tv/rustgamedev).

## Game Updates [#](https://gamedev.rs#game-updates)

### Cootsmania [#](https://gamedev.rs#cootsmania)

![Cootsmania gameplay](../../assets/29ea8052dda30706.jpg)


[Cootsmania](https://kuviman.itch.io/cootsmania) ([GitHub](https://github.com/kuviman/cootsmania))
is a multiplayer racing game made for [Ludwig Jam 2023](https://itch.io/jam/ludwig-2023) in 10 days
by [@kuviman](https://github.com/kuviman) (programming), [@rincs](https://rincsart.com) (art), and [@Brainoid](https://twitter.com/brainoidgames) (music & sfx).

The game is about racing other players around Ludwig’s house towards the next Coots (Ludwig’s cat) location. Every round half of the players get eliminated and eventually a winner is decided.

The game is written using a custom engine: [Geng](https://github.com/kuviman/geng).

![Tunnet screenshot: low poly models, blocky terrain, FPS view with a drill in hands](../../assets/1a6ed93515acb208.jpg)

Tunnet ([Steam](https://store.steampowered.com/app/2286390/Tunnet), [Itch.io](https://puzzled-squid.itch.io/tunnet)) by
[@puzzled_squid](https://puzzledsquid.xyz) is a small puzzle/exploration game where you
play as a robot technician who has been tasked with building a computer network
in an underground complex.

The project is implemented using the Bevy engine. It is currently under
development and is expected to be released later this year.
This month, the announcement trailer and the first few pages of the manual have
been published on the [project page](https://puzzled-squid.itch.io/tunnet).

![Debug window: terrain tiles, units, and paths](../../assets/ff683fa6fa548f54.png)

Open Combat ([Website](https://opencombat.bux.fr/), [GitHub](https://github.com/buxx/OpenCombat),
[Discord](https://discord.gg/6P2vtFh2Px)) is a real time tactical game
which takes place during the 2nd World War.

Some major changes this month :

- A live debug window has been introduced (using
[egui](https://github.com/emilk/egui)and its[ggegui](https://github.com/NemuiSen/ggegui)integration). It allows to live-modify and adjust the gameplay of the running game. - A big source code split has been done (see
[the merge request](https://github.com/buxx/OpenCombat/pull/104)) which separated the game logic and GUI. It allows running the game logic as a standalone server and working on different game parts more easily. - Integration of
[puffin](https://github.com/EmbarkStudios/puffin)to inspect performances

The developers are also working on high-definition infantry sprites integration and on a high-definition map (and are searching for graphic designer help!).

![A sheep with umbrella](../../assets/0fc8d78c9a11efef.gif)


[Tiny Glade](https://store.steampowered.com/app/2198150/Tiny_Glade/) is a small relaxing game about doodling
castles.

[@anopara](https://twitter.com/anastasiaopara) and [@h3r2tic](https://twitter.com/h3r2tic) recently added [terrain editing](https://store.steampowered.com/news/app/2198150/view/3651890488940565185).
They then faced an important game design question: how would sheep handle
it? Well, these cuddly little floofs are not mountain goats,
so the developers gave them tiny umbrellas.

Read more in their latest [Steam blogpost](https://store.steampowered.com/news/app/2198150/view/3669907614196390626).

![Screenshot of Cargo Space: a cosmonut flying between lots of orange squares](../../assets/45045e8ecd460e14.png)


[Cargo Space](https://helsing.studio/cargospace) ([Discord](https://discord.gg/ye9UDNvqQD)) by
[@johanhelsing](https://mastodon.social/@johanhelsing) is a co-op 2d space game where you build
a ship and fly it through space looking for new parts, fighting pirates and the
environment.

The game uses its own homemade XPBD-based physics engine implemented directly
using [Bevy](https://github.com/bevyengine/bevy) systems and types. This month the implementation was fleshed out
adding important features such as collision layers, composite colliders, one-way
platforms, and an efficient collision broadphase.

In other words, this means ship-to-ship collisions are finally happening. This was previously tricky, since ships are a combination of box colliders when colliding with each other and bevy_ecs_tilemap colliders (when colliding with the player).

One part of the broadphase implementation was split out into a new crate,
[bevy_sparse_grid_2d](https://github.com/johanhelsing/bevy_sparse_grid_2d). It provides a simple and convenient way to query for
entities that share one or more grid cells based on their axis-aligned bounding
box (AABB).

Read more about Cargo Space’s physics in [the long and detailed blog
post](https://johanhelsing.studio/posts/cargo-space-devlog-5).

![Many creatures flying and casting shadows](../../assets/591144f25b2f20ad.gif)

CyberGate ([YouTube](https://youtube.com/channel/UClrsOso3Xk2vBWqcsHC3Z4Q), [Discord](https://discord.gg/R7DkHqw7zJ)) is an
ambitious multiplayer project from CyberSoul, currently in development.
With cutting-edge procedural generation and artificial intelligence,
it promises to immerse players in a mysterious and enigmatic universe
filled with strange creatures and hidden secrets.

The latest updates to CyberGate include:

- A rebuilt renderer, providing improved graphics and performance.
- Shadow map cascades with seamless transitions for smooth shadow rendering.
- Soft shadows for more realistic shadow effects.
- A fog effect to create atmospheric depth and immersion.
- A sky box to add visual interest and realism to the game world.
- Support for importing GLTF models, expanding the range of assets available.

Join the journey into the unknown and help shape the future of CyberGate!
[Join the Discord server](https://discord.gg/R7DkHqw7zJ) to participate in upcoming Phase 7.0!

![Characters standing near a house](../../assets/53ed194a494c12ba.jpg)


[Legend of Worlds](http://legendofworlds.com) ([Discord](https://discord.gg/aqD7H3F7nz), [Twitter](https://twitter.com/DreamsectGames))
is a cross-platform, cross-play, 2D online sandbox multiplayer
experience where you can join, play, create, and share player-created worlds.

[The latest dev log](http://legendofworlds.com/dev-log-2) from [Rou](https://twitter.com/DreamsectGames) covers an update
to the open-source game engine created for this game.

Legend of Worlds uses Toxoid Engine. Toxoid is a cross-platform, polyglot, open-source WebAssembly game engine written in Rust. The architecture has been updated so that Toxoid games can now share memory directly between WASM components, and map access to the data values rather than deserializing a set of values every time, resulting in “massive performance gains”.

![Steam page screenshot](../../assets/84ec7524d8a23f06.jpg)


[Hydrofoil Generation](https://hydrofoil-generation.com/)
([Steam](https://store.steampowered.com/app/1448820/Hydrofoil_Generation/), [Facebook](https://facebook.com/HydrofoilGenerationSailing/), [Discord](https://discord.gg/DtKgt2duAy/))
is a realistic sailing/foiling inshore simulator in development for PC/Steam
that puts you in the driving seat of modern competitive sailing.

Hydrofoil Generation released on February 16th 2023 on Steam Early Access after almost 3 years of development.

The game is written completely in Rust, using a custom engine based on DirectX 11, physics powered by Rapier-3D.

Stefano Casillo, programmer commented: “Rust delivered on every single promise. I never experienced such an uneventful launch and QA as the one we had for Hydrofoil Generation. The software stability has been impressive since the beginning of the project and confirmed the trend at release with very few problems all very easy to address”.

Hydrofoil Generation currently sits at a very positive review rate of 96% on the Steam page and is praised for its challenging gameplay, performance and realistic physics.

![A cyclops attack](../../assets/4db13d91856ed754.jpg)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In February, swing SFX were added to the new sword abilities. Blocks were added
to spots that can spawn NPCs. Moderation badges were added, and fixes to the chat
command were made. A student contributed to Veloren on their two-week internship
about game design, you can [read about that here](https://veloren.net/devblog-205#potion-shops-were-created-during-a-two-week-internship-by-nixda). Work is
being done to add more functionality to sites, which are small models placed
around the world.

February’s full weekly devlogs: “This Week In Veloren…”: [#205](https://veloren.net/devblog-205), [#206](https://veloren.net/devblog-206).

![Training scenario screenshot: user is teached how to attach thrusters](../../assets/9474c03215770273.png)


[triverse](https://cragwind.itch.io/triverse) by [@cragwind](https://cragwind.com) is a WIP smart-pause RTS with custom unit creation
on a triangle grid canvas.
[This month’s update](https://cragwind.com/posts/scenarios-and-playability) includes:

- Training and challenge scenarios.
- Grid lines when building.
- Edge panning in fullscreen mode.
- Radar proximity markers to indicate objects that are off the visible portion of the map.

![concrete and rock blocks, water, and a tree casting a shadow](../../assets/21bbca2e4797cea8.jpg)


[Idu](https://epcc.itch.io/idu) ([Discord](https://discord.gg/MeGauteMj3)) is a strategic sandbox game about growing
plants that wish to reclaim nature, developed by [Elina Shakhnovich](https://mastodon.gamedev.place/@eli)
and [Johann Tael](https://mastodon.gamedev.place/@johann) featuring a bespoke Vulkan-based engine in Rust.

This month [a new demo was released](https://epcc.itch.io/idu/devlog/492261/demo-version-9-available-new-worlds):

- A new world generation with new buildings, stairs, caves, paths, and beaches.
- Simpler inventory management for materials.
- New help text that explains the game mechanics better.
- A configurable FOV and fullscreen toggle settings.
- Wind now affects not only leaves but tree branches as well.
- Significant GI performance improvements.

![Two giraffe character with debug bounding forms visualised](../../assets/02df378fd386a616.jpg)


Necking is a WIP competitive/cooperative 1-on-1 online game where players are giraffes and fight for male dominance in the giraffe way.

This month the devs have released [the first devlog](https://devildahu.ch/devlog/necking-1)
that tells about:

- The concept of the game and what inspired it.
- Custom joint system and migration to Rapier physics lib.
- Bevy controls design, including tongue controls.
- The
[cuicui](https://github.com/devildahu/bevy_mod_cuicui)UI framework.

## Engine Updates [#](https://gamedev.rs#engine-updates)

![godot-rust GDExtension logo](../../assets/fbb999d324851284.png)


The [release of Godot version 4.0](https://godotengine.org/article/godot-4-0-sets-sail/) marks a significant milestone in
the game development ecosystem. godot-rust aims to bring the open-source
game engine to the Rust community.

For the [Godot 4 (GDExtension) binding](https://github.com/godot-rust/gdextension), February was a very
productive month, with a handful of new contributors and [16 merged pull
requests](https://github.com/godot-rust/gdextension/pulse/monthly). An up-to-date feature overview is available
[in issue #24](https://github.com/godot-rust/gdextension/issues/24). Last month’s changes include:

- Support for arrays, packed arrays, and dictionaries
- Support for some geometric types (vectors, quaternions, colors)
- Bugfixes regarding ref-counts, use-after-free, memory leaks

On the [Godot 3 (GDNative) side](https://github.com/godot-rust/gdnative), lots of quality-of-life
improvements have found their way into the library:

- Class self-registration based on
`inventory`

crate - Flexible self types:
`fn instance(#[self] this: Instance<Self>)`

- Trait entry point:
`#[callbacks] impl GDNativeCallbacks for MyLibrary {...}`


Both bullet lists are examples for how the GDNative and GDExtension bindings mutually benefit each other, reusing proven designs for user-friendly Rust APIs.

![blue_engine egui-plugin demo: color picker](../../assets/2048505d9849b2e0.png)


[Blue Engine](https://github.com/AryanpurTech/BlueEngine) by [@ElhamAryanpur](https://github.com/ElhamAryanpur) is an easy to use, extendable, and
portable graphics engine built to make it easier to render 2D or 3D graphics.

Although the month of Febuary was slow for the development of the engine, there
have been significant efforts towards the addition of [documentation](https://docs.rs/blue_engine)
and the eventual release of the next version. In the meantime,
the plugins have favored significant updates and development in the month,
notably the [egui](https://github.com/AryanpurTech/BlueEngineEGUI) plugin.

Now the [egui plugin](https://github.com/AryanpurTech/BlueEngineEGUI) allow you to render objects of the engine direction
inside an egui window. This feature was built in collaboration with [@Noswad](https://github.com/TheNoswad).

This also introduced a new option in Objects: `is_visible: bool`

which hides an object
from getting rendered if set to false (set to `true`

as default). This allows
you to hide an object from getting rendered on the background of egui, and can then
add it to be rendered inside an egui window instead. So far the system on the second
design, suggestions are welcome to cement a better design. Refer to [example](https://github.com/AryanpurTech/BlueEngineEGUI/blob/master/examples/custom_3d.rs).

![Image of a scene made with Ambient](../../assets/6ae6dfc17af87e50.jpg)


After over a year in development, [version 0.1 of Ambient](https://ambient.run/post/introducing-ambient)
(formerly known as Dims) was unveiled to the public. It is an open-source
multiplayer 3D game runtime, compatible with any language that compiles
to/runs on WebAssembly, and is designed to make it easy to build and deploy
rich multiplayer worlds and experiences.

It is guided by several core principles, including seamless networking, data-oriented design, interoperability, and more. The core runtime is written in Rust and uses WGPU for graphics, Quinn for networking, and WebAssembly for user logic. This allows it to run on all major desktop platforms, with active work underway for the Web and other targets.

Check out [the GitHub](https://github.com/AmbientRun/Ambient) (2600 stars!) to get started with
building for/or on Ambient yourself, or chat with the developers and other
explorers on [the Discord](https://discord.gg/ambient).

*Discussion: /r/rust, Hacker News*

[Geng](https://github.com/kuviman/geng) by [@kuviman](https://github.com/kuviman) is a game engine that is used by him & friends
for mostly making small games for game jams.

The focus is to work on the web first (using WebGL1), but can also work easily on native platforms.

Font rendering is done using sdf textures,
which are being created on GPU based on [this article](https://astiopin.github.io/2019/01/06/sdf-on-gpu.html).
Some font improvements from February:

- Better curve approximation (still can be done better like in the article).
- Use euclidean distance instead of manhattan.
- Added a method to create sdf texture for text. (previously font only had sdf texture atlas with every glyph).

Support was added for OpenGL blend equations - e.g. minmax blending, which is now used instead of depth buffer for sdf textures

Also, some improvements related to sound:
API to query `Sound`

duration,
starting sound playback from specific position,
and changing the speed of `SoundEffect`

.

![a hi-tech soldier model blending between 5 animations](../../assets/d0b19f25b277178e.gif)

[Fyrox](https://fyrox.rs) ([GitHub](https://github.com/FyroxEngine/Fyrox), [Discord](https://discord.com/invite/xENF5Uh), [Twitter](https://twitter.com/DmitryNStepanov))
is a game engine that aims to be easy to use and provide a large set
of out-of-the-box features. This month’s updates include:

[Audio system’s refactoring](https://fyrox.rs/blog/post/twif13#audio-system-refactoring)to make it much more flexible.[Root motion](https://fyrox.rs/blog/post/twif14#root-motion)animation technique helps prevent “floating” or “sliding” effects.[Blend space](https://fyrox.rs/blog/post/twif15#blend-space)allows blending many animations based on two numeric input parameters (mostly useful for blending locomotion animations based on speed and direction).[Editor restyling](https://fyrox.rs/blog/post/twif16/#editor-restyling)brings cleaner and modern UI.

February’s full weekly devlogs: [#13](https://fyrox.rs/blog/post/twif13), [#14](https://fyrox.rs/blog/post/twif14),
[#15](https://fyrox.rs/blog/post/twif15), and [#16](https://fyrox.rs/blog/post/twif16).

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

![Game Preview](../../assets/faa5689f353c9fee.png)


[@grantshandy](https://github.com/grantshandy/) published an [article](https://grantshandy.github.io/posts/raycasting) about creating a simple
first-person game in Rust with [WASM-4](https://wasm4.org). It covers the basics of a ray casting
algorithm and minifying Rust with WebAssembly. You can play the finished game
[here](https://grantshandy.github.io/wasm4-raycaster/).

*Discussion: /r/rust*

### Voxel Meshing [#](https://gamedev.rs#voxel-meshing)

![Simple white and green voxels with ambient occlusion enabled](../../assets/0016f7d0b7d2473c.jpg)


Authors of [Space Farer](https://playspacefarer.com) - a WIP voxel-based survival/building
game - published a couple of articles about voxel meshing:

[“Voxel Meshing for the Rest of us”](https://playspacefarer.com/voxel-meshing)is an introduction to voxel meshing techniques.[“How (Not) to Improve Voxel Meshing Performance”](https://playspacefarer.com/voxel-meshing-performance)tells about some zero-copy optimizations.

![tutorial’s result: player’s ship moves and shoots into the enemy above](../../assets/e0fea4b6cdb7a304.gif)


[@whoisryosuke](https://mastodon.gamedev.place/@whoisryosuke) released [the first part in a series](https://whoisryosuke.com/blog/2023/making-galaga-in-rust-with-bevy-part-1)
on how to build a Galaga clone using Bevy.
It covers 2D sprites and meshes basics, setting up custom shaders for animated background,
and adding sound.

## Tooling Updates [#](https://gamedev.rs#tooling-updates)

### Sprite and Pixel Art Editor [#](https://gamedev.rs#sprite-and-pixel-art-editor)

![Image editor screenshot](../../assets/f39dc1bd57b0e4a5.png)


A sprite and pixel art editor made with egui and macroquad is being
developed by @yds12 ([GitHub](https://github.com/yds12), [Mastodon](https://fosstodon.org/@yds/)).
The project is already usable, but has not been made public yet. Current
features are:

- Drawing w/ brush, eraser, lines, rectangles, bucket (fill w/ color).
- Color selector, editable palette, and eyedropper (pick a color from the canvas).
- Resize or completely erase the canvas.
- Move the camera, zoom in and out.
- Selection (rectangular only for now), deleted, copied, and pasted; flip selection (horizontal or vertical).
- Layers: create, remove, moved up/down, and control visibility and opacity.
- Spritesheet: specify how many columns and rows your image has, and an animated preview will be displayed in a window w/ configurable scale.
- Save/load projects (with all its settings), export and import PNG/JPG.
- Status bar w/ info about canvas size, canvas position, color under mouse, etc.

The source is planned to be released in the next few weeks.

![Graphite logo](../../assets/6df4fd1f2cd8445e.png)


Graphite ([website](https://graphite.rs), [GitHub](https://github.com/GraphiteEditor/Graphite),
[Discord](https://discord.graphite.rs), [Twitter](https://twitter.com/GraphiteEditor)) is a free,
in-development raster and vector 2D graphics editor based around a Rust-powered
node graph compositing engine.

New features from February’s [sprint 23](https://github.com/GraphiteEditor/Graphite/milestone/23):

- Shaping up: Editing shapes is now easier thanks to point selection and manipulation improvements.
- Deep dive: The user experience of nested layer selection is improved by introducing “Deepest” and “Shallowest” modes.
- Scroll settings: Scroll up-and-down, or zoom in-and-out, at your preference using the new configuration for scroll wheel behavior.
- Graph growth: Additional node graph engineering introduces graceful type checking and brings GPU-accelerated compositing closer to realization.

As always, new contributors are kindly invited to
[get involved](https://graphite.rs/contribute) and take on
[approachable issues](https://github.com/GraphiteEditor/Graphite/labels/Good%20First%20Issue) with help from the
project’s friendly and supportive developer community on Discord.

[Open Graphite](https://editor.graphite.rs) in your browser and start creating! Share your
designs with #MadeWithGraphite on Twitter.



![egui app with lots of complex widgets, 2D and 3D views, etc](../../assets/9a7399c9d2e5d749.jpg)

[Click to see Rerun’s latest demo video](https://youtube.com/watch?v=8ZpvOagRt-o)

[Rerun](https://rerun.io) ([Discord](https://discord.gg/PXtCgFBSmH)) lets you log images, point clouds
and other visual data as easy as you would log text.
The data is streamed in real-time to the Rerun Viewer
which you can run natively or in a browser.

The Rerun Viewer builds configurable visualizations based on the data you log and the relationships between it. It uses transform hierarchies to lay out scenes and connect related data. It lets you scroll back and forth in time, and toggle between showing your data along different timelines, e.g. log time and sensor time. It’s built to be fast so you can explore without waiting.


All built in Rust on top of [egui](https://github.com/emilk/egui) library,
with an API for both Rust and Python.

This month, after a year of work, [Rerun was open-sourced under MIT & Apache 2](https://github.com/rerun-io/rerun)!

*Discussions: /r/rust*

## Library Updates [#](https://gamedev.rs#library-updates)

![2D example with various groups of tiles highlighted](../../assets/71a6eede873f3301.jpeg)


[hexx](https://github.com/ManevilleF/hexx) is a hexagonal tools library made by [@ManevilleF](https://linktr.ee/ManevilleF):

- Manipulate hexagonal coordinates, draw rings, lines, wedges, etc.
- Generate hexagonal grids, with conversion between your world and the hexagonal coordinates system.
- Compute 3d meshes for your hexagons.

It’s engine-agnostic, but was made with [bevy](https://github.com/bevyengine/bevy) integration in mind
and provides 2D and 3D [examples](https://github.com/ManevilleF/hexx/tree/main/examples).

*Discussions: Twitter*

![nanoshredder demo: windows with shader code and result behind](../../assets/72384ec66ce7fb0a.gif)

[Nanoshredder](https://github.com/not-fl3/nanoshredder) is an experimental fork of
[makepad’s shader-compiler](https://github.com/makepad/makepad/tree/master/platform/shader_compiler).
It compiles rust-like DSL into GLSL, Metal and HLSL.

This month it got a little [web demo](https://not-fl3.github.io/miniquad-samples/shadertoy_cross.html):
[macroquad’s shadertoy](https://github.com/not-fl3/macroquad/blob/master/examples/shadertoy.rs), a live editor with
generated Metal/GLSL preview.

[blink-alloc](https://github.com/zakarumych/blink-alloc) is a brand new arena-allocator with bunch of improvements
over existing solutions that is
tested with [Miri](https://github.com/rust-lang/miri) and follows [“Strict Provenance Rules”](https://github.com/rust-lang/rust/issues/95228).

Arena-allocators offer extremely fast allocations and deallocations. Allocation is just a few pointer arithmetic operations. And deallocation is nearly no-op. In exchange arena-allocator requires a point in time when all previous allocations are unused to reset state.


Rust’s borrow-checker ensures the requirement for reset making it 100% safe to use.TL;DR great for games, servers, cli tools, and more.


blink-alloc provides thread-local and multi-threaded allocators -
`BlinkAlloc`

and `SyncBlinkAlloc`

.
Single-threaded version [performs many times faster than bumpalo](https://github.com/zakarumych/blink-alloc/blob/main/BENCHMARKS.md).
The author couldn’t find another implementation to compare
the multi-threaded version’s performance.

It also provided out-of-the-box to fetch `BlinkAlloc`

in task/thread
and return it back when done, keeping multiple `BlinkAlloc`

instances warmed.

On top of raw allocations blink-alloc provides `Blink`

type
that works as safe allocator adaptor.
`Blink`

can allocate memory and initialize it with values provided by user.
Users may provide values as-is, as closures, or as iterators.
`Blink`

’s API is safe with few exceptions for niche use cases.

Those familiar with `bumpalo`

may think of `Blink`

as of `bumpalo::Bump`

.
Though `Blink`


- drops all placed values on reset, which makes it usable with any kind of types without resource leaks.
- Accepts any iterator type, not just
`ExactSizeIterator`

implementations. - Is configurable to use any
`BlinkAllocator`

implementation, thus not tied to`Global`

.

Currently, Rust’s standard collection types may use custom allocators
only one nightly and with `allocator_api`

feature enabled.
blink-alloc uses `allocator-api2`

crate to work on both stable and nightly.
Integration with other crates is simple and doesn’t require depending on
blink-alloc, only on `allocator-api2`

.

![pecs example, same as in the README](../../assets/9337325c307582dd.png)

In the ECS environment, you can’t use the standard async/await approach, which can make implementing asynchronous logic painful.

[pecs](https://github.com/jkb0o/pecs) is a plugin for the [Bevy](https://github.com/bevyengine/bevy) engine that solves this problem.
It allows you to execute the code asynchronously by chaining multiple
promises as part of [Bevy’s ecs](https://bevyengine.org/learn/book/getting-started/ecs) environment.

Each promise takes the state and result of the previous promise as arguments,
as well as any Bevy ECS system parameter, and passes the modified
state and new promise/result to the next promise. It’s easy to register custom
promises that wait for user input, events, asset loading, and so on. You can
also use [pecs](https://github.com/jkb0o/pecs) to wait for any or all of multiple promises to complete
before continuing with the rest of the code, as well as to loop asynchronously
until a condition is met.

[seldom_state](https://github.com/Seldom-SE/seldom_state) is a Bevy plugin that adds a `StateMachine`

component that you
can add to your entities. The state machine will change the entity’s components
based on states, triggers, and transitions that you define. It’s useful
for player controllers, animations, simple AI, etc.

This month [seldom_state](https://github.com/Seldom-SE/seldom_state) 0.4 has been released:

- Transition builders (
`StateMachine::trans_builder`

) which let you pass data from triggers to states. - The
`AnyState`

state, which you can use wherever`StateMachine`

accepts state type parameters, which lets you create transitions from any state, etc - A
`leafwing_input`

feature for`leafwing-input-manager`

integration, which enables 9 built-in triggers related to input.`JustPressedTrigger`

, for example. `OptionTrigger`

and`BoolTrigger`

traits, which are simpler to implement than`Trigger`

.

![preview of a grass chunk](../../assets/04cdc128aec25f61.png)

[warbler_grass](https://github.com/EmiOnGit/warbler_grass) is a new experimental [Bevy](https://github.com/bevyengine/bevy) plugin.
The goal is to provide an ergonomic, but performant way
to easily render huge amounts of grass.

Some of the currently integrated features are dynamic directional wind and chunk loading.

The project is now also published on [crates.io](https://crates.io/crates/warbler_grass).

[taffy](https://github.com/dioxuslabs/taffy), the pure Rust UI layout crate, now supports CSS grid!
Build your inventory menus with ease,
or make that sudoku game you’ve always dreamed of.

Taffy v0.3 also comes with more than a few performance improvements and bug fixes;
for more details, check out our [release notes](https://github.com/DioxusLabs/taffy/blob/main/RELEASES.md#030).

![cvars used in the RustCycles game - showcasing a console for the Fyrox engine](../../assets/52318e4d396f80d4.png)

[Cvars](https://crates.io/crates/cvars) ([GitHub](https://github.com/martin-t/cvars), [Discord](https://discord.gg/aA7hCFvYh9)) by [@martin-t](https://github.com/martin-t)
are a simple way to store settings you want to change at runtime
without restarting your game.

They offer a way to change struct fields based on their name.
This means games can store their config in a plain old struct
and use its statically typed fields with no overhead.
[Cvars](https://crates.io/crates/cvars) provide a derive macro to also allow changing each field
dynamically at runtime from a TUI.

The cvars project includes in-game consoles [for macroquad](https://github.com/martin-t/cvars#macroquad-console)
and [for Fyrox](https://github.com/martin-t/cvars#fyrox-console).

In addition to reading and setting cvars, they support history and offer a help message for new users. More advanced features such as autocomplete are planned for the next release.

*Discussions: /r/rust_gamedev*

## Other News [#](https://gamedev.rs#other-news)

- Other game updates:
[@Tantan shared a vlog](https://youtube.com/watch?v=xQLVYnD43vI)about the space colonization procedual tree generation technique[he’s using for his voxel game](https://github.com/TanTanDev/shrubbery).- Denis Lavrentev shared a couple of Primitive Engineering’s vlogs:
about
[chunk management](https://youtube.com/watch?v=_ZDagizAllY)and[the crafting system](https://youtube.com/watch?v=ILslZgEBlAo). [Hoive](https://github.com/cooscoos/Hoive)is multiplayer Rust version of the Hive boardgame.[Tigris and Euphrates](https://reddit.com/r/rust_gamedev/comments/111xlv7/tigris_n_euphrates)is a Rust version of the same-titled boardgame written using macroquad.[Scalp Invaders](https://metalmancy.itch.io/scalp-invaders)is game where you play as a colony of lice, launching themselves with great abandon through the scalp of a disgusted victim.

- Other engine updates:
[alkahest-rs](https://github.com/AlkimiaStudios/alkahest-rs)released a couple of vlogs about[UI rendering in general](https://youtube.com/watch?v=cvVDSin0jpA)and[rendering children widgets inside panels](https://youtube.com/watch?v=aaXflcuqQqw).

- Other learning material updates:
[Faith Ekstrand published the first article](https://collabora.com/news-and-blog/blog/2023/02/02/exploring-rust-for-vulkan-drivers-part-1)in a series about using Rust for Vulkan drivers.[“Learn WGPU” was updated to wgpu v0.15](https://sotrh.github.io/learn-wgpu/news/0.15).[PhaestusFox posted more episodes](https://youtube.com/@PhaestusFox/videos)of their “Platformer in Bevy” YouTube series.- The Unofficial Bevy Cheatbook by got two new chapters about
[“Cameras”](https://bevy-cheatbook.github.io/features/camera.html)and[“HDR, Tonemapping, Bloom”](https://bevy-cheatbook.github.io/features/hdr-tonemap.html). [Jan Metzger published an article](https://zazama.de/blog/creating-an-fps-limiter-in-rust-by-hooking-directx)about dynamically limiting FPS in DirectX games from an external DLL.

- Other tooling updates:
[denog](https://reddit.com/r/rust/comments/10tsfry/denog)is a gamedev-oriented fork of Deno with built-in window system integration.[cargo-nds](https://github.com/SeleDreams/cargo-nds)and[libnds-rs](https://github.com/SeleDreams/libnds-rs)allow[writing Rust games for Nintendo DS](https://reddit.com/r/rust/comments/10yk0kg/porting_rust_to_the_nntendo_ds), though both are WIP.

- Other library updates:
[dlss_wgpu](https://github.com/JMS55/dlss_wgpu)provides Deep Learning Super Sampling for wgpu.[oxidized_navigation v0.2](https://github.com/TheGrimsey/oxidized_navigation/blob/master/CHANGELOG.md#020-2023-02-13)brings full support for walkable radius, areas, and area cost multipliers.


## Discussions [#](https://gamedev.rs#discussions)

- /r/rust_gamedev:
- /r/rust:

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[‘Are We Game Yet?’ wants to know about projects/games/resources that aren’t listed yet](https://github.com/rust-gamedev/arewegameyet#contribute).[Graphite is looking for contributors](https://graphite.rs/contribute)to help build the new node graph and 2D rendering systems.[winit’s “difficulty: easy” issues](https://github.com/rust-windowing/winit/issues?q=is%3Aopen+is%3Aissue+label%3A%22difficulty%3A+easy%22).[Backroll-rs, a new networking library](https://github.com/HouraiTeahouse/backroll-rs/issues).[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[A/B Street’s “good first issue” issues](https://github.com/a-b-street/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/D-Good-First-Issue).[Ambient’s “good first issue” issues](https://github.com/AmbientRun/Ambient/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22).

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to @rust_gamedev on [Twitter](https://twitter.com/rust_gamedev),
[Mastodon](https://mastodon.gamedev.place/@rust_gamedev), or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev)
if you want to receive fresh news!

**Discuss this post on**:
[/r/rust_gamedev](https://reddit.com/r/rust_gamedev/comments/11m3z9e/rust_gamedev_43),
[Twitter](https://twitter.com/rust_gamedev/status/1633533886566105088),
[Mastodon](https://mastodon.gamedev.place/@rust_gamedev/109989058552826681),
[Discord](https://discord.gg/yNtPTb2).