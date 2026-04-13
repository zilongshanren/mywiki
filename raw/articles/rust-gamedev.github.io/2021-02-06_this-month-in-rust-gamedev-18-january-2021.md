---
title: 'This Month in Rust GameDev #18 - January 2021'
url: https://gamedev.rs/news/018/
author: Rust GameDev WG
published: '2021-02-06'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 18th issue of the Rust GameDev Workgroup’s
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

[Rust GameDev Podcast](https://gamedev.rs/news/018/#rust-gamedev-podcast-5)[Rust GameDev Meetup](https://gamedev.rs/news/018/#rust-gamedev-meetup)[Game Updates](https://gamedev.rs/news/018/#game-updates)[Learning Material Updates](https://gamedev.rs/news/018/#learning-material-updates)[Engine Updates](https://gamedev.rs/news/018/#engine-updates)[Library & Tooling Updates](https://gamedev.rs/news/018/#library-tooling-updates)[Popular Workgroup Issues in GitHub](https://gamedev.rs/news/018/#popular-workgroup-issues-in-github)[Requests for Contribution](https://gamedev.rs/news/018/#requests-for-contribution)

![text logo](../../assets/af29d83de55362d9.jpeg)


[The 5th podcast episode](https://rustgamedev.com/episodes/interview-with-alex-ene) is an interview with
[Alex Ene](https://twitter.com/_AlexEne_) creator of an upcoming dwarven simulation
game, [Dwarf World](https://dwarf.world).

In this week’s episode, Richard and Forest chat to Alex Ene, creator of the dwarven simulation game, Dwarf World. We cover writing custom engines, unit testing, build systems, and picking the right frameworks for your game.


Listen and subscribe from the following platforms:
[Rust GameDev Podcast (simplecast)](https://rustgamedev.com/),
[Apple Podcasts](https://podcasts.apple.com/gb/podcast/rust-game-dev/id1526304768),
[Spotify](https://open.spotify.com/show/7HRfGnTcXkLkQd9fxJbDGj),
[RSS Feed](https://feeds.simplecast.com/C6NQglnL),
[Google Podcasts](https://podcasts.google.com/feed/aHR0cHM6Ly9mZWVkcy5zaW1wbGVjYXN0LmNvbS9DNk5RZ2xuTA).

## Rust GameDev Meetup [#](https://gamedev.rs#rust-gamedev-meetup)

![Gamedev meetup poster](../../assets/40e7b649d82fa678.png)


The first iteration of the Rust Gamedev Meetup happened in January. It was an
opportunity for developers to show of what Rust projects they’ve been working on
in the game ecosystem. Developers showed off physics engines, custom build
tools, renderers, and more. You can watch the recording of the meetup [here on
Youtube](https://www.youtube.com/watch?v=2L3w3UiEzAk).

The next meetup will take place 13th of February
at 16:00 GMT on the [Rust Gamedev Discord server](https://discord.gg/yNtPTb2), and can
also be [streamed on Twitch](https://www.twitch.tv/rustgamedev).

## Game Updates [#](https://gamedev.rs#game-updates)

![teki preview](../../assets/a51f7da06aec0549.gif)


[Teki](https://github.com/o2sh/teki) is a free and open-source fangame of the [Tōhō](https://en.wikipedia.org/wiki/Touhou_Project) series
using [SDL2](https://github.com/Rust-SDL2/rust-sdl2) and [Legion](https://crates.io/crates/legion) for ECS. Thanks to WebAssembly - via [wasm-pack](https://rustwasm.github.io/wasm-pack)
-, teki can be played [online](https://o2sh.github.io/teki).

It is aimed to be a shoot ’em up game with “lots of bullets” a.k.a danmaku 弾幕 - literally “barrage” or “bullet curtain” in japanese.

The project is still at a “very” early stage of development (Dec. 2020).

![Fishgame gameplay](../../assets/fb2bd43fe8426087.gif)

[Fishgame](https://github.com/heroiclabs/fishgame-macroquad) is an online multiplayer game, created in a
collaboration between [Nakama](https://heroiclabs.com/), an open-source scalable game
server, and the [Macroquad](https://github.com/not-fl3/macroquad/) game engine.

The game is going to showcase nakama multiplayer capabilities for the rust language world.

This month the game got a public, multiplayer HTML5 build. [Play it online!](https://fedorgames.itch.io/fish-game?secret=UAVcggHn332a)



[gameplay video](https://www.youtube.com/watch?v=JCH2U5JOMlU)on YouTube

[Station Iapetus](https://github.com/mrDIMAS/StationIapetus) by [@mrDIMAS](https://github.com/mrDIMAS)
is a 3rd person shooter on the space prison Iapetus near the Saturn.

The game is based on the [rg3d](https://github.com/mrDIMAS/rg3d) game engine and is meant to be the proof that
rg3d is ready for commercial production. The game is a commercial project
which will be released in Steam.

![SeniorSKY](../../assets/42f10b8502760351.png)

[SeniorSKY](https://youtube.com/playlist?list=PLMmaJuk-D7iaObZyhyvc83tNwpx3ghzkY)
is a flight simulator which uses Vulkan API, developed by [@pmathia0](https://twitter.com/pmathia0).
As an aerospace engineering student, Peter has always been interested how
a flight simulator works under the hood.
The development of SeniorSKY started as a hobby project during university
studies.

SeniorSKY uses real-world elevation data with 1 arc second precision and can render the whole globe in real dimensions. During the flight, the terrain tiles are loaded dynamically based on real GPS coordinates of airplane, with a decreasing level of detail further from the camera. This is achieved using a combination of a terrain-quad-tree and GPU tessellation.

SeniorSKY also implements basic rendering of sky, atmosphere and fog.

To be able to simulate a flight, the application temporarily integrates 3rd party flight dynamics engine called JSBSim. Meanwhile, development of own, custom flight dynamics is already in progress.

![oicana game play](../../assets/78cfa28d6d09e8cc.png)

[Oicana](https://github.com/NiklasEi/oicana) is a tower defense game with puzzle aspects submitted to Mini
jam 71 [on itch](https://niklme.itch.io/oicana) by [M1nd0fRafa3l](https://itch.io/profile/m1nd0frafa3l) and
[@nikl_me](https://twitter.com/nikl_me). The game was written using the Rust game engine
[Bevy](https://bevyengine.org/).

Colorless puzzle pieces try to reach your base. Your towers have to shoot at the pieces to uncover their color. After defeating a piece, it will try to run away and you should catch it to upgrade your towers or build new ones.

Following the game jam the tower upgrades where improved and game audio was
changed to use [Kira](https://github.com/tesselode/kira) via an
[experimental bevy plugin](https://github.com/NiklasEi/bevy_kira_audio).

[
](https://katharostech.com/post/bounty-bros-prototype-game#video)
![Bounty Bros. Video](../../assets/546f98b47621db1c.jpg)


[Bounty Bros.](https://katharostech.com/post/bounty-bros-prototype-game)is a prototype dungeon crawler game in the spirit of “Legend of Zelda: Link to the Past”. The game is being developed by

[Katharos Technology](https://katharostech.com)as a playground for a future commercial game, along with a custom 2D engine built on top of

[Bevy](https://bevyengine.org/).

The engine, which is unnamed so far, will be Open Sourced soon and will be
designed to make it very easy to make games with a similar gameplay and style,
primarily by simply writing YAML configuration files and integrating with
[LDtk](https://ldtk.io).

### Flesh [#](https://gamedev.rs#flesh)

![flesh preview](../../assets/ce672982a9e25601.gif)

Flesh by [@im_oab](https://twitter.com/im_oab) is a 2D-horizontal shmup game with hand-drawn animation
and implement using tetra. It still in the development stage but have
a release date set in October 2021.

This game takes place inside the flesh of mysterious organisms that players will fight through multiple levels to get out.

![A/B Street in Cambridge](../../assets/d7499805e2d4e0a6.gif)


[A/B Street](https://github.com/a-b-street/abstreet) by [@dabreegster](https://twitter.com/CarlinoDustin) is a traffic simulation game exploring how small
changes to roads affect cyclists, transit users, pedestrians, and drivers, with
suppot for any city with OpenStreetMap coverage.

In January, [Bruce](https://github.com/BruceBrown) implemented variable traffic signal timing, dedicated
cycle-paths and pedestrian plazas were imported, [Michael](https://github.com/michaelkirk) and [Yuwen](https://www.yuwen-li.com/)
overhauled the UI buttons, and we finished day/night toggling. Loading on the
[web](http://abstreet.s3-website.us-east-2.amazonaws.com/dev/game/?--dev&cambridge/maps/great_kneighton.bin) and starting scenarios is also much faster!

### Paddlers [#](https://gamedev.rs#paddlers)

![A happy duck and sign showing: Paddlers version 0.2.0](../../assets/b277768e2c1c7a62.jpeg)


[Paddlers](https://paddlers.ch) ([GitHub](https://github.com/jakmeier/paddlers-browser-game), [Online Demo](https://demo.paddlers.ch)) by [@jakmeier](https://github.com/jakmeier)
is an MMORTS for the browser, developed as an experimental hobby project.

This month, version 0.2.0 has been released, which removes all dependencies to
[Stdweb](https://github.com/koute/stdweb) and [Quicksilver](https://github.com/ryanisaacg/quicksilver) while keeping the game itself virtually unchanged.
In the process, a part of the code of Paddlers moved to [Paddle](https://github.com/jakmeier/paddle), a new
framework for 2D browser games running on desktop and mobile phones.
More details on that are available [here](https://www.jakobmeier.ch/blogging/Paddlers_5.html).

Many new features for Paddle and Paddlers are already in the pipeline, so stay tuned for more exciting updates in the next monthly newsletter!

![Some players hanging out next to the bank Vault in Belmart](../../assets/a216d08aacf43349.jpg)

[Antorum](https://ratwizard.dev/dev-log/antorum) is a micro-multiplayer online role-playing game by [@dooskington](https://twitter.com/dooskington).
The game server is written in Rust, and the official client is being developed
in Unity.

Banking was implemented this month! Players can now store their items and wealth in a safe place. Additionally, the concept of “item combinations” was implemented, bringing more interesting crafting scenarios into the game.

### Harvest Hero [#](https://gamedev.rs#harvest-hero)

![Harvest Hero Screenshot](../../assets/ae280e3b4fa39a2d.png)


Harvest Hero ([Discord](https://discord.gg/3NU5tYwRxJ)) by [@bombfuse_dev](https://twitter.com/bombfuse_dev)
is an arcade/roguelike game built on top of [Emerald](https://github.com/Bombfuse/emerald).
This month’s updates include:

- Art update thanks to
[@ddooby](https://twitter.com/ddoobysnax). - Map templates for better designed maps.
- A shop system for buying abilities/enchantments.
- SFX were added to bring some more life to the game.

![Dwarf World](../../assets/79c810cc32902be4.gif)


[Dwarf World](https://dwarf.world) ([Discord](https://discord.gg/vsRCxnY))
by [Alex Ene](https://twitter.com/_AlexEne_) has added a couple of updates and improvements:

- Dynamic lights and light propagation so deeper caves are darker.
- An in-game feedback button that people can use to report bugs or just give general feedback.
- All random numbers are from seeded generators so it makes bugs easier to reproduce.
- A big chunk of a replay system is finished. This should help a lot with reproducing issues. Plus, it’s really fun to watch.
- Bug fixes and performance improvements, mostly related to rendering and culling systems.

If you’re interested in keeping a closer eye on the project and monitor
it’s progress,
you can join the game’s [discord channel](https://discord.gg/vsRCxnY).
That’s where the pre-alpha builds will drop there once they are
ready to be seen by a wider audience.

### Stellary 2 [#](https://gamedev.rs#stellary-2)

![Stellary 2 Banner](../../assets/c9fddd6bd019f374.jpg)


Stellary 2 by [@CoffeJunkStudio](https://twitter.com/CoffeJunkStudio) is a 3D
real-time artillery game in which the player has to destroy all enemy planets in
order to defend his own from extinction.

Based on the [SimJam 2020](https://itch.io/jam/dogpit-sim-jam) game
“[Stellary](https://coffejunkstudio.itch.io/stellary)”, the studio is now
working on this sequel with their self-developed “Sphere Engine”. It will
feature an underlying physically based gravity simulation, powering the space
battles in different solar systems. You can find regular updates on
[Twitter](https://twitter.com/CoffeJunkStudio).

By the way: “Stellary 2” is just a working title, feel free to drop them a PM on Twitter if you have a flash of inspiration!



![Homing Missiles](../../assets/8c98016151782d87.gif)

A real name was finally chosen for space_shooter_rs! [Theta Wave](https://github.com/amethyst/theta-wave) is a space
shooter game by developers [@micah_tigley](https://twitter.com/micah_tigley) and [@carlosupina](https://twitter.com/carlosupina). It is one of
the showcase games for the [Amethyst Engine](https://amethyst.rs/). In the past month, they have
been focused on improving the motion system for the game. The improvements
allowed them to begin adding more interesting behavior for moving entities.
Missiles were changed to home to the player.

![Way of Rhea screenshot](../../assets/a2199679916b5215.jpg)


Way of Rhea is a picturesque puzzle game that lets you correct your mistakes. Change your color, teleport past the colored gates, master the color powered circuits, and befriend the color changing crabs-but don’t let them out!

This month’s major updates include:

- Autosave support.
- Steam cloud support.
- A free demo was released as part of Boston FIG (no longer available).
- In game audio options.
- A new level featuring a new puzzle mechanic.
- An
[updated trailer](https://www.youtube.com/watch?v=PRifdHcaswc).

![Veloren Snow](../../assets/72f4da7232866fa2.gif)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In January, lots of work was done on new models that make the world feel more alive. Work was done on economic simulation, and many of the blog posts highlight this progress. This includes trading between sites, and professions. Skill trees were completed, and are now in the game.

Large changes are being implemented to the CI system to reduce build times. Work has been ongoing on improving the Veloren wiki, with many contributors adding to it. In February, a meeting will be held to discuss the 0.9 release, with does not yet have a release date.

January’s full weekly devlogs: “This Week In Veloren…”:
[#101](https://veloren.net/devblog-101),
[#102](https://veloren.net/devblog-102),
[#103](https://veloren.net/devblog-103),
[#104](https://veloren.net/devblog-104).

![Custom art assets for Shotcaller](../../assets/d21cf631e5fffccf.png)

[Shotcaller](https://github.com/amethyst/shotcaller) ([Discord](https://discord.gg/qvJyTYM)) is a minimalistic MOBA
that focuses strictly on macro-play with few actions-per-minute,
leaving only room for grand strategy decisions.
The game is made with [bracket-lib](https://github.com/thebracket/bracket-lib), a [custom game engine](https://github.com/jojolepro/minigene)
and [Plank ECS](https://www.jojolepro.com/blog/2021-01-13_planks_ecs).

Recent updates include:

[Version v0.4.0 was released](https://reddit.com/r/rust_gamedev/comments/kveih9/shotcaller_mobagame_v040).- First batch of custom art assets completed; will be implemented in the month to come.
- New leaders:
[Alchemist](https://github.com/amethyst/shotcaller/pull/29),[Axe](https://github.com/amethyst/shotcaller/pull/30),[Rubick](https://github.com/amethyst/shotcaller/pull/34),[Centaur](https://github.com/amethyst/shotcaller/pull/36),[Bristleback](https://github.com/amethyst/shotcaller/pull/40),[Shadow Fiend](https://github.com/amethyst/shotcaller/pull/35). [Gold system](https://github.com/amethyst/shotcaller/pull/31).[Headless option](https://github.com/amethyst/shotcaller/pull/44)(in preparation for AI/ML experimenting).[Fog of War](https://github.com/amethyst/shotcaller/pull/41).[Mouse support](https://github.com/amethyst/shotcaller/pull/46).



![Some generic gameplay demo](../../assets/9968f8e9b27d1f96.gif)

[watch a footage with sound](https://twitter.com/ozkriff/status/1341052260885942272)🔊

[Zemeroth](https://github.com/ozkriff/zemeroth) by [@ozkriff](https://twitter.com/ozkriff) is a minimalistic 2D turn-based tactical game.
Some of the recent updates:

- The game
[was migrated from good-web-game to macroquad](https://twitter.com/ozkriff/status/1332031459985682436)and converted to explicit async assets loading. - Proper
[sound effects & music were added](https://twitter.com/ozkriff/status/1341052260885942272)using the[quad-snd](https://github.com/not-fl3/quad-snd)library ([more details](https://twitter.com/ozkriff/status/1346422661187035136)).

The final preparations for v0.7 are wrapping up!

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

[“Hands-on Rust: Effective Learning through 2D Game Development and Play”](https://pragprog.com/titles/hwrust/hands-on-rust)
is a book by [Herbert Wolverson](https://bracketproductions.com)
(the author of [bracket-lib](https://github.com/thebracket/bracket-lib) and [the Rust Roguelike Tutorial](https://bfnightly.bracketproductions.com/rustbook)):
make fun games as you learn Rust through a series of hands-on gamedev tutorials
and real-world use of core language skills.

Recent [beta releases](https://pragprog.com/support/#beta-books) added the following chapters:

- #10: Fields of View;
- #11: More Interesting Dungeons;
- #12: Map Themes;
- #13: Inventory and Power Ups;
- #14: Deeper Dungeons;
- #15: Combat Systems and Loot;
- #16: Final Steps and Finishing Touches.

[Triangle from Scratch](https://rust-tutorials.github.io/triangle-from-scratch) ([source code](https://github.com/rust-tutorials/triangle-from-scratch))
is a WIP tutorial series by [@Lokathor](https://twitter.com/Lokathor) about drawing a triangle
without using any outside crates.
Two extensive chapters were added this month:

![Windows taskbar with Way of Rhea icon on the right](../../assets/032b208875c3e9fc.png)

[Way of Rhea](https://www.anthropicstudios.com/way-of-rhea)’s icon in the taskbar

[Anthropic Studios](https://anthropicstudios.com) has [shared an article](https://anthropicstudios.com/2021/01/05/setting-a-rust-windows-exe-icon) about
manually using `rc.exe`

and embedding the resulting `.res`

into your app
to set your game’s system icon on Windows.

*Discussions:
/r/rust_gamedev*

![tic-tac-tide img](../../assets/c2e142e910541ebe.png)


An exploration post on how to use WebSockets with [Tide](https://github.com/http-rs/tide) framework by creating
a simple tic-tac-toc game. It’s focused on how to implement `ws`

to enable all
time of real time apps (and games) with Rust and Tide.
You can also play [tic-tac-tide](https://tic-tac-tide.labs.javierviola.com/) online.

## Engine Updates [#](https://gamedev.rs#engine-updates)

[ggez](https://crates.io/crates/ggez) is a lightweight cross-platform game framework for making 2D
games with minimum friction.

The zero’th release candidate for version 0.6.0 has been released and
there has been no particularly horrific outcry of people’s games
exploding. A first release candidate with a pile of medium-sized bug
fixes should be coming in early February, hopefully soon followed by a
full release. [Feedback is welcome](https://github.com/ggez/ggez/milestone/6)!

Special thanks to the contributors who helped hunt bugs and organize PR’s to get this version out the door: @PSteinhaus, @Manghi, @AaronM04, @Systemcluster, and @Andy-Python-Programmer!

[Tetra](https://github.com/17cupsofcoffee/tetra) is a simple 2D game framework, inspired by XNA and Raylib. This month,
versions 0.5.7 and 0.5.8 were released, with various changes:

- Basic multisampled anti-aliasing support (with further improvements to come).
- Functions for generating primitive shape meshes.
- A more flexible
`Rectangle`

type. - Lots of bug fixes and docs improvements.

For full details, see the [changelog](https://github.com/17cupsofcoffee/tetra/blob/main/CHANGELOG.md).

Additionally, work on [version 0.6](https://github.com/17cupsofcoffee/tetra/blob/0.6/CHANGELOG.md) has begun, with a release
planned for some time in February!

![Fox model and egui controls for camera, light, etc](../../assets/1bdaf7520762fd94.png)


[Dotrix](https://dotrix.rs) ([Discord](https://discord.com/invite/DrzwBysNRd), [Twitter](https://twitter.com/lowenware)) got an official
[egui](https://github.com/emilk/egui) support and a new example demonstrating various
engine features and controls. The next big milestone for [Dotrix](https://dotrix.rs) developers is
a terrain engine and editor, also made with [egui](https://github.com/emilk/egui). Some progress you can
already find on [YouTube](https://youtube.com/channel/UCdriNXRizbBFQhqZefaw44A).

![rusty-editor screenshot](../../assets/26abbc33a2e7de09.jpg)

[rusty-editor](https://github.com/mrDIMAS/rusty-editor)which is a native scene editor for the rg3d game engine.

[rg3d](https://github.com/mrDIMAS/rg3d) ([Discord](https://discord.gg/xENF5Uh), [Twitter](https://twitter.com/DmitryNStepanov))
is a game engine that aims to be easy to use and provide large set
of out-of-box features. Some of the recent updates:

- Animation blending state machines were improved.
- It’s now possible to copy nodes in-place.
- The number of draw calls for UI was reduced by 70%.
- Fixed clipping issues and text measurement in the UI.
- Opacity for UI widgets was added.
- Layout of Scroll- and Wrap- panels was fixed.
- Light scatter issues for spot lights were fixed.
- Support for transparent meshes.
- Migration to rapier 0.5.
- Animation signal handling is fixed when animation playing in reverse.
- Animation tracks now are able to filter position/scale/rotation.
- Sprite rendering fixes.
- Improved copy/paste in rusty-editor.
- Lots of other small fixes and improvements.

## Library & Tooling Updates [#](https://gamedev.rs#library-tooling-updates)

[rkyv](https://github.com/djkoloski/rkyv) is a zero-copy deserialization framework for Rust. It’s similar to
FlatBuffers and Cap’n Proto and can be used for data storage and messaging.

Version 0.3 was released this month and brought some highly-requested features:

- A new hashmap implementation using perfect hashing to decrease memory usage and fix portability issues.
- The
`Unarchive`

trait to enable more traditional data deserialization for archived types. - Improved validation performance.
- Better error messages and API ergonomics.
- A
[book](https://djkoloski.github.io/rkyv)with more narrative documentation on architecture and internals. - More tests and realistic benchmarks against other popular serialization frameworks.

The next update will be [v0.4](https://github.com/djkoloski/rkyv/milestone/5) and is on the way soon with a release
date around mid-February.

[Mun](https://mun-lang.org) is a scripting language for gamedev focused on quick iteration times
that is written in Rust.

Revitalized from the holiday break, the Mun core team got cracking; those
[January updates](https://mun-lang.org/blog/2021/02/05/this-month-january) include:

- a ton of new language server features;
- the ability to emit IR;
- better documentation;
- bug fixes and other improvements.

![logo](../../assets/54d07143fd060634.png)


[GameLisp](https://gamelisp.rs) ([source code](https://github.com/fleabitdev/glsp),
[playground](https://gamelisp.rs/playground)) by [@fleabitdev](https://twitter.com/fleabitdev)
is a scripting language designed specifically for Rust game development.

This month, version 0.2.0 has been released. Some of the updates:

- Any
`'static`

Rust type, including types defined by external crates, can now be moved onto the garbage-collected heap and manipulated by GameLisp scripts. - Rust data on the garbage-collected heap can now contain pointers to other
garbage-collected data, by implementing a
`trace()`

method. - Version 0.1 could only bind non-capturing Rust closures, but closures
which capture
`'static`

data are now fully supported. - Rust function pointers can now be passed directly to GameLisp,
rather than using the
`rfn!`

macro. The clunky`lib!`

and`rdata!`

macros have also been removed. - Updated documentation starting from the
[“Rust Bindings”](https://gamelisp.rs/reference/rust-bindings.html)chapter.

For full details, see the [changelog](https://github.com/fleabitdev/glsp/blob/master/CHANGELOG.md).

*Discussions:
/r/rust*

[LDtk-rs](https://github.com/katharostech/ldtk-rs) is a Rust crate for reading the [LDtk](https://ldtk.io) map file format. The bindings
to the LDtk format are 100% automatically generated from the LDtk JSON Schema,
with the option to download the latest JSON Schema at build time for automatic
updates.

![LDtk Map Running in Bevy](../../assets/42d0422fa2c37956.jpg)

[“Cavernas”](https://adamatomic.itch.io/cavernas)by Adam Saltsman

[bevy_ldtk](https://github.com/katharostech/bevy_ldtk) is a Bevy plugin for loading [LDtk](https://ldtk.io) tilemaps.

It features:

- An efficient renderer that only uses 4 vertices per map layer.
- Hot reloading through the Bevy asset server integration.
- Heavily commented code to help others who want to see how to make their own tilemap renderers.

[kira](https://github.com/tesselode/kira) by [@tesselode](https://twitter.com/tesselode) is a game audio library tailored to composers and other
people who need expressive audio.

v0.4.0 was released with a new wasm32 support, a new handle-based API, improved error handling, and serde support for sequences, arrangements, and most config structs.

[Dimforge](https://dimforge.com/) creates open-source Rust crates for numerical simulation.
Some of the January updates:

[Parry](https://parry.rs)was announced, the successor of ncollide for 2D and 3D collision-detection in Rust.- The new version of
[Rapier](https://rapier.rs)brings many new features, including the ability to use custom shapes, as well as convex polygons/polyhedrons for 2D and 3D respectively.

You can read about all of the changes in the January edition of
[“This Month In Dimforge”](https://dimforge.com/blog/2021/01/29/this-month-in-dimforge).

![Spaceship](../../assets/8ee77522f4e1775d.jpg)


The community managed to squeeze the v0.7 releases out
at the end of the month. See the detailed notes on [gfx blog post](https://gfx-rs.github.io/2021/02/02/release-0.7.html).

The highlight of the show is about shaders. Most of wgpu-rs shaders are
now written in [WGSL](https://gpuweb.github.io/gpuweb/wgsl.html),
and gfx-rs community is inviting Rust game/graphics developers to evaluate if
[naga](https://github.com/gfx-rs/naga) could fulfill their shader translation needs in the future.

![imgui drag drop example](../../assets/4f23d2b9944545d7.gif)

[imgui-rs](https://github.com/imgui-rs/imgui-rs) is the Rust bindings for the ubiquitous immediate mode GUI library,
Dear ImGui.
Under new maintenance, [version 0.7](https://github.com/imgui-rs/imgui-rs/releases/tag/v0.7.0) has been released, which features a new
API for raw draw calls, support for ergonomic Drag and Drop, and tons of improvements.
Notably, many functions were made `inline`

and/or `const`

, including the `im_str!`

macro.

![egui widget gallery](../../assets/e3211fdb95cdd4ef.gif)

[egui](https://github.com/emilk/egui) is a simple, fast, and highly portable immediate mode GUI library.

This month [version 0.8](https://github.com/emilk/egui/blob/master/CHANGELOG.md#080---2021-01-17---grid-layout--new-visual-style) of egui was released with a new grid layout,
new look, and many smaller fixes and improvements.
You can try out egui in the [online demo](https://emilk.github.io/egui).

![bevy_egui screenshot](../../assets/6b4bacb24bb892c4.png)


[bevy_egui](https://github.com/mvlabat/bevy_egui) provides a [Egui](https://github.com/emilk/egui) integration
for the [Bevy](https://github.com/bevyengine/bevy) game engine.
It supports [bevy_webgl2](https://github.com/mrk-its/bevy_webgl2) and implements the full set of Egui features
(such as clipboard and opening URLs).

Try out the [online demo](https://mvlabat.github.io/bevy_egui_web_showcase/index.html).

![cli + web version](../../assets/87a97eb2baf14e6c.png)

[chess-engine](https://github.com/adam-mcdaniel/chess-engine) by [@adam-mcdaniel](https://github.com/adam-mcdaniel) is a pure Rust, no-std, dependency-free
chess engine built to run anywhere.

I love chess a lot. It’s definitely one of my favorite games ever. However, I’ve always been disappointed when trying to write programs that play chess digitally (particularly in a compiled language). Although several amazing engines exist, it’s near impossible to find a neat library for chess-related-programming that runs on everything.


[chess-engine]is a solution to my problem. If you want a chess engine that runs on embedded devices, the terminal,[the desktop (with a gui)], and[the web], this is probably your best bet.

*Discussions:
/r/rust*

![plaintext tables](../../assets/567d226340971d62.png)

[dcli](https://github.com/mikechambers/dcli) by [Mike Chambers](https://gamedev.rs/news/018/www.mikechambers.com) is a library and a collection
of utilities&apps that provide a command line interface (CLI) for viewing
player stats and data from Destiny 2, using the [Destiny 2 API](https://github.com/Bungie-net/api):

- dclis - retrieves primary platform and membership ids for Destiny 2 players.
- dclim - manages and syncs the remote Destiny 2 API manifest database.
- dclias - downloads and syncs Destiny 2 Crucible activity history into a local sqlite3 database file.
- dclic - retrieves character ids for the specified member.
- dclims - searches the Destiny 2 manifest by hash ids (from API calls).
- dclitime - generates date / time stamps for Destiny 2 weekly event moments.
- dclia - displays information on player’s current activity within Destiny 2.
- dcliah - displays Destiny 2 activity history and stats.
- dcliad - displays Destiny 2 Crucible activity / match details.

### Rust Support in [Shader Playground](http://shader-playground.timjones.io) [#](https://gamedev.rs#rust-support-in-shader-playground)

![source code in rust, compiler options, and spircv-coross output](../../assets/c0dba3b22770adb5.jpeg)


[Shader Playground](http://shader-playground.timjones.io) ([source code](https://github.com/tgjones/shader-playground))
by [@tgjones](https://github.com/tgjones) now allows you to try out writing shaders in Rust
(using [rust-gpu](https://github.com/EmbarkStudios/rust-gpu)) without downloading or building anything.

## Popular Workgroup Issues in GitHub [#](https://gamedev.rs#popular-workgroup-issues-in-github)

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[gfx-rs’s “contributor-friendly” issues](https://github.com/gfx-rs/gfx/issues?q=is%3Aissue+is%3Aopen+label%3Acontributor-friendly).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[A/B Street’s “good first issue” issues](https://github.com/a-b-street/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/good%20first%20issue).

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!