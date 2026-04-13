---
title: 'This Month in Rust GameDev #16 - November 2020'
url: https://gamedev.rs/news/016/
author: Rust GameDev WG
published: '2020-12-08'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 16th issue of the Rust GameDev Workgroup’s
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

[Rust GameDev Podcast #3](https://gamedev.rs/news/016/#rust-gamedev-podcast-3)[Last Call for Rust GameDev Survey](https://gamedev.rs/news/016/#last-call-for-rust-gamedev-survey)[Game Updates](https://gamedev.rs/news/016/#game-updates)[Learning Material Updates](https://gamedev.rs/news/016/#learning-material-updates)[Library & Tooling Updates](https://gamedev.rs/news/016/#library-tooling-updates)[Popular Workgroup Issues in GitHub](https://gamedev.rs/news/016/#popular-workgroup-issues-in-github)[Requests for Contribution](https://gamedev.rs/news/016/#requests-for-contribution)

![text logo](../../assets/c37fa0271f9fbf0b.jpeg)


[The third episode](https://rustgamedev.com/episodes/interview-with-chris-parsons) is an interview with [Chris Parsons](https://chrismdp.com) about
procedural history generation, custom game engines, the business
of indie games development and lessons learned from shipping his first title,
[Sol Trader](http://soltrader.net).

Listen and Subscribe from the following platforms:
[Rust GameDev Podcast (simplecast)](https://rustgamedev.com/),
[Apple Podcasts](https://podcasts.apple.com/gb/podcast/rust-game-dev/id1526304768),
[Spotify](https://open.spotify.com/show/7HRfGnTcXkLkQd9fxJbDGj),
[RSS Feed](https://feeds.simplecast.com/C6NQglnL),
[Google Podcasts](https://podcasts.google.com/feed/aHR0cHM6Ly9mZWVkcy5zaW1wbGVjYXN0LmNvbS9DNk5RZ2xuTA).

## Last Call for [Rust GameDev Survey](https://surveymonkey.com/r/F2JYRFF) [#](https://gamedev.rs#last-call-for-rust-gamedev-survey)

Our annual [Rust Game Development Ecosystem Survey](https://surveymonkey.com/r/F2JYRFF) will be closed
at the end of this week, 11. December 2020.
It’ll only take 10 minutes, and your responses help us
better understand the state of our ecosystem and where we
should try to focus our collective efforts.

## Game Updates [#](https://gamedev.rs#game-updates)

![15 minute tool](../../assets/9112255686b46470.png)


[A/B Street](https://abstreet.org) is a traffic simulation game exploring how small changes
to roads affect cyclists, transit users, pedestrians, and drivers. Any city
with OpenStreetMap coverage can be used!

Some of this month’s updates:

- A new tool to explore 15-minute neighborhoods was started.
- Simpler process for
[importing new cities](https://dabreegster.github.io/abstreet/howto/new_city.html). - Large internal refactoring for the GUI and initializing the simulation.

![Landscape](../../assets/7bcf7c367cfcec0b.jpg)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In November, Veloren released 0.8! This is the largest version yet, with over
50k lines of code added. GamingOnLinux wrote [an
article](https://www.gamingonlinux.com/2020/11/inspired-by-the-likes-of-cube-world-open-source-rpg-veloren-has-the-biggest-update-yet) about the release. You can see the [full
changelog here](https://gitlab.com/veloren/veloren/-/blob/master/CHANGELOG.md#080-2020-11-28). Veloren also spoke at MiniDebConf #2,
you can watch [the recording here](https://www.youtube.com/watch?v=76FPpOnshNw). In November, many
improvements were made to the UI, with map and buff updates. During the 0.8 code
freeze, many networking and combat bugs were fixed. The Veloren 0.8 release
party took place on the 28th and saw a peak of 112 players online, doubling the
previous record.



![Youtube preview img](../../assets/78fa5f663cba2055.gif)

You can read more about specific topics from November:

[First Time Contributing](https://veloren.net/devblog-92#first-time-contributing-by-ubruntu)[Community Spotlight](https://veloren.net/devblog-92#community-spotlight-kalculate)[Performance Analysis](https://veloren.net/devblog-93#performance-analysis-with-xmac94x)[0.8 Release Schedule](https://veloren.net/devblog-94#0-8-release-schedule)[Veloren Trailer Competition](https://veloren.net/devblog-94#veloren-screenshot-trailer-competition)[Chest of Goodies](https://veloren.net/devblog-94#chest-of-goodies-by-zesterer)[Iced Transition](https://veloren.net/devblog-94#iced-transition-by-imbris)[Particle Improvements](https://veloren.net/devblog-95#particle-improvements-by-timo)[Animal Attacks and AI](https://veloren.net/devblog-95#animal-attacks-and-ai-by-slipped-and-james)[Veloren 0.8 Launch](https://veloren.net/devblog-96#veloren-0-8-launch)[What People Are Saying About The Launch](https://veloren.net/devblog-96#what-people-are-saying-about-the-launch)[Idea Drop](https://veloren.net/devblog-96#idea-drop-by-u-o11c)

November’s full weekly devlogs: “This Week In Veloren…”:
[#92](https://veloren.net/devblog-92/),
[#93](https://veloren.net/devblog-93/),
[#94](https://veloren.net/devblog-94/),
[#95](https://veloren.net/devblog-95/),
[#96](https://veloren.net/devblog-96/).

In December, work will begin on 0.9. There are some discussions about larger refactors in the codebase. Many new developers have joined and are getting up to speed on contributing. Veloren will also reach its 100th blog post!

![Healing sceptre](../../assets/f247872f8d437fa5.jpg)

![FBSim initial version](../../assets/cde0d4154905d801.png)

[FBSim](https://github.com/IanTayler/fbsim) by [Ian Tayler](https://iantayler.com) is a football/soccer game where you program the
players using Rust and try to beat a team controlled by another AI.

You can follow the [tutorial](https://iantayler.com/2020/11/22/fbsim-football-playing-ai-agents-in-rust/) for implementing your own simple AI for FBSim,
or you can look at the code directly, which can be found on the
[github repo](https://github.com/IanTayler/fbsim). FBSim is at an early stage of development so issues and
comments are welcome!

*Discussions:
/r/rust_gamedev*

![Two players fishing at the beach](../../assets/9506e7ca792d1748.gif)


[Antorum Online](https://ratwizard.dev/antorum) is a micro-multiplayer online role-playing game by [@dooskington](https://twitter.com/dooskington).
The game server is written in Rust, and the official client is being developed in
Unity.

Many important changes and new features were implemented this month. Players can now harvest plants and go fishing! There were also some tweaks to the world engine to support named zones on the map.

![Akiki butcher](../../assets/eaa4ac197aadb80d.jpg)

[Akigi](https://akigi.com) is a WIP online multiplayer game.

In November, focus was put on gameplay. Prototyping of a butcher skill was done, which will allow for animals to be turned into raw resources. Support for rendering shadows in the MetalRenderer was added, bringing it one step closer to the WebGlRenderer. Lots of work was put into the ability to fire a bow. This spanned a few weeks, however enough functionality was added for it to feel like a solid part of gameplay. It still requires some polish, however, which will be the focus of the beginning of December.

Full devlogs:
[#091](https://devjournal.akigi.com/november-2020/091-2020-11-01.html),
[#092](https://devjournal.akigi.com/november-2020/092-2020-11-08.html),
[#093](https://devjournal.akigi.com/november-2020/093-2020-11-15.html),
[#094](https://devjournal.akigi.com/november-2020/094-2020-11-22.html),
[#095](https://devjournal.akigi.com/november-2020/095-2020-11-29.html).

![rymd animated combat v2](../../assets/1c7075e33e511d81.gif)


[rymd](https://profan.itch.io/rymd) by [@_profan](https://twitter.com/_profan) is a space shooter prototype made with [macroquad](https://github.com/not-fl3/macroquad).

Intended as a test platform for trying out rust for prototyping games and particularly for game AI programming purposes.

Recent updates include:

- Dynamic ship debris based on slicing source sprites into chunks.
- New hostile ship type, (ranger), which fires seeking missiles.
- New support ship type, (tech), which repairs friendly ships.
- Toggleable hitbox visualization.
- Still far too many particles.

![Shotcaller dual frontend](../../assets/63379845df8395d2.png)

[Shotcaller](https://github.com/amethyst/shotcaller) is a moddable RTS/MOBA game made with bracket-lib and specs.

This month [v0.3.1](https://github.com/amethyst/shotcaller/releases/tag/0.3.1) version was released.
Some of the updates:

- Kenney’s micro-roguelike tileset was added.
- Leaders now have an item inventory.
- A handling system of stats effectors for items.
- New tutorials about creating leaders and items.
- A
[fully functional web version](https://shotcaller.jojolepro.com/), including tileset.

Contributions welcome: [try add a new Leader](https://github.com/amethyst/shotcaller/issues/6).

![space_shooter_rs gameplay](../../assets/5ea8ccf3d02b5689.gif)


The [Space Shooter](https://github.com/amethyst/space_shooter_rs) project is a game in development by [Carlo Supina](https://twitter.com/carlosupina) and
[Micah Tigley](https://twitter.com/micah_tigley). It is a 2D “shoot-em-up” game that takes place in space and is
inspired by games like [Raiden](https://wikipedia.org/wiki/Raiden_(video_game)) and [Binding of Isaac](https://wikipedia.org/wiki/The_Binding_of_Isaac_(video_game)).

Exciting new additions have been made in November!

- Micah added a
[“paused” text overlay](https://snipboard.io/ql60oz.jpg)to provide a visual indication for when the game is paused. - Carlo added a
[new armor system](https://twitter.com/carlosupina/status/1331680041453953025)that gives a chance for destroyed enemies to drop armor consumables that can block a single hit from any damage source. - Work on a new
[Missile Launcher enemy](https://github.com/amethyst/space_shooter_rs/pull/93)has begun!

![game off logo](../../assets/79565235d486b817.png)


[Game Off](https://itch.io/jam/game-off-2020) is an annual game jam, where participants spend the month
of November creating games based on a secret theme.

Game Off 2020 theme was “MOONSHOT”. Here are some of the games made with Rust:

-
[“War of the Moons”](https://vleue.itch.io/wotm)by[@FrancoisMockers](https://twitter.com/FrancoisMockers)made with[bevy](https://bevyengine.org)([source code](https://github.com/mockersf/wotm)).Your goal is to conquer the planet, but it’s not possible until you control all the moons. The end result is not completely what I wanted, but it was a nice occasion to try

[rapier](https://rapier.rs)for physics and[lyon](https://github.com/nical/lyon)to draw shapes from[bevy](https://bevyengine.org).![gameplay](../../assets/ce4fa7efce0b3980.png)

-
[“Starlight 1961”](https://grzi.itch.io/starlight-1961)by[@grzi](https://twitter.com/JeremyThulliez)made with[amethyst](https://amethyst.rs)([source code](https://github.com/grzi/starlight-1961)).A die and retry landing game where you control a spaceship, its fuel and health inside 10 different levels. Each level is made up of enemies (cannons, plasma doors, saw blades, etc.), bonuses (fuel, health) and coins.

[@grzi](https://twitter.com/JeremyThulliez)also published a devlog post:[“My journey into GitHub GameOff 2020”](https://www.wootlab.io/blog/my-journey-into-github-gameoff-2020).![gameplay](../../assets/b451bf2795280582.png)

-
[“Everfight”](https://snoozetime.itch.io/everfight-gameoff2020)by[@SnoozeTime](https://github.com/SnoozeTime)made with[luminance](https://github.com/phaazon/luminance-rs)([source code](https://github.com/SnoozeTime/spacegame)).Battle hordes of human spaceships in order to reach the moon. Wave after wave, the enemy becomes stronger. Unlock infinite mode once you finished the game and try to beat your personal record.

![gameplay](../../assets/3b1cb9bccddab499.jpg)


## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

[“Hands-on Rust: Effective Learning through 2D Game Development and Play”](https://pragprog.com/titles/hwrust/hands-on-rust/)
by Herbert Wolverson is now in beta. The book teaches Rust through game development
examples, and is targeted at readers who have some experience with writing code
in other languages. It teaches beginner to intermediate-level Rust. It also teaches
high-level gamedev concepts, notably Entity-Component System (ECS) theory.

After walking you through installing Rust, a few simple examples teach the language basics. Then you put these together to make “Flappy Dragon” - a simple Flappy Bird clone. The book then changes gear and begins to build a dungeon crawler (roguelike) with tile graphics. The first beta walks you through the basics, “Flappy Dragon” and making an ECS-based dungeon crawler skeleton - focused on teaching basic Rust, ECS composition and control flow. Beta 2 added health, a heads-up display, combat and win/lose conditions - focused on making the user comfortable with Rust’s amazing iterator system. Beta 3 will add fields-of-view, more dungeon designs and map theming - focused on teaching trait use and creation.

Beta 1 launched November 11th, Beta 2 launched November 25th. The next beta is expected December 8th.

[@thefuntastic](https://thefuntastic.com) published an article detailing why Rust has the potential
to be significant for the future of programming in games:
the origins of the language, overview of the main technical features,
why Rust’s popularity grows, the state of the ecosystem,
main challenges lying ahead, and links
to some Rust gamedev resources and communities.

*Discussions:
/r/rust,
hacker news*



![A screenshot from the talk](../../assets/348ee9591d2d57dd.jpg)

[watch the recording here](https://youtube.com/watch?v=Yb-QR3Vm3sk).

This month, [@dns2utf8](https://twitter.com/dns2utf8) gave a [talk](https://youtube.com/watch?v=Yb-QR3Vm3sk) about
how to build a multiplayer game with actix-web that people with
any modern browser shipping JavaScript, Canvas Context2D and Websocket can play.

How coding a system with so many independently moving parts is less about the bits and bytes but more about the high-level capabilities rust offers. In this talk Stefan Schindler @dns2utf8 focused on how he designed the whole system from concept to implementation including hosting it on a CO2 neutral server.


You can play the MultiPlayer Snake game itself on [mps.estada.ch](https://mps.estada.ch).

Also, a [follow-up text note](https://estada.ch/2020/11/2/how-to-build-a-multiplayer-game-rustfest-global-2020-pre-event) was released.

[@Ratys](https://twitter.com/ratysz) wrote an article about system schedulers in [ECS](https://en.wikipedia.org/wiki/Entity_component_system). It contains
an overview of the scheduling problem itself, covers the constraints a solution
to it should consider, and dissects schedulers of [Bevy](https://bevyengine.org) engine and [ yaks](https://crates.io/crates/yaks) as
examples.

![Tutorial result](../../assets/071547248ecea93d.gif)

[@guimcaballero](https://twitter.com/guimcaballero) published a tutorial on using Bevy 0.3 to make a Chess clone in
3d. Most of the concepts are explained along the way, from how to load meshes to
how to select pieces and board squares, using [bevy_mod_picking](https://github.com/aevyrie/bevy_mod_picking/).

Development of new tutorial content has slowed down due to wgpu still being in
development. [@sotrh](https://patreon.com/sotrh) has committed to continue maintaining the project through
the coming version changes, and plans to add more new content when the API
solidifies. He with the help of other contributors such as GitHub user
[@kanerogers](https://github.com/kanerogers) worked through a series of issues to polish the repository before
the content freeze.
In addition to that he added a [compute pipeline showcase](https://sotrh.github.io/learn-wgpu/showcase/compute)
and an [imgui showcase](https://sotrh.github.io/learn-wgpu/showcase/imgui-demo).

In other news @sotrh has started a [Patreon](https://patreon.com/sotrh) to help fund research
and development on the Learn Wgpu site as well as other wgpu related projects.

You can learn more [on the Learn Wgpu news page](https://sotrh.github.io/learn-wgpu/news).

## Library & Tooling Updates [#](https://gamedev.rs#library-tooling-updates)



![Bevy's Breakout example running on an iPhone XR](../../assets/850f2bb9ad43658d.jpg)

[cargo-mobile](https://dev.brainiumstudios.com/2020/11/24/cargo-mobile.html) is a tool created by [Brainium Studios](http://www.brainiumstudios.com/site/index.html) to simplify Rust mobile
development. It generates Xcode and Android Studio projects, and provides handy
commands for building and deploying apps to iOS and Android devices.

This month, [profiling](https://crates.io/crates/profiling) was released on crates.io. This crate provides a very
thin abstraction over instrumented profiling crates like `puffin`

, `optick`

,
`tracy`

, and `superluminal-perf`

.

Mark up your code like this:

```
#[profiling::function]
fn some_function() {
burn_time(5);
for i in 0..5 {
profiling::scope!("Looped Operation");
burn_time(1);
}
}
```


And get visualizations like this (`optick`

and `puffin`

shown):

[rkyv](https://github.com/djkoloski/rkyv) is a zero-copy deserialization framework for Rust. It’s similar to
FlatBuffers and Cap’n Proto and can be used for data storage and messaging.

It has a handful of features that make it stand out:

- No schema restrictions.
- HashMap support out of the box.
- Trait object support through the
crate.`rkyv_dyn`

- Validation through the
crate, suitable for untrusted and potentially malicious data.`bytecheck`

- Safe mutable archives with pinning.

Reddit user [vlmutolo](https://reddit.com/r/rust/comments/jx32e8/rkyv_02_and_bytecheck_validation_mutable_archives/gcyfoqc) also made a [toy benchmark](https://git.sr.ht/~vlmutolo/rkyv-bench/tree/master/src/main.rs) comparing rkyv against serde
and bincode and found that rkyv had promising initial numbers:

```
serialize (bincode): 89 ns/iter
serialize (rkyv): 86 ns/iter
deserialize (bincode): 118 ns/iter
deserialize (rkyv): 16 ns/iter
```


A write-up on the [architecture and internals of rkyv](https://davidkoloski.me/blog/rkyv-architecture/) is also available.

*Discussions:
/r/rust (v0.1),
/r/rust (v0.2)*

[assets_manager](https://github.com/a1phyr/assets_manager) v0.4 [#](https://gamedev.rs#assets-manager-v0-4)

[assets_manager](https://github.com/a1phyr/assets_manager) provides a convenient way to work with external files, making
resources caching and hot-reloading easy and straightforward.

Version 0.4.0 was released this month, bringing loads of improvements.

- A
`Source`

trait, to load assets from anywhere. It makes the crate usable in WebAssembly. - Assets that can load other assets, with a transparent integration with hot-reloading. Using a manifest file has never been so easy!
- Improved performance.
- See the
[full changelog](https://github.com/a1phyr/assets_manager/releases/tag/v0.4.0)for more information.

![Dashboard demo](../../assets/1106e1e0b721e176.gif)

[Terra Mach](https://github.com/lykhonis/terramach) is a mapping frontend system to build graphical interfaces
for devices. It focuses on experiences around statistical data (graphs, diagrams),
mapping, and user input. When it comes to user experience, elements a user
interacts with are flexible enough to build many common experiences. Terra Mach
is highly inspired by Flutter. It leverages graphics library Skia to enable
highly performant 2D graphics.

[glam](https://github.com/bitshifter/glam-rs) is a simple and fast linear algebra crate for games and graphics.

This month version 0.11.2 was released. There were a number of important changes since the last newsletter.

The vector accessor methods for setting and getting individual vector elements
were replaced with direct access support. This means that now instead of needing
to use `.x()`

, `.set_x(x)`

or `.mut_x() = x`

the element may be accessed
directly via `.x = x`

and so on.

The reason that this was not done originally was that some types are backed by
SIMD types which do not support direct access. For these types direct access is
now supported with `Deref`

and `DerefMut`

implementations.

The direct access support was added in version 0.10.1 along side the accessor methods. The accessor methods were deprecated in 0.10.2 and have been removed in 0.11.0.

[winit](https://github.com/rust-windowing/winit) is a cross-platform window creation and event loop management library.

winit is looking for a new web platform maintainer! If you’re
interested, or know anyone who is, you can reach out via the
[tracking issue](https://github.com/rust-windowing/winit/issues/1777).

[Fluffl](https://github.com/K-C-DaCosta/fluffl) is a WIP generic media layer for graphics, IO, and audio
for desktop and the browser.

The only reason I wrote this crate at all was because I personally wanted to just have a generic interface were I can just write my OpenGL apps once and have that build to both desktop and the browser with little to no modification to source code.


Two demos are available atm:

- Basic graphics (using raw OpenGL via the “glow” crate) and audio demo:
[here](https://k-c-dacosta.github.io/wasm_bins/examples/audio_ex_1/). - Breakout clone demo:
[here](https://k-c-dacosta.github.io/wasm_bins/examples/brick_demo/).

*Discussions:
/r/rust*

[Rapier](https://rapier.rs) is a set of 2D and 3D physics engines for games, animation and
robotics written in Rust.

[This month](https://www.dimforge.com/blog/2020/12/01/this-month-in-dimforge/) the version 0.4.0 has been released with
exciting new features:

- the ability to read contact and proximity information from the narrow-phase.
- the ability to lock some translations and/or rotations for a rigid-body without using joints.

The following demo shows examples of translation locking (on the blue cuboid) and rotation locking (full locking on the capsule, partial locking on the cuboid):

![Rapier features](../../assets/097cf2b6eca902c4.gif)


A cross-platform determinism bug appearing on MacOS with the new Apple M1 ARM processor has also been fixed.

The [bevy_rapier](https://www.rapier.rs/docs/user_guides/rust_bevy_plugin/getting_started) plugin for the Bevy game engine has been updated to support
all the aforementioned features. In addition, it supports:

- the automatic removal of rigid-bodies, colliders, and joints when the entity they are attached to are removed from the Bevy ECS.
- the ability to attach multiple colliders to a single rigid-body using Bevy Hierarchy.

[Salva](https://salva.rs) is a set of 2D and 3D particle-based fluids simulation engines for
games and animation written in Rust.

Starting [this month](https://www.dimforge.com/blog/2020/12/01/this-month-in-dimforge/) Salva 0.5.0 no longer supports
[nphysics](https://nphysics.org) for simulating rigid-bodies. Instead, it implements two-ways
coupling with [Rapier](https://rapier.rs) (see the
[demo](https://twitter.com/dimforge/status/1329467380158898183)).

In addition to the Rapier integration, it is now possible to query Salva to retrieve all the fluid particles located inside an AABB. This can be useful for, e.g., spawning new particles ensuring there isn’t anything there already.

![rib](../../assets/8dad84cd5eb8a3cd.gif)


Parsing a 3D model file and understanding the different links between bone matrices, keyframes and vertices is a task that can take a lot of time and motivation of the developer. On top of that, combining the different bone transform matrices for the current frame is often error prone.

[rib](https://github.com/bmatthieu3/rib) is an attempt to tackle these problems and might help you save time.
Current features of [rib](https://github.com/bmatthieu3/rib) include:

- Support of collada files coming from the latest Blender version.
- Precomputation of the bone matrices expressed in the world space so that you just have to pass it to your shader for traditional GPU skinning.
- Interpolation between keyframes.
- (De)/serialization in binary thanks to
[bincode](https://github.com/servo/bincode).

[rib](https://github.com/bmatthieu3/rib) can be greatly extended, for example with the support of other format
handling skeleton data, such as the [glTF](https://github.com/KhronosGroup/glTF/blob/master/README.md) format.
Contributions are more than welcome.

[Kira](https://github.com/tesselode/kira) by [@tesselode](https://twitter.com/tesselode) is an audio library designed to help create expressive
audio for games. It aims to fill the holes in many game engines’ built-in audio
APIs with features for creating seamless music loops and scripting audio events.

v0.2.0 is coming out soon with an Arrangements feature for creating complex pieces out of individual sounds, tween easing, panning support, and workflow improvements.

The gfx-rs team has published a post [“The Big Picture”](https://gfx-rs.github.io/2020/11/16/big-picture.html) providing
the overview of all projects in the works, and how they are connected to each other.

[wgpu](https://github.com/gfx-rs/wgpu) has moved from [gfx-extras](https://github.com/gfx-rs/gfx-extras) to the new [gpu-alloc](https://github.com/zakarumych/gpu-alloc) and [gpu-descriptor](https://github.com/zakarumych/gpu-descriptor)
libraries by [@zakarumych](https://github.com/zakarumych). These are backend-agnostic, which allows `wgpu`

to now depend on `gfx-hal`

directly without intermediates. Patching [gfx-rs](https://github.com/gfx-rs/gfx)
will now be easier, without the need to release every little change.

Finally, all the latest [wgpu](https://github.com/gfx-rs/wgpu) code has landed into Gecko, and new
features and fixes are implemented in Firefox. That allows it to run
most of the updated [WebGPU samples](https://austineng.github.io/webgpu-samples).

![Iced - Game of Life example](../../assets/08021642cd86e523.gif)

[Game of Life example](https://github.com/hecrj/iced/tree/0.2/examples/game_of_life), made with Iced

Iced is an experimental cross-platform GUI library focused on simplicity and
type-safety. Inspired by [Elm](https://elm-lang.org).

[A new minor version](https://github.com/hecrj/iced/pull/637) was released this month containing a bunch of
improvements:

- An OpenGL renderer powered by
and`glow`

. It is an alternative to the default`glutin`

renderer.`wgpu`

- A trait-based approach to react to mouse and keyboard interactions in the
`Canvas`

widget. - Basic overlay support, allowing the superposition of interactive widgets on top of other widgets.
- A drop-down selector widget built on top of the overlay support.
- A widget that displays a QR code, powered by
.`qrcode`

- Additional internal enhancements, like event capturing and a faster event loop.

*Discussions:
/r/rust*

![KAS markdown](../../assets/a41116edf4633ee9.png)

[KAS](https://github.com/kas-gui/kas) by [@dhardy](https://github.com/dhardy) is a general-purpose UI toolkit; its
initial aim is “old school” desktop apps with good keyboard and touchscreen
support. Unlike many modern immediate-mode UIs, KAS’s widgets retain state,
allowing minimal per-frame updates. KAS supports embedded WebGPU graphics now,
and plans to support embedded usage and additional rendering systems.

[KAS-text](https://github.com/kas-gui/kas-text) v0.2 saw a significant revision to its API, including support for
rich text (bold, italic, underline, size and some layout improvements).
[KAS](https://github.com/kas-gui/kas) v0.6 pulls in those changes and adds a few fixes and QoL improvements.

![online demo](../../assets/e0d7adce983f41e7.png)


[Egui](https://github.com/emilk/egui) is a highly portable immediate mode GUI library in pure Rust.
This month a [v0.4.0 version](https://github.com/emilk/egui/blob/master/CHANGELOG.md#040---2020-11-28) was released
with much-improved text editing, and many bugfixes.
Check out an [updated online demo](https://emilk.github.io/egui).

Also, [egui_web](https://lib.rs/egui_web) v0.4.0 was released, with a simple fetch API -
[online example](https://emilk.github.io/egui/example.html).

![miniquad_wayland](../../assets/b3ad57818fefe0a7.gif)

[miniquad](https://github.com/not-fl3/miniquad) is cross-platform windowing and rendering library.

This month [KMS](https://www.kernel.org/doc/html/v4.15/gpu/drm-kms.html) [PR](https://github.com/not-fl3/miniquad/pull/158) landed on miniquad.
Now miniquad can run on without neither X11 or Wayland,
right on the Linux kernel with KMS.

![macroquad_particles](../../assets/8732b0b27fd3b153.gif)

[macroquad](https://github.com/not-fl3/macroquad) is a cross-platform (Windows/Linux/macOS/Android/iOS/WASM)
game framework built on top of [miniquad](https://github.com/not-fl3/miniquad).

This month macroquad got particle system editor aiming for simple 2d pixel-art
style effects: [try it out online here](https://fedorgames.itch.io/macroquad-particles).

![Animated low-poly character rendered by Dotrix](../../assets/4207359d9782bdb5.png)

The goal of [Dotrix](https://github.com/lowenware/dotrix) is to become a 3D engine for the new RPG project. The
engine is free and open source, delivering a set of common high-level features
like skeletal animation, skybox, terrain, camera controlling, input mapping and
many others. It is built on top of the [wgpu](https://github.com/gfx-rs/wgpu) with an ECS core
which is a part of the engine.

Currently supported features:

- Linear ECS with systems as simple functions, that can have optional context.
- Import of textures from PNG files.
- Import of multiple assets from GLTF files (textures, meshes, skins and animations).
- FPS and delta time counters.
- Rendering of meshes and simple scenes with light and camera controls.
- Rendering of skeletal animations.
- 3 showcase demo applications.

Next in sprint:

- Input management and mapping;
- Full camera control with mouse;
- Skybox renderer.

[Tetra](https://github.com/17cupsofcoffee/tetra) is a simple 2D game framework, inspired by XNA and Raylib. This month,
versions 0.5.3 and 0.5.4 were released, with some frequently requested features:

- A
`Mesh`

API, allowing users to create arbitrary 2D geometry - Experimental support for high-DPI rendering

There has also been numerous bug fixes and documentation improvements. For full
details and a list of breaking changes, see the [changelog](https://github.com/17cupsofcoffee/tetra/blob/main/CHANGELOG.md).

![logo](../../assets/4550d81eb2c8da32.png)


[Old Gods](https://github.com/schell/old-gods) is an WIP game engine meant for games
targeting the web and SDL2.
It reads Tiled map files into a specs based entity component system.
Rendering is handled by HtmlCanvasElement or the built-in SDL2 renderer.

*Discussions:
/r/rust*

[ogmo3](https://github.com/17cupsofcoffee/ogmo3) is a Rust crate for parsing projects and levels created with
[Ogmo Editor 3](https://ogmo-editor-3.github.io/). This month, version 0.1 was released, adding serialization
support, and helper methods for unpacking layer data. The [sample code](https://github.com/17cupsofcoffee/ogmo3/blob/main/examples/sample.rs)
has also been updated to show the new helpers in action.

![lots of overlapping bunnies](../../assets/56b7a021860158c0.png)

[ggez](https://github.com/ggez/ggez) is a 2D game framework inspired by Love2D. The project is chugging
along getting everything prepared for a 0.6 release at the end of 2020,
and a lot of work has been done in the last month:

- All major dependencies have been updated, including a long-overdue
update to
`winit`

0.23. - Over a dozen pull requests have been merged, large and small.
- A bunch of old issues have been cleaned up.

Major features to look forward to include far better math performance, a
`MeshBatch`

type, better ergonomics on Linux Wayland, and more. There’s
lots of work still to be done though. A bunch of issues are out of date
and need triage, docs need to be proofread, and especially examples need
be updated and tested on every platform imaginable. Try out the `devel`

branch and give it a go!



![a scene with lightning and multiple hi-poly character models](../../assets/e2b25332ffb377da.jpg)

[rg3d](https://github.com/mrDIMAS/rg3d) is a game engine that aims to be easy to use and provide large set
of out-of-box features. Some of the recent updates:

- Migrated to nalgebra from custom linear algebra.
- Replaced custom physics engine with Rapier.
- Implemented sound backend for macOS.
- Environment mapping - now objects can have reflections.
- Implemented geometry instancing - now you can render tons of objects with low overhead.
- Performance improvements.
- Added
[gobo](https://en.wikipedia.org/wiki/Gobo_(lighting))for spot lights. - Added CPU lightmapper - it is possible now to “bake” static lighting into a texture to improve performance.

Join the [rg3d’s Discord channel](https://discord.gg/xENF5Uh)
or follow [Dmitry Stepanov on Twitter](https://twitter.com/DmitryS36934349).

![multiple windows with asm and sprites](../../assets/1ee7441c47cc80f2.png)

[Another World Suite](https://github.com/malandrin/another-world-suite) by [@c_botana](https://cesarbotana.com/) is a Rust
implementation of the [“Another World”](https://en.wikipedia.org/wiki/Another_World_(video_game)) (“Out of This World” in USA)
game engine, compiled to WebAssembly to run it in the web.
It also includes a debugger and a resources viewer.

*Discussions:
Twitter*

![f1-telemetry-tui](../../assets/6b7967d2b2721c2a.gif)


[F1 Telemetry TUI](https://github.com/aldidana/f1-telemetry-tui) by [@aldidana](https://github.com/aldidana) is a terminal telemetry tool for F1 video games.

*Discussions:
Twitter*

![demo of running inferences for all digits](../../assets/82a2c268aab929b4.gif)

[bevmnist](https://vleue.itch.io/bevmnist-poc) by [@FrancoisMockers](https://twitter.com/FrancoisMockers) is a PoC for running
inferences from a neural network in a game made with [bevy](https://bevyengine.org), that can run in
WASM (source code on [github](https://github.com/vleue/bevmnist)).

Using [tract](https://github.com/sonos/tract), the goal was to test running neural network inferences from a
game. [MNIST handwritten digits classification](http://yann.lecun.com/exdb/mnist/) is the “hello world” of
neural networks, and has small enough networks available in [onnx](https://onnx.ai) format that
can run in real time in WASM. This project also has github actions that will
build and release a [bevy](https://bevyengine.org) game to itch.io for Linux, macOS, Windows and WASM.

## Popular Workgroup Issues in GitHub [#](https://gamedev.rs#popular-workgroup-issues-in-github)

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[winit is seeking new maintainers](https://github.com/rust-windowing/winit/issues/1777).[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[gfx-rs’s “contributor-friendly” issues](https://github.com/gfx-rs/gfx/issues?q=is%3Aissue+is%3Aopen+label%3Acontributor-friendly).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[A/B Street’s “good first issue” issues](https://github.com/dabreegster/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/good%20first%20issue).

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!