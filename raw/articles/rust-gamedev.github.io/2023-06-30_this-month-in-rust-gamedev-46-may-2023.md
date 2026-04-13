---
title: 'This Month in Rust GameDev #46 - May 2023'
url: https://gamedev.rs/news/046/
author: Rust GameDev WG
published: '2023-06-30'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 46th issue of the Rust GameDev Workgroup’s
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

[Announcements](https://gamedev.rs/news/046/#announcements)[Game Updates](https://gamedev.rs/news/046/#game-updates)[Engine Updates](https://gamedev.rs/news/046/#engine-updates)[Learning Material Updates](https://gamedev.rs/news/046/#learning-material-updates)[Tooling Updates](https://gamedev.rs/news/046/#tooling-updates)[Library Updates](https://gamedev.rs/news/046/#library-updates)[Other News](https://gamedev.rs/news/046/#other-news)[Discussions](https://gamedev.rs/news/046/#discussions)[Requests for Contribution](https://gamedev.rs/news/046/#requests-for-contribution)

## Announcements [#](https://gamedev.rs#announcements)

![find ferris screenshot: a cart with sweets, ferris, flowers, etc](../../assets/5e155d51d033ae23.png)

[Rusty Jam #3](https://itch.io/jam/rusty-jam-3) ran from May 21st 2023 to May 29th 2023 and the theme was
“Hidden in plain sight”.
The jam had a few but high-quality and awesome games.

Here’re the winners:

- 🥇
[Find Ferris](https://kuviman.itch.io/find-ferris)by kuviman. - 🥈
[Tug of Orb](https://anders429.itch.io/tug-of-orb)by anders429. - 🥉
[The Veiled Path](https://jebik.itch.io/the-veiled-path)by Jebik.

We wish all the participants good luck in their future endeavors!
The RustyJam will be back, so stay tuned on
[the Rusty Jam Discord](https://discord.gg/jZtz6y9gCJ) for future updates!

The 27th Rust Gamedev Meetup took place in May. You can watch the recording
of the meetup [here on Youtube](https://youtube.com/watch?v=WQ3ncBe9srM).

The schedule:

- Rusty Jam 3 by
[@ElhamAryanpur](https://github.com/ElhamAryanpur) - Blue Engine by
[@ElhamAryanpur](https://github.com/ElhamAryanpur) - Rerun by
[@wumpf](https://github.com/wumpf) - Graphite by
[@Keavon](https://github.com/Keavon)

The meetups take place on the second Saturday of every month via the [Rust
Gamedev Discord server](https://discord.gg/yNtPTb2) and are also [streamed on
Twitch](https://twitch.tv/rustgamedev).

## Game Updates [#](https://gamedev.rs#game-updates)

### Digital Extinction [#](https://gamedev.rs#digital-extinction)

![Building Placement in Digital Extinction](../../assets/99b9c7f3544db4b4.jpeg)

[Digital Extinction](https://de-game.org) ([GitHub](https://github.com/DigitalExtinction/Game), [Discord](https://discord.gg/vHMFuCWGSX),
[Reddit](https://reddit.com/r/DigitalExtinction)) by [@Indy2222](https://github.com/Indy2222) is a 3D real-time strategy game made with
[Bevy](https://bevyengine.org).

The most notable updates are:

- poles at unit manufacturing delivery locations for selected factories,
- pausing unit manufacturing when the spawn location is occupied,
[IME](https://en.wikipedia.org/wiki/Input_method)support for text boxes,- a lot of progress on multiplayer networking,
[logging](https://docs.de-game.org/logging/)to file and other logging improvements.

Support for multiplayer is a technologically complex problem to solve and it is
the last major missing feature before the [proof-of-concept](https://github.com/DigitalExtinction/Game/milestone/1) version
can be released. Therefore, a lot of effort currently goes in this direction.

The game is slowly gaining traction in the development community.
Check out our new [contributors here](https://github.com/DigitalExtinction/Game/graphs/contributors).

See [gameplay](https://youtu.be/_ibNMDgIQDE) screen recordings on YouTube.

More detailed monthly updates are available [here (May)](https://mgn.cz/blog/de07/) and
[here (June)](https://mgn.cz/blog/de08/).

![Tunnet screenshot: robots queueing outside nightclub](../../assets/57bbc923af2255d4.jpg)

Tunnet ([Steam](https://store.steampowered.com/app/2286390/Tunnet), [Itch.io](https://puzzled-squid.itch.io/tunnet)) is a short
puzzle/exploration game where the player digs tunnels and connects computers
together.

As a network engineer, the player will also have to respond to security
incidents.
In May, this game mechanic has been illustrated in a [devlog](https://puzzled-squid.itch.io/tunnet/devlog/532388/devlog-1-ghost-in-the-tunnels) and
a preview of the new [basic water simulation](https://mastodon.gamedev.place/@puzzled_squid/110322440469696044) has been posted.

![happy fish, exploding bombs, “thank you!” written in the central explosion and “just founded” in the bottom](../../assets/cc9b80f2a0854329.png)


This month [Fish Folk](https://fishfolk.org/games/jumpy) ([itch.io](https://spicylobster.itch.io), [Discord](https://discord.gg/4smxjcheE5))
has launched their [Kickstarter campaign](https://kickstarter.com/projects/erlendsh/fish-folk)
that has [already reached its funding goal](https://kickstarter.com/projects/erlendsh/fish-folk/posts/3821869)!

Even though the basic sum is collected, the campaign still continues to get more funds for the stretch goals:

The plan for how to allocate funds that exceed our €15k goal is very simple: For every additional €1,000 pledged to our campaign, we will prototype another fishy game archetype for our evergrowing bundle. Once our funding run concludes we will poll our backers on which game(s) you would like us to prioritize.


*Discussions: /r/rust*

![top-down view on the game world: wallks, traps, enemies, doors, etc](../../assets/9aa88c39a1ad09f0.png)

[escape-ai](https://github.com/bones-ai/rust-escape-ai) by [@bones-ai](https://twitter.com/BonesaiDev) is a Rust-based implementation of a genetic algorithm
and reinforcement learning simulation.
Its purpose is to train an AI named Zoe to escape a room it’s enclosed in.
The simulation is built using the Macroquad library.

The [YouTube video](https://youtube.com/watch?v=OeojCLDKaJU) demonstrates 1000 AI bots learning
how to escape five rooms of increasing difficulty.

*Discussions: /r/rust_gamedev*

[MEANWHILE IN SECTOR 80](https://ms80.space) ([Discord](https://discord.gg/A9GHQGNhJX), [mailing list](https://dashboard.mailerlite.com/forms/402073/85466601232532545/share))
by [Second Half Games](https://secondhalf.games) is an upcoming third person
action-engineering space game.

Second Half Games released the [first update video](https://youtube.com/watch?v=bgmySx_tv1s) for the game.
It includes an introduction to the studio, an overview of the game, and some of
the recent progress towards the first public demo.

![editing of windows on a cute cottage](../../assets/34d7eaa52460f439.gif)


[Tiny Glade](https://store.steampowered.com/app/2198150/Tiny_Glade) ([Twitter](https://twitter.com/PounceLight))
is a small relaxing game about doodling castles.

[This month](https://store.steampowered.com/news/app/2198150/view/3714952295473339216?l=english) was all about turning previous experiments
into reality.
The coloring and window prototypes are now proper features,
have dedicated UI, and play well with other building tools.

The devs have also been [toying with](https://twitter.com/h3r2tic/status/1663264361144565765) real-time global illumination
that could run on potato graphics cards.

![game screenshot: pixel art tile graphics](../../assets/c2afc687a755ee08.png)


Turtle Time by [@mikeder](https://mikeder.net) is a WIP p2p multiplayer turtle game
being made using Bevy, [ggrs](https://github.com/gschup/ggrs), and [matchbox](https://github.com/johanhelsing/matchbox).

This month [the first devlog](https://mikeder.net/blog/turtletime-devlog-1) was released:

- Quickly starting a project using
[bevy_game_template](https://github.com/NiklasEi/bevy_game_template). - Converting single player systems to multiplayer ones.
- Determinism, random spawns, and timers.

![instructions screen: game controls instructions](../../assets/eb3baefa71b46d09.jpg)


[DAshmoRE](https://hopfenherrscher.itch.io/dashmore) is a fast-paced arcade mobile game written using Bevy.

Get ready for a fast-paced and challenging arcade game where the only way to move is by skillfully dashing past enemies. With a single tap, you must navigate through a maze of enemies that move at different speeds and patterns. Can you master the art of dashing and achieve the highest score? Test your skills and reflexes in this thrilling arcade game.


The game’s features include:

- Single-tap controls and WASM build suited for playing on mobile phones.
- Power-ups like player repellent forcefields and slow-motion abilities.
- Integrated highscore system.

*Discussions: /r/rust_gamedev*

![one big space ship shooting lots of missles at another](../../assets/f3d3351460a0d64f.gif)

[NANOVOID](https://store.steampowered.com/app/2326430/NANOVOID) by [LogLogGames](https://loglog.games) is a WIP 2D tactical space shooter
that puts you in command of your own modular spaceship:
engage in intense, physics-driven battles, strategize with ship customization,
and outsmart your enemies.

This month [the first devlog](https://loglog.games/blog/nanovoid-devlog-1) was released
and it mostly was dedicated to experiments with Lua scripting.

Other updates include:

[A simple PID controller](https://twitter.com/LogLogGames/status/1659202148616523778)for rotating the ship.[The SFX for thrusters is now filtered](https://twitter.com/LogLogGames/status/1660062551651041281)based on the desired force.- On-hit SFX and explosions
[are starting to feel satisfying](https://twitter.com/LogLogGames/status/1660683311755165697). - Parts of the ship
[can now be individually inspected](https://twitter.com/LogLogGames/status/1663134570634461190)with pinnable UI. - Missiles targeting individual parts on enemy ships
[with some more UI tweaks](https://twitter.com/LogLogGames/status/1663667145018953729).

*Discussions: /r/rust_gamedev*

[Bevy Garage](https://github.com/alexichepura/bevy_garage) by [@alexichepura](https://mastodon.social/@alexichepura) is
a game-like car simulation playground
built with Bevy, rapier, and dfdx neural network.

Alexi released two introductory videos about the project:

[The main video](https://youtu.be/f6PcaTX58J4)that walks through the project.- Deep Q-Learning car training
[for 1 hour](https://youtu.be/A2JMPIWGXBsf).

You can also try out the WASM version of the simulation
[here](https://alexi.chepura.space/bevy-garage).

## Engine Updates [#](https://gamedev.rs#engine-updates)

![Demo of drawing with your hands in 3D space](../../assets/b12f1c208d9c8f8c.gif)


[stereokit-rs](https://github.com/MalekiRe/stereokit-rs) ([Discord](https://discord.com/invite/jtZpfS7nyK)) are bindings to [StereoKit](https://stereokit.net) - an easy-to-use
Mixed Realty engine, designed for creating VR, AR, and XR experiences.
While StereoKit is primarily intended to be used from C#,
all core functionality is implemented in native code,
and a C compatible header file is also available and
was used to create Rust bindings.

StereoKit’s features include:

- Wide platform support: HoloLens 2, Oculus Quest, Windows Mixed Reality, Oculus Desktop, SteamVR, Varjo, Monado (Linux), and eventually everywhere OpenXR is.
- Mixed Reality inputs like hands and eyes are trivial to access.
- Easy and powerful UI and interactions.
- Lots of model and texture formats are supported out of the box.
- Flexible shader/material system with built-in PBR.
- Performance-by-default instanced render pipeline.
- Flat screen MR simulator with input emulation for easy development.
- Runtime asset loading and cross-platform file picking.
- Physics.

You can use [a cargo-generate template](https://github.com/MalekiRe/stereokit-template) for a quick start
and the devs invite to join [their Discord server](https://discord.com/invite/jtZpfS7nyK)
if you have any questions.

*Discussions: /r/rust*

![screenshots from hotline’s tests](../../assets/9e549ffc0465c7c8.png)


[hotline](https://github.com/polymonster/hotline) ([Blog](https://www.polymonster.co.uk), [Twitter](https://twitter.com/polymonster), [Twitch](https://twitch.tv/polymonstr))
is a modern, high-performance, hot-reload graphics engine that
aims to provide low-level access to modern
graphics API features, while at the same time providing high-level ergonomic
optimizations.

[The recent updates](https://www.polymonster.co.uk/blog/building-new-engine-4) include:

- Tests of graphics functionality and lots of new examples,
- GPU Resources cleanup improvements,
- explicit API fore resource heaps,
- better bindless and bindful rendering models,
- GPU-driven ECS experiments.

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

![a scheme showing an agent jumping from pillar to pillar](../../assets/bd4f992a355ee3ba.png)


[@affanshahid](https://github.com/affanshahid) published [the first part of a new tutorial series](https://affanshahid.dev/posts/learning-game-dev-bevy-1)
on building a simple 2D platformer using Bevy.
The series is aimed at newcomers to the world of
game development and explores common game development concepts.

*Discussions: /r/rust*

![Game Development In Rust: Making A Strategy Game](../../assets/607082b57ef60359.png)

[@srodrigo](https://github.com/srodrigo) published the first three parts of a
[strategy game in Bevy series](https://srodrigoroyo.com/game-development-in-rust-strategy-game-1/). The series is aimed at
developers with some experience in Rust who want to dive into game development.

[The first part](https://srodrigoroyo.com/game-development-in-rust-strategy-game-1/)focuses on the basic concepts to create a battlefield for the battles to come.[The second part](https://srodrigoroyo.com/game-development-in-rust-strategy-game-2/)adds the first unit type.[The third part](https://srodrigoroyo.com/game-development-in-rust-strategy-game-3/)adds more unit types to create more compelling teams.

![Logos with ast-grep and bevy](../../assets/5fda0d6520321497.png)


[@HerringtonDarkholme](https://github.com/HerringtonDarkholme) published an [article](https://betterprogramming.pub/migrating-bevy-can-be-easier-with-semi-automation-here-is-how-1f6e21858e79)
about how to make Bevy migration easier by using git, cargo and [ast-grep](https://github.com/ast-grep/ast-grep).
The article uses the utility AI library [big-brain](https://github.com/zkat/big-brain) as an example
to illustrate bumping the Bevy version from 0.9 to 0.10
and covers four big steps: making a clean git branch,
updating the dependencies, running fix commands, and fixing failing tests.
By using semi-automation tools, you can migrate your Bevy projects
with less hassle and more confidence.

*Discussions:
/r/rust*

## Tooling Updates [#](https://gamedev.rs#tooling-updates)

![demo: switching between Jumpy/Punchy and choosing a verion](../../assets/35a315df9e1c4127.gif)


[Spicy Launcher](https://github.com/spicylobstergames/SpicyLauncher) by [@orhun](https://github.com/orhun) is a cross-platform launcher
for playing [Spicy Lobster](https://github.com/spicylobstergames) games.
Supports both command-line and [Tauri](https://tauri.app)-based graphical interface.

Currently supported games: [Fish Folk: Jumpy](https://github.com/fishfolks/jumpy), [Fish Folk: Punchy](https://github.com/fishfolks/punchy),
and recently added [Thetawave](https://github.com/thetawavegame/thetawave).

Planned features include auto updating games and mods management.

![Rerun showing 3D object detections in a 2D view](../../assets/39823e618cbb5e3b.gif)


[Rerun](https://rerun.io) ([Discord](https://discord.gg/npTFxYR9), [GitHub](https://github.com/rerun-io/rerun))
is an open-source SDK for logging complex visual data paired with a visualizer
for exploring that data over time. While its primary focus is on robotics and
computer vision, it can be useful for all kinds of
rapid prototyping & algorithm development.

Rerun was shown at the Rust GameDev meetup,
watch the recording [here](https://youtube.com/watch?v=dVk_kZ9VSDA).

[v0.6.0](https://github.com/rerun-io/rerun/releases/tag/v0.6.0) is out now! A few of the biggest highlights:

- You can now show 3D objects in 2D views connected by Pinhole transforms.
- You can quickly view images and meshes with
`rerun mesh.obj image.png`

. - The correct to install the rerun binary is now
`cargo install rerun-cli`

. - native_viewer is now an opt-in feature of the rerun library, leading to faster compilation times.
- SDK log calls are now batched on the wire, saving CPU time and bandwidth.
[Experimental WebGPU support](https://app.rerun.io/webgpu/index.html).

There’s a growing community on [Discord](https://discord.gg/npTFxYR9)
waiting for you to join in case you have any questions,
comments or just want to follow the latest development.
The [GitHub project](https://github.com/rerun-io/rerun) is MIT/Apache
licensed and open to contribute for everyone,
be it with suggestions, bugs or PRs.

[Smashline](https://github.com/blu-dev/smashline) is plugin and a Rust crate aimed at enhancing Smash modding,
more specifically focusing on script mods. Its main purpose is to enable
the replacement of different types of scripts found in Super Smash Bros. Ultimate,
while also offering additional utilities for creating what is known as “code mods”
within the modding community.

The [Smashline wiki](https://github.com/blu-dev/smashline/wiki) provides comprehensive explanations of its core features.

![Ruffle dekstop app](../../assets/ab5427b04e027334.png)


[Ruffle](https://ruffle.rs/) is an open-source Flash Player emulator written in Rust.
It brings Flash Player back to life, running smoothly on all modern systems
and web browsers.

[This month’s updates](https://ruffle.rs/blog/2023/05/29/progress-report.html) include:

- Bunch of new fan-favorite AS3 (ActionScript 3)games are now playable.
- Many graphics drawing methods have been fixed and implemented.
- XML support has progressed.
- AS2 (ActionScript 2) has seen progress as well: Additional XML methods have been implemented.
- The Ruffle desktop app now has an interface.
- Built-in save manager has been added.
- FLV support in progress, Flash content with external video files will be supported soon.

## Library Updates [#](https://gamedev.rs#library-updates)

![blit example: blitting the full sprite](../../assets/18ca67bf7b583dd3.png)


[blit](https://github.com/tversteeg/blit) is a GPL licensed library for quickly blitting 2D images on a pixel buffer.
After a long stale period development has resumed quite a bit
in the last couple of months.

The previous big release, [v0.7.0](https://github.com/tversteeg/blit/releases/tag/v0.7.0), saw a big improvement in performance
and API ergonomics. It also introduced interactive WebAssembly examples
[which can be seen here](https://tversteeg.nl/blit/showcase).

The latest big release, [v0.8.0](https://github.com/tversteeg/blit/releases/tag/v0.8.0), is a complete rewrite of the quite old
and admittendly outdated API. A focus has been put on both ergonomics and performance.
There’s now many ways of drawing a subsection, tiling, masking and creating
repeating slices of an image on a pixel buffer.

[seldom_state](https://github.com/Seldom-SE/seldom_state) is a Bevy plugin that adds a `StateMachine`

component that you
can add to your entities. The state machine will change the entity’s components
based on states, triggers, and transitions that you define. It’s useful
for player controllers, animations, simple AI, etc.

This month, [seldom_state](https://github.com/Seldom-SE/seldom_state) 0.6 was released:

- Triggers don’t need to be registered!
- MachineState and Trigger no longer require Reflect.
- StateMachine’s trans_builder accepts the current state in the closure, so you have dataflow between states!
- You may add and remove state components manually.
- More versatile on_enter and on_exit events.
- Trigger combinators
`not`

,`and`

, and`or`

. - Transitions have priority in the order they are added.
- You can use EventReader, Local, etc in your triggers!
- Added an
`EventTrigger<E>`

that triggers on an event. - StateMachine’s set_trans_logging sets whether to log state transitions
[And more](https://github.com/Seldom-SE/seldom_state/blob/main/CHANGELOG.md#06-2023-05-07)!

Thanks to [Sera](https://github.com/deifactor) for coauthoring this update!

[Kira](https://crates.io/crates/kira) ([GitHub](https://github.com/tesselode/kira)) by [@tesselode](https://twitter.com/tesselode) is a backend-agnostic library to create
expressive audio for games.

Kira v0.8 adds support for spatial audio, global modulation sources for easier and more powerful parameter tweening, compressor and EQ effects, and more powerful playback and loop region settings.

*Discussions:
/r/rust*

## Other News [#](https://gamedev.rs#other-news)

- Other game updates:
[Maginet will soon get a level editor](https://twitter.com/evrimzone/status/1658908555582341120)with in-editor play support.[@NullableEngineer released a vlog](https://youtube.com/watch?v=rHM-4vj3uyY)about implementing the first iteration of the network server for their WIP MMO.[Idu got a new water system](https://mastodon.gamedev.place/@johann/110440559190280054)that is a lot faster to and easier to render.

- Other engine updates:
[godot-rust got a new website](https://mastodon.gamedev.place/@GodotRust/110367270830037001)with latest API docs and direct links to learning resources and community platforms.[Bevy will get WebGPU support](https://reddit.com/r/rust/comments/13lb0h8/bevy_webgpu)in the next - v0.11 - release.

- Other learning material updates:
[@PhaestusFox](https://youtube.com/@PhaestusFox)has posted Bevy-related tutorial videos:[Herbal-Alchemy 1.4 Update](https://youtube.com/watch?v=MSsuR_6MqwE)and[“How to make a view cube in Bevy”](https://youtube.com/watch?v=HpAu1LpYNpM).

- Other library updates:
[grid](https://reddit.com/r/rust/comments/134l6mk/grid_v0_10)is a simple library that provides an easy to use and fast 2D grid data structure.[hexx](https://github.com/ManevilleF/hexx/releases/tag/0.6.0)v0.6 brings a bunch of new algorithms for hexagonal maps and overall API improvements.[faer](https://reddit.com/r/rust/comments/13ggs7k/faer_09)0.9 brings the non hermitian eigenvalue decomposition for real and complex matrices and also comes with the release of[qd](https://lib.rs/qd), a library for extended precision floating point arithmetic with faer compatibility.[quinn](https://github.com/quinn-rs/quinn/releases/tag/0.10.0)v0.10 introduces MTU discovery, updates to the latest version of rustls, improves platform support, and introduces a variety of new features, performance improvements, and bugfixes[funutd](https://github.com/SamiPerttu/funutd)is a 3D procedural texture library running on the CPU that features different tiling modes, an endless supply of proc-generated self-describing volumetric textures, Palette generation with Okhsv and Okhsl color spaces, and an interactive texture explorer.[bevy_diagnostics_explorer](https://github.com/zaycev/bevy-diagnostics-explorer)is a plugin allowing to visualize diagnostics (tracing spans) in VSCode.[pxo](https://github.com/appybara13/pxo)is a library for working with[Pixelorama](https://github.com/Orama-Interactive/Pixelorama)files.[frug](https://reddit.com/r/rust/comments/13im07r/introducing_frug)is a simple graphics library that was announced this month along with[some docs](https://santyarellano.github.io/frug_book).[egui](https://reddit.com/r/rust/comments/13px5zb/egui_022)v0.22 brings support for application icons on Windows and Mac, better dark/light mode detection, and error reporting on the web.[egui_tiles](https://github.com/rerun-io/egui_tiles)is a tiling layout engine for egui with drag-and-drop and resizing.


## Discussions [#](https://gamedev.rs#discussions)

- /r/rust:
- /r/rust_gamedev:

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[bevy_mod_scripting is looking for maintainers](https://github.com/makspll/bevy_mod_scripting/issues/48).[‘Are We Game Yet?’ wants to know about projects/games/resources that aren’t listed yet](https://github.com/rust-gamedev/arewegameyet#contribute).[Graphite is looking for contributors](https://graphite.rs/contribute)to help build the new node graph and 2D rendering systems.[winit’s “difficulty: easy” issues](https://github.com/rust-windowing/winit/issues?q=is%3Aopen+is%3Aissue+label%3A%22difficulty%3A+easy%22).[Backroll-rs, a new networking library](https://github.com/HouraiTeahouse/backroll-rs/issues).[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[A/B Street’s “good first issue” issues](https://github.com/a-b-street/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/D-Good-First-Issue).[Ambient’s “good first issue” issues](https://github.com/AmbientRun/Ambient/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22).

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!

**Discuss this post on**:
[/r/rust_gamedev](https://reddit.com/r/rust_gamedev/comments/14o566f/rust_gamedev_46),
[Mastodon](https://mastodon.gamedev.place/@rust_gamedev/110640765829636039),
[Twitter](https://twitter.com/rust_gamedev/status/1675242617917829122),
[Discord](https://discord.gg/yNtPTb2).