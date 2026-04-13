---
title: 'This Month in Rust GameDev #22 - May 2021'
url: https://gamedev.rs/news/022/
author: Rust GameDev WG
published: '2021-06-09'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 22nd issue of the Rust GameDev Workgroup’s
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

[Game Updates](https://gamedev.rs/news/022/#game-updates)[Learning Material Updates](https://gamedev.rs/news/022/#learning-material-updates)[Engine Updates](https://gamedev.rs/news/022/#engine-updates)[Tooling Updates](https://gamedev.rs/news/022/#tooling-updates)[Library Updates](https://gamedev.rs/news/022/#library-updates)[Requests for Contribution](https://gamedev.rs/news/022/#requests-for-contribution)

## Rust GameDev Meetup [#](https://gamedev.rs#rust-gamedev-meetup)

![Gamedev meetup poster](../../assets/4bbf944f6684e7f2.png)


The fifth Rust Gamedev Meetup happened in May. You can watch the recording of
the meetup [here on Youtube](https://www.youtube.com/watch?v=6drrul3p_hU). The meetups take place on
the second Saturday every month via the [Rust Gamedev Discord
server](https://discord.gg/yNtPTb2), and can also be [streamed on
Twitch](https://twitch.tv/rustgamedev). If you would like to show off what you’ve been
working on in a future meetup, fill out [this form](https://forms.gle/BS1zCyZaiUFSUHxe6).

## Game Updates [#](https://gamedev.rs#game-updates)

### Flesh [#](https://gamedev.rs#flesh)

![flesh preview](../../assets/0bdc8835fd3fa491.gif)

Flesh by [@im_oab](https://twitter.com/im_oab) is a 2D-horizontal shmup game with hand-drawn animation and
organic/fleshy theme. It is implemented using [Tetra](https://github.com/17cupsofcoffee/tetra). This month’s updates
include:

- Add (internal use) level editor.
- Add new enemy types.
- Prepare to release a short demo next month for collecting feedback.

![Airship](../../assets/0fa6446d593858c9.jpg)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

Veloren’s 3rd birthday was at the end of May, on the 25th! During the month, lots of systems were overhauled. Music changes were made to only play certain tracks in certain areas. Econsim was optimized, and many bugs were fixed. The minimap was overhauled, with many quality-of-life and visual improvements. Terrain compression speed was worked on, with many trials of different compression techniques.

The large physics overhaul was merged, and lots of patches are being added to
issues that popped up from it. You can see a small flight in action
[here](https://www.reddit.com/r/Veloren/comments/nc4tvo/i_cant_believe_how_beautiful_this_game_is/). Dungeons have been balanced, and many weapons have also
seen changes. In June, 0.10 will be released.

May’s full weekly devlogs: “This Week In Veloren…”:
[#118](https://veloren.net/devblog-118),
[#119](https://veloren.net/devblog-119),
[#120](https://veloren.net/devblog-120),
[#121](https://veloren.net/devblog-121),
[#122](https://veloren.net/devblog-122).

![Most of West Seattle has poor access to public libraries](../../assets/7450a72f1cb2851a.png)


[A/B Street](https://github.com/a-b-street/abstreet) by [@dabreegster](https://twitter.com/CarlinoDustin) is a traffic simulation game exploring how small
changes to roads affect cyclists, transit users, pedestrians, and drivers, with
support for any city with OpenStreetMap coverage. The project aims to engage
more citizens with transportation planning, letting people advocate for real
changes they want to see.

In May, travel time stopped being the only “score” for how well road changes work. Risk exposure of cyclists crossing dangerous intersections or travelling in front of high-speed traffic is now measured, with lots of data visualization work by Michael. Trevor also revived the 15-minute isochrone tool, finding areas of a city without easy access to education, hospitals, or other facilities. We also moved the map import process, with over 100 supported maps, to the cloud from a single poor laptop. OpenStreetMap importing now handles multiple turn lanes, U-turns, and stop signs much better.

![Animated image showing a small factory in the middle of the game island](../../assets/c00b049c868b4fcb.gif)

[The Process](https://twitter.com/PlayTheProcess/) by @setzer22 is an upcoming game about factory building, process
management and carrot production, built with Rust using the Godot game engine!

This month has been focused on improving the game’s UI and extending the machine logistics system, but there was also room for a few cosmetic improvements:

- Improved visualization of connections in the
[logistic network](https://twitter.com/PlayTheProcess/status/1391484080798281728). - Implemented configurable filters for machines to build a
[sorting machine](https://twitter.com/PlayTheProcess/status/1392894719311613953)! - New materials and
[terrain shader](https://twitter.com/PlayTheProcess/status/1396175924652019718). [Trees and dynamically updating grass](https://twitter.com/PlayTheProcess/status/1399774534417498121)using instanced rendering.

*Discussions:
/r/rust_gamedev,
Twitter*

![Game features](../../assets/9471d7639008b67f.gif)


[pGLOWrpg](https://github.com/roalyr/pglowrpg) by [@Roal_Yr](https://twitter.com/Roal_Yr)
is a Procedurally Generated Living Open World RPG,
a long-term project in development, which aims to be a narrative text-based game
with maximum portability and accessibility.

Recent updates include:

- Implemented dev features test arena.
- Implemented entity system draft.
- Sanitized coordinate systems everywhere (ooof!)
- Much refactoring.
- Resumed river generation development.

*Discussions: Twitter*

### Project YAWC [#](https://gamedev.rs#project-yawc)

![A map in Project YAWC being built.](../../assets/f1ae84056f624f0d.png)


Project YAWC ([Twitter](https://twitter.com/ProjectYawc)) is a turn-based
strategy game built in GGEZ, being developed by junkmail.

May saw the release of Alpha 5.4, including interface improvements, balance changes, new units, new maps, and netcode improvements.

An [alpha access request form](https://forms.gle/w22ohPGNk58fo9bv6) is available,
if you want to try it out.



![bounty-bros-title-screen](../../assets/05570ca4ce321e48.png)

[Bounty Bros.](https://katharostech.com/post/bounty-bros-update-3-sound-and-ui) is a prototype game, similar to the old Legend of
Zelda® games, developed by [Katharos Technology](https://katharostech.com) as a testing
ground for a future commercial game.

The last two months of development was primarily focused on sound and user interface:

- Music will play in different areas of the map and fade in when walking into an area with different music.
- In-game UI is now functional including a new start menu and a simple settings menu to toggle the CRT filter and pixel aspect ratio.
- The web player now has a simple loading icon instead of a solid black screen.

The web version was re-built and published under a new link so you can [try it
in your browser](https://katharostech.github.io/skipngo_pre-releases/refs/tags/pre-release-1/?asset_url=https://katharostech.github.io/bounty-bros_pre-releases/1).

You can read the full update in the [Blog Post](https://katharostech.com/post/bounty-bros-update-3-sound-and-ui).

### Harvest Hero & Harvest Hero Origins [#](https://gamedev.rs#harvest-hero-harvest-hero-origins)

![Harvest Hero Origins supports local multiplayer](../../assets/dfa3df786385cee9.gif)


Harvest Hero is currently on hold for now. After
[Gemdrop Games](https://twitter.com/GemdropGames) was formed, it was decided
that [Emerald](https://github.com/Bombfuse/emerald) needed to be tested to ensure it can withstand cross
publishing.
This means creating a smaller game in the
engine in order to figure out the publishing process for
Steam, Itch, Nintendo Switch, and guarantee its viability.

This resulted in the birth of [Harvest Hero Origins](https://gemdrop-games.itch.io/harvest-hero-origins), a small wave
defense arcade game with local co-op! Join the [Gemdrop Games Discord](https://discord.gg/CJRbxQn3d9)
to stay up to date with these games.

Features:

- Story Mode
- Survival Mode (with local co-op)
- Unlockable skins
- 2 unlockable playable characters


![Animation showing Bibi, the main protagonist of Outer Wonders, starting from the top entrance of a puzzle, rolling from obstacle to obstacle, leaning on bushes, flowers, and trees to reach the bottom exit of the puzzle](../../assets/165c41847d0d0e5e.gif)


[Outer Wonders](https://utopixel.itch.io/outer-wonders) is a colorful, pixel art, puzzle-based adventure game
developed by [Utopixel](https://utopixel.games) where you play as Bibi, a cute round monkey who
enjoys rolling in straight lines. Explore a whimsical nature where
altering the environment is key to progress, and solve puzzles to protect
its wonders.

Outer Wonders can be downloaded for Linux and Windows from [itch.io](https://utopixel.itch.io/outer-wonders).

May was mostly dedicated to code cleaning, small improvements, as well as blogging and community building. Updates of the month include:

- Refactored UI code to streamline menu stacking and ease the implementation of an upcoming options menu.
- Added support for menu navigation using the D-Pad alongside the existing analog stick support.
- Published a blog post about building Outer Wonders for Linux/itch.io
(
[english](https://utopixel.games/en/blog/building-outer-wonders-for-linux/),[french](https://utopixel.games/fr/blog/adaptation-outer-wonders-linux/)). - Posted weekly puzzles
[#16](https://twitter.com/utopixel/status/1389984537170620422),[#17](https://twitter.com/utopixel/status/1392526232596541449),[#18](https://twitter.com/utopixel/status/1395079712020602884)and[#19](https://twitter.com/utopixel/status/1397614237187551237)on social media for players wishing to give puzzles a try prior to downloading the game.

*Discussions:
/r/rust_gamedev,
Hacker News*

![agent stats and a fight with a spider in ~/dev/facundoolano](../../assets/4dc6281b7d0398c2.png)


[rpg-cli](https://github.com/facundoolano/rpg-cli) by [@facundoolano](https://github.com/facundoolano) is a bare-bones JRPG-inspired terminal game.
It can work as an alternative to cd where you randomly encounter enemies
as you change directories.
The game features:

- Character stats and leveling system.
- Automatic turn-based combat.
- Item and equipment support.
- 15+ enemy classes.
- Permadeath with item recovering.
- Run and bribe to escape battles.

*Discussions:
/r/rust_gamedev*



![Blast Repeller](../../assets/4bc34c9fd6383dd8.gif)

[Theta Wave](https://github.com/amethyst/theta-wave) is an open-source space shooter game by developers [@micah_tigley](https://twitter.com/micah_tigley) and
[@carlosupina](https://twitter.com/carlosupina). It is one of the showcase games for the [Amethyst Engine](https://amethyst.rs/). In
the past month, the [“Loot”](https://github.com/amethyst/theta-wave/releases/tag/v0.1.6) update was released which enhanced how loot drops
are rolled, spawned, and how their effects are applied to the game. The Loot Update
also added an attraction system that allows for entities to repel or attract
other entities.

Now an [“Organization”](https://github.com/amethyst/theta-wave/projects/5) update is in progress for Theta Wave. This update will
divide Theta Wave into two workspaces; a library and a binary. This update will also
add documentation comments for all of the library’s features.

## Engine Updates [#](https://gamedev.rs#engine-updates)

[Tetra](https://github.com/17cupsofcoffee/tetra) is a simple 2D game framework, inspired by XNA, Love2D, and Raylib. This
month, versions 0.6.4 and 0.6.5 were released, featuring:

- Stencil buffers
- Basic instanced mesh rendering
- Methods for reading textures back to the CPU (e.g. for screenshots)
- Support for passing slices/arrays as shader uniforms
- More utility methods for working with high-DPI displays
- Various bug fixes and docs improvements

For more details, see the [changelog](https://github.com/17cupsofcoffee/tetra/blob/main/CHANGELOG.md).

![rustcraft-img](../../assets/5dc46c03ef7ec942.png)


[Rustcraft](https://github.com/dskart/rustcraft) by @dskart
is a simple Minecraft engine written in Rust using wgpu.

It handles infinite world generation using gradient noise as well as placing and breaking blocks.

![rg3d](../../assets/5e2252e30de7c080.jpg)


[rg3d](https://github.com/mrDIMAS/rg3d) ([Discord](https://discord.gg/xENF5Uh), [Twitter](https://twitter.com/DmitryNStepanov)) is a game engine that
aims to be easy to use and provide a large set of out-of-box features. Some of
the recent engine updates:

- Initial 2D support (with lighting and physics)
- Multi-layer terrains (
[check this video](https://www.reddit.com/r/rust/comments/nlnfdb/timelapse_of_terrain_editing_in_rustyeditor_which/)) - Load balancer for texture uploader
- Customizable vertex format
- Instanced rendering fixes
- Menu items now can work without backing Menu widget
- Shadows fix for spotlights
- Selection improvements for Tree widget
- Continuous integration
- Basic Framework that hides engine initialization and game loop
- Performance improvements
- “Save” mode for FileSelector and FileBrowser widgets
- Various bug fixes and small improvements.

rusty-editor updates:

- Context menu for world outliner items
- Terrain editor
- Grid snapping for Move interaction mode
- Fixes for Move interaction mode in case of complex hierarchies
- Continuous integration
- Settings window refactoring + improvements
- Box selection mode bug fixes

![Zelda running on Nestadia](../../assets/e1d89a7f159ecebd.png)


[Nestadia](https://github.com/zer0x64/nestadia) by @zer0x64, @junior-n30 and @CBenoit is a
server-based NES emulator.

Nestadia was written as a reverse engineering and memory exploitation challenge for NorthSec CTF 2021, a cybersecurity competition. Contestants were required to reverse-engineer the emulator and ultimately write a Tool Assisted Speedrun to run arbitrary code inside a provided ROM.

After the competition, the code was open-sourced and cleaned up to remove references to the competition. The developers intend on fixing more bugs and adding more features in the near future.

Some interesting features of this emulator are its server-based nature, and the no_std core which means that the emulator can be built and ran pretty much anywhere without much work.

Incoming improvements include online multiplayer, sound, a WASM port, porting to a libretro core, and using wgpu instead of sdl for the native GUI and debugger.

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

After some GLSL issues trying to update the [“Learn WGPU”](https://sotrh.github.io/learn-wgpu) tutorial
to version WGPU 0.8, [@sotrh](https://patreon.com/sotrh) decided to migrate to WGSL.
This update was a lot of work, but relatively painless.
As a result, `shaderc`

is no longer a dependency.

Checkout more at [here](https://sotrh.github.io/learn-wgpu/news/#_0-8-and-wgsl).

[@TanTanDev](https://twitter.com/TanTanDev) published a [video](https://youtube.com/watch?v=96ht7rd3Y5I) about
how he made a voxel engine written in Rust using wgpu.

Currently voxel rendering, chunk management, flying camera,
and simple lightning is implemented.
The source code is released on [github](https://github.com/TanTanDev/first_voxel_engine).

*Discussions:
/r/rust_gamedev*

[Another video](https://youtu.be/ZltAssmicsM) by [@TanTanDev](https://twitter.com/TanTanDev) is about
the projects he made during his first year of learning Rust.
He also talks about why he likes the Rust programming language and community.

*Discussions: /r/rust_gamedev*

![A screenshot of Dig World gameplay](../../assets/9feac6ebe7a8a347.png)


@kuviman wrote a devlog about his experience writing a video game in Rust.

He needed to make a game in just 48 hours for the Ludum Dare 48 (LD48) game jam, so he chose a simple theme: digging.

20 hours later, he had a full-fledged MMO - complete with hackers!

*Discussion: r/rust_gamedev*

[This Reddit post](https://www.reddit.com/r/rust_gamedev/comments/n9v8m9/rust_in_unreal_engine_may_2021_summary/) discusses the current state of using Rust in
the Unreal Engine. It concludes that although there are several ways that Rust
could interact with the engine, all are still forced to use C++ to bootstrap
these operations.

[@chrisbiscardi](https://twitter.com/chrisbiscardi) published [a video](https://youtube.com/watch?v=4TJsEXupFso) about using Bevy’s event
readers and writers to implement a reset game button for a 2048 clone.

The video walks through implementing a “reset game” UI button in Bevy 0.5 by taking advantage of Bevy’s event system for reading and writing a ResetGameEvent. It also covers recursively despawning entities and sprites.

*Discussion: Twitter*

## Tooling Updates [#](https://gamedev.rs#tooling-updates)

![Piet Mondrian's artwork replicated in Graphite using the new color picker](../../assets/1570051be7cabaae.png)

Graphite ([GitHub](https://github.com/GraphiteEditor/Graphite), [Discord](https://github.com/GraphiteEditor/Graphite/blob/master/README.md#discord),
[Twitter](https://twitter.com/GraphiteEditor)) is an in-development vector and
raster graphics editor built on a nondestructive node-based workflow.

In the past month, new frontend features have mostly closed the gap for a visually complete UI while a major Rust backend refactor took place.

A new frontend system for floating menus was added to draw menus over the UI, like dropdown menu input widgets and popovers to display the new color picker. Also, the application menu bar was built with working buttons for the new Undo and Export SVG actions.

A large refactor in the Rust backend created a simpler communication strategy between all components in the software stack and a standard method of handling user inputs.

[Try it right now in your browser.](https://editor.graphite.design/) Graphite is making
rapid progress towards becoming a non-destructive, procedural graphics editor
suitable for replacing traditional 2D DCC applications. Please
[join the Discord](https://github.com/GraphiteEditor/Graphite/blob/master/README.md#discord) - and consider asking for a tour of the
code and how you can help!

## Library Updates [#](https://gamedev.rs#library-updates)

[Dimforge](https://dimforge.com) creates open-source Rust crates for numerical simulation.
Some of the [recent updates](https://dimforge.com/blog/2021/06/06/this-month-in-dimforge):

[Rapier](https://rapier.rs)v0.9 brings user-defined storages, colliders not attached to any rigid-body, velocity-based kinematic bodies, and a lot of[other improvements](https://github.com/dimforge/rapier/blob/master/CHANGELOG.md#v090).- bevy_rapier v0.10 was completely rewritten using the new user-defined storages to become significantly more ergonomic and “bevy-native” feel.
- New exhaustive user-guides for
[Rapier](https://www.rapier.rs/docs/user_guides/rust/getting_started)and[bevy_rapier](https://www.rapier.rs/docs/user_guides/rust_bevy_plugin/getting_started_bevy)were written. They cover all the available features of Rapier, excepted details about implementing your own custom storage for colliders and rigid-bodies. - The
[JS bindings for Rapier](https://github.com/dimforge/rapier.js)have been updated to use Rapier 0.9. - nalgebra v0.26 and v0.27 got
[const-generics support](https://www.dimforge.com/blog/2021/04/12/integrating-const-generics-to-nalgebra)and macros for constructing matrices/vectors/points in a convenient way.

![egui](../../assets/bf7f64047cffe826.gif)


[egui](https://github.com/emilk/egui) by [@emilk](https://twitter.com/ernerfeldt) is an easy-to-use immediate mode GUI library in pure Rust.

This month [version 0.12](https://github.com/emilk/egui/blob/master/CHANGELOG.md) of egui was released, with improved plots,
multitouch, user memory stores, window pivots, and more.

You can try out egui in the [online demo](https://emilk.github.io/egui).

*Discussions: /r/rust*

![Dota2 running on Naga](../../assets/ced77c60d8a5d70c.jpg)


Naga is a shader translation library in pure Rust, aiming to replace glsl-to-spirv and SPIRV-Cross.

In April the gfx-rs team shared a glimpse of the performance difference with
SPIRV-Cross on a single pipeline creation. In May, they did a full-fledged
Dota2 run on [gfx-portability](https://github.com/gfx-rs/portability) without SPIRV-Cross. All shader translation was
done by [naga](https://github.com/gfx-rs/naga), roughly 4x as fast as the C++ alternative
(with no pipeline caching involved). Read more on [gfx-naga-blog](https://gfx-rs.github.io/2021/05/09/dota2-msl-compilation.html).

![Rafx Wireframe Demo](../../assets/2cbe7961cd1991c5.jpg)

Rafx is a multi-backend renderer that optionally integrates with the
[distill](https://github.com/amethyst/distill) asset pipeline.

This month, [@dvd](https://github.com/DavidVonDerau) completed work on the new job system. It implements three
steps: extract, prepare, and write. These jobs are now more structured, making
them easier to implement while supporting concurrent execution and reducing
dynamic allocation. They also integrate with a visibility system to ensure that
off-screen objects are not processed.

[@aclysma](https://github.com/aclysma) continued work on OpenGL ES 2.0/3.0 backends and documented
[implementation details](https://github.com/aclysma/rafx/tree/master/docs/api/backends) of currently available
rendering backends.

Additionally, some rendering features were improved and added: mesh rendering now uses an instance-rate vertex buffer instead of per-object uniforms, improving performance. Rendering features now support wireframe and untextured rendering modes. An egui render feature was added, and the demo now uses egui instead of imgui.

![ui-example](../../assets/15dbdb9ee4e48aea.gif)

[Bevy Retro](https://github.com/katharostech/bevy_retro) is a [Bevy](https://bevyengine.org) plugin designed for making pixel-perfect
games as easily as possible.

This project was released under the [Katharos License](https://github.com/katharostech/katharos-license). This
license has moral and ethical implications that you may or may not agree with,
so please read it before making use of this project.

In the last two months, Bevy Retro has gained a few new features, the biggest of
which is an integration with the [RAUI](https://raui-labs.github.io/raui/) UI library ( also featured in this
newsletter ), allowing you to design a fully-fledged user interface for Bevy Retro
games. Additional features added were:

- A simple sound playing API
- Text rendering for the BDF font format
- Custom render hook support allowing you to use raw
[Luminance](https://github.com/phaazon/luminance-rs)API calls to render anything you want into the low-resolution framebuffer

You can ask questions or give feedback for Bevy Retro
[on GitHub](https://github.com/katharostech/bevy_retro/discussions).

![A tilemap with procedural textures](../../assets/be0b147426b8bcb9.png)

[Texture Generator](https://github.com/Orchaldir/texture_generator) by [Orchaldir](https://github.com/Orchaldir) is a library to generate textures,
and a library to use those textures to render tilemaps.
Both libraries can generate color & depth images and
support post-processing effects like lighting & ambient occlusion.
For randomness, the instance id (e.g. the 145th brick) and/or the tile id are hashed.

The [current release](https://github.com/Orchaldir/texture_generator/projects/8) focuses on furniture.

![Configuring two asset collections](../../assets/b805841139ee2ace.png)


`bevy_asset_loader`

by [@nikl_me](https://twitter.com/nikl_me) is a plugin for [Bevy](https://bevyengine.org) apps aiming to
improve a common pattern for asset-loading. The boilerplate required to load
assets during a “loading state” is reduced to a minimum. At the same time, the
plugin brings together the internal names of assets and their filepath, making
it easier to add new assets and to keep an overview over already existing ones.

The library introduces the `AssetCollection`

trait that can be derived. Any
number of asset collections can be loaded by a single `AssetLoader`

during a
configured app state. When all assets are loaded, the collections will be
inserted into Bevy’s ECS as resources. Afterwards, the `AssetLoader`

will
switch into a second configurable app state. At this point, your app can use
the asset collections that now contain loaded asset handles.

Currently, a single file always corresponds to one asset, and more complex
assets like e.g. `TextureAtlas`

are not yet supported. There are plans to
extend the `asset`

attribute to allow loading more complex assets. Stay tuned!

`tobj`

by [@Twinklebear](https://github.com/Twinklebear/) and [@virtualritz](https://github.com/virtualritz) is a simple and lightweight
option for loading OBJ files. `tobj`

was originally written inspired by
[@syoyo](https://github.com/syoyo)’s tinyobjloader, to provide a similar lightweight and easy to integrate
API for loading OBJ files in Rust.

While initially targeted at realtime rendering applications, `tobj`

has gained
more advanced importer functionality required for offline rendering,
simulation, and modeling applications, through recent work by [@virtualritz](https://github.com/virtualritz).
These features provide support for merging vertices to avoid discontinuities
in simulation packages and reordering vertices to allow omitting the
index buffer. These features have been added while preserving the original
lightweight API design goal of `tobj`

, making it a useful crate for a range of
applications loading with OBJ files.

![CSG difference operation with a sphere and three cylinders](../../assets/2529279ef7fa3a5f.png)


`libfive`

by [@virtualritz](https://github.com/virtualritz) is a safe, oxidized wrapper around
[Matt Keeter](https://github.com/mkeeter/)’s [ libfive](https://libfive.com/) – a “library and set of
tools for solid modeling especially suited for parametric and procedural
design”.

`libfive`

is based on [functional representation](https://en.wikipedia.org/wiki/Function_representation) (f-rep). F-reps can be
evaluated as 3D meshes with aribitrary precision.

One could e.g. use this for a compact definition of a game’s levels and mesh them adaptively, on the fly, during loading. With a density suitable for the machine/GPU running the game.

F-reps can also be sliced into polylines/vectors or bitmaps – e.g. for deriving
[level sets](https://en.wikipedia.org/wiki/Level_set) or for SLA/DLP 3D printing.

![A screenshot of NVIDIA NSight Systems with only one sections measured](../../assets/0acbdeaa9a8e248a.png)

NVIDIA® Tools Extension SDK (NVTX) is a C-based API for annotating events,
code ranges, and resources in your applications.
[nvtx-rs](https://github.com/simbleau/nvtx-rs) by [@simbleau](https://github.com/simbleau) is a safe rust wrapper for it.

The intent is to safely wrap the NVTX library in rusty fashion to provide a proper cross-platform library for GPU and CPU profiling. Ideally this library would be used in benchmarking rust applications and performing research on rust projects such as a GPU analysis with zero-cost abstraction.

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[Backroll-rs, a new networking library](https://github.com/HouraiTeahouse/backroll-rs/issues).[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[gfx-rs’s “contributor-friendly” issues](https://github.com/gfx-rs/gfx/issues?q=is%3Aissue+is%3Aopen+label%3Acontributor-friendly).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[A/B Street’s “good first issue” issues](https://github.com/a-b-street/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/good%20first%20issue).

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!

**Discuss this post on**:
[/r/rust_gamedev](https://www.reddit.com/r/rust_gamedev/comments/nwlcsp/this_month_in_rust_gamedev_22_may_2021/),
[Twitter](https://twitter.com/rust_gamedev/status/1402736426563870720),
[Discord](https://discord.gg/yNtPTb2).