---
title: 'This Month in Rust GameDev #32 - March 2022'
url: https://gamedev.rs/news/032/
author: Rust GameDev WG
published: '2022-04-11'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 32nd issue of the Rust GameDev Workgroup’s
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

[Rust GameDev Podcast](https://gamedev.rs/news/032/#rust-gamedev-podcast)[Rust GameDev Meetup](https://gamedev.rs/news/032/#rust-gamedev-meetup)[Game Updates](https://gamedev.rs/news/032/#game-updates)[Learning Material Updates](https://gamedev.rs/news/032/#learning-material-updates)[Engine Updates](https://gamedev.rs/news/032/#engine-updates)[Tooling Updates](https://gamedev.rs/news/032/#tooling-updates)[Library Updates](https://gamedev.rs/news/032/#library-updates)[Other News](https://gamedev.rs/news/032/#other-news)[Requests for Contribution](https://gamedev.rs/news/032/#requests-for-contribution)[Jobs](https://gamedev.rs/news/032/#jobs)

![text logo](../../assets/20d10db4323440e0.jpeg)


The Rust Gamedev Podcast features interviews with indie game developers creating titles with the Rust programming language. It covers technical topics as well as the business of open source and commercial indie games development.

In March, two episodes were released:

[The seventh episode](https://rustgamedev.com/episodes/interview-with-fish-fight) is a chat with Erlend and Ole about
[Fish Fight](https://github.com/heroiclabs/fishgame-macroquad), open source games development, and future game spin-offs.

[In the eighth episode](https://rustgamedev.com/episodes/interview-with-dustin-a-b-street), Forest chats to Dustin about [A/B Street](https://github.com/a-b-street/abstreet).

Listen and Subscribe from the following platforms:
[Rust GameDev Podcast (simplecast)](https://rustgamedev.com/),
[Apple Podcasts](https://podcasts.apple.com/gb/podcast/rust-game-dev/id1526304768),
[Spotify](https://open.spotify.com/show/7HRfGnTcXkLkQd9fxJbDGj),
[RSS Feed](https://feeds.simplecast.com/C6NQglnL),
or [Google Podcasts](https://podcasts.google.com/feed/aHR0cHM6Ly9mZWVkcy5zaW1wbGVjYXN0LmNvbS9DNk5RZ2xuTA).

## Rust GameDev Meetup [#](https://gamedev.rs#rust-gamedev-meetup)

![Gamedev meetup poster](../../assets/8ae071c46e0b4449.png)


The 14th Rust Gamedev Meetup took place in March. You can watch the
recording of the meetup [here on Youtube](https://youtu.be/dQPkyjbd36Y). The meetups
take place on the second Saturday every month via the [Rust Gamedev Discord
server](https://discord.gg/yNtPTb2) and are also [streamed on
Twitch](https://twitch.tv/rustgamedev).

## Game Updates [#](https://gamedev.rs#game-updates)

![Bevy Jam](../../assets/3afdfd40b8286ad2.png)


Voting on the first-ever [Bevy Jam](https://itch.io/jam/bevy-jam-1/) just finished! It was a
week-long event, where the goal was to make a game in
[Bevy Engine](https://bevyengine.org/), the free and open-source game engine
built in Rust. The theme was ‘Unfair Advantage’.

The [full results can be found on itch.io](https://itch.io/jam/bevy-jam-1/results), and you can read
an [exploration of the entries](https://techgeneral.org/bevy-jam-1-data-exploration/) to find out about how
these entries used different asset formats, crates, and Bevy features.

Here are the top five games:

#### 🥇 First Place: [Petty Party](https://jabuwu.itch.io/petty-party) [#](https://gamedev.rs#1st-place-medal-first-place-petty-party)

![Petty Party logo](../../assets/15a8e96a53a71e76.png)


[Petty Party](https://jabuwu.itch.io/petty-party) is a Mario Party inspired board game,
in which you play against the world’s worst opponent, who’s
actively rigging the game against you.

The game was originally very hard to beat, so the devs balanced the jam release fairly heavily in the player’s favour - however, if you beat the game, you can unlock the original difficulty as a ‘hard mode’!

The source for the game is available on [GitHub](https://github.com/jabuwu/petty-party).

#### 🥈 Second Place: [¿Quién es el MechaBurro?](https://ramirezmike2.itch.io/quien-es-el-mechaburro) [#](https://gamedev.rs#2nd-place-medal-second-place-quien-es-el-mechaburro)

![¿Quién es el MechaBurro?](../../assets/1ec336e906ef073d.gif)


[¿Quién es el MechaBurro?](https://ramirezmike2.itch.io/quien-es-el-mechaburro) is a singleplayer/local
multiplayer game (up to 4 players) with bots (8 total burros)
inspired by twin-stick shooters and aspects of Mario Kart. Players
choose to play as one of the burro piñatas and then attempt to be
the last burro standing in each level of the game. At the start
of each round, one burro is chosen randomly to be upgraded to the
Mechaburro, giving them an unfair advantage.

A postmortem devlog detailing the process of making the game during the
jam can be found [here](https://ramirezmike2.itch.io/quien-es-el-mechaburro/devlog/354715/bevy-jam-1-postmortem), a trailer for the game is
[viewable on YouTube](https://www.youtube.com/watch?v=YQeb2ffm_TI) and the source code for the game
is available [on GitHub](https://github.com/ramirezmike/quien_es_el_mechaburro).

![Chaz screenshot](../../assets/8adb6362c3cbe3db.png)


[Chaz](https://luizchagasjardim.itch.io/chaz) is a platform racing game, where you have to stay close to your
opponent in order to see where you’re going. Beat them to the floating
heart to win - but be warned, once you do, they’ll steal your moves!

The source code is available on [GitHub](https://github.com/lcjgames/chaz).

#### Fourth Place: [Warlock’s Gambit](https://gibonus.itch.io/warlocks-gambit) [#](https://gamedev.rs#fourth-place-warlock-s-gambit)

![Warlock’s Gambit Screenshot](../../assets/a5f8001d69ff42e8.jpg)


[Warlock’s Gambit](https://gibonus.itch.io/warlocks-gambit) is a puzzle game constructed like a
card game, playable in the browser. You are given a static deck and have to play
your cards carefully to beat your opponent. In keeping with the theme of the
jam, the decks are stacked against you. In fact, it’s impossible to win by
default. But you have a trick up your sleeve, literally. You can drag a card in
your sleeve to play it later.

The jam release was limited and confusing, but a post-jam update fixed the most annoying bugs, clarified the game rules, enabled importing custom decks, and added great code documentation (including a flow diagram demonstrating the game state changes).

The game code is licensed under MIT or Apache-2 and is [available on
GitHub](https://github.com/team-plover/warlocks-gambit).

#### Fifth Place: [Cheaters Never Win](https://cdsupina.itch.io/cheaters-never-win) [#](https://gamedev.rs#fifth-place-cheaters-never-win)

![Clip of Cheaters Never Win gameplay](../../assets/1befff582285d716.gif)


[Cheaters Never Win](https://cdsupina.itch.io/cheaters-never-win) is an unfairly difficult
infinite runner set in a cyberpunk world.

Collect keycaps in order to unlock cheat codes, which will give you access to forbidden powers - like jumping, and moving left!

Since the jam, the team has begun work on a full release for the game.

The source for this game is available on [GitHub](https://github.com/Corrosive-Games/Cheaters-Never-Win).

![VRacer screenshot](../../assets/78aeca78203511cd.gif)

V-Racer ([GitHub](https://github.com/Syn-Nine/rust-mini-games/tree/main/2d-games/vracer)) by
[@Syn-Nine](https://twitter.com/Syn9Dev) is a retro
drift racing game inspired by Atari
Battlezone and Wipeout, created using
Syn9’s [Rust Mini Game Framework](https://github.com/Syn-Nine/mgfw).
The game is part of an open source
[repository](https://github.com/Syn-Nine/rust-mini-games/) of several
mini-games that use this framework.

![hho screenshot](../../assets/1eae4eb98a695150.png)


Harvest Hero Origins by Gemdrop Games is an Arcade Wave Defense game featuring a co-op survival mode.

[Gemdrop Games](https://twitter.com/GemdropGames) collaborated with [Pixadome](https://www.pixadome.com/) to bring
their featured character Blue
from [Chenso Club](https://store.steampowered.com/app/1454730/Chenso_Club/) to the survival roster. Please go wishlist Chenso Club
to support the developers!

Blue is an android who wields a chainsaw to rip and tear through her enemies.
Slice and dice, then ride through enemies
in the new [Spring Fever expansion](https://store.steampowered.com/news/app/1651500/view/3112556530755817232)!

![Veloren on the Steam Deck](../../assets/b1e3faa5a3898923.jpg)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In March, Veloren was tested on the SteamDeck, which you can read about in
detail in [the weekly devblog](https://veloren.net/devblog-162#veloren-on-steamdeck-by-angelonfira). Lots of work was done
with Airshipper, Veloren’s launcher, including some bug fixes, but mainly the
switch to GitHub Releases as the download backend. This will make game updates
significantly faster and more reliable for players. Work is also being done to
make use of GitHub’s HTTP range requests to do partial patches where possible.
Audio work was done to improve swimming sounds playing unevenly, and more sounds
to gliding.

Veloren was also mentioned [on Hacker News](https://news.ycombinator.com/item?id=30667022), and lots of great
discussions happened in the comment section. In 2021, Veloren spoke at Rust in
Arts, and [the recording has recently been posted](https://rustfest.global/session/53-directors-commentary-veloren/). The
0.13 release map is in the works, with a jungle theme. CliffTowns are being
developed, as a new town located in the mountains. Veloren recorded another
reading club episode, this time about [Tracy and
optimizations](https://www.youtube.com/watch?v=-w0yTCjsV0k). A new series was also started, and the
first [Veloren Code Review was recorded](https://www.youtube.com/watch?v=gomKwQnEGA8).

March’s full weekly devlogs: “This Week In Veloren…”:
[#162](https://veloren.net/devblog-162),
[#163](https://veloren.net/devblog-163),
[#164](https://veloren.net/devblog-164),
[#165](https://veloren.net/devblog-165).

![rust-nonogram screenshot](../../assets/0a74d09cf57ce115.png)


Nonograms (AKA Picross) are logic puzzles that involve filling in cells on a
grid. The goal of [rust-nonogram](https://github.com/henryksloan/rust-nonogram) is to be a quick and engaging time-killer.
Featuring random puzzles and simple controls, it is a great way to have some
fun and test your skills.

![A screenshot looking down on mountainous terrain and an ocean](../../assets/921c306b3784d737.jpg)


“Terrain Generator” is a website made by [@kettlecorn](https://twitter.com/kettlecorn) that
generates procedural island landscapes. It uses WebAssembly SIMD and multithreading
via WebWorkers to speed up generation.

The terrain is generated with multi-octave simplex noise using the new
simplex-noise crate [ clatter](https://ianjk.com/terrain_generator/).

Terrain Generator’s code is open-sourced on [GitHub](https://github.com/kettle11/open_world_game).

![way of rhea capsule image](../../assets/44ea1b7c87f3aad1.jpg)


[Way of Rhea](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n32) is a puzzle adventure with hard puzzles and forgiving
mechanics being produced by [@masonremaley](https://twitter.com/masonremaley) in a custom Rust
engine. It has a demo available [on Steam](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n32).

Latest developments:

- A
[new demo](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n32)was pushed to Steam for PAX East - The
[mushroom biome](https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/clans/35599024/f356b295d6d71dcaebf4727eca0317269172b1d7.png)art was completed - All puzzles for the main game are complete
- More secrets have been added
- Four out of the five
[characters](https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/clans/35599024/4dbe4158059559176d25f4d9326280d83ec6c745.png)are now in the game `SDL_mixer`

was replaced with a custom Rust mixer built on top of[libsoundio](http://libsound.io/)- Numerous minor bug fixes and quality of life improvements, you can find
[more details here](https://store.steampowered.com/news/app/1110620/view/3180112431320346739?utm_campaign=tmirgd&utm_source=n32&utm_content=news)

You can stay up to date with the latest Way of Rhea developments by
[following it on Steam](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n32), signing up for [their mailing list](https://www.anthropicstudios.com/newsletter/signup),
or joining [their Discord](https://discord.gg/JGeVt5XwPP).

## Engine Updates [#](https://gamedev.rs#engine-updates)

![godot-rust logo](../../assets/a36ed4bc24b3186d.png)


godot-rust ([GitHub](https://github.com/godot-rust/godot-rust), [Discord](https://discord.com/invite/FNudpBD), [Twitter](https://twitter.com/GodotRust))
is a Rust library that provides bindings for the Godot game engine.

We are pleased to announce the release of godot-rust version 0.10.0.
This update brings many new quality-of-life features, such as basic
async and serde support, more flexible exporting of Rust symbols to
Godot, better CI and doc integration, among many more features that
have previously been exclusive to the [GitHub repo](https://github.com/godot-rust/godot-rust).

This release also makes the API much more user-friendly than previous versions with more consistent naming, flatter module structure and fewer redundancies.

Thank you to all of the contributors who made this possible!

A full list of the changes is available in the [changelog](https://github.com/godot-rust/godot-rust/blob/master/CHANGELOG.md).

![notan](../../assets/7b1174037e3c6420.jpg)


[Notan](https://github.com/Nazariglez/notan) is a simple and portable layer designed to create your own multimedia
apps on top of it without worrying about platform-specific code.

The main goal is to provide a set of APIs and tools that can be used to create your project in an ergonomic manner without enforcing any structure or pattern, always trying to stay out of your way. The idea is that you can use it as a foundation layer or backend for your next app, game engine, or game.

Version [v0.2.1](https://github.com/Nazariglez/notan/releases/tag/v0.2.0) improves and adds features focusing on the creation of apps,
like select mouse cursor or lazy loop among other things. The main focus was
to improve the integration with [egui](https://github.com/emilk/egui) supporting all its features.

[Tetra](https://github.com/17cupsofcoffee/tetra) is a simple 2D game framework, inspired by XNA, Love2D, and Raylib. This
month, Tetra 0.7 was released, featuring:

- Support for a wider variety of texture formats
- A more powerful API for blending
- Lots of bug fixes, cleanups, and improvements

For more details, see the [changelog](https://github.com/17cupsofcoffee/tetra/blob/main/CHANGELOG.md).

As mentioned in previous newsletters, this is likely to be the final release of
Tetra, as [the developer has decided to move onto other projects](https://www.seventeencups.net/posts/three-years-of-tetra/).

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

![Bevy video series title](../../assets/42d72742ea33768e.jpg)


Matthew Bryant ([Youtube](https://www.youtube.com/channel/UC7v3YEDa603x_84PgCPytzA),
[GitHub](https://github.com/mwbryant)) has been working on a video series on using
Bevy to create a Pokemon-style RPG, and just released four episodes. The goal is
to show and explain all the core features of Bevy while creating a real game
over ten 10-15 minute videos, currently releasing once per week. There is also
an accompanying [blog post](https://www.logicprojects.net/2022/03/) for the first video in the
series.

The [Bevy Cheatbook](https://bevy-cheatbook.github.io) by Ida Iyes is an unofficial reference-style book
teaching the Bevy game engine. It got many improvements over the past month.

There is a new [guided tutorial page](https://bevy-cheatbook.github.io/tutorial.html), to help you navigate
the book in an order that makes sense for learning, starting from beginner
topics and progressing towards more advanced! There is also a new “getting
started” page, as an alternative to Bevy’s official instructions.

New topics added to the book: working with Bevy Time/Timers/Stopwatches, ECS data storage kinds, exclusive systems, direct World access, non-Send types, and more…

Many pages have been overhauled for correctness and the quality of various code examples improved.

If you would like to support the project, donate to the author via
her [GitHub Sponsors](https://github.com/sponsors/inodentry). Follow [@IyesGames on
Twitter](https://twitter.com/IyesGames) for updates.

## Tooling Updates [#](https://gamedev.rs#tooling-updates)

![A screenshot of Bloom3D’s interface and a simple low-polygon building.](../../assets/75e39e9502e1e792.jpg)


[Bloom3D](https://bloom3d.com) is an extremely minimalist in-browser 3D modeling tool made
by [@kettlecorn](https://gamedev.rs/news/032/kettlecorn_twitter)
that released earlier this month.

Bloom3D is built completely with Rust from the user interface to core algorithms.
The game engine and many of the libraries powering Bloom3D are open-sourced on [GitHub](https://github.com/kettle11/koi).

![The logo for Noumenal, a colorful cube with spheres on each corner and a spherical hole in the center, and “Noumenal” written underneath.](../../assets/0aea8e83aa807395.jpg)


[Noumenal](https://noumenal.app) ([Discord](https://discord.gg/PFeZQE48gG),
[Twitter](https://twitter.com/noumenal_app)) by [@HackerFoo](https://hackerfoo.com) is a beautiful
and fast 3D modeling app for iOS.

Noumenal officially went into [public beta](https://testflight.apple.com/join/I6x5Yksx) this week, and so was
presented to a larger audience for the first time.

The goals of Noumenal are:

- Enjoyable to use on a mobile device
- Accessible to as many people as possible
- Real-time solid modeling with boolean operations
- Non-destructive editing and robustness to prevent data loss
- Intuitive manipulation by projecting from the screen glass into 3D space
- Export to the most widely used formats, such as glTF, USDZ, and STL for 3D printing

These goals have led to a unique interface.

![Graphite](../../assets/359db3141720722f.png)


Graphite is an in-development raster and vector 2D graphics editor that is free and open source. It will be powered by a node graph compositing engine that supercharges your layer stack, providing a completely non-destructive editing experience.

With the completion of the node graph UX design, work has begun building the
frontend and backend systems for the big leap to node-driven vector editing.
This works by composing groups of Rust functions together at runtime and/or
compile time. [Watch the (brief) talk](https://youtu.be/okWFrfaaADs?t=4014) about how
the backend implementation works around challenges imposed by Rust.

New editor features this month include importing bitmap image layers and
customizing stroke styling with dashed lines and rounded or beveled corners.
The [project website](https://graphite.rs) is also now mostly content-complete,
including new node graph mockups.

Check out the [new website](https://graphite.rs), try the
[Graphite editor](https://editor.graphite.rs) right now in your browser, star on
[GitHub](https://github.com/GraphiteEditor/Graphite), follow on [Twitter](https://twitter.com/GraphiteEditor), and join the
[Discord](https://discord.graphite.rs) to chat or get involved!

## Library Updates [#](https://gamedev.rs#library-updates)

![An animated gif depicting a simple match 3 game where gems are matched in sets of 3 or more and new gems drop down to take their place](../../assets/fb52be7112f21059.gif)


[bevy_match3](https://crates.io/crates/bevy_match3) ([GitHub](https://github.com/Sheepyhead/bevy_match3))
by [@Sheepyhead](https://twitter.com/devsheepy)
is an event-based Bevy crate for handling the logic side of match 3 games so
you can worry about making everything else!

This was recently released in its first public version, so there are several parts to improve, and it could really use some battle testing.

![Screenshot of example “rotozoom” from dos-like-rs, depicting a rotating tile grid of Ferris.](../../assets/be15595a204edbce.png)


[dos-like-rs](https://github.com/Enet4/dos-like-rs) by [@E_net4](https://twitter.com/E_net4)
provides Rust bindings to Mattias Gustavsson’s `dos-like`

,
a cross-platform framework for writing modern applications
with the look & feel of MS-DOS programs from the early 90’s.

A few technical details about the conception of these bindings
are presented in a [blog post on Dev.to](https://dev.to/e_net4/writing-bindings-to-dos-like-for-rust-some-lessons-learned-2p6k).

[Kira](https://github.com/tesselode/kira) by [@tesselode](https://twitter.com/tesselode) is a backend-agnostic library to create expressive audio
for games. It provides parameters for smoothly adjusting properties of sounds, a
flexible mixer for applying effects to audio, and a clock system for precisely
timing audio events.

v0.6.0 is a complete rewrite with a more elegant API, support for streaming sounds,
swappable backends, and more flexible mixer routing. See the full [changelog](https://github.com/tesselode/kira/releases/tag/v0.6.0) for
more details.

[Screen 13](https://github.com/attackgoat/screen-13) is an easy-to-use 2D/3D rendering engine in the spirit of QBasic. The
library provides a thin Vulkan 1.1 driver using smart pointers and a fully-generic
render graph structure.

Earlier this year [Screen 13](https://github.com/attackgoat/screen-13) was updated with a dynamic graph pattern, but there
was no good starter documentation and a few bugs. There is a [getting started](https://github.com/attackgoat/screen-13/blob/master/examples/getting-started.md)
guide now! Also, a ton of new features have been added in the last month:

- ImGui support
- Mac support
- Shader specialization

For more details, see the [changelog](https://github.com/attackgoat/screen-13/blob/master/CHANGELOG.md).

## Other News [#](https://gamedev.rs#other-news)

- Other game updates:
[Space Frontiers](https://github.com/starwolves/space)posted[a video](https://www.youtube.com/watch?v=EF5iUJNFz94)of their Atmospherics update.

- Other learning material updates:
[Hedgein](https://www.youtube.com/watch?v=qufQVtlYqrQ)started a ‘making one game per week’ YouTube series.


## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[Graphite is looking for contributors](https://github.com/GraphiteEditor/Graphite/issues/202)to help build the new node graph and 2D rendering systems.[winit’s “difficulty: easy” issues](https://github.com/rust-windowing/winit/issues?q=is%3Aopen+is%3Aissue+label%3A%22difficulty%3A+easy%22).[Backroll-rs, a new networking library](https://github.com/HouraiTeahouse/backroll-rs/issues).[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[A/B Street’s “good first issue” issues](https://github.com/a-b-street/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/D-Good-First-Issue).

## Jobs [#](https://gamedev.rs#jobs)

[DIMS](https://www.dims.co/jobs)(Stockholm/Remote)- Tools Programmer
- Internship: Game Design

[Embark Studios](https://careers.embark-studios.com/jobs)(Stockholm/Hybrid Remote)- Various roles


That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!

**Discuss this post on**:
[/r/rust_gamedev](https://www.reddit.com/r/rust_gamedev/comments/u1hfpf/this_month_in_rust_gamedev_32_march_2022/),
[Twitter](https://twitter.com/rust_gamedev/status/1513623277427728389),
[Discord](https://discord.gg/yNtPTb2).