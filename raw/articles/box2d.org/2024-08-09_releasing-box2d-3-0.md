---
title: Releasing Box2D 3.0
url: https://box2d.org/posts/2024/08/releasing-box2d-3.0/
published: '2024-08-09'
source_blog: Box2D
source_site: https://box2d.org/
category: graphics
fetched: '2026-04-19'
---

Over 18 months ago I [announced](https://box2d.org/posts/2023/01/starting-box2d-3.0/) that I was working on Box2D version 3.0 (v3 for short). And it has finally arrived! It has been a long journey and I’ve learned a lot. There is more work to do, but the library is ready to be used for game development.

I’d like to thank the Box2D users who tested v3 during the alpha and beta. Their feedback and bug reports have been super helpful! I made many changes and decisions based on input from the Box2D community on [Discord](https://discord.gg/BQC34X4v) and [GitHub](https://github.com/erincatto/box2d).

Let’s review my initial goals!

## Speculative collision

Version 3.0 completely overhauls continuous collision and response. It uses a hybrid speculative and time of impact approach.

This approach has the following benefits:

- a polygon skin is no longer required so there are no gaps between polygons
- naturally supports rounded polygons
- minimal movement pauses (time loss)
- easy to solve in parallel
- supports
[bullets](https://box2d.org/documentation/md_simulation.html#bullets)

The v3 continuous collision design seems to prevent almost all dynamic versus static tunneling. With bullets there is tunneling prevention for dynamic versus kinematic and dynamic, but it is not as robust.

I believe this strikes a good balance between performance and robustness. Let me know what you think!

## API changes

The v3 API is completely new. The entire API consists of enums, structs, and functions. There are no C++ classes, operator overloads, or inheritance. I’ve made minimal use of macros. All internal data is hidden in the `src`

directory, making the public include headers smaller and easier to read.

The use of [ids](https://box2d.org/documentation/index.html#autotoc_md20) replaces most pointers and should help reduce the chances of double frees and orphaned objects.

There are optional math operator overloads provided for C++ users.

I’m satisfied with the overall design, but I’m happy to get feedback.

## Moving to C from C++

Writing a whole library in C has been quite interesting! It has been challenging in some ways and refreshing in others.

Pros:

- C fits with how I naturally like to program
- C lets me focus on algorithms and data structures
- C compiles very fast

Cons:

- MSVC is behind the current C standard, making some things harder than they should be (e.g. multithreading)
- I want a simple type-safe dynamic array with bounds checking. Pretty please?

## Why not language X?

I think the decision to stick with C was correct. Debugging is easy. The tooling is good. I am very productive.

I am interested in other languages, but I think C is the right choice for Box2D and arguably game physics engines in general.

## Performance

Working on v3 performance was a long road with many [side quests](https://github.com/erincatto/solver2d). The main focus was [multithreading](https://en.wikipedia.org/wiki/Multithreading_(computer_architecture)) and [SIMD](https://en.wikipedia.org/wiki/Single_instruction,_multiple_data).

For multithreading I explored many options. Along the way I decided Box2D should support multithreading large piles of bodies, especially after seeing Petri Purho discuss the technology behind [Noita](https://www.youtube.com/watch?v=prXuyMCgbTc). This lead me to explore [graph coloring](https://en.wikipedia.org/wiki/Graph_coloring). I was inspired by the threading design of [bepu](https://www.bepuentertainment.com/).

I spent a lot of time looking at profilers. I found [Tracy](https://github.com/wolfpld/tracy) to be exceptionally useful as well as friendly to C development.

![Tracy](../../assets/a8447f3e348fcc3f.png)

*Tracy*

I also leaned on [enkiTS](https://github.com/dougbinks/enkiTS) for managing threads and the task pool. This is another excellent library that is also friendly to C development.

A big part of multithreading performance was minimizing single-threaded bottlenecks. This lead to persistent [islands](https://box2d.org/posts/2023/10/simulation-islands/), data-oriented data layout, broad-phase threading, faster collision pair management, reworked continuous collision, and threaded island splitting.

I implemented AVX2 for the contact solver since that is usually the bottleneck. This relied on graph coloring and gives a very nice speed gain. In a constraint solver it is necessary to gather and scatter body state data and in 2D it conveniently works out that this body state fits in 32 bytes, making this work great with 256-bit AVX vectors.

I also developed a benchmarking console application I can use to efficiently measure performance. This application emits CSV files that can be compared with the main branch using this [page](https://box2d.org/files/benchmark_results.html). This also shows how well v3 scales with core count and different processors. The bottom line is that v3 scales quite well with cores as long as they share an L2/L3 cache.

My initial approach to performance was multithreading but then I realized that single-threaded performance is also still important. I’m happy to say that my tests indicate that v3 is more than twice as fast as v2.4. This is mainly due to the data oriented design of v3 and the use of SIMD.

## Capsules

Yes, v3 finally got capsules! As a bonus rounded polygons are also available.

## Other improvements

Beyond my initial goals, I added even more stuff to v3.

### Soft Step solver

Version 3.0 ships with a new solver I’m dubbing *Soft Step* (formerly called `TGS_Soft`

). This arose from my [Solver2D](http://box2d.org/posts/2024/02/solver2d/) experiment. This solver is more stable in almost every way than version 2.4. It handles higher mass ratios, longer chains of bodies, larger stacks, and so on. It is based on [soft constraints](http://box2d.org/files/ErinCatto_SoftConstraints_GDC2011.pdf) and sub-stepping. Hence the name. It falls slightly behind the NGS block solver of v2.4 for vertical stacks, but that solver was basically designed for vertical stacking and I don’t think it is worth the performance trade-off just for vertical box stacks.

### Improved precision

I spent a fair bit of time adjusting the algorithms in Box2D to have improved precision. In my tests this means simulation runs well on worlds up to around 20 kilometers in size. Beyond that I think you would need to recenter the world or use doubles.

### Joints

Joints are a mixed bag. I removed the pulley and gear joints because I want to rework them later. On the other hand the remaining joints got new stuff. I added springs to many joints. I also added a motor to the distance joint.

### Extensive testing

I’ve made the samples application more extensive and faster. I added more unit tests. I’ve run sanitizers. Version 3.0 uses more complex algorithms than version 2.4 and it needs more testing.

## Release video

I made a video to celebrate the release of v3. I hope you enjoy it.

## Supporting Box2D

Box2D has been very fun to work on. However, I have put *a lot* of work into it. If your company uses Box2D, it should consider sponsoring Box2D. Of course sponsorship is optional in all cases.

If you’d like to sponsor Box2D development, you can sign up using [GitHub sponsors](https://github.com/sponsors/erincatto) or [Patreon](https://www.patreon.com/Box2D).

1062 words

2024-08-08 17:00 -0700