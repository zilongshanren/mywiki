---
title: 'This Month in Rust GameDev #36 - July 2022'
url: https://gamedev.rs/news/036/
author: Rust GameDev WG
published: '2022-08-11'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 36th issue of the Rust GameDev Workgroup’s
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

[Announcements](https://gamedev.rs/news/036/#announcements)[Game Updates](https://gamedev.rs/news/036/#game-updates)[Engine Updates](https://gamedev.rs/news/036/#engine-updates)[Learning Material Updates](https://gamedev.rs/news/036/#learning-material-updates)[Tooling Updates](https://gamedev.rs/news/036/#tooling-updates)[Library Updates](https://gamedev.rs/news/036/#library-updates)[Other News](https://gamedev.rs/news/036/#other-news)[Discussions](https://gamedev.rs/news/036/#discussions)[Requests for Contribution](https://gamedev.rs/news/036/#requests-for-contribution)

## Announcements [#](https://gamedev.rs#announcements)

### Rust GameDev Meetup [#](https://gamedev.rs#rust-gamedev-meetup)

![Gamedev meetup poster](../../assets/4c75589cbd7f54de.png)


The 18th Rust Gamedev Meetup took place in July. You can watch the recording of
the meetup [here on Youtube](https://youtu.be/mnuchYuR_ck). Here was the schedule from
the meetup:

- RustConf Arcade Cabinet -
[@carlosupina](https://twitter.com/carlosupina) - Blackjack -
[@setzer22](https://twitter.com/playtheprocess) - Dotrix -
[@lowenware](https://twitter.com/lowenware) - Graphite -
[@GraphiteEditor](https://twitter.com/graphiteeditor)

The meetups take place on the second Saturday every month via the [Rust Gamedev
Discord server](https://discord.gg/yNtPTb2) and are also [streamed on
Twitch](https://twitch.tv/rustgamedev). If you would like to show off what you’ve been
working on at the next meetup on [August 13th](https://everytimezone.com/s/17260ccd), fill out [this
form](https://forms.gle/BS1zCyZaiUFSUHxe6).

### Rust Game Ports Officialization [#](https://gamedev.rs#rust-game-ports-officialization)

![games collage](../../assets/a2d6e68c320706bb.jpg)


[64kramsystem](https://github.com/64kramsystem)’s Rust Game Ports [project](https://github.com/rust-gamedev/rust-game-ports) has
been officially adopted by the Rust game development working group.

The project is intended to be a reference for Rust game development, helping developers, especially newcomers, to understand how to use Rust game libraries, and design Rust games in general.

Devs are invited to explore and contribute! There are ports for all the levels and interests 😄

![colorful render of a 3d model of Ferris with additional wireframe view](../../assets/b6c1c0ef6cae3306.jpg)


[@RayMarch](https://twitter.com/Ray__March) created a 3d model of [Ferris the Rustacean](https://rustacean.net/)
for the Rust community!

The model is [now available for free here on github](https://github.com/RayMarch/ferris3d)!

It was released into the [public domain](https://creativecommons.org/publicdomain/zero/1.0/) so you can use it
however you like, even commercially!

*Discussions: Twitter*

[Tokyo Rust Game Hack Event](https://bombercrab-rust-game-hack.peatix.com/view): Aug 12th [#](https://gamedev.rs#tokyo-rust-game-hack-event-aug-12th)

![pixelart ferris and bombs](../../assets/ba7283c1b643b263.jpeg)


The team at [tonari.no](http://tonari.no) is back with the second edition
of the Tokyo Rust Game Hack event!

For this edition of the Game Hack event, we’re dragging you back through the mists of time, to the earlier days of arcade games. We’ve built a Bevy-powered, simple reimagining of classic Bomberman, with a modern twist. Players don’t participate by taking turns on an arcade stick. Instead, we will provide a crate that defines the character’s interaction with the world through a Player trait. By simply implementing that trait and compiling to a wasm target, you’ll be able to upload your character to the game, live. Adapt your strategy on the fly and bomb your way into the scoreboard!


[The player template repository](https://github.com/tonarino/bombercrab-player) is open sourced
ahead of time so you can get a nice headstart.

If you decide to come please sign up on [the event’s page](https://bombercrab-rust-game-hack.peatix.com/view).
You can participate physically or online, see the full announcement
for the details.

*Discussions:
/r/rust*

## Game Updates [#](https://gamedev.rs#game-updates)

[Way of Rhea](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n36) is a puzzle adventure with hard puzzles and forgiving
mechanics being produced by [@masonremaley](https://twitter.com/masonremaley) in a custom Rust
engine. You can support development by
[checking out the free demo and wishlisting on Steam](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n36)!

Way of Rhea was selected to be part of [PAX Rising online](https://store.steampowered.com/sale/PAXRisingOnline)! It
was also shown off in the June [Steam Game Festival](https://store.steampowered.com/sale/nextfest_june2022).
Other recent updates:

- Kotaku mentioned Way of Rhea in an article about
[fascinating upcoming indie games](https://kotaku.com/steam-indie-games-pc-wishlist-arctic-awakening-1849140770) [Lost In Cult](https://www.lostincult.co.uk/), a gaming journal, announced[preorders](https://www.lostincult.co.uk/?aff=18)for a new edition of Lock On containing a card game containing a card with a character from Way of Rhea featured- Mason posted a video interview covering
[why he became an indie dev](https://youtu.be/H0sIsrLWojs), among other things - Work has begun on puzzles for the final level of the game. This area combines the puzzle elements from all previous biomes for a final set of challenging puzzles.
- A weather system with
[rain](https://twitter.com/AnthropicSt/status/1546207348259266560)and[snow](https://twitter.com/AnthropicSt/status/1546320074923024384)was added to the game - More progress was made on the unreleased Linux platform layer
- More wildlife was added to the game
- Some logging and editor improvements were made

### Flesh [#](https://gamedev.rs#flesh)

![flesh preview](../../assets/3844d305652daf6f.gif)

[Flesh](https://store.steampowered.com/app/1660850/Flesh/) by [@im_oab](https://twitter.com/im_oab) is a 2D-horizontal shmup game with hand-drawn animation and
an organic/fleshy theme. It is implemented using [Tetra](https://github.com/17cupsofcoffee/tetra). This month’s updates
include:

- The game has BGM.
- Support global leaderboard.
- Integrate steam SDK using
[steamworks](https://crates.io/crates/steamworks)crate. - Add new enemy types for the 3rd area.
- Add squeezing effect when the enemy gets hit.

![hundreds of colliding colored balls in the air](../../assets/d9a1276dce318328.jpg)

CyberGate ([YouTube](https://youtube.com/channel/UClrsOso3Xk2vBWqcsHC3Z4Q), [Discord](https://discord.gg/R7DkHqw7zJ)) by CyberSoul
is a new multiplayer project that aims at procedurally generating distinct
universes and gameplay experiences. CyberGate is the name of the main world
where universes can be created and accessed by quantum portals.

Recent updates:

- Bandwidth became 16 times smaller by implementing entity prioritization + other techniques.
- Interpolation and Jitter prediction makes entities way smoother.
- Automatic and Reliable Spawn and Despawn of entities.
- Many other features and optimizations to do with rapier 3d physics, wgpu renderer, and quinn (quic) protocol.

[Join the Discord server](https://discord.gg/R7DkHqw7zJ) to participate in tests.

*Discussions: /r/rust_gamedev*

![A grid with dots and arrows](../../assets/62c4cb5e03b839dc.png)


[Botnet](https://github.com/JMS55/botnet) is an upcoming programming-based multiplayer game, where you write
scripts (compiled to WebAssembly) to control robots. Coordinate your network
of bots to gather resources, build new industry, and expand your control of
the server!

This month was primarily spent on BotnetReplayViewer - a visual program to watch matches and inspect entity data.

Additionally, the antenna structure was added. Building an antenna gives you control over the bay (room) it’s in, letting you build additional structures, and increasing the total number of bots you can control. Bots can also use antennas to store resources.

Interested in contributing? Head over to the
[GitHub discussion page](https://github.com/JMS55/botnet/discussions/categories/ideas) and suggest some ideas!

![Re-rolling gameplay](../../assets/d928e36c90d6c6ca.png)


[Re-Rolling!](https://mystal.itch.io/re-rolling) by [@mystalice](https://twitter.com/mystalice) is a top-down 2D
survival shooter where you fight off a horde of rats using weapons you randomly
rolled.

The game was created for [GMTK Jam 2022](https://itch.io/jam/gmtk-jam-2022) in 48 hours and was
heavily inspired by [20 Minutes Till Dawn](https://store.steampowered.com/app/1966900/20_Minutes_Till_Dawn/).

Re-Rolling! was made with Bevy using heron for physics, bevy_egui for in-game
UI, and a handful of other helpful crates and plugins. You can browse the source
on [GitHub](https://github.com/mystal/re-rolling).

![game logo + OS logos](../../assets/04ef16b64bdd7ec9.jpg)


In 2019 the programming puzzler [Robo Instructus](https://www.roboinstruct.us) was released
on [Steam](https://store.steampowered.com/app/1032170/Robo_Instructus) & [itch.io](https://bigabgames.itch.io/robo-instructus).

This month [Alex Butler](https://twitter.com/bigabgames) wrote [“Robo Instructus: 3 Years Old”](https://blog.roboinstruct.us/2022/07/16/3-years-old.html)
about how well the game did in the last year & to date: Sales by
platform/country/OS, player feedback, reviews & game updates.

![Simon arcade gameplay with arrows and buttons in different colors](../../assets/43d3b10b6c422ea1.gif)

Based on [Simon (Original)](https://en.wikipedia.org/wiki/Simon_(game)), made with [Bevy](https://bevyengine.org),
the goal of this game is to push buttons in the correct order,
in an ever-increasing sequence.

This game was made to fit with the [Rust Arcade Cabinet](https://github.com/rust-arcade/bevy-rust-arcade)
and was showcased at [RustConf Portland](https://rustconf.com) on August 5th 2022.

![Gliding above a forest](../../assets/0b02a40b54bdb9f1.jpg)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In July, Veloren released 0.13! You can [read the full blog post](https://veloren.net/release-0-13)
that includes a trailer for the release party, and information about the new
features in the release. This release party set a new record for most players on
the server at once, going from 195 to now 277! This version brings modular
weapons, real-time weather, cliff towns, cave biomes, level of detail trees, and
much more.

Other than the release party, July saw lots of work getting done. The translation system is undergoing an overhaul. Work is being done on the Scrolling Combat Text system, which gives some visual indicator to how much damage or healing you’re taking. Though is going into how to better handle server-side physics to reduce latency.

July’s full weekly devlogs: “This Week In Veloren…”:
[#179](https://veloren.net/devblog-179),
[#180](https://veloren.net/devblog-180),
[#181](https://veloren.net/devblog-181),
[#182](https://veloren.net/devblog-182).

![an animated black-colored character runs around and attacks anoter one](../../assets/76b08b4df445de9b.gif)

[Agma](https://github.com/TuckerBMorgan/Agma) by [@TuckerBMorgan](https://twitter.com/T_B_Morgan) is a 3D game built in the [Storm Engine](https://github.com/mooman219/Storm) that is based
on games like Lost Ark and Diablo. The author has been writing about their experience
with changing how they approach working on personal projects [here](https://medium.com/@tucker.bull.morgan/summoning-a-devil-544b130c8889).
It is built using a custom UDP-based networking stack, a custom ECS,
and a custom-skinned mesh renderer to maximize what the author could learn.

![zoomin gout from individual tiles to the whole space system](../../assets/163dcdfeb4ef869e.gif)

[Combine&Conquer](https://martinbucksoftware.itch.io) by [Martin Buck](https://github.com/I3ck) is a WIP strategy game
about automation similar to Satisfactory or Factorio.
This month’s updates include:

[Audio support, a new space view, colonization of planets, inventory overlay, and better notifications](https://buckmartin.de/combine-and-conquer/2022-07-06-v0.0.8.html).[New textures for structures, info box, updated overlays and modles](https://buckmartin.de/combine-and-conquer/2022-07-31-v0.0.9.html).

### Life Code [#](https://gamedev.rs#life-code)

[Bytellation shared the first video devlog](https://youtube.com/watch?v=a6ZnhXGp3JI) of a WIP ecosystem
coding game “Life Code”:

The game is intended to run in the browser and will be written in Rust which will be compiled to WASM. I’m using a very new and not yet matured game engine called Bevy. I will be creating the art and models in the game using Blender.

This will be a coding game which means players will have to use languages such as Python, Javascript, Rust, C++, and hopefully many more. It will be possible to play even if you don’t know how to code but the game will try to guide you to use real code instead of predefined behavior sets. Follow my journey where I try to create an impossible solo indie game with little to no game dev experience.


## Engine Updates [#](https://gamedev.rs#engine-updates)

![bevy terrain](../../assets/c4ce7399e4974116.jpg)

[Bevy](https://bevyengine.org) is a refreshingly simple data-driven game engine built in Rust. It
is [free and open source](https://github.com/bevyengine/bevy) forever!

Bevy 0.8 was a massive community effort. You can check out the [full release
blog post here](https://bevyengine.org/news/bevy-0-8), but here are some highlights:

[New Material System](https://bevyengine.org/news/bevy-0-8/#new-material-system)[Camera-driven Rendering](https://bevyengine.org/news/bevy-0-8/#camera-driven-rendering)[Built-in Shader Modularization](https://bevyengine.org/news/bevy-0-8/#built-in-shader-modularization)[Spot Lights](https://bevyengine.org/news/bevy-0-8/#spotlights)[Visibility Inheritance](https://bevyengine.org/news/bevy-0-8/#visibility-inheritance)[Upgraded to wgpu 0.13](https://bevyengine.org/news/bevy-0-8/#wgpu-0-13-new-wgsl-shader-syntax)[Automatic Mesh Tangent Generation](https://bevyengine.org/news/bevy-0-8/#automatic-mesh-tangent-generation)[Renderer Optimizations](https://bevyengine.org/news/bevy-0-8/#render-phase-sorting-optimization)[Scene Bundle](https://bevyengine.org/news/bevy-0-8/#scene-bundle)[Scripting / Modding Progress](https://bevyengine.org/news/bevy-0-8/#scripting-modding-progress-untyped-ecs-apis)[ECS Query Ergonomics and Usability](https://bevyengine.org/news/bevy-0-8/#query-intoiter)[ECS Internals Refactors](https://bevyengine.org/news/bevy-0-8/#ecs-lifetimed-pointers)[Reflection Improvements](https://bevyengine.org/news/bevy-0-8/#bevy-reflection-improvements)[Hierarchy Commands](https://bevyengine.org/news/bevy-0-8/#hierarchy-commands)[Bevy UI Now Uses Taffy](https://bevyengine.org/news/bevy-0-8/#taffy-migration-a-refreshed-ui-layout-library)

*Discussions:
/r/rust,
Hacker News,
Twitter*

![Concept art of a player creating a world in Dims](../../assets/9977455c239fa936.jpg)


[Dims](https://dims.co) ([Twitter](https://twitter.com/DimsWorlds), [Discord](https://discord.gg/Z5CAVmNE57),
[YouTube](https://youtube.com/channel/UCR5gOwS7uSl0a0dl7MLQoqg)) is a pre-alpha collaborative open-world
creation platform.
Users can hop in sessions and build a game together, allowing everyone
to bring out their inner game-maker.

In July, development continued to make great strides. Some of the highlights include:

- Continued work on the audio system, including in-game graphs of attenuation and other audio-related functions
- The introduction of an intent system that allows for user actions to be undone and replayed arbitrarily
- A complete UI facelift using Material UI icons and a new design language
- A new scripting system using WebAssembly + WASI and Rust as a guest language (look forward to an article on this soon!)
- The beginnings of a shared asset database that lets you and your team easily share assets amongst each other and with other projects
- Various infrastructural and rendering fixes, including more accurate PBR

Want to try Dims out for yourself? Come join the [Discord](https://discord.gg/Z5CAVmNE57) to be
notified of future public tests, see the latest features before everyone else,
and to talk to the devs personally.

![godot-rust logo](../../assets/c74558f831485698.png)


godot-rust ([GitHub](https://github.com/godot-rust/godot-rust), [Discord](https://discord.com/invite/FNudpBD), [Twitter](https://twitter.com/GodotRust))
is a Rust library that provides bindings for the Godot game engine.

The last few months have been a bit quieter around godot-rust. A lot of this
can be attributed to developers exploring the [GDExtension API](https://godotengine.org/article/introducing-gd-extensions), the
successor of GDNative for Godot 4. At this point, a lot of the foundation is
still being built, however, some more concrete plans are outlined in
[#824](https://github.com/godot-rust/godot-rust/issues/824). Further updates will be posted in that issue or on Twitter.

Nevertheless, several improvements have been integrated to godot-rust since
0.10, with [version 0.10.1 on the horizon](https://github.com/godot-rust/godot-rust/issues/907). Some notable examples:

- GDScript utility functions like lerp, ease or linear2db (
[#901](https://github.com/godot-rust/godot-rust/issues/901)) - Property support for standard collection types (
[#883](https://github.com/godot-rust/godot-rust/issues/883)) - Methods for Rect2 and Aabb (
[#867](https://github.com/godot-rust/godot-rust/issues/867))

![Gamercade preview](../../assets/adba0d528ba61769.gif)

[Gamercade](https://gamercade.io) ([Discord](https://discord.gg/Qafv2Fpt5j), [GitHub](https://github.com/gamercade-io))
by @RobDavenport is a WASM-powered fantasy console focused
on building multiplayer neo-retro games.

After over half a year in development, Gamercade and related tools are ready
for pre-alpha testing. This includes the [console](https://github.com/gamercade-io/gamercade_console) itself,
as well as the [editor](https://github.com/gamercade-io/gamercade_editor).

Gamercade’s killer feature is the ease of developing multiplayer games. The console is able to simplify networked game development process in the best way possible: build a local multiplayer game, and get full online play for free!

The WASM Api features powerful but simple built-in features like input, 2d graphics, random number generation, and more. Limitations do exist, but are flexible, such as resolutions up to 1920 x 1080, and a maximum of 256 color palettes with up to 64 colors each.

The community around the project is small, but is looking to expand.
Come on over to the [subreddit][Gamercade-Subreddit], or hang out and chat
on [Discord](https://discord.gg/Qafv2Fpt5j), where the developers interact with members
and post updates daily. The project is newly [open source](https://github.com/gamercade-io)
and looking for contributors, suggestions, as well as awesome game demos.

*Discussions:
/r/rust_gamedev,
/r/fantasyconsoles*

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

![sandfall_8k](../../assets/c8945392634fae67.gif)

[@hakolao](https://github.com/hakolao) published a [tutorial](https://okkohakola.com/posts/sandfall_tutorial) about creating
[cellular automata](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) sand fall simulations with compute shaders.

Typically, cellular automata sand fall is done with the CPU due to the two-way relationship between the cells on a grid. This article shows a way to tackle sand fall creation using compute shaders to achieve massive parallelism.

Additional to compute shaders, this tutorial is a great introduction to the
[Vulkano](https://github.com/vulkano-rs/vulkano) library. It also works as a
good base for learning how to create simple graphics pipelines. You will also
get to use Bevy and Egui.

*Discussions:
/r/rust_gamedev*

![Example of the results of doing an A* search from a start node to a goal node](../../assets/1dc53929913d2b12.png)


[Pathfinding in Rust: A tutorial with examples](https://blog.logrocket.com/pathfinding-rust-tutorial-examples)
is an article with examples of how to use the [pathfinding](https://crates.io/crates/pathfinding)
crate to do breadth-first, Dijkstra’s, and A* search. It links to the
[gregstoll/rust-pathfinding](https://github.com/gregstoll/rust-pathfinding) repo which has working code for all of these.



![vertex shaders example](../../assets/d90e2ec1bb0a5d26.png)

[@chrisbiscardi](https://twitter.com/chrisbiscardi) published a [video](https://youtube.com/watch?v=85uJc81SQZ4)
about using the new Material shader APIs in Bevy 0.8 to transform the
vertex positions in a custom mesh plane using a vertex shader.

*Discussions: Twitter*



![vertex shaders example](../../assets/f497f0b22ac7a615.png)

[@chrisbiscardi](https://twitter.com/chrisbiscardi) published a [video](https://youtube.com/watch?v=SOOOc9-joVo)
that introduces the new Material APIs in Bevy 0.8. It covers AsBindGroup,
uniforms, and using Perlin Noise in a fragment shader to render different
colors onto a cube in a variety of ways.

*Discussions: Twitter*

[Rusteroids](https://github.com/filtoid/rusteroids) is a tutorial recreating a clone of Asteroids
in Rust, using SDL2 and the [Specs](https://docs.rs/specs/latest/specs/) library.

New episodes are released weekly and added to the playlist. The most
recent video shows how to safely create global state to store global values,
such as the high score. The most recent code has been released for Windows, on
[Itch.io](https://filtoid.itch.io/rusteroids) (with other platforms coming soon).

You can subscribe to the [YouTube Channel](https://youtube.com/channel/UC1m6P72nySpB3lKWDYGVipw),
to never miss an episode, or follow [@ecatstudios](https://twitter.com/ecatstudios) on
Twitter!

![A screenshot from RuggRogue: a tiled view on a dungeon and a classic textual UI](../../assets/284fcbe13a05d69f.png)


[@tung](https://github.com/tung) has been working on a simple web-playable roguelike [RuggRogue](https://tung.github.io/ruggrogue)
inspired by the [Rust Roguelike Tutorial](https://bfnightly.bracketproductions.com/)
and documented the source code structure in a guide:

If you want to learn about the

[source code], you’ll also want to check out the[RuggRogue Source Code Guide]: a 23-chapter technical web book about the ideas, algorithms and structure of the code. It covers topics such as rendering, event handling, game states, the hand-rolled field of view and pathfinding calculations, game balance and more.

*Discussions:
/r/roguelikes,
/r/rust*

## Tooling Updates [#](https://gamedev.rs#tooling-updates)

![NES Bundler running Data Man with GUI showing](../../assets/fa5ba96440308794.png)

[NES Bundler](https://github.com/tedsteen/nes-bundler) is a NES ROM packaging tool by [@tedsteen](https://github.com/tedsteen).
Did you make a NES-game but none of your friends own a Nintendo? Don’t worry.
Put your ROM and configuration in NES Bundler and build an executable for Mac,
Windows or Linux. What you get is a single executable with

- Simple UI for settings
- Re-mappable Keyboard and Gamepad input (you bundle your default mappings).
- Save/Restore state
- Netplay!

It’s early days, but the key features are there, and work is ongoing to make it more mature!

![Blackjack: A procedural bridge being edited in real-time](../../assets/2c95b6af93f708cc.gif)


[Blackjack](https://github.com/setzer22/blackjack) by @setzer22 is a new procedural modeling application made in Rust,
using rend3, wgpu, and egui. It follows the steps of applications like
Houdini, or Blender’s geometry nodes project and provides a node-based
environment to compose procedural recipes to create 3d models.

The focus for the past few months has been on evolving Blackjack from a proof of concept into a usable application. Its current status is not yet production ready, but it can now be used to build complex procedural models editable inside a game engine thanks to its new engine integration system.

Some of the new features include:

- A better data model for meshes, based on groups and channels.
- Game engine integration with Godot, more engines coming soon.
- Introduce Lua as an extension language.
- Add many new nodes: Extrude along curve, Copy to points…
- Add experimental support for L-Systems.
- Reworked Look & Feel

A talk about Blackjack’s vision and a tour of its features was shared at the
start of July in the [Rust gamedev meetup](https://onrendering.com/data/papers/catmark/HalfedgeCatmullClark.pdf). Interested
developers are encouraged to [check the project out on GitHub](https://github.com/setzer22/blackjack) and
post on the Discussion boards!

![Shaders courtesy of @leondenise.](../../assets/f4586fd94a29eb79.gif)


[bevy_shadertoy_wgsl](https://github.com/eliotbo/bevy_shadertoy_wgsl) is a [Shadertoy](https://www.shadertoy.com) clone for the Bevy game engine,
where the GLSL shader language is replaced by WGSL. It already comes
with a dozen examples and plenty more to go. Feel free to add your own
shaders to the list!

Plus, [GLSL2WGSL](https://eliotbo.github.io/glsl2wgsl/) is a new translator tool that should help migrate the
vast majority of GLSL code to WGSL.

The above GIF showcases the new additions to the examples for
[bevy_shadertoy_wgsl](https://github.com/eliotbo/bevy_shadertoy_wgsl): two shaders originally written in [Shadertoy](https://www.shadertoy.com) by
[@leondenise](https://twitter.com/leondenise), and translated to WGSL with the help of [GLSL2WGSL](https://eliotbo.github.io/glsl2wgsl/).
The first part is a reproduction of Joe Gardner from the movie Soul,
and the second part is a lightweight fluid shader.

![Graphite logo](../../assets/aef06b56e7471700.png)


Graphite ([website](https://graphite.rs), [GitHub](https://github.com/GraphiteEditor/Graphite),
[Discord](https://discord.graphite.rs), [Twitter](https://twitter.com/GraphiteEditor)) is a free,
in-development raster and vector 2D graphics editor that will be based around a
Rust-powered node graph compositing engine.

July’s [sprint](https://github.com/GraphiteEditor/Graphite/milestone/17) focused on editor-centric
refactors upgrading stopgap measures to more robust systems.

- Making a splash: The default document is replaced by a welcome splash screen following a refactor allowing for zero open documents.
- Modifying for Macs: Input handling supports the nonstandard modifier keys on Mac keyboards, including labels in the UI.
- Setting a high bar: The menu bar cleans up actions and supports new ones like “File” > “Import”. Displayed hotkeys are based on the actual key mapping source, varying by OS.
- Keeping organized: The editor codebase is restructured to cut away technical debt and create consistency for new contributors and better docs going forward.

Open the [Graphite editor](https://editor.graphite.rs) in your browser to give it a try
and share your creations with #MadeWithGraphite on Twitter.

### Nintendo Switch Will Be a Tier 3 Target in Rust 1.64 [#](https://gamedev.rs#nintendo-switch-will-be-a-tier-3-target-in-rust-1-64)

[The pull request by @jam1garner](https://github.com/rust-lang/rust/pull/88991) that adds a no_std support for
the aarch64-nintendo-switch-freestanding target was merged this month
after a lengthy legal investigation.
This is the first step towards working on incrementally adding support
for the Nintendo Switch.
Check out [this Twitter thread](https://twitter.com/jam1garner/status/1547814292107378695) for more details
about the changes.

And btw, speaking of Nintendo targets: the std support for the Nintendo 3DS
(armv6k-nintendo-3ds) was [also merged this month](https://github.com/rust-lang/rust/pull/95897)!

*Discussions:
/r/rust*

## Library Updates [#](https://gamedev.rs#library-updates)

[bevy_godot](https://github.com/rand0m-cloud/bevy_godot) is an in-development library that offers a familiar Bevy environment
inside of the [Godot Engine](https://godotengine.org). [bevy_godot](https://github.com/rand0m-cloud/bevy_godot) currently features Scene
Tree integration, collision detection, spawning Godot scenes from Bevy, and
included examples to demonstrate the API. The upcoming update will feature Godot
signal events, Bevy assets integration, and a full implementation of the Dodge
the Creeps example game.

[bevy_godot](https://github.com/rand0m-cloud/bevy_godot) is looking for contributors to help grow the library to fit all
Godot Engine game development needs.

[hecs](https://github.com/Ralith/hecs) is a fast, lightweight, and unopinionated archetypal ECS library.

[Version 0.8](https://github.com/Ralith/hecs/blob/master/CHANGELOG.md#080) marks a breaking change to most methods that
previously took a generic type parameter `T: Component`

, replacing them with
methods taking type parameters which must be *references to* component types
instead. This resolves a long-standing footgun where users accustomed to writing
`&T`

in queries might write `world.get::<&T>`

, interpreted by rustc as
referencing the valid component type `&'static T`

, resulting in code that
compiles but fails to access the intended component.

[bevy_mod_wanderlust](https://crates.io/crates/bevy_mod_wanderlust)
([GitHub](https://github.com/PROMETHIA-27/bevy_mod_wanderlust)) by
[@PROMETHIA-27](https://github.com/PROMETHIA-27) is a character controller plugin for Bevy engine.

Inspired by [this excellent video](https://www.youtube.com/watch?v=qdskE8PJy6Q),
it is implemented on top of [Rapier physics](https://rapier.rs) and highly
customizable. Wanderlust includes a variety of settings to target many different
character controller types, including 2D/3D platformers, spacecraft, and
first/third person games.

![Variable width stroke in action](../../assets/2c6f6b52b1942e1a.png)


[Lyon](https://github.com/nical/lyon) ([GitHub](https://github.com/nical/lyon)) by [Nical](https://github.com/nical)
is a collection of crates providing various 2D vector graphics utilities, including
fast tessellation algorithms, easy to integrate in typical GPU accelerated rendering
engines.

Lyon made its symbolic [1.0.0 release](https://crates.io/crates/lyon/1.0.0)
reflecting the stability of the project. Highlights in this release include:

- Initial support for variable line width in the stroke tessellator.
- An efficient algorithm to query positions at given distances along a path.
- Improved support for specifying custom endpoint attributes in paths and algorithms.
- And more. You can read the
[announcement blog post here](https://nical.github.io/posts/lyon-1-0.html).

![3D capsles shooting red dots at each other](../../assets/ea6c5fcf93030c75.gif)

[Renet](https://github.com/lucaspoffo/renet) by [@lucaspoffo](https://github.com/lucaspoffo) is a network library to create
games with the Server-Client architecture.

Built on top of UDP, it has its own protocol to send and receive reliable messages more suited for fast-paced games than TCP. Some other features are:

- Connection management
- Authentication and encrypted connections
- Communication through multiple types of channels:
- Reliable Ordered: guarantee ordering and delivery of all messages
- Unreliable Unordered: no guarantee of delivery or ordering of messages
- Block Reliable: for bigger messages, such as level initialization

- Packet fragmentation and reassembly

Renet comes with [bevy_renet](https://github.com/lucaspoffo/renet/tree/master/bevy_renet), a plugin for the Bevy engine, and also with
[renet_visualizer](https://github.com/lucaspoffo/renet/tree/master/renet_visualizer), an egui interface to visualize network metrics.

![miniquad fileopen](../../assets/7bd9b0fa019ace36.gif)

[miniquad](https://github.com/not-fl3/miniquad/) is a safe and cross-platform rendering library
focused on portability and low-end platform support.

This month [OpenGl 2.1/GLESv2](https://github.com/not-fl3/miniquad/pull/305) PR got merged, adding support for old
android phones, virtual machines, and just old computers.
While the PR itself is quite small, it solved a very old design issue:
[compatibilities proposal](https://github.com/not-fl3/miniquad/pull/176). Fixing this issue opened the door for
both lower-end backends, like gl1, and higher-level backends. Metal is the
next in line.

![A model using a PBR shader featuring roughness and metalicness texture maps](../../assets/0ad1bdf150008a18.jpg)

[Samuel Rosario](https://www.artstation.com/artwork/bKJ0EE), rendered in bevy

[bevy_mod_fbx](https://github.com/HeavyRain266/bevy_mod_fbx) is a pre-alpha library to load FBX (Autodesk Filmbox) files
into [bevy](https://bevyengine.org) 0.8, based on [fbxcel-dom](https://lib.rs/crates/fbxcel-dom).
It currently:

- Loads geometry and meshes
- Loads mesh attributes such as color
- Loads default material diffuse textures, normal maps, and emissive maps
- Loads the custom Maya PBR materials, including all material textures
- Load the scene tree and translate it to bevy’s hierarchy

Planned features include providing a basic Lambert/Phong shader to better handle more standard materials, loading animations and skinned mesh skeletons/rigs.

The project is poorly tested and is looking for testers. It will soon be available on crates.io.

![logo of shame - shader metaprogramming](../../assets/38c28f9de8806d55.jpg)


[shame](https://github.com/RayMarch/shame) lets you author shaders and pipeline layouts
in a single seamless piece of rust code. It offers:

- a simple and lightweight setup,
- type checks from input assembly all the way to fragment output,
- (re)generate different shaders/pipelines based on runtime parameters,
[shader hot reloading](https://github.com/RayMarch/shame/tree/main/examples),[examples using wgpu](https://github.com/RayMarch/shame/tree/main/examples)!

A Discord channel for questions/feedback is linked in the
[GitHub readme](https://github.com/RayMarch/shame).

![A behavior tree visualization that starts with a "root" node and branches
into leafs like "run" and "get in cover"](../../assets/06165474e18304f7.png)

[bonsai-bt](https://github.com/Sollimann/bonsai) by [@Sollimann](https://github.com/Sollimann) is a Rust implementation of behavior trees.

A Behavior Tree (BT) is a data structure in which we can set the rules of how certain behaviors can occur and the order in which they would execute. BTs are a very efficient way of creating complex systems that are both modular and reactive. These properties are crucial in many applications, which has led to the spread of BT from computer game programming to many branches of AI and Robotics.


*Discussions: /r/rust_gamedev*

[shades](https://github.com/phaazon/shades) and [shades-edsl](https://github.com/phaazon/shades-edsl) [#](https://gamedev.rs#shades-and-shades-edsl)

![a source code that uses shades and a running app with the result: a gradient from green to red](../../assets/d757bdd37e8b27ac.png)


[@phaazon](https://phaazon.net) has published [a detailed article](https://phaazon.net/blog/shades-edsl) that introduces
[shades](https://github.com/phaazon/shades) and [shades-edsl](https://github.com/phaazon/shades-edsl) - two Rust crates to write shaders by writing pure Rust:

- The
[shades](https://github.com/phaazon/shades)crate provides all needed types and other building blocks - while
[shades-edsl](https://github.com/phaazon/shades-edsl)provides a proc-macro[EDSL](https://en.wikipedia.org/wiki/Domain-specific_language#External_and_Embedded_Domain_Specific_Languages)for transforming regular Rust code into the API from shades.

This crate provides an EDSL to build shaders, leveraging the Rust compiler (rustc) and its type system to ensure soundness and typing. Because shaders are written in Rust, this crate is completely language agnostic: it can in theory target any shading language - the current tier-1 language being GLSL. The EDSL allows to statically type shaders while still generating the actual shading code at runtime.


![black dots connected with ed lines in #d space](../../assets/bc374ed491c9741a.png)


[fdg](https://github.com/grantshandy/fdg) by [@grantshandy](https://grantshandy.github.io) is a [force-directed graph](https://en.wikipedia.org/wiki/Force-directed_graph_drawing) drawing framework.

The goal of this project is to provide a force-directed graph framework and algorithms for Rust, as well as 2D and 3D visualizers that work on the web and desktop. It sits on top of

[petgraph]and manages the positions of your nodes.

You can view all the examples online [here](https://grantshandy.github.io/fdg).

The project consists of three parts:

[fdg-sim](https://github.com/grantshandy/fdg/tree/main/fdg-sim)- the underlying force simulation framework that handles your dataset’s positions based on a physics engine of your choice (or creation).[fdg-macroquad](https://github.com/grantshandy/fdg/blob/main/fdg-macroquad)- a visualizer that uses macroquad for rendering.[fdg-img](https://github.com/grantshandy/fdg/tree/main/fdg-img)- a SVG visualizer for your graphs.

*Discussions: /r/rust*

## Other News [#](https://gamedev.rs#other-news)

- Other game updates:
[Hydrofoil Generation devs shared](https://twitter.com/HydrofoilG)a bunch of screenshots and videos with a new boat.[@epcc10](https://twitter.com/epcc10)shared a few videos about Idu getting a[better water rendering and physics](https://twitter.com/epcc10/status/1545918011185549313)and[better interaction with soil](https://twitter.com/epcc10/status/1547723415015919622).[Felix Windström](https://twitter.com/sov_gott_games)shared a couple of Paddlepunks updates:[a wizard leveling up their walls](https://twitter.com/sov_gott_games/status/1543227926052847616), and[increased the active time on witch’s doritos](https://twitter.com/sov_gott_games/status/1548340577233580035).[Legend of Worlds released their first devlog](https://reddit.com/r/rust_gamedev/comments/w2508b/legend_of_worlds_1).- The
[Bounce Up!](https://cryscan.itch.io/bounce-up)block breaker game shared a[video preview of the practice mode](https://youtube.com/watch?v=ohNQgahuj6U). [Theta Wave is now is now playable in the browser on itch.io](https://reddit.com/r/rust/comments/w4h4ad/thetawave_play_itch). Give it a try and let the author know what you think![Fish Folly](../../assets/fd438b2bbfcff8f4.img)posted a couple videos of[their new AI](https://youtube.com/watch?v=YRE5g57aZEg)and[the falling over mechanic](https://youtube.com/watch?v=RuoLInE34dM).[Punchy v0.0.2](https://reddit.com/r/rust/comments/vt44wq/media_punchy_v002)and[v0.0.3](https://reddit.com/r/rust/comments/waltwb/media_fish_fight_punchy_v003)were released, featuring scenes, egui UI, AI, playable web build, new enemy variants, controller remapping, and throwable bottles.

- Other tooling updates:
[annelid](https://github.com/dagit/annelid)is a speedrun timer with autosplitter for fxpak/sd2snes written using egui.[unitypacker](https://github.com/paulfigiel/unitypacker)is a tool for creating .unitypackages from the command line.

- Other learning material updates:
[@PhaestusFox](https://youtube.com/c/PhaestusFox)released a bunch of Bevy tutorial videos covering: gamepads, touch input, bevy 0.8 update & migration, and hierarchy.[The “Learn WGPU” tutorial was updated to wgpu v0.13](https://sotrh.github.io/learn-wgpu/news/0.13).- KyleMayes
[has ported vulkan-tutorial.com to vulkanalia](https://reddit.com/r/rust_gamedev/comments/w2g16h/another_vulkan_tutorial). [bevy_roguelike](https://github.com/tomuxmon/bevy_roguelike)is a project that implements reusable Bevy ECS systems and components for writing roguelike games.

- Other library updates:
[wgpu v0.13 and naga v0.9](https://reddit.com/r/rust_gamedev/comments/vp571t/release_of_wgpu_v013_and_call_for_testing)bring the newest WGSL spec support, improved presentation and pipelining, and lots of performance and correctness improvements. The devs also decided to make the DX12 backend default on Windows and are looking for testers.[bevy_pancam](https://github.com/johanhelsing/bevy_pancam)is a 2d-camera plugin for Bevy that works with orthographic cameras.


## Discussions [#](https://gamedev.rs#discussions)

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[‘Are We Game Yet?’ wants to know about projects/games/resources that aren’t listed yet](https://github.com/rust-gamedev/arewegameyet#contribute).[Graphite is looking for contributors](https://graphite.rs/contribute)to help build the new node graph and 2D rendering systems.[winit’s “difficulty: easy” issues](https://github.com/rust-windowing/winit/issues?q=is%3Aopen+is%3Aissue+label%3A%22difficulty%3A+easy%22).[Backroll-rs, a new networking library](https://github.com/HouraiTeahouse/backroll-rs/issues).[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[A/B Street’s “good first issue” issues](https://github.com/a-b-street/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/D-Good-First-Issue).

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!

**Discuss this post on**:
[/r/rust_gamedev](https://reddit.com/r/rust_gamedev/comments/wm0rl8/this_month_in_rust_gamedev_36_july_2022),
[Twitter](https://twitter.com/rust_gamedev/status/1557819704684716035),
[Discord](https://discord.gg/yNtPTb2).