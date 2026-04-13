---
title: 'This Month in Rust GameDev #27 - October 2021'
url: https://gamedev.rs/news/027/
author: Rust GameDev WG
published: '2021-11-07'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 27th issue of the Rust GameDev Workgroup’s
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

[Rust GameDev Meetup](https://gamedev.rs/news/027/#rust-gamedev-meetup)[Game Updates](https://gamedev.rs/news/027/#game-updates)[Learning Material Updates](https://gamedev.rs/news/027/#learning-material-updates)[Engine Updates](https://gamedev.rs/news/027/#engine-updates)[Tooling Updates](https://gamedev.rs/news/027/#tooling-updates)[Library Updates](https://gamedev.rs/news/027/#library-updates)[Other News](https://gamedev.rs/news/027/#other-news)[Meeting Minutes](https://gamedev.rs/news/027/#meeting-minutes)[Discussions](https://gamedev.rs/news/027/#discussions)[Requests for Contribution](https://gamedev.rs/news/027/#requests-for-contribution)

## Rust GameDev Meetup [#](https://gamedev.rs#rust-gamedev-meetup)

![Gamedev meetup poster](../../assets/4b7dbcb7e2ccc86f.png)


The tenth Rust Gamedev Meetup happened in October. You can watch the recording
of the meetup [here on Youtube](https://youtu.be/ta2HY4lD3iM). The meetups take place on
the second Saturday every month via the [Rust Gamedev Discord
server](https://discord.gg/yNtPTb2) and are also [streamed on
Twitch](https://twitch.tv/rustgamedev). If you would like to show off what you’ve been
working on at the next meetup on [November 13th](https://everytimezone.com/s/1f02d66b), fill
out [this form](https://forms.gle/BS1zCyZaiUFSUHxe6).

## Game Updates [#](https://gamedev.rs#game-updates)

![hgs_screen](../../assets/45a0af339ce1d4a8.png)


[Hydrofoil Generation Sailing](https://www.facebook.com/HydrofoilGenerationSailing/) ([Facebook](https://www.facebook.com/HydrofoilGenerationSailing),
[Discord](https://discord.gg/DtKgt2duAy)) is a realistic sailing/foiling
inshore simulator in development for PC/Steam that will put you in the
driving seat of modern competitive sailing.

The game is the brain child of industry veteran Stefano Casillo (of Assetto Corsa fame) and features a custom made 3D engine based on DirectX11 via winapi-rs.

An engine conversion to WGPU is currently under evaluation in order to guarantee an easier port to platform such as Steam Deck or even mobile in the future.

Early Access release on Steam is expected in mid 2022.

![An animated gif showing an engineer shooting rockets](../../assets/d41a797b3fb75bf4.gif)

[The Process](https://twitter.com/PlayTheProcess) by @setzer22 is an upcoming game about factory building, process
management, and carrot production, built with Rust using the Godot game engine!

For the past two months the project has seen some slow but steady progress. Work has started towards a simple combat system that will have the engineers fighting hordes of robots to defend their factories.

This month the game has seen the following changes and improvements:

- New assets like
[a robot enemy](https://twitter.com/PlayTheProcess/status/1436722776186966023)(concept by @Kath_Art_ic, modelling by @mkdirsrc),[a shoulder mounted gun](https://twitter.com/PlayTheProcess/status/1439970905220960259)and[new machine icons](https://twitter.com/PlayTheProcess/status/1455232744573788162). - A new system to attach armor-like models to in-game characters.
- Foundations of a combat system.
- Carrockets™! 🥕🚀
[(1)](https://twitter.com/PlayTheProcess/status/1445098719326658562)and[(2)](https://twitter.com/PlayTheProcess/status/1454787650657951745)

![LibraCity screenshot](../../assets/4b5b701325057351.png)


[LibraCity](https://djeedai.github.io/libracity/) is a puzzle city planning game by [@djeedai](https://twitter.com/djeedai) where you need to build
a city while balancing it on a needle (the center of the board). It was built for
[Ludum Dare 49](https://ldjam.com/events/ludum-dare/49/libra-city) using the [Bevy Engine](https://bevyengine.org/), and is a first-time use of the engine.

Post-jam, a webassembly version was added and published, which now allows
[playing the game online](https://djeedai.github.io/libracity/).

The code source is freely [available on GitHub](https://github.com/djeedai/libracity).

[Chaos Theory](https://ldjam.com/events/ludum-dare/49/chaos-theory-1) - gamified double pendulum simulator [#](https://gamedev.rs#chaos-theory-gamified-double-pendulum-simulator)

![Chaos Theory Gif](../../assets/072c635d5f031188.gif)


[Chaos Theory](https://ldjam.com/events/ludum-dare/49/chaos-theory-1) is a tiny HTML5 game by [@necauqua](https://twitter.com/necauqua) where you can draw and
simulate pendulums with a few goals and restrictions per level.
It was done for [Ludum Dare 49](https://ldjam.com/events/ludum-dare/49/chaos-theory-1) with a help of a small custom
engine with Rust being compiled to WASM and drawing shapes to an HTML5 canvas.

You can play the game [online](https://ld49.necauqua.dev), and the source code
is available [here](https://github.com/necauqua/chaos-theory) and
[here](https://github.com/necauqua/ld-game-engine).

![Me And My Unicycle screenshot](../../assets/babb19eb2be70b62.png)

[Me And My Unicycle](https://niklme.itch.io/me-and-my-unicycle) is a 2D physics game by [@nikl_me](https://twitter.com/nikl_me) submitted to Ludum
Dare 49. It is build with [Bevy](https://github.com/bevyengine/bevy) and [the code can be found on GitHub](https://github.com/NiklasEi/me_and_my_unicycle).

Following the LD49 theme “unstable”, the game is about riding a unicycle with challenging controls. Try making it through each level without falling.

All assets are self-made. The developer had a lot of fun recording audio and sound effects!

![image/crunda gameplay](../../assets/349b58d1b51d65be.gif)


[Crunda](https://ldjam.com/events/ludum-dare/49/crunda) is a game created in 48 hours for Ludum Dare 49.

Its unique wobbly planets are controlled by a Rust library.

Crunda was created by [Dan Slocombe](https://twitter.com/SLCMB/), came third, and was rated the
most fun competition game! The [sources can be found here](https://github.com/danslocombe/crunda_ludum_dare_49).

![berry](../../assets/c36d8d8657fe7c66.png)


[Berry Run](https://bombfuse.itch.io/berry-run/) is a community stream meme game by [@bombfuse_dev](https://twitter.com/bombfuse_dev) built on top of
[Emerald Engine](https://github.com/Bombfuse/emerald). It’s centered around the Twitch streamer [@berrybebopboy](https://twitter.com/berrybebopboy) and
was built in about 2 days.

Help Berry run as far as they can without tripping and falling!

Dodge the babies (no kids, no babies), evade the grannies (they’re heading to the grand canyon), and don’t touch belf (belf is sacred). Also a bunch of dunces left their logs and rocks lying around, better not to touch those, it would be rude to touch someone’s logs and rocks.


![Lonely Star screenshot](../../assets/f2112765a0d2a2a8.png)


[Lonely Star](https://17cupsofcoffee.itch.io/lonely-star) is a 2D ‘endless runner’ game by [@17cupsofcoffee](https://twitter.com/17cupsofcoffee), featuring
simple generative music. It was built with [Tetra](https://github.com/17cupsofcoffee/tetra) back in February 2020,
for Weekly Game Jam 135.

This month, it was made [open-source](https://github.com/17cupsofcoffee/lonely-star), and received a
small update to improve the UI and fix a few bugs.

![Soldank](https://raw.githubusercontent.com/smokku/soldank/master/sshot.png)


[Soldank](https://github.com/smokku/soldank) ([GitHub](https://github.com/smokku/soldank),
[Discord](https://discord.gg/cTaC4UtqE6)) by [@smokku](https://twitter.com/smokkku)
is an open source clone of [Soldat](http://soldat.pl/) engine. It aims for full compatibility
with original game files, mods and gameplay with modernized
graphics engine and multiplayer networking code.

Recent developments include:

- Engine/game code split
- Command Line Interface
[Rhai](http://rhai.rs/)scripting`hecs_rapier`

integration- Key/mouse-binding support
- Soldat’s
`.cfg`

files support - Custom debug shapes rendering
- Performance degradation fix
- Refactored code to build on
`hecs`

ECS - ECS entities debug UI

The developer have also written a blog post:
‘* Engine and scripting*’

![image/gameplay of the game: circle and triangles](https://gamedev.rs/news/027/graph_game.gif)

[Graph Game](https://vrixyz.github.io/graph_nav/) ([GitHub](https://github.com/Vrixyz/graph_nav))
uses [Bevy](https://bevyengine.org/) as its engine. You can play it from your
[browser](https://vrixyz.github.io/graph_nav/) - click on colored triangles,
guess the rules and survive as long as possible!

Development has just begun, and the future of the project is not clear -
the developer welcomes you to come and discuss next steps on the game’s
[Discord server](https://discord.gg/ZeRkj8pD4n).

![way of rhea capsule image](../../assets/439f4c36f95d2720.jpg)


[Way of Rhea](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n27) is a puzzle adventure with hard puzzles and forgiving
mechanics. It is being produced by [@masonremaley](https://twitter.com/masonremaley).

Latest developments:

- Way of Rhea now has a
[free demo available on Steam](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n27) - Way of Rhea was shown at
[PAX West](https://west.paxsite.com/)this year (as were a couple other Rust games!), and will also be showcased at[MAGWest](https://www.magwest.org/) - A new trailer showing off new level art
[was published](https://www.youtube.com/watch?v=46ELQYaH0uw) - Additional animation work,
[visuals](https://twitter.com/AnthropicSt/status/1448056148138119169), and puzzles have been added to the game - Improvements were made to the undo system, the tutorial level, and the dialogue system in response to user feedback
- Some Proton compatibility problems were fixed, some visual glitches were fixed, and support was added for adaptvie vsync

You can stay up to date on the latest developments of Way of Rhea by
[following it on Steam](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n27), or signing up for
[the mailing list.](https://www.anthropicstudios.com/newsletter/signup)

![Animated gameplay that looks like pong mixed with an anime fighting game](../../assets/67cc916bbbb2753a.gif)

PaddlePunks is a versus tennis game by [Felix Windström](https://twitter.com/sov_gott_games)
with a diverse cast of characters and playstyles and online play with rollback
netcode. The game takes cues from both fighting games and arcade classics, and
besides netplay supports local play against another human or several levels of
AI.

You can download and play the game now on [itch.io](https://sovgott.itch.io/paddlepunks), or
join the [Discord](https://discord.gg/cpPDeVcWxc) to chat with the developer and other
players. Updates are also posted to [Twitter](https://twitter.com/sov_gott_games).

![An early-morning sunrise](../../assets/c2c85379343f8994.jpg)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In October, Veloren hit 10,000 commits, as well as 10,000 members on the Discord
server! Shrubs got added, along with improvements to rivers, and the
addition of waterfalls. There have been efforts to diagnose some network issues
that have been causing downloads to not work for some people. Crafting is going
through overhauls on the backend. [New aurora shaders](https://www.youtube.com/watch?v=60kt915avjI)
were added as well.

Initial ideas are being discussed to try and improve the amount of asset files that have to be downloaded with each update of the game, which will help improve the 200MB that has to be downloaded after each nightly update. New jewelery has been added, and sneaking is being improved to make agents in the game react better to it. Ongoing worldgen improvemnts are also being made as we head into November.

October’s full weekly devlogs: “This Week In Veloren…”:
[#140](https://veloren.net/devblog-140),
[#141](https://veloren.net/devblog-141),
[#142](https://veloren.net/devblog-142),
[#143](https://veloren.net/devblog-143).

## Engine Updates [#](https://gamedev.rs#engine-updates)

![amethyst logo](../../assets/6692a81ae6e6d242.png)


This month, the developers of the Amethyst game engine
[announced that they would be winding down development](https://amethyst.rs/posts/amethyst--starting-fresh).

The Amethyst Foundation, however, lives on! It will be shifting focus to support the wider Rust game development ecosystem, through engine-agnostic libraries, curated guides/lists, and more inititives yet to be announced.

[All is Cubes](https://github.com/kpreid/all-is-cubes/) 0.3.0 [#](https://gamedev.rs#all-is-cubes-0-3-0)

All is Cubes ([GitHub](https://github.com/kpreid/all-is-cubes/), [Crates.io](https://crates.io/crates/all-is-cubes)) by [kpreid](https://github.com/kpreid)
is a game/engine for worlds made of blocks made of voxels. It is intended to be
usable both as an engine or rendering library, or as a game with built-in
editor/programming functionality (genre(s) to be determined). While the project
is still highly incomplete and API-unstable, the 0.3.0 release marks a lot of
now-usable functionality ([changelog](https://github.com/kpreid/all-is-cubes/blob/main/CHANGELOG.md#030-2021-10-09)):

- UI: mouselook, multiple example scenes, inventory with stacks, and rendering to image files.
- Simulation/mechanics: character collision against arbitrary voxel shapes, much-improved light propagation, transactional state updates (all-or-nothing, internally order-independent), and “behaviors” attached to game objects for scripting/animation.
- Rendering: high-voxel-count blocks (incomplete, but usable for text as seen in the above screenshot), “smooth lighting” (interpolated across faces), frustum culling, and correct sRGB-versus-linear color handling.

The next planned milestone is saving/loading.

[Tetra](https://github.com/17cupsofcoffee/tetra) is a simple 2D game framework, inspired by XNA, Love2D, and Raylib. After
a few quiet months, version 0.6.6 has been released, featuring:

- A big overhaul of the keyboard API, with better support for international layouts
- Lots of new functions for manipulating the game window
- A long-requested
[ECS example](https://github.com/17cupsofcoffee/tetra/blob/main/examples/ecs.rs) - Bugfixes and docs improvements

For more details, see the [changelog](https://github.com/17cupsofcoffee/tetra/blob/main/CHANGELOG.md).

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)



![An early-morning sunrise](../../assets/27c93bc52a7c5476.png)

Back in September, the University of Glasgow’s GameLab held a ‘GameDev Mini
Symposium’ online. One of the featured speakers was
[Herbert Wolverson](https://twitter.com/herberticus), writer of ‘[Hands-on Rust](https://pragprog.com/titles/hwrust/hands-on-rust/)’,
who gave a talk on using Rust for game development.

This talk is now available to [view on Herbert’s YouTube channel](https://www.youtube.com/watch?v=OzUsPi4kHes).

## Tooling Updates [#](https://gamedev.rs#tooling-updates)

![SPV-0.1.0 screenshot](../../assets/5d2c1407bd23b5bb.png)


[SPV](https://github.com/AlbinSjoegren/SPV) by [Albin Sjögren](https://github.com/AlbinSjoegren)
is a calculator utility for working with astronomical position and velocity data.

What was added for the first alpha release:

- A new UI
- Corrected vector normalizing
- JSON and TXT exporting

The primary features that are being worked on:

- A crate version
- Output file structure
- Batch processing

For any feature requests, reach out to the developer on [Discord](https://discordapp.com/users/258254056185659392)
or [GitHub](https://github.com/AlbinSjoegren/SPV).

## Library Updates [#](https://gamedev.rs#library-updates)

![bevy webgl2 via wgpu](../../assets/0952564a1d4d6246.png)

The team is happy to announce the release of wgpu-0.11 and naga-0.7.
Details can be found on the [gfx-rs blog](https://gfx-rs.github.io/2021/10/07/release-0.11.html). The most exciting feature
is WebGL2 support. With some caveats, users no longer need to wait for
WebGPU in the browsers in order to deploy on the Web. Support is still
a bit rough, and patches come out regularly, but most examples work.

@kvark also visited [Rust LA Meetup](https://rustlang.la/) to [talk about Naga](https://vimeo.com/632377558)
and the history of processing shaders with Rust.

![rend3-scifi](../../assets/15451ae087343f0e.jpg)

rend3 is a 3D rendering library that focuses on having an easy to use interface without sacrificing performance or customizability.

As part of their monthly release schedule, the developers are excited to announce the release of rend3-0.2. The most prominent change is the ability to use fully customizable materials. Any combination of data and textures can now be used as a material for custom render routines. This unties the user from PBR-based materials.

Along with the customizability that comes with this change, the CPU time
required to render a complex scene is 7x less due to highly optimal data
structures. For more information see [this talk](https://www.youtube.com/watch?v=F0wGz5UJTrY) at the Rust
graphics meetup.

The [v0.2 version](https://crates.io/crates/rend3) was published on crates.io
([docs](https://docs.rs/rend3) and [examples](https://github.com/BVE-Reborn/rend3/tree/v0.2/examples)). The 0.3 release is
just a week away and further improves customizability.

[hecs_rapier](https://github.com/smokku/hecs_rapier) 0.11.0 [#](https://gamedev.rs#hecs-rapier-0-11-0)

[hecs_rapier](https://github.com/smokku/hecs_rapier) is a physics engine for hecs ECS.
It is a direct port of [bevy_rapier2d](https://github.com/dimforge/bevy_rapier).

Recent development added joints and physics_hooks support.
This makes `hecs_rapier`

feature complete, with `bevy_rapier2d`

feature parity.

[bevy_atmosphere](https://github.com/JonahPlusPlus/bevy_atmosphere) 0.1.1 [#](https://gamedev.rs#bevy-atmosphere-0-1-1)

![dawn in bevy_atmosphere](../../assets/20ca97d174863d59.png)


[bevy_atmosphere](https://github.com/JonahPlusPlus/bevy_atmosphere) ([GitHub](https://github.com/JonahPlusPlus/bevy_atmosphere)) by @JonahPlusPlus
is a procedural sky plugin for Bevy.

By adding the `AtmospherePlugin`

, users get a skybox around the camera in their scene.
Users can also set the appearance of the sky adding a `AtmosphereMat`

resource.

0.1.0 and 0.1.1 have been released on [crates.io](https://crates.io/crates/bevy_atmosphere).

0.1.1 changes the default position of the sun to be in the sky, so only the plugin is needed to get a Unity-like sky.

[bevy_kira_audio](https://github.com/NiklasEi/bevy_kira_audio) is a [Bevy](https://github.com/bevyengine/bevy) plugin that integrates the audio library [Kira](https://github.com/tesselode/kira)
into [Bevy](https://github.com/bevyengine/bevy) applications.

In the latest version `0.6.0`

, you can load files with custom semantic
durations and play looped audio with an intro. The plugin now also cleans up
old sound instances. Following Bevy, [bevy_kira_audio](https://github.com/NiklasEi/bevy_kira_audio) is now licensed under
dual MIT + Apache 2.0, and the library will no longer crash on systems without
an audio device.

![bevy_verlet](../../assets/f688a87d333a420a.gif)


[bevy_verlet](https://github.com/ManevilleF/bevy_verlet) is a lib for projects using [Bevy Engine](https://bevyengine.org/)
providing a plugin to use [verlet integration](https://en.wikipedia.org/wiki/Verlet_integration)
physics. Very useful for cloth simulation and joints, and less expensive than
complex physics engine, it is a nice addition to 2D or 3D projects. Making good
use of the Entity-Component-System architecture of the bevy engine, any entity
can become a `VerletPoint`

and have physics applied to it.

The crate also provides *sticks* which constrains the points in order to create
strings or cloth. With its modularity, you may customize the physics precision
(iterations), the gravity, and the physics time step to use.

New features:

- Query parallel batching and custom batching size
- Global documentation
- Fixed issues with timesteps
- Improved examples

You may contact the author on Twitter at [@ManevilleF](https://twitter.com/ManevilleF) or join the
[discussion](https://twitter.com/ManevilleF/status/1437350669858611202?s=20).

![bevy_pen_tool2](../../assets/cc08fedf2ea111f2.gif)


Bevy Pen Tool is a plugin that helps developers make 2D paths using Bezier curves. Its user interface provides functionality for:

- spawning Bezier curves,
- moving end points and control points of Bezier curves,
- linking individual Bezier curves to each other,
- grouping curves,
- saving and loading paths as look-up tables (typically for animations and agent movement),
- generating arbitrary 2D meshes that fill the interior of a path using the Lyon crate,
- generating a mesh that follows a path like a road,
- saving meshes and roads in “.obj” format,

A stable version of Bevy Pen Tool should come out as a crate shortly
after Bevy 0.6 shows up. Here is a link to the [repo for more
information](https://github.com/eliotbo/bevy_pen_tool).

[Sparsey](https://github.com/LechintanTudor/sparsey) by [@LechintanTudor](https://github.com/LechintanTudor) is a sparse set-based Entity Component System
(ECS) with component storage grouping, granular component change detection,
fallible systems and beautiful syntax.

The latest release (0.4) adds support for optional system parameters, which
allows `Option<Res<T>>`

and `Option<ResMut<T>>`

to be used in system functions.

This release also features a refactored `ComponentStorage`

which makes adding,
removing and swapping components faster, swapping being especially important
since it enables component grouping, a features that makes certain queries
specified by the user extremely fast.

Finally, some implementation details were hidden from the public API and the
`#[must_use]`

attribute was added to functions whose results should not be
discarded.

![godot-rust logo](../../assets/8ca61fe2aae69e16.png)


godot-rust ([GitHub](https://github.com/godot-rust/godot-rust), [Discord](https://discord.com/invite/FNudpBD), [Twitter](https://twitter.com/GodotRust))
is a Rust library that provides bindings for the Godot game engine.

Recent developments have added [foundational support to async](https://github.com/godot-rust/godot-rust/pull/804)
that enables users to make use of the Rust async runtimes with the Godot Engine
(thanks to chitoyuu for the PR).

In addition to the foundational support, lyonbeckers was kind enough to
include a [new recipe in the User Guide](https://github.com/godot-rust/book/pull/44) that covers
how to configure async with `tokio`

.

The team also merged several smaller bug fixes in [#791](https://github.com/godot-rust/godot-rust/pull/791), [#795](https://github.com/godot-rust/godot-rust/pull/795),
and [#800](https://github.com/godot-rust/godot-rust/pull/800) and is making steady progress towards version 0.10.0.

Finally, the team has recently added a [third party project](https://godot-rust.github.io/book/projects.html)
section in the book to help promote games, applications, and libraries/tools
that are working with godot-rust. If you have a project that you would like to
be included, please feel free to reach out to the godot-rust team.

## Other News [#](https://gamedev.rs#other-news)

- Other game updates:
- LD49
[Unbalanced Brawl](https://ldjam.com/events/ludum-dare/49/unbalanced-brawl)([GitHub](https://github.com/yopox/LD49)) is an autochess with ever-changing rules in the shop. - LD49
[Chevalchemy](https://ldjam.com/events/ludum-dare/49/chevalchemy-a-hoof-of-concept)([GitHub](https://github.com/xlambein/ldjam49)) is a game where you play as a horse alchemist working for the great Neighcolas Flamel. - LD49
[Proc Spider](https://ldjam.com/events/ludum-dare/49/procedural-spider)([GitHub](https://github.com/darthdeus/procedural-spider)) is a small game where you play a big spider chasing small spiders. [mk48.io](https://mk48.io)([GitHub](https://github.com/SoftbearStudios/mk48)) is an online multiplayer naval combat game, in which you take command of a ship and sail your way to victory.- Tweets about
[Bitgun](https://store.steampowered.com/app/1673940/BITGUN)progress:[new inventory and weapon systems](https://twitter.com/LogLogGames/status/1449485172114591749),[new item pickup](https://twitter.com/LogLogGames/status/1449742242734772225),[jumping zombies](https://twitter.com/LogLogGames/status/1450922044065992708),[death animation](https://twitter.com/LogLogGames/status/1451088866052489218). [An update about the progress of Rust version of Nox Futura](https://reddit.com/r/roguelikedev/comments/pqbvv1/sharing_saturday_380/hdbx5xt).[A Recall Singularity](https://twitter.com/RecallSingular1)shared a[YouTube video](https://youtube.com/watch?v=nsjnCZslNdg)that shows new shooting sounds, camera movement, and asteroid dragging.

- LD49
- Other learning material updates:
[A video by TanTan](https://youtube.com/watch?v=G-IuH6R-yD8)about rewriting a voxel game three times: in Unity, Rust (no engine) and Bevy.

- Other engine updates:
[A recording of the first rg3d live-coding stream](https://reddit.com/r/rust/comments/qena0b/media_rg3d_game_engine_live_coding).- The first prototype of
[VNgine](https://gitlab.com/porky11/vngine-rs)- Visual Novel Engine -[was announced on /r/rust](https://reddit.com/r/rust/comments/pyvcen/first_prototype_of_vngine). - Also, a general purpose graphics engine
[Blue Engine](https://github.com/ElhamAryanpur/BlueEngine)[was announced on /r/rust_gamedev](https://reddit.com/r/rust_gamedev/comments/q4rana/blue_engine).

- Other tooling updates:
[Fearless-NES](https://github.com/TomasKralCZ/Fearless-NES)is a NES emulator written using egui, macroquad, and GilRs.[FishSteam](https://github.com/not-fl3/FishFight-The-Prequel/tree/main/fishsteam)is a tool for deploying SteamWorks-enabled steam builds for Windows/macOS/Linux without SteamWorks SDK on a CI.

- Other library updates:
[Crevice v0.8](https://github.com/LPGhatguy/crevice/blob/main/CHANGELOG.md#080---2021-10-26)brings a direct support for many math libraries and allows to generate GLSL source from structs.[SPV](https://github.com/AlbinSjoegren/SPV)0.0.6 is the second pre-alpha release of a celestial object position and velocity calculator.[Thunderdome](https://github.com/LPGhatguy/thunderdome/blob/main/CHANGELOG.md)generational arena library released[0.4..0.5 versions](https://github.com/LPGhatguy/thunderdome/blob/main/CHANGELOG.md).[egui 0.15](https://reddit.com/r/rust/comments/qeue67/announcing_egui_015)brings: syntax highlighting, horizontal scrolling, new monospace font, and a new opt-in glow backend for eframe.[New puffin-egui/puffin-viewer](https://twitter.com/ernerfeldt/status/1447961523696066564)allows selection and manipulation of multiple frames.[Shalrath](https://github.com/QodotPlugin/shalrath)is a fully-safe Rust representation and nom parser for Quake map files.


## Meeting Minutes [#](https://gamedev.rs#meeting-minutes)

There is currently discussion ongoing around bringing back the Rust GameDev Working Group’s regular meetings.

If you are interested in getting involved, please join the
[discussion thread](https://github.com/rust-gamedev/wg/discussions/115)
on the working group’s issue tracker!

## Discussions [#](https://gamedev.rs#discussions)

On the Rust user forum, there was [a post](https://users.rust-lang.org/t/tokio-tungstenite-async-game-server-design/65996)
asking how to use async/await (more specifically, `tokio`

and
`tokio_tungstenite`

) to develop a multiplayer game server.
The responses contain some useful ideas and advice which
may be helpful for other people’s projects!

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[Graphite is looking for contributors](https://github.com/GraphiteEditor/Graphite/issues/202)to help reach the 0.1 Alpha release.[winit’s “difficulty: easy” issues](https://github.com/rust-windowing/winit/issues?q=is%3Aopen+is%3Aissue+label%3A%22difficulty%3A+easy%22).[Backroll-rs, a new networking library](https://github.com/HouraiTeahouse/backroll-rs/issues).[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[A/B Street’s “good first issue” issues](https://github.com/a-b-street/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/D-Good-First-Issue).

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!

**Discuss this post on**:
[/r/rust_gamedev](https://www.reddit.com/r/rust/comments/qoy5rv/this_month_in_rust_gamedev_27_october_2021/),
[Twitter](https://twitter.com/rust_gamedev/status/1457461009833238528),
[Discord](https://discord.gg/yNtPTb2).