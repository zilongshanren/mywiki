---
title: 'This Month in Rust GameDev #41 - December 2022'
url: https://gamedev.rs/news/041/
author: Rust GameDev WG
published: '2023-01-28'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 41st issue of the Rust GameDev Workgroup’s
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

[Announcements](https://gamedev.rs/news/041/#announcements)[Game Updates](https://gamedev.rs/news/041/#game-updates)[Engine Updates](https://gamedev.rs/news/041/#engine-updates)[Learning Material Updates](https://gamedev.rs/news/041/#learning-material-updates)[Tooling Updates](https://gamedev.rs/news/041/#tooling-updates)[Library Updates](https://gamedev.rs/news/041/#library-updates)[Other News](https://gamedev.rs/news/041/#other-news)[Discussions](https://gamedev.rs/news/041/#discussions)[Requests for Contribution](https://gamedev.rs/news/041/#requests-for-contribution)

## Announcements [#](https://gamedev.rs#announcements)

### Rust Graphics Meetup 3 [#](https://gamedev.rs#rust-graphics-meetup-3)

![Graphics meetup logo](../../assets/390ae8c9f940012a.jpg)


The 3rd Rust Graphics Meetup will take place on the [28th of January 2023 at
16:00 GMT](https://everytimezone.com/s/feafb968). This meetup is a chance to show off what
you’ve been working on in the graphics community, or see what other people have
been doing!

If you’re interested in speaking, please add a comment to [this
issue](https://github.com/gfx-rs/meetup/issues/3). You can also [read about the previous graphics
meetup](https://gamedev.rs/blog/graphics-meetup-02/).

### Rust GameDev Meetup [#](https://gamedev.rs#rust-gamedev-meetup)

![Gamedev meetup poster](../../assets/4a116bf88eb67a92.png)


The 22nd Rust Gamedev Meetup took place in December. You can watch the recording
of the meetup [here on Youtube](https://youtube.com/watch?v=Ck2R0yqTLcU). Here was the schedule
from the meetup:

- Fyrox Engine -
[@dmitrynstepanov](https://twitter.com/dmitrynstepanov) - Rusty Vangers -
[@kvark](http://kvark.github.io) - Graphite -
[@GraphiteEditor](https://twitter.com/GraphiteEditor)

The meetups take place on the second Saturday of every month via the [Rust
Gamedev Discord server](https://discord.gg/yNtPTb2) and are also [streamed on
Twitch](https://twitch.tv/rustgamedev). If you would like to speak at the next meetup on
January 14th, please [respond to the monthly GitHub
issue](https://github.com/rust-gamedev/meetup/issues/2).

![a screenshot of the account’s header: gamepad-in-gear logo, description and verified links](../../assets/dabced0dc13179f6.png)


As you may know, we have [a @rust_gamedev Twitter account](https://twitter.com/rust_gamedev) for
making announcements and collecting all the cool rust gamedev stuff there
into one feed.

In the last couple of months a significant portion of rust game developers
has either migrated from Twitter to [Mastodon](https://en.wikipedia.org/wiki/Mastodon_(social_network)) or started cross-posting there,
so [we’ve decided](https://github.com/rust-gamedev/wg/issues/131) to create a similar “official”
[@rust_gamedev account on the mastodon.gamedev.place server](https://mastodon.gamedev.place/@rust_gamedev).

Please follow us there and post your own relevant updates on [Fediverse](https://en.wikipedia.org/wiki/Fediverse)
using either the #RustGameDev tag or #RustLang #GameDev combo.

*Discussions:
/r/rust_gamedev*

## Game Updates [#](https://gamedev.rs#game-updates)

### Digital Extinction [#](https://gamedev.rs#digital-extinction)

![laser trail in Digital Extinction](../../assets/e98699e7c9bbf021.jpeg)

[Digital Extinction](https://de-game.org) ([GitHub](https://github.com/DigitalExtinction/Game), [Discord](https://discord.gg/vHMFuCWGSX),
[Reddit](https://reddit.com/r/DigitalExtinction)) by [@Indy2222](https://github.com/Indy2222) is a 3D real-time strategy game made with
[Bevy](https://bevyengine.org).

This month’s update is somewhat smaller but there has been some important progress in multiplayer.

The most notable updates are:

- game configuration is loaded from a file (
[docs](https://docs.de-game.org)), - a simple game lobby server has been created (
[docs](https://docs.de-game.org)), - a Bevy plugin with the lobby client has been implemented,
- several minor community, infrastructure, and other improvements have been done.

A more detailed update summary is available [here](https://mgn.cz/blog/de03).

![Real time tactical 2nd world war game](../../assets/fb91afefd25ec2eb.png)

Open Combat
([Website](https://opencombat.bux.fr/),
[GitHub](https://github.com/buxx/OpenCombat),
[Discord](https://discord.gg/6P2vtFh2Px))
by [bux](https://github.com/buxx/) is a real time tactical game
which takes place during the 2nd world war.

Since the last news about this game, the game engine has been rewritten to permit multiplayer. Most of the basic game engine features have been rewritten with the new engine (soldier moves, visibilities, map, etc.). Vehicle concept has been introduced to a T-26 tank. Basic fight features like gunfire and shelling have been introduced.

![Cute buildings, title, road, and sheep](../../assets/bd78ab13f25b2744.png)


[@anopara](https://twitter.com/anastasiaopara)’s and [@h3r2tic](https://twitter.com/h3r2tic)’s tiny building game
now finally has a name! It’s [Tiny Glade](https://store.steampowered.com/app/2198150/Tiny_Glade/)!

Tiny Glade is a small relaxing game about doodling
castles. Explore gridless building chemistry, and
watch the game carefully assemble every brick, pebble,
and plank. There’s no management, combat, or wrong
answers - just kick back and turn forgotten meadows
into lovable dioramas. Wishlist on [Steam](https://store.steampowered.com/app/2198150/Tiny_Glade/)!

![Shooting automatons in Temple Knight](../../assets/cff212664a981068.jpg)

Temple Knight ([Itch.io](https://nilaysavant.itch.io/temple-knight), [Twitter](https://twitter.com/nilay_savant/status/1607789552621727744))
by [@nilaysavant](https://github.com/nilaysavant) is a 3D FPS game developed using [Bevy](https://bevyengine.org).
You play the role of a knight and protect the temple from raiding automatons.

What began as an experiment to learn game dev in Rust using [Bevy](https://bevyengine.org).
Initially motivated by the visual appeal of a [scene running in the browser via WASM](https://twitter.com/nilay_savant/status/1568307034390675456).
It quickly started taking the shape of a game:

- From adding
[Rapier](https://rapier.rs/)for[basic physics](https://twitter.com/nilay_savant/status/1569665425046384641)to developing mechanics for other entities. - Path finding for Automaton’s using
[control systems](https://twitter.com/nilay_savant/status/1573783227911012352). - Which was later switched to a deterministic
[A-start navmesh approach](https://twitter.com/nilay_savant/status/1574735050809413633). - Developed mechanics for the player controller including the first-person-camera.
- Implemented weapon + projectiles systems.
- Finally,
[custom shaders for projectiles](https://twitter.com/nilay_savant/status/1607115041253519361)were added as a finishing touch.

An experiment that became the first game published by [@nilaysavant](https://github.com/nilaysavant).
Play [Temple Knight](https://nilaysavant.itch.io/temple-knight) in your browser.

![cargo space screenshot: two instances of the game running in parallel](../../assets/7ff138181bd28437.png)


[Cargo Space](https://helsing.studio/cargospace) ([Discord](https://discord.gg/ye9UDNvqQD)) by
[@johanhelsing](https://mastodon.social/@johanhelsing) is a co-op 2d space game where you build a
ship and fly it through space looking for new parts, fighting pirates and the
environment.

Johan wrote [an introductory post](https://johanhelsing.studio/posts/cargo-space-devlog-0) about the design idea,
and a tentative plan for its development.

The first step was to make an initial offline single-player prototype. This is
covered in the [first devlog](https://johanhelsing.studio/posts/cargo-space-devlog-1) along with topics such as
procedural generation, 2d platforming, bloom, and various community Bevy crates,
such as [bevy_ecs_tilemap](https://github.com/StarArawn/bevy_ecs_tilemap), [bevy_ecs_ldtk](https://github.com/Trouv/bevy_ecs_ldtk) and [bevy_particle_systems](https://github.com/abnormalbrain/bevy_particle_systems).

The procedural generation needs for the game also resulted in a new crate being born.
[noisy_bevy](https://github.com/johanhelsing/noisy_bevy) is a CPU and GPU noise plugin for Bevy.

After this, p2p rollback networking was added using [bevy_ggrs](https://github.com/gschup/bevy_ggrs) and [Matchbox](https://github.com/johanhelsing/matchbox).
The [second devlog](https://johanhelsing.studio/posts/cargo-space-devlog-2) goes through this in detail, and in
particular how integration between [bevy_ggrs](https://github.com/gschup/bevy_ggrs) and [leafwing_input_manager](https://github.com/Leafwing-Studios/leafwing-input-manager) was
implemented.

![Kraken](../../assets/a29c43e944e46590.png)

[@ThousandthStar](https://github.com/ThousandthStar) is creating 8bit Duels
([Discord](https://discord.gg/NbBcF4bGU5), [GitHub](https://github.com/ThousandthStar/8bit-duels)),
an 8bit style turn-based multiplayer strategy game.

Last month, an artist joined ThousandthStar to create art for the game.
A testing server has now been set up
(more information is in the [Discord](https://discord.gg/NbBcF4bGU5) server).

Furthermore, these three new troops have been added to the game: Reaper, Kraken, and Spider. The game now also includes new abilities for the various troops to come.

The full devlog for this month can be found [here](https://thousandthstar.github.io/posts/8bd-part5).

![flesh preview](../../assets/51db5834b9f657b3.gif)

[Flesh](https://store.steampowered.com/app/1660850/Flesh/) by [@im_oab](https://twitter.com/im_oab) is a 2D-horizontal shmup game with hand-drawn animation and
an organic/fleshy theme. It is implemented using [Tetra](https://github.com/17cupsofcoffee/tetra). This month’s updates
include:

- Change player bullet color and add trail particle.
- Add SFX when special weapon ready.
- Increase blood splash particles.
- Postpone release date to Q1, 2023.

### Pirate Annihilation [#](https://gamedev.rs#pirate-annihilation)

![Pirate annihilation game view](../../assets/b3527883b56c4b79.png)

[Kenney](https://twitter.com/KenneyNL)

Pirate Annihilation ([GitHub](https://github.com/indiedevcasts/pirate-annihilation), [Twitter](https://twitter.com/indiedevcasts))
by [indiedevcasts](https://indiedevcasts.com) ([@theredfish](https://twitter.com/theredfi_sh)) is a last-man-standing game
where pirate ships battle against each other in stormy seas.

The very [first devlog](https://youtu.be/lT1QmAHPRoo) is available on Youtube.
It describes the implementation of a smooth damping effect to follow the player
with the camera, jitter and stuttering issues, and the core game mechanics are
now defined.

![A wendigo at night](../../assets/562709b95776ca8a.jpg)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In December, work has been done to create a website to better assist moderation
in the game. Several months of project finances were done, and all of the data
is [publically visible](https://docs.google.com/spreadsheets/d/1Fk6kDsCdZLhVszXdsWUjoG4Cgc3cLbTqJgZ-gY3Ndq0/edit#gid=0). Work on Wyverns has continued, and
lots of effort is being put into their wings. Some UI elements have changed
location, both the bag and spellbook buttons were merged with other button bars.

Frost Gigas are another big item in the works. These creatures will be Veloren’s world boss. Gigas will hopefully be the first of a numerous elemental giants to roam the open world of Veloren and will need a large group of players to be able to take it down and collect it’s new uncraftable and legendary loot!

December’s full weekly devlogs: “This Week In Veloren…”:
[#201](https://veloren.net/devblog-201),
[#202](https://veloren.net/devblog-202),
[#203](https://veloren.net/devblog-203).

![repeater boss](../../assets/e5a3222e8da316c5.gif)

Thetawave is an open-source, roguelite, physics-based, space shooter game made
with [Bevy](https://bevyengine.org) and [Rapier](https://rapier.rs/).

This month, the first boss enemy was added to the
game. Unlike other enemies, it is composed of a single “mob” entity and 7
“mob segment” entities. It also uses behavior sequences to regularly change
its active set of behaviors. You can follow [@carlosupina](https://twitter.com/carlosupina) on Twitter for
regular updates about the game.

![Swords, Crates, Grenades, & Mines](../../assets/3a61e97c952ac26c.png)

[Jumpy](https://github.com/fishfolks/jumpy) ([GitHub](https://github.com/fishfolks/jumpy), [Discord](https://discord.gg/4smxjcheE5), [Twitter](https://twitter.com/spicylobsterfam)) by
[Spicy Lobster](https://spicylobster.itch.io) is a pixel-style, tactical 2D shooter with a fishy
theme.

In the last month, work started on a new architecture for the core Jumpy game loop.

Determinism and snapshot/restore functionality has been a challenge for networking support in jumpy. To address this, Jumpy has started migrating the core game loop to a custom, micro Entity Component System that is deterministic and can be trivially snapshot and restored.

By being simple and planning to eventually support a pure C API, it’s also intended for the micro-ECS approach to make it vastly easier to create a performant modding interface to Jumpy in the future.

Work has almost been finished on the new Bones ECS and the surrounding [Bones](https://github.com/fishfolk/bones)
framework, which is still built on Bevy for rendering and otherwise talking to
the hardware. The hope is that Bones can become a framework for making other
games similar in scope to Jumpy, without those games have to re-invent everything
that was needed to get features like UI, networking, localization, asset loading,
etc.

As soon as the ECS migration is finished, the plan is to get the final game juicing and polish done and to make a proper MVP release.

![hgs_screen](../../assets/6997ff59ffe446b3.jpg)


[Hydrofoil Generation](https://hydrofoil-generation.com/)
([Steam](https://store.steampowered.com/app/1448820/Hydrofoil_Generation/), [Facebook](https://facebook.com/HydrofoilGenerationSailing/), [Discord](https://discord.gg/DtKgt2duAy/))
is a realistic sailing/foiling inshore simulator in development for PC/Steam
that will put you in the driving seat of modern competitive sailing.

The game is written completely in Rust, using a custom engine based on DirectX 11, physics powered by Rapier-3D.

Jaxx Vane Studio army of 2, Stefano Casillo and Chax Duero is pushing through the final steps to get the game ready for Steam Early Access release.

As final QA approaches the team is at work to add the last level of polish and more details as possible to every aspect of the game.

A new Tutorial System has been added to introduce people with different backgrounds to the game as gently as possible making the learning curve of this complex simulator less steep.

Stefano is also back on [Twitch](https://twitch.tv/kunosstefano) streaming coding sessions live.

Hydrofoil Generation should be available on Steam in the first months of 2023.

![shooting 2.5D enemies through a doorway](../../assets/906d2da1e919c749.gif)


[Doomé](https://dzejkop.itch.io/doome) by [Patryk Wychowaniec](https://pwy.io) and [Jakub Trąd](https://github.com/Dzejkop)
is a GameOff’22 FPS game:

<…> the topic was cliché and our game is Doom meets Portal meets The Stanley Parable, with real-time raytraced graphics (that work plenty fast even on a CPU) and a 10-minute storyline!


The source code [is available on GitHub](https://github.com/Patryk27/doome).
The game is written with a custom [rust-gpu](https://github.com/EmbarkStudios/rust-gpu)-based raytracer:
[strolle](https://reddit.com/r/rust/comments/zsrvss/strolle_raytracing).
[Watch a talk from a recent Rust Wrocław’s meeting](https://youtu.be/S85Tw0dVtmw?t=5306)
to learn more about the implementation details.

You can play the game online and/or get binaries [at itch.io](https://dzejkop.itch.io/doome).

*Discussions: /r/rust*

![Steam page: a screenshot with some factory and short description](../../assets/b0d6ed89d0734b82.png)


[Combine&Conquer](https://store.steampowered.com/app/2220850/Combine_And_Conquer) ([itch.io](https://martinbucksoftware.itch.io), [devlog](https://buckmartin.de/combine-and-conquer.html),
[Discord](https://discord.gg/peBD6Z5PvN)) by [Martin Buck](https://github.com/I3ck)
is a WIP relaxing multi-planetary 2D factory automation game.
This month’s updates include:

[Early Access release on Steam](https://store.steampowered.com/app/2220850/Combine_And_Conquer).[A bunch of minor v0.3.* versions](https://buckmartin.de/combine-and-conquer.html)with loads of bugfixes and small improvements in UX, rendering, etc.

*Discussions:
/r/rust_gamedev*

![lots of small red ships are attacking a large blue ship in close range](../../assets/7925f596f1db87b3.png)


[triverse](https://cragwind.itch.io/triverse) by [@cragwind](https://cragwind.com) is a WIP smart-pause RTS with custom unit creation
on a triangle grid canvas.

In a distant star system, AI collectives vie for power. Assemble and control a self-replicating fleet to harvest resources, salvage wreckage, and defend your territory. Using modular parts, design ships to counter threats while balancing mobility, defense, and firepower.


You can find [the detailed guide to playing here](https://cragwind.com/triverse/)
and [play the web version on itch.io](https://cragwind.itch.io/triverse).

This month’s [updates](https://cragwind.itch.io/triverse/devlog) include:

[Salvaging parts](https://cragwind.itch.io/triverse/devlog/458561/salvaging-parts)from wreckage using workers for building your own units.[Torpedo launchers](https://cragwind.itch.io/triverse/devlog/464791/torpedo-launcher)for taking out large or stationary targets.

## Engine Updates [#](https://gamedev.rs#engine-updates)

![ABSM Editor](../../assets/30f8b2421d15a2ef.gif)


[Fyrox](https://github.com/FyroxEngine/Fyrox) ([Discord](https://discord.com/invite/xENF5Uh), [Twitter](https://twitter.com/DmitryNStepanov)) is a game engine that
aims to be easy to use and provide a large set of out-of-the-box features. In December
it got a lot of new functionality and improved existing:

- Animation system rework is completed
- Animation and ABSM editors are now fully usable
- Reflection improvements
`Copy Value as String`

for Inspector- Ability to enable/disable scene nodes
- Customizable graph update pipeline
- UI Widgets improvements
- Curve editor improvements
- Lots of bug fixes

[Runty8](https://github.com/jjant/runty8) is an experimental port of the [Pico8](https://www.lexaloffle.com/pico-8.php)
fantasy console that supports writing games in Rust.

Runty8 has recently added support for WebAssembly, which means that you can now run your games in the browser!

Feel free to [follow their template](https://github.com/jjant/runty8#making-your-own-games) to start making your own games.

The project is in very early stages, and is currently looking for contributors.
If you’re interested, feel free to read their [contributing guide](https://github.com/jjant/runty8/blob/master/CONTRIBUTING.md)
or browse through the [open issues](https://github.com/jjant/runty8/issues).

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

![Rustacean Station’s logo: rusty Ferris](../../assets/a8d94e5fd097a571.jpeg)


The [Rustacean Station](https://rustacean-station.org) podcast
[interviewed Gray Olson](https://rustacean-station.org/episode/gray-olson),
the developer of [Presser](https://gamedev.rs/news/039#presser) - a library that aims to make
it easier to safely work with byte buffers.

In this episode, [Gray](https://grayolson.me) talks about
art and graphic designing work for Embark Studio,
computer graphics and ray tracing,
memory allocation in Rust’s virtual machine,
and Embark’s vision of Rust gamedev.

![Same title but as an image](../../assets/8589a701e2f08efd.jpg)


[@whoisryosuke](https://mastodon.gamedev.place/@whoisryosuke) released [a blog post](https://whoisryosuke.com/blog/2022/importing-gltf-with-wgpu-and-rust) on how to
parse GLTF files in Rust, render them using wgpu,
and play animations imported from Blender.

![a window that shows a circle button, title, and a click counter](../../assets/13b0f3f6e060d420.png)


[@Paper010](https://github.com/Paper010) released a short two-part tutorial
aimed at beginners who want to get started with game development
with Rust and [macroquad](https://github.com/not-fl3/macroquad):

[The first part](https://dev.to/paper010/rust-create-a-clicker-game-with-macroquad-1820)covers the minimal version of a clicker game.[The second part](https://dev.to/paper010/part-2-create-a-clicker-game-with-rust-4nne)explains how to play sounds and change colors.

The final source code [is available on GitHub](https://github.com/Paper010/rust-clicker-game).

## Tooling Updates [#](https://gamedev.rs#tooling-updates)

Graphite ([website](https://graphite.rs), [GitHub](https://github.com/GraphiteEditor/Graphite),
[Discord](https://discord.graphite.rs), [Twitter](https://twitter.com/GraphiteEditor)) is a free,
in-development raster and vector 2D graphics editor based around a Rust-powered
node graph compositing engine.

December’s [sprint 21](https://github.com/GraphiteEditor/Graphite/milestone/21) introduces:

- Chain reaction: The Imaginate feature, an AI image generation workflow
powered by
[Stable Diffusion](https://en.wikipedia.org/wiki/Stable_Diffusion), becomes a node. Chain together a sequence of fine-tuned generation steps. And explore ideas by branching the graph into new creative directions. - Node nurturing: New features provide polish to the node graph. Nodes can be copy/pasted, hidden, previewed, and linked more easily.
- Bugs, begone!: A major effort to improve editor usability fixes dozens of bugs and paper cuts. Boolean shape operations now crash less frequently, the UI no longer slows down badly over time, and undo history is finally fixed.

Stay tuned for the imminent Alpha Milestone 2 release and progress converting existing features into nodes.

Open the [Graphite editor](https://editor.graphite.rs) in your browser to give it a try
and share your creations with #MadeWithGraphite on Twitter.

## Library Updates [#](https://gamedev.rs#library-updates)

[Inox2d](https://github.com/Inochi2D/inox2d) ([Discord](https://discord.com/invite/abnxwN6r9v)) by the Inox2d Workgroup
is an experimental official Rust implementation
of the [Inochi2D](https://inochi2d.com) puppet animation technology.
Inochi2d is notably used by the popular vtuber [@AsahiLina](https://youtube.com/@AsahiLina).

Currently, Inox2d is still not on par with the [reference implementation](https://github.com/Inochi2D/inochi2d).
Basic features like [animations](https://github.com/Inochi2D/inox2d/issues/5) and
a proper [camera API](https://github.com/Inochi2D/inox2d/issues/7) have yet to be worked on.

Users who really want to use it should instead go with the reference implementation.
If using Rust, through the official [inochi2d-rs](https://github.com/Inochi2D/inochi2d-rs) bindings.

Currently, Inox2d contributors are working on a [WGPU renderer backend](https://github.com/Inochi2D/inox2d/pull/6).
They are also looking forward towards an [official Bevy integration](https://github.com/Inochi2D/inox2d/issues/1)!

![an UI showing the currently running dialog in the bottom and some control buttons in the top-right corner](../../assets/2050f926129d28c7.png)


[bevy_rpg](https://github.com/project-flara/bevy-rpg) ([Discord channel](https://discord.com/channels/676678179678715904/1054506073240899684)) by [@fianathedevgirl](https://github.com/fianathedevgirl)
is a plugin allowing RPG or visual novel dialogs
to be made with the Bevy game engine.

At the moment, it can be used for very basic dialogs. “Choose dialog” or text input dialog are still not implemented and the dialog controller buttons doesn’t work yet.

If you are interested in seeing how it should be used in production,
checkout [“Project Flara”](https://github.com/project-flara/project-flara). It’s a prototype/demo game
made by the same author showcasing a JRPG-ish indie game written in Rust.
The author also made a basic example [here](https://github.com/project-flara/bevy-rpg/blob/main/examples/basic.rs).

![character sprite generator](../../assets/d1e001fefd6cd616.png)

lpcg ([Crates.io](https://crates.io/crates/lpcg), [GitHub](https://github.com/buxx/lpcg/)) by
[bux](https://github.com/buxx/) is a library which generates character sprites,
based on assets from the [Liberated Pixel Cup](https://lpc.opengameart.org/).

![egui_dnd in action](../../assets/f97eb47192d492be.gif)

[showcase](https://lucasmerlin.github.io/egui_dnd/)of egui_dnd

[egui_dnd](https://lucasmerlin.github.io/egui_dnd/) ([github](https://github.com/lucasmerlin/egui_dnd), [crates.io](https://crates.io/crates/egui_dnd)) by [@lucasmerlin](https://github.com/lucasmerlin)
is a new drag and drop sorting crate for egui. While egui itself includes some drag
and drop support, it’s not intuitive to use. This crate provides a simple
abstraction over egui’s drag and drop features.

The first release contains initial support for vertical sorting. If there is interest, more features could be added.

*Discussions: /r/rust*

![scene displaying generated colliders](../../assets/60b1c2a2b445b5ad.png)


[bevy_rapier_collider_gen](https://github.com/shnewto/bevy_rapier_collider_gen) by [@shnewto](https://github.com/shnewto) is a library
for generating bevy_rapier2d colliders for bevy apps, from images with
transparency.

Features include out of box support for generating:

- Convex polyline colliders
- Polyline colliders
- Convex hull colliders
- Heightfield colliders
- Other colliders or geometries by getting edge coordinates in “drawing order”
- Multiple colliders from a single image

For more, in pictures, see the picture book retrospective
[“misadventures in collider generation”](https://drinkspiller.com/bevy-rapier-collider-gen).

[Mun](https://mun-lang.org) is a scripting language for gamedev focused on quick iteration times
that is written in Rust.

The previous Mun release dates back over one and a half years. Since then - slowly but steadily - the Mun Community and Core Team have been working towards Mun v0.4.0 and it’s finally here!

Mun v0.4 does not only bring array support to Mun, but it also lays the
groundwork for a plethora of language features that require indirect types and
recursion. For a full list have a look at the [changelog](https://github.com/mun-lang/mun/releases/tag/v0.4.0), but
the main improvements are:

- Dynamically-sized arrays
- Simplified function invocations from Rust
- Simplified struct API for Rust
- Apple M1 & experimental iOS support
- Upgrade to LLVM 13
- Support for runtime usage in entity component systems (ECS)

![a screenshot: spherical characters doing stuff](../../assets/00d43b4128376e22.jpg)

[Creative Playground](https://twitter.com/createplayremix), which uses rust-gpu and raytracing

[Rust-gpu](https://github.com/EmbarkStudios/rust-gpu) ([Discord](https://discord.com/channels/750717012564770887/750717499737243679)) allows you
to write your GPU shaders in the Rust language.
It consists of a Rust compiler backend for generating SPIR-V shader
modules and an API to address GPU resources.

Release v0.4.0 brings a lot of upgrades, bug fixes, maturity, and now also supports raytracing shaders! Furthermore, all dependent crates have been published to crates.io, so pointing to rust-gpu’s GitHub in your Cargo.toml is no longer required.

Eager to get started? Check out the [Dev Guide](https://embarkstudios.github.io/rust-gpu/book/introduction.html), or
chat with the devs and the community on the public [Discord server](https://discord.com/channels/750717012564770887/750717499737243679).

assets_manager ([GitHub](https://github.com/a1phyr/assets_manager), [crates.io](https://crates.io/crates/assets_manager))
is a library to easily load and cache assets. It comes with support for multiple
file formats and out-of-the-box hot-reloading.

The last release includes internals performance improvements and more flexibility in the way to load assets.

[Ggez bindings](https://github.com/a1phyr/ggez-assets_manager) were also updated to latest ggez version.

![Demo of improved tables shows smooth column resizing](../../assets/6a9fb79a6ae27103.gif)


[egui](https://egui.rs) is an easy-to-use immediate mode GUI library in pure Rust.

This month [egui v0.20](https://twitter.com/ernerfeldt/status/1600869756491673600) was released. Highlights:

- Support for
[AccessKit](https://github.com/AccessKit/accesskit)vastly improves the accessibility of[eframe](https://lib.rs/eframe)apps on Windows and Mac. - Vastly improved tables (see above) for
[rerun.io](https://rerun.io)’s needs. - Improved wgpu renderer that now allows using egui-wgpu on the web, with a WebGL backend.
- egui now expects integrations to do all color blending in gamma space.
- Interactive widgets can now be on top of other interactive widgets. Great for putting floating widgets on top of 3D content, for instance.
[ecolor](https://docs.rs/ecolor)helper lib for all the color conversions needs.- Helper functions for animating panels that collapse/expand.

For full details see the [changelog](https://github.com/emilk/egui/blob/master/CHANGELOG.md#0200---2022-12-08---accesskit-prettier-text-overlapping-widgets).

[forma](https://github.com/google/forma) by google is a (thoroughly) parallelized experimental
Rust vector-graphics renderer with both a software (CPU) and hardware (GPU)
back-end having the [goals](https://github.com/google/forma#readme) of portability, performance, simplicity,
and minimal size.
Forma relies on Rust’s SIMD auto-vectorization/intrinsics and [Rayon](https://github.com/rayon-rs/rayon)
to have good performance on the CPU,
while using [WebGPU](https://github.com/gpuweb/gpuweb) ([wgpu](https://wgpu.rs/)) to take advantage of the GPU.

A few implementation highlights that make the library stand out from commonly used vector renderers:


- Curvature-aware flattening. All higher cubic Béziers are approximated by quadratic ones, then, in parallel, flattened to line segments according to their curvature. This
[technique]was developed by Raph Levien.- Cheap translations and rotations. Translations and rotations can be rendered without having to re-flatten the curves, all the while maintaining full quality.
- Parallel pixel grid intersection. Line segments are transformed into pixel segments by intersecting them with the pixel grid. We developed a simple method that performs this computation in O(1) and which is run in parallel.
- Efficient sorting. We ported
[crumsort]to Rust and parallelized it with Rayon, delivering improved performance over its pdqsort implementation for 64-bit random data. Scattering pixel segments with a sort was inspired from Allan MacKinnon’s work on[Spinel].- Update only the tiles that change (currently CPU-only). We implemented a fail-fast per-tile optimizer that tries to skip the painting step entirely. A similar approach could also be tested on the GPU.

While Forma is a general-purpose library it can be an interesting building block
for vector-based games and engines (see the [spaceship demo](https://github.com/google/forma/blob/681e8bfd3/demo/src/demos/spaceship.rs)
from the above image).

*Discussions: /r/rust*

## Other News [#](https://gamedev.rs#other-news)

- Other game updates:
[Ivy Sly renamed](https://twitter.com/ivy_sly_/status/1603289612574937092)their online turn-based fighting game (and superpowered fight scene simulator) Yomi Hustle to “Your Only Move Is HUSTLE” due to a trademark infringement; The game also[got a Steam page](https://store.steampowered.com/app/2212330/Your_Only_Move_Is_HUSTLE)in preparation for the upcoming release in February.- Orlando Valverde published
[a new version Pushin’ Boxes](https://twitter.com/septum___/status/1606176677540683776)that features a level editor. [Dustin Carlino shared](https://a-b-street.github.io/docs/project/history/vision_and_validate)a retrospective of 2022 and 2023 plans for the A/B Street project.[Paddlepunks got a new parry variation](https://twitter.com/sov_gott_games/status/1600958840220299266)to homura that “pauses” the ball for a bit before reflecting it back harder than the regular parry[@ollej released a web playable version](https://hachyderm.io/@ollej/109506591357987042)of the macroquad port of the Infinite Bunner game.[@kuviman released Flashdark](https://twitter.com/kuviman/status/1598410936460738560)- a small first-person horror game where you see the dark world using your flashdark and solve puzzles while avoiding the ghost.[Fish Folk: Punchy v0.2 was released](https://twitter.com/spicylobsterfam/status/1600122907572654080): Big Bass Boss has a new bomb toss attack, hitstop on damage application has changed, the beginnings of support for multiple attacks per fighter and attack chains are implemented, and players can now wear special hats.[Red Life](https://reddit.com/r/rust/comments/zgv101/red_life_surviving_on_mars)is a small game about an astronaut who is trying to survive in the hostile environment of Mars.[@Tantan shared a vlog](https://youtube.com/watch?v=PnwhUeyrQ54)about a bug he had encountered during adding multiplayer to his voxel game.[Life Code shared a vlog](https://youtube.com/watch?v=miUD9Ni7LnQ)about making a user interface using egui with AI assistance.[@enigmanark shared a bunch of updates](https://twitter.com/hashtag/RetrosicII?f=live)about the RetrosicII shmup game.

- Other engine updates:
[square_wheel](https://reddit.com/r/rust/comments/zd31kv/squarewheel_software_renderer_video)is a pretty advanced FPS-oriented software renderer for modern CPUs.[Anthony Utt](https://twitter.com/alkimia_studios)released new vlogs about the[Alkahest](https://github.com/AlkimiaStudios/alkahest-rs)engine progress:[orthograthic cameras](https://youtube.com/watch?v=eCVLRpJFOTQ),[transforms, textures, and scenes](https://youtube.com/watch?v=WMIfFA2m9TA), and[2D render batching](https://youtube.com/watch?v=HEqvKx4ihRU).

- Other learning material updates:
[Raph gave a talk](https://youtube.com/watch?v=zVUTZlNCb8U)about the vision for high performance UI implemented in Rust, and status of the current Xilem effort to build it. Includes sections on the piet-gpu 2D rendering engine, integration with AccessKit, and some details of the reactive architecture.[PhaestusFox](https://youtube.com/playlist?list=PL6uRoaCCw7GN_lJxpKS3j-KXuThRiSXc6)has posted more episodes of their ‘Bevy Basics’ tutorial series.[Maciej Główka released a blog post](https://maciejglowka.com/blog/text-based-json-toml-resources-in-bevy-engine)on nuances of loading game data from TOML or JSON assets into Bevy-based games.- Matthew Bryant released another
[Bevy Intro Tutorials](https://youtube.com/playlist?list=PLT_D88-MTFOPPl75g4WshL1Gx2bnGTUkz)YouTube video:[“Compute Shaders in Bevy”](https://youtube.com/watch?v=neyIpnII-WQ).

- Other tooling updates:
[uCrowds shared a video](https://reddit.com/r/rust_gamedev/comments/zvud5j/ucrowds_150k_agents)of a Rusty crowd simulation engine compiled to WASM and running a simulation of 150.000 agents in real-time in a browser.

- Other library updates:
[devices](https://github.com/hankjordan/devices)is a cross-platform library for retrieving information about connected devices, supports Linux and Windows.[quad-svg](https://github.com/macnelly/quad-svg)is a small library for rendering .svg files to[macroquad](https://github.com/not-fl3/macroquad)’s Texture2D using[resvg](https://github.com/RazrFalcon/resvg).[@MatanLurey](https://twitter.com/MatanLurey)released[mythoji](https://github.com/matanlurey/mythoji)- a minimal Rust crate that helps to identify and display fantasy appropriate emojis.[durian](https://github.com/spoorn/durian)is a general purpose client/server networking library that provides a “thin” abstraction layer on top of the QUIC protocol (using[quinn](https://github.com/quinn-rs/quinn)) to make writing netcode extremely simple, automatically taking care of connection/streams management, byte details, packet framing/fragmentation/reassembly, parallel sender/receivers, etc.[faer](https://github.com/sarah-ek/faer-rs)is a collection of crates that implement a low-level API for linear algebra routines that is somewhat similar to BLAS/Lapack, but gives more control to users by allowing parallelism to be specified on a per-call basis.[bevy_adventure](https://github.com/hankjordan/bevy_adventure)is a framework for building adventure games in Bevy that features GLTF support, multuple scenes with dynamic objects, inventory, and automatic camera animation.


## Discussions [#](https://gamedev.rs#discussions)

- /r/rust_gamedev:

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[‘Are We Game Yet?’ wants to know about projects/games/resources that aren’t listed yet](https://github.com/rust-gamedev/arewegameyet#contribute).[Graphite is looking for contributors](https://graphite.rs/contribute)to help build the new node graph and 2D rendering systems.[winit’s “difficulty: easy” issues](https://github.com/rust-windowing/winit/issues?q=is%3Aopen+is%3Aissue+label%3A%22difficulty%3A+easy%22).[Backroll-rs, a new networking library](https://github.com/HouraiTeahouse/backroll-rs/issues).[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[A/B Street’s “good first issue” issues](https://github.com/a-b-street/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/D-Good-First-Issue).

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!

**Discuss this post on**:
[/r/rust_gamedev](https://reddit.com/r/rust_gamedev/comments/10naebl/this_month_in_rust_gamedev_41_december_2022),
[Twitter](https://twitter.com/rust_gamedev/status/1619290431761817600),
[Mastodon](https://mastodon.gamedev.place/@rust_gamedev/109765982808236944),
[Discord](https://discord.gg/yNtPTb2).