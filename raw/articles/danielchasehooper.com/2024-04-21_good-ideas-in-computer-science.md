---
title: Good Ideas in Computer Science
url: https://danielchasehooper.com/posts/good-ideas-in-cs/
published: '2024-04-21'
source_blog: Daniel Hooper
source_site: https://danielchasehooper.com/
category: graphics
fetched: '2026-04-19'
---

April 21, 2024・3 minute read

Programmers love arguing for their favorite technologies. C++ vs Rust. Mac vs PC. These arguments overshadow the victories of Computer Science — the ideas that we all agree on. To unearth these ideas, I recently [asked a simple question](https://twitter.com/DanielcHooper/status/1778795850107424827) on Twitter/X:

What ideas in computer science are universally considered good?


By “universally considered good” I mean they *aren’t* debated. Ideas so widespread and effective that you might not even think of them as being invented. Each idea may not be suitable in all situations, but you won’t find a programmer that thinks you should *never* use them. I intentionally focus on *ideas*, not *implementations*. For example: Unix contains many good ideas, but is not on the list because it is an implementation.

Here’s my list, including the year each idea appeared:

Intentionally excluded:

Garbage Collection

There are many examples of teams fighting the garbage collector to hit performance goals 4. The

Databases

Databases are more than just one idea, with many ways to combine those ideas into a “database shape”. Some good ideas in databases: [Structured query language](https://en.wikipedia.org/wiki/SQL), [B-trees](https://en.wikipedia.org/wiki/B-tree), [ACID transactions](https://en.wikipedia.org/wiki/ACID).

Other data structures and algorithms

There are too many to list. Few are as universal as arrays and hashmaps, which appear in almost all programs.

Object Oriented Programming

There is a large group of programmers that do not consider Object Oriented Programming good 5. I recommend

By 1974, 50 years ago, we had most of what we call modern computing. Today’s fundamentals are the same — a C programmer from 1974 would feel at home on a modern computer except for the alien-like speed. I hope we have new ideas that in 50 years will be universally considered good.

Discuss on [Twitter](https://twitter.com/DanielcHooper/status/1782446647047311466)

Discuss on [Lobste.rs](https://lobste.rs/s/kruxyr/good_ideas_computer_science)

[Here’s a look](https://devblogs.microsoft.com/oldnewthing/20240401-00/?p=109599) at programming before the call stack [↩︎](https://danielchasehooper.com#fnref:1)

It’s unclear to me what language was the first to compile to multiple architectures. [Reach out](https://twitter.com/DanielcHooper) if you know. [↩︎](https://danielchasehooper.com#fnref:2)

By “Virtual Address Space” I mean the ability for Program A and Program B to be written without knowledge of each other and run simultaneously without memory interference. This allows both to use the same virtual memory address, say 0x12345678, because it maps to different physical memory addresses. Some people confused this with [paging](https://en.wikipedia.org/wiki/Memory_paging) (which moves data from RAM to the hard drive when RAM usage is high), and [memory mapping](https://en.wikipedia.org/wiki/Memory-mapped_file) (which allows you to access the hard drive using memory instructions). [↩︎](https://danielchasehooper.com#fnref:3)

[OOP is bad](https://www.youtube.com/watch?v=QM1iUe6IofM), [Clean Code Horrible Performance](https://www.computerenhance.com/p/clean-code-horrible-performance), [What’s wrong with OOP](https://www.dataorienteddesign.com/dodbook/node12.html) [↩︎](https://danielchasehooper.com#fnref:5)