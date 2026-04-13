---
title: 'This Month in Rust GameDev #5 - December 2019'
url: https://gamedev.rs/news/005/
author: Rust GameDev WG
published: '2020-01-10'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the fifth issue of the Rust GameDev Workgroup’s monthly newsletter.

[Rust](https://rust-lang.org) is a systems language pursuing the trifecta:
safety, concurrency, and speed.
These goals are well-aligned with game development.

We hope to build an inviting ecosystem for anyone wishing
to use Rust in their development process!
Want to get involved? [Join the Rust GameDev working group!](https://github.com/rust-gamedev/wg#join-the-fun)

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).
Feel free to send PRs about your own projects!

I’m the community lead for

[Rust London]and I just wanted to put out the feelers for anybody who is London based and would like to give a talk at our Rust London Meetup. We want to hold a special LDN Talks event solely focused on GameDev.

## Game Updates [#](https://gamedev.rs#game-updates)

[A/B Street](https://github.com/dabreegster/abstreet#ab-street) - Adjust Traffic Patterns in Real Cities [#](https://gamedev.rs#a-b-street-adjust-traffic-patterns-in-real-cities)

Ever been on a bus stuck in traffic, wondering why there are cars parked on the
road instead of a bus lane?
[A/B Street](https://github.com/dabreegster/abstreet#ab-street) is a game exploring how small changes to
road space and traffic signals affect the movement of drivers, cyclists,
transit users, and pedestrians. The game models Seattle as accurately as
possible using [OpenStreetMap](https://openstreetmap.org) and other public datasets, lets the player adjust
existing infrastructure, and then does a detailed comparison to see who the
changes help and hurt.

A/B Street is written in Rust, using a custom GUI library on top of [glium](https://github.com/glium/glium).

[Play it now](https://github.com/dabreegster/abstreet/blob/master/docs/INSTRUCTIONS.md) and
[start contributing](https://github.com/dabreegster/abstreet/issues) to
expand the game to more cities, model light rail and shared foot/bike paths,
and work on gameplay modes (like “make everything as slow as possible” and
“what if nobody owned and parked personal vehicles?”).

![Demo of some UI work in A/B Street](../../assets/bc780faee8bbc9fd.gif)


December highlights:

- Preview traffic signal changes “live” without resetting the simulation
- UI: new minimap, popup info panels with graphs, better shapes, and colors for cars
- Data viz: histogram showing count of faster/slower trips, visualizing which road has the longest backup at a traffic signal, breaking down the timeline of a trip (walk to a car, drive somewhere, look for parking, walk to destination…)
- Improved pedestrian pathfinding and decisions to use a bus or not

*Discussions:
/r/rust*

![Vehicle’s collision shape](../../assets/2d656e755693ddb0.png)


[vange-rs](https://github.com/kvark/vange-rs) is the project of re-implementing the [Vangers](https://en.wikipedia.org/wiki/Vangers) game (from 1998)
in Rust using modern development practices, parallel computations, and GPU.

This month, the project has gained a few major features.
The biggest one is an implementation of the physics engine
completely on GPU in a closed loop.
At the same time, the CPU code path was fixed to allow
for a smooth ride ([video](https://reddit.com/r/rust_gamedev/comments/e8r695/vangers_gpu_physics_engine)).

Another pack of changes has landed to allow many NPC cars to be riding
the world alongside the user.
The renderer has shifted towards being completely instanced,
and CPU physics computations were parallelized.
The game can now host up to 50000 total cars on the level,
all simulated at once, with up to 5000 on screen at a time
([video](https://reddit.com/r/rust_gamedev/comments/eg3k6x/spawning_4k_of_cars_in_vangers)).

In minor features, it became possible to jump in the game as well as change the car color.

The project has also started the [development blog](http://kvark.github.io/vange-rs),
describing both new and old technology, such as:

[Data formats](https://kvark.github.io/vange-rs/2019/12/12/data-formats.html)used in the original game.[Collision model](https://kvark.github.io/vange-rs/2019/12/17/collision-model.html)of the original game.[Pure-GPU implementation](https://kvark.github.io/vange-rs/2019/12/19/gpu-collisions.html)of the collision model.

![Morning landscape](../../assets/d527c2cc51c6e187.png)


[Veloren](https://veloren.net) is an open world, open-source voxel RPG
inspired by Dwarf Fortress and Cube World.

Some of December’s updates:

- A formal changelog
- Pathfinding
- Airshipper launcher progress
- Erosion system improvements
- First animated UI elements

You can read more about some specific topics:

[Character States Overhaul](https://veloren.net/devblog-48#character-states-overhaul-by-adam)[Airshipper Update](https://veloren.net/devblog-46#airshipper-updates-with-songtronix)[SFX](https://veloren.net/devblog-46#sfx-with-shandley)[Contributor Spotlight: @AngelOnFira](https://veloren.net/devblog-46/#contributor-spotlight-angelonfira)[Pathfinding](https://veloren.net/devblog-45/#pathfinding-by-chrischrischris)[Mac Build Predicament](https://veloren.net/devblog-44/#lantern-slides-mac-build-predicament)[Unfinished Rust CI Blog](https://veloren.net/devblog-44/#lantern-slides-unfinished-rust-ci-blog)

![Sitting on the edge](../../assets/a7b7239f2311775f.png)


In the works for January include player account authentication, preliminary modding work, and character state systems. There are ongoing talks that are also looking into the networking system and optimizations.

December’s full weekly devlogs: “This Week In Veloren…”:
[#44](https://veloren.net/devblog-44),
[#45](https://veloren.net/devblog-45),
[#46](https://veloren.net/devblog-46),
[#47](https://veloren.net/devblog-47),
[#48](https://veloren.net/devblog-48).

![Some lake, hills, blue sunny sky and debug output](../../assets/71df66ca62c32202.png)


[voxel-rs](https://github.com/Technici4n/voxel-rs) is a new multiplayer Minecraft-like sandbox game engine
written in Rust using [wgpu-rs](https://github.com/gfx-rs/wgpu-rs).

The game is currently under heavy development and it’s not yet playable.


The project’s roadmap is [here](https://github.com/Technici4n/voxel-rs#roadmap).

*Discussion:
/r/rust*

![menu, levels, and customers](../../assets/046d4b17d54674da.gif)


[@oliviff](https://twitter.com/oliviff) released [v0.1.2](https://twitter.com/oliviff/status/1205891407606636544)..[v0.1.4](https://twitter.com/oliviff/status/1207671483981537280)
versions of “[Tennis Academy: Dash](https://iolivia.me/posts/6-months-of-rust-game-dev)”:

- 🖼️ art redesign, & new colour palette;
- ✂️ spritesheet and assets packing;
- 🧮 the game finally has a name: “Tennis Academy: Dash”;
- ⛱️ logo, splash screen, and UI polish.

![Trying to shoot down the missles](../../assets/4e78bcd20a3ddcd7.gif)


[Dank Defense](https://elijahlucian.itch.io/dank-defense-theyre-coming) by [Elijah Lucian](https://twitter.com/ELI7VHBO7)
is a fun little missle defense game made in Rust using [ggez](https://github.com/ggez/ggez).


[Akigi]is a multiplayer online world where most believe that humans are inferior.

Some of December’s updates:

- The game server was ported to
[specs](https://github.com/amethyst/specs); - The spawning system was rewritten and simplified;
- Initial scenery setup using YAML config files;
- Pathfinding now works between arbitrarily sized sets of tiles;
- Better test coverage;

Full December’s devlogs:
[#046](https://devjournal.akigi.com/december-2019/2019-12-15.html),
[#047](https://devjournal.akigi.com/december-2019/2019-12-22.html),
[#048](https://devjournal.akigi.com/december-2019/2019-12-29.html).

*Discussions:
/r/rust_gamedev*



![Playing with dirt](../../assets/05fc18ece0a1c164.gif)

[Garden](https://epcc.itch.io/garden) is an upcoming game centered around growing realistic plants.

Some of December’s updates:

- a new terrain system that doesn’t use voxels with surface nets anymore,
but regular cubic voxels with heightmaps (
[video](https://youtube.com/watch?v=xU93FGrk1d8)); - new building materials;
- improved rendering performance and compilation time;

![Updated cards & battle UI](../../assets/409f4029b4dd96ee.jpg)


[Slavic Castles](https://leinnan.itch.io/slavic-castles) is a card game inspired by [Arcomage](https://en.wikipedia.org/wiki/Arcomage).

The following changes were made since the last devlog:

- real cards that are loaded from JSON file;
- the project migrated to
[quicksilver](https://github.com/ryanisaacg/quicksilver); - menu, simple animations and visual & audio feedback;
- ability to save the game state.

*Discussions:
/r/rust_gamedev*

[Alex Butler](https://twitter.com/bigabgames) continues to polish their “[Robo Instructus](https://store.steampowered.com/app/1032170/Robo_Instructus)” puzzle game -
[1.18, 1.19, and 1.20 versions were released](https://steamcommunity.com/app/1032170/allnews):
UI tweaks, better translations (including full Russian translation!),
bugfixes, and performance optimizations.

-
[Azriel](https://azriel.im)published an[“I See The Character In UI”](https://azriel.im/will/2019/12/20/i-see-the-character-in-ui)devlog:- Character selection UI displays the character that the player will use.
- Control settings UI allows players to view the configured control keys.
- User interfaces (UIs) are largely defined through configuration, making development and customization easier.
- Events to control application behaviour can be defined in configuration.

-
[@dave_tucker](https://twitter.com/dave_tucker)is reimplementing some classics. -
[@carlosupina](https://twitter.com/carlosupina)has been adding animations and boss enemies to[Space Shooter](https://github.com/amethyst/space_shooter_rs); -
[@a5huynh](https://twitter.com/a5huynh)got the rotating map working;![Rotating map](../../assets/49db32566d8cd92c.gif)


## Library & Tooling updates [#](https://gamedev.rs#library-tooling-updates)

![Rayn output example - this renderer uses ultraviolet for its math](../../assets/0d2b219da9c5efb3.png)


[ultraviolet](https://crates.io/crates/ultraviolet) is a crate for computer-graphics and games-related linear algebra,
but *fast*, both in terms of productivity and in terms of runtime performance.

This month [ultraviolet v0.4](https://grayolson.me/blog/posts/ultraviolet-0.4) was released by [@fu5ha](https://twitter.com/fu5ha).
It brings
[transform](https://docs.rs/ultraviolet/0.4.3/ultraviolet/transform/index.html)
& [projection](https://docs.rs/ultraviolet/0.4.3/ultraviolet/projection/index.html)
modules and many smaller improvements.

Check out the [full release announcement post](https://grayolson.me/blog/posts/ultraviolet-0.4).

[component_group](https://github.com/sunjay/component_group) v0.2 [#](https://gamedev.rs#component-group-v0-2)

[component_group](https://github.com/sunjay/component_group) is a crate for working with a group of [specs](https://github.com/amethyst/specs)::Components.

This crate defines the

[ComponentGroup]trait. This trait is used to make managing a group of`specs::Component`

instances easier. This is useful when you have several components that are often created, read, and updated together. You can use this trait to easily move an entire group of components between instances of specs::World.

[This article](http://adventures.michaelfbryan.com/posts/ecs-outside-of-games) by [Michael Bryan](http://adventures.michaelfbryan.com) discusses
the usage of the ECS pattern in a [CAD](https://en.wikipedia.org/wiki/Computer-aided_design) library.
It’s obviously not about games,
but it still can be interesting for some game developers.

*Discussions:
/r/rust*

![The triangles generated with vertical and horizontal traversals of the same path](../../assets/43e7cfa6986b2d3b.png)


[Lyon](https://github.com/nical/lyon) a rust crate to tessellate arbitrary 2D shapes into
triangle meshes that can be easily rendered on the GPU.

This month [@nical](https://nical.github.io) released [Lyon 0.15](https://nical.github.io/posts/new-tessellator.html).
The fill tessellator was rewritten from scratch (it took two years),
it should solve robustness issues the previous implementation had
and also has a bunch of new features.

Check out the [full release announcement post](https://nical.github.io/posts/new-tessellator.html).

*Discussions:
/r/rust*

[winit](https://github.com/rust-windowing/winit) is a pure-Rust library for creating and managing windows.

A new alpha release of winit brings the web support. The web version expectedly has some API limitations (like window decorations, resizing, fullscreen, etc).

Web support is very much in alpha, and we’d like to encourage you to try it out and stress-test it so we can see where the issues are and improve where necessary.


Check out [the announcement post](https://users.rust-lang.org/t/winit-0-20-and-web-support/36155).

*Discussions:
/r/rust*

[ggez](https://github.com/ggez/ggez) is a lightweight game framework for making 2D games with minimum friction,
inspired by [love2D](https://love2d.org).

[Icefox](https://github.com/icefoxen) published [“The State Of GGEZ 2020”](https://wiki.alopex.li/TheStateOfGGEZ2020) blog post
with an overview of what happened in ggez’s development this year,
what is the current ggez 0.6 development status,
what’s in the roadmap, and thoughts about the Rust ecosystem.

*Discussions:
/r/rust*

[miniquad](https://github.com/not-fl3/miniquad) by [@fedor_games](https://twitter.com/fedor_games) is a safe cross-platform rendering library
focused on portability and low-end platforms support.

Web demos:
[quad](https://not-fl3.github.io/miniquad-samples/quad.html),
[offscreen](https://not-fl3.github.io/miniquad-samples/offscreen.html),
[astroblasto](https://not-fl3.github.io/miniquad-samples/astroblasto.html),
[arkanoid](https://not-fl3.github.io/miniquad-samples/arkanoid.html),
[zemeroth](https://not-fl3.github.io/miniquad-samples/zemeroth.html).

[@fedor_games](https://twitter.com/fedor_games) also posted a few Patreon updates this month:

After a year of work [godot-rust](https://github.com/GodotNativeTools/godot-rust) 0.7 bindings were released.
Some of the updates:

- Rust 2018;
- The API description of Godot classes was updated to the stable Godot version 3.1.1;
- More helper traits and derive/procedural macroses to reduce the boilerplate;
- Iterators for Godot collection types;
- New example projects;

Also, check out [a Godot-Specs example project](https://github.com/tom-leys/godot-rust/tree/feature_specs_integration_example/examples/specs_integration)
by [@RecallSingularity](https://twitter.com/RecallSingular1).

[raylib](https://raylib.com) is a simple C 2D/3D game engine with virtually no dependencies.
This month, [raylib-rs](https://github.com/deltaphc/raylib-rs) 1.0 was released - mostly idiomatic
and thread-safe Rust raylib bindings.

*Discussions:
/r/rust_gamedev*

[Makepad](http://makepad.nl) is a creative software development platform for Rust
that compiles to WASM/WebGL, macOS/Metal, Windows/DX11, Linux/OpenGL.

An early alpha version of Makepad Basic was launched. This version shows off the development platform, but does not include the visual design tools or library ecosystem yet.

Play with Rust+Wasm live at [makepad.nl](http://makepad.nl).

*Discussions:
/r/rust*

[Tetra](https://tetra.seventeencups.net) is a simple 2D game framework
that uses SDL2 for event handling and OpenGL 3.2+ for rendering.

This month, [@17cupsofcoffee](https://twitter.com/17cupsofcoffee) has released Tetra v0.3.
Main changes are:

[nalgebra](https://nalgebra.org)linalg library was replaced with[vek](https://github.com/yoanlcq/vek);- Improved window/input events;
- Improved cameras/transform matrices;
- More flexible screen scaling;
- Better error handling;

[@17cupsofcoffee](https://twitter.com/17cupsofcoffee) also posted [a little example](https://gist.github.com/17cupsofcoffee/f5082a13626ddf0030075d542262c728)
of how you can implement pooling for sound effects

This is handy for situations where you don’t want more than X instances of the same sound playing at once (e.g. if the player is able to fire a weapon as fast as they can hit a button), etc…


[@puppetmaster updated their “Compact Space” game](https://twitter.com/fischspiele/status/1206014736300728322)
to Tetra 0.3, added some sound effects and a little x-max surprise.

[@JohanLindfors](https://twitter.com/JohanLindfors) updated their [Snake](https://github.com/programmeramera/snake-in-tetra)
and [Flappy Bird](https://github.com/programmeramera/flappy-in-rust) sample games to Tetra 0.3.

Also, the Snake sample now has
[a ten step tutorial on how to build it from scratch](https://github.com/programmeramera/snake-in-tetra/tree/5c7cc79f8/tutorial).

[rg3d-sound](https://github.com/mrDIMAS/rg3d-sound) is a new sound library in active development.

This month it has gained three major features:

[Head-related transfer function](https://en.wikipedia.org/wiki/Head-related_transfer_function)support - it provides perfect binaural sound. Try it:`cargo run --example hrtf --release`

[Reverberation](https://en.wikipedia.org/wiki/Reverberation)support - basic effect that gives your scene “sound volume”. Try it:`cargo run --example reverb --release`

[Vorbis/ogg](https://en.wikipedia.org/wiki/Vorbis)support - a compressed format similar to mp3.

[rg3d-sound](https://github.com/mrDIMAS/rg3d-sound) is a component of the [rg3d](https://github.com/mrDIMAS/rg3d) game engine.

### @siebencorgie’s Voxel Engine [#](https://gamedev.rs#siebencorgie-s-voxel-engine)

![roughness-based reflections](../../assets/245abc594e99b26c.jpeg)


[@siebencorgie](https://twitter.com/siebencorgie) got [voxel global illumination](https://twitter.com/siebencorgie/status/1209086915925991425)
and [voxel cone traced reflections](https://twitter.com/siebencorgie/status/1201171106641698816) working in their voxel engine.

![Rendology demo screenshot](../../assets/9a3f891ff748f8a7.png)


[Rendology](https://github.com/leod/rendology) is a 3D rendering pipeline based on Glium and written in Rust.
It features basic implementations of shadow mapping, deferred shading,
a glow effect, FXAA and instanced rendering.

An [“Introduction to Rendology”](https://leod.github.io/rust/gamedev/rendology/2019/12/13/introduction-to-rendology.html) article
outlines some of the concepts of Rendology
and describes how they came to be this way.

*Discussions:
/r/rust*

[Oxygengine](https://github.com/PsichiX/Oxygengine) v0.5 [#](https://gamedev.rs#oxygengine-v0-5)

[Oxygengine](https://github.com/PsichiX/Oxygengine) is
“the hottest HTML5 + WASM game engine for games written in Rust with web-sys”.

Main updates of v0.5 version:

- Automated asset packs generation on build phase;
- Loading assets from asset packs;
- Support for audio: sound effects (buffered) and background music > (streaming);
- Support for 2D physics (rigid bodies and colliders) via
[nphysics2d](https://nphysics.org/); - A new example:
[a basic web game](https://github.com/PsichiX/Oxygengine/tree/master/demos/basic-web-game).

*Discussions:
/r/rust*

![Mun logo](../../assets/90b7f565d888913b.png)


[Mun](https://mun-lang.org) is a scripting language for gamedev focused on quick iteration times
that is written in Rust.

[December updates](https://mun-lang.org/blog/2020/1/1/this-month-december) include:

- Parsing of tuple data structures;
- Parsing and type inferencing of data structure literals;
- Indexing of data structure fields;
- Improved handling of data structure information;
- Type checking of binary operations;
- A community member made a PoC of Mun-powered hot reloading
in
[Veloren](https://veloren.net);

![Roguelike gameplay sample](../../assets/9057ef911b4bda0f.gif)


[The Roguelike Tutorial](http://bfnightly.bracketproductions.com/rustbook) by [@blackfuture](https://patreon.com/blackfuture)
includes almost 70 chapters now and continues to grow!

Some of the December’s updates:

- item identification and magical weapons;
- a generic “effects” system;
- cursed items, scrolls of remove curse, and item identification scrolls;
- items that affect your attributes, generic statuses;
- spells, spellbooks, weapon proc fx, mob special abilities, DoT, initiative +/- effects;
- a dragon lair in a ruined fort;
- multi-tile entities including pathfinding;
- parameterized procgen of magic weaponry/armor;

Also, check out
[@blackfuture’s 2019 Roguelike Development Retrospective post](https://reddit.com/r/roguelikedev/comments/eij9nl/2020_in_roguelikedev_one_knight_in_the_dungeon).

[doryen-rs](https://github.com/jice-nospam/doryen-rs) is an ASCII roguelike library with native and WASM support.
Uses the uni-gl and uni-app crates from the [unrust](http://github.com/unrust/unrust) game engine.

[doryen-rs](https://github.com/jice-nospam/doryen-rs) v1.2.1 was released this month.
Some of the new features:

- added InputApi.keys_released() and InputApi.keys_pressed() that return iterators on key events since last update;
- added alpha example showcasing framebuffer overdrawing;
- added text input support through InputApi.text();
- added a visual demo showcasing subcell resolution + dynamic lighting in a real time roguelike;

![Multiplayer session](../../assets/1f0daf5324db13e6.png)


[nes-rust](https://github.com/takahirox/nes-rust) by [@superhoge](https://twitter.com/superhoge) -
[NES](https://en.wikipedia.org/wiki/Nintendo_Entertainment_System) (Famicom) emulator in Rust on the Web, compiled to WASM.

This month nes-rust got remote multiplay:

Once you enter a room, share the URL with someone and start the game you want to play with them. Enjoy!


![Animation editing sample](../../assets/fedfbee24c3f5c02.gif)



[rx]is an extensible, modern and minimalist pixel editor, designed with great care and love for artists and hackers. It was conceived to have as little UI as possible, and instead focus on the work.

The 0.3 release comes with:

[vim-like visual mode](https://rx.cloudhead.io/videos/manipulating.webm),- a
[new website](https://rx.cloudhead.io), - and a
[user guide](https://rx.cloudhead.io/guide.html)!

*Discussions:
/r/rust*

[Texel](https://github.com/almindor/texel) is an ASCII art and landscape editor with VIM-like controls.
It aims to make editing ASCII art easy especially for use in games.

*Discussions:
/r/rust*

![Embark’s logo](../../assets/0804351e23fb6199.png)


[Embark](https://embark.rs) posted [the second issue of their newsletter](https://us20.campaign-archive.com/?u=4206f0696b8b13a996c701852&id=0339af3ed2).
Here’re some of the Rust news from it:

[“Inside Rust at Embark 🦀”](https://medium.com/embarkstudios/inside-rust-at-embark-b82c06d1d9f4)- a peek inside Embark’s day-to-day work with Rust and open source gamedev ([/r/rust](https://reddit.com/r/rust/comments/e7120k/inside_rust_at_embark));[cargo-about](https://github.com/embarkstudios/cargo-about)- a cargo plugin to generate list of all licenses for a crate ([/r/rust](https://www.reddit.com/r/rust/comments/e74uux/embarkstudioscargoabout_cargo_plugin_to_generate))

## Popular Workgroup Issues in GitHub [#](https://gamedev.rs#popular-workgroup-issues-in-github)

[#32 “Selective Enabling/Disabling optimizations at a crate/file/function level”](https://github.com/rust-gamedev/wg/issues/32);[#46 “Make sure key crates have](https://github.com/rust-gamedev/wg/issues/46);`crev`

code reviews”[#69 “Input Handling”](https://github.com/rust-gamedev/wg/issues/69);[#71“ Proof Of Concept Crate: Simplistic Bump Allocator“](https://github.com/rust-gamedev/wg/issues/71);[#75 “Standardised API for sharing thread pools”](https://github.com/rust-gamedev/wg/issues/75);[#77 “Can we contribute to OpenXR to get Keyboard/Mouse support to be official?”](https://github.com/rust-gamedev/wg/issues/77);[#79 “Polymorph project”](https://github.com/rust-gamedev/wg/issues/79);

## Meeting Minutes [#](https://gamedev.rs#meeting-minutes)

[See all meeting issues](https://github.com/rust-gamedev/wg/issues?q=label%3Ameeting) including full text notes
or [join the next meeting](https://github.com/rust-gamedev/wg#join-the-fun).

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs));[winit’s “Good first issue” and “help wanted” issues](https://github.com/rust-windowing/winit/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+label%3A%22status%3A+help+wanted%22+label%3A%22Good+first+issue%22);[gfx-rs’s “contributor-friendly” issues](https://github.com/gfx-rs/gfx/issues?q=is%3Aissue+is%3Aopen+label%3Acontributor-friendly);[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22);[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22);[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A);[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner);[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22);[A/B Street’s “good first issue” issues](https://github.com/dabreegster/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22);

## Bonus [#](https://gamedev.rs#bonus)

Just an interesting Rust gamedev link from the past. :)



![Modulator video](../../assets/94d296bb067031b1.gif)

In the November of 2018,
[@AndreaPessino](https://twitter.com/AndreaPessino) (Founder/CTO of [Ready At Dawn](https://readyatdawn.com) Studios)
released a [Modulator](https://github.com/apessino/modulator) crate and an awesome
[“Modulator (Rust conding series)”](https://youtube.com/watch?v=n-txrCMvdms) tutorial video about it.

[Modulator](https://github.com/apessino/modulator) is a Rust crate for abstracted, decoupled modulation sources.

Modulators are sources of change over time which exist independently of the parameters they affect, their destinations.


Modulator comes with playground/testbed application [Modulator Play](https://github.com/apessino/modulator_play):

An environment to visualize and test the modulator crate and to experiment with expressive 2d primitive rendering. Based on Piston Window, this application is meant to be both a test bed for the Modulator crate and its included source types, and a minimal friction environment to experiment with Rust coding.


*Discussions:
/r/rust*

That’s all news for today, thanks for reading!

Subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!