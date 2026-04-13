---
title: 'This Month in Rust GameDev #7 - February 2020'
url: https://gamedev.rs/news/007/
author: Rust GameDev WG
published: '2020-03-05'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the seventh issue of the Rust GameDev Workgroup’s monthly newsletter.

[Rust](https://rust-lang.org) is a systems language pursuing the trifecta:
safety, concurrency, and speed.
These goals are well-aligned with game development.

We hope to build an inviting ecosystem for anyone wishing
to use Rust in their development process!
Want to get involved? [Join the Rust GameDev working group!](https://github.com/rust-gamedev/wg#join-the-fun)

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).
Feel free to send PRs about your own projects!

![Thanks cloud: Amethyst, ggez, gfx-rs, specs, serde and many other projects](../../assets/0d240805e38a6373.png)


The [results](https://rust-gamedev.github.io/posts/survey-01) of the Rust GameDev [ecosystem survey](https://rust-gamedev.github.io/posts/newsletter-001/#survey-from-the-rust-gamedev-working-group-clipboard)
were published.

After an unfortunate delay, we can finally present the results. We received a whopping 403 responses! This trove of valuable feedback will inform the WG’s roadmap for 2020.


*Discussions:
/r/rust,
/r/rust_gamedev*

[Are We Game Yet?](https://arewegameyet.com/) Updates [#](https://gamedev.rs#are-we-game-yet-updates)

[Are We Game Yet?](https://arewegameyet.com/) is a website cataloguing the Rust gamedev ecosystem,
with hundreds of links to crates, games and helpful resources.

This month, it received some major updates:

- All of the site’s data files have been unified into a consistent TOML schema, making it easier to add new links.
- Categories have been added for games and resources, and you can now add an item to multiple categories without duplicating the data.
- Page load times have been reduced (especially on the homepage).
- The styling has been improved to make the site look better on mobile, and to resolve some accessibility issues.

[Ownership was also recently transferred across to the gamedev working group](https://github.com/rust-gamedev/arewegameyet/issues/210),
to allow for more people to help with maintainance.

There’s never been a better time to add your projects to the site,
so [please come and contribute](https://github.com/rust-gamedev/arewegameyet#contribute)!

A new Discord server dedicated to Rust GameDev was started
by [@dasifefe](https://github.com/dasifefe) this month:
[ invitation link](https://discord.gg/yNtPTb2).

Besides talking about Rust, it’s a place that could be used to show your work-in-progress, art (visual or audio), discuss game design, etc.

Also, in case you didn’t know, there is a quite active “games-and-graphics”
channel on the [community-run Discord server](https://discord.gg/6Zvghp).

![Tallin’s old town](../../assets/d4743c5d04930462.jpeg)


[@logicsoup](https://twitter.com/logicsoup) - one of the developers behind [Garden](https://epcc.itch.io/garden) -
[is planning to organize](https://twitter.com/logicsoup/status/1224404367723454478) the first (and hopefully one of many)
Rust Hack’n’Learn meetup in Tallinn on March 13.

A Hack’N’Learn is an event where we get together and work on personal (or open-source) projects on our own computers.


If you’re interested, visit ** tallinn.rs** and follow

[@RustTallinn](https://twitter.com/RustTallinn).

## Game Updates [#](https://gamedev.rs#game-updates)

![Rusty Shooter in-game screenshot](../../assets/a14019d508981f10.jpg)


[Rusty Shooter](https://github.com/mrDIMAS/rusty-shooter) is a Quake3-like first-person shooter
written in Rust using [rg3d engine](https://github.com/mrDIMAS/rg3d).

Features:

- Common FPS elements: bots, items, weapons;
- Single game mode - deathmatch;
- More or less modern graphics (shadows, deferred shading, particle systems etc.);
- Fully animated bots using animation blending state machines;
- Single map - something like legendary Q3DM6;
- Path finding using navmesh;
- Save/load functionality;
- GUI: main menu, options, HUD, leader board (using
[rg3d-ui library](https://github.com/mrDIMAS/rg3d-ui)); - Binaural sound (using
[rg3d-sound library](https://github.com/mrDIMAS/rg3d-sound)).

Small gameplay video (work-in-progress):

![itch.io page: ASCII art logo with an ant, game features, video and screenshots](../../assets/80ae2d28ae7aa5ec.png)


[Native Systems](https://nativesystems.rs) is working on “Colony Genesis” -
an ant colony sandbox game with ASCII graphics.

Establish a new colony and help it grow or let it develop on its own.


This month an alpha version was published on itch: [check it out here](https://nativesystems.itch.io/colony).

![Rolling mountain landscape](../../assets/155540ad4eadc439.png)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG
inspired by Dwarf Fortress and Cube World.

At the beginning of the month, the team met for a 0.6 intro meeting. It was decided that 0.6 would focus on things for the player to do, and hence will be called “The Content Update”.

Research has been done on multiple areas this month. One domain is level of detail, which is allowing mountains off in the distance to be rendered much faster. Another domain is server persistence. Finding a way for the server to efficiently persist player information is a large part of what is needed for The Content Update.

Here is the February changelog:

```
- Fixed NPCs attacking the player forever after killing them
- Extend run sfx to small animals to prevent sneak attacks by geese
- Added sfx for wielding/unwielding weapons
- Added new orc hairstyles
- Added gamma setting
- Configurable fonts
- Translation status tracking
- Fixed /give_exp ignoring player argument
- Allow spawning individual pet species, not just generic body kinds
- Added daily Mac builds
- Removed highlighting of non-collectible sprites
- Added zoomable and rotatable minimap
- Added rotating orientation marker to main-map
- Brighter / higher contrast main-map
- Added music system
```




![veloren development](../../assets/364661a0ef058e89.gif)

You can read more about some specific topics:

![Hanging out](../../assets/678f803572d73ed1.png)


In March, there will be a heavy focus on completing level of detail work as well as persistence. Modding support will be explored further. Player achievements will be merged into the game, and we will start looking at where more content can be added.

February’s full weekly devlogs: “This Week In Veloren…”:
[#53](https://veloren.net/devblog-53),
[#54](https://veloren.net/devblog-54),
[#55](https://veloren.net/devblog-55),
[#56](https://veloren.net/devblog-56).



![Gameplay demo: two giant tank armies clashing](../../assets/a67708c7e4cf2071.gif)

[Oxidator](https://github.com/Ruddle/oxidator) by [@Ruddle](https://github.com/Ruddle) is a real-time strategy game/engine
written with Rust and WebGPU.
It’s inspired by Total Annihilation, Supreme Commander, Spring Engine,
and Zero-k.

The project’s goal is to provide a modern, carefully crafted, minimal and highly constrained set of tools for players/designers to create mods without programming knowledge.

Some of the current features:

- Simulation: working draft of flock behavior and collision detection, basic health and damage computation, construction and repair;
- Rendering: basic display of a heightmap & 3D models (with instancing), fxaa, screen-space reflections;
- UI: select units (picking and rectangle selection), move & build orders;
- Multiplayer: working PoC localhost tcp client/server;
- Map editor: raise, lower, flatten, blur, noise pencil;
- Unit editor: basic editor with joint & mesh selection and parameter editing (speed, turn rate, health, etc);



![Unit editor demo: move agent's parts](../../assets/f82b206f034315bc.gif)



![Map editor demo: use pencil tool to instantly create a lake and mountains](../../assets/6d9d7e9dc0e2efa7.gif)

[UniverCity](https://store.steampowered.com/app/808160/UniverCity) is an isometric university management game:

Manage your staff, professors and students and try and build the best UniverCity around! Build up your UniverCity solo or against friends and build many different types of classes whilst trying to ensure students get good grades, or maybe just try and build the best looking UniverCity.


This month, [v1.0 was released on Steam](https://steamcommunity.com/gid/103582791461907043/announcements/detail/1694978169192631655)
along with [releasing the game’s sources under GPL-3](https://github.com/Thinkofname/UniverCity).

This update

marks the end of development for nowand adds in some basic workshop support.

![Demo: builing a classroom](../../assets/9ed4d9ca9b9568cb.gif)


The license is GPL-3 and the code is the same as the version released on Steam (the Steam version is built with the ‘steam’ feature enabled). Due to the GPL licensing the steamworks support is disabled by default which breaks things like the ‘modding’ menu and multiplayer.

The assets

are not includedwith the release and will have to be copied from the game on Steam.

*Discussions:
/r/rust*

![Everpuzzle preview](../../assets/0f06f78b0125427b.gif)


[Everpuzzle](https://github.com/Skytrias/everpuzzle) is a Tetris Attack like action-puzzle game written in Rust.

Everpuzzle aims to become a similar game like Tetris Attack and expand on its concepts. The project was recently rewritten with minimal dependencies to achieve small compile times and gain more control over the underlying engine architecture. In the past Everpuzzle was using Amethyst with ECS, however there were some issues that made development difficult. Everpuzzle’s big goals are AI, Multiplayer and different Game modes.

Big changes coming in version 0.2, full list [here](https://github.com/Skytrias/everpuzzle/blob/master/CHANGELOG.md):

- Gamepad support (singleplayer)
- Multiple grids
- AI Bot
- Better Randomization of blocks
- Combos / Chains - with Highlighting
- Better animations

Video: [Everpuzzle rewrite - Code Walkthrough (code outdated)](https://youtube.com/watch?v=qA2zcaUVRKY).

![Spider NPCs](../../assets/a614347de947a21f.jpg)


[Antorum](https://dooskington.com) is a multiplayer RPG where players build their characters
and fight against the growing threats on the isle.
The game server is authoritative and written in Rust,
while the client is written in Unity/C#.

This month, the focus was on cooking skill. This includes recipes and cookware. Players will need a cooking appliance, such as a stove or campfire to cook some Chonkrat Stew inside a pot. A heavy refactor to the interaction system had to be made, as well as changes to networking.

Check out te full devlog: [#18 “Cooking”](https://dooskington.com/dev-log/18).

![Traffic lights](../../assets/231fd92b9defb785.png)


[Scale](https://github.com/Uriopass/Scale) is a recent project about modern day society simulation from the
bottom-up by [Uriopass](http://douady.paris/aboutme.html).

In February, the Inspector for specs entities was mostly finished and the
traffic simulation made great progress.
A second [blog post](http://douady.paris/blog/scale_2.html) was released about it.

[A recent video](https://youtu.be/nk6F42BQllU) also shows different traffic features such
as traffic lights, stop signs and car AI working together.

*Discussions:
/r/rust_gamedev*

![Ultimate scale screenshot showing winds and blips](../../assets/6c058509d21a95db.png)


[Ultimate Scale](https://github.com/leod/ultimate-scale) is a puzzle game in which you build
increasingly large machines to solve increasingly difficult problems.
The game consists of wind and blips.
Wind propagates along pipes and causes blips to move.
Blips, in turn, activate blocks.

[Leod](https://leod.github.io/) is currently working on the core design: How to make the game fun and
what blocks to add. He posted about their thoughts and progress on a
[Reddit comment](https://reddit.com/r/rust_gamedev/comments/f3cll6/ultimate_scale_counting_modulo_three/fhhu5ol).
Regularly, videos are posted on their
[youtube channel](https://youtube.com/channel/UChSw7WP2i0GIw61FIeTeGsA) showing different machines
made in game such as an [extensible counter modulo 10](https://youtu.be/zmKRJAF4xcI)
and a [buffer](https://youtu.be/IM3BRM_MZrE).

A custom 3D rendering pipeline based on glium called [Rendology](https://github.com/leod/rendology) was developed
for this project. A [blog post](https://leod.github.io/rust/gamedev/rendology/2019/12/13/introduction-to-rendology.html) talks about its design and
relation to Ultimate Scale.

*Discussions:
/r/rust_gamedev*

![release](../../assets/1974a977a6d6a637.gif)


Tennis academy dash is a time management game where you are the manager of a tennis academy and you need to coordinate various players to play on your courts.

The game is still a work in progress, but the demo version
has been uploaded to itch.io this month, so you can go ahead and check it out!
Give it a go
(the build is only for mac at the moment but other platforms coming soon)
and drop a comment with any feedback on [tennis-academy-dash](https://iolivia.itch.io/tennis-academy-dash).

[Alexandru Ene](https://alexene.dev) is working on a dwarf colony management game “Dwarf World”.

This month, the project got an official site: [dwarf.world](https://dwarf.world).

Also, check out development streams:
every Sunday at 19:30 PM GMT [on Twitch](https://twitch.tv/nomad_pixel).


Space is a lonely place, but at least you’ve got the music to keep you company.

[Lonely Star](https://17cupsofcoffee.itch.io/lonely-star) is a side-scrolling infinite runner,
with simple generative music.
You collect orbs and fly through rings in order to play notes and stay alive.

It was developed by [17cupsofcoffee](https://twitter.com/17cupsofcoffee),
using the [Tetra](https://github.com/17cupsofcoffee/tetra) 2D game framework,
for [Weekly Game Jam #135](https://gamedev.rs/news/007/weekly-game-jam-135).

Tetra itself also received two small updates recently:

[Version 0.3.2 was released](https://twitter.com/17cupsofcoffee/status/1217524602513055749), with bugfixes and some tools for simple AABB collision detection.[The Pong tutorial was updated with a new chapter](https://twitter.com/17cupsofcoffee/status/1219758851416895489), showing how to use Tetra’s graphics and input APIs.

![High detail terrain chunk with PRR](../../assets/421b1967230be4a9.png)

[Akigi](https://akigi.com) is a multiplayer online world where most believe that humans are inferior.

This month saw a heavy focus on the web client. An alpha release is slated for April 9th, 2020. Lots of client refactoring was done, and experiments were run in the browser.

Some of February’s updates:

[Input Event Processor System](https://devjournal.akigi.com/february-2020/2020-02-09.html#input-event-processor-system);[Terrain Loading and Rendering](https://devjournal.akigi.com/february-2020/2020-02-16.html#terrain-loading-and-rendering);[User Interface Elements](https://devjournal.akigi.com/february-2020/2020-02-16.html#user-interface-elements);[The WebGL Renderer](https://devjournal.akigi.com/february-2020/2020-02-16.html#the-webgl-renderer);[Rendering Meshes](https://devjournal.akigi.com/february-2020/055-2020-02-23.html#rendering-meshes);[Rendering Terrain](https://devjournal.akigi.com/february-2020/055-2020-02-23.html#rendering-terrain);

February’s full devlogs:
[#053](https://devjournal.akigi.com/february-2020/2020-02-09.html),
[#054](https://devjournal.akigi.com/february-2020/2020-02-16.html),
[#055](https://devjournal.akigi.com/february-2020/055-2020-02-23.html),

![Will Network Play Screenshot](../../assets/e181d43fbad270c3.png)


[Will](https://azriel.im/will/) is a 2.5D moddable action / adventure game.

This month Azriel wrote a post about how decisions were made when [designing
network play](https://azriel.im/will/2020/02/29/designing-network-play/).

[Way of Rhea](https://store.steampowered.com/app/1110620/Way_of_Rhea) is an upcoming puzzle platformer that takes place
in a world where you can only interact with objects that match your current color.

This month, an updated trailer with new character art was released.
[Check it out on the game’s Steam page](https://store.steampowered.com/app/1110620/Way_of_Rhea).

### Noodle Cat [#](https://gamedev.rs#noodle-cat)

![Noodle game physics demo](../../assets/f08cf4eb73182151.gif)


[@Fryer00](https://twitter.com/Fryer00) tweeted a bunch of updates about their
WIP Box2D physics game prototype:

- Day 45:
[contraction mechanic](https://twitter.com/Fryer00/status/1225829271597395971); - Day 46:
[turn/flip/swap-front-and-back movement mechanics](https://twitter.com/Fryer00/status/1227327016380305415); - Day 48:
[food](https://twitter.com/Fryer00/status/1232181181690654720).

![pyramid generation demo](../../assets/8b15fe5c233fc0b9.jpg)


[Garden](https://epcc.itch.io/garden) is an upcoming game centered around growing realistic plants.

[January](https://cyberplant.xyz/posts/january) and [February](https://cyberplant.xyz/posts/february) devlogs
were posted by [@logicsoup](https://twitter.com/logicsoup).
Some of the updates:

- 🌘 Physically-based shading
- 🕹 3D model loading and texturing for richer environments
- 💦 Soil moisture content
- 🌠 Alpha mipmapping
- and more info regarding some game mechanics as well

![Magic missiles in Grumpy Visitors](../../assets/df68596ea3138b1f.jpg)


Grumpy Visitors is a top-down 2D co-op action/arcade game highly inspired by Evil Invasion. It runs on Amethyst game engine.

This winter Grumpy Visitors received some updates with the focus on graphics and UI:

- Repainting mage sprites with shaders
- New missiles graphics
- Monsters death animations
- Modal windows for menu UI

Check them out in the [latest winter devlog](https://mvlabat.github.io/2020-03-02-winter-update/).

![cities, planes and keys](../../assets/5969840f785f36ed.png)

[Make China Great Again](https://globalgamejam.org/2020/games/make-china-great-again-5) ([source](https://github.com/PsichiX/global-game-jam-2020))
by [@PsichiX](https://github.com/PsichiX) is a GlobalGameJam game written using [Oxygengine](https://github.com/PsichiX/Oxygengine).

### pGLOWrpg [#](https://gamedev.rs#pglowrpg)

![37 possible unique biomes](../../assets/b71aca7ac5d839af.gif)


[@Roal_Yr](https://twitter.com/Roal_Yr) tweeted a bunch of updates about their “pGLOWrpg” project:

[proper river attractors](https://twitter.com/Roal_Yr/status/1218940947070885888);[floodfill and distinguished regions](https://twitter.com/Roal_Yr/status/1218634118516396033);[extravagant dev environment](https://twitter.com/Roal_Yr/status/1229785132455878656);[optimized pathfinding, unique regions](https://twitter.com/Roal_Yr/status/1228659336349655042);[Reworked noise and erosion](https://twitter.com/Roal_Yr/status/1231139098288697345);[37 possible unique biomes](https://twitter.com/Roal_Yr/status/1231640620072128512);

[Alex Butler](https://twitter.com/bigabgames) continues to polish their “[Robo Instructus](https://store.steampowered.com/app/1032170/Robo_Instructus)” puzzle game -
[1.23 and 1.24 versions were released](https://steamcommunity.com/app/1032170/allnews):
dependency updates, bugfixes and performance optimizations.

![Harvesting and refining some Gold](../../assets/9353bd7ece356e35.png)

[Tom Leys](https://twitter.com/RecallSingular1) is working on a “The Recall Singularity” game
about designing autonomous factory ships and stations.
This month, they published a devlog post:
[“Space Factory Building in Feb 2020”](https://medium.com/@recallsingularity/recalling-nov-2019-236cdf9c0a8a).

Some of the updates:

- Networking improvements;
- Godot-Rust interaction improvements;
- Players can now control their ships and create new ones;
- Top-down view and flying HUD;
- Asteroids procgen.

Also, the post gives an overview of the project’s history, talks about community building, and overcoming personal challenges.

Check out stream highlights on [Tom’s YouTube channel](https://youtube.com/channel/UCzgUlowiaKXJiNIAi0c9Qsg/videos).

*Discussions:
/r/rust*

### For the Quest [#](https://gamedev.rs#for-the-quest)

![walking demo](../../assets/02d8e0207360c9fc.gif)


[@seratonik](https://twitter.com/seratonik) tweeted a bunch of updates
about their “For the Quest” (working title) game project:

- Switched to the
`specs`

ECS; - Added a few new object models and an 8-direction animated sprite with idle animations;
- The map renderer is now powered by a chunking system to fix clipping issues;
- Added basic collision detection.

## Library & Tooling Updates [#](https://gamedev.rs#library-tooling-updates)

[joetsoi](https://joetsoi.github.io) has written [a blog post](https://joetsoi.github.io/fix-your-timestep-rust-ggez/), demonstrating how the concepts
from the well-known ‘[Fix Your Timestep](https://gafferongames.com/post/fix_your_timestep/)’ article can be applied
when making games with Rust and GGEZ.

The examples are very well explained, and can easily be translated to other engines, so it’s worth checking out even if you’re not a GGEZ user!

Main updates:


- New pressure resolution methods.
- Viscosity, surface tension, and elasticity can now be simulated.
- Ability to remove fluids/boundaries/collider couplings after their addition.
- Ability to add particles to a fluid that has already been created.

Watch a [“Salva 0.2: DFSPH, viscosity, surface tension, and elasticity”](https://youtube.com/watch?v=NBoSEanWHE4)
demo video.

*Discussions:
/r/rust*

### savefile 0.6.1 [#](https://gamedev.rs#savefile-0-6-1)

[savefile](https://crates.io/crates/savefile) is a serialization crate used to effortlessly serialize rust crates
and enums into a binary format. Anything implementing the `Write`

trait can
be serialized and deserialized. First-class versioning support and introspection
are some other features available.

Version 0.6.1 includes a fix and should be updated to if compilation using
the savefile-derive crate produces a “`SaveFileError`

not found” compiler error.

For details, see the [github page](https://github.com/avl/savefile) or the [savefile documentation](https://docs.rs/savefile/0.6.1/savefile).

### specs 0.16 [#](https://gamedev.rs#specs-0-16)

[specs](https://crates.io/crates/specs) is an entity-component system (ECS) library, designed for high
performance. This update increases the MSRV to 1.38 and removes the `"nightly"`

feature.

In this version, the [panic message has been improved](https://github.com/amethyst/shred/issues/182) to include
the name of the type that is accessed on stable Rust, as well as suggestions for
how to fix the issue. Prior to `specs 0.16`

, retrieving a resource that had not
been added to the `World`

panics with an obscure *“resource not found”* message,
and the `"nightly"`

feature was necessary to discover what resource that is.

In addition, the [ Send and Sync trait constraints are
removed](https://github.com/amethyst/specs/issues/673) from resources and


`Component`

s when the
`"parallel"`

feature is disabled – enabling types such as
`wasm_bindgen::JsValue`

to be used with non-parallel `specs`

.For more details, please see the [ specs changelog](https://github.com/amethyst/specs/blob/0.16.1/CHANGELOG.md#0161-2020-02-18).

![Riot Games API logo: steampunk](../../assets/9a6970d4fda58ff0.jpg)


[riven](https://github.com/MingweiSamuel/Riven) is a [Riot API](https://developer.riotgames.com/) library for Rust.

Riven handles rate limits and large requests with ease. Data structs and endpoints are automatically generated from the

[Riot API Reference]([Swagger]).

*Discussions:
/r/rust*

[weasel](https://github.com/Trisfald/weasel) by [@Trisfald](https://github.com/Trisfald) is a customizable battle system for turn-based games.

- Simple way to define the combat’s rules, taking advantage of Rust’s strong type system.
- Battle events are collected into a timeline to support save and restore, replays, and more.
- Client/server architecture; all battle events are verified by the server.
- Minimal performance overhead.

The idea behind this crate is to provide a structured and safe framework to manage the game state. Users can create a battle and evolve it by applying events. Then, weasel takes care of keeping a historical timeline. It also help with serializing/deserializing save files or sharing and verifying events between clients and server. The game logic is defined through traits, which is nice because it can benefit from Rust’s type system and compile time checks.


Check out [examples](https://github.com/Trisfald/weasel/tree/master/examples) to see how it works in practice.

[Shipyard](https://crates.io/crates/shipyard) is an ECS library built on top of sparse sets.

Some of [the v0.3 updates](https://reddit.com/r/rust/comments/fbo8wf/shipyard_03_release):

- There’s now a
[User guide](https://leudz.github.io/shipyard/book)to explain what can be done and how; - No need to register components anymore, storages are now automatically created when they are first accessed;
- !Send and !Sync components;
- Unique components;
- Components sorting;
- no_std support.

[image](https://github.com/image-rs/image) crate provides basic imaging processing functions and methods
for converting to and from image formats.

Check out [the release blog for 0.23](https://blog.image-rs.org/2020/02/07/release-0.23.0.html)!
It comes with improvements to error handling,
and the buffer and loading interfaces.

![Logo](../../assets/334998967aed19b9.png)


[Superluminal](https://superluminal.eu/) is a next-generation CPU sampling profiler
for C/C++ on Windows
that has [recently got an official Rust support](https://superluminal.eu/rust).

Embark have recently open-sourced [superluminal-perf-rs](https://github.com/embarkStudios/superluminal-perf-rs) -
a small crate that integrates with Superluminal profiler on Windows.

Example usage:

```
superluminal_perf::begin_event("my-event");
calc();
superluminal_perf::end_event();
superluminal_perf::begin_event("my-event2");
calc2();
superluminal_perf::end_event();
```


### Rust on [RG-300 Consoles](https://retrogame300.com/products/retro-game-300) [#](https://gamedev.rs#rust-on-rg-300-consoles)

[@alexpdp7 shared their experience](https://reddit.com/r/rust_gamedev/comments/fabgof/wrote_a_rust_program_that_demonstrates_graphics)
of writing an interactive application in Rust
for the retro [RG-300](https://retrogame300.com/products/retro-game-300) console.

The process is complex for a lot of reasons:


- Cross-compiling for MIPS is tough <…>
- Graphics is done through the Linux framebuffer <…>
- Sound uses old-style Linux OSS <…>
It’s a bit clunky, but it works! There are quite a few devices with very similar hardware this should work with. It should be possible to make simple games for such devices, which I find particularly motivating :)


You can find a working example that does graphics, sound and controls
with some explanations at [alexpdp7/retrofw2-rust](https://github.com/alexpdp7/retrofw2-rust).

[crow](https://crates.io/crates/crow) is a pixel perfect 2D rendering engine based on OpenGL.
It is designed to be easy to use while still allowing
for nearly everything one might want while using pixel art.

A showcase game is [being developed](https://github.com/lcnr/akari) with crow.

![Akari WIP screenshot](../../assets/0976253c6cf8444b.png)


### miniquad: [“Rust 2D Engine 2020 Roadmap”](https://patreon.com/posts/34230612) [#](https://gamedev.rs#miniquad-rust-2d-engine-2020-roadmap)

![mainloop async/await experiment in macroquad](../../assets/0090720e88c13248.png)

[miniquad](https://github.com/not-fl3/miniquad) by [@fedor_games](https://twitter.com/fedor_games) is a safe cross-platform rendering library
focused on portability and low-end platforms support.

This month:

- miniquad and related crates set up yearly goals:
[“Rust 2D Engine 2020 Roadmap”](https://patreon.com/posts/34230612); - A first try on the higher-level engine design:
[flappy bird.rs](https://github.com/not-fl3/macroquad/blob/126773535/examples/flappy_bird.rs); [miniquad was successfully built for Android](https://twitter.com/fedor_games/status/1223602773532520448).

[luminance](https://github.com/phaazon/luminance-rs) by [@phaazon](https://twitter.com/phaazon_) is a type-safe, type-level and stateless
graphics framework.

This month [luminance v0.39 got released](https://reddit.com/r/rust/comments/fbe3l0/luminance039).
Updates:

- Remove the concept of layering in textures. Textures’ layerings (i.e. either flat or arrayed) is now encoded directly in the dimension of the texture.
- Add support for texture arrays. They can now be passed constructed and passed as uniforms to shader programs.

[glium](https://github.com/glium/glium) is an elegant and safe OpenGL wrapper.

It’s no longer actively developed by its original author, but maintenance is continued by the surrounding community.

This month [glium v0.26 was released](https://github.com/glium/glium/blob/master/CHANGELOG.md#version-0260-2020-02-09):

- Updated glutin to
[version 0.23.0](https://github.com/rust-windowing/glutin/blob/master/CHANGELOG.md#version-0230-2020-02-06). - Removal of some unsound code that rustc warns about.
- Report the precise shader stage in which a shader failed compilation.

![wgpu-rs logo](../../assets/6e71fca18becfe13.png)


Here’re some of the [gfx](https://github.com/gfx-rs/gfx)/[wgpu](https://github.com/gfx-rs/wgpu-rs) ecosystem February updates:

-
Check out a new

[“Lear WGPU” tutorial](https://sotrh.github.io/learn-wgpu). -
[@kvark](https://github.com/kvark)gave a “Building WebGPU with Rust” talk at FOSDEM.[You can watch the recorded video here](https://fosdem.org/2020/schedule/event/rust_webgpu). -
[naga](https://github.com/gfx-rs/naga)is a new experimental shader translation library for the needs of gfx-rs project and WebGPU. It’s meant to provide a safe and performant way of converting to and from[SPIR-V](https://en.wikipedia.org/wiki/Standard_Portable_Intermediate_Representation). -
The abovementioned

[Oxidator](https://github.com/Ruddle/oxidator)RTS game is based on wgpu. -
[nbodysim](https://git.koesters.xyz/timo/nbodysim)is a realtime 3D N-Body-Simulation.![Simple demo with two bodies](../../assets/2292acae21724eca.gif)

-
[nannou](https://github.com/nannou-org/nannou)in an open-source creative-coding toolkit for Rust. This month its graphics backend[was transitioned to wgpu](https://github.com/nannou-org/nannou/pull/452). -
After

[the support for unstable WebIDL was added to wasm-bindgen](https://github.com/rustwasm/wasm-bindgen/pull/1997)the work on integrating web-sys into wgpu-rs has begun.

[tikan](https://gitlab.com/tendsinmende/tikan) by [@siebencorgie](https://twitter.com/siebencorgie) is a Rust/Vulkan based 3d engine that tries
to use high-resolution voxels to real-time ray-trace the final picture.

This month a [new video was released](https://youtu.be/98XdA3BpWZU)
to showcase new voxel renderer:

[Patchwork](https://github.com/RedSquirrelsNut/patchwork) is a convenient crate for drawing tiles from a tilesheet
using a ‘SpriteBatch’ with `ggez`

.
It is an update to [the Mosaic crate by @Repnop](https://github.com/repnop/mosaic),
which is no longer maintained.

![KAS widgets example](../../assets/11e1b1c6d7a381b4.png)


[KAS](https://github.com/kas-gui/kas), the tool**K**it **A**bstraction **S**ystem, is a general-purpose GUI toolkit.

0.3 is a decent sized release, focussing primarily on drawing, themes and layouts. Highlights include:

- a new FlatTheme,
- many small visual improvements,
- access to medium-level and low-level drawing APIs for custom widgets,
- window size limits,
- and switchable themes and colour schemes.

![Layout example](../../assets/ca919eebff625f7e.png)


[Pushrod](https://github.com/KenSuenobu/rust-pushrod) by [@KenSuenobu](https://github.com/KenSuenobu)
is a Cross Platform UI Widget Library for Rust that uses SDL2
and leans heavily towards the KISS principle.

This month [0.2.27 was released](https://reddit.com/r/rust/comments/f1fcya/pushrod_0227_sdl2based_gui).
Some of the updates:

- Improved documentation & examples;
- Tile Widget;
- Tab Bar Widget.

This month [Oxygengine](https://github.com/PsichiX/Oxygengine) got new version 0.7.0 with
[Visual Novel and Animation](https://reddit.com/r/rust_gamedev/comments/fd7kza/oxygengine_visual_novel_and_animation_modules_are)
modules that allows users to focus on making VN games easily,
with virtually no code needed to be written -
it is a groundbreaking start in developing a set of tools
for the professional game developers.

As few might notice, Oxygengine is starting to get more complex modules, there is a reason for that - this engine is made with one big goal in mind, which is: to became a tool used by professionals, giving easy way to make complex games easily, therefore the current milestone is about bringing a basic game editor with first game maker module along with blueprints-like visual scripting and animation tool - the most important tools for visual novel game designers!


![Oxygengine Visual Novel Teaser](../../assets/811a01eeee1af31d.gif)


You can find sources of the project that shows how to use these modules
in the [engine demo projects](https://github.com/PsichiX/Oxygengine/tree/master/demos/visual-novel-testbed).

Another thing that was shipped in last milestone was a module that allows to make and run your game logic designed in Blueprint-like visual scripting. Next milestone is focused on delivering a base for professional modular game editor that will allow users to easily create a complex and animated Visual Novel games using Visual Scripting - game makers for another genres are currently in planning stage.

![Different font makes the log easier to read](../../assets/529440e1f3d97ab3.jpg)


[The Roguelike Tutorial](http://bfnightly.bracketproductions.com/rustbook) by [@blackfuture](https://patreon.com/blackfuture)
includes more than 70 chapters now and continues to grow!

Some of February’s updates:

- C71: adds easy to use, colored, logging and an achievement counter system to track your progress through the dungeon.
- C72: 2nd layer (VGA) for the log, refactors for batched draw calls.
- C73: Systems use Specs dispatch on native, and single-thread on WASM.

[bracket-lib](https://github.com/thebracket/rltk_rs) (previously [rltk_rs](https://github.com/thebracket/rltk_rs)) by [@blackfuture](https://patreon.com/blackfuture)
is a Rust implementation of [C++ Roguelike Toolkit](https://github.com/thebracket/rltk).

This month the project was renamed and split into many crates:

This is RLTK, renamed because it is increasingly finding usage outside of just Roguelikes. It’s also been divided into a number of crates, to make it easy to pick-and-choose the features you need.


`rltk`

crate wraps bracket-lib and re-exports in the`rltk::`

and`rltk::prelude`

namespace. This preserves compatibility with all existing RLTK projects.`bracket-algorithm`

-traits exposes the traits required for the various algorithm systems in other crates.`bracket-color`

is my RGB/HSV color management system.`bracket-geometry`

exposes various geometric primitives and helpers. Supports other crates.`bracket-noise`

is a port of Auburn’s FastNoise to Rust.`bracket-pathfinding`

provides a high-performance A* (A-Star) pathing system, as well as Dijkstra maps.`bracket-random`

is a dice-oriented random number generator, including parsing of RPG-style dice strings such as 3d6+12.

![Neovide Animated Cursor Example](../../assets/d3a5ca4fb1f199ae.gif)


[Neovide](https://github.com/Kethku/neovide) is a frontend for neovim that brings a lot of visual niceties.
It uses vulkan and skia for rendering.

## Popular Workgroup Issues in GitHub [#](https://gamedev.rs#popular-workgroup-issues-in-github)

## Meeting Minutes [#](https://gamedev.rs#meeting-minutes)

[See all meeting issues](https://github.com/rust-gamedev/wg/issues?q=label%3Ameeting) including full text notes
or [join the next meeting](https://github.com/rust-gamedev/wg#join-the-fun).

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs));[winit’s “Good first issue” and “help wanted” issues](https://github.com/rust-windowing/winit/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+label%3A%22status%3A+help+wanted%22+label%3A%22Good+first+issue%22);[gfx-rs’s “contributor-friendly” issues](https://github.com/gfx-rs/gfx/issues?q=is%3Aissue+is%3Aopen+label%3Acontributor-friendly);[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22);[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22);[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A);[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner);[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22);[A/B Street’s “good first issue” issues](https://github.com/dabreegster/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22);[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue);

## Bonus [#](https://gamedev.rs#bonus)

Just an interesting Rust gamedev link from the past. :)

![A screenshot of the beginning of the game](../../assets/ee38f65723ab87d5.png)


[“It’s Not Cool”](https://ratys.itch.io/its-not-cool) is a [LD42](https://en.wikipedia.org/wiki/Ludum_Dare) turn-based strategy game
by [@Ratysz](https://github.com/Ratysz).
It’s based on the GGEZ game engine.

Assume role of the mayor of a small coastal city, caught in the middle of hilariously rapid global warming spurt.

Build a freezer for the polar bears!


*Discussions:
/r/rust_gamedev,
/r/rust*

That’s all news for today, thanks for reading!

Subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!