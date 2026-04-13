---
title: Papers I like (part 5)
url: https://fgiesen.wordpress.com/2017/09/02/papers-i-like-part-5/
published: '2017-09-02'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Papers I like (part 5)

Continued from [part 4](https://fgiesen.wordpress.com/2017/08/28/papers-i-like-part-4/).

### 19. Curtsinger, Berger – [“Stabilizer: Statistically sound performance evaluation”](http://people.cs.umass.edu/~emery/pubs/stabilizer-asplos13.pdf) (2013; performance evaluation)

Current CPUs are chock-full of associative data structures that are indexed by memory addresses, either virtual or physical. In no particular order, we have: multiple cache levels (for instructions, data, or both), multiple [TLB](https://en.wikipedia.org/wiki/Translation_lookaside_buffer) levels, page entry caches, branch target buffers (multiple levels), branch direction history, snoop filters, cache directories and more. (Not all of these exist everywhere or are necessarily distinct.)

All of these implement a kind of “forgetful” dictionary/map structure, and they are usually implemented as set-associative caches. Without going into too much detail, that means that addresses are “hashed” (some caches use relatively decent hash functions, but most that are on time-critical paths just use a few bits from the middle of the address as their “hash”). For a given hash value, there are then typically somewhere between 2 and 16 locations in the cache that values with that hash can be stored in (that’s the “set” in “set-associative”). Generally, to free up a slot, something else has to be thrown out (“evicted”) first; there’s a lot of design freedom in how caches pick what gets evicted. Most commonly, it’s either one of several [LRU](https://en.wikipedia.org/wiki/Cache_replacement_policies#Least_Recently_Used_.28LRU.29) approximations (“real” LRU for more than 3-4 elements is relatively expensive in hardware) or just a (pseudo-)random eviction policy.

Even when there is no randomness in the cache policy, the addresses themselves are also somewhat random. Virtual addresses within a process used to be mostly the same between two runs of the same program (this is possible because each process gets its own address space), but this made it easy to write reproducible security exploits, so we got ASLR (address space layout randomization), which deliberately shuffles the memory map to make writing reliable exploits harder. Even without ASLR, memory maps for separate runs of the same process weren’t always exactly the same; for example, changing the size of the environment variables or command line can also have a big knock-on effect on the memory map as various areas get moved to make space.

Modifying code in any way whatsoever can have significant effects on memory layout too. If a single function changes size, the linker is going to end up moving everything after it (for a randomly picked function, on average that’s going to be half the program) to a different location.

For anything that is indexed with *physical* memory addresses (typically L2 and below cache levels, and everything associated with them), things are even less predictable. Two back-to-back runs of the same process may have the same virtual address map if they have the same environment, command line and ASLR is disabled, but they’re unlikely to get assigned the exact same physical memory as the previous run, because physical memory is a globally shared resource between all the processes running on a system, and the OS is servicing physical memory allocations and deallocations all the time.

The end result is that even if you manage to carefully control for other spanners in the works such as background tasks and services (which have a tendency to start intensive tasks like indexing when you least expect it), network traffic (lots of incoming or outgoing packets that are not for your program can have a serious effect), available memory, and GPU/CPU voltage/frequency scaling, it’s possible to end up with dramatic execution time differences between either two runs of the same program, or two runs of two versions of a program that haven’t touched any code in the inner loops.

How bad does this get for real-world code? Now don’t get me wrong, many programs aren’t significantly affected by such issues at all. But some are; and microscopic layout differences can have decidedly macroscopic consequences. The SPECint 2000 “perl” benchmark (which is just the Perl interpreter running some – completely deterministic! – code) is infamous for having +-5% swings (this happens for multiple architectures) whenever *anything* in the executable changes. [“Causes of Performance Instability due to Code Placement in X86”](http://llvm.org/devmtg/2016-11/Slides/Ansari-Code-Alignment.pdf) (presentation given at the LLVM US Dev Meeting 2016) has some particularly drastic examples.

This kind of thing is particularly insidious when you’re spending time tinkering with some hot loop. Ever made a change that really should have made things faster but instead was a noticeable slow-down? Often these things are explained if you look at the generated machine code (if you are the kind of person who does that, that is), but sometimes they really are completely mysterious and apparently random – or at least “twitchy”, meaning there are big swings whenever you make *any* change, with no discernible rhyme or reason. It’s really frustrating to chase this type of problem down if you’re ever stuck with it (it involves a lot of staring at CPU performance counters between different versions of a program), but probably worse is when you don’t notice it’s happening at all, and think that what ends up being a “random” (or at least accidental/unintended) fluctuation is due to an intentional change working as expected.

That’s where this paper comes in. Stabilizer uses various tricks to (to the extent possible) re-randomize memory layout in LLVM-compiled code periodically while the app is running. It can’t move existing allocations, but it can add random padding on thread stacks, make new heap allocations return addresses in a different range, and shuffle machine code around. While any *individual* memory layout has its own biases, sampling over *many* independent memory layouts during a test run allows systematically controlling for memory layout effects. Ideally (if the memory layout gets sufficiently randomized and there are no other confounding factors), it results in the different runs being independent and identically distributed, meaning the Central Limit Theorem applies and the resulting sum distribution is Gaussian. That’s very good news because Gaussians are easy to do statistical hypothesis testing with, which the paper then proceeds to do.

I wish this kind of thing was standard on every platform I’m developing for, but sadly the paper’s implementation never seems to have made it past a research prototype (as far as I can tell).

### 20. Tomasulo – [“An efficient algorithm for exploiting multiple arithmetic units”](http://people.eecs.berkeley.edu/~kubitron/courses/cs252-S07/handouts/papers/tomasulo.pdf) (1967; computer architecture)

Many important computer architecture ideas are *way* older than you might expect. The primary reason is that there was intensive research and fierce competition in the mainframe/supercomputer market in the 1960s and 70s. Decades later, after advances in semiconductor manufacturing made microprocessors (entire processors *on a single chip*!) first possible and then kept the available transistor budget at consumer-relevant prices increasing exponentially, more and more ideas that used to be limited to top-of-the-line, room-sized computing devices became relevant for mass-market electronics.

Tomasulo’s paper talks about the floating-point unit in the very top of the line of the famous System/360 series, the Model 91. Sources disagree on how many of these were ever built; the count is somewhere between 10 and 20. Worldwide. Just the CPU set you back about $5.5 million, in 1966 dollars (which would be $41.5 million at the time I’m writing this, September 2017). But it wouldn’t do you much good by itself; you’d also want to shop for a console, a couple punch-card readers, a tape drive or two, maybe even a disk drive, some line printers… you get the idea. My point being, the computer market was *different* in the 1960s.

System/360 is extremely influential. It pioneered the idea of an *Instruction Set Architecture* (ISA). In the 60s, every CPU model had its own instruction set, operating system, and compilers. It was considered normal that you’d have to rewrite all your software when you got a newer machine. System/360 had a different idea: it specified a single ISA that had multiple implementations. At the low end, there was the Model 30. It executed 34500 instructions per second and had, depending on configuration, somewhere between 8KB and 64KB of core memory (and I do mean [core memory](https://en.wikipedia.org/wiki/Magnetic-core_memory)). At the very top, there was the Model 91, running 16.7 million instructions per second and with several megabytes of RAM. Of course, there were several models in between. And all of them would run the exact same programs. Note I wrote *is* earlier; the direct descendants of System/360 are still around, albeit re-branded as [“z/Architecture”](https://en.wikipedia.org/wiki/Z/Architecture) (slashes still going strong after 50 years!) when it was extended to 64 bits. IBM announced a new iteration, the z14, with custom CPU just a few weeks ago, and yes, they are still backwards compatible and will run 1960s System/360 code if you want them to.

Snicker all you want about mainframes, but if you manage to design a computer architecture in the 1960s that is still a multi-billion-dollar-a-year business (and still gets new implementations 50 years on), you certainly did *something* right.

Anyway: in retrospect, we can clearly say that this whole ISA idea was a good one. But it comes with a new problem: if the whole pitch for your product line is that you can always upgrade to a bigger machine if you need higher performance, then these bigger machines better deliver increased performance on whatever code you’re running, without a programmer having to modify the programs.

Which brings us to the Model 91 floating-point unit and Tomasulo’s algorithm. The model 91 FPU had separate, pipelined floating-point adders and multipliers. This is now completely standard, but was novel and noteworthy then (there’s a [separate paper](http://sites.google.com/site/arqui2unsl/ibm_360_unidad_fp.pdf) on the FPU design that’s fascinating if you’re interested in that sort of thing; among other things, that FPU was the source of [Goldschmidt’s division algorithm](https://en.wikipedia.org/wiki/Division_algorithm#Goldschmidt_division)).

The Model 91’s instruction unit could deliver one instruction per clock cycle. FP additions took 2 cycles (pipelined), single-precision multiplies 3 cycles (pipelined), and single-precision divisions 12 cycles (blocking, since they are executed as a sequence of multiplies).

Now if you were writing code for that specific machine by hand, unrolling loops where necessary etc., it would not be very hard to write code that actually achieves a rate of 1 new instruction per clock cycle – or at least, it wouldn’t be if the original System/360 architecture had more than 4 floating-point registers. But combine the 4 floating-point registers available, the relatively slow storage access (judging by the paper, loads had a latency of about 10 clock cycles), and the desire to be “plug-in compatible” and not require hand-tuned code for good performance if possible, a different solution was required.

Thus, Tomasulo’s algorithm, the first “shipping” instance of out-of-order execution, albeit only for the FPU portion of the Model 91, and only issuing one instruction per cycle. (The first attempt at *superscalar* out-of-order execution I’m aware of was designed by Lynn Conway for the IBM ACS-1 around the same time, but the project got [canned](http://ai.eecs.umich.edu/people/conway/Memoirs/ACS/Lynn_Conway_ACS_Reminiscences.pdf) for political reasons).

What I particularly like about Tomasulo’s paper is that it illustrates the process of incrementally modifying the initial in-order floating point unit design to its out-of-order equivalent. Textbook treatments of out-of-order execution generally deal with more complicated full out-of-order machines; focusing it on a single FPU makes it easy to see what is going on, and how the changes are relatively incremental.

The underlying ideas for out-of-order execution are closely related to the local value numbering I talked about last time in the context of SSA construction – namely, eliminating unnecessary dependencies that are just the result of name collisions rather than true dataflow between operations. CPUs don’t have the same difficulty as compilers in that they don’t need to build a representation valid for *all possible* control flow sequences through a given function; instead, they can either wait until control flow is decided (as in the Model 91 variant) or use speculation to, effectively, bet on a single likely control flow outcome when encountering a branch. (If that bet turns out to be wrong, all instructions thus started have to be cancelled.)

While out-of-order execution as a concept has been around for a long time, as far as I can tell, the first mass-produced *fully* out-of-order machines – in the sense of fully committing to out-of-order and speculative execution for the majority of the processor core, not just at the “periphery” (say for the FPU) – came out all within a few years of each other in the mid-90s. There’s IBM’s PowerPC 604 (December 1994), Intel’s Pentium Pro (November 1995), the MIPS R10000 (January 1996), and the DEC Alpha 21264 (October 1996).

Of these, the first two use a variant of Tomasulo’s algorithm using reservation stations, and the last two used a different approach based on explicit register renaming. Some processors even mixed the two styles: several of the early AMD Athlons used Tomasulo in the integer pipe and explicit register renaming for floating-point/SIMD.

Newer processors seem to tend towards explicit renaming; it usually has less data movement than Tomasulo’s algorithm, because for the most part, the signals passed through the pipeline are indices into a physical register file instead of actual values. The difference is especially pronounced with wide SIMD registers. But Tomasulo’s algorithm was very popular for quite a long time.

### 21. Wilson, Johnstone, Neely, Boles – [“Dynamic storage allocation: A survey and critical review”](http://www-2.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15213-f98/doc/dsa.pdf) (1995; memory allocation)

This one is a survey of memory allocation algorithms as of 1995; that is to say, it collects almost everything you need to know about how to implement memory (de)allocation for single-threaded programs, but doesn’t cover multi-threaded environments, which only really became a serious concern later. That’s not as big a gap as it may sound, because the main adaptations necessary to get a useful multi-threaded allocator are, at least conceptually, relatively clean. (one-sentence summary of proven-out approaches: thread-local caches, deferring of cross-thread frees, and multiple arenas).

But back to 1995: why is this paper on my list? Well, if you started programming in the early 90s on home computers or PCs (like me), then your early experiences with dynamic memory allocation pretty much sucked. (As far as I can tell, many late-80s era Unices were not all that much better.)

The key problems were this:

- These allocators tended to be buggy, slow, or both at the same time. For example, it was fairly common for
`realloc`

implementation to be buggy and corrupt the heap in certain circumstances. - They tended to have high levels of memory fragmentation, meaning that programs that did many allocations and deallocations would tend to end up reserving a lot more memory space than they were actively using, because there were lots of awkwardly-sized holes in the middle of the address space that were not large enough to satisfy normal allocation requests.
- All of this would be exacerbated by running in environment without virtual memory (this one did not apply to the aforementioned Unices, obviously). With virtual memory and swap space, growing memory use over time is more an inconvenience than a show-stopper. The program’s performance (and system performance in general) slowly degrades. Without virtual memory, the moment you want to allocate even one byte more than there is memory in the machine, you get an “out of memory” condition and, more likely than not, your program crashes.

The reason I’m citing this paper is because it turns out that the first two issues are related. In particular, it turns out that there were many issues with the way memory allocators were usually designed and evaluated. Most significantly, the “standard procedure” to evaluate allocators in the literature for a long time was to generate statistics for the sizes of memory allocations from real programs (or sometimes by building Markov models for the allocation/deallocation patterns), and then evaluate allocators using synthetic traces generated to match those statistics, rather than using actual allocation traces recorded from full runs of some test programs.

It turns out that this is a serious mistake. One of the most important characteristics of “real” allocation traces is that allocation and deallocation patterns tend to be bursty, and the statistics used didn’t capture any of those patterns.

This survey looks critically at this evaluation methodology, points out its flaws, and also points out the necessity of systematically analyzing the effect of individual allocation *policies*, rather than just testing complete allocators against each other.

In the follow-up paper [“The memory fragmentation problem: solved?”](http://www.cs.tufts.edu/~nr/cs257/archive/paul-wilson/fragmentation.pdf) the same authors analyze various allocator implementations and show that roving-pointer “next-fit”, one of the more popular algorithms at the time (and recommended by Knuth’s “The Art of Computer Programming”), has particularly bad fragmentation behavior, and shows that address-ordered first fit and best fit perform quite well, having very low overall fragmentation. In short, the high fragmentation produced by many late-80s and early-90s allocators was primarily because they used an algorithm that exacerbates the problem, which went unnoticed for a long time because the accepted analysis methodology was deeply flawed.

The authors of both papers collaborated with Doug Lea, who improved his allocator dlmalloc in response; dlmalloc implements a combination of segregated-storage (for smaller sizes) and best-fit (based on a radix tree, for larger requests). The resulting allocator is quite famous and was the basis for many later follow-up allocators.

### 22. Meyer, Tischer – [“GLICBAWLS – Grey Level Image Compression By Adaptive Weighed Least Squares”](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.131.4042&rep=rep1&type=pdf) (2001; image compression)

This paper is not like the other papers on this list.

For one thing, the name is a pretty obvious backronym. For another, the paper comes with a reference implementation – because the algorithm was originally developed as an entry for the [International Obfuscated C Code Contest](http://ioccc.org/) and fits in [1839 bytes of C / ASCII art](http://ioccc.org/2000/bmeyer.c).

Nevertheless, the algorithm is quite elegant and was, at the time it was released, easily among the best lossless grayscale image compressors. I wouldn’t use it today because it’s just way too serial internally, but I still have a soft spot for it.

### 23. Hutton et al. – [“Improving FPGA Performance and Area Using an Adaptive Logic Module”](http://www2.engr.arizona.edu/~ece506/readings/project-reading/6-cad/altera-alm.pdf) (2004; FPGAs)

This one, I don’t have that much to write about.

Here’s the short version: the combinational logic elements in [FPGAs](https://en.wikipedia.org/wiki/Field-programmable_gate_array) are internally realized as small lookup tables (LUTs). Arbitrary Boolean functions are thus described by their truth tables, which is stored in small SRAMs: 16 bits of SRAM for a 4-input binary logic function.

On the first page, the paper has a picture of a simple logic cell: a 4-bit LUT plus a D flip-flop. This used to be the standard building block of FPGAs, because it yields a good trade-off between area and delay for synthesized designs.

What this paper does is derive the design of a different logic module cell that can express either multiple 4-input LUTs, arbitrary 6-input LUTs, certain pairs of two 6-input logic functions with two outputs, and certain 7-input logic functions.

This is purely geeking out but it’s pretty cool if you’re interested in that sort of thing!

The Stabilizer paper is my favorite of the bunch, if only because I have been struggling with exactly the same issues at work. I’m sort of surprised it’s not more prevalent, but I think maybe it’s because very few people actually run performance regression tests.

One thing we did that helped a surprising amount was to make the builds reproducible; in particular, build it using only relative paths so that all references to __FILE__ are the same no matter what path one uses to build from. (Of course, the build is only reproducible as long as you don’t change the source code, but it still helped with overall stability.) Apart from that, we invented something similar to Stabilizer’s link randomization, but entirely static (link-time), and I hadn’t thought of heap randomization at all. It’s a bit sad that it’s stuck on an old version of LLVM, though. Interesting, link randomization alone reduces performance by something like 5–10%! My theory here is that there’s a lot of locality in which function call which simply based on the name (C++ namespaces and classes as a prefix, for one), so you kill your instruction cache.

Of course, an interesting question is whether one can use these effects to one’s advantage; I mean, if your compile gets “unlucky” one day and one of your important benchmarks drop, it’s nice to know that you don’t need to go hunting for a regression, but it’s maybe still not so cool to ship that binary to your customers! One could imagine something PGO-like to benchmark a bunch of different compiles and pick the one that performs the best. Unfortunately, any such “golden binary” effects are likely to be very specific to the CPU the binary was benchmarked on.

Heh, the Stabilizer paper reminds me of something.

Back in high school (the early 2000’s) I was pretty active in computing Olympiads (with good results too), and as I progressed to a university I kept in touch with folks who ran them. At one point I was asked to help them write a test/evaluation harness.

Basically, they were trying to move away from a manual testing process to an automated one, where you could just upload the code and the server would compile it and run tests automatically. Most of the stuff was done by other people, but one piece was still missing. My task was to write a program that would run the compiled executable in a restricted environment. In particular:

* It needed to limit the amount of RAM available to the process;

* It needed to restrict access to important files (to prevent hacking);

* It needed to limit the amount of CPU time given to the program (programs that take too long had to be terminated);

* It needed to measure just how fast it executed (if multiple participants get the right answer, the fastest program wins);

* Any console output needed to be forwarded to the submitter;

* Bonus points for any information salvaged if the program crashes.

Being a Windows guy, I also tried to write this in Windows, although I suspect that Linux or any other modern OS would have given me the same problems.

Long story short – I did make something, but the part about “measuring how fast it executed” was hardly anything I’m proud of. Since Windows is a preemptive OS, there’s basically a bazillion uncontrollable things that can influence a program’s execution time. How to measure it fairly?

And even some controllable things are questionable if and how they should be accounted for. For example, due to CPU caches, iterating over a large 2D array will have radically different performance characteristics depending on whether it was done row-first or column first. Reading a file all-at-once and then parsing a memory buffer will be faster than reading it byte-by-byte. Etc. Should participants be punished/rewarded for (not)knowing such things? If they did figure out the right algorithm, but simply ran afoul of some obscure hardware/software quirk, should this really be reflected in their score? Just what is it that we’re trying to evaluate here?

I still don’t know the answer. In the end I just took the naive clock ticks before starting and terminating the process, fully aware that this is hardly adequate, but I’ve been wondering about it ever since. Is there a better way of measuring this? (OK, one thing I can think of is running the same program a bunch of times and taking some sort of mean/median/average, but even that’s not perfect)

In all UNIX systems, you can ask for how much CPU time a process used (or you can limit it to be killed after using a set amount of quota). I would be surprised if Windows doesn’t have something similar.

On a system without other load and runtimes measured in seconds, I wouldn’t be too worried, though.

Yes, you can do that, but here’s the catch – what do you do with non-CPU time? Somebody reading a large input file by lots of seeking back and forth will waste a lot of time (bad design, should be punished) but most of it will be I/O that doesn’t consume CPU. And someone who wants to be evil could try to DoS the system by executing an infinite loop of Sleep(1000000). But taking there’s no way to tell if a program was idle because of it’s own fault or if the OS simply decided to do something else for a while.

I have also encountered problematic workloads in which performance categorization was sometimes an issue, with random strange outliers across runs: some may be memory layout, bad JITting (yes, there is VM involved), some may be random garbage collections (yes, there is also a garbage collector involved), and so on…

In regard of the Stabilizer paper, I am not sure if my approach of just sticking to robust statistical estimators (e.g median instead of mean and so on – https://en.m.wikipedia.org/wiki/Robust_statistics for more) is the approach of the caveman, or of the pragmatic engineer.