---
title: This One Weird Trick Let's You Beat the Experts
url: http://hacksoflife.blogspot.com/2015/06/beating-experts.html
author: Benjamin Supnik
published: '2021-10-29'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

As I've mentioned in the past, one of my goals with this blog is to launch my post-development career in tech punditry and eventually author an O'Reilly book with an animal on the cover.* So today I'm going to add click-baity titles to my previous pithy quotes and tell you about

**that one weird trick that will let you beat the experts and write faster code**than the very best libraries and system implementations.But first, a Vox-style explanatory sub-heading.

### StackOverflow is a Website That Destroys New Programmers' Hopes and Dreams

Here is a typical question you might see on Stack Overflow**:

I'm new to programming, but I have written a ten line program. How can I wrote my own custom allocator for my new game engine? I need it to be really fast and also thread safe.

StackOverflow is a community full of helpful veteran programmers who are there for the newbies among us, so someone writes an answer like this.***

Stop. Just stop. Unplug your keyboard and throw it into the nearest dumpster - it will help your game engine to do so. The very fact that you asked this question shows you should not be trying to do what you do.

You cannot beat the performance of the system allocator. It was written by a Linux programmer with an extraordinarily long beard. That programmer spent over 130 years studying allocation patterns. To write the allocator, he took a ten year vow of silence and wrote the allocator in a Tibetan monastery using the sand on the floor as his IDE. The resulting allocator is hand-optimized for x86, ARM, PDP-11 macro-assembler, and the Zilog Z-80. It uses non-deterministic finite state automata, phase-induced reality distortion fields, atomic linked lists made from enriched Thorium, and Heisenberg's uncertainty principle. It is capable of performing almost 35 allocations per second. You are not going to do better.

Discouraged, but significantly wiser, our young programmer realizes that his true calling in life is to simply glue together code other people have written, and vows to only develop electron apps from this point forward.

But what if I told you there was this one weird trick that would allow our newbie programmer to beat the system allocator's performance?

### The Secret of My Success

Come closer and I will whisper to you the one word that has changed my life. This one thing will change how you code forever. Here's what our young programmer needs to do to beat the system allocator:


**Cheat.**


Here, I'll show you how it's done.

static char s_buffer[1024]; void * cheat_malloc(size_t bytes) { return s_buffer; } void cheat_free(void * block) { }

(Listing 1 - the world's worst allocator.)

One thing you cannot deny: this code is

*a lot faster than malloc.*Now you might be saying: "Ben, that is literally the worst allocator I have ever seen" (to which I say "Hold my beer") but you have to admit: it's not that bad if you don't

*need*all of the other stuff malloc does (like getting blocks larger than 1K or being able to call it more than once or actually freeing memory). And really fast. Did I mention it was fast?And here we get to the pithy quotes in this otherwise very, very silly post:

You might not need the full generality and feature set of a standard solution.

and

You can write a faster implementation than the experts if you don't solve the fully general problem.

In other words, the experts are playing a hard game - you win by cheating and playing tic tac toe while they're playing chess.

### All That Stuff You Don't Need

A standard heap allocator like malloc does

*so much stuff*. Just*look*at this requirements list.- You can allocate any size block you want. Big blocks! Small blocks! Larger than a VM page. Smaller than a cache line. Odd sized blocks, why not.
- You can allocate and deallocate your blocks in any order you want. Tie your allocation pattern to a random number generator, it's fine, malloc's got your back.
- You can free and allocate blocks from multiple threads concurrently, and you can release blocks on different threads than you allocated them from. Totally general concurrency, there are no bad uses of this API.

The reason I'm picking on these requirements is because they make the implementation of malloc complicated and slow.****

One of the most common ways to beat malloc that every game programmer knows is a bump allocator. (I've heard this called a Swedish allocator, and it probably has other names too.) The gag is pretty simple:

- You get a big block of memory and keep it around forever. You start with pointer to the beginning.
- When someone wants memory, you move the pointer forward by the amount of memory they want and return the old pointer.
- There is no free operation.
- At the end of a frame, you reset the pointer to the beginning and recycle the entire block.
- If you want this on multiple threads, you make one of these
*per thread.*

This is fast! Allocation is one add function, freeing is zero operations, and there are no locks. In fact, cache coherency isn't that bad either - successive allocations will be extremely close together in memory.

Our bump allocator is only slightly more complex than the world's worst allocator, but it shares a lot in common: it's faster because it doesn't provide all of those general purpose features that the heap allocator implements. If the bump allocator is too special purpose, you're out of luck, but if it fits your design needs, it's a win.

And it's simple enough you can write it yourself.

### General Implementations are General

You see the same thing with networking. The conventional wisdom is: "use TCP, don't reinvent TCP", but when you look into specific domains where performance matters (e.g. games, media streaming) you find protocols that do roll their own, specifically because TCP comes with a bunch of overhead to provide its abstraction ("the wire never drops data") that are expensive and not needed for the problem space.

So let me close with

*when*to cheat and roll your own. It makes sense to write your own implementation of something when:- You need better performance than a standard implementation will get you and
- Your abstraction requirements are simpler or more peculiar than the fully general case and
- You can use those different/limited requirements to write a faster implementation.

You might need a faster implementation of the fully general case - that's a different blog post, one for which you'll need a very long beard.

* The animal will be some kind of monkey flinging poop, obviously.

** Not an actual StackOverflow question.

*** Not an actual StackOverflow answer. You can tell it's not realistic because the first answer to any SO question is always a suggestion to use a different language.

**** I mean, not that slow - today's allocators are pretty good - and certainly better than I can write given those requirements. But compared to the kinds of allocators that

*don't solve those problems*, malloc is slower.
## No comments:

## Post a Comment