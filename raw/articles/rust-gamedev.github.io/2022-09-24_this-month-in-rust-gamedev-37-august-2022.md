---
title: 'This Month in Rust GameDev #37 - August 2022'
url: https://gamedev.rs/news/037/
author: Rust GameDev WG
published: '2022-09-24'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 37th issue of the Rust GameDev Workgroup’s
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

## Announcements [#](https://gamedev.rs#announcements)

![Bevy Jam 2](../../assets/ee4ac988c4e0cccd.png)


Voting on [Bevy Jam #2](https://itch.io/jam/bevy-jam-2/) just finished! It was a
10 day event, where the goal was to make a game in
[Bevy Engine](https://bevyengine.org/), the free and open-source game engine
built in Rust. The theme was ‘Combine’.

The [full results can be found on itch.io](https://itch.io/jam/bevy-jam-2/results). There were 404 participants,
85 submissions, and 2,674 ratings, making it the biggest Bevy Jam yet!
(And maybe the biggest Rust game jam ever?)

Here are the top five games:

#### 🥇 First Place: [USA Football League Scouting Combine XLV](https://ramirezmike2.itch.io/usa-football-league-scouting-combine-xlv) [#](https://gamedev.rs#1st-place-medal-first-place-usa-football-league-scouting-combine-xlv)

![USA Football League Scouting Combine XLV logo](../../assets/23a0105c7160135e.png)


[USA Football League Scouting Combine XLV](https://ramirezmike2.itch.io/usa-football-league-scouting-combine-xlv) is a game where you take
part in the historic unveiling of the “Combine Combine” event at this year’s
USA Football League Scouting Combine!

USAFLSCXLV is singleplayer action game where you attempt to score as many touchdowns as you can while avoiding professional football players, navigating a corn maze and also avoiding a combine machine harvesting the maze.

The source for the game is available on [GitHub](https://github.com/ramirezmike/bevy_jam_02_entry).

#### 🥈 Second Place: [Loot Goblin](https://park-dev.itch.io/loot-goblin) [#](https://gamedev.rs#2nd-place-medal-second-place-loot-goblin)

![Loot Goblin](../../assets/b6c1664a149dbbd3.png)


[Loot Goblin](https://park-dev.itch.io/loot-goblin) is a game where you craft your way to victory in a
unique adventurer’s backpack simulation!

We’re going dungeon crawling, but all the hard work is done for you by the valiant Sir Hoardalot, and you, as his resourcesful Loot Goblin are going to keep his backpack in order! Craft potions and weapons to strengthen the hero, and help kill the evil Ogre Necromancer.

The source code for the game is available [on GitHub](https://github.com/vanGeck/bevy-jam-2).

#### 🥉 Third Place: [Shanty Quest: Treble at Sea](https://jabuwu.itch.io/shanty-quest) [#](https://gamedev.rs#3rd-place-medal-third-place-shanty-quest-treble-at-sea)

![Shanty Quest Screenshot](../../assets/98f66366ba7eb7de.png)


In [Shanty Quest: Treble at Sea](https://jabuwu.itch.io/shanty-quest), you combine the magical instruments
and become the Pirate King!

The source code is available on [GitHub](https://github.com/jabuwu/shanty-quest).

![Combobox Screenshot](../../assets/bbbc5056799e7ca8.png)


[Combobox](https://combobox-game.itch.io/combobox) is a game where you navigate through space with a tiny robot
combining boxes with unique features!

The source code is available on [GitHub](https://github.com/ComboboxGame/Combobox).

#### Fifth Place: [Mole Rancher](https://infinitefall.itch.io/mole-rancher) [#](https://gamedev.rs#fifth-place-mole-rancher)

![Mole Rancher Screenshot](../../assets/65e40ef4beced015.png)


[Mole Rancher](https://infinitefall.itch.io/mole-rancher) is a game where you made it through university, got
your PhD, and now you have been selected to work in an top secret experimental
facility which promises a way to generate infinite energy through the combination
of various strange particles.

Use power to generate curious molecules, check their properties in your logbook, monitor their progress through your trusty E-merge device, and try not to let the reactor overheat!

And don’t worry about those armed guards on the way in, as long as you meet your quota then you’ll have no problems…

The source for this game is available on [GitHub](https://github.com/V4L3NC3/mole_rancher).

### Rust GameDev Meetup [#](https://gamedev.rs#rust-gamedev-meetup)

![Gamedev meetup poster](../../assets/810f584ff640804b.png)


The 19th Rust Gamedev Meetup took place in August. You can watch the recording of
the meetup [here on Youtube](https://youtu.be/s9kf9HVUKYE). Here was the schedule from
the meetup:

- RustConf Arcade Cabinet -
[@carlosupina](https://twitter.com/carlosupina) - Blue Engine -
[@aryanpur_elham](https://twitter.com/aryanpur_elham) - Veloren -
[@VelorenProject](https://twitter.com/VelorenProject) - Graphite -
[@GraphiteEditor](https://twitter.com/GraphiteEditor) - All is Cubes -
[@switchborg](https://twitter.com/switchborg)

The meetups take place on the second Saturday every month via the [Rust Gamedev
Discord server](https://discord.gg/yNtPTb2) and are also [streamed on
Twitch](https://twitch.tv/rustgamedev).

![screenshot of the game: many players, block and an explosion](../../assets/ae5bd8283d4ce4ad.jpg)


[Pablo Mansanet shared a report](https://blog.tonari.no/rust-game-hack-2022) about how
the 2022 Tokyo Rust Game Hack went.

## Game Updates [#](https://gamedev.rs#game-updates)

[Catacomb 2-64k](https://github.com/64kramsystem/catacomb_ii-64k) is a (completed) experimental
project in porting a moderately complex project, first from C to unsafe Rust,
then to (fully) safe Rust.

The objective of the project has been to study the tooling, transformations
and the overall process required perfom real-world, exact, ports; an article
will follow in September on [64kramsystem’s blog](https://saveriomiroddi.github.io).

The port uses the [Rust-SDL2 bindings](https://github.com/Rust-SDL2/rust-sdl2). More exact ports
of id Software games are expected in the future, with the introduction of a
refactoring tool based on the
[Language Server Protocol](https://microsoft.github.io/language-server-protocol)/[Rust Analyzer](https://github.com/rust-lang/rust-analyzer).

![browser udp technology](../../assets/7adf8d9fae2dffd3.jpg)

CyberGate ([YouTube](https://youtube.com/channel/UClrsOso3Xk2vBWqcsHC3Z4Q), [Discord](https://discord.gg/R7DkHqw7zJ)) by CyberSoul
is a new multiplayer project that aims at procedurally generating distinct
universes and gameplay experiences. CyberGate is the name of the main world
where universes can be created and accessed by quantum portals.

Recent updates:

- Ported to browser (wgpu with webgl backend)
- Unreliable network protocol achieved with WebRTC
- Dynamically spawn and synchronize ECS components using macros
- Massively improved the events system and actions system
- Refactored over 50% of the project
- Small features such as grabbing objects and dash forward
- Fixed 3 major bugs that slowed down the server

[Join the Discord server](https://discord.gg/R7DkHqw7zJ) to participate in upcoming Phase 5.0!

*Discussions: /r/rust_gamedev*

![Rusty Aquarium visualization](../../assets/f95b1cf4694785e0.gif)

[Rusty Aquarium](https://github.com/ollej/rusty-aquarium) by [@ollej](https://twitter.com/ollej) is a data visualization tool as a virtual fish
tank written in Rust and Macroquad. Different data points control how many
fishes are shown, how they move, how fast they swim, and which size they are.
It can be used to monitor data in a visual way, while those uninitiated only
see a serene fish tank.

Since Macroquad is cross-platform, Rusty Aquarium is available for Windows, Mac, Linux as well as for browsers using WebAssembly.

The aquarium can be controlled in various different ways:

- System monitoring binary to show CPU usage, disk usage, and processes.
- Integrate with Google Sheets to control fishes.
- Back it with an URL that generates a JSON file.

This month, a blog post with the [story behind Rusty Aquarium](https://blog.agical.se/en/posts/the-story-behind-rusty-aquarium/)
was published on the [Agical](https://blog.agical.se/en/) blog. The code was restructured and the packaged
files now contain binaries for input data generation.

![Infinite Bunner](../../assets/8085b7b7033b4ae1.gif)

[Infinite Bunner](https://github.com/ollej/rust-bunner-macroquad) is a game from the book [Code the Classics vol 1](https://wireframe.raspberrypi.org/books/code-the-classics1) that has
been ported by [@ollej](https://twitter.com/ollej) to Rust and Macroquad from Python and PyGame Zero.
It is a modern version of the classic arcade game Frogger with improved
graphics and sound.

The game has been sent in to the [Rust Game Ports](https://github.com/rust-gamedev/rust-game-ports) project as
an educational example. It shows how to make a 2D game in Macroquad with
graphics and sound.

[Code the Classics vol 1](https://wireframe.raspberrypi.org/books/code-the-classics1) is a book from Wireframe Magazine that tells the
history of five classic video games. It also includes code listings of modern
versions of the games written in Python with the PyGame Zero framework.

### Tiny Building Game [#](https://gamedev.rs#tiny-building-game)

![Country_slice_gif](../../assets/00b5126ba90ef421.gif)


The untitled “Tiny Building Game” is a stress-free feel-good game focused on just
building something pretty. It is being made by [@anastasiaopara](https://twitter.com/anastasiaopara) and
[@h3r2tic](https://twitter.com/h3r2tic), who has recently joined the project!

This month, there was a large visual update, which added [trees and flowers](https://twitter.com/anastasiaopara/status/1560673892574035969),
as well as [fences and gates](https://twitter.com/anastasiaopara/status/1565629377823395841).

Right now, the team is actively working on setting up a Steam page. Stay
tuned by following the [newsletter](https://dashboard.mailerlite.com/forms/10395/51067704544593017/share)!

![Promotional image of the Math It game](../../assets/b0690a83a205e2dc.png)

[Math It](https://vrixyz.itch.io/math-it) was made with [Bevy](https://bevyengine.org/) for the [Bevy Jam 2](https://itch.io/jam/bevy-jam-2).

The goal of the game is to get as close as possible to the target number and compete with others on a global leaderboard.

![A cave with lava](../../assets/f6d21ed6d50eca1b.jpg)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In August, long-awaited work on a new internationalization system with Fluent was merged. The real-time simulation v2 system is now in a place, which has allowed for blacksmiths to now sell swords and armour with only a few additional lines of code. Work was done to implement a spectator mode in game, as well as fix a bug about respawning while having a status effect on you persisting, such as being on fire from swimming in lava.

August’s full weekly devlogs: “This Week In Veloren…”:
[#183](https://veloren.net/devblog-183),
[#184](https://veloren.net/devblog-184),
[#185](https://veloren.net/devblog-185),
[#186](https://veloren.net/devblog-186),
[#187](https://veloren.net/devblog-187).

## Engine Updates [#](https://gamedev.rs#engine-updates)

[miniquad](https://github.com/not-fl3/miniquad/) is a pure Rust, cross-platform graphics library.

This month was about polishing miniquad-android experience.
To make it easier for regression testing, miniquad got
[the android playground](https://github.com/not-fl3/quad-android-playground).

The playground demonstrates all known android shenanigans in one quad-based app.

It includes:

- onscreen keyboard
- java interop (with file dialog as an example)
- dealing with big java services (with bluetooth as an example)
- accessing permissions, both runtime and compile time

[Runty8](https://github.com/jjant/runty8) is an experimental port of the [Pico8](https://www.lexaloffle.com/pico-8.php)
fantasy console that supports writing games in Rust.

Its current goals are to follow Pico8’s APIs as closely as possible, to allow easily porting existing games to Rust, as well as developing new games in a familiar development environment.

The project is in very early stages, and is currently looking for contributors.
If you’re interested, feel free to read their [contributing guide](https://github.com/jjant/runty8/blob/master/CONTRIBUTING.md)
or browse through the [open issues](https://github.com/jjant/runty8/issues).

![Gamercade preview](../../assets/65a9a203ed2b26b3.gif)

[Gamercade](https://gamercade.io) ([Discord](https://discord.gg/Qafv2Fpt5j), [GitHub](https://github.com/gamercade-io/gamercade_console))
by @RobDavenport is a WASM-powered fantasy console focused
on building multiplayer neo-retro games.

Gamercade is preparing for their first alpha release! This includes all the core features needed for a fantasy console and game library: input, graphics, and audio. It also has networked multiplayer, and an editor.

They implemented the in-game sound engine from scratch. They also improved the
editor to allow creation of instruments and tracks. It synthesizes sounds at
runtime, and produces something like an 80s synth, a 90s SoundBlaster, and a
touch of SNES. Songs and Sfx are built using a tracker interface.
[This video](https://youtube.com/watch?v=cRsOvefap_U) shows a small sample of what it is capable of.

“Wavetables” are great for classic sounds like 8-bit chiptunes or even more complicated sounds. “FM Synth” is a 4-op FM synthesizer. Masters of this technique can produce a huge variety of instruments, effects, and other otherwordly things. “Sampler” rounds out the rest of the system, providing pre-recorded sample playback. Samples can be pitched and played as the desired note.

Come hang out and chat on [Discord](https://discord.gg/Qafv2Fpt5j), where the developers
interact with members and post updates daily. The project is
[open source](https://github.com/gamercade-io/gamercade_console) and looking for contributors, suggestions,
as well as awesome game demos.

## Tooling Updates [#](https://gamedev.rs#tooling-updates)

![Graphite logo](../../assets/c794ec8d6423f1ae.png)


Graphite ([website](https://graphite.rs), [GitHub](https://github.com/GraphiteEditor/Graphite),
[Discord](https://discord.graphite.rs), [Twitter](https://twitter.com/GraphiteEditor)) is a free,
in-development raster and vector 2D graphics editor that will be based around a
Rust-powered node graph compositing engine.

August’s [sprint](https://github.com/GraphiteEditor/Graphite/milestone/18) focused on Bézier shape editing and layer
transformation improvements.

- Ahead of the curve: Bézier shapes gain support for curve extension and shape closing using the Pen tool and inserting points along curves with the Path tool.
- Front and center: Layer origins may be set to control the center of rotation and scale using the Transform tool.

Meanwhile, design and architecture work on the Graphene node-based programming language has been well underway. Graphene is the data graph engine that will replace Graphite’s tree-based layer system in the next few sprints and evolve into a raster-and-vector render engine over time.

Open the [Graphite editor](https://editor.graphite.rs) in your browser to give it a try
and share your creations with #MadeWithGraphite on Twitter.

## Library Updates [#](https://gamedev.rs#library-updates)

![hot-lib-reloader thumbnail](../../assets/be4891b6607d7a6d.png)


[hot-lib-reloader](https://github.com/rksm/hot-lib-reloader-rs) is a development tool that allows you to reload functions
of a running Rust program. This allows to do “live programming” where you
modify code and immediately see the effects in your running program. Gone
are the days of edit-compile-restart loops (to some degree).

hot-lib-reloader works by reloading parts of your application that are defined
as dynamic libraries. This approach works on Linux, MacOS, and Windows but has
some constraints - see the [documentation](https://docs.rs/hot-lib-reloader/latest/hot_lib_reloader/) for details. There are several
[examples](https://github.com/rksm/hot-lib-reloader-rs/tree/master/examples), showing how to create hot-reload setups with various frameworks
and libraries, e.g. bevy, egui, and [nannou](https://youtu.be/hyyeLtJ7SQk).

![Configuring a sound when playing it](../../assets/086ed863923fa48c.png)

[bevy_kira_audio](https://github.com/NiklasEi/bevy_kira_audio/) by [@nikl_me](https://twitter.com/nikl_me) is an alternative audio plugin for the [Bevy](https://bevyengine.org/)
game engine. It uses [Kira](https://github.com/tesselode/kira) as its audio library and aims to integrate
well with Bevy’s ECS.

Last month saw the release of versions [0.11.0](https://github.com/NiklasEi/bevy_kira_audio/blob/main/CHANGELOG.md#v0110) and [0.12.0](https://github.com/NiklasEi/bevy_kira_audio/blob/main/CHANGELOG.md#v0120). With the
latest version, sound settings like volume, playback-rate, or panning can
be adjusted directly when playing audio. The screenshot above shows the new API
with multiple example settings. The plugin now also offers control
over single sound instances via asset handles and will apply configurable
tweens to most operations.

![Configuration of a loading state](../../assets/00233a955031a1fb.png)

[bevy_asset_loader](https://github.com/NiklasEi/bevy_asset_loader/) by [@nikl_me](https://twitter.com/nikl_me) is a plugin for [Bevy](https://bevyengine.org/) apps aiming to
improve a common pattern for asset-loading. The boilerplate required to set up
a loading-state is reduced to a minimum. The plugin is based on storing
asset handles in resources, which makes it easy to use them in any system
across your app.

The screenshot above shows how a loading state can be added to the Bevy app in the latest version of the plugin. The update also fixed issues with configuring the same loading state in different places of your code and enabled users to define their own dynamic assets.

![notan examples](../../assets/41cac4b69fdfd183.gif)


[Notan](https://github.com/Nazariglez/notan) is a simple and portable layer designed to create your own
apps on top of it without worrying about platform-specific code.

It provides a set of APIs and tools that can be used to create your project in an ergonomic manner without enforcing any structure or pattern, sharing the same codebase across multiple platforms.

The main focus for version [v0.6](https://github.com/Nazariglez/notan/releases/tag/v0.6.0) was improving how uniforms
are set using the layout std140 for the user with a macro,
among internal fixes and improvements.

[Shipyard](https://github.com/leudz/shipyard) is an Entity Component System focused on usability and speed.

This monthh, 0.6 was released with big improvements to workloads and tracking.

The new [visualizer](https://leudz.github.io/shipyard/visualizer) is a first step towards visual
inspection and interaction with the library.
For now it can only show which components are used by which systems
and vice-versa.

Learn more about this release in the [release post](https://users.rust-lang.org/t/shipyard-0-6-release/79504).

*Discussions:
/r/rust
/r/rust_gamedev*

[Edict](https://github.com/zakarumych/edict) by [@zakarumych](https://github.com/zakarumych) is powerful Rust ECS crate that expands traditional ECS
feature set. The new version 0.2 is getting [ready for release](https://docs.rs/edict/0.2.0-rc.3/edict/). This ECS is based
on archetypes for fast cache-friendly iteration. And there are quite a few novel
features:

[Edict](https://github.com/zakarumych/edict)allows to express relations between entities usingtrait. Relations are linked to a pair of entities - origin and target. This opens a wide range of opportunities to create entity graphs with custom logic.`Relation`

- Custom hooks for components and relations to trigger actions when component is dropped/replaced, or when relation target is dropped.
- Optional
trait.`Component`

[Edict](https://github.com/zakarumych/edict)allows using component types that do not implementwith some restrictions.`Component`

- Change tracking with flexible queries for modified components suitable for complex use cases. E.g. incremental saves can fetch all components modified since previous save.
- Type-agnostic component borrowing. Component type may define list of types
that can be borrowed from it. Important use case is borrowing
.`dyn Traits`

[Edict](https://github.com/zakarumych/edict)supports parallel execution. Built-in scheduler uses systems that implementtrait. Functions can be safely transformed into systems similarly to`System`

.`bevy_ecs`


[grid_pathfinding](https://github.com/tbvanderwoude/grid_pathfinding) is a new pathfinding crate aimed at providing a fast,
out-of-the-box system for pathfinding on various types of grids. While the
current 0.1.1 release is not very configurable yet, the idea is to make the
crate more malleable working towards a 0.2.0 release so that it will support
a range of grids (4-connected, 8-connected, weighted, etc.) as well as
heuristics. Specifically, [grid_pathfinding](https://github.com/tbvanderwoude/grid_pathfinding) 0.1 assumes a uniform-cost
8-grid with a Chebyshev cost metric and heuristic. More long-term goals are
support for multi-tile and multi-agent pathfinding variants.

The current implementation is based on [Jump Point Search](https://en.wikipedia.org/wiki/Jump_point_search) with
[improved pruning rules](https://www.researchgate.net/publication/287338108_Improving_jump_point_search). On top of this, [connected components](https://en.wikipedia.org/wiki/Component_(graph_theory)) are used to
avoid flood-filling behaviour if no path exists - see the
[documentation](https://docs.rs/grid_pathfinding/0.1.1/grid_pathfinding/) and [examples](https://github.com/tbvanderwoude/grid_pathfinding/tree/main/examples) for information on
how to manage these components. Especially when simulating many agents in
real-time, using components can make a big difference.

## Other News [#](https://gamedev.rs#other-news)

- Other game updates:
[Caveth](https://github.com/Dequog/caveth)is a game made with macroquad where you can shoot enemies with a cannon.[Im-Oab released a free Steam demo of the shump Flesh](https://store.steampowered.com/app/1660850/Flesh/?beta=0)and also added[new enemy types](https://twitter.com/Im_Oab/status/1557714901434781696),[boss animations](https://twitter.com/Im_Oab/status/1564581193454354432), and[bullet shadows](https://twitter.com/Im_Oab/status/1562015685521604610).[Spherical Go](https://github.com/Dominux/spherical-go)if the Go game’s implementation with a variety of spherical fields.[Combine and Conquer has a new devlog about 0.10 version](https://buckmartin.de/combine-and-conquer/2022-08-20-v0.0.10.html)that brings vector graphics, “merger” and “splitter” structures, new tech-tree UI, overlay improvements, and new tiers for existing structures.[bevy-cheeseball](https://github.com/Rust-Ninja-Sabi/rust-bevy-cheeseball)is a 3D marble game inspired by Monkey Ball and made with Bevy and Rapier.[Punchy v0.04](https://reddit.com/r/rust_gamedev/comments/x1ekmg/fish_folk_punchy_v004)was released, featuring MVP for the first boss enemy, an entirely refactored fighter state model[which was written up on the wiki](https://github.com/fishfolks/punchy/wiki/Fighter-State-Machine), updates to the enemy AI targeting, camera progression boundaries, updates to debug tools, a health recovery item, and updates to the way attacks are defined and loaded from resources.

- Other learning material updates:
[Console #118 - Interview with Connor of rend3](https://console.substack.com/p/console-118)- PhaestusFox added a bunch of new videos
to their
[“Bevy Basics”](https://youtube.com/playlist?list=PL6uRoaCCw7GN_lJxpKS3j-KXuThRiSXc6)YouTube series. [@fronkongames shared a quick guide](https://rjgameiro.medium.com/let-fun-rust-unity-f7f62609ba49)to integrating Rust code into Unity.[@samkevich published a “Learn OpenGL with Rust” series](https://github.com/samkevich/learn_gl_with_rust).[@jack1232 released a “Rust wgpu Graphics Programming Tutorial” YouTube series](https://youtube.com/playlist?list=PL_UrKDEhALdJS0VrLPn7dqC5A4W1vCAUT).

- Other engine updates:
[Fyrox v0.27](https://fyrox.rs/blog/post/feature-highlights-0-27)features a new Fish Folly game example, compile-time reflection, plugin, and scripting improvements, and two new book chapters about[particle systems](https://fyrox-book.github.io/fyrox/scene/particle_system_node.html)and[terrain](https://fyrox-book.github.io/fyrox/scene/terrain_node.html).[Pyxel v0.18](https://twitter.com/kitao/status/1564234852185960449)’s main highlight is the experimental web support.[Bevy released a blog post](https://bevyengine.org/news/bevys-second-birthday/)about the second birthday of the engine with a retrospective and future plans.

- Other tooling updates:
[@HackerFoo shared a video](https://youtube.com/watch?v=qJOPLxFfbMw)of a WIP meta-editor to record contact movement to create interactive tutorials for Noumenal.[nbody-wasm-sim](https://github.com/simbleau/nbody-wasm-sim)is a WebGPU N-Body astrophysics simulation in Rust + WASM.[wgen](https://github.com/jice-nospam/wgen)is a simple multi-threaded heightmap generator made with egui and three_d.[bevy-shell-template](https://github.com/kurbos/bevy-shell-template)is an opinionated, monolithic template for Bevy with cross-platform CI/CD, native + WASM launchers, and managed cross-platform deployment.

- Other library updates:
[bevy_streamdeck](https://github.com/vleue/bevy_streamdeck)is a Bevy plugin to interact with Stream Deck.[kira v0.7 release](https://github.com/tesselode/kira/releases/tag/v0.7.0)brings a bunch of important bug fixes some of which require breaking changes.[egui v0.19](https://twitter.com/ernerfeldt/status/1561010036255739904)brings a lot of various small API improvements and optimizations.[Alex Dixon shared a blog post](https://www.polymonster.co.uk/blog/maths-rs)about creating another linear algebra library -[maths-rs](https://github.com/polymonster/maths-rs).[fundsp](https://github.com/SamiPerttu/fundsp)is an audio digital signal processing library for audio processing and synthesis.[bevy_ecs_tilemap](https://github.com/StarArawn/bevy_ecs_tilemap)is an ECS-friendly tilemap rendering crate for Bevy.


That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!

**Discuss this post on**:
[/r/rust_gamedev](https://reddit.com/r/rust_gamedev/comments/xnjeym/this_month_in_rust_gamedev_37),
[Twitter](https://twitter.com/rust_gamedev/status/1573978074550616064),
[Discord](https://discord.gg/yNtPTb2).