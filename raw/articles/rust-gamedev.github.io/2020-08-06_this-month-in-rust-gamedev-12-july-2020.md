---
title: 'This Month in Rust GameDev #12 - July 2020'
url: https://gamedev.rs/news/012/
author: Rust GameDev WG
published: '2020-08-06'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the twelfth issue of the Rust GameDev Workgroup’s
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

[Game Updates](https://gamedev.rs/news/012/#game-updates)[Learning Material Updates](https://gamedev.rs/news/012/#learning-material-updates)[Library & Tooling Updates](https://gamedev.rs/news/012/#library-tooling-updates)[Meeting Minutes](https://gamedev.rs/news/012/#meeting-minutes)[Requests for Contribution](https://gamedev.rs/news/012/#requests-for-contribution)[Jobs](https://gamedev.rs/news/012/#jobs)[Bonus](https://gamedev.rs/news/012/#bonus)

## Game Updates [#](https://gamedev.rs#game-updates)



![Youtube preview: mountains & spheres](../../assets/2b25309d359145e9.jpeg)

[watch the demo on Youtube](https://youtube.com/watch?v=SIkkYRQ07tU).

Jani Peltonen has recently released a [4K intro](https://github.com/janiorca/sphere_dance)
which is completely written in Rust and GLSL
and published an article [“Writing a winning 4K intro in Rust”](https://www.codeslow.com/2020/07/writing-winning-4k-intro-in-rust.html):

A 4K intro is a demo where the entire program (including any data) has to be 4096 bytes or less so it is important that the code is as space efficient as possible. Rust has a bit of a reputation for creating bloated executables so I wanted to find out if is possible to create very space efficient code with it.


*Discussions:
/r/rust,
hacker news*

![game logo + OS logos](../../assets/05da9d7fc704beb4.jpg)


One year ago [Alex Butler](https://twitter.com/bigabgames) released the “[Robo Instructus](https://www.roboinstruct.us)” puzzle game
on [Steam](https://store.steampowered.com/app/1032170/Robo_Instructus) & [itch.io](https://bigabgames.itch.io/robo-instructus).

This month Alex released a devlog post [“Robo Instructus: 1 Year Later”](https://blog.roboinstruct.us/2020/07/16/1-year-later.html)
about how well the game did after the release:
sales by platform/country/OS, player feedback & reviews, etc.

People mostly don’t publish sales figures, I guess it makes more business sense to be vague. But maybe these will be helpful or interesting in some way.


Also, Alex continues to maintain and polish the game: [1.29 version](https://store.steampowered.com/newshub/app/1032170/view/4355495589078346745)
brings auto-scrolling improvements, better lang parsing,
bugfixes, and dependency updates.

*Discussions:
/r/rust*



![Golf Club in Crate Before Attack](../../assets/edfa3e78cc6b9105.gif)

[Crate Before Attack](https://cratebeforeattack.com) by [koalefant (@CrateAttack)](https://twitter.com/CrateAttack)
is a skill-based grappling hook multiplayer game where frogs combat their friends
while navigating the landscape with their sticky tongues.

A summary of July changes:

- Gameplay: added a new melee weapon:
[the Golf Club](https://youtu.be/UYxZQh68T6E). - Maps: added new map
[Ruins](https://youtu.be/D63xy7sXStk)by[Kesha Astafyev](https://www.behance.net/spoon_tar) - Animation: added eye tracking, frogs will track the closest danger with their eyes such as a projectile or a pet.
- Lobby: it is now possible to observe a match after it was started, added chat, user list with country flags, match details, and map previews.
- Localization: the game comes in three languages now: English, Spanish, Russian.
- Numerous bugfixes and tweaks.

Here is [a Playable Browser build](https://cratebeforeattack.com/play).
More details are on [the YouTube channel](https://youtube.com/channel/UC_xMilPTLuuE5iLs1Ml9zow)
and in [July Update DevLog-entry](https://cratebeforeattack.com/posts/20200731-july-update/).

[Wonder](https://kettlecorn.itch.io/wonder) ([source code](https://github.com/kettle11/LD46)) is a casual physics puzzle game by [@kettlecorn](https://twitter.com/kettlecorn)
made for the web with WebAssembly, browser APIs, and no game framework.
The objective is to collect all the stars on each level
by drawing lines for the ball to roll along.

The game was made in 48 hours for the
[Ludum Dare game jam](https://ldjam.com) that occurred in April.
@kettlecorn recently published an article going into the technical and
creative challenges encountered making the game:
[“Making a Game in 48 hours with Rust and WebAssembly”](https://ianjk.com/rust-gamejam/).

Wonder can be [played in the browser on itch.io](https://kettlecorn.itch.io/wonder).

### Vlad Zhukov’s [Online RTS Prototype](https://twitter.com/VladZhukov0/status/1288091150339969024) [#](https://gamedev.rs#vlad-zhukov-s-online-rts-prototype)

[Vlad Zhukov](https://twitter.com/VladZhukov0) shared a video of a WIP multiplayer online strategy game
where you fight with other players for territory.
Currently, there are two types of resources and 5 types of buildings.
To build on the tile you need to occupy it with your warriors first.
The player who occupied all enemies’ tiles win.

The game is written with [miniquad](https://github.com/not-fl3/miniquad)
and a custom GUI library.
Some parts of the game are promised to be open-sourced in the future.
Read more about crates used in this project [here](https://reddit.com/r/rust_gamedev/comments/hzdzqg/my_new_online_strategy_game/fzk4l25).

*Discussions:
twitter,
/r/rust_gamedev*

![screenshot](../../assets/8bb2af3cb1da0a09.jpeg)


[A/B Street](https://abstreet.org) is a traffic simulation game exploring
how small changes to roads affect cyclists, transit users, pedestrians,
and drivers.

This month [versions v0.2.2..v0.2.5](https://github.com/dabreegster/abstreet/releases) were released.
Some of the updates:

- A new random traffic scenario generator that makes people go between houses and workplaces.
- New commute pattern explorer tool.
- New character art to give cutscenes a bit more personality.
- Lots of pathfinding and user interface improvements.
- Bugfixes and improved performance (especially startup time on large maps).

![gameplay](../../assets/f04949df8f6bce5d.gif)


[@oliviff](https://twitter.com/oliviff) released [Tennis Academy Dash](https://iolivia.itch.io/tennis-academy-dash)
[v0.2](https://twitter.com/oliviff/status/1285298082033348609):

This release features:

- a layering/scene management system
- transitioning between UI scenes and game scenes
- improving the level loading to work with string config files
- adding a 5th level

[protochess](https://protochess.com/) ([source](https://github.com/raytran/protochess)) is an online multiplayer chess website
that lets you build custom pieces/boards.

Want a piece that can move like a knight + queen? Sure. Want to play on a 16x16 sized board? Impractical but you can do it!


The frontend is written in Svelte with routing from Routify
and styling with the Bulma CSS framework.
All the chess logic is written in Rust, and compiled to WebAssembly to run singleplayer.
The multiplayer websocket server uses Warp
and is modeled after [this project](https://www.mattkeeter.com/projects/pont/).

*Discussions:
/r/rust*

### Nox Futura (Rust Edition) [#](https://gamedev.rs#nox-futura-rust-edition)

![SSAO demo](../../assets/14b718bcb47fec86.jpeg)


[Herbert Wolverson](https://bracketproductions.com)
(the author of [bracket-lib](https://github.com/thebracket/bracket-lib) and [the Rust Roguelike Tutorial](http://bfnightly.bracketproductions.com/rustbook/))
continues porting their old [“Nox Futura” project](https://thebracket.itch.io/nox-futura) to Rust.
The game uses wgpu, Legion, and Dear ImGui.

Some of this month’s updates:

[The project’s repo is now public](https://github.com/thebracket/noxfutura);- Voxel-friendly SSAO;
- The render pipeline is now about 75% done;
- Jobs board, buildings creation, and lumberjacking;
- 3D cursor and mouse picking;
- Voxelized Vegetation and growing trees;
- Improved A* pathfinding and performance in general.

Check out Sharing Saturday devlogs for more detailed reports:
[#1](https://reddit.com/r/roguelikedev/comments/hktr2y/sharing_saturday_318/fwutz7n),
[#2](https://reddit.com/r/roguelikedev/comments/hp04g6/sharing_saturday_319/fxnsn8h),
[#3](https://reddit.com/r/roguelikedev/comments/ht6wcc/sharing_saturday_320/fygjvkg),
[#4](https://reddit.com/r/roguelikedev/comments/hxcvp8/sharing_saturday_321/fz5atmd).

![gameplay](../../assets/763b10b1a7408daf.png)


[@peat](https://twitter.com/peat) released a simple multiplayer demo of [Textcamp](http://play.text.camp:8080/), a
text-based adventure game.

The goal of Textcamp is to build a modern [MUD](https://en.wikipedia.org/wiki/MUD) platform that can be played
by [ anyone, anywhere](https://text.camp/). It’s very early in development, so please

[say hello](https://twitter.com/textdotcamp)if you’re interested in contributing code or stories!

This demo features:

- Basic scene, mob, and item templating, with spawning and combat.
- Multiplayer authentication and support for hundreds of players.

![Basic Projectiles](../../assets/09fc243a6edbfb35.png)


[Canon Collision](https://canoncollision.com) by [@rukai](https://twitter.com/thisIsRukai) is an Undertale + Homestuck
fan-made platform fighter with powerful tools for modding.

This month, he started work on the project again after taking a break. Notable changes:

[basic projectiles](https://twitter.com/thisIsRukai/status/1287377878460456963),[WIP grab implementation (with some humorous results)](https://www.youtube.com/watch?v=sSrBGpT-Ebs),[New animations + attacks](https://www.youtube.com/watch?v=AaPkRSNhoSM),- and
[custom shaders](https://twitter.com/thisIsRukai/status/1279324105125163008).

### pGLOWrpg [#](https://gamedev.rs#pglowrpg)

![Improved river pathfinding, paths respect topography](../../assets/1c792cd56d9441bd.gif)


The [@pGLOWrpg](https://twitter.com/pglowrpg) (Procedurally Generated Living Open World RPG) is a long-term
project in development by [@Roal_Yr](https://twitter.com/Roal_Yr), which aims to be a text-based game with
maximum portability and accessibility and focus on interactions and emergent
narrative.

For the past month(s) the main focus of the development was on the river generation system in the worldgen. Main features of the river generator are:

- High robustness with most edge cases covered;
- Single-pass with subsequent iterations generation, with numerous options to tweak the process for either precision of the pattern or speed of generation;
- Rivers are sorted upon intersections, their widths are adjusted, waterfalls are formed when necessary;
- Inflow and outflow directions are recorded for each cell, which allows following the river upstream or downstream;
- Simple yet effective erosion model implemented, which ensures no upwards flows are allowed;
- Each stream has its unique ID, which will later be linked to the stream data;
- Streams have 12 orders of magnitude from smallest brooks to major rivers;
- All the options are available to user under “General”, “Advanced” and “Very advanced” sections for any level of fine-tuning.

Further development will involve re-factoring of the code and making it ready
to be published prior to implementing new features. For small dev reports follow
[@pGLOWrpg](https://twitter.com/pglowrpg) on Twitter.

![Sandbox screenshot](../../assets/77d50c8a4a5215d7.png)


[Sandbox](https://github.com/JMS55/sandbox) is a falling sand game by JMS55 that provides a variety of fun
particle types to place, and then you get to watch the resulting interactions!

As they didn’t make it in time for last month’s newsletter, this month’s edition covers the work they did in June and July:

- Released version 1.0 and 1.1, created a flatpak package and associated metadata,
and published it to
[Flathub](https://flathub.org/apps/details/com.github.jms55.Sandbox). - Several new particles such as Fire, Mirror, Glitch, and some hidden ones, and tweaked or overhalled almost every other particle!
- A fancy new glow post process effect for Acid/Fire/Electricity,
created using wgpu-rs compute shaders.
- As a precursor to this, they made a PR to the pixels crate that removes the old RenderPass approach in favor of giving the user direct access to wgpu.

- Made a slick new icon and background for the game.
- Added a video recording feature using gstreamer-rs and x264enc,
and then later removed it (for now).
- Moving from recording the raw texture generated for pixels to the post-processed texture from wgpu involved a major overhaul, and it proved too glitchy and slow. Hopefully, it will be revived later, in the form of recording user inputs.

- Many structural improvements, such as less glitchy particle placement with Bresenham’s line algorithm, better error handling, and ensuring particles are only ever stored on the heap.
- Performance improvements, including generating noise in a separate thread.
- Currently WIP: UI using imgui.

Got any ideas? Leave an [issue on github](https://github.com/JMS55/sandbox), or add it yourself!

[Pushin’ Boxes](https://septum.io/games/pushin-boxes) ([itch](https://septum.itch.io/pushin-boxes))
is a [Sokoban](https://en.wikipedia.org/wiki/Sokoban) clone made with [ggez](https://github.com/ggez/ggez) by
[@septum](https://twitter.com/septum___). It features 16 levels of puzzling box-pushin’ action
where the player controls a little robot (named プシン).
Check out a [blog post](https://septum.io/blog/my-first-game) about the game’s release.

![gameplay sample](../../assets/6b6a1dda4fcc550f.gif)


[Don’t Stop](https://superahtoms.itch.io/dont-stop) by @superahtoms is a rhythm game
written using Rust and SDL2 for the [GMTK 2020 jam](https://itch.io/jam/gmtk-2020).

Ever just wanted to keep dancing but the fuzz wants you to stop? Well now you can! Just keep on dancing, don’t let the bouncers grab you while you’re doing it or your fun stops! Keep being the life of the party because you are Party Pat!

Be like wind, be fast, dance and don’t get caught!


*Discussions:
/r/rust_gamedev*

[shotcaller](https://github.com/amethyst/shotcaller) is a WIP quick (~7mins) ASCII-rendered RTS/MOBA game.

In the way “MOBA” games such as DOTA2 or LoL are usually played, the captain of the team is the default shotcaller.

The shotcaller needs to be unbiased and not have tunnel vision. You need to be able to think in the future and tell what would happen if you did this or that. This becomes crucial when deciding to base-race or teleport back to defend. ~reddit-user

Everyone on the team can play the part of Shotcaller on occasion. The act of shotcalling is not typically the most prevalent activity of any player, even for a captain — after all, they also need to play their hero.

But in this game, all you do is shotcalling and big-picture strategizing. The game plays as if you were controlling the 6th-person-in-the-booth “coach” player, and your team (of AI-played bots) actually follows your instructions to the letter, within their designed constraints.


The game is in an early stage of development,
[check out the design document](https://www.notion.so/Shotcaller-7374d2b2819c42ccb40f01dc7089d419) for details and plans.



![fps-game-screenshot](../../assets/f5bac93df9dfee99.jpeg)

[footage from the game’s current state](https://youtu.be/NIJNgr9zeXk).

On this update, [@pingFromHeaven](https://twitter.com/pingFromHeaven) talks about the lighting implementation that
sets the tone for the game, how Rust is good at shortening the debugging
times, which is especially valuable when working directly with OpenGL and why
he doesn’t describe what the game is about.

The next update is going to be about establishing the mood further, which includes a more elaborate environment with more details, basic SFX and particles.

![new agent info panel](../../assets/3d6aad4850bd99f9.jpeg)


[Zemeroth](https://github.com/ozkriff/zemeroth) by [@ozkriff](https://twitter.com/ozkriff) is a minimalistic 2D turn-based tactical game.

Some of the recent updates:

- The game got a new development roadmap:
[“Final Push”](https://twitter.com/ozkriff/status/1280874966855176199). - UI updates:
[widget stretching](https://twitter.com/ozkriff/status/1284154997190594560)and[more informative “dots”](https://twitter.com/ozkriff/status/1284418956296626176). - A few actions
[got additional effects](https://twitter.com/ozkriff/status/1282051985907298306). - The work on adding sounds has begun.

![Sunrise](../../assets/3f987e4249b850b6.gif)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In July, Veloren reached its 1000th merge! Lots of work has been done towards the 0.7 release. The release date has been pushed from the beginning of August to mid-August. A loot table system was added to item drops. Lots of work has been done on animations and quadrupeds. Networking has switched to a new system. Significant improvements have been made to pathfinding system to improve fast quadruped movement. Particle systems are being implemented and optimized. A crafting GUI has been added. Translations have stabilized significantly, and there is a framework for translators to know what needs to be done.

![Fire particles](../../assets/8a9034cc075d5513.gif)

You can read more about some specific topics from July:

[Networking Milestone](https://veloren.net/devblog-75#networking-milestone-by-xmac94x)[The Case of the Disappearing Entities](https://veloren.net/devblog-75#the-case-of-the-disappearing-entities-by-imbris)[Pathfinding](https://veloren.net/devblog-75#pathfinding-with-zesterer)[GUID Insights](https://veloren.net/devblog-75#guid-insights-by-sharp)[Particle System](https://veloren.net/devblog-76#particle-system-by-lobster)[Translation Help](https://veloren.net/devblog-76#we-need-your-help-for-translations-this-is-how-it-s-done-by-xmac94x)[Particle Improvements](https://veloren.net/devblog-77#particle-improvements-by-lobster)[CPU Workloads](https://veloren.net/devblog-77#cpu-workloads-by-angelonfira)[Refactoring WORLD_SIZE](https://veloren.net/devblog-78#refactoring-world-size-by-sharp)

July’s full weekly devlogs: “This Week In Veloren…”:
[#75](https://veloren.net/devblog-75),
[#76](https://veloren.net/devblog-76),
[#77](https://veloren.net/devblog-77),
[#78](https://veloren.net/devblog-78).

In August, 0.7 will be released. Work will continue on castle and cave generation. The inaugural episode of the Rust Game Dev podcast will be released, which features an interview by Veloren developers.

![Quadrupeds](../../assets/201bc9a13b868163.png)

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

[@aclysma](https://twitter.com/aclysma) published a [tutorial](https://blog.aclysma.com/rust-on-ios-with-sdl2/) that describes setting up
Rust/SDL2 on iOS. The resulting app can run in the simulator as well as on
physical devices. [SDL2](https://www.libsdl.org/download-2.0.php) is a mature library providing basic rendering,
audio, and input support. It can also be used to set up an opengl or vulkan
surface. This demo is using [Rust-SDL2](https://crates.io/crates/sdl2) for bindings.

![sokoban update](../../assets/b59e05d582b6ec6d.png)


The Rust Sokoban tutorial is an online book aimed at Rust gamedev beginners which walks through making a simple Sokoban game using ggez and ECS (with specs). It tries to teach the basics of architecting in ECS and basic Rust concepts through a hands-on approach.

This month:

- the book was officially released on July 10th;
- the project received 3 external contributions;
- a few text edits were done, including fixing an issue with code snippets not appearing correctly;
- work on translations has started (🇨🇳 translation coming soon 🤞).

You can follow
the release discussion [on Twitter](https://twitter.com/oliviff/status/1281641563257360384),
provide feedback [on github](https://github.com/iolivia/rust-sokoban) and
read the book at [sokoban.iolivia.me](https://sokoban.iolivia.me).



![youtube preview](../../assets/cca69fb3af4dc0dd.jpeg)

[TanTan](https://twitter.com/Tantan22430802) released a [video tutorial](https://youtube.com/watch?v=TUE_HSgQiG0)
that guides you through all the step of making a pong game in Rust
using the GGEZ framework.

The source code [can be found here](https://github.com/TanTanDev/rusty_pong).

Data-Oriented Design is an approach to program optimization focused on considering the features and limitations of the target hardware, and carefully controlling the memory layout of data to take advantage of those.

In [this article](http://jamesmcm.github.io/blog/2020/07/25/intro-dod/#en), [jamesmcm](https://github.com/jamesmcm) provides benchmarks and
code for four example scenarios:

[Array of Structs vs. Struct of Arrays](https://en.wikipedia.org/wiki/AoS_and_SoA)- Branching in a hot loop
- Iteration in a vector vs. a linked list
- Monomorphisation vs.
[Dynamic Dispatch](https://doc.rust-lang.org/book/ch17-02-trait-objects.html#trait-objects-perform-dynamic-dispatch)

The full article is available [here](http://jamesmcm.github.io/blog/2020/07/25/intro-dod/#en).



![youtube preview: a slide with Tower Rangers game](../../assets/afa31745f75f0650.jpeg)

[watch the talk](https://youtu.be/0Bj-5C2Zfqs?t=1404).

During the recent [“Rust and Tell”](https://berline.rs/2020/07/28/rust-and-tell.html) online event
[Stephan @extrawurst Dilly](https://twitter.com/extrawurst) gave a [“Rust’N’Games” talk](https://youtu.be/0Bj-5C2Zfqs?t=1404)
about their experience of using Rust in games at [Gameroasters](https://www.gameroasters.com/).

## Library & Tooling Updates [#](https://gamedev.rs#library-tooling-updates)

![Functional scheme](../../assets/3eefa952edaef628.png)


[Servo for Unity](https://github.com/MozillaReality/servo-unity) is a Unity native plugin and a set
of Unity C# script components allow third parties to incorporate
Servo browser windows into Unity scenes.

[A blog post about the project](https://blog.mozvr.com/a-browser-plugin-for-unity) gives a good
overview of the project goals, capabilities, architecture, challenges,
and future development plans.

[big-brain](https://github.com/zkat/big-brain) by [Kat Marchán](https://twitter.com/zkat__) is a [utility AI](https://en.wikipedia.org/wiki/Utility_system) library for games,
built on the specs ECS.

It lets you define complex, intricate AI behaviors for your entities based on their perception of the world. Definitions are almost entirely data-driven, using plain .ron files, and you only need to program considerations (entities that look at your game world), and actions (entities that perform actual behaviors upon the world). No other code is needed for actual AI behavior.


[weasel](https://github.com/Trisfald/weasel) by [@Trisfald](https://github.com/Trisfald) is a customizable battle system for turn-based games.

This month [v0.8 was released](https://github.com/Trisfald/weasel/releases/tag/v0.8.0).
Highlights include:

- New event types
- Inanimate objects
- Status effects
- Many new examples

[naia](https://github.com/naia-rs/naia) (**n**etworking **a**rchitecture for **i**nteractive **a**pplications)
is a cross-platform (currently WebAssembly & Linux) networking engine that intends
to make multiplayer game development in Rust dead simple and lightning fast.

At the highest level, you register Event and Entity implementations in a module shared by Client & Server. Then, naia will facilitate sending/receiving those Events between Client & Server, and also keep a pool of tracked Entities synced with each Client for whom they are “in-scope”. Entities are “scoped” to Clients with whom they share the same Room, as well as being sufficiently customizable to, for example, only keep Entities persisted & synced while within a Client’s viewport or according to some other criteria.


*Discussions:
/r/rust*

![Voronoi diagram example](../../assets/a94f7ace3650326b.png)


[voronator](https://github.com/fesoliveira014/voronator-rs) by [Felipe Santos](https://twitter.com/fesoliveira0) is …
a Rust port of the [d3-delaunay](https://github.com/d3/d3-delaunay) and [delaunator](https://github.com/mapbox/delaunator) libraries
that provide delaunay triangulation and Voronoi diagram generation.

*Discussions:
/r/rust*

[Mun](https://mun-lang.org) is a scripting language for gamedev focused on quick iteration times
that is written in Rust.

[Rustacean Station](https://rustacean-station.org) released [a podcast about Mun](https://rustacean-station.org/episode/020-mun)
in which the Mun Core Team sat down with host Jeremy
to talk about why they chose Rust to develop Mun. If you are interested in
having an inside look into Mun’s origins and evolution, we recommend you check
it out - or any of Rustacean Station’s other podcasts for that matter!

Their additional [July updates](https://mun-lang.org/blog/2020/07/30/this-month-july) include:

- initial support for the Language Server Protocol;
- a community entry for the
[Make It or Break It content](https://github.com/mun-lang/mun/issues/220)of Spaceship recreated with Mun & Rust; - CLI support for creating Mun projects;
- performance benchmarks and improvements;
- bugfixes and improved documentation.

### ash(-window) [#](https://gamedev.rs#ash-window)

[ ash-window](https://crates.io/crates/ash-window), an interoperability library for

[and](https://crates.io/crates/ash)

`ash`

[, is now part of the](https://crates.io/crates/raw-window-handle)

`raw-window-handle`

`ash`

repository and will be updated more closely
with new `ash`

releases.### grr 0.8 [#](https://gamedev.rs#grr-0-8)

[ grr](https://github.com/msiglreith/grr) is a modern OpenGL 4.5+ wrapper.
It provides a cleaned up API built around Vulkan’s naming scheme.
The latest release further pushes the crate towards
full compatibility with the core features.

Most notable changes:

- Added support for a bunch of Formats
- Extended transfer operations (Attachment <-> Host <-> Buffer <-> Image)
- Raw context access
- Shader & Pipeline log control
- Device submission control

Special thanks to [@masonium](https://github.com/masonium)
for contributing a lot of these features and fixes!

![miniquad ios](../../assets/ace60533dc2c4f49.jpg)


[miniquad](https://github.com/not-fl3/miniquad) is a safe and cross-platform rendering library
focused on portability and low-end platforms support.

This month opengl backend of miniquad was successfully ported to iOS.
With this update [macroquad](https://github.com/not-fl3/macroquad), [good-web-game](https://github.com/not-fl3/good-web-game) and all the games
build directly with [miniquad](https://github.com/not-fl3/miniquad) can be run on IOS, Android, WASM,
Linux, macOS and Windows!

![procgen dynamic "grass field"](../../assets/028c48fa1a705058.jpeg)

[@MacTuitui](https://twitter.com/MacTuitui)’s everyday

[nannou](https://nannou.cc)experiment #1274

The work is ongoing to validate all the incoming commands and guarantee API safety.
Special thanks to [@GabrielMajeri](https://github.com/GabrielMajeri) for helping to convert assertions
into errors at `wgpu`

level.
The wgpu devs are also introspecting shader requirements
and matching them against the pipelines, but this will take more effort
before it will become universally available.

[@cwfitzgerald](https://github.com/cwfitzgerald) has been busy adding a few handy native-only extensions,
such as descriptor indexing and push constants.
They have also converted the project’s logging to [tracing](https://crates.io/crates/tracing),
setting up the infrastructure for CPU profiling.

In the past 2 months, the API for descriptor structures in `wgpu-rs`

have been undergoing a turbulent period.
First, non-exhaustive semantics led to introduction of constructors.
Then, efforts to reduce code duplication inside `wgpu`

project has led to the
[bovine invasion](https://github.com/gfx-rs/wgpu-rs/pull/460) on wgpu-rs API side.
The devs are figuring out the plan to address that with a builder pattern now,
which will address both the `Cow`

s and non-exhaustives,
hopefully putting an end to the turbulence.

In the meantime, `wgpu-rs`

ecosystem is flourishing with applications and libraries.
The [showcase gallery](https://wgpu.rs/#showcase) was updated with a few shiny images.

Finally, [@kunalmohan](https://github.com/kunalmohan) has been busy
[implementing WebGPU in Servo](https://github.com/servo/servo/projects/24), based on `wgpu`

.
Thanks to this work, Servo is currently ahead of Gecko
in terms of API being up-to-date and covered 🎉.
It’s already capable of rendering most of the examples,
and the devs are looking forward to the day when the same Rust code
(rendering with `wgpu-rs`

) will be deployable to the Web,
and viewable from Firefox, Servo, Chrome, and other browsers.

[luminance](https://github.com/phaazon/luminance-rs) by [@phaazon](https://twitter.com/phaazon_) is a type-safe, type-level and stateless
graphics framework.

This month [luminance v0.40 got released](https://phaazon.net/blog/luminance-0.40).
Some of the highlights:

- The complete backend/architecture redesign.
- A new platform crate has appeared:
[luminance-sdl2](https://crates.io/crates/luminance-sdl2), which adds support for the sdl2 crate. [luminance-webgl](https://crates.io/crates/luminance-webgl)and luminance-web-sys, to support the Web!- A
[luminance-examples-web](https://github.com/phaazon/luminance-rs/tree/master/luminance-examples-web)crate is available to test with`yarn`

easily. [luminance-front](https://crates.io/crates/luminance-front), which is a front crate to ease working with luminance types.- The type system experience has been greatly improved. Most of the time, you will not have to annotate types anymore — like Program or Tess.
- About
`Tess`

, a BIG update has landed, has it’s now heavily typed (vertex type, index type, vertex instance data type, memory interleaving type). - More render states features, such as the possibility to enable or disable depth writes, separate RGB/alpha blending, etc. etc.
- Also, the
[luminance book](https://rust-tutorials.github.io/learn-luminance/)got updated.

A complete changes list and a migration guide can be found
[in the CHANGELOG](https://github.com/phaazon/luminance-rs/blob/master/luminance/CHANGELOG.md#040).

luminance-0.41 got released a few days after to fix some type design problems with the gates, and to enhance the error flow in graphics pipelines, revisited to be more flexible and seamless.

Also, check out the
[“The compile-time deinterleaving interface”](https://phaazon.net/blog/typesafe-deinterleaving)
blog post that delves deep into this new feature.

*Discussions:
/r/rust*

![execution flow example](../../assets/3e42e0c047ab7f2c.png)


[Graphene](https://github.com/ApoorvaJ/graphene) is a Vulkan render graph. Still heavily a work in progress,
it is built to be a simpler abstraction over Vulkan, with long-term ambitions to
serve as a graphics test-bench.

Currently, it implements a mesh render pass followed by a chromatic aberration
post-process in less than [250 lines of Rust code](https://github.com/ApoorvaJ/graphene/blob/a1ee574d92445f4cff195ca517af2912ebfce697/src/demos/00/main.rs).
Current features include easy Vulkan initialization, automatic swapchain
resizing, glTF mesh loading, and shader hot-reloading.
Check out a [“Render graphs” blog post](https://apoorvaj.io/render-graphs-1/)
for a more in-depth introduction to the project.

![chromatic aberration demo](../../assets/8344605b8a112b44.jpeg)


You can follow progress on [GitHub](https://github.com/ApoorvaJ/graphene) or on [Twitter](https://twitter.com/ApoorvaJ).

### Vulkan Renderer (Name TBD) [#](https://gamedev.rs#vulkan-renderer-name-tbd)



![Vulkan renderer on iOS prototype](../../assets/869b6d937bb6860e.jpeg)

[@aclysma](https://twitter.com/aclysma) published a [new vulkan-based renderer](https://github.com/aclysma/renderer_prototype) that
uses [atelier-assets](https://github.com/amethyst/atelier-assets) to load 3D scenes exported from blender.

The objective of this repo is to build a scalable, flexible, data driven renderer. Scalable in the sense of performance as well as suitability for use in large, real-world projects. This means streaming, LODs, visibility systems, and multi-threaded draw call submission need to be possible. Additionally it means thinking through how an asset pipeline would work for a team with dedicated artists and supporting workflow-friendly features like hot reloading assets, possibly on remote devices.


This video demonstrates the renderer running on iOS and receiving asset updates
via wifi. The scene is “sponza” exported from blender. Vulkan is supported on
windows and linux natively. Support for macOS and iOS is via the
well-established [MoltenVK](https://github.com/KhronosGroup/MoltenVK) project.

The demo was ported from PC to iOS over a single weekend and out of approximately 300 crate dependencies (including complex, OS-specific ones like tokio), all but a few worked out-of-the-box!

![Demo of Ludusavi GUI](../../assets/981621f0c2c1a795.gif)


[Ludusavi](https://github.com/mtkennerly/ludusavi) is a tool written in Rust by [@mtkennerly](https://twitter.com/mtkennerly) for backing up PC game
save data. It has backup info for more than 7,000 games, is cross-platform for
Windows, Linux, and Mac, and has a GUI as well as a command line interface.
The GUI was created using the [Iced](https://crates.io/crates/iced) crate.

The [backup info](https://github.com/mtkennerly/ludusavi-manifest) is sourced from [PCGamingWiki](https://www.pcgamingwiki.com/wiki/Home) so that everyone can help to
expand the data, and it’s stored in a documented format so that other backup
tools can share the same data set. A [plugin](https://github.com/mtkennerly/ludusavi-playnite) for [Playnite](https://playnite.link) was also just
released.

[Langcraft](https://github.com/SuperTails/langcraft) is the Minecraft LLVM target you’ve never wanted.

Langcraft started as a dare to the `#lang-dev`

channel of the Rust
Community Discord to be able to parse Rust code in Minecraft.
Naturally, it grew into a full code generator that can translate
most LLVM IR to
[Minecraft data packs](https://minecraft.gamepedia.com/Data_Pack),
the game’s deliberately-limited in-game scripting language. Langcraft
is entirely language independent, so any language with an LLVM-based
compiler can (with the right API bindings) run in Minecraft. Currently,
bindings to both C and Rust exist. While not as visually impressive as
a redstone computer, Langcraft does stretch the bounds of the game quite
a bit, using jukeboxes for memory, armor stands to represent pointers,
and rearranging compiled code to make it run in the bounds of the data
packs’ fixed instruction limit.

This is all, naturally, entirely useless. The project is also still
heavily work-in-progress and does not pretend to be stable, but it is
usable. A handwritten interpreter for a Rust-like language has already
been demonstrated running, and even more complex projects like [CHIP-8
emulators](https://github.com/Dhole/chip8-rs.git) function (albeit at
extremely slow speed).

You can watch a [video of Rust interpreter running Fizzbuzz](https://youtube.com/watch?v=Cx0w5Wn9pPU):

## Meeting Minutes [#](https://gamedev.rs#meeting-minutes)

[See all meeting issues](https://github.com/rust-gamedev/wg/issues?q=label%3Ameeting) including full text notes
or [join the next meeting](https://github.com/rust-gamedev/wg#join-the-fun).

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[winit’s “Good first issue” and “help wanted” issues](https://github.com/rust-windowing/winit/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+label%3A%22status%3A+help+wanted%22+label%3A%22Good+first+issue%22).[gfx-rs’s “contributor-friendly” issues](https://github.com/gfx-rs/gfx/issues?q=is%3Aissue+is%3Aopen+label%3Acontributor-friendly).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[A/B Street’s “good first issue” issues](https://github.com/dabreegster/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).

## Jobs [#](https://gamedev.rs#jobs)

-
[Embark](https://www.embark-studios.com)is looking to hire Open Source Engineer specifically to work on Rust projects (Remote or Stockholm, Sweden):At Embark, we love the openness and collaborative nature of the quickly growing ecosystem and community around Rust, including its tens of thousands of open source crates. We’re committed to supporting a thriving open source ecosystem for game development in Rust.

As an Open Source Engineer at Embark, you will work with our community and engineering teams on open source. You’ll help maintain and develop our open source presence, and be a key link between Embark and the greater software ecosystem.

You can find all of the details on their

[job offer page](https://www.embark-studios.com/jobs/910166-open-source-engineer).

Btw, Embark are also

[looking for Software Engineer interns](https://www.embark-studios.com/jobs/915561-internship-software-engineer-rust).![Embark’s logo](../../assets/2f47b1cb20de423f.jpg)


## Bonus [#](https://gamedev.rs#bonus)

Just an interesting Rust gamedev link from the past. :)



![youtube preview](../../assets/8ec14157218928e0.jpeg)

[SHAR](https://fedorgames.itch.io/shar) (Russian “Шар” - ball) by [@fedor_games](https://twitter.com/fedor_games) (author of [miniquad](https://github.com/not-fl3/miniquad)/[macroquad](https://github.com/not-fl3/macroquad))
is a 3rd-person online action game that aims to create unique experience
combining destructible world and team-based ball game.

SHAR is an action combination of tactical and sports game in the destructible world. The rules are extremely simple: two teams, one ball. The team that carries the ball into the opponent’s gates gets a score, the team with the most score at the end of the game is the winner. However, this is where things get interesting! Players have the variety of skills and tricks and destructible environment to fiddle around to slam the opponent and win the game.


Some of the game’s features:

- A network-synchronized physics engine powered by bullet-rs;
- A bunch of physics-based player skills;
- Extensive build-in editors for game maps, skeletal animation, effects & particle systems;
- Modding support.

The game was built on top of a homegrown game engine using:
winit, glium, imgui-rs, [tinyecs](https://github.com/not-fl3/tinyecs), [awesomium-rs](https://github.com/not-fl3/awesomium-rs), [ears](https://github.com/nickbrowne/ears).

During RustFest Zurich 2017, Fedor gave a self-descriptive talk
“SHAR: Rust’s gamedev experience”.
You can [watch the recording here](https://youtube.com/watch?v=nXR8f4r6ggM).

The game was in active development around 2016-2017.
In 2017 the game [passed Steam Greenlight](https://steamcommunity.com/sharedfiles/filedetails/?id=868228143).
During 2018 [the project was suspended](https://fedorgames.itch.io/shar/devlog/52720/time-to-move-on).

That’s all news for today, thanks for reading!

Subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!