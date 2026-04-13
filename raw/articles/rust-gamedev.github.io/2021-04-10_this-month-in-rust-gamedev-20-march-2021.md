---
title: 'This Month in Rust GameDev #20 - March 2021'
url: https://gamedev.rs/news/020/
author: Rust GameDev WG
published: '2021-04-10'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 20th issue of the Rust GameDev Workgroup’s
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

[Game Updates](https://gamedev.rs/news/020/#game-updates)[Learning Material Updates](https://gamedev.rs/news/020/#learning-material-updates)[Engine Updates](https://gamedev.rs/news/020/#engine-updates)[Library & Tooling Updates](https://gamedev.rs/news/020/#library-tooling-updates)[Requests for Contribution](https://gamedev.rs/news/020/#requests-for-contribution)

## Rust GameDev Meetup [#](https://gamedev.rs#rust-gamedev-meetup)

![Gamedev meetup poster](../../assets/ec1047a2e7c60b3f.png)


The third Rust Gamedev Meetup happened in March. It was an opportunity for
developers to show off what Rust projects they’ve been working on in the game
ecosystem. Developers showed off game engine demos, in-game playthroughs,
tooling, and more. You can watch the recording of the meetup [here on
Youtube](https://youtube.com/watch?v=gqCxt8XL92o).

The next meetup will take place on the 10th of April at 16:00 GMT on the [Rust
Gamedev Discord server](https://discord.gg/yNtPTb2), and can also be [streamed on
Twitch](https://twitch.tv/rustgamedev). If you would like to show off what you’ve been
working on, fill out [this form](https://forms.gle/BS1zCyZaiUFSUHxe6).

## Game Updates [#](https://gamedev.rs#game-updates)

![MineWars Game Screenshot](../../assets/0e79e47e5e07de6d.jpg)


[MineWars](https://minewars.cc) ([Twitter](https://twitter.com/MineWarsGame), [Reddit](https://reddit.com/r/minewars))
by @jamadazi is Minesweeper reimagined as a Multiplayer Real Time Strategy!

Capture mines. Move them around. Cause explosion chains. Take out enemy mines. Defend your Cities. Fight for territory. Eliminate other players. Play on a procedurally-generated map.

The game has been privately in development for many months and was just
announced publicly. The project is currently working towards an alpha release
for public playtesting. Read the announcement on the [website](https://minewars.cc) for
more information.

Made in the [Bevy Game Engine](https://bevyengine.org).

![Super Mario 64 JavaScript](../../assets/c968e9c2d8ed1fc3.jpg)


[sm64js](https://sm64js.com) ([GitHub](https://github.com/sm64js/sm64js), [Discord](https://discord.gg/7UaDnJt)) is a rewrite
of the decompilation project of Super Mario 64 in JavaScript with a strong focus
on massive multiplayer online.
The [backend](https://github.com/sm64js/sm64js-mmo-server) recently has been rewritten in Rust by [@marior](https://twitter.com/marior_dev)
and is now live.

You can find more information about it in [this recent blog post](https://net64-mod.github.io/blog/sm64js/),
where the developers of a similar mod called Net64 are talking
about several decompilation projects.

Some of the most recent additions are:

- Karts and gliders.
- Health meters.
- More visuals with butterflies and fish.

A stress test is scheduled for 2021-04-17 17:30 UTC and everyone is invited to join.

![Bibi rolling around](../../assets/45914e5f9ff800f7.gif)


[Outer Wonders](https://utopixel.games/en/blog/introducing-outer-wonders) by the [Utopixel Studio](https://twitter.com/utopixel)
is a pixelart puzzle-based adventure game built using SDL2.

Explore a world of fantasy in Outer Wonders. Play as Bibi, the cute round monkey, unveil the natural wonders surrounding your native village, and unravel their mysteries in this ecological puzzle-based adventure game.


March was mostly about various preparations for the upcoming playable demo release. Some of the recent updates:

- More lively in-game environments.
- Scripted cutscenes.
- Translations.
[Linux support progress](https://utopixel.games/en/blog/building-outer-wonders-for-multiple-platforms).[Lot’s of level and technical testing](https://utopixel.games/en/blog/testing-outer-wonders-demo-before-release).- The playable demo
[will be released on April 16](https://utopixel.games/en/blog/outer-wonders-demo-release-on-april-16).

![Mars with a RdBu colormap](../../assets/de1773e23cffa82a.gif)

[Aladin Lite](https://github.com/cds-astro/aladin-lite/tree/develop) is a spatial image survey visualizer developed by the [Astronomical
Observatory of Strasbourg](https://cds.u-strasbg.fr/index-fr.gml) in France. Since its first release in 2013,
[Aladin Lite](https://github.com/cds-astro/aladin-lite/tree/develop) has been used by astronomers as well as amateurs that
are curious about exploring the sky.

Originally developed using 2D Javascript canvas, its core has been fully
rewritten in Rust and WebGL2 using [wasm-bindgen](https://github.com/rustwasm/wasm-bindgen).
New features include:

- The support of multiple allsky projections (mercator, aitoff, …).
- The blending of multiple surveys.
- The support of FITS file images.

For more information, see a [talk](https://youtube.com/watch?v=TILtJOiiRoc) done at the ADASS 2020
conference. A web page is also available [here](https://bmatthieu3.github.io/hips_webgl_renderer/index.html) for you to test.
You are also very welcolme to contribute to the project by e.g. posting issues
on the project’s github.

!["Portal in portal" scene](../../assets/8c43943113f20aa2.png)

[Portal Explorer](https://github.com/optozorax/portal) by [@optozorax](https://twitter.com/optozorax) is a web
visualizator of mind-blowing portals.

In Portal Explorer you can view how interesting portals are constructed, and
visually explore their properties by moving and rotating them. This program
doesn’t work well on mobile, better opened from PC. The most interesting
scene is [portal in portal](https://optozorax.github.io/portal/?scene=portal_in_portal).

Created using ray-tracing in shaders, engine is [macroquad](https://github.com/not-fl3/macroquad),
interface is [egui](https://github.com/emilk/egui).

![Wandering agents hauling items around and digging](../../assets/eee76eb310b687b7.gif)

[Name Needed](https://github.com/DomWilliams0/name-needed) by [@DomWilliams0](https://github.com/DomWilliams0) is a one man
effort to produce an open source, intuitive and high performance Dwarf
Fortress-esque game.

The engine is custom, built with SDL2 and OpenGL. It’s still early days, but steady progress has been made over the last 18 months. The developer aims to release occasional technical devlogs about interesting parts of the engine, which so far include:

![Orbital Decay](../../assets/1aea0f47d46259ba.gif)

[Orbital Decay](https://gridbugs.itch.io/orbital-decay) by [@stevebob](https://github.com/stevebob) is an
[open-source](https://github.com/stevebob/orbital-decay) turn-based tactical roguelike with a focus
on ranged combat. Deal enough damage to enemies to get through their armour
without breaching the hull of the station, or risk being pulled into the void.
It was made for the [7 Day Roguelike 2021](https://itch.io/jam/7drl-challenge-2021) game jam.

Traverse a procedurally-generated space station to reach the fuel bay on the 5th floor. Choose your weapons and upgrades wisely to make it past the station’s former crew - now a horde of ravenous undead.

Read more about Orbital Decay on its [development blog](https://www.gridbugs.org/7drl2021-day7/).

![Title card with game name and a big mansion](../../assets/fb041f0b74d25402.png)


[Disguiser](https://mcneja.github.io/disguiser) ([itch.io](https://mcneja.itch.io/disguiser-2021-7drl), [source code](https://github.com/mcneja/disguiser))
by [@mcneja](http://playtechs.blogspot.com)
is a coffee-break turn-based stealth game inspired by Thief that
was made for the [7 Day Roguelike 2021](https://itch.io/jam/7drl-challenge-2021) game jam.
The randomly-generated mansions are loosely based on Chinese courtyard houses,
with symmetry, enclosed gardens, and a public-to-private gradient
from the entrance northward.

The development process is documented in
a [bunch of devlog posts](http://playtechs.blogspot.com/search/label/2021-7drl).

*Discussions:
/r/rust_gamedev*

![a screenshot with in-game message](../../assets/28da3a203a5547e7.jpg)


[secbot](https://thebracket.itch.io/secbot) ([web version](http://bfnightly.bracketproductions.com/secbot2021), [souce code](https://github.com/thebracket/secbot-2021-7drl))
by [Herbert Wolverson](https://bracketproductions.com) is another 7DRL submission:

The idea behind SecBot is that an outpost has ceased communications, so the morally dubious Bracket Corporation dispatch a security bot to find out what happened. Upon arrival, it becomes clear that things aren’t going well for the colony - so the player rushes around collecting colonists and shepherding them back to the spaceship. I tried to bake some narrative/flavor into the game, and create a fun game you can enjoy over a coffee-break.


Btw, Herbert is going to give a “Learning Rust With Game Development” talk
at [Rust Meetup Linz on April 22](https://rust-linz.at).



![bounty-bros-character-on-map](../../assets/7ee642beaf673ea9.png)

[Bounty Bros.](https://katharostech.com/post/bounty-bros-on-web) is a prototype game similar to the old Legend of
Zelda® games developed by [Katharos Technology](https://katharostech.com) as a testing
ground for a future commercial game.

In the last 2 months Bounty Bros. has gotten a lot of updates. Now you can [play
the game](https://skipngo.katharostech.com/?asset_url=https://bounty-bros.skipngo.katharostech.com/) right inside of your browser on desktop or mobile
devices!

- You can no longer walk through walls or objects.
- You can now walk into buildings.
- The camera follows the player without passing beyond the map borders.
- Rendering is now scaled pixel-perfect.
- Mobile touch controls were added.
- There is a new
[retro mode](https://skipngo.katharostech.com/?asset_url=https://bounty-bros.skipngo.katharostech.com/&enable_crt=true&pixel_aspect_ratio=1.3)that tries to make it look like the game is running on an old CRT television.

All of the source code, excluding assets and artwork, was also made available and split into two independent projects.

These projects were released under the
[Katharos License](https://github.com/katharostech/katharos-license). This license has moral and ethical
implications that you may or may not agree with, so please read it before making
use of these projects:

[Bevy Retro](https://github.com/katharostech/bevy_retro)([forum](https://github.com/katharostech/skipngo/discussions)) - a Bevy plugin for pixel-perfect games.[Skip’n Go](https://github.com/katharostech/skipngo)([forum](https://katharostech.com/post/bounty-bros-on-web)) - a simple game engine for making top-down pixel games.

You can read the full update in the [Blog Post](https://katharostech.com/post/bounty-bros-on-web).

![Improved text rendering](../../assets/58b5be1fd259cf69.jpg)


[pGLOWrpg](https://github.com/roalyr/pglowrpg) ([Twitter](https://twitter.com/pglowrpg)) by [@Roal_Yr](https://twitter.com/Roal_Yr)
is a Procedurally Generated Living Open World RPG,
a long-term project in development, which aims to be a narrative text-based game
with maximum portability and accessibility.

Recent updates include:

- Reformatting a print interface, making it very easy to link text UI and code.
- Switching to .ron file format for storing configs and strings.
- Implementing individual strings coloring for better visual perception.

![gameplay screenshot wthh an explosion](../../assets/833f557eb90cefa3.png)


[rusty-bomber](https://rgripper.github.io/rusty-bomber) ([source code](https://github.com/rgripper/rusty-bomber)) by [@rgripper](https://github.com/rgripper) and [@Cupnfish](https://github.com/Cupnfish)
is a BomberMan clone written using Bevy & Rapier that works on desktop and web.

Check out the [devlog](https://github.com/rgripper/rusty-bomber/blob/548d50470/blog/blog.md) for more details about
the project’s internals.

### Stellary 2 [#](https://gamedev.rs#stellary-2)



![Stellary 2 Anti-Missile Laser](../../assets/2c5e26cb9bdcd1f9.gif)

[watch the full video](https://twitter.com/CoffeJunkStudio/status/1378719827347509249)

Stellary 2 by [@CoffeJunkStudio](https://twitter.com/CoffeJunkStudio) is a 3D real-time space
shooter in which the player has to control his spaceship to colonize each planet
in the solar system.

In the last month, the game concept has been overhauled. Most importantly:

- Planets become inhabitable over time, starting with the outermost one in order to bring head-to-head matches to an end eventually.
- Full focus on multiplayer, including AIs.
- Players can’t die mid-game anymore. When defeated, they re-spawn and lose a colony for it (if they have one) instead of dying. This prevents long waiting times when playing against friends.

You can follow the development of Stellary 2 on [Twitter](https://twitter.com/CoffeJunkStudio).

![Elevation data in A/B Street](../../assets/db2d5c3566d24f02.jpg)


[A/B Street](https://github.com/a-b-street/abstreet) by [@dabreegster](https://twitter.com/CarlinoDustin) is a traffic simulation game exploring how small
changes to roads affect cyclists, transit users, pedestrians, and drivers, with
support for any city with OpenStreetMap coverage.

In March, elevation data courtesy of [Eldan](https://github.com/eldang/) was imported, letting cycling
speeds uphill be adjusted. Importing any area from OpenStreetMap can now be
done from the UI with no command-line experience, and custom travel demand
models based on UK-wide census data can now be generated. Some important
simulation fixes for roundabouts improve gridlock, and [Michael](https://github.com/michaelkirk) and [Yuwen](https://www.yuwen-li.com/)
helped adjust the UI panel layout for smaller screens.

![Egregoria city at dawn](../../assets/8452d0f9cea58e2f.jpg)


[Egregoria](https://github.com/Uriopass/Egregoria) ([GitHub](https://github.com/Uriopass/Egregoria), [Discord](https://discord.gg/CAaZhUJ))
by [@Uriopass](https://github.com/Uriopass)
is a simulation oriented city builder that tries
to replicate modern society as well as possible.

The [8th devlog](https://douady.paris/blog/egregoria_8.html) was published.
Updates include:

- Multiplayer based on deterministic lockstep
- Economy revamp inspired by Anno 1800
- Infinite world using procedural generation
- Many more QoL features

See also the [YouTube summary video](https://youtu.be/qH2SKWbRV5I)
of the past 6 months of development.

![Gargoyle’s Quest](../../assets/9df8f58e73a15cfc.png)


[Gargoyle’s Quest](https://github.com/ShamylZakariya/Platformer) by [@ShamylZakariya](https://github.com/ShamylZakariya) is an implementation of level one
of the 1990 [Gameboy platformer](https://en.wikipedia.org/wiki/Gargoyle%27s_Quest) built using [wgpu](https://github.com/gfx-rs/wgpu-rs).

![Fishgame](../../assets/0ba850dc475a1782.gif)

[Fishgame](https://github.com/heroiclabs/fishgame-macroquad) [(web build)](https://fedorgames.itch.io/fish-game?secret=UAVcggHn332a) is an online multiplayer game,
created in a collaboration between [Nakama](https://heroiclabs.com/), an open-source scalable
game server, and the [Macroquad](https://github.com/not-fl3/macroquad) game engine.

This month:

- fishgame migrated to
[nakama-rs](https://github.com/not-fl3/nakama-rs)(featured in this newsletter as well). - Also a second weapon, the sword, was added to the game.

![Airship](../../assets/3f2e0609a62e1de7.jpg)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

In March, Veloren released 0.9. Lots of work throughout the month was put towards preparing for this. NPC merchants and trading was merged. Many changes were made to combat, including buffs and combat. Player-to-player trading was also implemented. Lots of work was done in optimizing Veloren. This included significantly improving how long physics was talking, and network improvements. Metrics tracking was also overhauled to better track the different systems in Veloren. Pathfinding is also working through an overhaul. A large feature implemented in March was Airships being merged into the game. This prompted a redo of how physics in the game is handled.

A survey was sent out in preparation for the release. A lot of information was
gathered about how players experience Veloren, and the items they like or don’t
like. These can all be ready in [devblog #112](https://veloren.net/devblog-112).
This was followed up by the 0.9 release, which turned out to be the largest yet.
At peak, 133 players joined the main server. There were problems throughout the
release party relating to networking, as well as our tick performance.

March’s full weekly devlogs: “This Week In Veloren…”:
[#109](https://veloren.net/devblog-109),
[#110](https://veloren.net/devblog-110),
[#111](https://veloren.net/devblog-111),
[#112](https://veloren.net/devblog-112).
[#113](https://veloren.net/devblog-113).



![Enemy Formations](../../assets/a66c332bfe555048.gif)

[Theta Wave](https://github.com/amethyst/theta-wave) is an open-source space shooter game by developers [@micah_tigley](https://twitter.com/micah_tigley) and
[@carlosupina](https://twitter.com/carlosupina). It is one of the showcase games for the [Amethyst Engine](https://amethyst.rs/). In
the past month, the [“Foundations”](https://github.com/amethyst/theta-wave/releases/tag/v0.1.4) update was released which included numerous
refactors that improved the accessibility of contributing to the game.

They are now working on the [“Formations”](https://github.com/amethyst/theta-wave/projects/2) update which will organize how
waves of enemies are spawned into the game.

Notable changes:

- Formations can be defined in a data file
- New
`InvasionFormation`

phase where formations of enemies are spawned from a pool of formations

![harvest_hero_level](../../assets/ae3efb01a73d194e.gif)


[Harvest Hero](https://discord.gg/CJRbxQn3d9) ([Discord](https://discord.gg/CJRbxQn3d9), [Twitter](https://twitter.com/bombfuse_dev))
by [@bombfuse](https://twitter.com/bombfuse_dev) is an arcade/roguelite where you whack Groobles.
Built on top of [Emerald](https://gamedev.rs/news/020/#emerald).

Harvest Hero has undergone a large change, migrating from semi-randomly generated levels to handcrafted levels that are randomly selected throughout your playthrough.

This means using [Ogmo](https://ogmo-editor-3.github.io/) to design levels,
and using [nano-ogmo](https://github.com/Bombfuse/nano-ogmo) to import them.

Updates:

- General UI update
- Importing ogmo levels via nano-ogmo
[April Fools demo](https://bombfuse.itch.io/him-character-demo-harvest-hero)



![Station Iapetus Youtube](../../assets/0bfe3eed410d2573.png)

[Station Iapetus](https://github.com/mrDIMAS/StationIapetus) by [@mrDIMAS](https://github.com/mrDIMAS) is a 3rd person shooter on the
prison Iapetus near the Saturn.
This month’s updates include:

- Inventory fixes and improvements
- Splash damage for grenades
- Weapon recoil
- More items
- Bots now hear player
- More assets
- First level improvements
- Procedural animation of impact for bots
- More sounds
- Separate scene for menu with music
- Pause game when in menu
- More switches in options menu
- Turrets

[Way of Rhea](https://store.steampowered.com/app/1110620?utm_campaign=tmirgd&utm_source=n20) is a picturesque puzzle platformer—without the platforming.
Solve mind bending color puzzles, unlock new areas of a vibrant hub world, and
talk to NPCs to unravel the mysteries of a world you left behind!

Way of Rhea is being produced by [@masonremaley](https://twitter.com/masonremaley). Latest Way of
Rhea developments:

- A free demo was distributed as part of
[Indie Maker Syndicate](https://indiemakersyndicate.com/)’s online event - The demo included a number of minor visual improvements
[aimed at better communicating the game’s mechanics](https://twitter.com/masonremaley/status/1375534918646763528) - Progress is being made adding
[new artwork](https://twitter.com/masonremaley/status/1377693351198216193)to the game - Tools for laying out artwork in game were
[improved](https://twitter.com/masonremaley/status/1377736615997636611) - A crash reporter was implemented to give players the option to report issues
directly to
[Way of Rhea’s Discord](https://discord.gg/JGeVt5XwPP). A writeup will be posted explaining how it works soon! - Work has begun on a dialog system for chatting w/ NPCs!

## Engine Updates [#](https://gamedev.rs#engine-updates)

[Tetra](https://github.com/17cupsofcoffee/tetra) is a simple 2D game framework, inspired by XNA, Love2D, and Raylib. This
month, versions 0.6.1 and 0.6.2 were released, featuring:

- Support for blend modes and premultiplied alpha
- Scissor rectangles (useful for UI rendering)
- Word wrapping for text
- More events and methods for tracking/controlling the window’s state
- Bugfixes and docs improvements

For more details, see the [changelog](https://github.com/17cupsofcoffee/tetra/blob/main/CHANGELOG.md).

Additionally, a [template repository](https://twitter.com/17cupsofcoffee/status/1357750836370284544) has been created,
demonstrating some useful patterns for structuring a Tetra project.

![Current state of starframe graphics and physics](../../assets/cb64e9474d81230f.gif)


[Starframe](https://github.com/m0lentum/starframe) by [@molentum](https://twitter.com/molentum_) is a work-in-progress game engine for physics-y
sidescrolling 2D games.

This month, [its physics engine was revamped once more](https://twitter.com/molentum_/status/1360723470414450688)
(for the last time, hopefully),
implementing a modern solver method called Extended Position-Based Dynamics.
Also, [a blog post](https://molentum.me/blog/starframe-constraints/) was published, covering the
development of the physics engine so far in a great deal of mathematical
detail.

### Emerald [#](https://gamedev.rs#emerald)

![emerald_logo](../../assets/372cc7c5ca283a80.png)


[Emerald](https://github.com/Bombfuse/emerald) by [@bombfuse](https://twitter.com/bombfuse_dev)
is a 2D game engine focused on being as portable as possible.

The ultimate goal of Emerald is to be a fully featured engine
that you can slap onto any device with relative ease.
It’s currently able to run on WASM, Raspberry Pi, Mac, Windows, and Linux
thanks to [miniquad](https://github.com/not-fl3/miniquad).

Features include physics via [rapier2d](https://github.com/dimforge/rapier),
ECS via [hecs](https://github.com/Ralith/hecs), and font rendering via [fontdue](https://github.com/mooman219/fontdue).

Recent updates:

- Rendering to textures was added (
[example](https://github.com/Bombfuse/emerald/blob/eb38d868a/examples/render_to_texture.rs)). [WASM game sample](https://bombfuse.itch.io/him-character-demo-harvest-hero).

![rg3d Youtube](../../assets/8055115a88c863e6.png)


[rg3d](https://github.com/mrDIMAS/rg3d) ([Discord](https://discord.gg/xENF5Uh), [Twitter](https://twitter.com/DmitryNStepanov)) is a game engine that
aims to be easy to use and provide a large set of out-of-box features. Some of
the recent engine updates:

- Context menus and tooltips (huge thanks to
[MinusGix](https://github.com/MinusGix)). - Performance improvements for UI.
- Parallax Mapping.
- Ability to enable/disable scenes.
- Expansion strategies for TreeView.
- LOD system fixes.
- Graphical fixes.
- First version of engine’s architecture overview.
- Various bug fixes and small improvements.

[Editor](https://github.com/mrDIMAS/rusty-editor) updates:

- Ability to edit collision groups and mask for colliders.
- Ability to clear command stack.
- Ability to change render path for meshes.
- LOD editor.
- “Collapse All”, “Expand All”, “Locate Selection” buttons for world outliner.
- “Fit Collider” feature fixes.
- Picking fixes.
- Change selection when paste from clipboard.
- “Slow” and “Fast” camera movement modifiers.
- Navmesh selection fixes.
- Simple TBN visualizer.
- Parallax mapping switch in settings.

![Oxygengine + RAUI integration](../../assets/8f682ca369b51f7c.gif)

[Oxygengine](https://github.com/PsichiX/Oxygengine) by [@PsichiX](https://twitter.com/psichix) is the hottest
HTML5 + WASM game engine for games written in Rust with web-sys.
The goal of this project is to combine professional game development tools under
one highly modular toolset.

- Version 0.16.0 was focused on integration of
[RAUI](https://github.com/PsichiX/raui)crate into the engine to allow building rich UI/UX experience for your games using declarative mode UI composition (which now makes currently used simple UI Elements feature deprecated and it’s gonna be removed at some point in the near future). - In addition to that
[basic web game demo](https://github.com/PsichiX/Oxygengine/tree/master/demos/basic-web-game)and[pokemon-like RPG demo](https://github.com/PsichiX/Oxygengine/tree/master/demos/pokemon)were enhanced with new UI showing how to build UI/UX with RAUI. - Next months will be focused on making RPG showing full potential of what you can do with RAUI in Oxygengine, as well as remaking Visual Novel module to be entirely based on RAUI in a way similar to how RenPy is made!

![PBR material example](../../assets/f1b687168edecb30.png)

[Bevy](https://bevyengine.org) is a refreshingly simple data-driven game engine built in Rust. It is
[free and open source](https://github.com/bevyengine/bevy) forever!

Bevy 0.5 was a massive community effort. You can check out the
[full release blog post here](https://bevyengine.org/news/bevy-0-5), but here are some highlights:

- Physically Based Rendering (PBR).
- GLTF Improvements, such as support for PBR textures and a new top-level GLTF asset type.
- Bevy ECS V2: a complete rewrite of the Bevy ECS core with a hybrid component storage model, Archetype Graphs, stateful queries, and across-the-board performance improvements.
- A brand new Parallel System Executor packed with features: explicit system dependencies, system labels, system sets, improved run criteria, and increased parallelism.
- Reliable change detection: efficiently query changes to any component or resource at any point in time (even across frames).
- State System Rewrite: a new stack-based state system that makes running systems for different states (ex: menus vs in-game) much easier.
- Rich text: style text “spans” with different colors / fonts while still respecting layout.
- HIDPI text: render crisp text at any resolution.
- 2D world space text, world to screen space conversions, 2d/3d orthographic camera improvements, render layers, sprite flipping, improved color space handling, wireframes, timer improvements, and more!

*Discussions:
/r/rust,
Hacker News,
Twitter*

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

![A screenshot from the middle of the game](../../assets/99aa228d69251bca.jpg)


This month Tammy Xu published an article about [Alex Butler](https://twitter.com/bigabgames)’s two-year journey
of creating [Robo Instructus](https://store.steampowered.com/app/1032170/Robo_Instructus).
The article touches lots of topics like:
why a custom game engine in Rust was choosen, design of the custom
scripting language, and game design of programming puzzles.

The Unofficial Bevy Cheatbook by @jamadazi is a practical reference book for
the [Bevy Game Engine](https://bevyengine.org). It teaches programming patterns, features, and
solutions to common problems. Written to be concise and easy to learn from.

The book recently got a major overhaul for the big new Bevy 0.5 release. Many pages were expanded or rewritten, new content added, and community feedback addressed.

If you are interested in Bevy, this book is now one of the most detailed learning resources. Have fun making cool things with Bevy!

[Bevy game template](https://github.com/NiklasEi/bevy_game_template) by [@nikl_me](https://twitter.com/nikl_me)
is a template repository for a Bevy game.

The goal is to present a possible structure for Bevy games and at the same time reduce the amount of copy paste when starting a new project. The repository includes a GitHub workflow for Linux, MacOS, and Windows builds (WASM will be supported soon) and comes with a small, opinionated example game.

![NES Tetris with Hard Drop and Ghost Piece](../../assets/dca74a53aa317fd0.gif)

A [blog post](https://www.gridbugs.org/reverse-engineering-nes-tetris-to-add-hard-drop) describing the process of reverse-engineering
the rendering and input-handling logic in the NES version of Tetris, and using
a [rust embedded domain-specific language](https://github.com/stevebob/mos6502/blob/master/tetris-hard-drop-patcher/src/main.rs#L23) to
make a [patching tool](https://github.com/stevebob/mos6502/tree/master/tetris-hard-drop-patcher) that generates code (6502
machine code) to add hard drop (instantly dropping the current piece) and to
render a ghost piece (the dotted outline showing where the current piece will
land).

The patching tool uses the crate
[mos6502_assembler](https://github.com/stevebob/mos6502/tree/master/assembler) to specify 6502 assembly in
rust and generate machine code. Many of the reverse-engineering experiments
were done using [this rust NES emulator](https://github.com/stevebob/mos6502/tree/master/nes-emulator). The
result is available as an [IPS Patch](https://github.com/stevebob/mos6502/raw/master/tetris-hard-drop-patcher/tetris-hard-drop.ips).

*Discussions:
Hacker News,
/r/rust*

[@kettlecorn](https://twitter.com/kettlecorn) wrote
a beginner-friendly [tutorial](https://ianjk.com/ecs-in-rust/) that dives into the
inner workings of the Entity-Component-System pattern.
The tutorial walks through a minimalist ECS
implementation to illustrate how the pattern works, and
why it’s useful.

*Discussion:
/r/rust*

### Writing a 3D Shooter Using rg3d [#](https://gamedev.rs#writing-a-3d-shooter-using-rg3d)

[@mrDIMAS](https://github.com/mrDIMAS) started a tutorial series about making a 3D shooter
using the [rg3d](https://github.com/mrDIMAS/rg3d) game engine.
So far three parts were released:

[“Character Controller”](https://rg3d.rs/tutorials/2021/03/05/tutorial1.html)- engine & editor basics, simple character controller.[“Weapons”](https://rg3d.rs/tutorials/2021/03/09/tutorial2.html)- player weapon with recoil and simple impact effect.[“Bots, AI”](https://rg3d.rs/tutorials/2021/03/11/tutorial3.html)- bots, actor animations, and a simple AI.

![Tile map with basic agents and resources](../../assets/b0b1b5d62ec7052a.png)


[@philipk](https://github.com/philipk) shared a [blog post](https://philipk.github.io/devblog/blog/tdd-gamedev-feedback-loop) about using tests not only
for verifying correctness, but also for faster feedback loops in some
circumstances. [RobotCards](https://philipk.github.io/devblog/robotcards) - a WIP game that uses the Legion ECS -
is used as a practical example.

*Discussions:
/r/rust_gamedev*

## Library & Tooling Updates [#](https://gamedev.rs#library-tooling-updates)

[genesis](https://github.com/StygianLightning/genesis) by [@StygianLightning](https://github.com/StygianLightning) is a library for generating statically-typed
ECS worlds by using a procedural macro.

Unlike other ECS libraries and frameworks, which do dynamic borrow-checking at runtime, you define all your components upfront and generate a completely statically typed ECS, with borrow checking done at compile time. Gone are the days of passing a World between functions, only to encounter a dynamic borrow checking problem!

genesis is a lightweight ECS library that doesn’t provide any scheduling capabilities. Instead, you can query the storage for each component type directly.

[Shipyard](https://crates.io/crates/shipyard) by [@leudz](https://github.com/leudz) is an ECS library built on top of sparse sets
and focused on usability and speed.

Main changes of the [latest version](https://users.rust-lang.org/t/shipyard-0-5-release/57203):

- The
`system!`

macro, packs, and`Shiperator`

trait were removed. - Bulk add entity - faster way than adding entities one by one.
- Accurate modification tracking by default.
- No more
`try_*`

- now all functions that can fail because of storage access return a Result while almost all others panic. - More flexible workload building and debugging.
- Customizable views and storages.
- Significant performance improvements.

![planck logo](../../assets/ab5487d53617fb53.png)


[Planck ECS](https://github.com/jojolepro/planck_ecs) ([GitHub](https://github.com/jojolepro/planck_ecs), [Blog](https://jojolepro.com/blog/2021-01-13_planck_ecs/),
[Patreon](https://patreon.com/jojolepro)) by [@jojolepro](https://github.com/jojolepro)
is a brand new minimalist and safe ECS library.

The 1.0 release happened in the past month, featuring: various fixes, quality of life improvements, removal of unsafe code and completion of tests and documentation.

The library is currently considered completed, which means that all planned features are implemented, tested and benchmarked. Future updates will focus on performance improvements and usability improvements.

[Planck ECS](https://github.com/jojolepro/planck_ecs) is also used in [Shotcaller](https://github.com/amethyst/shotcaller) which is featured in
this newsletter too.

You can read more about the library on the [Blog](https://jojolepro.com/blog/2021-01-13_planck_ecs/) and on
[GitHub](https://github.com/jojolepro/planck_ecs).

*Discussions: /r/rust*

[hecs](https://github.com/Ralith/hecs) is a fast, lightweight, and unopinionated archetypal ECS library.

Version 0.5 introduces a column-major serialization mode. This imitates the in-memory data layout, enabling higher performance than the already-fast row-major serialization mode. Because columnar layout places similar data nearby, it also improves the effectiveness of compression.

Other changes include major optimizations to spawning entities and adding/removing components, inspired by the archetype graph model recently adopted by bevy.

[rkyv](https://github.com/djkoloski/rkyv) is a zero-copy deserialization framework for Rust. It’s similar to FlatBuffers
and Cap’n Proto and can be used for data storage and messaging.

A [benchmark](https://github.com/djkoloski/rust_serialization_benchmark) was put together to compare rkyv
against other leading serialization solutions and gather feedback and use
cases for development. A [summary and analysis](https://davidkoloski.me/blog/rkyv-is-faster-than) of the
results is also available.

Version 0.5 is hot off the presses and rolls up features from the 0.4 development cycle:

- Derive macros can now implement
`PartialEq`

and`PartialOrd`

between archived and unarchived types. - Custom type bounds for serialization and deserialization can be added with derive attributes.
- Helper types like
[AlignedVec](https://docs.rs/rkyv/0.5.0/rkyv/struct.AlignedVec.html)and[Infallible](https://docs.rs/rkyv/0.5.0/rkyv/struct.Infallible.html)were introduced to improve ergonomics. `const_generics`

are now enabled by default.- Helper functions have been added to make getting root objects easier.
- Several bugfixes and performance improvements.

A [feedback issue](https://github.com/djkoloski/rkyv/issues/67) is still open for providing feedback on
further development.

[gba](https://github.com/rust-console/gba) is a crate for making GBA games with Rust.
This month it was updated to 0.4!
It’s using the new `thumbv4-none-eabi`

target, and has
an overall simpler build process than before.

The project is still a work in progress, but if you’ve wanted to try an embedded experience this is an easy way to test the waters. No hardware required! Compiled binaries can be run in a GBA emulator just fine.

[kira](https://github.com/tesselode/kira) by [@tesselode](https://twitter.com/tesselode) is a game audio library tailored to composers and other
people who need expressive audio.

v0.5.0 was released with mixer send tracks, new effects, and playback position tracking for instances, as well as a variety of smaller improvements.

[Quinn](https://github.com/quinn-rs/quinn) is an async-friendly implementation of the state-of-the-art QUIC
transport protocol soon to be standardized by the IETF.

QUIC is a uniquely versatile foundation for building application protocols. Its support for low-latency communication, multiplexing, fine-grained reliability, and security make an excellent basis for real-time game networking, providing an array of powerful primitives unavailable on UDP or TCP.

[Quinn 0.7](https://github.com/quinn-rs/quinn/releases/tag/0.7.0) introduces support for Tokio 1.0 and many
optimizations and bug fixes, and updates to [draft 32](https://tools.ietf.org/html/draft-ietf-quic-transport-32) of the proposed
standard. With last call underway in the IETF, the devs expect to release an
implementation of the final standard soon with no major changes.

[nakama-rs](https://github.com/not-fl3/nakama-rs) is a pure Rust implementation of the [Nakama](https://heroiclabs.com/) protocol.

[Nakama](https://heroiclabs.com/) is an open-source server designed to power modern games and apps.
Features include user accounts, chat, social, matchmaker, realtime multiplayer,
and much [more](https://heroiclabs.com).

Being pure Rust, [nakama-rs](https://github.com/not-fl3/nakama-rs) brings the full API and socket options to any
platform Rust works on.

The [smaa-rs](https://github.com/fintelia/smaa-rs) library provides fast and high quality post-process
anti-aliaising using the [SMAA algorithm](http://www.iryoku.com/smaa/). It is designed to be
easy to integrate into other [wgpu](https://github.com/gfx-rs/wgpu-rs) applications with only a few
added lines of code.

The 0.2 series released this month includes a steamlined API which makes it easier to enable/disable anti-aliasing via a configuration setting. Currently SMAA 1x is supported with SMAA S2x likely to be added depending on interest.

![voxel bunny on wgpu](../../assets/3828f4f17590451d.png)

[wgpu](https://github.com/gfx-rs/wgpu-rs) is a [WebGPU](https://gpuweb.github.io/gpuweb/) implementation in Rust. It is safe, efficient,
and portable: can target both native (Vulkan/D3D/Metal) and the Web.

Most progress in March was focused around [WGSL](https://gpuweb.github.io/gpuweb/wgsl/) shaders and validation.
[naga](https://github.com/gfx-rs/naga) has seen a lot of improvements in the SPIR-V and WGSL parsing, as well
as backend code generation. Most importantly, it now fully validates both
statements and expressions. No more accidental foot shots from adding vec2
and vec3 in the shaders!

The last and the biggest (in terms of shader complexity) example - “water” has been successfully ported to WGSL 🎉.

A small addition to our native-only features - conservative rasterization
feature - was added by [@wumpf](https://github.com/Wumpf) and demonstrated on a voxel bunny 🐇

Finally, there is a blog post on Mozilla [graphics team blog](https://mozillagfx.wordpress.com/2021/03/10/webgpu-progress/) about the
progress using [wgpu](https://github.com/gfx-rs/wgpu-rs) in Gecko.

*Discussions:
/r/rust_gamedev*

![A Sci-Fi helmet model](../../assets/06f078c2649fd829.jpg)

[glTF model viewer](https://github.com/msiglreith/grr-gltf)created by

[@msiglreith](https://github.com/msiglreith)using rust-gpu

[rust-gpu](https://shader.rs) is a new codegen backend by Embark Studios for Rust, aimed at making
Rust a first class language for writing GPU shaders!
This past month was the [release of rust-gpu v0.3](https://github.com/EmbarkStudios/rust-gpu/releases/tag/v0.3.0).
Some of the highlights:

- A lot of technical debt that was visible to users
(such as
`#[allow(unused_attributes)]`

) was removed. - rust-gpu now also supports basic ADT enums and has a whole inference pass for storage class variables.
- All Embark’s shaders for their internal engine
[are now written in Rust](https://twitter.com/repi/status/1365256477569667075)- no more GLSL/HLSL, just Rust for all CPU & GPU code!

Full release notes are available [here](https://github.com/EmbarkStudios/rust-gpu/releases/tag/v0.3.0).

For more information on how to get started with using rust-gpu in your projects,
check out [the Rust-GPU Dev Guide](https://embarkstudios.github.io/rust-gpu/book/).

*Discussions:
/r/rust*

![rafx tilemap rendering](../../assets/4befb33cc2663c19.png)

[LDTK level editor](https://ldtk.io)

Rafx is a multi-backend renderer that optionally integrates with the
[distill](https://github.com/amethyst/distill) asset pipeline. This month, a fourth layer
was introduced to the library, `rafx-renderer`

. It provides a plugin system,
simplifying framework setup in a project.

The demo now includes a tilemap renderer that integrates with the [LDTK level
editor](https://ldtk.io). The `distill`

integration processes the level files offline
for very efficient loading/rendering at runtime.

Sprite rendering in general is also much faster now. Scenes with 40k-100k sprites can render at 60fps (measured on M1 mini) depending on transparency/distinct Z values in the scene. New examples demonstrate tilemap and sprite rendering.

Early work was also done to reuse descriptor sets across frames and reduce dynamic memory allocation when working with descriptor sets. Rafx also includes more options for HDR tonemapping.

![femtovg](../../assets/2086f41982ae4329.png)


FemtoVG is a 2D canvas like vector graphics library based on nanovg that has been previously featured in this newsletter.

This month, the FemtoVG team has implemented a new rendering backend based on
the `wgpu`

library. This work is being done in this [fork](https://github.com/adamnemecek/femtovg) of
FemtoVG and will be merged into the main repo soon. The team is currently
looking for users to try out the new backend and provide feedback.

Join the [FemtoVG Discord channel](https://discord.gg/V69VdVu).

### Kajiya [#](https://gamedev.rs#kajiya)

![A race car in its natural habitat inspired by the Cornell Box](../../assets/101f8474a5fd3fe1.gif)


Kajiya by [@h3r2tic](https://github.com/h3r2tic) is a real-time global illumination renderer.

It utilizes Vulkan Ray Tracing via [ash](https://github.com/MaikKlein/ash) and [hassle-rs](https://github.com/Traverse-Research/hassle-rs) to
implement multi-bounce light transport in fully dynamic scenes. By shooting
only two rays per pixel on average, it keeps performance high; thanks to a
voxel-based light cache and extensive spatio-temporal filtering, it keeps
noise low. It supports physically-based rendering of [GLTF](https://github.com/gltf-rs/gltf) scenes,
and achieves a close match to reference path-tracing.

Kajiya is still in its infancy, and not yet available to the public, but you
can get glimpses of its development by following the author on [Twitter](https://twitter.com/h3r2tic).

![pixel-perfect-collision-demo](../../assets/44076ca573e2ce2a.gif)

[example](https://github.com/katharostech/bevy_retro/tree/master/examples#collisions)

[Bevy Retro](https://github.com/katharostech/bevy_retro) is a new [Bevy](https://bevyengine.org) plugin designed for making pixel-perfect
games.

This project was released under the [Katharos License](https://github.com/katharostech/katharos-license). This
license has moral and ethical implications that you may or may not agree with,
so please read it before making use of this project.

Bevy Retro features:

- Web and desktop support out of the box - it even runs in Safari on iOS!
- Integer pixel coordinates - no need to round floats to keep pixels aligned!
- Support for sprites, sprite sheets and animations.
- A super simple hierarchy system.
- A custom, scaled, pixel-perfect renderer with three camera modes: fixed width, fixed height, and letter-boxed.
- An
[LDtk](https://ldtk.io)map loading plugin. - Pixel-perfect collision detection.
- Support for post-processing effects using custom shaders or the built-in CRT filter.
- Support for custom pixel aspect ratios.

Feel free to discuss the project and provide feedback
[on GitHub](https://github.com/katharostech/bevy_retro/discussions).

![RAUI + Tetra TODO app](../../assets/b90eb96617df2499.gif)

[RAUI](https://github.com/PsichiX/raui) by [@PsichiX](https://twitter.com/psichix) is a Renderer Agnostic User
Interface crate that is based on declarative mode UI composition similar to
React.js and UE4 Slate system.

This month’s updates:

- Advanced navigation system mainly for the use in
[Oxygengine](https://github.com/PsichiX/Oxygengine)game engine. [Tesselation renderer](https://github.com/PsichiX/raui/tree/master/raui-tesselate-renderer)module to allow buildings Vertex + Index + Batch buffers for backends that allows to render meshes.[Tetra integration](https://github.com/PsichiX/raui/tree/master/raui-tetra-renderer)crate that allows use of RAUI with[Tetra](https://github.com/17cupsofcoffee/tetra)game framework.- Porting
[demos](https://github.com/PsichiX/raui/tree/master/demos)to Tetra which became one of two mainly supported backends for RAUI.

![Code example of usage of this library.](../../assets/71e27b58682bd1de.png)

[egui-macroquad](https://github.com/optozorax/egui-macroquad) is a small library to use [egui](https://github.com/emilk/egui) inside of
[macroquad](https://github.com/not-fl3/macroquad). It consists only of two functions.

Used in [Portal Explorer](https://github.com/optozorax/portal), see the section above.

[building-blocks](https://github.com/bonsairobo/building-blocks) v0.6.0 [#](https://gamedev.rs#building-blocks-v0-6-0)

![LOD Terrain](../../assets/1de52d9889a37890.jpg)


In v0.6.0, the [building-blocks](https://github.com/bonsairobo/building-blocks) voxel library brings a couple important features
for scaling up to large maps:

- pyramids for level of detail
- multichannel arrays

There is still much work to be done to optimize the voxel mesh LOD at large
scales and improve the cosmetics of LOD transitions, but the preliminary work
has allowed us to demonstrate the feasibility of this approach with a new demo
that you can view [here](https://youtube.com/watch?v=fCP8xZYJiSI).

Full release notes are available on [here](https://github.com/bonsairobo/building-blocks/releases/tag/v0.6.0).

*Discussions:
/r/rust*

![whattheframe gui](../../assets/f5b36db759145370.png)


[WhatTheFrame](https://github.com/JMS55/whattheframe) by [@JMS55](https://github.com/JMS55)
is a frame-based cpu profiler crate along with a [GTK](https://gtk.org/) ([gtk4-rs](https://github.com/gtk-rs/gtk4-rs#gtk4-rs-)) based GUI.

This project aims to answer the question: Which frames of my game are slow, and why?

It aims to be simple to use, consisting of only 3 functions: Call `let _r = Profiler::new_frame()`

at the start of each frame, `let _r = Profiler::new_task("task_name")`

whenever you
want to profile a task, and finally `Profiler::end_profiling()`

once at the end.

You can then open the resulting `.wtf`

profile in the GUI and analyze the results.

This month was spent designing and implementing both the GUI and profiler crate. The core functionality of both programs are complete, and all that remains is cleanup, tweaks, optimization, and finally packaging the GUI up.

![Bitmapflow interpolating a walking mech animation](../../assets/db2794ddf9756678.gif)

Bitmapflow ([GitHub](https://github.com/Bauxitedev/bitmapflow)) by [@bauxitedev](https://twitter.com/bauxitedev) is a tool to help you
generate [inbetweens](https://en.wikipedia.org/wiki/Inbetweening) for animated sprites. In other words, it makes your
animations smoother. It uses [optical flow](https://en.wikipedia.org/wiki/Optical_flow) to try to guess how the pixels move
between frames, and blends them accordingly. The results are far from perfect,
and probably require some editing by hand afterwards, but it can produce decent
results.

It supports loading and saving animated gifs, spritesheets and individual frames.

The tool is written using godot-rust and executables are available for Windows, although Linux support will be coming soon. (If you compile the program from source, it already works on Linux.)

A full demonstration and walkthrough of the program is available on
[YouTube](https://youtube.com/watch?v=rC359dDAMiI).

You can try it out yourself on [itch.io](https://bauxite.itch.io/bitmapflow).

*Discussions: /r/rust_gamedev*

!["Graphite" drawn using the circles and rectangles of the new tool drawing system](../../assets/a7ff2f0e7f04812c.png)

Graphite ([GitHub](https://github.com/GraphiteEditor/Graphite), [Discord](https://github.com/GraphiteEditor/Graphite/blob/master/README.md#discord),
[Twitter](https://twitter.com/GraphiteEditor)) is an in-progress vector and
raster graphics editor built on a nondestructive node-based workflow.

The team has grown from 1 to 5 in the past month and major progress was made
building core architectural Rust code. A large accomplishment was designing the
[software architecture diagram](https://files.keavon.com/-/CostlyViolentPurplemarten/Architecture_Diagram.png).

The current editor now has functional Select, Rectangle, and Ellipse tools
thanks to the newly-added tool state machine and SVG viewport drawing. The UI
now also implements tool-related icons and buttons, bringing it closer to
parity with the design mockup. The team also set up a Web/Rust-WASM build
system, GitHub CI to confirm PRs compile, and put together
[starter documentation](https://github.com/GraphiteEditor/Graphite/blob/master/docs/index.md) for the codebase, UX design, and manual.

Graphite is making rapid progress towards becoming a nondestructive, procedural
graphics editor suitable of replacing traditional 2D DCC applications. Please
[join the Discord](https://github.com/GraphiteEditor/Graphite/blob/master/README.md#discord) - and consider asking for a tour of the
code and how you can help!

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

[femtovg is looking for help with the wgpu backend](https://reddit.com/r/rust/comments/mfuo4m/femtovg_2d_vector_graphics_crate_is_looking_for).[Embark’s open issues](https://github.com/search?q=user:EmbarkStudios+state:open)([embark.rs](https://embark.rs)).[gfx-rs’s “contributor-friendly” issues](https://github.com/gfx-rs/gfx/issues?q=is%3Aissue+is%3Aopen+label%3Acontributor-friendly).[wgpu’s “help wanted” issues](https://github.com/gfx-rs/wgpu-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).[luminance’s “low hanging fruit” issues](https://github.com/phaazon/luminance-rs/issues?q=is%3Aissue+is%3Aopen+label%3A%22low+hanging+fruit%22).[ggez’s “good first issue” issues](https://github.com/ggez/ggez/labels/%2AGOOD%20FIRST%20ISSUE%2A).[Veloren’s “beginner” issues](https://gitlab.com/veloren/veloren/issues?label_name=beginner).[Amethyst’s “good first issue” issues](https://github.com/amethyst/amethyst/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[A/B Street’s “good first issue” issues](https://github.com/a-b-street/abstreet/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).[Mun’s “good first issue” issues](https://github.com/mun-lang/mun/labels/good%20first%20issue).[SIMple Mechanic’s good first issues](https://github.com/mkhan45/SIMple-Mechanics/labels/good%20first%20issue).[Bevy’s “good first issue” issues](https://github.com/bevyengine/bevy/labels/good%20first%20issue).

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!