---
title: 'This Month in Rust GameDev #33 - April 2022'
url: https://gamedev.rs/news/033/
author: Rust GameDev WG
published: '2022-05-14'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the 33rd issue of the Rust GameDev Workgroup’s
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

[Announcements](https://gamedev.rs/news/033/#announcements)[Game Updates](https://gamedev.rs/news/033/#game-updates)[Engine Updates](https://gamedev.rs/news/033/#engine-updates)[Learning Material Updates](https://gamedev.rs/news/033/#learning-material-updates)[Tooling Updates](https://gamedev.rs/news/033/#tooling-updates)[Library Updates](https://gamedev.rs/news/033/#library-updates)[Other News](https://gamedev.rs/news/033/#other-news)[Requests for Contribution](https://gamedev.rs/news/033/#requests-for-contribution)[Jobs](https://gamedev.rs/news/033/#jobs)

## Announcements [#](https://gamedev.rs#announcements)

### Rust GameDev Meetup [#](https://gamedev.rs#rust-gamedev-meetup)

![Gamedev meetup poster](../../assets/597a6fd38dad8f32.png)


The 15th Rust Gamedev Meetup took place in April. You can watch the recording of
the meetup [here on Youtube](https://youtu.be/okWFrfaaADs). The meetups take place on
the second Saturday every month via the [Rust Gamedev Discord
server](https://discord.gg/yNtPTb2) and are also [streamed on
Twitch](https://twitch.tv/rustgamedev). If you would like to show off what you’ve been
working on at the next meetup on [May 14th](https://everytimezone.com/s/1baaa280), fill out [this
form](https://forms.gle/BS1zCyZaiUFSUHxe6).

### Rust Graphics Meetup 2 [#](https://gamedev.rs#rust-graphics-meetup-2)

The 2nd Rust Graphics Meetup will take place on the [21st of May, at 16:00
UTC+0](https://everytimezone.com/s/b6ec5c17). This meetup is a chance to show off what you’ve
been working on in the graphics community, or see what other people have been
doing!

If you’re interested in speaking, please fill out the
[form](https://forms.gle/DyvZ4WFZanTaLGGa7). You can also [watch one of the
talks](https://www.youtube.com/watch?v=F0wGz5UJTrY) from the first meetup.

### RustConf Arcade Cabinet [#](https://gamedev.rs#rustconf-arcade-cabinet)

![arcade cabinet](../../assets/0ff1d50b9dccd4f9.gif)


[Carlo](https://twitter.com/carlosupina) is building a custom arcade cabinet that will be at
RustConf 2022 in Portland. It is an opportunity for Rust game developers to
share their games with the broader community. If you are interested in getting
your game on the cabinet, read [this Twitter thread](https://twitter.com/carlosupina/status/1523715837726961664) and
fill out the [interest form](https://forms.gle/onFm5fCygdbiArqJ7).

## Game Updates [#](https://gamedev.rs#game-updates)

![way of rhea capsule image](../../assets/6af011601c5cc1a7.jpg)


[Way of Rhea](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n33) is a puzzle adventure with hard puzzles and forgiving
mechanics being produced by [@masonremaley](https://twitter.com/masonremaley) in a custom Rust
engine. It has a demo available [on Steam](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n33).

Way of Rhea was recently [shown off at PAX East!](https://twitter.com/AnthropicSt/status/1517129411790843905) A [minor
patch](https://steamcommunity.com/games/1110620/announcements/detail/3175611379276019942?utm_campaign=tmirgd&utm_source=n32&utm_content=news) has been released to the demo with post-PAX fixes:

- An issue that made the last puzzle in the third forest level difficult to navigate with a controller was worked around
- Colliders in the Hermes puzzle were fixed (previously you could land on top of a gate if you held left while sliding)
- The attract mode that was used at PAX has been merged (not in demo)
- More jungle biome scenery has been placed (not in demo)
- A crash at startup on CPUs that don’t support the
`andn`

instruction was fixed (part of the BMI extension to x64) - The game can now generate mini dumps on Windows and Linux in the event that it crashes and if given consent, forward them to the developer for analysis

You can stay up to date with the latest Way of Rhea developments by [following
it on Steam](https://store.steampowered.com/app/1110620/Way_of_Rhea/?utm_campaign=tmirgd&utm_source=n33), signing up for [their mailing list](https://www.anthropicstudios.com/newsletter/signup), or
joining [their Discord](https://discord.gg/JGeVt5XwPP).

### BITGUN [#](https://gamedev.rs#bitgun)

![BITGUN gameplay](../../assets/79d854a533c54aee.gif)

[BITGUN](https://store.steampowered.com/app/1673940/BITGUN/) ([Discord](https://discord.com/invite/XrGZQkq), [Twitter](https://twitter.com/LogLogGames)) by [@darth](https://github.com/darthdeus) and [@shosanna](https://github.com/shosanna) is an action
roguelite zombie shooter with difficult and satisfying combat you can learn and
master. Guns break quickly and you lose all your gear when you die.

The game was just released on Steam! It has been developed by a programming duo
called LogLog Games. They have been working on it for the past year and it is
their biggest game so far (they also have 2 smaller games). [BITGUN](https://store.steampowered.com/app/1673940/BITGUN/) is written
in Godot Engine but it is using Rust language extensively (it has around 7500
lines of Rust and 4200 lines of GDScript).

The main changes from the demo version of the game:

- New missions added with extra difficulty
- Improved AI which doesn’t just chase the player but behaves unpredictably
- New zombie types - ranged zombie, big spider, zombie spawner
- Added comic-book style story
- Improved tutorial and new player experience
- Reworked inventory system with simplified armor

*Discussion: /r/rust*

![Riding at night](../../assets/bafb002393755701.jpg)

[Veloren](https://veloren.net) is an open world, open-source voxel RPG inspired by Dwarf
Fortress and Cube World.

For April Fool’s day, Veloren made a post about a new direction; [Need for
Voxels: Veloren Cart](https://veloren.net/veloren-direction/). Enjoy the read! Veloren also participated
in Reddit’s /r/place, and got a small place right below /r/rust. Several months
of project finances were processed, and [discussed in a blog
post](https://veloren.net/devblog-167#finances-by-angelonfira). The [Veloren Reading Club saw its 8th
episode](https://www.youtube.com/watch?v=ff9EXhCXmFY), which was on the topic of graphics and
particles. A [second Veloren Code Review session](https://www.youtube.com/watch?v=keI0VpjkgZg) was
held, in which two developers went through a merge request that focused on
combat numbers.

Work was done to improve how loadouts work, specifically surrounding inheritance from other configs. Tweaks were made to arthropods, which should make them more fun to fight. Work is being done to prepare for the 0.13 release, with a custom map being built, and a special treasure map being created for the launch party. Player bank storages are being developed, which will allow players to store excess items in towns.

April’s full weekly devlogs: “This Week In Veloren…”:
[#166](https://veloren.net/devblog-166),
[#167](https://veloren.net/devblog-167),
[#168](https://veloren.net/devblog-168),
[#169](https://veloren.net/devblog-169).

### Oasis of Lost Hope [#](https://gamedev.rs#oasis-of-lost-hope)

![Oasis of Lost Hope](../../assets/678695c3eb505182.jpg)


Oasis of Lost Hope is a game where fertile ground is steadily consumed by dark, barren land called blight. Water helps defend an area from being consumed, but reserves are finite. The player needs to collect ore to build more irrigation towers and delay doom for a few more seconds. Yet one thing is certain: the days of fertile land are counted.

The game is an entry for the Ludum Dare 50 Jam, the theme of which was “Delay
the Inevitable”. It has been developed by setzer22 and Bromeon and [open-sourced
on GitHub](https://github.com/Bromeon/LudumDare50). The game is built on top of godot-rust alongside GDScript.
The Rust language is not exactly known for fast prototyping, but with a slightly
less safety-conservative fork of godot-rust, the game jam experience was
surprisingly smooth. When modeling mechanics such as the expanding blight or the
water pipe network, Rust really showed its strength as a strongly typed and fast
language.

![Extremely Extreme Sports](../../assets/2a278c54ce8a05bb.gif)


[Extremely Extreme Sports](https://kuviman.itch.io/extremely-extreme-sports) ([GitHub](https://github.com/kuviman/extremely-extreme-sports),
[Discord](https://discord.gg/DZaEMPpANY)) is a multiplayer online downhill racing game [made for
Ludum Dare 50 game jam](https://ldjam.com/events/ludum-dare/50/extremely-exteme-sports), scored top 3 in fun. Explode the mountain,
and race against the avalanche as well as your friends.

Features:

- Online multiplayer
- Character customization
- Emoting
- A little bit of gameplay

Developed by [@kuviman](https://github.com/kuviman) using [custom engine](https://github.com/kuviman/geng). A [postmortem blog
post](https://kuviman.itch.io/extremely-extreme-sports/devlog/372532/extremely-extreme-sports-postmortem) was written about the jam experience, and it includes
postjam updates.

*Discussions: /r/rust_gamedev*

## Engine Updates [#](https://gamedev.rs#engine-updates)

![bevy mushroom](../../assets/22b416789b37cae2.jpg)

[Bevy](https://bevyengine.org) is a refreshingly simple data-driven game engine built in Rust. It
is [free and open source](https://github.com/bevyengine/bevy) forever!

Bevy 0.7 was a massive community effort. You can check out the [full release
blog post here](https://bevyengine.org/news/bevy-0-7), but here are some highlights:

[Skeletal animation and mesh skinning](https://bevyengine.org/news/bevy-0-7/#skeletal-animation)[GLTF animation importing](https://bevyengine.org/news/bevy-0-7/#gltf-animation-importing)[Unlimited* point lights in a scene](https://bevyengine.org/news/bevy-0-7/#unlimited-point-lights)[Improved clustered forward rendering: dynamic/adaptive clustering and faster, more accurate cluster assignment](https://bevyengine.org/news/bevy-0-7/#light-clustering-features-and-optimizations)[Compressed texture support (KTX2 / DDS / .basis): load more textures in a scene, faster](https://bevyengine.org/news/bevy-0-7/#compressed-gpu-textures)[Compute shader / pipeline specialization: Bevy’s flexible shader system was ported to compute shaders, enabling hot-reloading, shader defs, and shader imports](https://bevyengine.org/news/bevy-0-7/#bevy-native-compute-shaders)[Render to texture: cameras can now be configured to render to a texture instead of a window](https://bevyengine.org/news/bevy-0-7/#render-to-texture)[Flexible mesh vertex layouts in shaders](https://bevyengine.org/news/bevy-0-7/#flexible-mesh-vertex-layouts)[ECS improvements: Order systems using their names, Query::many_mut, use conflicting parameters in systems via ParamSets, WorldQuery derives](https://bevyengine.org/news/bevy-0-7/#ergonomic-system-ordering)[Documentation improvements: better examples, more doc tests, and more coverage](https://bevyengine.org/news/bevy-0-7/#documentation-improvements)[More audio control: pause, volume, speed, and looping](https://bevyengine.org/news/bevy-0-7/#audio-control)[Power usage options to enable only updating Bevy Apps when input occurs](https://bevyengine.org/news/bevy-0-7/#eventloop-power-saving-modes)

*Discussions:
/r/rust,
Hacker News,
Twitter*

### Dims [#](https://gamedev.rs#dims)

![dims foliage](../../assets/a2dd1d288a67ec37.jpg)

Dims is an open-world creation platform.

In their latest [dev log](https://www.youtube.com/watch?v=jgkhsY8aZO8) they demonstrate a new foliage rendering
and spawning system, which automatically spawns foliage and trees based on
“habitat rules”. This means a user can simply “paint” a world and it will get
populated with plants and rocks automatically.

They are also planning to host a screenshot competition in the next few weeks for anyone who would like to try out the platform and create their own landscapes. Sign up for the newsletter on their website to get notified when it starts!

*Discussions:
Foliage rendering on reddit,
Erosion tool on reddit*

![Eldiron Image](../../assets/66a77efc8d30eaf6.png)

[Eldiron](https://www.eldiron.com) ([GitHub](https://github.com/markusmoenig/Eldiron), [Discord](https://discord.gg/ZrNj6baSZU),
[Twitter](https://twitter.com/MarkusMoenig)) by [@markusmoenig](https://github.com/markusmoenig) is a creator for classic role
playing games (RPGs) written in Rust.

Eldiron v0.5 features inbuild tilemaps, a node-based behavior system and region editors.

Development Updates in April:

- Support for 4 layers of tiles for game regions. This enables transparency and support for top-down and isometric views.
- Game regions can now contain named areas.
- Areas can contain behavior nodes to spawn monsters, lay traps, or displace tiles (for example to open a door).
- New “Systems” module to create behavior for Combat and soon for Crafting, Magic and more. System behavior trees can be called from any character.

Eldiron v1 will be able to create any kind of RPG utilizing square tiles, like the classical Ultima series.

![Hotham Image](../../assets/ef7781cd3f93a291.png)

[Hotham](https://github.com/leetvr/hotham) is a game engine for standalone VR devices, trying to make VR
development just a little bit less painful.

0.2 has been released with some *breathtaking* maintenance and performance
improvements that make Hotham marginally easier to use. If you’re interested in
Rust and VR and haven’t checked out the project already, now is an excellent
time to do so.

A huge thank you to our sponsors and contributors (big hat-tip to @jmgao) and
the wonderful members of the [Hotham discord](https://discord.gg/SZEZUX6ZsQ).

## Learning Material Updates [#](https://gamedev.rs#learning-material-updates)

![Game Development with Rust and WebAssembly Book Cover](../../assets/1cb62762a1b22e4a.png)


[Game Development with Rust and WebAssembly](https://subscription.packtpub.com/product/game_development/9781801070973) by Eric Smith (a.k.a
[@paytonrules](https://www.twitter.com/paytonrules)) was published in April. It takes a
tutorial approach to lead the reader through building an endless runner using
Rust and WebAssembly. You can play the completed game [here](https://rust-games-webassembly.netlify.app).

From the summary: This book is an easy-to-follow reference to help you develop your own games, teaching you all about game development and how to create an endless runner from scratch. You’ll begin by drawing simple graphics in the browser window, and then learn how to move the main character across the screen. You’ll also create a game loop, a renderer, and more, all written entirely in Rust. After getting simple shapes onto the screen, you’ll scale the challenge by adding sprites, sounds, and user input. As you advance, you’ll discover how to implement a procedurally generated world. Finally, you’ll learn how to keep your Rust code clean and organized so you can continue to implement new features and deploy your app on the web.

[@HeavyRain266](https://github.com/HeavyRain266) published an article, ‘[Why I choose to build my game from
scratch](https://www.reddit.com/r/rust_gamedev/comments/uewu9h/reasons_why_i_choose_to_build_my_game_from/)’, a short story about their implementation of the game
‘Forbidden Valley’ from scratch in Rust. The author aims to show how much you
can learn from building your dream game without the help of any game engine.

*Discussions: r/rust_gamedev*

![devlog logo](../../assets/ce787440635b1822.jpg)


@hedgein ([GitHub](https://github.com/hedgein), [Twitch](https://twitch.tv/hedgein)) started a devlog
series called Brontefy Me. This series walks through the development of games in
the [Bevy engine](https://bevyengine.org). There are two episodes released so far. The [first
episode](https://www.youtube.com/watch?v=DdD6VhmEIiU) focuses on getting up and running with the
engine, and the [second episode](https://www.youtube.com/watch?v=tx31BKX0yIA) starts expanding into
game mechanics.

## Tooling Updates [#](https://gamedev.rs#tooling-updates)

![Logo](../../assets/3aa61ad81bc23fff.png)


[Vismut](https://gitlab.com/vismut-org/vismut) ([GitLab](https://gitlab.com/vismut-org/vismut), [Zulip](https://vismut.zulipchat.com)) by [@lukors](https://gitlab.com/lukors) will be a
procedural texturing tool.

[Version 0.5](https://gitlab.com/vismut-org/vismut/-/releases/v0.5.0) contains a brand new backend to create a better base
for future improvements. A [blog post](https://orsvarn.com/vismut-architecture/) describes the differences
between the old and the new architecture.

![Graphite](../../assets/767be69b7401e6a7.png)


Graphite ([website](https://graphite.rs), [GitHub](https://github.com/GraphiteEditor/Graphite),
[Discord](https://discord.graphite.rs), [Twitter](https://twitter.com/GraphiteEditor)) is a free
in-development raster and vector 2D graphics editor. It will be powered by a
node graph compositing engine that supercharges your layer stack, providing a
completely non-destructive editing experience.

The past month’s Sprint 14 has focused on further editor features and UX improvements:

-
**It’s your type:**The Text tool now provides over 1400 fonts with bold/italic styles from the Google Fonts library. -
**Oh snap!:**A refactor and polish pass on the snapping system provides better clarity and consistency. And shapes now have outlines on hover and selection for easier targeting. -
**Have a dialog:**Supported by a refactor that moved dialog layouts into the Rust backend, users can now create new documents of specified sizes and export artwork as PNG/JPG with new File menu dialogs. -
**Pack it up:**The web component of the stack was finally upgraded to Webpack 5 which cleans up a mess of outdated dependencies.

[Open the editor](https://editor.graphite.rs) in your browser and give it a try.

## Library Updates [#](https://gamedev.rs#library-updates)

![notan](../../assets/eb73ee23fef85b56.jpeg)


[Notan](https://github.com/Nazariglez/notan) is a simple and portable layer designed to create your own multimedia
apps on top of it without worrying about platform-specific code.

The main goal is to provide a set of APIs and tools that can be used to create your project in an ergonomic manner without enforcing any structure or pattern, always trying to stay out of your way. The idea is that you can use it as a foundation layer or backend for your next app, game engine, or game.

The latest version [v0.3.0](https://github.com/Nazariglez/notan/releases/tag/v0.3.0) comes with audio support for all platforms using as
default backend [oddio](https://github.com/Ralith/oddio) and [symphonia](https://github.com/pdeljanov/Symphonia).

## Other News [#](https://gamedev.rs#other-news)

- Other game updates:
[Last of the Sky Folk](https://ianjk.com/ld50)is a grapple-hook based platformer created for LD50.[Heute Nicht](https://eira-hx.itch.io/heute-nicht)rythm game is another LD50 submission.

- Other learning material updates
- PhaestusFox started a
[Bevy tutorial servies](https://reddit.com/r/rust_gamedev/comments/tz75eb/bevy_game_engine_tutorial_series)and[0.6 to 0.7 Migration Guide](https://reddit.com/r/rust_gamedev/comments/u4uhs2/bevy_06_to_07_migration_guide)YouTube series. [@TantanDev](https://twitter.com/TantanDev)released a[“Rust multi-threading code review”](https://youtube.com/watch?v=jkHqrkcEHRc)video.

- PhaestusFox started a
- Other library updates:
[tween](https://github.com/sanbox-irl/tween)is an std-optional tweening library, designed for use in games and animations.[cosync](https://github.com/sanbox-irl/cosync)provides a single-threaded, sequential, parameterized async runtime.[SuInput](https://github.com/Sorenon/Action-System)is an input system designed to give pancake and XR applications access to a huge range of input devices while minimizing the amount of complexity needed to support them.[bevy_blender v0.2](https://reddit.com/r/rust_gamedev/comments/u7acfc/update_on_bevy_blender_releasing_v02_and_inquiry)with lots of new features is out.


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