---
title: 'Review: “Multithreading for Visual Effects”, CRC Press 2014'
url: https://bartwronski.com/2014/09/21/review-multithreading-for-visual-effects/
published: '2014-09-21'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

Today I wrote a short review about a book I bought and read recently – [“Multithreading for Visual Effects” published by CRC Press 2014](http://www.crcpress.com/product/isbn/9781482243567) and including articles by Martin Watt, Erwin Coumans, George ElKoura, Ronald Henderson, Manuel Kraemer, Jeff Lait, James Reinders. Couple friends asked me if I recommend it, so I will try to briefly describe its contents and who I can recommend it for.

![BxN4wfoIcAE00_t](../../assets/ba29942a0b9d481e.jpg)


## What this book is not

This book is a collection of various VFX related articles. It is not meant to be a complete / exhaustive tutorial for designing multi-threaded programs or algorithms or how VFX industry approaches multithreading in general. On the other hand, I don’t really feel it’s just a collection of technical papers / advancements like ShaderX or GPU Pro books are. It doesn’t include very detailed presentation of any algorithm or technique. Rather it is a collection of post-mortems of various studios, groups and people working on a specific piece of technology and how they had to face multi-threading, problems they encountered and how they solved them.

Lots of articles have no direct translation to games or real time graphics – you won’t get any ready-to-use recipe for any specific problem, so don’t expect it.

## What I liked about it

I really enjoyed practical aspects of the book – talking about actual problems. Most of the problem comes from the fact that existing code bases contain tons of not threaded / tasked, legacy code with tons of global states and “hacks”. It is trivial to say “just rewrite bad code”, but when talking about technology developed for many years, producing desired results and already deployed in huge studios (seems that VFX studios are often order of magnitude larger than game ones…) obviously it is rarely possible. One article provides very interesting reasoning in whole “refactor vs rewrite” discussion.

Authors are not afraid to talk about such not-perfect code and provide practical information how to fix it and avoid such mistakes in the future. There are at least couple articles that mention best code practices and ideas about code design (like working on contexts, stateless / functional approach, avoiding global states, thinking in tasks etc.).

I also liked that authors provided very clear description of “failures” and practicality of final solutions, what did and what didn’t work and why. Definitely this is something most scientific / academic papers are lacking, but here it was described clearly and will definitely help readers.

## Short chapters descriptions

### “Introduction and Overview”, James Reinders

Brief introduction in history of hardware, its multi-threading capabilities and why they are so important. Distinction between threading and tasking. Presentation of different parallel computations solutions easily available in C++ – OpenMP, Intel TBB, OpenCL and others. Very good book introduction.

### “Houdini, Multithreading existing software”, Jeff Lait

Great article about the problem of multithreading existing, often legacy code bases. Description of best practices when designing multi-threaded/tasked code and how to fix existing, not perfect one (and various kinds of problems / anti-patterns you may face). I can honestly recommend this article to **any** game or tools programmer.

### “The Presto Execution System: Designing for Multithreading”, George ElKoura

Introductory article about threaded systems designs when dealing with animations. Very beneficial for any engine or tools programmers as describes many options for parallelism strategies, their pros and cons. Final applied solution is not really applicable for games run-time, but IMO this article is a still very practical and good read for game programmers.

### “LibEE: Parallel Evaluation of Character Rigs”, Martin Watts

Second chapter exclusively about animations, but applicable to any node/graph-based systems and their evaluation. Probably my favorite article in the book because of all the performance numbers, compared approaches and practical details. I really enjoyed its in-depth analysis of several cases, how multi-tasking worked on specific rigs and how content creators can (and probably at some point will have to) optimize their content for optimal and parallel evaluation. The last part is something often not covered by any articles at all.

### “Fluids: Simulation on the CPU”, Ronald Henderson

Interesting article describing process of picking and evaluating most efficient parallel data structures and algorithms for specific case of fluids simulation. It is definitely not exhaustive description of fluids simulation problem, but rather example analysis of parallelizing a specific problem – very inspiring.

### “Bullet Physics: Simulation with OpenCL”, Erwin Coumans

Introduction to GPGPU with OpenCL with case study of [Bullet physics engine](http://bulletphysics.org/wordpress/). Introduction to rigid body simulation, collision detection (tons of references to great “[Real-time collision detection](http://realtimecollisiondetection.net/)“) nicely overlapping with description of OpenCL, GPGPU / compute simulations and differences between them and classic simulation solutions.

### “OpenSubdiv: Interoperating GPU Compute and Drawing”, Manuel Kraemer

IMO the most specialized article. As I’m not an expert on mesh topologies, tessellation and Catmull-Clark surfaces it was for me quite hard to follow. Still, depiction of the title problem is clear and proposed solutions can be understood even by someone who doesn’t fully understand the domain.

## Final words / recommendation

I feel that with next-gen and bigger game levels, vertex counts and texture resolutions we need not only better runtime algorithms, but also better content creation and modification pipelines. Tools need to be as responsive as they used to be couple years ago, but this time with order of magnitude bigger data sets to work on. This is the area where we almost converged with the problems VFX industry faces. From discussions with many developers, it seems to be the biggest concern of most game studios at the moment – tools are lagging in development compared to the runtime part and we are just beginning to utilize network caches and parallel, multithreaded solutions.

I always put emphasis on short iteration times (they allow to fit more iterations at the same time, more prototypes that directly translate to better final quality of anything – from core gameplay to textures and lighting), but with such big data sets to process, they would have to grow unless we optimize pipelines for modern workstations. Multi-threading and multi-tasking is definitely the way to go.

Too many existing articles and books either only mentioned parallelization problem, or silently ignored it. “Multithreading for Visual Effects” is very good as it finally describes practical side of designing code for multi-threaded execution.

I can honestly recommend “Multithreading for Visual Effects” to any engine, tools and animations programmers. Gameplay or graphics programmers will benefit from it as well and hopefully it will help them create better quality code that runs efficiently on modern multi-core machines.

You must be logged in to post a comment.