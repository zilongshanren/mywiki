---
title: 'This Month in Rust GameDev #42 - January 2023'
url: https://gamedev.rs/news/042/
author: Rust GameDev WG
published: '2023-02-26'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 42nd issue of the Rust GameDev Workgroup’s
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

[Announcements](https://gamedev.rs/news/042/#announcements)[Game Updates](https://gamedev.rs/news/042/#game-updates)[Engine Updates](https://gamedev.rs/news/042/#engine-updates)[Learning Material Updates](https://gamedev.rs/news/042/#learning-material-updates)[Tooling Updates](https://gamedev.rs/news/042/#tooling-updates)[Library Updates](https://gamedev.rs/news/042/#library-updates)[Other News](https://gamedev.rs/news/042/#other-news)[Discussions](https://gamedev.rs/news/042/#discussions)[Requests for Contribution](https://gamedev.rs/news/042/#requests-for-contribution)[Jobs](https://gamedev.rs/news/042/#jobs)

## Announcements [#](https://gamedev.rs#announcements)

### Rust Graphics Meetup #3 [#](https://gamedev.rs#rust-graphics-meetup-3)

The Rust Graphics Meetup is an online gathering where Rustaceans share technical details of their work related to graphics and compute, not affiliated with any particular stack. The third edition happened on January 28th! These were the talks:

- Hello, Blade! -
[Dzmitry Malyshau](https://github.com/kvark) - Implementing an Extensible Renderer -
[Philip Degarmo](https://github.com/aclysma) - Rend3: High Performance, Cross Platform, GPU Driven Rendering in wgpu and
WebGPU -
[Connor Fitzgerald](https://github.com/cwfitzgerald)

Learn more at the [gfx meetup repo](https://github.com/gfx-rs/meetup). The individual videos haven’t been uploaded
yet, but you can watch the [full meetup here](https://www.youtube.com/watch?v=63dnzjw4azI). Thanks
everyone for tuning in and helping to make this happen!

### Rust GameDev Meetup [#](https://gamedev.rs#rust-gamedev-meetup)

![Gamedev meetup poster](../../assets/6c7b6da85cb04c06.png)


The 23rd Rust Gamedev Meetup took place in January. You can watch the recording
of the meetup [here on Youtube](https://youtu.be/iSu-9yKsCRY). Here was the schedule
from the meetup:

- Blade -
[@kvark](https://github.com/kvark) - Digital Extinction-
[@Indy2222](https://twitter.com/Indy2222) - Graphite -
[@GraphiteEditor](https://twitter.com/GraphiteEditor)

The meetups take place on the second Saturday of every month via the [Rust
Gamedev Discord server](https://discord.gg/yNtPTb2) and are also [streamed on
Twitch](https://twitch.tv/rustgamedev).

## Game Updates [#](https://gamedev.rs#game-updates)

### Digital Extinction [#](https://gamedev.rs#digital-extinction)

![Building Placement in Digital Extinction](../../assets/64f14d5086dee92e.jpeg)

[Digital Extinction](https://de-game.org) ([GitHub](https://github.com/DigitalExtinction/Game), [Discord](https://discord.gg/vHMFuCWGSX),
[Reddit](https://reddit.com/r/DigitalExtinction)) by [@Indy2222](https://twitter.com/Indy2222) is a 3D real-time strategy game made with
[Bevy](https://bevyengine.org).

This month the game had two new first-time contributors, [@0HyperCube](https://github.com/0HyperCube) and
[@Polostor](https://github.com/Polostor) (Péťa Tománek).

The most notable updates are:

- several multiplayer related screens were added to the menu: sign-in / sign-up, game listing, and game creation,
- building draft is now semi-transparent and colored green or red based on obstacles,
- double clicking on a unit or building leads to the selection of all visible entities of the same type,
- the mouse cursor is now confined to the game window,
- the camera can be moved horizontally with arrow keys,
- pop-up in-game menu was added, it is opened with Escape key,
- work on game head-up display / panel (HUD) was initiated,
- various errors are now briefly displayed as toasts in the UI,
- support of map hashing was added and deterministic map paths are used,
- several small fixes, and code quality improvements.

See [gameplay](https://youtu.be/JP01dAbtoc8) and [menu](https://youtu.be/APTlkGnn6vA) screen recordings on YouTube.

A more detailed update summary is available [here](https://mgn.cz/blog/de04/).

![Screenshot of p2p multiplayer in Cargo Space: One instance running on windows
and one in Chrome](../../assets/5c035375e802274f.png)

[Cargo Space](https://helsing.studio/cargospace) ([Discord](https://discord.gg/ye9UDNvqQD)) by
[@johanhelsing](https://mastodon.social/@johanhelsing) is a co-op 2d space game where you build
a ship and fly it through space looking for new parts, fighting pirates and the
environment.

This month, sprites were added for basic character poses, as well as basic sound effects, making the game come alive and feel more like a proper 2D platformer.

Support for [ bevy_ggrs](https://github.com/gschup/bevy_ggrs)’ synctest sessions was implemented. This
allows detecting de-syncs by constantly performing rollbacks and comparing world
state checksums). This caught some very rare de-sync bugs.

The game also adopted [Matchbox](https://github.com/johanhelsing/matchbox)’s newly added support for
cross-platform p2p. This means sessions between players on web and native are
now supported ([video](https://mastodon.social/@johanhelsing/109681997649114818)).

All of this is discussed in detail in the [third devlog
entry](https://johanhelsing.studio/posts/cargo-space-devlog-3).

Johan also wrote [an article](https://johanhelsing.studio/posts/cargo-space-devlog-4) on how sound effects were
implemented in a rollback-aware way, canceling mispredicted sounds, and handling
“late” sounds. It describes a solution that could easily be adopted for any game
made with [ bevy_ggrs](https://github.com/gschup/bevy_ggrs).

![Screenshot of a tree emerging from a cave in Idu](../../assets/a87ecabaac6a6d50.jpg)

[Idu](https://epcc.itch.io/idu) ([Discord](https://discord.gg/MeGauteMj3)) Idu is a strategic sandbox game about growing
plants that wish to reclaim nature, developed by [Elina
Shakhnovich](https://mastodon.gamedev.place/@eli) and [Johann Tael](https://mastodon.gamedev.place/@johann) featuring a
bespoke Vulkan-based engine in Rust.

After almost a whole year of relative silence, they have begun releasing new demos in January. The new demo version 8 comes with a new renderer supporting interactive, flowing water. Also, the simulated trees in Idu changed a lot, as they’re now able to flower, in addition to dropping leaves. The new demo features a lot of new plant textures, branching logic, and better rhizome and root simulation.

Player accessibility and the gameplay itself is better now as well, due to a completely new menu and a lot of new items, such as porous gabion blocks and ladders.

Read more and download the newest demo from [Idu’s page on itch.io](https://epcc.itch.io/idu).

![A river with flora and fauna](../../assets/da46f6cacd3ab097.jpg)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In January, Veloren released version 0.14! This update included trading with
pets, musical instrument crafting, the Sea Chapel, and many more changes. You
can read all about that update in the [release post](https://veloren.net/release-0-14/).

Veloren’s Site2 system can now be hot-reloaded. Site2 allows you to describe
procedures for how objects like houses, trees, or bridges should be generated.
Hot-reloading allows you to change the Site2 code and watch the changes take
effect in real-time. The official 2023 Veloren OST was also released, and can be
[watched on YouTube](https://www.youtube.com/watch?v=yNxxCwwKyes).

January’s full weekly devlogs: “This Week In Veloren…”: [#204](https://veloren.net/devblog-204).

## Engine Updates [#](https://gamedev.rs#engine-updates)

![Particle System Preview](../../assets/4dda16447db1c451.gif)


[Fyrox](https://github.com/FyroxEngine/Fyrox) ([Discord](https://discord.com/invite/xENF5Uh), [Twitter](https://twitter.com/DmitryNStepanov)) is a game engine
that aims to be easy to use and provide a large set of out-of-the-box features.
In January it hit version 0.29 and got the following features:

- Animation system rework
- Animation editor
- Animation blending state machine editor rework
- Sprite sheet editor
- Ability to change scene settings
- Improved WebAssembly support
- Customizable graph update pipeline
- Node and property selector widgets
- Message passing for scripts
- Reflection refactoring to support interior mutability
- Deterministic particle systems
- Ability to animate material properties
- Various bug fixes

You can read more about the changes in the [feature highlights
post](https://fyrox.rs/blog/post/feature-highlights-0-29/).

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

![Title card: Introduction to the Entity Component System](../../assets/6abbef5f5a792870.png)


[@indiedevcasts](https://twitter.com/indiedevcasts) published [a new blog post](https://indiedevcasts.com/posts/ecs-introduction), exploring
object-oriented and data-oriented designs before giving an introduction to the
Entity Component System paradigm.

## Tooling Updates [#](https://gamedev.rs#tooling-updates)

![Foxtrot in action](../../assets/34d0de11836970f0.gif)


[Foxtrot](https://github.com/janhohenheim/foxtrot) was created by Jan Hohenheim ([@janhohenheim](https://github.com/janhohenheim)) as an all-in-one
starting point for 3D projects made in Bevy. While he appreciated that other
Bevy templates showed nicely how to wire up systems and setup a game loop, he
was missing a showcase for commonly used features that are scattered around
various libraries. So he created Foxtrot, where he collected the most basic
features he could need for future projects or jams. The [latest release](https://github.com/janhohenheim/foxtrot/releases/latest)
features:

- loading a 3D level from GLTF files
- automatically assigning physics colliders
- a custom dialog system
- saving and loading the game
- a force-based third-person character controller
- shaders
- pathfinding
- a flexible camera system with easings supporting various perspectives
- a custom in-game editor window for live tweaks such as spawning new objects.

![Graphite logo](../../assets/f6cbee2983b2b262.png)


Graphite ([website](https://graphite.rs), [GitHub](https://github.com/GraphiteEditor/Graphite),
[Discord](https://discord.graphite.rs), [Twitter](https://twitter.com/GraphiteEditor)) is a free,
in-development raster and vector 2D graphics editor based around a Rust-powered
node graph compositing engine.

New features from January’s [sprint 22](https://github.com/GraphiteEditor/Graphite/milestone/22):

- Picture this: Imported images are now part of the node graph. The new
*Image Frame*node converts bitmap data into a vector rectangle holding the image. This paves the way for other vector data like shapes and text to soon be converted into nodes and composited alongside images. - Instant iterations: Incremental graph compilation avoids recompiling the whole graph each time an edit is made or a value changes. This makes iteration faster and enables caching of intermediate computations for faster rendering.

And soon, the Alpha Milestone 2 release will launch with new node graph
features, a revamped website, and a wider-reaching project announcement. Join
the [newsletter](https://graphite.rs/#newsletter) and stay tuned.

[Open Graphite](https://editor.graphite.rs) in your browser and start creating! Share your
designs with #MadeWithGraphite on Twitter.

## Library Updates [#](https://gamedev.rs#library-updates)

[big-brain](https://crates.io/crates/big-brain) ([GitHub](https://github.com/zkat/big-brain), [Discord](https://discord.com/channels/691052431525675048/829441190067306596)) by
[@zkat](https://github.com/zkat) is a highly parallel [Utility AI](https://en.wikipedia.org/wiki/Utility_system) library for the
Bevy game engine.

[big-brain](https://crates.io/crates/big-brain) recently tagged [v0.16.0](https://github.com/zkat/big-brain/releases/tag/v0.16.0), bringing with it a couple
of breaking changes and a few goodies.

Probably the biggest change in this release is the removal of the blanket
[ ActionBuilder](https://docs.rs/big-brain/0.16.0/big_brain/actions/trait.ActionBuilder.html) and

[implementations for](https://docs.rs/big-brain/0.16.0/big_brain/scorers/trait.ScorerBuilder.html)

`ScorerBuilder`

`Clone`

types.
This is a fairly significant breaking change, but one that is fairly easy to
resolve: simply use the new `#[derive(ActionBuilder)]`

and
`#[derive(ScorerBuilder)]`

macros to derive the necessary implementations for
your Action and Scorer Components and you should be good to go.Finally, since the recent [merging of the bevy scheduler
changes](https://tech.lgbt/@alice_i_cecile/109815432105482093), big-brain users should expect the
next version of big-brain to bring with it some significant breaking changes to
scheduling, so keep an eye out for that and be mindful of building a lot on top
of the current [ BigBrainStage](https://docs.rs/big-brain/0.16.0/big_brain/enum.BigBrainStage.html) (which is used by the default

`BigBrainPlugin`

).*Discussions: Mastodon*



![Waveform displayed on a screen](../../assets/bc8363da62ad265e.png)

[RustySynth](https://github.com/sinshu/rustysynth) is a SoundFont MIDI synthesizer written in pure Rust. The purpose
of this library is to provide MIDI music playback functionality for any Rust
application without complicated dependencies. The code base is lightweight and
can be used with any audio driver that supports streaming audio (e.g.
[rust-sfml](https://github.com/jeremyletang/rust-sfml)).

Features:

- Tuned mainly for gamedev and has low CPU usage.
- Support for standard MIDI files.
- No dependencies other than the standard library.
- Available under a permissive license (MIT).

`tween`

is a library for manipulating values in stylish and beautiful ways. It
has been almost entirely rewritten for `v2.0.0`

, now featuring a significantly
improved API, fewer generics, and much, much faster performance.

Additionally, it has added support for Looping, Oscillating, and Extrapolating tweens. With all of this, making custom tweens is much easier. An example of making a Bezier tween is included.

`scene-graph`

is a library for creating graph structures similar to the one used
in engines like Unity or Unreal. It is fast, performant, and easy to manipulate.
It’s especially useful for user interfaces. Although only in `v0.1.0`

, feedback
would be very appreciated.

![Torchbearer in action](../../assets/d0088a6a6fec4042.png)

[torchbearer](https://github.com/redwarp/torchbearer) by [@redwarp](https://github.com/redwarp) is a library that provides a set of tools to find
your path in a grid-based dungeon. Specifically, it provides a quick
implementation of pathfinding and field of view algorithm.

The 0.6.x version rewrites the field of view algorithm to cast vision rays in a
Bresenham circle around the point of origin. This change from its [original
implementation](https://sites.google.com/site/jicenospam/visibilitydetermination) makes it faster as it removes the needs for
error correction.

![matchbox logo](../../assets/5571fd47724561dd.png)


[Matchbox](https://github.com/johanhelsing/matchbox) is a library for easily establishing unreliable, unordered,
peer-to-peer WebRTC data connections using rust WASM. This enables low-latency
multiplayer browser games.

Originally, it was written for web assembly, but a native implementation using
[WebRTC.rs](https://webrtc.rs) has been available since 0.4. However, a few minor incompatibilities
between the two implementations meant connections between native and web were
not possible.

In version 0.5, however, [Alex Rozgo](https://github.com/rozgo) fixed the last of these issues. And
cross-play sessions are now finally fully supported.

In addition, [johanhelsing](https://mastodon.social/@johanhelsing) fixed a serious bug that used
to cause disconnections on recent versions of Firefox.

The tutorial series on [how to make a p2p web game with Bevy, GGRS and
Matchbox](https://johanhelsing.studio/posts/extreme-bevy) was also updated to the latest versions of all three
libraries.

*Discussions: Mastodon*

![miniquad ios](../../assets/8df8ccdb357ff6e6.gif)

[miniquad](https://github.com/not-fl3/miniquad) is a safe and cross-platform rendering library focused on portability
and low-end platform support.

This month metal backend [PR](https://github.com/not-fl3/miniquad/pull/344) finally landed on miniquad!

It is not yet ready for any production use, but it is available on crates.io as 0.4.0-alpha.

With this change, miniquad support webgl1, gl2, gles2/gles3, gl3+, metal on web, macOS, iOS, Android, Windows, and Linux.

## Other News [#](https://gamedev.rs#other-news)

- Other game updates:
[Hydrofoil](https://twitter.com/HydrofoilG)is getting closer to their February release date.- Tiny Glade now
[has terrain modification](https://twitter.com/anastasiaopara/status/1617925842163863554). - Thetawave now
[has a functional boss enemy](https://twitter.com/carlosupina/status/1611808954455146498). - 8bit Duels is just released their
[fifth devlog](https://reddit.com/r/rust_gamedev/comments/102kwgf/8bit_duels_devlog_part_5). - Combine And Conquer just released
[version 0.4.0](https://buckmartin.de/combine-and-conquer/2023-01-14-v0.4.0.html). - Your Only Move is Hustle is now available on Steam.
- TheGrimsey write a devblog
[“Magic Missiles & the Registries”](https://twitter.com/TheGrimsey/status/1615788141314510848). - Flesh has a
[new redrawn background in the first area](https://twitter.com/Im_Oab/status/1616542479951724546), and has[been tested to run on the Steam Deck](https://twitter.com/Im_Oab/status/1619230923970736128). [DGS](https://reddit.com/r/rust_gamedev/comments/10ifm62/dgs_the_multiplayer_game_of_go)is a multiplayer game of Go, with spherical fields and VR support.- Triverse has a
[set of devlogs out](https://cragwind.itch.io/triverse/devlog), with the most recent covering[scenarios and playability](https://cragwind.itch.io/triverse/devlog/485898/scenarios-and-playability). - Fish Folk: Punchy has
[released version 0.3](https://reddit.com/r/rust_gamedev/comments/10qwgcn/fish_folk_punchy_v03). - Life Code has
[a new video](https://twitter.com/LifeCodeGame/status/1611856359003426816)explaining how the diet selection tool works. - Digg is a new game being made with Bevy, and has
[a devlog](https://reddit.com/r/rust_gamedev/comments/10of2sz/creating_a_new_game_with_bevy)that walks through the first two weeks of development. [Revolver Time](https://allocatedartist.itch.io/revolver-time)is a game made in 1 week with Godot and Rust, and has[a video](https://youtube.com/watch?v=LNcGzn7ZsNI)explaining how it was made.[Canal Mania](https://lee-orr.itch.io/canal-mania)is a game created for the Historically Accurate Game Jam.


- Other learning material updates:
[Native iOS Touch Events w/ Rust](https://itnext.io/rust-native-ios-touch-events-8b01418e0f3b)is a tutorial on how to use Rust to create native iOS touch events.[Bevy Basics video series](https://youtube.com/playlist?list=PL6uRoaCCw7GN_lJxpKS3j-KXuThRiSXc6)is a series of videos that covers the basics of Bevy.[Platformer in Bevy video series](https://youtube.com/playlist?list=PL6uRoaCCw7GN_lJxpKS3j-KXuThRiSXc6)is a series of videos that covers how to make a platformer in Bevy.


- Other engine updates:
[alkahest-rs](https://twitter.com/alkimia_studios/status/1610802953828405248)released put about a video about[implementing texture batching](https://www.youtube.com/watch?v=quoHV9HHHJA).[godot-rust](https://twitter.com/GodotRust/status/1615606253052362752)saw large improvements to the Godot 3 bindings.[petrichor64](https://makeavoy.itch.io/petrichor64)is a retro-inspired small 3D fantasy engine.


- Other tooling updates:
[Ten Minute Physics](https://reddit.com/r/rust/comments/10l4ae5/ten_minute_physics_demos_in_rust_with_wasm_webgl)is a reimplementation of Matthias Müller’s “Ten Minute Physics” demos in Rust with WASM + WebGL.[rgis](https://github.com/frewsxcv/rgis)is a geospatial data viewer written in Rust.


- Other tooling updates:
[wgpu v0.15, naga v0.11](https://reddit.com/r/rust/comments/10lf10i/wgpu_015_and_naga_011)were released.[raster_fonts](https://reddit.com/r/rust_gamedev/comments/100vmqq/announcing_font2img_and_raster_fonts), a library for deserializing the resulting metadata, was announced.[nvtt](https://reddit.com/r/rust_gamedev/comments/10eq1uh/nvtt_rs_has_been_updated_to_use_nvidia_texture)has been updated to use Nvidia Texture Tools 3.[oxidized_navigation](https://twitter.com/TheGrimsey/status/1615063433367494656)is a nav-mesh generation & pathfinding crate to use with Bevy.[VPlugin](https://github.com/VPlugin/VPlugin)is a Rust framework to develop and use plugins within your project, without worrying about the low-level details.[egui_glium](https://twitter.com/ernerfeldt/status/1621811309284130816)is looking for a new maintainer.[direct-storage](https://github.com/Tsukisoft/direct-storage-rs)provides Rust bindings for DirectStorage.[bones](https://reddit.com/r/rust_gamedev/comments/10j74lt/bones)is a work-in-progress, opinionated game framework built on Bevy.[airsim-client](https://reddit.com/r/rust_gamedev/comments/10ij9lv/airsimclient)is a Rust client library for interacting with Microsoft Airsim.[Rapier](https://dimforge.com/blog/2023/01/22/the-year-2022-in-dimforge)wrote a year in review for 2022, and took a look ahead to 2023.[bevy-magic-light-2d](https://github.com/zaycev/bevy-magic-light-2d)is an experimental dynamic 2D global illumination system for Bevy, based on SDF ray-marching and screen space irradiance cache probes.[notan v0.9](https://reddit.com/r/rust/comments/10pwgka/released_a_new_version_of_notan_a_sdllike_lib)was released.


## Discussions [#](https://gamedev.rs#discussions)

- /r/rust_gamedev:

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[‘Are We Game Yet?’ wants to know about projects/games/resources that aren’t listed yet](https://github.com/rust-gamedev/arewegameyet#contribute).[Graphite is looking for contributors](https://graphite.rs/contribute)to help build the new node graph and 2D rendering systems.[winit’s “difficulty: easy” issues](https://github.com/rust-windowing/winit/issues?q=is%3Aopen+is%3Aissue+label%3A%22difficulty%3A+easy%22).[Backroll-rs, a new networking library](https://github.com/HouraiTeahouse/backroll-rs/issues).[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[A/B Street’s “good first issue” issues](https://github.com/a-b-street/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/D-Good-First-Issue).

## Jobs [#](https://gamedev.rs#jobs)

[Ambient](https://www.ambient.run/career)(Remote)- Engine Programmer
- Rendering Engineer
- Open Source Community Engineer

[Embark Studios](https://careers.embark-studios.com/jobs)(Stockholm/Hybrid Remote)- Various roles


That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!

**Discuss this post on**:
[/r/rust_gamedev](https://www.reddit.com/r/rust_gamedev/comments/11cpysa/this_month_in_rust_gamedev_42),
[Twitter](https://twitter.com/rust_gamedev/status/1629925295376441345),
[Mastodon](https://mastodon.gamedev.place/@rust_gamedev/109932672837603113),
[Discord](https://discord.gg/yNtPTb2).