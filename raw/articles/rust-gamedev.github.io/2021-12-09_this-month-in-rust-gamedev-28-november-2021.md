---
title: 'This Month in Rust GameDev #28 - November 2021'
url: https://gamedev.rs/news/028/
author: Rust GameDev WG
published: '2021-12-09'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 28th issue of the Rust GameDev Workgroup’s monthly newsletter.
[Rust](https://rust-lang.org) is a systems language pursuing the trifecta: safety, concurrency, and
speed. These goals are well-aligned with game development. We hope to build an
inviting ecosystem for anyone wishing to use Rust in their development process!
Want to get involved? [Join the Rust GameDev working group!](https://github.com/rust-gamedev/wg#join-the-fun)

You can follow the newsletter creation process by watching [the coordination
issues](https://github.com/rust-gamedev/rust-gamedev.github.io/issues?q=label%3Acoordination). Want something mentioned in the next newsletter? [Send us
a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io). Feel free to send PRs about your own projects!

[Rust GameDev Meetup](https://gamedev.rs/news/028/#rust-gamedev-meetup)[Game Updates](https://gamedev.rs/news/028/#game-updates)[Learning Material Updates](https://gamedev.rs/news/028/#learning-material-updates)[Engine Updates](https://gamedev.rs/news/028/#engine-updates)[Tooling Updates](https://gamedev.rs/news/028/#tooling-updates)[Library Updates](https://gamedev.rs/news/028/#library-updates)[Other News](https://gamedev.rs/news/028/#other-news)[Discussions](https://gamedev.rs/news/028/#discussions)[Requests for Contribution](https://gamedev.rs/news/028/#requests-for-contribution)

## Rust GameDev Meetup [#](https://gamedev.rs#rust-gamedev-meetup)

![Gamedev meetup poster](../../assets/1dff5fd179bd2e0e.png)


The eleventh Rust Gamedev Meetup happened in November. You can watch the
recording of the meetup [here on Youtube](https://youtu.be/nLyiLnC5mn4). The meetups
take place on the second Saturday every month via the [Rust Gamedev Discord
server](https://discord.gg/yNtPTb2) and are also [streamed on
Twitch](https://twitch.tv/rustgamedev). If you would like to show off what you’ve been
working on at the next meetup on [December 11th](https://everytimezone.com/s/bb9cdaec), fill out
[this form](https://forms.gle/BS1zCyZaiUFSUHxe6).

## Game Updates [#](https://gamedev.rs#game-updates)

### Flesh [#](https://gamedev.rs#flesh)

![flesh preview](../../assets/1508c3ec361d6921.gif)

[Flesh](https://store.steampowered.com/app/1660850/Flesh/) by [@im_oab](https://twitter.com/im_oab) is a 2D-horizontal shmup game with hand-drawn animation and
an organic/fleshy theme. It is implemented using [Tetra](https://github.com/17cupsofcoffee/tetra). This month’s updates
include:

- Support different types of ships that players can choose.
- Add a melee weapon.

![Screenshot of One-Click Ninja](../../assets/fc86779d24e067df.png)

One-Click Ninja is a rhythm game made in 10 days for [1-Button Jam 2021](https://itch.io/jam/1-button-jam-2021),
written in Rust using the [Bevy](https://bevyengine.org) engine.

The source is available MIT licensed on [GitHub](https://github.com/fluffysquirrels/one-click-ninja), and you can
[play in your browser on itch.io](https://fluffysquirrels.itch.io/one-click-ninja).

Fish Fight is a fast-paced 2D brawler game, played by 1-4 players online or on a
shared screen, built with [macroquad](https://github.com/not-fl3/macroquad) game engine.

This month it got a trailer, and the game is now available to wishlist on
[Steam](https://store.steampowered.com/app/1771640/Fish_Fight_The_Prequel/)!

BITGUN ([Steam](https://store.steampowered.com/app/1673940/BITGUN/), [Twitter](https://twitter.com/logloggames),
[Discord](https://discord.gg/XrGZQkq)) by [@LogLogGames](https://twitter.com/logloggames) is an action
roguelike zombie shooter with lots of blood. The game is built using Godot and
Rust (via [godot-rust](https://godot-rust.github.io/)).

They recently implemented a mission system, where you can select one of [three
types of missions](https://twitter.com/LogLogGames/status/1464009563976392713?s=20) to go to from the central camp. One is to
defend supplies from a horde of zombies, the second is to search a facility for some
object or clear all the zombies and the last one is to fight your way through a
tunnel full of spiders and other enemies! They also worked on a
[tutorial](https://twitter.com/LogLogGames/status/1461898845810348033?s=20).

![Halloween Mahjong Solitaire screenshot](../../assets/8cee21ed309fac63.png)

Halloween Mahjong Solitaire ([GitHub](https://github.com/Syn-Nine/rust-mini-games/tree/main/2d-games/mahjong)) by
[@Syn-Nine](https://twitter.com/Syn9Dev) is a game created for the [Game Developers
Refuge 4x4x4 Challenge](http://noop.rocks/gdr/viewtopic.php?f=2&t=70) in October 2021.

The challenge was to create a Halloween-themed game based on four emojis. In this case the chosen emoji combination was: skull_and_crossbones, bat, game_die, and shinto_shrine (☠️ 🦇 🎲 ⛩️).

The game is part of an open source repository of several mini-games that use
Syn9’s [Rust Mini Game Framework](https://github.com/Syn-Nine/mgfw).

### Country Slice [#](https://gamedev.rs#country-slice)

![country-slice-gif](../../assets/e622b486bf559378.gif)


[Country Slice](https://github.com/anopara/country-slice) is
[@anastasiaopara](https://twitter.com/anastasiaopara/)’s hobby project, where users can draw a
small scene, and their input is amplified with real-time procedural geometry
generation.

Country Slice uses [Bevy Engine](https://github.com/bevyengine/bevy) for entity management, and has
recently [been ported to OpenGL](https://twitter.com/anastasiaopara/status/1464304076074672144?s=20) (using
[gl-rs](https://github.com/brendanzab/gl-rs/tree/master/gl) and [glutin](https://github.com/rust-windowing/glutin)). It is being developed openly on
[GitHub](https://github.com/anopara/country-slice).

You can follow the development of Country Slice on
[Twitter](https://twitter.com/anastasiaopara/).

![Travelling merchant](../../assets/7134efece55da492.jpg)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In November, Veloren started a new initiative to help new developers learn more
about the codebase; the Veloren Reading Club. You can watch the
[first](https://www.youtube.com/watch?v=DpXwYEe_LWo) and [second](https://www.youtube.com/watch?v=n8XayRvVBEs) sessions
now. Hats were merged, and a major rewrite of the server-hosting section of the
book happened. New textures were made for item drops. Some concept art was
created for what massive cities could look like. Dynamic weather was added, and
you can [watch that in action](https://www.youtube.com/watch?v=MZwfaohynvc).

Experience sharing went through a large overhaul to evenly distribute EXP gained across groups. The difficulty of dungeons was adjusted to be more balanced for new players. Persistence was added to skills, and measures were put in place to help with future migrations to new skill trees. Work was done on site2, the system that is used to generate structures procedurally. This will help make the variance more dynamic by adding more parameters that can be adjusted. In December, Veloren will release 0.12, hopefully with some holiday spirit!

November’s full weekly devlogs: “This Week In Veloren…”:
[#144](https://veloren.net/devblog-144),
[#145](https://veloren.net/devblog-145),
[#146](https://veloren.net/devblog-146),
[#147](https://veloren.net/devblog-147),
[#148](https://veloren.net/devblog-148).

![An animation of a platformer where the entire world bends around
you](../../assets/72486022df102de4.gif)

BENDYWORM ([GitHub](https://github.com/Bauxitedev/bendyworm), [Twitter](https://twitter.com/bauxitedev/status/1466034866122891266)) by
[@bauxitedev](https://twitter.com/bauxitedev) is a platformer with a twist: the entire
world bends and twists around you as your progress through the level. Why?
Because you’re inside of a gigantic worm, and worms are bendy.

The game was made for GitHub Game Off 2021, and uses `godot-rust`

behind the
scenes.

The game is available for free on [itch.io](https://bauxite.itch.io/bendyworm), and the source
code is available on [GitHub](https://github.com/Bauxitedev/bendyworm). (Windows only for now, Linux
build available soon)

*Discussions:
/r/rust/,
Twitter*

Molecoole is a top-down shooter roguelike where you build your character from
different atoms. Each atom has a unique ability to provide tons of variety
between playthroughs. It’s made using the [Bevy
Engine](https://github.com/bevyengine/bevy).

This month Molecoole launched its [Steam page](https://store.steampowered.com/app/1792170/Molecoole/)! They also added
[new weapons](https://twitter.com/kiss_mrton/status/1459567092995403776) and new [bosses](https://twitter.com/kiss_mrton/status/1457022034949689351).

In December their main focus will be on audio and polishing the game.

![hgs_screen](../../assets/e2a0d6320af4e66d.jpg)


[Hydrofoil Generation](https://hydrofoil-generation.com/) ([Facebook](https://www.facebook.com/HydrofoilGenerationSailing/), [Discord](https://discord.gg/DtKgt2duAy/)) is a
realistic sailing/foiling inshore simulator in development for PC/Steam that
will put you in the driving seat of modern competitive sailing.

November was dedicated to the launch of the [Steam Store](https://store.steampowered.com/app/1448820/Hydrofoil_Generation/) page and
associated [trailer](https://youtu.be/CfmCLr19Hbs) showcasing Hydrofoil Generation’s custom Rust
engine in motion for the first time. Constant tweaks to the boat behavior and
addition of gameplay features are ongoing as the planned Q2 2022 Steam Early
Access release gets closer and closer.

December 2021 will see an attempt to port the rendering backend of the game from DirectX 11 to WGPU to widen the number of platforms reachable with a particular interest in the Steam Deck that seems to offer the perfect controller layout for such a demanding simulation as Hydrofoil Generation.

You will be able to follow the progress of the port Mondays and Fridays on
[Twitch](https://www.twitch.tv/kunosstefano).

### Idu [#](https://gamedev.rs#idu)

![idu’s new sprinkler in action](../../assets/a16585d58a241a3b.gif)


Idu ([Discord](https://discord.gg/PR3GgYYkym)) by [@logicsoup](https://twitter.com/logicsoup) and [@epcc10](https://twitter.com/epcc10) is an upcoming game
centered around growing realistic plants.

In November, a new major update was released that overhauled the automatic watering system. In addition, an automatic stair builder and a grass-cutting tool was added to reduce the tediousness of these common tasks.

A free playable alpha demo is available at [Idu’s Discord server’s
demo-download channel](https://discord.gg/PR3GgYYkym)! Updates are posted to their
[Youtube](https://www.youtube.com/channel/UC1JmPXgbR5R2dCsM_QJGe1w) as well.

![items moving through the belt](../../assets/8a4e4f7cae9e13a6.png)


Combine&Conquer by [Martin Buck](https://github.com/I3ck) is a WIP strategy game about automation
similar to Satisfactory or Factorio.

This month Martin finished [writing a detailed devlog](https://buckmartin.de/combine-and-conquer.html) for the project
from the first commit up until now. A few dozen short posts cover various topics
including simulation of arms and conveyor belts with moving items, blueprints,
testing, rendering, save and load, tech tree and research, and multiplayer.

*Discussions:
/r/rust_gamedev*

![Pong, but one of the characters rewinds time to figure out which of the other
player's ballusions is actually real](../../assets/c32fe1429ebc5cdf.gif)

PaddlePunks is a versus tennis game by [Felix Windström](https://twitter.com/sov_gott_games)
with a diverse cast of characters and playstyles and online play with rollback
netcode.

Latest developments:

- Some engine work to improve performance on laptops with integrated GPUs
- Balance updates to make the skeleton less overbearing
- Presented the game at
[Rustfest](https://watch.rustfest.global/)in an interactive session.

You can download and play the game now on [itch.io](https://sovgott.itch.io/paddlepunks), or join
the [Discord](https://discord.gg/cpPDeVcWxc) to chat with the developer and other players.

Shroom Kingdom ([GitHub](https://github.com/Shroom-Kingdom), [Discord](https://discord.gg/SPZsgSe),
[Twitter](https://twitter.com/shrm_kingdom)) is an upcoming play-to-earn video game built with web
technologies running on the [NEAR Blockchain](https://near.org). It is a 2D
platformer, where players can also build their own levels and share them with
others.

Currently, a prototype of the game is in development. The game is written with
the [Bevy game engine](https://bevyengine.org) and the [Rapier physics engine](https://rapier.rs/) and is
compiled to WebAssembly. The prototype is still very basic, but you can already
place and remove blocks and have a feeling about the physics recreation of the
original games.

In the past months, there also has been the SHRM token launch and a [token
airdrop](https://twitter.com/shrm_kingdom/status/1450362543608901634?s=20) for NEAR early adopters. The [Shroom Kingdom
DAO](https://whitepaper.shroomkingdom.net/8_DAO.html) is looking for people, who want to become involved and get paid
with their very own token.

To onboard new users to blockchain gaming, a [linkdrop campaign](https://linkdrop.shroomkingdom.net/)
is currently in development, where people can claim a small amount of NEAR token
to create their own wallet.

## Engine Updates [#](https://gamedev.rs#engine-updates)

[Tetra](https://github.com/17cupsofcoffee/tetra) is a simple 2D game framework, inspired by XNA, Love2D, and Raylib. This
month, version 0.6.7 was released, featuring:

- Updates to the gamepad backend, adding rumble support for a much wider variety of controllers (including DualShock 4s)
- Various bugfixes and docs improvements

For more details, see the [changelog](https://github.com/17cupsofcoffee/tetra/blob/main/CHANGELOG.md).

Additionally, development has begun on version 0.7 - check out [the planned
features and changes](https://github.com/17cupsofcoffee/tetra/issues/297), and feel free to suggest more!

[Oxygengine](https://github.com/PsichiX/Oxygengine) v0.24.0 [#](https://gamedev.rs#oxygengine-v0-24-0)

![Oxygengine RPG game template](../../assets/802737e80edce973.gif)


The hottest HTML5 + WASM game engine for games written in Rust with web-sys.

[@PsichiX](https://twitter.com/PsichiX), the creator of [Oxygengine](https://github.com/PsichiX/Oxygengine), spent the last two months on making:

- First few chapters of the book explaining how Oxygengine works in:
[Oxygengine Essentials Book](https://psichix.github.io/Oxygengine/). - New hardware-accelerated renderer based on Material Graphs (to allow making
faster and better quality game visuals - more about that in
[Material Graph based rendering](https://psichix.github.io/Oxygengine/concepts/ha-renderer/introduction.html#material-graph-based-rendering)chapter). - New Overworld game module (which aims to provide all essential features needed by RPG game developers, to let them focus on making an actual game).
- New AI feature module (WIP) that integrates
[Emergent AI](https://github.com/PsichiX/emergent)crate with the engine. - Plugin-based asset pipeline as well as support for LDtk software projects.

All of these changes mark the beginning of stabilizing phase of the engine. The API more or less won’t change much - now the focus is put entirely on the features that will push progress towards the Ignite visual game editor for artists and game designers to use.

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

[The Raytracer Challenge](https://github.com/jakobwesthoff/the_ray_tracer_challenge_in_rust) is a project with the goal
to write a raytracer from scratch in Rust, while showing each step of the way
[as a weekly live coding session](https://www.youtube.com/playlist?list=PLy68GuC77sUTyOUvDhVboQoOlHoa4XrSO). Everything is
documented, starting with implementing [Vectors](https://youtu.be/xGEDQXBMdV4) and
[Matrices](https://youtu.be/RYALPW0pJr4) all the way to creating [Phong
Lighting](https://youtu.be/HSgS_NQob2I).

November has been a busy month for the project with lots of visual changes in the raytraced results:

-
[Basic animation support](https://youtu.be/3LinpB7ns60)came along allowing the easy creation of video sequences. -
More realistic and life-like scenes due to

[Shadow Casting](https://youtu.be/agqAUa1qgGo). -
As a new basic body type

[Planes](https://youtu.be/4y1aRPiH9Ko)came to life.

![Rustacean Station Logo](../../assets/f3e6a1e4d7b74de2.jpeg)


The [Rustacean Station](https://rustacean-station.org/) is a podcast about the Rust language.

In November, [Herbert Wolverson](https://twitter.com/herberticus) [was
interviewed](https://rustacean-station.org/episode/048-herbert-wolverson/) about game development in Rust. In this
episode, lots is discussed about existing game development engines, and how Rust
is breaking into this space with engines like Bevy, Amethyst, and RG3D. There is
also a discussion on the Entity Component System paradigm in comparison to
Object Oriented Programming.

In [this blog post](https://raphlinus.github.io/gpu/2021/11/17/prefix-sum-portable.html), [Raph Levien](https://levien.com/) describes the current state
of coding on a graphics card. The post describes how going about writing custom
code still induces many issues in this day and age, and what modern technologies
can be used to help make this easier. [Rust-gpu](https://github.com/EmbarkStudios/rust-gpu) is mentioned as a possible way
to write compute shaders in a “real language”.

![ascii map and ui](../../assets/f530b78b3bd939fd.jpg)

[The Roguelike Tutorial](http://bfnightly.bracketproductions.com/rustbook) by [@herberticus](https://twitter.com/herberticus) got a [new 75th (!)
chapter](http://bfnightly.bracketproductions.com/rustbook/chapter_75.html) that shows how to generate a chaotic Voronoi-based city
plaza inhabited by dark elves and adds a new big demon enemy to guard the Abyss
portal.

You can battle your way down to the Dark Elf Plaza, and find the gateway to Abyss - but only if you can evade a hulking demon and a horde of elves—with very little in the way of help offered. Next up, we’ll begin to build the Abyss.


![A screenshot of a game in a browser](../../assets/bcd2e0b4547dcd60.jpg)

Another update from [@herberticus](https://twitter.com/herberticus) is a bonus article for the [Hands-on
Rust](https://hands-on-rust.com) book: [“Run Your Rust Games in a Browser”](https://hands-on-rust.com/2021/11/06/run-your-rust-games-in-a-browser-hands-on-rust-bonus-content/) that guides the
reader through the basics of building and publishing [bracket-lib](https://github.com/amethyst/bracket-lib) games in
WebAssembly.

## Tooling Updates [#](https://gamedev.rs#tooling-updates)

![SPV-0.3.5 screenshot](../../assets/a16fe974c59289c1.png)


[SPV](https://github.com/AlbinSjoegren/SPV) by [Albin Sjögren](https://github.com/AlbinSjoegren) is a calculator utility for working with astronomical
position and velocity data.

In the last month, a relative position and velocity calculation system has been added. This is due to the inaccuracy of astronomic data. With this new method that relies on the orbital elements of two body systems getting data for multibody simulation is now possible.

Apart from this new equation set, [SPV](https://github.com/AlbinSjoegren/SPV) now also has a more standard color
scheme based on the one GitHub uses. This month also came with numerous bug
fixes and a more concrete plan for future development.

For any feature requests, reach out to the developer on [Discord](https://discordapp.com/users/258254056185659392)
or [GitHub](https://github.com/AlbinSjoegren/SPV).

[PickPicPack](http://www.p43d.com/pickpicpack) 0.1.6 [#](https://gamedev.rs#pickpicpack-0-1-6)

![PickPicPack 0.1.6](../../assets/6bd153835c5df529.gif)


[PickPicPack](http://www.p43d.com/pickpicpack) ([GitHub](https://github.com/p4ymak/pickpicpack), [Gumroad](https://p4ymak.gumroad.com/l/pickpicpack)) by
[@p4ymak](http://www.p43d.com/p4ymak) is a tiny yet powerful utility for packing images into
rectangles with arbitrary aspect ratio.

It is useful for creating mood boards, daily art reports, presentations and other collages.

Features so far:

- Interactive loading
- Scaling images to equal size
- Optional margin between images
- Custom aspect ratio; now you can set aspect ratio by text in any form
- CLI; you can use it without GUI and embed it into your project manager tool

![Graphite](../../assets/47e5b758a478096e.png)


Graphite ([GitHub](https://github.com/GraphiteEditor/Graphite), [Discord](https://discord.graphite.design),
[Twitter](https://twitter.com/GraphiteEditor)) is an in-development vector and raster graphics
editor built on a non-destructive node-based workflow.

The previously announced Alpha release was delayed as core devs returned to school - January is the new goal. Development now continues to pick up speed. Design of the project website has continued for its launch soon, alongside the Alpha release.

The project upgraded to the Rust 2021 edition and made big improvements to the
frontend TypeScript and web infrastructure. The editor UI is now fully
responsive at small window sizes. Unsaved document tabs display an `*`

and warn
before closing the window. Ruler measurements now move and scale with the
document. And the new snapping system helps draw/move shapes aligned with
others.

[Try it right now in your browser.](https://editor.graphite.design) Graphite is making
steady progress towards becoming a non-destructive, procedural graphics editor
suitable for replacing traditional 2D DCC applications. [Join the
Discord](https://discord.graphite.design) and get involved!



![youtube preview: modelling tree's branches using ball as a cursor](../../assets/36f8dd4a8568b96b.jpg)

[Solid Editor](https://solidengine.org/solid-editor) is [Solid Engine](https://solidengine.org)’s custom-built voxel
graphics editor. It is designed to be a key part of the engine’s asset pipeline,
enabling the creation of game-ready voxel graphics assets. Since the engine part
is pretty far from being done, the author decided to release this editor as a
standalone application.

Besides being natively compatible with Solid Engine, the editor sports some generally interesting and unique features.


- True WYSIWYG editing. The editor scene is rendered using Solid Engine’s path tracer in real-time, yielding realistic lighting while editing.
- The possibility to edit voxels directly in 3D, by using any brightly colored ball as a 3D pointing device. Read more about the
[Ball Pointer].- A novel approach to editor tools. Instead of many different tools with overlapping functionality (e.g. “draw square” vs. “select square”, or “bucket fill” vs. “magic wand”) there is only one, a versatile Selection tool. Different effects can be applied to the selected voxels, producing the same results as regular editor tools. Combined with real-time effect preview, the user experience is very similar to that of classic graphics editors, with the added benefit of being able to tweak every edit before applying it.

*Discussions:
/r/rust_gamedev*

## Library Updates [#](https://gamedev.rs#library-updates)

[Pixels](https://github.com/parasyte/pixels) is a tiny hardware-accelerated pixel framebuffer. Its goals include
pixel-perfect rendering and custom shader pipelines for textures with direct
pixel access. It’s perfect for making 2D animations, games, and emulators.

Version 0.8.0 was released this month, bringing highly-anticipated support for
WASM targets, as well as support for Raspberry Pi 4. A [minimal example for web
browsers](https://github.com/parasyte/pixels/tree/0.8.0/examples/minimal-web) is included to get you started. Full details are available
in the [release notes](https://github.com/parasyte/pixels/releases/tag/0.8.0).

[Quinn](https://github.com/quinn-rs/quinn) is an async-enabled implementation of the state-of-the-art IETF QUIC
transport protocol, a robust foundation for real-time networking.

[Quinn 0.8](https://github.com/quinn-rs/quinn/releases/tag/0.8.0) introduces support for the final QUIC 1 specification
defined in [RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.html). Other highlights include an improved CUBIC
congestion controller, a more ergonomic configuration API, and numerous
performance and robustness improvements.

[hecs](https://github.com/Ralith/hecs) is a fast, lightweight, and unopinionated archetypal ECS library.

[Version 0.7](https://github.com/Ralith/hecs/blob/master/CHANGELOG.md#071) introduces several new features, including two new
query combinators, a `CommandBuffer`

for recording operations to be applied to a
`World`

at a future time, accessors for efficient random access within columns,
and a variant of `EntityBuilder`

that clones its components and can therefore be
spawned from repeatedly. Other improvements include compatibility with 32-bit
MIPS and PPC, and introduction of a niche to `Entity`

so that e.g.
`Option<Entity>`

will not consume additional space.

![module before/after](../../assets/627547fb0cf58e49.png)


godot-rust ([GitHub](https://github.com/godot-rust/godot-rust), [Discord](https://discord.com/invite/FNudpBD), [Twitter](https://twitter.com/GodotRust))
is a Rust library that provides bindings for the Godot game engine.

November has been a month of refactoring for godot-rust. The API was cleaned up across different locations, reducing confusion and making the library more accessible:

- The module simplification (
[#811](https://github.com/godot-rust/godot-rust/pull/811)) continued initial efforts on the module structure, such as shorter paths and avoidance of redundant re-exports. Some differences between v0.9.3 and now can be seen in the above picture. - Several core symbols were renamed for consistency (
[#815](https://github.com/godot-rust/godot-rust/pull/815)):`RefInstance`

->`TInstance`

and`TypedArray`

->`PoolArray`

, among others. - Another refactoring affects the
`Variant`

conversion methods ([#819](https://github.com/godot-rust/godot-rust/pull/819)). Instead of`Variant::to_i64()`

which may silently fail and return a default value (Godot behavior), the recommended method is now`Variant::to<T>()`

. This enables genericity and is more idiomatic in Rust, returning an`Option`

to indicate success or failure.

As a binding to a C++ library, one topic godot-rust has to deal with is the use
of `unsafe`

, which sometimes boils down to a trade-off between safety and
ease-of-use. Even though Rust provides basic guidelines, there are different
philosophies on their execution, see [The CXX Debate](https://steveklabnik.com/writing/the-cxx-debate) for an example. To
discuss how APIs interacting with Godot can be as ergonomic as possible while
preserving safety, [issue #808](https://github.com/godot-rust/godot-rust/pull/808) was opened.

NavMesh crate is a pathfinding library for 2D and 3D games.

This month changes by [@PsichiX](https://twitter.com/PsichiX):

- Added NavGrid structure to find paths on grids.
- Added NavFreeGrid structure to find paths on cells put in free layout manner (used for example on clusters of cells rather than the condensed grid).
- Added NavIslands structure to allow hierarchical pathfinding (used for example with streamed navigation islands, such as other pathfinding structures).

[Rust CUDA](https://github.com/Rust-GPU/Rust-CUDA) by [Riccardo D’Ambrosio](https://github.com/RDambrosio016) is a [newly-released
project](https://www.reddit.com/r/rust/comments/qzv428/announcing_the_rust_cuda_project_an_ecosystem_of/) with the goal of making Rust a Tier-1 language
for fast GPU computing. There are still many bugs, and it’s in an early stage.

With this release comes a few crates. [rustc_codegen_nvvm](https://crates.io/crates/rustc_codegen_nvvm) for compiling Rust to
CUDA PTX code using rustc’s custom codegen mechanisms and the libnvvm CUDA
library. [cust](https://crates.io/crates/cust) for actually executing the PTX is a high-level wrapper for the
CUDA Driver API. [cuda_builder](https://crates.io/crates/cuda_builder) for easily building GPU crates. [cuda_std](https://crates.io/crates/cuda_std) is
the GPU-side standard library which complements rustc_codegen_nvvm. [gpu_rand](https://crates.io/crates/gpu_rand)
is a GPU-friendly random number generation. [nvvm](https://crates.io/crates/nvvm) is high-level bindings to
libnvvm, and [ptx_compiler](https://crates.io/crates/ptx_compiler) is high-level bindings to the PTX compiler APIs,
which are currently incomplete. [find_cuda_helper](https://crates.io/crates/find_cuda_helper) is for finding CUDA on the
system. There are many other works in progress.

## Other News [#](https://gamedev.rs#other-news)

- Other game updates:
[Rust Shooter progress report](https://reddit.com/r/rust_gamedev/comments/r06n8o/rust_shooter_another_update): GLTF import, more character animations and weapons, and underwater effects.[A video of the new record for speedrunning the Way of Rhea demo](https://www.youtube.com/watch?v=Z0lKsABSwME)(spoilers!)[Necrophaser](https://reddit.com/r/rust_gamedev/comments/ql65sw/alpha_release_of_necrophaser)is a recently alpha-released Top-Down Shooter made with Bevy.[A new spaceship for Stellary 2](https://twitter.com/CoffeJunkStudio/status/1459493244648280071).[Endless Trial](https://reddit.com/r/rust_gamedev/comments/qw5e36/endless_trial_simple_2d_bullethell_game)is a 2D bullet-hell game made in Tetra.

- Other learning material updates:
[GBA From Scratch](https://lokathor.github.io/gba-from-scratch/introduction.html)is a tutorial on how to code for the Game Boy Advance using Rust.[Ping Pong Tutorial](https://phychic-owl.medium.com/rust-project-ping-pong-game-665766cc45ed)is a walkthrough on creating a ping pong game in Rust.

- Other engine updates:
[rg3d now has a cheat/guide book](https://rg3d-book.github.io).[miniquad got a GL2 backend](https://twitter.com/fedor_games/status/1462804219719831552)for even better support of old and/or virtual systems.

- Other library updates:
[natura](https://github.com/ziyasal/natura)is a simple and efficient spring animation library.


## Discussions [#](https://gamedev.rs#discussions)

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[Graphite is looking for contributors](https://github.com/GraphiteEditor/Graphite/issues/202)to help reach the 0.1 Alpha release.[winit’s “difficulty: easy” issues](https://github.com/rust-windowing/winit/issues?q=is%3Aopen+is%3Aissue+label%3A%22difficulty%3A+easy%22).[Backroll-rs, a new networking library](https://github.com/HouraiTeahouse/backroll-rs/issues).[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[A/B Street’s “good first issue” issues](https://github.com/a-b-street/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/D-Good-First-Issue).

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!

**Discuss this post on**:
[/r/rust_gamedev](https://www.reddit.com/r/rust_gamedev/comments/rcmz17/this_month_in_rust_gamedev_28_november_2021/),
[Twitter](https://twitter.com/rust_gamedev/status/1469009470420398082),
[Discord](https://discord.gg/yNtPTb2).