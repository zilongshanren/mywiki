---
title: 'This Month in Rust GameDev #45 - April 2023'
url: https://gamedev.rs/news/045/
author: Rust GameDev WG
published: '2023-05-31'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 45th issue of the Rust GameDev Workgroup’s
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

[Announcements](https://gamedev.rs/news/045/#announcements)[Game Updates](https://gamedev.rs/news/045/#game-updates)[Engine Updates](https://gamedev.rs/news/045/#engine-updates)[Learning Material Updates](https://gamedev.rs/news/045/#learning-material-updates)[Tooling Updates](https://gamedev.rs/news/045/#tooling-updates)[Library Updates](https://gamedev.rs/news/045/#library-updates)[Other News](https://gamedev.rs/news/045/#other-news)[Discussions](https://gamedev.rs/news/045/#discussions)[Requests for Contribution](https://gamedev.rs/news/045/#requests-for-contribution)

## Announcements [#](https://gamedev.rs#announcements)

### Rust GameDev Meetup [#](https://gamedev.rs#rust-gamedev-meetup)

![Gamedev meetup poster](../../assets/325cbc698fea0e93.png)


The 26th Rust Gamedev Meetup took place in March. You can watch the recording
of the meetup [here on Youtube](https://youtube.com/watch?v=Vq60NvWy8Io).
The meetups take place on the second Saturday of every month via the [Rust
Gamedev Discord server](https://discord.gg/yNtPTb2) and are also [streamed on
Twitch](https://twitch.tv/rustgamedev).

![list of winners](../../assets/35f981d7d8175273.jpg)


Voting on the [Bevy Jam 3](https://itch.io/jam/bevy-jam-3) has finished! It was a
week-long event, where the goal was to make a game in
[Bevy Engine](https://bevyengine.org/), the free and open-source game engine
built in Rust. The theme was ‘Side Effects’.

- 1:
[LinkSider](https://kuviman.itch.io/linksider)by kuviman, daivy, shadow-crusherz - 2:
[Neon Breach: Tower Defence](https://louisnivrat.itch.io/neon-breach-tower-defence)by louisNivrat - 3:
[Battle for Rattoria](https://jabuwu.itch.io/battle-for-rattoria)by jabuwu

The jam had a solid turnout with 353 participants, 78 submissions, and 2,158 ratings! A lot of the submissions have a web build so it’s easy to try them out yourself.

The [full results can be found on itch.io](https://itch.io/jam/bevy-jam-3/results).

Another Rusty Jam starts on May 21st!

It’s a great chance to try out some new Rusty tech, form a team of like-minded rustaceans, and feel what a full cycle of making a game in Rust feels like in miniature!

This jam focuses more on using Rust than anything else. That means you aren’t restricted on your design, music, or graphics, as long as you use Rust to make it!

The optional-to-use theme for the jam is going to be announced
in [the jam’s Discord](https://discord.gg/8dUQJFFmxG) and pinned in the community section.
While you’re waiting for the theme, you can start looking for a team
in the looking-for-team Discord channel.
If you want solo though, that’s fine too.

## Game Updates [#](https://gamedev.rs#game-updates)

![hundreds of npcs smoothly interpolating](../../assets/116f4b0542bd30cc.jpg)

CyberGate ([YouTube](https://youtube.com/channel/UClrsOso3Xk2vBWqcsHC3Z4Q), [Discord](https://discord.gg/R7DkHqw7zJ)),
an ambitious multiplayer project in development by CyberSoul,
aims to invite players into a constantly evolving universe.
Harnessing the power of procedural generation and artificial intelligence,
this work-in-progress aspires to provide an engaging experience
that emphasizes exploration and discovery across its diverse worlds.

The latest updates to CyberGate include:

- Networking Interpolation version 2: increased reliability over frame rate changes, improved accuracy of object motion and detail by ~20%, and objects update 12-45 milliseconds faster.
- Server compilation was drastically simplified (100x faster).
- Improved browser server process, to have more consistent behavior.
- Improved mouse lock on browsers.
- Simplified code related to state synchronization.
- Significant gameplay changes and bug fixes.

They are currently working on universe generation alghorithms for version 8.0.
Participate [by joining the Discord server](https://discord.gg/R7DkHqw7zJ).

![Online Matchmaking Menu Page](../../assets/3c4943643dc62d0e.png)

[Jumpy](https://github.com/fishfolks/jumpy) ([GitHub](https://github.com/fishfolks/jumpy), [Discord](https://discord.gg/4smxjcheE5), [Twitter](https://twitter.com/spicylobsterfam)) by
[Spicy Lobster](https://spicylobster.itch.io) is a pixel-style, tactical 2D shooter with a fishy
theme.

In the last month, Jumpy released [v0.7.0](https://github.com/fishfolk/jumpy/releases/tag/v0.7.0) with support for online
and LAN network games! Networking has been a long time coming, with many
architecture decisions being made specifically with networking in mind. While
network performance may still need to be tweaked, and there are still some bugs
to fix, the proof-of-concept was a success. You can start matches on your local
network, or online, with no configuration necessary!

The Fish Folk game series has a [pre-launch page up on Kickstarter](https://www.kickstarter.com/projects/erlendsh/fish-folk),
expected to go public in mid-May.

![thetawave-gameplay](../../assets/f195edb65bbf5e5e.gif)


Thetawave is an open-source, physics based, space shooter game.
This month, Thetawave 0.1.0 was [released](https://github.com/thetawavegame/thetawave/releases/tag/v0.1.0).
The main features of this update were:

- local multiplayer,
- a second character,
- many sprite adjustments,
- and many gameplay tweaks from in-person playtesting with
the
[thetawave arcade cabinet](https://twitter.com/carlosupina/status/1650200385485774850).

The easiest way to play the most up to date version of Thetawave
on your machine is to download it through the
[Spicy Launcher](https://github.com/spicylobstergames/SpicyLauncher/releases/tag/v0.3.0). Otherwise, you can play the game in your
browser on the [itch.io page](https://metalmancy.itch.io/thetawave).

Feel free to reach out in the #thetawave channel in
the [Spicy Lobster discord server](https://discord.gg/52WCcgJkcE) if you are
interested in contributing.

[Way of Rhea](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n45) is a puzzle game with hard puzzles and forgiving
mechanics being produced by [@masonremaley](https://twitter.com/masonremaley) in a custom Rust engine.
You can support development by [checking out the free demo and wishlisting on Steam](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n45)
or [signing up for the mailing list](https://anthropicstudios.com/newsletter/signup/tech)!

Recent updates:

- Time controls (pause, play, fastforward)
- Staves switch in place so that crabs don’t inadvertently move them when cycling
- Increased drag on various physics objects to prevent bouncing over targets
- Increased staff throw velocity to make it easier to throw staves off ledges
- Improved interactive hover visuals on staves
- Fixed bug where you could take objects from the crab while he’s riding the elevator
- Fixed edge cases around saving on load screens
- Fixed edge cases with sleep system and pausing
- More flexible save points in crab puzzles (save points can now conditionally trigger only when a crab is present)
- More work on end game

Also, Way of Rhea was part of the [Steam Puzzle Fest](https://store.steampowered.com/category/puzzle_matching)!

![game title in ascii art as a game’s level](../../assets/e8a1d551f67b8c4f.png)


[l1t](https://github.com/alex-laycalvert/l1t) by [@alex-laycalvert](https://aldevelop.com) is a WIP terminal game about
shooting lasers and lighting statues to solve puzzles.

In each level, you have to configure mirrors, lasers, and other items to light up all the statues while avoiding any mishaps like shooting yourself with a laser beam.

There’s only 4 core levels right now but in addition to adding more the developer is working on a repository system where web servers can host level files and users can subscribe to them.

*Discussions: /r/rust*

![new menu screenshot](../../assets/e3506fc9d99bb309.png)


[Maginet](https://evrimzone.itch.io/maginet) by [Evrim](https://twitter.com/evrimzone) is a fast-paced turn-based strategy game
with local/versus-ai/online play on PC/mobile
where two guilds of mages battle each other.

[This month’s updates](https://evrimzone.itch.io/maginet/devlog/519667/grand-ceremony-for-the-beta) include:

- New mage and board sprites from
[@MrmoTarius](https://twitter.com/MrmoTarius). - New main menu that brings the ability to switch between loadout modes.
- Better AI heuristics for evaluating the board.
- Better health UI.

The developers are looking for feedback from testers.

![tree branches on top of water](../../assets/412a22bd71ce55ca.jpeg)


[Idu](https://epcc.itch.io/idu) ([Discord](https://discord.gg/MeGauteMj3)) is a strategic sandbox game about growing
plants that wish to reclaim nature, developed by [Elina Shakhnovich](https://mastodon.gamedev.place/@eli)
and [Johann Tael](https://mastodon.gamedev.place/@johann) featuring a bespoke Vulkan-based engine in Rust.

This month [a new demo was released](https://epcc.itch.io/idu/devlog/513652/demo-version-10-flower-tuned-antennas):

- New inventory and interaction system.
- Office file cabinets for keeping things tidy.
- Converters convert signals from nearby flowers into colorful blocks.

![three small windows are merged into one bigger one](../../assets/6db3896bc2987acd.gif)

[Tiny Glade](https://store.steampowered.com/app/2198150/Tiny_Glade) ([Twitter](https://twitter.com/PounceLight), [Youtube](https://youtube.com/@pouncelight)) is a small relaxing game
about doodling castles.

[This month’s updates](https://store.steampowered.com/news/app/2198150?emclan=103582791472800070&emgid=3682298662732600151) include:

- More brick colors.
- New gothic windows style.
- Ability to merge windows together into a bigger one.
- New arch algorithm that works better for rough terrain.
- The project’s beta testing should start this summer and the release should happen somewhere in 2024.

![NYX awards banners on top from a screenshot from the game](../../assets/712fd570e055c2cb.jpg)


[Hydrofoil Generation](https://hydrofoil-generation.com)
([Steam](https://store.steampowered.com/app/1448820/Hydrofoil_Generation), [Facebook](https://facebook.com/HydrofoilGenerationSailing/), [Discord](https://discord.gg/DtKgt2duAy/))
is a realistic sailing/foiling inshore simulator in development for PC/Steam
that puts you in the driving seat of modern competitive sailing
that is available in Early Access on Steam.

[This month’s updates](https://steamcommunity.com/app/1448820/allnews) include:

- A brand new location to test your hydrofoil skills:
[Bermuda](https://youtube.com/watch?v=qUggXlUfflY). - An improved protocol for line crossing detection is now implemented, which means that Hydrofoil Generation is now even more fair and accurate.
- Also,
[the game won](https://store.steampowered.com/news/app/1448820/view/3723957592121893508)two Silver awards for the PC Game: Racing and Simulation category.

## Engine Updates [#](https://gamedev.rs#engine-updates)

![a set of cool and mostly physics-centered demos](../../assets/947afb9b6e452b05.gif)

[Ambient 0.2](https://www.ambient.run/post/ambient-0-2) is now out after two months of development.
Ambient is an open-source runtime for building high-performance multiplayer
games and 3D applications powered by WebAssembly, Rust and WebGPU. Projects
consist of assets and logic built around the currently Rust-only Ambient API,
and these projects can be loaded by any compatible runtime running on any
platform.

This release brings a few major features, including basic support for playing sounds, being able to run WASM on the client (in addition to the server), and automatic proxying of servers by the Ambient Proxy. This allows anyone with the URL to connect to a server, without having to worry about port forwarding.

Finally, Ambient UI can now be used from guest code. Combined with networking and ECS, this unlocks an exciting new capability: multiplayer UI! The blog post walks through the creation of a basic multiplayer beat sequencer using these features.

Check out [the GitHub](https://github.com/AmbientRun/Ambient) to get started with building for/or
on Ambient yourself, or chat with the developers and other explorers on
[the Discord](https://discord.gg/ambient).

*Discussion: /r/rust, Hacker News*

![godot-rust GDExtension logo](../../assets/6e35dd625d5ad6f6.png)


The Godot 4 binding for Rust, also known as [gdext](https://github.com/godot-rust/gdext), now features
[a reworked website](https://godot-rust.github.io). The site acts as a hub to all the relevant
resources and community platforms. It also hosts auto-generated API docs
from `cargo doc`

, for latest snapshots and active pull requests.

On the library side, April has brought [lots of improvements](https://github.com/godot-rust/gdextension/pulse/monthly)
regarding engine interaction, notably:

- FFI bugfixes (
[#234](https://github.com/godot-rust/gdextension/issues/234),[#249](https://github.com/godot-rust/gdextension/issues/249),[#250](https://github.com/godot-rust/gdextension/issues/250)) - Class constants and notifications (
[#219](https://github.com/godot-rust/gdextension/issues/219),[#223](https://github.com/godot-rust/gdextension/issues/223)) `Callable`

support ([#231](https://github.com/godot-rust/gdextension/issues/231))- Initial threading experiments (
[#212](https://github.com/godot-rust/gdextension/issues/212))

For the near future, the plan is to iron out the new website and CI, as well as some QoL improvements such as better compile times.

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

![bevy logo](../../assets/fe288982cad2df06.png)


[Piotr Siuszko](https://mastodon.gamedev.place/@MevLyshkin) wrote [a blog post](https://mevlyshkin.com/blog/bevy-github-actions)
explaining how to automate building and publishing game written with Bevy
to GitHub Pages using GitHub Actions.

![red dots or black bg](../../assets/f1764abed2a2a5c6.gif)

[Yendor](https://github.com/lecoqjacob) published [a mini-tutorial series](https://lecoqjacob.github.io/bevy_shader_playground/bevy_gol_example/index.html)
exploring compute shaders in Bevy using their [Game of Life example](https://github.com/bevyengine/bevy/blob/main/examples/shader/compute_shader_game_of_life.rs)
and adding some new features to it: camera controller, wrapping simulation, and
drawing on the simulation.

![TDD in Rust game dev with bevy](../../assets/4c910bdbbad074ad.png)


[Edgardo Carreras writes about his experience](https://edgardocarreras.com/blog/tdd-in-rust-game-engine-bevy) with Test-Driven Development
while developing a game engine in Rust using Bevy. TDD is an iterative software
development approach that involves writing automated tests before writing the code.
In the article, Edgardo explains the benefits of TDD and how it can help in game
development. He also shares his testing process, including how he used Bevy’s ECS
architecture to write tests for his game engine.

*Discussions: /r/rust_gamedev*

![a couple characters moving around and interacting](../../assets/b509f05ddbab702c.gif)


[@maciekglowka](https://mastodon.gamedev.place/@maciekglowka) started a blog series on creating a
roguelike game using Bevy Engine.
There are currently seven parts, focusing mostly on setting up a basic
game architecture. The topics discussed so far include: separating logic from
graphics in the ECS; designing a turn-based game loop; command pattern
for the unit actions.

The first part of the series can be found [here](https://maciejglowka.com/blog/bevy-roguelike-tutorial-devlog-part-1).

*Discussions:
/r/roguelikedev*

![phaestusfox youtube](../../assets/b257f99c8b0bff8d.png)


[@PhaestusFox](https://youtube.com/@PhaestusFox) released a bunch of new Bevy tutorials
on Youtube about all things Bevy.
Level up your game dev skills with PhaestusFox’s tutorials and learn more from
very basic how-to’s to more complex full tutorials like how to make a platformer
in Bevy.

![Katamari gif](../../assets/bcb9b9c80a2cb147.gif)


[Ryosuke](https://mastodon.gamedev.place/@whoisryosuke) recently participated in a Bevy game jam.
Ryosuke’s goal was to create a game inspired by Katamari Damacy, an old
PlayStation 2 game. In the game, a prince rollsup objects to make planet
sized balls.
Ryosuke shares their [learning process](https://whoisryosuke.com/blog/2023/making-katamari-for-bevy-game-jam) of the almost-finished
Katamari clone running on Windows. They cover topics like the physics library and
how they created the user interface using a tool egui.
It is also suggested to have some basic knowledge of Bevy game engine
before you dive into the article.

![3D Midi Piano](../../assets/9de703e2a3dbfc09.gif)


[Ryosuke](https://mastodon.gamedev.place/@whoisryosuke) has also recently published [a tutorial](https://whoisryosuke.com/blog/2023/3d-midi-piano-using-rust-and-bevy)
on how to create a 3D MIDI piano visualizer app using the
Bevry game engine in Rust. They shared their learning experience, including
reading MIDI input with Rust and integrating it with the game engine.

![Blender result with colored vertical layers](../../assets/1b632f7f147f77d2.png)


[Theor](https://github.com/theor) became interested in the data format of the classic game Doom
and decided to write Rust code to extract its maps and convert them into vector
graphics for laser cutting.
Theor’s [blog post](https://theor.xyz/doom-maps-laser-cut/) explores Doom specifics, geometry, writing SVG,
rendering and triangulation.

*Discussions: /r/rust*

![strategy game bevy console](../../assets/2156d2326c1115a2.png)


[Sergio Rodrigo Royo](https://srodrigoroyo.com/about/) started [a new series](https://srodrigoroyo.com/game-development-in-rust-strategy-game-1) about
creating a 2D turn-based strategy game in Rust. In this tutorials one will learn
how to’s such as: adding differents units, sound effects, providing multiplayer support,
and designing a simple UI.

![3d football](../../assets/bcac801de692e17c.jpg)


[UnravelSports](https://unravelsports.github.io/) recently presented their [latest project](https://github.com/UnravelSports/rs-football-3d).
The project is a proof-of-concept to show football data in 3D and the ultimate goal
is to utilize this feature to animate body-pose data and potentially connect it
to a VR in the future.

Check out a recent [PySport talk](https://youtube.com/watch?v=VwatoPOKIl8) for more in-depth info.

![Flappy bird](../../assets/c244b67dbcd32d31.png)


[bones-ai](https://github.com/bones-ai) recently shared [their project](https://github.com/bones-ai/rust-flappy-bird-ai),
which is a neuro-evolution simulation of an AI playing popular game Flappy Bird.

In the [youtube video](https://www.youtube.com/watch?v=Ea_N1CJwMR8) 1000 AI agents are released into
the game environment of Flappy Bird with the goal of learning how to survive and
stay alive for as long as possible.

## Tooling Updates [#](https://gamedev.rs#tooling-updates)

Rustracer, a PBR [glTF 2.0](https://www.khronos.org/gltf) renderer based on Vulkan ray-tracing.
It can render (almost) any glTF 2.0 scene by pure path tracing
at an interactive speed.
Compared with rasterization-based glTF renderers, Rustracer needs some
(scene-dependent) time for sample accumulation in exchange for global illumination.

On top of that, the control panel provides a rich set of viewing options and debugging utilities.

It also can serve as a glTF viewer or a reference renderer.

The code base itself is a learning resource for [Ash](https://github.com/ash-rs/ash) (Vulkan bindings in Rust),
hardware ray tracing and glTF processing in Rust.

![tile map editor and other tool windows like command event editor](../../assets/0be463810716bc08.png)


[Luminol](https://github.com/Astrabit-ST/Luminol) by [@speak2erase](https://github.com/Speak2Erase) and [@somedevfox](https://github.com/somedevfox) is a remake
of the RPG Maker editor, based mostly off of [RPG Maker XP](https://store.steampowered.com/app/235900/RPG_Maker_XP)
(aka RMXP), with the intent of creating a more modern, feature rich,
and open source version of RMXP.

RGSS, RMXP’s runtime, has already been open sourced thanks to [mkxp](https://github.com/Ancurio/mkxp).
However, despite several attempts, no one has fully remade the editor.
There are [some tools](https://github.com/20kdc/gabien-app-r48) out there that cover some of its functionality,
but none are user friendly, nor feature complete.

RGSS is actually quite enjoyable to use. The actual editor though - not so much: dated and often unintuitive UI, extensibility issues, binary format that is allergic to source control, and arbitrary limits that never existed in previous versions. Luminol was born out of sheer frustration from dealing with these issues - and hopes to fix them!

Luminol’s key differences:

- Completely GPU accelerated (RMXP is software rendered).
- Edit multiple maps at the same time.
- Multiple data formats.
- Edit encrypted archives (rgssad).
- Open-source.
- Better user experience overall.

Luminol is currently looking for contributors:
[there is a lot to be done](https://github.com/Astrabit-ST/Luminol/issues).
If you’d like to help contribute, please reach out to [@speak2erase](https://github.com/Speak2Erase)!

![Graphite logo](../../assets/36dcca7dc5fe634f.png)


Graphite ([website](https://graphite.rs), [GitHub](https://github.com/GraphiteEditor/Graphite),
[Discord](https://discord.graphite.rs), [Twitter](https://twitter.com/GraphiteEditor)) is a free,
in-development raster and vector 2D graphics editor based around a Rust-powered
node graph compositing engine.

April’s [sprint 25](https://github.com/GraphiteEditor/Graphite/milestone/25) developments:

- Brushing up: The new Brush tool makes it possible to paint raster-based art.
- Writing down: A refactor of the Text tool integrates typographic content in the node graph. Finally, all artwork types are node-based.
- Showing true colors: Node graph compositing now uses linear, not gamma, color. Key new color adjustment nodes are added.
- Laying the groundwork: Further engineering work prepares the node graph language for GPU execution. And development continues toward in-graph layer stack compositing.

As always, new contributors are cordially invited to
[get involved](https://graphite.rs/contribute) and take on
[approachable issues](https://github.com/GraphiteEditor/Graphite/labels/Good%20First%20Issue) with help from the
project’s friendly and supportive developer community on Discord.

[Open Graphite](https://editor.graphite.rs) in your browser and start creating!

![many images opened in one window](../../assets/60a3d40858c3699a.jpg)


[Image Maniac](https://github.com/AllenDang/img_maniac) is a cross-platform image viewer designed for game developers
and other creative professionals. The project’s features include:

- Infinite canvas for drag-n-dropping many images onto the main window, and view them all in a single, unified workspace.
- Quick RGBA channel switching using number keys is usefil for game developers who work with textures and materials.
- Broad format support including PNG, JPG, BMP, DDS, TGA, KTX2, and HDR.
- Focus on performance even with large files and multiple image at once.

*Discussions: /r/rust*

## Library Updates [#](https://gamedev.rs#library-updates)

![left part is "crab simulator" game where the player gains an item
right part is "clash of crabs" where player is able to use the item](../../assets/d4987386fa82d6f3.jpg)

[Backpack](https://github.com/Vrixyz/backpack) is an inventory system to share items between different games,
for example:

- Raise a crab in Crab Simulator,
- Make it fight in Crab Shooter,
- Cook it in Crab Cook…
- Gain a crab skin in your favorite game!

[Backpack](https://github.com/Vrixyz/backpack) is in a pre-MVP state: a tech prototype is working.

The project is not affiliated or related to Blockchain/NFTs: it uses a PostgreSQL DB to store users, games and items. Authentication is done via email/password, third party authentication via OAuth will be a future goal. An Authenticated user can create apps and add item definitions to these. Other users can get an independent instance of that item and modify its data.

The next project milestone is 2 minimalist interconnected games released by the end of 2023.

## Other News [#](https://gamedev.rs#other-news)

- Other game updates:
[Combine&Conquer v0.5.2](https://buckmartin.de/combine-and-conquer/2023-04-05-v0.5.2.html)brings significant graphical improvements.- exocave - an FPS about exploring a subterranean world -
[got a grappling hook](https://cragwind.itch.io/exocave/devlog/516142/grappling-hook)to ease the movement through caverns and chasms. [Railroad Scheduler](https://coffejunkstudio.itch.io/railroad-scheduler)is a game about planning routes and scheduling for a set of trains.[Stellar Cortex’s first devlog is out](https://bentley.codes/stellar-cortex/foundations-of-a-space-based-economy): it talks about foundational systems that should allow space based commerce.[Logic RPG](https://logicprojects.itch.io/logic-rpg)got two vlogs:[about CI and docs](https://youtube.com/watch?v=a9LZYozNChg)and[post processing, 3D conversions, and physics](https://youtube.com/watch?v=SmqQ_Is9QX8).[Elttob released a couple vlogs](https://youtube.com/playlist?list=PLsFMLV-H_GYt8KzbJnzrapNkUNtRcBB2n)about their voxel game Stockholm.[Digital Extinction’s recent updates](https://mgn.cz/blog)include unit manufacturing, shadows, and multiplayer.

- Other engine updates:
- Other learning material updates
[@PsichiX posted a tutorial](https://psichix.github.io/Intuicio/tutorial/index.html)on building your own scripting solution with Intuicio.

- Other tooling updates:
[ironboy](https://reddit.com/r/rust/comments/12qj2ty/ironboy)by @nicolas-siplis is a high accuracy GameBoy emulator written in Rust and available in the browser via WASM.

- Other library updates:
[Strolle](https://reddit.com/r/rust/comments/12u4ovi/strolle)is an experimental real-time renderer that supports global illumination.[blend v0.8](https://github.com/lukebitts/blend/blob/master/CHANGELOG.md#blend-08)brings better support for Blender primitives and API improvements.[lox](https://reddit.com/r/rust/comments/12teoxi/lox_a_fast_polygon_mesh_library)is a library for creating, generating, processing, and analyzing polygon meshes.[bitcode](https://reddit.com/r/rust/comments/12nw1pc/bitcode_format)is a games-oriented bitwise encoder/decoder which attempts to shrink the serialized size without sacrificing speed.[virtual_joystick](https://github.com/SergioRibera/virtual_joystick)provides virtual joystick UI widgets for Bevy projects.[faer v0.7](https://reddit.com/r/rust/comments/12estz9/faer_07)and[v0.8 releases](https://reddit.com/r/rust/comments/12tw26r/faer_08)bring better SIMD operations support for non native types and overall performance improvements.[egui_graphs](https://github.com/blitzarx1/egui_graphs)provides an interactive graph visualization widget powered by egui and petgraph.[Alkahest](https://reddit.com/r/rust_gamedev/comments/12auz7o/alkahest_02)is a schema-based serialization library that features infallible serialization, zero-overhead serialization of sequences, lazy deserialization and supports wide variety of formulas.[wgpu v0.16](https://github.com/gfx-rs/wgpu/releases/tag/v0.16.0)brings a bunch of changes to sync with latest spec, improved APIs, and lots of bugfixes.[the png create](https://reddit.com/r/rust/comments/12ks0ka/png_crate_gets_an_ultrafast_compression)got an ultrafast compression mode - up to 4x faster decompression.


## Discussions [#](https://gamedev.rs#discussions)

- /r/rust_gamedev:

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[‘Are We Game Yet?’ wants to know about projects/games/resources that aren’t listed yet](https://github.com/rust-gamedev/arewegameyet#contribute).[Graphite is looking for contributors](https://graphite.rs/contribute)to help build the new node graph and 2D rendering systems.[winit’s “difficulty: easy” issues](https://github.com/rust-windowing/winit/issues?q=is%3Aopen+is%3Aissue+label%3A%22difficulty%3A+easy%22).[Backroll-rs, a new networking library](https://github.com/HouraiTeahouse/backroll-rs/issues).[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[A/B Street’s “good first issue” issues](https://github.com/a-b-street/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/D-Good-First-Issue).[Ambient’s “good first issue” issues](https://github.com/AmbientRun/Ambient/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22).

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!

**Discuss this post on**:
[/r/rust_gamedev](https://reddit.com/r/rust_gamedev/comments/13xh0q7/this_month_in_rust_gamedev_45_april_2023),
[Mastodon](https://mastodon.gamedev.place/@rust_gamedev/110469105162579330),
[Twitter](https://twitter.com/rust_gamedev/status/1664256969408913411),
[Discord](https://discord.gg/yNtPTb2).