---
title: 'This Month in Rust GameDev #15 - October 2020'
url: https://gamedev.rs/news/015/
author: Rust GameDev WG
published: '2020-11-09'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 15th issue of the Rust GameDev Workgroup’s
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

Table of contents:

[Annual Survey from the Rust GameDev WG](https://gamedev.rs/news/015/#annual-survey-from-the-rust-gamedev-wg)[Game Updates](https://gamedev.rs/news/015/#game-updates)[Learning Material Updates](https://gamedev.rs/news/015/#learning-material-updates)[Library & Tooling Updates](https://gamedev.rs/news/015/#library-tooling-updates)[Popular Workgroup Issues in GitHub](https://gamedev.rs/news/015/#popular-workgroup-issues-in-github)[Requests for Contribution](https://gamedev.rs/news/015/#requests-for-contribution)

As we did [last year](https://rust-gamedev.github.io/posts/survey-01), we are once again running
a Rust Game Development Ecosystem Survey. It’ll only take 10 minutes,
and your responses help us better understand the state of our ecosystem
and where we should try to focus our collective efforts.

## Game Updates [#](https://gamedev.rs#game-updates)

![Landscape](../../assets/7c175c7de616573b.jpeg)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In October, lots of work was done on the UI, and a buff system. There was an overhaul done to the staff item that gives it new primary and secondary attacks. There has also been work done on the axe and bow. The cloud system was overhauled and brought a cheaper way to compute the 3D noise that the system uses. The skill bar was overhauled to implement a new design that could handle the new buff system. This was also the first overhaul in over a year. A SFX system is in the works to allow effects to be mapped to blocks, for sounds like crickets or birds.

You can read more about some specific topics from October:

[Modelling Process](https://veloren.net/devblog-88#gemu)[Staff Overhaul](https://veloren.net/devblog-89#staff-overhaul-by-sam)[New Skillbar and Buffs Visuals](https://veloren.net/devblog-89#new-skillbar-and-buffs-visuals-pfau)[Cloud Improvements](https://veloren.net/devblog-90#cloud-improvements-by-zesterer)[Buffs](https://veloren.net/devblog-91#buffs-by-sam)[Alignment and Hostility](https://veloren.net/devblog-91#alignment-and-hostility-by-adam)[Fixing CI](https://veloren.net/devblog-91#fixing-ci-by-xmac94x)

October’s full weekly devlogs: “This Week In Veloren…”:
[#88](https://veloren.net/devblog-88),
[#89](https://veloren.net/devblog-89),
[#90](https://veloren.net/devblog-90),
[#91](https://veloren.net/devblog-91).

In November, Veloren will release 0.8. Veloren will also be speaking at MiniDebConf on November 22nd.

![Healing sceptre](../../assets/f96918c3e24e6f89.jpeg)



![Leaderboard Histogram](../../assets/51f85d550505e8fe.gif)

[Crate Before Attack](https://cratebeforeattack.com) by [koalefant (@CrateAttack)](https://twitter.com/CrateAttack)
is a skill-based multiplayer game where frogs fight and race using their sticky
tongues as grappling hooks.

A [browser build](https://cratebeforeattack.com/play) can be played online.

Changes since the last update:

- Added a global leaderboard that visualizes Race and Training results in an interactive histogram.
- Tweaked frogs physics to make them more bouncy, added an option that would keep tongue connected as long as a key is being pressed.
[Online Ghosts](https://youtu.be/j87I8akUTkc)were added. One can now compete with real players instead of AI when playing Race mode.- Improved load-times: level graphics is now quantized with an 8-bit palette, signed distance fields that are used for collisions are now generated offline. Downloads are cached in an IndexedDB, so subsequent starts are even faster.
- Multiple bugs were fixed.

More details are in [September](https://cratebeforeattack.com/posts/20201001-september-update) and
[October](https://cratebeforeattack.com/posts/20201029-october-update) DevLog entries and in
[YouTube-channel](https://www.youtube.com/channel/UC_xMilPTLuuE5iLs1Ml9zow).

![Egregoria roads at night](../../assets/4399592940f4f686.jpg)


[Egregoria](https://github.com/Uriopass/Egregoria)’s objective is to become a granular society simulation,
filled with fully autonomous agents interacting with their world in real-time.

The [6th devlog](http://douady.paris/blog/egregoria_6.html) was published. Updates include:

- Island generation.
- Day/night cycle.
- Human AI via utility systems.
- Specs to
[legion 0.3](https://github.com/amethyst/legion)port.

See also [the recent video](https://www.youtube.com/watch?v=mfvAuvC-XLg) showcasing very basic AI.

Join [Egregoria’s Discord server](https://discord.gg/CAaZhUJ).

*Discussions:
/r/rust_gamedev*

![A/B Street on the web](../../assets/07cb96592e5b3682.png)


[A/B Street](https://abstreet.org) is a traffic simulation game exploring how small changes
to roads affect cyclists, transit users, pedestrians, and drivers. Any city
with OpenStreetMap coverage can be used!

Some of this month’s updates:

[web version](http://abstreet.s3-website.us-east-2.amazonaws.com/dev/)launched, powered by`winit`

,`glow`

, and other dependencies having support for WebAssembly;- an
[OpenStreetMap viewer](http://abstreet.s3-website.us-east-2.amazonaws.com/osm_demo/)with 100 cities imported; - “thought bubbles” for cars looking for parking, by
[Michael](https://github.com/michaelkirk); - slow portions of a trip highlighted in the info panel, by
[Sam](https://github.com/NoSuchThingAsRandom/);

### Worship The Sun [#](https://gamedev.rs#worship-the-sun)

![Worship The Sun](../../assets/04189d43a723e410.jpg)

Worship The Sun is a dark, mysterious 2D puzzle-platform game with computer science themes. It introduces the player to a rich language of puzzle elements and challenges them to solve difficult puzzles that require experimentation, comprehension, and internalisation of the game’s mechanics.

The game is built using a custom engine that sits on top of [legion](https://github.com/amethyst/legion),
[wgpu](https://github.com/gfx-rs/wgpu), and a handful of other crates. It features dynamic lighting, a
flexible particle system, bespoke collision behaviour, and a Vim-inspired level
editor. The majority of game assets are hand drawn in [Procreate](https://procreate.art/)
and painstakingly animated.

The game is a few months into development with a release target of late 2021.
You can read about how swimming was added to the game in [GameDev Note 1:
Taking the Plunge](https://tuzz.tech/blog/taking-the-plunge) which contains a sneak peek at some of the levels.
For updates and possible playtesting opportunities, follow
[@chrispatuzzo](https://twitter.com/chrispatuzzo) and a [/r/WorshipTheSunGame](https://reddit.com/r/WorshipTheSunGame) subreddit.

![Garden](../../assets/001cc0bbaad80d97.png)

[Garden](https://www.cyberplant.xyz) is a procedural tree-growing, strategical ecosystem-restoration
and biological simulation game with an infinite amount of plant species where
every leaf is simulated, and the natural resources are scarce.
Every specimen is unique, as the plants grow by responding to the live changes in
the environment.
The player has to balance many complex mechanics to sustain life and go
forward in the game.
The game and the custom engine are developed in Rust with an OpenGL backend.

Garden developers (temporary name) are preparing for a demo release in a couple of months by tying everything together into a coherent experience. The game is also continually optimized to run on less powerful GPUs, so that everyone can enjoy it.

Some of the [updates from the October devlog](https://cyberplant.xyz/posts/october_2020):

- Near-infinite variety of plant species achieved through treating branch segments as Markov chains (enabling different growth speeds and probabilities for other segment types’ growth from one another) and simulating photosynthesis as an electrical circuit (enabling sugar storage in the form of root vegetables, for example).
- Concrete brick destruction mechanics were implemented. Dust particles for the animation that appears upon breaking, as well as the debris, were also added to the game.
- Saving and loading are almost complete.
- A watering can was added.
- Smoother soil and debris outlines.

Follow the developers [@logicsoup](https://twitter.com/logicsoup) and [@epcc10](https://twitter.com/epcc10) on Twitter for more updates.

[Akigi](https://akigi.com) is a WIP online multiplayer game.

In October, more progress was made on the editor tool for placing entity spawn points. Work was started on prototyping the hunting skill. Functionality was added to allow focusing for TextAreas in the user interface. Improvements were made to the engine’s asset management code to make it more generalized.

Full devlogs:
[#087](https://devjournal.akigi.com/october-2020/087-2020-10-04.html),
[#088](https://devjournal.akigi.com/october-2020/088-2020-10-11.html),
[#089](https://devjournal.akigi.com/october-2020/089-2020-10-18.html),
[#090](https://devjournal.akigi.com/october-2020/090-2020-10-25.html).

![Sun Prison gameplay](../../assets/e59a29aec94fa8e9.gif)


[Sun Prison](https://github.com/ropewalker/sun_prison) by [Dima Lazarev](https://twitter.com/dmitrywithouti) is a WIP turn-based
meditation on Rubik’s cube, [Sokoban](https://github.com/ropewalker/bevy_sokoban), and roguelikes, being
implemented with [Bevy engine](https://bevyengine.org).
The game is in the very early stages of development,
but it is already possible to [get lost in the dark](https://twitter.com/dmitrywithouti/status/1309025584039768064)
or to be [eaten by zombies](https://twitter.com/dmitrywithouti/status/1309982656260648960).

Follow [@dmitrywithouti](https://twitter.com/dmitrywithouti) on Twitter for updates.

[Camp Misty](https://github.com/ReeCocho/camp-misty) is an asymmetric
multiplayer game played on the command line. The game is played with two
people. One of the players is a helpless victim searching for car parts. If
they find all of the parts, they can repair their car and escape the camp. The
other player is a ruthless killer who is trying to hunt down the victim.

The game was created as a learning exercise in about two weeks by
[@ReeCocho](https://github.com/ReeCocho), with contributions from the many helpful members of [/r/rust](https://reddit.com/r/rust).

![A small marketplace area with a few merchants](../../assets/6734f0ded2ff40d9.jpg)


Antorum Online is a micro-multiplayer online role-playing game by [@dooskington](https://twitter.com/dooskington).
The game server is written in Rust, and the current “official” client is being
developed in Unity. The server can be self-hosted, and the network protocol is
open, so even custom clients that adhere to the protocol can connect and play.

Two more devlogs were published this month, regarding work done to implement shops, character creation, and a few other features:

![game’s banner](../../assets/eb4bb68e45924cb8.png)


[The Honor Sagas](https://khonsulabs.itch.io/honorsagas) is an early-in-development 2d MMORPG project.
October was the first month of development, and [@ectonDev](https://twitter.com/ectonDev) wrote
[a postmortem](https://khonsulabs.itch.io/honorsagas/devlog/192252/the-honor-sagas-devtober-postmortem) of the progress made while participating
in [#Devtober](https://itch.io/jam/devtober-2020).

### Project YAWC [#](https://gamedev.rs#project-yawc)

![An in-progress game of Project YAWC.](../../assets/4e09020d98d79845.png)


Project YAWC is a turn-based strategy game in the style of Advance Wars in development by junkmail. October saw the release of Alpha 3, including dynamically generated info cards and minor networking changes. For inquiries or if you are interested in playtesting, contact projectyawc(at)gmail.com.

![Power Kick](../../assets/947178ffef22ab23.png)


[Power Kick](https://kakoeimon.itch.io/power-kick) is a one screen platform game inspired by similar old arcade games
like Bubble Bobble and SnowBros.
Your task is to hit the enemies till they get dizzy and then kick them out of
their misery to proceed to the next stage. The kicked enemies will hit the
colliding enemies with a possibility to create a chain reaction
(similar to the pushed snowball in SnowBros).

The game has 20 stages and in stage 10 and 20 you will face a helicopter boss.

Can be played solo on the web through WebAssembly or up to two players in the downloadable version: the first player with the keyboard and the second one with a joypad.

The development took around two weeks thanks to [macroquad](https://github.com/not-fl3/macroquad) and [hecs](https://crates.io/crates/hecs).

![rymd animated combat](../../assets/0a3ba89d81fdfae2.gif)


[rymd](https://profan.itch.io/rymd) by [@_profan](https://twitter.com/_profan) is a space shooter prototype made with [macroquad](https://github.com/not-fl3/macroquad).
Intended as a test platform for trying out rust for prototyping games and
particularly for game AI programming purposes.

Development started at the end of October, recent additions include:

- Basic enemy AI behaviour mostly based on steering behaviours.
- Possibly the world’s most nauseating physics-driven camera.
- Too many particles.

![walking through a forest](../../assets/30be8d8f8da34b3d.gif)


The [@pGLOWrpg](https://twitter.com/pglowrpg) (Procedurally Generated Living Open World RPG) is a long-term
project in development by [@Roal_Yr](https://twitter.com/Roal_Yr), which aims to be a text-based game with
maximum portability and [accessibility](https://youtu.be/_jgzAddgEPU)
and focus on replayability, interactions, and emergent narrative.

For the past month the main focus of the development was on:

- Improving the UI.
- Implementing the input autocomplete system.
- Implementing save data import and parsing.
- Implementing world navigation system.
- Implementing rudimentary CLI graphics (for debugging and some future use).

Main features of the reported (pre-alpha) version are:

- Ability to generate and explore one or many worlds (see previous news).

For main feature reports and dev blogs follow [@pGLOWrpg](https://twitter.com/pglowrpg) on Twitter.

![space shooter boss fight](../../assets/2b18d139d7d5833e.gif)


The [Space Shooter](https://github.com/amethyst/space_shooter_rs) project is a game in development by [Carlo Supina](https://twitter.com/carlosupina) and
[Micah Tigley](https://twitter.com/micah_tigley). It is a 2D “shoot-em-up” game that takes place in space and is
inspired by games like [Raiden](https://wikipedia.org/wiki/Raiden_(video_game)) and [Binding of Isaac](https://wikipedia.org/wiki/The_Binding_of_Isaac_(video_game)).

Recent development has been focused on creating an online book for documentation for the game. While still a work in progress, the following content is now available:

If you’re interested in hearing about planning
an effective code refactor for a project using ECS, make sure to check out
[How to Revive a Dead Rust Project](https://rustfest.global/session/22-project-necromancy-how-to-revive-a-dead-rust-project/) at [RustFest Global 2020](https://rustfest.global/).



![Jumping across walls minigame](../../assets/684e0a907a05d8f7.png)

[a demo video](https://youtu.be/sstqGppo7L4)

[Weegames](https://yeahross.itch.io/weegames) ([source code](https://github.com/yeahross0/weegames))
is a fast-paced minigame collection.

There are now 40 minigames in the collection. New features in the latest release include boss games and high scores.

![gameplay](../../assets/ea37a173696208f9.gif)


[Canon Collision](https://canoncollision.com) by [@rukai](https://twitter.com/thisIsRukai) is an Undertale + Homestuck
fan-made platform fighter with powerful tools for modding.

This month, he completed the abstractions needed for character-specific logic. Notable changes:

[toriel’s fireball](https://twitter.com/thisIsRukai/status/1302250049972314112)[wobbly fireball shaders](https://twitter.com/thisIsRukai/status/1299311125285142529)[items that can be picked up and thrown](https://twitter.com/thisIsRukai/status/1297507398693736448)[character specific logic](https://twitter.com/thisIsRukai/status/1314872752642297856)

![Simulation demo](../../assets/bfcda42ef8a6945e.gif)


[galaxy-sim.github.io](https://galaxy-sim.github.io) ([source](https://github.com/Katsutoshii/barnes-hut-rs)) by [@zephybite](https://twitter.com/zephybite) and [@joshikatsu](https://twitter.com/joshikatsu)
is a colliding galaxies simulation based on [Barnes-Hut and direct algorithms](https://en.wikipedia.org/wiki/Barnes-Hut_simulation).
The project is written using Rust, ThreeJS, and WASM.

*Discussions:
Twitter*

### Ludum Dare 47 [#](https://gamedev.rs#ludum-dare-47)

[Ludum Dare](https://ldjam.com/events/ludum-dare/47) is a regular game jam event,
during which developers create games from scratch in a weekend
based on a theme suggested by the community.

LD47’s theme was “Stuck in a loop”. Here are some of the games made with Rust:

-
[“The Island”](https://ldjam.com/events/ludum-dare/47/the-island)by[@kuviman](https://github.com/kuviman)([source code](https://github.com/kuviman/ludumdare47)).A multiplayer online sandbox game. Explore, craft, and try to escape the island (spoiler: you can not, you are stuck in a loop). The world regenerates where you don’t see.

Check out the devlog post:

[“LudumDare 47 - The Island”](https://blog.kuviman.com/2020/10/18/ludumdare47.html).![gameplay](../../assets/47a1a0f8fff67204.gif)

-
[“Time Ghosts”](https://ldjam.com/events/ludum-dare/47/time-ghosts)by[@Healthire](https://twitter.com/Healthire)([source code](https://github.com/Healthire/ld47)).You have a limited time to collect the next part for the Machine, when 12 seconds have passed time rewinds and you have to start over. But don’t worry, your past self is still around to repeat your past actions.

![gameplay](../../assets/85e5b9804e4d9f2d.png)

-
[“Quantum Loops”](https://ldjam.com/events/ludum-dare/47/quantum-loops)by[@necauqua](https://twitter.com/necauqua)([source code](https://github.com/necauqua/quantum-loops)).There is a particle forced to exist in a quantum loop and it really hates being real! Disrupt the quantum levels with most efficient use of your energy to let it escape back into nothing!

![gameplay](../../assets/d19af7cc727b20c8.gif)

-
[“Keep Inside”](https://ldjam.com/events/ludum-dare/47/keep-inside)by[@davidB](https://github.com/davidB)made with Bevy ([source code](https://github.com/davidB/ld47_keep_inside)).A solo pong on a circle.

![gameplay](../../assets/2845a4faec227fce.gif)

-
[“Keep Moving and Nobody Burns”](https://github.com/mockersf/kmanb)by[@FrancoisMockers](https://twitter.com/FrancoisMockers)made with Bevy ([source code](https://github.com/mockersf/kmanb)).Aim for the high score while avoid getting burned either by that big wall of fire or by your own bombs! Every round, the game will get harder, but you will earn more points. To help you, blowing up those crates may drop bonus that will make your bombs more useful.

![gameplay](../../assets/2f3bc485fc17b355.png)

-
[“Bloody Baron”](https://ldjam.com/events/ludum-dare/47/bloody-baron)by[@torresguilherme](https://github.com/torresguilherme)([source code](https://github.com/torresguilherme/bloody-baron)).You’re in a building with 9 other people, and one of them is a brutal killer. Don’t get caught by them, and use your abilities and your logic skills to solve the mystery and vote the right person in the trial!

![gameplay](../../assets/8ff3ed5823159b7f.png)

-
[“Soy Content”](https://ldjam.com/events/ludum-dare/47/soy-content)by[@walterpie](https://github.com/walterpie)made with Bevy ([source code](https://github.com/walterpie/ldjam-47)).A misleading puzzle game with a twist. Find your way in a non-euclidean maze of interconnected rooms. Warning: Game doesn’t contain any Soy.

![gameplay](../../assets/96e6843eaba229a9.png)


## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

### How to: WGPU + Winit + ECS + Pixels [#](https://gamedev.rs#how-to-wgpu-winit-ecs-pixels)

[@nyxtom](https://twitter.com/nyxtom) published several articles on game
development for Entity-Component-Systems, Windowing and Event Loops, and WGPU.

[ECS in Rust](https://nyxtom.dev/2020/10/06/ecs-in-rust/)- written as a high level introduction to entity component systems and using the[hecs](https://crates.io/crates/hecs)crate.[Winit and Pixels](https://nyxtom.dev/2020/10/07/winit-rust/)- introduces cross platform window management/event loops and provides a tutorial for writing simple pixel graphics and 2d game development using the[pixels](https://github.com/parasyte/pixels)crate (based on WGPU).[Framebuffers, WGPU and Rust](https://nyxtom.dev/2020/10/08/framebuffers/)- an in-depth analysis of high-level graphics terminology and a full length tutorial for setting up the api and clearing the screen with WGPU.

![Snake clone tutorial output](../../assets/05d9ceb66193617c.gif)

Bevy is a rapidly growing game engine written in Rust. This tutorial walks through creating a snake clone, introducing Bevy concepts on the way. The tutorial covers resources, systems, timers, entities, components, materials, creating a grid system, and spawning/despawning entities.

### Rust FFI: Microsoft Flight Simulator SDK [#](https://gamedev.rs#rust-ffi-microsoft-flight-simulator-sdk)

[@ryan_levick](https://gamedev.rs/news/015/twitter.com/ryan_levick) made two livestreams about Rust FFI and SDK for
Microsoft Flight Simulator 2020.
You can watch recordings here:

[Part 1](https://youtube.com/watch?v=jNNz4h3iIlw): bindgen, C ABIs, linkers, and more.[Part 2](https://youtube.com/watch?v=ugiR9M16fwg): more high-level concerns like API design and making an idiomatic API.

Subscribe to [@ryanlevick on Twitch](https://twitch.tv/ryanlevick) for future streams.

*Discussions:
/r/rust*

[@Therocode](https://twitter.com/therocode) published an [article](https://blog.therocode.net/2020/10/a-guide-to-rust-sdl2-emscripten) that
explains how to port games to the web using Emscripten.
It is not only useful if you have an existing game to port, but
also if you are looking for a starting point for a new application.

*Discussions:
/r/rust*

## Library & Tooling Updates [#](https://gamedev.rs#library-tooling-updates)

![tetris on rust-psp](../../assets/96b7de14dc855c55.jpg)


Move over Tetris Effect and Tetris 99, the first game has been created with
[rust-psp](https://github.com/overdrivenpotato/rust-psp), and it’s [Tetris](https://github.com/sajattack/rust-psp/tree/tetris/examples/tetris)! This was a big step because it proves that
rust-psp is ready for game development, even though it’s still `#![no_std]`

.
`std`

support is a work in progress, and the project is always open to new
contributors to the library, the tooling, or people who want to make PSP games
in Rust.

Another development for rust-psp this month is [reverse engineering](https://psp.re)
of the Sony library for the hardware vector floating point unit of the PSP.
All the vector and matrix operations provided by the Sony library have been
PR’ed to rust-psp’s main repo, and there are still more functions to come.

To stay up to date on [rust-psp](https://github.com/overdrivenpotato/rust-psp) development, you can join the project’s [Discord](https://discord.gg/tvGzD4GqvF)
or follow [@sajattack](https://twitter.com/sajattack) on Twitter.

![screenshot](../../assets/aba4c0ddea94a09f.png)


[gbemu](https://github.com/BlueBlazin/gbemu) by [@BlueBlazin](https://github.com/BlueBlazin) is a Gameboy/Gameboy Color Emulator which
[runs in the browser](https://gbemu.netlify.app).

… I wrote the emu just for myself as a learning experience. So it’s lacking in a lot of features you’d expect from one made for others to use, and it’s also not mobile-friendly unfortunately (but I’ll work on that soon). Still, it may be of some interest to someone here :D


*Discussions:
/r/rust*

![SSB & Rust logos](../../assets/2dbfb6ab837f75ab.png)


[skyline-rs](https://github.com/ultimate-research/skyline-rs) by [@jam1garner](https://twitter.com/jam1garner) is a project seeking to allow Rust code to
unofficially use the Nintendo Switch SDK focused on modding.

This month, [@jam1garner](https://twitter.com/jam1garner) made a blog post, [Rust for Modding Smash Ultimate](https://jam1.re/blog/rust-for-game-modding),
focused on detailing why Rust was such a good fit for modding games on the
Switch and his experience porting Rust to the Nintendo Switch.
It also features updates regarding:

- Crates for working with Nintendo and Namco textures formats
(
[bntx](https://github.com/jam1garner/bntx)and[nutexb](https://github.com/jam1garner/nutexb)). - An auto-updater client and server for Rustaceans writing Switch mods.
- The introduction of
[skyline-web](https://github.com/skyline-rs/skyline-web), a new library for working with the Switch’s web browser. - Additions to the
[skyline fork](https://github.com/jam1garner/rust-std-skyline)of the Rust standard library.

[shared-arena](https://github.com/sebastiencs/shared-arena) by [@0x5eb](https://twitter.com/0x5eb) is a thread-safe & efficient memory pool.
Memory pools are useful for speeding up dynamic (de)allocation
of large amounts of data of the same size.

shared-arena provides three memory pools with different trade-offs:

![SharedArena, Arena, Pool](../../assets/e165a72cfdaf553a.png)


The crate uses unsafe in a few places,
but the code is covered by the miri interpreter, valgrind and 3 sanitizers
(address, leak, and memory) [on each commit](https://github.com/sebastiencs/shared-arena/blob/master/.github/workflows).

*Discussions:
/r/rust*

[glam](https://github.com/bitshifter/glam-rs) is a simple and fast linear algebra crate for games and graphics.

This month v0.10.0 was released. There were a lot of additions in this update and a small breaking change.

-
The return type of

`Vec4::truncate()`

was changed from`Vec3A`

to`Vec3`

which is a breaking change and thus the version jumped from 0.9 to 0.10. -
Vector swizzle functions similar to those found in

[GLSL](https://www.khronos.org/opengl/wiki/Data_Type_(GLSL)#Swizzling)were added. Swizzle functions allow a vector’s elements to be reordered. The result can be a vector of a different size to the input. Swizzles are implemented with SIMD instructions where possible, e.g. for the`Vec4`

type.`let v = vec4(1.0, 2.0, 3.0, 4.0); // Reverse elements of `v`. // If SIMD is supported this will use a vector shuffle. let wzyx = v.wzyx(); let yzw = v.yzw(); // Swizzle the yzw elements of `v` into a `Vec3` let xy = v.xy(); // You can swizzle from a `Vec4` to a `Vec2` let yyxx = xy.yyxx(); // And back again`

-
[no_std](https://rust-embedded.github.io/book/intro/no-std.html)support was added, using[libm](https://github.com/rust-lang/libm)for math functions that are not implemented in`core`

. -
Optional support for the

[bytemuck](https://docs.rs/bytemuck)crate was added, this allows appropriate glam types to be cast into`&[u8]`

.

For a full list of changes see the [glam changelog](https://github.com/bitshifter/glam-rs/blob/master/CHANGELOG.md).

![output example](../../assets/bf1b04c0bb3da96c.png)


[density-mesh](https://github.com/PsichiX/density-mesh) by [@PsichiX](https://github.com/PsichiX) is an image density/height map to mesh generator.
It consists of two crates:

- density-mesh-core - generates mesh from density map.
- density-mesh-image - generates density map from image.

A typical use case would be to use two of them to create mesh from images but in case you have your own image handler, you can stick to the core module and produce density maps by yourself.

There’s also a [CLI tool](https://github.com/PsichiX/density-mesh#cli).

*Discussions:
/r/rust*

[Rapier](https://rapier.rs) is a set of 2D and 3D physics engines for games, animation and
robotics written in Rust.

[This month](https://www.dimforge.com/blog/2020/11/01/this-month-in-dimforge/) the version 0.3.0 has been released with exciting
new features:

- cylinders and cones as collider shapes;
- collision groups (with bit masks) and collision filters (with callbacks) for deciding what pairs of colliders can touch;
- the ability to set the mass of rigid-bodies explicitly;
- linear and angular damping, to progressively slow down rigid-bodies;
- the ability to attach some user-defined data (of type
`u128`

) to any collider or rigid-body.

The [bevy_rapier](https://www.rapier.rs/docs/user_guides/rust_bevy_plugin/getting_started) plugin for the Bevy game engine has been updated to support
all the aforementioned features.

Finally, a [continuous benchmarking](https://www.dimforge.com/blog/2020/10/01/this-month-in-dimforge#rapier-continuous-benchmarking) infrastructure has been set
up to make sure performance regressions can be detected early.

[Physme](https://github.com/walterpie/physme) is not your typical physics engine. It doesn’t exactly simulate
real world physics and it never will. Instead, it has only two goals:

- To provide satisfying real-time dynamics for 2D and 3D games.
- To have a simple to use API.

Physme will only work with [bevy](https://bevyengine.org) and is not made to support other game
engines.
The current release supports bevy 0.2, but work is being done to support
bevy 0.3.

The current feature set includes:

- Rigid bodies
- Multiple colliders per body
- Static and semikinematic bodies
- Sensor bodies
- Oriented bounding boxes
- Fixed, mechanical and spring joints
- Broad phase

All of the above-listed features are supported in both 2D and 3D.

[Mun](https://mun-lang.org) is a scripting language for gamedev focused on quick iteration times
that is written in Rust.

[October updates](https://mun-lang.org/blog/2020/10/31/this-month-october) include:

- a plugin for mdbook to test Mun code;
- support for modules and visibility;
- the ability to generate enum ABI types;
- bug fixes and other improvements.

![Meshing Example](../../assets/db8cc23736e61e70.gif)


[Building Blocks](https://github.com/bonsairobo/building-blocks) by [@bonsairobo](https://github.com/bonsairobo)
is an engine-agnostic voxel library that implements real-time data structures
and algorithms for: edits on compressed maps, meshing, search, and collisions.

The library has recently seen two releases:

To prove out the functionality of the library, the [voxel-mapper](https://github.com/amethyst/voxel-mapper)
project was ported to use building-blocks instead of ilattice3.
This resulted in improved performance and memory usage
when doing large edits and working with large maps:

![Terraforming demo](../../assets/fd8cb9def3067ba0.gif)


Join [Building Blocks’s Discord server](https://discord.gg/CnTNjwb).

![Rust GPU Sky](../../assets/6da23f42e218c74a.jpg)

[Rust GPU](https://github.com/EmbarkStudios/rust-gpu) is a project backed by [Embark Studios](https://www.embark-studios.com/)
to make Rust a first-class language and ecosystem for building GPU code.

Although still in very early stages of development,
[Rust GPU released v0.1 in October](https://github.com/EmbarkStudios/rust-gpu/releases/tag/v0.1),
and has already garnered over 2000 stars on GitHub.
Currently, compiling and running very simple shaders
works, and a significant portion of the core library also compiles. While things
like if-statements and while-loops are working, many things aren’t implemented yet.
For example, for-loops, iterators and match/switch aren’t supported yet. That
means that while being technically usable, Rust GPU is far from being
production-ready.

The motivation behind the project:

Historically in games, GPU programming has been done through writing either HLSL, or to a lesser extent GLSL. These are simple programming languages that have evolved along with rendering APIs over the years. However, as game engines have evolved, these languages have failed to provide mechanisms for dealing with large codebases, and have generally stayed behind the curve compared to other programming languages.

In part this is because it’s a niche language for a niche market, and in part this has been because the industry as a whole has sunk quite a lot of time and effort into the status quo. While over-all better alternatives to both languages exist, none of them are in a place to replace HLSL or GLSL. Either because they are vendor locked, or because they don’t support the traditional graphics pipeline. Examples of this include CUDA and OpenCL. And while attempts have been made to create language in this space, none of them have gained any notable traction in the gamedev community.


The code for the sky example above:

```
#[spirv(entry = "fragment")]
pub fn main_fs(input: Input<Vec4>, mut output: Output<Vec4>) {
let dir: Vec3 = input.load().truncate();
let cs_pos = Vec4(dir.0, -dir.1, 1.0, 1.0);
let ws_pos = {
let p = clip_to_world.mul_vec4(cs_pos);
p.truncate() / p.3
};
let dir = (ws_pos - eye_pos).normalize();
let color = sky(dir, sun_pos); // evaluate Preetham sky model
output.store(color.extend(0.0))
}
```


*Discussions:
/r/rust,
Hacker News,
Twitter*

gfx-rs support for D3D has been improved. [@kvark](https://github.com/kvark) landed a few critical fixes
in the DX12 backend, including the proper handle freeing, compressed textures
support, blend factors, and debug markers.

[@cwfitzerald](https://github.com/cwfitzgerald) brought DX11 backend practically to the 1st tier with titanic
work spread over a dozen of pull requests.
It is now able to run [bve-reborn](https://github.com/BVE-Reborn/bve-reborn) correctly:

![bve-reborn on dx11](../../assets/85500b0cb71d0b90.jpg)


The `ggez`

game library traditionally tries to make at least one release
at the end of each year, and that is fast approaching. While the
graphics engine rewrite is still a work in progress, there’s plenty of
other useful updates to be made. Bugfixes, dependency updates, and other
ergonomic fixes are all on the table. A lot of work has already been
done: removing `nalgebra`

from the public API in favor of just using
`mint`

, re-working some dependencies to improve build times, and
updating and cleaning up a pile of minor issues. However, there’s still
about a hundred accumulated bugs and PR’s to triage and figure out, and
a lot of testing to do. Please help! The release checklist is
available [here](https://github.com/ggez/ggez/milestone/6).

![miniquad_wayland](../../assets/c1c1d5962e254e78.gif)

[miniquad](https://github.com/not-fl3/miniquad) is cross-platform windowing and rendering library.

This month two big PRs got into the final review stage:

[Native Wayland support](https://github.com/not-fl3/miniquad/pull/152): as usual, no third-party dependencies or C code involved; Clean build time for Wayland examples are about 3s.[The Metal backend PR](https://github.com/not-fl3/miniquad/pull/135)showed good signs of life,[quad](https://github.com/not-fl3/miniquad/blob/master/examples/quad.rs)and[offscreen](https://github.com/not-fl3/miniquad/blob/master/examples/offscreen.rs)examples got successfully run on Metal.

![macroquad-gif](../../assets/1cd92572ca620405.gif)

[macroquad](https://github.com/not-fl3/macroquad) is a cross-platform (Windows/Linux/macOS/Android/iOS/WASM)
game framework built on top of [miniquad](https://github.com/not-fl3/miniquad).

This month was about polishing 0.3-alpha version. Important things that got fixed:

- Text rendering was reimplemented with
[fontdue](https://github.com/mooman219/fontdue):[example](https://github.com/not-fl3/macroquad/blob/master/examples/text.rs),[web demo](https://not-fl3.github.io/miniquad-samples/macroquad_text.html). - A long-term
[issue with Android resources system](https://github.com/not-fl3/macroquad/issues/45)got fixed. - Particle system was released:
[example](https://github.com/not-fl3/macroquad/blob/master/particles/examples/particles.rs), [web demo][particles-web-demo].

And special shoutout goes to [donuts](https://github.com/cedric-h/donuts) game by [@cedric-h](https://github.com/cedric-h) - a simple game
made in a couple of days, like a jam game.
It’s a really good showcase of macroquad’s approach to simple game code
that allows hardcoding and hacks for empowering gameplay experiments.

[rg3d](https://github.com/mrDIMAS/rg3d) is a game engine that aims to be easy to use and provide large set
of out-of-box features. Some of the recent updates:

- Implemented fully asynchronous resource loading.
- Added compressed textures support (DXT1, DTX3, DTX5).
- Added filtering and wrapping options for textures.
- Added sky box.
- Added texture import options for resource manager.
- All dependencies were moved to rg3d workspace, so there is no need to manually download them when working with the latest version of the engine.
- Extracted HRTF code in the separate
[crate](https://github.com/mrDIMAS/hrtf), so it could be used without rg3d. - Lots of other bugfixes and improvements.

Join the [rg3d’s Discord channel](https://discord.gg/xENF5Uh)
or follow [Dmitry Stepanov on twitter](https://twitter.com/DmitryS36934349).

[Bevy](https://bevyengine.org) is a refreshingly simple data-driven game engine built in Rust.
It is [free and open source](https://github.com/bevyengine/bevy) forever!

This month, thanks to 59 contributors, 122 pull requests, and their
[generous sponsors](https://github.com/sponsors/cart), Bevy 0.3 was released. You can view the
[full Bevy 0.3 announcement here](https://bevyengine.org/news/bevy-0-3). Here are some highlights:

- Initial Android and iOS support
- Asset system improvements:
- Asset handle reference counting
- Asset loaders can now load multiple assets
- Sub asset loading
- Asset dependencies

- GLTF scene loader
- Bevy ECS improvements
- Query ergonomics: query.iter() returns a real iterator now!
- 100% lockless parallel ECS
- Performance improvements
- Thread local resources

- Flexible mesh vertex attributes and index buffer specialization
- WASM asset loading, touch input, transform re-rewrite, gamepad settings, plugin Groups, dynamic Window Settings, documentation search-ability.

*Discussions:
/r/rust,
hacker news,
twitter*

Community updates:

[bevy_rapier 0.5](https://rapier.rs/docs/user_guides/rust_bevy_plugin/getting_started): The Rapier Physics project released updates to their official Bevy plugins, which add support for Bevy 0.3 as well as the latest Rapier features[announced here](https://www.dimforge.com/blog/2020/11/01/this-month-in-dimforge).[bevy_easings](https://crates.io/crates/bevy_easings): A plugin for easing a component value to another value, mainly used to animate transition between two transforms, but usable for other components.[bevy_miniquad](https://github.com/smokku/bevy_miniquad): A plugin replacing winit windowing and render pipeline with[miniquad](https://github.com/not-fl3/miniquad)library.[physme](https://github.com/walterpie/physme): A simplistic physics engine for both 2D and 3D simulation. Physically inaccurate, but feels satisfying and is easy to use.[bevy_networking_turbulence](https://github.com/smokku/bevy_networking_turbulence): Networking plugin running on[naia-socket](https://github.com/naia-rs/naia-socket)and[turbulence](https://github.com/kyren/turbulence)libraries.[Making a Snake Clone](https://mbuffett.com/posts/bevy-snake-tutorial/): Walkthrough on how to make a snake clone.[bevy_tilemap](https://github.com/joshuajbouw/bevy_tilemap): A plugin with generic types for rendering multi-threaded chunk-based tile maps.[Keep Inside](https://github.com/davidB/ld47_keep_inside): A solo pong on a circle (made for Ludum Dare 47)[Keep Moving and Nobody Burns](https://github.com/mockersf/kmanb): A bomberman against time (made for Ludum Dare 47)

Join the Bevy’s [Discord](https://discord.com/invite/gMUk5Ph), [/r/bevy subreddit](https://reddit.com/r/bevy),
and follow [@BevyEngine on Twitter](https://twitter.com/BevyEngine).

[Tetra](https://github.com/17cupsofcoffee/tetra) is a simple 2D game framework, inspired by XNA and Raylib. This month,
versions 0.5.1 and 0.5.2 were released, fulfilling some long-standing feature
requests:

- Custom error types can now be used in your game loop
- Custom shaders gained support for multiple texture samplers and color uniforms
- Methods were added to
`Texture`

and`Canvas`

for writing pixel data at runtime - Various helpful
`std`

traits were implemented for`Color`


For full details and a list of breaking changes, see the [changelog](https://github.com/17cupsofcoffee/tetra/blob/main/CHANGELOG.md).

[ogmo3](https://github.com/17cupsofcoffee/ogmo3) is a Rust crate for parsing projects and levels created with
[Ogmo Editor 3](https://ogmo-editor-3.github.io/). It is loosely modeled after `ogmo-3-lib`

, the Haxe reference
implementation of an Ogmo level parser.

This month, it was released onto crates.io for the first time, and a
[full example](https://github.com/17cupsofcoffee/ogmo3/blob/main/examples/sample.rs) was added, showing how a simple project can be
loaded into a game engine.

![Demo: sponza atrium](../../assets/3ac4d94f1040a45f.png)


[Wilds](https://github.com/zakarumych/wilds) is very early in development game engine.

It features a renderer that uses Vulkan [ray-tracing extension](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/man/html/VK_KHR_ray_tracing.html) supported
by NVidia RTX cards and future AMD cards.
Screenshot above is rendered using [DDGI](https://morgan3d.github.io/articles/2019-04-01-ddgi/) technique implemented exclusively
with Rust and GLSL for shaders.
In the whole scene there is only one directional light source - “sun” -
and no “ambient” light.
All geometry in viewport is shadowed from “sun” and is lit with diffuse
illumination.

To keep things as simple as possible the engine uses [Hecs](https://crates.io/crates/hecs) - minimalistic
ECS library.
Assets are loaded asynchronously using [Goods](https://github.com/zakarumych/goods) asset manager.

Traditional rasteriazation rendering pipeline and support [wgpu](https://github.com/gfx-rs/wgpu) backend are planned
to support wider range of platforms/hardware.

Implementing GUI system and basic editor is also a priority goal.

Follow progress [on Twitter](https://twitter.com/zakarum4).
Contributions and feedback are always welcome.

![output example](../../assets/1ef9d49df99b4e32.png)


[fastnbt](https://github.com/owengage/fastnbt) by [@owengage](https://github.com/owengage) is a fast parsing library
for Minecraft’s NBT and Anvil formats.

The project consists of several crates:

- fastnbt - fast deserializer and parser for Minecraft: Java Edition’s NBT data format.
- fastanvil - for rendering Minecraft worlds to maps.
- fastnbt-tools - various tools for NBT/Anvil, notably a map renderer.
- anvil-wasm - an entirely in-the-browser map renderer.
Demo at
[owengage.com/anvil](https://owengage.com/anvil).

The project supports only the latest version of Minecraft (1.16 at the moment).

*Discussions:
/r/rust*

### mcproto [#](https://gamedev.rs#mcproto)

mcproto by [@Twister915](https://github.com/Twister915) is an implementation of the Minecraft multiplayer
network protocol in Rust. It consists of three crates:

[mcproto-rs](https://github.com/Twister915/mcproto-rs)- the protocol itself,[mctokio](https://github.com/Twister915/mctokio)- tokio I/O stuff,[rustcord](https://github.com/Twister915/rustcord)- a layer 7 server-switching proxy implementation (WIP).

*Discussions:
/r/rust*

[Ajour](https://getajour.com) is a World of Warcraft addon manager written in Rust using [Iced](https://github.com/hecrj/iced) as GUI
library. The project is completely advertisement free, privacy respecting, and
open source.

October updates include:

- Catalog support for installing addons.
- Beta, PTR support.
- Release channels on addons.
- CLI options to run Ajour headless.
- Community driven API.

Join the [Discord server](https://discord.com/invite/ajour) and say hi.

In addition to adding Linux Support for more Windows-exclusive games,
Valve Software’s wine-based translation layer for Linux: Proton now
includes Rust as part of its build system.
[Media Converter](https://github.com/ValveSoftware/Proton/tree/proton_5.13/media-converter), is a Proton module
written in Rust as a gstreamer plugin to convert certain media encodings
from one format to another.

Documentation for building Proton is available on [GitHub](https://github.com/ValveSoftware/Proton).
Further documentation on Media Converter and its source code is available
on the module’s [repository](https://github.com/ValveSoftware/Proton/tree/proton_5.13/media-converter)

## Popular Workgroup Issues in GitHub [#](https://gamedev.rs#popular-workgroup-issues-in-github)

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[winit’s “Good first issue” and “help wanted” issues](https://github.com/rust-windowing/winit/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+label%3A%22status%3A+help+wanted%22+label%3A%22Good+first+issue%22).[gfx-rs’s “contributor-friendly” issues](https://github.com/gfx-rs/gfx/issues?q=is%3Aissue+is%3Aopen+label%3Acontributor-friendly).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[A/B Street’s “good first issue” issues](https://github.com/dabreegster/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/good%20first%20issue).

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!