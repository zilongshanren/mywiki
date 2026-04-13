---
title: 'This Month in Rust GameDev #2 - September 2019'
url: https://gamedev.rs/news/002/
author: Rust GameDev WG
published: '2019-10-05'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the second issue of the Rust GameDev Workgroup’s monthly newsletter.

[Rust](https://rust-lang.org) is a systems language pursuing the trifecta:
safety, concurrency, and speed.
These goals are well-aligned with game development.

We hope to build an inviting ecosystem for anyone wishing
to use Rust in their development process!
Want to get involved? [Join the Rust GameDev working group!](https://github.com/rust-gamedev/wg#join-the-fun)

## Game Updates [#](https://gamedev.rs#game-updates)

![Town surrounded by a wall](../../assets/43621e850107f74e.png)


[Veloren](https://veloren.net) is an open-world, open-source multiplayer voxel RPG.
The game is in an early stage of development, but is playable.

Some of the September’s improvements:

- Improved multi-staged towns generation;
- Improved inventory system and character creation;
- Massive progress on water, water physics, lakes, and rivers!
- New chunks data structure;
- Three-dimensional map and minimap;
- First-person view;
- Bows and arrows;
- Performance optimization;

New video: [“24 Minutes of Alpha Gameplay”](https://youtube.com/watch?v=YyvXXCjpbqQ).

Full weekly devlogs “This Week In Veloren…”:
[#31](https://veloren.net/devblog-31),
[#32](https://veloren.net/devblog-32),
[#33](https://veloren.net/devblog-33),
[#34](https://veloren.net/devblog-34),
[#35](https://veloren.net/devblog-35).

![fighters smash demons in fire and poison clouds](../../assets/55b179834ac68967.png)


[Zemeroth](https://github.com/ozkriff/zemeroth) is a minimalistic 2D turn-based tactical game.

This month [Zemeroth v0.6](https://github.com/ozkriff/zemeroth/releases/tag/v0.6.0) was released.
Main features of this release are:

- renown and fighter upgrades,
- possessions,
- sprite frames and flips,
- status effect icons.

Read the [full devlog post](http://ozkriff.games/2019-09-21--devlog-zemeroth-v0-6) or watch [the video version](http://youtu.be/6tZByt4LBlU).

[@VladZhukov0](https://twitter.com/VladZhukov0) published a few devlogs about their
[“Twenty Asteroids”](https://itch.io/queue/c/449652/rustlang-games?game_id=477762) game:

Updates include:

- New enemies: a ship with a big pinball-like bullet and a laser-mesh ship;
- New upgrades: laser range and bullets reflection;
- Explosion size now depends on asteroid’s size;
- Improved main menu, upgrade and death screens;
- Better color contrast;
- New AI behaviors: follow and circle around;
- Debugging performance plots;

-
[Space Shooter v0.1.3](https://github.com/amethyst/space_shooter_rs/releases/tag/v0.1.3)by[@carlosupina](https://twitter.com/carlosupina)introduced a currency system, shop system, and sound effects:[watch the devlog video](https://youtube.com/watch?v=MmdUrZzuGfw). -
![Stabman in the beginning of the overworld level](../../assets/7cacde98a4d8d7e1.png)

-
[@mvlabat](https://twitter.com/mvlabat)is[working on interpolation in his multiplayer prototype (video)](https://youtu.be/xJm6cI_XmT4). -
[Azriel Hoh](https://twitter.com/im_azriel)released[a major new devblog update titled “Focus!”](https://azriel.im/will/2019/09/27/focus).![bots attack](../../assets/34eb1dbc463c0e18.png)

-
[@webshinra](https://twitter.com/Webshinra)made progress with raycasted FOV in their hexagonal game.![hexagonal map with two mechs, paths and visually blocked tiles](../../assets/b29e19f5c6c89db3.jpeg)


### Other Game News [#](https://gamedev.rs#other-game-news)

-
[@dooskington](https://twitter.com/dooskington)published their 5th devlog:[“Stats And Skills”](https://dooskington.com/dev-log/5);![Stats and skill demo](../../assets/aec28e371538bc6a.jpeg)

-
[Alex Butler](https://twitter.com/bigabgames)continues to polish their “[Robo Instructus](https://steamcommunity.com/games/1032170/announcements/detail/1604892840079306082)” game;[1.8, 1.9, 1.10 and 1.11 versions were released](https://steamcommunity.com/app/1032170/allnews): official macOS support, bugfixes, and better translations.![Robo Instructus gameplay screenshot with full UI](../../assets/40427b09e1b2595c.jpg)

-
[@Wraithan got tower placement working](https://twitter.com/Wraithan/status/1172982932341805056)in their “WraithDefense” tower defence game; the development process[is streamed on Twitch](https://twitch.tv/wraithan).![Towers on the map](../../assets/eb6405713a5427df.jpeg)

-
[@oliviff](https://twitter.com/oliviff)released[v0.0.1](https://twitter.com/oliviff/status/1168556346431692800)and[v0.0.2](https://twitter.com/oliviff/status/1172912164488843265)updates for[Tennis Academy](https://iolivia.me/posts/6-months-of-rust-game-dev): simplified gameplay flow, areas, cash flow, animations, players’ state visual cues and more.![Tennis Academy v0.0.2 Demo](../../assets/bfe6e14ed953cbdb.gif)

-
The

[Garden](https://epcc.itch.io/garden)game is[under active development again](https://twitter.com/logicsoup/status/1174259591250661379). Devlogs[are coming soon!](https://twitter.com/logicsoup/status/1166469607412158464)![a screenshot from Garden showing a build and some trees](../../assets/b9cd193039e5d385.jpeg)

-
[“Live”](https://nuria.itch.io/live-rust)by[@pincfloit](https://twitter.com/pincfloit)- a small command-line interface survival game [[twitter](https://twitter.com/pincfloit/status/1173965160089837568),[github](https://github.com/codegram/live-rust)]. -
[@MrVallentin](https://twitter.com/MrVallentin)tweeted a bunch of updates about their voxel engine:[falling cubes](https://twitter.com/MrVallentin/status/1170164060542918656),[text rendering](https://twitter.com/MrVallentin/status/1170515003113451520),[60M cubes generated in the blink of an eye](https://twitter.com/MrVallentin/status/1171773622039515136),[remeshing](https://twitter.com/MrVallentin/status/1171774889335951361),[retrospective video](https://twitter.com/MrVallentin/status/1174493952894033920),[saving and loading](https://twitter.com/MrVallentin/status/1176996637681623042), and some more.![screenshot of the WIP terrain generation](../../assets/f669fe7049b73d0c.jpeg)

-
[@Mistodon](https://twitter.com/Mistodon)got their entire game[“Disconnect”](https://mistodon.itch.io/disconnect)to[render in the terminal](https://twitter.com/Mistodon/status/1175361784246603776);

## Library & Tooling updates [#](https://gamedev.rs#library-tooling-updates)

[gfx-rs](https://github.com/gfx-rs/gfx) is a Rust project aiming to make low-level GPU programming
portable with low overhead.
It’s a single Vulkan-like Rust API with multiple backends that implement it:
Direct3D 12/11, Metal, Vulkan, and even OpenGL.

[wgpu-rs](https://github.com/gfx-rs/wgpu-rs) is a Rust project on top of gfx-rs that provides safety,
accessibility, and even stronger portability.

- gfx-rs was slimmed down: “magical” deps (like
[failure](https://github.com/rust-lang-nursery/failure)and[derivative](https://github.com/mcarton/rust-derivative)) were removed and it sped up the fresh gfx-hal build by a factor of 8.5X; the “typed” layer of gfx-hal got removed. - Backend features were removed from wgpu-rs;
- An entirely new
[swapchain](https://vulkan-tutorial.com/Drawing_a_triangle/Presentation/Swap_chain)model was prototyped and implemented.

*Discussions:
/r/rust*

![Mun text logo](../../assets/5ce7d7a37e037cbc.png)


[Mun](https://mun-lang.org) is a scripting language for gamedev
focused on quick iteration times that is written in Rust.

Mun’s pillars:

- Hot Reloading. Mun natively supports hot reloading - the process of changing code and resources while an app is running - on all target platforms and consoles with marginal runtime overhead. Its runtime has useful error messages, and can easily be embedded into other languages.
- Static Typing. Mun’s type system eliminates an entire class of runtime errors and provides powerful IDE integration with auto-completion and refactoring tools allowing developers to focus on writing code.
- Performance. Mun uses LLVM to compile to machine code that can be natively executed on any target platform, guaranteeing the best possible runtime performance.

The driving force behind the development of Mun is natively supported hot reloading for functions and data. As such, the language and its syntax will keep growing at the rate in which hot reloading-supported semantics is added. Currently, the language looks like this:

```
fn main() {
let sum = add(a, b);
// Comments: Mun natively supports bool, float, and int
let is_true = true;
let var: float = 0.5;
}
// The order of function definitions doesn't matter
fn add(a: int, b: int): int {
a + b
}
```


The source code of the project
[is available on GitHub](https://github.com/mun-lang/mun)
under the MIT or Apache licenses.

Mun’s runtime is implemented in Rust.
Check out [a GIF demo of the Rust hot reloading functionality](https://reddit.com/r/rust/comments/cywwtv/progress_on_hot_reloading_experimentation_in_rust)
that shows:

- Catching and logging of errors (e.g. type mismatch),
- hot reloading of a shared library’s symbols (used for reflection) and method logic,
- runtime invocable methods and type/method reflection.

*Discussions:
/r/rust*

### Rust [Roguelike Toolkit](https://github.com/thebracket/rltk_rs) and [Roguelike Tutorial](https://bfnightly.bracketproductions.com/rustbook) [#](https://gamedev.rs#rust-roguelike-toolkit-and-roguelike-tutorial)

![Minimal pathfinding and FoV example](../../assets/5cdafe38fafc7285.gif)


[rltk_rs](https://github.com/thebracket/rltk_rs) by [@herberticus](https://patreon.com/blackfuture) is a Rust implementation of
[C++ Roguelike Toolkit](https://github.com/thebracket/rltk) ([what is a “roguelike?”](https://en.wikipedia.org/wiki/Roguelike)).

It provides all the basic functionality one needs to write a roguelike game, as well as mouse support, an embedded resource system, Web Assembly support, and more.

All [examples](https://github.com/thebracket/rltk_rs#examples) are linked to browser WASM to try.

The back-end uses [glow](https://github.com/grovesNL/glow) to abstract OpenGL between versions.
API for embedding assets directly into your binary.

If you’d like to see a functional roguelike that uses rltk_rs,
check out [Rusty Roguelike](https://github.com/thebracket/rustyroguelike).

[The Roguelike Tutorial](https://bfnightly.bracketproductions.com/rustbook) includes more than 20 chapters now
and continues to grow.

It covers topics from “hello rust” and “what is an ECS?” to adding monsters, equipment, nice menus, save/load, multiple levels, bloodstains, particle effects, magic mapping scrolls, and more.

The tutorial has Web Assembly links to all examples so you can run them in your browser.

![Generated textures samples](../../assets/9082b8b1192284b0.jpg)


[Embark](https://embark.games) has open-sourced their texture synthesis crate ** texture-synthesis**.
It’s an example-based non-parametric image generation algorithm
written in Rust.

[The repo](https://github.com/EmbarkStudios/texture-synthesis) also includes multiple
code examples along with test images,
and a compiled binary with a command-line interface
can be found under the release tab.

Also, see a great long recorded talk
[“More Like This, Please! Texture Synthesis and Remixing from a Single Example”](https://youtu.be/fMbK7PYQux4)
which explains this technique and the background more in-depth.

Full list of stuff that [Embark](https://embark.games) has released so far:
[embark.rs](http://embark.rs).

*Discussions:
twitter*

Also,

[Embark will be sponsoring RustFest in Barcelona this year.](https://twitter.com/AriVanider/status/1171359194336903169)[Embark started hiring new grads](https://embark.games/position/software-engineer-new-grad)[[twitter](https://twitter.com/AriVanider/status/1173903615498567680)].

Iced is a renderer-agnostic GUI library focused on simplicity and type-safety.
It was originally born as an attempt at bringing the simplicity of [Elm](https://elm-lang.org)
and The Elm Architecture into [Coffee 2D game engine](https://github.com/hecrj/coffee).

Features:

- Simple, easy-to-use, renderer-agnostic API;
- Responsive, flexbox-based layouting;
- Type-safe, reactive programming model;
- Lots of built-in widgets and custom widget support.

Check out [the design overview in the repo’s README](https://github.com/hecrj/iced#overview).

*Discussions:
/r/rust*

![amethyst logo](../../assets/6692a81ae6e6d242.png)


[Amethyst](https://amethyst.rs) is a game engine and tool-set
for ambitious game developers.
It enables game developers to make complex games without getting
into too much trouble, by means of data-driven design
and the ECS architecture.

Tooling:

-
[Amethyst Engine v0.13 was released](https://github.com/amethyst/amethyst/releases/tag/v0.13.0). A new`amethyst_tiles`

crate was added and[the Pong tutorial](https://book.amethyst.rs/stable/pong-tutorial/pong-tutorial-06.html)is now complete with the addition of an audio section. -
[@_AndreaCatania](https://twitter.com/_AndreaCatania)published an[“Initialize physics world - Amethyst physics tutorial #1”](https://youtube.com/watch?v=XzSKuY9nv7A)video. -
[amethyst-imgui v0.5 is out](https://twitter.com/AmethystEngine/status/1177720011013709824), supporting a beta-version of the new imgui docking feature.![docking widgets demo](../../assets/2d9ee8fc03f18987.gif)

-
[“How to do a turn-based game with the ECS pattern”](https://community.amethyst.rs/t/classic-turn-based-workflow-how-to/1082/20)post, by[@webshinra](https://twitter.com/webshinra). -
[@valkum](https://github.com/valkum)is[implementing area lights using linearly transformed cosines](https://youtube.com/watch?v=KVpLPInWRWg).

![Recall Singularity’s ship base](../../assets/f175a98fa40eee88.jpeg)


[Tom Leys](https://twitter.com/RecallSingular1) is working on a “The Recall Singularity” game
about designing autonomous factory ships and stations
and this month they published a few posts
about using [the Godot engine](https://godotengine.org) with Rust:

[“How I use Rust and Godot to Explore Space”](https://blog.usejournal.com/how-i-use-rust-and-godot-to-explore-space-806bb810e950)[[/r/godot](https://reddit.com/r/godot/comments/d5qdoy/inspiration_how_i_use_rust_and_godot_to_explore)];[“Gorgeous Godot games in Rust”](https://medium.com/@recallsingularity/gorgeous-godot-games-in-rust-1867c56045e6)[[/r/rust](https://reddit.com/r/rust_gamedev/comments/d75qfz/gorgeous_godot_games_in_rust)];[“A Basic Godot-Rust Structure”](https://medium.com/@recallsingularity/a-basic-godot-rust-structure-eb855ba07223);

![Top-down view on a generated dungeon](../../assets/ffa0b3168072d2ec.png)


[@whostolemyhat](https://twitter.com/whostolemyhat) published the fourth part
of their tutorial series on procedural generation with Rust.
In this tutorial, the room generation is updated so it can pick from a selection
of pre-built room patterns as well as create the standard empty room.

*Discussions:
/r/rust*

### Other Library & Tooling News [#](https://gamedev.rs#other-library-tooling-news)

-
- an implementation of sets and maps designed for small and medium number of stored elements which change quickly - i.e. in a dynamically evolving scene in a video game.**uset** -
- a parser and runtime for[blend](https://github.com/lukebitts/blend)[Blender](https://blender.org)’s .blend files that can be used to read (almost) everything inside the file: from mesh data, materials, cameras and animations to user preferences, window locations and render settings [[/r/rust](https://reddit.com/r/rust/comments/d70lu6/blend_a_parser_and_runtime_for_blenders_blend)]. -
(Rust bindings for[cubism-rs](https://github.com/Veykril/cubism-rs)[Live2D Cubism](https://www.live2d.com/en/download/cubism-sdk)) got renderer support for[Piston2D](https://www.piston.rs).![Live2D Piston demo](../../assets/5532bcd8c29f14bd.png)

-
[“GitHub Actions CI with Rust and SDL2”](https://alexene.dev/2019/09/04/Github-actions-CI-rust-SDL2.html)-[Alexandru Ene](https://twitter.com/_AlexEne_)wrote a post about CI with[github actions](https://github.com/features/actions)for[their hobby game project](https://alexene.dev/2019/01/15/After-hours-game-development.html)that uses Rust and SDL2.![GitHub Actions with SDL2 screencast demo](../../assets/c35d5198c5d7a1fc.gif)

-
[@phaazon](https://github.com/phaazon)released[luminance](https://crates.io/crates/luminance)0.33 that[brings geometry instancing support](https://reddit.com/r/rust/comments/d0us73/announcement_luminance033); also, the third wiki chapter[“Wavefront .obj loader”](https://github.com/phaazon/luminance-rs/wiki/Wavefront-.obj-loader)was released.![loaded and lighted Suzanne model](../../assets/b3cfaa4381de3e14.png)

-
[phaazon/spline-editor](https://github.com/phaazon/spline-editor)- a simple spline editor for the[splines crate](https://crates.io/crates/splines)written using[luminance](https://crates.io/crates/luminance).![complex spline in the editor](../../assets/51f30932dccd9a07.png)

-
[@magistratic](https://twitter.com/magistratic)gave a talk on the Doom’s[BSP](https://en.wikipedia.org/wiki/Binary_space_partitioning)rendering engine using their Rust implementation as a demonstration at RevolverConf: recording (in Norwegian) and a WASM demo available[here](https://magnushoff.com/blog/doom-revolverconf)([source code](https://github.com/maghoff/wad-render/tree/revolverconf-2019.2)).![WASM demo](../../assets/70b5192943e3c491.png)

-
by**rx**[@cloudhead](https://cloudhead.io)is a modern pixel editor and animator; this month, v0.2.0 was released, with new brush modes - pixel perfect drawing, symmetry and multi-frame drawing - a new GLFW backend and`.gif`

output. [[/r/rust](https://reddit.com/r/rust/comments/dauizc/rx_v020_released_a_modern_pixel_editor),[github](https://github.com/cloudhead/rx)]. -
Pixel art editor

is now[Xprite](https://pickitup247.com/xprite.html)[open source under GNU GPL](https://github.com/rickyhan/xprite-editor)[[/r/rust](https://reddit.com/r/rust/comments/d4r0o3/pixel_art_editor_xprite_is_now_open_source),[/r/rust_gamedev](https://reddit.com/r/rust_gamedev/comments/d3vl65/xprite_is_now_open_source)].![XPrite drawing demo](../../assets/5a5810cf6a363b40.gif)

-
by ([minimum](https://github.com/aclysma/minimum)[@aclysma](https://twitter.com/aclysma)) is a game development framework that provides basic tooling and a content authoring workflow; this month, rendering of draggable shapes in the editor and rotation/scaling were added [[YouTube demo](https://youtube.com/watch?v=BON_RvVFiWY)].![editor with a bunch of shapes](../../assets/dc303ba448700825.png)

-
The

macro-based property editor by[imgui-inspect](https://github.com/aclysma/imgui-inspect)[@aclysma](https://twitter.com/aclysma)is a by-product of the above-mentioned “minimum” project.![inspector widget with position, debug draw rect, and physics body sub-widgets](../../assets/119149c8d585a027.png)

-
[Project Deios](https://kickstarter.com/projects/dungeonfog/project-deios-dungeonfog-mapmaker-suite-for-worldbuilders)decided to implement their core in Rust and has been looking for a Rust graphics programmer:[/r/rust announcement](https://reddit.com/r/rust/comments/d487dr/were_looking_for_a_rust_graphics_programmer).![Deios logo ant promo pic](../../assets/ffa8656d10e64608.jpg)


## Popular Workgroup Issues in GitHub [#](https://gamedev.rs#popular-workgroup-issues-in-github)

[#36 “Adoption of Rust over time in existing game codebases”](https://github.com/rust-gamedev/wg/issues/36)[#48 “Placement New”](https://github.com/rust-gamedev/wg/issues/48)[#49 “Branch prediction hints (i.e. Likely/Unlikely)”](https://github.com/rust-gamedev/wg/issues/49)[#51 “Using wasm-bindgen for games”](https://github.com/rust-gamedev/wg/issues/51)

## Meeting Minutes [#](https://gamedev.rs#meeting-minutes)

[See all meeting issues](https://github.com/rust-gamedev/wg/issues?q=label%3Ameeting) including full text notes
or [join the next meeting](https://github.com/rust-gamedev/wg#join-the-fun).

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[winit](https://github.com/rust-windowing/winit):[gfx-rs’s “contributor-friendly” issues](https://github.com/gfx-rs/gfx/issues?q=is%3Aissue+is%3Aopen+label%3Acontributor-friendly);[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22);[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22);- Request from Amethyst:
[“The renderer-agnostic GUI library “Iced” by @hecrj looks](https://twitter.com/AmethystEngine/status/1169922826033336320).*so*good. If someone wants to make this work with Amethyst please get in touch with us! (or just do it…)”

## Bonus [#](https://gamedev.rs#bonus)

Just an interesting Rust gamedev link from the past. :)

** Sandspiel** is a falling sand game by

[@MaxBittker](https://maxbittker.com)built in late 2018 using Rust (via WASM), WebGL, and some JS glueing things together.

Sandspiel is a pixel physics simulation sandbox where you can paint with elements, conduct experiments and build your own world!

Elements include Ice, Water, Sand, Lava, Fire, Oil, Plant, Fungus, and many more!

The goal was to produce an cellular automata environment that’s interesting to play with and supports the sharing and forking of fun creations with other players. Ultimately, I want the platform to support editing and uploading of your own elements via a programmable cellular automata API.


The history of the game and the development process are documented in a great
** “Making Sandspiel”** blog post.

The game’s community is still active: check
[@sandspiel_feed feed of uploads](https://twitter.com/sandspiel_feed).

*Discussions:
/r/rust,
/r/programming,
hacker news*

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!