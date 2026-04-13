---
title: 'This Month in Rust GameDev #1 - August 2019'
url: https://gamedev.rs/news/001/
author: Rust GameDev WG
published: '2019-09-02'
source_blog: Rust Game Development Working Group
source_site: https://rust-gamedev.github.io/
category: game programming
fetched: '2026-04-13'
---

Welcome to the inaugural issue of the Rust Game Development Workgroup’s monthly (hopefully!) newsletter.

[Rust](https://rust-lang.org) is a systems language pursuing the trifecta:
safety, concurrency, and speed.
These goals are well-aligned with game development.

We hope to build an inviting ecosystem for anyone wishing
to use Rust in their development process!
Want to get involved? [Join the Rust GameDev working group!](https://github.com/rust-gamedev/wg#join-the-fun)

## News and Blog Posts [#](https://gamedev.rs#news-and-blog-posts)

Interested (maybe already invested?) in using Rust for game development? Please set aside a brief moment to answer this short survey about the current state of our GD ecosystem and what the GD working group can do to nurture it. 🌱

While we’d greatly appreciate a modicum of identifying information so we can easily connect with you for further discussions, sharing that information is optional. Only 3 questions in this survey are mandatory and we’ve saved the most important one for last.

The survey is now being processed for publishing. We’re still accepting responses until the survey has been published and subsequently closed for good.

Also, check out our previous post
[“Introducing the Rust Game Development Working Group”](https://rust-gamedev.github.io/2019/08/18/introducing-the-rust-game-development-working-group.html)
if you haven’t seen it yet
[[/r/rust](https://reddit.com/r/rust/comments/cs44vx/introducing_the_rust_game_development_working),
[twitter](https://twitter.com/rust_gamedev/status/1163137574812209152)].

[nphysics](https://nphysics.org) 0.12 release contains several long awaited features:

- The support for linear and non-linear
*continuous-collision detection (CCD)*with colliders on rigid bodies and sensors. There’s[a brand new page of the user guide](https://www.nphysics.org/continuous_collision_detection)about it. - Rigid body
*velocity damping*: this allows to artificially slow down some bodies. This is essential for, e.g., top-down 2D games where traditional coulomb friction cannot be used. - Rigid body
*maximum velocity*limit: it is possible to force a rigid body to never get a velocity higher than a threshold. - The possibility to use
*custom containers*for bodies, colliders, joints, and force generators. This helps overcoming some difficulties related to borrowing, and also help for the integration of nphysics with other solutions. The physics world structures will no longer own those containers.

With [ncollide](https://ncollide.org) 0.20, it is now possible to compute the time of impact
between two shapes undergoing an arbitrary rigid motion.
This is known as non-linear time-of-impact computation.
This is used by the new CCD integration on nphysics 0.12.

Watch [a “CCD support on nphysics 0.12” video](https://youtube.com/watch?v=EnjgJp9mKz0)
or [play with the online demo yourself](https://nphysics.org/demo_all_examples3)
(choose “CCD” in the “Select example” menu).

Also, check out
[“About the future of nphysics: a pure rust 2D and 3D real-time physics engine”](https://www.patreon.com/posts/about-future-of-28917514)
[[/r/rust](https://reddit.com/r/rust/comments/cm2858/about_the_future_of_nphysics_a_pure_rust_2d_and)].

### Way of Rhea [Trailer](https://youtube.com/watch?v=VIzqlI-gbAY) and [Steam Wishlist](https://store.steampowered.com/app/1110620/Way_of_Rhea) Announced [#](https://gamedev.rs#way-of-rhea-trailer-and-steam-wishlist-announced)



![Part of the trailer](../../assets/88c170e05f638453.gif)

[the full trailer](https://youtube.com/watch?v=VIzqlI-gbAY)

[A new trailer](https://youtube.com/watch?v=VIzqlI-gbAY) and the [Steam wishlist](https://store.steampowered.com/app/1110620/Way_of_Rhea)
were published for “Way of Rhea” by [Anthropic Studios](https://anthropicstudios.com).

Way of Rhea is an upcoming puzzle platformer that takes place in a world where you can only interact with objects that match your current color.

Take a look at [this Reddit comment](https://reddit.com/r/rust_gamedev/comments/co8kqd/way_of_rhea_trailer_steam_wishlist_announced/ewryjet) with a quick summary
about implementation and tooling.

*Discussions:
/r/rust_gamedev,
twitter*

![Veloren screenshot](../../assets/11a4c020ee99c8ff.png)


Veloren is an open-world, open-source multiplayer voxel RPG. The game is in an early stage of development, but is playable.

The 0.3 version was a long time coming, and there has been a ton added to Veloren. Here is a small list of the major changes in this version:

- XP and leveling
- Better combat, movement, and animations
- Enemies, bosses
- Better world generation, more biomes
- Build mode
- Caves, lanterns, lights, dungeons
- Character customization, multiple races
- Inventories (WIP)
- Day/night, better shaders, voxel shadows
- Many performance optimizations

*Discussions:
/r/rust*

Also, if you want to see how the work on 0.4 is going,
check out other August’s weekly devlog posts:
“This Week in Veloren…”
[#28](https://veloren.net/devblog-28),
[#29](https://veloren.net/devblog-29),
and [#30](https://veloren.net/devblog-30).

![RUZZT screenshot](../../assets/0f2adf1024f8e500.png)


[@yokljo](https://github.com/yokljo) published [RUZZT](https://github.com/yokljo/ruzzt) - a [ZZT](https://en.wikipedia.org/wiki/ZZT) game engine clone written in Rust.

My wife and I wrote this as a fun exercise, and went a lot further with it than originally anticipated. We wanted to try to replicate the original game’s behaviour by simply looking at it running in Dosbox and seeing if we could make RUZZT do the same thing. This means the code architecture is likely very different from the original game.

Eventually we did get far enough that it seemed like a waste of time to try to guess how some specific things were implemented, so we used a disassembler to make sure various behaviours worked correctly.


*Discussions:
/r/rust*

[oxygengine-navigation](https://github.com/PsichiX/Oxygengine/tree/master/oxygengine-navigation) - Navmesh Pathfinding System for ECS Games [#](https://gamedev.rs#oxygengine-navigation-navmesh-pathfinding-system-for-ecs-games)

![oxygengine-navigation interactive demo](../../assets/f2457414b4127e3f.gif)


[oxygengine-navigation](https://github.com/PsichiX/Oxygengine/tree/master/oxygengine-navigation) is a crate to perform pathfinding
on [navmeshes](https://en.wikipedia.org/wiki/Navigation_mesh).
It’s an ECS module (compatible with any SPECS engine)
and is a part of a bigger [Oxygen game engine](https://github.com/PsichiX/oxygengine).

Here’s a [demo/example of the integration with Amethyst](https://github.com/PsichiX/Oxygengine/tree/master/demos/amethyst-integration).

![amethyst logo](../../assets/6692a81ae6e6d242.png)


-
[Amethyst v0.12 quietly released](https://github.com/amethyst/amethyst/releases/tag/v0.12.0)and now the project moves to two-week release cycle. -
2D action platformer

[Space Menace](https://github.com/amethyst/space-menace)by[@krankur](https://github.com/krankur)partnered with Amethyst to become an official showcase project ([announcement](https://amethyst.rs/posts/space-menace-showcase)).![Space Menace screenshot](../../assets/d99f2c9048b5f1ae.png)

-
[Evoli](https://github.com/amethyst/evoli)released[v0.2](https://github.com/amethyst/evoli/releases/tag/v0.2.0)and[moved into 3D](https://community.amethyst.rs/t/evoli-v0-2-video-log-retrospective/1007).![Evlovi screenshot](../../assets/e5b4009a72de76c4.png)

-
New tools for 2D game development:

[the Sheep spritesheet packer and Amethyst 2D Starter](https://amethyst.rs/posts/tools-for-2d-games). -
Scripting support

[edges closer](https://community.amethyst.rs/t/scripting-what-do-we-need-to-get-there/958). -
Learning from Legion:

[an ECS design discussion](https://community.amethyst.rs/t/legion-ecs-discussion/965). -
[Arsenal](https://github.com/katharostech/arsenal)- a Blender game engine built on Amethyst and Rust ([announcement](https://community.amethyst.rs/t/arsenal-the-vision-for-a-full-amethyst-blender-integration/911)). -
[amethyst-imgui](https://github.com/amethyst/amethyst-imgui)and[Laminar](https://github.com/amethyst/laminar)(a semi-reliable UDP-based protocol for multiplayer games) steadily mature. -
[Rendy](https://github.com/amethyst/rendy)(rendering engine) is well[on its way towards web and OpenGL support](https://twitter.com/AmethystEngine/status/1159765804205957120). -
Atelier Editor underwent some

[visual planning](https://github.com/amethyst/atelier-editor/issues/21).

A few days ago a third showcase project
[was announced](https://amethyst.rs/posts/third-showcase-game-space-shooter):
[“Space Shooter”](https://github.com/amethyst/space_shooter_rs)
by [Carlo Supina](https://twitter.com/carlosupina)
[[/r/rust](https://www.reddit.com/r/rust/comments/cwy4qq/amethyst_showcase_space_shooter_shootem_up),
[twitter](https://twitter.com/carlosupina/status/1167094848907808768)].

![“Space Shooter” gameplay](../../assets/97f9bef7703bc330.gif)


![Embark logo](../../assets/31a149f3c48a2711.jpg)


A quote from the announcement:

We’ve put together a tracking page for our Rust open source work, future ideas/plans, and issues that we’ve run into and want to improve on.

It is still pretty early, but hope it can be useful or of interest to see what we, a commercial games company, is planning and thinking about Rust.

We are also open to collaborate with other companies or individuals, as well as sponsoring more open source work to improve and support the ecosystem. Feel free to reach out to us here or on

[opensource@embark-studios.com]!

Also, Embark has recently open-sourced [physx-rs](https://github.com/EmbarkStudios/physx-rs) - [PhysX](https://github.com/NVIDIAGameWorks/PhysX) bindings to Rust.

![“ball” example](../../assets/602eb3b2d5260293.png)


Quite complex big C++ project to build & bind to (

[@h3r2tic]did some magic). Eventually want full native Rust lib but PhysX is feature rich & performant today so nice to be able to use it!

![screenshot from Olivia’s game](../../assets/c47d31eb4ae2d780.png)


[@oliviff](https://twitter.com/oliviff) tells about theirs experience of developing a hobby game
“Tennis Academy” in Rust for six months.

Here’s [a YouTube video](https://www.youtube.com/watch?v=96qPwvDEAuI)
with the current state of the game.

Features of the game:

- 💵money: every item costs money and the money is substracted when buying an item
- 👟tennis courts of all types: hard, clay, concrete and grass
- 🎁more object types: benches, balls, roof tiles
- ⏱️time: the game keeps track of how many days/months/years it’s been
- 🌶️main menu
- 🏠build menu
- ⛹️player selection menu
- ↩️assignments: a player can be assigned to a court or a bench
- 🛣️basic pathfinding: a player can find its way to an assigned court or bench
- 📈skill levels: a player playing on a court will get increased tennis skill level
- 🛌needs: a player who plays too much will get tired and need rest

*Discussions:
/r/rust_gamedev,
twitter*

![Mipmap example](../../assets/be511dd26100e50b.png)


`gfx-hal`

is a low-overhead Vulkanic GPU API in Rust.
Version 0.3 is published that includes:

- MSAA resolves
- events API
- building Vulkan backend on Apple platforms
- “readonly” storage support in DX12 backend
- WASM and compute support in GL backend
- lots of fixes and improvements in all backends

*Discussions:
/r/rust*

`wgpu`

is a safe, modern and portable GPU API for native platforms and the Web.
It’s based on gfx-hal and Rendy.
Our implementation and its Rust wrapper `wgpu-rs`

have reached version 0.3.
Major improvements:

- API is (mostly) updated to the upstream WebGPU working group spec
- internal deadlock protection
`raw-window-handle`

support- individual tracking of texture array layers and mipmap levels
- more API features:
- multisampling
- indirect draw and dispatch
- stencil masks and reference values

- more examples!
- more state validation!

*Discussions:
discourse,
/r/rust*

[luminance](https://github.com/phaazon/luminance-rs) is a type-safe, type-level and stateless Rust graphics framework.

luminance v0.31 was released by [@phaazon](https://github.com/phaazon).
This version brings [LOTS of major changes and bugfixes](https://github.com/phaazon/luminance-rs/blob/master/luminance/CHANGELOG.md#031),
including two new crates:

[luminance-derive](https://crates.io/crates/luminance-derive)- provides several procedural derive macros you can use to easily implement all required traits to work with luminance. Especially, some traits that are unsafe can be implemented in a safe way with that crate.[luminance-glutin](https://crates.io/crates/luminance-glutin)- the windowing crate support for[glutin](https://github.com/rust-windowing/glutin).

Also, two ways to learn luminance were added:


The

[examples]. They are like unit tests: each introduces and focuses on a very specific aspect or feature. You should read them if you are interested in given feature. They’re not well suited to learn from scratch and they are weaker than a structured tutorial but more concise.The

[wiki]. It contains various chapters, including tutorials and onboarding newcomers. It will not provide you with the best description of a given feature as it focuses more on the overall comprehension and explaining than code directly.

### Other News [#](https://gamedev.rs#other-news)

-
[Vlad Zhukov](https://twitter.com/VladZhukov0)shared[theirs first Youtube devlog](https://youtu.be/7NojrtICE1k)about the development of an asteroids-like game[with Voronoi diagrams for procedural destructions](https://twitter.com/VladZhukov0/status/1162462543530643457).![Gameplay of Vlad’s prototype](../../assets/ab49c92a1f33d261.gif)

-
[Azriel](https://azriel.im/)published a devlog[“Charging Up”](https://azriel.im/will/2019/08/16/charging-up)- characters in[Will](https://azriel91.itch.io/will)can now charge up by holding the Attack button.![charging sprites from Will](../../assets/f5fc0d22112b2bab.png)

-
[droprate](https://crates.io/crates/droprate)- a crate for choosing outcomes based on a weighted probability map, aka more player-friendly random numbers [[/r/rust](https://reddit.com/r/rust/comments/co3buo/ann_droprate_a_crate_for_randomly_choosing_things)]. -
[“Compare Against Your Friends”](https://blog.roboinstruct.us/2019/08/02/better-than-your-friends.html)- after the[1.0 release](https://reddit.com/r/rust/comments/cdw1ct/robo_instructus_is_out_now_programming_puzzle)of[Robo Instructus](https://store.steampowered.com/app/1032170/Robo_Instructus),[Alex Butler](https://twitter.com/bigabgames)released a few more versions that fix some bugs, improve performance, scoring and UI.![RoboInstructus logo from Steam](../../assets/0172edf98283e735.jpg)

-
[@Remco](https://twitter.com/wodannson)shared on Twitter[a video of hot reloading demonstration](https://twitter.com/wodannson/status/1157472538622078976)[[/r/rust](https://reddit.com/r/rust/comments/cldaew/hot_reloading_of_function_bodies_in_rust),[/r/rust_gamedev](https://reddit.com/r/rust_gamedev/comments/cldajt/hot_reloading_of_function_bodies_in_rust/)]. -
[rx](https://cloudhead.io/rx)- a minimalist and extensible pixel editor in Rust [[/r/rust](https://www.reddit.com/r/rust/comments/cv6o4q/announcing_rx_minimalist_and_extensible_pixel),[repo](https://github.com/cloudhead/rx)].

## Popular Workgroup Issues in GitHub [#](https://gamedev.rs#popular-workgroup-issues-in-github)

[#23 “[Needed Crate] A pure rust SPIRV generator”](https://github.com/rust-gamedev/wg/issues/23)[#25 “The state of math libraries”](https://github.com/rust-gamedev/wg/issues/25)[#26 “[Tracker] Better windowing/graphics inter-operation”](https://github.com/rust-gamedev/wg/issues/26)[#42 “[Discussion] A plan for crate stewardship”](https://github.com/rust-gamedev/wg/issues/42)[rust-gamedev.github.io](https://github.com/rust-gamedev/rust-gamedev.github.io):

## Meeting Minutes [#](https://gamedev.rs#meeting-minutes)

[See all meeting issues](https://github.com/rust-gamedev/wg/issues?q=label%3Ameeting)
including full text notes or [join the next meeting](https://github.com/rust-gamedev/wg#join-the-fun).

## Requests for Contribution [#](https://gamedev.rs#requests-for-contribution)

## Bonus [#](https://gamedev.rs#bonus)

Just an interesting Rust gamedev link from the past. :)

![A Snake’s Tale’s logo](../../assets/aa51d7a75f7d2913.png)


On 2017.07.06 one of the first commercial Rust games [“A Snake’s Tale”](https://m12y.com/a-snakes-tale)
by [Michael Fairley](https://twitter.com/michaelfairley) was released:
[Steam](https://store.steampowered.com/app/654810/A_Snakes_Tale) (Windows/Linux/macOS),
[itch.io](https://m12y.itch.io/a-snakes-tale),
[AppStore](https://itunes.apple.com/us/app/a-snakes-tale/id1211845149?mt=8&at=1001lnX5),
[Google Play](https://play.google.com/store/apps/details?id=com.m12y.asnakestale).

A Snake’s Tale is a puzzle game about snakes in cramped places. Clear a path to get to the hole, eat some eggs along the way, and make sure to press all the buttons.




![Part of A snake's Tail's trailer](../../assets/30e8d91795dd83a9.gif)

[the full release trailer](https://www.youtube.com/watch?v=23pQmEuueNw)

A few posts about the game and how it was developed:

That’s all news for today, thanks for reading!

Want something mentioned in the next newsletter?
[Send us a pull request](https://github.com/rust-gamedev/rust-gamedev.github.io).

Also, subscribe to [@rust_gamedev on Twitter](https://twitter.com/rust_gamedev)
or [/r/rust_gamedev subreddit](https://reddit.com/r/rust_gamedev) if you want to receive fresh news!