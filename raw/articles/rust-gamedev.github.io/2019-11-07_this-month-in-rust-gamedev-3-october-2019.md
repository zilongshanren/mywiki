---
title: 'This Month in Rust GameDev #3 - October 2019'
url: https://gamedev.rs/news/003/
author: Rust GameDev WG
published: '2019-11-07'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the third issue of the Rust GameDev Workgroup’s monthly newsletter.

[Rust](https://rust-lang.org) is a systems language pursuing the trifecta:
safety, concurrency, and speed.
These goals are well-aligned with game development.

We hope to build an inviting ecosystem for anyone wishing
to use Rust in their development process!
Want to get involved? [Join the Rust GameDev working group!](https://github.com/rust-gamedev/wg#join-the-fun)

## Game Updates [#](https://gamedev.rs#game-updates)

![chest and inventory with items](../../assets/5c60610f367d645a.png)


[Sulis](https://sulisgame.com) is a Role Playing Game (RPG) with turn based, tactical combat,
deep character customization and an engaging storyline.
The game has been built from the ground up with modding
and custom content in mind.
Currently supported on Windows and Linux platforms.

The game is currently fully playable
and includes the first act of The Twin Expanse,
an old school RPG campaign in the vein of classic games
such as *Baldur’s Gate*,
but mixing in modern elements from titles like
*Divinity: Original Sin* and *Pillars of Eternity*.

The core game engine as well as the campaign
are still under heavy development.
Users are encouraged to [file issues with bugs](https://github.com/Grokmoo/sulis/issues),
feature requests, or any other feedback.

![flaming fingers spell demonstration](../../assets/e833d4ff235736b0.png)


Features:

- Cross platform native binaries, currently
[built for Windows and Linux](https://github.com/Grokmoo/sulis/releases) - Multiple campaigns with over 8 hours of playtime, featuring both handcrafted and procedural content.
- A detailed and fully realized world and story - check out
the
[Lore page](https://sulisgame.com/lore). - Designed with modding in mind - although more work still needs to be done in this area.
- A powerful 2D graphics engine with zoom, scalable UI, HiDPI support, and a swappable graphics backend.
- Runs on very modest hardware - even software renderers (although at a reduced frame rate).

![ability tree gui](../../assets/4dbe32062b780503.png)


The GPLv3-licensed [source code is hosted on GitHub](https://github.com/Grokmoo/sulis).
Sulis is written in Rust, with scripting in Lua and most data files in the YAML format.

*Discussions:
/r/rust_gamedev*

![Bumpy terrain with a rivers and trees](../../assets/830e01139b0b433b.png)


[Veloren](https://veloren.net) is an open-world, open-source multiplayer voxel RPG.
The game is in an early stage of development, but is playable.

This month [a v0.4 version was released](https://veloren.net/devblog-37)
and a [player survey results was published](https://veloren.net/devblog-36/#player-survey).

Some of October’s improvements:

- lots of bugfixes and optimizations;
- improved erosion, rivers and water flow physics;
- user interface improvements;
- improved game lore;
- RFC procedure for 0.5 development.

New video: [“Cities, dungeons and other structures”](https://www.youtube.com/watch?v=iwP7SXdWcTg)
[[/r/veloren](https://reddit.com/r/Veloren/comments/ddp0n9/veloren_cities_dungeons_and_other_structures)].

The full weekly devlogs “This Week In Veloren…”:
[#36](https://veloren.net/devblog-36),
[#37](https://veloren.net/devblog-37),
[#38](https://veloren.net/devblog-38),
[#39](https://veloren.net/devblog-39).

Also, check out [/r/veloren subreddit](https://reddit.com/r/Veloren),
it’s pretty active.

![Exported models with textureas and skeletal animations](../../assets/6473337d1f3fa71b.jpg)


[Canon Collision](https://canoncollision.com) by [@rukai](https://twitter.com/thisIsRukai) is an Undertale + Homestuck
fan-made platform fighter with powerful tools for modding.
It was forked from another project of rukai’s
[PF Sandbox](https://github.com/rukai/PF_Sandbox) so he could focus on making
a game rather then an engine.

This month,
[exporting and hot-reloading assets from blender](https://twitter.com/thisIsRukai/status/1180477120113340417),
[freelook camera](https://twitter.com/thisIsRukai/status/1182945899485335552),
[textures](https://twitter.com/thisIsRukai/status/1182945899485335552),
and [animations](https://twitter.com/thisIsRukai/status/1188261107124727808)
were added to the project.

![Antorum screenshot: a few human characters, a few rats and an inventory UI](../../assets/27de3b9ef2ce6494.jpeg)


[Antorum](https://dooskington.com) is a multiplayer RPG where players build their characters
and fight against the growing threats on the isle.
The game server is authoritative and written in Rust,
while the client is written in Unity/C#.

This month, [@dooskington](https://twitter.com/dooskington) published a bunch of devlogs:

[#6 “Items And Inventory”](https://dooskington.com/dev-log/6);[#7 “Grubbnet”](https://dooskington.com/dev-log/7);[#8 “The Editor”](https://dooskington.com/dev-log/8);[#9 “The Editor, Pt. 2”](https://dooskington.com/dev-log/9);[#10 “Terrain Sync”](https://dooskington.com/dev-log/10).

As described in the [7th devlog](https://dooskington.com/dev-log/7),
an initial version of a “[grubbnet](https://github.com/Dooskington/grubbnet)” crate was published.

It’s a lightweight TCP client/server for writing networked applications and games. It abstracts socket code, keeps track of connections, and delivers everything back to the developer in a nice list of events. In addition to handling network events (such as client connects and disconnects), handling incoming packets is as easy as grabbing an iterator over the incoming packet queue.

It’s the same networking crate that the Antorum game server uses under the hood.

![Two crabs fencing on a 1D map](../../assets/63627389ab0ae323.png)


[Ferris Fencing](http://ferrisfencing.org) is a live tournament in which
player-programmed bots combat each other on a [RISC-V](https://riscv.org) virtual machine.
It is a showcase of [CKB-VM](https://github.com/nervosnetwork/ckb-vm), a simple implementation of the RISC-V instruction set,
written in the Rust programming language.

The Ferris Fencing tournament is not yet live,
but fencers may begin building their bots and testing them locally.
Instructions are in the [GitHub repo](https://github.com/brson/ferris-fencing).

[Tennis Academy](https://iolivia.me/posts/6-months-of-rust-game-dev) v0.03 & v0.0.4 [#](https://gamedev.rs#tennis-academy-v0-03-v0-0-4)

![4 courts with players](../../assets/267c43690e4c790c.png)


[@oliviff](https://twitter.com/oliviff) released [v0.0.3](https://twitter.com/oliviff/status/1185576890746265600)
and [v0.0.4](https://twitter.com/oliviff/status/1185945850771660805) updates for [Tennis Academy](https://iolivia.me/posts/6-months-of-rust-game-dev):

- 🏘️ improved reception area queueing
- 🎆 timed effects when players disappear
- ⛹️ click to collect coins from player
- 👟 4 courts on screen
- ⛹️ matching t-shirts for players
- 💯 money is now score
- 🚥 court + t-shirt colour matching logic
- 📊 score multipliers

![Virtual piano keyboard](../../assets/bd421520a8fcbbf3.png)


[piano-rs](https://github.com/ritiek/piano-rs) is a multiplayer piano using UDP sockets
that can be played using computer keyboard, in the terminal.

*Discussions:
/r/rust*

![Dissolve gameplay demo](../../assets/ee278b9d93a0a4e8.gif)


[“Will it dissolve?”](https://puppetmaster.itch.io/dissolve) is a small puzzle game
for [“Open Jam 2019”](http://openjam.io)
where you have to prepare the level so that it will
automatically convert and dissolve in the future.

Programmed with the help of the [Tetra engine](https://github.com/17cupsofcoffee/tetra).
[The source code is available here](https://github.com/puppetmaster-/will_it_dissolve).

![Garden screenshot: a tree, leaves, water and ruins](../../assets/e340450302faa3a1.jpeg)


[Garden](https://epcc.itch.io/garden) is an upcoming game centered around
growing realistic plants.

The following changes were made since the last devlog:

- Improved flowers were added.
- The plant simulation code is almost finalized, and developers will be able to start adding new species soon.
- The procedural ruin generation was improved: no more floating concrete chunks.

Also, a new design plan was created:

- The main objective is to restore the luscious ecosystem in a polluted wasteland. The player will have to continuously figure out how to handle different environmental constraints to keep trees growing, collect enough fruit and figure out what to do with them, and unlock new goals and flora.
- But for players who are interested in wild, goalless plant growth, there’ll also be a sandbox mode. As one progresses in the main game and “unlocks” more trees, playing around with creating flourishing jungle troves will be possible.

To stay informed of smaller updates, screenshots, and new devlogs,
follow [@logicsoup](https://twitter.com/logicsoup) on Twitter.

[EVE Aether Wars](https://store.steampowered.com/app/1165670/EVE_Aether_Wars__Tech_Demo/) Backend Optimization [#](https://gamedev.rs#eve-aether-wars-backend-optimization)

[@aidanhs shared](https://twitter.com/aidanhs/status/1181584776584675328)
a small [EVE Aether Wars](https://store.steampowered.com/app/1165670/EVE_Aether_Wars__Tech_Demo/) backend optimization success story:

To double the tick rate to 30Hz, our underlying @rustlang layer

[from last time]needed…a two line bugfix and some metrics support. Nice proof point for reliable software in Rust!

[Alex Butler](https://twitter.com/bigabgames) continues to polish their “[Robo Instructus](https://store.steampowered.com/app/1032170/Robo_Instructus/)” game;
[1.12, 1.13, and 1.14 versions were released](https://steamcommunity.com/app/1032170/allnews):
non-ascii code input, new icons, bugfixes, and better translations.

![translated menu items](../../assets/c0fb4bcbb74c4691.png)


-
[“Rendering a 2D game in 3D”](https://medium.com/@recallsingularity/rendering-a-2d-game-in-3d-bd24ddbee6eb)-[Tom Leys](https://twitter.com/RecallSingular1)is working on a “The Recall Singularity”[Godot](https://godotengine.org)/Rust game about designing autonomous factory ships and stations and this month they published a post about evolution of the game’s rendering.![Recall Singularity screenshot: map, a few belts and processing nodes](../../assets/9ea698f12b7a3adf.png)

-
[@ardawanizadi](https://twitter.com/ardawanizadi)shared a[short text report](https://reddit.com/r/godot/comments/dilbar/game_progress_for_almost_a_month_rust_godot)and a[video demo](https://twitter.com/ardawanizadi/status/1184353596927688704)of their progress with a project of an OpenWorld game this month: character physics, weapon system, cameras, animations system, dynamic damage system. -
[“Pong Clone in Godot Using ‘gdnative’ Rust Bindings”](https://reddit.com/r/godot/comments/dfam0p/i_made_a_pong_clone_in_godot_using_the_gdnative)-[@you-win](https://github.com/you-win)couldn’t find any full game examples that used[godot-rust](https://github.com/GodotNativeTools/godot-rust)so they made their own [[source code](https://github.com/you-win/godot-pong-rust)].

### Ludum Dare 45 [#](https://gamedev.rs#ludum-dare-45)

[Ludum Dare](https://en.wikipedia.org/wiki/Ludum_Dare) is a regular game jam event,
during which developers create games from scratch in a weekend
based on a theme suggested by the community.

LD45’s theme was “Start with nothing”. Here are some of the games made with Rust:

-
[“Working Title”](https://ldjam.com/events/ludum-dare/45/working-title)by[@NoahRosenzweig](https://twitter.com/NoahRosenzweig)made with Amethyst ([source code](https://github.com/Noah2610/LD45-WorkingTitle)).*Experience a work in progress.*Play through the development process of a 2D platformer game, and watch your environment transform as you progress… The further you get, the more features are added, including menacing enemies, destructive spikes, and adaptive music.

![Working Title: an early stage of the game](../../assets/77aafb0070822920.png)

-
[“Mindmaze”](https://ldjam.com/events/ludum-dare/45/mindmaze)by[@sigodme](https://twitter.com/sigodme)([source code](https://github.com/sigod/ludum-dare-45)).A small and unhurried story about devious passages of the trapped human mind. Begin in the middle of oblivion as shadow and take a walk through every chamber of this place to find all shards of lost personality. Can you find the way out?!

![Mindmaze: main menu](../../assets/3727ebe0d2b6352f.png)

-
[“Legally Dead”](https://ldjam.com/events/ludum-dare/45/legally-dead)by[@vilcans](https://twitter.com/vilcans)made with[ggez](https://ggez.rs)([source code](https://github.com/vilcans/ld45)).With nothing, not even memories, you find yourself maneuvering some kind of craft in strange caves.

![ultra-low-poly ship in low-poly caves](../../assets/c9bc89719a36015b.png)

Check out the devlog post:

[“Tools and tech for my game written in Rust”](https://ldjam.com/events/ludum-dare/45/legally-dead/tools-and-tech-for-my-game-written-in-rust).

### Amethyst Games [#](https://gamedev.rs#amethyst-games)

-
See the “Working Title” LD45 game above.

-
A top-down 2D shooter

[“Grumpy Visitors”](https://github.com/amethyst/grumpy_visitors)by[@mvlabat](https://twitter.com/mvlabat)became an official showcase game.Read the announcement post:

[“Showcase game #4: Grumpy Visitors”](https://amethyst.rs/posts/showcase-game-4-grumpy-visitors).Current game features:

- Cooperative multiplayer;
- Spawning monsters with basic AI;
- Sprite animations and custom shaders (health HUD).

![A magician shooting missiles at giant bugs](../../assets/e12ee3f3a8157cbf.png)

-
[Arrakis](https://github.com/JPMoresmau/arrakis)by[@JpMoresmau](https://twitter.com/JpMoresmau)is a 80s game ported in Rust and Amethyst.It’s a mini role-playing/adventure game. The goal? Walk through the streets of Arrakis to find the fabled Wizard of Arrakis, that can teach you arcane powers you’ve only dreamt of!

![Arrakis screenshot](../../assets/e2f694dfa1924245.png)

-
[@webshinra](https://twitter.com/Webshinra)finished porting their hexagonal game to Amethyst and is now preparing to build gameplay.![hexagonal pam with a few mechs](../../assets/e06706c3ad7a98ff.jpg)

-
[@takeryo_eeic](https://twitter.com/takeryo_eeic)is also working on a turn-based hexagonal game.[Watch the video demo here](https://twitter.com/takeryo_eeic/status/1190142474062184448). -
[Space Shooter](https://github.com/amethyst/space_shooter_rs)by[@carlosupina](https://twitter.com/carlosupina)got[2 new items](https://github.com/amethyst/space_shooter_rs/pull/19)and[1 new enemy](https://github.com/amethyst/space_shooter_rs/pull/18).

## Library & Tooling updates [#](https://gamedev.rs#library-tooling-updates)

Compile times (full and incremental) are one of Rust’s pain points.
[Azriel](https://azriel.im) published a devlog about optimizing [Will](https://azriel91.itch.io/will)’s build times.
Summary:

In a 45k LOC / 102-crate workspace, moving tests from member crates into a single workspace_tests crate achieved the following improvements:


- Build and test duration in release mode reduced from 23 minutes to 13 minutes.
- Debug artifact disk usage reduced from 20 G to 7 G (65% reduction, fresh build), or 230 G to 50 G (78% reduction, ongoing development).

*Discussions:
/r/rust*

### 🛈 Tip: Speed Up Iteration Time By Using [LLD Linker](https://lld.llvm.org) [#](https://gamedev.rs#i-tip-speed-up-iteration-time-by-using-lld-linker)

Takeaways from [an interesting tweet](https://twitter.com/VladZhukov0/status/1186412587958845442)
from [VladZhukov0](https://twitter.com/VladZhukov0)
and a [/r/rust thread “Is the rust compiler really THAT slow?”](https://reddit.com/r/rust/comments/dl4c8o/is_the_rust_compiler_really_that_slow):

-
Try switching to

[LLD linker](https://lld.llvm.org):`RUSTFLAGS="-C link-arg=-fuse-ld=lld" cargo run # Alternatively, you can set `rustflags` in your `.cargo/config``

Depending on your project structure, OS, and toolchain this can potentially speed up the incremental compilation a few times.

-
Also, try disabling debug information (if you don’t need it):

`# in your `Cargo.toml` [profile.dev] debug = 0`


Now the linking only takes around one second, compared to 10 seconds previously.

Reduced my average compilation time from 10-20s (which is a bit crazyness for gamedev iteration) to 5-7s. Wonder why haven’t I tried this before?🤔


Also, see this GameDev WG tracker/complaint issue:
[#50 “Linking Time”](https://github.com/rust-gamedev/wg/issues/50).

![RLSL code sample](../../assets/353a8baa2409e151.png)

This month, [@MaikKlein_DEV](https://twitter.com/MaikKlein_DEV) gave a talk at
[The Khronos Group](https://www.khronos.org)’s meetup in Munich
about bringing Rust to the GPU:
[here’re the slides](https://docs.google.com/presentation/d/1_cB-sxUusYVoCYdXnqwAg2u3-lrqBfgrUj205ytxYaw).

[RLSL](https://github.com/MaikKlein/rlsl) (Rust Like Shading Language) is an *experimental* project
that allows compiling Rust to [SPIR-V](https://www.khronos.org/registry/spir-v).

Current features:

- Supports cargo;
- Multiple entry points can be defined in the same SPIR-V module;
- Currently supports Vertex, Fragment and Compute shaders;
- Shader code can run on the CPU because rlsl is a subset of Rust.

Also, check out older posts:

*Discussions:
/r/rust,
hacker news*

![sailor screenshot: vector terrain map and some basic UI](../../assets/c75212538cd70a71.png)

[Yatekii/sailor](https://github.com/Yatekii/sailor)- a wgpu-based sailing navigation application

[gfx-rs v0.4 was released](https://reddit.com/r/rust/comments/dm89t2/gfxhal_version_04_release):
major changes were described in [the last blog post](https://gfx-rs.github.io/2019/10/01/update.html),
for the detailed list of changes, see the
[CHANGELOG](https://github.com/gfx-rs/gfx/blob/master/CHANGELOG.md#hal-040-23-10-2019).

![vulkano logo](../../assets/6543ded680df5a83.png)


[A twitter thread by @Tomaka](https://twitter.com/tomaka17/status/1188513260473110528) about why command buffers
in [Vulkano](http://vulkano.rs) (a Rust library that wraps around [Vulkan graphics API](https://www.khronos.org/vulkan))
are so complicated.

![a spline sample with node handles](../../assets/769fefdb4bb21789.png)


[splines](https://crates.io/crates/splines), a crate by [@phaazon](https://twitter.com/phaazon_) to handle spline interpolation,
[just got released in version 3.0.0](https://reddit.com/r/rust/comments/dln7yd/splines300).

That version adds support for stroke Bézier interpolation,
which is a Bézier interpolation but allows you to break the handles
(instead of the regular 180° angle formed
by the handle with the `Interpolation::Bezier`

mode).

[spline-editor](https://github.com/phaazon/spline-editor) got a patch to allows you to try stroke Bézier.

[Mun](https://mun-lang.org) is a scripting language for gamedev
focused on quick iteration times that is written in Rust.

The Mun Team started October with the launch of the [mun-lang.org](https://mun-lang.org) website,
[Discord server](https://discord.gg/SfvvcCU), and [OpenCollective](https://opencollective.com/mun)
and processing the feedback from a larger audience.
Now the team is moving towards v0.1 release.

Also, check out /r/rust [“The Mun programming language is going live!” post](https://reddit.com/r/rust/comments/de51ai/the_mun_programming_language_is_going_live).

![ultraviolet benchmarks table](../../assets/9d4caefe59707ba5.png)


[ultraviolet](https://github.com/termhn/ultraviolet) by [@fu5ha](https://twitter.com/fu5ha) is a crate to do basic, computer-graphics-related,
linear algebra, but fast, by taking full advantage of [SIMD](https://en.wikipedia.org/wiki/SIMD).

<…> To do this, it uses an “SoA” (

[Structure of Arrays]) architecture such that each Wec (wide-vec) actually contains the data for 4 Vecs and will do any operation on all 4 of the vector ‘lanes’ at the same time. Doing this is potentially much (factor of 10) faster than an “AoS” ([Array of Structs]) layout, as all current Rust linear algebra libraries do, depending on your work load. However, algorithms must be carefully architected to take full advantage of this, and doing so can be easier said than done, especially if your algorithm involves significant branching.

*Discussions:
/r/rust*

![salva’s logo](../../assets/996abdf3e28cff8b.png)


Main updates:

-
[salva.rs](https://salva.rs)- two new crates for fluid simulation: salva2d and salva3d!Salva is a new project dedicated to fluid simulation. The goal of salva is to provide CPU-based, particle-based, 2D and 3D, fluid simulation libraries that can be used for interactive and offline application like animation. It could be used, to some extents, for video games (especially the 2D version), as long as the number of particles is kept small.

Watch a

[“Fluid simulation with salva 0.1 and nphysics 0.13”](https://www.youtube.com/watch?v=356unTmeVUk)video or play with the online[2D](https://www.salva.rs/demo_all_examples2)or[3D](https://www.salva.rs/demo_all_examples3)WASM demos yourself. -
[nphysics 0.13](https://nphysics.org)brings: some support of breakable joint constraints, and more improvements on the integration with ECS. -
[@sebcrozet](https://github.com/sebcrozet)(the main developer of all the current rustsim projects)[have been added to the GitHub sponsor beta](https://github.com/sponsors/sebcrozet).

*Discussions:
/r/rust*



![cyclone physics demo](../../assets/59a151960b478241.gif)

[cyclone-physics-rs](https://github.com/heyrutvik/cyclone-physics-rs) by [@heyrutvik](https://twitter.com/heyrutvik) a new WIP game physics engine
based on the [“Game Physics Engine Development” book](https://www.crcpress.com/Game-Physics-Engine-Development-How-to-Build-a-Robust-Commercial-Grade/Millington/p/book/9780123819765).

[@cynic64](https://github.com/cynic64) shared a [demo video](https://youtube.com/watch?v=UrnSCpf_yw0) and
a [report about their WIP rendering engine](https://reddit.com/r/rust/comments/dpa3ar/wip_rendering_engine).

It’s based on Vulkano and consists of three repos:

[re-ll](https://github.com/cynic64/re-ll)- low level abstractions for Vulkano’s command buffers and windows.[render-engine](https://github.com/cynic64/render-engine)- Vulkan abstraction.[test-render-engine](https://github.com/cynic64/test-render-engine)- various little programs created with render-engine. “pretty” is the one shown in the video, “base” shows the basic functionality.

[The Roguelike Tutorial](http://bfnightly.bracketproductions.com/rustbook) by [@blackfuture](https://patreon.com/blackfuture)
includes almost 40 chapters now and continues to grow.

Some of the October’s updates:

- traps and doors;
- mapgen algorithms including Waveform Collapse;
- prefab levels and sections;
- guided procgen for towns.

All chapters have links to WASM demos.

Also, 0.5 version of [rltk-rs](https://github.com/thebracket/rltk_rs) brings
abstraction between back-ends, better compile time,
web version improvements, and more examples.

[Nannou](https://nannou.cc) is a creative coding framework that aims to make it easy
for artists to express themselves with simple, fast, reliable code.

[Nannou has been awarded 10K USD in funding](https://nannou.cc/posts/moss_grant_announce)
as a part of the [MOSS Mission Partners](https://mozilla.org/en-US/moss/mission-partners) track.
The proposed work is aimed towards improving the state
of some foundational crates within the Rust audio ecosystem
over the next three to four months.

Key areas of our work will include:

- Addressing some long-standing issues in
[CPAL](https://github.com/rustaudio/cpal). - Review and improve CPAL’s web audio support.
- Implement a simple web app and guide demonstrating CPAL’s web audio support.
- Design, develop and document a standard audio graph abstraction and crate, reflecting on lessons learned and limitations of prior efforts, and the requirements of the wider rust audio community.

*Discussions:
/r/rust*

### Amethyst [#](https://gamedev.rs#amethyst)

![amethyst logo](../../assets/6692a81ae6e6d242.png)


-
[specs](https://github.com/amethyst/specs)and its related repositories[awesome-specs](https://github.com/amethyst/awesome-specs),[hibitset](https://github.com/amethyst/hibitset)and[shred](https://github.com/amethyst/shred)were moved to[Amethyst organization](https://github.com/amethyst)[[URLO](https://users.rust-lang.org/t/specs-parallel-ecs-moved-to-amethyst-organization/33815)]. -
[amethyst_physics v0.1.1 was released](https://www.reddit.com/r/rust_gamedev/comments/dm3jsf/amethyst_v011_contacts_events): now it’s possible to fetch Rigid body contacts events. -
[@_AndreaCatania](https://twitter.com/_AndreaCatania)published two video tutorials:

## Popular Workgroup Issues in GitHub [#](https://gamedev.rs#popular-workgroup-issues-in-github)

## Meeting Minutes [#](https://gamedev.rs#meeting-minutes)

[See all meeting issues](https://github.com/rust-gamedev/wg/issues?q=label%3Ameeting) including full text notes
or [join the next meeting](https://github.com/rust-gamedev/wg#join-the-fun).

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[/r/rust: “Need help porting steam libraries to rust”](https://reddit.com/r/rust/comments/diuqg7/need_help_porting_steam_libraries_to_rust);[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs));[winit’s “Good first issue” and “help wanted” issues](https://github.com/rust-windowing/winit/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+label%3A%22status%3A+help+wanted%22+label%3A%22Good+first+issue%22);[gfx-rs’s “contributor-friendly” issues](https://github.com/gfx-rs/gfx/issues?q=is%3Aissue+is%3Aopen+label%3Acontributor-friendly);[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22);[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22);[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A);[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner);[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22);

## Bonus [#](https://gamedev.rs#bonus)

Just an interesting Rust gamedev link from the past. :)

[Gravisim](https://github.com/bcamp1/Gravisim) by [@bcamp1](https://github.com/bcamp1)
is a simulation of universal gravitation.
It uses [Newton’s Law for Universal Gravitation](https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation)
to run an n-body physics simulation.

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).
Feel free to send PRs about your own projects!

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!