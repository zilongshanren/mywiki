---
title: 'This Month in Rust GameDev #11 - June 2020'
url: https://gamedev.rs/news/011/
author: Rust GameDev WG
published: '2020-07-07'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the eleventh issue of the Rust GameDev Workgroup’s
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

[Legion Game Jam](https://gamedev.rs/news/011/#legion-game-jam)[Game Updates](https://gamedev.rs/news/011/#game-updates)[Learning Material Updates](https://gamedev.rs/news/011/#learning-material-updates)[Library & Tooling Updates](https://gamedev.rs/news/011/#library-tooling-updates)[Popular Workgroup Issues in GitHub](https://gamedev.rs/news/011/#popular-workgroup-issues-in-github)[Meeting Minutes](https://gamedev.rs/news/011/#meeting-minutes)[Requests for Contribution](https://gamedev.rs/news/011/#requests-for-contribution)[Bonus](https://gamedev.rs/news/011/#bonus)

The “Legion” game jam by [Laticoda](https://itch.io/profile/laticoda) is about
[the Roman Empire](https://wikipedia.org/wiki/Roman_Empire) for the background theme
and ECS paradigm for the technical side.
The conditions are:

- Open-source & Rust only.
- Projects should use some ECS library
(you can choose
[Legion](https://github.com/TomGillen/legion)if you don’t have one). - Team working and recycling old assets are allowed.

Submissions open to August 1st 2020.

It can be RPG, strategic, arcade or else; multi or solo. What you want. Just try to include a little bit of history and culture taste. Don’t be afraid, it is not ranked.


Also, participants are encouraged to
[document the development process at the event’s forum](https://itch.io/jam/legion-jam-rustlang/community).

## Game Updates [#](https://gamedev.rs#game-updates)



![Way of Rhea Trailer](../../assets/2940095c76adb376.jpeg)

[Way of Rhea](https://www.anthropicstudios.com/way-of-rhea) ([steam](https://store.steampowered.com/app/1110620/Way_of_Rhea))
is an upcoming puzzle platformer that takes place in a world
where you can only interact with objects that match your current color.
It’s being built in a custom engine, and custom scripting language both written
in Rust by [Mason Remaley](https://twitter.com/masonremaley). This month’s updates:

- A demo was released as part of the
[Steam Game Festival](https://store.steampowered.com/sale/gamefestival)! The festival has since ended, so the demo is no longer available. [@masonremaley](https://twitter.com/masonremaley)ran An AMA[at /r/rust_gamedev](https://reddit.com/r/rust_gamedev/comments/hc7vex/i_just_released_a_demo)and[/r/IndieDev](https://reddit.com/r/IndieDev/comments/hc7mf2/i_just_released_a_demo)about the development of the game.- The studio hosted a
[speedrun competition](https://steamcommunity.com/app/1110620/discussions/0/2569815696856844856)as part of the Steam festival,[here’s the winning run](https://youtu.be/AmYU0TXc4Ls). - A colorblind friendly mode was added to the game,
and
[a couple other changes](https://store.steampowered.com/newshub/app/1110620/view/2445966074565244552)were made in response to feedback from the festival.

Follow development updates on [the game’s Twitter](https://twitter.com/anthropicst)
or [subscribe to its newsletter](https://www.anthropicstudios.com/newsletter/signup/tech).

[A/B Street](https://abstreet.org) - Adjust Traffic Patterns in Real Cities [#](https://gamedev.rs#a-b-street-adjust-traffic-patterns-in-real-cities)

![Measuring the effects of changes](../../assets/3b872f5dd2684972.gif)

[A/B Street](https://abstreet.org) is a traffic simulation game exploring how
small changes to roads affect cyclists, transit users, pedestrians, and drivers.

June highlights:

- Alpha release with a
[trailer](https://www.youtube.com/watch?v=LxPD4n_1-LU), an excited reaction from[r/seattle](https://old.reddit.com/r/Seattle/comments/hdtucd/ab_street_think_you_can_fix_seattles_traffic/), and some[local press coverage](https://www.thestranger.com/slog/2020/06/29/43999454/ab-streets-game-lets-you-create-the-seattle-street-grid-of-your-dreams) - Support for parking lots, automatically inferring the number and position of individual slots from OpenStreetMap geometry
- Names of roads shown in-game, in a way that doesn’t cause clutter with agents moving nearby
- Work starting on light rail and restricting through-traffic to zones

A/B Street uses a [custom GUI library](https://github.com/dabreegster/abstreet/tree/master/ezgui/), leveraging `glium`

, `usvg`

, and
`lyon`

. Help with Rust and visual/game design is always welcome! Check out the
[roadmap](https://github.com/dabreegster/abstreet/blob/master/docs/roadmap.md) and [good first issues](https://github.com/dabreegster/abstreet/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22).



![In-game visual scripting prototype](../../assets/25a0be665a6cdc61.gif)

[Crate Before Attack](https://cratebeforeattack.com) by [koalefant (@CrateAttack)](https://twitter.com/CrateAttack)
is a skill-based grappling hook multiplayer game where frogs combat their friends
while navigating the landscape with their sticky tongues.

A summary of recent changes:

- Visuals: added two new artist-painted levels:
[Space](https://youtu.be/IOmD1LRJ6NA)and[Dinosaurs](https://youtu.be/UgIBNolI7Wo). - Gameplay:
[AI can now play all game modes](https://youtu.be/IUBZgusI7aI), added Quick Game option, - In-game
[visual scripting prototype](https://youtu.be/LLAc9_cOR9o). - Physics tweaks and
[improved terrain normal sampling](https://youtu.be/r5BAe03MRZo) - Multiplayer: added in-game chat, private matches with secret links, improved game setup UI. Numerous bugfixes and tweaks
[Playable Browser build](https://cratebeforeattack.com/play).

More details in [June Update DevLog-entry](https://cratebeforeattack.com/posts/20200630-june-update/)
and on [the YouTube channel](https://youtube.com/channel/UC_xMilPTLuuE5iLs1Ml9zow).

![screenshot: concrete & trees](../../assets/31073fb3ff1edef7.jpeg)


[Garden](https://epcc.itch.io/garden) is an upcoming game centered around growing realistic plants.
Some of the updates from [the June devlog](https://cyberplant.xyz/posts/june):

- Soil collision detection & changes to the soil column generation.
- Plant sim & terrain updates happen at different times & separately.
- Proper Global Illumination research.
- Automatic in-game texture reloading.

![Animation improvements](../../assets/5d99df13ee9ab99d.gif)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In June, Veloren did a big interview with GamingOnLinux, be sure to [check it
out](https://www.gamingonlinux.com/2020/06/interviewed-veloren-an-upcoming-foss-multiplayer-voxel-rpg)! Veloren’s lead artist also started a weekly blog
about his work on Veloren, which you can see [here](https://www.patreon.com/posts/weekly-blog-no-1-37819335). Veloren recently
reached the [first page](https://gitlab.com/explore/projects/starred) of most starred projects on Gitlab! The
[Veloren Youtube channel](https://www.youtube.com/channel/UCmRjlnKnSRRihWPPNasl_Qw) also reached 1000
subscribers.

A lot has been done over the last month towards 0.7, which is slated to release at the beginning of August. Lots of work has been done improving UI and animations. These will help towards the goal of 0.7 being the “progression” update. Many improvements have been made to the continuous integration system to make it more reliable and faster. Mac support was added to Airshipper, the Veloren launcher. Significant work was done on the world simulation front. This includes economic simulations that will represent trade and resource pricing in settlements and cities. Castle generation is also now in the works.

![Work on castle generation](../../assets/2e308ed3696c7577.jpeg)


Test coverage and documentation has started to improve, and a workflow around it
is being developed. The project is now hosting a [proper documentation
site](https://docs.veloren.net/veloren_voxygen/index.html) that is updated with each merge. A #ux working group was
created to facilitate discussions on improvements to player interactions in
Veloren. Lots of translations were merged, including Swedish, Polish, and
Brazilian Portugese. The skill system is moving on to implementation, being a
coordinated effort between the game design, art, and combat working groups.

You can read more about some specific topics from June:

[Mod Analysis](https://veloren.net/devblog-70#mod-analysis-by-bottledbyte)[Improving CI](https://veloren.net/devblog-70#improving-ci-by-xmac94x)[Economic Research](https://veloren.net/devblog-72#economic-research-by-zesterer)[Compilation Improvements](https://veloren.net/devblog-72#compilation-improvements-by-xmac94x)[Improving Test Coverage](https://veloren.net/devblog-73#improving-test-coverage-by-angelonfira)[Skill System Work](https://veloren.net/devblog-74#skill-system-work-by-xvar)[Animation updates](https://veloren.net/devblog-74#animation-updates)

June’s full weekly devlogs: “This Week In Veloren…”:
[#70](https://veloren.net/devblog-70),
[#71](https://veloren.net/devblog-71),
[#72](https://veloren.net/devblog-72),
[#73](https://veloren.net/devblog-73),
[#74](https://veloren.net/devblog-74).

In July, work will be done to complete the progression systems. There will be financial meetings held to discuss how funds from the project’s Open Collective will be distributed.

Also, check out [a talk about open source and Veloren](https://youtube.com/watch?v=aS26sqT09Pw):

![ships with greater thrust explode](../../assets/ea11f4f3d57b54c6.gif)

[Zero to Game](https://zerotoga.me) is a project that documents
the creation of an independent space game from zero.

My plan for this website is to narrate my independent development of a computer game in the Rust programming language. I’ve never done this before, and so I hope to be able to show you the progression right from zero all the way up to a game.


- Zero game programming experience.
- Zero experience in the Rust programming language.
- Zero experience making assets, images, sounds, models, etcetera.

Currently published posts:

[#1 “Finding Zero”](https://zerotoga.me/dev/findingzero)- where the game development journey is beginning.[#2 “Inspiring Design”](https://zerotoga.me/dev/inspiringdesign)- how Factorio, Screeps, and Space Station 13 are inspiring the game’s design.[#3 “Picking Technology”](https://zerotoga.me/dev/pickingtechnology)- researching a technology path for the game project to start out on.[#4 “Leading Design Challenges”](https://zerotoga.me/dev/leadingdesignchallenges)- the spacetime issues with combining gameplay inside and outside of spaceships.[#5 “Fast Spaceship Physics”](https://zerotoga.me/dev/fastspaceshipphysics)- prototyping a spaceship physics simulation aimed at speed.[#6 “Physical Destruction”](https://zerotoga.me/dev/physicaldestruction)- the structure and implementation of a spaceship destruction prototype.[#7 “Rendering in Rust”](https://zerotoga.me/dev/renderinginrust)- working through from tutorial code to meet the needs of the game’s first Rust scene render.

![Screenshot of the Pont board game](../../assets/951cd467222de536.png)


Pont is a multiplayer online board game based on
[Qwirkle](https://en.wikipedia.org/wiki/Qwirkle), implemented by [Matt Keeter](https://twitter.com/impraxical).
Both the client and server are written in Rust,
using WebAssembly to run the client in the browser
without any Javascript (besides a small shim).

It can be played online [here](https://pont.mattkeeter.com)!

The system architecture is described in a [blog post](https://mattkeeter.com/projects/pont)
and the source is available [on GitHub](https://github.com/mkeeter/pont)

*Discussions:
/r/rust,
Hacker News*

![Scale screenshot](../../assets/81b81ac4b0023a9f.png)


[Scale](https://github.com/Uriopass/Scale)’s objective is to become a granular society simulation,
filled with fully autonomous agents interacting with their world in real time.

The 4th [devlog](http://douady.paris/blog/scale_4.html) was published, talking about
the new renderer based on [wgpu-rs](https://github.com/gfx-rs/wgpu-rs), pathfinding, parking,
curved roads and a new crate extracted from the project called [flat_spatial](https://crates.io/crates/flat_spatial).

*Discussions:
/r/rust_gamedev*

[runner](https://github.com/jayrave/runner) is a simple side-scrolling endless runner game that takes place in
a bright world that only has our fearless adventurer & a few pesky beings
that are bent on keeping her from running! It uses [specs](https://github.com/amethyst/specs) for [ECS](https://en.wikipedia.org/wiki/Entity_component_system)
and has multiple frontends: [sdl2](https://github.com/Rust-SDL2/rust-sdl2) & [quicksilver](https://github.com/ryanisaacg/quicksilver).
Between the two frontends it can target the majority of the platforms:
Web, Mac, Linux, Windows (untested) & possible even iOS & Android.

![Part of the game map](../../assets/5c88ca05fef38eb4.jpeg)

[Animal Fight Chess](https://github.com/netcan/AnimalChess) (斗兽棋, “Doe Show Chee”) by [@netcan](https://github.com/netcan)
is a Rust implementation of a popular Chinese game.

To win the game, one player must successfully move any animal into
the Den(兽穴) of the opponent or eat all animals of the opponent.
The basic move is just one space either forward, backward, left, or right.
The pieces never move diagonally.
Each player has eight pieces,
[different animals with different degrees of power](http://ancientchess.com/graphics-rules/dou_shou_qi_jungle_game-pieces-values.jpg),
a larger power piece can eat a little power piece, but rat can eat elephant.
Here’s a picture of the pieces, their English names,
and relative powers indicated by a number.
See full rules at [ancientchess.com](http://ancientchess.com/page/play-doushouqi.htm)
or [Wikipedia](https://en.wikipedia.org/wiki/Jungle_(board_game)).

The project uses alpha beta pruning algorithm for AI and provides a python module to use AlphaZero algorithm for training.

![screenshot: planets and words](../../assets/84b277ce066edbf8.png)


[rs-type](https://github.com/akiross/rs-type) is a WIP typing game
inspired by [zty.pe](https://zty.pe/).
It can load [KTouch courses](https://github.com/KDE/ktouch/tree/master/data/courses)
and also has a built-in basic vector drawing tool for painting backgrounds.

![gif](../../assets/59deac311d026352.gif)


[Guacamole Runner](https://github.com/EllenNyan/guacamole-runner) is a small game made with
[Tetra](https://github.com/17cupsofcoffee/Tetra) and [Shipyard](https://github.com/leudz/shipyard) in approximately 2 days
by [@EllenNyan](https://twitter.com/EllenNyan0214).
The game’s concept is that the player is constantly falling
and must jump off planes to stay in the air.
When they go over the top of the dirt tiles
they plant flowers which gives them points.

![Video of snaky keyboard lights in action](../../assets/c75e21ed90b96333.gif)


[Wooting Snake](https://github.com/TanTanDev/wooting_snake) is a snake game where the visuals
are represented on your keyboard lights, instead of a computer screen.

[TanTan](https://twitter.com/Tantan22430802) released a [video](https://youtu.be/OhhscXz-60g)
documenting the process of making this project.

![terrain, bg trees, and a character](../../assets/df8f59e3fc447e91.jpeg)


[Anthony Brigante](https://abrigante.com/) started working on a 2D sandbox game.
Two devlogs were released this month:



![Weegames](../../assets/1d5d24dbd68be240.jpg)

[a demo video](https://youtube.com/watch?v=A_GqhZ_7EIw)

[Weegames](https://yeahross.itch.io/weegames) is a fast-paced minigame collection.
There are 23 odd games all made using free images and sounds.
The more minigames you beat the faster they get.

![Fluid demo](../../assets/994ef90c6d5dde65.gif)


[blub](https://github.com/wumpf/blub) is a WIP 3D fluid simulation playground build with wgpu-rs and imgui-rs.
It focuses primarily on hybrid approaches lagrangian/eularian approaches
(PIC/FLIP/APIC..). Check the project’s README for more details.

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

This month, [Tyler Zhang gave a talk](https://youtube.com/watch?v=_22oxXEX_xc?t=709) at
London Virtual Talks about the theory and implementation
of 4D physics visualization.
The demo’s source code [could be found here](https://github.com/t-veor/hypervis).



![Boids demo](../../assets/a4eee8651ff042af.jpeg)

[the video demo](https://drive.google.com/file/d/1ri4x-jCX8SA9oX8OqDIKtXhYIrEKlGjO/view)

[@twitu](https://github.com/twitu) has published a three-part blog series
about simulating a group of virtual agents (boids)
that will swim around an enclosed space behaving like a school of fish.

This is a beautiful application of procedural graphics generation, where simple rules create complex patterns. It’s almost entirely inspired by Sebastian Lague’s

[Coding Adventure with boids].

[A fistful of boids](https://blog.bitsacm.in/a-fistful-of-boids)- Setting up the scene and basic animation[For a few boids more](https://blog.bitsacm.in/for-a-few-boids-more)- Generating boids and obstacle avoidance[The school, the boid and the Rusty](https://blog.bitsacm.in/the-school-the-boid-and-the-rusty)- Simulating a flock, parallelism and benchmarking performance

*Discussions:
/r/rust*

![The fire effect itself](../../assets/1b654cfd4f6e045d.gif)


[doomfire](https://github.com/r-marques/doomfire) by [@r-marques](https://github.com/r-marques) is Rust implementations of the DOOM fire effect
(based on [Fabien Sanglard’s blog post](https://fabiensanglard.net/doom_fire_psx))
using different 2d graphics libraries:
[minifb](https://github.com/emoon/rust_minifb),
[pixels](https://github.com/parasyte/pixels),
[sdl2](https://github.com/Rust-SDL2/rust-sdl2),
[wasm-bindgen](https://github.com/rustwasm/wasm-bindgen)
+ [Canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API).

This could be helpful for someone new to rust and trying to get into game development and looking for the right libraries to use.


*Discussions:
/r/rust*

## Library & Tooling Updates [#](https://gamedev.rs#library-tooling-updates)

![demo-gif](../../assets/6e6213dfcc51dfd8.gif)


Just what everyone’s always wanted, [Rust on the Sony PSP](https://github.com/overdrivenpotato/rust-psp)! 😆

This project is a port and improvement of the unofficial C/C++ PSPSDK from 2005 It does not require a custom GCC toolchain to be installed. Only Rust nightly and a cargo subcommand.

The psp crate provides a `psp::sys`

submodule that houses the entire Sony PSP
API. The authors are working to have these interfaces merged into the libc crate.
The PSP, unfortunately, uses non-standard dynamic linking,
(and some libraries are statically linked!), so function definitions
marked extern are not enough. Eventually, this sys lib will be wrapped with a more
rust-friendly library.

Rather than patching LLVM or rustc, the rust-psp team has also merged a
`mipsel-sony-psp`

target upstream, and published cargo-psp. This is a subcommand
that works exactly like cargo build, except it also builds the crate into a
PSP-specific executable format called `PRX`

and packages that into an
`EBOOT.PBP`

, the standard format for a PSP Homebrew.

The crate has reached full user-mode parity with the unofficial C/C++ SDK.
Kernel-mode support still needs to be worked on. Aside from library
imports, there is also support for PSP-specific custom assembly instructions
via the `vfpu_asm!`

macro, with no need for a custom compiler toolchain.
There is also optional `embedded-graphics`

support and a function to benchmark
or time your code.

The next major milestone for rust-psp is std support.
If you are interested in helping out, please feel free to join the rust-psp
channel in the [PSP Homebrew discord server](https://discord.gg/WY8XhDG).

[glam](https://github.com/bitshifter/glam-rs) is a simple and fast linear algebra crate for games and graphics.

This month [glam 0.9](https://github.com/bitshifter/glam-rs/blob/master/CHANGELOG.md#090---2020-06-28) was published to crates.io. This update is a breaking
change from 0.8.

In 0.9 the `Vec3`

type was changed from being a 128 byte SIMD vector type to a
tuple of three floats. This changes the size of `Vec3`

from 16 bytes to 12 bytes
and the alignment from 16 bytes to 4 bytes. This might not affect all users but
if `Vec3`

was used in a context where the size or alignment mattered, such as in
FFI or as input to shaders, this could cause breakage.

The SIMD parts of `Vec3`

were moved to a new type, `Vec3A`

(`A`

for Aligned)
which is 16 byte aligned and thus 16 bytes in size. The `Vec3A`

type is still
there for users who want the performance benefits of the SIMD implementation.

The motivation for this change was that it is potentially surprising and
confusing for new users that the `Vec3`

type was not 12 bytes. Also, it’s common
that users needed a `Vec3`

that was just 12 bytes.

While glam is reasonably stable it has not yet reached a 1.0 release so it seemed like now is the time to address such issues in the API.

![Language Server Diagnostics in action](../../assets/f7504950cb0d09b5.gif)

[Mun](https://mun-lang.org) is a scripting language for gamedev focused on quick iteration times
that is written in Rust.

After the dust of the [Mun v0.2 release](https://mun-lang.org/blog/2020/05/16/release-mun-v0-2-0) settled, this month’s focus
has been on fixing several issues found by community members, improving the
overall quality of the code base and working towards the next release: Mun v0.3.

Their [June updates](https://mun-lang.org/blog/2020/06/30/this-month-june) include:

;*Make It or Break It*contest- several fixes for issues that arose thanks to the contest;
- the foundation for Mun projects;
- an initial language server setup;

![logo](../../assets/f76fec2ee703438a.png)


[GameLisp](https://gamelisp.rs/) (glisp) is a scripting language built for and in Rust and utilizes
syntax from the LISP family of programming languages. It provides a fast and
efficient garbage collector that runs every frame instead of freezing a thread.

GameLisp also provides [a playground](https://gamelisp.rs/playground/) to experiment with
different projects. A reference guide is also [available](https://gamelisp.rs/reference/) as
well as [API documentation](https://docs.rs/glsp/0.1.0/glsp/) for integration into Rust.

The crate has had its [initial release](https://crates.io/crates/glsp/), a roadmap and ways
to contribute are available on GameLisp’s [GitHub Respository](https://github.com/fleabitdev/glsp/).

[safe_arch](https://github.com/Lokathor/safe_arch) is a crate by [@lokathor](https://twitter.com/lokathor) that safely exposes
CPU arch intrinsics via `#[cfg()]`

.
This month v0.4 and v0.5 versions were released.
The main improvements are:

- 256 bit supports
- Almost all the API was reworked for better naming consistency

[yaks](https://crates.io/crates/yaks) is a minimalistic framework for automatic multithreading
of [ hecs](https://crates.io/crates/hecs) ECS library using

[Rayon](https://crates.io/crates/rayon)data-parallelism library.

While the project itself started earlier this year, with this month’s release
`yaks`

gained an overhauled API, further leaning into the promise of
simplicity:

- systems are any functions or closures of a specific signature,
`Executor`

is a container for one or more systems,- system execution order can be defined when building an
`Executor`

to create concurrent chains of systems, - resources used by systems (any data that is not associated with an entity) are now borrowed for the duration of execution, instead of being owned by the framework.

All items in the library are exhaustively documented, and the repository contains a fully annotated example.

Enabled-by-default `parallel`

cargo feature can be disabled to force
everything in `yaks`

to become single-threaded, which allows using code
written with the framework on platforms without threading - notably, web.

[macroquad](https://github.com/not-fl3/macroquad) by [@fedor_games](https://twitter.com/fedor_games) is cross-platform
(Windows/Linux/macOS/Android/WASM) game framework
build on top of [miniquad](https://github.com/not-fl3/miniquad).

The project now has [a Discord community server](https://discord.gg/WfEp6ut)
([Matrix bridge](https://matrix.to/#/#quad-general:matrix.org))
with channels for all the quad-family projects:
miniquad, macroquad, good-web-game, and nanoserde.

Also, two new examples came from the awesome macroquad community:

-
“snake” - try it

[in the browser](https://not-fl3.github.io/miniquad-samples/snake.html)([source](https://github.com/not-fl3/macroquad/blob/master/examples/snake.rs)) -
“asteroids” - try it

[in the browser](https://not-fl3.github.io/miniquad-samples/asteroids.html)([source](https://github.com/not-fl3/macroquad/blob/master/examples/asteroids.rs))

megaui is macroquad’s imgui-like UI system.
Recently, megaui got decent input widgets: input fields, editboxes, and sliders.
All of them support copy-pasting back and forth from the browser.
Check out [the web demo](https://not-fl3.github.io/miniquad-samples/ui.html)
([source](https://github.com/not-fl3/macroquad/blob/master/examples/ui.rs)):

![ui](../../assets/2d139360b1da0bb8.gif)


[nanoserde](https://github.com/not-fl3/nanoserde/) by [@fedor_games](https://twitter.com/fedor_games) is a fork of makepad-tinyserde
with syn/quote/proc_macro2 dependencies removed.
It attempts to solve a serde’s problems of long clean compilation time,
increased incremental build time, and build artifacts size.
nanoserde may be useful when the whole game has less than a minute
clean build time and spending ~40s on serde is unreasonable.

```
> cargo tree
nanoserde v0.1.0 (/../nanoserde)
└── nanoserde-derive v0.1.0 (/../nanoserde/derive)
```


Some benchmarks and tiled map deserializing example
[could be found here](https://github.com/not-fl3/nanoserde-bench).

[Tetra](https://github.com/17cupsofcoffee/Tetra) is a simple 2D game framework, inspired by XNA and Raylib. This month,
[version 0.4](https://twitter.com/17cupsofcoffee/status/1275778769077317637) was released, featuring:

- A rework of the text rendering API, which improves performance and fixes a number of long-standing bugs
- Functions for capturing the player’s mouse
- Various tweaks and bug fixes under the hood

Also, [a new guide has been added to Tetra’s website](https://tetra.seventeencups.net/distributing/), listing some
things to consider when distributing your game to the public. This guide is
still a work in progress, so contributions are welcomed!

Project “NodeFX” by [Christian Vallentin (@MrVallentin)](https://twitter.com/MrVallentin)
is an unnamed node-based tool for creating GLSL shaders in real-time,
entirely written in Rust.

This month added support for both 2D and 3D SDF nodes. The above screenshot is
a meta example of creating a node using some of the 2D SDF primitives and
operations.
[An example of some 3D SDFs can be found on Twitter.](https://twitter.com/MrVallentin/status/1276961197645008896)

Next month is all about adding more UI, to make the application more
user-friendly and fully-fledged. After UI has been added, there is a planned
release of the application.
More information can be found on [Twitter](https://twitter.com/MrVallentin).

![Chumtoad](../../assets/84fb52a7f1ade519.jpg)


[Göld](https://github.com/Vurich/goeld) is a WIP game engine for hacking together 3D games using old tech.
It uses wgpu-rs and is based on the simple mental model of PyGame or Löve,
but for Goldsrc/Quake-era tech.

The ultimate goal of the project is to have a simple engine that can do basically everything that many simplistic 3D games will need, without making an attempt at being too general.

Current features:

- Quake 2 maps loading (although not Quake/Goldsrc maps yet) and rendering with proper BSP culling and frustum culling.
- Loading and rendering of HL1 models.
- Simple dynamic lighting system.

*Discussions:
/r/rust_gamedev*

[Arsenal](https://github.com/katharostech/arsenal) is the concept for a 2D and 3D game engine that is fully integrated
with [Blender](https://blender.org) and built on a Rust core. The engine will be built around an
entity component system ( probably [Shipyard](https://github.com/leudz/shipyard) ) for its performance and game
design advantages. The vision of Arsenal is to build an Open Source game engine
that is suitable for games of any scale and that is easily approachable by a
wide audience of both complete beginners and seasoned experts.

Arsenal currently has a [POC](https://github.com/katharostech/arsenal/releases/tag/v0.1.0) working, but there is no support for
adding custom game logic. The next major step for Arsenal is to get initial
[scripting support](https://github.com/leudz/shipyard/issues/96) in Shipyard. The scripting plan for
Arsenal borrows heavily from the [Amethyst scripting RFC](https://github.com/amethyst/rfcs/blob/master/0001-scripting.md)
with the first target scripting language being Python. Other languages that are
candidates for being added later are be [Mun](https://mun-lang.org), Lua, and maybe other languages
written in Rust such as [Gluon](https://github.com/gluon-lang/gluon).

More information on the Arsenal development direction can be found in the latest
Arsenal development [blog post](https://katharostech.com/post/arsenal-development-now-on-github-sponsors).

[Katharos Technology](https://katharostech.com) has gone live on [GitHub Sponsors](https://github.com/sponsors/katharostech/) as a
means to fund development of the development of the [Arsenal](https://github.com/katharostech/arsenal) game engine and
supporting Rust gamedev libraries and tools such as [GFX](https://github.com/gfx-rs/gfx), and [WGPU](https://github.com/gfx-rs/wgpu).

![Demo of transforming Ferris](../../assets/b57a6a7d10c11713.gif)


[Vimnail](https://github.com/TanTanDev/vimnail) is a WIP mode-based image editor inspired by Vim.
The goal of the project is to be able to compose images without using the mouse.

[TanTan](https://twitter.com/Tantan22430802) also released a [devlog video](https://youtu.be/2cSY43OcuZc) about the project.

This month [Garett Cooper](https://garettcooper.com/) released [GC NES Emulator](https://garettcooper.com/#/nes-emulator)
that allows you to play classic Nintendo Entertainment System games in the browser.

The core of the GC NES Emulator is implemented in the Rust programming language, which supports Web Assembly as a compilation target. With a WASM version of the emulator, I’ve written a javascript wrapper that takes the frame rendered with the Rust code and displays it on an HTML 5 canvas. At present, this is done completely synchronously, though I would like to move it into a worker at some point in the future


## Popular Workgroup Issues in GitHub [#](https://gamedev.rs#popular-workgroup-issues-in-github)

## Meeting Minutes [#](https://gamedev.rs#meeting-minutes)

[See all meeting issues](https://github.com/rust-gamedev/wg/issues?q=label%3Ameeting) including full text notes
or [join the next meeting](https://github.com/rust-gamedev/wg#join-the-fun).

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[gl-rs is seeking new maintainers](https://github.com/brendanzab/gl-rs/issues/524);[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs));[winit’s “Good first issue” and “help wanted” issues](https://github.com/rust-windowing/winit/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+label%3A%22status%3A+help+wanted%22+label%3A%22Good+first+issue%22);[gfx-rs’s “contributor-friendly” issues](https://github.com/gfx-rs/gfx/issues?q=is%3Aissue+is%3Aopen+label%3Acontributor-friendly);[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22);[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22);[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A);[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner);[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22);[A/B Street’s “good first issue” issues](https://github.com/dabreegster/abstreet/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22);[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue);

## Bonus [#](https://gamedev.rs#bonus)

Just an interesting Rust gamedev link from the past. :)

During RustConf 2018, Catherine West gave a keynote talk
“Using Rust For Game Development” that introduced a lot of people
to the concept of ECS and is now considered a classic.
You can [watch the recording here](https://youtube.com/watch?v=aKLntZcp27M) ([slides](https://kyren.github.io/rustconf_2018_slides/index.html)).

A few months later [an extended text version was released](https://kyren.github.io/2018/09/14/rustconf-talk.html).

*Discussions:
/r/rust,
/r/programming*

That’s all news for today, thanks for reading!

Subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!