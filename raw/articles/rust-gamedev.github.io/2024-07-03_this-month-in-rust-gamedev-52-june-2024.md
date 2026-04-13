---
title: 'This Month in Rust GameDev #52 - June 2024'
url: https://gamedev.rs/news/052/
author: Rust GameDev WG
published: '2024-07-03'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 52th issue of the Rust GameDev Workgroup’s
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

[Announcements](https://gamedev.rs/news/052/#announcements)[Game Updates](https://gamedev.rs/news/052/#game-updates)[Engine Updates](https://gamedev.rs/news/052/#engine-updates)[Learning Material Updates](https://gamedev.rs/news/052/#learning-material-updates)[Tooling Updates](https://gamedev.rs/news/052/#tooling-updates)[Library Updates](https://gamedev.rs/news/052/#library-updates)[Interviews](https://gamedev.rs/news/052/#interviews)[Blog Posts](https://gamedev.rs/news/052/#blog-posts)[Jobs](https://gamedev.rs/news/052/#jobs)[Engine Newsletters](https://gamedev.rs/news/052/#engine-newsletters)[Future News](https://gamedev.rs/news/052/#future-news)

## Announcements [#](https://gamedev.rs#announcements)

For years, our readers have asked for a way to subscribe to this newsletter by email. This again came up in our [recent survey](https://gamedev.rs/blog/survey-02/).
We’re happy to announce that this feature is now available! When you visit our [homepage](https://gamedev.rs/),
you can now scroll down and find an email subscription form.
We’ll send you an email whenever a new post is published, which currently is once per month.

The emails are currently sent from [gamedev-rs@proton.me](mailto:gamedev-rs@proton.me).
We will switch this to an actual @gamedev.rs address in the future. Please tell us if you encounter any issues with the emails.

## Game Updates [#](https://gamedev.rs#game-updates)

[Untitled Pixel Wizards Game](https://slowrush.dev) is a local-multiplayer [Noita](https://store.steampowered.com/app/881100/Noita/)-like platformer about
killing baddies using spells powered by pixel physics. This month was focused on juicing up said baddies:

[Pew Pew Pew](https://www.slowrush.dev/news/pew-pew/): baddies learned to shoot at players.[Hot Pursuit](https://www.slowrush.dev/news/hot-pursuit/): baddies also learned to chase players! (They’re real smart.)[Status Update](https://www.slowrush.dev/news/status-update/): physically-simulated pixels learn to burn & poison players & baddies.[Ragdolls](https://www.slowrush.dev/news/ragdolls/): corpses of dead baddies learn to tumble around all realistic-like.[Fiddling with Fire](https://www.slowrush.dev/news/fiddling-with-fire/): the fire mechanic figures out how to better burn baddies.



![Way of Rhea](../../assets/54b533efd81a8e1d.jpg)

Way of Rhea ([Steam](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n52), [Newsletter](https://anthropicstudios.com/newsletter/signup/tech)) is a color-based puzzle game with difficult puzzles, but
forgiving mechanics developed by [Mason Remaley](https://masonremaley.com/) in a custom Rust engine. Since its release in May,
Mason has fixed many bugs and implemented quality-of-life improvements.

They recently conducted an [AMA on /r/rust_gamedev](https://www.reddit.com/r/rust_gamedev/comments/1cwqcfl/i_spent_6_years_developing_a_puzzle_game_in_rust/) about their experience
developing and shipping a game after six years in Rust.
They then curated the questions and answers into a [blog post](https://gamesbymason.com/2024/06/01/wor-ama/).
It includes questions about Rust, libraries, experiences writing a custom game engine, and game development in general.



![Gunbugs shooting at a bunch of eggplants](../../assets/533714105a13a5db.jpg)

Gunbug is a 2D online co-op horde survival shoot’em up game.

It focuses on shooting lots of enemies with lots of guns. It can be played solo or with up to 10 players.

It is built with [Bevy](https://bevyengine.org) and uses [bevy_rapier](https://github.com/dimforge/bevy_rapier) for ray casting,
[bevy_kira_audio](https://github.com/NiklasEi/bevy_kira_audio) for audio, and [renet](https://github.com/lucaspoffo/renet) for networking.
The iOS and macOS versions are built with [xbuild](https://github.com/rust-mobile/xbuild).

You can wishlist the game on [Steam](https://store.steampowered.com/app/2946990?utm_source=this_month_in_rust). Playtests start in the upcoming months.
iOS and Android builds already work, but store pages don’t exist yet.

## Engine Updates [#](https://gamedev.rs#engine-updates)

![godot-rust logo](../../assets/20de387b679b9c7f.jpg)


godot-rust ([GitHub](https://github.com/godot-rust/gdext), [Discord](https://discord.gg/aKUCJ8rJsc), [Mastodon](https://mastodon.gamedev.place/@GodotRust), [Twitter](https://twitter.com/GodotRust)) by [@Bromeon](https://github.com/Bromeon)
provides Rust bindings for the [Godot engine](https://godotengine.org/).

After quite a bit of development on GitHub, the Godot 4 bindings are now available on [crates.io](https://crates.io/crates/godot) –
you can immediately get started using
`cargo add godot`

. Furthermore, the GDExtension API level can now be specified with a Cargo feature, e.g. `api-4-1`

.

The `ScriptInstance`

API has matured a lot over the past months. This feature allows users to write Godot scripts in Rust, which can be
attached to nodes (just like GDScript). Scripts allow for quickly attaching/detaching functionality in a scene.

The overall API has seen several consistency improvements: reorganized modules, `self`

/`&self`

receivers on geometric types,
easier element access for `Array`

/`Dictionary`

/`Packed*Array`

. The library has also benefited from Rust’s
[ #[diagnostic::on_unimplemented]](https://blog.rust-lang.org/2024/05/02/Rust-1.78.0.html#diagnostic-attributes) to improve user-facing error messages.

*Discussions:
/r/rust,
Mastodon,
X*

*See also the devlog article.*

![Sharp Screen-Space Reflections in Bevy 0.14](../../assets/f7fb878fec7694b6.jpg)

The Bevy game engine is gearing up to release version 0.14.
The (probably) last release candidate is out now and ready for testing.
If you want to help out,
check out the [draft release notes](https://bevyengine.org/news/draft-bevy-0-14/) and the [draft migration guide](https://bevyengine.org/learn/migration-guides/0-13-to-0-14/) and report any issues you find.

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

The community-beloved unofficial [Bevy Cheatbook](https://bevy-cheatbook.github.io/) by Ida “Iyes” is a collection of Bevy tutorials, recipes and advanced documentation.
The cheatbook is currently in the process of being updated to Bevy 0.14 and now features the following new chapters:

[Transform Interpolation/Extrapolation](https://bevy-cheatbook.github.io/cookbook/smooth-movement.html): How to get smooth-looking movement on-screen for things you simulate in FixedUpdate[Internal Parallelism](https://bevy-cheatbook.github.io/programming/par-iter.html): Multithreading within a Bevy system[One-Shot Systems](https://bevy-cheatbook.github.io/programming/one-shot-systems.html): Systems that you run on-demand, not in a schedule[Background Computation](https://bevy-cheatbook.github.io/fundamentals/async-compute.html): How to do processing that may span multiple frame updates and not hold up the game’s framerate with long CPU work.

Olle Wreede of [Agical](https://www.agical.se/) published a [complete guide](https://mq.agical.se/) on
how to develop a classic 2D shoot ’em up game using the game library
Macroquad and the Rust programming language.

It covers everything from a simple Hello World Macroquad application to adding graphics, audio, a shader, a graphical menu, and how to release the game on multiple platforms.

### Other learning materials [#](https://gamedev.rs#other-learning-materials)

[Using tracing to profile a Bevy project](https://rornic.com/posts/using-tracing-to-profile-a-bevy-project/)[Bevycation of Brackeys First Game in Godot Tutorial](https://github.com/Occuros/bevycation_brackeys_first-game-in-godot): A Bevy version of Brackeys’[“How to make a Video Game - Godot Beginner Tutorial”](https://www.youtube.com/watch?v=LOhfqjmasi0)

## Tooling Updates [#](https://gamedev.rs#tooling-updates)

![The Playdate console](../../assets/2305a01dcc3687d8.png)

[Rusty Playdate](https://github.com/boozook/playdate) ([GitHub](https://github.com/boozook/playdate), [Mastodon](https://gamedev.social/@playdaters)) by [@boozook](https://github.com/boozook)
is a large set of crates and tools for the full cycle of creating games for the [Playdate handheld console](https://play.date/).

A big part of the Rusty Playdate project is the [ cargo-playdate](https://github.com/boozook/playdate/tree/main/cargo) tool that functions as a build system.
It works as a cargo-plugin as well as a standalone, and does several things:

- It manages the compilation of your program,
- builds assets for the crate and its dependencies,
- generates a manifest,
- and assembles it all into a bundle that runs on the device or a simulator.

In this month `cargo-playdate`

v0.5 has been [released](https://github.com/boozook/playdate/releases/tag/2024.06.18) and received massive refactoring, bugfixes and new features:

- support for
[cargo’s auto-targets](https://doc.rust-lang.org/cargo/reference/cargo-targets.html#target-auto-discovery), i.e. targets such as`bin`

or`example`

that aren’t declared in the Cargo.toml [target-specific package-info](https://github.com/boozook/playdate/blob/main/support/build/README.md#target-specific-package-info)is inherited from the main package-info`package.metadata.playdate.options`

is inherited from the`workspace.metadata`

- incremental builds now work as expected

The register decoder in the [ pd-symbolize-crashlog](https://crates.io/crates/playdate-symbolize/0.2.0) was also updated.
It now properly decodes all available registers such as
PSR,
CFSR, and
HSFR.

## Library Updates [#](https://gamedev.rs#library-updates)

![egui_ratatui running in Bevy](../../assets/654efd5db5b61169.jpg)

[egui_ratatui](https://github.com/gold-silver-copper/egui_ratatui) by [gold-silver-copper](https://github.com/gold-silver-copper) is an [egui](https://github.com/emilk/egui) widget that is also a [ratatui](https://github.com/ratatui-org/ratatui) backend.
It allows you to create Terminal User Interfaces (TUIs) inside egui.
You can try out the [web demo](https://gold-silver-copper.github.io/) to see it in action.

The current release is the product of months of iteration, and is now “stable”. It is Wasm compatible and engine agnostic: use it in Bevy, *Quad, eframe, pixels, etc.

`egui_ratatui`

is currently being used for the development of a game and
educational software at a startup with no issues so far.

FMOD-oxide brings safe rust bindings to the FMOD sound engine. This crate tries to be as rusty and low-cost as possible, without comprimising on any APIs. Certain APIs, such as loading banks from a pointer, are marked as unsafe, but are still available for use.

![Bevypunk: a recreation of Cyberpunk 2077's UI made with Lunex](../../assets/bbeaa3564dedea39.jpg)

Lunex is a path based retained layout engine for Bevy entities, built around vanilla Bevy ECS. It gives you the ability to make your own custom UI using regular ECS like every other part of your app. Notably, this includes world-space 3D UI!

The above screenshot is from the [Bevypunk UI Web Demo](https://idedary.itch.io/bevypunk), which includes a main menu and a character creation screen.

You can get started by reading the [bevy_lunex book](https://bytestring-net.github.io/bevy_lunex/).

হালকা: *in bengali, haalka means “light” (e.g. not heavy) and can also be used to mean “easy”*

Haalka is an ergonomic reactivity library powered by the [FRP](https://en.wikipedia.org/wiki/Functional_reactive_programming) signals of [futures-signals](https://github.com/Pauan/rust-signals).
It is a port of the web UI libraries [MoonZoon](https://github.com/MoonZoon/MoonZoon) and [Dominator](https://github.com/Pauan/rust-dominator)
and offers the same signal semantics as a thin layer on top of bevy_ui.

While haalka is primarily targeted at UI and provides high level UI abstractions as such, its core abstraction can be used to manage signals-powered reactivity for any entity, not just bevy_ui nodes.

![A candle shining 2D light](../../assets/99b88ce7620aa3b8.gif)

bevy_light_2d is a new general purpose 2D lighting for the Bevy game engine. Designed to be simple to use, yet expressive enough to fit a variety of needs. Features include:

- Component driven design
- Configurable point lights
- Camera-specific ambient light
- Single-camera rendering

[bevy_hanabi](https://github.com/djeedai/bevy_hanabi) 0.11 [#](https://gamedev.rs#bevy-hanabi-0-11)

![Trails in Hanabi](../../assets/f16315a98a2b6d30.gif)

Hanabi is a GPU particle system plugin for the Bevy game engine.
The most notable new feature in [bevy_hanabi 0.11](https://github.com/djeedai/bevy_hanabi) is support for trails and ribbons.

![A fountain of particles](../../assets/84de9bc7387822fd.jpg)

berdicles is an expressive CPU particle system for the Bevy engine. Features include:

- Instancing based CPU particles.
- Expressive non-physics based particle traits.
- Familiar setup with Bevy’s native Material and Mesh.
- Particles as emitters.
- Mesh based particle trails.
- Particle events that spawn other particles.
- Billboard particles.

### Other Library Updates and Releases [#](https://gamedev.rs#other-library-updates-and-releases)

[glam 0.28](https://github.com/bitshifter/glam-rs):`glam`

is a foundational crate when it comes to math in general in Rust. For example, its types are directly visible in the`Vec`

types Bevy consumes and re-exports, like`Vec3`

. v0.28 brings AArch64 NEON SIMD support as well as a couple smaller breaking changes.[gdext-coroutines](https://github.com/Houtamelo/gdext_coroutines): Run Rust coroutines in Godot 4.2+ (through GDExtension), inspired on Unity’s Coroutines design.[FunDSP 0.18](https://github.com/SamiPerttu/fundsp): FunDSP is an audio DSP ([digital signal processing](https://en.wikipedia.org/wiki/Digital_signal_processing)) library for audio processing and synthesis. This release is a rewrite that adds no_std and SIMD support.

## Interviews [#](https://gamedev.rs#interviews)

![Arcade cabinet close up](../../assets/d30d67f11a34b4ce.jpg)

[Metalmancy](https://www.micronote.tech/) are creating custom and configurable arcade machines. Their flagship game [Thetawave](https://store.steampowered.com/app/2427510/Thetawave) is coded in Rust.

Hyelim of [Framework](https://frame.work) interviewed Carlo and Joanna on their games
and arcade machines at [OpenSauce](https://opensauce.com/).

![An idyllic scenery made in Tidy Glade](../../assets/8c91703d6a7fd95a.jpg)

To celebrate the release of Tiny Glade’s [demo version](https://store.steampowered.com/app/2198150/Tiny_Glade/), Pounce Light’s Anastasia Opara and
Tomasz Stachowiak have joined 80 Level [in an interview](https://80.lv/articles/exclusive-tiny-glade-developers-discuss-bevy-proceduralism-publishers-cozy-games) to discuss the game’s history, proceduralism,
Bevy, Rust, self-publishing, and the “cozy games” genre.

## Blog Posts [#](https://gamedev.rs#blog-posts)

[This post](https://dioxus.notion.site/Dioxus-Labs-High-level-Rust-5fe1f1c9c8334815ad488410d948f05e) by the founder of [Dioxus Labs](https://dioxuslabs.com/) is a direct response to
the recently published [“Leaving Rust gamedev after 3 years”](https://loglog.games/blog/leaving-rust-gamedev/) by LogLogGames.
If you’ve missed the original post, it has made its rounds as a well-written critique of Rust’s gamedev ecosystem and shortcomings
inherent to the language itself.

[Dioxus Labs + “High-level Rust”](https://dioxus.notion.site/Dioxus-Labs-High-level-Rust-5fe1f1c9c8334815ad488410d948f05e) is a detailed response to the original post, outlining concrete steps to improve the situation
and signaling the author’s readiness to fund the development of features they see as necessary for the ecosystem to thrive.

*Discussions: lobste.rs,
/r/rust,
Hacker News*

### Virtual Geometry in Bevy 0.14 [#](https://gamedev.rs#virtual-geometry-in-bevy-0-14)

![The Stanford bunny split into meshlets](../../assets/1b9e256c5459b7df.jpg)

Ever wondered how [Unreal 5’s Nanite](https://dev.epicgames.com/documentation/en-us/unreal-engine/nanite-virtualized-geometry-in-unreal-engine) works under the hood?
Jasmine, who reimplemented the virtual geometry technology for Bevy’s upcoming 0.14 release,
wrote a [post](https://jms55.github.io/posts/2024-06-09-virtual-geometry-bevy-0-14/) explaining the concepts and the nitty-gritty details of the implementation.
The post is very technical in nature, so if you’ve never heard of this technology before,
they recommend you first watch Brian Karis’ SIGGRAPH 2021 lecture [A Deep Dive into Nanite Virtualized Geometry](https://www.youtube.com/watch?v=eviSykqSUUw) ([slides](https://advances.realtimerendering.com/s2021/Karis_Nanite_SIGGRAPH_Advances_2021_final.pdf)).

## Jobs [#](https://gamedev.rs#jobs)

Ubisoft Montreal is searching for an [online Rust programmer](https://www.ubisoft.com/en-us/company/careers/search/743999993500090-programmer-online-unannounced-project)
for an unannounced project.

## Engine Newsletters [#](https://gamedev.rs#engine-newsletters)

- This Week In Bevy
- This Week In Quads

## Future News [#](https://gamedev.rs#future-news)

Editing this newsletter wouldn’t be possible without [your contributions](https://github.com/rust-gamedev/rust-gamedev.github.io/pulls?q=is%3Apr+in%3Atitle+%27N52%27).
Thanks to everyone who helped us this month!

If you want something mentioned in the next newsletter, [send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

You can also get an early look at pending issues for the [next newsletter](https://github.com/rust-gamedev/rust-gamedev.github.io/pulls?q=is%3Apr+in%3Atitle+%27N53%27).

That’s all news for today, thanks for reading!

Also, subscribe to our socials if you want to receive fresh news!

- X/Twitter:
[@rust_gamedev](https://twitter.com/rust_gamedev) - Mastodon:
[@rust_gamedev](https://mastodon.gamedev.place/@rust_gamedev) - Reddit:
[/r/rust_gamedev](https://reddit.com/r/rust_gamedev)

**Discuss this post on**:
[/r/rust_gamedev](https://www.reddit.com/r/rust_gamedev/comments/1dudvrk/this_month_in_rust_gamedev_june_edition_released/),
[Lemmy](https://lemmy.world/post/17176132),
[Mastodon](https://mastodon.gamedev.place/@rust_gamedev/112722731870962460),
[X/Twitter](hhttps://x.com/rust_gamedev/status/1808489666426851340),
[Hacker News](https://news.ycombinator.com/item?id=40865690),
[Discord](https://discord.gg/yNtPTb2).