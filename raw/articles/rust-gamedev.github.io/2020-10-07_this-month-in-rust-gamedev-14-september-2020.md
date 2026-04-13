---
title: 'This Month in Rust GameDev #14 - September 2020'
url: https://gamedev.rs/news/014/
author: Rust GameDev WG
published: '2020-10-07'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 14th issue of the Rust GameDev Workgroup’s
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

[Game Updates](https://gamedev.rs/news/014/#game-updates)[Learning Material Updates](https://gamedev.rs/news/014/#learning-material-updates)[Library & Tooling Updates](https://gamedev.rs/news/014/#library-tooling-updates)[Popular Workgroup Issues in GitHub](https://gamedev.rs/news/014/#popular-workgroup-issues-in-github)[Requests for Contribution](https://gamedev.rs/news/014/#requests-for-contribution)

## Game Updates [#](https://gamedev.rs#game-updates)

![Landscape](../../assets/1d8fb9dc11535a75.png)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In September, Veloren hit 5000 commits to the main repo! A privilege escalation bug was found in the game. It was quickly patched, and a PSA was sent out to notify server owners of its presence. A Discord bot was created to help manage a testing server. Airshipper, Veloren’s launcher, saw the release of version 0.4.0. Lots of work is going on to improve the state of Veloren’s server infrastructure. A stress test was run with 15 players to see how smaller server could handle running the game.

Improvements were made to the chunk compression which resulted in a ~7x memory reduction in their storage. The settings menu has been overhauled, along with many other elements of the UI. A stone golem boss was merged, adding a new boss to dungeons. Work has been done on beam weapons and collisions, resulting in a significantly improved healing sceptre.

You can read more about some specific topics from September:

[Compilation Breakdown](https://veloren.net/devblog-84#compilation-breakdown-by-angelonfira)[Improved Server Metrics](https://veloren.net/devblog-85#improved-server-metrics-to-improve-server-performance-by-xmac94x)[PSA: Privilege Escalation bug](https://veloren.net/devblog-86#psa-privilege-escalation-bug)[Animation Changes](https://veloren.net/devblog-86#animation-changes-by-slipped)[Attack Updates](https://veloren.net/devblog-86#attack-updates-by-sam)[Beam Collisions](https://veloren.net/devblog-86#beam-collisions-by-sam)[Sceptre Rework](https://veloren.net/devblog-87#sceptre-rework-by-sam)[Memory Optimizations](https://veloren.net/devblog-87#memory-optimizations-by-sharp)[Art Blog #7](https://www.patreon.com/posts/art-blog-no-7-41635011)

September’s full weekly devlogs: “This Week In Veloren…”:
[#84](https://veloren.net/devblog-84),
[#85](https://veloren.net/devblog-85),
[#86](https://veloren.net/devblog-86),
[#87](https://veloren.net/devblog-87).

![Healing sceptre](../../assets/79387ae4b1aad48c.png)

In October, Veloren will keep pushing towards more scalable infrastructure. Tests are happening to move towards a Kubernetes cluster to manage more infrastructure from code. Optimizations will keep coming in as we find places to improve. 0.8 may release sometime this month, however, the exact date is yet to be set.

![Isometric buildings and textured areas](../../assets/4a2c4aba11a60781.png)


[A/B Street](https://abstreet.org) is a traffic simulation game exploring how small changes
to roads affect cyclists, transit users, pedestrians, and drivers. Any city
with OpenStreetMap coverage can be used!

Some of this month’s updates:

- finished support for driving on the left side of the road;
- isometric buildings and support for textures by
[Michael](https://github.com/michaelkirk); - a flurry of major UI updates, thanks to the return of the project’s UX designer;
- an option to disable parking simulation, to workaround missing data;
- alleyways imported from OSM;
- more realistic traffic signal timing constraints, thanks to
[Sam](https://github.com/NoSuchThingAsRandom/), a new contributor.

![screenshot: trees and water](../../assets/ae04bbf78c799f3a.jpeg)


[Garden](https://epcc.itch.io/garden) is an upcoming game centered around growing realistic plants.
Some of the updates from [the September devlog](https://cyberplant.xyz/posts/september/):

- The project switched to Nvidia’s PhysX from a custom physics engine.
- More accurate plant clone placement.
- Significant rendering performance improvements.
- Work on saving and loading system has begun.

![screenshot](../../assets/25fd41ff3644ee4a.png)


[galangua](https://tyfkda.github.io/galangua/) by [@tyfkda](https://twitter.com/tyfkda) is a dynamic 2D shoot ’em up game,
written in Rust using SDL2.
It works on the desktop as well as in the browser.

[Way of Rhea](https://store.steampowered.com/app/1110620/Way_of_Rhea/) is a puzzle platformer that takes place in a world where you can
only interact with items that match your current color.
Changes since the last update:

-
The circuit level has been reworked: it’s now split into three different levels and the puzzles are better tutorialized, and there are more of them.

-
A tiny amount of screen shake was added to the game.

-
Work has begun on a couple of new levels for the ice biome In this biome, you have to learn to predict the behavior of the crabs to solve the puzzles.

![Ice Biome](../../assets/e77c65d503640ab6.png)


Follow [@AnthropicSt](https://twitter.com/anthropicst) or [@masonremaley](https://twitter.com/masonremaley) on Twitter or
[sign up for the mailing list](https://www.anthropicstudios.com/newsletter/signup/tech) for updates.

![Live editing of procedural architecture rules](../../assets/36a479de916ce042.png)


[Citybound](https://aeplay.org/citybound) is a city simulation and city building game. This month,
[Anselm Eickhoff](https://twitter.com/ae_play) published [a small demo](https://reddit.com/r/Citybound/comments/j2xg2s/sneak_peek_custom_procedural_architecture) of his domain specific language
for procedural architecture, which is interpreted by Rust and now supports
hot-code reload of building rules in the running game.

### Recall Singularity [#](https://gamedev.rs#recall-singularity)

![Demo of the basic ship collision](../../assets/74ce3d970a7768eb.png)

The Recall Singularity is a game about designing autonomous factory ships and
stations created by [Tom Leys](https://twitter.com/RecallSingular1).

This month a new devlog was posted:
[“Recall Singularity in Sep 2020”](https://medium.com/@recallsingularity/recall-singularity-in-sep-2020-e2f33a85fd7c).
You can also check out a [status update and progress video here](https://youtube.com/watch?v=kUIiU9LtOFY).

Updates include:

- Improving the robustness of the game core and networking.
- Ship sections and standalone ships.
- Different synchronization algorithms for different game modes.

![Mimas screenshot](../../assets/b0127c0a6cfc7c46.png)


[Mimas](https://github.com/est31/mimas) is a WIP voxel engine and game, inspired by Minetest and Minecraft.
It’s been in development for almost 2 years and has recently seen a public
prototype release 0.4.0.

Several of the current features:

- Procedural map generation with hilly landscape, trees, flowers, water, and caves
- Map manipulation (removal/addition of blocks)
- Crafting
- Chests
- Textures (taken from the Minetest project, under CC-BY-SA license)
- Tools
- QUIC based network protocol with SRP based authentication
- Multiplayer: chat, (hardcoded) avatars
- Ability to add custom content (e.g. blocks) using a toml format

Imgur screenshot [gallery](https://imgur.com/a/vvo7len).

![Gameplay screenshots](../../assets/5771d0d872f516a9.jpeg)


[Nox Futura](https://github.com/thebracket/noxfutura) by [@blackfuture](https://patreon.com/blackfuture)
is an open-source long-term passion project,
a Dwarf-Fortress and RimWorld inspired base building game.

Some of the [recent updates](https://reddit.com/r/roguelikedev/comments/ivgdnj/sharing_saturday_329/g5t5lo0):

- The WGPU-based rendered is undergoing a major restructure.
- The game was updated to Legion 0.3 - it required rewriting a lot of code, but the new syntax sugar is a joy to use, and the backend is even faster now.
- The Greedy Voxel algorithm was significantly improved.
- OBJ models are now supported - useful for things like tree/vegetation geometry, which can now use a stylized low-poly graphic without the added weight of a bunch of cubes.
- Palette-based rendering - the output system is now constrained to a 256 color palette, mostly to play with stylized 3D rendering.
- New format for data files that combines multiple RON objects in one place.

### pGLOWrpg [#](https://gamedev.rs#pglowrpg)

![pGLOWrpg banner](../../assets/0edecdeee4e11ff2.png)


The [@pGLOWrpg](https://twitter.com/pglowrpg) (Procedurally Generated Living Open World RPG) is a long-term
project in development by [@Roal_Yr](https://twitter.com/Roal_Yr), which aims to be a text-based game with
maximum portability and accessibility and focus on interactions and emergent
narrative.

The pGLOWrpg meets its first official anniversary on September the 15th
and goes public at [pGLOWrpg repo](https://github.com/roalyr/pglowrpg)!

For the past month the main focus of the development was on:

- Improving the UI.
- Major refactoring.
- Unification of I/O means.
- Making things ready for publication.

Main features of the reported version are:

- Ability to generate one or many worlds from customizable presets.
- Ability to have output in both raw (b/w .png) and colorized images.
- Generated data is as follows: terrain, watermask, biomes, rivers, geological regions, rainfall, and temperature.

For main feature reports and dev blogs follow [@pGLOWrpg](https://twitter.com/pglowrpg) on Twitter.

### Oh no, Lava! [#](https://gamedev.rs#oh-no-lava)

![shooting water into lava](../../assets/9e3031fddcc7ed8a.gif)


“Oh no, Lava!” by [@captainfleppo](https://twitter.com/captainfleppo) is the working title
of a platforming game which take inspiration
from an old iOS game created back in 2014. The game is running with [Bevy](https://bevyengine.org)
as its core. The gameplay isn’t there yet, but you as a player need to jump on
furnitures, collect coins, and fight lava/fire based enemies with your water gun.

![Summoner imps throw a swordsman around](../../assets/96516f42165d64e1.gif)

[Zemeroth](https://github.com/ozkriff/zemeroth) by [@ozkriff](https://twitter.com/ozkriff) is a minimalistic 2D turn-based tactical game.
Some of the recent updates:

- The game now
[stores simulated text lifetimes](https://twitter.com/ozkriff/status/1306651821314891776)for each tile during the event processing to reduce popup text overlapping. - Push bombs are more useful now: they still don’t cause direct damage,
but
[now they can push away other bombs too](https://twitter.com/ozkriff/status/1304458740758970368). [All the assets sources are merged into the main repository](https://twitter.com/ozkriff/status/1297239743269412864)and the project now uses[resvg](https://lib.rs/resvg)instead of console Inkscape for svg->png rendering.- Abilities
[don’t have parameters now](https://twitter.com/ozkriff/status/1300817277714075648). - Dynamic depth-sorting
[was implemented](https://twitter.com/ozkriff/status/1310603877507620865). - The work on adding sounds continues:
check out the
[video of the first results](https://twitter.com/ozkriff/status/1303736184045174785)🔊. - Smaller UI improvements and bugfixes.

[Akigi](https://akigi.com) is a WIP online multiplayer game.
In September, lots of work was done on terrain sculpting systems. Another tool
was added, allowing material painting onto the terrain. Along with the scenery
placement tool, there are now three separate tools in the editor’s arsenal.

Full devlogs:
[#083](https://devjournal.akigi.com/september-2020/083-2020-09-06.html),
[#084](https://devjournal.akigi.com/september-2020/084-2020-09-13.html),
[#085](https://devjournal.akigi.com/september-2020/085-2020-09-20.html),
[#086](https://devjournal.akigi.com/september-2020/086-2020-09-27.html).

![Play Go against AI and friends on the web](../../assets/f40de9a8ef74bd87.jpg)

[BUGOUT](https://github.com/Terkwood/BUGOUT) is a web application which allows you to play Go/Baduk/Weiqi
against a leading AI ([KataGo](https://github.com/lightvector/KataGo)).
It provides a multiplayer mode so that you can play other humans,
either by joining a public queue or sharing a private URL to your friend.

The user interface is lifted from [Sabaki](https://github.com/SabakiHQ/Sabaki).

The initial installation’s AI is powered by an energy-efficient
[dev board](https://developer.nvidia.com/embedded/jetson-nano-developer-kit).

BUGOUT is marching actively toward production, at which point the team will publish the website address and invite users. The author anticipates being finished with the production release prior to Jan 1, 2021.

![Tetris Bane](../../assets/e6e5cde1432f2bb5.png)


[Tetris Bane](https://andrew-jones.itch.io/tetris-bane) is an open-source Tetris clone
that mixes things up with multiple game modes.
There’s a hard bane mode, classic mode for the purists,
ultra hard metal mode, and a chill mode.
Tetris Bane challenges you to get more then 2 lines in metal mode.

You can [download](https://andrew-jones.itch.io/tetris-bane) the game for Windows, macOS and Linux.

The game is written using [rust-sdl2](https://github.com/Rust-SDL2/rust-sdl2).
[The source code is available here.](https://github.com/andii1701/tetris-bane)

### Project YAWC [#](https://gamedev.rs#project-yawc)

![Screenshot of an in-progress game of Project YAWC](../../assets/b29aa1730d737d9f.png)


Project YAWC is an in-progress Advance-Wars style strategy game being developed
by junkmail using [ggez](https://ggez.rs/) as a framework. The game is currently in a closed alpha
state with working netplay. September saw the release of version A2, including
revamped netcode and the full core set of units.

![space_shooter_rs_gameplay](../../assets/11de4817dc20f04a.gif)


[space_shooter_rs](https://github.com/amethyst/space_shooter_rs) is a 2D shooter game made with the [Amethyst](https://amethyst.rs) game engine.
It is inspired by games like Raiden and the Binding of Isaac.

In September, [Micah Tigley](https://twitter.com/micah_tigley) joined the project and has been collaborating with
[Carlo Supina](https://twitter.com/carlosupina) to refactor a significant chunk of the codebase. Lots of work has
been on collision detection, combat, and movement. This will allow for easier
future development.

Both developers wrote about the work and their experiences developing space_shooter_rs:

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

![cool bear with glasses](../../assets/f81af687dc60a4cc.png)

[@fasterthanlime](https://fasterthanli.me/) published a giant blog post
[“So you want to live-reload Rust”](https://fasterthanli.me/articles/so-you-want-to-live-reload-rust)
- a very deep technical dive into reloading a dylib
and a bunch of related issues.
Lots of interesting insights for folks who want
to better understand nuances of hot reloading.

*Discussions:
/r/rust*

[rust-wasm-hotreload](https://github.com/shekohex/rust-wasm-hotreload) by [@ShekoHex](https://twitter.com/ShekoHex) is a PoC of using WebAssemply
as a hot-reloadable code logic at runtime without restarting the host process.
[Check out a video demo here](https://twitter.com/ShekoHex/status/1302973994417651714).

This month [@sothr](https://github.com/sothr) released another chapter
of the [“Learn WGPU”](https://sotrh.github.io/learn-wgpu) tutorial:
[“Threading WGPU Resource Loading with Rayon”](https://sotrh.github.io/learn-wgpu/intermediate/tutorial13-threading).

Also, the whole tutorial [was upgraded to WGPU v0.6](https://sotrh.github.io/learn-wgpu/news/#_0-6).

![hexagonal strategy map with region borders](../../assets/e3eb7bf75f451a4f.jpeg)

A small note by [@VladZhukov0](https://twitter.com/VladZhukov0) about drawing lines and chains
with signed distance fields.
The resulted lines are nice looking on edges and have rounded corners.
Chains for this article are assumed to be opaque.

Check out the [online demo](https://pum-purum-pum-pum.github.io/lines/)
and its [source code](https://github.com/pum-purum-pum-pum/Lines).

With the full power of Cargo build scripts and [Tera](https://tera.netlify.app), you can create an advanced
GLSL preprocessor which can generate code conditionally, in loops, and even
inherit code from other templates.

![An OpenGL preprocessor for Rust](../../assets/dafcfd338679454f.png)


Writing plain GLSL code is uncomfortable, code is quite often is duplicated, libraries
aren’t something natural for GLSL (means you can’t out of the box do #include “library.glsl”).
The last point is especially problematic if some constants actually originate in
your game logic (like the number of player types). Updating these values manually
in your shader code is repetitive and prone to both error and simple forgetfulness.
It’s really helpful to build some kind of preprocessor for your GLSL code,
which can include other files, so you can organize your code into manageable chunks.
With the power of [Tera](https://tera.netlify.app), it’s now easy to accomplish.
Because Rust is also often used for web projects, which need a lot of templated
web-pages preprocessing, we can borrow such technology for our needs,
combine it with cargo build scripts and create a compile-time preprocessing tool.

### Rust, Gamedev, ECS, and Bevy [#](https://gamedev.rs#rust-gamedev-ecs-and-bevy)

![Bevy hello world code snippet and two game screenshots, one displaying two blue spheres in a grey canvas and another one displaying a gameboy colored tile game](../../assets/49ce4e27170d79d4.png)


[@hugopeixoto](https://twitter.com/hugopeixoto) released a couple of blog posts on ECS and Bevy,
including a tutorial on how to get started.

-
The

[first part](https://hugopeixoto.net/articles/rust-gamedev-ecs-bevy.html)gives us an in depth overview of what ECS. It starts with pseudocode for an object oriented approach and goes through several iterations until we get to the ECS paradigm. -
The

[second part](https://hugopeixoto.net/articles/rust-gamedev-ecs-bevy-p2.html)is a tutorial on how to use[bevy](https://bevyengine.org), a data driven game engine built in Rust. It goes over the basic features of the engine, using the example presented in the first part.

[@TantanDev](https://twitter.com/TantanDev) is back with [another video](https://youtube.com/watch?v=Qjc0V58lB7A)!
In this one, they made a Flappy Bird clone using Bevy
and shared their experience programming with it.

The source code [can be found here](https://github.com/TanTanDev/flappy_bevy).



![diff-gi-gif](../../assets/eb75ef79f215f1a5.gif)

[DI2edd](https://reddit.com/u/DI2edd) shared his [real-time diffuse global illumination demo on /r/rust_gamedev](https://reddit.com/r/rust_gamedev/comments/ixocl2/real_time_diffuse_global_illumination).
It’s written in 100% Rust and uses WGPU for graphics, proving that the API
is an excellent choice even for advanced computer graphics applications.

The technique provides real time global illumination for static lambertian
geometry, and is the implementation of the 2017 paper [“Real-time Global
Illumination by Precomputed Local Reconstruction
from Sparse Radiance Probes”](https://arisilvennoinen.github.io/Projects/RTGI/index.html),
which proposes a spherical harmonics-based approach to solve the rendering equation
in real time.

In practice, this means that the expensive light transport calculations are performed
in a precomputation step, which relies on - among others - [embree-rs](https://github.com/Twinklebear/embree-rs),
and [nalgebra](https://github.com/dimforge/nalgebra) to produce a compressed
representation of the scene that is then used for lighting reconstruction at runtime.

## Library & Tooling Updates [#](https://gamedev.rs#library-tooling-updates)

![Benchmarks](../../assets/3cdb2920b89df592.png)


[Legion](https://github.com/amethyst/legion) is among Rust’s fastest and most powerful ECS libraries.
After months in development, v0.3 has finally been released to crates.io.
This is a huge release amounting to a near total rewrite of the library
and a major step towards a stable 1.0 release.

[Check out the v0.3 announcement post](https://amethyst.rs/posts/legion-ecs-v0.3)
for an overview of the new API and all the updates.

The project’s repo has also been moved to the Amethyst org to reflect its close collaboration with the Amethyst community.

*Discussions:
/r/rust*

[Thunderdome](https://github.com/LPGhatguy/thunderdome) is a ~~gladitorial~~ generational arena library inspired by
[generational-arena](https://crates.io/crates/generational-arena), [slotmap](https://crates.io/crates/slotmap), and [slab](https://crates.io/crates/slab). It provides constant time
insertion, lookup, and removal via small (8 byte) keys that stay 8 bytes when
wrapped in `Option<T>`

.

Data structures like Thunderdome’s `Arena`

store values and return keys that can
be later used to access those values. These keys are stable across removals and
have a generation counter to solve the [ABA Problem](https://en.wikipedia.org/wiki/ABA_problem).

```
let mut arena = Arena::new();
let foo = arena.insert("Foo");
let bar = arena.insert("Bar");
assert_eq!(arena[foo], "Foo");
assert_eq!(arena[bar], "Bar");
arena[bar] = "Replaced";
assert_eq!(arena[bar], "Replaced");
let foo_value = arena.remove(foo);
assert_eq!(foo_value, Some("Foo"));
// The slot previously used by foo will be reused for baz.
let baz = arena.insert("Baz");
assert_eq!(arena[baz], "Baz");
// foo is no longer a valid key.
assert_eq!(arena.get(foo), None);
```


*Discussions:
twitter*

[Fontdue](https://github.com/mooman219/fontdue) is a simple, no_std, pure Rust, TrueType & OpenType
font rasterizer and layout tool.
It strives to make interacting with fonts as fast as possible,
and currently has the lowest end to end latency for a font rasterizer.

Fontdue depends on [ttf-parser](https://github.com/RazrFalcon/ttf-parser) for parsing fonts,
which supports a wide range of TrueType and OpenType features.

A non-goal of this library is to be allocation free and have a fast, “zero cost” initial load. Fontdue does make allocations and depends on the alloc crate. Fonts are fully parsed on creation and relevant information is stored in a more convenient to access format. Unlike other font libraries, the font structures have no lifetime dependencies since it allocates its own space.

Project’s roadmap:

- v1.0: fontdue is designed to be a replacement for rusttype, ab_glyph, parts of glyph_brush, and glyph_brush_layout. This is a class of font libraries that don’t tackle shaping.
- v2.0: Shaping - the complex layout of text such as Arabic and Devanagari - will be added. There are two potential pure Rust libraries (allsorts or rustybuzz) that are candidates for providing a shaping backend to Fontdue, but are relatively immature right now.

*Discussions: /r/rust*

[ultraviolet](https://crates.io/crates/ultraviolet) by [@fu5ha](https://twitter.com/fu5ha) is a crate for computer-graphics
and games-related linear algebra, but *fast*,
both in terms of productivity and in terms of runtime performance.

This month [ultraviolet v0.6](https://fusha.moe/blog/posts/ultraviolet-0.6) was released.
Updates include:

- Support for 256-bit wide AVX vectors and instructions as well as 128-bit wide SSE instructions which were already supported.
- Support for f64/double precision floats under the f64 feature, including f64x2 and f64x4 SIMD-accelerated types.
- Support for
[mint](https://github.com/kvark/mint)for most scalar types. - Lots of smaller API and performance improvements.

*Discussions:
/r/rust*

[Mun](https://mun-lang.org) is a scripting language for gamedev focused on quick iteration times
that is written in Rust.

[September updates](https://mun-lang.org/blog/2020/10/01/this-month-september/) include:

- on-going work for multi-file projects;
- build pipeline improvements;
- bug fixes in the Mun compiler and C++ bindings;
- a lot of refactors and quality of life improvements.

[audir](https://github.com/norse-rs/audir) is a low level audio library supporting Windows (WASAPI), Linux (Pulse)
and Android (OpenSLES & AAudio).

It aims at providing a minimal and mostly unsafe but feature-rich API on top of common audio backends with focus on gaming applications. The initial release version 0.1.0 provides basic recording and playback support for all available backends, including a small music player example!

Currently looking into coupling with [dasp](https://github.com/RustAudio/dasp) for dsp audio graphs to provide
a higher level entry point.

[Crevice](https://github.com/LPGhatguy/crevice) is a library that helps define GLSL-compatible (std140) structs for
use in uniform and storage buffers. It uses new `const fn`

capabilities
stabilized in [Rust 1.46.0](https://blog.rust-lang.org/2020/08/27/Rust-1.46.0.html) to align types with explicitly zeroed padding.

Crevice depends heavily on [mint](https://github.com/kvark/mint) to support almost any Rust math library. It
also contains helpers for safely sizing and writing buffers, making dynamic
buffer layout a breeze.

```
#[derive(AsStd140)]
struct MainUniform {
orientation: mint::ColumnMatrix3<f32>,
position: mint::Vector3<f32>,
scale: f32,
}
let value = MainUniform {
orientation: cgmath::Matrix3::identity().into(),
position: [1.0, 2.0, 3.0].into(),
scale: 4.0,
};
upload_data_to_gpu(value.as_std140().as_bytes());
```


*Discussions:
twitter*

![femtovg](../../assets/528442b5cff2e63f.png)


[FemtoVG](https://github.com/femtovg/femtovg) is a 2D canvas API in Rust, based on [nanovg](https://github.com/memononen/nanovg).

Currently, FemtoVG uses OpenGL as a rendering backend. A Metal backend is 95% done, and a wgpu backend is on the roadmap. The project is definitely looking for contributors.

Unlike NanoVG, FemtoVG has full text-shaping support thanks to harfbuzz.

FemtoVG, just like the original NanoVG, is based on the *stencil-then-cover*
approach presented in [GPU-accelerated Path Rendering](https://github.com/femtovg/femtovg/blob/master/assets/gpupathrender.pdf).

Join the [Discord channel](https://discord.gg/V69VdVu)
or follow [FemtoVG on twitter](https://twitter.com/femtovg).

[gfx-rs](https://github.com/gfx-rs/gfx) and [gfx-portability](https://github.com/gfx-rs/portability) [#](https://gamedev.rs#gfx-rs-and-gfx-portability)

![gfx-rs logo](../../assets/397c2e46dead062a.png)


[gfx-portability](https://github.com/gfx-rs/portability) is a Vulkan portability implementation based on [gfx-rs](https://github.com/gfx-rs/gfx).
It’s basically a drop-in implementation of Vulkan on top of Metal and D3D12,
useful on platforms that don’t have native Vulkan support, or have buggy drivers.

It released version [0.8.1](https://github.com/gfx-rs/portability/releases/tag/0.8.1)
with official support for the new [KHR portability extension](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/man/html/VK_KHR_portability_subset.html),
as well as a few other extensions, plus a number of correctness fixes.

gfx-rs team asks Rust users of Vulkano, Ash, and other Vulkan-only wrappers to try out the gfx-portability as a solution on macOS and relevant Windows 10 platforms.

In [gfx-rs](https://github.com/gfx-rs/gfx) itself, the DX12 backend, and the descriptor indexing feature support
got improved. There has been a push to get DX11 backend in a solid shape,
and it can now run [vange-rs](https://github.com/kvark/vange-rs) pretty well 🎉.

[Riddle](https://github.com/vickles/riddle) is a Rust media library in the vein of SDL,
building as far as possible on the most active/standard Rust libraries
(winit, wgpu, image, etc). Riddle is deliberately not an engine, or a framework.
It is a library devoted to exposing media related features in a unified way while
avoiding prescribing program structure. It provides abstractions over windowing,
input, audio, image loading/manipulation and provides a basic wgpu based 2D
renderer.
The [docs](https://vickles.github.io/riddle/0.1.0/riddle) contain runnable examples for most methods and types.

The goal is to provide a stable foundation, resilient to developments in the Rust gamedev ecosystem, on which games, custom engines, and other media applications can be built.

*Discussions:
/r/rust_gamedev*

[bracket-lib](https://github.com/thebracket/bracket-lib) (previously `rltk_rs`

) by [@blackfuture](https://patreon.com/blackfuture)
is a Rust implementation of [C++ Roguelike Toolkit](https://github.com/thebracket/rltk).

Bracket-lib is going through a stability pass, focusing on freezing the API.
It will be featured in the author’s upcoming book:
*Hands-on Rust: Effective Learning through 2D Game Development and Play*.
The book should be going into early access/beta in time for the next newsletter.



![quadgames](../../assets/bc314ce166624b0a.gif)

[macroquad](https://github.com/not-fl3/macroquad) by [@fedor_games](https://twitter.com/fedor_games) is a cross-platform
(Windows/Linux/macOS/Android/iOS/WASM)
game framework build on top of [miniquad](https://github.com/not-fl3/miniquad).

This month 0.3 preview was released, featuring:

-
Improved

[documentation](https://docs.rs/macroquad/0.3.0-alpha.0/macroquad/index.html)on docs.rs. -
Screen reading shaders and a

[tutorial about them](https://not-fl3.github.io/platformer-book/screen-reading.html). -
Updated “shadertoy” - small interactive GLSL playground - example. Check out the

[web demo](https://not-fl3.github.io/miniquad-samples/shadertoy.html)and its[source code](https://github.com/not-fl3/macroquad/blob/master/examples/shadertoy.rs).

Also, [@not-fl3](https://github.com/not-fl3) (the main developer of all current *quad projects)
has been added to the GitHub Sponsors.
Check out the project’s story, vision, and roadmap
on the new [sponsors page](https://github.com/sponsors/not-fl3)!

[Tetra](https://github.com/17cupsofcoffee/tetra) is a simple 2D game framework, inspired by XNA and Raylib. This month,
version [0.5](https://twitter.com/17cupsofcoffee/status/1301210538299609088) was released, featuring:

- Cargo feature flags, allowing you to remove unused functionality and shrink your build
- Relative mouse events and infinite mouse movement (allowing for FPS-style control schemes)
- Extra methods for getting and setting the state of a playing sound

For full details and a list of breaking changes, see the [changelog](https://github.com/17cupsofcoffee/tetra/blob/main/CHANGELOG.md).

Additionally, this month [puppetmaster](https://github.com/puppetmaster-) released [tetrapack](https://github.com/puppetmaster-/tetrapack), a set of useful
extensions for Tetra. This includes:

- Helpful timer types
- Looping background music
- Custom mouse cursors
- Input utility functions
- Tilemaps and tile animations

[Bevy](https://bevyengine.org) is a refreshingly simple data-driven game engine built in Rust.
It is [free and open source](https://github.com/bevyengine/bevy) forever!

This month, thanks to 87 contributors, 174 pull requests, and their
[generous sponsors](https://github.com/sponsors/cart), Bevy 0.2 was released. You can view the
[full Bevy 0.2 announcement here](https://bevyengine.org/news/bevy-0-2). Here are some highlights:

- Async Task System: Bevy now has a brand new async-friendly task system, which enables the creation of context-specific task pools. For example, you might have separate pools for compute, IO, networking, etc. This also provides the flexibility to load balance work appropriately according to work type and/or priority. This new task system completely replaces Rayon and the cpu usage wins were huge!
- Initial Web Platform Support: (A subset of) Bevy now runs on the web using WebAssembly/WASM! Specifically, Bevy apps can run Bevy ECS schedules, react to input events, create an empty canvas (using winit), and a few other things. This is a huge first step, but it is important to call out that there are still a number of missing pieces, such as 2D/3D rendering, multi-threading, and sound.
- Parallel Queries: Systems that use queries already run in parallel, but before this change the queries themselves could not be iterated in parallel. Bevy 0.2 adds the ability to easily iterate queries in parallel, which builds on top of the new Async Task System.
- Transform System Rewrite: Bevy’s old transform system used separate
`Translation`

,`Rotation`

, and`Scale`

components as the “source of truth”, which were then synced to a`LocalTransform`

component after each update. There are Good Reasons™ to use this approach, but it created a “lag” between the calculated LocalTransform and the source components and dataflow between components is hard to reason about. This problem was resolved by making a newer, simpler transform system that uses a consolidated`Transform`

type. - Joystick/Gamepad Input: The Bevy Input plugin now has cross-platform support for most controllers thanks to the gilrs library!
- Bevy ECS Performance Improvements: generational entity IDs, read-only queries, lock-free world APIs, direct component lookup.

Community plugin updates:

[bevy_rapier](https://github.com/dimforge/bevy_rapier): Rapier Physics’ official Bevy plugin was updated to support Bevy 0.2.[bevy_ninepatch](https://crates.io/crates/bevy_ninepatch): Display 9-Patch UI elements, where you can specify how different parts of a PNG should grow.[bevy_mod_picking](https://github.com/aevyrie/bevy_mod_picking): 3d cursor picking and highlighting.[bevy_contrib_colors](https://crates.io/crates/bevy_contrib_colors): A simple color library.[bevy_input_map](https://crates.io/crates/bevy_prototype_input_map): Converts user inputs from different input hardware into game specific actions. Ex: keyboard “Space” or joystick “A” can be mapped to a “Jump” Action.[bevy_prototype_lyon](https://github.com/Nilirad/bevy_prototype_lyon): Draw 2D shapes, like triangles, circles, and beziers.[bevy_contrib_inspector](https://github.com/jakobhellermann/bevy-contrib-inspector): Visually edit fields of your bevy resources in a browser or native view.

*Discussions:
/r/rust,
hacker news,
twitter*



![a scene with lightning and a hi-poly character model](../../assets/1d1721f12c5d8863.jpg)

[video demo of one of the new examples](https://twitter.com/DmitryS36934349/status/1312836831390687232).

[rg3d](https://github.com/mrDIMAS/rg3d) is a game engine that aims to be easy to use and provide large set
of out-of-box features. Some of the recent updates:

- Render to texture - it is possible to render scenes into textures.
- Added support for scenes made in
[rusty-editor](https://github.com/mrDIMAS/rusty-editor). - Added sprite graph node.
- Added simple lightmapper (still WIP).
- Added new UI widgets and features:
- Message box - classic message box with different combinations of buttons.
- Wrap panel - arranges its children by rows or columns with wrapping.
- File browser - a browser for file system.
- Color picker - classic HSV+RGB+Alpha color picker.
- “Bring into view” for scroll panel.
- Replaced font rasterizer by fontdue.
- Improved hotkeys in text box.

- Improved performance and documentation.

Join the [rg3d’s Discord channel](https://discord.gg/xENF5Uh)
or follow [Dmitry Stepanov on twitter](https://twitter.com/DmitryS36934349).

![rusty editor](../../assets/8e49f2e3b9c2b37b.jpg)


[rusty-editor](https://github.com/mrDIMAS/rusty-editor) is a scene editor for the [rg3d](https://github.com/mrDIMAS/rg3d) engine.
Some of the recently added features:

- asset browser + asset previewer,
- multiselection,
- improved properties editor,
- lots of other small improvements and fixes.

[godot-rust](https://godot-rust.github.io/) v0.9 [#](https://gamedev.rs#godot-rust-v0-9)

![cute logo](../../assets/c7dfe700596fc38b.png)


[godot-rust](https://godot-rust.github.io/) provides high-level Rust bindings
to the [Godot game engine](http://godotengine.org).

This month [v0.9 was released](https://godot-rust.github.io/release-notes/0-9-0/).
Besides lots of quality-of-life improvements, this update brings a massive
redesign of the API in order to solve long-standing soundness problems.
As there’re numerous breaking changes,
a [chapter about migration from 0.8](https://godot-rust.github.io/book/migrating-0-8.html) was added
to the user guide.

## Popular Workgroup Issues in GitHub [#](https://gamedev.rs#popular-workgroup-issues-in-github)

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[winit’s “Good first issue” and “help wanted” issues](https://github.com/rust-windowing/winit/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+label%3A%22status%3A+help+wanted%22+label%3A%22Good+first+issue%22).[gfx-rs’s “contributor-friendly” issues](https://github.com/gfx-rs/gfx/issues?q=is%3Aissue+is%3Aopen+label%3Acontributor-friendly).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[A/B Street’s “good first issue” issues](https://github.com/dabreegster/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/good%20first%20issue).

That’s all news for today, thanks for reading!

Subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!