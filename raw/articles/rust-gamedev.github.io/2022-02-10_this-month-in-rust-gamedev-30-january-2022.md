---
title: 'This Month in Rust GameDev #30 - January 2022'
url: https://gamedev.rs/news/030/
author: Rust GameDev WG
published: '2022-02-10'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 30th issue of the Rust GameDev Workgroup’s
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

[Rust GameDev Meetup](https://gamedev.rs/news/030/#rust-gamedev-meetup)[Game Updates](https://gamedev.rs/news/030/#game-updates)[Learning Material Updates](https://gamedev.rs/news/030/#learning-material-updates)[Engine Updates](https://gamedev.rs/news/030/#engine-updates)[Tooling Updates](https://gamedev.rs/news/030/#tooling-updates)[Library Updates](https://gamedev.rs/news/030/#library-updates)[Other News](https://gamedev.rs/news/030/#other-news)[Discussions](https://gamedev.rs/news/030/#discussions)[Requests for Contribution](https://gamedev.rs/news/030/#requests-for-contribution)[Jobs](https://gamedev.rs/news/030/#jobs)

## Rust GameDev Meetup [#](https://gamedev.rs#rust-gamedev-meetup)

![Gamedev meetup poster](../../assets/242a3acd459af39c.png)


The twelfth Rust Gamedev Meetup happened in January. You can watch the
recording of the meetup [here on Youtube](https://youtu.be/BIMsBFbPV-c). The meetups
take place on the second Saturday every month via the [Rust Gamedev Discord
server](https://discord.gg/yNtPTb2) and are also [streamed on
Twitch](https://twitch.tv/rustgamedev).

## Game Updates [#](https://gamedev.rs#game-updates)

### Flesh [#](https://gamedev.rs#flesh)

![flesh preview](../../assets/160fce8af5a2596e.gif)

[Flesh](https://store.steampowered.com/app/1660850/Flesh/) by [@im_oab](https://twitter.com/im_oab) is a 2D-horizontal shmup game with hand-drawn animation and
an organic/fleshy theme. It is implemented using [Tetra](https://github.com/17cupsofcoffee/tetra). This month’s updates
include:

- The completed first level, with a mid-boss and main boss.
- The second level of the game with new enemies.

![Rust engine powering original game](../../assets/dcf9fefb5083479b.jpg)

[Rusty Vangers](https://vange.rs) by [@kvark](https://github.com/kvark/) is a modern re-implementation of the original
[Vangers](https://www.gog.com/en/game/vangers) game from the last century.
It’s in Rust, and uses GPU and multiple threads heavily.

Something incredible has been brewing within the small but dedicated community
of the original game. They prototyped a pluggable rendering interface in order
to support rendering the game via [Rusty Vangers](https://vange.rs) instead of the default
CPU-based rasterizer. The plugin is made as a static library sub-crate with a
bunch of C-exported functions.
The approach worked for the terrain, so the mini working group transitioned
to moving more visual features off the old path and into the Rust-based plugin.

At the same time, [Rusty Vangers](https://vange.rs) engine got a number of important
fixes and additions:

- water is rendered fair as transparent surfaces
- lighting evaluation on the second layer is fixed
- dynamic terrain and palette modification is supported
- custom viewport support
- can render menu screens, not just the game levels

![way of rhea capsule image](../../assets/8f4362e9694e7b66.jpg)


[Way of Rhea](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n30) is a puzzle adventure with hard puzzles and forgiving
mechanics being produced by [@masonremaley](https://twitter.com/masonremaley) in a custom Rust
engine. It has a demo available [on Steam](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n30).

Latest developments:

[Making Your Game Go Fast by Asking Windows Nicely](https://www.anthropicstudios.com/2022/01/13/asking-windows-nicely/)was published, discussing Windows-specific performance tweaks in Way of Rhea’s engine- Work started on the Snowcrab + Teleporter puzzles, completing nearly all the puzzles in the main game
- Work began on art for The Professor (pictured left), Shrew, and Hermes
- Work began on artwork for the Mushroom Biome, and continued on the Hub World
- The narrative was reworked, and the dialogue system was improved
- The main menu, pause menu, and option screen UIs were replaced

You can stay up to date with the latest Way of Rhea developments by
[following it on Steam](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n30), signing up for [their mailing list](https://www.anthropicstudios.com/newsletter/signup),
or joining [their Discord](https://discord.gg/JGeVt5XwPP).

![Garden of the Centaur screenshot](../../assets/e82f37b50111090c.png)

Garden of the Centaur ([GitHub](https://github.com/Syn-Nine/rust-mini-games/tree/main/2d-games/centaur)) by
[@Syn-Nine](https://twitter.com/Syn9Dev) is an action-puzzle mini game where you navigate a
garden maze and steal the Centaur’s gems. Getting caught spells certain doom.

The game was created using Syn9’s [Rust Mini Game Framework](https://github.com/Syn-Nine/mgfw) and is
part of an open source [repository](https://github.com/Syn-Nine/rust-mini-games/) of several mini-games
that use this framework.

![Kataster screenshot](../../assets/40f13fca7306f302.jpg)


[Kataster](https://github.com/Bobox214/Kataster) by [@Bobox214](https://github.com/Bobox214) is a single-screen space shooter mini-game,
using [bevy](https://bevyengine.org/) and [heron](https://github.com/jcornaz/heron) (powered by [rapier](https://rapier.rs)).

Its goal is to be a simple demonstration game for [bevy](https://bevyengine.org/), and provide newcomers
another example to look into when they begin their journey with the engine.

The latest version includes:

- Support for
[bevy](https://bevyengine.org/)0.6 - A new shader background to showcase integration with the new renderer.

![Bright lantern](../../assets/25f3b5aa7cd4e31a.jpg)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In January, another [Veloren Reading Club was
recorded](https://www.youtube.com/watch?v=nR2WDBMjkh8)! The `entity_sync`

system was refactored to
be parallel. This was the largest bottleneck during the last release party, and
this fix will allow us to more easily surpass the 200 player mark on the server.
Work has been done to improve dagger animations. Sounds for flowing rivers are
now more bubbly sounding. Work is happening to get the OpenGL renderer to work
with WGPU for Veloren, as the project transitioned to Vulkan, but wants to keep
backward compatibility for older GPUs.

Skiing and ice skating have gotten to a playable state. The mounts system was
overhauled to make it more ergonomic to work with, you can [watch a video of
that here](https://www.youtube.com/watch?v=fJpeOJT78TI). Several experimental shaders have been
added, along with a “point glow” which help lanterns look better. With these new
shaders, swimming underwater is a whole new experience! A tracking issue was
created for worldgen issues that will help coordinate direction for some large
systems in the future.

January’s full weekly devlogs: “This Week In Veloren…”:
[#152](https://veloren.net/devblog-152),
[#153](https://veloren.net/devblog-153),
[#154](https://veloren.net/devblog-154),
[#155](https://veloren.net/devblog-155),
[#156](https://veloren.net/devblog-156).

![Editor for Not Snake](../../assets/497883cdeb7a6de6.gif)


Not Snake ([GitHub](https://github.com/ramirezmike/not_snake_game), [Itch](https://ramirezmike2.itch.io/not-snake)) by [Michael Ramirez](https://github.com/ramirezmike) is a
3D snake game where you don’t play as the snake.

Not Snake is being developed using the [Bevy game engine](https://bevyengine.org). The
first version can be played [here](https://ramirezmike2.itch.io/not-snake). An updated version
is now being worked on since the 0.6 release of [Bevy](https://bevyengine.org).

The bulk of the work this month was spent on creating a level editor
using the [egui](https://github.com/emilk/egui) and [bevy_mod_picking](https://github.com/aevyrie/bevy_mod_picking) crates to
make it easier to add new features/modes to the game.

Current features include:

- Able to create, customize, and delete game entities
- Multi-select entities for bulk changes
- Can play-test levels in the editor
- Camera controls
- Save/Load levels

More details on the initial editor work and a retrospective of the first
version of the game can be read [here](https://ramirezmike2.itch.io/not-snake/devlog/333283/retrospective-working-on-new-features) and a video of
the save/load feature can be seen [here](https://www.youtube.com/watch?v=cwI00pXDc6Q).

[Harvest Hero Origins](https://store.steampowered.com/app/1651500/Harvest_Hero_Origins/) is now available [#](https://gamedev.rs#harvest-hero-origins-is-now-available)

![harvest_hero](../../assets/f0247aeafbb24040.jpg)


[Harvest Hero Origins](https://store.steampowered.com/app/1651500/Harvest_Hero_Origins/) is an Arcade Wave Defense game that has been
in development by [Gemdrop Games](https://twitter.com/gemdropgames) for the past 10 months.

It is the studio’s first commercial release, developed in
the [Emerald](https://github.com/Bombfuse/emerald) game engine.

The game is available now on Windows and Linux for $2.99 with a launch discount of 10%!

The studio plans to provide free updates for a period of time, before moving on to focusing 100% of their efforts on the sequel, Harvest Hero.

Features

- Story Mode
- Survival Mode
- Competitive Leaderboards
- Infinitely Replayable
- 3 unique heroes
- 3 skins per hero
- Local co-op (online through steam remote play)


![hgs_screen](../../assets/33c3bfe0ef6597a0.jpg)


[Hydrofoil Generation](https://hydrofoil-generation.com/)
([Steam](https://store.steampowered.com/app/1448820/Hydrofoil_Generation/), [Facebook](https://www.facebook.com/HydrofoilGenerationSailing/), [Discord](https://discord.gg/DtKgt2duAy/))
is a realistic sailing/foiling inshore simulator in development for PC/Steam
that will put you in the driving seat of modern competitive sailing.

The last couple of months saw great disappointment for the failed port to WGPU due to unexpected performance losses compared to the old renderer. The game is now back to its original DirectX 11 renderer.

February will see the beginning of the private alpha testing program, an exciting opportunity to gather the first feedback about boat handling and controls before diving into one of the most challenging tasks of the game: sailing rules implementation.

Content-wise, Hong Kong will soon join Den Haag as a race location while the racecourse is becoming more and more alive with the addition of spectators boats. The playable foiling catamaran Jx50 is also constantly getting graphical updates and physics tweaks.

Hydrofoil Generation is scheduled to release on Steam Early Access in Summer 2022.

### Country Slice [#](https://gamedev.rs#country-slice)

![country_slice](../../assets/b79b8c988c04dad5.gif)


[Country Slice](https://github.com/anopara/country-slice) is
[@anastasiaopara](https://twitter.com/anastasiaopara/)’s hobby project, where users can draw a
small procedurally assembled scene.

The newest addition is an erase brush and an ability to continue existing walls.

[@anastasiaopara](https://twitter.com/anastasiaopara/) also shared [a Twitter thread](https://twitter.com/anastasiaopara/status/1477570256180817924)
about doing procedural generation in Houdini vs Rust & OpenGL.

## Engine Updates [#](https://gamedev.rs#engine-updates)

godot-rust ([GitHub](https://github.com/godot-rust/godot-rust), [Discord](https://discord.com/invite/FNudpBD), [Twitter](https://twitter.com/GodotRust))
is a Rust library that provides bindings for the Godot game engine.

The start of 2022 is a good opportunity to showcase a few godot-rust games in
development. More info is available in [the book](https://godot-rust.github.io/book/projects/games.html).

![godot-rust example games](../../assets/b5a042efa4acd7d2.jpg)


Using custom builds of the Godot engine involved quite a bit of ceremony in the
past: manual CLI invocations, code replacement, and re-wiring of the
`gdnative-bindings`

subcrate. The approach has been fundamentally overhauled,
and is now as simple as specifying the crate feature `custom-godot`

([#833](https://github.com/godot-rust/godot-rust/pull/833)). The library will automatically look for a `godot`

executable
in the system path (or a `GODOT_BIN`

environment variable), and regenerate
`api.json`

. This makes using older or module-extended Godot versions a breeze.

The latest `master`

branch has now been updated to support Godot 3.4 out of the
box ([#829](https://github.com/godot-rust/godot-rust/pull/829)).

Upcoming godot-rust version 0.10 seems to be finally on the horizon, with only a
handful of tasks left ([#842](https://github.com/godot-rust/godot-rust/issues/842)). A changelog since v0.9.3 is now
available. The continuous stream of small improvements here and there has led to
a sizable list! ([#845](https://github.com/godot-rust/godot-rust/pull/845))

![An example Rusty Engine game](../../assets/434948a05aaccc35.png)

[Rusty Engine](https://github.com/CleanCut/rusty_engine) by [Nathan Stocks](https://github.com/CleanCut) is a game engine built on top of Bevy
for people who are learning Rust.

Notable new features in Version 4.0 include: no need for an `init!`

macro, new
collider visualization, text can now be rotated and scaled, and an updated
[online tutorial](https://cleancut.github.io/rusty_engine/). See [the changelog for 4.0](https://github.com/CleanCut/rusty_engine/blob/main/CHANGELOG.md#400---2022-01-29) for the full details. On the
back end Bevy has been updated to 0.6 and `bevy_prototype_debug_lines`

was
replaced with `bevy_prototype_lyon`

.

![bevy bistro night](../../assets/59a3fcb5f485e850.jpg)

[Bevy](https://bevyengine.org/) is a refreshingly simple data-driven game engine built in Rust. It is
[free and open source](https://github.com/bevyengine/bevy) forever!

Bevy 0.6 was a massive community effort. You can check out the
[full release blog post here](https://bevyengine.org/news/bevy-0-6), but here are some highlights:

[A brand new modern renderer that is prettier, faster, and simpler to extend](https://bevyengine.org/news/bevy-0-6/#the-new-bevy-renderer)[Directional and point light shadows](https://bevyengine.org/news/bevy-0-6/#directional-shadows)[Clustered forward rendering](https://bevyengine.org/news/bevy-0-6/#clustered-forward-rendering)[Frustum culling](https://bevyengine.org/news/bevy-0-6/#visibility-and-frustum-culling)[Significantly faster sprite rendering with less boilerplate](https://bevyengine.org/news/bevy-0-6/#sprite-batching)[Native WebGL2 support](https://bevyengine.org/news/bevy-0-6/#webgl2-support). You can test this out by running the[Bevy Examples in your browser](https://bevyengine.org/examples)![High level custom Materials](../../assets/7fc6aea17c0f47a9.img)[More powerful shaders: preprocessors, imports, WGSL support](https://bevyengine.org/news/bevy-0-6/#wgsl-shaders)[Bevy ECS ergonomics and performance improvements. No more .system()!](https://bevyengine.org/news/bevy-0-6/#bevy-ecs)

*Discussions:
/r/rust,
Hacker News,
Twitter*

![three-d example of environment lighting](../../assets/371f7a75b65c5bce.jpg)

[ three-d](https://github.com/asny/three-d)
is a 2D/3D renderer targeting both desktop and web
that aims to make rendering simple and give the user full control.

`three-d`

0.10 has been released featuring:

- Environment lighting (image-based lighting)
- HDR environment map
- Headless graphics context
- Tangent vertex attributes
- Texture transform
- Cube map render targets
- f16 and u16 texture data types
- and more…

See [this Twitter thread](https://twitter.com/AsgerNyman/status/1482711259673944067) for videos.

[Tetra](https://github.com/17cupsofcoffee/tetra) is a simple 2D game framework, inspired by XNA, Love2D, and Raylib. This
month, an alpha version of Tetra 0.7 was released, featuring:

- Support for a wider variety of texture formats
- A more powerful API for blending
- Lots of bug fixes, cleanups, and improvements

For more details, see the [changelog](https://github.com/17cupsofcoffee/tetra/blob/main/CHANGELOG.md).

Alongside the release of this version, it was also [announced](https://twitter.com/17cupsofcoffee/status/1479601522661109764)
that Tetra is no longer under active development. The developer
has written a [retrospective blog post](https://www.seventeencups.net/posts/three-years-of-tetra/), explaining what went well
and what didn’t go so well with the engine’s development, and giving some
rationale for why they decided to move on from the project.

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

[Mason Remaley](https://twitter.com/masonremaley) published [a blog post](https://www.anthropicstudios.com/2022/01/13/asking-windows-nicely/) covering
Windows-specific performance tweaks employed in his Rust game engine:

Normally, to make your software go faster, it has to do less work. This usually involves improving your algorithms, skipping work the user won’t see, factoring your target hardware into the design process, or modifying your game’s content.

We’re not talking about any of that today. This post is a list of ways to make your game run faster on Windows–without making any major changes to your game’s content, code, or algorithms.


You can read more [here](https://www.anthropicstudios.com/2022/01/13/asking-windows-nicely/).

*Discussions:
/r/rust_gamedev*

[Justin Hurstwright](https://twitter.com/justin_rhw) published a [blog post](https://justinryanh.github.io/post/refactoring_from_legion_to_bevy/) describing
how to migrate from Legion ECS into Bevy ECS without giving up on
the other frameworks one might rely on.

You can read it [here](https://justinryanh.github.io/post/refactoring_from_legion_to_bevy/).

Trimoq ([GitHub](https://github.com/trimoq), [Twitter](https://twitter.com/amann_dev)) wrote [a blog
post](https://medium.com/digitalfrontiers/taking-rust-for-a-ride-to-azeroth-what-writing-an-ah-scanner-in-rust-taught-me-58edc936cbb) about writing a game client for a popular MMORPG. It
focuses on some negative parts of Rust and its ecosystem. There are three key
takeaways from this post:

- Stay away from low-level libraries if you are not aware of how deep the rabbit hole goes.
- Evaluate the library ecosystem of Rust thoroughly before using it for a project that requires somewhat exotic functionality.
- Rust forces you to care about the details, regardless of whether you want to.

The remainder of the article goes into depth on these three points.

This month, [Bevy Cheatbook](https://bevy-cheatbook.github.io) focused on refactors to improve navigation,
usefulness, and make maintenance easier going forward.

- Updated for Bevy 0.6
- Chapters reorganized to present content better and make things easy to find
[New page summarizing all the useful built-in types in Bevy](https://bevy-cheatbook.github.io/builtins.html)- Better info about
[working with WASM](https://bevy-cheatbook.github.io/platforms/wasm.html) - Info about
[cross-compiling for Windows from Linux](https://bevy-cheatbook.github.io/setup/cross/linux-windows.html) - Internal refactor for easy management of links, easier to avoid old/stale links
- Can link everything from everywhere! All pages are now full of links!
- All mentions of Bevy APIs now link to
[docs.rs](https://docs.rs/bevy)

The next priority for the project is to provide at least some coverage of the areas of Bevy still not in the book: 2D, 3D, UI, scenes, rendering…

If you’d like to support the project, donate to the author via
[GitHub Sponsors](https://github.com/sponsors/inodentry). Follow [@IyesGames on
Twitter](https://twitter.com/IyesGames) for updates.

![Screenshot of Extreme Bevy](../../assets/ecf1e61b3cb9272c.png)


Extreme Bevy is a [tutorial series](https://helsing.studio/posts/extreme-bevy) on how to create a low-latency
P2P web game.

It covers how to:

- Use
[Matchbox](https://helsing.studio/posts/introducing-matchbox)for setting up P2P connections using WebRTC data channels. - Implement rollback using
[GGRS](https://github.com/gschup/ggrs) - And using
[Bevy](https://bevyengine.org)with the above

The game itself is also live [here](https://helsing.studio/extreme), and [its source is on
GitHub](https://github.com/johanhelsing/extreme_bevy)

## Tooling Updates [#](https://gamedev.rs#tooling-updates)

![Demo that shows a simple circuit](../../assets/f49f7106805066fd.png)


Nodus ([GitHub](https://github.com/r4gus/nodus)) by [@r4gus](https://github.com/r4gus) is a digital circuit simulator
built with the Bevy game engine. The project is in an early stage of
development but, most of the basic features are implemented. That includes:

- Insert components like gates, switches, clocks, or light bulbs into the world using a radial context menu.
- Build digital circuits by connecting inputs and outputs of components with each other.
- Save projects to a .ron file and reload them later.

![Graphite](../../assets/cb7dbf8667258698.png)


[Graphite](https://graphite.rs) ([GitHub](https://github.com/GraphiteEditor/Graphite),
[Discord](https://discord.graphite.rs), [Twitter](https://twitter.com/GraphiteEditor)) is an in-development
raster and vector 2D graphics editor that is free and open source. It is
powered by a node graph compositing engine that supercharges your layer stack,
providing a completely non-destructive editing experience.

The team is proud and excited to announce Graphite alpha, the minimum viable product release for a web-based vector graphics editor. After one year in pre-alpha development by Rust Gamedev community members, this first milestone of alpha is here.

Graphite alpha launches **Saturday, February 12** together with a new
[project website](https://graphite.rs).

Work now commences on the second alpha milestone, focused on building the node
graph system and vector render engine. You are invited to join the team and
help make this exciting endeavor possible. [Join the Discord](https://discord.graphite.rs)
and get involved!

[Try Graphite right now in your browser](https://editor.graphite.rs) and please
[star the GitHub repo](https://gamedev.rs/news/030/graphite-repo) to build momentum. Thank you for helping
reach 1000⭐!

## Library Updates [#](https://gamedev.rs#library-updates)

### leafwing-input-manager [#](https://gamedev.rs#leafwing-input-manager)

`leafwing-input-manager`

([GitHub](https://github.com/Leafwing-Studios/leafwing-input-manager),
[crates.io](https://crates.io/crates/leafwing-input-manager)) by [@alice-i-cecile](https://twitter.com/AliceICecile)
is an ergonomic, featureful and fully documented Bevy library
for expressively abstracting over user input.

Supports local multiplayer, enables input rebinding, integrates with `bevy_ui`

,
and handles chords!



![Rafx Screenshot](../../assets/a7a0cb4eac9b7247.jpg)

[watch TAA demo on youtube](https://www.youtube.com/watch?v=iWYpX7RGUSA)!

[Rafx](https://github.com/aclysma/rafx) is a multi-backend renderer that optionally integrates with the
[distill](https://github.com/amethyst/distill) asset pipeline.

Since the previous rafx update in this newsletter (6 months ago!), many new features have been introduced to improve performance and image quality. The main rendering pipeline has also been split into “modern” and “basic” pipelines. Unlike the basic pipeline which focuses on wide compatibility, the modern pipeline uses forward-clustered lighting and handles hundreds of shadow-casting lights. It is targeting compute shaders and will be adding bindless and GPU-driven rendering soon.

Since the last update, the modern pipeline adds GPU-accelerated light binning,
SSAO, shadow map atlasing/caching, TAA with sharpening, and auto-exposure/HDR.
In addition, both modern and basic pipelines now support transparency. A
[video demonstrating TAA](https://www.youtube.com/watch?v=iWYpX7RGUSA) (temporal anti-aliasing) is
available on youtube.

With these performance improvements, `rafx`

is now able to render challenging
scenes with photorealistic style at 60FPS/1440p on modern, mid-range GPUs.

[erupt-bootstrap](https://gitlab.com/Friz64/erupt-bootstrap) by [@Friz64](https://blog.friz64.de/about) is a Vulkan Bootstrapping library for Rust.

When starting a new Vulkan project, there’s always the struggle of writing a
whole bunch of boilerplate code in order to, e.g., get your first triangle on
the screen. You have to create a `VkInstance`

, with the validation layers
set up and working for development. Then select the best suited
`VkPhysicalDevice`

for your app’s requirements. Use that to create a `VkDevice`

with the appropriate queue families chosen. Oh, and after that, you need
to struggle with managing and resizing a Vulkan swapchain.

That’s no fun — and this is where [erupt-bootstrap](https://gitlab.com/Friz64/erupt-bootstrap) comes in. It aims to
abstract over all of this to get you up and running in no time. It’s inspired by
the excellent [vk-bootstrap](https://github.com/charles-lunarg/vk-bootstrap) library for C++.

[Edict](https://github.com/zakarumych/edict) is a new archetype-based ECS implementation by [@zakarumych](https://github.com/zakarumych).

The novel feature of [Edict](https://github.com/zakarumych/edict) is entity ownership implemented via reference counting.
This optional feature allows creating owned kind of `Entity`

“reference”,
that ensures the entity is alive and despawns it on drop.
Storing owning `Entity`

in the component of another entity
creates ownership relation between those entities.
Even though `Entity`

is an owning reference,
components of the entity are can be queried from `World`

as usual.
Shared ownership is also available.

Optimized for both high density `World`

s with thousands of entities
and also for `World`

s with a lower number of entities spread among many archetypes.
[Edict](https://github.com/zakarumych/edict) is aimed at a wide range of game genres and use cases outside of games.

Built-in change detection with epochs allows systems to query for components
that were updated since the last run of that query,
or since any other epoch as defined by `Tracks`

argument.
This opens the possibility to have multiple POV on changes even in a single system.
For example, server-side netcode can track changes individually
for each client and query for changes since the last ACK.
[Edict](https://github.com/zakarumych/edict) optimizes iteration significantly when entities
with modified components are queried.

Although ECS abbreviation implies, [Edict](https://github.com/zakarumych/edict) does not come
with predefined `System`

trait and systems scheduler.
We can call it ECQ (Entity-Component-Query) as an alternative to ECS.

[Edict](https://github.com/zakarumych/edict) is added to [ecs_bench_suite](https://github.com/rust-gamedev/ecs_bench_suite)
so anyone can compare performance in some trivial examples with other ECS.

Development focus for February is making more public API, including unsafe parts, to allow writing custom queries, implement schedulers with parallel execution, etc.

[Backroll](https://github.com/HouraiTeahouse/backroll-rs) is a 100% type-safe native Rust implementation of the
[GGPO](https://www.ggpo.net/) rollback netcode library. The core library has gone through
superficial updates, but the [Bevy plugin](https://crates.io/bevy-backroll) has been
massively overhauled. This update significantly improves the ergonomics of setting
up rollback netcode for your game (no more ugly turbofishes! No more generic type
parameter config type!), provides an automatic way of saving and loading Bevy
components and resources, and fully parallelizes the saving and loading of game
state when a rollback occurs.

![Bevy Smud screenshot](../../assets/edea67c72a907986.png)

[Bevy Smud](https://github.com/johanhelsing/bevy_smud) is a new [Bevy](https://bevyengine.org) plugin for drawing 2D
shapes using signed distance fields.

It contains ports of all of [Inigo Quilez’ 2D SDF
primitives](https://iquilezles.org/www/articles/distfunctions2d/distfunctions2d.htm),
and allows easily composing said primitives together.

Shapes that share the same SDF and fill are automatically instanced, as shown in
the [demo video of 100k birds](https://twitter.com/jkhelsing/status/1486794339682508809)

## Other News [#](https://gamedev.rs#other-news)

- Other game updates:
[Molecoole](https://twitter.com/kiss_mrton/status/1477330931199496201)has some new gameplay footage from #screenshotsaturday.[Wordlet](https://www.reddit.com/r/rust/comments/s9kjoh/wordlet_a_commandline_clone_of_wordle_written_in/)is a command-line clone of Wordle, written in Rust.[BITGUN](https://twitter.com/LogLogGames/status/1481358714170970115)is looking for beta testers.[System Fault](https://www.lightsout.games/news/system-fault-early-access)is now in early access.[Lantern](https://qatoqat.itch.io/lantern)is a cute adventure game about a cat taking a nap.[Fish Fight](https://spicylobster.itch.io/fishfight/devlog/332434/fish-fights-past-present-and-future)has a new devlog about their past, present and future.[Starframe](https://molentum.me/blog/starframe-ropes/)has a new devlog about rope physics.[Cake Thieves](https://play.google.com/store/apps/details?id=com.GeTech.CakeThieves)is a strategy game about protecting cake from ants… with cannons![Idu](https://twitter.com/logicsoup/status/1487924659693703169)has released a new demo.[Sugarcane](https://gitlab.com/macmv/sugarcane)is a minigame-focused Minecraft server written in Rust.

- Other learning material updates:
- ‘
[How Bevy Uses Traits For Labelling](https://deterministic.space/bevy-labels.html)’ explains a cool usage of traits in the Bevy game engine. - ‘
[Writing a Tiny Rust Game Engine For Web](https://ianjk.com/game-engine-in-rust/)’ shows how to write a game engine with zero Rust dependencies. - ‘
[Extending States in Bevy](https://vaporsoft.net/extending-states-in-bevy/)’ shows how to make Bevy’s`State`

system more powerful. - ‘Mastering Plugin Loadings in Bevy’ (
[part 1](https://maz.digital/mastering-plugin-loadings-bevy-part-12)and[part 2](https://maz.digital/mastering-plugin-loadings-bevy-part-22)) is an overview of how Bevy plugins work, and how to write your own. - ‘
[Bevy Stages or The Frames Lifecycle](https://maz.digital/bevy-stages-or-the-frames-lifecycle)’ is an overview of the Bevy engine’s game loop lifecycle.

- ‘
- Other engine updates:
[Fyrox 0.24](https://rg3d.rs/general/2022/01/07/0.24-feature-highlights.html)(formerly known as rg3d) has been released.

- Other tooling updates:
[Fun Notation](https://www.reddit.com/r/rust_gamedev/comments/sfdl5s/fun_notation_guitar_tab_viewer)is a Bevy-based guitar tab viewer.[gbrs](https://github.com/adamsoutar/gbrs)is a Rust Game Boy emulator.

- Other library updates:
[Dimforge](https://dimforge.com/blog/2022/01/02/the-year-2021-in-dimforge/)posted a retrospective on their 2021, and goals for 2022.[poll-promise](https://github.com/EmbarkStudios/poll-promise)is a crate for polling asynchronous operations.[ezinput 0.2](https://twitter.com/eexsty/status/1485942270981464065)was released, providing easier input handling for Bevy.[bevy_asset_loader](https://crates.io/crates/bevy_asset_loader)had several new releases.[bevy_game_template](https://github.com/NiklasEi/bevy_game_template)was published.[big-brain 0.10](https://github.com/zkat/big-brain/releases/tag/v0.10.0)(a library for Utility AI in Bevy) was released.


## Discussions [#](https://gamedev.rs#discussions)

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[Graphite is looking for contributors](https://github.com/GraphiteEditor/Graphite/issues/202)to help build the new node graph and 2D rendering systems.[winit’s “difficulty: easy” issues](https://github.com/rust-windowing/winit/issues?q=is%3Aopen+is%3Aissue+label%3A%22difficulty%3A+easy%22).[Backroll-rs, a new networking library](https://github.com/HouraiTeahouse/backroll-rs/issues).[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[A/B Street’s “good first issue” issues](https://github.com/a-b-street/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/D-Good-First-Issue).

## Jobs [#](https://gamedev.rs#jobs)

[Embark Studios](https://careers.embark-studios.com/jobs)(Stockholm/Hybrid Remote) - Various roles

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!

**Discuss this post on**:
[/r/rust_gamedev](https://www.reddit.com/r/rust_gamedev/comments/spg3l1/this_month_in_rust_gamedev_30_january_2022/),
[Twitter](https://twitter.com/rust_gamedev/status/1491871330198818821),
[Discord](https://discord.gg/yNtPTb2).