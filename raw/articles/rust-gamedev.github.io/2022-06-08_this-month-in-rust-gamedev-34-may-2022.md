---
title: 'This Month in Rust GameDev #34 - May 2022'
url: https://gamedev.rs/news/034/
author: Rust GameDev WG
published: '2022-06-08'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 34th issue of the Rust GameDev Workgroup’s
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

[Announcements](https://gamedev.rs/news/034/#announcements)[Game Updates](https://gamedev.rs/news/034/#game-updates)[Learning Material Updates](https://gamedev.rs/news/034/#learning-material-updates)[Engine Updates](https://gamedev.rs/news/034/#engine-updates)[Tooling Updates](https://gamedev.rs/news/034/#tooling-updates)[Library Updates](https://gamedev.rs/news/034/#library-updates)[Other News](https://gamedev.rs/news/034/#other-news)[Popular Workgroup Issues in GitHub](https://gamedev.rs/news/034/#popular-workgroup-issues-in-github)[Discussions](https://gamedev.rs/news/034/#discussions)[Requests for Contribution](https://gamedev.rs/news/034/#requests-for-contribution)[Jobs](https://gamedev.rs/news/034/#jobs)

## Announcements [#](https://gamedev.rs#announcements)

### Rust Graphics Meetup 2 [#](https://gamedev.rs#rust-graphics-meetup-2)

The 2nd Rust Graphics Meetup took place on the 21st of May. The videos of the talks have been released:

[Vismut](https://youtube.com/watch?v=0IsllXP7_pY)-[Lukas Orsvärn](https://github.com/lukors)[Screen-13](https://youtube.com/watch?v=ywZznsCXUjs)-[John Wells](https://github.com/attackgoat/screen-13)[Optimizing wgpu with Data Driven Design](https://youtube.com/watch?v=DDG4bcGs7zM)-[Connor Fitzgerald](https://github.com/cwfitzgerald)

### Rust GameDev Meetup [#](https://gamedev.rs#rust-gamedev-meetup)

![Gamedev meetup poster](../../assets/ac9fbef81c28c723.png)


The 16th Rust Gamedev Meetup took place in May. You can watch the recording of
the meetup [here on Youtube](https://youtu.be/XOpZIzmFifk). Here was the schedule from
the meetup:

- RustConf Arcade Cabinet -
[@carlosupina](https://twitter.com/carlosupina) - Puzzle platformer -
[@tesselode](https://twitter.com/tesselode) - Veloren -
[@AngelOnFira](https://twitter.com/AngelOnFira) - Graphite -
[@GraphiteEditor](https://twitter.com/graphiteeditor)

The meetups take place on the second Saturday every month via the [Rust Gamedev
Discord server](https://discord.gg/yNtPTb2) and are also [streamed on
Twitch](https://twitch.tv/rustgamedev). If you would like to show off what you’ve been
working on at the next meetup on [June 11th](https://everytimezone.com/s/ffc60181), fill out [this
form](https://forms.gle/BS1zCyZaiUFSUHxe6).

### 3D Ferris [#](https://gamedev.rs#3d-ferris)

![colorful render of a 3d model of Ferris with additional wireframe view](../../assets/2767ed1d283a0b3a.jpg)


[@RayMarch](https://twitter.com/Ray__March) is
creating a game-ready 3D model of [Ferris the Rustacean](https://rustacean.net/). These links
provide a more detailed look:
[360 overview](https://twitter.com/Ray__March/status/1512907700740444163),
[Ferris dancing](https://twitter.com/Ray__March/status/1523717266730151936).

Once the model is finished, it will be published under a permissive license on
[GitHub](https://github.com/RayMarch), so you can use it in your 3D game,
rendering demo, v-tuber avatar, you name it!

If you have any feedback feel free to share on [Discord](https://discord.com/channels/676678179678715904/974371568975216700).

*Discussions: Twitter*

### RustConf Arcade Cabinet [#](https://gamedev.rs#rustconf-arcade-cabinet)

![arcade cabinet](../../assets/2043856cae0a1bab.png)


[Carlo](https://twitter.com/carlosupina) is building a custom arcade cabinet that will be at
RustConf 2022 in Portland. It is an opportunity for Rust game developers to
share their games with the broader community. If you are interested in getting
your game on the cabinet, read [this Twitter thread](https://twitter.com/carlosupina/status/1523715837726961664) and
fill out the [interest form](https://forms.gle/onFm5fCygdbiArqJ7).
All of the parts for the cabinet are currently in production,
and art for the sides is in progress.
Check out the latest update [here](https://twitter.com/carlosupina/status/1532717151240323072).

## Game Updates [#](https://gamedev.rs#game-updates)

![Gameplay demo](../../assets/eba18779a4bc6900.gif)


[Battleship](https://github.com/orhun/battleship-rs) by [@orhun](https://github.com/orhun/) is the [battleship game](https://en.wikipedia.org/wiki/Battleship_(game)) implemented in Rust.

Features:

- Fully playable between 2 players on the terminal.
- No installation required.
- Works over TCP sockets.
- Very lightweight to host your own server (only has 1 dependency).

[ROOM4DOOM](https://gitlab.com/flukejones/room4doom) is a rewrite of the classic Doom engine in Rust with some
modernisation.

[@flukejones](https://twitter.com/flukejones) has been very busy in the last 4 months completing
many parts of ROOM4DOOM; rendering, subsystems for menus, status bar, intermissions,
and of course the actual gameplay - you can now complete Doom 1 in ROOM4DOOM.

A recent Twitter thread has been cleaned up and expanded into a blog post providing
context to the project and a walk-through of the history.
You can view that [here](https://ljones.dev/blog/room4doom-20220529/).

![a ghost, stuck in limbo, on a mountain pass](../../assets/1fdb4a01a42edbad.png)


[limbo_pass](https://github.com/shnewto/limbo_pass) by [@shnewto](https://github.com/shnewto/) is a little 3D walking sim in Bevy that uses
scenes, meshes, and materials exported directly from Blender.

Features include:

- Blender assets exported to glTF
- Collision detection with
[bevy_rapier3d](https://github.com/dimforge/bevy_rapier) - Looping audio with
[bevy_kira_audio](https://github.com/NiklasEi/bevy_kira_audio)

For more info, see the [announcement post](https://twitter.com/shnewto/status/1520897809968340992) and the
[gameplay video](https://youtu.be/gxUesnuTBBI).

![hgs_screen](../../assets/d37c57f253322ac4.jpg)


[Hydrofoil Generation](https://hydrofoil-generation.com/)
([Steam](https://store.steampowered.com/app/1448820/Hydrofoil_Generation/), [Facebook](https://facebook.com/HydrofoilGenerationSailing/), [Discord](https://discord.gg/DtKgt2duAy/))
is a realistic sailing/foiling inshore simulator in development for PC/Steam
that will put you in the driving seat of modern competitive sailing.
Hydrofoil Generation is based on a custom made DirectX 11 based engine.

A new [trailer](https://youtu.be/oFtFdmnkkSI) just landed showcasing new animations, the new
Hong Kong location, and camera modes.

Meanwhile, private beta-testing is well underway with good feedback regarding boat controls and physics, netcode, and software stability, Rust for sure delivered on all the promises here.

The first set of Sailing rules has also been implemented and part of the current beta testing process with more rules to be added in the next months.

Sadly the target Q2 2022 Early Access release on Steam couldn’t be hit and now the team is aiming at a Q4 2022 release.

### Country Slice [#](https://gamedev.rs#country-slice)

![Country_slice_gif](../../assets/5155850da7ba12d2.gif)


Country Slice (WIP name) is a relaxing building game being made by [@anastasiaopara](https://twitter.com/anastasiaopara).

This month, she added an animated undo system. You can find more details in this
[Twitter thread](https://twitter.com/anastasiaopara/status/1530473522224582656), and follow the [newsletter](https://dashboard.mailerlite.com/forms/10395/51067704544593017/share)
for more updates.

[Way of Rhea](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n34) is a puzzle adventure with hard puzzles and forgiving
mechanics being produced by [@masonremaley](https://twitter.com/masonremaley) in a custom Rust
engine. You can support development by [wishlisting the game on Steam](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n34), and
[giving feedback](https://steamcommunity.com/app/1110620/discussions/0/3275817732933009791/) on the Steam demo.

Way of Rhea was selected to be part of the Cerebral Puzzle Showcase! The event
is over, you can still find the
[list of games and some of the demos here](https://store.steampowered.com/sale/CerebralPuzzleShowcase). Recent updates:

- More work was done on the
[Jungle Biome visuals](https://store.steampowered.com/news/app/1110620?emclan=103582791465120432&emgid=3180116240852440293) - Dynamic gradient overlays were added to the engine to give a sense of depth
- Fixed bug where Nvidia drivers would incorrectly trigger the crash dump writer
- Fixed a long-running draw call sorting problem that could lead to popping
- Fixed an audio failure when unplugging the active speaker

![Flying down a mountain](../../assets/e5164c721f6293cb.jpg)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In May, work was done on Wyvern models. Smoke was improved from houses, and now has different colours and strengths. A rib cage generator was added, so now there are large bone structures from ancient times around the world. Level of detail objects were added, so trees can now be seen on far-off mountains. This makes the world feel significantly more alive. A lot of work was done on the performance of the game server, as Veloren has been seeing over 100 concurrent players at peak on the server nearly every day for the past few weeks.

Lots of work was done on balancing items and drop rates. Water caves have been worked on, which now means that you might need to enter them from underwater. Modular weapons were merged, which was a change several months in the making. NPCs are now able to pick up items that are on the ground. Work was done on taming and mounting various animals. Weather is still in the works, with improvements to the ambient SFX system for rain. A new UI concept was created for what Airshipper might be able to look like in the future.

May’s full weekly devlogs: “This Week In Veloren…”:
[#170](https://veloren.net/devblog-170),
[#171](https://veloren.net/devblog-171),
[#172](https://veloren.net/devblog-172),
[#173](https://veloren.net/devblog-173),
[#174](https://veloren.net/devblog-174).

![Screenshot: one human hugs another](../../assets/fb27a9595549b8a6.jpg)


[The Hug Game](https://hug.hihaheho.com) by [the HIHAHEHO Studio](https://hihaheho.com)
is an active ragdoll remote hugging simulator made with Bevy and rapier.

The arms are individually controlled using a keyboard on desktop and touch controls on mobile to make various hugs. You can click “Random” to play with a random person or “Room” to share a link to someone you want to play with.

The source code of the game is [available on GitHub](https://github.com/Hihaheho/Hug).



![Preview: a factory](../../assets/7e30a55d62f8db88.png)

[Connect factories on different planets via spaceships](https://reddit.com/r/IndieDev/comments/uxcc7v/connect_different_planets)

[Combine&Conquer](https://martinbucksoftware.itch.io) by [Martin Buck](https://github.com/I3ck) is a WIP strategy game
about automation similar to Satisfactory or Factorio.
This month’s updates include:

[a new view to see in-flight spaceships](https://buckmartin.de/combine-and-conquer/2022-05-05-ship-view.html),[single render node](https://buckmartin.de/combine-and-conquer/2022-05-04-single-node-notification-bg.html),[and the first public prototype release on itch.io](https://buckmartin.de/combine-and-conquer/2022-05-07-itch-io-release.html).

*Discussions: /r/rust*

## Engine Updates [#](https://gamedev.rs#engine-updates)

![Fyroxed](../../assets/71712b05cee153f9.png)


[Fyrox](https://github.com/FyroxEngine/Fyrox) ([Discord](https://discord.com/invite/xENF5Uh), [Twitter](https://twitter.com/DmitryNStepanov)) is a game engine that
aims to be easy to use and provide a large set of out-of-the-box features. In May
it hit version 0.25 which added a lot of new functionality:

- Static plugin system.
- User-defined scripts.
- Play mode for the editor.
- Animation blending state machine editor.
- Prefab inheritance improvements.
- Layout and render transform support for widgets.
- Shortcuts improvements in the editor.
- UI performance improvements.
- Double click support in
`fyrox-ui`

. - Better serializer error recovery.
- Tons of small improvements and fixes.

Sometime after, the engine hit version 0.26 which was primarily focused on bug fixing, but also added some interesting features:

- Project template generator.
- Script API improvements.
- Shader cache fixes.
- Skybox validator.

See full list of changes in respective blog posts - [0.25](https://fyrox.rs/blog/post/feature-highlights-0-25/) and [0.26](https://fyrox.rs/blog/post/feature-highlights-0-26/). Everybody,
who wants to learn how to use the engine should check the new
[2D Platformer Tutorial](https://fyrox-book.github.io/fyrox/tutorials/platformer/part1.html).

[miniquad](https://github.com/not-fl3/miniquad/) is a pure Rust, cross-platform graphics library.

[The biggest PR in miniquad’s history](https://github.com/not-fl3/miniquad/pull/278) landed this month, finishing
the effort of removing all the `sapp`

legacy.

Changes include:

- No more
`sapp-*`

crates. Now it’s just one crate, miniquad! No mess with individual crates anymore, no FFI for miniquad - sapp communication. - On Linux, miniquad does not depend/statically link with lib*-dev packages. Miniquad can choose between glx/egl, x11/wayland at runtime.
- MacOS implementation does not depend on any Objective C code anymore.

[Dims](https://dims.co) ([Twitter](https://twitter.com/DimsWorlds), [Discord](https://discord.gg/Z5CAVmNE57),
[YouTube](https://youtube.com/channel/UCR5gOwS7uSl0a0dl7MLQoqg)) is a WIP open-world creation platform.
Some highlights from the project’s [latest dev log](https://dims.co/post/up-next):

[A terrain tool](https://youtube.com/watch?v=jgkhsY8aZO8)that allows quick landscape creation while still making sure that the biomes are unique and diverse.[A tool to let creators script gameplay events](https://youtube.com/watch?v=rKgv38zkey0)without having ever done any programming.- The pre-alpha is now open for a limited time,
so
[come and try building your own open world games](https://dims.co)!

Also, a bunch of feature videos and tutorials were
[uploaded on the YouTube channel](https://youtube.com/channel/UCR5gOwS7uSl0a0dl7MLQoqg) -
make sure to take a look if you’re interested in Dims.

*Discussions:
/r/rust_gamedev,
/r/worldbuilding*

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

![Bevy Materials video series thumbnail](../../assets/8a4b60d65c74f3e1.png)


[Matthew Bryant](https://youtube.com/channel/UC7v3YEDa603x_84PgCPytzA) has created
[a series about Bevy’s Material abstraction](https://youtube.com/playlist?list=PLT_D88-MTFOMNRPAC-62Hz096aIjT4Noy),
showing how to use custom WGSL shaders in Bevy.

The series walks through the documentation to understand why steps are done in order to build a clear theoretical understanding of Bevy’s high-level abstractions.

- The first of the three videos covers the bare minimum needed to render a material;
- the second introduces bind groups to use textures and generic data in the shader;
- and the final video ties into Bevy’s ECS to copy game data onto the graphics card every frame.

He will be releasing videos about UI in Bevy and Rapier physics next month.

![A picture of speakers](../../assets/b0bd3e33daa47bc6.jpeg)


[QQparty](https://github.com/alanpoon/qq_party) is a serverless multiplayer game built with Bevy ECS
and [Wasmcloud](https://wasmcloud.dev/).

This month, [@rustropy_gaming](https://twitter.com/rustropy_gaming) joined Cosmonic to give
a series of Wasmcloud talks in Kubecon 2022 VLC. They demonstrated
how Bevy can be added into Wasmcloud’s actors as a serverless
game server.

You can check out a recording of the talk on [YouTube](https://youtube.com/watch?v=8q2sPPX5aXY&list=PLj6h78yzYM2Ni0u-ONljTkv4uOutyjwq9&index=3),
as well as viewing the [slides](https://static.sched.com/hosted_files/cloudnativewasmdayeu22/3c/lightingtalk-alan_pdf.pdf). For updates on QQparty,
follow [@rustropy_gaming](https://twitter.com/rustropy_gaming) on Twitter!

![A screenshot of the latest Rusteroids tutorial](../../assets/98ad339e053cfff7.png)


[Rusteroids](https://github.com/filtoid/rusteroids) is a tutorial recreating a clone of Asteroids
in Rust, using SDL2 and the [Specs](https://docs.rs/specs/latest/specs/) library.

New episodes are released weekly and added to the playlist. Most recently,
collision detection was added to reset the game state when the asteroid
and player collide. The latest episode is [here](https://youtube.com/watch?v=KTDdlWErmYU&list=PLFOS-Gn3aXROnSfl26esPExssd-rQw6jD&index=9).

You can subscribe to the [YouTube Channel](https://youtube.com/channel/UC1m6P72nySpB3lKWDYGVipw),
to never miss an episode, or follow [@ecatstudios](https://twitter.com/ecatstudios) on
Twitter!

[@chrisbiscardi](https://twitter.com/chrisbiscardi) published a [video](https://youtube.com/watch?v=gjeEYntkvoY)
on setting up a new 2D platformer project using Bevy. The video covers
integrating with LDTK, Rapier, and becy_ecs_tilemap to get a working
character controller with collisions in a sandbox. It also touches on
staple crates such as bevy_asset_loader and iyes_loopless.

*Discussions:
/r/rust_gamedev,
Twitter*

![Robocave screenshot](../../assets/93227af542de530a.jpg)


[This article](https://cragwind.com/blog/posts/comparing-voxel-game-fsharp-rust/) walks through the process of rewriting an F#
game in Rust. It explores the similarities between the languages and talks
about using simple code constructs where possible. It talks about the Rust
crates used to help with the process. Finally, it goes over a conclusion
comparing the speed of both versions of the games, and the sizes of the
codebases.

![Rustacean Station Logo: rusty Ferris](../../assets/4885c260c492e8da.jpeg)


In May the [Rustacean Station](https://rustacean-station.org) podcast
[interviewed Eric Smith](https://rustacean-station.org/episode/066-eric-smith), the author
of [“Game Development with Rust and WebAssembly”](https://packtpub.com/product/game_development/9781801070973).

In this episode, lots is discussed about why Rust is becoming a good language for game development, different game engines, is Rust web-ready, insights on Rust game development, and Eric’s writing process.

[GamesFromScratch shared a YouTube video](https://youtube.com/watch?v=mLXwR88Dzkc) with an overview of
the most popular engines, frameworks, and libraries for Rust game development,
including: Amethyst, Piston, Bevy, Fyrox, ggez, godot-rust, raylib, SDL2, and SFML.

### New Book: [Multiplayer Game Development in Rust](https://manning.com/books/multiplayer-game-development-in-rust) [#](https://gamedev.rs#new-book-multiplayer-game-development-in-rust)

![Book cover with a MEAP mark](../../assets/f36f9ba849c62eb9.png)


The [“Multiplayer Game Development in Rust”](https://manning.com/books/multiplayer-game-development-in-rust) book by
[@Extrawurst](https://twitter.com/Extrawurst) and [@lyonbeckers](https://twitter.com/lyonbeckers) is now available in Manning Early Access Program.

Multiplayer Game Development in Rust teaches you to construct your own multiplayer game. You’ll build a simple game client, but the real work happens on the backend. Chapter-by-chapter, you’ll add scalability, persistence, benchmarking, and tracing to support game features like real-time multiplayer scorekeeping, leader boards, and server-to-client messaging. Along the way, you’ll get pro tips about what makes Rust so great for game development, and you’ll work with state-of-the-art technologies that take full advantage of the cloud. Best of all, everything you learn will apply to any application that requires real-time server technology.


At the moment, 4 of 12 chapters are available:

- Introducing Rust in Games
- Building a Game Client
- Building a Game Server
- Making a Multiplayer Client

The book is estimated to be finished in early 2023.

[@tesselode](https://twitter.com/tesselode) shared [an article](https://tesselode.github.io/articles/audio-libraries-considered-challenging) about
the difficulties of making audio libraries:

I develop a game audio library called

[Kira]. Here’s some of the hard parts I’ve figured out. If you decide to make an audio library for some reason, learn from my experimentation! <…> Making audio libraries is hard. I don’t know the best way to do it. This is just what I’ve tried and how it went for me.

*Discussions: /r/rust*

## Tooling Updates [#](https://gamedev.rs#tooling-updates)

[Bloom3D](https://gamedev.rs/news/034/bloom3d) is a minimalist web app for 3D modeling that’s built in Rust.

Bloom is powered by a custom game engine called [ koi](https://gamedev.rs/news/034/koi) that is open-sourced
on GitHub.

This month [@kettlecorn](https://twitter.com/kettlecorn) released a new version of
[Bloom3D](https://bloom3d.com) that adds a variety of new features including a
rectangle tool, move tool, and OBJ export.
Check out the [Twitter announcement thread](https://twitter.com/kettlecorn/status/1529193509462360065) for an overview
and videos of all the new features.

![Graphite](../../assets/cc4ed2efaab6bf79.png)


Graphite ([website](https://graphite.rs), [GitHub](https://github.com/GraphiteEditor/Graphite),
[Discord](https://discord.graphite.rs), [Twitter](https://twitter.com/GraphiteEditor)) is a free,
in-development raster and vector 2D graphics editor. It will be powered by a
node graph compositing engine that supercharges your layer stack, providing a
completely non-destructive editing experience.

-
Spring cleaning: The past month’s Sprint 15 work has focused mostly on technical debt cleanup, documentation, and bug fixes around the frontend. That continues with the Rust backend next month.

-
A radiant gradient: The Gradient tool now supports radial styles in addition to linear.

-
New blog post:

[Learn about the plans](https://graphite.rs/blog/distributed-computing-in-the-graphene-runtime/)for distributed computing across many CPUs and GPUs with Graphene, the Rust-based node graph engine and renderer that will power Graphite.

Open the [Graphite editor](https://editor.graphite.rs) in your browser to give it a try
and share your creations with #MadeWithGraphite on Twitter.

## Library Updates [#](https://gamedev.rs#library-updates)

[bevy_mod_scripting](https://github.com/makspll/bevy_mod_scripting) by @makspll is a brand new Bevy plugin
enabling multi-language scripting (currently in Lua and Rhai).

The plugin is in early stages but as of now supports:

- Handling events at multiple points of your stage pipeline.
- Sending events to specific, or all scripts.
- Setting event priority to order your callbacks.
- Defining custom state and APIs at initialization.
- Sending run-time error events (to for example show them in an in-game console).
- One-shot scripts.

General Bevy API support is under-way so stay tuned!

![bevy_silk logo](../../assets/e16c91cf98c12cd4.png)


[bevy_silk](https://github.com/ManevilleF/bevy_silk) by @[ManevilleF](https://twitter.com/ManevilleF) is a cloth physics plugin for Bevy.

Apply cloth physics to any mesh, by adding a single component to your entity!

Features:

- Collision support using
[bevy_rapier](https://github.com/dimforge/bevy_rapier) - Global and per-entity physics customization
- Dynamic smooth and flat normals
- Wind forces
- Custom cloth anchors

The library is fully documented and the repository provides various usage examples.

*Discussions: Twitter*

[bevy_asset_loader](https://github.com/NiklasEi/bevy_asset_loader) by [@nikl_me](https://twitter.com/nikl_me) is a Bevy plugin that helps with asset
loading and asset organisation. It greatly reduces boilerplate code for
loading states and can resolve asset configuration at run time.

This month, version `0.11.0`

was released. It supports loading lists of files
as `Vec<HandleUntyped>`

or `Vec<Handle<T>>`

. This is an alternative to loading
folders, which is not supported on the web. You can now track the loading
progress of your assets with [iyes_progress](https://github.com/IyesGames/iyes_progress) and build loading bars.
Integrating with [iyes_loopless](https://github.com/IyesGames/iyes_loopless) gives you some benefits of stageless
scheduling in current Bevy. Additionally, the loading of assets fields
without attributes was improved. It now uses the `FromWorld`

trait
instead of `Default`

.

More improvements will likely follow for the dynamic asset story. One goal is to allow loading any custom values as dynamic assets.

[bevy_kira_audio](https://github.com/NiklasEi/bevy_kira_audio) by [@nikl_me](https://twitter.com/nikl_me) is an alternative audio
plugin for Bevy. It uses [Kira](https://github.com/tesselode/kira) to play and control
game audio.

This month saw the release of version `0.10.0`

. The plugin
now uses the latest Kira release, which was a major rewrite.
The audio channel API is improved by making all channels
resources in Bevy’s ECS and sounds can be directly loaded
from asset files with settings like their volume, playback
rate, or panning. Additionally, the audio backend can now
be configured before creation through a settings resource.

[Sparsey](https://github.com/LechintanTudor/sparsey) by [@LechintanTudor](https://github.com/LechintanTudor) is a sparse set-based Entity Component System
with beautiful and concise syntax.

The latest release, 0.8.0, adds some convenience panicking functions for
borrowing resources and a method for resetting a `World`

to its default state
without having to recreate it.

[Notan](https://github.com/Nazariglez/notan) is a simple and portable layer designed to create your own multimedia
apps on top of it without worrying about platform-specific code.

The main goal is to provide a set of APIs and tools that can be used to create your project in an ergonomic manner without enforcing any structure or pattern, always trying to stay out of your way. The idea is that you can use it as a foundation layer or backend for your next app, game engine, or game.

The latest version [v0.4](https://github.com/Nazariglez/notan/releases/tag/v0.4.0) adds [touch support](https://nazariglez.github.io/notan-web/examples/input_touches.html) and fixes some minor bugs.

[carrier-pigeon](https://github.com/MitchellMarinoDev/carrier-pigeon) by [@MitchellMarinoDev](https://github.com/MitchellMarinoDev) is a rusty networking library for games.
It builds on the standard library’s TcpStream and UdpSocket types
and handles all the serialization, sending, receiving, and deserialization.
This way you can worry about what to send,
and pigeon will worry about how to send it.
This also allows you to send and receive different types of messages independently.

[bevy-pigeon](https://github.com/MitchellMarinoDev/bevy-pigeon) is a Bevy plugin for carrier-pigeon.

[bong](https://github.com/MitchellMarinoDev/bong) is a combination of breakout and pong
that showcases bevy-pigeon and carrier-pigeon.

## Popular Workgroup Issues in GitHub [#](https://gamedev.rs#popular-workgroup-issues-in-github)

## Other News [#](https://gamedev.rs#other-news)

- Other game updates:
- After the initial release of
[BITGUN](https://store.steampowered.com/app/1673940/BITGUN),[LogLogGames](https://loglog.games)released a[bunch of updates packed with various bugfixes and improvements](https://store.steampowered.com/news/app/1673940). [Gravity Well](https://github.com/thebracket/gravity_well)is a simple two-player (shared keyboard) game in which you collect salvage and try not to fall into a black hole that can be played online[here](https://bfnightly.bracketproductions.com/gravity_well).[Flesh](https://store.steampowered.com/app/1660850/Flesh)got a[new enemy type](https://twitter.com/Im_Oab/status/1523210359045206017), new[UI’s fade in/out](https://twitter.com/Im_Oab/status/1525249464562491393), and[damage animation for enemies](https://twitter.com/Im_Oab/status/1529400914364465153).[Grocery Bagger 9000](https://reddit.com/r/rust_gamedev/comments/uxz0oz/grocery_bagger)is a WIP Tetris-like puzzler built with Bevy.

- After the initial release of
- Other tooling updates:
[clymene](https://github.com/lucas-miranda/clymene)by[@LukeRaccoon](https://twitter.com/LukeRaccoon)is a CLI atlas generation tool that doesn’t just outputs a packed image, but also a data set about its sources, which can be either static images or animations.

- Other learning material updates:
- The Unofficial Bevy Cheatbook by got
[a WIP chapter about rendering](https://bevy-cheatbook.github.io/gpu/intro.html). [@scvalex](https://twitter.com/scvalex)shared a[blog post](https://scvalex.net/posts/63)about how the NixOS flake for Rust/egui/eframe/glutin/OpenGL[looks like](https://gitlab.com/scvalex/sixty-two/-/tree/flake-blogpost).[@ychshn](https://twitter.com/ychshn)shared a live-stream recording[“Let’s Code Snake with Rust and WASM”](https://youtu.be/iR7Q_6quwSI).- PhaestusFox added a bunch of new videos
to their
[“Bevy Basics”](https://youtube.com/playlist?list=PL6uRoaCCw7GN_lJxpKS3j-KXuThRiSXc6)YouTube series.

- The Unofficial Bevy Cheatbook by got
- Other library updates:
[mmap_cache](https://crates.io/crates/mmap-cache)is a low-level API for a memory-mapped cache of a read-only key-value store.[crevice v0.10](https://github.com/LPGhatguy/crevice/blob/main/CHANGELOG.md#0100---2022-05-26)brings mint integration and a couple of API improvements.[glyphon](https://crates.io/crates/glyphon)provides a simple way to render 2D text with wgpu.[egui 0.18](https://reddit.com/r/rust/comments/ugefgv/egui_018)was released, with the ability to embed 3D inside egui, table and date picker widgets, better text contrast in bright mode, and more.- Following the release of egui v0.18,
[bevy_egui 0.14](https://twitter.com/penicillin_duck/status/1520703733755166720)and[puffin_egui 0.15.0](https://twitter.com/ernerfeldt/status/1524368923931590657)were published. [bevy_puffin](https://github.com/mvlabat/bevy_puffin)integrates the[puffin](https://github.com/EmbarkStudios/puffin)instrumentation profiler with Bevy.[bevy_rosc](https://github.com/DrLuke/bevy_rosc)integrates[rosc](https://github.com/klingtnet/rosc)- an Open Sound Control library - into Bevy.[bustsuri](https://github.com/NemuiSen/bustsuri)is a Bevy asset that provides 2D collision detector and kinematics.- The Bevy engine
[started collaborating](https://reddit.com/r/rust/comments/umwjt4/bevy_and_dioxus_are_collaborating_on_stretch2)with[@dioxuslabs](https://twitter.com/dioxuslabs)on a flexible, high-performance, cross-platform UI layout library[sprawl](https://github.com/DioxusLabs/sprawl)(based on abandoned[stretch](https://github.com/vislyhq/stretch)).


## Discussions [#](https://gamedev.rs#discussions)

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[Graphite is looking for contributors](https://github.com/GraphiteEditor/Graphite/issues/202)to help build the new node graph and 2D rendering systems.[winit’s “difficulty: easy” issues](https://github.com/rust-windowing/winit/issues?q=is%3Aopen+is%3Aissue+label%3A%22difficulty%3A+easy%22).[Backroll-rs, a new networking library](https://github.com/HouraiTeahouse/backroll-rs/issues).[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[A/B Street’s “good first issue” issues](https://github.com/a-b-street/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/D-Good-First-Issue).

## Jobs [#](https://gamedev.rs#jobs)

[DIMS](https://dims.co/jobs)(Stockholm/Remote): Various roles, open applications accepted.[Embark Studios](https://careers.embark-studios.com/jobs)(Stockholm/Hybrid Remote): Various roles, open applications accepted.

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!

**Discuss this post on**:
[/r/rust_gamedev](https://reddit.com/r/rust_gamedev/comments/v7xxr7/this_month_in_rust_gamedev_34),
[Twitter](https://twitter.com/rust_gamedev/status/1534619187477467138),
[Discord](https://discord.gg/yNtPTb2).