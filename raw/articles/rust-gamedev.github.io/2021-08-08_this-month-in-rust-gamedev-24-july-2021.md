---
title: 'This Month in Rust GameDev #24 - July 2021'
url: https://gamedev.rs/news/024/
author: Rust GameDev WG
published: '2021-08-08'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 24th issue of the Rust GameDev Workgroup’s
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

[Game Updates](https://gamedev.rs/news/024/#game-updates)[Learning Material Updates](https://gamedev.rs/news/024/#learning-material-updates)[Engine Updates](https://gamedev.rs/news/024/#engine-updates)[Tooling Updates](https://gamedev.rs/news/024/#tooling-updates)[Library Updates](https://gamedev.rs/news/024/#library-updates)[Requests for Contribution](https://gamedev.rs/news/024/#requests-for-contribution)

## Rust GameDev Meetup [#](https://gamedev.rs#rust-gamedev-meetup)

![Gamedev meetup poster](../../assets/251be86dc60a26e1.png)


The seventh Rust Gamedev Meetup happened in July. You can watch the recording of
the meetup [here on Youtube](https://www.youtube.com/watch?v=0cefGQyZXH4). The meetups take place on
the second Saturday every month via the [Rust Gamedev Discord
server](https://discord.gg/yNtPTb2), and are also [streamed on
Twitch](https://twitch.tv/rustgamedev). If you would like to show off what you’ve been
working on at the next meetup on [August 14th](https://everytimezone.com/s/391b6160), fill
out [this form](https://forms.gle/BS1zCyZaiUFSUHxe6).

## Game Updates [#](https://gamedev.rs#game-updates)

![Llama ride](../../assets/5d7711add73232b0.png)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In July, work focused on larger tasks that tend to come up between versions.
Optimizations were made for networking with compression, and message queue
improvements ([devblog #127](https://veloren.net/devblog-127)). Modular weapons are in the works, which
will allow for much more dynamic ways to choose what you fight with. The project
also hit 300k lines of code.

Many contributors are working on the art and asset front, with lots of new SFX,
models, and UI elements making their way into the game. Caves are also getting a
lot of love, and a bloom feature is being integrated. Some members broke down
what they plan to have done by the 0.11 release at the beginning of September,
and you can read about that in [devblog #130](https://veloren.net/devblog-130).

July’s full weekly devlogs: “This Week In Veloren…”:
[#127](https://veloren.net/devblog-127),
[#128](https://veloren.net/devblog-128),
[#129](https://veloren.net/devblog-129),
[#130](https://veloren.net/devblog-130).

![Zemeroth on Google Play](../../assets/0a1f39fb2592b0c8.jpg)


[Zemeroth](https://github.com/ozkriff/zemeroth/) is a turn-based hexagonal tactics game, developed by [@ozkriff](https://twitter.com/ozkriff).

This month, an early access version of the game was released as a free
download on [Google Play](https://play.google.com/store/apps/details?id=rust.zemeroth) - if you have an Android
device, give it a try!

![hho_header](../../assets/0982a9fe7880c0d3.png)


Harvest Hero Origins is an arcade wave defense game by [Gemdrop Games](https://twitter.com/GemdropGames),
built in Rust on top of [Emerald](https://github.com/Bombfuse/emerald). A [Steam](https://store.steampowered.com/app/1651500/Harvest_Hero_Origins/) page has recently been
made and the game is set to release sometime at the end of this summer.

Battle the oncoming waves of enemies with a friend in local co-op, unlock new playable characters and skins, and make your way to the top of the leaderboard!

Additionally, HHO will be at [PAXWest](https://west.paxsite.com/)
this year, so come check out their booth
if you’ll be there!

![Shroom Kingdom Asset Extractor](../../assets/c31e5c9c6590e052.gif)

Shroom Kingdom ([GitHub](https://github.com/Shroom-Kingdom), [Discord](https://discord.gg/SPZsgSe), [Twitter](https://twitter.com/shrm_kingdom))
is an upcoming play-to-earn video game built with web technologies
running on the [NEAR Blockchain](https://near.org).
In a recent [blog post](https://net64-mod.github.io/blog/shroom-kingdom/) you can read the motivation behind this.

You can play with your favorite plumber brothers. Build your own levels or play levels from others. Every level built on Shroom Kingdom is stored on the blockchain as an NFT.

By playing the game you can either actively earn SHRM tokens via participating in game activities or earn them passively, if other people play or like your levels. The SHRM token will be used to acquire in-game purchases such as unlocking new building blocks or increasing level upload limits.

You can either extract existing assets from Super Mario Maker 2 or use
compatible game mod files from e.g. [Gamebanana](https://gamebanana.com/).
The asset extractor is already working, but support for more file types
needs to be added.

The game will likely be built with [Bevy](https://bevyengine.org/)
and [Rapier](https://rapier.rs/) compiled to WebAssembly.
Next steps include developing a Proof of Concept.

![Screenshot of the game](../../assets/7225a835ee77e8be.png)

[Wicked Potions](https://niklme.itch.io/wicked-potions) is a match-three game developed by
[@nikl_me](https://twitter.com/nikl_me) and [jennifervphan](https://itch.io/profile/jennifervphan) for the [Bored Pixels Jam 8](https://itch.io/jam/bored-pixels-jam-8).
They wrote the game using the [Bevy game engine](https://bevyengine.org/) and created all of the
textures and audio.

The main focus of the game during the one-week jam period were the assets. After the voting period, the developers plan to extend the game mechanics and story a bit more.

![Showcase image for the new inventory UI in The Process](../../assets/ea3fc9812cc6c455.gif)

[The Process](https://twitter.com/PlayTheProcess) by @setzer22 is an upcoming game about factory building,
process management, and carrot production,
built with Rust using the Godot game engine!

Continuing with last month’s migration of old GDScript code to ECS in Rust, this
month’s main focus has been on porting the GUI code. This has resulted in
the birth of a Godot integration for [egui](https://docs.rs/egui/) that now
powers the game’s interface.

This month has seen the following changes and improvements:

- Finished migration of character controller code to ECS style. Now with
[300% more jumps!](https://twitter.com/PlayTheProcess/status/1413081233396011012) - Implemented
[better ambient lighting](https://twitter.com/PlayTheProcess/status/1413943539160031246)and enable using different skies for radiance and display. This required a[forked godot version](https://github.com/setzer22/godot/tree/feature/cosmetic_sky). - Implement a
[new inventory and toolbar](https://twitter.com/PlayTheProcess/status/1417774452012724226)interface using egui. - Integrated the
[puffin profiler](https://twitter.com/PlayTheProcess/status/1420277428199559174)into the game using the godot_egui integration.

![game logo + OS logos](../../assets/0a8af90cc350097c.jpg)


Two years ago [Alex Butler](https://twitter.com/bigabgames) released the “[Robo Instructus](https://www.roboinstruct.us)” puzzle game
on [Steam](https://store.steampowered.com/app/1032170/Robo_Instructus) & [itch.io](https://bigabgames.itch.io/robo-instructus).

This month Alex released a devlog post [“Robo Instructus: 2 Years Old”](https://blog.roboinstruct.us/2021/07/16/2-years-later.html)
about how well the game did in the last year:
Sales by platform/country/OS, player feedback & reviews, etc.

The game also continues to receive updates, the latest [1.33 version](https://store.steampowered.com/news/app/1032170/view/2998819983294763294)
includes full 简体中文 & Español language support.

![New weapons](../../assets/b6c808804fce77dc.png)


Fish Fight ([Twitter](https://twitter.com/fishfightgame)) is a continuation of the demo project
known as Fish Game - made by the same team of people ([@fedor_games](https://twitter.com/fedor_games) and
[@erlend_sh](https://twitter.com/erlend_sh)), now operating as independents. Their goal is to make a
published game, written entirely in Rust and developed as openly as
possible. They are hoping to go public with the open source repo
within a month or so.

Changes and improvements from the last month:

[Pre-alpha trailer released!](https://twitter.com/fishfightgame/status/1424084016467226624)- Loads of new weapons added:
- Mind-controlled Jellyfish
- Kick-bombs (bomberman-style)
- Cursed Skull
- Handcannon
- Gatling gun
- Sproingers
- Pirate Boots
- ..and more!

- Whole new Environmentals system added for map-wide events (mass-shark attack incoming!)
- Physics doc & improvements



![Amethyst to Bevy](../../assets/4487414e29990796.gif)

[Theta Wave](https://github.com/amethyst/theta-wave) is an open-source space shooter game by developers [@micah_tigley](https://twitter.com/micah_tigley) and
[@carlosupina](https://twitter.com/carlosupina). It is one of the showcase games for the [Amethyst Engine](https://amethyst.rs/). In
the past month, they finished the [“Organization”](https://github.com/amethyst/theta-wave/projects/5) update and
made the decision to start working on porting the game to the Bevy engine. You can
find the Bevy version of Theta Wave [here](https://github.com/thetawavegame/thetawave).

Progress on this port is going strong - you can find the GitHub issue for
the port [here](https://github.com/thetawavegame/thetawave/issues/2).



![bounty-bros-title-screen](../../assets/77520f1d8c812782.jpg)

[Bounty Bros.](https://katharostech.com/post/bounty-bros-update-4-physics-damage-pathfinding) is a prototype, top-down adventure game, developed
by [Katharos Technology](https://katharostech.com) as a testing ground for a future
commercial game.

The last two months of development added lots of new features:

- Integrated a new physics system and character controller that allows for smoother character movement.
- Added a new damage system and made cactuses hurt the player.
- Added a life bar and a game over screen.
- Added a pause menu and a fullscreen button.
- Started work on enemy pathfinding.

All the new features can be tested in the latest [web demo](https://katharostech.github.io/skipngo_pre-releases/refs/tags/pre-release-2/?asset_url=https://katharostech.github.io/bounty-bros_pre-releases/2),
and the [blog post](https://katharostech.com/post/bounty-bros-update-4-physics-damage-pathfinding) has the full details of what’s new and what’s
coming next!

![Flesh screenshot](../../assets/f30779c20a504063.jpg)


[Flesh](https://store.steampowered.com/app/1660850/Flesh/) is a 2D horizontal SHMUP by [@Im_Oab](https://twitter.com/Im_Oab/), with a hand-drawn animation style
and an organic/fleshy theme.

This month, a [Steam page](https://store.steampowered.com/app/1660850/Flesh/) was published for the game - it can now be
wishlisted, ahead of a planned release later this year!

## Engine Updates [#](https://gamedev.rs#engine-updates)

`ggez`

0.6 has been released! `ggez`

is a lightweight cross-platform
game framework for making 2D games with minimum friction, with an API
inspired by Love2D.

This release includes many additions, improvements, and bug fixes,
including a `MeshBatch`

type for drawing many instances of the same
geometry, improvements to canvas drawing, updated `winit`

dependencies
that function more smoothly on Linux under Wayland, better error
handling, and more. The whole changelog is available
[here](https://github.com/ggez/ggez/blob/0.6.0/CHANGELOG.md).

More importantly, `ggez`

is now maintained by a group of volunteers,
with the original maintainer stepping down from active development after
over four years. The new maintainers are mostly responsible for the 0.6
release, and will hopefully be bringing good ideas and tech to the
library for years to come. For details, see [this github
issue](https://github.com/ggez/ggez/issues/875).

![Zemeroth running on Android](../../assets/b880bd059cc7828e.jpg)

[Zemeroth](https://gamedev.rs#zemeroth)) running on Android!

[Macroquad](https://github.com/not-fl3/macroquad) is a cross-platform game framework, inspired heavily by Raylib.

This month, a [new tutorial](https://macroquad.rs/tutorials/android/) was published on the
Macroquad website, showing how a game written with the framework can be
ported to Android. It details all of the steps, from building to packaging
for a release on Google Play.

In other news, Macroquad used to depend on rodio+cpal for audio on
native platforms and a custom WebAudio implementation for web, with a custom
abstraction on top of both. This month, Macroquad’s audio system was
reimplemented on top of raw OS APIs - ALSA, OpenSLES, CoreAudio and WASAPI.
This functionality has now been extracted into a crate: [quad-snd](https://github.com/not-fl3/quad-snd).

[Emerald](https://github.com/Bombfuse/emerald) is a 2D portable game engine aiming to export to every
possible target: Windows, Linux, macOS, Android, iOS, Xbox,
Playstation, Nintendo Switch.

In addition to being portable, [Emerald](https://github.com/Bombfuse/emerald) aims to be easy to use
while providing quality features like built-in physics and
Aseprite integration.

If any of this sounds good to you, and you’d like to be a part of it,
[Emerald](https://github.com/Bombfuse/emerald) welcomes all contributors to help make an extremely portable
game engine! Join them on their [Discord server](https://discord.gg/NHsz38AhkD).

![Demonstration of Starframe’s new rope physics](../../assets/b2fd3fdafe9b7dd0.gif)


[Starframe](https://github.com/m0lentum/starframe/) by [@molentum](https://twitter.com/molentum_) is a work-in-progress game engine for physics-y
sidescrolling 2D games.

This month’s noteworthy development was [particle-based ropes](https://twitter.com/molentum_/status/1421204030441889792)
capable of full two-way coupling with rigid bodies, demonstrated above.
Capsule-shaped colliders were also added.

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

[“Hands-on Rust: Effective Learning through 2D Game Development and Play”](https://pragprog.com/titles/hwrust/hands-on-rust/)
by Herbert Wolverson is now in print, as a full color paperback and ebook.
The book teaches Rust through game development examples, and is targeted at
readers who have some experience with writing code in other languages. It
teaches beginner to intermediate-level Rust. Hands-on Rust also teaches
high-level game development concepts, notably Entity-Component System (ECS)
theory.

After walking you through installing Rust, a few simple examples teach the language basics. Then you put these together to make “Flappy Dragon” - a simple Flappy Bird clone. The book then changes gear and begins to build a dungeon crawler (roguelike) with tile graphics.

Outside of the USA, Hands-on Rust is available through [Amazon](https://www.amazon.com/dp/1680508164).

Herbert also published the first [“Hands-on Rust bonus content”](https://medium.com/pragmatic-programmers/flappy-dragon-rust-647e91a34dd4).
The bonus content extends Flappy Dragon to include smooth movement and
animated sprites.



![rg3d RPG screenshot](../../assets/05bd48980ceba89e.jpg)

[Click here](https://www.youtube.com/watch?v=l2ZbDpoIdqk)to see a video of the character controller in action!

Dimitry Stepanov (aka @mrDIMAS) published a
[tutorial series](https://rg3d.rs/tutorials/2021/07/09/rpg-tutorial1.html) about
making an RPG in Rust using the rg3d game engine. In part one of the series,
he builds a character controller from scratch. While that may not sound very exciting,
it’s still a great way to learn the basics of rg3d and Rust gamedev in general!

## Tooling Updates [#](https://gamedev.rs#tooling-updates)

{{ image_figure( alt=“Graphite logo” src=“graphite_scream.png” caption=“A recreation of “The Scream” in Graphite by Norgate“) }}

Graphite ([GitHub](https://github.com/GraphiteEditor/Graphite), [Discord](https://discord.graphite.design),
[Twitter](https://twitter.com/GraphiteEditor)) is an in-development vector and
raster graphics editor built on a non-destructive node-based workflow.

In the past month, the editor has gained numerous vector editing features, including moving layers with the keyboard or mouse, filling and copying colors, flipping and aligning selected layers, and setting blend modes and layer opacity.

Scrollbars, rulers, and thumbnails are now functional. Full screen support has been added, along with a hotkey to center the artwork. An options bar with tool-specific settings and actions has been implemented, currently allowing the number of sides of a polygon to be selected. The order of layers can now be changed using hotkeys.

[Try it right now in your browser.](https://editor.graphite.design) Graphite is making
rapid progress towards becoming a non-destructive, procedural graphics editor
suitable of replacing traditional 2D DCC applications. The release of Graphite
0.1 is anticipated in the coming month; come
[join the Discord](https://discord.graphite.design) to help make it happen!

## Library Updates [#](https://gamedev.rs#library-updates)

[discord-sdk](https://github.com/EmbarkStudios/discord-sdk) is an open source implementation of the [Discord Game SDK](https://discord.com/developers/docs/game-sdk/sdk-starter-guide) by
[Embark Studios](https://embark.dev).

This month saw the release of the initial [ 0.1.0](https://github.com/EmbarkStudios/discord-sdk/blob/main/CHANGELOG.md#010---2021-07-21)
(and

[) version of the crate, which implements initial support for:](https://github.com/EmbarkStudios/discord-sdk/blob/main/CHANGELOG.md#011---2021-07-28)

`0.1.1`

[Activities](https://discord.com/developers/docs/game-sdk/activities)[Lobbies](https://discord.com/developers/docs/game-sdk/lobbies)[Overlay](https://discord.com/developers/docs/game-sdk/overlay)[Relationships](https://discord.com/developers/docs/game-sdk/relationships)[Users](https://discord.com/developers/docs/game-sdk/users)- Application registration (so your game can be launched by Discord)

The API is still rough, but should be in a good enough state to try out!

[rkyv](https://github.com/rkyv/rkyv) is a zero-copy deserialization framework for Rust. It’s an alternative
to serde that makes it easy to quickly and safely load data into memory.

This month, rkyv 0.7 was released with many new features:

[Endian-agnostic serialization](https://github.com/rkyv/rend)[Greatly improved performance](https://github.com/djkoloski/rust_serialization_benchmark)- Enhanced
`no_std`

support [Wrapper types](https://docs.rs/rkyv/0.7.4/rkyv/with/index.html)[A new](https://docs.rs/rkyv/0.7.4/rkyv/collections/btree_map/index.html)`BTreeMap`

implementation- Reduced dependencies
- Support for some common external crates

The full changelog can be found on the [release page](https://github.com/rkyv/rkyv/releases/tag/v0.7.0).

![Throne](../../assets/5834c89a69ba144d.png)


[Throne](https://github.com/t-mw/throne) is a new scripting language for game prototyping and story logic. The
language is rule-based, which allows certain types of logic to be expressed more
concisely than using an object-based language, while remaining fast to execute
and easy to embed in an existing engine. Throne can be experimented with in the
web [playground](https://t-mw.github.io/throne-playground/).

![godot_egui](../../assets/40ba174fd9cd3111.gif)


[godot_egui](https://docs.rs/godot_egui/) is an integration of the [egui](https://github.com/emilk/egui)
crate for the Godot engine using Rust, enabling highly dynamic and performant
user interfaces in an immediate-mode style in Godot.

Godot has a great GUI system, so why use `godot_egui`

instead? A more in-depth
rationale can be found in the crate’s README, but the main reason is to provide
a GUI system for godot-rust games that is closer to Rust’s data driven
philosophy.

Unlike other egui integrations, `godot_egui`

has the special feature of being
embedded as a custom Godot scene tree node. This effectively allows combining
Godot’s retained mode UI and container-based placement with the simplicity of
immediate-mode style GUI code of `egui`

, getting the best of both worlds.

The [github repository](https://github.com/setzer22/godot-egui) has an example
project and usage instructions to get you started with immediate-mode GUI
programming with Godot and Rust!

![Franzplot on wgpu](../../assets/2849ca83546c8d3a.gif)


Following the [Family Reunion](https://gamedev.rs/news/023/#wgpu-family-re-union) initiative, [wgpu](https://github.com/gfx-rs/wgpu) team has been busy rebuilding
the graphics infrastructure. The new D3D12 backend has been merged, which
concludes the trip of moving (or rewriting?) all of the implementation into
Rust. In addition to a “lean and mean” implementation of the host API side,
which turned out to match the WebGPU API very well, the new backend works with
[naga](https://github.com/gfx-rs/naga) exclusively for generation of HLSL shaders.
This is in contrast with gfx-backend-dx12, which only supported SPIRV-Cross.

The team also wrote the blog post [Release of v0.9 and the Future of wgpu](https://gfx-rs.github.io/2021/07/16/release-0.9-future.html).
One of the interesting bits is `gfx`

repository switching to
maintenance mode.

Last but not the least, Francesco Cattoglio described their adventure
with rewriting [Franzplot](https://gfx-rs.github.io/stories/franzplot.html) on a new blog hosted by the wgpu team. This blog will
accumulate stories of wgpu users and their interesting projects.

![GGRS](../../assets/28919187b9923999.png)


[GGRS](https://github.com/gschup/ggrs) by [@g_schup](https://twitter.com/g_schup) is a reimagination of the [GGPO](https://www.ggpo.net/) P2P rollback network SDK
written in 100% safe Rust.

The freshly released version 0.4 comes with tons of fixes for P2P sessions with
up to four players and any number of spectators. More importantly, the repository
now features a [tutorial](https://gschup.github.io/ggrs/docs/getting-started/quick-start/) and full game [examples](https://github.com/gschup/ggrs/tree/main/examples) for every type of session.

![physics example](../../assets/af0ab4c24dce2bf1.gif)

[Bevy Retrograde](https://github.com/katharostech/bevy_retro) (formerly Bevy Retro) is a [Bevy](https://bevyengine.org/) plugin
designed for making pixel-perfect games as easily as possible.

This project was released under the [Katharos License](https://github.com/katharostech/katharos-license). This
license has moral and ethical implications that you may or may not agree with,
so please read it before making use of this project.

In the last two months, Bevy Retrograde has gotten a major update and is also on crates.io for the first time!

- The transform system was migrated to use Bevy’s own transform system.
- The pixel-perfect alignment restriction can now be optionally disabled on a per-sprite basis. This makes it possible to do smooth character and projectile movement if desired.
- The
[Heron](https://github.com/jcornaz/heron)physics engine ( which is powered by Rapier ) was integrated, with a custom extension for automatically creating collision shapes from sprite outlines. - It was decided to start work on migrating Bevy Retrograde to use Bevy’s own rendering abstraction, making it compatible with the larger Bevy rendering ecosystem. This will hopefully be finished in the next release.

More information can be found in the Bevy Retrograde
[release notes](https://github.com/katharostech/bevy_retrograde/releases/tag/v0.2.0).

You can ask questions or give feedback for Bevy Retrograde
[on GitHub](https://github.com/katharostech/bevy_retro/discussions).

![Quilkin](../../assets/3827688110766cf1.png)


[Quilkin](https://github.com/googleforgames/quilkin) is a non-transparent UDP proxy specifically designed for use with
large scale multiplayer dedicated game server deployments, to ensure security,
access control, telemetry data, metrics and more.

This month saw the initial
[0.1.0](https://github.com/googleforgames/quilkin/releases/tag/v0.1.0)
release of the project, as well as announcement blog posts from project
co-founders [Embark Studios](https://gamedev.rs/news/024/(https://embark.dev)) and [Google Cloud](http://cloud.google.com/gaming):

[Embark Studios: Say hi to Quilkin, an open-source UDP proxy](https://medium.com/embarkstudios/say-hi-to-quilkin-an-open-source-udp-proxy-88577c795204)[Google Cloud: Introducing Quilkin: open-source UDP proxies built for game server communication](https://cloud.google.com/blog/products/gaming/introducing-quilkin)

Quilkin is being actively developed and would love contributors and feedback.
Please join the [Discord](https://discord.gg/mfBNZjBDnc),
[mailing list](https://groups.google.com/forum/#!forum/quilkin-discuss) or
follow the project on [Twitter](https://twitter.com/quilkindev).

[@nikl_me](https://twitter.com/nikl_me) wrote a [blog post](https://www.nikl.me/blog/2021/asset-handling-in-bevy-apps/) about creating
[bevy_asset_loader](https://github.com/NiklasEi/bevy_asset_loader), a plugin to simplify asset handling in [Bevy](https://bevyengine.org/)
applications. The post outlines how bevy_asset_loader can be used and
discusses future improvements to the crate.

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[winit’s “difficulty: easy” issues](https://github.com/rust-windowing/winit/issues?q=is%3Aopen+is%3Aissue+label%3A%22difficulty%3A+easy%22).[Backroll-rs, a new networking library](https://github.com/HouraiTeahouse/backroll-rs/issues).[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[A/B Street’s “good first issue” issues](https://github.com/a-b-street/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/D-Good-First-Issue).

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!

**Discuss this post on**:
[/r/rust_gamedev](https://www.reddit.com/r/rust_gamedev/comments/p0hgsy/this_month_in_rust_gamedev_24_july_2021/),
[Twitter](https://twitter.com/rust_gamedev/status/1424398304700420102),
[Discord](https://discord.gg/yNtPTb2).