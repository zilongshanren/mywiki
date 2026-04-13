---
title: 'This Month in Rust GameDev #47 - June 2023'
url: https://gamedev.rs/news/047/
author: Rust GameDev WG
published: '2023-08-01'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 47th issue of the Rust GameDev Workgroup’s
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

[Announcements](https://gamedev.rs/news/047/#announcements)[Game Updates](https://gamedev.rs/news/047/#game-updates)[Engine Updates](https://gamedev.rs/news/047/#engine-updates)[Learning Material Updates](https://gamedev.rs/news/047/#learning-material-updates)[Tooling Updates](https://gamedev.rs/news/047/#tooling-updates)[Library Updates](https://gamedev.rs/news/047/#library-updates)[Other News](https://gamedev.rs/news/047/#other-news)

## Announcements [#](https://gamedev.rs#announcements)

The 28th Rust Gamedev Meetup took place in June. You can watch the recording
of the meetup [here on Youtube](https://youtube.com/watch?v=1DiA3OYqvqU).

The schedule:

- Blade by
[@kvark](https://github.com/kvark) - Graphite by
[@Keavon](https://github.com/Keavon) - Digital Extinction by
[@Indy2222](https://github.com/Indy2222/) - Bevy Jam #3 Games by
[@AngelOnFira](https://github.com/AngelOnFira)

The meetups take place on the second Saturday of every month via the [Rust
Gamedev Discord server](https://discord.gg/yNtPTb2) and are also [streamed on
Twitch](https://twitch.tv/rustgamedev).

## Game Updates [#](https://gamedev.rs#game-updates)

![flesh preview](../../assets/97a345b4ec127e56.gif)

[Flesh](https://store.steampowered.com/app/1660850/Flesh/) by [@im_oab](https://twitter.com/im_oab) is a 2D-horizontal shmup game with hand-drawn animation,
an organic/fleshy theme and a unique story. It is implemented using [Tetra](https://github.com/17cupsofcoffee/tetra).
The game’s development has finished and will be released soon. The last update
before release includes:

- Intro/Ending/End credits animation.
- Add a variant version of Conway’s Game of Life as background.
- Improve effect in the gameplay with distortion shaders.
- Update the demo build with improved graphics and performance.

![In-game screenshot of a real-time render of a modular gridmap-based spaceship interior](../../assets/5823faaabd923b99.png)

[Space Frontiers](https://github.com/starwolves/space) ([GitHub](https://github.com/starwolves/space), [Discord](https://discord.gg/yYpMun9CTT), [Twitter](https://twitter.com/starwolvesstar), [Reddit](https://reddit.com/u/StarwolvesStar), [Steam Group](https://steamcommunity.com/groups/starwolvescommunity))
by [Starwolves](https://starwolves.io) is an online moddable sci-fi action RPG community game
simulating space (and spaceships) in 3D.

By the end of last year, the client was made with Godot. Shortly after that the
decision was made to replace the Godot project with a [Bevy Engine](https://bevyengine.org/) client.

Rust and Bevy are now used for both server and client.
There are a lot of advantages such as sharing libraries and neat code replication,
reducing code overhead.
In fact, both the server and client are now developed in [the same virtual workspace](https://github.com/starwolves/space).

The client includes a new camera perspective from top-down isometric to 1st person.
A new 3D dynamic gridmap framework has been successfully implemented in ECS.
The prototype includes an in-game map editing tool with the ability to export to
file.
Inspired by the videogame “System Shock”.
There is a recently uploaded [showcase video](https://youtu.be/Qr_in7tUxAM).

The project is commercial, [open-source](https://github.com/starwolves/space) and has a proprietary license.
There is a milestone for a license change to free open-source.

[Starwolves.io Bulletin Board](https://starwolves.io) was launched half a year ago.
There are 25~ registrants left that can receive a permanent unique forum group/title.

*Discussions: StarWolves.io Bulletin Board*

### Digital Extinction [#](https://gamedev.rs#digital-extinction)

![Building Placement in Digital Extinction](../../assets/5fea97d072c07638.jpeg)

[Digital Extinction](https://de-game.org) ([GitHub](https://github.com/DigitalExtinction/Game), [Discord](https://discord.gg/vHMFuCWGSX),
[Reddit](https://reddit.com/r/DigitalExtinction)) by [@Indy2222](https://github.com/Indy2222/) is a 3D real-time strategy game made with
[Bevy](https://bevyengine.org).

The most notable updates are:

- nightly versions are automatically built and published on
[de-game.org](https://de-game.org/)and elsewhere, - significant progress has been made on multiplayer and networking,
- animated arrows on terrain are displayed for selected factories, indicating the path from the units’ spawn points to their delivery locations,
- semi-transparent square markers are drawn on the terrain around selected buildings,
- health bars are briefly displayed above units and buildings when they take damage or their health changes,
- the implementation and design of the “Energy” have started to take shape,
- the head-up display (HUD) shows the total battery charge and the number of selected units and buildings,
- the main theme song plays in a loop, the volume of the music can be configured,
- the aspect ratio of the minimap matches that of the game map,
- the option to invert camera zooming has been added to the configuration,
- the
[documentation](https://docs.de-game.org/)has been converted to mdBook.

See [gameplay](https://youtu.be/aRk65kyIEes) screen recordings on YouTube.

A more detailed July update is available [here](https://mgn.cz/blog/de09/).

### Tribes [#](https://gamedev.rs#tribes)

![Tribes preview](../../assets/514425ef4aefe889.jpg)


Tribes (working title) by [@uvizhe](https://github.com/uvizhe) is a turn-based strategy game about
tribes of hunters and gatherers. It’s being developed using Bevy.

The [first devlog](https://uvizhe.im/posts/tribes-p1/) introduces the game, outlines its current state and
future plans, accompanied by some thoughts from the developer.

*Discussions:
/r/rust_gamedev,
Twitter,
Mastodon*

[Way of Rhea](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n47) is a puzzle game with hard puzzles but forgiving
mechanics being produced by [@masonremaley](https://twitter.com/masonremaley) in a custom Rust engine.
You can support development by [checking out the free demo and wishlisting on Steam](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n47)
or [signing up for the mailing list](https://anthropicstudios.com/newsletter/signup/tech)!

Recent updates:

- Puzzle design and layout complete!
- Continued work on polish, working towards a closed beta
- Work continued on native
[Linux & Steam Deck port](https://twitter.com/AnthropicSt/status/1683955327711211520), the port is unfinished but playable - Increased staff throw velocity to make it easier to throw staves off ledges
- Various performance improvements (separate spatial hash for interactive objects)
- Way of Rhea will be part of the
[Cerebral Puzzle Showcase](https://www.cerebralpuzzleshowcase.com/)August 3rd-7th!

![Veloren visual comparison](../../assets/391afb5d78424a75.jpg)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In June, Veloren prepared for an upcoming release coming in July. Work included various fixes, charms, one-way walls, ip address anonymization in logs, the addition of the frost gigas boss in game, savanna hut updates, plant creatures, cyclops, and much more.

Ongoing work is happening on ship movement, pet commands, Terracotta ruins, dwarven quarry, coastal towns, clifftown rework, and axe skills. Work is happening to add physics interactions that increase your height as you’re gliding. This includes thermal and ridge lifts.

June’s full weekly devlogs: “This Week In Veloren…”: [#211](https://veloren.net/devblog-211), [#212](https://veloren.net/devblog-212).

## Engine Updates [#](https://gamedev.rs#engine-updates)

![macroquad](../../assets/60736be53e5d38c2.gif)

Macroquad got ported to miniquad-0.4, supporting Metal on Mac and IOS.

On the surface all the macroquad API stayed exactly the same, but with
`use macroquad::miniquad::*`

being such a breaking change - major version
number was bumped. Major version bump made possible to fix a few
long-lasting issues, check the [full changelog](https://macroquad.rs/articles/macroquad-0-4/)
for all the changes.

![godot-rust GDExtension logo](../../assets/f42ae8e5d070a008.png)


In the last few weeks of gdext development, the [GDExtension
API](https://github.com/godot-rust/gdextension) breaks in Godot’s recently released [4.1
version](https://godotengine.org/article/godot-4-1-is-here/). Migration is mostly done, several FFI bugs have been
addressed on the way.

The godot-rust book now [has a “Hello World” tutorial](https://godot-rust.github.io/book/gdext) + guides on
compatibility and selecting Godot version.

Noteworthy features:

- Vector swizzling
- Signals with parameters
- Rust-native APIs for Rect2, Aabb, and Plane
- ToVariant/FromVariant derives
- Godot native structures

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

### Bevy Rendering Demystified [#](https://gamedev.rs#bevy-rendering-demystified)

![Bevy Rendering Demystified Thumbnail](../../assets/070edfaadb0b69e7.png)


[@logicprojects](https://www.youtube.com/@logicprojects) published a [video](https://youtu.be/5oKEPZ6LbNE) covering the
details of Bevy’s rendering systems. Specifically, he covered the engine’s
internal implementation of UI Rendering to show how data flows from the ECS
world down to the final wgpu draw calls.

### Procedural Trees in Ambient [#](https://gamedev.rs#procedural-trees-in-ambient)

![Procedural tree in Ambient](../../assets/25b35798efab05f0.jpg)


[@mebyz](https://github.com/mebyz) authored a set of articles “building mmo-ready procedural trees using
Ambient engine”. The three ([1](https://medium.com/@emmanuel.botros/webgpu-wasm-rust-building-mmo-ready-procedural-trees-using-ambient-engine-part-1-2359225b592), [2](https://medium.com/@emmanuel.botros/webgpu-wasm-rust-building-mmo-ready-procedural-trees-using-ambient-engine-part-2-60ccce4c6adc),
[3](https://medium.com/@emmanuel.botros/webgpu-wasm-rust-building-mmo-ready-procedural-trees-using-ambient-engine-part-3-5a217ecdcabe)) posts cover a week’s worth of explorations into simple
pseudo-random procedural ecosystem generation (trees, mushrooms, etc)
system/strategy for Ambient.

## Tooling Updates [#](https://gamedev.rs#tooling-updates)

[Rerun](https://rerun.io) ([Discord](https://discord.gg/npTFxYR9), [GitHub](https://github.com/rerun-io/rerun)) is an open-source SDK
for logging complex visual data paired with a visualizer for exploring that data
over time. While its primary focus is on robotics and computer vision, it can be
useful for all kinds of rapid prototyping & algorithm development.

[v0.7.0](https://github.com/rerun-io/rerun/releases/tag/v0.7.0) is out now, but it turned out a little bit smaller:

A few of the biggest highlights:

- Much more powerful transformation logging
- any affine transforms works now!
- supports many more formats and shows them in the viewer as-is

- Better color mapping range detection for images and tensors
- Add support for motion JPEG via the new jpeg_quality parameter to log_image
- Many small improvements to samples & documentation

There’s a growing community on [Discord](https://discord.gg/npTFxYR9) waiting for you to join in
case you have any questions, comments or just want to follow the latest
development. The [GitHub project](https://github.com/rerun-io/rerun) is MIT/Apache licensed and open to
contribute for everyone, be it with suggestions, bugs or PRs.

## Library Updates [#](https://gamedev.rs#library-updates)

![Example code written with posh, simplified from the hello triangle example](../../assets/1e3d690267899a0e.jpg)


[ posh](https://github.com/leod/posh) is a crate that seamlessly integrates a graphics library with an
embedded functional shading language. It is a proof of concept that aims to
demonstrate that graphics programming can be both type-safe and ergonomic.

With `posh`

, shaders are written in plain Rust (with some caveats). Procedural
macros are only required for defining custom vertex and uniform types.

The core component of `posh`

is the `Program<U, V, F>`

type, which acts as a
bridge between the shading language and the graphics library. This type
represents a compiled shader and serves as the entry point for draw calls. By
explicitly carrying the types `U`

(uniform interface), `V`

(vertex shader
interface), and `F`

(fragment shader interface), `posh`

enables static
verification, ensuring that the data provided in draw calls matches the shader’s
signature.

For simplicity, `posh`

currently targets OpenGL ES 3.0. Although it is an
experimental project, its authors hope to inspire the community to further
explore how static typing can elegantly bridge the gap between host code and
shader code.

For more details, check out the [examples](https://github.com/leod/posh/tree/main/examples) or the authors’ [blog
post](https://leod.github.io/rust/gamedev/posh/2023/06/04/posh.html).

![Boytacean preview](../../assets/e46fc9228a0df01e.gif)


[Boytacean](https://github.com/joamag/boytacean/) by [@joamag](https://github.com/joamag) is a web-based Game Boy Color emulator (and
library) written in Rust.

Major features include:

- Full Game Boy and Game Boy Color emulation.
- Web (using WebAssembly) and SDL frontends.
- Ultra-fast performance.
- Accurate PPU emulation.
- Game Boy Printer emulation.
- and many others…

## Other News [#](https://gamedev.rs#other-news)

- Other game updates:
[Idu](https://epcc.itch.io/idu)is a game about growing simulated plants, recent updates include addition of a GPU particle system.[Nanovoid](https://store.steampowered.com/app/2326430/NANOVOID/)is a 2D tactical space shooter game, most recent features have been added to the ship editor.[Cells](https://github.com/psincf/Cells)is a singleplayer game inspired by[agar.io](https://agar.io/).[MS80](https://ms80.space/)is a game about scavenging parts and creating things with them to survive alien attacks. MS80 now does basic simulation of thermodynamics.[Maginet](https://evrimzone.itch.io/maginet)updated their game interface and debuted the editor update![Combine And Conquer](https://martinbucksoftware.itch.io/combine-and-conquer)new release fixes issues with item rendering.[rust-drive-ai](https://github.com/bones-ai/rust-drive-ai)is a self driving AI simulation game built in span of 30 days that uses the Bevy engine. In addition, under the hood the cars are controlled using neural networks and trained by a genetic algorithm.[The Station](https://www.youtube.com/watch?v=fecn1qPNu3c)is a brand new NASA-punk survival game.[Turtletime](https://github.com/mikeder/turtletime)is a multiplayer competitive turtle game built using the Bevy and Matchbox.[Tiny Glade](https://pouncelight.games/tiny-glade/)updated path detailing.[Fish Folk](https://www.kickstarter.com/projects/erlendsh/fish-folk/posts/3841752)is collection of arcade style multiplayer games where you dive deep in the ocean!

- Other learning material updates:
[Game Dev Graphics](https://www.youtube.com/watch?v=Hqi8QREXwrE)posted a series of 3D graphics tutorials in Rust from scratch.[Maciej Główka](https://maciejglowka.com/contact/)brings updates for map generation to his[Bevy roguelike tutorial](https://maciejglowka.com/blog/bevy-roguelike-tutorial-devlog-part-10-room-placement/).[Learning Game Dev](https://affanshahid.dev/posts/learning-game-dev-bevy-3/)brings a third edition to their tutorials with building a platformer with Bevy.

- Other engine updates:
[Bitang](https://github.com/aedm/bitang)is a new framework for demoscene productions.

- Other library updates:

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!