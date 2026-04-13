---
title: 'This Month in Rust GameDev #4 - November 2019'
url: https://gamedev.rs/news/004/
author: Rust GameDev WG
published: '2019-12-08'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the fourth issue of the Rust GameDev Workgroup’s monthly newsletter.

[Rust](https://rust-lang.org) is a systems language pursuing the trifecta:
safety, concurrency, and speed.
These goals are well-aligned with game development.

We hope to build an inviting ecosystem for anyone wishing
to use Rust in their development process!
Want to get involved? [Join the Rust GameDev working group!](https://github.com/rust-gamedev/wg#join-the-fun)

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).
Feel free to send PRs about your own projects!

## Game Updates [#](https://gamedev.rs#game-updates)

[Le Train Dispatcher](http://athorus.itch.io/ltd) - Route Trains in Simulated Rail Network [#](https://gamedev.rs#le-train-dispatcher-route-trains-in-simulated-rail-network)

![Demo of Le Train Dispatcher](../../assets/b7c2e5c071afb032.gif)


Le Train Dispatcher ([itch.io](http://athorus.itch.io/ltd), [Patreon](https://patreon.com/athorus))
allows you to route trains in a fully simulated rail network.
Particular care has been taken on the realistic management of light signals
(block systems, switch protection), train physics and curve tracing.

The game is programmed in Rust and the main crates used are: ggez, imgui and serde.

This first version is fully playable, but if you want to comment,
bring your ideas or contribute to the development of the game,
in any way, do not hesitate to post a [message](https://athorus.itch.io/ltd/community).

Unique characteristics:

- Realistic light signals simulation: Huge engineering work has been done to have realistic management of railway signaling.
- No collision: Yes it’s fun to watch many trains running automatically without getting in. All your actions are checked: you cannot put the trains in danger.
- True physics
- Each locomotive or wagon has its own weight, its driving or braking force, its coefficient of adhesion.
- The curves are not simple circles, they are calculated with the same equations as those used in real road or rail networks.


![Character creation screen](../../assets/650c2064b801782b.png)


[Veloren](https://veloren.net) is an open-world, open-source multiplayer voxel RPG.
The game is in an early stage of development, but is playable.

Some of November’s updates:

- The main repository reached 50,000 lines of code (according to
[Tokei](https://github.com/XAMPPRocky/tokei)); [Airshipper launcher](https://gitlab.com/veloren/airshipper)was significantly improved;- game design working group was started;
- improved auth, player creation screen, asset compression, lore, and soundtrack;
- CI upgrades, lots of bugfixes and content upgrades.

The full weekly devlogs “This Week In Veloren…”:
[#40](https://veloren.net/devblog-40),
[#41](https://veloren.net/devblog-41),
[#42](https://veloren.net/devblog-42),
[#43](https://veloren.net/devblog-43).

Check out a new video [“What is Veloren?”](https://youtube.com/watch?v=IIl271iDulY)
by @DoNeo and @RonVal4 (it’s in Russian but has English subtitles):

Also, they’ve written [an article in Russian about Veloren for dtf.ru](https://dtf.ru/indie/83725-veloren-igra-mechty).

![Math Defense screenshot](../../assets/cb62a6faf1a0acac.png)


[Math Defense](https://jackmott.itch.io/math-defense) by [@512Avx](https://twitter.com/512Avx) is a math game for kids.

Progress through addition, subtraction, multiplication, and division by solving the math problems to shoot down enemy space ships. Multiple difficulty levels and fully customizable by editing the levels.json file. Create your own levels, change the difficulty, whatever you like.


![Sulis logo](../../assets/9dd77afb3a849703.png)


[Sulis](https://sulisgame.com/dev-modding/9-dev/15-managing-resources) is a Role-Playing Game (RPG) with turn-based, tactical combat,
deep character customization, and an engaging storyline.

This month, an article [“Basic Resource Management”](https://sulisgame.com/dev-modding/9-dev/15-managing-resources)
was published:

In developing Sulis, one of the primary goals is easy and powerful modding capabilities. To that end, virtually all resources are defined via simple YAML files. The idea is that anyone with a text editor can create new resources or edit existing ones easily. However, this immediately brings up the question of how to manage all these resources within the game’s state. In Sulis, this is handled via a central resource manager.


While Sulis is used as the primary example, the article should apply to pretty much any game.

Also, the project (the game itself and its source code)
[was reviewed by gamefromscratch.com](https://youtube.com/watch?v=gvibvDiVzn8)
[[/r/rust_gamedev](https://reddit.com/r/rust_gamedev/comments/du48iw/sulis_an_rpg_created_using_rust_gamesfromscratch)].

[Paddlers](https://github.com/jakmeier/paddlers-browser-game) is a multi-player real-time strategy browser game
about making all Paddland’s ducks happy.

Check out a live demo at [demo.paddlers.ch](http://demo.paddlers.ch)
(a test user’s username is “Tester”, password is “1”).

This month the third devlog was published:
[“#3: Fun with Rust and distributed systems”](https://www.jakobmeier.ch/blogging/Paddlers_3.html).
It overviews the architecture and implementation of the project.

![screenshot: battlefield after slaying some chonkrats](../../assets/8b29a59c7224f5ae.jpeg)


[Antorum](https://dooskington.com) is a multiplayer RPG where players build their characters
and fight against the growing threats on the isle.
The game server is authoritative and written in Rust,
while the client is written in Unity/C#.

This month, @dooskington published
the [11th devlog “Drop Tables”](https://dooskington.com/dev-log/11)
about the implementation of a drop table system to handle monster loot.



![Demo of the basic ship collision](../../assets/36599e12cd94c13e.gif)

[Tom Leys](https://twitter.com/RecallSingular1) is working on a “The Recall Singularity” game
about designing autonomous factory ships and stations
and this month they published a devlog post:
[“Recalling Nov 2019”](https://medium.com/@recallsingularity/recalling-nov-2019-236cdf9c0a8a).

You can also [watch a video version here](https://youtube.com/watch?v=AoPSAoqmTCk).

Summary:

- basic networked inputs to move ships or players;
- physics for ships, including collisions;
[Twich streaming the development](https://twitch.tv/recallsingularity);- a more generic approach to syncronising from Rust (Specs) to Godot.

![Just a screenshot of some battle](../../assets/d19dfec64c95d83d.jpg)


[Slavic Castles](https://leinnan.itch.io/slavic-castles) is a card game inspired by [Arcomage](https://en.wikipedia.org/wiki/Arcomage)
written in Rust using [ggez](https://github.com/ggez/ggez)/[good-web-game](https://github.com/not-fl3/good-web-game).

You can play online [here](http://leinnan.ayz.pl/ukw/slavic_castles/index.html)
or on [itch.io](https://leinnan.itch.io/slavic-castles).

*Discussions:
/r/rust_gamedev*

![robots demo](../../assets/ab9cdfa611ca9c27.gif)


[@oliviff](https://twitter.com/oliviff) released [v0.0.5](https://twitter.com/oliviff/status/1192178573488070659)..[v0.1.0](https://twitter.com/oliviff/status/1199073510443945985)
versions of [Tennis Academy](https://iolivia.me/posts/6-months-of-rust-game-dev):

- ⏰ players have patience levels and leave when they get bored;
- ✨ score multipliers with text effects;
- 🥇 winning and losing states;
- 🤖 no more people, the robots have taken over!
- 🎨 new colour palette and graphics, new buttons and UI (using
[Iced](https://github.com/hecrj/iced)).

The game is now officially named “Twenty Asteroids”.

[@VladZhukov0](https://twitter.com/VladZhukov0) published
[a short video of the updated/tweaked gameplay](https://twitter.com/VladZhukov0/status/1197855075269521409).

![Flying cars](../../assets/3639bca751fc0aa7.png)


[Erasterra](https://coffejunkstudio.itch.io/erasterra) is a geography racing game.
It uses Rust to implement the matchmaking server.

It made sense to implement the matchmaker in Rust because it’s designed to be a long-running service and as such it may not crash. Rust simply makes it easier to implement non-crashing software 🙌


![Garden screenshot: ruins, trees and water in craters](../../assets/0982fbd8b490fb1c.jpeg)


[@logicsoup](https://twitter.com/logicsoup) tweeted a bunch of updates, including:

![A screenshot of a later game level](../../assets/4b92a59a2816206b.jpeg)


[Alex Butler](https://twitter.com/bigabgames) continues to polish their “[Robo Instructus](https://store.steampowered.com/app/1032170/Robo_Instructus/)” game;
[1.15, 1.16, and 1.17 versions were released](https://steamcommunity.com/app/1032170/allnews):
Rust 1.39, bugfixes, and better translations.

### GitHub Game Off 2019 [#](https://gamedev.rs#github-game-off-2019)

![gameoff logo](../../assets/9f005b1cb50c8f01.gif)


[GitHub’s Game Off](https://itch.io/jam/game-off-2019)
is an annual month-long game jam (hackathon for building games).
This year’s theme is [“leaps and bounds”](https://github.blog/2019-11-01-game-off-2019-theme-announcement).

-
[“TopDown”](https://fedorgames.itch.io/ggoff2019)by[@fedor_games](https://twitter.com/fedor_games)made with[their own unannounced game engine](https://twitter.com/fedor_games/status/1192989017840730112)([source code](https://github.com/not-fl3/gameoff-2019)).![TopDown: gameplay sample](../../assets/a3c8e134f8943913.gif)

-
[“Compact Space”](https://puppetmaster.itch.io/compact-space)by[@fischspiele](https://twitter.com/fischspiele)made with specs and Tetra ([source code](https://github.com/puppetmaster-/compact-space)).How long can you stay alive?

![Compact-Space screenshot: asteroids, ship, aliens](../../assets/973ee9d58fd49b1f.png)

-
“evo” by

[@ZappedCow](https://twitter.com/)made with Tetra ([source code](https://github.com/jlauener/evo)).A life/environment simulator with a bit of rogue-like tossed in.

![evo: demo](../../assets/ab7032d946c76d2f.gif)


### Amethyst Games [#](https://gamedev.rs#amethyst-games)

-
[Azriel](https://azriel.im)published a[“That Looks Good On UI”](https://azriel.im/will/2019/11/08/that-looks-good-on-ui)devlog.What’s new:

- Animated menus and backgrounds can be defined.
- Player names can be specified in controller configuration.
- Winner is displayed when a game ends.

Behind the scenes, the following code maintenance has been made:

- Moved all tests into a separate crate – 1.9x speedup, 65% less disk usage.
- Assets are loaded into separate asset components – easier to share logic between different types of objects.
- Asset loading is done in stages, in preparation for the ability to disable certain stages.

![Will: Winner Status Demo](../../assets/90c6f8ebc4594b90.png)

-
[@takeryo_eeic](https://twitter.com/takeryo_eeic)named their hexagonal game “Conquest”,[added a main menu](https://twitter.com/takeryo_eeic/status/1195263050896429057), and[showed a video of new map generator and map scrolling](https://twitter.com/takeryo_eeic/status/1192407134245228546).![Main menu demo](../../assets/852e2e1141814032.png)


## Library & Tooling updates [#](https://gamedev.rs#library-tooling-updates)

![how entities/handles are related to each others](../../assets/6d22b84470f797ac.jpg)


[@kooparse](https://twitter.com/kooparse) published [a post about implementing a quick memory arena](https://kooparse.com/blog/memory-arena).

For my game, I decided to store almost every entity in a big chunk of memory allocated only once when the program boot. I am using this technique for three reasons. First, I want full and precise control over how memory is managed in the game, second I want better data locality in order to increase cache hits from the cpu, and finally, at runtime asking the operating system in order to allocate more memory is slow.


![some webgpu logo](../../assets/fa784116b5ba4830.png)


[wgpu](https://github.com/gfx-rs/wgpu) is a library in Rust that is meant to be the go-to solution
for most graphics and compute needs.

wgpu-rs version 0.4 was released on crates.
wgpu is based on [gfx-hal-0.4](https://reddit.com/r/rust/comments/dm89t2/gfxhal_version_04_release) and includes
changes from the [previous blog post](https://gfx-rs.github.io/2019/10/01/update.html);

A few notable additions are:

- proper Windows 7 support;
- support for multiple clients on the same GPU server;
- slimmed-down Rendy dependencies (memory and descriptor);
- new skybox example.

Lyon has [updated examples](https://github.com/nical/lyon/pull/496)
for this version, showing how to draw vector graphics on `wgpu`

.

Also, `wgpu`

is now a part of Gecko code base for powering the emerging WebGPU implementation.

### Book: [Learn Luminance](https://rust-tutorials.github.io/learn-luminance) [#](https://gamedev.rs#book-learn-luminance)

[luminance](https://github.com/phaazon/luminance-rs) is a type-safe, type-level and stateless Rust graphics framework.

This month, [@phaazon](https://github.com/phaazon) released a [“Learn Luminance”](https://rust-tutorials.github.io/learn-luminance) book.
Luminance’s wiki was deprecated and the book is now the central reference
to onboard newcomers to use luminance as well as people
who would like to give luminance a try and who knows nothing about rendering.

*Discussions:
/r/rust*

Btw, [@resinten is working on a game using luminance](https://twitter.com/resinten/status/1194825522418765826):

![Pixels logo](../../assets/bf303f9ac68c4707.png)


[Pixels](https://github.com/parasyte/pixels) by [@kodewerx](https://twitter.com/kodewerx) is a tiny hardware-accelerated
pixel frame buffer based on wgpu.
It’s supposed to be used for emulators, software rendering,
2D animations and games prototyping.

Check out [the URLO announcement post](https://users.rust-lang.org/t/announcing-pixels-hardware-accelerated-pixel-frame-buffer/34326/1).

*Discussions:
/r/rust_gamedev*

[metropolis](https://github.com/GuyL99/metropolis) by [@GuyL99](https://github.com/GuyL99)
is a high-level graphics renderer, with easy functions to use.

This crate should make graphics programming easy with functions like rect, ellipse, line, text, and such, and it’s fast with 60-120 FPS on a bad computer.


*Discussions:
/r/rust_gamedev*

^ Click to see [a demo video](https://www.youtube.com/watch?v=El99FgGSzfg).

[skulpin](https://github.com/aclysma/skulpin) by [@aclysma](https://twitter.com/aclysma) provides an easy option for drawing
hardware-accelerated 2D by combining Vulkan and [Skia](https://skia.org).

[ultraviolet](https://github.com/termhn/ultraviolet) v0.2 [#](https://gamedev.rs#ultraviolet-v0-2)

[ultraviolet](https://github.com/termhn/ultraviolet) v0.2 were released by [@fu5ha](https://twitter.com/fu5ha).
This release introduces [Bivectors](https://en.wikipedia.org/wiki/Bivector) and [Rotors](https://en.wikipedia.org/wiki/Rotor_(mathematics)) and improved usability.

*Discussions:
/r/rust*

![rayn fractal render example](../../assets/df5d73a470b40734.png)


Also, [Rayn v0.3 was released recently](https://reddit.com/r/rust/comments/dxjn64/rayn_03_a_major_update_with_deeply_integrated/) - it’s a CPU-based
path tracing renderer focused on rendering SDFs (specifically fractals)
that is based on [ultraviolet](https://github.com/termhn/ultraviolet).

![Mun logo](../../assets/235482403e6e518c.png)


[Mun](https://mun-lang.org) is a scripting language for gamedev focused
on quick iteration times that is written in Rust.

As a language, Mun is still far from production-ready, but this release gives you a glimpse of what natively supported hot reloading will look like in the future. The purpose of this release is to showcase our progress and gather feedback from those brave souls willing to try out Mun at this early stage.


To get started, read [the Mun Book](https://docs.mun-lang.org)
and have a look at [Rust examples](https://github.com/mun-lang/mun/tree/master/crates/mun_runtime/examples).

For the full roadmap of Mun, have a look at their [Trello board](https://trello.com/b/ZcMiREnC/mun-roadmap).

*Discussions:
/r/rust*

[glsl](https://crates.io/crates/glsl) is a crate to parse GLSL formatted sources into a typed AST.
The crate exposes several methods, types and modules
to perform transformations on that AST, among outputting GLSL,
SPIR-V generation and visiting the AST with possible in-place mutations.

[glsl v3.0](https://reddit.com/r/rust/comments/dw87um/glsl30_official_release_announcement) was released by [@phaazon](https://github.com/phaazon):

- the CPP directives (e.g.
`#line`

,`#pragma`

,`#ifdef`

, etc.) are now all implemented; - improved parsing of deeply nested expressions;
- multiline annotations () is now supported as a best-effort;
- other bugfixes.

![example output](../../assets/171ab13a3076ebc1.png)


[SPIR-Q](https://github.com/PENGUINLIONG/spirq-rs) is a lightweight [SPIR-V](https://en.wikipedia.org/wiki/Standard_Portable_Intermediate_Representation) query library.

SPIR-Q <…> can be very useful for dynamic graphics/compute pipeline construction, shader debugging and so on. SPIR-Q is currently compatible with a subset of SPIR-V 1.5, with most of graphics capabilities but no OpenCL kernel capabilities covered. Btw, SPIR-Q currently only depends on the Rust standard library.


*Discussions:
/r/rust*

![Iced demo](../../assets/223950d71687eb84.gif)


[Iced](https://github.com/hecrj/iced) is a renderer-agnostic GUI library focused on simplicity
and type-safety.

This month, a [beta version of Iced was released](https://reddit.com/r/rust/comments/e1jckj/iced_a_crossplatform_gui_library_new_release).
The most important new features are:

- A
[basic renderer](https://github.com/hecrj/iced/pull/22)built on top of[wgpu](https://github.com/gfx-rs/wgpu); - A windowing shell powered by
[winit](https://github.com/rust-windowing/winit); - A
[web runtime](https://github.com/hecrj/iced/pull/17)based on[dodrio](https://github.com/fitzgen/dodrio)(try the tour on[iced.rs](https://iced.rs)); - First-class
[async actions](https://github.com/hecrj/iced/pull/62), leveraging futures; - New widgets, like
[text inputs](https://github.com/hecrj/iced/pull/37)and[scrollables](https://github.com/hecrj/iced/pull/35).

Also, [Cryptowatch is now sponsoring the development of Iced!](https://blog.cryptowat.ch/2019/11/25/sponsoring-rust-gui-library-iced)

### Embark’s Stockholm Rust Meetup and Newsletter [#](https://gamedev.rs#embark-s-stockholm-rust-meetup-and-newsletter)

![Embark logo white on black](../../assets/95d09b741f953707.png)


Videos from [Embark](https://embark.rs)’s Stockholm Rust Meetup arrived:

-
[“An Unholy Fusion of Rust and C++ in physx-rs”](https://youtube.com/watch?v=RxtXGeDHu0w)-[Tomasz Stachowiak](https://twitter.com/h3r2tic), senior software engineer at Embark, details their experiences combining Rust and C++ code during the creation of the physx-rs open source project [[/r/rust](https://reddit.com/r/rust/comments/du91t1/an_unholy_fusion_of_rust_and_c_in_physxrs)]; -
[“Rust, Open Source, Game Dev”](https://youtube.com/watch?v=lpOg2nl3kr0)-[Jake Shadle](https://twitter.com/Ca1ne)explains how Rust, open source, and game development fit together [[/r/rust](https://reddit.com/r/rust/comments/du9g5d/rust_open_source_game_dev_stockholm_rust_meetup)];

Also, [Embark started a newsletter](https://embark.dev/#newsletter).
Check out the first issue
[“11/08/2019 - Rust, Blender, Hacktoberfest, and more: Newsletter 001 from Embark”](http://eepurl.com/gI3v89).

![Nannou example screenshot](../../assets/c30ce6e46663492b.png)


A beginner-level tutorial article teaching how to build a small demo
with the [nannou](https://nannou.cc) creative coding framework.

![Dungeon generation demo](../../assets/daca267cdb9651b2.gif)


[The Roguelike Tutorial](http://bfnightly.bracketproductions.com/rustbook) by [@blackfuture](https://patreon.com/blackfuture)
includes almost 60 chapters now and continues to grow!

Some of the November’s updates:

- backtracking/persistent maps,
- dynamic colored lighting,
- town portals, and teleportation in general (including optionally affecting NPCs),
- cheat mode (for testing later maps).

[nes-rust](https://github.com/takahirox/nes-rust) by [@superhoge](https://twitter.com/superhoge) -
[NES](https://en.wikipedia.org/wiki/Nintendo_Entertainment_System)(Famicom) emulator in Rust on the Web, compiled to WASM.

Check out the [online Demo](https://raw.githack.com/takahirox/nes-rust/master/index.html).

### Amethyst [#](https://gamedev.rs#amethyst)

![Amethyst logo](../../assets/5a989fd8c047334c.png)


-
[Blaine Price](https://blaineprice.me)is working on a “The Ten Top” game and shared a[“Rustlang Up Some Grub at The Ten Top”](https://blaineprice.me/posts/rustlang-up-some-grub)devlog about dependency graphs;![food truck](../../assets/bacf344f105f2322.jpg)

-
[@mvlabat](https://github.com/mvlabat)posted[“How can we improve custom shaders user experience?”](https://community.amethyst.rs/t/how-can-we-improve-custom-shaders-user-experience/1230); -
[“Future of nalgebra and math in Amethyst”](https://community.amethyst.rs/t/future-of-nalgebra-and-math-in-amethyst/1228)discussion; -
[“Skepticism about Rendy”](https://community.amethyst.rs/t/skepticism-about-rendy/1221)discussion;

## Popular Workgroup Issues in GitHub [#](https://gamedev.rs#popular-workgroup-issues-in-github)

[#50 “Linking Time”](https://github.com/rust-gamedev/wg/issues/50);[#51 “Using wasm-bindgen for games”](https://github.com/rust-gamedev/wg/issues/51);[#68 “Modding”](https://github.com/rust-gamedev/wg/issues/68);[#69 “Input Handling”](https://github.com/rust-gamedev/wg/issues/69);[#71 “Proof Of Concept Crate: Simplistic Bump Allocator”](https://github.com/rust-gamedev/wg/issues/71);[#73 “Membership Listing”](https://github.com/rust-gamedev/wg/issues/73);

## Meeting Minutes [#](https://gamedev.rs#meeting-minutes)

[See all meeting issues](https://github.com/rust-gamedev/wg/issues?q=label%3Ameeting) including full text notes
or [join the next meeting](https://github.com/rust-gamedev/wg#join-the-fun).

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[@kyren is looking for a new maintainer for “rlua”](https://reddit.com/r/rust/comments/dyhylu/luster_lua_vm_in_rust_this_project_is_currently);[Add assets (graphics, levels, sounds) to Le Train Dispatcher](https://itch.io/t/616119/contributing);[/r/rust: “Need help porting steam libraries to rust”](https://reddit.com/r/rust/comments/diuqg7/need_help_porting_steam_libraries_to_rust);[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs));[winit’s “Good first issue” and “help wanted” issues](https://github.com/rust-windowing/winit/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+label%3A%22status%3A+help+wanted%22+label%3A%22Good+first+issue%22);[gfx-rs’s “contributor-friendly” issues](https://github.com/gfx-rs/gfx/issues?q=is%3Aissue+is%3Aopen+label%3Acontributor-friendly);[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22);[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22);[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A);[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner);[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22);

## Bonus [#](https://gamedev.rs#bonus)

Just an interesting Rust gamedev link from the past. :)



![Pascal Penguin logo](../../assets/66d8698c34911903.png)

[release trailer](https://youtube.com/watch?v=EgFr73AUwps)

[“Adventures of Pascal Penguin”](http://luduminis.com/pascal/about/)
by [Matthew Michelotti](http://luduminis.com)
is a 2D grid-based puzzle game with levels designed around slippery ice.

Push blocks and bounce off bumpers as you try to reach the crystal at the end of each level. Grab invisibility orbs to walk through solid objects. Build a safe path over boiling lava and ice-cold water. There are 40 levels spread out across 5 zones. Can you complete them all?


Written using the [Gate](https://github.com/SergiusIW/gate) game engine.

That’s all news for today, thanks for reading!

Subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!