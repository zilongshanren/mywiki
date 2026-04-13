---
title: 'This Month in Rust GameDev #35 - June 2022'
url: https://gamedev.rs/news/035/
author: Rust GameDev WG
published: '2022-07-07'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 35th issue of the Rust GameDev Workgroup’s
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

[Announcements](https://gamedev.rs/news/035/#announcements)[Game Updates](https://gamedev.rs/news/035/#game-updates)[Learning Material Updates](https://gamedev.rs/news/035/#learning-material-updates)[Engine Updates](https://gamedev.rs/news/035/#engine-updates)[Tooling Updates](https://gamedev.rs/news/035/#tooling-updates)[Library Updates](https://gamedev.rs/news/035/#library-updates)[Other News](https://gamedev.rs/news/035/#other-news)[Discussions](https://gamedev.rs/news/035/#discussions)[Requests for Contribution](https://gamedev.rs/news/035/#requests-for-contribution)[Jobs](https://gamedev.rs/news/035/#jobs)

## Announcements [#](https://gamedev.rs#announcements)

![text logo](../../assets/2d531cd7de6f2d8f.jpeg)


The Rust Gamedev Podcast features interviews with indie game developers creating titles with the Rust programming language. It covers technical topics as well as the business of open source and commercial indie games development.

In June, [the ninth episode](https://rustgamedev.com/episodes/interview-with-carter-anderson-bevy) was released. It’s a chat with Carter
Anderson about the [Bevy engine](https://bevyengine.org/), and a dive into its history.

Listen and Subscribe from the following platforms:
[Rust GameDev Podcast (simplecast)](https://rustgamedev.com/),
[Apple Podcasts](https://podcasts.apple.com/gb/podcast/rust-game-dev/id1526304768),
[Spotify](https://open.spotify.com/show/7HRfGnTcXkLkQd9fxJbDGj),
[RSS Feed](https://feeds.simplecast.com/C6NQglnL),
or [Google Podcasts](https://podcasts.google.com/feed/aHR0cHM6Ly9mZWVkcy5zaW1wbGVjYXN0LmNvbS9DNk5RZ2xuTA).

### Rust GameDev Meetup [#](https://gamedev.rs#rust-gamedev-meetup)

![Gamedev meetup poster](../../assets/679d7dd5e0724dc0.png)


The 17th Rust Gamedev Meetup took place in June. You can watch the recording of
the meetup [here on Youtube](https://youtu.be/drcX3dCS5MY). Here was the schedule from
the meetup:

- Choir -
[@kvark](https://twitter.com/kvark) - RustConf Arcade Cabinet -
[@carlosupina](https://twitter.com/carlosupina) - retime -
[@Togg](https://github.com/ZKpot) - Graphite -
[@GraphiteEditor](https://twitter.com/graphiteeditor)

The meetups take place on the second Saturday every month via the [Rust Gamedev
Discord server](https://discord.gg/yNtPTb2) and are also [streamed on
Twitch](https://twitch.tv/rustgamedev). If you would like to show off what you’ve been
working on at the next meetup on [July 9th](https://everytimezone.com/s/92d2228b), fill out [this
form](https://forms.gle/BS1zCyZaiUFSUHxe6).

![Aaron: a drawing of a humanoid fox](../../assets/69b9148455f32b4a.png)

[the mascot of the jam](https://gamedev.rs/blog/rustyjam-02)

The [second Rusty Jam](https://gamedev.rs/blog/rustyjam-02) just ended!
[17 games](https://itch.io/jam/rusty-jam-2/entries) were completed and submitted
over the one-week jam. The games were rated by the community
and the top three games are:

- 🥇
[“Chick the Dog”](https://uriopass.itch.io/chick-the-dog)by Uriopass - 🥈
[“A walk around the block”](https://ramirezmike2.itch.io/a-walk-around-the-block)by ramirezmike - 🥉
[“Fight for the Frontier”](https://logicprojects.itch.io/fight-for-the-frontier)by rand0m and logicprojects

The Rusty Jam will be back, so stay tuned on
[the Rusty Jam Discord Server](https://discord.gg/jZtz6y9gCJ) for future updates!

### RustConf Arcade Cabinet [#](https://gamedev.rs#rustconf-arcade-cabinet)

![arcade cabinet](../../assets/91d09779e0682a8e.jpg)


[Carlo](https://twitter.com/carlosupina) is building a custom arcade cabinet that will be at
RustConf 2022 in Portland. It is an opportunity for Rust game developers to
share their games with the broader community. If you are interested in getting
your game on the cabinet, read [this Twitter thread](https://twitter.com/carlosupina/status/1523715837726961664) and
fill out the [interest form](https://forms.gle/onFm5fCygdbiArqJ7).
The arcade cabinet has been assembled and painted. He is currently in the process
of helping developers get their games playable on the machine. If you have a Bevy
game, you can use the [bevy-rust-arcade crate](https://crates.io/crates/bevy-rust-arcade) to quickly get
your game compatible. Deadline is the end of July!
You can find the latest update [here](https://twitter.com/carlosupina/status/1539032439284240386).

## Game Updates [#](https://gamedev.rs#game-updates)

![hgs_screen](../../assets/6768d5bf3b1b368e.jpg)


[Hydrofoil Generation](https://hydrofoil-generation.com/)
([Steam](https://store.steampowered.com/app/1448820/Hydrofoil_Generation/), [Facebook](https://facebook.com/HydrofoilGenerationSailing/), [Discord](https://discord.gg/DtKgt2duAy/))
is a realistic sailing/foiling inshore simulator in development for PC/Steam
that will put you in the driving seat of modern competitive sailing.
Hydrofoil Generation is based on a custom-made DirectX 11 based engine in
Rust.

June saw a lot of features added to the game, most notables being “New TV
Overlays”, “Control Assists”, “Ropes Rendering” plus several physics
improvements. Stefano Casillo, the developer went through all of them in
a recent [devlog](https://youtu.be/AqwqyL9RqAk).

Work in July will focus on the physics implementation of a new boat, a foiling multihull coming with her own set of new challenges.

Hydrofoil Generation is targeting a Q4 2022 Early Access release on Steam.

![RuggRogue gameplay screenshot](../../assets/e27e6eef32ac3819.png)


[RuggRogue](https://tung.github.io/ruggrogue/) by [@tung](https://github.com/tung/) is a simple web-playable roguelike, inspired by the
[Rust Roguelike Tutorial](https://bfnightly.bracketproductions.com/) and made using Rust and SDL.
It can be played natively on Windows and Linux,
and in the browser thanks to Emscripten.

Features:

- Discover new monsters and equipment the deeper you go.
- Hunger and regeneration: stay fed and stay healed!
- Choose between graphical tiles and ASCII display.
- Menu-based UI with hotkeys.
- Auto-run to quickly follow corridors and cross open space.
- Save and load system.
- New Game Plus mode!

The source code is complemented by the
[RuggRogue Source Code Guide](https://tung.github.io/ruggrogue/source-code-guide/),
a 23-chapter technical web book covering the ideas, algorithms, and structure of
the code.

*Discussions:
/r/rust_gamedev,
/r/roguelikes*

![games collage](../../assets/76ed95282477cf47.jpg)


Rust Game Ports is a port of several games to Rust/pure-Rust game engines.

This month the last planned port has been completed; the games are:

- Boing (Pong clone, ported to
[ggez](https://github.com/ggez/ggez)) - Cavern (Bubble Bobble clone, ported to
[Macroquad](https://github.com/not-fl3/macroquad)) - Rusty Roguelike (from the
[Hands-on Rust book](https://pragprog.com/titles/hwrust/hands-on-rust); ECS ported to[Bevy](https://github.com/bevyengine/bevy)) - Soccer (Sensible Soccer clone, ported to
[Fyrox](https://github.com/FyroxEngine/Fyrox))

A Bevy ECS tutorial, based on Rusty Roguelike, has been published, and it’s announced in this newsletter.

### vetovoima [#](https://gamedev.rs#vetovoima)

![vetovoima gravity manipulation GIF](../../assets/a50e491ef548c11a.gif)

[vetovoima](https://yourmagicisworking.itch.io/vetovoima) by [@MatiasKlemola](https://twitter.com/MatiasKlemola) is an arcade game
where you control gravity!

The world is a hollow circle with a star in the center. You’re the Yellow Block and your goal is to navigate through shifting debris to the Tall Blue Block before the time runs out. The challenge is to survive the chaos that ensues from changes to gravity.

vetovoima is built with the Bevy engine using Rapier for physics and Lyon for rendering (via Bevy plugins).

Source available on [GitHub](https://github.com/klemola/vetovoima).

[Botnet](https://github.com/JMS55/botnet) is an upcoming programming-based multiplayer game,
where you write scripts (compiled to WebAssembly) to control robots.
Coordinate your bots to gather resources, build new industries,
and expand your control of the server.

This month saw the start of the project, and a majority of the foundational
code was written. Next month we’ll be adding more features, and aim to flesh out
the game beyond [basic pathfinding and resource harvesting](https://github.com/JMS55/botnet/blob/master/example_bot/src/lib.rs).

Interested in contributing? Head over to the
[github discussion page](https://github.com/JMS55/botnet/discussions/categories/ideas) and suggest some ideas!

![Screenshot of a level in Star Machine](../../assets/f5988a94a584de3b.png)


[Star Machine](https://twitter.com/Seldom_SE/status/1532909654681849856) by [@Seldom_SE](https://twitter.com/Seldom_SE) is a puzzle game built in Bevy, where
you wire together components to escape each level.

Although its development is currently inactive, the developer
recently made [a video demo](https://twitter.com/Seldom_SE/status/1532909654681849856) of the early levels.

![Screenshot of a Quoridor-rs gameplay](../../assets/e21339a142b7fbce.png)


[Quoridor-rs](https://github.com/baehyunsol/Quoridor-rs) by [@baehyunsol](https://github.com/baehyunsol) is a [Quoridor](https://en.wikipedia.org/wiki/Quoridor) game implemented in
[Macroquad](https://github.com/not-fl3/macroquad).

Quoridor is a 2-4 player strategy board game. Each player has a pawn. They move the pawn or place a wall each round. The objective of the game is to move the pawn to the opposite side of the board.

The game implements most of the basic Quoridor features, but it only supports 2 players, not 3 or 4. It also doesn’t have AI players or network games.

![Gliding above a forest](../../assets/5eafc24dcec7d09d.jpg)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In June, a memory issue was found within the graphics stack. Weather is also
getting closer to completion. There is a large write-up about it in one of [this
month’s blog posts](https://veloren.net/devblog-176).

Lots of work has also gone into optimizing the Site2 system. Site2 is used to
create many different shapes around the world, such as houses in towns, or
citadels around the world. With these optimizations, it will be significantly
easier to render chunks, which will have a dramatic effect on their load time.
You can read more about these optimizations in [this blog post](https://veloren.net/devblog-178).

June’s full weekly devlogs: “This Week In Veloren…”:
[#175](https://veloren.net/devblog-175),
[#176](https://veloren.net/devblog-176),
[#177](https://veloren.net/devblog-177),
[#178](https://veloren.net/devblog-178).

![hho summer banner](../../assets/0e28fd8247388fa2.png)


[Gemdrop Games](https://twitter.com/GemdropGames) have worked with their friends at [Octosoft](https://twitter.com/RenaineGame)
to bring Shroomella to Harvest Hero Origins!

[Renaine](https://store.steampowered.com/app/662340/Renaine/) is an upcoming Action Platformer game about Aine,
an immortal Phoenix Knight.

Shroomella is a Mushroom Shroom witch aiding Aine on her quest! In Harvest Hero Origins, she uses her variety of magical mushrooms to fight off the endless Grooble hordes.

On top of that, they’re adding:

- A new map
- Two new cards
- Two new enemies
- A revised story boss fight

The game is built on the [Emerald Game Engine](https://github.com/Bombfuse/emerald).

![Chimera Rancher cover art](../../assets/622c2e79c94b0257.png)


[Chimera Rancher](https://nightlyside.itch.io/chimera-rancher) is a game where you must defend your ranch
from an angry hoard of villagers with the help of your chimera friends!

Submitted as part of [Rusty jam #2](https://itch.io/jam/rusty-jam-2) by [cdsupina](https://cdsupina.itch.io/),
[Nightly Side](https://nightlyside.itch.io/), [hedgein](https://hedgein.itch.io/), and [tigleym](https://tigleym.itch.io/). This
game was developed using the [bevy](https://bevyengine.org/) game engine.

## Engine Updates [#](https://gamedev.rs#engine-updates)

[ggez](https://github.com/ggez/ggez) by [@icefoxen](https://github.com/icefoxen), [@nobbele](https://github.com/nobbele), and [@PSteinhaus](https://github.com/PSteinhaus) is a cross-platform game
framework for making 2D games with minimum friction. It aims to implement an
API based on the LÖVE game framework.

This version has finally moved ggez away from pre-ll gfx and into the world
of [wgpu](https://github.com/gfx-rs/wgpu)! This hopefully means fewer bugs, greater stability, and easier
maintainability at the cost of some low-performance devices such as the
Raspberry Pi.

As for the user-facing API:

- Instead of module functions, you now have methods on sub-contexts, which
look like
`ctx.keyboard.is_key_pressed(key)`

. - You are now required to pass around an explicit canvas to draw onto.
`DrawParam`

now has a Z (aka layer) parameter, so you don’t have to draw objects in order.- Shaders are far easier to use, via normal Rust structs with a simple derive.

As this is a rather large update and a first release candidate, there are plenty
of bugs that are currently being fixed - please send any issues you encounter
to their [issue tracker](https://github.com/ggez/ggez/issues)!

*Discussions: /r/rust_gamedev*

[Dims](https://dims.co) ([Twitter](https://twitter.com/DimsWorlds), [Discord](https://discord.gg/Z5CAVmNE57),
[YouTube](https://youtube.com/channel/UCR5gOwS7uSl0a0dl7MLQoqg)) is a pre-alpha collaborative open-world
creation platform.
Users can hop in sessions and build a game together, allowing everyone
to bring out their inner game-maker.

June brought about several developments for the platform, including:

- Several development and testing streams, with the latest being
[a recreation of Rhodes from Red Dead Redemption 2](https://www.youtube.com/watch?v=piEAGSFx-QU)within the engine - A new audio engine with advanced real-time synthesis and composition capabilities, including network synchronisation
- Improved terrain manipulation tools, including new brushes, biome presets,
and more intuitive UI
- Choose between “Nordic Mountains” ⛰ and “Colorado Deserts” 🏜

- Various improvements to the rendering engine, including decal and billboard rendering, FBX loading, macOS support, and more
- Initial work on a versatile new scripting system, with independent threads of execution for every object

Want to try Dims out for yourself? Come join the [Discord](https://discord.gg/Z5CAVmNE57) to be
notified of future public tests, see the latest features before everyone else,
and to talk to the devs personally.

![miniquad fileopen](../../assets/bd66e099315a8051.gif)


[miniquad](https://github.com/not-fl3/miniquad/) is a safe and cross-platform rendering library
focused on portability and low-end platform support.

In versions prior to 0.3, it was virtually impossible to integrate, for
example, a big in-app payments or advertisement SDK into a Miniquad Android
game. 0.3 has solved this, giving the possibility to interop with any Java code.
The developer has posted [a write-up of this functionality](https://macroquad.rs/articles/java/) on
the macroquad site.

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

![Brontefy Me Devlog #3](../../assets/a276b6d1cc19a02c.png)


[@hedgein](https://github.com/hedgein) continues the [Brontefy Me](https://www.youtube.com/watch?v=oNxMN47tKxs) series!
In this latest devlog, she gives an update on where Brontefy Me will be
heading and why it slowed down. During a recent [stream](https://www.twitch.tv/hedgein), it
was also mentioned that [@hedgein](https://github.com/hedgein) is leaning towards hosting
a monthly Brontefy Me Game Jam for her community, as game jams give her
better accountability. Further updates will be given in her [Discord server](https://discord.gg/FnU6hxNGaP).

![Learn Bevy’s ECS by ripping off](../../assets/9c1eb55977b86e33.png)


“Learn Bevy’s ECS by ripping off someone else’s project” is a mini-book that uses
the game Rusty Roguelike from the book [Hands-on Rust](https://pragprog.com/titles/hwrust/hands-on-rust)
as a base, in order to explain Bevy’s ECS.

The idea is for a beginner to learn ECS concepts from the base book, then apply them using Bevy; the structure of the game is ideal for a gentle introduction to ECS architecture.

[@PhaestusFox](https://www.youtube.com/c/PhaestusFox) is close to finishing the [Bevy Basics](https://www.youtube.com/playlist?list=PL6uRoaCCw7GN_lJxpKS3j-KXuThRiSXc6)
[User Input](https://www.youtube.com/playlist?list=PL6uRoaCCw7GMWzJ-L2cU5ZruWkEld6a_N) mini-series.

In this 5 part mini-series, they cover how a developer can go about collecting
user input using the [Bevy](https://bevyengine.org/) game engine.

[Episode 1](https://youtu.be/pB3ERI5JtrA)is an overview of Bevy’s various input structs[Episode 2](https://youtu.be/G37yUGL3e1U)covers keyboard presses[Episode 3](https://youtu.be/1q5iQsLVGJA)covers mouse clicks and movement[Episode 4](https://youtu.be/PjLozjlOgJ4)covers gamepad buttons and joysticks[Episode 5](https://www.youtube.com/c/PhaestusFox)covers touchscreen or drawing pad strokes

## Tooling Updates [#](https://gamedev.rs#tooling-updates)

![Screen recording showing the construction of a heart shape using the Noumenal app.](../../assets/db5809a33be50cee.gif)


[Noumenal](https://noumenal.app) ([App Store](https://apps.apple.com/us/app/noumenal/id1584884105),
[Discord](https://discord.gg/PFeZQE48gG), [Twitter](https://twitter.com/noumenal_app))
by [@HackerFoo](https://hackerfoo.com) is an elegant 3D solid modeling app for iOS.

After a final stretch of performance improvements, bug fixes, and even some new features, Noumenal was released and is available on Apple’s App Store!

*Discussion: /r/rust*

![Graphite](../../assets/ecfc72ad6aa26ea7.png)


Graphite ([website](https://graphite.rs), [GitHub](https://github.com/GraphiteEditor/Graphite),
[Discord](https://discord.graphite.rs), [Twitter](https://twitter.com/GraphiteEditor)) is a free,
in-development raster and vector 2D graphics editor. It will be powered by a
node graph compositing engine that supercharges your layer stack, providing a
completely non-destructive editing experience.

June’s [sprint 16](https://github.com/GraphiteEditor/Graphite/milestone/16) focused mainly on bug fixes and big
under-the-hood changes:

- Ahead of the curve: A long-awaited refactor replaces the underlying Bézier curve data structure in alignment with requirements for Pen tool improvements and the upcoming node system.
- Sending mixed messages: The internal messaging system was upgraded to sequence the message processing in a more predictable stack-based order. A new subscription-based event broadcaster was integrated as well.
- Back on the menu: The application menu bar content definitions were moved from the JS frontend to a permanent home in the Rust backend.

Open the [Graphite editor](https://editor.graphite.rs) in your browser to give it a try
and share your creations with #MadeWithGraphite on Twitter.

![quad-gif screenshot](../../assets/2306dea4390202f2.png)


[quad-gif](https://github.com/ollej/quad-gif) by [@ollej](https://twitter.com/ollej) is a tiny library that can be used in a Macroquad game
to show a looping GIF animation. It also includes a small example binary that
displays a GIF in the middle of a window. The library can also be used as a
simple way to make an animation from a list of textures.

## Library Updates [#](https://gamedev.rs#library-updates)

[psf2](https://github.com/Ralith/psf2) is a minimal, unopinionated, no-std parser for the v2
[PC Screen Font](https://www.win.tue.nl/~aeb/linux/kbd/font-formats-1.html) bitmap font format.

PSF2 fonts are simple, compact, and readily available due to their use as Linux console fonts. They are extremely fast to draw at their intended resolution, making them a great choice to quickly get text on the screen, especially when a low-resolution, fixed-width aesthetic is desired.

The psf2 crate parses font data, exposing font size, glyph lookup, and iterators to traverse a glyph’s bitmap for easy rendering. Due to its limited scope, it is much smaller and faster than conventional text rasterizers but cannot support variable-width, anti-aliased, or shaped text.

[ezinput](https://crates.io/crates/ezinput/versions) by [@eexsty](https://github.com/eexsty) is a powerful input-agnostic library,
targeting complete support for axis and button handling in the Bevy game
engine.

EZInput strives to be simple as possible using the nifty ECS features that Bevy offers, while still being powerful and flexible without using any unsafe code. This and the previous 0.3.* releases were targeted for performance and ergonomics improvements, including a new declarative macro to allow for cleaner and smaller code.

[glam](https://github.com/bitshifter/glam-rs) is a simple and fast linear algebra crate for games and graphics.

This month version 0.21 of glam was released. Because glam is not a generic
library, when support was added for `f64`

, `i32`

, and `u32`

types back in glam
0.12, macros were used internally to avoid a lot of code duplication. This
unfortunately obfuscated the internals of glam for anyone who needed to view the
source.

As of the 0.21 release the majority of glam code is now generated using an
offline tool and committed to the repo. The macros that were used to define
glam’s internal implementation are gone. This means what users see when reading
docs or stepping through glam in the debugger is plain old Rust code. Many
functions have also been made `const fn`

removing the need for macros to create
`const`

values.

![A rendering of a fancy loft apartment](../../assets/e9c9ce99f645698f.jpg)


[kajiya](https://github.com/EmbarkStudios/kajiya/) by [@h3r2tic](https://github.com/h3r2tic) is an experimental real-time global illumination
renderer.

In June, a long-standing branch landed, bringing with it a complete overhaul of indirect lighting. The new implementation uses spatiotemporal reservoir resampling (ReSTIR) and a novel irradiance cache, bringing forth larger scenes, quicker response to lighting changes, and less noise.

A [detailed overview](https://github.com/EmbarkStudios/kajiya/blob/main/docs/gi-overview.md) of the new global illumination
techniques is available, complete with animated diagrams!

June has also seen the addition of texture compression, automatic exposure, a new display rendering transform, and a simplification of the interface. The viewer app now supports drag-and-drop of scene files, glTF models, and HDRI backdrops.

*Discussions:
twitter (0.2 release),
twitter (texture compression).*

![Notan texture to file](../../assets/895f87dff8a34eb5.gif)


[Notan](https://github.com/Nazariglez/notan) is a simple and portable layer designed to create your own multimedia
apps on top of it without worrying about platform-specific code.

The main goal is to provide a set of APIs and tools that can be used to create your project in an ergonomic manner without enforcing any structure or pattern, always trying to stay out of your way. The idea is that you can use it as a foundation layer or backend for your next app, game engine, or game.

The latest version [v0.5](https://github.com/Nazariglez/notan/releases/tag/v0.5.0) fixes multiple bugs, improves [EGUI](https://github.com/emilk/egui) support and adds
a new feature to export texture [to png](https://nazariglez.github.io/notan-web/examples/texture_to_file.html) easily.

## Other News [#](https://gamedev.rs#other-news)

- Other game updates:
[Fires of Eschaton](https://twitter.com/FiresOfEschaton/status/1534119771045826567)is a PvP focused turn-based fantasy game, currently under development.[Idu](https://twitter.com/epcc10/status/1532889644165120001)is testing out some new water physics.[Combine and Conquer](https://buckmartin.de/combine-and-conquer/2022-06-16-sound.html)has a new devlog about its sound support.[Fish Folly](https://www.reddit.com/r/rust_gamedev/comments/vi5jok/media_fish_folly_a_fyrox_showcase_game_inspired/)is a new Fyrox showcase game, inspired by Fall Guys.[Punchy](https://twitter.com/spicylobsterfam/status/1540105977810255872)is a beat-em-up spin off of[Fish Fight](https://fishfight.org/), built with Bevy.[Jungle Chess](https://www.reddit.com/r/rust_gamedev/comments/v3btkk/browser_jungle_chess_with_rust_wasm/)is a WASM implementation of a Chinese board game.[Croquet](https://twitter.com/gocroquet/status/1531336194725797889)is working on synchronized physics, using Rapier.[Bevy City](https://mungbungo.itch.io/bevy-city)is a voxel city generator, built with Bevy.[Measure Once](https://robtfm.github.io/measure_once/)is a game about cutting wood into the right shapes.[Galactic Mess](https://www.youtube.com/watch?v=DO8vwehkr38)has added new outfits and weapons.

- Other learning material updates:
[Rustacean Station](https://rustacean-station.org/episode/emil-ernerfeldt/)interviewed the developer of egui.[Rusteroids](https://www.youtube.com/playlist?list=PLFOS-Gn3aXROnSfl26esPExssd-rQw6jD)is a video tutorial series, building an asteroids clone with Rust and SDL2.[NVIDIA GPU Profiling with Rust](https://simbleau.github.io/blog/gpu-profiling-with-rust/)is an introduction on how to use NVIDIA’s NSight tools with Rust.[Practical Programming with Dr. Xu](https://www.reddit.com/r/rust/comments/vmpjcr/rust_wgpu_graphics_programming_tutorial_youtube/)has continued their WGPU tutorial series.[Anthropic Studios](https://www.youtube.com/watch?v=H0sIsrLWojs)(developers of Way of Rhea) posted a dev interview video.[Lyrapuff](https://www.youtube.com/watch?v=_PNiRGIAfY4)posted a video showing how to render a triangle with Vulkan and Rust.

- Other engine updates:
[pufferfish](https://github.com/pufferfish-rs/pufferfish)is a new, opinionated 2D game framework.

- Other tooling updates:
[GBemulator](https://github.com/p4ddy1/gbemulator)is a Game Boy emulator written from scratch.

- Other library updates:
[bevy_mod_picking](https://github.com/aevyrie/bevy_mod_picking/releases/tag/v0.7.0)released version 0.7 of their Bevy mouse picking plugin.[bevy_mod_outline](https://github.com/komadori/bevy_mod_outline)is a Bevy plugin for drawing outlines around meshes.[Bevy YOLECK](https://github.com/idanarye/bevy-yoleck)is a crate that allows Bevy games to be their own level editor.[bevy_mod_raycast](https://github.com/aevyrie/bevy_mod_raycast/releases/tag/v0.5)released version 0.5 of their raycasting plugin.[taffy](https://github.com/DioxusLabs/taffy)is a cross-platform UI layout library.


## Discussions [#](https://gamedev.rs#discussions)

[/r/rust_gamedev](https://reddit.com/r/rust_gamedev/):[“Shopping list”](https://www.reddit.com/r/rust_gamedev/comments/v8tx37/shopping_list/)(a list of things that are missing from the ecosystem)[“Hands-on Rust: Further reading”](https://www.reddit.com/r/rust_gamedev/comments/v4q4pr/handson_rust_further_reading)[“How can I start developing a 3D game engine?”](https://reddit.com/r/rust_gamedev/comments/v3z4i1/how_can_i_start_developing_a_3d_game_engine)[“Bevy or Fyrox for 3D Game Development?”](https://reddit.com/r/rust_gamedev/comments/v7svhg/bevy_or_fyrox_for_3d_game_dev)


## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[‘Are We Game Yet?’ wants to know about projects/games/resources that aren’t listed yet](https://github.com/rust-gamedev/arewegameyet#contribute).[Graphite is looking for contributors](https://graphite.rs/contribute)to help build the new node graph and 2D rendering systems.[winit’s “difficulty: easy” issues](https://github.com/rust-windowing/winit/issues?q=is%3Aopen+is%3Aissue+label%3A%22difficulty%3A+easy%22).[Backroll-rs, a new networking library](https://github.com/HouraiTeahouse/backroll-rs/issues).[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/issues).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[A/B Street’s “good first issue” issues](https://github.com/a-b-street/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/D-Good-First-Issue).

## Jobs [#](https://gamedev.rs#jobs)

[DIMS](https://dims.co/jobs)(Stockholm/Remote): Various roles, open applications accepted[Embark Studios](https://careers.embark-studios.com/jobs)(Stockholm/Hybrid Remote): Various roles, open applications accepted[Mutate](https://rustjobs.dev/featured-jobs/Mutate-Rust-Backend-Software-Engineer-7kfTlQFSagzwHhugw1p0)(Remote): Rust Backend Software Engineer

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!

**Discuss this post on**:
[/r/rust_gamedev](https://www.reddit.com/r/rust_gamedev/comments/vtrelw/this_month_in_rust_gamedev_35_june_2022/),
[Twitter](https://twitter.com/rust_gamedev/status/1545135032334950403),
[Discord](https://discord.gg/yNtPTb2).