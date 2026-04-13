---
title: High Performance Code Is Designed, Not Optimized
url: http://hacksoflife.blogspot.com/2015/01/high-performance-code-is-designed-not.html
author: Benjamin Supnik
published: '2015-01-04'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Sigh...this is what I get for pretending to do work when I could have been writing blog posts and changing my blogger theme a few dozen times. I was


But Joshua Barczak






Over the next few posts I will try to make the case that the factors that really affect performance (both for the better and the worst) tend to get settled very early in the design process, and therefore the notion of having high performance code by pushing performance work to late in the process is lunacy.


* I do already love the sound of my own voice blathering on, and I'm also pretty excited to spout off on topics that I know nothing about. so I figure I am at least partly qualified for the job.

*totally*going to write a big rant about how it's not okay to use Knuth as an excuse to pull code straight out of your ass and then hope to fix performance at the last minute by repeatedly finding and beating on the hot spots with a profiler.But Joshua Barczak

[totally beat me to it](http://www.joshbarczak.com/blog/?p=580). So, um, go read what he read.
I have a bunch of ~~rants~~topics I want to discuss in detail, but to start, here's an attempt at a pithy quote (for my future career as a tech pundit):

High performance software is always high performance by design.I cannot emphasize this enough: high performance applications meet their performance goals by designing for performance from day one. For all the parts of X-Plane where I am proud of our performance, I can point to a subsystem that was designed to be fast, and where performance is part of its fundamental architecture.

The

[Knuth quote about premature optimization](http://web.archive.org/web/20130731202547/http://pplab.snu.ac.kr/courses/adv_pl05/papers/p261-knuth.pdf)isn't just often misquoted, it's incorrect. To have high performance software, it is not enough to focus tightly on actual hot spots in the code and tune them. The architecture of the code must be designed for high performance. A better version of the Knuth quote might be:Premature design without analyzing the performance characteristics of the problem is the root of all evil.Clearly I'm going to have to slim that quote down and stylize it if I'm ever going to make it as a pundit.*

Over the next few posts I will try to make the case that the factors that really affect performance (both for the better and the worst) tend to get settled very early in the design process, and therefore the notion of having high performance code by pushing performance work to late in the process is lunacy.

* I do already love the sound of my own voice blathering on, and I'm also pretty excited to spout off on topics that I know nothing about. so I figure I am at least partly qualified for the job.

High performance code is both. You need the quality design *and* the hand tuning of the hot spots. Doing only half the work usually fails.



ReplyDeleteBut you're perfectly correct that the second part is useless without the first.

Totally true, and I realized after writing this post that it does kind of come off like "design, then don't performance profile", which is crazy. If you haven't profiled performance you don't even know whether your code works. (It would be like writing code and never running it.)



DeleteI think the term "hand tune" is also ambiguous. It could mean:

- Rewrite specific bits of code based on performance profiling data (e.g. change your memory layout based on profiled L2 cache misses).

- Rewrite specific bits of code using more labor-intensive high performance techniques (e.g. rewrite a hot loop in assembly).

Both are valid - both the listening to the profiler and the using more labor where it's worth it.