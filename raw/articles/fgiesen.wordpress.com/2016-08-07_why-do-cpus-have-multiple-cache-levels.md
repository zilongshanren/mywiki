---
title: Why do CPUs have multiple cache levels?
url: https://fgiesen.wordpress.com/2016/08/07/why-do-cpus-have-multiple-cache-levels/
published: '2016-08-07'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Why do CPUs have multiple cache levels?

This is a reader question from “jlforrest” that seems worth answering in more detail than just a single sentence:

I understand the need for a cache but I don’t understand why there are multiple levels of cache instead of having just one larger level. In other words, let’s say the L1 cache is 32K, the L2 cache is 256K, and the L3 cache is 2M, why not have a single 32K + 256K + 2M L1 cache?


The short version is that the various cache levels have very large variations in how they are designed; they are subject to different constraints and fulfill different purposes. As a rule of thumb, as you climb up the levels of the cache hierarchy, the caches get larger, slower, higher density (more bits stored per unit area), consume less power per bit stored, and gain additional tasks.

In the hopes of building some intuition here, let’s start with an elaborate and somewhat quaint analogy. That’s right, it is…

### Cache story time!

Suppose you’re a white-collar office worker in some unnamed sprawling 1960s bureaucracy, with no computers in sight, and your job involves a lot of looking at and cross-referencing case files (here being folders containing sheets of paper).

You have a desk (the L1 data cache). On your desk are the files (cache lines) you’re working on right now, and some other files you recently pulled and are either done with or expect to be looking at again. Working with a file generally means looking at the individual pages it contains (corresponding to bytes in a cache line). But unless they’re on your desk, files are just treated as a unit. You always grab whole files at a time, even if there’s only one page in them that you actually care about right now.

Also in the office is a filing cabinet (L2 cache). That cabinet contains files you’ve handled recently, but aren’t using right now. When you’re done with what’s on your desk, most of these files will go back into that filing cabinet. Grabbing something from the cabinet isn’t immediate – you need to walk up there, open the right drawer and thumb through a few index cards to find the right file – but it’s still pretty quick.

Sometimes other people need to look at a file that’s in your cabinet. There’s a guy with a cart, Buster (representing a sort of ring bus) who just keeps doing his rounds through all the offices. When an office worker needs a file they don’t have in their private cabinet, they just write a small request slip and hand it to Buster. For simplicity’s sake, let’s just say Buster knows where everything is. So the next time he comes by your office, Buster will check if someone requested any files that are in your cabinet, and if so will just silently pull these files out of the cabinet and put them on his cart. The next time he comes by the office of whoever requested the file, he’ll drop the file in their cabinet, and leave a receipt on the desk.

Every once in a while, Buster notices a requested file *isn’t* in the cabinet, but on the desk instead. In that case, he can’t just silently grab it; he needs to ask the worker at the desk whether they’re done with it, and if no, that worker and the one who put in the request need to agree on what to do. There are tediously elaborate corporate protocols on what to do in that situation (meetings will be called for sure!).

The filing cabinets are usually full. That means Buster can’t just put a new file in; he has to make space first, which he does by grabbing another file, preferably one that hasn’t been used in a while. Those files, Buster takes to the archive in the basement (L3 cache). In the basement, groups of files are kept densely packed in cardboard boxes on industrial shelving units. The regular office workers don’t get to come down here at all; it’s well out of their way and they’re not familiar with the details of the filing system. We leave that to the archival clerks.

Whenever Buster gets down here, he drops all the old files he grabbed for archival in the “in” tray at the front desk. He also drops off all the request slips for files that aren’t in any of the filing cabinets upstairs, but he doesn’t wait around until the clerks bring the files back, since it takes a while. They’re just going to take the request slips, pick up the file in question, and drop it off in the “out” tray whenever they’re done. So every time Buster comes around, he grabs whatever is in the “out” tray, puts it on his cart and takes it to the recipient when he next comes by.

Now, the problem is, there’s a *lot* of these files, and even with the efficient packing, they’re not even close to fitting in the basement. Most of the files are kept off-site; this is an office building in a nice part of town, and rents over here are way too high to spend that much space on storage. Instead, the company rents warehouse space 30 minutes out of town, where most of the old files are kept (this corresponds to DRAM). At the front desk of the basement sits Megan, the Head Archivist. Megan keeps track of which files are kept in the basement, and which are warehoused. So when Buster drops his request slips in the “in” tray, she checks which of them correspond to files in the basement (to be handled by the archival clerks) and which aren’t on-site. The latter just get added to a big pile of requests. Maybe once or twice a day, they send a van to the warehouse to grab the requested files, along with a corresponding number of old files to be mothballed (as said, the basement is full; they need to make space before they can store any more files from the warehouse).

Buster doesn’t know or care about the details of the whole warehousing operation; that’s Megan’s job. All he knows is that usually, those request slips he hands to the archive are handled pretty quickly, but sometimes they take hours.

### Back to the original question

So, what’s the point of this whole elaborate exercise? Briefly, to establish a more concrete model than an opaque “magic cache” that allows us to think more clearly about the logistics involved. The logistics are just as important in designing a chip as they are in running an efficient office.

The original question was “why don’t we build a single large cache, instead of several small ones”. So if you have say a quad-core machine with 4 cores that each have 32KB L1 data cache, 256KB L2 cache, plus 2MB of shared L3 cache, why don’t we just have a ~3MB shared cache to begin with?

In our analogy: for pretty much the same reason we have individual office desks that are maybe 1.50m wide, instead of seating four different people at a single enormous desk that is 150m wide.

The point of having something on the desk is that it’s within easy reach. If we make the desk too big, we defeat that purpose: if we need to walk 50m to get the file we want, the fact that it’s technically “right here on our desk” isn’t really helping. The same goes for L1 caches! Making them bigger makes them (physically) larger. Among other things, this makes accessing them slower and consume more energy (for various reasons). L1 caches are sized so they’re large enough to be useful, but small enough so they’re still fast to access.

A second point is that L1 caches deal with different types of accesses than other levels in the cache hierarchy. First off, there’s several of them: there’s the L1 data cache, but there’s also a L1 instruction cache, and e.g. Intel Core CPUs also have another instruction cache, the uOp cache, which is (depending on your point of view) either a parallel L1 instruction cache or a “L0 instruction cache”.

L1 data caches gets asked to read and write individual items that are most commonly between 1 and 8 bytes in size, somewhat more rarely larger (for SIMD instructions). Cache levels higher up in the hierarchy don’t generally bother with individual bytes. In our office analogy, everything that’s not on a desk somewhere is just handled at the granularity of individual files (or larger), corresponding to cache lines. The same is true in memory subsystems. When a core is performing a memory access, you deal in individual bytes; the higher-level caches generally handle data wholesale, one cache line at a time.

L1 instruction caches have quite different access patterns than data caches do, and unlike the L1 data cache, they’re read-only as far as the core is concerned. (Writing into the instruction cache generally happens indirectly, by putting the data in one of the higher-level unified caches, and then having the instruction cache reload their data from there). For these (and other) reasons, instruction caches are generally built quite differently from data caches; using a single unified L1 cache means that the resulting design needs to meet several conflicting design criteria, forcing compromises that make it worse at either purpose. A unified L1 cache also needs to handle both the instruction and data traffic, which is quite the load!

As an aside: as a programmer, it’s easy to ignore how much cache bandwidth is needed to fetch instructions, but it’s quite a lot. For example, when not running code from the uOp cache, all Intel Core i7 CPU cores can fetch 16 bytes worth of instructions from the L1 instruction cache, every cycle, and will in fact keep doing so as long as instruction execution is keeping up with decoding. At 3GHz, we’re talking on the order of 50GB/s *per core* here, just for instruction fetches – though, granted, only if the instruction fetch unit is busy all the time, instead of being stalled for some reason or other. In practice, the L2 cache usually only sees a small fraction of this, because L1 instruction caches work quite well. But if you’re designing a unified L1 cache, you need to anticipate at least bursts of both high instruction and high data traffic (think something like a fast memcpy of a few kilobytes of data with both source and destination in the L1 data caches).

This is a general point, by the way. CPU cores can handle *many* memory accesses per cycle, as long as they all hit within the L1 caches. For a “Haswell” or later Core i7 at 3GHz, we’re talking aggregate code+data L1 bandwidths well over 300GB/s *per core* if you have just the right instruction mix; very unlikely in practice, but you still get bursts of very hot activity sometimes.

L1 caches are designed to be as fast as possible to handle these bursts of activity when they occur. Only what misses L1 needs to be passed on to higher cache levels, which don’t need to be nearly as fast, nor have as much bandwidth. They can worry more about power efficiency and density instead.

Third point: sharing. A big part of the point of having individual desks in the office analogy, or per-core L1 caches, is that they’re *private*. If it’s on your private desk, you don’t need to ask anyone; you can just grab it.

This is crucial. In the office analogy, if you were sharing a giant desk with 4 people, you can’t just grab a file. That’s not just *your* desk, and one of your other 3 co-workers might need that file right now (maybe they’re trying to cross-reference it with another file they just picked up at the other end of the desk!). Every single time you want to pick up something, you need to yell out “everyone OK if I grab this?”, and if someone else wanted it first, you have to wait. Or you can have some scheme where everyone needs to grab a ticket and wait in line until it’s their turn if there’s a conflict. Or something else; the details don’t matter much here, but anything you do requires coordination with others.

The same thing applies with multiple cores sharing a cache. You can’t just start stomping over data unannounced; anything you do in a shared cache needs to be coordinated with all the others you’re sharing it with.

That’s why we have private L1 caches. The L1 cache is your “desk”. While you’re sitting there, you can just go ahead and work. The L2 cache (“filing cabinet”) handles most of the coordination with others. Most of the time, the worker (the CPU core) is sitting at the desk. Buster can just come by, pick up a list of new requests, and put previously requested files into the filing cabinet without interrupting the worker at all.

It’s only when the worker and Buster want to access the filing cabinet at the same time, or when someone else has requested a file that’s lying on the worker’s desk, that they need to stop and talk to each other.

In short, the L1 cache’s job is to serve its CPU core first and foremost. Because it’s private, it requires very little coordination. The L2 cache is still private to the CPU core, but along with just caching, it has an extra responsibility: deal with most bus traffic and communication instead of interrupting the core (which has better things to do).

The L3 cache is a shared resource, and access to it does need to be coordinated globally. In the office analogy, this worked by the workers only having a single way to access it: namely, by going through Buster (the bus). The bus is a choke point; the hope is that the preceding two cache levels have winnowed down the number of memory accesses far enough that this doesn’t end up being a performance bottleneck.

### Caveats

This article covers one particular cache topology that is matches current desktop (and notebook) x86 CPUs: per-core split L1I/L1D caches, per-core unified L2 cache, shared unified L3 cache, with the cores connected via a ring bus.

*Not every system looks like this.* Some (primarily older) systems don’t have split instruction and data caches; some have full Harvard architectures that treat instruction and data memory as completely separate all the way through. Often L2s are shared between multiple cores (think one office with one filing cabinet and multiple desks). In this type of configuration, the L2 caches effectively act as part of the bus between cores. Many systems don’t have L3 caches, and some have both L3 and L4 caches! I also didn’t talk about systems with multiple CPU sockets etc.

I stuck with a ring bus because it fits in nicely with the analogy. Ring buses are reasonably common. Sometimes (especially when only two or three blocks need to be connected) it’s a full mesh; sometimes it is multiple ring buses connected with a crossbar (which maps reasonably to the office analogy: a multi-story office building with one “Buster” making his rounds per floor, and an elevator connecting the floors).

As a software developer, there’s a natural tendency to assume that you can magically connect module A to module B and the data just teleports from one end to the other. The way memory actually works is incredibly complicated by now, but the abstraction presented to the programmer is just one of a large, flat array of bytes.

Hardware doesn’t work like that. Pieces aren’t magically connected through an invisible ether. Modules A and B aren’t abstract concepts; they’re physical devices, actual tiny machines, that take up actual physical area on a silicon die. Chips have a “floor plan”, and that’s not a vague nod or an in-joke; it’s an actual 2D map of what goes where. If you want to connect A to B, you need to run an actual, physical wire between them. Wires take up space, and driving them takes power (more the longer they are). Running a bunch of wires between A and B means it’s physically blocking area that could be used to connect other things (yes, chips use wires on multiple layers, but it’s still a serious problem; google “routing congestion” if you’re interested). Moving data around on a chip is an actual logistical problem, and a fiendishly complicated one at that.

So while the office thing is tongue-in-cheek, “who needs to talk to whom” and “how does the geometry of this system look – does it admit a sensible layout?” are very relevant questions for both hardware and overall system design that can have a huge impact. Spatial metaphors are a useful way of conceptualizing the underlying reality.

Another thing about the L1 cache is that it’s not the only cache which is consulted on every memory access: there is also the TLB. (Modern Intel chips have split I/D TLBs and multi-level TLBs… details.) I can’t think of an obvious way to fit TLBs into the office analogy.

Modern memory systems are often designed such that the TLB and L1 cache can be searched at the same time, with a final tag check to ensure that both the TLB and the L1 cache “hit”. If you’re especially clever, you can engineer your TLB replacement policy to try to ensure that almost all of the time, a L1 cache hit implies a TLB hit. With a large unified cache, it’s difficult to see how you would do this.

Unless you wanted a unified TLB too? Or a much larger TLB which ensured that it covered all of the unified cache? It simplifies the design to have a relatively modest-sized L1 cache.

Yeah, I didn’t want to bring virtual memory into this since even just talking about the “payload” caches themselves there are enough moving parts already. :)

@decourse – perhaps the TLB could be though of as actually holding a set of most recently looked at pages in your hand.

The TLB is more like an index card that maps the case numbers you’re working with to a separate set of filing numbers. :) You keep the translations for the ones you’re working with regularly on hand, and someone has a master directory you can consult if it’s a case number that’s not on that index card.

This is really one of the best explanations of CPU cache I’ve seen. Thanks!

I wonder how much of that knowledge is still needed for developers?

Of course, it depends on the programming level you work with. If you use really low-level language: like C (C++) (not to mention asm), then it might be worthy to understand the mechanics. But even then compilers do a great job of optimizing things (C++). And if you use languages like Jave or .NET then you might even don’t have a chance to access such low-level stuff.

Memory is one of

thefundamental abstractions in computing, and the details of how it’s implemented “under the hood” have major implications everywhere. In any language that compiles to machine code (be it ahead-of-time compiled C or even just-in-time compiled JavaScript!), cache-friendly data structures and algorithms frequently make a difference of an order of magnitude or more. (The difference is less pronounced with bytecode interpreters or similar, since the base overhead is larger.)For the most part, compilers can’t help you with this. In some fairly restricted cases (mostly dealing with very regular computations on large multidimensional arrays of numbers), some compilers can apply optimizations such as loop tiling that drastically affect cache behavior. Computations that fit the bill are few and far between in most programs.

For the most part, it’s about choosing the right data structures and algorithms. Some languages really are high-level enough that the programmer only specifies the desired result and the exact implementation is up to the compiler (database query languages such as SQL or Datalog are an example), and such optimizations are possible. But the languages you mention (C++, Java, .NET languages such as C#) are not in that category. If you use a java.util.LinkedList in your classes’ interface, the compiler is not allowed to replace that with a java.util.ArrayList no matter how much it might want to. In .NET, there’s a distinction between reference and value types; they have different semantics, and they are also quite different in terms of memory access (reference types are always indirected through a pointer; value types are stored inline in their containing scope). Many of these are not things a compiler is allowed to change in your program; as a a general rule, most compilers have a lot of freedom about what they’re allowed to do inside a function (especially after inlining it into one of its callers), and are much more constrained when externally visible aspects such as method signatures or data types are concerned.

Thanks for the reply. Good points.

Even if you don’t unerstand how L1 works, you have to get a basic understanding of how memory works. And in that case data structures that are cache friendly (continous order in memory, local) wil lbe much better that just pointer to nodes scattered around the memory space.

So, in general I think every programmer shoulw try to understand what CPU cache does, but I worry that too many people won’t care and just rely on compiler/tools.

I intend to keep this in my L1 cache for sometime so that my brain can process, and totally understand it.

This is very well explained.

Wow, this is an incredible post; takes me back to grad school and architecture class! I especially like the analogy where you talk about the desks being private. I also never thought about how instruction caches and data caches are separate (at least in the x86/64 world), which makes a lot of sense.

So much of what we do as engineers is built on layers and layers of abstraction. There’s a photo (which I can’t find at the moment) of dune buggy tied to a flatbed truck which is sitting inside of a small box truck which is inside a semi-truck. It’s a perfect example of encapsulation. We depend on all those layers to work together, but most people don’t have a good understanding of what’s really going on.

At least in the network/services world, we throw around the term “full-stack” today for people who can at least setup the stuff they work on from start to finish (and if you can automate it, you get into the “dev-ops” world as well). Where security problems are found are where we find breaks between these layers of encapsulation.

Even for developers who may never touch machine architecture, analogies like this really help to build a high level understanding of very complex systems.

When we find edge cases that allow us to break those contracts between layers, we can find exploits. If we can break one of those straps; say the one holding flatbed to the box truck, all the other layers of straps and safety can break, causing the entire thing to come falling out the back.

Separate instruction and data caches (along with first-level instruction/data TLBs when paging is supported) are common everywhere, not just on x86. Common ARMs, POWERs/PowerPCs, MIPSs, SPARCs etc. do the same thing.

It’s a very natural subdivision in any pipelined processor, because instruction fetches have to happen every single cycle (as long as the core isn’t stalled), they generally have a different working set from data, and they happen many pipeline stages earlier than data cache accesses do. Splitting the two allows more specializaton and avoids some nasty structural hazards.

I used to think that the biggest advantage of separate I/D caches is that it bought you more specialised cache management logic (e.g. you didn’t have to spend as much hardware on coherence and anything involving “write” operations for instruction caches, and could spend more implementing basic block prefetch, or stuff like that).

That is an advantage, to be sure. But now I think the biggest advantage is that it gives the rest of the pipeline the illusion of a Harvard architecture.

Well said, good choice of analogy.

A slightly more technical audience would have benefited from the “cycles per instruction” math. Yes, I know the vast complexity of a modern x86 CPU and its ability to juggle dozens of instructions in flight muddies the story, but at the same time the stark numeric understanding that it costs 100-200 instruction times to get one cache line from memory — and that only if the bank of memory was idle when the request arrived — would let the reader start to “feel” the optimization problem which led to multiple cache tiers.

Arranging algorithms to optimally use a particular cache organization (“blocking”) and dealing with regular application access patterns which match the memory interleave (“stride”) I will leave to those who program supercomputers.

– someone who designed CPUs for a while, before most of the people reading this were born

Thanks for the great article, how much does this analogy differs with the topology of ARM chip?

It has nearly nothing to do with the underlying architecture; different x86 implementations have differently structured cache hierarchies, and so do the myriad ARMs.

Private per-core L1 caches that are split between instruction and data (with associated TLBs) are near-universal in high-performance microprocessors, and have been a fixture for over 20 years at this point.

Beyond that, there’s a lot of variation. You can buy cores with anything between 0 (e.g. ARM Cortex-M0) and 4 (e.g. Intel Broadwell-C) numbered levels of cache these days, and a case can be made that the uOp cache in Broadwell-C effectively acts as “L0 instruction cache”, bringing the number of cache levels up to 5. :)

Don’t get attached to any particular detail too much. The example chosen is nice in that having 3 cache levels allows me to show different organizations (private L2 connected to a shared bus, shared L3) for the higher cache levels. The interesting point here is not so much the particular decisions themselves, but what underlying trade-offs drive them: the most important one definitely is that you want private L1 caches so your cores can (for the most part) proceed uninterrupted, with the higher cache levels handling most of the communication. Beyond that, it’s instructive to look at real-world designs, but I don’t think you’ll get a lot out of doctoring the metaphor to fit.

Very well explained sir, liked the example very much which helped to understand level of cache easily and precisely,

can you talk about what in this ananlogy is the two or 40 hands that the secretery have that are called hyperthreading? do they share the same desk most of the time or do they have different desks?

the 40 was because fiora aeterna told me that it happens in gpu. of course cpu hyperthreading is more like 2 than 40.

Hyperthreading is a single worker on a single desk that is time-slicing his work between two (or more) cases, switching to work on another case when some file he needs for his current case isn’t on hand.

Current hyperthreading implementations just stuff instructions in the same pipeline and tags them with thread 0/1, and splits them on write. (not sure how they handle pipeline flushes/misspredictions among threads)

I’m the ‘jlforrest’ who asked the original question. Thanks for the very illuminating answer. One reason I asked it was that I was under the (clearly incorrect) impression that accesses from one part of a CPU chip to another would take place at roughly the same speed. Is this actually true, but the requirements of a multicore cache coherency within a processor add enough overhead that it isn’t true in practice?

I also remember the days when some cache levels weren’t on the CPU chip at all – they were on the motherboard. Accessing them was still faster than accessing RAM. Things are simpler now.

Maintaining cache coherency usually does not make things much slower at all. More precisely, the implementations of it you see in the real world don’t, because chip makers are willing to throw a considerable amount of clever engineering at the problem of making the average memory operation fast (even if that does make contented operations somewhat slower). The crucial point is that most memory accesses don’t experience contention. The fast paths don’t end up doing much more work than a regular cache in a single-processor system (with no other cores to worry about) would, and the slow paths are taking rarely, unless the core you’re running does bad things (like having all cores contend on the same lock), in which case performance will tank badly. :)

A big factor in the higher cache levels being slower is simply that they’re larger, farther away, and reaching them usually requires passing through a few stages of buffering.

Modern CPUs are clocked fast enough, and the propagation speed of electrical signals in them is slow enough – which is to say, a small enough fraction of the speed of light :) – that you can’t round-trip a signal from one corner of the chip to the opposite end within a single clock cycle. For the outermost wire layers, you apparently get about 1/4 c. At 4GHz for a high end desktop CPU, your cycle time is 0.25ns. At that speed, that means your signal can travel (on the fastest metal layers!) about 18.7mm within a single clock cycle. That’s one way. If you want a reply back, and assuming the recipient replies instantaneously (not realistic), you need to travel the same distance back – so you get about 9.4mm.

Next, let’s consider the size of the chips in question. According to AnandTech, an Intel Skylake GT2 4C CPU die measures about 9mm×13.5mm (and that’s on the small end for a desktop chip, as they note). As you can see that’s too large to manage a round-trip in a single cycle. And that’s purely considering propagation delay; there are other factors too.

Large caches take a while to access. Part of this is simply propagation delay from distance traveled – some of it within the cache, some to get to the cache (and back). Another part is addressing the cache, e.g. taking the address bits and figuring out which row of the cache they correspond too. That’s a few logic ops per row (more for larger caches because there’s more address bits participating in that computation), and they add their part of the delay. Yet another factor is that caches often are in a different clock domain than at least some of the things they’re connected to, and cache accesses are generally not done directly; they go through a queue first, which both acts as a buffer for potential clock speed transitions and helps smooth over bursty access patterns. They also add extra delay, though.

Another big one is that the caches really are built quite differently. For example, Intel likes to use so-called VIPT (virtually indexed, physically tagged) L1 data caches. Without going into too much detail, L1 data caches are usually N-way set associative, which means that for every address, there’s N possible locations in the cache where it can be stored. For the last few generations, Intel has used N=8 in their L1 caches. Now, each cache line stores both its contents and a “tag”, which stores the address for the cache line being kept there. These are usually physical memory addresses, not the virtual memory addresses user-mode programs commonly deal with. Now, virtual addresses have to be translated to physical addresses before a memory access can happen; there’s another type of cache, the TLB, that handles this bit (TLBs are by now built as multi-level caches as well). But first completing the translation, then performing the access would be slow. A VIPT cache computes the index (which determines which N possible locations to look at) from the

virtualaddress, so the memory access can start before the correspondingphysicaladdress is even known.For the last few generations, Intel has had 8-way associative L1 data caches with 32KB size. The index is computed from the lower address bits – 32KB/8 = 4KB, the smallest supported page size on x86, which is the granularity of virtual memory remapping. Because the index is computed from the lower virtual address bits that don’t get remapped under the address translation, these lower address bits also match the corresponding physical address bits. The only problems is that we don’t yet know which of the 8 different potential locations the data we need is in – so the cache “simply” fetches all 8! The rest of the address translation proceeds in parallel, and once the right physical address is known, the correct copy (of the 8 fetched), is sent outwards to the load/store unit. This kind of trickery shaves something like 1-2 cycles of precious latency off the L1 data access time. It’s worth it there, but nowhere else. By the time a L2 fetch happens (after a L1 miss), the physical address is known; and in a L2 (or later) access path, you’ll generally probe the tags first, to figure out which way (“ways” are how the N possible locations for a given address are called) to access, and then only get that one copy of the data. Doing the tag lookup before rather than in parallel with the data lookup is slower but also a lot more power-efficient (among other things), and L2 (and higher) caches don’t need to squeeze every single cycle the way L1 caches do.

There’s plenty more things like that. :)

Note that most of these are purely increases in latency; even when a signal takes a few cycles to reach the destination, that doesn’t mean you can’t change it every cycle if you want to; it just takes a while for the data to propagate from one end to the other.

Hi ryg, it’s a little off topic, but is the Istruction cache has the same security mechanism as the L1 Data cache? i would have thought not necessarily, for the common use is that the code stays pretty much constant, but when i looked at the disassembly of FlushInstructionCache(otherProcess,…) i saw that all it does is return true. i am thinking it’s a legacy function from times or from a different arch where the instruction cache didn’t have those protections.

well, i kinda care about it because writing a debugger has a lot of changing the code binary, and i don’t know if i should still call FlushInstructionCache or not?

thanks

The 8th mage.

What do you mean by “security mechanism” here? The main security feature on the memory access path is memory protection/permissions, but that is handled on a per-page basis and happens in the TLBs.

x86s keep their instruction caches coherent with data caches, if that’s what you mean. But that’s not a security thing, that’s for backwards compatibility: self-modifying code used to be quite common on x86 up until the 486 era or so, and current x86s want to make sure that code still works.

Were there occurrences of cache line sizes that differ from L1 to the lower levels? I can see why a bigger cache line for l3 lets say can have a positive impact because memory->l3 is more about bandwidth and less about latency.

Nice cache primer. I guess the the access pattern is surely a parameter in the worst case traffic especially on a data cache, though mitigated by the cache design eg block size\associativity etc.

Even a few years later, one of the best articles about how (some parts of) CPUs work. How do you think does this analogy fit to OoO behaviors like speculative exeuction or store forwarding? For me, the L1 sounds like an incredible part of the CPU.