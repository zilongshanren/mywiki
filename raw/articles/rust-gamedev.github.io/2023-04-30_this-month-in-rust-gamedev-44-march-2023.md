---
title: 'This Month in Rust GameDev #44 - March 2023'
url: https://gamedev.rs/news/044/
author: Rust GameDev WG
published: '2023-04-30'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 44th issue of the Rust GameDev Workgroup’s
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

[Announcements](https://gamedev.rs/news/044/#announcements)[Game Updates](https://gamedev.rs/news/044/#game-updates)[Engine Updates](https://gamedev.rs/news/044/#engine-updates)[Learning Material Updates](https://gamedev.rs/news/044/#learning-material-updates)[Tooling Updates](https://gamedev.rs/news/044/#tooling-updates)[Library Updates](https://gamedev.rs/news/044/#library-updates)[Other News](https://gamedev.rs/news/044/#other-news)[Discussions](https://gamedev.rs/news/044/#discussions)[Requests for Contribution](https://gamedev.rs/news/044/#requests-for-contribution)

## Announcements [#](https://gamedev.rs#announcements)

### Rust GameDev Meetup [#](https://gamedev.rs#rust-gamedev-meetup)

![Gamedev meetup poster](../../assets/93b05c908d44c9bf.png)


The 25th Rust Gamedev Meetup took place in March. You can watch the recording
of the meetup [here on Youtube](https://youtube.com/watch?v=EVxjxP6sZtA). Here was the schedule
from the meetup:

- Blue Engine -
[@aryanpur_elham](https://twitter.com/aryanpur_elham) - Blade -
[@kvark](https://kvark.github.io/) - 8bit Duels -
[@ThousandthStar](https://github.com/ThousandthStar) - Veloren -
[@velorenproject](https://twitter.com/velorenproject) - Graphite -
[@GraphiteEditor](https://twitter.com/GraphiteEditor)

The meetups take place on the second Saturday of every month via the [Rust
Gamedev Discord server](https://discord.gg/yNtPTb2) and are also [streamed on
Twitch](https://twitch.tv/rustgamedev).

## Game Updates [#](https://gamedev.rs#game-updates)

![movement_animations](../../assets/f36b463ad8e743df.png)

[@ThousandthStar](https://github.com/ThousandthStar) is creating a simple multiplayer turn-based strategy using the
[Bevy Engine](https://bevyengine.org/). The [latest devlog](https://thousandthstar.github.io/posts/8bd/8bd-part6) brings features like ownership indicators,
movement and attack animations, and a chat system.

The game is under development. The [8-bit Discord](https://discord.com/invite/NbBcF4bGU5) is the best place to talk
about the game.

8bit Duels will be getting UI updates next, and the first version should release soon after that. Other troops are coming as well.

*Discussions: 8-bit Discord*

![Hit and blackhole particle effects](../../assets/cc0dbd30b68d3af9.gif)

CyberGate ([YouTube](https://youtube.com/channel/UClrsOso3Xk2vBWqcsHC3Z4Q), [Discord](https://discord.gg/R7DkHqw7zJ)),
an ambitious multiplayer project in development by CyberSoul,
aims to invite players into a constantly evolving universe.
Harnessing the power of procedural generation and artificial intelligence,
this work-in-progress aspires to provide an engaging experience
that emphasizes exploration and discovery across its diverse worlds.

The latest updates to CyberGate include:

- Skybox Animation and Transitions
- Dynamic Point Lights
- Particle System
- Post-processing Screen Shake for Hit Feedback
- Hit Particle Effects
- Blackhole

They released the 7th major update in March,
They are now working on universe generation alghoritms for the 8th.
Participate [by joining the Discord server](https://discord.gg/R7DkHqw7zJ).

![A person in a red suit shooting zombies with a pistol](../../assets/4efde9e300508b84.png)


[ZOMBIE DEMO GAME](https://lpghatguy.itch.io/zombie-demo-game) is a small third-person zombie shooter by [@LPGhatguy](https://twitter.com/LPGhatguy) and
[@evaera](https://twitter.com/evaeraevaera) that was released this month.

It features an astonishing 10 minutes of gameplay, a built-in level editor, and zombies! It was produced in order to practice shipping a game and uses a custom engine using wgpu, hecs, and lots of other great crates from the ecosystem.

ZOMBIE DEMO GAME is available for Windows and Linux
[on itch.io](https://lpghatguy.itch.io/zombie-demo-game) today.

*Discussion: Twitter*

### Shifting Chamber [#](https://gamedev.rs#shifting-chamber)

![Shifting Chamber Screen shot](../../assets/bd9d082222dbbdfb.png)


Shifting Chamber ([itch.io](https://maciekglowka.itch.io/shifting-chamber),
[GitHub](https://github.com/maciekglowka/shifting_chamber)) is a simple tactics game where
the player, instead of moving the character, manipulates the map around it.
The goal is to defeat the enemies by forcing them into hazardous
positions - since they cannot be attacked directly.

The game is in an early prototype / proof of concept phase. It is written with the help of the Bevy engine. There is currently only a WASM build (freely available on the itch.io)

![Live Map Editing Example](../../assets/1c5af3355a342692.gif)

[Jumpy](https://github.com/fishfolks/jumpy) ([GitHub](https://github.com/fishfolks/jumpy), [Discord](https://discord.gg/4smxjcheE5), [Twitter](https://twitter.com/spicylobsterfam)) by
[Spicy Lobster](https://spicylobster.itch.io) is a pixel-style, tactical 2D shooter with a fishy
theme.

In the last month, the first [MVP release](https://github.com/fishfolk/jumpy/releases/tag/v0.6.0) of Jumpy was made. The
release adds some major new features including a live map editor, critters,
extended player animations, and basic AI. Soon afterward [an update](https://github.com/fishfolk/jumpy/releases/tag/v0.6.1)
was made with revised maps and some important bug fixes.

Along with the release is a new blog post, sharing thoughts on some of the lessons
learned during development:
[Jumpy v0.6 Retrospective](https://fishfolk.org/blog/jumpy-0-6-retrospective/).

The efforts are now focused on getting network play implemented, with a two player LAN proof-of-concept already working. The hope is to get the remaining network issues fixed and the online matchmaker connected before making another release as soon as it’s ready.

![Tunnet screenshot: a weird looking computer network](../../assets/b21da96e031189b8.jpg)

Tunnet ([Steam](https://store.steampowered.com/app/2286390/Tunnet), [Itch.io](https://puzzled-squid.itch.io/tunnet)) by
[@puzzled_squid](https://puzzledsquid.xyz) is a short puzzle/exploration game where you
build a computer network in an underground complex.

This project is still WIP and the first [devlog](https://puzzled-squid.itch.io/tunnet/devlog/507508/devlog-0-gameplay-loop-and-subnetworks) has been
posted this month. The post describes the main gameplay loop as well as some
of the new environments recently added.

The game is developed using Bevy and is expected to be released late 2023.

### Digital Extinction [#](https://gamedev.rs#digital-extinction)

![Building Placement in Digital Extinction](../../assets/2692e5cf662bd80e.jpeg)

[Digital Extinction](https://de-game.org) ([GitHub](https://github.com/DigitalExtinction/Game), [Discord](https://discord.gg/vHMFuCWGSX),
[Reddit](https://reddit.com/r/DigitalExtinction)) by [@Indy2222](https://github.com/Indy2222) is a 3D real-time strategy game made with
[Bevy](https://bevyengine.org).

The most notable updates are:

- simple unit manufacturing was added,
- game minimap was added,
- game end detection was implemented,
- shadows were enabled,
- the health of all units & buildings was decreased,
- the “Quit Game” button in the game menu leads to the main menu instead of the termination of the application,
- close button was added to all menu screens,
- maximum number of players was made configurable by each map,
- screen edge size for camera movement was decreased,
- malformed configuration does not lead to a crash but a toast with an error message is displayed.
[Bevy](https://bevyengine.org)was upgraded to v0.10.

See [gameplay](https://youtu.be/_ibNMDgIQDE) screen recordings on YouTube.

More detailed monthly updates are available [here (March)](https://mgn.cz/blog/de05/) and
[here (April)](https://mgn.cz/blog/de06/).

[Way of Rhea](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n44) is a puzzle game with hard puzzles and forgiving
mechanics being produced by [@masonremaley](https://twitter.com/masonremaley) in a custom Rust
engine. You can support development by
[checking out the free demo and wishlisting on Steam](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n44)!

Recent updates:

- Undo/redo is better tutorialized.
- Existing onboarding hints were improved both functionally and visually.
- New onboarding hints were added to ensure new players understand that teleporters are interactive.
- Various performance improvements were made.
- End-game puzzles were completed.
- Work has begun on laying out the end-game art.
- A release plan has been drafted.
- Way of Rhea was shown at PAX West.
- Way of Rhea will be part of the upcoming
[Steam Puzzle Fest](https://partner.steamgames.com/doc/marketing/upcoming_events/themed_sales/puzzle_2023)!



![Screenshot from the game Boat Journey showing ASCII art of a boat and some islands](../../assets/a97c4f0248e13f1c.png)

[Boat Journey](https://gridbugs.itch.io/boat-journey) ([GitHub](https://github.com/gridbugs/boat-journey))
is a turn-based game where you drive a boat through a
procedurally-generated landscape on a voyage along a river destined for the
ocean. Accept passengers to have them help you on your journey. Fight monsters,
collect junk, trade the junk for fuel, use the fuel to travel to the ocean.

Features:

- Large procedurally-generated world
- Turn the boat at 45-degree increments
- Text-only graphics. You can play it in a terminal if you like!
- Hand-drawn ansi-art character portraits
- You can take on a ghost as a passenger and then become a ghost yourself.

Boat Journey was made for the [7 Day Roguelike 2023](https://itch.io/jam/7drl-challenge-2023) game jam.
The devlog is [here](https://www.gridbugs.org/7drl2023-day1/).

![Screen Ball](../../assets/6f69935f48ecb89d.png)


[Screen Ball](https://github.com/NightsWatchGames/screen-ball) ([GitHub](https://github.com/NightsWatchGames/screen-ball), [YouTube](https://youtube.com/watch?v=pKV6fTmJfmE)) by [@lewiszlw](https://github.com/lewiszlw)
is a game that lets you play ball on screen for a rest when you’re tired from work.
Inspired by the video published by Bevy community member PaulH#7052.

![Battle City](../../assets/7ef5f20e8752bf11.png)


[Battle City](https://github.com/NightsWatchGames/battle-city) ([GitHub](https://github.com/NightsWatchGames/battle-city), [YouTube](https://youtube.com/watch?v=54Z2WBFZfzA)) by [@lewiszlw](https://github.com/lewiszlw)
is a Bevy clone of the classical Battle City game
- which brought a lot of happiness to the author’s childhood.

You can play it [here](https://nightswatchgames.github.io/games/battle-city/).

![3D view on a two-weeled robot on a hex map](../../assets/9e0cf3935adc8488.jpg)

[BattleBots Simulator](https://twitter.com/nilay_savant/status/1632419019914645504) ([Twitter](https://twitter.com/nilay_savant/status/1632419019914645504)) by [@nilaysavant](https://github.com/nilaysavant)
is a “BattleBots” themed robot wars simulator developed using [Bevy](https://bevyengine.org).

The game is planned to have multiple combat arenas. Each player can compete using their selected robot. Players will be able to score and win by damaging and destroying opponent robots. Or by knocking opponents out of the arena.

There are 3 variants of the robots planned as follows:

- Light Weight “Annoyance”: Low mass/HP, but will be unpredictable and fast. It will slowly kill by consistently annoying and damaging opponents.
- Medium Weight “Sniper”: Medium weight robot that will be equipped with a high boost. This will allow it to knockout opponents or push them out of the arena.
- Heavy Weight “TANK”: Highest mass/HP and momentum. Slow moving but hard to kill. Equipped with magnetic wedges that will help pin/push opponents out of the arena.

The game is currently a work in progress. For updates follow [Nilay Savant](https://twitter.com/nilay_savant) on Twitter.

*Discussions: Twitter*

### Cargo Space [#](https://gamedev.rs#cargo-space)

![Screenshot of Cargo Space’s friends list context menu: “invite to lobby” is highlighted](../../assets/d8678f085b37db29.png)


[Cargo Space](https://helsing.studio/cargospace) ([Discord](https://discord.gg/ye9UDNvqQD)) by
[@johanhelsing](https://mastodon.social/@johanhelsing) is a co-op 2d space game where you build
a ship and fly it through space looking for new parts, fighting pirates and the
environment.

This month’s development was all about lobbies, chat and integrating with Steam. This spawned a couple of new micro-crates.

[bevy_crossbeam_event](https://github.com/johanhelsing/bevy_crossbeam_event) lets you spawn Bevy events by
sending to a crossbeam channel, which is convenient with callbacks that require
move semantics, such as those in bevy-steamworks.

[steam_dev_launcher](https://github.com/johanhelsing/steam_dev_launcher) is a cross-platform binary crate all
about dev-friendly ways to launch your game through Steam. That is: without
losing logs, panic traces, and optionally using a custom binary or setting extra
environment variables (launch from `/target/debug/your_game`

).

Read more about all this in [this month’s devlog entry](https://johanhelsing.studio/posts/cargo-space-devlog-5).

![OpenCombat HUD: a window with a "Begin" button](../../assets/93d5251fde4fda6d.png)

Open Combat ([Website](https://opencombat.bux.fr/), [GitHub](https://github.com/buxx/OpenCombat),
[Discord](https://discord.gg/6P2vtFh2Px)) is a real-time tactical game
which takes place during the 2nd World War.

Some major changes this month :

- Add basic HUD logic for troops and game management
- Add high definition assets management for zoom display

High-definition infantry sprites integration if planned for next month and we are searching for graphic designer help.

![Campfire by the lights](../../assets/e8c5d1d8f6bab673.jpg)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In March, culling of underground terrain was added, improving rendering speeds. There has been a large influx of player growth, which has been rallying the focus on server optimizations. Optimizations for buffs and auras were added, specifically around how much network bandwidth is being used. A visual guide of Veloren was created, which should help onboard new players to the game. It covers items such as basic controls, what to do when you start the game, basic crafting, and much more. More work has gone into the real-time simulation system improvements. It includes behaviour of where birds should fly to, and how species repopulation works.

March’s full weekly devlogs: “This Week In Veloren…”: [#207](https://veloren.net/devblog-207).

![Gamplay demo: square grid, red/blue mages moving around and attacking each other](../../assets/fbc31bb4c3c7df19.gif)


[Maginet](https://evrimzone.itch.io/maginet) by [Evrim](https://twitter.com/evrimzone) is a fast-paced turn-based strategy game
with local/versus-ai/online play on PC/mobile
where two guilds of mages battle each other.

This month’s updates include:

![A castle scene showcasing new editing features](../../assets/a45270f12f77070d.gif)


[Tiny Glade](https://store.steampowered.com/app/2198150/Tiny_Glade) ([Twitter](https://twitter.com/PounceLight), [Youtube](https://youtube.com/@pouncelight)) is a small relaxing game
about doodling castles. This month’s updates include:

- New shapes, including dedicated circle and rectangle shapes.
- Alignment and snapping helpers for the freeform walls.
- Improved robustness of “wall mess” handling algorithm.

Read more in their latest [Steam blogpost](https://store.steampowered.com/news/app/2198150/view/3681169040455721390).

Anastasia also posted [a cool thread](https://twitter.com/anastasiaopara/status/1634633463247560704) about their approach
to marketing and promotion of the project.

![Drawning animation](../../assets/77722189a16f1d9b.gif)


[Infinilands](https://store.steampowered.com/app/1882900/Infinilands) by [@FluffyCreature](https://twitter.com/FluffyGameDev) is a WIP pixel art sandbox survival game:

Infinilands is a pixel art sandbox survival game that lets you explore and modify a procedurally generated world full of unique plants, creatures and ruins. You can build houses and fight monsters with your friends in online/split-screen co-op. This game also supports dedicated server.


This month’s updates include:

[Water logic](https://twitter.com/FluffyGameDev/status/1636004535117180928).- Auto-tiling for both
[normal](https://twitter.com/FluffyGameDev/status/1633856225598160898)and[block](https://twitter.com/FluffyGameDev/status/1637166713249624066)placement modes.

## Engine Updates [#](https://gamedev.rs#engine-updates)

![code in the editor on the left and live scene view with textured shapes on the right](../../assets/bcbf45c709d469ee.jpg)

[hotline](https://github.com/polymonster/hotline) ([Blog](https://polymonster.co.uk), [Twitter](https://twitter.com/polymonster))
is a modern, high-performance, hot-reload
graphics engine written in Rust. It aims to provide low-level access to modern
graphics API features, while at the same time providing high-level ergonomic
optimizations.

It uses Bevy’s ECS so the focus can remain primarily on the graphics architecture. Direct3D12 is the only supported platform, but the graphics API is abstracted to account for future ports to Vulkan and Metal. The project is in its early stages but already has a decent amount of features showcasing different render strategies, async command buffer generation, plugin based architecture, and hot-reload support for Rust code, HLSL shaders, and render configs. It supports ImGui with docking and multiple windows, video decoding, complex image loading (cubemaps, arrays, volumes), and more.

[@polymonster](https://github.com/polymonster) has been live streaming development on [Twitch](https://twitch.tv/polymonstr)
with archives available on [YouTube](https://youtube.com/channel/UCQRmui5w4Urz-h4P9CL7rmA).
Recently they have been designing a bindless material system.

![bevy ruins](../../assets/42a056fbd021e43b.jpg)


[Bevy](https://bevyengine.org) is a refreshingly simple data-driven game engine built in Rust.
It is [free and open-source](https://github.com/bevyengine/bevy) forever!

Bevy 0.10 brought many incredible new features.
You can check out the [full release blog post here](https://bevyengine.org/news/bevy-0-10),
but here are some highlights:

[ECS Schedule v3](https://bevyengine.org/news/bevy-0-10/#ecs-schedule-v3)[Cascaded Shadow Maps](https://bevyengine.org/news/bevy-0-10/#cascaded-shadow-maps)[Environment Map Lighting](https://bevyengine.org/news/bevy-0-10/#environment-map-lighting)[Depth and Normal Prepass](https://bevyengine.org/news/bevy-0-10/#depth-and-normal-prepass)[Smooth Skeletal Animation Transitions](https://bevyengine.org/news/bevy-0-10/#smooth-skeletal-animation-transitions)[Improved Android Support](https://bevyengine.org/news/bevy-0-10/#improved-android-support)[Revamped Bloom](https://bevyengine.org/news/bevy-0-10/#revamped-bloom)[Distance and Atmospheric Fog](https://bevyengine.org/news/bevy-0-10/#distance-and-atmospheric-fog)[StandardMaterial Blend Modes](https://bevyengine.org/news/bevy-0-10/#standardmaterial-blend-modes)[More Tonemapping Choices](https://bevyengine.org/news/bevy-0-10/#more-tonemapping-choices)[Color Grading](https://bevyengine.org/news/bevy-0-10/#color-grading-control)[Parallel Pipelined Rendering](https://bevyengine.org/news/bevy-0-10/#parallel-pipelined-rendering)[Windows as Entities](https://bevyengine.org/news/bevy-0-10/#windows-as-entities)[Renderer Optimizations](https://bevyengine.org/news/bevy-0-10/#renderer-optimizations)[ECS Optimizations](https://bevyengine.org/news/bevy-0-10/#ecs-optimizations)

*Discussions:
/r/rust,
Hacker News,
Twitter*

[Fyrox](https://fyrox.rs) ([GitHub](https://github.com/FyroxEngine/Fyrox), [Discord](https://discord.com/invite/xENF5Uh), [Twitter](https://twitter.com/DmitryNStepanov))
is a game engine that aims to be easy to use and provide a large set
of out-of-the-box features. This month’s highlights include:

[Basic Android support](https://fyrox.rs/blog/post/twif17#basic-android-support)for GLES3.0+ devices - usable but the renderer lacks mobile-specific optimizations.[Lightmapper fixes](https://fyrox.rs/blog/post/twif17#lightmapper-fixes).[Blend shapes](https://fyrox.rs/blog/post/twif18#blend-shapes)allows to dynamically change 3D meshes (useful for facial animation, etc).- Fyrox now uses
[tinyaudio](https://github.com/mrDIMAS/tinyaudio)as[its sound output backend](https://fyrox.rs/blog/post/twif18#audio-improvements).

*Discussions: /r/rust_gamedev*

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

### Developing an editor with egui [#](https://gamedev.rs#developing-an-editor-with-egui)

![Gif displaying the functionality of the editor](../../assets/73ee17d403fc698b.gif)


[@TheGrimsey](https://mastodon.social/@TheGrimsey) published a three-part series of articles about developing a Spell
Editor with egui.

[“Databases & Editors (1/3)”](https://thegrimsey.net/2023/03/07/Bevy-Four-Editor.html)covers displaying egui windows & tables of entries.[“Editors (2/3): Editing entries”](https://thegrimsey.net/2023/03/12/Bevy-Five-Editor-Two.html)elaborates on handling editing of entries & properties such as enums.- Finally,
[“Editors (3/3): Selection dialog & new entries”](https://thegrimsey.net/2023/03/21/Bevy-Six-Editor-Three.html)talks about developing a selection dialog and creating new entries.



![Title slide from presentation about writing NES assembly programs in Rust](../../assets/1ed18acb75d217d0.jpg)

This is a talk about writing a program for the Nintendo Entertainment System that exposes all of its audio processor registers through an interface that lets the user flip bits using the controller and hear the result in real-time. The program is written in Rust using an Embedded Domain-Specific Language. The talk demonstrates the features of the language and how they can be used to help express NES assembly programs in Rust.

Some features of the EDSL:

- defining and calling assembly functions by string labels
- using Rust as a powerful macro language (e.g. generate code inside a for-loop)
- using Rust’s type system to catch invalid combinations of instruction and addressing mode

The source code for the NES program described in the talk is
[here](https://github.com/gridbugs/nes-audio-playground) and there is a [demo of the tool on
youtube](https://youtube.com/watch?v=QHoISiWdPXo). The PDF of the slides from the talk are
[here](https://raw.githubusercontent.com/gridbugs/nes-programming-in-rust-sydney-rust-meetup-2023-03-01/main/slides.pdf).

![depth prepass in bevy 0.10](../../assets/dda2c3bc502b8a16.jpg)

[@chrisbiscardi](https://hachyderm.io/@chrisbiscardi) published a [video](https://youtube.com/watch?v=3OHaEVHahIg) about
using the Depth Prepass texture in Bevy 0.10. The depth prepass, along with the
normal prepass, are new passes in Bevy 0.10 that allow you to access distance
from the camera and normal direction for a particular pixel on the screen. The
textures created by these passes can then be used to power effects in your own
custom shaders.

*Discussions: YouTube,
Mastodon*

![a render near the final state of /r/place](../../assets/fb03c4c22b93cb4e.jpg)


[@codetheweb](https://github.com/codetheweb) published an [article](https://maxisom.me/posts/applying-5-million-pixel-updates-per-second) that explores the
basics of wgpu by optimizing a program that replays [/r/place](https://reddit.com/r/place/). By the end,
CPU usage is around 18-25% while applying an average of 5m pixel updates per
second at 10,000x playback speed.

*Discussions:
/r/rust,
/r/rust_gamedev*

[Matthew Bryant](https://youtube.com/@logicprojects) released [a video](https://youtu.be/luyDgccpHgE)
focused on the design and implementation of a dialog system for NPCs
in his [RPG game](https://github.com/mwbryant/logic-turn-based-rpg). This is the 4th in a weekly series about
the high level ECS design of a full game using Bevy.

## Tooling Updates [#](https://gamedev.rs#tooling-updates)

![Tiger screenshot: classuic UI layout](../../assets/a4146cd85da18bae.png)


Tiger ([GitHub](https://github.com/agersant/tiger),
[itch.io](https://agersant.itch.io/tiger) by
[@agersant](https://mastodon.gamedev.place/@agersant) is a visual tool to
author game spritesheets and their metadata.

Version 1.0 launched this month, which means Tiger is ready for production. It currently has the following features:

- Easy-to-use timeline to author animation.
- Supports perspectives for any 2D game (top-down, sidescroller, isometric, etc.).
- Automatically hot-reloads source images when they are changed.
- Packs animation frames into texture atlases.
- Can add and tag hitboxes.
- Flexible template system exports metadata in any text-based format.
- Free and open-source with a permissive license.

![Tarsila's UI](../../assets/5b435dcce295bf1a.png)

Tarsila is a pixel art and spritesheet editor written in Rust using
egui and [macroquad](https://github.com/not-fl3/macroquad), inspired by [Aseprite](https://www.aseprite.org/).
The first public release (0.1.0) has been published on March 18th,
with [basic features](https://github.com/yds12/tarsila/blob/master/docs/user_guide.md).

Since the publication not many new features have been added, mostly bugfixes and an overhaul of the input system, in preparation for configurable shortcuts (via a text file and later GUI).

In the [roadmap](https://github.com/yds12/tarsila/blob/master/ROADMAP.md) for 0.2.0 are things like color
effects (change hue, saturation, etc.), ovals and circles, and more.

We welcome [contributions](https://github.com/yds12/tarsila/blob/master/CONTRIBUTING.md)! Big thanks to contributors
@quiet-bear and @crumblingstatue.

![Rerun’s new select & hover highlights in a browser](../../assets/ace44711c7aa2dfa.gif)


Rerun ([Discord](https://discord.gg/npTFxYR9),
[GitHub](https://github.com/rerun-io/rerun), [Website](https://rerun.io))
is an open-source SDK for logging complex visual data paired with a visualizer
for exploring that data over time. While its primary focus is on robotics and
computer vision, it can be useful for all kinds of
rapid prototyping & algorithm development.

Three new versions got released since the last newsletter!
[0.5.0](https://github.com/rerun-io/rerun/releases/tag/v0.5.0)
is now latest. A few of the biggest highlights:

- The web-viewer is, while still experimental & unpolished, now stable.
[Try it out here!](https://app.rerun.io) - Rerun can now be embedded in Jupyter notebooks
- Depth textures can now directly be visualized with point clouds and have a variety of color map settings.
- Selection/hover highlights use now outlines for better visibility and in order to avoid changing the visualization itself.
- Picking is now done on the GPU, fixing many issues of the previous system
- All color-mapping is now done on-the-fly on the GPU, faster & less memory use
- Support for mesh vertex colors.
[New example](https://github.com/rerun-io/rerun/blob/main/examples/python/opencv_canny/main.py)of forever-streaming a web-camera image to Rerun.- Major improvements to the data store for better performance and memory usage

There’s a growing community on [Discord](https://discord.gg/npTFxYR9)
waiting for you to join in case you have any questions,
comments or just want to follow the latest development.
The [GitHub project](https://github.com/rerun-io/rerun) is MIT/Apache
licensed and open to contribute for everyone,
be it with suggestions, bugs or PRs.

![Vector artwork made in Graphite: Valley of Spires](../../assets/7b831b94ab575fbd.png)

Graphite ([website](https://graphite.rs), [GitHub](https://github.com/GraphiteEditor/Graphite),
[Discord](https://discord.graphite.rs), [Twitter](https://twitter.com/GraphiteEditor)) is a free,
in-development raster and vector 2D graphics editor based around a Rust-powered
node graph compositing engine.

March’s [sprint 24](https://github.com/GraphiteEditor/Graphite/milestone/24) brings forth:

- Vector nodes: A major refactor moves vector shape layers into the node graph.
Now the
*shape*,*transform*,*fill*, and*stroke*are all set via nodes in the graph. Text is the final remaining holdout and will be node-ified next, letting the node graph act as the universal layer type.

As always, new contributors are kindly invited to
[get involved](https://graphite.rs/contribute) and take on
[approachable issues](https://github.com/GraphiteEditor/Graphite/labels/Good%20First%20Issue) with help from the
project’s friendly and supportive developer community on Discord.

[Open Graphite](https://editor.graphite.rs) in your browser and start creating! Share your
designs with #MadeWithGraphite on Twitter.

![new text input support on mobile devices](../../assets/fc29cdf298e518e3.jpg)

[Ruffle](https://ruffle.rs) is an open-source Flash Player emulator, written in Rust. It aims to run
natively on all modern operating systems and web browsers, leveraging Rust’s
memory safety guarantees to avoid the security pitfalls that Flash became
notorious for in its later years.

[This month’s updates](https://ruffle.rs/blog/2023/03/12/progress-report.html) include:

- Significant improvements to AVM1 engine accuracy fix dozens upon dozens of ActionScript 2 games.
- Work on the AVM2 (ActionScript 3) backend
[is also speeding up](https://ruffle.rs/avm2.html), a bunch of AS3 games are now playable. - Better mobile devices support: text input boxes and iOS a context menu.

[Check out the blog post](https://ruffle.rs/blog/2023/03/12/progress-report.html) for more details.

![screenshot: a bunch of minimalist vehicle assets](../../assets/a8c3ea60a817be15.png)


Orlop by [Tim Rach](https://timrach.de) is a media management tool for anyone who works
with a large asset library on a daily basis.

Organise and browse your asset collection with built-in tagging, search and preview functionality. Automatic tagging requires no effort - just import your asset folder and go!


The beta version is available [on itch.io](https://tirch.itch.io/orlop)
or [through Testflight](https://orlop.dev#beta).

![Foxtrot in Action](../../assets/220f5b9aeb86a748.gif)


Jan Hohenheim’s ([@janhohenheim](https://github.com/janhohenheim)) [Foxtrot](https://github.com/janhohenheim/foxtrot), the all-in-one for the Bevy engine,
has reached its [0.2 milestone](https://github.com/janhohenheim/foxtrot/milestone/2).
Thanks to feedback, contributions and crates from the community, it has now
reached a fairly stable state. While there used to be a major change every week
before, the project will limit itself to updating only minor things during a
Bevy version lifecycle and do major reworks only in time for new versions.

So, if anyone was eyeing it but was turned off by the frequent big changes or the lack of some features, now is the time! Version 0.2.0 includes the following cool new features compared to 0.1.0:

- Wasm support, with
[a live demo here](https://janhohenheim.github.io/foxtrot). If the mouse lock doesn’t work, spam “Esc” a bunch of times 😉 - Beautiful grass through
[warbler_grass](https://crates.io/crates/warbler_grass) - Buttery smooth cameras through
[bevy_dolly](https://github.com/BlackPhlox/bevy_dolly) - Dynamic pathfinding through
[oxidized_navigation](https://crates.io/crates/oxidized_navigation) - Simplified error handling through
[bevy_mod_sysfail](https://crates.io/crates/bevy_mod_sysfail) - Easy to write plugins through
[seldom_fn_plugin](https://crates.io/crates/seldom_fn_plugin) - Sprinting particles through
[bevy_hanabi](https://github.com/djeedai/bevy_hanabi) - A demo scene with houses (CC0 if you want to reuse them)
- A dialog that gets draws letter-by-letter and is nicer to look at
- Better documentation

Thanks also to [bevy_game_template](https://github.com/NiklasEi/bevy_game_template),
without which Foxtrot would not be possible in the first place! And thanks
to PhaestusFox, who [made a video about the template](https://youtube.com/watch?v=MsYX4he_z_8)

## Library Updates [#](https://gamedev.rs#library-updates)

![Screenshot of 1-bit sprites drawn using bevy_text_mode.](../../assets/5e8bb70664022b42.png)


[bevy_text_mode](https://crates.io/crates/bevy_text_mode) ([GitHub](https://github.com/yopox/bevy_text_mode)) by [yopox](https://github.com/yopox) is a Bevy plugin that
makes it possible to set the background and the foreground color of a texture atlas
sprite (built-in Bevy sprites only have a tint property).
This plugin is convenient when using 1-bit tilesets such as [MRMOTEXT](https://mrmotarius.itch.io/mrmotext).

The 0.1 release adds a `TextModeTextureAtlasSprite`

component with
configurable background, foreground, x/y flip and opacity.

*Discussion: Mastodon*

### Matchbox [#](https://gamedev.rs#matchbox)

![matchbox logo](../../assets/0ddf1db9dee090b4.png)


[Matchbox](https://github.com/johanhelsing/matchbox) is a library for easily establishing unreliable, unordered,
peer-to-peer WebRTC data connections using rust WASM (and native). This enables
cross-platform low-latency multiplayer games.

Previously, the socket opened a single udp-like data channel. In version 0.6, however, support for adding extra channels with configurable ordering and package retransmits was added. This enables direct p2p tcp-like connections as well.

Two new crates were added in this release. matchbox_signaling, lets you set up a custom signaling server, also supporting client-server topologies, enabling scenarios where one player acts as the host for the other players.

bevy_matchbox provides ergonomic usage with Bevy. Severely cutting down on the boiler-plate needed.

The tutorial series on [how to make a p2p web game with Bevy, GGRS and
Matchbox](https://johanhelsing.studio/posts/extreme-bevy) was also updated to the latest versions of all three
libraries.

Read more about all the new features in the [0.6 release post](https://johanhelsing.studio/posts/matchbox-0-6).

*Discussions:
/r/rust,
/r/rust_gamedev,
/r/bevy,
Mastodon*

![hot-rebuild](../../assets/cdc0b1af00c07b87.gif)

[Bevy Rust-GPU](https://github.com/bevy-rust-gpu) by [@Shfty](https://github.com/Shfty)
is a suite of crates encoding a practical [rust-gpu](https://github.com/EmbarkStudios/rust-gpu) workflow for [bevy](https://bevyengine.org).

The latest release brings new GPU interop traits, shader macro robustness,
and compatibility with [bevy](https://bevyengine.org) 0.10 and [rust-gpu](https://github.com/EmbarkStudios/rust-gpu) 0.6.
Further development continues apace, with major improvements to the SPIR-V
interchange pipeline, shader compilation machinery, and support code already merged.

The project is still in development, and presently relies on custom forks of the associated crates. However, various PRs have been filed upstream to build out a robust interchange between them, with the hope of mainline compatibility - and a corresponding crates.io release - sometime in the future.

In particular, [@eddyb](https://github.com/eddyb) deserves special thanks for his work on the [rust-gpu](https://github.com/EmbarkStudios/rust-gpu) side,
which has enabled and informed many of the improvements tabled for the next release,
and greatly accelerated the process of making Rust a viable shading language
for users of Bevy and WGPU.

*Discussion: /r/bevy*

![3d-distance-field](../../assets/0a52f0cbffbec76d.gif)

Announcing [rust-gpu-sdf](https://github.com/bevy-rust-gpu/rust-gpu-sdf), by [@Shfty](https://github.com/Shfty); a no-std signed distance field library
designed for use on both CPU and GPU.

[Signed distance fields](https://en.wikipedia.org/wiki/Signed_distance_function) are a powerful computational tool
that allows a surface to be represented by a function from position to distance.
This has [intuitive applications](https://iquilezles.org/articles/raymarchingdf) in various domains such as rendering,
collision, meshing, and volume modeling, providing the means to represent analytically
smooth geometry, dynamic morphing (as pictured), and various other effects
that would traditionally require specialized tools to model.

[rust-gpu-sdf](https://github.com/bevy-rust-gpu/rust-gpu-sdf) aims to enumerate this domain to the fullest extent allowed
by Rust’s type system, lifting its traditionally monolithic implementation style
into a set of intuitive composable operators, and leveraging a natural synergy
with functional programming to provide powerful compositional tools.

Contrary to its working title, [rust-gpu-sdf](https://github.com/bevy-rust-gpu/rust-gpu-sdf) is actually [rust-gpu](https://github.com/EmbarkStudios/rust-gpu)-agnostic,
so can be used anywhere Rust can;
it’s presently named as such due to being built as the primary consumer of [bevy-rust-gpu](https://github.com/bevy-rust-gpu),
with a view to providing a performant and compositional way to compile SDFs
into SPIR-V for rendering on the GPU.

It’s presently in a heavy-development prerelease state, so watch this space!

![Differently pixelated foxes](../../assets/a4fd089837143412.jpg)


Jan Hohenheim ([@janhohenheim](https://github.com/janhohenheim)) recently published a new crate called [pixelate_mesh](https://github.com/janhohenheim/pixelate_mesh).
It is a Bevy plugin that provides a Pixelate component that one can add to any
entity holding a mesh or a scene, which it will then pixelate without any post-processing.
The idea is to recreate the effect seen in [Prodeus](https://youtube.com/watch?v=Vb-hPYOIwMw).

## Other News [#](https://gamedev.rs#other-news)

- Other game updates:
[Combine&Conquer v0.5](https://buckmartin.de/combine-and-conquer/2023-03-08-v0.5.0.html)brings multi cursor support, the ability to turn structures on/off, and a view that shows your factory’s production stats.[bevy-rust-wasm-experiments](https://reddit.com/r/bevy/comments/11o5pve/bevy_wasm_and_accelerometer)is a small video game with Bevy that compiles both to desktop and WASM and showcases how you can get input from your smartphone’s accelerometer.[vustnexus](https://twitter.com/SethMadDev/status/1631357764495630336)is a side-scroller about surviving and defeating the infect of the Vust Swarm![The Beat Of Space](../../assets/bbbbaba5bdeda127.img)is a space-themed rhythm game built with[macroquad](https://github.com/not-fl3/macroquad).[Pirate Annihilation posted the second YouTube devlog](https://youtube.com/watch?v=udR3kzrDnAc)about the switch from 2D to 3D, hexagonal map, and new camera.

- Other learning material updates:
[PhaestusFox posted more YouTube videos](https://youtube.com/@PhaestusFox/videos)about Bevy.[s0lly shared a video on creating transparent windows using Bevy](https://youtube.com/watch?v=gymEcIAi_J8).[An article about creating a Snake game](https://medium.com/comsystoreply/creating-a-small-game-with-webassembly-and-rust-20c6945efa1d)for the browser with WASM and Rust.[@whoisryosuke released a tutorial](https://whoisryosuke.com/blog/2023/getting-started-with-egui-in-rust)on getting started with egui in Rust.

- Other engine updates:
[Tetra v0.8](https://twitter.com/17cupsofcoffee/status/1636706157568962563)brings a bunch of small API improvements and bugfixes. The engine is still in maintainence-only mode though.

- Other tooling updates:
[@Setzer22 shared a demo](https://mastodon.gamedev.place/@Setzer22/110011331330540420)of how smooth subdivision works in the Blackjack editor.[Epic Asset Manager](https://github.com/AchetaGames/Epic-Asset-Manager)is an unofficial client to install Unreal Engine, download and manage purchased assets, projects, plugins and games from the Epic Games Store.- Asahi Linux (Linux distro for Apple Silicon Macs)
[uses Rust in their Vulkan drivers](https://reddit.com/r/rust/comments/11wosur/vulkan_on_asahi_linux). [forerunner](https://dev.to/heavyrain266/forerunner-a-storytelling-platform-for-composing-souls-like-action-rpgs-4p9k)is a WIP storytelling platform for composing Souls-like Action-RPGs using the cloud infrastructure and Pixar’s USD as the core parts.

- Other library updates:
[winit-block-on](https://github.com/notgull/winit-block-on)is an adaptor that allows one to easily block on futures using winit as a reactor.[tinyaudio](https://reddit.com/r/rust/comments/11rei24/ann_tinyaudio)is a cross-platform, easy-to-use, low-level audio output library from the creator of the Fyrox engine.[faer v0.5](https://reddit.com/r/rust/comments/122823y/faer_v05)brings a new SVD module, which implements the singular value decomposition for real matrices[Bevy Hanabi v0.6](https://twitter.com/djeedai/status/1634129348746772481)brings a new property-based architecture for more control at runtime and also an optimized GPU buffer with Attribute-based particle layout.


## Discussions [#](https://gamedev.rs#discussions)

- /r/rust_gamedev:

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[‘Are We Game Yet?’ wants to know about projects/games/resources that aren’t listed yet](https://github.com/rust-gamedev/arewegameyet#contribute).[Graphite is looking for contributors](https://graphite.rs/contribute)to help build the new node graph and 2D rendering systems.[winit’s “difficulty: easy” issues](https://github.com/rust-windowing/winit/issues?q=is%3Aopen+is%3Aissue+label%3A%22difficulty%3A+easy%22).[Backroll-rs, a new networking library](https://github.com/HouraiTeahouse/backroll-rs/issues).[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[A/B Street’s “good first issue” issues](https://github.com/a-b-street/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/D-Good-First-Issue).[Ambient’s “good first issue” issues](https://github.com/AmbientRun/Ambient/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22).

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!

**Discuss this post on**:
[/r/rust_gamedev](https://reddit.com/r/rust_gamedev/comments/134ge7q/rust_gamedev_44_march_2023),
[Mastodon](https://mastodon.gamedev.place/@rust_gamedev/110292471915457618),
[Twitter](https://twitter.com/rust_gamedev/status/1652952371851345920),
[Discord](https://discord.gg/yNtPTb2).