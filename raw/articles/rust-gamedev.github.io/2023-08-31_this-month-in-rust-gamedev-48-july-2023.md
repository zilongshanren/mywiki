---
title: 'This Month in Rust GameDev #48 - July 2023'
url: https://gamedev.rs/news/048/
author: Rust GameDev WG
published: '2023-08-31'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 48th issue of the Rust GameDev Workgroup’s
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

[Announcements](https://gamedev.rs/news/048/#announcements)[Game Updates](https://gamedev.rs/news/048/#game-updates)[Engine Updates](https://gamedev.rs/news/048/#engine-updates)[Learning Material Updates](https://gamedev.rs/news/048/#learning-material-updates)[Tooling Updates](https://gamedev.rs/news/048/#tooling-updates)[Library Updates](https://gamedev.rs/news/048/#library-updates)[Other News](https://gamedev.rs/news/048/#other-news)[Discussions](https://gamedev.rs/news/048/#discussions)[Requests for Contribution](https://gamedev.rs/news/048/#requests-for-contribution)

## Announcements [#](https://gamedev.rs#announcements)

The 29th Rust Gamedev Meetup took place in July.
You can watch the recording of the meetup [here on YouTube](https://youtu.be/47wamZL5IFw).
The schedule:

The meetups take place on the second Saturday of every month
via the [Rust Gamedev Discord server](https://discord.gg/yNtPTb2)
and are also [streamed on Twitch](https://twitch.tv/rustgamedev).

## Game Updates [#](https://gamedev.rs#game-updates)

![tiled map with lots of grass and trees, some resources and a couple of named pawns](../../assets/b606ed0f33ab44b1.png)


[Colony](https://github.com/ryankopf/colony) by [@ryankopf](https://github.com/ryankopf) is a colony simulator game built with Bevy that
is open source and is in a pre-alpha stage. Similar to other colony simulator games
like Dwarf Fortress or Rimworld, there are units that have their own traits and
can be instructed to perform tasks like farming and chopping trees.

You can have your units build things, farm stuff, and explore, and the game is soon to be moving onto adding more content and UI, as core features are being completed.

*Discussions: /r/rust*

![OpenCombat completed HUD](../../assets/a17af6c74f6c59e5.jpg)

Open Combat ([Website](https://opencombat.bux.fr), [GitHub](https://github.com/buxx/OpenCombat),
[Discord](https://discord.gg/6P2vtFh2Px)) is a real-time tactical game
which takes place during the 2nd World War.

Some major changes this month:

- HUD has been filled with a minimap and squad information.
- Multiple issues about zoom and move on map have been fixed.
- A high-definition map has been created.

Some fixes and improvements have to be done, but the devs are near to publishing the official demo of the game!

![Universal quic server](../../assets/a4f9553fa4fb674f.jpg)

CyberGate ([YouTube](https://youtube.com/channel/UClrsOso3Xk2vBWqcsHC3Z4Q), [Discord](https://discord.gg/R7DkHqw7zJ)),
CyberSoul is developing an ambitious multiplayer project,
utilizing procedural generation and AI to offer a dynamic universe.

The latest updates to CyberGate include:

- Implemented a Webtransport Client and a universal quic server.
- A custom game launcher that is reliable and efficient.
- Universal mechanism to save, load, and upgrade the game world from disk.
- Optimized multithreaded evolution algorithms for generating universes.
- Created an accessible editor for fine-tuning component values.

Participate in Testing and Engage with CyberSoul: [on Discord](https://discord.gg/R7DkHqw7zJ).

[Way of Rhea](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n48) is a puzzle game with hard puzzles but forgiving
mechanics being produced by [@masonremaley](https://twitter.com/masonremaley) in a custom Rust engine.
You can support development by [checking out the free demo and wishlisting on Steam](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n48)
or [signing up for the mailing list](https://anthropicstudios.com/newsletter/signup/tech)!

Recent updates:

- Way of Rhea now natively supports Linux, and Steam Deck! Mason released a
[writeup on the port here](https://anthropicstudios.com/2023/08/21/way-of-rhea-linux). - Way of Rhea was part of the
[Cerebral Puzzle Showcase](https://cerebralpuzzleshowcase.com). - Crash handling was improved, and the build process was simplified (necessary
for post-release support).
A fix was landed to
[backtrace-rs](https://github.com/rust-lang/backtrace-rs/pull/553)as part of the improved crash handling. - Time controls were released as part of the updated demo.

![tiny-snake.rs running in the terminal](../../assets/898ff09cec7fdd8f.gif)


[tiny-snake.rs](https://github.com/Rodrigodd/tiny-snake.rs) by [@Rodrigodd](https://github.com/Rodrigodd) is a terminal snake game, with a minimal binary
size.

The entire game is implemented in a single file of pure Rust code, with zero dependencies. All interactions with the system are done through raw syscalls (so it only runs on Linux, sorry) and the program is completely panic-free (panic handling increases the binary size by almost 4KiB).

The game can be compiled using a single `rustc`

command, and the resulting
binary is only 2760 bytes.

*Discussions: /r/rust*

![Screenshot featuring the new enemiy: the crow](../../assets/df63fd7a4eccc05c.png)


[8bit Duels](https://github.com/ThousandthStar/8bit-duels) ([Discord](https://discord.com/invite/NbBcF4bGU5)) is a turn-based strategy game made
by [@ThousandthStar](https://github.com/ThousandthStar). It has been in development for the past year,
and the release is right around the corner!
A new blog post along with a release Youtube video is coming soon
on [this channel](https://youtube.com/channel/UCllwuaF9ac8sNni8v03GomQ).

This month’s update includes a completely remade user interface.
The [devlog](https://thousandthstar.github.io/posts/8bd/8bd-part7) covers the change from the [bevy_ui](https://lib.rs/bevy_ui) crate
to [belly](https://github.com/jkb0o/belly), which provides a nice HTML-like syntax for building the UI.
The last devlog post will address the re-implemented UI and the new troop: the Crow!

The Crow, as seen in the screenshot above, is a hooded bird assassin with two daggers. It can attack twice per turn, dealing 2 damage each time. The Crow is the last of the five 8bit Duels characters.

![lots of glowing particles (aka ants) moving to the destination](../../assets/ed4ed719414805d8.png)


[Ant Colony Simulation](https://github.com/bones-ai/rust-ants-colony-simulation) depicts an ant colony where the ants
have a simple task: to find food and bring it back to the colony.
To achieve this goal, they use signals called pheromones.
These pheromone signals guide the ants to the food source and back to their colony.

[@BonesaiDev](https://youtube.com/@bonesai-dev) released a couple of videos about the project:

[An overall explanation](https://youtu.be/98pUSZAM_7M)of how it works.[A timelapse](https://youtu.be/5xdfTJBMnwI)of ant colony at 5x speed.[2D Bloom showcase timelapse](https://youtu.be/Z4IRY_LKtt8)with 1k ants.

The project is written using Bevy.
You can find the source code [on GitHub](https://github.com/bones-ai/rust-ants-colony-simulation).

Follow [@BonesaiDev on Twitter](https://twitter.com/BonesaiDev) or on [YouTube](https://youtube.com/@bonesai-dev)
to receive future updates about this and their other AI simulation projects.

![Screenshot of an astronaut in front of stars and two galaxies](../../assets/052fe12caf3f070f.png)


[Cargo Space](https://helsing.studio/cargospace) ([Discord](https://discord.gg/ye9UDNvqQD)) by
[@johanhelsing](https://mastodon.social/@johanhelsing) is a co-op 2d space game where you build
a ship and fly it through space looking for new parts, fighting pirates and the
environment.

This months development was all about making endless procedurally generated parallaxing space backgrounds, choosing an appropriate rng crate, and making the implementation seedable and cross-platform deterministic.

Johan’s [devlog entry](https://johanhelsing.studio/posts/cargo-space-devlog-7) explains all this in detail, as well
as how distant parallax can be an immersive replacement for ui and minimaps.

![Veloren visual comparison](../../assets/ebb5b07384478dbf.jpg)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In July, Veloren released version 0.15! You can read about the release in the
[0.15 blog post](https://veloren.net/release-0-15), and watch the [release party
trailer](https://youtube.com/watch?v=weIK41W3tX0). Here are some of the changes in this release:

- The first world boss, the ‘frost giga’: seek him out if you dare!
- A new dungeon: Adlet caves.
- Airships can now be used by players.
- Enemy loot is now shared between players.
- A reputation system: if you commit crimes, NPCs will remember it!
- Improved AI: NPCs will talk to players and each other about events in the world.
- Much richer world simulation: NPCs will migrate and pass on rumours.
- You can now choose your character’s starting town.
- A durability and repair system.
- Improved accessibility, performance, bug fixes, and much, much more!

Work over July includes TCP receive buffer increase, spawn tab completion, loot changes, translation updates, dwarven quarry ⛏️ (still inactive in game), coastal town, desert city fixes, CI optimization, and shorter item count texts. Work is going on to add a web-based translation tool for Veloren.

July’s full weekly devlogs: “This Week In Veloren…”: [#213](https://veloren.net/devblog-213), [#214](https://veloren.net/devblog-214).

![concrete islands, some dirts, water, lots of vines](../../assets/d2319e9210044d96.jpg)


[Idu](https://epcc.itch.io/idu) ([Discord](https://discord.gg/MeGauteMj3)) is a strategic sandbox game about growing
plants that wish to reclaim nature, developed by [Elina Shakhnovich](https://mastodon.gamedev.place/@eli)
and [Johann Tael](https://mastodon.gamedev.place/@johann) featuring a bespoke Vulkan-based engine in Rust.

This month [a new demo was released](https://epcc.itch.io/idu/devlog/565550/demo-version-11-vines-swimming-and-magic):

- New water mechanics: instantly fill large pools and build channels to transport water.
- A climbing plant.
- A new particle system for special effects.
- Swimming and improved climbing out of water.
- Configurable keybindings.

[MEANWHILE IN SECTOR 80](https://ms80.space) ([Discord](https://discord.gg/A9GHQGNhJX), [mailing list](https://dashboard.mailerlite.com/forms/402073/85466601232532545/share))
by [Second Half Games](https://secondhalf.games) is an upcoming third-person
action-engineering space game.

This month the third update was released, you can [watch](https://youtube.com/watch?v=0wRXX-dRFr)
or [read it](https://secondhalf.games/news/2023-07-05-ms80-update-3). Highlights:

- New engineering system allows inspecting objects around the player, modifying your equipment using workbenches, and adding wires between sockets located on different pieces of equipment.
- Improved physics simulation that now features heat radiation and incandescence.

![GIF from the trailer: 2d space arcade gameplay](../../assets/38c8c0abc2c523ae.gif)


[Space Kitty](https://ghashy.itch.io/space-kitty) by [@ghashy](https://ghashy.itch.io) is a platformer
about a Kitty floating in space in search of crackers.

Somewhere in the distant space there are lots of tasty crackers floating around. In search of this highly valuable resource there are two competing parties - the DOGS and the KITTY. One can never say when the contest had begun, but it’s clear that to this day there is a game for the title of the Great Cracker Collector. Every time the cracker is taken the lucky one emits a signal to the base about his achievement. The KITTY - highly responsible and intelligent creature - always sends the exact amount of collected treasures, while the DOGS rely on their feelings. Some of them truly believe that they got multiple crackers at a time, some just can’t count, and about honesty of the others one can only guess…


The source code of the game can be found [on GitHub](https://github.com/ghashy/Space-Kitty).

*Discussions: /r/rust_gamedev*

![Screenshot of the Steam page](../../assets/25c346752f46d09d.jpg)


[Flesh](https://store.steampowered.com/app/1660850/Flesh) by [@im_oab](https://twitter.com/im_oab) is a 2D-horizontal shmup game with hand-drawn animation,
an organic/fleshy theme and a unique story. It is implemented using [Tetra](https://github.com/17cupsofcoffee/tetra).

After almost three years of development, it’s finally [out on Steam](https://store.steampowered.com/app/1660850/Flesh)!

Dive into a surreal journey as you devour a ship and battle peculiar creatures in this 2D side-scrolling bullet hell shmup. Unleash your skills, dodge relentless barrages, and uncover hidden mysteries in a hand-drawn world of flesh and gore.


The demo version was also updated, so consider trying the project out yourself.

*Discussions: /r/rust_gamedev*

![Screenshot of a level up window asking the player if they want new GPU, VRM or register](../../assets/6db278dcd7f878b0.png)


[HackeRPG](https://fellow-pablo.itch.io/hackerpg) is a WIP action game where you play as a developer
who needs to fight viruses and bugs with coding in real-time.
The game’s features include controlling your character using coding
and expanding your toolset by programming your own functions, variables and daemons.

[Recent updates](https://fellow-pablo.itch.io/hackerpg/devlog/563473/002-build) include:

- The first playable prototype is now avalable on itch.io.
- Sound effects.
- Input autocomplete.
- New enemies.

[Here’s a YouTube video](https://youtube.com/watch?v=ZIwcFl0wyx8) that showcases the current gameplay.

## Engine Updates [#](https://gamedev.rs#engine-updates)

![bevy ssao](../../assets/1091b25ccfcee434.jpg)


[Bevy](https://bevyengine.org) is a refreshingly simple data-driven game engine built in Rust.
It is [free and open-source](https://github.com/bevyengine/bevy) forever!

Bevy 0.11 brought many incredible new features.
You can check out the [full release blog post here](https://bevyengine.org/news/bevy-0-11),
but here are some highlights:

[Screen Space Ambient Occlusion (SSAO)](https://bevyengine.org/news/bevy-0-11/#screen-space-ambient-occlusion)[Temporal Anti-Aliasing (TAA)](https://bevyengine.org/news/bevy-0-11/#temporal-anti-aliasing)[Morph Targets](https://bevyengine.org/news/bevy-0-11/#morph-targets)[Robust Contrast Adaptive Sharpening (RCAS)](https://bevyengine.org/news/bevy-0-11/#robust-contrast-adaptive-sharpening)[WebGPU Support](https://bevyengine.org/news/bevy-0-11/#webgpu-support)[Improved Shader Imports](https://bevyengine.org/news/bevy-0-11/#improved-shader-imports)[Parallax Mapping](https://bevyengine.org/news/bevy-0-11/#parallax-mapping)[Skyboxes](https://bevyengine.org/news/bevy-0-11/#skyboxes)[Schedule-First ECS APIs](https://bevyengine.org/news/bevy-0-11/#schedule-first-ecs-apis)[Gizmos](https://bevyengine.org/news/bevy-0-11/#gizmos)[ECS Audio APIs](https://bevyengine.org/news/bevy-0-11/#ecs-audio-apis)[UI Borders](https://bevyengine.org/news/bevy-0-11/#ui-node-borders)[Grid UI Layout](https://bevyengine.org/news/bevy-0-11/#grid-ui-layout)[UI Performance Improvements](https://bevyengine.org/news/bevy-0-11/#faster-ui-render-batching)

*Discussions:
/r/rust,
Hacker News,
Twitter,
Mastodon*

![GIF showing focusing camera on object in the editor](../../assets/d4fb14a30c88baa4.gif)


[Fyrox](https://fyrox.rs) ([GitHub](https://github.com/FyroxEngine/Fyrox), [Discord](https://discord.com/invite/xENF5Uh), [Twitter](https://twitter.com/DmitryNStepanov))
is a game engine that aims to be easy to use and provide a large set
of out-of-the-box features.

This month [Fyrox v0.31 was released](https://fyrox.rs/blog/post/fyrox-game-engine-0-31). Highlights include:

- A huge bunch of editor improvements like the ability to create custom editor plugins, ability to open multiple scenes, saving/loading docking manager layout, and a separate panel for camera preview.
- Inverter node for AI behaviour trees.
- 9-slice image widget.
- Lots of
[API docs](https://docs.rs/fyrox)and[the book](https://fyrox-book.github.io)improvements, mostly related to UI stuff.

*Discussions: /r/rust*

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

### Mobile Development with Bevy [#](https://gamedev.rs#mobile-development-with-bevy)

[@Nikl](https://mastodon.online/@nikl_me) spent some time developing a mobile game using Bevy and
documented findings on his [blog](https://nikl.me). [The first post](https://nikl.me/blog/2023/notes_on_android_development_using_bevy)
contains notes on general project setup and some Android specific solutions.

GitHub workflows were created for automatic builds.
[A guide on how to set up an iOS workflow](https://nikl.me/blog/2023/github_workflow_to_publish_ios_app) was released at
the end of July.

![Diagram of WGPU stack from the article](../../assets/f3c315413ed9c0f1.png)


[Vladimir Zaytsev](https://twitter.com/xyzw_io) released [the first part](https://xyzw.io/posts/backend-gpu-p1)
of a series about introducing backend engineers to GPU programming:

In this series of articles, I would like to offer a gentle and popular introduction to GPU programming specifically tailored for engineers. Whether you’re new to GPU programming or simply want to expand your knowledge, we’ve got you covered. I’ll explain the fundamentals of GPU programming in a way that’s easy to grasp if you’re more accustomed to working with backend services.


The first part gives a high-level introduction into GPU compute landscape and walks a reader through a toy GPU program written with wgpu.

## Tooling Updates [#](https://gamedev.rs#tooling-updates)

![Rerun showing a large 3D point cloud](../../assets/6ec60a06b960b409.png)


[Rerun](https://rerun.io) ([Discord](https://discord.gg/npTFxYR9), [GitHub](https://github.com/rerun-io/rerun)) is an open-source SDK
for logging complex visual data paired with a visualizer for exploring that data
over time. While its primary focus is on robotics and computer vision, it can be
useful for all kinds of rapid prototyping & algorithm development.

[v0.8.0](https://github.com/rerun-io/rerun/releases/tag/0.8.0) and subsequently [v0.8.1](https://github.com/rerun-io/rerun/releases/tag/0.8.1) are out now!

A few of the biggest highlights:

- Pinhole logging is now easier to use in many cases.
- The visualizer can now show coordinate arrows for all affine transforms within the view.
- Users that build their own Viewer applications can now add fully custom Space Views.
- New optional flush_timeout specifies how long Rerun will wait if a TCP stream is disconnected during a flush.
- The
`RecordingStream`

now offers a stateful time API, similar to the Python APIs - Defaults to 8ms long microbatches instead of 50ms. This makes the default behavior more suitable for use-cases like real-time video feeds.
- The web viewer now incremental loads .rrd files when streaming over HTTP. #2412

There’s a growing community on [Discord](https://discord.gg/npTFxYR9) waiting for you to join in
case you have any questions, comments or just want to follow the latest
development. The [GitHub project](https://github.com/rerun-io/rerun) is MIT/Apache licensed and open to
contribute for everyone, be it with suggestions, bugs or PRs.

![UI with field for input file and separate panels for different output parts](../../assets/759cfeb08934952d.jpeg)


[glTF IBL Sampler UI](https://github.com/pcwalton/gltf-ibl-sampler-egui) by [@pcwalton](https://twitter.com/pcwalton) is
an artist-friendly egui frontend that wraps [glTF IBL Sampler](https://github.com/KhronosGroup/glTF-IBL-Sampler)
to generate cubemap skyboxes from panoramas.

It provides an easy way to generate skyboxes for use in Bevy and other new game engines that use the modern KTX2 format as their native texture format. By default, the panorama is split up into base color, diffuse, and specular parts, with the mipmap levels corresponding to different roughness values of the material.

## Library Updates [#](https://gamedev.rs#library-updates)

![Balls held by string swinging and hitting each other in a Newton's cradle](../../assets/523bb13e16122bfd.gif)

[bevy_xpbd](https://github.com/Jondolf/bevy_xpbd) by [@Jondolf](https://github.com/Jondolf) is a 2D and 3D physics engine based on
Extended Position Based Dynamics for the Bevy game engine.
It uses Bevy’s Entity Component System (ECS) directly for the simulation data
and logic, which makes the design and API feel better integrated into Bevy while
avoiding the overhead associated with copying lots of data to a separate data
structure like in many other physics engines such as bevy_rapier.

In mid-July, bevy_xpbd 0.2 was released, featuring:

- Spatial queries (ray casting, shape casting, point projection, intersection tests);
- Bevy 0.11 support;
- Improved scheduling;
- Velocity damping;
- Gravity scale;
- Locking translational and rotational axes;

and much more. You can find more details in the
[release post](https://joonaa.dev/blog/03/bevy-xpbd-0-2-0) and [changelog](https://github.com/Jondolf/bevy_xpbd/releases/tag/v0.2.0).

A lot of work was also done during the rest of July. The physics debug renderer
was improved, collision stability issues were significantly reduced, external
impulses were added, and Bevy’s own `Transform`

s can now be used directly
for moving bodies. The narrow phase part of collision detection was also
refactored into a separate plugin, which makes multithreading and several
upcoming features much easier to implement while also improving modularity.

*Discussions: /r/rust_gamedev*

[Sparsey](https://github.com/LechintanTudor/sparsey) by [@LechintanTudor](https://github.com/LechintanTudor) is a fast and flexible Entity Component System
based on sparse sets.

The latest release, v0.11.0, improves the performance of adding and removing components from entities and adds new functions for running systems that only borrow data from one of World, Resources or SyncResources.

![Glowing particles circling and raising up](../../assets/a0f2510d92abd060.gif)

The [Hanabi](https://crates.io/crates/bevy_hanabi) library ([GitHub](https://github.com/djeedai/bevy_hanabi), [docs.rs](https://github.com/djeedai/bevy_hanabi)) is a
modern VFX library for the [Bevy game engine](https://bevyengine.org). It focuses on scale to produce
stunning visual effects (VFX) in real time, offloading most of the work to
the GPU (compute shaders), with minimal CPU intervention. The design is inspired
by modern particle systems found in other industry-leading game engines.

This month, [Hanabi](https://crates.io/crates/bevy_hanabi) saw its biggest release so far.
Version 0.7 of Hanabi not only brings support for Bevy 0.11,
but also adds a whole new Expression API
to provide a new level of customizing for VFX authors.
With expressions, developers can combine simple building blocks
like simulation parameters (`time`

, `delta_time`

),
effect properties (user-defined variables controlled from CPU),
and math operators (`add`

, `mul`

, `cos`

, …),
to directly modify each attribute of a particle (position, velocity, …)
and form complex behaviors with complete control.
The expression API complements and extends the existing `Modifier`

-based workflow
to achieve even more complex effects.

This release also marks a major stepping stone toward the ability to build a visual editor (node graph) to build and tweak visual effects in real time.

Other changes include the ability to set a screen-space size for particles,
and a new `KillSphereModifier`

to confine particles
to the inside or the outside of a sphere.
See the [CHANGELOG](https://github.com/djeedai/bevy_hanabi/blob/v0.7.0/CHANGELOG.md) for all details.

![olf primitives gradually fade out and damaged regions
are marked with red rectangles](../../assets/93e42896089a4c71.png)

[Iced](https://iced.rs) is a Rust GUI library focused on simplicity and type safety.

[Iced v0.10](https://github.com/iced-rs/iced/releases/tag/0.10.0) is a huge release that brings a lot of updates.
Some highlights:

- Huge improvements to the text handling strategy
thanks to the adoption of
[cosmic-text](https://github.com/pop-os/cosmic-text). - A new CPU-only software renderer based on
[tiny-skia](https://github.com/RazrFalcon/tiny-skia). - Runtime renderer fallback.
- Configurable LineHeight support for text widgets.
- Nested overlays.
- Backend-specific primitives.
- Offscreen rendering & screenshots.
- Gradients for backgrounds.
- ComboBox widget.

*Discussions: /r/rust*

## Other News [#](https://gamedev.rs#other-news)

- Other game updates:
[Robo Instructus](https://store.steampowered.com/app/1032170/Robo_Instructus)was released 4 year ago -[Alex Butler shared an article](https://blog.roboinstruct.us/2023/07/16/4-years-old.html)about game’s updates, stats, and user feedback from the last year.[snaked](https://kuviman.itch.io/snaked)by[@kuviman](https://github.com/kuviman)is a reversed snake game where you play as food.[@Syn9Dev](https://twitter.com/Syn9Dev)shared a couple of updates about their retro JRPG:[battle inventory](https://twitter.com/Syn9Dev/status/1676082920182755332)and[cave bugs enemies](https://twitter.com/Syn9Dev/status/1676969827980935172).[Sulis](https://sulisgame.com)v1.0[was released this month](https://github.com/Grokmoo/sulis/releases/tag/1.0.0).[@martin-t resumed developemnt of RecWars](https://reddit.com/r/rust_gamedev/comments/1548teg/resumed_recwars).[Vladimir Zaytsev posted a video](https://reddit.com/r/rust_gamedev/comments/14t8xgw/colonysim)of his WIP colony sim showcasing the early progress on construction mechanics.[mochia.net](https://reddit.com/r/rust/comments/15c0j97/a_virtual_pet_site)is a virtual pet site inspired by Neopets, with a backend written in Rust.[@dobkeratops shared an update on their WIP shooter game](https://reddit.com/r/rust_gamedev/comments/14wsnhx/rust_shooter_update)featuring lighting tweaks and vehicle turrets.[Maginet](https://twitter.com/evrimzone/status/1681302065069559812)added an undo button and preparing for Steam release.[PatchGames started working on a new city building game](https://twitter.com/PatchGamesStdio/status/1677369018225680397).

- Other engine updates:
[godot-rs now supports Godot 4.1](https://mastodon.gamedev.place/@GodotRust/110669301088668526).[ggez v0.9](https://reddit.com/r/rust_gamedev/comments/14v6x3z/ggez_news_0_9)mostly brings slight API tweaks and bugfixes. The devs also shared their plans for ggez v10: 3d support, async asset loading, and coroutines.

- Other learning material updates:
[GitGhillie shared an article](https://itch.io/blog/564971/blender-to-bevy-workflow-physics-props)about using Blender as a level editor for Bevy.[PhaestusFox released more Bevy tutorials on YouTube](https://youtube.com/@PhaestusFox): mostly about Bevy v0.11, Bevy’s UI plugins, and Rapier integration.

- Other tooling updates:
- Other library updates:
[bevy_vello](https://github.com/vectorgameexperts/bevy_vello)is a Bevy plugin that provides rendering support for[lottie](https://lottiefiles.com/what-is-lottie)animations and SVGs on Bevy using[Vello](https://github.com/linebender/vello)and[Velato](https://github.com/linebender/velato).[hexx v0.8](https://github.com/ManevilleF/hexx/releases/tag/0.8.0)release adds a hexmod representation and resolution system.[cuicui_layout](https://github.com/nicopap/cuicui_layout)is a dumb layout algorithm you can rely on, built for and with Bevy.[renet v0.0.13](https://github.com/lucaspoffo/renet/releases/tag/0.0.13)slightly improves the API and brings a couple of bugfixes.


## Discussions [#](https://gamedev.rs#discussions)

- /r/rust_gamedev:

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[bevy_mod_scripting is looking for maintainers](https://github.com/makspll/bevy_mod_scripting/issues/48).[‘Are We Game Yet?’ wants to know about projects/games/resources that aren’t listed yet](https://github.com/rust-gamedev/arewegameyet#contribute).[Graphite is looking for contributors](https://graphite.rs/contribute)to help build the new node graph and 2D rendering systems.[winit’s “difficulty: easy” issues](https://github.com/rust-windowing/winit/issues?q=is%3Aopen+is%3Aissue+label%3A%22difficulty%3A+easy%22).[Backroll-rs, a new networking library](https://github.com/HouraiTeahouse/backroll-rs/issues).[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[A/B Street’s “good first issue” issues](https://github.com/a-b-street/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/D-Good-First-Issue).[Ambient’s “good first issue” issues](https://github.com/AmbientRun/Ambient/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22).

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!