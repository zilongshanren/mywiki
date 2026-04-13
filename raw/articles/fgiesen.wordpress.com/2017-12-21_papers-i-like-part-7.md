---
title: Papers I like (part 7)
url: https://fgiesen.wordpress.com/2017/12/21/papers-i-like-part-7/
published: '2017-12-21'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Papers I like (part 7)

Continued from [part 6](https://fgiesen.wordpress.com/2017/11/20/papers-i-like-part-6/).

### 27. Qureshi, Jaleel et al. – [“Adaptive Insertion Policies for High Performance Caching”](http://web.ece.ucdavis.edu/~anhttran/files/download/caching/ISCA-2007-Qureshi-SetDuelingControl.pdf) (2007; computer architecture/caches)

I have written [about](https://fgiesen.wordpress.com/2016/08/07/why-do-cpus-have-multiple-cache-levels/) [caches](https://fgiesen.wordpress.com/2014/08/18/atomics-and-contention/) [before](https://fgiesen.wordpress.com/2014/07/07/cache-coherency/), so I’ll skip explaining what exactly a cache is, why you would want them and how they interact with the rest of the system and go straight to (some of) the details.

Caches in hardware are superficially similar to hash tables/maps/dictionaries on the software side: they’re associative data structures, meaning that instead of being accessed using something like an array index that (more or less) directly corresponds to a memory location, they’re indexed using a key, and then there’s an extra step where these keys are converted into locations of the corresponding memory cells. But unlike most software hash tables, caches in HW usually have a fixed size and hence “forget” old data as new data is being inserted.

There are a few ways this can work. On one extreme, you have what’s called “direct-mapped” caches. These compute a “hash function” of the key (the key often being a physical or virtual memory address, and the “hash function” most often being simply “take some of the address bits”, hence the quotation marks) and then

have a 1:1 mapping from the hash to a corresponding memory location in some dedicated local memory (mostly SRAM). The important point being that each key (address) has exactly one location it can go in the cache. Either the corresponding value is in that location, or it’s not in the cache at all. You need to store some extra metadata (the “tags”) so you know what keys are stored in what location, so you can verify whether the key in that location is the key you wanted, or just another key that happens to have the same hash code. Direct-mapped caches are very fast and have low power consumption, but they perform poorly when access patterns lead to lots of collisions (which often happens by accident).

At the other extreme, there’s “fully associative” caches. These allow any key to be stored in any location in the cache. Finding the corresponding location for a key means comparing that key against all the tags – that is, basically a linear search, except it’s usually done all in parallel. This is slower and a lot more power-hungry than direct-mapped caches; it also really doesn’t scale to large sizes. The primary advantage is that fully associative caches don’t have pathological cases caused by key hash collisions. When they’re used (mostly for things like TLBs), are rarely bigger than 40 entries or so.

In the middle between the two, there’s “set associative” caches (usually denoted N-way associative, with some number N). In a N-way associative cache, each key can be stored in one of N locations, which collectively make up the “set”. The set index can be determined directly from the key hash, and then there’s a (parallel) linear search over the remaining N items using the tags to determine which item in the set, if any, matches the key. This is the way most caches you’re likely to encounter work. Note that a direct-mapped cache is effectively a 1-way associative cache, and a fully associative cache is a cache where the degree of associativity is the same as the number of entries.

Because caches have a fixed size, inserting a new entry means that (in general) an older entry needs be evicted first (or replaced, anyway). In a direct-mapped cache, we have no choice: there is a single location where each key can go, so whatever item was in that slot gets evicted. When we have a higher number of ways, though, there’s multiple possible locations where that key could go, and we get to decide what to evict to free up space.

This decision is the “insertion policy” (also “replacement policy” or “eviction policy” in the literature – these are not quite the same, but very closely related) in the paper title. The problem to be solved here is essentially the same problem solved by operating systems that are trying to decide which portions of a larger virtual memory pool to keep resident in physical memory, and therefore classic [page replacement algorithms](https://en.wikipedia.org/wiki/Page_replacement_algorithm) apply.

This is a classic CS problem with a known, provably optimal solution: Bélády’s OPT. The only problem with OPT is that it heavily relies on time travel, which is permissible for research purposes but illegal to use in production worldwide, as per the 1953 Lucerne Convention on Causality and Timeline Integrity. Therefore, mass-market hardware relies on other heuristics, most commonly LRU (Least-Recently Used), meaning that the item that gets evicted is whatever was used least recently. (In practice, essentially nobody does true LRU for N>2 either, but rather one of various LRU approximations that are cheaper to implement in HW.)

LRU works quite well in practice, but has one big weakness: it’s not “scan resistant”, meaning it performs poorly on workloads that iterate over a working set larger than the size of the cache – the problem being that doing so will tend to wipe out most of the prior contents of the cache, some of which is still useful, with data that is quite unlikely to be referenced again before it gets evicted (“thrashing”).

One option to avoid this problem is to not use LRU (or an approximation) at all. For example, several of the ARM Cortex CPU cores use (pseudo-)random replacement policies in their caches, which is not as good as well-working LRU, but at the same time better than a thrashing LRU.

This paper instead proposes a sequence of modifications to standard LRU that require very little in the way of extra hardware but substantially improve the performance for LRU-thrashing workloads.

The first step is what they call LIP (“LRU Insertion Policy”): when thrashing is occurring, it’s not useful to keep cache lines around unless we think they’re going to be reused. The idea is simple: replace the least-recently-used cache line as before, but then don’t mark the newly-inserted cache line as recently used, meaning that cache line *stays* flagged as least-recently used. If there is a second access to this cache line before the next insertion, it will get flagged as recently used; but if there isn’t, that cache line will get replaced immediately. In a N-way associative cache, this means that at most 1/N’th of the cache will get wiped on a scan-like workload that iterates over a bunch of data that is not referenced again in the near future. (It is worth noting here that updating the recently-used state as described makes sense for L2 and deeper cache levels, where the primary type of transactions involves full-size cache lines, but is less useful in L1 caches, since most processors don’t have load instructions that are as wide as a full cache line, so even a pure sequential scan will often show up as multiple accesses to the same cache line at the L1 level.)

LIP is scan-resistant, but also very aggressive at discarding data that isn’t quickly re-referenced, and hence doesn’t deal well with scenarios where the working set changes (which happens frequently). The next step is what the paper calls BIP (“bimodal insertion policy”): this is like LIP, except that the just-inserted cache line is flagged as recently used *some* of the time, with low probability. The paper just uses a small counter (5 bits) and performs a recency update on insertion whenever the counter is zero.

BIP is a good policy for workloads that would thrash with pure LRU, but not as good as LRU on workloads that have high locality of reference (which many do). What we’d really like to do is have the best of both worlds: use LRU when it’s working well, and only switch to BIP when we’re running into thrashing, which is what the authors call DIP (“Dynamic Insertion Policy”), the “adaptive insertion policy” from the paper title. The way they end up recommending (DIP via “Set Dueling”) is really simple and cool: a small fraction of the sets in the cache always performs updates via pure LRU, and another small fraction (of the same size) always performs updates via pure BIP. These two fractions make up the “dedicated sets”. The cache then keeps track of how many misses occur in the pure-LRU and pure-BIP sets, using a single saturating 10-bit counter, “PSEL”: when there’s a miss in one of the pure-LRU sets, PSEL is incremented. When one of the pure-BIP sets misses, PSEL is decremented.

In effect, the algorithm is continuously running experiments in a small fraction of the cache. When PSEL is small (below 512), LRU is “winning”: there are fewer misses in the LRU sets than in the BIP sets. When PSEL is larger, BIP is in the lead, producing fewer misses than LRU. The rest of the sets (which makes up the majority of them) are “follower sets”, and use whatever insertion policy is currently winning. If PSEL is below 512, the follower sets use LRU, else they use BIP.

And… that’s it. The implementation of this in hardware is a really simple modification to an existing cache module; it requires the two counters (15 bits of storage total), a tiny bit of glue logic, and the only extra decision that needs to happen is whether the LRU status should be updated on newly-inserted cache lines (entries) or not. In particular, the timing-critical regular cache access path (read with no new insertion) stays exactly the same. Most of the relevant bits of the design fits into a tiny block diagram in figure 16 of the paper.

What’s amazing is that despite this relative simplicity, DIP results in a significant improvement on many SPEC CPU2000 benchmarks, bridging two thirds of the gap between regular LRU and the unimplementable OPT, and performing significantly better than all other evaluated competing schemes (including significantly more complex algorithms such as using [ARC](https://en.wikipedia.org/wiki/Adaptive_replacement_cache)), despite only having a fraction of the hardware overhead.

Even if you’re not designing hardware (and most of use are not), the ideas in here are pretty useful in designing software-managed caches of various types.

### 28. Thompson – [“Reflections on Trusting Trust”](https://www.cs.colorado.edu/~jrblack/class/csci6268/s14/p761-thompson.pdf) (1983 Turing Award lecture; security)

Ken Thompson and Dennis Ritchie got the 1983 ACM Turing Award for their work on Unix. Ken Thompson delivered this acceptance speech, which turned into a classic paper on its own right.

In it, he describes what is now known as the “Thompson hack”. The idea is simple: suppose you put a really blatant backdoor in some important system program like the “login” command. This is easy to do given the source, but also really blatant – why would anyone run your modified login program of their own volition?

So for the next stage, suppose you don’t actually put the backdoor in the login program itself. Instead, you hijack some program that is used to produce such system programs, like the C compiler. Say, instead of inserting your backdoor directly in “login”, you insert some evil code in the system C compiler that checks whether you’re compiling the login program, and if so, inserts your backdoor code itself. Now, a security review of the login source code will not turn up anything suspicious, but the compiler will still insert the backdoor on every compilation. However, you now put some (even more highly suspicious) code into the C compiler!

For the third and final stage, we can make this disappear as well: the important thing to note is that all major C compilers are, themselves, written in C (“bootstrapping”). Therefore, we can now add some more logic to the backdoor we added to the C compiler in the previous step: we also add some code to the C compiler that adds in our backdoors (including modification of the login program, as well as the changes we’re making to the C compiler itself) whenever the C compiler itself is compiled.

Having done this successfully, we can remove all traces of the backdoor from the C compiler source code: we now have a binary of a modified. evil C compiler that backdoors “login”, and also detects when we’re trying to compile a clean C compiler, producing another evil C compiler with the same backdoors instead. This kind of trickery is impossible to detect via source code review; and if you’re thinking that you would spot it in the binary, well, you can imagine more involved versions of the same idea that also hijack your operating system, file system drivers etc. to make it impossible to see the surreptitious modifications to the original binary.

That is not just idle musing; 33 years after Ken Thompson’s acceptance speech, this problem is more current than ever. Persistent malware that burrows into trusted components of the machine (like firmware) and is undetectable by the rest of the firmware, the OS and everything that runs on the machine is a reality, and the recent security vulnerabilities in the [Intel Management Engine](https://en.wikipedia.org/wiki/Intel_Management_Engine#Security_vulnerabilities) present on most processors Intel has shipped in the past 10 years are a reality.

Over the past few years, there have been efforts towards reproducible builds of open-source OSes and trustable (trustworthy?) end-to-end verifiable hardware design, but this is a real problem as more and more of our lives and data moves to computers we have no reason to trust (and sometimes every reason not to). We’re not getting out of this any time soon.

### 29. Dijkstra, Lamport et. al-[“On-the-fly Garbage Collection: an Exercise in Cooperation”](http://lamport.azurewebsites.net/pubs/garbage.pdf) (1978; garbage collection)

This is the paper that introduced concurrent Garbage Collection via the tri-color marking invariant. It forms the basis for most non-concurrent incremental collectors as well. No matter where you stand on garbage collection, I think it’s useful (and interesting!) to know how collectors work, and this is one paper you’ll be hard-pressed to avoid when delving into the matter; despite the claim in the paper’s introduction that “it has hardly been our purpose to contribute specifically to the art of garbage collection, and consequently no practical significance is claimed for our solution”, this is definitely one of the most important and influential papers on GC ever written.

I won’t go into the details here; but as with anything Lamport has written or co-authored, his [notes](http://lamport.azurewebsites.net/pubs/pubs.html#garbage) on the paper are worth checking out.

### 30. Lamport – [“Multiple Byte Processing with Full-Word Instructions”](http://lamport.azurewebsites.net/pubs/multiple-byte.pdf) (1975; bit twiddling)

In my original list on Twitter, I summarized this by saying that “I thought I wouldn’t need to do this anymore when we got byte-wise SIMD instructions on CPUs, and then CUDA came along and it was suddenly profitable on GPUs.”

This style of technique (often called “SWAR” for SIMD-within-a-register) is not new (nor was it in 1975, as far as I can tell), but Lamport’s exposition is better than most, since most sources just give a few examples and expect you to pick up on the underlying ideas themselves. Fundamentally, it’s about synthesizing at least some basic integer SIMD operations from non-SIMD integer arithmetic.

I used to consider this kind of thing a cute hack back when I was first doing graphics with software rendering back in the mid-90s. As my earlier quote illustrates, I thought these tricks were mostly obsolete when most CPUs started getting some form of packed SIMD support.

However, I used this technique in my DXT1 compressor back in 2007 (primarily because I only need a few narrow bit fields and SIMD intrinsic support in most compilers was in a relatively sorry state back then), published the source code, and was soon told by [Ignacio Castaño](http://www.ludicon.com/castano/blog/) (then at NVidia) that this technique was good a for about a 15% increase (if I remember correctly) in throughput for the NVidia Texture Tools CUDA encoder.

Since then, I have used SWAR techniques in GPU kernels myself, and I’ve also used them to paper over missing instructions in some SIMD instruction sets for multi-platform code – some of this quite recently (within the past year).

Within the last few years, PC GPUs have started adding support for narrower-than-32-bit data types and packed arithmetic, and mobile GPUs have always had them. And no matter what kind of computing device you’re writing code for, sometimes you just need to execute a huge number of very simple operations on tons of data, and a 2x-4x (or even more) density increase over standard data types is worth the extra hassle.

Separately, I just keep bumping into ways to map certain kinds of parallel-scan type operations to integer adder carry logic. It’s never as good as dedicated hardware would be, but unlike specialized hardware, integer adders are available everywhere *right now* and are not going anywhere.

In short, I’ve changed my mind on this one. It’s probably always going to be a niche technique, but it’s worth checking out if you’re interested in low-level bit hacks, and the wins can be fairly substantial sometimes. You might never get to use it (and if you do, please *please* write proper comments with references!), but I’ve come back to it often enough by now to consider it a useful part of my tool chest.

### The end

And that’s it! It took me a while to get through the full list of my recommendations and write the extended summaries. That said, spacing the posts out like this is probably better to read than having a giant dump of 30+ papers recommended all at once.

Either way, with this list done, regular blogging will resume in the near future. At least that’s the plan.

Curious question: Is the “1953 Lucerne Convention on Causality and Timeline Integrity” something you just made up, or is it a reference to an actual science-fiction story?

I made it up. The closest equivalent in a SF story I can think of is the Eschaton from Charles Stross’s “Singularity Sky”, which puts it as: “Thou shalt not violate causality within my historic light cone. Or else.”

By 2005, hardware backdoors have been done for decades. Reflections on Trusting Trust is the academics realizing what people have already been able to do from the start. It isn’t surprising that backdoors become harder to detect once put into the hardware, OS, binaries, or other low level systems.

“Reflections on Trusting Trust” isn’t from 2005, it’s from 1984.