---
title: 'This Month in Rust GameDev #25 - August 2021'
url: https://gamedev.rs/news/025/
author: Rust GameDev WG
published: '2021-09-08'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 25th issue of the Rust GameDev Workgroup’s
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

[Game Updates](https://gamedev.rs/news/025/#game-updates)[Learning Material Updates](https://gamedev.rs/news/025/#learning-material-updates)[Engine Updates](https://gamedev.rs/news/025/#engine-updates)[Tooling Updates](https://gamedev.rs/news/025/#tooling-updates)[Library Updates](https://gamedev.rs/news/025/#library-updates)[Popular Workgroup Issues in GitHub](https://gamedev.rs/news/025/#popular-workgroup-issues-in-github)[Requests for Contribution](https://gamedev.rs/news/025/#requests-for-contribution)

## Rusty Jam [#](https://gamedev.rs#rusty-jam)

![Rusty Jam Site](../../assets/251b5f396647ca3d.png)


The first (unofficial) Rust Game Jam just completed! The [Rusty
Jam](https://itch.io/jam/rusty-jam) is a game jam to work on games made completely in Rust.
19 games were completed and submitted over the one-week jam. The games were
rated by the community, and the top three games were:

- First place:
[Winter](https://mrrafael.itch.io/winter)by MrRafael - Second place:
[Murder User Dungeon](https://sheepyhead.itch.io/murder-user-dungeon)by Sheepyhead, cdsupina, and Nightlyside - Third place:
[To be Dire](https://septum.itch.io/to-be-dire)by mdaffin, TimeLark and septum

The Rusty Jam will be back, so stay tuned on the [Rusty Jam Discord
Server](https://discord.gg/jZtz6y9gCJ) for more updates!

## Rust GameDev Meetup [#](https://gamedev.rs#rust-gamedev-meetup)

![Gamedev meetup poster](../../assets/ccad50019a0b29e9.png)


The eighth Rust Gamedev Meetup happened in August. You can watch the recording
of the meetup [here on Youtube](https://www.youtube.com/watch?v=g-QZAVipiuU). The meetups take place on
the second Saturday every month via the [Rust Gamedev Discord
server](https://discord.gg/yNtPTb2) and are also [streamed on
Twitch](https://twitch.tv/rustgamedev). If you would like to show off what you’ve been
working on at the next meetup on [September 11th](https://everytimezone.com/s/c603b7e6), fill
out [this form](https://forms.gle/BS1zCyZaiUFSUHxe6).

## Game Updates [#](https://gamedev.rs#game-updates)

[
](https://euclidean-whale.itch.io/pixie-wrangler)
![Screenshot of Pixie Wrangler showing pixies traveling along paths drawn by
the player.](../../assets/e6a8d9c5edde9784.png)


[itch.io](https://euclidean-whale.itch.io/pixie-wrangler),

[GitHub](https://github.com/rparrett/pixie_wrangler)) by

[@rparrett](https://github.com/rparrett)is a puzzle game reminiscent of old school printed circuit board design software.

Help the Pixies get from their outputs to their inputs while doing battle with the intentionally less-than-ergonomic circuit design software. Pixie Wrangler is currently a prototype, but includes 9 complete levels.

Pixie Wrangler was built with [Bevy 0.5](https://bevyengine.org/) with support from these other great
projects: [bevy_webgl2](https://github.com/mrk-its/bevy_webgl2), [bevy_prototype_lyon](https://github.com/Nilirad/bevy_prototype_lyon), [bevy_asset_ron](https://github.com/inodentry/bevy_asset_ron),
[bevy_easings](https://github.com/mockersf/bevy_extra/tree/master/bevy_easings).

![Vange-rs on wgpu-0.10](../../assets/0a308a78b3a5af4c.png)

Vange-rs is a rewrite of the iconic Vangers game from 1998 in Rust, heavily utilizing GPU for rendering.

The rendering engine has seen a major upgrade. Essential shaders were rewritten
into [WGSL](https://gpuweb.github.io/gpuweb/wgsl/), which streamlined the shader pipelines and culled out the
dependency tree. Code was ported on the latest [wgpu](https://github.com/gfx-rs/wgpu)-0.10 release and helped
identify a few issues. Most importantly, this change made the game able to
finally be distributed, and maybe even compiled for the Web in the future. Read
more on the [WGSL-related blog post](https://vange.rs/2021/08/25/pure-rust.html).

In order to take advantage of the new superpowers, the [Rusty Vangers](https://kvark.itch.io/vangers) game (the
new working title) was published on Itch.io.



![RecWars screenshot](../../assets/65b8154f0a560b87.png)

[RecWars](https://github.com/martin-t/rec-wars) by @martin-t is a free and open source Rust clone of [RecWar](https://github.com/martin-t/rec-wars#the-original-game), a top
down vehicle shooter.

The game is a work-in-progress, this month it gained split-screen for 2 players and an in-game console to change cvars - you can edit any of the configuration variables that define its gameplay balance while playing.

RecWars uses the [macroquad](https://github.com/not-fl3/macroquad) engine so it can be played on the desktop as well
as [in the browser](https://martin-t.gitlab.io/gitlab-pages/rec-wars/macroquad.html).

![Vehicle Evolver Deluxe in action, showing multiple vehicles attempting to complete an obstacle course](../../assets/ab0d02b880074839.gif)

[Vehicle Evolver Deluxe](https://bauxitedev.github.io/vehicle_evolver_deluxe/index.html)
([GitHub](https://github.com/Bauxitedev/vehicle_evolver_deluxe),
[Twitter](https://twitter.com/bauxitedev/status/1423916614651678722)) by
[@bauxitedev](https://twitter.com/bauxitedev) is a simulation that runs in your browser, using AI (to be
specific: [genetic algorithms](https://en.wikipedia.org/wiki/Genetic_algorithm))
to try to build better and better vehicles. The vehicles have to overcome an
obstacle course, starting with some slight hills, followed by steeper hills, and
finally some jumps. The vehicles are made out of panels and wheels, connected
together, similar to the game
[Besiege](https://store.steampowered.com/app/346010/Besiege/), except in 2D. It
was built using Rust and the Bevy game engine.

[Try the live web demo
here.](https://bauxitedev.github.io/vehicle_evolver_deluxe/index.html) (It needs
a relatively fast computer, on mobile browsers, it’ll run really slow.)

### Liminal Lab 000 [#](https://gamedev.rs#liminal-lab-000)



![Screenshot of Liminal Lab 000 showing a white-walled laboratory test chamber
with buttons on the floor, lights on the wall, and a dark cube levitating
overhead.](../../assets/bbe9d232a5c01af5.png)

Liminal Lab 000 ([live version](https://pebazium.web.app/)) by [@pebaz](https://github.com/Pebaz) is a tiny, minimalistic
puzzle game with 1 puzzle designed around the concept of [Liminal
Spaces](https://aesthetics.fandom.com/wiki/Liminal_Space). Liminal Spaces are usually abandoned, transitional places
where life once thrived. These spaces are somehow familiar to the viewer but the
viewer has never been there. The unsettling feeling of being alone comes from
the realization that the viewer does not belong in that space but is merely
passing through it.

Liminal Lab 000 was built using [Macroquad](https://github.com/not-fl3/macroquad), utilizes voxel rendering
with 8x8x8 chunks, and is hosted on Google Firebase Hosting.

*Discussions: /r/rust_gamedev*

![Level example from Not Snake](../../assets/5cd58814baa127c6.png)


Not Snake ([GitHub](https://github.com/ramirezmike/not_snake_game), [Itch](https://ramirezmike2.itch.io/not-snake)) by [Michael Ramirez](https://github.com/ramirezmike) is a
3D snake game where you don’t play as the snake.

Not Snake was developed using the [Bevy game engine](https://bevyengine.org). It was
completed and [released for free](https://ramirezmike2.itch.io/not-snake) in August and can be played on
Windows, Linux, MacOS, and in browser (Chrome recommended) although there are
fewer audio/performance issues running the executables versus the browser
version.

There have been several large changes since the last update in June including adding new levels, new music, and adding a narrator who does an OK job of keeping score.

*Discussions:
/r/rust_gamedev,
/r/indiegames*

![Screenshot of "A Day at the Movies"](../../assets/7ecae552bf51418d.png)

“A Day at the Movies” ([GitHub](https://github.com/ramirezmike/rust_gamejam_0821), [Itch](https://ramirezmike2.itch.io/a-day-at-the-movies)) by
[Michael Ramirez](https://github.com/ramirezmike) is a short game about stealth, movies, and friendship.

“A Day at the Movies” was made using the [Bevy game engine](https://bevyengine.org) in 7
days as part of the Rusty Jam. Despite the placeholder art and lack of audio, it
can be played from start-to-finish and is literally guaranteed to bring a smile
to all who play it. Just make sure to follow the instructions on how to get into
the “Ferris the Crab” movie room.

It’s playable in-browser on [itch](https://ramirezmike2.itch.io/a-day-at-the-movies) and the code can be viewed on
[GitHub](https://github.com/ramirezmike/rust_gamejam_0821).

![Screenshot of Sombervale depicting the starting location](../../assets/2636e393acf45466.png)


Sombervale ([GitHub](https://github.com/blipjoy/sombervale), [itch.io](https://blipjoy.itch.io/sombervale), [Twitch](https://www.twitch.tv/blipjoy)) by
[@blipjoy](https://github.com/blipjoy) is a game built in seven days for Rusty Jam. It is styled like an old
handheld game with a 160x128 screen resolution and 16-color palette.

The top 3 things that went well for this project were the art, tilemap support,
and ECS. On the art side, the silhouettes in the background turned out better
than expected. The backlighting (or at least the impression of backlighting)
looks quite nice, even in motion. Tilemap support was added near the end of the
jam built on [tiled](https://crates.io/crates/tiled). It catapulted development progress from seeing major
changes every day to making major changes every hour. [shipyard](https://crates.io/crates/shipyard) is the Entity
Component System crate used in Sombervale. This had a tricky learning curve, but
simplified complex interactions between entities.

Something that went poorly was choosing a scope that couldn’t possibly be completed on time. As usual, everything turned into a stretch goal! Secondly, a lot of time was allocated to features that didn’t make the cut. Much of this was a result of trying to be perfect instead of efficient. It’s a good game jam lesson that often has to be relearned the hard way.

### Shattersong Online [#](https://gamedev.rs#shattersong-online)

![Screenshot of Shattersong Online showing a portal leading between two shards](../../assets/c45c9cab7c2d83e1.png)


Shattersong Online is an online sandbox game written in Rust, with the goal of supporting thousands of players in a shared universe, with hundreds of players per shard. In-game portals let players travel between shards hosted on separate physical servers.

Since the initial announcement in July, we have worked on restructuring large parts of the codebase to make adding new content more ergonomic. We tested out the new organization by adding a new monster type from scratch (pictured above).

Read the [dev blog](https://triplehex.dev/shattersong-online/) for more info, follow
[@triplehex](https://twitter.com/triplehexdev) on twitter for updates, and join the
[shattersong discord](https://discord.gg/K5RHxVEK6F) for questions!

![An animated gif showing a machine setup to smelt iron ore](../../assets/b4710f9f4b4fe2d0.gif)

[The Process](https://twitter.com/PlayTheProcess) by @setzer22 is an upcoming game about factory building, process
management, and carrot production, built with Rust using the Godot game engine!

This month has seen a lot of activity: More improvements to the level editor, in-game assets, and general gameplay improvements. But the main focus has been on a new building system with improved ergonomics. The game is now approaching a point where all the core mechanics for the factory simulation are in place, but more in-game content and assets are still required to reach the first playable demo.

This month the game has seen the following changes and improvements:

- New assets like
[wooden planks](https://twitter.com/PlayTheProcess/status/1423712530267054086),[machine parts](https://twitter.com/PlayTheProcess/status/1433160712231297027)and[mashed carrot cans](https://twitter.com/PlayTheProcess/status/1434466387787923456), with their in-game recipes. - A new machine, the
[centrifuge](https://twitter.com/PlayTheProcess/status/1430923976574910466) - A new system to tweak properties with
[OSD sliders](https://twitter.com/PlayTheProcess/status/1424638751041536001)to speed up iteration times. Short explanation[here](https://twitter.com/PlayTheProcess/status/1424638756246675459). - A new egui-powered
[main menu](https://twitter.com/PlayTheProcess/status/1425785805453373444)for the main game screen. - Improvements to the building system:
[ghost markers](https://twitter.com/PlayTheProcess/status/1427560636289069059),[ramps](https://twitter.com/PlayTheProcess/status/1428300028712558595),[walls](https://twitter.com/PlayTheProcess/status/1429391914130882564),[machines](https://twitter.com/PlayTheProcess/status/1430229400923119621)and[conveyor belts](https://twitter.com/PlayTheProcess/status/1430479444213485574)!

*Discussions:
/r/rust_gamedev*

![Murder-User Dungeon gameplay screenshots](../../assets/d73a911cb3abd9be.png)


Murder-User Dungeon (MUD) ([GitHub](https://github.com/TheRealTeamFReSh/MurderUserDungeon), [Itch](https://sheepyhead.itch.io/murder-user-dungeon)) by
[@Nightlyside](https://nightlyside.github.io/), [@cdsupina](https://github.com/cdsupina), [@Shippyhead](https://github.com/Sheepyhead) is
a 2D game made for the [Rusty Jam 21](https://itch.io/jam/rusty-jam) in just one week with the
theme “*Illusion of Security*”.

Tony is a young man. Finally having his own apartment is a good thing! He will learn how to live by himself and how to enjoy the small things in life like playing on his old retro computer: the Astaria 3600 running SafeOS 3.1.

However, you will quickly realize that the internet is not so friendly. You will meet new people in the Labyrinth(TM) game, and not being friendly to them can have a serious impact on your real life!

In Murder-User Dungeon you will juggle between exploring the Labyrinth(TM) game in your console, hiding from vengeful gamers and making sure you fulfill your human needs.

To win the game, you must reach the end of the Labyrinth(TM)!


The developers aimed to make the player feel that they were safe in their apartment at first - however as the game goes on and the player makes enemies of other gamers in the Labyrinth, they risk them coming to their apartment to get revenge.

The team split development of the game, so that each member could work
independently on separate features. While [@cdsupina](https://github.com/cdsupina) worked on the
needs system and the graphics, [@Sheepyhead](https://github.com/Sheepyhead) worked on the UI and
menus, and [@Nightlyside](https://nightlyside.github.io/) worked on the console and Labyrinth
gameplay.

MUD was developed using the [Bevy game engine](https://bevyengine.org/), Rapier2D for
collisions, Aseprite for the graphics, and a lot of free assets from the
internet (which are credited at the end of the game’s description).

Linux and Windows builds are available on the Itch page, and feedback is welcomed!

*Discussions:
r/rust_gamedev,
r/rust,
Rusty Jam Discord*



![Theta Wave Mobs](../../assets/79043e8ecdd5de36.gif)

[Theta Wave](https://github.com/thetawavegame/thetawave) is an open-source space shooter game by developers [@micah_tigley](https://twitter.com/micah_tigley)
and [@carlosupina](https://twitter.com/carlosupina). In the past month, they have been working towards porting
Theta Wave to the Bevy Engine. Most of the work this month has been focused on
implementing all of the existing mobs in Bevy and Rapier.

Progress on this port is going strong - you can find the GitHub issue for the
port [here](https://github.com/thetawavegame/thetawave/issues/2).

*Discussions:
Twitter*

![SHRM token distribution](../../assets/b9e4ff3c32d8a2f0.png)

Shroom Kingdom ([GitHub](https://github.com/Shroom-Kingdom), [Discord](https://discord.gg/SPZsgSe),
[Twitter](https://twitter.com/shrm_kingdom)) is an upcoming play-to-earn video game built with web
technologies running on the [NEAR Blockchain](https://near.org).

This month the [whitepaper draft](https://whitepaper.shroomkingdom.net/) has been published and a lot
of thoughts have been put into the token economics and how to integrate the game
with the blockchain. The Shroom Kingdom DAO (Decentralised Autonomous
Organization) is looking for self-motivated people, who want to help build the
project. DAO members will be rewarded with the $SHRM token, which will soon be
launched on the NEAR mainnet after the final feedback round from NEAR core team
members.

A Proof of Concept has also been published for the app, which will be built with Bevy and Rapier compiled to WebAssembly and which uses React for the GUI.

To incentivise early adoption of the project, an [NFT airdrop](https://shroomkingdom.net/blog/nft-airdrop/)
has been announced. The NFT will only be acquirable for a limited amount of
time.

![Screenshot of fishfight.org website](../../assets/6e1d01989100ddd4.png)


[Fish Fight](https://fishfight.org/) ([GitHub](https://github.com/fishfight/FishFight), [Discord](https://discord.gg/4smxjcheE5),
[website](https://fishfight.org/)) is a love letter to its spiritual
predecessor [Duck Game](https://store.steampowered.com/app/312530/Duck_Game/).

[As promised](https://fishfight.itch.io/ff/devlog/281554/fish-fight-reloaded),
after months of private prototyping of early invitees, the Fish Fight devs are
finally ready to make their code and community channels available to the general
public. They also launched their website! You can read the [announcement
post](https://fishfight.itch.io/ff/devlog/291737/fish-fight-is-open-source) and the [design doc](https://www.notion.so/erlendsh/Fish-Fight-1647ed74217e4e38a59bd28f4f5bc81a).

![TO BE DIRE cover art](../../assets/30665b5d6ab0f58a.png)


TO BE DIRE by [@mdaffin](https://mdaffin.itch.io), [@TimeLark](https://timelark.itch.io) and [@septum](https://septum.itch.io), is a prototype survival
game made in a week with [Bevy](https://bevyengine.org) for the first [Rusty Jam](https://itch.io/jam/rusty-jam).

The main idea behind the design of TO BE DIRE is venturing out of the safe zone
in order to survive, adding elements of gameplay like gathering resources, and
maintaining the player character health and hunger, which are common for the
genre, finally having the implementation of the monsters and fear system as a
way to further address the first Rusty Jam’s theme “Illusion of Security”. [Read
more about TO BE DIRE’s design in the issues at GitLab](https://gitlab.com/mdaffin/tbd/-/issues?scope=all&state=closed).

Download the game at [itch.io](https://septum.itch.io/to-be-dire) (available for Linux and Windows)
and/or get the source code at [GitLab](https://gitlab.com/mdaffin/tbd).

![Exploring dungeons](../../assets/13d2df9d05fca777.jpg)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In August, lots of preparation was done to get Veloren ready for the 0.11 release coming in September. Work was done on refactoring parts of the codebase, and making server administration more ergonomic. Towers were added, which allow for above-ground dungeons. Skill trees were tweaked for better progression. Modular weapons had a heavy amount of work put into them and were recently merged. Work was done to prevent the camera from clipping through walls as much.

Improvements were made to the physics system, as well as other optimizations to
the real-time simulation system. Terrain persistence was completed and is now
being tested on the main server. Balancing was done to loot tables, and more
animations were added to characters. In September, 0.11 will be released. Come
out to the [release party on the 11th at 18:00 UTC](https://opencollective.com/veloren/events/veloren-0-11-release-party-05c1a306)!

August’s full weekly devlogs: “This Week In Veloren…”:
[#131](https://veloren.net/devblog-131),
[#132](https://veloren.net/devblog-132),
[#133](https://veloren.net/devblog-133),
[#134](https://veloren.net/devblog-134),
[#135](https://veloren.net/devblog-135).

![What’s the word](../../assets/5ed342bfc24119e4.gif)


A UI-based game in which you tap (or miss) buttons. Created with [Bevy
engine](https://bevyengine.org/) and [egui](https://github.com/mvlabat/bevy_egui), it demonstrates
how *small* you can scope your project for a [(Rusty) game
jam](https://itch.io/jam/rusty-jam/results)!

![Humankind’s logo](../../assets/7542049db7040926.jpeg)


[Humankind](https://store.steampowered.com/app/1124300/HUMANKIND) is a Civilization-like game from [Amplitude Studios](https://www.amplitude-studios.com),
out of Early Access a few weeks ago.
While the game itself isn’t written in Rust,
its [gorgeous encyclopedia](https://humankind-encyclopedia.games2gether.com/en-us) and persona sharing service
[are written using rocket.rs](https://twitter.com/SobertKaos/status/1429812457820786694).

Since the encyclopedia has a big constraint of being used inside an embedded
in-game browser that has a bit of performance issues with full JS frameworks
the team opted for server-side rendering with the [Tera](https://github.com/Keats/tera) template framework.

I had people working on that without any prior rust experience, and they were ready to code in no time thanks to good language documentation & useful compiler messages.

We didn’t do anything particularly complex, but the safety of Rust combined with performance enabled us to make this run for way less $$. You don’t have to do complex system programming to profit from Rust’s benefits.


## Engine Updates [#](https://gamedev.rs#engine-updates)

[rg3d](https://github.com/mrDIMAS/rg3d) ([Discord](https://discord.gg/xENF5Uh), [Twitter](https://twitter.com/DmitryNStepanov)) is a game engine that
aims to be easy to use and provide a large set of out-of-the-box features. [A
video](https://www.youtube.com/watch?v=N8kmZ9aBtZs) was released with updates from version 0.22. [Another
video](https://www.youtube.com/watch?v=mzshg_0ZvLk) about the engine made by [@GameFromScratch](https://www.youtube.com/channel/UCr-5TdGkKszdbboXXsFZJTQ), with
the accompanying article that can be found [here](https://gamefromscratch.com/rg3d-open-source-rust-3d-game-engine/).

Lots has been happening with recent rg3d engine development. Physically-based rendering (PBR) was added. High dynamic range rendering is now supported, along with tone mapping, color grading, and gamma correction. Manual and auto-exposure functionality was added for cameras. There is now a widget for editing curves, and it supports custom curves. Lots of usability improvements were made, such as begin able to change the path of resources, UI performance gains, and better ways to manage assets.

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

![Panda Doodle logo](../../assets/f2ec9fb5790ba6bd.png)


[@lucamoller](https://github.com/lucamoller) published [a blog post](https://lucamoller.medium.com/rewriting-my-mobile-game-in-rust-targeting-wasm-1f9f82751830)
describing his experience trying to learn Rust by working on a hobby project to
migrate his mobile game from a native C++ implementation to a Rust-based one
targetting WASM.

The post is written in a storytelling manner going through the author’s motivations to work on this project and the main challenges they faced while learning Rust and implementing a game using WASM.

The resulting game, [Panda Doodle](https://pandadoodle.lucamoller.com/), runs smoothly on mobile
device browsers, and the [source code](https://github.com/lucamoller/pandadoodle-rust-wasm) was open
sourced to help inspire other developers that wish to venture into implementing
WASM-based games in Rust.

*Discussions:
/r/rust*

## Tooling Updates [#](https://gamedev.rs#tooling-updates)

![Graphite alpha teaser](../../assets/150182dde4fd25cd.png)

Graphite ([GitHub](https://github.com/GraphiteEditor/Graphite), [Discord](https://discord.graphite.design),
[Twitter](https://twitter.com/GraphiteEditor)) is an in-development vector and
raster graphics editor built on a non-destructive node-based workflow.

Work has progressed on features for the imminent Alpha release. A project website has been designed and will launch this month. Crucial user-facing features have been added: saving/opening documents; a bug report dialog for panics; an auto-generated list of dependency license notices; and a new undo/redo system.

The new Path Tool shows Bézier anchor/control points (soon to be draggable). Rendering performance is much better and scrollbars now work with the infinite canvas. There’s a new bounding box around selected shapes that are transformable with Blender-inspired [G]/[R]/[S] keys.

[Try it right now in your browser.](https://editor.graphite.design) Graphite is making rapid
progress towards becoming a non-destructive, procedural graphics editor suitable
for replacing traditional 2D DCC applications. The public alpha release is coming
very soon. [Join the Discord](https://discord.graphite.design) and get involved!

![rx](../../assets/e193b630ec0b3b4f.png)


[rx](https://rx.cloudhead.io) ([website](https://rx.cloudhead.io), [code](https://github.com/cloudhead/rx), [community](https://discord.gg/xHggPjfsS9)) by
[@cloudhead](https://twitter.com/cloudhead) is a modern and minimalist pixel editor written in Rust.

Rx is a pixel art editor/animator written in Rust in about 12K LOC, which combines a vim-like modal interface with a cursor-based editor.

Release v0.5 was just published. There are several new commands that help with
color palettes. A flood fill tool has been added. You can now move between
frames with the `h`

and `l`

keys. The command key `:`

has been fixed to help
with non-ANSI layouts. Compatability was added for non x86_64 systems. Support
was added for pasting from the clipboard into the command line. Animation
rendering is now a lot smoother.

## Library Updates [#](https://gamedev.rs#library-updates)

![GGRS](../../assets/e79b701e6aa35166.png)


[GGRS](https://github.com/gschup/ggrs) by [@g_schup](https://twitter.com/g_schup) is a reimagination of the [GGPO](https://www.ggpo.net/) P2P rollback network SDK
written in 100% safe Rust.

Since the last update, GGRS has released version 0.4.4 and received performance
updates and fixes, such as a [sparse saving
feature](https://gschup.github.io/ggrs/blog/sparse-saving/). The authors also
proudly present [bevy_GGRS](https://github.com/gschup/bevy_ggrs)!

bevy_GGRS is a plugin to integrate GGRS easily into the popular game engine
[bevy](https://bevyengine.org/). It features automatic saving and loading of components and resources
defined by the user through bevy’s reflection tools. The plugin is currently in
development and uses features that have not been released in bevy 0.5. With bevy
0.6 on the horizon, bevy_GGRS is planning to publish to
[crates.io](https://crates.io), as well.

If you are interested in developing with GGRS, check the following resources:

![Rend3 on wgpu-0.10](../../assets/d8350608692d9b6e.jpg)

The team has released wgpu-0.10 with a fully rewritten graphics abstraction
(“wgpu-hal” instead of “gfx-hal”), as well as [naga](https://github.com/gfx-rs/naga) version 0.6. Read more in
[Release of a Pure-Rust v0.10 and a Call For Testing](https://gfx-rs.github.io/2021/08/18/release-0.10.html).

There were a few issues spotted, but overall it went smooth for such a big
change. User libraries were quick to update: [iced#1000](https://github.com/hecrj/iced/pull/1000), [kas#241](https://github.com/kas-gui/kas/pull/241),
[pixels#187](https://github.com/parasyte/pixels/pull/187), and others.

On the shader side, in addition to improved validation, hundreds of fixes to the
produced outputs, the atomic operations are now supported when using [WGSL](https://gpuweb.github.io/gpuweb/wgsl/)
sources.

The release comes at a cost of DX11 backend, which isn’t there comparing to wgpu-0.9. On the plus side, the new GL backend performs much better. It runs most of the examples, and has been successfully tested on Raspberry Pi-3. Still, more work ahead to make it solid, and to support WebGL2 properly.

[godot-egui](https://github.com/setzer22/godot-egui)-0.1.8 [#](https://gamedev.rs#godot-egui-0-1-8)

![An animation showing godot-egui running as a plugin inside the editor](../../assets/d4c80d5fb6c86c06.gif)

The [egui](https://github.com/emilk/egui) backend for
[godot-rust](https://github.com/godot-rust/godot-rust) is improving fast. Some
bugs have been ironed out during this past month, and the integration has got
several features:

- The repository now includes an example of how to setup egui to create
[Godot editor plugins](https://twitter.com/PlayTheProcess/status/1431660162587275267). Contribution by @jacobsky. - Custom font support by drag & dropping font files right from Godot editor.
- Updated crate to match latest egui 0.14.2
- Configurable texture filtering.
- Several bugfixes and improvements.

Additionally, a new [theme
editor](https://github.com/setzer22/godot-egui/issues/5) is in the works, which
hopefully will be helpful to other egui backends as well!

[Dimforge](https://dimforge.com) creates open-source Rust crates for numerical simulation.
Some of the [recent updates](https://dimforge.com/blog/2021/08/15/the-last-two-months-in-dimforge):

[New user-guide for Rapier’s JS bindings](https://rapier.rs/docs/user_guides/javascript/getting_started_js).[nalgebra](https://nalgebra.org)v0.29 brings better soundness and non-Copy types support.[Rapier](https://rapier.rs)0.11 brings a full set of joint limits.- The work on unbreakable reduced-coordinates joints for Rapier is also in progress.

## Popular Workgroup Issues in GitHub [#](https://gamedev.rs#popular-workgroup-issues-in-github)

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[winit’s “difficulty: easy” issues](https://github.com/rust-windowing/winit/issues?q=is%3Aopen+is%3Aissue+label%3A%22difficulty%3A+easy%22).[Backroll-rs, a new networking library](https://github.com/HouraiTeahouse/backroll-rs/issues).[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[A/B Street’s “good first issue” issues](https://github.com/a-b-street/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/D-Good-First-Issue).

That’s all the news for last month, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or the [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh
news and updates about the ecosystem every day!

**Discuss this post on**:
[/r/rust_gamedev](https://www.reddit.com/r/rust_gamedev/comments/pki6iw/this_month_in_rust_gamedev_25_august_2021/),
[Twitter](https://twitter.com/rust_gamedev/status/1435700216510943234),
[Discord](https://discord.gg/yNtPTb2).