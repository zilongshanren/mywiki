---
title: 'This Month in Rust GameDev #9 - April 2020'
url: https://gamedev.rs/news/009/
author: Rust GameDev WG
published: '2020-05-06'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the ninth issue of the Rust GameDev Workgroup’s
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

[This month’s London Rust meetup](https://meetup.com/Rust-London-User-Group/events/269357779) features three gamedev talks:

- “Rust GameDev WG” by
[@_AlexEne_](https://twitter.com/_AlexEne_)([slides](https://docs.google.com/presentation/d/1-uPn_a03oePVxJrw6l0u-DYlbJC_1i8i4DMs5J2grGw)) - “Levelling up in Rust” by
[@oliviff](https://twitter.com/oliviff)([slides](https://docs.google.com/presentation/d/1R49kKosTRoQU6UPk9xAc8fXd3_GEnzzrrEfKwS97XHM)) - “Scala to Rust: one game at a time” by
[@plippe](https://github.com/plippe)([slides](https://docs.google.com/presentation/d/1YP9ksYnk0Mzycywd0w_4X4QWAPQEqZtm8zTTvVEtedM))

Here’s a [direct link to the recorded stream](https://youtube.com/watch?v=o9QeKfKLXXM).

[DUNGEONFOG](https://dungeonfog.com/) is Hiring [#](https://gamedev.rs#dungeonfog-is-hiring)

![DUNGEONFOG editor](../../assets/32f08446c1a1842a.jpeg)


[DUNGEONFOG](https://dungeonfog.com/) are developing editor tools for drawing and visualizing
RPG tabletop maps.
They’re looking for a wgpu-rs developer for 2D graphics drawing.

You can find all of the details on their [job offer page](https://dungeonfog.com/about/job-offers/).

## Game Updates [#](https://gamedev.rs#game-updates)

[“Crate Before Attack”](https://cratebeforeattack.com) by @koalefant
is a multiplayer game where frogs combat their friends
while navigating a landscape with their sticky tongue.
It is a hybrid of a realtime and turn-based game.

The game [can be played right in the browser (PC-only)](https://cratebeforeattack.com/play).

It is built for Web using [miniquad](https://github.com/not-fl3/miniquad) and [tokio](https://tokio.rs) crates and features:

- Swift roping (aka grappling hook);
- Diverse weapons;
- Local and online multiplayer;
- Procedural animation;
- Fun physics.

Check the [devlog](https://cratebeforeattack.com/posts). It has three posts atm:

Also, there’re a lot of dev videos on the game’s
[YouTube channel](https://youtube.com/channel/UC_xMilPTLuuE5iLs1Ml9zow).

[A/B Street](https://github.com/dabreegster/abstreet#ab-street) is a game by [dabreegster](https://github.com/dabreegster/) exploring how small changes to
road space and traffic signals affect the movement of drivers, cyclists,
transit users, and pedestrians. The game models Seattle as accurately as
possible using [OpenStreetMap](https://openstreetmap.org) and other public datasets, lets the player adjust
existing infrastructure, and then does a detailed comparison to see who the
changes help and hurt.

First of all, [a standalone 2D GUI crate](https://www.reddit.com/r/rust/comments/fejx5a/demo_of_a_new_gui_2d_drawing_crate/) was published
extracted from A/BStreet’s GUI code.
It features fully vectorized text using [lyon](https://github.com/nical/lyon) and supports lots of
widgets such as “buttons (with keybindings), checkboxes, sliders, pop-up menus,
text entry, and some data viz things”.
Thanks to its simplicity (everything is a colored polygon), this crate runs on
many different architectures and even on the web via [glow](https://github.com/grovesNL/glow).

Here’s an example of what it can do:

![abstreet gui](../../assets/5e995793cc4a2b15.png)


Dabreegster also uploaded a recorded version of their
[rust meetup talk](https://www.reddit.com/r/Citybound/comments/g1k6du/rust_meetup_talk_on_ab_street/) about the inner working of abstreet.

In case anybody here is interested in more city simulation in Rust, the talk is about half project overview and half deep dive into code.


ABstreet had some great contributor work coming in, notably from omalaspinas who implemented an optional SEIR pandemic model into the game.

And for anyone interested in more frequent updates, the
[abstreet subreddit](https://www.reddit.com/r/abstreet) has had weekly update posts since
September 2019.

*Discussions:
/r/rust*

![citybound web ui screenshot](../../assets/6503021a799d800d.jpeg)


Citybound is a city building game that uses microscopic models to vividly simulate the organism of a city arising from the interactions of millions of individuals.


It is developed by [aeplay](https://github.com/aeplay) and uses a homemade actor system for
everything called [kay](https://crates.io/crates/kay), you can see its power on
[this impressive tech demo](https://youtu.be/qr9GTTST_Dk).

In April, aeplay made two livestreams about conceptualizing pedestrians and
pandemic models using feedback from the chat.
You can watch the replay for the two livestreams on youtube: [here](https://youtu.be/fQMxVV57wzg)
and [here](https://youtu.be/8DevxAYw47A).

![Pedestrians](../../assets/acb5e577148d5271.png)


[Scale](https://github.com/Uriopass/Scale) is a granular society simulation by [Uriopass](http://douady.paris/aboutme.html), with the objective
of having fully autonomous agents interacting with their world in real time.

A [devlog](http://douady.paris/blog/scale_3.html) was published, explaining how pedestrians were added
to the simulation, and that a new renderer based on [wgpu-rs](https://github.com/gfx-rs/wgpu-rs) is in
development.
[A short video](https://youtu.be/QXF1-1BNddM) was also posted together with the post
for a more concise update.

*Discussions:
/r/rust_gamedev*

### For The Quest [#](https://gamedev.rs#for-the-quest)

![For The Quest screenshot](../../assets/42b6913cf27344c4.jpg)


For The Quest is the working title for a game in early development by
[@seratonik](https://twitter.com/seratonik). Written entirely in Rust and compiled to WebAssembly,
For The Quest is destined to become a MMORPG set in a post-apocalyptic
Earth where your goal is to band together into like-minded factions to
not only survive in this new world, but to unearth the cause of humanity’s
downfall.

For The Quest is currently undergoing engine development with a focus on running smoothly in modern browsers using WebGL 2.0 before moving onto native desktop ports.

New developments in April:

- Finished re-working and optimizing the rendering pipeline to allow for post-processing and other screen-space effects
- Planar reflections implemented, and work with an upgraded form of the specular maps to determine how reflective a surface is
- Add a flagging system so surfaces can identify their type to the shading system so effects can be selectively applied per pixel
- Used the new flagging system to identify water surfaces and make them “ripple” their reflections
- Updated the mapping/tile system to support “sunken” floor tiles, which allows for ponds, lakes, cliff edges, etc.
- Started work on plans for a streaming asset manager
- New desert/sand tileset models & textures (Thanks
[Mishayla](https://www.artstation.com/mpaulson)!)

Follow [@seratonik](https://twitter.com/seratonik) on Twitter for updates.

![shadows demo](../../assets/304dc656e46f7902.jpeg)


[Akigi]is a multiplayer online world where humans aren’t the only intelligent animals.

Some of this months’s updates:

Full devlogs:
[#061](https://devjournal.akigi.com/april-2020/061-2020-04-05.html),
[#062](https://devjournal.akigi.com/april-2020/062-2020-04-12.html),
[#063](https://devjournal.akigi.com/april-2020/063-2020-04-19.html),
[#064](https://devjournal.akigi.com/april-2020/064-2020-04-26.html).

### Blobs’n’Bullets [#](https://gamedev.rs#blobs-n-bullets)

![shmup](../../assets/bebe82e11f8e7c9b.gif)


[@rhmoller started working](https://twitter.com/rhmoller/status/1254179448586481669) on
a retro twin-stick shooter “Blobs’n’Bullets”.
It uses WASM, web-sys, canvas and the gamepad-api
and features a local 2-player coop.

![gameplay screenshot with ASCII art graphics](../../assets/ec5eb30d6663c646.png)


[Native Systems](https://nativesystems.rs) is working on “Colony Genesis” - an ant colony sandbox game
with ASCII graphics.
This month v0.1.3 and v0.1.4 versions were released. Some of the updates:

- Add controls to highlight all ants by behavior (SHIFT+select)
- Fix frame loop timer to prevent fast forwards
- Adds temperature diffusion and adjusts rates It should now be easier to maintain high enough temperatures over night and in lower soil layers for eggs to develop normally.

![shmup gameplay](../../assets/597c61d8f44b0e49.gif)


[ssshmup](https://github.com/mkhan45/ssshmup) by [@mkhan45](https://github.com/mkhan45)
is a small small shoot ’em up made with [ggez](https://ggez.rs) and [specs](https://github.com/amethyst/specs).

*Discussions:
/r/rust_gamedev*

[Alex Butler](https://twitter.com/bigabgames) continues to polish their “[Robo Instructus](https://store.steampowered.com/app/1032170/Robo_Instructus)” puzzle game -
[1.25, 1.26, and 1.27 versions were released](https://steamcommunity.com/app/1032170/allnews):
automatically follow execution when paused,
bugfixes, dependency updates, and performance optimizations.

Also, Alex published a new crate supporting the rasterization
of .otf lines and quad/cubic Bézier curves: [ab_glyph_rasterizer](https://crates.io/crates/ab_glyph_rasterizer).
It’s around 2-5x faster than the current rusttype .ttf rasterizer.

### Amethyst Games [#](https://gamedev.rs#amethyst-games)

-
“Conquest” by

[@takeryo_eeic](https://twitter.com/takeryo_eeic)is a hexagonal tactic game. This month[its model were updated](https://twitter.com/takeryo_eeic/status/1246189179467214850)and the UX was reworked to feel like moving chess pieces. Check out a[new gameplay video](https://twitter.com/takeryo_eeic/status/1249850460678193152): -
[Grumpy Visitors](https://github.com/amethyst/grumpy_visitors)by[@mvlabat](https://github.com/mvlabat)is a top-down 2D co-op action/arcade game highly inspired by Evil Invasion. Two weeks ago the game received a few updates of UI and multiplayer.Also,

[a short video](https://twitter.com/mvlabat/status/1257362218078867460)was posted to twitter, showing the latest state of Grumpy Visitors:![grumpy_visitors-video](../../assets/427b9a352382064d.gif)

-
[Boulder Dash](https://github.com/dpc/boulder-dash.rs)remake by[dpc](https://github.com/dpc)- a new remake of an old classic.![pixelart boulders](../../assets/d48097d38a8bb65d.png)

-
[Jérémy Thulliez](https://twitter.com/JeremyThulliez)shared their experience making 3 little games:- A
[gameboy proof-of-concept](https://twitter.com/JeremyThulliez/status/1255042737579134977)([repository](https://github.com/grzi/rust-gameboy-game-poc)) [Tetris](https://twitter.com/JeremyThulliez/status/1251903725276454913)([repository](https://github.com/grzi/rust-tetris))- Pong (
[blog post](https://www.wootlab.io/blog/pong-in-rust-with-amethyst),[repository](https://github.com/grzi/rust-pong))

- A
-
[Will](https://github.com/azriel91/autexousious)by[Azriel](https://twitter.com/im_azriel)is a moddable 2.5D action / adventure game.[This month’s update](https://azriel.im/will/2020/04/24/browsers-assemble/)includes preliminary support for WASM, with most effort directed in the underlying Amethyst library.Check out the

[video](https://youtu.be/Hc8EtqrlJsE)to see online play between native and web clients. -
[Realm.One](https://github.com/Machine-Hum/realm.one)is an open-source MMO game written using the Amethyst game engine. Recently there has been some simple AI integrated into the game. This will cause monsters to chase and attack you!Next up will be items and experience!

[“GameDev in Rust (Ep.2): Monsters and AI! (Part B)”](https://youtu.be/8hvnjKf4M5M)- ECS-based design with Amethyst, networking and tiled 2d based design.


### Ludum Dare 46 Games [#](https://gamedev.rs#ludum-dare-46-games)

[Ludum Dare 46](https://ldjam.com/) was this month!
The theme was “Keep it alive”, and there was a bunch of cool games made in Rust!
Here’s a roundup of some of them:

-
[“The Hum”](https://ldjam.com/events/ludum-dare/46/the-hum)by[Hoichael](https://ldjam.com/users/hoichael),[williwiderstand](https://ldjam.com/users/williwiderstand), and[NoahRo](https://ldjam.com/users/noahro)([source code](https://github.com/Noah2610/LD46-TheHum),[itch.io](https://noahro.itch.io/the-hum)):Feed the bonfire. Keep it alive.

![the hum screenshot](../../assets/67f5d55f21768be9.jpg)

-
[“The Last Ship”](https://ldjam.com/events/ludum-dare/46/the-last-ship)by[FedorL](https://ldjam.com/users/fedorl)([source code](https://github.com/not-fl3/ld46),[itch.io](https://fedorgames.itch.io/ld46),[Twitter thread](https://twitter.com/fedor_games/status/1251900504369778690)):Carry humanity from dying planet into the bright future!

![the last ship screenshot](../../assets/4176bf16a65588d3.jpg)

-
[“Frog Rations”](https://ldjam.com/events/ludum-dare/46/frog-rations)by[healthire](https://ldjam.com/users/healthire)([source code](https://github.com/Healthire/ld46),[Twitter thread](https://twitter.com/healthire_/status/1251412661016895488)):Keep the frog alive by eating flies, but beware of the snake!

![frog rations screenshot](../../assets/cc63a9750d9d1e67.jpg)

-
[“WOODS”](https://ldjam.com/events/ludum-dare/46/woods)by[Feilkin](https://ldjam.com/users/feilkin)([source code](https://github.com/Feilkin/mela/tree/master/examples/ld46),[itch.io](https://feilkin.itch.io/woods)):Keep the flame alive in the darkness!

![woods screenshot](../../assets/93d104fae9363c4f.jpg)

-
[“Wonder”](https://ldjam.com/events/ludum-dare/46/wonder)by[Ian Kettlewell](https://ldjam.com/users/ian-kettlewell)([source code](https://github.com/kettle11/LD46),[itch.io](https://kettlecorn.itch.io/wonder)):Keep alive a sense of wonder.

![wonder screenshot](../../assets/2f871e192274f48d.jpg)

-
[“Lighthouse Keeper”](https://ldjam.com/events/ludum-dare/46/lighthouse-keeper)by[dooskington](https://ldjam.com/users/dooskington)([source code](https://github.com/Dooskington/ld46),[itch.io](https://dooskington.itch.io/ld46-lighthouse-keeper)):Alone on a rock in the sea, your job is an important one. Keep the lighthouse safe and operational, and don’t lose your mind. The goal is to survive for 30 days. Unfinished.

![lighthouse keeper screenshot](../../assets/b2c483a74a8e48dc.jpg)

-
[“Fermi Paradox”](https://ldjam.com/events/ludum-dare/46/fermi-paradox)by[tversteeg](https://ldjam.com/users/tversteeg)([source code](https://github.com/tversteeg/ld46)):How come we don’t see any life from other planets? What does an intergalactic society need to do to survive? Fermi Paradox is a combination of the arcade games of yesteryear with some modern twists.

![fermi paradox screenshot](../../assets/4784e3110788bc7b.jpg)


![Buildings](../../assets/f57a5f733fd7b1f1.png)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG
inspired by Dwarf Fortress and Cube World.

Lots of systems have been finished up in April to prepare for the launch of 0.6. Many improvements have been made to the combat systems. Basic world and civilization simulations have been implemented. Lots of new soundtracks have been added. The UI is being reworked. Experimental work is being done with migrating to wgpu, and the level of detail system is a lot closer to being merged. Villagers have been getting a lot of love as well, making the world feel more alive.

Here is the April changelog:

```
- Complete rewrite of the combat system into a state machine
- Abilities like Dash and Triplestrike
- Fireball explosions
- Many new armors and weapons to find in chests
- Fleshed out "attack" animation into alpha, beta and spin type attacks
- Fleshed out range attack into charging and shooting anims for staff/bow
- Added a silhouette for players when they are occluded
- Added transparency to the player when zooming in
- Added dragging and right-click to use functionality to inventory,
armor & hotbar slots
- Added basic world and civilisation simulation
- Added fields, crops and scarecrows, paths, bridges, procedural house generation
- Added lampposts, NPCs that spawn in towns, and simple dungeons
- Added sub-voxel noise effect
- Added waypoints next to dungeons
- Added non-uniform block heights
- Added a Level of Detail (LoD) system for terrain sprites and entities
- Villagers tools and clothing, cultists clothing
- You can start the game by pressing "enter" from the character selection menu
```


![Hanging out](../../assets/7b47ebd489562b99.png)

You can read more about some specific topics from April:

The final touches of 0.6 are wrapping up. The team will meet once 0.6 is released to disucss what 0.7 will look like. See you next month!

April’s full weekly devlogs: “This Week In Veloren…”:
[#62](https://veloren.net/devblog-62),
[#63](https://veloren.net/devblog-63),
[#64](https://veloren.net/devblog-64),
[#65](https://veloren.net/devblog-65),

## Library & Tooling Updates [#](https://gamedev.rs#library-tooling-updates)

### Rust Sokoban Tutorial [#](https://gamedev.rs#rust-sokoban-tutorial)

![sokoban level](../../assets/e8a84637c6e165c6.gif)


Rust Sokoban tutorial is an online book aimed at Rust gamedev beginners
which walks through making a simple Sokoban game using ECS, ggez and specs.
It tries to teach the basics of architecting in ECS and basic Rust concepts
through a hands-on approach.
[@oliviff](https://twitter.com/oliviff) is currently looking for a few people
to beta test the tutorial before it goes live,
if you’ve got a spare couple of hours and you’d like to contribute,
send her a [DM](https://twitter.com/messages/compose?recipient_id=118804845).

[@dasifefe shared their thoughs](https://dasifefe.com/post-2020-04-05-01.html)
about using multiple ECSes in a project.

[@bitshifternz](https://twitter.com/bitshifternz) (author of [glam](https://github.com/bitshifter/glam-rs)) has written [a blog post](https://bitshifter.github.io/2020/04/12/mathbench-build-timings)
about comparing build times of some popular Rust gamedev math crates
(including glam, cgmath, nalgebra, euclid, vek, pathfinder_geometry)
using a [mathbench-rs](https://github.com/bitshifter/mathbench-rs) unit tests suit.

@hoj-senna started writing a new tutorial about [ash](https://github.com/MaikKlein/ash) and Vulkan in general:
[“Ashen Aetna”](https://hoj-senna.github.io/ashen-aetna).
The current version has 20 chapters and covers basics of general 3d graphics
and setting all the stuff you need to draw your first triangle with [ash](https://github.com/MaikKlein/ash).

*Discussions:
/r/rust*

![demo of how the Z-order curve fills the space](../../assets/12f94191b3502a4a.jpeg)


[@snorrwe](https://snorrwe.onrender.com/) has written [a blog post](https://snorrwe.onrender.com/posts/morton-table)
about exploring an implementation of a linear quadtree
and comparing it with a naive implementation of spacial data querying.
All code mentioned in the post [is available on GitHub](https://github.com/snorrwe/morton-table).

*Discussions:
/r/rust*

[@sylvain has written a tutorial](https://dev.to/sobertkaos/simple-2dcamera-system-for-rust-with-ggez-2o2h) about implementing
a simple 2D camera on top of [GGEZ](https://ggez.rs).

![logo](../../assets/cacec5cb17e0e08d.jpeg)


Authors of [Vis Arcana](https://visarcana.com/2020/05/04/what-is-vis-arcana/) shared a [blog post](https://visarcana.com/2020/04/24/our-backend-technology)
explaining why they’ve chosen Rust for their project’s backend.

… Rust advertises as a very productive language in which most errors (apart from logical ones) are caught at the compilation stage. After more than a year of working with it, I must admit that it’s absolutely correct – new game modules are added extremely quickly, and the number of errors has dropped to practically zero. …


![an example of a multi-layered game level](../../assets/66d20c9520810790.jpeg)

[Anthropic Studios](https://anthropicstudios.com) has [shared a post](https://anthropicstudios.com/2020/03/30/symmetric-matrices)
about implementing a layer system to [“Way of Rhea”’s](https://store.steampowered.com/app/1110620/Way_of_Rhea) physics engine
using [symmetric matrices](https://en.wikipedia.org/wiki/Symmetric_matrix) and [triangle numbers](https://en.wikipedia.org/wiki/Triangular_number).

[turbulence](https://github.com/kyren/turbulence) and [goggles](https://github.com/kyren/goggles) [#](https://gamedev.rs#turbulence-and-goggles)

This month @kyren released two libraries: [turbulence](https://github.com/kyren/turbulence) and [goggles](https://github.com/kyren/goggles).


[turbulence]is the more interesting of the two, it is another attempt at a rust-based networking library for games. The main thing I think that sets it apart is that it is async while being totally reactor, executor, and platform agnostic. It is a library that just allows you to take a stream of unreliable, unordered packets and turn them into N independent unreliable, unordered or reliable, ordered streams of messages.

[goggles]is probably not as interesting, but it is an aggressively stripped down fork of specs / shred with more of the insides exposed. My favorite part about specs is how easy it is to use just the parts of it that you actually need, but I wanted to go further. For me, the functionality of specs that I needed was really just the entity allocator, a few storage types, MaskedStorage, and the Join system. goggles is just that: the bare minimum pieces that you need to assemble your own ECS system, as independent as I could make them.

*Discussions:
/r/rust_gamedev*

μsfx is a small library built for generating sound effects in code during
runtime. μsfx can be integrated with the `cpal`

and `music`

crates as well as
`SDL2`

crate bindings.

Samples are available on [μsfx’s github readme](https://github.com/tversteeg/usfx) and further
documentation is avialable on the [docs.rs page](https://docs.rs/usfx/0.1.3/usfx/).

This latest version (0.1.3) provides fixes for saw, triangle, and square waves.

[Iced](https://crates.io/crates/iced) is experimental, cross-platform GUI crate focused
on simplicity and type safety.
Iced can be used natively, in a web browser, or can use wgpu,

The new release includes:

- Styling based on trait implementations.
- Event subscriptions that take place asynchronously by using streams.
`Canvas`

widgets, for drawing 2D graphics`PaneGrid`

widgets, which can dynamically organize layout by splitting panes that can be resized.`Svg`

widgets, which can render vector graphics.`ProgressBar`

widgets- Integration into exisiting
`wgpu`

projects. - Options for integrating futures executors into a project.
- TextInput selection
- Texture Atlas support for
`iced-wgpu`


Full docuementation for Iced is available on the [docs.rs page](https://docs.rs/iced/0.1.1/iced/)
as well as examples and how to contribute are available on [iced github repo](https://github.com/hecrj/iced)

[assets_manager](https://crates.io/crates/assets_manager) is a crate that provides convenient loading,
caching, and reloading of external resources. The crate is pay-for-what-you-take,
provides a high level API, and is concurrent.

This newest version provides for hot-reloading, directory-loading (being able to load from a single directory all at once, for extensible games), meta loaders, and various other improvements.

Examples and documentation are available on [assets_manager’s docs.rs](https://docs.rs/assets_manager/0.2.2/assets_manager/)
and additional information about contributing are available on the [github repository](https://github.com/a1phyr/assets_manager)

`gfx-rs`

and `wgpu`

News [#](https://gamedev.rs#gfx-rs-and-wgpu-news)

![hectic screenshot: graveyard and vampires](../../assets/30a9acdfc3b99a82.png)

[hectic-rs](https://github.com/expenses/hectic-rs)- Rust/wgpu/specs re-write of hectic by

[@expenses](https://github.com/expenses)

wgpu-0.5 release happened! See the [changelog](https://github.com/gfx-rs/wgpu/blob/master/CHANGELOG.md#v05-06-04-2020).
It’s based on `gfx-hal-0.5`

(which was covered in the [March newsletter](https://rust-gamedev.github.io/posts/newsletter-008/#gfx-rs-and-wgpu-news)),
uses in-house gfx-extras crates adopted from Rendy,
has many fixes and improvements, and totally changes the way passes are recorded.

`wgpu`

project got restructured by only leaving `wgpu-core`

and `wgpu-types`

in the main (“core logic”) repository.
`wgpu-native`

is moved out into a [separate one](https://github.com/gfx-rs/wgpu-native).
`wgpu-remote`

got fully moved into mozilla-central as “gfx/wgpu_bindings”
(this is “gfx” in a general sense, not gfx-rs in particular).

The Web target (aka “wasm32-unknown-unknown”) is now officially supported
by `wgpu-rs`

! 🎉
@grovesNL wrote the announcement to [gfx-rs blog](https://gfx-rs.github.io/2020/04/21/wgpu-web.html).

At the same time, @kvark was implementing support for WebGPU in Firefox
(Nightly only) with help of `wgpu`

.
They published results of this milestone on [Mozilla Hacks](https://hacks.mozilla.org/2020/04/experimental-webgpu-in-firefox).
The combined efforts allowed all the `wgpu-rs`

examples to be run
in Firefox Nightly on all platforms
(yes, even on Android, terms and conditions apply…).

Given the wide spectrum of uses for `wgpu`

(“core”), it became most important
to be able to debug and reproduce visual issues, be it either the user’s fault,
or wgpu implementations’.
To aid these scenarios, a new [API tracing infrastructure](https://github.com/gfx-rs/wgpu/pull/619)
was built into the core.
It’s now possible to replay user’s `wgpu`

workloads in a separate player
on an entirely different platform.

In gfx-rs land, @mistodon created a nice [series of tutorials](https://www.falseidolfactory.com/projects/learning-gfx-hal)
for the gfx-hal API.

This month [@PsichiX](https://github.com/PsichiX) - creator of the [Oxygengine](https://github.com/PsichiX/Oxygengine) game engine - made
further progress with the Ignite game editor, a hub application for game making
tools for Indie game developers.

-
Code editor and Media player:

![Ignite Code editor and Media player](../../assets/0a561331232e5fc2.gif)

-
Play Mode window to play and test your game directly in the editor:

![Ignite Play Mode window](../../assets/50335c66f2f8745b.jpeg)

-
Additionaly new procedural macro was introduced into Oxygengine, this macro allows to bake information about types that will tell Ignite how to edit data of this types:

![Oxygengine Proc macro](../../assets/6042d6174fc6f0c4.png)


There was an additional work done within Oxygengine ecosystem, which is
[Chrobry](https://gamedev.rs/news/009/chrobry) crate - data driven template engine which is used in Ignite
as part of tool that allows to create new projects from templates provided by
plugins imported into Ignite editor.

If you want to be up to date with Oxygengine ecosystem progress, make sure to
follow project on GitHub and see [Oxygengine Project board](https://gamedev.rs/news/009/oxygengine-project).

![erupt logo](../../assets/e102408dad68baab.png)


[erupt](https://crates.io/crates/erupt) provides bindings to the Vulkan API.

Features include:

- Full Vulkan API coverage
- First-class support for all extensions
- High quality auto-generated function wrappers
- A diverse
`utils`

module - Complete auto-generation of everything except
`utils`

- Function loading
- A high level
`Builder`

for every struct - Type-safe pointer chain support

Just like ash, erupt focuses on exposing good bindings to the *raw* Vulkan API
instead of providing manually written wrappers around it like Vulkano. On top
of this it tries to improve on some features where ash lacks, e.g.
auto-generation, extensions, documentation and utils.

For more information visit [docs.rs](https://docs.rs/erupt) and [GitLab](https://gitlab.com/Friz64/erupt).

![OfficeRL screenshot](../../assets/b26171a283aa7031.png)


[bracket-lib](https://github.com/thebracket/bracket-lib) is a toolkit for creating roguelikes in Rust.
Version 0.8.0 of the library was released this month,
adding many new features and fixes, such as:

- A new input system
- RGBA support, with conversions to RGB and HSV
- Support for bigger Unicode font maps
- A ‘flexible’ terminal with support for floating point positions
- A ‘sprite’ terminal that lets you render sprites wherever you want
- A ‘virtual’ terminal, sections of which can be rendered to other terminals
- Runtime font switching
- OpenGL hooks
- Framerate limiting

Full release notes are available on [/r/rust](https://www.reddit.com/r/rust_gamedev/comments/fz5rb7/bracketlib_work_week_of_4112020_080_has_shipped/).

The author of the library has also published a [new tutorial](https://bracketproductions.com/posts/minituts/spherical_noise/),
showing how you can use simplex noise to generate worlds
[[twitter thread](https://twitter.com/herberticus/status/1252335121258237953)].

In the wider community, DrMelon has published a alpha version of [OfficeRL](https://drmelon.itch.io/officerl),
a roguelike built with bracket-lib that’s set
in an eternally sprawling office complex.

![miniquad logo](../../assets/026c57d49e8b990f.png)

`miniquad`

project got a logo[miniquad](https://github.com/not-fl3/miniquad) is a safe and cross-platform rendering library
focused on portability and low-end platforms support.

This month `miniquad`

-based games got a recommended way to make sounds:
[quad-snd](https://github.com/not-fl3/quad-snd).
Here’s a [WASM demo](https://not-fl3.github.io/miniquad-samples/mixer.html) ([source](https://github.com/not-fl3/quad-snd/blob/master/examples/mixer.rs)).

[good-web-game](https://github.com/not-fl3/good-web-game) now uses [quad-snd](https://github.com/not-fl3/quad-snd) and can run ggez’s [“sounds”](https://github.com/not-fl3/good-web-game/blob/audio/examples/sounds.rs)
example: [WASM demo](https://not-fl3.github.io/miniquad-samples/sounds.html).

`macroquad`

is minimalistic game framework on top of miniquad,
strongly inspired by [raylib](https://www.raylib.com).

This month `macroquad`

’s rendering system got 2D custom cameras support:
[example source](https://github.com/not-fl3/macroquad/blob/master/examples/camera.rs).
Also, `macroquad`

’s UI system now support TTF fonts:
[online demo](https://not-fl3.github.io/miniquad-samples/ui.html), [source](https://github.com/not-fl3/macroquad/blob/master/examples/ui.rs).

[Tetra](https://github.com/17cupsofcoffee/tetra) is a simple 2D game framework, inspired by XNA and [Raylib](https://www.raylib.com).
After a quiet few months, versions [0.3.3](https://twitter.com/17cupsofcoffee/status/1246407935980339200), [0.3.4](https://twitter.com/17cupsofcoffee/status/1249410227935510536)
and [0.3.5](https://twitter.com/17cupsofcoffee/status/1254076418365030400) were all released over the course of April.

Highlights of this month’s updates include:

- New integrations with the OS, such as file dropping and clipboard manipulation
- More utilities for working with mouse and keyboard input
- Enhancements to the animation API
- Various under-the-hood improvements and optimizations

[Tetra’s website](https://tetra.seventeencups.net/) has also had an overhaul,
and is [looking for contributions to the showcase section](https://twitter.com/17cupsofcoffee/status/1255901557322928128).
If you’re working on a project with Tetra, submit an issue or a PR
to the [website repo](https://github.com/17cupsofcoffee/tetra-www) to get it added!

![Melody Madness screenshot](../../assets/7ab5d4ec913cbe6a.png)


[Dathos](https://github.com/BrianMWest/dathos-game-engine) is a simple, extendable 2D game engine built in Rust.
It exposes a Ruby API for writing game/rendering logic,
and a Rust API that allows you to build native extensions for those scripts.

[@resinten](https://twitter.com/resinten/status/1255697868104531968), the author of the engine, has also published
an example game called [Melody Madness](https://github.com/BrianMWest/melody-madness).
Players submit commands via a Slack channel,
trying to write a melody one note at a time.

[Shipyard](https://crates.io/crates/shipyard) is an ECS library built on top of sparse sets.

Main changes:

- Systems are now functions
- Workloads can return errors
`Iterator`

and`IntoIterator`

are supported

-
Early

[WASM support](https://community.amethyst.rs/t/wasm-effort/1336)exists on the.`wasm`

branch- Basic input, audio, and rendering support.
- Online play support through
`WebSocket`

s. - Includes OpenGL support for native applications.

-
by`amethyst_lyon`

[@cuberoo_](https://twitter.com/cuberoo_)provides integration with the.`lyon`

tessellation libraryThis is used as a renderer plugin.

-
[MachineHum](https://github.com/Machine-Hum)shared two videos on his game development ventures:[Compiling Amethyst](https://youtu.be/YVmk82nxahM)for the[GameShell](https://www.clockworkpi.com/).[Making Pokemon Gold](https://youtu.be/oQZnF5dmIjY).


### This Month in Mun [#](https://gamedev.rs#this-month-in-mun)

[Mun](https://mun-lang.org) is a scripting language for gamedev focused on quick iteration times
that is written in Rust.

The Mun Team posted a [technical blog](https://mun-lang.org/blog/2020/05/01/memory-mapping) about how they
implemented hot reloading of structs.

Their [April updates](https://mun-lang.org/blog/2020/05/02/this-month-april) include:

- hot reloading of structs;
- 128-bit integer support;
- improved literal support;
- complete operator support for fundamental types;
- improved documentation;
- bugfixes and improved test coverage.

![A scene rendered with Sarekt](../../assets/2751a4ed9b692b16.png)


[Sarekt](https://github.com/brandonpollack23/sarekt) is a Vulkan-based renderer by Brandon Pollack.

The library has [examples](https://github.com/brandonpollack23/sarekt/tree/master/examples) corresponding
to the steps of vulkan-tutorial.com,
which may be helpful if you want to compare its API with raw Vulkan code.

*Discussions:
/r/rust*

[@hagsteel](https://hagsteel.com)has written a[beginner-friendly tutorial](https://hagsteel.com/posts/godot-rust/)on how to get up and running with Godot and Rust. It’s written with Linux in mind, but should be transferrible to other operating systems [[/r/rust](https://www.reddit.com/r/rust_gamedev/comments/g126es/godot_rust_hagsteel_a_tutorial)].[@hagsteel](https://hagsteel.com)has also written a[blog post](https://hagsteel.com/posts/godot-rust-legion/)with their take on how to use the Legion ECS library with Rust and Godot [[/r/rust](https://www.reddit.com/r/rust_gamedev/comments/g2avzc/using_rust_godot_legion)].[@schr3da](https://www.youtube.com/channel/UC4jYW3lJKrEvOqCQ2ElryGw)has published a series of video tutorials on how Rust can be used effectively with Godot:- Basic Keyboard Controls -
[Part 1](https://youtube.com/watch?v=qEHrRLLYc3Q)and[Part 2](https://youtube.com/watch?v=_Lxr6pAXBsQ) [Debugging GDNative Scripts with LLDB](https://youtube.com/watch?v=aMaT6pyDocg)[File Watching with cargo-watch](https://youtube.com/watch?v=McNgUqzmQkk)- Creating a Simple Platformer -
[Part 1](https://youtube.com/watch?v=SIesTvp_ZD8),[Part 2](https://youtube.com/watch?v=GKIUWbW4G9o)and[Part 3](https://youtube.com/watch?v=_n_5MDEquk4)

- Basic Keyboard Controls -

## Meeting Minutes [#](https://gamedev.rs#meeting-minutes)

[See all meeting issues](https://github.com/rust-gamedev/wg/issues?q=label%3Ameeting) including full text notes
or [join the next meeting](https://github.com/rust-gamedev/wg#join-the-fun).

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

- Beta-test the
[Rust Sokoban Tutorial](https://gamedev.rs/news/009/#rust-sokoban-tutorial); [Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs));[winit’s “Good first issue” and “help wanted” issues](https://github.com/rust-windowing/winit/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+label%3A%22status%3A+help+wanted%22+label%3A%22Good+first+issue%22);[gfx-rs’s “contributor-friendly” issues](https://github.com/gfx-rs/gfx/issues?q=is%3Aissue+is%3Aopen+label%3Acontributor-friendly);[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22);[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22);[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A);[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner);[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22);[A/B Street’s “good first issue” issues](https://github.com/dabreegster/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22);[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue);

## Bonus [#](https://gamedev.rs#bonus)

Just an interesting Rust gamedev link from the past. :)

{{ image_figure( alt=“example” src=“valora-example.jpeg” caption=““dead end” by turnage, 2019“) }}

A few months ago a generative art library [“valora”](https://github.com/turnage/valora)
was released by [@turnage](https://paytonturnage.com).
Features:

- Repeatable works at arbitrary resolutions without changing the work
- Managed rngs for repeatable works and controlled rng trees
- Support for using a different, custom GLSL shader for each vector path
- GLSL live coding with “#include” support
- An ergonomic derive-based GLSL uniforms interface
- Animation support for brainstorming and cumulative pieces

Check out the [guide](https://paytonturnage.gitbook.io/valora) and [gallery](https://paytonturnage.gitbook.io/valora/gallery).

*Discussions:
/r/rust*

That’s all news for today, thanks for reading!

Subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!