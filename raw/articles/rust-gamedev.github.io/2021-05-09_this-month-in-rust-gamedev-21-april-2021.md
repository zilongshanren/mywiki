---
title: 'This Month in Rust GameDev #21 - April 2021'
url: https://gamedev.rs/news/021/
author: Rust GameDev WG
published: '2021-05-09'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 21st issue of the Rust GameDev Workgroup’s
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

[Rust GameDev Meetup](https://gamedev.rs/news/021/#rust-gamedev-meetup)[gamedev.rs](https://gamedev.rs/news/021/#gamedev-rs)[Game Updates](https://gamedev.rs/news/021/#game-updates)[Learning Material Updates](https://gamedev.rs/news/021/#learning-material-updates)[Engine Updates](https://gamedev.rs/news/021/#engine-updates)[Library & Tooling Updates](https://gamedev.rs/news/021/#library-tooling-updates)[Requests for Contribution](https://gamedev.rs/news/021/#requests-for-contribution)

## Rust GameDev Meetup [#](https://gamedev.rs#rust-gamedev-meetup)

![Gamedev meetup poster](../../assets/db83dcb3753e8f2f.png)


The fourth Rust Gamedev Meetup happened in April. It was an opportunity for
developers to show off what Rust projects they’ve been working on in the game
ecosystem. This month, we heard a talk about threading in WASM, profiling,
getting a game ready for release, and much more. You can watch the recording of
the meetup [here on Youtube](https://www.youtube.com/watch?v=XE0lH0tlbBs).

The meetups take place on the second Saturday every month via the [Rust
Gamedev Discord server](https://discord.gg/yNtPTb2), and can also be [streamed on
Twitch](https://twitch.tv/rustgamedev). If you would like to show off what you’ve been
working on in a future meetup, fill out [this form](https://forms.gle/BS1zCyZaiUFSUHxe6).

## gamedev.rs [#](https://gamedev.rs#gamedev-rs)

As you may have noticed, [rust-gamedev.github.io](https://rust-gamedev.github.io)
(this site) got an awesome custom domain: [gamedev.rs](https://gamedev.rs)!
We’ve been looking for a good & available domain a [long time](https://github.com/rust-gamedev/rust-gamedev.github.io/issues/233).
Huge thanks to Juratech Systems for donating their domain
to the Rust GameDev WG! ❤️

We’ve also [switched to a more compact URL scheme](https://github.com/rust-gamedev/rust-gamedev.github.io/pull/586)
with separate categories for [the newsletter](https://gamedev.rs/news)
and [other posts](https://gamedev.rs/blog).

*Discussions:
/r/rust_gamedev,
Twitter*

## Game Updates [#](https://gamedev.rs#game-updates)



![GIF showing Micronaut's primary level recursion mechanic](../../assets/a5bd178b829eb947.gif)

Micronaut is a small puzzle platformer by [@Healthire](https://twitter.com/healthire) made in 48 hours for the
Ludum Dare 48 Compo. Run and jump your way through a recursive level layout to
reach the end. Cross platform for native and web, with source available on
[GitHub](https://github.com/Healthire/ld48).

*Discussions: Twitter, ldjam.com*

[The Submariner](https://kettlecorn.itch.io/submariner) is a minimalist action
game made by [@kettlecorn](https://twitter.com/kettlecorn) for the Ludum Dare 48 Compo. Dive
deep into the murky depths, defend yourself with torpedoes,
and try to find a way home!

The Submariner was made with the [Macroquad](https://github.com/not-fl3/macroquad) game engine
and [hecs](https://github.com/Ralith/hecs) was used as the Entity-Component-System (ECS) data structure.

*Discussions: ldjam.com*

![Depth-First Search’s title card](../../assets/1f1927381433036a.jpg)


[Depth-First Search](https://ldjam.com/events/ludum-dare/48/depth-first-search) by [@LPGhatguy](https://twitter.com/LPGhatguy) and [@evaeraevaera](https://twitter.com/evaeraeveara) is a space
dogfighting game made in 72 hours for the Ludum Dare 48 Jam. Travel alone to the
center of the galaxy, battling space pirates, alien eyeballs, and more.

The game was made possible by [wgpu](https://github.com/gfx-rs/wgpu), [egui](https://github.com/emilk/egui), [rapier](https://github.com/dimforge/rapier), [hecs](https://github.com/Ralith/hecs), and many more
Rust community libraries!

*Discussions: ldjam.com, Twitter*

![MineWars Game Screenshot](../../assets/5ab5fb6782b4f534.jpg)


[MineWars](https://minewars.cc) ([Twitter](https://twitter.com/MineWarsGame), [Reddit](https://reddit.com/r/minewars))
by @jamadazi is Minesweeper reimagined as a Multiplayer Real Time Strategy!

First announced publicly last month, the project is working towards an alpha
release for public playtesting. This month’s progress has been mostly internal
refactoring to be able to support networked multiplayer fully. The next steps
are to implement the remaining core game mechanics. The client implementation
may be changed to use the new `bevy_ecs_tilemap`

crate.

Made in the [Bevy Game Engine](https://bevyengine.org).

![Fish game](../../assets/4e53c37547278de3.gif)


[Fish game](https://github.com/heroiclabs/fishgame-macroquad) is an online multiplayer game,
created in a collaboration between [Nakama](https://heroiclabs.com/), an open-source scalable
game server, and the [Macroquad](https://github.com/not-fl3/macroquad) game engine.

This month:

-
[Fish game tutorial](https://macroquad.rs/tutorials/fish-tutorial/)got published. The tutorial breaks down the game codebase into steps, from setting up an empty macroquad project into building a platformer game, and then turning it into a multiplayer game with Nakama. -
[Web build](https://fedorgames.itch.io/fish-game)went live on itch.io

### Project YAWC [#](https://gamedev.rs#project-yawc)

![A demonstration of the Project YAWC map editor](../../assets/01eb38bd3c416c1a.png)


Project YAWC ([Twitter](https://twitter.com/ProjectYawc)) is a turn-based
strategy game built in GGEZ, being developed by junkmail.

April saw the release of Alpha 5, including the integrated map editor, alongside balance changes and unit additions.

An [alpha access request form](https://forms.gle/w22ohPGNk58fo9bv6) is available,
if you want to try it out.

![Animated image showcasing the test map in The Process](../../assets/561389e6b5a0e38d.gif)

[The Process](https://twitter.com/PlayTheProcess/) by @setzer22 is an upcoming
game about factory building, process management and carrot production, built
with Rust using the Godot game engine!

Some of the main highlights of the game:

- Automate complex processes by combining machines and programmable workers.
- Obtain materials from a wide variety of natural resources: Even chicken!
- An upbeat, wholesome aesthetic: Factories don’t need to be depressing.

This last month was focused on implementing the following features:

- A
[test map](https://twitter.com/PlayTheProcess/status/1381648397569036291)to ensure all corners of the codebase are working - Improved player mobility by introducing a
[grappling hook](https://www.reddit.com/r/rust_gamedev/comments/mztqhy/added_a_grappling_hook_to_my_game_built_with_rust/)

The game has been in active development for over a year and is now approaching its first initial playable alpha version. Stayed tuned to the official twitter for updates!

*Discussions:
/r/rust_gamedev,
Twitter*

![Improved text rendering](../../assets/adc809a00f47ee00.jpg)


pGLOWrpg ([GitHub](https://github.com/roalyr/pglowrpg), [Twitter](https://twitter.com/pglowrpg)) by [@Roal_Yr](https://twitter.com/Roal_Yr)
is a Procedurally Generated Living Open World RPG,
a long-term project in development, which aims to be a narrative text-based game
with maximum portability and accessibility.

Recent updates include:

- Finished implementing new printing interface.
- Different types of text: normal, announcement, banner, etc.
- Text color scheme in separate .ron preset file.
- Text wrap implemented.
- Fallback modes for text printing implemented.



![Screenshot of Taipo showing a variety of towers and enemies](../../assets/efbd2e9a1250a1d5.png)

Taipo ([itch.io](https://euclidean-whale.itch.io/taipo), [GitHub](https://github.com/rparrett/taipo)) by [@rparrett](https://github.com/rparrett)
is a Tower Defense game that’s controlled solely by typing words and phrases.

Taipo is intended to be a thin veneer of a game over a tool for practicing Japanese, but there’s an English mode as well. Gameplay sessions are short and the game is playable in a desktop web browser.

Taipo was built with [Bevy 0.5](https://bevyengine.org) with web builds made possible by
[bevy_webgl2](https://github.com/mrk-its/bevy_webgl2) and [bevy_kira_audio](https://github.com/NiklasEi/bevy_kira_audio). Taipo is also supported by these great
projects: [bevy_tiled](https://github.com/stararawn/bevy_tiled), [bevy_asset_ron](https://github.com/jamadazi/bevy_asset_ron).

![Consolidated intersections in A/B Street](../../assets/482e193fe1dd0376.png)


[A/B Street](https://github.com/a-b-street/abstreet) by [@dabreegster](https://twitter.com/CarlinoDustin) is a traffic simulation game exploring how small
changes to roads affect cyclists, transit users, pedestrians, and drivers, with
support for any city with OpenStreetMap coverage.

In April, a new road editor was prototyped, letting the number and width of lanes be changed. Initial installation and downloading new maps is now simpler. Slowly, complex intersections are being handled better. The team also completed four usability study sessions and adjusted the UI accordingly.

[Way of Rhea](https://store.steampowered.com/app/1110620?utm_campaign=tmirgd&utm_source=n21) is a picturesque puzzle platformer—without the platforming.
Solve mind bending color puzzles, unlock new areas of a vibrant hub world, and
talk to NPCs to unravel the mysteries of a world you left behind!

Way of Rhea is being produced by [@masonremaley](https://twitter.com/masonremaley). Latest Way of
Rhea developments:

- A
[hierarchy tree view](https://twitter.com/AnthropicSt/status/1387947007508160517)was added to the editor to make getting art into the game easier. - Work is wrapping up getting
[art into the first snow crab level!](https://twitter.com/AnthropicSt/status/1388907046574215172) [@masonremaley](https://twitter.com/masonremaley)wrote up[an article walking through how the Way of Rhea crash reporter works](https://www.anthropicstudios.com/2021/03/05/crash-reporter/).[@masonremaley](https://twitter.com/masonremaley)is mixing signed distance fields, bézier curves, and art by[Carolyn Whitmeyer](https://www.instagram.com/cw_visuals_insta/)to create[procedural vines](https://twitter.com/masonremaley/status/1389070879536173056).[Carolyn Whitmeyer](https://www.instagram.com/cw_visuals_insta/), the game’s artist, released[a demo real including some content from Way of Rhea](https://twitter.com/masonremaley/status/1387102693626421254).

![Airship](../../assets/134a04de5ddd256f.jpg)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In April, work started on 0.10. Work is being done on combat, with new models being created for enemies, animations being refined, and new player gear being added. The trading and economic systems have continued progress at a good pace. The music system was expanded to support combat music.

Veloren’s financial state was overhauled to examine previous expenses, and prepare for provisioning the dedicated server. Functionality was added to switch between server-authoritative and client-authoritative physics. Skeletons for big-winged creatures were added. Data being sent over the network is being optimized to reduce the amount of bandwidth players have to use.

April’s full weekly devlogs: “This Week In Veloren…”:
[#114](https://veloren.net/devblog-114),
[#115](https://veloren.net/devblog-115),
[#116](https://veloren.net/devblog-116).
[#117](https://veloren.net/devblog-117).

![Animation showing Bibi, the main protagonist of Outer Wonders, jumping from a treetop through a hole, rolling from obstacle to obstacle at the bottom of the tree, and then leaning on a coiled snake to jump back up to the other side of the treetop and continue its way](../../assets/6433edfac35370d5.gif)


[Outer Wonders](https://utopixel.itch.io/outer-wonders) is a colorful, pixel art, puzzle-based adventure game
developed by [Utopixel](https://utopixel.games) where you play as Bibi, a cute round monkey who
enjoys rolling in straight lines. Explore a whimsical nature where
altering the environment is key to progress, and solve puzzles to protect
its wonders.

In April, [Utopixel](https://utopixel.games) released the first playable demo of [Outer Wonders](https://utopixel.itch.io/outer-wonders)
for Windows and Linux on [itch.io](https://utopixel.itch.io/outer-wonders)! In order to achieve this, the [Utopixel](https://utopixel.games)
team:

- Added a cutscene and a tutorial level at the beginning of the demo campaign.
- Integrated sound effects for interaction with the environment and the UI.
- Finished implementing full support for Linux on
[itch.io](https://utopixel.itch.io/outer-wonders)through a portable build of the game. - Polished the menus by adding a “
*Press any key to continue*” prompt on game startup, as well as a confirmation prompt for all quit buttons. - Tested the demo thoroughly on both Windows and Linux to fix all bugs and level design issues.



![Enemy Formations](../../assets/48e0b8558ce3518e.gif)

[Theta Wave](https://github.com/amethyst/theta-wave) is an open-source space shooter game by developers [@micah_tigley](https://twitter.com/micah_tigley) and
[@carlosupina](https://twitter.com/carlosupina). It is one of the showcase games for the [Amethyst Engine](https://amethyst.rs/). In
the past month, the [“Formations”](https://github.com/amethyst/theta-wave/releases/tag/v0.1.5) update was released which organized how mobs
are spawned in different phases of the level.

They are now working on the [“Loot”](https://github.com/amethyst/theta-wave/projects/4) update which will enhance how loot drops
are rolled, spawned, and how their effects are applied to the game.

[Station Iapetus](https://github.com/mrDIMAS/StationIapetus) by [@mrDIMAS](https://github.com/mrDIMAS) is a 3rd person shooter on the
prison Iapetus near Saturn.
This month’s updates include:

- New level (lab)
- More assets
- Performance improvements
- Bots now able to use weapons
- Melee attacks are much harder to avoid now
- Bots drop items
- Journal

## Engine Updates [#](https://gamedev.rs#engine-updates)

[macroquad](https://github.com/not-fl3/macroquad) is a cross-platform (Windows/Linux/macOS/Android/iOS/WASM) game
framework built on top of [miniquad](https://github.com/not-fl3/miniquad).

This month macroquad finally got out of alpha and `0.3`

got released!
All the examples with both sources and interactive wasm versions may
be found on [the new macroquad website](https://macroquad.rs/examples).

[Tetra](https://github.com/17cupsofcoffee/tetra) is a simple 2D game framework, inspired by XNA, Love2D, and Raylib. This
month, version 0.6.3 was released, featuring:

- BMFont support
- An
`ImageData`

type for loading and manipulating images on the CPU - More color utilities, including shortcuts for premultiplied alpha
- Bugfixes and docs improvements

For more details, see the [changelog](https://github.com/17cupsofcoffee/tetra/blob/main/CHANGELOG.md#063---2021-04-09).

Additionally, [Tetra’s website](https://tetra.seventeencups.net/) has been updated to make it easier
to read and contribute to. The site features tutorials, guides and FAQs on how to
use Tetra effectively, as well as a showcase of cool projects made using the
framework - additions are welcomed!

![Oxygengine UI splash screen](../../assets/b4ad68a60456f89c.gif)

[Oxygengine](https://github.com/PsichiX/Oxygengine) by [@PsichiX](https://twitter.com/psichix) is the hottest
HTML5 + WASM game engine for games written in Rust with web-sys.
The goal of this project is to combine professional game development tools under
one highly modular toolset.

This month’s changes include:

- Fixed bugs with rendering images on Firefox browser.
- Added support for filters.
- Updated
[RAUI](https://github.com/PsichiX/raui)dependency to improve UI. - Added support for image smoothing render command.
- Added
[puzzle game demo WIP](https://github.com/PsichiX/Oxygengine/tree/master/demos/soulhunter)that shows how to use RAUI to make for example fancy splash screens with RAUI.

![rg3d](../../assets/51f705e3ccac5e91.png)


[rg3d](https://github.com/mrDIMAS/rg3d) ([Discord](https://discord.gg/xENF5Uh), [Twitter](https://twitter.com/DmitryNStepanov)) is a game engine that
aims to be easy to use and provide a large set of out-of-box features. Some of
the recent engine updates:

- WebAssembly support (
[check online demo](https://rg3d.rs/assets/webexample/index.html)) - Proc-macro for Visit trait
- On-demand texture compression
- Performance improvements
- Various bug fixes and small improvements.

![arcana](../../assets/94895cc178ee6251.gif)

[Arcana](https://github.com/zakarumych/arcana) is a new game engine built with focus on ease of use
without compromising on level of control.
The engine is aimed to support a wide variety of games,
from pixel-art to fully ray-traced,
from single-player puzzles to online strategies.

It is at a very early stage, not all necessary subsystems are done and code is in flux.

The demo shown above was coded in a single evening, together with sprite sheet loading and sprite animations which will be integrated into the engine later.

The default 2D renderer renders sprites with auto-batching,
so all sprites are rendered in single instanced draw call,
allowing rendering millions of sprites in one frame. Rendering
is done with [ sierra](https://github.com/zakarumych/sierra) - a Vulkan-like graphics API with
batteries included. The engine also uses

[as its ECS, and rolls its own simplistic](https://crates.io/crates/hecs)

`hecs`

`System`

trait to define and run
systems, once per frame or with fixed steps. [physics is integrated for 2D cases, but this system is kept opt-in.](https://rapier.rs/docs/)

`rapier`

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

The Unofficial Bevy Cheatbook by @jamadazi is a practical book for learning the
[Bevy Game Engine](https://bevyengine.org).

The book recently got an assortment of improvements and new content, including
a detailed page about [input handling](https://bevy-cheatbook.github.io/features/input-handling.html) and a chapter about
[browser games using WASM](https://bevy-cheatbook.github.io/platforms/wasm.html) (written with help from @Zaszi).

The author now has a [GitHub Sponsors](https://github.com/sponsors/jamadazi), support them!

[@camsjams](https://twitter.com/camsjams) released [a video](https://youtube.com/watch?v=T1ZT0EkzvgI) about
developing a shooting gallery using Bevy
to demonstrate 2D games with multiple layers of depth.
Some of the features covered in the video:

- Basic UI with score and countdown clock.
- 2D shooting with moving set pieces - clouds, grass, water.
- Tracking of target hits, each target having their own unique movement speed and points.
- Game over state when clock runs out.

[TanTan](https://twitter.com/TantanDev) released a [video](https://youtube.com/watch?v=KEQIWqSq42k) about making a water shader,
loading 3D models, creating a beautiful transition shader
using glium and macroquad.
The water & transition shader is open source and can be found
[here](https://github.com/TanTanDev/macroquad_tantan_toolbox).



![Rust Linz talk screenshot](../../assets/d87b5f2af99f860e.png)

As part of April’s Rust Linz meetup, [Herbert Wolverson](https://twitter.com/herberticus)
gave a talk about using game development as a means of learning
Rust, stepping through the creation of Flappy Dragon - a simple game
used in his book ‘Hands-On Rust’ to teach the language basics.

‘Hands-On Rust’ is currently available for 50% off, via a coupon
posted on the [author’s twitter](https://twitter.com/herberticus/status/1387090355250675716).



![Rust LA talk screenshot](../../assets/01c89426a0b48cc6.png)

As part of April’s Rust LA meetup, [Andrea Pessino](https://twitter.com/AndreaPessino) from
[Ready at Dawn](http://www.readyatdawn.com/) gave a talk examining how to increase Rust adoption
among game developers and performance-centric developers, giving
practical, actionable advice to those who hit early bumps in their
Rust discovery.

![How To Write a Crash Reporter](../../assets/cfbb630399b7c1f4.jpg)


[@masonremaley](https://twitter.com/masonremaley) wrote [an article](https://www.anthropicstudios.com/2021/03/05/crash-reporter/) walking
through [Way of Rhea’s](https://store.steampowered.com/app/1110620?utm_campaign=tmirgd&utm_source=n21) crash reporter implementation.

The article covers how to detect a crash, how to report a crash via chat services like Discord or Slack, and how to implement a robust native UI on Windows to handle requesting user consent to file the report, as well as some design considerations.

![logo](../../assets/b605230597913fc1.png)


[awesome-quads](https://github.com/ozkriff/awesome-quads) is a curated list of links to [miniquad](https://github.com/not-fl3/miniquad)/[macroquad](https://github.com/not-fl3/macroquad)-related
code & resources: libraries & plugins, games, examples, apps, docs, etc.
The list has more than 40 links atm:
feel free to write a PR if something isn’t mentioned yet.

## Library & Tooling Updates [#](https://gamedev.rs#library-tooling-updates)

![Screenshot of tree rendering](../../assets/65504a06c387ad0e.png)


[wgpu](https://github.com/gfx-rs/wgpu) is a [WebGPU](https://gpuweb.github.io/gpuweb/) implementation in Rust. It is safe, efficient,
and portable: can target both native (Vulkan/D3D/Metal) and the Web.

The team has rolled out gfx-hal-0.8 and wgpu-0.8 updates on crates!
Read [gfx-release-blog](https://gfx-rs.github.io/2021/04/30/release-0.8.html) for more details.

In April, the team implemented more validation on both the host and the shader
sides. [Naga](https://github.com/gfx-rs/naga)’s coverage of SPIR-V and MSL features is also greatly improved.

On the infrastructure side, [wgpu](https://github.com/gfx-rs/wgpu) integrated [profiling](https://github.com/aclysma/profiling) and got the first
[naga performance](https://github.com/gfx-rs/wgpu-rs/discussions/879) numbers, which looked promising.

[nalgebra](http://nalgebra.org) ([GitHub](http://github.com/dimforge/nalgebra), [Discord](http://discord.gg/vt9DJSW)) by [Dimforge](http://dimforge.com) is a general-purpose
linear-algebra library.

With its version 0.26, [nalgebra](http://nalgebra.org) replaced the use of [generic-arrays](https://docs.rs/generic-array/0.14.4/generic_array/) by
regular Rust arrays using const-generics. See the [blog-post](https://www.dimforge.com/blog/2021/04/12/integrating-const-generics-to-nalgebra/) to get all
the details! In particular, this results in significant benefits:

- Simpler generic programming with statically-sized vectors/matrices.
- Much simpler debugging: inspect the content of vectors/matrices more easily.
- Vectors and matrices with dimensions known at compile-time can be constructed in a const-fn context.

![Low poly car model](../../assets/4f7d3df6d4b6ecbc.jpg)

[Opensubdiv-petite](https://crates.io/crates/opensubdiv-petite) is a high level, selective, oxidized wrapper around Pixar’s
[OpenSubdiv](https://graphics.pixar.com/opensubdiv/docs/intro.html) [sudivison surface](https://en.wikipedia.org/wiki/Subdivision_surface) meshing and evaluation library. OpenSubdiv allows
for real time updates of the subdivided mesh if the topology of the control mesh
is stable (e.g. a deforming character in a game).

The crate comes with a trait for converting into a `bevy::Mesh`

and a [ bevy example](https://github.com/virtualritz/opensubdiv-petite/blob/master/opensubdiv-petite/examples/bevy.rs).

This is an early release. None of the GPU acceleration backends are yet
exposed on the Rust side. Contact [@virtualritz](https://github.com/virtualritz) is you want to help out with
that.

His [ tobj fork](https://github.com/virtualritz/tobj) also has a bunch new features that help loading OBJ files for
use with opensubdiv-petite. E.g. merging disconnected vertices during import.

The car model above was borrowed from [@quaternius](https://www.patreon.com/quaternius) low poly
[car collection on itch.io](https://quaternius.itch.io/lowpoly-cars).

This month, version 1.0 of [profiling](https://github.com/aclysma/profiling) was released on crates.io. 🎉 🎉

This crate provides a very thin abstraction over instrumented profiling crates
like `puffin`

, `optick`

, `tracing`

, `tracy`

, and `superluminal-perf`

.

Profiling is used by multiple projects including `gfx-hal`

, `rafx`

, and
`wgpu`

.

```
let executor = Executor::default();
let events = [executor.create_event_handle(), executor.create_event_handle()];
async fn wait_event(events: [EventHandle; 2], executor: Executor) {
executor.event(&events[0]).await;
executor.event(&events[1]).await;
}
executor.spawn(wait_event(events.clone(), executor.clone()));
assert_eq!(executor.step(), true);
assert_eq!(executor.step(), true);
executor.notify_event(&events[0]);
assert_eq!(executor.step(), true);
executor.notify_event(&events[1]);
assert_eq!(executor.step(), false);
```


[simple-async-local-executor](https://github.com/enlightware/simple-async-local-executor) by [Enlightware](https://enlightware.ch)
is a single-threaded polling-based executor suitable for use in games, embedded
systems or WASM.

This executor can be useful when the number of tasks is small or
if a small percentage is blocked. Being polling-based, in the general
case it trades off efficiency for simplicity and does not require any
concurrency primitives such as `Arc`

, etc.

[wasm_plugin](https://github.com/alec-deason/wasm_plugin) by @alec-deason is a
low-ish level tool for easily hosting WASM based plugins for modding or scripting.

The latest version now supports calling host functions from the plugin and more flexible serialization which allows plugins to be written in languages other than Rust.

It consists of two crates:

[wasm_plugin_host](https://lib.rs/crates/wasm_plugin_host)which wraps a wasmer instance with methods for calling functions on the guest plugin.[wasm_plugin_guest](https://lib.rs/crates/wasm_plugin_guest)which provides an attribute macro to easily import and- export functions to the host.

[egui](https://github.com/emilk/egui) by [@emilk](https://twitter.com/ernerfeldt) is an easy-to-use immediate mode GUI library in pure Rust.

This month [version 0.11](https://github.com/emilk/egui/blob/master/CHANGELOG.md) of egui was released, with many improvements,
including optimized to run almost twice as fast!

You can try out egui in the [online demo](https://emilk.github.io/egui).

[bevy_egui](https://github.com/mvlabat/bevy_egui) provides an [Egui](https://github.com/emilk/egui) integration
for the [Bevy](https://github.com/bevyengine/bevy) game engine.
It supports [bevy_webgl2](https://github.com/mrk-its/bevy_webgl2) and implements the full set of Egui features
(such as clipboard and opening URLs).

In April, [version 0.4](https://github.com/mvlabat/bevy_egui/blob/main/CHANGELOG.md) was released, providing an integration with
Egui 0.11 and implementing multiple windows support.

Try out the [online demo](https://mvlabat.github.io/bevy_egui_web_showcase/index.html).

![puffin_egui](../../assets/394f792e91e2aad2.gif)


[puffin_egui](https://github.com/emilk/puffin_egui) by [@emilk](https://twitter.com/ernerfeldt) is an easy-to-use integration
of the [puffin](https://github.com/EmbarkStudios/puffin) profiler for the [egui](https://github.com/emilk/egui) GUI library.

It has never been easier to add an in-game flamegraph profiler to your game!

[
](https://gamedev.rs/[rafx-webgl-demo](https:/aclysma.github.io/rafx/demo-web/index.html))
![Rafx WebGL 1.0 Demo](../../assets/3b1f849465a62452.png)


[click for live demo](https://aclysma.github.io/rafx/demo-web/index.html)!

[distill](https://github.com/amethyst/distill)asset pipeline. This month, frustum culling and a new OpenGL ES 2.0/WebGL 1.0 backend were added.

[@dvd](https://github.com/DavidVonDerau) revived the `rafx-visibility`

crate and implemented frustum culling.
Frustum culling greatly reduces draw call counts, improving frame rate
in certain scenes. The changes also improve consistency between various
rendering feature implementations (i.e. meshes, text etc.) and avoids running
the extract-prepare-submit pipeline on entities that are not visible.

[@aclysma](https://github.com/aclysma) implemented an OpenGL ES 2.0 backend. While ES2 cannot support all
functionality in `rafx-api`

, it provides very broad compatibility. This means
the core functionality of rafx-api can be used with almost any mobile device
or browser ([~98% web coverage](https://caniuse.com/?search=webgl).)

![RAUI Scroll Box](../../assets/510d58f39b8d8e59.gif)

[RAUI](https://github.com/PsichiX/raui) by [@PsichiX](https://twitter.com/psichix) is a Renderer Agnostic User
Interface crate that is based on declarative mode UI composition similar to
React.js and UE4 Slate system.

This month’s changes include:

- Moved from
`widget_hooks!`

and`widget_component!`

to`#[pre_hooks]`

and`#[post_hooks]`

macros. - Added
`PropsData`

and`MessageData`

derive macros. - Improved support for Scroll Box widgets to allow frictionless usage.
- Added use of Scroll Box in
[TODO demo app](https://github.com/PsichiX/raui/tree/master/demos/todo-app)to demonstrate how to use it.

![Ferris drawn in Graphite using the new drawing tools - Art credit: Uriopass](../../assets/198333e555a3e77f.png)

Graphite ([GitHub](https://github.com/GraphiteEditor/Graphite), [Discord](https://github.com/GraphiteEditor/Graphite/blob/master/README.md#discord),
[Twitter](https://twitter.com/GraphiteEditor)) is an in-progress vector and
raster graphics editor built on a nondestructive node-based workflow.

The team size has doubled in the past month — thank you to the new contributors! Since then, systems related to editor tools and data flow were added. The editor now has proper input behavior on the existing Rectangle and Ellipse Tools plus the new Shape and Line Tools while holding modifier keys. Pen Tool implementation has begun, supporting polylines. Shapes are now drawn with live previews.

Additional work has gone into improving render performance, building the color
system in the Rust backend, and adding initial support for displaying shapes
in the Layer Tree panel. [Try it right now in your browser.](https://editor.graphite.design/)

Graphite is making rapid progress towards becoming a nondestructive, procedural
graphics editor suitable of replacing traditional 2D DCC applications. Please
[join the Discord](https://github.com/GraphiteEditor/Graphite/blob/master/README.md#discord) - and consider asking for a tour of the
code and how you can help!

![Super Mario Bros. running in KindNES](../../assets/18754f3adca53f26.png)


[KindNES](https://github.com/henryksloan/kind-nes/releases/tag/v0.9.1-beta) by [@henryksloan](https://github.com/henryksloan)
is a new NES emulator that supports sound, controllers, and
much of the NES library.

KindNES is designed to strike a balance between performance, hardware accuracy, and code clarity. It directly emulates the CPU, graphics, and sound of the NES with minimal approximation. The code is intended to pair well with the NESdev wiki as a resource for learning about the NES.

KindNES is in a playable state, and is approaching a release version. Features planned before release include saving and an improved cross-platform GUI.

![Screenshot of Pong with debugger](../../assets/04c85d3aa8f1c1e2.jpg)

[Chip-8-rs](https://github.com/JonathanMurray/chip-8-rs) by @jonathanmurray is
a CHIP-8 emulator with some basic debugging functionality.

When running a game through the emulator, CHIP-8 instructions are listed next to the main display, with the currently executed one highlighted. By running at a very low clock-frequency (and pausing/resuming) you can step through a program one instruction at a time, to better understand how it works (or doesn’t work!).

See it in action on [YouTube](https://youtu.be/nVDJ5PZpPfI?t=72).

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[femtovg is looking for help with the wgpu backend](https://reddit.com/r/rust/comments/mfuo4m/femtovg_2d_vector_graphics_crate_is_looking_for).[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[gfx-rs’s “contributor-friendly” issues](https://github.com/gfx-rs/gfx/issues?q=is%3Aissue+is%3Aopen+label%3Acontributor-friendly).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[A/B Street’s “good first issue” issues](https://github.com/a-b-street/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/good%20first%20issue).

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!

**Discuss this post on**:
[/r/rust_gamedev](https://reddit.com/r/rust_gamedev/comments/n8g79b/this_month_in_rust_gamedev_21_april_2021),
[Twitter](https://twitter.com/rust_gamedev/status/1391415309421187076),
[Discord](https://discord.gg/yNtPTb2).