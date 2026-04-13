---
title: 'This Month in Rust GameDev #50 - April 2024'
url: https://gamedev.rs/news/050/
author: Rust GameDev WG
published: '2024-05-03'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 50th issue of the Rust GameDev Workgroup’s
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

[Announcements](https://gamedev.rs/news/050/#announcements)[Game Updates](https://gamedev.rs/news/050/#game-updates)[Engine Updates](https://gamedev.rs/news/050/#engine-updates)[Learning Material Updates](https://gamedev.rs/news/050/#learning-material-updates)[Library Updates](https://gamedev.rs/news/050/#library-updates)[Other News](https://gamedev.rs/news/050/#other-news)[Discussions](https://gamedev.rs/news/050/#discussions)

## Announcements [#](https://gamedev.rs#announcements)

*Please fill out this survey before skipping this section! More info below!*

Hey everyone, it’s been a while! As you’ve certainly noticed, the newsletter has
been on hiatus for a while. The reason was mostly maintainer burnout, which is also
why the newsletter of August 2023 was not published [until a few days
ago](https://gamedev.rs/news/049/).

We’re back now though! A couple of community members, Jan Hohenheim
([@janhohenheim](https://github.com/janhohenheim)) and Thierry Berger ([@Vrixyz](https://github.com/Vrixyz)), have led the revival of the
newsletter. This includes making changes requested by the community, and
improving sustainability for the long term.

You can read more about the changes being made in [this blog
post](https://gamedev.rs/blog/newsletter-changes/).

### Community Survey [#](https://gamedev.rs#community-survey)

This restructuring is also a good time to improve the content of the newsletter.
We’ve got some community feedback on the [Rust GameDev Discord](https://discord.gg/game-development-in-rust-676678179678715904) already
and would like to hear more from you. It would be great if you could fill out
[this survey](https://forms.gle/oeSb46twWsxRKYJe7) to let us know how we can improve the newsletter going
forward. The survey closes on the **28th of May**. We will be evaluating the
[survey](https://forms.gle/oeSb46twWsxRKYJe7) results in an upcoming blog post, so stay tuned for that.

That’s all for now. Have fun reading!

## Game Updates [#](https://gamedev.rs#game-updates)

[Way of Rhea](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n50) just got a release date: it will be coming to Steam on
**May 20th, 2024**!

Way of Rhea ([Steam](https://store.steampowered.com/app/1110620/Way_of_Rhea/)) is a color-based puzzle game with difficult puzzles, but forgiving
mechanics being developed by [@masonremaley](https://twitter.com/masonremaley) in a custom Rust engine.

You can support development by [wishlisting Way of Rhea on Steam](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n50), or
[signing up for the mailing list](https://anthropicstudios.com/newsletter/signup/tech).

Recently, a [closed beta](https://store.steampowered.com/news/app/1110620/view/7665759271877780609) began. All characters now have voices, and various [speedrunning features](https://clan.cloudflare.steamstatic.com/images//35599024/6ee82d4e0105f073082c83626e37933e682b5936.png) were added.
Older CPUs are [now supported](https://store.steampowered.com/news/app/1110620/view/4118050466869150657).
Secrets were made harder, and an [in-game achievement UI](https://clan.cloudflare.steamstatic.com/images//35599024/573f81c1ebce54d9efedcd693fcbe684a5629c7f.png) was created.

For the full changelog, see the [release notes](https://store.steampowered.com/news/app/1110620).

![Super Mario 64 JavaScript Archive](../../assets/a184903b8c197465.jpg)


[SM64JSARCHIVE](https://sm64jsarchive.com) is an actively maintained fork of [sm64js](https://github.com/sm64js/sm64js/tree/MMO): a decompilation project of Super Mario 64 to JavaScript.
Additional sidenote: The MMO servers are not always running for sm64jsarchive.

The backend server, which is written in Rust,
is now live at [https://sm64jsarchive.com](https://sm64jsarchive.com)

A successful stress test for the MMO feature was run on April 10th.

![OpenCombat: demo available soon](../../assets/c9c7db01b4654ec1.jpg)

Open Combat ([GitHub](https://github.com/buxx/OpenCombat), [Discord](https://discord.gg/6P2vtFh2Px)) is a real-time tactical game
which takes place during World War II.

The basic game logic and HUD are now complete, and the high-definition map for the demo is finished.

Some things are missing, like high-definition assets for soldiers or minimal AI for opponents.
But the [demo is playable](https://github.com/buxx/OpenCombat/releases) and the team would love to hear your feedback!

![Times of Progress: an isometric city builder game set during the industrial revolution](../../assets/8cd1afc29a83d50d.jpg)


Times of Progress ([Steam](https://store.steampowered.com/app/2628450/Times_of_Progress/), [Twitter/X](https://twitter.com/ElmoSampedro), [Mastodon](https://mastodon.online/@elmowilk))
is an upcoming city builder game set during the industrial revolution.

In April, they added lots of UI widgets and improved performance by refactoring the orders system.

The demo is not available yet but interested players can sign up for the upcoming closed beta by joining the [newsletter](https://subscribepage.io/pressingthumbs).

### Monk Tower [#](https://gamedev.rs#monk-tower)

![Monk Tower Screen shot](../../assets/cad892c313ed9a46.png)


Monk Tower ([itch.io](https://maciekglowka.itch.io/monk-tower), [Google Play](https://play.google.com/store/apps/details?id=com.maciejglowka.monk_tower), [Github](https://github.com/maciekglowka/tower-rl))
is a tiny coffee-break roguelike game, intended for short runs (ca. 15mins).

The gameplay is quite distilled and revolves mostly around resource management. The player has limited inventory capacity and the weapons get damaged after each use. There are 20 randomly generated levels to beat.

It is available on desktop (Windows / Linux), Android, and Web (mobile friendly). The game’s source code also comes with a custom WGPU-based 2D framework.

*Discussions: ( /r/roguelikes)*

### You are Merlin [#](https://gamedev.rs#you-are-merlin)

![You are Merlin screenshot](../../assets/e2658f818c3196a2.png)


You are Merlin ([Web Game](https://hseager.github.io/you-are-merlin-www/), [GitHub - Rust/CLI](https://github.com/hseager/you-are-merlin), [GitHub - WASM](https://github.com/hseager/you-are-merlin-www)) by [@hseager](https://github.com/hseager)
is a text adventure game that compiles to both CLI and WebAssembly.

This initial version features a main quest, side quests, items, and a boss fight. Players can choose their favourite visual theme such as Zelda, Warcraft, and Fallout. The web version also supports mobile devices.

Although fairly simple, this first version provides a good foundation for building more features in later updates.

*Discussions: ( /r/rust_gamedev)*

![Machine Gun and Periscope](../../assets/fe89093f46bc6325.png)

[Jumpy](https://github.com/fishfolks/jumpy) ([GitHub](https://github.com/fishfolks/jumpy), [Discord](https://discord.gg/4smxjcheE5), [Twitter](https://twitter.com/spicylobsterfam)) by
[Spicy Lobster](https://spicylobster.itch.io/) is a pixel-style, tactical 2D shooter with a fishy
theme.

This month the base functionalities of round scoring and map transitions have been implemented. New weapons such as the Blunderbuss, Periscope, and Machine Gun are ready for fish-on-fish combat.

Jumpy is now featuring corpse physics and a “ragdoll” button to send your Fish [flopping about](https://github.com/fishfolk/jumpy/pull/932).

On the treasure map for the near future is improving UX and new player experience, polish and improvements on match scoring / round transitions, and more awesome weapons.

## Engine Updates [#](https://gamedev.rs#engine-updates)

### Bottomless-Pit 0.3 [#](https://gamedev.rs#bottomless-pit-0-3)

![The Bottomles-Pit Logo. A small hole in the ground with cat ears and text saying bottomless-pit](https://eggshark.dev/images/bplogo.png)


Bottomless-Pit is a 2d game engine written with WGPU that has been around for a year, which can be found on [crates.io](https://crates.io/crates/bottomless-pit) and [GitHub](https://github.com/EggShark/bottomless-pit).
Very recently a 2d camera was added as well as WASM and web support.
Current development is being focused on stability and QoL changes like texture sampling options and improved input.
You can check out several [engine examples on the web](https://eggshark.dev/bp-examples).
Since the engine is in its infancy, its developer calls for developers to use it and give the engine some feedback.

Current features are:

- Custom Shader Support
- Basic rendering
- Text rendering
- Input and window event handling

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

### Building games for Android with Rust [#](https://gamedev.rs#building-games-for-android-with-rust)

[@maciekglowka](https://github.com/maciekglowka) has recently shared some thoughts [on their blog](https://maciejglowka.com/blog/building-games-for-android-with-rust/) about building Rust games
for Android. Rather than a step-by-step guide, it is a collection
of issues one can possibly encounter when targeting Android.

Topics mentioned:

- ‘Window’ creation (via winit)
- Android app’s lifecycle vs. the WGPU surface creation
- User data storage
- System UI hiding via jni and Android API
- Building AAB files to meet Google Play requirements

### Bevy: A case study in ergonomic Rust [#](https://gamedev.rs#bevy-a-case-study-in-ergonomic-rust)

[Chris Biscardi](https://www.youtube.com/c/chrisbiscardi) was at RustNation UK recently and gave talk on Bevy’s
Rusty ergonomics titled [Bevy: A case study in ergonomic Rust](https://www.youtube.com/watch?v=CnoDOc6ML0Y).
In their own words:

There are at least two, if not three, talks worth of material around how Bevy progressively discloses complexity across multiple “stacks” of APIs; and the work done so far is very impressive in terms of how it all fits together, especially as a large-and-growing OSS project.


### Reactivity in Bevy: From the Bottom Up [#](https://gamedev.rs#reactivity-in-bevy-from-the-bottom-up)

[Talin](https://dreamertalin.medium.com/) wrote a three-part series on [“Reactivity in Bevy: From the Bottom Up”](https://machinewords.hashnode.dev/reactivity-in-bevy-from-the-bottom-up-part-1),
which describes the workings of `bevy_reactor`

, an experimental, work-in-progress framework for doing reactive programming within Bevy.

## Library Updates [#](https://gamedev.rs#library-updates)

### Jolt Bindings [#](https://gamedev.rs#jolt-bindings)

[Lucian Greathouse](https://lpg.space/) has published their [Jolt](https://github.com/jrouwe/JoltPhysics) bindings for Rust. Jolt is a C++ physics engine you might know from its use in Horizon: Forbidden West.
Lucian has previously worked on [JoltC](https://github.com/SecondHalfGames/JoltC), a C API for Jolt, which this project uses in the background.

The bindings work can be found on the [just-rust GitHub repo](https://github.com/SecondHalfGames/jolt-rust) GitHub repository and come in two flavors:

`joltc-sys`

: Unsafe bindings to the C API`rolt`

: Ergonomic and safe Rust API

### Hexx 0.17 [#](https://gamedev.rs#hexx-0-17)

Hexx, the popular crate for hexagonal tools, [has released version 0.17](https://github.com/ManevilleF/hexx/releases/tag/0.17.0).
This release has a strong focus on performance:

- Large performance improvement on various computations like rings and wedges
- Add support for optimized storage for hexagonal and rhombus-shaped maps
- Added support for rectiline path

And utility:

- Added a 13th example showcasing all natively supported shapes
- Removed confusing items

[lightyear_website](https://github.com/cBournhonesque/lightyear) is a comprehensive networking library for bevy to make multiplayer games.
It comes with multiple types of transports (WebTransport, WebSocket, UDP, etc.)
and supports replication techniques like client-side prediction, server interpolation, interest management, and more!
Check out the [examples](https://github.com/cBournhonesque/lightyear/tree/main/examples)!

The latest release, [0.13](https://github.com/cBournhonesque/lightyear/releases/tag/0.13.0), brings two big new features:

**Steam support**: you can now use the Steamworks SDK as your transport layer, which lets you use the Valve network! Note that lightyear supports running multiple transports in parallel, so it’s possible to have cross-play between Steam and non-Steam users.**Listen-server mode**: it is now possible to run a server and a client in the same process/bevy app. This can be useful to avoid the costs of a dedicated server, or to have a similar codebase between singleplayer and multiplayer.

## Other News [#](https://gamedev.rs#other-news)

- Alice I. Cecile of the Bevy Foundation would like to collect community feedback
on game development in Rust. Please fill out
[her survey](https://forms.gle/kLzv5Ww3U8dLGUHU8)!

## Discussions [#](https://gamedev.rs#discussions)

LogLog games has published a [very well-written blog post](https://loglog.games/blog/leaving-rust-gamedev/) about their reasons to leave Rust gamedev.
It talks about shortcomings in Rust as a language in general and as a game development tool in particular.
Some insights into the limitations of ECS are also provided. Some interesting community discussions have been sparked by this post:

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!

**Discuss this post on**:
[/r/rust_gamedev](https://www.reddit.com/r/rust_gamedev/comments/1cja5v8/this_month_in_rust_gamedev_april_edition_released/),
[rust@lemmy.ml](https://lemmy.ml/post/15196466),
[Hacker News](https://news.ycombinator.com/item?id=40248347),
[Mastodon](https://mastodon.gamedev.place/@rust_gamedev/112377678490780983),
[Twitter](https://twitter.com/rust_gamedev/status/1786406704629829935),
[Discord](https://discord.gg/yNtPTb2).