---
title: 'This Month in Rust GameDev #38 - September 2022'
url: https://gamedev.rs/news/038/
author: Rust GameDev WG
published: '2022-10-14'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 38th issue of the Rust GameDev Workgroup’s
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

[Announcements](https://gamedev.rs/news/038/#announcements)[Game Updates](https://gamedev.rs/news/038/#game-updates)[Engine Updates](https://gamedev.rs/news/038/#engine-updates)[Learning Material Updates](https://gamedev.rs/news/038/#learning-material-updates)[Tooling Updates](https://gamedev.rs/news/038/#tooling-updates)[Library Updates](https://gamedev.rs/news/038/#library-updates)[Other News](https://gamedev.rs/news/038/#other-news)[Popular Workgroup Issues in GitHub](https://gamedev.rs/news/038/#popular-workgroup-issues-in-github)[Discussions](https://gamedev.rs/news/038/#discussions)[Requests for Contribution](https://gamedev.rs/news/038/#requests-for-contribution)[Bonus](https://gamedev.rs/news/038/#bonus)

## Announcements [#](https://gamedev.rs#announcements)

### Rust GameDev Meetup [#](https://gamedev.rs#rust-gamedev-meetup)

![Gamedev meetup poster](../../assets/96543a96aff6db81.png)


The 20th Rust Gamedev Meetup took place in September. You can watch the recording
of the meetup [here on Youtube](https://www.youtube.com/watch?v=QKqqDilZ448).

The meetups take place on the second Saturday every month via the [Rust Gamedev
Discord server](https://discord.gg/yNtPTb2) and are also [streamed on
Twitch](https://twitch.tv/rustgamedev).

## Game Updates [#](https://gamedev.rs#game-updates)

![building and fighting](../../assets/56907592e5c1c48f.gif)

CyberGate ([YouTube](https://youtube.com/channel/UClrsOso3Xk2vBWqcsHC3Z4Q), [Discord](https://discord.gg/R7DkHqw7zJ)) by CyberSoul
is an attempt to use artificial intelligence to build diverse universe experiences
with strange creatures and procedural gameplay styles.
Currently in Phase 5.2 (analogously version 0.5.2),
they finalized a playable game with the tech they have developed up until now.

Recent updates:

- In-house Transport layer with Reliability and Package aggregation, over WebRTC
- Implemented Winit background process on all browsers
- Introduced Grabbing and Building Mechanics
- Created enemy AI that groups and flies in colonies. Includes a deadly night mode
- Usernames and life points with Fontdue.rs
- Menu and leaderboard using yakui.rs
- Improved the Automation to push Server Updates
- Improved wasm related performance, latency, and connection freezing bugs.

[Join the Discord server](https://discord.gg/R7DkHqw7zJ) to participate in upcoming Phase 6.0!

*Discussions: /r/rust_gamedev*

![Graviton](../../assets/d7c9f44e84bd1b8e.png)

[Graviton](https://www.gravitongame.art/) by
[@hakolao](https://github.com/hakolao)
is a relaxing simulation game in which you draw colored sand and watch it
interact with gravity.

The game is going to be released in early access on
[Steam](https://store.steampowered.com/app/2137280/Graviton__A_Relaxing_Sand_Simulation/?utm_source=rust_gamedev&utm_medium=web)
during this October.

*Discussions: /r/rust_gamedev*

### Flesh [#](https://gamedev.rs#flesh)

![flesh preview](../../assets/5f81d94c8a7d0e3f.gif)

[Flesh](https://store.steampowered.com/app/1660850/Flesh/) by [@im_oab](https://twitter.com/im_oab) is a 2D-horizontal shmup game with hand-drawn animation and
an organic/fleshy theme. It is implemented using [Tetra](https://github.com/17cupsofcoffee/tetra). This month’s updates
include:

- Finishing up the last area of the game.
- Making animation of the game’s intro/ending.

### Thetawave [#](https://gamedev.rs#thetawave)

![thetawave-boss](../../assets/7677311aed3c48eb.gif)

Thetawave is a physics based, cosmic horror themed space shooter by
[@carlosupina](https://twitter.com/carlosupina).
In the past month, work has begun on the first boss enemy in the game,
the [Repeater](https://twitter.com/carlosupina/status/1572976552165474307).

Thetawave has also joined the [@spicylobsterfam](https://twitter.com/spicylobsterfam) incubator.
Feel free to reach out to the developer
if you are interested in contributing!

![Ultimechs - let the games begin](../../assets/3a0bc96a42373752.png)


[Ultimechs](https://www.resolutiongames.com/ultimechs)
([Discord](https://discord.com/invite/srX92DRt9G),
[Twitter](https://twitter.com/ultimechs),
[Facebook](https://www.facebook.com/Ultimechs/),
[Reddit](https://www.reddit.com/r/Ultimechs/),
[YouTube](https://www.youtube.com/channel/UC6t6delBJRxnaBcqBPpC3Gg))
by [Resolution Games](https://www.resolutiongames.com)
is a future sports game played with mechs.
It is VR, multiplayer, and free to play.

Ultimechs is partially written in Rust.
The Rust code is for the core of the game, including the game rules,
networking, and physics (that use [Rapier](https://www.rapier.rs/)).
The rest of the game, including the graphics, audio, user input,
and everything that happens outside the arena,
is made in [Unity](https://unity.com/).

The game was released on the 15th of September
on the [Meta Quest 2](https://www.oculus.com/experiences/quest/5118731164870081/) and [SteamVR](https://store.steampowered.com/app/1657780/Ultimechs/).

There is [a conference talk](https://www.youtube.com/watch?v=nLCNsIs1-ZU)
and [a blog post](https://www.resolutiongames.com/blog/programming-a-vr-game-using-rust)
about the choice of Rust and how they combined Rust with the studio’s
standard tools Unity and C#.
[Another blog post](https://www.resolutiongames.com/blog/calling-rust-from-c-in-unity)
goes into more depth about calling Rust code from C# in Unity.

[eo-rs](https://eo-rs.dev) by [@sorokya](https://github.com/sorokya)
is a development library and game server for the MMORPG
[Endless Online](https://www.endless-online.com).

Recent updates:

- Made NPCs appear and move around in the game world
- Created a proxy tool to document interactions between the original client and server
- Implemented player stat calculations
- Made NPCs talk

### Tiny Building Game [#](https://gamedev.rs#tiny-building-game)

![Tiny_building_game_gif](../../assets/8dbfe55a0d15107e.gif)


The untitled “Tiny Building Game” is a stress-free feel-good game focused on just
building something pretty. It is being made by [@anastasiaopara](https://twitter.com/anastasiaopara) and
[@h3r2tic](https://twitter.com/h3r2tic).

This month, the team welcomed [Martin](https://twitter.com/MartinKvale) (sound design) and [Oda](https://twitter.com/OdaTilset) (music) as well as
adding various game elements, such as fences, gates, pillars and [butterflies](https://twitter.com/h3r2tic/status/1573747327751360512). You
can watch this short [YouTube video](https://youtu.be/CizG3hv7DhQ) to catch a glimpse of how it’s all coming together.

Right now, the team is working towards the game announcement. Stay
tuned by following the [newsletter](https://dashboard.mailerlite.com/forms/10395/51067704544593017/share)!

![Riding into the sunset](../../assets/1798ec46f9861bc9.jpg)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In September the official Veloren server saw a new all time high of more than 400 players logged in at the same time, with an average load of 200 players. This caused slow in-game responses and the development team quickly optimized to reduce the server load and introduced a new graphical server browser for balancing.

Due to the more diverse user base, a lot of languages received translation updates. The most common crash dialog was improved to suggest the workaround of trying a different graphics backend, while the large number of players still using DX11 block an upgrade to a more recent WGPU version.

Septembers’s full weekly devlogs: “This Week In Veloren…”:
[#188](https://veloren.net/devblog-188),
[#189](https://veloren.net/devblog-189),
[#190](https://veloren.net/devblog-190).

![Escape the hotel](../../assets/5f32d6cf0ce5c1f8.png)

[Subfuse](https://dgriffin.itch.io/subfuse) is a short 1st person puzzle/escape game made for
[Bevy Jam #2](https://itch.io/jam/bevy-jam-2) with an accompanying [postmortem](https://dgriffin.itch.io/subfuse/devlog/422315/subfuse-postmortem)
that goes into some detail about the process of making the game.

## Engine Updates [#](https://gamedev.rs#engine-updates)

![godot-rust new export syntax](../../assets/9ae3cc752f9344a1.png)

`#[method]`

syntax, which replaces existing `#[export]`

and allows omitting
the base parameter.godot-rust ([GitHub](https://github.com/godot-rust/godot-rust), [Discord](https://discord.gg/aKUCJ8rJsc), [Twitter](https://twitter.com/GodotRust))
is a Rust library that provides bindings for the Godot engine.
In September, development was divided into three tasks:

- Maintenance releases
[0.10.1](https://github.com/godot-rust/godot-rust/pulls?q=is%3Apr+milestone%3Av0.10.1)and[0.10.2](https://github.com/godot-rust/godot-rust/pulls?q=is%3Apr+milestone%3Av0.10.2) - Godot 3.5 support in v0.11 (
[#910](https://github.com/godot-rust/godot-rust/issues/910)) - Ongoing
[GDExtension](https://godotengine.org/article/introducing-gd-extensions)efforts ([#824](https://github.com/godot-rust/godot-rust/issues/824))

Besides support for Godot 3.5.1, a change that many users will notice is the
new `#[method]`

+ `#[base]`

syntax, replacing `#[export]`

as illustrated above.

The GDExtension/Rust binding has finally reached a state where a first experimental version is within reach in October. If you are fine with the bugs and missing features, you can give it a try very soon!

![Gamercade preview](../../assets/ab7431b512ab6dda.gif)

[Gamercade](https://gamercade.io) ([Discord](https://discord.gg/Qafv2Fpt5j), [GitHub](https://github.com/gamercade-io/gamercade_console))
by @RobDavenport is a WASM-powered fantasy console focused
on building multiplayer neo-retro games.

Gamercade has launched their first official release! Version `0.1.0`

has
all of the functions and features need to start building awesome single-
and multi-player games: input, graphics, audo, networking, and more.
[The full release article](https://gamercade.io/blog/gamercade-0-1-0) goes into higher detail about
the feature set of Gamercade, and includes example images and animations.

Full controller support made it into the `0.1.0`

release, including analog
sticks, analog triggers, as well as emulation of those for those without
a game pad. Additionally, they added a command line tool, called `gccl`

which
streamlines many of the pain points in developing Gamercade games. A number of
quality-of-life and bug fixes also made it into the release.

The team is already planning out their feature set for the next release, `0.2.0`

,
which is based around the theme of “two.” The next release will include more
multiplayer features like two or more local players, two or more networked instances,
stereo sound support, and much more.

Come hang out and chat on [Discord](https://discord.gg/Qafv2Fpt5j), where the developers
interact with members and post updates daily. The project is
[open source](https://github.com/gamercade-io/gamercade_console) and looking for contributors, suggestions,
as well as your awesome game creations.

![A short video of changing the speed of the day/night cycle from Dims script parameters](../../assets/abd37052b29a8c9e.gif)


[Dims](https://dims.co) ([Twitter](https://twitter.com/DimsWorlds), [Discord](https://discord.gg/Z5CAVmNE57),
[YouTube](https://youtube.com/channel/UCR5gOwS7uSl0a0dl7MLQoqg)) is a pre-alpha collaborative open-world
creation platform.
Users can hop in sessions and build a game together, allowing everyone
to bring out their inner game-maker.

In September, the platform continued to make steady progress, with new features and bugfixes being made on a daily basis. The highlights are:

- The team’s very first game of entirely scripted multiplayer Team Deathmatch 🎉
- All player logic was moved to the Rust scripting layer, allowing for it to be changed on the fly
- The implementation of animation retargeting, so you can use any animation with any model, as long as they share the same skeletal structure
- Scripting now has greater access to the ECS, allowing it to move the sun 🌅
- Initial work on an asset database and pipeline, so that you can import any asset and use it amongst your Dims projects
- An all-new object manipulation/placement tool suite
- Objects can now be consistently stacked, moved as a group, placed within each other, and more!

- Many other infrastructural changes and improvements, including macOS and Linux builds

Want to try Dims out for yourself? Come join the [Discord](https://discord.gg/Z5CAVmNE57) to be
notified of future public tests, see the latest features before everyone else,
and to talk to the devs personally.

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

![A screenshot of the tic tac toe clone the tutorial covers](../../assets/13a9895b7911555d.png)


@herluf-ba published a beginner friendly [3 part tutorial series](https://herluf-ba.github.io/making-a-turn-based-multiplayer-game-in-rust-01-whats-a-turn-based-game-anyway.html)
about making turn-based multiplayer games using rust.
It covers what games can be considered “turn-based”,
how to write a simple but neat game server using [renet](https://github.com/lucaspoffo/renet),
and finally how to tie it all together with a client app made with [bevy](https://github.com/bevyengine/bevy).

![monthly videos](../../assets/f7abb1594d3b982e.jpeg)


[@chrisbiscardi](https://twitter.com/chrisbiscardi) publishes a Rust video every day each
month on [YouTube](https://www.youtube.com/c/chrisbiscardi).

This month started off with a [low-level WGPU series](https://www.youtube.com/playlist?list=PLWtPciJ1UMuBs_3G-jFrMJnM5ZMKgl37H)
that focuses on WGPU APIs as a primitive to understand
Bevy’s renderer. Moving forward with that, he explored
[debugging shaders with RenderDoc](https://www.youtube.com/watch?v=vblsZgBcgyw),
[porting shaders](https://www.youtube.com/watch?v=ynLEQVPRfZs) from Blender to Bevy,
[generating custom meshes](https://www.youtube.com/watch?v=s0xY4muPwj8) and interesting
types of [noise](https://www.youtube.com/watch?v=An2GMk8URMo).

At a higher level, Chris covered a comparison between
[Bevy and Nannou](https://www.youtube.com/watch?v=Cf08TlwUNf4) for creative coding
endeavours and the top 10 games from [Bevy Game Jam #2](https://www.youtube.com/watch?v=VBMzaMEOhFI).
He also put (more than) [1 million particles](https://www.youtube.com/watch?v=MWIO-jP6pVo)
inside of a Bevy app, and continued working on a
[2D platformer implementation](https://www.youtube.com/watch?v=VWzqmquIZHc&t=2s).

## Tooling Updates [#](https://gamedev.rs#tooling-updates)

### Feldversuch [#](https://gamedev.rs#feldversuch)

![Feldversuch](../../assets/b84d286f5dea467f.gif)


Feldversuch by [@siebencorgie](https://twitter.com/siebencorgie)
is an experimental extension to the class of wavetable
synthesizers based on signed distance fields.

Feldversuch uses user defined fields not only to render the
interface, but to generate sound based on them as well. The
so-called *sampling plane* (seen moving back and forth above)
defines the wave shape that is played back.

Further experiments include rotation (instead of the sweep
movement) as well as different interpretations of the wave
shape. Have a look at the [presentation video](https://www.youtube.com/watch?v=GZVdzcwSEaw)
and the [blog post](https://siebencorgie.rs/gallery/feldversuch/)
for further details.

## Library Updates [#](https://gamedev.rs#library-updates)

### bevy_oddio [#](https://gamedev.rs#bevy-oddio)

![an example using bevy_oddio](../../assets/fcab5c1d87e0c5d7.png)

[bevy_oddio](https://github.com/harudagondi/bevy_oddio) by [@harudagondi](https://twitter.com/harudagondi) is an audio plugin
for the [Bevy](https://github.com/bevyengine/bevy) game engine that uses the [oddio](https://github.com/Ralith/oddio) library.
It aims to allow first class support of non-static audio sources
like procedurally generated audio.
The library also aims to have a high amount of flexibility
in controlling custom audio sources where typical audio sink methods
would not suffice.

The previous month saw a new [0.2.0](https://github.com/harudagondi/bevy_oddio/releases/tag/v0.2.0) release which
irons out some bugs and added new ergonomic features to allow a
better user experience. There is now added support for `Mono`

and `Stereo`

audio sources, support for more [oddio](https://github.com/Ralith/oddio)
types, a new example for controlling volume, and much more.
A lot of the APIs have been reworked to make it more flexible
and some public items were deleted to reduce redundancy.

The above screen shows an example of controlling a custom made audio source
([taken from here](https://github.com/harudagondi/bevy_fundsp/blob/ca08963820c83dd723784db6c6f87df8eadd60e0/examples/oddio/controlled.rs#L40-L52)) by calling the .control() method.

![showcase using the demo](../../assets/6edc33202fd875ad.gif)

[demo](https://canleskis.github.io/bevy-particular-demo/)

[Particular](https://github.com/Canleskis/particular) by [@Canleskis](https://github.com/Canleskis) is a library allowing for simulations of
N-body gravitational interaction of particles. It aims to be simple
to integrate in existing game and physics engines, such as [Bevy](https://github.com/bevyengine/bevy) or [Rapier](https://www.rapier.rs/).
See the [demo source code](https://github.com/Canleskis/bevy-particular-demo/blob/main/src/nbody.rs) for the example of an integration (less than 50
actual lines of code!).
The [demo](https://canleskis.github.io/bevy-particular-demo/) is available on the browser (Chromium-based recommended)
with various scenes you can interact with.

Particular can be used with [rayon](https://github.com/rayon-rs/rayon) to leverage multithreading on the
CPU (`parallel`

feature). Although the current algorithm performs well enough
for most use cases, with a single frame taking around 5 ms with 5000 particles
on an I9 9900K, future updates will introduce other implementations to allow for
faster computation of the forces (example: [Barnes-Hut](https://en.wikipedia.org/wiki/Barnes%E2%80%93Hut_simulation)).

You can find more about Particular with
[this video](https://www.youtube.com/watch?v=oFrq9ckHoN8&) from
[@ChristopherBiscardi](https://github.com/ChristopherBiscardi), or
[this post](https://www.reddit.com/r/rust/comments/x7uhoq/media_particular_a_simple_library_for_nbody/)
on Reddit.

![notan examples](../../assets/faaf944fdff621b5.gif)


[Notan](https://github.com/Nazariglez/notan) is a simple and portable layer designed to create your own
apps on top of it without worrying about platform-specific code.

It provides a set of APIs and tools that can be used to create your project in an ergonomic manner without enforcing any structure or pattern, sharing the same codebase across multiple platforms.

The focus of version [v0.7](https://github.com/Nazariglez/notan/releases) was improvements and fixes, however the main
improvement was how textures are created, allowing to create textures that
depend on the backend. The main benefit of this new feature is that Notan
can now load on browsers to the GPU `HtmlImageElement`

or it could load
other types of browser’s images as well (like `HtmlCanvasElement`

).

![example of pathfinding](../../assets/f73403b545c97176.gif)

[demo](https://vleue.github.io/bevy_pathmesh/)

[Polyanya](https://github.com/vleue/polyanya) by [@FrancoisMockers](https://twitter.com/FrancoisMockers) is a library implementing
[Polyanya](https://www.ijcai.org/proceedings/2017/0070.pdf), a Compromise-free Pathfinding algorithm on a
Navigation Mesh. It is currently the fastest known optimal online any angle
path planning algorithm. Unlike A*, any angle path planning techniques are not
bound to a grid and will find a taut path.

An integration with [Bevy](https://github.com/bevyengine/bevy) is on-going, with a [few examples](https://vleue.github.io/bevy_pathmesh/)
available in WASM. Next area of work will be around navigation mesh editing.

## Popular Workgroup Issues in GitHub [#](https://gamedev.rs#popular-workgroup-issues-in-github)

## Other News [#](https://gamedev.rs#other-news)

- Other game updates:
[Disk-0 Madness](https://maxcurzi.itch.io/disk-0-madness)is a bullet hell game, written in Rust for the WASM-4 fantasy console.[Combine and Conquer](https://buckmartin.de/combine-and-conquer/2022-09-23-v0.1.0.html)released version 0.1, moving into early access.[bevy-rapier-car-sim](https://github.com/alexichepura/bevy-rapier-car-sim)is a 3D car simulation in Rust.[PongRust](https://larsdu.github.io/PongRust/)is an ‘unbeatable’ Pong game.[My Roguelite](https://ostwilkens.github.io/my-roguelite/)is a browser-based 3D roguelite.[Life Code](https://www.youtube.com/watch?v=ftVkklmO1Dk)is an ecosystem simulation game.[Klod](https://devildahu.ch/devlog/making-of-klod-tech/)released a retrospective post about their Katamari-inspired platformer.

- Other engine updates:
[Rustacean Station](https://rustacean-station.org/episode/dmitry-stepanov/)interviewed the developer of the Fyrox engine.[The Fyrox Book](https://fyrox-book.github.io/fyrox/scene/inheritance.html)added a new chapter on property inheritance.[Bevy’s scheduling overhaul RFC](https://github.com/bevyengine/rfcs/pull/45)was merged.

- Other learning material updates:
[LogRocket](https://blog.logrocket.com/rust-bevy-entity-component-system)posted about Bevy’s ECS API.[Wade Zimmerman](https://devmap.org/native-ios-game-development-w-rust-a1134887c35f)wrote about their native iOS game dev journey with Rust.[Rust and Tell](https://www.youtube.com/watch?v=-UUImyqX8j0)featured a talk on hot reloading.[Bevy Basics](https://www.youtube.com/playlist?list=PL6uRoaCCw7GN_lJxpKS3j-KXuThRiSXc6)continued their series of beginner Bevy tutorials.[Yishn](https://www.youtube.com/watch?v=QCys49c44PU)coded an Astroids clone with Bevy.

- Other library updates:
[big-brain](https://github.com/zkat/big-brain/releases/tag/v0.14.0)released version 0.14 of its Utility AI library, with fixes and lots more observability improvements.[egui_dock](https://crates.io/crates/egui_dock)adds docking support to egui.[Valence](https://github.com/valence-rs/valence)is a framework for building Minecraft servers in Rust.[Luminance](https://phaazon.net/blog/2022-luminance-redesign-part-1)is a type-safe graphics framework, which is currently undergoing a major rewrite.[Bevy ECSS](https://github.com/afonsolage/bevy_ecss)is a library for integrating a subset of CSS with Bevy’s ECS system.[dtm](https://github.com/Ku95/dtm)is a fast encoder/decoder for the DTM image format.


## Discussions [#](https://gamedev.rs#discussions)

- /r/rust_gamedev

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[‘Are We Game Yet?’ wants to know about projects/games/resources that aren’t listed yet](https://github.com/rust-gamedev/arewegameyet#contribute).[Graphite is looking for contributors](https://graphite.rs/contribute)to help build the new node graph and 2D rendering systems.[winit’s “difficulty: easy” issues](https://github.com/rust-windowing/winit/issues?q=is%3Aopen+is%3Aissue+label%3A%22difficulty%3A+easy%22).[Backroll-rs, a new networking library](https://github.com/HouraiTeahouse/backroll-rs/issues).[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[A/B Street’s “good first issue” issues](https://github.com/a-b-street/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/D-Good-First-Issue).

## Bonus [#](https://gamedev.rs#bonus)

[Ruffle](https://ruffle.rs/) is an open-source Flash Player emulator, written in Rust. It aims to run
natively on all modern operating systems and web browsers, leveraging Rust’s
memory safety guarentees to avoid the security pitfalls that Flash became
notorious for in its later years.

Many of today’s game developers got their start developing in Flash, and Ruffle aims to help preserve this part of internet (and gaming!) history for future generations to look back on.

For a look back at the history of Flash gaming, and the influence it has has
on games today, check out [Flash Game History](https://www.flashgamehistory.com/).

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!

**Discuss this post on**:
[/r/rust_gamedev](https://www.reddit.com/r/rust_gamedev/comments/y3u42s/this_month_in_rust_gamedev_38_september_2022/),
[Twitter](https://twitter.com/rust_gamedev/status/1580915833941151744),
[Discord](https://discord.gg/yNtPTb2).