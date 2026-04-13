---
title: 'This Month in Rust GameDev #40 - November 2022'
url: https://gamedev.rs/news/040/
author: Rust GameDev WG
published: '2022-12-19'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 40th issue of the Rust GameDev Workgroup’s
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

[Announcements](https://gamedev.rs/news/040/#announcements)[Game Updates](https://gamedev.rs/news/040/#game-updates)[Engine Updates](https://gamedev.rs/news/040/#engine-updates)[Learning Material Updates](https://gamedev.rs/news/040/#learning-material-updates)[Tooling Updates](https://gamedev.rs/news/040/#tooling-updates)[Library Updates](https://gamedev.rs/news/040/#library-updates)[Other News](https://gamedev.rs/news/040/#other-news)[Popular Workgroup Issues in GitHub](https://gamedev.rs/news/040/#popular-workgroup-issues-in-github)[Discussions](https://gamedev.rs/news/040/#discussions)[Requests for Contribution](https://gamedev.rs/news/040/#requests-for-contribution)[Jobs](https://gamedev.rs/news/040/#jobs)

## Announcements [#](https://gamedev.rs#announcements)

### Rust GameDev Meetup [#](https://gamedev.rs#rust-gamedev-meetup)

![Gamedev meetup poster](../../assets/e3641f7442d51cc7.png)


The 21st Rust Gamedev Meetup took place in November. You can watch the recording
of the meetup [here on Youtube](https://youtube.com/watch?v=BS_446HI12I).

The meetups take place on the second Saturday of every month via the
[Rust Gamedev Discord server](https://discord.gg/yNtPTb2) and are also
[streamed on Twitch](https://twitch.tv/rustgamedev).
If you would like to speak at the next meetup, please
[respond to the monthly GitHub issue that will be created](https://github.com/rust-gamedev/meetup#how-to-sign-up-to-speak).

## Game Updates [#](https://gamedev.rs#game-updates)

![Swords, Crates, Grenades, & Mines](../../assets/433bbf5858d51374.png)

[Jumpy](https://github.com/fishfolks/jumpy) ([GitHub](https://github.com/fishfolks/jumpy), [Discord](https://discord.gg/4smxjcheE5), [Twitter](https://twitter.com/spicylobsterfam)) by
[Spicy Lobster](https://spicylobster.itch.io) is a pixel-style, tactical 2D shooter with a fishy
theme.

In the last month, Jumpy migrated from a client-server networking model to a P2P
Rollback model using [GGRS](https://github.com/gschup/ggrs). This was to address shortcomings with the server
model that had been implemented, and to take advantage of the excellent
user experience that rollback networking can offer.

The rollback model did come with the new requirement to run up to 8 simulation frames per 16ms screen refresh, though, and unfortunately the JavaScript bindings used to implement the game items were not performant enough to keep up. For now, scripting has been temporarily disabled.

This sparked a quick migration of the TypeScript files to Rust, and also
[a discussion](https://github.com/fishfolk/jumpy/discussions/489) about future possibilities for using WASM to
get better determinism and rollback performance, along with lower-overhead WASM
scripts.

With promising ideas for future improvements, the rest of the month was spent focusing on getting the initial items completed, with Grenades, Swords, Crates, and Mines all landing recently.

With just one more item planned and minimal clean up work, an MVP release is just around the corner!

![At the Abyss](../../assets/3f93bf416abe7698.png)

CyberGate ([YouTube](https://youtube.com/channel/UClrsOso3Xk2vBWqcsHC3Z4Q), [Discord](https://discord.gg/R7DkHqw7zJ)) by CyberSoul is an
ambitious endeavor to create an immersive universe experience with the power of
artificial intelligence and procedurally generated gameplay styles. Explore a
world filled with strange creatures and thrilling adventures!

The latest updates include:

- A new islands map featuring a safe zone and progressively more challenging levels.
- Collectible Cubic Orbs that provide health, points, and bullets.
- An intuitive interface for day cycle, inventory (bullets), and cooldowns.
- Upgrade your stats as you level up.
- And an Emergency Recall feature for when you’re stranded.

Be among the first to experience the wonders of AI-driven universe with
CyberGate! [Join the Discord server](https://discord.gg/R7DkHqw7zJ) to participate in
the upcoming Phase 7.0!

### Rusty Vangers [#](https://gamedev.rs#rusty-vangers)

![Vange-rs rendered with a voxel tree](../../assets/3e5f7c87783caf58.jpg)


[Rusty Vangers](https://vange.rs) ([GitHub](https://github.com/kvark/vange-rs), [Itch-io](https://kvark.itch.io/vangers)) is an
experimental re-implementation of the [Vangers](https://store.steampowered.com/app/264080/Vangers) game,
using GPUs and multi-threading in Rust.

The project has started with a strong focus on rendering, since efficient GPU implementation of a Voxel world as large as 2048x16384x256 (that’s about 8 giga-voxels!) turned into a tough challenge, even though the original game from 1998 easily does it on CPU.

Finally, after years of experiments, a method has been implemented
that is fast and universal when it comes to viewing angles. It’s based
on an acceleration structure in the form of a voxel octree.
This work has landed at the start of November, and now it’s possible
to [ride through](https://vimeo.com/manage/videos/765602608) the strange worlds
while looking from behind the car, or even from inside it.

This method runs on all APIs (including OpenGL!), thanks to wgpu/naga portability. It’s suitably fast, regardless of perspective, even on an old macBook with an integrated GPU. It concludes the rendering story of the project, and the devs can shift focus on other areas.

*Discussions:
/r/rust_gamedev*

### Digital Extinction [#](https://gamedev.rs#digital-extinction)

![laser trail in Digital Extinction](../../assets/ab60d9237e323fe5.jpeg)

[Digital Extinction](https://de-game.org) ([GitHub](https://github.com/DigitalExtinction/Game), [Discord](https://discord.gg/vHMFuCWGSX),
[Reddit](https://reddit.com/r/DigitalExtinction)) by [@Indy2222](https://github.com/Indy2222) is a 3D real-time strategy game made with
[Bevy](https://bevyengine.org).

Here is the summary of the changes since the last update. It consists of commit range ffd5987..494096b (2022-11-03-2022-11-27). There were 75 non-merge commits in total.

The most notable updates are:

- trails after laser fires are briefly visible,
- flying drones no longer slide on terrain but fly in height,
- simple main menu and map selection were added,
- a game design document was kicked off,
- both Rust API, and other technical documentation are automatically published
at
[docs.de-game.org](https://docs.de-game.org), - many community-related improvements have been made,
- the game was migrated to the new Bevy v0.9,
- there were some code quality and performance improvements,
- de_tools crate was fixed.

A more detailed update summary is available [here](https://mgn.cz/blog/de02).

![In-game screenshot of a player pointing a laser gun.](../../assets/6be14abc7bc6b97f.png)


[Space Frontiers](https://github.com/starwolves/space) ([GitHub](https://github.com/starwolves/space), [Discord](https://discord.gg/yYpMun9CTT), [Twitter](https://twitter.com/starwolvesstar), [Reddit](https://reddit.com/u/StarwolvesStar), [Steam Group](https://steamcommunity.com/groups/starwolvescommunity))
by [Star Wolves](https://starwolves.io) is an online sci-fi action community RPG game simulating
space (and spaceships) in 3D.

The game has been in-development for over two years.
The server and client were successfully prototyped with Godot several
years ago. After that, the server, with all its features, was
successfully ported to [Bevy](https://bevyengine.org). The client is now getting the same
porting treatment!

The project is commercial, [open-source](https://github.com/starwolves/space) and has a proprietary license.
There is a milestone for a license change to free open-source.

Space Frontiers seeks to deliver customized community gameplay experiences.
Read more about plugins and content customization in the [development journal](https://starwolves.io/showthread.php?tid=1).

The official StarWolves.io forum and discussion board were launched a week ago. The first 50 registrants will receive a permanent unique forum group/title.

![Screenshot of Timely Defuse, featuring a chubby hero disarming a bomb. Dynamites are scattered about. “WAVE 5” and a score of 199 appear at the top.](../../assets/30da11a51a65014a.png)


[Timely Defuse](https://e-net4.itch.io/timely-defuse) ([GitHub](https://github.com/Enet4/timely-defuse)) by [@E_net4](https://hachyderm.io/@E_net4)
is a mobile Web game using Bevy, submitted to GitHub Game Off 2022.
In this game, explosives are coming out of nowhere
and it’s the hero’s job to stop as many of them from exploding as possible.

Some remarks about the experience of creating Timely Defuse
were shared on [Dev.to](https://dev.to/e_net4/timely-wrap-up-quick-notes-on-timely-defuse-441o).

![Screenshot of Spaceviata, showing the galaxy with some stars discovered and the game UI.](../../assets/c26f3795284554fb.png)


[Spaceviata](https://vleue.itch.io/spaceviata) ([GitHub](https://github.com/mockersf/spaceviata)) by [@FrancoisMockers](https://hachyderm.io/@FrancoisMockers)
is a strategy game made with [Bevy](https://bevyengine.org), submitted to GitHub Game Off 2022.

Starting with one star, your goal in this turn-by-turn game is to conquer the galaxy, fighting against AI players, and balancing exploration with colonization to avoid stretching your resources too thin.

[Scummstreets](https://ratwizard.dev/dev-log/scummstreets) is a new multiplayer online role-playing game by [@dooskington](https://twitter.com/dooskington).
The game is a fork/sequel to [Antorum Isles](https://antorum.ratwizard.dev), so the game server is written in Rust,
and the official client is made with Unity. It’s still in a pre-alpha state.

There was one dev log published this month:

![UI preview](../../assets/348bd6ece48c6e45.png)

[@ThousandthStar](https://github.com/ThousandthStar) is creating an 8bit themed multiplayer game. It’s a turn-based
strategy game and is currently under development. This month, the
[blog](https://thousandthstar.github.io) got moved from [dev.to](https://dev.to/thousandthstar) to ThousandthStar’s own
blog on GitHub.

The game is soon getting a UI, and more packets need to be implemented before
the game is ready to play. ThousandthStar is excited for the game to be
playable, but it will probably take some time, since he is doing it as a side
project when he has some time. The game is lacking troop spawns, a turn system,
and some more troops! Any and all ideas posted to the
[r/rust_gamedev](https://reddit.com/r/rust_gamedev/comments/ylksma/thousandthstars_multiplayer) thread are greatly appreciated.

If possible, ThousandthStar would like the art to be made up of voxel models instead of just pixel art, but he doesn’t know if he’ll reach that point yet.

*Discussion: r/rust_gamedev*

![A riverside](../../assets/49c8b0847db59f4d.jpeg)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

Doors were worked on, and now they open more consistently in a single direction.
There is ongoing work to add train tracks to the world, as well as train
stations in villages. A talk about Veloren was given at the Rust and Cpp Cardiff
Meetup, which [you can watch here](https://youtube.com/watch?v=bT2SeYXpQm8).

Work was done on minotaurs to improve their attacks. A new dungeon type, adlet, is being worked on. Bird animations are also having some work done. Houses are seeing an uplift with some tests being done. In December, Veloren will be hosting a Christmas event in the second half of the month.

November’s full weekly devlogs: “This Week In Veloren…”:
[#197](https://veloren.net/devblog-197),
[#198](https://veloren.net/devblog-198),
[#199](https://veloren.net/devblog-199).

![top view on lots of machinery and belts](../../assets/a7506e0493807152.jpg)


[Combine&Conquer](https://martinbucksoftware.itch.io) ([Steam](https://store.steampowered.com/app/2220850/Combine_And_Conquer)) by [Martin Buck](https://github.com/I3ck)
is a WIP multi-planetary automation game similar to Satisfactory or Factorio.
[This month’s updates](https://buckmartin.de/combine-and-conquer/2022-11-22-v0.3.0.html) include:

- Reworked belts/arms/assemblers,
- modules improvements,
- structure tiers additions,
- color palettes,
- UI and planet visuals improvements.

Also, [check out a cool video](https://reddit.com/r/rust_gamedev/comments/yk9onb/the_two_year_development_progress_of_my) with the progress of the project
over two years of development.

## Engine Updates [#](https://gamedev.rs#engine-updates)

[pixel_engine](https://github.com/Maix0/pixel_engine) by [@Maix0](https://github.com/Maix0) is a 2D game engine that started as a Rust-version
of olcPixelGameEngine (written in C++). It was used as a learning project
for Maix0, where he worked on it for over 3 years.

This engine has a very straightforward API and is mostly CPU based (the exception is Decals which are GPU-sprites) but it can achieve some things. Use it as a way to learn new algorithms or to make a simple game.

It uses [wgpu](https://wgpu.rs) underneath so there is support for all desktop targets and WASM
(even though there is a bug in the WASM builds
where the keyboard layout is only QWERTY).

The most recent addition is the [SpriteRef](https://docs.rs/pixel_engine/0.6.0/pixel_engine/graphics/struct.SpriteMutRef.html), a way to create a view
inside a sprite where it is possible to draw in it.
You can have multiple non-overlapping views at the same time.

![Animation Editor](../../assets/5ed8cc6959a51ce6.png)


[Fyrox](https://github.com/FyroxEngine/Fyrox) ([Discord](https://discord.com/invite/xENF5Uh), [Twitter](https://twitter.com/DmitryNStepanov)) is a game engine that
aims to be easy to use and provide a large set of out-of-the-box features. In November
it got a lot of new functionality and improved existing:

- Major animation system rework
- New animation editor
- Reworked animation blending state machine editor
- Major improvements to the curve editor widget
- Curve-based animation system
- Smart placement mode for move gizmo
- Node and property selectors
- Better WebAssembly support - asynchronous scene loading and WASM project template
- Various improvements for project template generator
- Lots of bug fixes

![bevy bloom lion](../../assets/a8fc3fd5539da6b1.jpeg)


[Bevy](https://bevyengine.org) is a refreshingly simple data-driven game engine built in Rust.
It is [free and open source](https://github.com/bevyengine/bevy) forever!

Bevy 0.9 brought many incredible new features.
You can check out the [full release blog post here](https://bevyengine.org/news/bevy-0-9),
but here are some highlights:

[HDR Post Processing, Tonemapping, and Bloom](https://bevyengine.org/news/bevy-0-9/#hdr-post-processing-tonemapping-and-bloom)[FXAA](https://bevyengine.org/news/bevy-0-9/#fxaa-fast-approximate-anti-aliasing)[Deband Dithering](https://bevyengine.org/news/bevy-0-9/#deband-dithering)[Other Post Processing Improvements](https://bevyengine.org/news/bevy-0-9/#post-processing-view-target-double-buffering)[New Scene Format](https://bevyengine.org/news/bevy-0-9/#new-scene-format)[Code Driven Scene Construction](https://bevyengine.org/news/bevy-0-9/#dynamic-scene-builder)[Improved Entity/Component APIs](https://bevyengine.org/news/bevy-0-9/#improved-entity-component-apis)[Exclusive System Rework](https://bevyengine.org/news/bevy-0-9/#exclusive-system-rework)[Enum Reflection](https://bevyengine.org/news/bevy-0-9/#enum-reflection)[Time Shader Globals](https://bevyengine.org/news/bevy-0-9/#time-shader-globals)[Plugin Settings](https://bevyengine.org/news/bevy-0-9/#plugin-settings)[Bevy UI Z-Indices](https://bevyengine.org/news/bevy-0-9/#bevy-ui-z-indices)

*Discussions:
/r/rust,
Hacker News,
Twitter*

![godot-rust GDExtension](../../assets/1e8e742b8aeb39e8.png)


godot-rust ([GitHub](https://github.com/godot-rust/gdextension), [Discord](https://discord.gg/aKUCJ8rJsc), [Twitter](https://twitter.com/GodotRust))
is a Rust library that provides bindings for the Godot engine. Just this month,
a [Mastodon account](https://mastodon.gamedev.place/@GodotRust) was opened to share development info.

November brings the long-awaited GDExtension binding, enabling access to Godot 4 features from Rust. Still in an early experimental phase, it is already possible to run smaller examples like Godot’s famous Dodge-the-Creeps tutorial game.

Compared to the GDNative binding, APIs are a bit simpler now:

- One central
`Gd<T>`

pointer combining`Ref`

/`Instance`

and their type-states - Self-registering classes:
`#[derive(GodotClass)]`

and you’re good-to-go - Less
`unsafe`

, less`unwrap()`

, more runtime checks

The repository is available at [godot-rust/gdextension](https://github.com/godot-rust/gdextension), while the
current development status is tracked in [#24](https://github.com/godot-rust/gdextension/issues/24). The [book](https://github.com/godot-rust/book) as
well as documentation are still under construction.

![Defold logo](../../assets/75e8338773abdc3a.png)


[@JustAPotota](https://github.com/JustAPotota) is working on rusty bindings for the [Defold](https://defold.com) engine
and [has started a thread about this on Defold’s forum](https://forum.defold.com/t/writing-native-extensions-in-rust/71980)
where you can fond all more info and updates.

The project is split up into a few different parts:

[defold-rs](https://github.com/JustAPotota/defold-rs)- Rust bindings to dmSDK and test project for new bindings[defold-rs-extender](https://github.com/JustAPotota/defold-rs-extender)- Custom build server[defold-rs-template](https://github.com/JustAPotota/defold-rs-template)- Rust port of the native extension template

It works the same way as regular C/C++ extensions: everything is done on the build server and you only need the standard Defold editor to build games. <…>

These extensions are full Cargo projects. The main benefit being that you can use any of the Rust libraries on crates.io in your Defold game just by listing them in your Cargo.toml. Theoretically, you could even write a game with the Bevy game engine and embed it into a Defold project!


Note that the project is in an early stage: only bundling for Windows and Linux is currently supported, you must host your own build server and it provides no sandboxing or security against malicious extensions.

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

![Floating bananas and cubes with stony texture](../../assets/a6b2aa0f8e2e8c36.jpg)


[@whoisryosuke](https://mastodon.gamedev.place/@whoisryosuke) wrote [a blog post](https://dev.to/whoisryosuke/render-pipelines-in-wgpu-and-rust-2dh3)
on how to parse #GLTF files in Rust, render them using WebGPU,
and play animations imported from Blender!

![Youtube preview: bevy logo, rapier logo and a piece of Rust code](../../assets/4c9a02bd6401e8dd.jpg)


[Matthew Bryant](https://youtube.com/@logicprojects) released [a video](https://youtube.com/watch?v=GwlZ5EPu8l0)
with a broad overview of some of the core features and organization
of the [Rapier](https://rapier.rs) physics engine’s [Bevy plugin](https://github.com/dimforge/bevy_rapier).

![Embark’s logo: title and a person in space helmet](../../assets/05475ef26710798e.jpg)


[@repi](https://mastodon.gamedev.place/@repi) shared [some internal guidelines](https://gist.github.com/repi/d98bf9c202ec567fd67ef9e31152f43f) about how they
look into and evaluate health & quality of Rust crates
at [Embark Studios](https://embark.dev).

note: I wrote this for our internal documentation & guidelines at Embark so not all of it is likely relevant for other companies, but sharing here as others expressed interest in seeing it

these are not exact rules but things to consider, esp. for adding dependencies for long term use in large Rust project in production.

our project is ~500k LoC and uses ~700 crates, so some care and active gardening is in needed. which is why we (read: @ca1ne) also built

`cargo-deny`

and`cargo-about`

early on and use it heavily.

[@jntrnr](https://jntrnr.com) made a [video overview of the guide](https://youtube.com/watch?v=4sZTcBg50wc).

## Tooling Updates [#](https://gamedev.rs#tooling-updates)

Boytacean ([GitHub](https://github.com/joamag/boytacean), [Working Emulator](https://boytacean.joao.me))
by [@joamag](https://github.com/joamag) is a Game Boy emulator written in Rust
with both Native (using SDL) and Web (using WebAssembly) frontends that has been
created as a learning experiment to better understand both Rust capabilities and
Game Boy hardware.
The Web frontend is especially interesting making use of Web standards like
[Gamepad API](https://developer.mozilla.org/docs/Web/API/Gamepad_API/Using_the_Gamepad_API) to provide a rich and joyful experience for both
desktop and mobile devices.
Performance wise the web version runs smoothly with little to no significant
hardware requirements.

Even though Boytacean supports most Game Boy games and passes most well-known test ROMs there are still some features lacking like support for Game Boy Color and APU (sound) support.

You can check this [Reddit post](https://reddit.com/r/rust/comments/ywxugc/game_boy_emulator_using_rust) for more information.

![Graphite logo](../../assets/1a40a3a053b77366.png)


Graphite ([website](https://graphite.rs), [GitHub](https://github.com/GraphiteEditor/Graphite),
[Discord](https://discord.graphite.rs), [Twitter](https://twitter.com/GraphiteEditor)) is a free,
in-development raster and vector 2D graphics editor based around a Rust-powered
node graph compositing engine.

November’s [sprint 20](https://github.com/GraphiteEditor/Graphite/milestone/20) introduces:

- Filling in the blanks: The Imaginate tool gains Inpaint/Outpaint, letting
users
[replace content](https://youtube.com/watch?v=Ck2R0yqTLcU&t=3269)in masked areas and even[“uncrop”](https://youtube.com/watch?v=Ck2R0yqTLcU&t=3862s)entire images, powered by[Stable Diffusion](https://en.wikipedia.org/wiki/Stable_Diffusion). - Going native: Graphite is now available as a desktop app, thanks to Tauri. The app now has access to system resources like rustc and the GPU, which lets it compile and run node graph effects as SPIR-V compute shaders in Vulkan for hardware-accelerated rendering.
- Connecting the dots: The node graph compositor now
[supports interactive editing](https://youtube.com/watch?v=Ck2R0yqTLcU&t=4332), so users can drag nodes and chain together effects. Nodes can be set in the Properties panel or exposed as inputs in the graph.

It’s easy to get involved with the project by developing new nodes. Join the
project [Discord](https://discord.graphite.rs) and ask how to begin.

Stay tuned for the imminent Alpha Milestone 2 release and progress converting existing features into nodes.

Open the [Graphite editor](https://editor.graphite.rs) in your browser to give it a try
and share your creations with #MadeWithGraphite on Twitter.

## Library Updates [#](https://gamedev.rs#library-updates)

![bevy_atmosphere collage: colored skies](../../assets/341a521117ddabf6.png)


bevy_atmosphere ([crates.io](https://crates.io/crates/bevy_atmosphere),
[docs.rs](https://docs.rs/bevy_atmosphere/latest/bevy_atmosphere/),
[GitHub](https://github.com/JonahPlusPlus/bevy_atmosphere))
is now compatible with Bevy 0.9.

The focus of this update was decoupling the atmospheric model from the
compute pipeline. What this means is that users can choose a different model
or create their own using the `Atmospheric`

trait. This sets the groundwork for
having a variety of models to choose from, each for a different type of game.

With the removal of the `Atmosphere`

resource, comes the addition of the
`AtmosphereModel`

resource and the `Nishita`

and `Gradient`

models. `Nishita`

is the same model that was used in the previous version of bevy_atmosphere.
`Gradient`

is a new model that provides a simple gradient of three colors,
making it ideal for stylized games.

There is also the `Atmosphere<T>`

and `AtmosphereMut<T>`

system params,
which can be used to work with a particular model
without having to cast it from `AtmosphereModel`

.

If you want to read more about the technical changes, check out the developer’s
[blog post](https://jonahplusplus.dev/2022/12/01/bevy_atmosphere_0.5.html)!

*Discussions:
/r/rust_gamedev,
/r/bevy,
/r/rust*

![Bevy sequential actions simple demo](../../assets/0314efb4d32a6507.gif)

`bevy-sequential-actions`

([GitHub](https://github.com/hikikones/bevy-sequential-actions), [docs.rs](https://docs.rs/bevy-sequential-actions))
is a simple helper library for the [Bevy](https://bevyengine.org) game engine.
It aims to execute a queue of various actions in a sequential manner.

An action is anything that implements the `Action`

trait,
and can be added to any `Entity`

that contains the `ActionsBundle`

.
In the image above, the following actions have been added:

```
commands
.actions(entity)
.config(AddConfig {
order: AddOrder::Back,
start: true,
repeat: Repeat::Forever,
})
.add(WaitAction::new(1.0))
.add(MoveAction::new(Vec3::X * 2.0))
.add(WaitAction::new(1.0))
.add(MoveAction::new(Vec3::X * -2.0));
```


With version `0.6`

comes the ability to
add a collection of actions that run in parallel.
This means that all actions will start and stop at the same time,
as the whole collection is treated as “one action”.
In other words, the action queue will only advance
when all actions in the collection are finished.

```
commands
.actions(agent)
.add_many(
ExecutionMode::Parallel,
actions![
action_a,
action_b,
action_c,
]
);
```


[Sparsey](https://github.com/LechintanTudor/sparsey) by [@LechintanTudor](https://github.com/LechintanTudor) is an Entity Component System focused on
flexibility, conciseness and providing features exclusive to its sparse
set-based implementation.

The latest release takes advantage of the newly added Generic Associated Types to provide a uniform interface for running systems, functions and closures that borrow data from World and Resources, via the “run”, “run_locally” and “run_exclusive” functions.

Example:

```
let heaviest = sparsey::run(&world, &resources, |weights: Comp<Weight>| {
(&weights)
.iter()
.with_entity()
.max_by_key(|(_entity, &weight)| weight)
.map(|(entity, _weight)| entity)
});
```


![Bevy Quickmenu simple menu demo](../../assets/9df59450ffca3221.gif)


bevy_quickmenu ([crates.io](https://crates.io/crates/bevy_quickmenu),
[docs.rs](https://docs.rs/bevy_quickmenu), [GitHub](https://github.com/terhechte/bevy_quickmenu)) allows quickly
creating nested game menus that can be navigated with keyboard, gamepad or
mouse.

Bevy Quickmenu builds on BevyUI and allows defining nested menu structures in a super simple way. Its also very extensible and customisable. If you game needs menus and you would like to support multiple input methods, give it a try.

For example, a simple vertical menu can be defined like this:

```
fn root_menu(state: &CustomState) -> Menu<Actions, Screens, CustomState> {
Menu::new(
"root",
vec![
MenuItem::image(state.logo.clone()),
MenuItem::headline("Menu"),
MenuItem::action("Start", Actions::Close),
MenuItem::screen("Sound", Screens::Sound)
.with_icon(MenuIcon::Sound),
MenuItem::screen("Controls", Screens::Controls)
.with_icon(MenuIcon::Controls),
],
)
}
```


For a more involved example, check out [this definition of a settings screen
with control device selection and a sound menu](https://github.com/terhechte/bevy_quickmenu/blob/main/examples/settings.rs).
[Version 0.1.5](https://github.com/terhechte/bevy_quickmenu/releases/tag/0.1.5) was just released which simplifies
generics and makes it easier to create dynamic menus.

*Discussion:
/r/rust_gamedev*

![notan examples](../../assets/c75ac69c4269dade.gif)


[Notan](https://github.com/Nazariglez/notan) is a simple abstraction layer that provides cross-platform windowing,
input, audio, graphics and other features, in an ergonomic manner without
enforcing any structure or pattern and treating WebAssembly as a first-class citizen.

The version [v0.8](https://github.com/Nazariglez/notan/releases/tag/v0.8.0) is one of the biggest releases, adding several improvements
in the drawing APIs and fixes and improvements in some other features like the
clipboard support.

You can check the [demos](https://nazariglez.github.io/notan-web) online and read more about the changes on the [changelog](https://github.com/Nazariglez/notan/blob/main/CHANGELOG.md).

[Bevy Hikari](https://github.com/cryscan/bevy-hikari) v0.3 [#](https://gamedev.rs#bevy-hikari-v0-3)

![bevy-hikari screenshot](../../assets/fd916656fe9f82ca.jpeg)

`bevy-hikari`

([crates.io](https://crates.io/crates/bevy-hikari), [docs.rs](https://docs.rs/bevy-hikari),
[GitHub](https://github.com/cryscan/bevy-hikari)), a path tracing renderer for [Bevy](https://bevyengine.org), is now compatible
with the 0.9 version of the engine.

In recent updates, the renderer implements light BVH, which allows faster and more accurate multiple emissive sampling. It also features a spatial upscaler based on FSR 1.0 and a temporal upscaler based on SMAA Tu4x, making it more affordable for median end devices.

![Bevy vfx bag gif](../../assets/9ba99945b7a2892b.gif)

`bevy-vfx-bag`

([GitHub](https://github.com/torsteingrindvik/bevy-vfx-bag), [docs.rs](https://docs.rs/bevy-vfx-bag/0.1.0/bevy_vfx_bag))
is a visual effects library for the [Bevy](https://bevyengine.org) game engine.

It had its initial 0.1.0 release aligned with Bevy’s recent 0.9.0 release. Each effect has a plugin and effects are applied in order:

```
// Shows an example of adding three post processing effects:
app
.add_plugin(BevyVfxBagPlugin) // Always needed
.add_plugin(RaindropsPlugin) // Shows rain on-screen
.add_plugin(ChromaticAberrationPlugin) // Skews color channels
.add_plugin(LutPlugin) // Allows using a look-up table to remap colors for
// having a specific "feel" to your game
.run();
```


The camera which receives these effects is marked as such:

```
commands
.spawn(Camera3dBundle { ... })
.insert(PostProcessingInput) // Marks this camera for post processing usage
```


Effect settings can be changed at runtime:

```
fn update(time: Res<Time>, mut ca: ResMut<ChromaticAberration>) {
// Make the red color channel skew in a sinusoidal fashion
ca.magnitude_r = time.elapsed_seconds().sin();
}
```


The GitHub repository has examples and videos for all effects.

A complete rework of the plugin is underway for version 0.2.0, where the main goal is to align with and use Bevy’s render graph features, including the new post processing double buffering feature which arrived in 0.9.0.

![Eight animated sprites with various configurations](../../assets/e3cbdc82e7a68bf0.gif)


`seldom_pixel`

([GitHub](https://github.com/Seldom-SE/seldom_pixel), [Video Demo](https://youtu.be/pmTPdGxYVYw))
by [Seldom](https://github.com/Seldom-SE) is a Bevy plugin for limited color palette pixel art games,
with features for filters, animations, typefaces, particle emitters,
`bevy_ecs_tilemap`

integration, and much more.

In November, `seldom_pixel`

received its 0.1 and 0.1.1 releases for Bevy 0.8.
Its `main`

branch supports Bevy 0.9, but depends on a particular
`bevy_ecs_tilemap`

commit.

*Discussions:
Twitter*

![example app: a manu with hayak’s logo, title and 3 buttons: play, options, quit](../../assets/8e4f7869457c303b.png)


[Kayak UI](https://github.com/StarArawn/kayak_ui) is a WIP declarative UI that features:

- Easy to use declarative syntax using a custom proc macro.
- Fast and accurate layouts using
[morphorm](https://github.com/geom3trik/morphorm). - Style system built to kind of mimic CSS styles.
- Image and Nine patch rendering.

There’s also [a book](https://github.com/StarArawn/kayak_ui/blob/main/book/src/SUMMARY.md) that covers the basic concepts;

![A design demo application showcasing widgets and theming capabilities](../../assets/d9888c8244f0a986.png)

[Iced](https://github.com/hecrj/iced) is an experimental cross-platform GUI library focused on simplicity and
type-safety, inspired by Elm.

This month’s [v0.5 release](https://github.com/iced-rs/iced/pull/1520) features include:

- Stabilization of stateless widgets: the old widget API has been completely
replaced by stateless widgets. Alongside the new API, there are a bunch
of new helper functions and macros for easily describing view logic
(like
`row!`

and`column!`

). - First-class theming: a complete overhaul of the styling primitives, introducing a Theme as a first-class concept of the library.
- Widget operations: an abstraction that can be used to traverse (and operate on) the widget tree of an application in order to query or update some widget state.
- Lazy widget that can call some view logic only when some data has changed.
- The Canvas widget can draw linear gradients now.
- Touch support for Canvas.
- iced_glow now is capable of rendering both the Image and Svg widgets.

Finally, and deserving a special mention,

[System76 has decided to use iced]instead of GTK for Pop!_OS’ desktop environment! This is one of the most important adoption events since the inception of the library. The engineers at[System76]are already contributing a bunch of great improvements to iced, as well as breaking ground in long-standing issues that could benefit the whole GUI ecosystem in Rust (like proper text rendering!).

*Discussions: /r/rust*

## Other News [#](https://gamedev.rs#other-news)

- Other game updates:
- A free open beta on
[Yomi Hustle](https://ivysly.itch.io/your-only-move-is-hustle)- an online turn-based fighting game and superpowered fight scene simulator by[Ivy Sly](https://twitter.com/ivy_sly_)- has begun! [@johann](https://mastodon.gamedev.place/@johann)shared a couple of Idu screenshots with[dynamic global illumination](https://mastodon.gamedev.place/@johann/109355219994971392)and[a video of stress-testing the framerate](https://youtube.com/watch?v=yyicR63hZ0o)with the whole map full of vegetation.[@crispy_dev posed a video](https://youtube.com/watch?v=QvBinznAYqY)about making a roguelike from scratch in Rust.[@devildahu](https://devildahu.ch)posted[two](https://devildahu.ch/devlog/gba-c-to-rust)[gssa-2](https://devildahu.ch/devlog/gba-c-to-rust-2)about rewriting[“Generic Space Shooter Advance”](https://github.com/devildahu/gssa-rs)GBA game in Rust.[@Kane_rogers](https://twitter.com/Kane_rogers)shared[a video of the latest iteration of The Station](https://youtube.com/watch?v=C8XzNnhELtk)VR survival game being build with the[Hotham](https://github.com/leetvr/hotham)engine.- @Tantan shared video devlogs about
[improving combat feel](https://youtube.com/watch?v=54D6hgui2Kc)and working on[a multiplayer networking architecture](https://youtube.com/watch?v=EFzFHrzIiz8)of his voxel game.

- A free open beta on
- Other engine updates:
[Anthony Utt](https://twitter.com/alkimia_studios)has recently converted the WIP[Alkahest](https://github.com/AlkimiaStudios/alkahest-rs)engine from C++ to Rust and[released a vlog](https://youtube.com/watch?v=OtX_8MD--fc)about it and its UI render specifically.[@markusmoenig](https://github.com/markusmoenig)has published[the first public pre-release build](https://eldiron.com/blog/prerelease)of[Eldiron](https://eldiron.com)- a cross-platform RPG engine that draws heavily on the earlier Ultima games for inspiration.

- Other tooling updates:
[@Setzer22](https://mastodon.gamedev.place/@Setzer22)shared a couple of posts with feature previews for the next[Blackjack](https://github.com/setzer22/blackjack)release:[copy&paste](https://mastodon.gamedev.place/@Setzer22/109352818515866403),[an examples folder with annotated graphs](https://mastodon.gamedev.place/@Setzer22/109360242068079618),[gizmos](https://mastodon.gamedev.place/@Setzer22/109377500780164246), and[face selection](https://mastodon.gamedev.place/@Setzer22/109381333034474452).[@eurigilberto shared a video](https://mastodon.gamedev.place/@EuriHerasme/109368645008002886)of a cool little VR terrain generation app made using Rust and WebGL.

- Other library updates:
[Taffy UI v0.2](https://tech.lgbt/@alice_i_cecile/109399333226449807)brings improved flexbox and significant performance improvements[kopi](https://github.com/hasenbanck/kopi)by[@hasenbanck](https://github.com/hasenbanck)is a small abstraction to easily and safely embed an ECMAScript runtime inside a Rust based application.[dynec](https://github.com/SOF3/dynec)by[@SOF3](https://github.com/SOF3)is a statically archetyped opinionated ECS-like framework.[guiedit](https://github.com/aleokdev/guiedit)by[@aleokdev](https://github.com/aleokdev)is a WIP library for easily adding a developer GUI to any graphical application.[bevy_tweening v0.6](https://github.com/djeedai/bevy_tweening/blob/main/CHANGELOG.md#060---2022-11-15)features Bevy v0.9 support, new Duration-based elapsed API, better looping control with RepeatCount/RepeatStrategy, and fixed change detection[dungeon-generator](https://github.com/MoutonSanglant/dungeon-generator)by[@MoutonSanglant](https://github.com/MoutonSanglant)is a naive dungeon generator for rogue-like games, mostly done for education purposes.[leafwing_input_playback](https://github.com/Leafwing-Studios/leafwing_input_playback)by[@alice-i-cecile](https://github.com/alice-i-cecile)is an input recording and playback library for the[Bevy](https://bevyengine.org)game engine.


## Popular Workgroup Issues in GitHub [#](https://gamedev.rs#popular-workgroup-issues-in-github)

## Discussions [#](https://gamedev.rs#discussions)

- /r/rust_gamedev:

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[‘Are We Game Yet?’ wants to know about projects/games/resources that aren’t listed yet](https://github.com/rust-gamedev/arewegameyet#contribute).[Graphite is looking for contributors](https://graphite.rs/contribute)to help build the new node graph and 2D rendering systems.[winit’s “difficulty: easy” issues](https://github.com/rust-windowing/winit/issues?q=is%3Aopen+is%3Aissue+label%3A%22difficulty%3A+easy%22).[Backroll-rs, a new networking library](https://github.com/HouraiTeahouse/backroll-rs/issues).[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[A/B Street’s “good first issue” issues](https://github.com/a-b-street/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/D-Good-First-Issue).

## Jobs [#](https://gamedev.rs#jobs)

-
[DIMS](https://dims.co)(Stockholm, Sweden) is building a Rust game engine and creation platform dedicated to creating large multiplayer open-world games and[has a lot of open positions](https://dims.co/career), including Game Engine Programmer:Come build a game engine and creation platform from scratch in Rust! It’s got everything: game-like collaborative building, networking by default, procedural worldbuilding, WebAssembly for scripting, WebGPU for graphics, and community-driven co-creation.

You can find all of the details in

[their job offer page](https://linkedin.com/jobs/view/3378931463). -
Ultimate Games (London, UK)

[is looking for Mid-to-Senior level Rust Graphics engineer](https://linkedin.com/jobs/view/senior-graphics-engineer-at-ultimate-games-3399850617).

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!

**Discuss this post on**:
[/r/rust_gamedev](https://reddit.com/r/rust_gamedev/comments/zqeq8i/rust_gamedev_40),
[Mastodon](https://mastodon.gamedev.place/@rust_gamedev/109544178943651668),
[Twitter](https://twitter.com/rust_gamedev/status/1605061212911403008),
[Discord](https://discord.gg/yNtPTb2).