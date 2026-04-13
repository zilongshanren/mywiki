---
title: 'This Month in Rust GameDev #8 - March 2020'
url: https://gamedev.rs/news/008/
author: Rust GameDev WG
published: '2020-04-08'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the eighth issue of the Rust GameDev Workgroup’s monthly newsletter.

[Rust](https://rust-lang.org) is a systems language pursuing the trifecta:
safety, concurrency, and speed.
These goals are well-aligned with game development.

We hope to build an inviting ecosystem for anyone wishing
to use Rust in their development process!
Want to get involved? [Join the Rust GameDev working group!](https://github.com/rust-gamedev/wg#join-the-fun)

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).
Feel free to send PRs about your own projects!

## Spreading the Word [#](https://gamedev.rs#spreading-the-word)

If you’re working on a project that heavily relies on some engine/framework,
consider informing its authors about your work:
as the community is growing it happens more and more that
frameworks/engines authors just don’t know about users of their libs
(this note was requested by Icefox in relation to [GGEZ projects](https://github.com/ggez/ggez/blob/master/docs/Projects.md)).

## Game Updates [#](https://gamedev.rs#game-updates)

![DynaMaze promotional image](../../assets/38d5d9989ca48292.png)


[DynaMaze](https://boringcactus.itch.io/dynamaze) is an [open-source](https://github.com/boringcactus/dynamaze) multiplayer
puzzle/strategy game written in Rust and compiled to WebAssembly, made by
[@boringcactus](https://github.com/boringcactus). Adjust the maze to build a path to your target and
keep the other players from getting to theirs.

![Slime99](../../assets/88efbcbf99f787e9.png)


[Slime99](https://gridbugs.itch.io/slime99) by [@stevebob](https://github.com/stevebob) is an [open-source](https://github.com/stevebob/slime99)
roguelike made for the [7 Day Roguelike 2020](https://itch.io/jam/7drl-challenge-2020) game jam.

A traditional roguelike where the outcomes of attacking and defending are pre-determined and visible. Gameplay revolves around fighting slimes, adding to your sequence of combat outcomes, and using abilities to modify the order in which combat outcomes occur. It’s set in a neon sewer!

![Will main menu](../../assets/8dd945f417470c86.png)


[Will](https://azriel.im/will) is a 2.5D moddable action/adventure game.

Highlights of [this month’s update](https://azriel.im/will/2020/03/13/join-me/) include:

- Going
[open-source](https://github.com/azriel91/autexousious) - Network play (early version)

![gameplay sample](../../assets/6ab09b729f1cae03.gif)


[@oliviff](https://twitter.com/oliviff) released [Tennis Academy: Dash](https://iolivia.itch.io/tennis-academy-dash)
[v0.1.7](https://twitter.com/oliviff/status/1243972292750819329):

- 👟 blue players are back
- 🎆 improved particle effects
- 🖼️ a few art fixes

Also, [@oliviff continues to work on their Rust gamedev tutorial](https://twitter.com/oliviff/status/1238978081429299201).

### For The Quest [#](https://gamedev.rs#for-the-quest)

![For The Quest screenshot](../../assets/c07eaaac98a311b0.jpg)


For The Quest is the working title for a game in early development by
[@seratonik](https://twitter.com/seratonik). Written entirely in Rust and compiled to WebAssembly,
For The Quest is destined to become a MMORPG set in a post-apocalyptic
Earth where your goal is to band together into like-minded factions to
not only survive in this new world, but to unearth the cause of humanity’s
downfall.

For The Quest is currently undergoing engine development with a focus on running smoothly in modern browsers using WebGL 2.0 before moving onto native desktop ports.

New developments in March:

- Collision and Activation-Based Triggerable Entities (Able to load new areas)
- New overworld “sky light” directional lighting shaders in addition to omni-directional point lighting for underground areas
- New Ice Cavern models and textures, establishing a hybrid pixel-art in 3D style - mapping tool has been expanded to allow for rotating “tiles” to build extensive environments in a simple text format for rapid prototyping
- Specular maps added to the engine and world for that extra shine
- Started refactoring the rendering pipeline to allow for screen-space effects such as reflections and ambient occlusion

Follow [@seratonik](https://twitter.com/seratonik) on Twitter for updates.

[Urban Gift](https://twitter.com/UrbanGiftGame): Teaser Video [#](https://gamedev.rs#urban-gift-teaser-video)

[Urban Gift](https://twitter.com/UrbanGiftGame) is part detective game and part superhero simulator.
This month a teaser video was released:

Follow development updates on [Twitter](https://twitter.com/UrbanGiftGame).

[Realm.One](https://github.com/Machine-Hum/realm.one) is an open-source MMO game
written using the Amethyst game engine.
This month two videos were posted:

[“GameDev in Rust (Episode 0)”](https://youtu.be/S5SCBe_CzjQ)- ECS-based design with Amethyst, networking and tiled 2d based design.[“GameDev in Rust (Episode 1): Monsters and AI!”](https://youtube.com/watch?v=JxT3r56aqcA)- how the monsters are managed on server-side and integration with Tiled map editor.

![ASCII art logo with an ant](../../assets/05c0caa2986ba5f8.png)


[Native Systems](https://nativesystems.rs) is working on “Colony Genesis” -
an ant colony sandbox game with ASCII graphics.

This month v0.1.1 and v0.1.2 versions were released. Some of the updates:

- Add color palette options to Settings including a modified palette for red-green color blindness
- Add lifecycles to more ant castes
- Nurse ants give food to larvae
- Nurse ants on the surface will return to the colony
- Fix for foragers getting stuck in dig state at colony entrance
- Updated pathfinding

![gameplay samble: moving platforms, projectiles, and changing gravity](../../assets/0bc40ecfc6a9e469.gif)


[Ascension 2](https://outkine.itch.io/ascension-2) by [@outkine](https://github.com/outkine) is a simple gravity-based platformer.

Hop your way through bite-sized levels while dodging spikes and turrets. Then, change the direction of gravity, and do it all again!


### pGLOWrpg [#](https://gamedev.rs#pglowrpg)

![Improved temperature map generation](../../assets/c281da20df517508.png)


[@Roal_Yr](https://twitter.com/Roal_Yr) tweeted a bunch of updates about their “pGLOWrpg” project:

[Rivers erosion](https://twitter.com/Roal_Yr/status/1236003795265519616): this will ensure no rivers flow upwards and the canyons through the landmass are more smooth.[River segmentation and width increment](https://twitter.com/Roal_Yr/status/1242824451449856004).[Improved the temperature map generation](https://twitter.com/Roal_Yr/status/1236268367968964610).[Improved topography map rendering](https://twitter.com/Roal_Yr/status/1236366942094622721).

![game screenshot](../../assets/e8b07d173153b430.png)



[Akigi]is a multiplayer online world where most believe that humans are inferior.

Some of March’s updates:

[Migration to specs is finished](https://devjournal.akigi.com/march-2020/058-2020-03-15.html).[Asset compilation rewrite](https://devjournal.akigi.com/march-2020/058-2020-03-15.html#asset-compilation-rewrite).[Deploying process update](https://devjournal.akigi.com/march-2020/059-2020-03-22.html).[Preparations for the initial alpha release is being done](https://devjournal.akigi.com/march-2020/060-2020-03-29.html).

Full devlogs:
[#056](https://devjournal.akigi.com/march-2020/056-2020-03-01.html),
[#057](https://devjournal.akigi.com/march-2020/057-2020-03-08.html),
[#058](https://devjournal.akigi.com/march-2020/058-2020-03-15.html),
[#059](https://devjournal.akigi.com/march-2020/059-2020-03-22.html),
[#060](https://devjournal.akigi.com/march-2020/060-2020-03-29.html),

![game screenshot: spheres!](../../assets/3c45c7573a2d887c.png)


In [Sphere Game](https://coffejunkstudio.itch.io/spheregame) by [Coffé Junk Studio](https://twitter.com/CoffeJunkStudio)
you control a sphere in a bowl-shaped 2D space:

Your goal is to hit the other spheres as hard as possible to shatter them into pieces! But take care; if you get hit too hard too often by other spheres, you will be smashed yourself! Avoiding them is challenging as the bent space keeps dragging you to the center. Can you destroy everything around you until you are the only one left?


The game is a test for the studio’s “Sphere Engine” engine that is being implemented using Rust and Vulkan.

![game screenshot: DNA](../../assets/682cc385499ab65b.png)


[Helix Repair](https://coffejunkstudio.itch.io/helix-repair) is another game by [Coffé Junk Studio](https://twitter.com/CoffeJunkStudio)
written using the same engine.
Your task is to repair a broken DNA sequence
by replacing wrong nucleobases with the right ones.
You have 20 seconds: how many nucleobases can you repair within that time?

The game was developed within one weekend during the Global Game Jam 2020, whose theme was “repair”.

[Garden](https://epcc.itch.io/garden) is an upcoming game centered around growing realistic plants.

[March](https://cyberplant.xyz/posts/march) devlogs were posted.
Some of the updates:

- Splashing sweat symbol water diffusion in the new soil;
- Herb improved leaf translucency;
- Joystickcollision detection, player movement;
- Artist palette debug tool for visualizing the forces acting upon a game object and its other vectors.

![new icons and ability descriptions](../../assets/55742febc8897b53.jpeg)


[Zemeroth](https://github.com/ozkriff/zemeroth) by [@ozkriff](https://twitter.com/ozkriff) is a minimalistic 2D turn-based tactical game.
Some of this month’s updates:

[Some of the text buttons were replaced by icons](https://twitter.com/ozkriff/status/1241718003470917635).- Ability descriptions.
- Popup screens and exit confirmation dialogs.
- New
`zgui`

widgets: ColoredRect, LayersLayout. - Inactive buttons are either hidden or grayed-out now.
- The project
[fully switched to](https://twitter.com/ozkriff/status/1244960610296696834)as the first step of the migration to`good-web-game`

[miniquad](https://github.com/not-fl3/miniquad).

![LoD](../../assets/48e79abbc84434a1.png)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG
inspired by Dwarf Fortress and Cube World.

Many systems have been worked on in March. Worldsim is making progress through simulation of civilization over time. The map has seen improvements for lighting. Certain parts of the UI have been going through big changes. Many small outstanding issues have been worked on by a few diligent contributors. Networking is also being reworked from the ground up.

Here is the March changelog:

```
- Added sfx for wielding/unwielding weapons
- Fixed NPCs attacking the player forever after killing them
- Added sfx for collecting, dropping and using inventory items
- New attack animation
- weapon control system
- Game pauses when in singleplayer and pause menu
- Added authentication system (to play on the official server register on https://account.veloren.net)
- Added gamepad/controller support
- Added player feedback when attempting to pickup an item with a full inventory
- Added free look
- Added Italian, Portuguese, and Turkish translations
```


![Hanging out](../../assets/0d9d84037595476d.png)


You can read more about some specific topics:

[New Networking Protocol](https://veloren.net/devblog-57#new-networking-protocol-by-xmac94x)[External Work](https://veloren.net/devblog-58#the-external-work-of-imbris)[Winit Issues](https://veloren.net/devblog-59#status-of-the-winit-update-branch)[UI Improvements](https://veloren.net/devblog-59#ui-improvements-by-pfau-and-co)[Map Improvements](https://veloren.net/devblog-60#map-improvements-by-sharp)[World Simulation Process](https://veloren.net/devblog-61#world-simulation-process-by-zesterer)

With the Content Update scheduled to come out at the end of April, many systems will be finishing up development. Keep a lookout for the launch party!

March’s full weekly devlogs: “This Week In Veloren…”:
[#57](https://veloren.net/devblog-57),
[#58](https://veloren.net/devblog-58),
[#59](https://veloren.net/devblog-59),
[#60](https://veloren.net/devblog-60),
[#61](https://veloren.net/devblog-61).

## Library & Tooling Updates [#](https://gamedev.rs#library-tooling-updates)

![lighing demo](../../assets/fa0c09200da9ea0b.gif)


[bracket-lib](https://github.com/thebracket/bracket-lib) (previously `rltk_rs`

) by [@blackfuture](https://patreon.com/blackfuture)
is a Rust implementation of [C++ Roguelike Toolkit](https://github.com/thebracket/rltk).

Some of this month’s updates:

- Input API.
`bracket-color`

now supports pallets and RGBA.- The graphical (OpenGL, WASM, Amethyst) render targets now support alpha channel.
- Arbitrary clipping window on any layer.
- New
`VirtualConsole`

system. - New functions for right-justifying printed text.
- Fonts and dimensions in terminal layers can now be switched at run-time.
- New layer type that lets you specify glyph position as a float.
- New sprite layer.
- Updated examples.

Main updates:

[simba](https://crates.io/crates/simba)- a crate that defines a set of traits for writing code that can be generic with regard to the number of lanes of the input numeric value. Those traits are implemented by f32, u32, i16, bool as well as SIMD types like f32x4, u32x8, i16x2, etc.- benchmarks:
[“SIMD Array-of-Structures-of-Arrays in nalgebra and comparison with ultraviolet”](https://rustsim.org/blog/2020/03/23/simd-aosoa-in-nalgebra). [alga](https://github.com/rustsim/alga)abstract algebra crate is switched to passive maintenance mode.

### gfx-rs and wgpu news [#](https://gamedev.rs#gfx-rs-and-wgpu-news)

![Deeper game](../../assets/62b92ef3245281cf.png)

[deeper](https://github.com/arnfaldur/deeper)uses wgpu for rendering

[gfx-hal-0.5](https://github.com/gfx-rs/gfx/) was released!
Improvements done in March:

- Debug markers. Users are now able to debug-annotate parts of the rendered frame, so that inspecting it in a GPU debugger is more enjoyable.
- The generic range parameters are removed in favor of simple structs. This is a move towards simpler low-level API.
- Physical device features for NDC Y-flip and sampler mirror clamp are added.
- Physical device performance hints are introduced. The first hint is for “base vertex/instance” support.
`SmallVec`

is removed from the API, it’s reshaped to avoid any heap allocations. Previously, it had to touch the heap on multiple descriptor sets or command buffers.- DX12 got true support for read-only storage bindings. This is one of the opt-in derivations from Vulkan that allow to better map users logic to non-Vulkan backends, also used by WebGPU.
- Last but not the least, @zicklag
[has been fighting](https://github.com/gfx-rs/gfx/pull/3151)with the OpenGL backend to align its API with the rest of the crowd, armed with[surfman](https://github.com/pcwalton/surfman). The fight is reading conclusion, and we are crossing fingers to add OpenGL support to`wgpu-rs`

as it lands.

[wgpu](https://github.com/gfx-rs/wgpu) and
[wgpu-rs](https://github.com/gfx-rs/wgpu-rs) changes in March:

- @grovesNL reached an epic milestone in the Web target
by showing the
[first triangle](https://github.com/gfx-rs/wgpu-rs/pull/193#issuecomment-599156540). Users will soon be able to seamlessly target the web with their existing`wgpu-rs`

applications. 🚀 `wgpu-types`

crate is created to share types between the Web target and the native one.- @lachlansneff improved the
*async*story quite a bit, we also converted more methods to be asynchronous. - Debug labels support.
- Id management story for browsers with a GPU process has been completely redesigned and now working well.
- All the objects are properly destroyed and GPU tracked if needed.
- Ability to provide a
`Surface`

so that the selected adapter can present to it. - New “mailbox” present mode.

Satellite projects:

[naga](https://github.com/gfx-rs/naga)- the new in-house shader translator has reached the milestone of successfully loading a WGSL[boids example](https://github.com/gfx-rs/naga/blob/thda1f6a4/test-data/boids.wgsl)and generating a valid Metal source for it. 🎉[metal-rs](https://github.com/gfx-rs/metal-rs)has got a lot of contribution by @adamnemecek. Indirect command encoding is particularly exciting![gfx-extras](../../assets/33982c22fd1da098.img)is a new library that is forked from rendy-memory/descriptor.[gfx-ocean](https://github.com/gfx-rs/gfx-ocean)was moved to gfx-rs organization and updated to gfx-hal-0.5.[gfx-portability](https://github.com/gfx-rs/portability)was also updated.

![miniquad android](../../assets/e925492ded6d2456.gif)


[miniquad](https://github.com/not-fl3/miniquad) by [@fedor_games](https://twitter.com/fedor_games) is a safe cross-platform rendering library
focused on portability and low-end platforms support.
Some of this month’s updates:

- example project by @PonasKovas,
illustrating android and web platform-dependent configuration:
[mandelbrot](https://github.com/PonasKovas/miniquad-mandelbrot). - first prototype for embedded debug frame introspection:
[introspection](https://twitter.com/fedor_games/status/1241616794114232321).

![Daily Sketch 0114 by Mactuitui](../../assets/05bb7dbee1d3b6a7.png)

[Nannou](https://nannou.cc) is a creative coding framework that aims to make it easy
for artists to express themselves with simple, fast, reliable code.

This month [Nannou v0.13 was released](https://nannou.cc/posts/nannou_v0.13).
Some of the updates:

- Migration to wgpu-rs.
- Nicer native macOS experience.
- Capturing Frames & Textures.

Also check out lots of cool sketches from the community:
[#nannou](https://twitter.com/search?q=%23nannou&src=typed_query) tag on Twitter.

![Oculus Quest](../../assets/964f6934d29fd6bf.jpg)


The [second part](https://krupitskas.github.io/posts/quest-dev-part-2/) of Nikita Krupitskas’
[blog series](https://krupitskas.github.io/posts/quest-dev-part-1/) on developing a game engine for the Oculus Quest
has been posted.

This part of the series describes how a simple Rust project can be built for Android - useful even if you’re not targeting the Oculus hardware!

![const-tweaker UI](../../assets/8ac5d96222553a8a.gif)


Thomas Versteeg has released a new crate called `const-tweaker`

, which provides
a web UI that can be used to tweak `const`

variables in a running application.
This can be used as a simpler alternative to embedded scripting languages or
hot-reloading in your games.

*Discussions: /r/rust*

a1phyr has created a crate called `assets_manager`

, which provides a convenient way
to load and cache external resources. It abstracts over the filesystem logic, and
provides a variety of built-in loaders for common Serde formats (e.g. TOML, JSON).
Hot-reloading support is also planned in the future.

*Discussions: /r/rust*

[netstack](https://crates.io/crates/netstack/0.3.0) is a batteries included networking crate for games. Requiring an
exchange of a secret and connection tokens. At the moment, UDP transport,
connection management, packet signaling, and packet acknowledgement are
features already implemented. Examples for getting started are provided
on the [crates.io page](https://gamedev.rs/news/008/netstack).

Version 0.3.0 adds basic monitoring functionality
along with traits `ClientMonitor`

and `ServerMonitor`

.
A work-in-progress prometheus exporter has also been added in this version.

Issues and contributions can be made to [Netstack’s github repository](https://gamedev.rs/news/008/netstack-github).
Work in progress documentation is available on [Netstack’s docs.rs](https://gamedev.rs/news/008/netstack-docs).

![Lighting example](../../assets/0bc7deb62038f85c.png)


[three-d](https://github.com/asny/three-d) is a renderer which targets both desktop (OpenGL) and web
(WebAssembly + WebGL2) which makes it possible to develop a 3D application on
desktop and easily deploy it on web.

This month [three-d v0.1](https://crates.io/crates/three-d) was released.
Main features:

- Thin and low-level graphics abstraction layer which maps one-to-one with the OpenGL/WebGL2 graphics APIs.
- Medium-level modular abstractions of common graphics concepts.
- Deferred renderer with high-level components.
- Default windows for easy setup.

![Spider example](../../assets/609523cadf0492b9.jpeg)


It is possible to build your own rendering features from low- or medium-level
components and combine with other high-level features, so you can already now
make some cool stuff. See for example these [examples](https://asny.github.io/three-d/).

### This Month in Mun [#](https://gamedev.rs#this-month-in-mun)

[Mun](https://mun-lang.org) is a scripting language for gamedev focused on quick iteration times
that is written in Rust.

The Mun Team [announced](https://mun-lang.org/blog/2020/03/10/this-month-february) that they have obtained a $15k grant
as part of the [MOSS Mission Partners](https://www.mozilla.org/en-US/moss/mission-partners) track, to further develop hot
reloadable data structures.

Their [March updates](https://mun-lang.org/blog/2020/04/02/this-month-march) include:

- marshalling of value structs;
- extern functions;
- garbage collector (defaults to mark&sweep);
- performance benchmarks;
- bugfixes and improved test coverage.

This month Oxygengine creator [published plans](https://www.reddit.com/r/rust_gamedev/comments/fe57s0/oxygengine_development_progress_tracker/) for the future
of the engine, where he explains the long term goal of the project that explains
why Oxygen is definitely not a toy or a hobby project and how that will shape
its feature towards being a toolset for the professionals. Project progress
tracker [can be found here](https://github.com/PsichiX/Oxygengine/projects/1).

Also, [@PsichiX](https://github.com/PsichiX) has started to work on the modular game editor
(extendable with user-made plugins) called **Ignite**, that will ease creating
games with the engine.

You can look at [the first editor module](https://twitter.com/PsichiX/status/1243380190752813064) - Asset
Browser:

![Oxygengine Asset Browser](../../assets/36040f45b60cd232.gif)


-
- Better panic messages on
`stable`

Rust. - Support for setting log levels from configuration.
- Text field rendering corrections.
- Target multiple overlapping UI entities with events.

- Better panic messages on
-
is the underlying ECS that powers Amethyst but there’s an`specs`

[ongoing prospect](https://github.com/amethyst/rfcs/issues/22)of moving to.`legion`

[@csherratt](https://github.com/csherratt)wrote an[excellent post](https://csherratt.github.io/blog/posts/specs-and-legion/)comparing both libraries. Also an[in-depth discussion](https://community.amethyst.rs/t/archetypal-vs-grouped-ecs-architectures-my-take/1344)about archetypal and grouped ECS design took place on the forum.![specs vs amethyst layout](../../assets/ef29d545c6738f87.png)

-
[Atelier](https://github.com/amethyst/atelier-assets)is an asset management and processing framework for games. Coupled with,`legion`

[@aclysma](https://github.com/aclysma)and[@kabergstrom](https://github.com/kabergstrom)built an[editor prototype](https://github.com/aclysma/atelier-legion-demo)demonstrating the following capabilities:- Prefab loading, saving, and hot-reloading
- Entity creation / deletion
- Component addition / removal
- Undo and Redo


Check out the [demo video](https://youtube.com/watch?v=9Vwi29RuQBE) and
[forum discussion](https://community.amethyst.rs/t/atelier-legion-integration-demo/1352).

-
There is an

[ongoing effort to bring WASM support to Amethyst](https://community.amethyst.rs/t/wasm-effort/1336). Check out the[contribution guide](https://github.com/amethyst/amethyst/tree/wasm/docs/CONTRIBUTING_WASM.md)and[project board](https://github.com/amethyst/amethyst/projects/20)for current status. -
[@ToferC](https://github.com/ToferC)reviewed their experience using Amethyst to build a space combat game,[Paladin](https://github.com/ToferC/paladin). Check out the[review on youtube](https://youtube.com/watch?v=avW2Nr6ak-o).

`ash`

is lightweight wrapper around Vulkan.

The latest version comes with support for Vulkan 1.2 and following extensions:

- VK_KHR_timeline_semaphore
- VK_KHR_ray_tracing
- VK_KHR_external_memory_fd

[Rectangle Pack](https://github.com/chinedufn/rectangle-pack) v0.1.5 [#](https://gamedev.rs#rectangle-pack-v0-1-5)

`Rectangle Pack`

is a Rust crate focused on rectangle packing: Laying out any smaller
number of rectangles inside any number of larger rectangles. The developer’s use
for the library is in packing textures from texture atlases on the GPU, although
the library does not have any concept of texture, and can be used in any
context where rectangle packing may be needed.

Version 0.1.5 adds implementation for error handling for RectanglePackError.

A getting started guide is available on the [project’s homepage](https://github.com/chinedufn/rectangle-pack).
Full documentation is available at the [rectangle-pack docs.rs section](https://crates.io/crates/rectangle-pack/0.1.5).

## Popular Workgroup Issues in GitHub [#](https://gamedev.rs#popular-workgroup-issues-in-github)

## Meeting Minutes [#](https://gamedev.rs#meeting-minutes)

[See all meeting issues](https://github.com/rust-gamedev/wg/issues?q=label%3Ameeting) including full text notes
or [join the next meeting](https://github.com/rust-gamedev/wg#join-the-fun).

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs));[winit’s “Good first issue” and “help wanted” issues](https://github.com/rust-windowing/winit/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+label%3A%22status%3A+help+wanted%22+label%3A%22Good+first+issue%22);[gfx-rs’s “contributor-friendly” issues](https://github.com/gfx-rs/gfx/issues?q=is%3Aissue+is%3Aopen+label%3Acontributor-friendly);[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22);[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22);[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A);[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner);[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22);[A/B Street’s “good first issue” issues](https://github.com/dabreegster/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22);[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue);- @kvark: Anybody wants to work on the
[GLSL front-end](https://github.com/gfx-rs/naga/issues/23)in Naga? One day, we’ll be able to finally replace glsl-to-spirv, which is used by a lot of graphics applications and is prone to issues.

## Bonus [#](https://gamedev.rs#bonus)

Just an interesting Rust gamedev link from the past. :)

![Robo Instructus logo](../../assets/23a8fc9778f566d3.jpeg)


On 2019.07.16 a puzzle game [“Robo Instructus”](https://www.roboinstruct.us) by [Alex Butler](https://twitter.com/bigabgames)
was released after two years of development:
[Steam](https://store.steampowered.com/app/1032170/Robo_Instructus)/[itch.io](https://bigabgames.itch.io/robo-instructus) (demo is available).

Salvage Engineer, you have a new assignment on a distant world…

Robo Instructus is a puzzle game in which players manoeuvre a robot by issuing instructions via a simple programming language. As players progress through the game they unlock new functions to overcome new puzzles, each of which can be solved in multiple ways. The more you master the robot, the more elegant and powerful your solutions will be.

Take the role of a Salvage Engineer sent across space. Use wits and tenacity to uncover the secrets of this isolated, frozen world.


Check out the [release trailer](https://youtube.com/watch?v=sIjaIxPp2_w).

The game is written using gfx-rs (pre-ll), winit, and opengl.
You can read more about its development in the [ awesome devlog](https://blog.roboinstruct.us)
that has lots of cool posts like

[“Robo Instructus: Behind The Scenes”](https://blog.roboinstruct.us/2019/06/26/behind-the-scenes.html).

*Discussions:
/r/rust*

That’s all news for today, thanks for reading!

Subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!