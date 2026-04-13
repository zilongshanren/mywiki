---
title: 'This Month in Rust GameDev #29 - December 2021'
url: https://gamedev.rs/news/029/
author: Rust GameDev WG
published: '2022-01-19'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 29th issue of the Rust GameDev Workgroup’s
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

[Rust GameDev Meetup](https://gamedev.rs/news/029/#rust-gamedev-meetup)[Game Updates](https://gamedev.rs/news/029/#game-updates)[Learning Material Updates](https://gamedev.rs/news/029/#learning-material-updates)[Engine Updates](https://gamedev.rs/news/029/#engine-updates)[Tooling Updates](https://gamedev.rs/news/029/#tooling-updates)[Library Updates](https://gamedev.rs/news/029/#library-updates)[Other News](https://gamedev.rs/news/029/#other-news)[Discussions](https://gamedev.rs/news/029/#discussions)[Requests for Contribution](https://gamedev.rs/news/029/#requests-for-contribution)

## Rust GameDev Meetup [#](https://gamedev.rs#rust-gamedev-meetup)

![Gamedev meetup poster](../../assets/a3e7effd67d5e30e.png)


The thirteenth Rust Gamedev Meetup happened in December. You can watch the
recording of the meetup [here on Youtube](https://youtu.be/S7aoi_4a2uE). The meetups
take place on the second Saturday every month via the [Rust Gamedev Discord
server](https://discord.gg/yNtPTb2) and are also [streamed on
Twitch](https://twitch.tv/rustgamedev).

## Game Updates [#](https://gamedev.rs#game-updates)

![Tet-Rust screenshot](../../assets/e2314251ae5b8542.gif)

Tet-Rust ([GitHub](https://github.com/Syn-Nine/rust-mini-games/tree/main/2d-games/tet-rust)) by
[@Syn-Nine](https://twitter.com/Syn9Dev) is a mini game based on the famous falling puzzle
block game.

The game was created to exercise Syn9’s [Rust Mini Game Framework](https://github.com/Syn-Nine/mgfw) and is
part of an open source [repository](https://github.com/Syn-Nine/rust-mini-games/) of several mini-games
that use this framework.

### The Beast of Monte Carlo [#](https://gamedev.rs#the-beast-of-monte-carlo)

![The Beast of Monte Carlo Screenshot](../../assets/c55aaf1f7a5ad5cb.png)

The Beast of Monte Carlo by [@Syn-Nine](https://twitter.com/Syn9Dev) is a mini role-playing
game in development to help work out new features for Syn9’s
[Rust Mini Game Framework](https://github.com/Syn-Nine/mgfw).

This month’s progress included:

- prototyping tilemap and frame-based animation to make a simple walkaround engine
- creating a general purpose maze generation algorithm and porting random world map generation from C++ to Rust
- creating new sprite artwork and animation, as well as mocking up the battle system

The gameplay and art are influenced by games such as Final Fantasy VI and Lufia II with a heavy focus on procedural content generation.

![In-game screenshot of 10x Sprint Master, depicting a project workboard and two team members.](../../assets/a5a2e5151140384e.png)


[10x Sprint Master](https://e-net4.itch.io/10x-sprint-master) ([GitHub](https://github.com/Enet4/10xSprintMaster)) by [@E_net4](https://twitter.com/E_net4)
is a simulation game where you play the role of
a software development lead engineer.
Write tasks, coordinate a team of developers,
fix bugs and manage feature delivery,
while trying to mitigate the torments of technical debt.

The game was submitted to GitHub Game Off 2021,
and was written using [Yew](https://yew.rs) with graphics done in pure HTML and CSS.

The author also published a [blog post on Dev.to](https://dev.to/e_net4/10x-sprint-master-a-technical-and-social-experiment-ahp)
about the game’s technical and social dimensions.

Molecoole is a top-down shooter roguelike where you build your character
from different atoms. Each atom has a unique ability providing
tons of variety between playthroughs.
It’s made using the [Bevy Engine](https://github.com/bevyengine/bevy).

This month Molecoole devs focused on
adding more [variety](https://twitter.com/kiss_mrton/status/1473725282918014977): different enemies, atoms etc…

They also launched their first teaser [video](https://twitter.com/kiss_mrton/status/1467242884927614976),
it gives us a glimpse into 3 different bioms, bosses, enemies and more.

![Winter in a town](../../assets/75e786a8e71d07c9.jpg)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In December, Veloren ran a Christmas week. From the 20th to the 30th of December, there were several winter-themed changes on the main server. Snow was everywhere, decorations were added to locations, and NPC wore Christmas hats! The 150th Veloren blog was also released in December. An experimental new section of the newsletter gives video recaps of the last week’s blog post.

The ability to edit the appearance of characters was added to the game. Work was done on armor tooltips to make them more clear. Skiing is in the works, with some work to still be done on animations and physics. New images were created for item displays, which are now stored as .vox files.

December’s full weekly devlogs: “This Week In Veloren…”:
[#149](https://veloren.net/devblog-149),
[#150](https://veloren.net/devblog-150),
[#151](https://veloren.net/devblog-151),
[#152](https://veloren.net/devblog-152).

### Country Slice [#](https://gamedev.rs#country-slice)

![Country Slice](../../assets/a6516b4029973460.gif)


[Country Slice](https://github.com/anopara/country-slice) is
[@anastasiaopara](https://twitter.com/anastasiaopara/)’s hobby project, where users can draw a
small scene, and their input is amplified with real-time procedural
generation.

This month’s biggest update was adding an ability to draw
paths that, if intersected with walls, automatically generate arches. You can
read a Twitter thread that briefly covers how it
[was optimized to run in 1-2ms](https://twitter.com/anastasiaopara/status/1472627194409230343).

### Fish Fight [#](https://gamedev.rs#fish-fight)

![Fish demo scene](../../assets/7f99a7b23683c8ee.jpg)


Fish Fight ([GitHub](https://github.com/fishfight/FishFight), [Discord](https://discord.gg/4smxjcheE5),
[website](https://fishfight.org/))

Fish Fight is a tactical 2D shooter, played by up to 4 players. It is also a 2D-pixels-platformer game engine optimized for modding.

In-game level editor was [released](https://github.com/fishfight/FishFight/releases/tag/v0.3), along with an [editor tutorial](https://fishfight.github.io/FishFight/editor.html).
A retrospective devlog was posted: [Fish Fight’s past, present, and future](https://spicylobster.itch.io/fishfight/devlog/332434/fish-fights-past-present-and-future).

BITGUN ([Steam](https://store.steampowered.com/app/1673940/BITGUN/), [Twitter](https://twitter.com/logloggames),
[Discord](https://discord.gg/XrGZQkq)) by [@LogLogGames](https://twitter.com/logloggames) is an action
roguelike zombie shooter with lots of blood. The game is built using Godot
and Rust (via [godot-rust](https://godot-rust.github.io/)).

They are now heading to a public playtest via Steam and you can signup
[here](https://airtable.com/shrMUw2Xz98tdj8gW) to play the game for free in exchange for a short feedback.
They recently added [cutscenes](https://twitter.com/LogLogGames/status/1479752293306273792), which are telling a bit more
story about this post-apocalyptic zombie world where people are scared of getting
infected and supplies are rare. They also launched a project [Name your zombie](https://loglog.games/pages/name-your-zombie/)
where you can get your Twitter or TikTok username as a name of a random zombie
and a tombstone in the game!

![Cars, some terrain with roads and lava](../../assets/adfa1e71ba3b2840.jpeg)


[vange.rs](https://vange.rs) is the project of re-implementing the [Vangers](https://en.wikipedia.org/wiki/Vangers) game (from 1998)
in Rust using modern development practices, parallel computations, and GPU.

This month [@caiiiycuk](https://twitter.com/caiiiycuk) ported it to the “wasm32-unknown-emscripten” target
via wgpu’s GLES3 backend and [posted an article](https://caiiiycuk.medium.com/vange-rs-webassembly-in-rust-498e2f960a04)
about the process and observations.

The web version of vange-rs can be [played online here](https://caiiiycuk.github.io/vangers-web/vange-rs/).

*Discussions:
/r/rust_gamedev*

![planes shooting each other](../../assets/69ebc4003983cf48.gif)


[Bevy Combat](https://github.com/ElliotB256/bevy_combat) by [@ElliotB256](https://github.com/ElliotB256) is
a WIP sci-fi battle simulation written using Bevy.

Some of the current features:

- Combat and targetting AI;
- Simple weapons (instant hit), damage, health, shields, and mortality;
- Death animations and explosions;

Check out the [web demo here](https://elliotb256.github.io/bevy_combat).

### Rust City [#](https://gamedev.rs#rust-city)

![road, buildings with various utilities and some GUI](../../assets/d105ca814823db8c.jpg)


[@oliviff](https://twitter.com/oliviff) is working on a city building game.
Some of [this month’s updates](https://twitter.com/oliviff/status/1473266319881654274):

- Basic zoning placeholders when building roads.
- Advanced zoning for residential, commercial, and industry.
- Populating zoned areas based on demand.
- Buildings don’t function unless they have utilities.
- Finances and transactions
- Population tracker.
- pipes required for a house to receive water.
- cables required for a house to receive electricity.
- build mode for pipes and cables.
- UI to toggle different layers visibility.

### Antorum Isles (pka Antorum Online) [#](https://gamedev.rs#antorum-isles-pka-antorum-online)

![isles!](../../assets/ac8adae4e8bb3936.jpg)


[Antorum Isles](https://antorum.ratwizard.dev) is a micro-multiplayer online role-playing game
by [@dooskington](https://twitter.com/dooskington).
The game server is written in Rust, and the client is Unity-based.

Main highlights of the latest [@dooskington’s devlog](https://ratwizard.dev/dev-log/antorum/39):

[Now you can download the client and play the game](https://antorum.ratwizard.dev)!- The project is mostly finished, it won’t receive more major new features or updates.
- The editor and the dedicated server binaries should be released soon.

## Engine Updates [#](https://gamedev.rs#engine-updates)

{{ image_figure( alt=“An example Rusty Engine game” src=“rusty_engine3.png” caption=“The “Road Race” game prototype running under Rusty Engine 3.0“) }}

[Rusty Engine](https://github.com/CleanCut/rusty_engine) by [Nathan Stocks](https://github.com/CleanCut) is a game engine built on top of Bevy
for people who are learning Rust.

Version 3.0 is a large release with many breaking changes. Notable new features
include: [a full tutorial](https://cleancut.github.io/rusty_engine/), custom asset loading (sprites, sounds, fonts),
customizable game state, an interactive collider creator, and much more.
See [the changelog for 3.0](https://github.com/CleanCut/rusty_engine/blob/main/CHANGELOG.md#300---2021-12-30) for the full details.

![Examples: drawing methods, sound, tilemap and music editors](../../assets/d94edc240146d8b5.png)


[Pyxel](https://github.com/kitao/pyxel) ([Discord](https://discord.gg/FC7kUZJ)) by [@kitao](https://twitter.com/kitao) is a retro game engine
(inspired by [PICO-8](https://lexaloffle.com/pico-8.php) and [TIC-80](https://tic80.com)) that uses Python for scripting:

- 16 color palette,
- 256x256 sized 3 image banks,
- 256x256 sized 8 tilemaps,
- 4 channels with 64 definable sounds,
- 8 peces of music which can combine arbitrary sounds,
- Image and sound editor,
- Keyboard, mouse, and gamepad inputs.

Check out the [official](https://github.com/kitao/pyxel#try-pyxel-examples)
and [user-provided](https://github.com/kitao/pyxel/wiki/Pyxel-User-Examples) examples.

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

[@TheFern2](https://github.com/TheFern2) published a [video tutorial](https://youtube.com/watch?v=nnojR-8PT4M) on how to
set up Rust with [SFML bindings](https://lib.rs/sfml) for Windows users (using MSVC C++).

rust-sfml’s [wiki page with instructions for Windows](https://github.com/jeremyletang/rust-sfml/wiki/Windows) was also updated.

[@TanTanDev](https://twitter.com/TanTanDev) published a [video](https://youtu.be/L7M_vbo1N2g) about the process of adding Rust
support for the Unity game engine.

Is it really possible? YES it is! I managed to make a game 100% coded in Rust, but using Unity as editor and runtime. This has to be one of my craziest projects yet!

I utilized a library called Bevy game framework/engine, to handle the gameplay programming. Utilizing Bevy systems I was able to hide the FFI code from the gameplay code.


The resulting source code [can be found here](https://github.com/TanTanDev/runity).

[“Tetris in Rust from scratch”](https://youtube.com/playlist?list=PLBNbqulT6FWw9C39_WIT_dcCIj1AdxiAy) is a series of livestreams
by [Over Developed](https://youtube.com/channel/UCROob9baB-fRBDSyNq_8i4g) that showcases beginner/intermediate Rust concepts
using Tetris as an example.
Episodes:


[In the first episode], we lay the groundwork for the project, creating the overall structure and some of the primitives that will be used by the game engine.[In the second episode], we flesh out some more behavior in the game engine, and fix some bugs that were introduced in the previous session.[In the third episode], we start writing the interface code for rendering the GUI.[In this episode], we connect the game logic to the GUI and finally see some interactivity.

*Discussions:
/r/rust*

## Tooling Updates [#](https://gamedev.rs#tooling-updates)

![Blackjack demo: Connecting visual nodes and tweaking various parameters to procedurally generate a beveled box in real-time](../../assets/5744bb144cad5e23.gif)


[Blackjack](https://github.com/setzer22/blackjack) by @setzer22 is a new procedural modeling application made in Rust,
using rend3, wgpu and egui. It follows the steps of applications like
Houdini, or Blender’s geometry nodes project and provides a node-based
environment to compose procedural recipes to create 3d models.

The project was recently announced, and an official open-source release is planned during the following month. Here’s a highlight of the upcoming features:

- A node-based editor to compose operations like 3d math, vertex/edge/face selections and mesh edit operations.
- Several polygon edit operations like bevel, chamfer and extrude.
- Viewport display with support for displaying primitive ids and triangle half-edge winding.

*Discussions:
/r/rust_gamedev,
/r/rust*

![Graphite](../../assets/f44577c6c91996c2.png)


Graphite ([GitHub](https://github.com/GraphiteEditor/Graphite), [Discord](https://discord.graphite.design),
[Twitter](https://twitter.com/GraphiteEditor)) is an in-development vector and raster graphics
editor built on a non-destructive node-based workflow.

The completion of [Sprint 10](https://github.com/GraphiteEditor/Graphite/milestone/10?closed=1) wraps up a productive month
of features and stability improvements. Documents persist page reloads via
IndexedDB browser storage. The layer panel got some love. Vector anchor points
can be dragged (beginnings of the Path/Pen Tools). Per-tool footer bar hints
teach possible user input actions. And a big code cleanup/refactor took place
behind the scenes.

Additional new features and QoL improvements: artboards, panel resizing, the
Navigate Tool, outline view mode, support for touch input and non-Latin
keyboards, an *About Graphite* dialog with version info, plus dozens of bugs
and crashes were resolved.

[Try it right now in your browser.](https://editor.graphite.design) Graphite is making
steady progress towards becoming a non-destructive, procedural graphics editor
suitable for replacing traditional 2D DCC applications. [Join the
Discord](https://discord.graphite.design) and get involved!

![Demo that shows colored chords, notes, and tabs](../../assets/1e414972698e1709.gif)


[Fun Notation](https://notation.fun) ([GitHub](https://github.com/notation-fun/notation)) is [@yjpark](https://github.com/yjpark)’s
experimentation on musical notations built on top of Bevy.
The idea is to help with music visualization, practicing,
and provide a nicer way to show scores or tabs.

Some of current ideas tried in the app:

- colors for notes (based on the relative notation),
- color and shapes for chords,
- guitar tabs to show both pitch and durations for notes.

*Discussions:
/r/rust_gamedev*

## Library Updates [#](https://gamedev.rs#library-updates)

[assets_manager](https://github.com/a1phyr/assets_manager/) provides a high-level API to load and cache external resources
with a focus on performance and hot-reloading.

In addition to built-in support for new formats like WebP, glTF and fonts,
[version 0.7](https://github.com/a1phyr/assets_manager/releases/tag/0.7.0) brings a few quality of life improvements. Additionally,
hot-reloading is now supported for custom asset sources.

These features led to a new crate: [ggez-assets_manager](https://github.com/a1phyr/ggez-assets_manager/), whose goal is to ease
use of assets_manager with ggez engine!

![albedo pathtracer](../../assets/46c85816303368fc.png)

The team concluded 2021 with the release of wgpu-0.12 and naga-0.8.
Details can be found on the [gfx-rs blog](https://gfx-rs.github.io/2021/12/25/this-year.html) and [wgpu reddit discussion](https://reddit.com/r/rust_gamedev/comments/rjci2n/wgpu012_is_released/).
Lots of fixes are shipped alongside one much-awaited improvement:
the error messages from validating shaders were finally made readable:

```
┌─ interpolate.wgsl:21:25
│
21 │ out.linear_centroid = vec2<f32>(64.0, 125.0, 1.0);
│ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^ naga::Expression [16]
Entry point vert_main at Vertex is invalid:
Expression [16] is invalid
Composing expects 2 components but 3 were given
```


[Pixels](https://github.com/parasyte/pixels) is a tiny hardware-accelerated pixel frame buffer. It is popularly
used for emulators, software renderers, 2D pixel art games, and desktop
utilities.

Version 0.9.0 brings a few breaking changes. Notably, wgpu was updated to
0.12 and it now requires Edition 2021. Full details are available in the
[release notes](https://github.com/parasyte/pixels/releases/tag/0.9.0).

![YAML configuration files for bevy_proto](../../assets/8e646c660b08aa7e.png)


[bevy_proto](https://github.com/MrGVSV/bevy_proto) is a small plugin for the [Bevy](https://github.com/bevyengine/bevy) game engine, allowing entities to
be defined in their own config files (called “Prototypes”). These config files
are then read into a resource that you can use to spawn their pre-defined
entities from within any Bevy system.

The recently released 0.2 version, adds a templating feature (as suggested
by [@chrisburnor](https://github.com/chrisburnor)). This new feature allows any
entity prototype to define one or more templates, from which it will inherit
additional component definitions (including those from a template’s templates).

This makes defining many entities with common functionality (such as enemy types or weapons) much easier and reduces code duplication for an overall better experience.

For more info, check out
the [original PR](https://github.com/MrGVSV/bevy_proto/pull/2), or explore
the [assets](https://github.com/MrGVSV/bevy_proto/tree/main/assets)
and [examples](https://github.com/MrGVSV/bevy_proto/tree/main/examples) folders.

![Demo of the Tauri based development app](../../assets/f16b85223e60ae93.gif)


[bevy-remote-devtools](https://github.com/reneeichhorn/bevy-remote-devtools) is a plugin and UI application for the [Bevy](https://github.com/bevyengine/bevy) game
engine allowing to view entities and their components, asset resources
like meshes, events from the [tracing](https://github.com/tokio-rs/tracing) crate and system timings using a
very basic profiler. It also supports all of that over network so
debugging can be done from any remote machine and vice versa.

The first release of the 0.1 version comes with basic support for the
aforementioned features. It contains a plugin for [Bevy](https://github.com/bevyengine/bevy) that will extend
you application with a small REST HTTP API that can be consumed by the
included [Tauri](https://tauri.studio/en/) based UI application.

![A rendering of a warmly-lit ruins environment](../../assets/092bf57828ab4c5a.jpg)


[kajiya](https://github.com/EmbarkStudios/kajiya/) ([Discord](https://discord.gg/dAuKfZS))
by [@h3r2tic](https://github.com/h3r2tic) is an experimental real-time global illumination
renderer made with Vulkan, and utilizing [rust-gpu](https://github.com/EmbarkStudios/rust-gpu).

Last month the project was released into open source along with
a tiny sample: [Cornell McRay t’Racing](https://github.com/h3r2tic/cornell-mcray/).

The renderer is permissively licensed, and includes several cutting-edge algorithms, including ray-traced effects. It isn’t built to ship games (yet), but serves as a convenient platform for learning and research.

*Discussions:
medium,
/r/rust,
twitter (kajiya),
twitter (cornell-mcray).*

[Shard](https://github.com/HindrikStegenga/Shard) by @HindrikStegenga is an Archetype-based Entity Component System.

Version 0.2 is a complete rewrite of the ECS, with the main new feature that it supports no_std environments.

*Discussions: /r/rust*

[rapid-qoi](https://github.com/zakarumych/rapid-qoi) by @zakarumych is an implementation of QOI format written in Rust.

QOI format can fit nicely as a replacement for PNG and other common loseless image formats for game engines given its simplicity and blazing fast encoding and decoding.

[rapid-qoi](https://github.com/zakarumych/rapid-qoi) has a simple API, zero unsafe, zero dependencies,
fast build times and high performance.
It is compatible with finalized QOI spec published in December.

[ash](https://github.com/MaikKlein/ash) is lightweight wrapper around Vulkan.

This month [v0.34 was released](https://github.com/MaikKlein/ash/releases/tag/0.34.0). Highlights include:

- Now ash defaults to linking Vulkan directly, which saves the libloading dep and is more idiomatic for apps that don’t have a fallback.
- Debug impls can be disabled for a faster build.
- More extensions and lots of miscellaneous API cleanup.

## Other News [#](https://gamedev.rs#other-news)

- Other game updates:
[BENDYWORM](https://bauxite.itch.io/bendyworm)now[runs on Linux natively](https://twitter.com/bauxitedev/status/1467817606111498240).[Rust Shooter progress report](https://reddit.com/r/rust_gamedev/comments/rj5lut/rust_shooter_another_update): enemies are proper player entities with rudimentry AI now, new indoor environment.[aous](https://vleue.itch.io/aous)is a Game Off’21 game about the survival of a mutating ant colony.[Embark’s Arc Raiders game is using some Rust on the server side](https://twitter.com/repi/status/1469324284619337728).

- Other engine updates:
[@DmitryNStepanov](https://twitter.com/DmitryNStepanov)did a few more[rg3d](https://github.com/mrDIMAS/rg3d)live-coding streams, here’re the recordings:[second](https://youtube.com/watch?v=TQaCyC_tGko),[third](https://youtube.com/watch?v=OsZCusri1Nw),[fourth](https://youtube.com/watch?v=FGi8evJFdnw).[godot-rust was upgraded](https://twitter.com/GodotRust/status/1472269798641971200)to support Godot 3.4 out of the box, so the manual api.json is not needed.[Oxygengine](https://github.com/PsichiX/Oxygengine)v0.26 brings: different image types (2D, 2D Array, 3D), samplers instead of textures, render target fixes, and also an[RPG template](https://reddit.com/r/rust_gamedev/comments/r5xobe/oxygengine_rpg_game_template).

- Other library updates:

## Discussions [#](https://gamedev.rs#discussions)

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[Graphite is looking for contributors](https://github.com/GraphiteEditor/Graphite/issues/202)to help reach the 0.1 Alpha release.[winit’s “difficulty: easy” issues](https://github.com/rust-windowing/winit/issues?q=is%3Aopen+is%3Aissue+label%3A%22difficulty%3A+easy%22).[Backroll-rs, a new networking library](https://github.com/HouraiTeahouse/backroll-rs/issues).[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[A/B Street’s “good first issue” issues](https://github.com/a-b-street/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/D-Good-First-Issue).

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!

**Discuss this post on**:
[/r/rust_gamedev](https://reddit.com/r/rust_gamedev/comments/s82gcd/this_month_in_rust_gamedev_29_december_2021),
[Twitter](https://twitter.com/rust_gamedev/status/1483927872532271107),
[Discord](https://discord.gg/yNtPTb2).