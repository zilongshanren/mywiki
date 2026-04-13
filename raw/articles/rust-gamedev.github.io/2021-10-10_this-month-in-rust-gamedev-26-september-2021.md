---
title: 'This Month in Rust GameDev #26 - September 2021'
url: https://gamedev.rs/news/026/
author: Rust GameDev WG
published: '2021-10-10'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 26th issue of the Rust GameDev Workgroup’s
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

[Rust GameDev Meetup](https://gamedev.rs/news/026/#rust-gamedev-meetup)[Rust Graphics Meetup #1](https://gamedev.rs/news/026/#rust-graphics-meetup-1)[Rust GameDev Podcast #6](https://gamedev.rs/news/026/#rust-gamedev-podcast-6)[Game Updates](https://gamedev.rs/news/026/#game-updates)[Learning Material Updates](https://gamedev.rs/news/026/#learning-material-updates)[Engine Updates](https://gamedev.rs/news/026/#engine-updates)[Tooling Updates](https://gamedev.rs/news/026/#tooling-updates)[Library Updates](https://gamedev.rs/news/026/#library-updates)[Popular Workgroup Issues in GitHub](https://gamedev.rs/news/026/#popular-workgroup-issues-in-github)[Requests for Contribution](https://gamedev.rs/news/026/#requests-for-contribution)[Discussions](https://gamedev.rs/news/026/#discussions)

## Rust GameDev Meetup [#](https://gamedev.rs#rust-gamedev-meetup)

![Gamedev meetup poster](../../assets/d50b3d4ba81ec6a4.png)


The ninth Rust Gamedev Meetup happened in September. You can watch the recording
of the meetup [here on Youtube](https://youtu.be/TH3AErcNcTY). The meetups take place on
the second Saturday every month via the [Rust Gamedev Discord
server](https://discord.gg/yNtPTb2) and are also [streamed on
Twitch](https://twitch.tv/rustgamedev).

## Rust Graphics Meetup #1 [#](https://gamedev.rs#rust-graphics-meetup-1)

![logo](../../assets/61b6c08ca51214f3.png)


The Rust Graphics Meetup is an online gathering where rustaceans share technical details of their work related to graphics and compute, not affiliated to any particular stack. The pilot edition has happened on Oct 2nd! Check out the talks:

[gfx-rs Lessons Learned](https://youtube.com/watch?v=m0JgF5Wb-dA)-[@kvark](https://github.com/kvark),[slides](https://github.com/gfx-rs/meetup/blob/main/Meeting01/GfxLessonsLearned.pdf).[rend3 Architecture: Efficient, Customizable Rendering](https://youtube.com/watch?v=F0wGz5UJTrY)-[@cwfitzgerald](https://github.com/cwfitzgerald),[slides](https://github.com/gfx-rs/meetup/blob/main/Meeting01/rend3s_Architecture_-_Efficient_Customizable_Rendering.pdf).[Blub - Interactive GPU Fluid Solver](https://youtube.com/watch?v=Yzr9va5UtiE)-[@wumpf](https://github.com/wumpf),[slides](https://github.com/gfx-rs/meetup/blob/main/Meeting01/Blub_-_Quick_tour_through_a_GPU_fluid_solver.pdf).

Learn more at the [gfx meetup repo](https://github.com/gfx-rs/meetup).
Thanks everyone for tuning in and helping to make this happen!

![text logo](../../assets/26cd67dde7b506ca.jpeg)


[The sixth episode](https://rustgamedev.com/episodes/interview-with-remco-and-basz) is an interview with Remco and Basz, creators of
[Mun](https://mun-lang.org/). Programming language creation is discussed, along with challenges
and what future developments are incoming from the [Mun project](https://mun-lang.org/).

Listen and Subscribe from the following platforms:
[Rust GameDev Podcast (simplecast)](https://rustgamedev.com/),
[Apple Podcasts](https://podcasts.apple.com/gb/podcast/rust-game-dev/id1526304768),
[Spotify](https://open.spotify.com/show/7HRfGnTcXkLkQd9fxJbDGj),
[RSS Feed](https://feeds.simplecast.com/C6NQglnL),
[Google Podcasts](https://podcasts.google.com/feed/aHR0cHM6Ly9mZWVkcy5zaW1wbGVjYXN0LmNvbS9DNk5RZ2xuTA).

## Game Updates [#](https://gamedev.rs#game-updates)

BITGUN ([Steam](https://store.steampowered.com/app/1673940/BITGUN/), [Twitter](https://twitter.com/logloggames),
[Discord](https://discord.gg/XrGZQkq)) by [@LogLogGames](https://twitter.com/logloggames) is an action
roguelike zombie shooter with lots of blood and guns, similar to games like
Hotline Miami, Nuclear Throne, and Heat Signature. The game is built using Godot
and Rust (via [godot-rust](https://godot-rust.github.io/)).

They recently re-worked the in-game UI using [egui](https://github.com/emilk/egui) with
[godot-egui](https://github.com/setzer22/godot-egui), allowing much easier custom widgets such as
[drag & drop on items between inventory slots](https://twitter.com/LogLogGames/status/1444072221681635333).

*Discussions: Twitter*

![Handful of minigames including hedgehogs and raspberries](../../assets/97bb5345fe5a70d6.jpg)


[Weegames](https://yeahross.itch.io/weegames) is a fast-paced minigame collection.
The Windows version of the game has been rewritten to use Macroquad,
so now the web and downloadable versions of the game share the same codebase.
Development for the web version has moved to the
[Weegames GitHub](https://github.com/yeahross0/weegames) repository.

![An odd structure in the woods](../../assets/d749d884c0da70b4.jpg)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In September, Veloren hosted its largest release party ever! At peak, 181 players
were playing on the server together. You can read about all the changes to 0.11
in [the release blog](https://veloren.net/release-0-11/), and be sure to watch the
[release trailer](https://www.youtube.com/watch?v=l1oOjvaWJlw)! During the release party, several devs
spoke about the changes, which you can watch [here](https://www.youtube.com/watch?v=J5Xz-vbE27Q). This
release party was the first one to handle the high player load with no issues,
and give hope for much larger servers in the future.

Shaderc was replaced with Naga early on in the month. This was the result of over a year of work. Hitboxes are in the process of being overhauled to handle non-cylindrical targets better. Improvements were made to how the cursor selects objects in game. As always, lots of experimental work is being done to the economic system. Cultist raiders were added, which means that raiding parties will now attack nearby settlements. This is a great example of how the realtime simulation is starting to become more visible to players.

September’s full weekly devlogs: “This Week In Veloren…”:
[#136](https://veloren.net/devblog-136),
[#137](https://veloren.net/devblog-137),
[#138](https://veloren.net/devblog-138),
[#139](https://veloren.net/devblog-139).

[Harvest Hero Origins](https://store.steampowered.com/app/1651500/Harvest_Hero_Origins) @ PAX West 2021 [#](https://gamedev.rs#harvest-hero-origins-pax-west-2021)

![hho @ pax](../../assets/9a4e47df8aeab81a.jpg)

[Harvest Hero Origins](https://store.steampowered.com/app/1651500/Harvest_Hero_Origins)
([Discord](https://discord.gg/CJRbxQn3d9),
[Twitter](https://twitter.com/GemdropGames))
is an arcade wave defense game by [Gemdrop Games](https://twitter.com/GemdropGames),
built in Rust on top of [Emerald](https://github.com/Bombfuse/emerald).

Gemdrop Games recently took Harvest Hero Origins to [PAX West 2021](https://twitter.com/GemdropGames/status/1433819047481659394)
and had a very positive response from most of the players!
Being able to watch people play the game was extremely valuable,
the developers were able to see pain points in UI/UX design
and can now fix them without worry.
They were also able to see what players find fun about controlling each hero,
which helps with the next hero planning in the full release of the game.

Harvest Hero Origins is still planned to release by the end of 2021,
please wishlist it on [Steam](https://store.steampowered.com/app/1651500/Harvest_Hero_Origins)!

### Molecoole [#](https://gamedev.rs#molecoole)

![Connecting to different atoms](../../assets/2e50d4a14e310e83.gif)


Molecoole is a topdown action roguelite where you connect with different atoms
to create the strongest Molecoole to defeat the baddies! Molecoole was created
by two brothers: [Márton](https://twitter.com/kiss_mrton) and [Dániel](https://twitter.com/FrenetiqDan).

In Molecoole the strongest focus is about making different combos by connecting
atoms. The original version was made in Unity for a game jam, but they decided
to make an actual game out of it using the Bevy engine. It currently includes
their own implementation for 2D animation, collision detection, and particles.
In September, one of the main development areas was making the game nicer to
play, so they introduced the [ezing](https://github.com/michaelfairley/ezing) crate and also implemented slowing the
[game time](https://twitter.com/kiss_mrton/status/1434189320865341444). They are using the [LDtk](https://ldtk.io) editor to make the level sections for the
procedural generation.

![circle race](../../assets/c4fe5e31cd96d80a.jpg)


Circle Race was made by [@kuviman](https://github.com/kuviman) for [TriJam 135](https://itch.io/jam/trijam-135), where you needed to create
a game in three hours. The theme was “Circles”. You are a circle, connected with
two other “thruster” circles. You play inside a circle, consisting of “tire”
circles. Circle around it to find your best circle time!

Made using [@kuviman](https://github.com/kuviman)’s own engine [geng](https://github.com/kuviman/geng/).

*Discussions:
/r/rust_gamedev*

![monke pizza](../../assets/d0b48df10f78403c.jpg)


Game made by [@kuviman](https://github.com/kuviman) for [VimJam 2](https://itch.io/jam/vimjam2). The theme for this jam was “Boss” and
the limitation was “On The Edge”.

Monke Pizza is an online multiplayer monke pizza restaurant simulator. You are
always on the edge of being fired. That is *if* you work here. Otherwise, you are
on the edge of being hired. Because that is how BOSS is bossing.

Made using [@kuviman](https://github.com/kuviman)’s own engine [geng](https://github.com/kuviman/geng/).

### Idu [#](https://gamedev.rs#idu)

![idu’s titlescreen](../../assets/1242ca67652604a0.jpg)


Idu ([Discord](https://discord.gg/PR3GgYYkym)) by [@logicsoup](https://twitter.com/logicsoup) and [@epcc10](https://twitter.com/epcc10)
is an upcoming game centered around growing realistic plants.

In September, the project previously codenamed “garden” has been renamed to “idu”! In Idu, every plant is continuously formed by the simulation. There are unique responses from a plant’s surroundings and your care. Simulated leaves and shoots grow into plants with a mind of their own. Here is the changelog of Demo Version 4:

- Fixed freezing when help menu was displayed
- Added support for all older Ubuntu versions from 16.04
- Fixed crashing when roots extended over the world border
- Pressing ESC in menus acts as a back button
- Fixed the issue where pruning didn’t work on the first day after loading the game
- Fixed the game choosing integrated GPU even when a discrete one was available

A playable alpha demo has been released and is freely available
at [Idu’s Discord server’s #demo-download channel](https://discord.gg/PR3GgYYkym)!

![Some players fishing at the beach](../../assets/42afc427026b0a8f.jpg)

[Antorum Online](https://ratwizard.dev/dev-log/antorum) is a micro-multiplayer online role-playing game by [@dooskington](https://twitter.com/dooskington).
The game server is written in Rust, and the official client is being developed
in Unity.

A few new features and lots of fixes were released to players this month, including item enchantments and the mining skill! Crafting has been expanded as well, and there are a ton of new monsters to fight and gear pieces to create.

![agent stats and a fight with a spider in ~/dev/facundoolano](../../assets/f3d9c99eb5fc3e3e.png)


[rpg-cli](https://github.com/facundoolano/rpg-cli) by [@facundoolano](https://github.com/facundoolano) is a minimalist computer RPG written in Rust.
Its command-line interface can be used as a cd replacement
where you randomly encounter enemies as you change directories.

This month, the v1.0 version was released.
Some of the [updates](https://github.com/facundoolano/rpg-cli/releases):

- New magic rings.
- A bunch of new quests including ring-related ones.
- Stat increasing stones.
- Sorcerer enemy class.

## Engine Updates [#](https://gamedev.rs#engine-updates)

[good-web-game](https://github.com/ggez/good-web-game) has been released on crates.io, together with [ggez](https://github.com/ggez/ggez) 0.6.1!
ggez is a lightweight cross-platform game framework for making 2D games
with minimum friction, with an API inspired by Love2D. good-web-game is a
subset of ggez, which is based upon [miniquad](https://github.com/not-fl3/miniquad) and can therefore run natively
on the web, mobile and of course desktop as well.

good-web-game was originally created to run [Zemeroth](https://ozkriff.itch.io/zemeroth) on the web. However,
as Zemeroth switched from using ggez to [macroquad](https://github.com/not-fl3/macroquad/) the project was
discontinued, until recently. In search of [a new graphics backend for ggez](https://github.com/ggez/ggez/issues/962)
the ggez team now picked up development again and released a massive update,
updating good-web-game for compatability to ggez 0.6, expanding its
functionality.

With only [a single change in boilerplate code](https://github.com/PSteinhaus/PSteinhaus.github.io/blob/main/ggez/web-examples/README.md#ggez-animation-example) many ggez 0.6 games can now be
directly ported to good-web-game. Yet, it’s no drop in replacement for ggez
as [several key differences remain](https://github.com/ggez/good-web-game#differences).

![godot-rust logo](../../assets/2e79f7ea55a63a2b.png)


godot-rust ([GitHub](https://github.com/godot-rust/godot-rust), [Discord](https://discord.com/invite/FNudpBD), [Twitter](https://twitter.com/GodotRust))
is a Rust library that provides bindings for the Godot game engine.

In the last month, a lot of documentation has been added to the book. The new
entries in [FAQ](https://godot-rust.github.io/book/faq.html), [Recipes](https://godot-rust.github.io/book/recipes.html) and [Game Architecture](https://godot-rust.github.io/book/gdnative-overview/architecture.html)
don’t focus on specific APIs, but put them into a bigger context and highlight
typical challenges encountered in practice.

Besides smaller bugfixes, the library itself added support for `serde`

serialization of core types ([#743](https://github.com/godot-rust/godot-rust/pull/743), thanks to Waridley).

In terms of automation and tooling, September was a very productive month:

-
Translation of Godot’s documentation based on

`[bbcode]`

to RustDoc with intra-doc links, making Godot APIs much more readable and discoverable. -
Refactoring of GitHub Actions CI, allowing quick and precise feedback for contributors.

-
Automation of latest documentation, now hosted under

[godot-rust.github.io/docs](https://godot-rust.github.io/docs).

As the godot-rust community keeps growing, the project can now be found
[on Twitter](https://twitter.com/GodotRust) with the GodotRust handle.

![hotreload](../../assets/418a8254829f300c.gif)

`emd.loader().hotreload()`

[Emerald](https://github.com/Bombfuse/emerald) by [@bombfuse](https://twitter.com/bombfuse_dev)
is a 2D game engine focused on being super portable and easy-to-use.

Currently supported platforms are:
Windows, Linux (WIP gamepad support), macOS (WIP gamepad support),
Web, Android (WIP audio, gamepad Support),
[GameShell](http://imgur.com/a/8cWxOPs),
and even [WearOS](https://twitter.com/bombfuse_dev/status/1444100458260299778)!

Recently added features include:

- Texture hot reloading (sound hot reloading is coming soon!).
- Cross-platform file saving/loading. This is essential for games, basically allows the user to save their files to the platform specific save directory.

[Emerald](https://github.com/Bombfuse/emerald) has slowly been growing, both in contributor size and feature sets
recently. If any of this interests you and you’d like to contribute,
[feel free to grab a task](https://github.com/Bombfuse/emerald/issues),
fork and PR!

![physically-connected groups of primitives are framed with rectangles](../../assets/150a283ccac44428.jpeg)

[Starframe](https://github.com/m0lentum/starframe/) by [@molentum](https://twitter.com/molentum_) is a work-in-progress game engine for physics-y
sidescrolling 2D games.

This month, a lot of work was done on optimizing the physics engine.
Most importantly, [spatial partitioning was added](https://twitter.com/molentum_/status/1432441648890449920) to speed up
collision detection. Also notably, [a graph algorithm was
implemented](https://twitter.com/molentum_/status/1438877808412008450) to divide the world into disjoint islands,
enabling some parallelism and skipping of computations.

Starframe’s physics is now very close to game-ready, and it no longer makes sense to work on the engine without a concrete project to use it. Thus, work has begun on a platformer based around connecting things with ropes. More details to be shown soonish!

![two synchronized views on tanks players-controlled tanks shooting each other](../../assets/e3f59d46e50ff28a.gif)

[Arcana](https://github.com/zakarumych/arcana) is ECS based game engine focused on simplicity and performance.

It recently got huge progress towards multiplayer support.
Traditional client-server systems were added and used in the [“Tanks” example](https://github.com/zakarumych/arcana/tree/master/examples/tanks).

Clients send only command queue to the server and server sends game world updates to the clients. Engine supports multiple players per client. For example, players may be added for each active input device.

To allow wide variety of genres player is not attached to one specific entity and may control many. In RTS player may control all their units and will send commands for each one.

Gameplay system that consumes commands doesn’t even need to be aware of netcode. Either way, it just drains command queue of an entity and utilizes them. That system must not be run on clients at all.

[Arcana](https://github.com/zakarumych/arcana) is very early work-in-progress and may not always work
out-of-the-box atm, but stability improvements are expected next month.



![rg3d 0.23 feature highlights video](../../assets/b838ded6cdc62ca6.jpg)

[video](https://youtube.com/watch?v=3tOdwmRWLKw)

[rg3d](https://github.com/mrDIMAS/rg3d) ([Discord](https://discord.gg/xENF5Uh), [Twitter](https://twitter.com/DmitryNStepanov), [Patreon](https://www.patreon.com/mrdimas))
is a game engine that aims to be easy to use and provide a large
set of out-of-the-box features.
This month [v0.23 was released](https://rg3d.rs/general/2021/09/13/0.23-feature-highlights.html). Some of the updates:

- Physically based rendering (PBR) with metallic workflow.
- High dynamic range (HDR) rendering pipeline & textures.
- Custom shaders and materials.
- Emission maps - allows you to define glowing parts using emission map.
- Gamma correction, manual/auto exposure, and color grading.
- Lots of the editor’s improvements: material editor, unified material pipeline for terrains, improved inspector, etc.

Check out the [blog post](https://rg3d.rs/general/2021/09/13/0.23-feature-highlights.html) or
the [feature highlights video](https://youtube.com/watch?v=3tOdwmRWLKw) for more info.

*Discussions: /r/rust*

![A dialogue window](../../assets/a39e32ab46c3cf59.png)

[Capstone](https://www.reddit.com/r/rust_gamedev/comments/paz35s/capstone)- a WIP game that uses Rust RPG Toolkit

[Rust RPG Toolkit](https://github.com/olefasting/rust_rpg_toolkit) by [@olefasting](https://github.com/olefasting) is an engine for creating
highly customizable and user modable action 2D action RPG’s using Rust amd JSON.

The project started out as a part of the [Capstone](https://www.reddit.com/r/rust_gamedev/comments/paz35s/capstone) game but was separated
as it grew in scope.
It uses JSON files for most of its game data and resources specification
so that games can be created with very little interaction with the Rust code.
This has the benefit of making the end product very easy to modify,
both for non-developers involved in the development process, and by end users.
Modification can be done either by modifying a game’s data files directly,
or by creating user modules, which are supported out-of-the-box.

Note that this is in early and very heavy development: the API is subject to constant change, as it has newly transitioned from being a game project to a library.

*Discussions:
/r/rust_gamedev*

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

![Title card](../../assets/545f2e48529ea15c.jpg)


[Dan Olson](https://twitter.com/olson_dan/status/1438600242962698256) gave a talk at the Game Developers Conference in
July about using Rust for game tooling. The talk describes how Rust is being
integrated at Treyarch. Dan gives a “sales pitch” about several Rust benefits,
and goes over several case studies about where it is used. It makes appearances
in the Treyarch image packer, and is used in 3 major tools, and around 20
smaller one-off tools. Around 120k lines of Rust code have been written for the
projects.

If you have a GDC Vault account, you can watch [the video](https://gdcvault.com/play/1027315).
If you don’t, you can still read [the slides](https://research.activision.com/publications/2021/09/the-rust-programming-language-for-game-tooling).

[Learn Wgpu](https://sotrh.github.io/learn-wgpu) Updated: No More Swap Chains! [#](https://gamedev.rs#learn-wgpu-updated-no-more-swap-chains)

As part of the update to 0.10, the wgpu team removed the `SwapChain`

from the
API. The `Surface`

will now be used to retrieve textures to render to wrapped
in `SurfaceTexture`

s. You configure the `Surface`

in a similar way to how you
would configure the `SwapChain`

, except the struct is now called
`SurfaceConfiguration`

instead of `SwapChainDescriptor`

.

If you want to know more, you can check [the tutorial’s news page](https://sotrh.github.io/learn-wgpu/news).

## Tooling Updates [#](https://gamedev.rs#tooling-updates)

![borderlands save editor](../../assets/3b190eb5c72a2fab.png)


The [Borderlands 3 Save Editor](https://github.com/ZakisM/bl3_save_edit) by [ZakisM](https://github.com/ZakisM)
is a tool to help you modify your Borderlands 3 Saves and Profiles
written using [Iced](https://github.com/iced-rs/iced). Currently, it runs on Windows, Mac OS and Linux.
It supports modifying PC saves as well as decrypted PS4 saves
(and converting between them).

## Library Updates [#](https://gamedev.rs#library-updates)

![Deno with wgpu crown](../../assets/92f07bfcd9be4447.png)

[wgpu](https://github.com/gfx-rs/wgpu) is a cross-platform, safe, pure-rust graphics API that runs natively
on Vulkan, Metal, D3D12, D3D11, and OpenGLES; and on top of WebGPU on wasm.

wgpu has set up the infrastructure to run WebGPU proper tests on its CI,
via [Deno](https://github.com/denoland/deno). This will ensure correctness down the road when we reach a
decent level of coverage. Read more on [gfx-rs blog](https://gfx-rs.github.io/2021/09/16/deno-webgpu.html).

Aside from that, wgpu team has been pumping out patches. In fact, wgpu-0.10 is easily the most patched release of all!

![matchbox demo screenshot: Waiting for 3 more players](../../assets/d0c161ab416a3134.png)


Matchbox by [@jkhelsing](https://twitter.com/jkhelsing) is a new peer-to-peer networking project for
establishing unreliable, unordered connections between peers on the internet.
The goal is to enable low-latency multiplayer games written in Rust WASM.

Matchbox consists of:

- A tiny signaling server,
, which acts as a rendezvous point. It helps peers discover each other and deal with NAT traversal in order to establish more direct ways of communication.`matchbox_server`

- A crate,
, which handles connecting to a signalling server and establishing a WebRTC data channel between each connected peer.`matchbox_socket`

- A
[demo/template project](https://github.com/johanhelsing/matchbox/tree/main/matchbox_demo)using[Bevy](https://bevyengine.org)and[GGRS](https://gschup.github.io/ggrs)to implement a web game with peer-to-peer rollback netcode. A live version is hosted[here](https://helsing.studio/box_game).

More info is available in the [repository](https://github.com/johanhelsing/matchbox) and
[introductory blog post](https://johanhelsing.studio/posts/introducing-matchbox).

[Sparsey](https://github.com/LechintanTudor/sparsey) by [@LechintanTudor](https://github.com/LechintanTudor) is a new sparse set-based Entity Component System
(ECS) with component storage grouping, granular component change detection,
fallible systems and beautiful syntax.

The goal of [Sparsey](https://github.com/LechintanTudor/sparsey) is to provide a sparse set-based ECS which fully takes
advantage of its core data structure. An example of this is component storage
grouping, a feature which allows getting the best performance possible when
iterating over queries that match certain patterns described by the user, at
the cost of a performance penalty when inserting or removing components from
these storages.

To get started with [Sparsey](https://github.com/LechintanTudor/sparsey), check out the [Sparsey Cheat Sheet](https://github.com/LechintanTudor/sparsey/blob/master/guides/cheat_sheet.md) and the
[examples on GitHub](https://github.com/LechintanTudor/sparsey/tree/master/examples)!

![bevy_verlet](../../assets/780c1b2f6e4e1087.gif)


[bevy_verlet](https://github.com/ManevilleF/bevy_verlet) is a lib for projects using [Bevy Engine](https://bevyengine.org/)
providing a plugin to use [verlet Integration](https://en.wikipedia.org/wiki/Verlet_integration)
physics. Very useful for Cloth simulation and joints, and less expensive than
complex physics engine, it is a nice addition to 2D or 3D projects. Making good
use of the Entity-Component-System architecture of the bevy engine, any entity
can become a `VerletPoint`

and have physics applied to it.

The crate also provides *sticks* which constrains the points in order to create
strings or cloth. With its modularity, you may customize the physics precision
(iterations), the gravity, and the physics time step to use.

Not yet available on crates.io, the lib will be released after a few missing features are provided:

- Primitive collision
- Object batching (optimization)
- Global documentation

You may contact the author on Twitter [@ManevilleF](https://twitter.com/ManevilleF) or join the
[discussion](https://twitter.com/ManevilleF/status/1437350669858611202?s=20).

[hecs](https://github.com/Ralith/hecs) is a fast, lightweight, and unopinionated archetypal ECS library.

Version 0.6 introduces `PreparedQuery`

, allowing query set-up cost to be
amortized across multiple invocations. `EntityRef`

’s API was expanded to include
a single-entity `query`

method, and now exposes the referenced entity’s
handle. Finally, `World::spawn_batch`

and `reserve`

were optimized for better
performance when called repeatedly.

A revamped and refactored version of @F3kilo’s ktx2-reader,
this serves as a parsing library for the texture container format
of ktx2. This format allows you to store textures in formats that
GPU apis directly accept, without decoding costs. For more information,
[read the docs](https://docs.rs/ktx2).

ktx2 writing support will come a future release.

![rend3 sci-fi base scene](../../assets/bcee51e5fc0b9a9a.jpg)

rend3 is a new 3D rendering library that focuses on having an easy to user interface without sacrificing performance or customizability. It comes with PBR materials and render routine out of the box and utilizes GPU culling to enable incredible performance with such a simple API.

There’re many fun things in the pipeline including a full custom shader system, both cpu and gpu side optimization, and more rendering features.

The [v0.1 version](https://crates.io/crates/rend3) was published on crates.io
([docs](https://docs.rs/rend3) and [examples](https://github.com/BVE-Reborn/rend3/tree/v0.1.2/examples)) and v0.2 is going
to be coming out very soon.

[imgui-rs](https://github.com/imgui-rs/imgui-rs) is the Rust bindings for the Dear ImGui framework,
allowing users to easily build up complex debug widgets and tools.

In [v0.8.0](https://github.com/imgui-rs/imgui-rs/releases/tag/v0.8.0), the library’s API continued its overhaul to both be more
similar to the C++ API while feeling like native Rust. Specifically,
the odious `im_str!`

macro was deprecated – using inline strings directly
(and anything `AsRef<str>`

) simply works. Most functions also make extensive
use of RAII-style drop tokens to track `begin`

/`end`

calls.
Lastly, it was updated to use current Dear ImGui v1.84, and bound to
the new APIs, including the new Tables API.

![Utility AI](../../assets/2646d79026675ea5.gif)

[Emergent AI](https://github.com/PsichiX/emergent/) by [@PsichiX](https://twitter.com/psichix) is a new crate designed
to provide modern AI solutions for games written in Rust. Its highly modularized
and hierarchical architecture allows users to express a wide range of AI behaviors
complexity, from small scale, to big scale, allowing user to pick proper solution
to each AI problem using smaller building blocks.

Along with the library, there is an
[“Emergent AI - Smart agents and events for games”](https://psichix.github.io/emergent/) book being
written with goal to explain in-depth to readers how modern AI systems works and
showing step by step process of how one could build them on their own.

```
_______
/ E \
_______/ (4,3) \
/ \ W:3 /
_______/ (3,2) \_______/
/ \ W:1 /
/ (2,2) \_______/
\ W:3 /
\_______/
/ \
_______/ (2,1) \
/ \ W:3 /
_______/ (1,0) \_______/
/ S \ W:4 /
/ (0,0) \_______/
\ W:6 /
\_______/
```


[hexagonal_pathfinding_astar](https://github.com/BlondeBurrito/hexagonal_pathfinding_astar) is an implementation of the A-Star pathfinding algorithm
tailored for traversing a bespoke collection of weighted hexagons.
It’s intended to calculate the most optimal path to a target hexagon where you’re
traversing from the centre of one hexagon to the next along a line orthogonal
to a hexagon edge.
Check out the project’s [README](https://github.com/BlondeBurrito/hexagonal_pathfinding_astar) for more info.

![Pixels logo](../../assets/f2b90ee91357e27b.png)


[pixels](https://github.com/parasyte/pixels) by [@parasyte](https://github.com/parasyte) is a tiny hardware-accelerated pixel frame buffer
based on wgpu. It gives you a pixel buffer and you can poke colors into it
(on the CPU side). The buffer is uploaded to the GPU as a texture,
and all scaling and clipping is handled by a default shader.
For additional control, you can add your own custom shaders for pre- and post-processing.

The v0.6 release adds support for wgpu 0.10 which is a huge improvement. The only breaking changes are reexports and an error variant name change. In most cases, this upgrade is a drop-in replacement.

*Discussions:
/r/rust*

![a window with many widgets and tabs](../../assets/87cba9898bcd8108.gif)

[KAS](https://github.com/kas-gui/kas) by [@dhardy](https://github.com/dhardy) is a general-purpose retained UI toolkit.
This month v0.10 was released:

- KAS now supports dynamic linking, allowing faster builds. Additionally using a faster linker (lld or mold) allows 6x improvement on re-build speed for the Gallery example.
- Keyboard navigation has been revised to match standard desktop GUIs.
- Themes have been improved, with (better) shadows under pop-up menus and (on one theme) under buttons.
- Crates have been reshuffled so that now (most) users only depend on kas.
- OpenGL on Linux is supported (mostly thanks to WGPU improvements).
- KAS-text now exposes its
`fontdb::Database`

, allowing text in SVGs.

Also, the author notes that this may be the last release of [KAS](https://github.com/kas-gui/kas)
because of the lack of interest to the project.

*Discussions: /r/rust*

## Popular Workgroup Issues in GitHub [#](https://gamedev.rs#popular-workgroup-issues-in-github)

## Discussions [#](https://gamedev.rs#discussions)

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[Graphite is looking for contributors](https://github.com/GraphiteEditor/Graphite/issues/202)to help reach the 0.1 Alpha release and are participating as a[Hacktoberfest](https://hacktoberfest.digitalocean.com/)project.[winit’s “difficulty: easy” issues](https://github.com/rust-windowing/winit/issues?q=is%3Aopen+is%3Aissue+label%3A%22difficulty%3A+easy%22).[Backroll-rs, a new networking library](https://github.com/HouraiTeahouse/backroll-rs/issues).[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[A/B Street’s “good first issue” issues](https://github.com/a-b-street/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/D-Good-First-Issue).

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!

**Discuss this post on**:
[/r/rust_gamedev](https://reddit.com/r/rust_gamedev/comments/q5fjyk/this_month_in_rust_gamedev_26),
[Twitter](https://twitter.com/rust_gamedev/status/1447294414607556613),
[Discord](https://discord.gg/yNtPTb2).