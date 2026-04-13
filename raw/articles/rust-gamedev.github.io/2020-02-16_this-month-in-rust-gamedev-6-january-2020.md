---
title: 'This Month in Rust GameDev #6 - January 2020'
url: https://gamedev.rs/news/006/
author: Rust GameDev WG
published: '2020-02-16'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the sixth issue of the Rust GameDev Workgroup’s monthly newsletter.

[Rust](https://rust-lang.org) is a systems language pursuing the trifecta:
safety, concurrency, and speed.
These goals are well-aligned with game development.

We hope to build an inviting ecosystem for anyone wishing
to use Rust in their development process!
Want to get involved? [Join the Rust GameDev working group!](https://github.com/rust-gamedev/wg#join-the-fun)

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).
Feel free to send PRs about your own projects!

[Ready at Dawn Studios](https://readyatdawn.com) is Hiring [#](https://gamedev.rs#ready-at-dawn-studios-is-hiring)

[@AndreaPessino](https://twitter.com/AndreaPessino) have announced that [Ready At Dawn Studios](https://readyatdawn.com) is hiring:

See the linked Twitter threads for details.

![Rustacean Station logo](../../assets/f27c1c24f2e42cc2.jpg)


[Jake Shadle](https://twitter.com/Ca1ne), a veteran of DICE/Frostbite,
was interviewed at [RustFest 2019](https://barcelona.rustfest.eu) by the [Rustacean Station](https://rustacean-station.org/episode/011-jake-yoshua-stjepan) podcast
on using Rust for game development at Embark Studios.
Topics/timestamps:

- [01:25] What is yours (and Embark’s) background in game development?
- [02:14] What is the relevance of the Frostbite engine and what is your experience with it?
- [04:15] What makes you think that Rust as a language is suitable for game development?
- [06:13] How is parallelism employed in a game engine on the scale of Frostbite?
- [07:07] Where is the Rust library ecosystem lacking for your use case, and what crates are you making use of?
- [11:13] Why is Embark interested in WebAssembly?
- [14:20] How can someone get in touch or learn more about Embark?

## Game Updates [#](https://gamedev.rs#game-updates)

![Morning landscape](../../assets/e821d653dbd2bc4a.png)


^ Morning landscape


[Veloren](https://veloren.net) is an open world, open-source voxel RPG
inspired by Dwarf Fortress and Cube World.

At the end of January, Veloren 0.5 was released! Most of January was spent on preparing for this. It was also the first anniversary of This Week in Veloren! There has been a devblog each week since the end of January last year. Here are some of the big changes in this release:

```
- Added initial region system implementation
- Added moon and clouds
- Added proper SFX system
- Added changelog
- Added Scrolling Combat Text (SCT) & Settings for it
- Added options to disable clouds and to use cheaper water rendering
- Added client-side character saving
- Added a localization system to provide multi-language support to voxygen
- Added fullscreen and window size to settings so that they can be persisted
- Added coverage based scaling for pixel art 28 new mobs
- Added waypoints
- Added pathfinding to NPCs
- Overhauled NPC AI
- Pets now attack enemies and defend their owners
- Added collars to tame wild animals
```


You can read more about some specific topics:

[How to Effectively Write a Proposal for the Game Design Team](https://veloren.net/devblog-49#how-to-effectively-write-a-proposal-for-the-game-design-team-by-silentium)[Iterator Problems](https://veloren.net/devblog-50#iterator-problems-with-angelonfira-and-sharp)[Erosion Worldgen Updates](https://veloren.net/devblog-50#erosion-worldgen-updates-by-sharp)[Airshipper Progress](https://veloren.net/devblog-52#airshipper-progress-by-songtronix)[Veloren For All Of Us: Localization System](https://veloren.net/devblog-52#veloren-for-all-of-us-localization-system-by-ender)[1 Year of This Week in Veloren](https://veloren.net/devblog-52#1-year-of-this-week-in-veloren-by-angelonfira)

![Sitting on the edge](../../assets/f40134dc50d3ccf4.png)


In February, the developers hope to push forward to 0.6 with a strong intro meeting. Authentication is slated to be released, as well as the Airshipper GUI beta. Hopefully, we also see controller support and improvements to the sound system as well.

January’s full weekly devlogs: “This Week In Veloren…”:
[#49](https://veloren.net/devblog-49),
[#50](https://veloren.net/devblog-50),
[#51](https://veloren.net/devblog-51),
[#52](https://veloren.net/devblog-52).

![Dwarfs, cow and campfire demo](../../assets/a9848d791698d9fc.gif)


[Alexandru Ene](https://alexene.dev) is working on a dwarf colony management game.
This month, a
[“Physically Based Temperature Simulation For Games”](https://alexene.dev/2020/01/10/Physically-based-temperature-simulation-for-games.html)
devlog was released:
how to adapt real-world thermodynamics formulas to a game
and why you may want to do it?

![itch collection of 12 games](../../assets/8490764e6da437ca.png)


[Micro Entertainment Pack](https://itch.io/c/707330/micro-entertainment-pack) is a collection of 12 tiny desktop games
by [Liam O’Connor](https://twitter.com/kamatsu8).

I like to watch terrible TV shows on my computer, but often they tend to drag so I like to have something else to do at the same time. Thus, I developed the Micro Entertainment Pack — fun casual games that fit in a fraction of your screen real estate. These games are inspired mostly by the Microsoft Plus! Entertainment packs for Windows, but I am also throwing in some other enjoyable titles from my days as a classic mac user.


All games in the pack are made using Liam’s [tesserae](https://crates.io/crates/tesserae) library for graphics composed
out of 8x8 2 colour tiles.
All graphics were drawn using the tesseraed editor that comes with the library.
All games use a common tileset to do all of their graphical drawing.

![Society scales](../../assets/c15b5b5218ea5797.png)


[Scale](https://github.com/Uriopass/Scale) is a new open-source project about modern day society simulation
from the bottom-up.

Each individual has its own thought model, meaning every action has its importance and influences the environment. Scale is not a video game, but rather a live artwork. The world itself won’t be generated or created by the user but is part of the project. That way, the focus is on the world itself and not on the tools to build it.


Also, check out
[the first devlog about the author’s motivation and vision](http://douady.paris/blog/scale_1.html).

*Discussions:
/r/rust_gamedev*

### Colony Genesis - ASCII Ant Colony Sandbox [#](https://gamedev.rs#colony-genesis-ascii-ant-colony-sandbox)

![New colony screenshot](../../assets/a7a957be14b7ffc1.png)


[Native Systems](https://nativesystems.rs) is working on a “Colony Genesis” ant colony sandbox game.

Current features:

- Procedurally generated world
- Day/night cycle and weather
- Temperature, humidity, and fluid simulation
- Food sources including aphid and fungus harvesting
- 6 castes governing ant behavior and attributes

*Discussions:
/r/rust_gamedev*

![Final game demo: snake eats red dots](../../assets/bcb11b8cc9fd6b03.gif)


[@jeremylikness](https://twitter.com/jeremylikness) started publishing a course
[“Snake Game With Rust, JavaScript, and WebAssembly”](https://medium.com/@geekrodion/snake-game-with-rust-javascript-and-webassembly-5e22b357ec7b).

We will learn how to export API implemented with Rust to JavaScript app. We will get to know canvas rendering, applications of vectors, and basics of game development.


At the moment, the series consists of six articles (of eight planned):

[Game Architecture](https://medium.com/@geekrodion/snake-game-with-rust-javascript-and-webassembly-929f79efc78f)[Creating Game Instance](https://medium.com/@geekrodion/snake-game-with-rust-javascript-and-webassembly-part-2-9d729b87c186)[Rendering the Game](https://medium.com/@geekrodion/snake-game-with-rust-javascript-and-webassembly-part-3-94b618db74a3)[Placing the Food](https://medium.com/@geekrodion/snake-game-with-rust-javascript-and-webassembly-part-4-1f20ab2638c4)[Game Loop](https://medium.com/@geekrodion/snake-game-with-rust-javascript-and-webassembly-part-5-7c114ce4583a)[Moving the Snake](https://medium.com/@geekrodion/snake-game-with-rust-javascript-and-webassembly-part-6-274a0f9bbbfe)

The source code can be found [in this repo](https://github.com/RodionChachura/rust-js-snake-game)
and you can [check out the game itself here](https://rodionchachura.github.io/rust-js-snake-game/).

[“12 Seconds Awake”](http://12-seconds-awake.psichix.io) by [@PsichiX](https://twitter.com/PsichiX) is a small 2D top-down
physics-based tank war game with worms-like turn mechanics
written using [Oxygengine](https://github.com/PsichiX/Oxygengine) (see “Oxygengine” section below).

*Discussions:
/r/rust_gamedev*

### Tennis Academy: Dash [#](https://gamedev.rs#tennis-academy-dash)

![menu, levels, and customers](../../assets/bfd5b44461e25084.gif)


[@oliviff](https://twitter.com/oliviff) released [v0.1.5 version](https://twitter.com/oliviff/status/1218632638136754182)
of “Tennis Academy: Dash”:

- 🍜 the puppy has a bowl
- 🛁 code refactoring and using clippy
- 💯 UI displaying score and other info

![COWs screenshot](../../assets/da3c16c5c4e7c956.png)


Another Game Off submission: [COWs](https://pilotinpyjamas.itch.io/cows) is a WIP puzzle game
about turning complete cows.

Welcome to the Logically Executed Automatic Paddock, or LEAP for short, where we keep our cows. Whoops, did I say cow? I meant to say COW. That stands for “Carry On Walking”.

I suppose all of our COWs happen to be cows too. What a coincidence!

Our COWs are bound together to solve puzzles. Some of our COWs are advanced enough that we call them COmputational Workers (COW for short). It’s a logical LEAP, but you’re BOUND to get it.


### Noodle Cat [#](https://gamedev.rs#noodle-cat)

![Debug rendering of Cat’s physics parts](../../assets/ed4f8fa7a76c0f38.png)


[@Fryer00](https://twitter.com/Fryer00) tweeted a bunch of updates about their WIP Box2D physics game prototype:

[snake kinematics](https://twitter.com/Fryer00/status/1212597726606692353)and[“air swimming” force](https://twitter.com/Fryer00/status/1217924172346728449);- 🐾
[paws grabbing](https://twitter.com/Fryer00/status/1216229512238829568)and[animation](https://twitter.com/Fryer00/status/1218167388165885952); [Harfbuzz-based text renderer](https://twitter.com/Fryer00/status/1219320622544838659);[debug rendering](https://twitter.com/Fryer00/status/1213770289999437825)and[interactive debugging settings](https://twitter.com/Fryer00/status/1220850604647555078);[extending](https://twitter.com/Fryer00/status/1222794916646006784).

### Urban Myth [#](https://gamedev.rs#urban-myth)

![relationships view mode](../../assets/893f8457d47f0abf.jpeg)


[@cmd_tea](https://twitter.com/cmd_tea) tweeted about the progress
of their [Allegro](https://github.com/SiegeLord/RustAllegro)-based superhero-themed game
“Urban Myth” (working title):

![Sticks that surround Pookie’s house](../../assets/c374bb2da5cd7c91.png)



[Akigi]is a multiplayer online world where most believe that humans are inferior.

Some of January’s updates:

- Autonomous NPC architecture & movement;
- New capuchin rigged mesh and animation;
- Chasing and basic combat system;

Full January’s devlogs:
[#049](http://devjournal.akigi.com/january-2020/2020-01-05.html),
[#050](https://devjournal.akigi.com/january-2020/2020-01-12.html),
[#051](https://devjournal.akigi.com/january-2020/2020-01-19.html),
[#052](https://devjournal.akigi.com/january-2020/2020-01-26.html).

![gameplay screenshot: ships and asteroids](../../assets/d57e0a3c23a9ca75.png)


[Split](https://mistodon.itch.io/split) is a game about outrunning a supernova
and using time travel to improve your chances.

In the middle of using time travel to research a dying star, you find yourself fleeing from a supernova. I know, who would have guessed.

On the route to safety are three When Points - time traveling stations. This means you can retry your journey between them as many times as you like. The faster you move between them, the further from danger you are.


Features:

- 3 extremely high speed stages
- Multiple variants of stages, depending on how quickly you reach them
- 5 different ending epilogues, based on your completion time

![Spider NPCs](../../assets/31985cf3c35c0bd6.jpg)


[Antorum](https://dooskington.com) is a multiplayer RPG where players build their characters
and fight against the growing threats on the isle.
The game server is authoritative and written in Rust,
while the client is written in Unity/C#.

This month, [@dooskington](https://twitter.com/dooskington) published a bunch of devlogs:

-
[Realm.One](https://github.com/Machine-Hum/realm.one)is a new open-source tile-based game written using the Amethyst game engine. It is the first game that will be integrated into[the distributed MMO platform Worlds](https://github.com/Machine-Hum/Worlds).Meet the first devlog:

[“Adventures with Rust - Game Development”](https://medium.com/@ryan.cjw/adventures-with-rust-game-development-1d998c45381c)[[/r/rust_gamedev](https://reddit.com/r/rust_gamedev/comments/eljx1s/adventures_with_rust_game_development)];![Realm.One screenshot](../../assets/43b44c84f1c4d163.png)

-
[Azriel](https://azriel.im)published an[“I Choose UI”](https://azriel.im/will/2020/01/31/i-choose-ui)devlog:- Character selection UI lists all available characters, with player selections highlighted.
- Map selection UI lists all available maps, with a selection highlight.

![Updated character selection UI that shows all chars](../../assets/e25abbf6b3c08841.png)

-
[@mvlabat shared a video](https://twitter.com/mvlabat/status/1219341273573863425)about the evolution of a fragment shader for a magic missile in[Grumpy Visitors](https://github.com/amethyst/grumpy_visitors); -
[“Wall Jump”](https://legendiguess.itch.io/wall-jump)by[@legendiguess](https://twitter.com/legendiguess)is a simple game for WeeklyGameJam.Nothing special, just a two minutes adventure of a Wall. Collect wall putty and return back to the house.

![Wall Jump gameplay sample](../../assets/deed038e831f17ed.gif)


## Library & Tooling Updates [#](https://gamedev.rs#library-tooling-updates)

### Rust 1.41: [Profile Overrides](https://doc.rust-lang.org/cargo/reference/profiles.html#overrides) are Stable Now! [#](https://gamedev.rs#rust-1-41-profile-overrides-are-stable-now)

![Rust 1.41](../../assets/5c3572fe4e09935f.png)


Though it wasn’t mentioned in [the official announcement post](https://blog.rust-lang.org/2020/01/30/Rust-1.41.0.html),
Rust 1.41 brings a cargo feature
that many gamedevs have been waiting a long time for:
[profile overrides](https://doc.rust-lang.org/cargo/reference/profiles.html#overrides).

This feature allows you to:

-
Use optimized deps in debug build to reduce incremental build time and get a sane FPS.

To override the settings for all dependencies (but not any workspace member), use the “*” package name:

`[profile.dev.package."*"] opt-level = 2`

-
Do not optimize build-dependencies (like

`syn`

) to increase full release build time:`[profile.release.build-override] opt-level = 0`


*Discussions:
/r/rust_gamedev,
/r/rust*

[@MontyPatrick](https://twitter.com/MontyPatrick) shared their initial experience of diving into Rust GameDev
in the [“Adventuring into the World of Games in Rust”](https://phoward.me/introduction/rust/game-development/2020/01/27/gamedev-rust.html) blog post.

Overall, while things are still relatively new in developing games in Rust I believe that Rust can serve as a great alternative to languages such as C++ in the field of game development.


![Rusty Q3 main menu](../../assets/a71a3292f9b603fb.jpeg)


[Immunant](https://immunant.com) published an article [“Translating Quake 3 into Rust”](https://immunant.com/blog/2020/01/quake3):

The Rust-loving team at

[Immunant]has been hard at work on[C2Rust], a migration framework that takes the drudgery out of migrating to Rust. Our goal is to make safety improvements to the translated Rust automatically where we can, and help the programmer do the same where we cannot. First, however, we have to build a rock-solid translator that gets people up and running in Rust. Testing on small CLI programs gets old eventually, so we decided to try translating Quake 3 into Rust. After a couple of days, we were likely the first people to ever play Quake3 in Rust!

Check out a
[video of transpiling Q3, loading the game and playing it](https://youtube.com/watch?v=lQjvSJLDXW4).

*Discussions:
/r/rust,
/r/programming,
Hacker News*

[A short blog post](https://ejmahler.github.io/rust_in_unreal) by @ejmahler about getting Rust code
integrated into Unreal Engine.

I’ve written a full writeup

[here], which includes a full demo project and all the necessary engine changes. You’ll need to be logged into GitHub with an account that has access to the Unreal Engine source code. If not, the link will look like a 404 – but it’s easy to[request access].As a quick summary of features I’ve found to work:


- Compiling a Rust crate as an Unreal Engine Module
- C++ Unreal modules linking to our Rust crate
- Automatic rebuilding C++ and binaries that depend on Rust code when that Rust code changes

*Discussions:
/r/rust*

![Rust OpenGL in 2 Kbytes](../../assets/cb27741ee306dc32.png)


Jani Peltonen has published an article [“Writing a 4K intro in Rust”](https://codeslow.com/2020/01/writing-4k-intro-in-rust.html):

For now I have a simple intro that initializes a modern OpenGL context in Win32 and puts up a relatively simple shader. The compressed size is <2Kbytes which, I think, validates Rust as viable language for writing 4K intros.


*Discussions:
/r/rust*

### 3D Graphics in Your Browser with Rust and WASM [#](https://gamedev.rs#3d-graphics-in-your-browser-with-rust-and-wasm)

![Slide with table of content](../../assets/30cd340b3832a40c.png)


Doug Milford released three tutorial videos:

[discord_game_sdk](https://github.com/ldesgoui/discord_game_sdk) in an *unofficial* safe interface to the [Discord Game SDK](https://discordapp.com/developers/docs/game-sdk/sdk-starter-guide).

The [Discord Game SDK](https://discordapp.com/developers/docs/game-sdk/sdk-starter-guide) provides features such as, but not limited to:

- Activities (Rich Presence)
- Users, Avatars and Relationships
- Lobbies, Matchmaking and Voice communication
- Faux-P2P Networking on Discord’s Infrastructure
- Cloud Synchronized Storage
- Store Transactions
- Achievements

[Optimath](https://github.com/djugei/optimath) by [@djugei](https://djugei.github.io)
is an experimental const generics based linear algebra library
that works without any allocations in no_std and utilizes SIMD.
*Requires nightly toolchain.*

Project goals:

Besides being hopefully useful as a library it is also an exploration of rusts newer advanced type system features. It is therefore an explicit goal to provide feedback to the developers of those features.

[The]contains some of that.`insights`

moduleIt is also meant to explore the design space of Linear Algebra libraries that utilize those features. As such it may serve as inspiration for how bigger linalg libraries might adopt them.


*Discussion:
/r/rust*

[keyframe](https://github.com/HannesMann/keyframe) is a simple library for animation.

Features:

- Several
[easing functions](https://easings.net/en), including user-defined Bézier curves and keyframable curves; - Animation sequences;
[mint](https://github.com/kvark/mint)integration for 2D/3D/4D support (points, rectangles, colors, etc)

Animation sequences example:

```
use keyframe::{keyframes, Keyframe, AnimationSequence};
fn example() {
// (value, time) or (value, time, function)
let mut sequence = keyframes![
(0.5, 0.0), // <-- EaseInOut used from 0.0 to 0.3
(1.5, 0.3, Linear), // <-- Linear used from 0.3 to 1.0
(2.5, 1.0) // <-- Easing function here is never used, since we're at the end
];
sequence.advance_by(0.65);
assert_eq!(sequence.now(), 2.0);
assert_eq!(sequence.duration(), 1.0);
}
```


![Ranged attack demo](../../assets/ad933598d8d9e38a.gif)


[The Roguelike Tutorial](http://bfnightly.bracketproductions.com/rustbook) continues to grow:
chapter [#70 “Missiles and Ranged Attacks”](http://bfnightly.bracketproductions.com/rustbook/chapter_70.html) was added to the book.
It adds targeting, ranged weaponry, AI that shoots back,
and projectile particles to the mix.

[rltk_rs](https://github.com/thebracket/rltk_rs) by [@blackfuture](https://patreon.com/blackfuture) is a Rust implementation of
[C++ Roguelike Toolkit](https://github.com/thebracket/rltk).

This month [rltk_rs v0.6](https://reddit.com/r/roguelikedev/comments/etiywv/sharing_saturday_295/ffi13dw/) was released. Some of the updates:

- Breaking changes: usize for indexing, cargo features rename, TryInto in generic functions, and a few more;
- “sticky” ctrl/alt/shift modifiers;
- more auto-derived traits;
- performance optimizations & bugfixes;
- updated examples.

[@bonsairobo](https://medium.com/@bonsairobo) published an article
[“Implementing a Turn-Based Game in an ECS with SPECS-Task”](https://medium.com/@bonsairobo/implementing-a-turn-based-game-in-an-entity-component-system-with-specs-task-d7f3358198b4):

I’ve heard from a few people who are just getting started with entity component systems (ECS) that implementing logic for a turn-based game seems more complicated than it should be. I thought that seemed odd, but I just recently ran into this problem myself. While certainly not insurmountable, implementing turn-based logic in an ECS just doesn’t feel great. I think the reason is that no one likes to implement a loop via distributed state machines.


[@flukejones](https://twitter.com/flukejones) forked an old Rust ECS benchmark set
and updated it to show some of the more recent ECS around:
[tiny_ecs](https://gitlab.com/flukejones/tiny_ecs), [hecs](https://github.com/Ralith/hecs), and [legion](https://github.com/jaynus/legion): [flukejones/ecs_bench](https://github.com/flukejones/ecs_bench).

[awesome-wgpu](https://github.com/rofrol/awesome-wgpu) is a new curated list of [wgpu](https://github.com/gfx-rs/wgpu-rs)-related links:
learning resources, games, app, articles, etc.

Also, check out a new `wgpu-rs`

-based ios app:

![Mao Brush logo](../../assets/db9d2a29125c953b.png)



[Mao Brush]realistically simulated the writing effect of Chinese brush + rice paper, the focus is on bringing the traditional Chinese calligraphy art to the digital age.The WebGPU-based (wgpu-rs) brush engine uses the LBM fluid simulation to achieve the unique expression of the brush. You can use it to experience the splash of Chinese calligraphy anytime, anywhere, and create brush calligraphy works.


[crow](https://crates.io/crates/crow) is a simple and efficient pixel based 2D graphics library.
It’s designed to be easy to use and should allow users
to do nearly everything they want
without requiring custom renderers or unsafe code.

[luminance](https://github.com/phaazon/luminance-rs) by [@phaazon](https://twitter.com/phaazon_) is a type-safe, type-level and stateless
graphics framework.

This month [luminance v0.38](https://github.com/phaazon/luminance-rs) got released.
Among the changes:

- The
`Mode::Patch`

tessellation primitive. - The pipelines can now be customized in deeper ways (besides clear color, one can enable or disable clearing color buffer, depth buffer, sRGB framebuffers, dynamic viewport, etc.).
- sRGB textures.
- Framebuffers now accept a Sampler to control how their associated textures will be sampled.
[A cool displacement mapping example](https://github.com/phaazon/luminance-rs/blob/master/docs/imgs/displacement_map.gif).

A complete changes list can be found [in the CHANGELOG](https://github.com/phaazon/luminance-rs/blob/master/luminance/CHANGELOG.md#038).

Also, the luminance book got updated: [check it out here](https://rust-tutorials.github.io/learn-luminance).

*Discussions:
/r/rust*

Btw, [@resinten](https://twitter.com/resinten) continues working on a luminance-based game:

- extra parallax layers,
- a basic UI with placeholder art,
- dialog system,
- updated player movement,
- music.

![Example walking an entry point of a SPIR-V file](../../assets/bc712af39403251b.png)

[SPIR-Q](https://github.com/PENGUINLIONG/spirq-rs) is a lightweight [SPIR-V](https://en.wikipedia.org/wiki/Standard_Portable_Intermediate_Representation) query library.
This month v0.2..v0.4.1 versions were released:

- SPIR-Q is now more handy with better and easier reflection information accessors;
- component number for shared-location interface variables;
- separable sampler types;
- descriptor access type query & multibinding for all descriptors;
- new examples, bugfixes, and significant performance improvements.

[glsl](https://crates.io/crates/glsl) is a crate to parse GLSL formatted sources into a typed AST.

[glsl-4.0 and glsl-quasiquote got released this month](https://reddit.com/r/rust/comments/eklo6l/official_announcement_glsl40).
Some of the updates:

- support for two backward-compatible keywords: attribute and varying (allows parsing GLSL450);
- binary operands are now parsed as left-associative.

*Discussions:
/r/rust*

This month [Oxygengine](https://github.com/PsichiX/Oxygengine) got
[JavaScript scripting interface](https://reddit.com/r/rust_gamedev/comments/epupkb/oxygengine_pure_js_scripting_backend_for_quick)
to allow faster prototyping of games.

This prebuilt WASM version would let game devs with JS background to quickly prototype game ideas and then slowly move their logic into Rust implementation, while learning Rust meantime.


Example source code: [oxygengine-js/js/index.js](https://github.com/PsichiX/Oxygengine/blob/master/oxygengine-js/js/index.js).

Also, you can now [instantiate entities from prefab assets](https://reddit.com/r/rust/comments/eunppk/oxygengine_instantiate_entities_from_prefab_assets).

[miniquad](https://github.com/not-fl3/miniquad) by [@fedor_games](https://twitter.com/fedor_games) is a safe cross-platform rendering library
focused on portability and low-end platforms support.

Some of this month’s updates:

[first crates.io version](http://crates.io/crates/miniquad);- native macOS support;

![MuOxi cog logo](../../assets/e5f8936ff3b4a0f5.png)


[MuOxi](https://github.com/duysqubix/MuOxi) is a modern library for creating [online multiplayer text games](https://en.wikipedia.org/wiki/MUD)
(MU* family) using the powerful features offered by Rust;
backed by Tokio and Diesel.

Current Status:

There is a working TCP server that allows for multiple connections and handles them accordingly. Effort is focused at the moment in designing the database architecture utilizing Diesel with PostgreSQL backend.


*Discussions:
/r/rust*

[Mun](https://mun-lang.org) is a scripting language for gamedev focused
on quick iteration times that is written in Rust.

[January updates](https://mun-lang.org/blog/2020/01/31/this-month-january) include:

[vscode plugin](https://marketplace.visualstudio.com/items?itemName=0x9ef.vscode-mun);- use extern functions in dispatch table;
- add marshalling of structs;
- add struct as marshallable field type;
- bugfixes and improved test coverage.

![NES games](../../assets/54a9e00eb43000c2.png)


[nestur](https://github.com/spieglt/nestur) is yet another NES emulator.
It’s mostly an educational project but it’s usable.

- SDL2 is the only dependency
- no use of unsafe
- NTSC timing
- supports mappers 0-4 which cover ~85% of games

*Discussions:
/r/rust*

## Popular Workgroup Issues in GitHub [#](https://gamedev.rs#popular-workgroup-issues-in-github)

## Meeting Minutes [#](https://gamedev.rs#meeting-minutes)

[See all meeting issues](https://github.com/rust-gamedev/wg/issues?q=label%3Ameeting) including full text notes
or [join the next meeting](https://github.com/rust-gamedev/wg#join-the-fun).

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs));[winit’s “Good first issue” and “help wanted” issues](https://github.com/rust-windowing/winit/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+label%3A%22status%3A+help+wanted%22+label%3A%22Good+first+issue%22);[gfx-rs’s “contributor-friendly” issues](https://github.com/gfx-rs/gfx/issues?q=is%3Aissue+is%3Aopen+label%3Acontributor-friendly);[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22);[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22);[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A);[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner);[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22);[A/B Street’s “good first issue” issues](https://github.com/dabreegster/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22);[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue);

## Bonus [#](https://gamedev.rs#bonus)

Just an interesting Rust gamedev link from the past. :)

[“A bot for Starcraft in Rust, C or any other language”](https://habr.com/post/436254)
is an article by Roman @humbug Proskuryakov
about writing a dynamic library for Windows that could be loaded
into [StarCraft](https://en.wikipedia.org/wiki/StarCraft:_Brood_War)’s address space to manage units.

*Discussions:
/r/rust,
Hacker News*

That’s all news for today, thanks for reading!

Subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!