---
title: Cache coherency primer
url: https://fgiesen.wordpress.com/2014/07/07/cache-coherency/
published: '2014-07-07'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Cache coherency primer

I’m planning to write a bit about data organization for multi-core scenarios. I started writing a first post but quickly realized that there are a few basics I need to cover first. In this post, I’ll try just that.

### Caches

This is a whirlwhind primer on CPU caches. I’m assuming you know the basic concept, but you might not be familiar with some of the details. (If you are, feel free to skip this section.)

In modern CPUs (almost) all memory accesses go through the cache hierarchy; there are some exceptions for memory-mapped IO and write-combined memory that bypass at least parts of this process, but both of these are corner cases (in the sense that the vast majority of user-mode code will never see either), so I’ll ignore them in this post.

The CPU core’s load/store (and instruction fetch) units normally can’t even access memory directly – it’s physically impossible; the necessary wires don’t exist! Instead, they talk to their L1 caches which are supposed to handle it. And about 20 years ago, the L1 caches would indeed talk to memory directly. At this point, there’s generally more cache levels involved; this means the L1 cache doesn’t talk to memory directly anymore, it talks to a L2 cache – which in turns talks to memory. Or maybe to a L3 cache. You get the idea.

Caches are organized into “lines”, corresponding to aligned blocks of either 32 (older ARMs, 90s/early 2000s x86s/PowerPCs), 64 (newer ARMs and x86s) or 128 (newer Power ISA machines) bytes of memory. Each cache line knows what physical memory address range it corresponds to, and in this article I’m not going to differentiate between the physical cache line and the memory it represents – this is sloppy, but conventional usage, so better get used to it. In particular, I’m going to say “cache line” to mean a suitably aligned group of bytes in memory, no matter whether these bytes are currently cached (i.e. present in any of the cache levels) or not.

When the CPU core sees a memory load instruction, it passes the address to the L1 data cache (or “L1D$”, playing on the “cache” being pronounced the same way as “cash”). The L1D$ checks whether it contains the corresponding cache line. If not, the whole cache line is brought in from memory (or the next-deeper cache level, if present) – yes, the whole cache line; the assumption being that memory accesses are localized, so if we’re looking at some byte in memory we’re likely to access its neighbors soon. Once the cache line is present in the L1D$, the load instruction can go ahead and perform its memory read.

And as long as we’re dealing with read-only access, it’s all really simple, since all cache levels obey what I’ll call the


Basic invariant: the contents of all cache lines present in any of the cache levels are identical to the values in memory at the corresponding addresses, at all times.

Things gets a bit more complicated once we allow stores, i.e. memory writes. There’s two basic approaches here: write-through and write-back. Write-through is the easier one: we just pass stores through to the next-level cache (or memory). If we have the corresponding line cached, we update our copy (or maybe even just discard it), but that’s it. This preserves the same invariant as before: if a cache line is present in the cache, its contents match memory, always.

Write-back is a bit trickier. The cache doesn’t pass writes on immediately. Instead, such modifications are applied locally to the cached data, and the corresponding cache lines are flagged “dirty”. Dirty cache lines can trigger a write-back, at which points their contents are written back to memory or the next cache level. After a write-back, dirty cache lines are “clean” again. When a dirty cache line is evicted (usually to make space for something else in the cache), it always needs to perform a write-back first. The invariant for write-back caches is slightly different.


Write-back invariant:after writing back all dirty cache lines, the contents of all cache lines present in any of the cache levels are identical to the values in memory at the corresponding addresses.

In other words, in write-back caches we lose the “at all times” qualifier and replace it with a weaker condition: either the cache contents match memory (this is true for all clean cache lines), or they contain values that eventually need to get written back to memory (for dirty cache lines).

Write-through caches are simpler, but write-back has some advantages: it can filter repeated writes to the same location, and if most of the cache line changes on a write-back, it can issue one large memory transaction instead of several small ones, which is more efficient.

Some (mostly older) CPUs use write-through caches everywhere; some use write-back caches everywhere; some have a simpler write-through L1$ backed by a write-back L2$. This may generate redundant traffic between L1$ and L2$ but gets the write-back benefits for transfers to lower cache levels or memory. My point being that there’s a whole set of trade-offs here, and different designs use different solutions. Nor is there a requirement that cache line sizes be the same at all levels – it’s not unheard-of for CPUs to have 32-byte lines in L1$ but 128-byte lines in L2$ for example.

Omitted for simplicity in this section: cache associativity/sets; write-allocate or not (I described write-through without write-allocate and write-back with, which is the most common usage); unaligned accesses; virtually-addressed caches. These are all things you can look up if you’re interested, but I’m not going to go that deep here.

### Coherency protocols

As long as that single CPU core is alone in the system, this all works just fine. Add more cores, each with their own caches, and we have a problem: what happens if some other core modifies data that’s in one of our caches?

Well, the answer is quite simple: nothing happens. And that’s bad, because we *want* something to happen when someone else modifies memory that we have a cached copy of. Once we have multiple caches, we really need to keep them synchronized, or we don’t really have a “shared memory” system, more like a “shared general idea of what’s in memory” system.

Note that the problem really is that we have multiple caches, not that we have multiple cores. We could solve the entire problem by sharing all caches between all cores: there’s only one L1$, and all processors have to share it. Each cycle, the L1$ picks one lucky core that gets to do a memory operation this cycle, and runs it.

This works just fine. The only problem is that it’s also slow, because cores now spend most of their time waiting in line for their next turn at a L1$ request (and processors do a *lot* of those, at least one for every load/store instruction). I’m pointing this out because it shows that the problem really isn’t so much a multi-*core* problem as it is a multi-*cache* problem. We know that one set of caches works, but when that’s too slow, the next best thing is to have multiple caches and then make them behave *as if* there was only one cache. This is what cache coherency protocols are for: as the name suggests, they ensure that the contents of multiple caches stay coherent.

There are multiple types of coherency protocols, but most computing devices you deal with daily fall into the category of “snooping” protocols, and that’s what I’ll cover here. (The primary alternative, directory-based systems, has higher latency but scales better to systems with lots of cores).

The basic idea behind snooping is that all memory transactions take place on a shared bus that’s visible to all cores: the caches themselves are independent, but memory itself is a shared resource, and memory access needs to be arbitrated: only one cache gets to read data from, or write back to, memory in any given cycle. Now the idea in a snooping protocol is that the caches don’t just interact with the bus when they want to do a memory transaction themselves; instead, each cache continuously snoops on bus traffic to keep track of what the other caches are doing. So if one cache wants to read from or write to memory on behalf of its core, all the other cores notice, and that allows them to keep their caches synchronized. As soon as one core writes to a memory location, the other cores know that their copies of the corresponding cache line are now stale and hence invalid.

With write-through caches, this is fairly straightforward, since writes get “published” as soon as they happen. But if there are write-back caches in the mix, this doesn’t work, since the physical write-back to memory can happen a long time after the core executed the corresponding store – and for the intervening time, the other cores and their caches are none the wiser, and might themselves try to write to the same location, causing a conflict. So with a write-back model, it’s not enough to broadcast just the writes to memory when they happen; if we want to avoid conflicts, we need to tell other cores about our intention to write *before* we start changing anything in our local copy. Working out the details, the easiest solution that fits the bill and works for write-back caches is what’s commonly called the [MESI protocol](http://en.wikipedia.org/wiki/MESI_protocol).

### MESI and friends

This section is called “MESI and friends” because MESI spawned a whole host of closely related coherency protocols. Let’s start with the original though: MESI are the initials for the four states a cache line can be in for any of the multiple cores in a multi-core system. I’m gonna cover them in reverse order, because that’s the better order to explain them in:

**I**nvalid lines are cache lines that are either not present in the cache, or whose contents are known to be stale. For the purposes of caching, these are ignored. Once a cache line is invalidated, it’s as if it wasn’t in the cache in the first place.**S**hared lines are clean copies of the contents of main memory. Cache lines in the shared state can be used to serve reads but they can’t be written to. Multiple caches are allowed to have a copy of the same memory location in “shared” state at the same time, hence the name.**E**xclusive lines are also clean copies of the contents of main memory, just like the S state. The difference is that when one core holds a line in E state, no other core may hold it at the same time, hence “exclusive”. That is, the same line must be in the I state in the caches of all other cores.**M**odified lines are dirty; they have been locally modified. If a line is in the M state, it must be in the I state for all other cores, same as E. In addition, modified cache lines need to be written back to memory when they get evicted or invalidated – same as the regular dirty state in a write-back cache.

If you compare this to the presentation of write-back caches in the single-core case above, you’ll see that the I, S and M states already had their equivalents: invalid/not present, clean, and dirty cache lines, respectively. So what’s new is the E state denoting exclusive access. This state solves the “we need to tell other cores before we start modifying memory” problem: each core may only write to cache lines if their caches hold them in the E or M states, i.e. they’re exclusively owned. If a core does not have exclusive access to a cache line when it wants to write, it first needs to send an “I want exclusive access” request to the bus. This tells all other cores to invalidate their copies of that cache line, if they have any. Only once that exclusive access is granted may the core start modifying data – and at that point, the core knows that the only copies of that cache line are in its own caches, so there can’t be any conflicts.

Conversely, once some other core wants to read from that cache line (which we learn immediately because we’re snooping the bus), exclusive and modified cache lines have to revert back to the “shared” (S) state. In the case of modified cache lines, this also involves writing their data back to memory first.

The MESI protocol is a proper state machine that responds both to requests coming from the local core, and to messages on the bus. I’m not going to go into detail about the full state diagram and what the different transition types are; you can find more in-depth information in books on hardware architecture if you care, but for our purposes this is overkill. As a software developer, you’ll get pretty far knowing only two things:

Firstly, in a multi-core system, getting read access to a cache line involves talking to the other cores, and might cause them to perform memory transactions.

Writing to a cache line is a multi-step process: before you can write anything, you first need to acquire both exclusive ownership of the cache line and a copy of its existing contents (a so-called “Read For Ownership” request).

And secondly, while we have to do some extra gymnastics, the end result actually does provide some pretty strong guarantees. Namely, it obeys what I’ll call the


MESI invariant: after writing back all dirty (M-state) cache lines, the contents of all cache lines present in any of the cache levels are identical to the values in memory at the corresponding addresses. In addition,at all times, when a memory location is exclusively cached (in E or M state) by one core, it is not present in any of the other core’s caches..

Note that this is really just the write-back invariant we already saw with the additional exclusivity rule thrown in. My point being that the presence of MESI or multiple cores does not necessarily weaken our memory model at all.

Okay, so that (very roughly) covers vanilla MESI (and hence also CPUs that use it, ARMs for example). Other processors use extended variants. Popular extensions include an “O” (Owned) state similar to “E” that allows sharing of dirty cache lines without having to write them back to memory first (“dirty sharing”), yielding MOESI, and MERSI/MESIF, which are different names for the same idea, namely making one core the designated responder for read requests to a given cache line. When multiple cores hold a cache line in Shared state, only the designated responder (which holds the cache line in “R” or “F” state) replies to read requests, rather than everyone who holds the cache line in S state. This reduces bus traffic. And of course you can add both the R/F states and the O state, or get even fancier. All these are optimizations, but none of them change the basic invariants provided or guarantees made by the protocol.

I’m no expert on the topic, and it’s quite possible that there are other protocols in use that only provide substantially weaker guarantees, but if so I’m not aware of them, or any popular CPU core that uses them. So for our purposes, we really can assume that coherency protocols keep caches coherent, period. Not mostly-coherent, not “coherent except for a short window after a change” – properly coherent. At that level, barring hardware malfunction, there is always agreement on what the current state of memory should be. In technical terms, MESI and all its variants can, in principle anyway, provide full [sequential consistency](http://en.wikipedia.org/wiki/Sequential_consistency), the strongest memory ordering guarantee specified in the C++11 memory model. Which begs the question, why do we have weaker memory models, and “where do they happen”?

### Memory models

Different architectures provide different memory models. As of this writing, ARM and POWER architecture machines have comparatively “weak” memory models: the CPU core has considerable leeway in reordering load and store operations in ways that might change the semantics of programs in a multi-core context, along with “memory barrier” instructions that can be used by the program to specify constraints: “do not reorder memory operations across this line”. By contrast, x86 comes with a quite strong memory model.

I won’t go into the details of memory models here; it quickly gets really technical, and is outside the scope of this article. But I do want to talk a bit about “how they happen” – that is, where the weakened guarantees (compared to the full sequential consistency we can get from MESI etc.) come from, and why. And as usual, it all boils down to performance.

So here’s the deal: you will indeed get full sequential consistency if a) the cache immediately responds to bus events on the very cycle it receives them, and b) the core dutifully sends each memory operation to the cache, in program order, and wait for it to complete before you send the next one. And of course, in practice modern CPUs normally do none of these things:

- Caches do
*not*respond to bus events immediately. If a bus message triggering a cache line invalidation arrives while the cache is busy doing other things (sending data to the core for example), it might not get processed that cycle. Instead, it will enter a so-called “invalidation queue”, where it sits for a while until the cache has time to process it. - Cores do not, in general, send memory operations to the cache in strict program order; this is certainly the case for cores with Out-of-Order execution, but even otherwise in-order cores may have somewhat weaker ordering guarantees for memory operations (for example, to ensure that a single cache miss doesn’t immediately make the entire core grind to a halt).
- In particular, stores are special, because they’re a two-phase operation: we first need to acquire exclusive ownership of a cache line before a store can go through. And if we don’t already have exclusive ownership, we need to talk to the other cores, which takes a while. Again, having the core idle and twiddling thumbs while this is happening is not a good use of execution resources. Instead, what happens is that stores start the process of getting exclusive ownership, then get entered into a queue of so-called “store buffers” (some refer to the entire queue as “store buffer”, but I’m going to use the term to refer to the entries). They stay around in this queue for a while until the cache is ready to actually perform the store operation, at which point the corresponding store buffer is “drained” and can be recycled to hold a new pending store.

The implication of all these things is that, by default, loads can fetch stale data (if a corresponding invalidation request was sitting in the invalidation queue), stores actually finish later than their position in the code would suggest, and everything gets even more vague when Out of Order execution is involved. So going back to memory models, there are essentially two camps:

Architectures with a weak memory model do the minimum amount of work necessary in the core that allows software developers to write correct code. Instruction reordering and the various buffering stages are officially permitted; there are no guarantees. If you need guarantees, you need to insert the appropriate memory barriers – which will prevent reordering and drain queues of pending operations where required.

Architectures with stronger memory models do a lot more bookkeeping on the inside. For example, x86 processors keep track of all pending memory operations that are not fully finished (“retired”) yet, in a chip-internal data structure that’s called the MOB (“memory ordering buffer”). As part of the Out of Order infrastructure, x86 cores can roll back non-retired operations if there’s a problem – say an exception like a page fault, or a branch mispredict. I covered some of the details, as well as some of the interactions with the memory subsystem, in my earlier article “[Speculatively speaking](https://fgiesen.wordpress.com/2013/03/04/speculatively-speaking/)“. The gist of it is that x86 processors actively watch out for external events (such as cache invalidations) that would retroactively invalidate the results of some of the operations that have already executed, but not been retired yet. That is, x86 processors know what their memory model is, and when an event happens that’s inconsistent within that model, the machine state is rolled back to the last time when it was still consistent with the rules of the memory model. This is the “memory ordering machine clear” I covered in [yet another earlier post](https://fgiesen.wordpress.com/2013/01/31/cores-dont-like-to-share/). The end result is that x86 processors provide very strong guarantees for all memory operations – not quite sequential consistency, though.

So, weaker memory models make for simpler (and potentially lower-power) cores. Stronger memory models make the design of cores (and their memory subsystems) more complex, but are easier to write code for. In theory, the weaker models allow for more scheduling freedom and can be potentially faster; in practice, x86s seem to be doing fine on the performance of memory operations, for the time being at least. So it’s hard for me to call a definite winner so far. Certainly, as a software developer I’m happy to take the stronger x86 memory model when I can get it.

Anyway. That’s plenty for one post. And now that I have all this written up on my blog, the idea is that future posts can just reference it. We’ll see how that goes. Thanks for reading!

Because I am the grammar Nazi I noticed a few minor errors. FWIW. Delete this comment after reading if you want. In particular, ‘are’ ain’t contractable.

usage so, well, get used

virtually-addressed caches

there’s only one L1$

There are multiple types

But if there are write-back caches

there are essentially two camps

there are no guarantees

All fixed. Man, tons of pluralization mistakes this time. Thanks for the list!

You said that MESI could, potentially, provide full sequential consistency, which is true but together with the rhetoric afterwards could be interpreted as x86 offering sequential consistency. In fact sequential consistency is really too expensive. It means (IIRC) that writes have to wait for all preceding reads, which is sometimes insanely expensive and really not worth it.

Excellent article. I look forward to the follow-up.

I’ve always find it curious (and it is a perpetual source of confusion to many developers) that reordering of memory operations is completely orthogonal to reordering of instructions. And, in fact, most CPUs that reorder instructions do not reorder memory operations, and vice-versa. Odd but true.

“In fact sequential consistency is really too expensive. It means (IIRC) that writes have to wait for all preceding reads, which is sometimes insanely expensive and really not worth it.”In the x86 memory model, writes

dohave to wait for all preceding reads, always. The IA-32 architecture manuals spell this out clearly in section 8.2.2, “Memory Ordering in P6 and More Recent Processor Families”. I quote:In other words, writes may be reordered with newer reads (i.e. they may finish later than they occur in program order – a natural consequence of having store buffers) but for the most part, that’s it. This is not full sequential consistency (since after all writes may happen later than in program order) but it’s close. I believe x86’s model is essentially the same as SPARC’s “Total Store Order” model, but the details get hairy.

This sounds as though x86’s really can’t do much memory reordering at all, and as if it had to be really slow. But that’s not true. x86 cores can and do reorder memory operations – they’re just not allowed to get caught :). This is where the whole Memory Order Buffer business comes into place. MOB entries are assigned in program order, and are also retired in program order. Imagine that all memory operations in the MOB get tagged with a time stamp (just a counter) that’s assigned in an order consistent with the memory model. That’s not necessarily how it works internally, but it’s a decent model.

While an entry is in the MOB (i.e. a memory operation is pending and not yet retired), we need to watch out for external events (i.e. cache invalidations) that can invalidate the results of that operation. When such an event occurs, that operation was invalid (same as if it was a mispredicted branch), and so are all instructions that followed it in “memory order”. So now the core needs to roll back the state to right before it executed that instruction, and try again. The primary cost, as far as I can tell (and the devil’s in the details, so having never implemented it, I might well be missing something important!), is that you really need to be able to detect ordering violations for

allcache lines referenced by any instruction in the MOB. I believe other processors with an explicit locked cache line and LL/SC semantics (e.g. POWER or ARM) only need to be able to detect this case for the locked cache line, which is much simpler. On the other hand, I believe it’s that same infrastructure that allowed Intel to put the transactional memory extensions into Haswell with relatively little work; most of the heavy lifting was already being done anyway!Anyway, it’s essentially just another kind of speculative execution. Just as we can speculate on our branch prediction being correct, and rolling back operations when it wasn’t, we can speculate on memory ordering violations being rare, and roll back when they occur.

Helpful article! You may want to add a paragraph describing N-way associative caching, and perhaps link to Ulrich Drepper’s “What Every Programmer Should Know About Memory” (http://www.akkadia.org/drepper/cpumemory.pdf), which is a great read.

I intentionally left out cache associativity and several other topics. (Each section has keywords with additional topics you can search for.)

Set associativity is an important part of how caches work but has no effect whatsoever on cache coherency which is the topic of this post.

The stay around in this queue for a while until the cache

The should be They

the machine is state is rolled back to the last time

Delete the first is

Thanks for writing this, I learned a lot, and it was at just the right level of abstraction for me to understand as a software dev.

Do you have a post about complications with distributed shared memory? Why does it seem that software based coherence protocols like Paxos are more popular than hardware based ones like Microsoft’s FaRM?

Have you heard of ScaleMP? They’re a hypervisor that presents memory from many small nodes as a single address space. How do you think they would maintain coherency?

Oops, this got buried in the comment approval queue for a while. Thanks for your corrections, all fixed!

I have never interacted with distributed shared memory and can’t comment on it.

Lets have an instance where we have two cores each having L1$ and shared L2 and the model is coherent. Now, at a given time the memory say 0xFFFF_CCCC which is preoccupied in L1$ with value=0x0, Core0 write 1 at 0xFFFF_CCCC and Core1 reads 0xFFFF_CCCC. What will core0 reads in write-back mode or write through mode? I believe in-spite if being coherent at given instant core0 will read 0xFFFF_CCCC as 0x1 and core1 will read 0x0.

Core 0 can’t write before acquiring cache line exclusive ownership, which invalidates core 1’s copy.

Excellent post.

A question from a beginner that everybody else probably knows the answer to – I understand the need for a cache but I don’t understand why there are multiple levels of cache instead of having just one larger level. In other words, let’s say the L1 cache is 32K, the L2 cache is 256K, and the L3 cache is 2M, why not have a single 32K + 256K + 2M L1 cache?

Some trivial typos:

Some trivial typos:

“there’s a bunch of basics” -> “there are a bunch of basics”

“there’s some exceptions for memory-mapped IO” -> “there are some exceptions for memory-mapped IO”

Thanks for the typos, fixed!

Replying to your main question took me a while and was meaty enough to turn it into its own post, which is now here. Thanks for the question and I hope the wait’s been worth it. :)

Actually, “there are a bunch of basics” is incorrect. The rule here is, the subject must match the verb in number. There’s only one bunch, so “there is a bunch”. This is a common overcorrection because people overlook the effect of “bunch of” and try to match the verb number to “basics”. Not correct.

I have a question on MESI , let’s say we have cpu0 ,cpu1, both of them are on S state, cpu0 wants to write ,so it sends I to other cpu, once other cpu invalid their cache line ,then do modification, changes state to M . what if cpu1 wants to do modification either at the same time? it sends I to another cpu, eventually, which one will win?

second question is if one won ,change to it’s state to M , how about another cpu, will it’ write lost? or it will read from main memo, restart it’s write process?

The sequence of events goes:

1. Cpu0 wants to write cache line, sends an upgrade request on the bus.

2. Cpu1 (and all other caches that have the line present) acknowledge upgrade, set the state of their version of the line to I.

3. Once Cpu0 has received all acknowledgements, it sets its version of the line to E state.

4. Either that same cycle or some time later (doesn’t matter), Cpu0 actually updates the contents of its version of the cache line, at which point it switches to M state. (Meaning the cache line is dirty and needs to be written back to memory if it gets evicted.)

No CPU can change its state unilaterally. All such operations require messages being sent back and forth, and acknowledgement by all involved parties.

If Cpu1 wants to upgrade the cache line “at the same time” as Cpu0, what happens is that both CPUs want to initiate a bus transaction involving that cache line in the same cycle. There can only be one such transaction per cycle, and the bus decides (arbitrarily, from the point of view of the CPUs anyway) who wins. Whoever loses needs to try again later. Say Cpu0 wins (so we’re in the scenario above). Then Cpu1, which wants to write to a cache line it currently doesn’t have (since Cpu0 just won the race in the previous cycle, causing Cpu1 to transition its copy of the line to I state), needs to issue a RFO (Read For Ownership) request on the bus.

If Cpu0 were to respond to that immediately, we could have a situation where Cpu0 has its copy of the cache line in E state but hasn’t finished a write, and then immediately relinquishes ownership (so Cpu0’s state of the cache line goes to I) and sends the data to Cpu1. If you allow this, you can have a livelock situation, where Cpu0 and Cpu1’s states of the cache line in question oscillate between I and E without either making any progress.

The typical solution is for Cpu0 not to respond to the RFO until it has had a chance to finish the write that caused it to grab the cache line in the first place. Because Cpu1 can’t do anything with the cache line until it has received a reply to the RFO, this solves this particular race. But you still need to be careful with algorithms that use atomic read-modify-write primitives, to ensure that there is forward progress. This is a tricky issue. and processors that expose low-level primitives like load-linked store-conditional make visible just how tricky, since the buck is passed on to code that uses those primitives. :) (Usually, there is a limit on number of instructions executed between LL and SC, branches are quite restricted, the code between the LL and SC must fit into a small number of cache lines, and so forth…)

Thank you so much for your reply , if the situation gets more complicated ,like we get store buffer and invalid queue involved, let’s say initially, both of the cpu cache line are on S state, cpu0 keeps the write operation in it’s store buffer, then sends I to other cpu, cpu1 received request ,and just keeps it in invalid queue , then cpu1 wants to write , it sends I to cpu0, do the same thing, eventually, both of the cpu will have content in store buffer ,and invalid queue, it seems a little mass, my first question is that when the invalid queue will be processed(when it is full or under other situation?)

2 which one goes first for both cpu?

3 is it disorder ? if the rule like what you point out on above? one cpu receives all Invalid response first ,then it starts to process the store buffer ,finish the modification, change the state ,then reply others ,others will not proceed util it gets the response ?

First off, store buffers and invalidation queues don’t enter into the coherency protocol at all.

The coherency protocol defines a mechanism to synchronize cache line states over some shared medium (like a bus) in a way that guarantees they are consistent with each other, by sending messages between all participants.

Both invalidation queues and store buffers don’t change any of that. From the point of view of the coherency protocol, they’re an implementation detail.

As far as MESI is concerned, as soon as you acknowledge an invalidate transaction on the bus, that cache line is in I state on your end, and you’re promising to behave as if the cache line was in I state for all future bus transactions (well, until the cache line state changes again). If you happen to acknowledge invalidates immediately but put them into a queue on your end, that’s your problem, and it’s completely local to the core. Same thing with store buffers. These are structures internal to the core that don’t affect the coherency protocol and are completely invisible to other parties on the bus.

Neither of them affect the coherency protocol. Both of them affect the cores’ perception of memory ordering. The view of memory maintained by MESI across the bus is coherent at all times, i.e. there is never any disagreement about what the current “official” contents of any cache line are, and there is always at most one modified (dirty) copy of a cache line in the system.

However, invalidation queues mean that the actual contents of any given cache don’t necessarily agree with the agreed-upon “official” version. Any cache might still have a stale copy of a cache line that was already acknowledged as invalidated on the bus.

Whether this is considered a problem or not depends on the CPU’s memory ordering model. CPUs with weak memory ordering completely expose this fact and just expect the programmer to deal with it. CPUs with stronger memory ordering (like x86), or at least some instructions with stronger ordering requirements (e.g. ARMv8’s load-acquire instructions), have to do more work.

The details of this get complicated, but on something fairly strongly-ordered like x86, you can think of it like this (I’m oversimplifying here): actual cache access is weakly ordered (and also subject to out-of-order execution), but every load and every incoming invalidation message is time-stamped. In addition, the processor keeps track of what the original program ordering of loads was.

Then, long after a load has gotten its data, but before the corresponding instruction is allowed to commit/retire, the CPU ensures that:

1. all older instructions in program order have retired (this is a general requirement for all instructions and not specific to loads)

2. all queued invalidations that happened before the load time-stamp have been processed (i.e. this is a partial drain of the invalidation queue, where every invalidate older than the load has to have been processed),

3. none of those invalidations affected any cache lines touched by the load

If and only if these conditions are fulfilled, a load is allowed to retire. Otherwise the machine is rolled back to just before the offending load, which then gets re-issued.

Store buffers are similar, just on the opposite end. Buffered stores are stores that the CPU intends to happen later, but that have not been written to the cache yet.

And yes, it definitely gets messy. It is not at all easy to guarantee that all this flushing and retrying in the presence of ordering conflicts even eventually makes forward progress when multiple CPUs try to access the same cache lines – this is something that hardware designers have to take pains to ensure.

I’ve been reading lots of articles about memory order and cache coherency, and found this one the most helpful.

One thing is still confusing me:

Quote from https://research.swtch.com/hwmm

“`

Litmus Test: Write Queue (also called Store Buffer)

Can this program see r1 = 0, r2 = 0?

// Thread 1 // Thread 2

x = 1 y = 1

r1 = y r2 = x

On sequentially consistent hardware: no.

On x86 (or other TSO): yes!

“`

This is a litmus test mentioned in many other articles. They all say that both r1 and r2 being zero could happen on TSO because of the existence of the store buffer. They seem to assume that all the stores and loads are executed in order, and yet the result is both r1 and r2 being zero. This later concludes that “store/load reordering could happen”, as a “consequence of the store buffer’s existence”.

However we know that OoO execution could also reorder the store and the load in both threads. In this sense, regardless of the store buffer, this reordering could result in both r1 and r2 being zero, as long as all four instructions retire without seeing each other’s invalidation to x or y. And this seems to me that “store/load reordering could happen”, just because “they are executed out of order”. (I might be very wrong about this since this is the best I know of speculation and OoO execution.)

My question can be stated another way: say I somehow observed this litmus test on an x86 machine, was it because of the store buffer, or OoO execution? Or is it even possible to know which?

Last, no matter whether my questions are answered, I want to show my respect to this wonderful post. Thank you.

The short version is that you have no way of telling, and that OoO cores actually reorder memory access however they want; the memory ordering guarantees don’t actually need to be followed to the letter as long as the observed behavior doesn’t change, and most reorderings are benign! So CPUs actually reorder as they want but do some bookkeeping to keep track of when that reordering would actually change results in a way that is not allowed, and only these need special care.

The slightly longer version is that no out-of-order core I know of, no matter the architecture (i.e. whether it be x86, ARM, POWER/PPC, …), actually obeys the architectural memory ordering rules at time of instruction execution. In an OoO core, both loads and stores execute speculatively in an essentially arbitrary order, and potentially long (can be hundreds of cycles) before it is known whether they should even happen at all. Bus transactions such as acquiring exclusive cache line ownership are also initiated speculatively, potentially long before it is known if that store will even happen.

Speculative loads affect what’s in the various caches, which is implementation-specific and not subject to architectural guarantees. Speculative stores in an OoO core don’t write their data to memory/caches at all at execution time; they write the address and data into what is essentially a transaction log that is applied at commit/retire time, once it is known whether the store actually executed. Intel somewhat confusingly calls these log entries the “store buffers”, but they are actually a different type of store buffer than what is normally used for the “store buffers” in memory model descriptions. Let’s just refer to the log of speculative stores as the Store Queue (that’s the more common name), while “store buffers” are a separate queue of pending writes to the cache or memory that are definitely going to happen (they’re not speculative anymore) but haven’t happened yet. (These exist in most in-order cores too, and are there for different reasons than the OoO Store Queue is.)

Anyway, what actually happens in OoO cores is that the chip actually executes loads and stores in whatever order it wants to but knows what the architectural memory ordering rules are. If it determines at retire time that the order it chose gives results that would be impossible under the architectural memory model, it doesn’t retire the load/store, flushes the speculative state and retries from the offending memory access – similar to a mispredicted branch.

Exactly what kind of bookkeeping is necessary here depends on what the architectural guarantees are, so the exact mechanisms are different between say ARM and x86, but just for intuition, you can think of it like this: once a core actually executes a load or store (loads actually access the cache, store execution just populates a Store Queue entry) the target cache line address goes on a watch list. If that cache line gets changed between the instruction getting executed (which is when the data was actually read for load) and the instruction retiring (which is when the load/store truly happens as far as the running program and the external world is concerned), we need to be careful because we might be introducing visible deviations from the architectural memory model. Tracking exactly when we made a non-allowed change can get tricky, and there’s a trade-off to be made here between the precision of whatever logic is ultimately used (we want to be as close to “exact” as possible, letting reorderings that are permitted by the architectural memory model go through, to avoid unnecessary pipeline flushes) and the complexity (and likelihood of bugs) in the resulting hardware.

Anyway, the upshot of all this is that only a small fraction of loads/stores executed in a typical program actually accesses memory that is concurrently modified by another core, and the only time we actually need to follow the rules is in the cases when there are concurrent memory accesses from another core involved. OoO cores effectively have a relaxed memory model for most loads and stores most of the time, plus some tracking logic to determine when they’re being too sloppy so they can flush and try again.

Thank you for your kind answer. I have a further question: Say I somehow disabled the store buffer on an x86 CPU with OoO cores, so that the retired store will directly commit to L1D. For the given litmus test in my original question, can this program see r1 = 0, r2 = 0?

That is equally (I hope) asking: Does x86 OoO core allow the later load to retire before the earlier store, given that this is a store/load reordering which is permitted by the architectural memory model?

The first question is just meaningless because it breaks its own premise.

If you “disabled the store buffers” on an OoO x86 CPU, the result would not be that stores would happen immediately, but rather that you wouldn’t be able to do any stores at all. The store buffers are the mechanism by which data actually gets written to the memory hierarchy. If you remove them and still want to be able to do stores, you need to replace them with something else that does that job, and your question is still impossible to answer because there is no unique mechanism you would do in its place.

You could replace the way stores are committed with a mechanism that ensures sequential consistency, and then they would be sequentially consistent. You could replace them with a much more relaxed implementation and then they would have a weaker memory model than x86. In either scenario the answer doesn’t depend on whether you “disable store buffers” or not, but only on what you do instead, which could be anything.

As for the second question, it depends on what you mean by “later load” and “earlier store”. If you mean the operations on the thread the CPU is executing, then no. Retirement is strictly in program order, always, independent of memory model. This is true on every out-of-order CPU. Any observed reorderings are not because instructions retire out of order, they never do; they occur because actual execution (when the results of the operation were determined) and commit (when they turn from speculative to actual and might eventually become visible) are not at the same time, and because it takes time both for operations from external agents to become visible to us, and for our operations to become visible to other observers.

If instead you mean later/earlier in the sense of some global timestamp or something, that also doesn’t work, because such a linear ordering of events only exists with sequential consistency, and the x86 memory model permits executions that are not sequentially consistent; observers do not agree on the ordering of events.

If retirement is strictly in program order, can we say that for this specific litmus test, the observed reordering is solely caused by the store buffer? Or is anything else out there causing the observed reordering too?

The store buffer isn’t actually the cause of the reordering either; what’s really going on is that both the store buffer and the reordering are symptoms of the same underlying cause: the way the memory access path is built and pipelined necessitates both of them.

The actual reasons differ from core to core, but very different cores implementing different architectures have converged on a similar solution in that spot.

For OoO cores, there are several things going on but one of the things to consider here is that retirement/commit is in-order. But while the out-of-order execution logic makes sure that throughput limits such as “1 store per cycle max” are obeyed at execution time, that is not the (program) order that instructions actually commit in. So if you have say 3 back-to-back stores in your program and your CPU can execute at most 1 store per cycle, the OoO logic will space these out over 3 cycles, but you might still need to commit 3 of them in the same cycle if they’re right next to each other in program order. But we don’t have the hardware to do 3 stores at once. We can do one per cycle (in this example). One option would be to straight-up refuse to retire more than 1 store per cycle. So the first cycle could retire earlier instructions up to and including the first store; the cycle after, you only get to retire that single store instruction; and the cycle after, you can retire the 3rd store and maybe what comes after. That’s adding a bottleneck in the in-order portion of the pipeline though, which is a bad place to have them, and we already know that our out-of-order execution logic spaces the stores out so we get at most one new store per cycle; our long-term average of stores per cycle is never above 1, so there’s no fundamental problem here, they can just come in bursts.

So what actually happens in this example is that the CPU commits the 3 stores at once in the same cycle, but they don’t actually write to the cache in the same cycle. They go serially in 3 separate cycles. In other words they go into a queue at commit time, and we can either size that pessimistically for the worst case (possible, but I’ve never seen it done), or you can assign each instruction a place in that queue way early (in the in-order frontend, at rename/allocate time), and only free up that queue spot once the data is actually written. That way we have some amount of slack from the queue size and if we run out of queue space, we stall in the front end and stop adding new instructions entirely (and then size the queue so this doesn’t happen often).

Furthermore, it turns out that your typical OoO core _already has a queue of pending stores anyway_. That’s the store queue I mentioned earlier that’s the log of speculative stores that we’re not sure yet should actually write to memory or not. So all that really happens here in out-of-order x86s is that the data structure for pending speculative stores and the data structure for committed-but-not-yet-written-to-memory stores is the same, and the queue entries are actually freed after the real write is done.

That part explains why Intel generally uses the term “store buffers” to refer to both the speculative out-of-order thing (the Store Queue Entries) and the post-commit TODO list of stores that are going to write back but haven’t yet, because in their big cores, they’re the same thing.

Anyway, so in this particular example, the ultimate go/no go decision is when the instruction commits. But in any given cycle, we can either have more than 1 store, or have just a single store but a backlog of older stores from earlier more-than-1-store cycles to go through. We decide whether that store is going to happen or not, and then it might hang around waiting in line for a few more cycles, and anything that happens between the commit and the actual write can’t influence the decision to actually store or not anymore.

The store buffers/SQ entries do other things as well that have nothing to do with multi-core memory ordering; they’re an integral part of the OoO machinery for memory operations, in particular the ability to speculate around stores. If you didn’t have them at all then every store would be the equivalent of a pipeline flush (because it needs to wait until it becomes non-speculative). No good. A “light” version would be to force retirement to only allow 1 store per cycle through (instead of the relaxed version which maintains a long-term average of <=1 but allows bursts), but this too comes at a major performance cost so it's not usually done.

That's out-of-order cores. In-order cores also usually have store buffers, in pretty much the same place, but for very different reasons. The cores I'm aware of have them in essence because of virtual memory and timing requirements, but there might well be other designs that have them for different reasons.

What does virtual memory have to do with it? Well, any address occurring in the program is not actually a real (physical) memory address; it's a virtual address, and every memory access (loads and stores both) first needs to translate those addresses from virtual to physical, a process that itself can involve several memory accesses. The fast (and common) path, however, uses a dedicated cache, usually called the Translation Lookaside Buffer or TLB for short, that caches virtual to physical address translations.

The direct implementation of this first does a TLB lookup on the virtual address to get the translation, and then an access into the data cache array with the translated address. But that's a problem, because the TLB lookup itself takes a similar time to the cache data array access, so adding virtual memory support like that will (in the best case, mind you!) substantially increase L1 memory access latency, which is no good since that tends to be one of the key performance limiters for most code, and while out-of-order cores have at least some ability to try and schedule around this and do other work at the same time, we're now assuming an in-order core, which has no way to hide that extra latency even if it wanted to.

There are many ways to solve this problem. One way is to access the cache with virtual addresses instead. No need for translation on the access path (good), causes many other problems with virtual memory that need to be addressed elsewhere (bad). Not a common choice for CPUs, I've seen some GPUs use this for their lower cache levels though. Another, "way prediction" uses a predictor (like a branch predictor) to predict where in the cache a given virtual address would end up. The most popular choice for CPUs for the past 25 years or so has been VIPT caches (virtually indexed, physically tagged) which in essence builds things so that a given virtual address can only map to a relatively small number of locations in the cache, usually something like 4 or 8. And then on every load, the cache simultaneously starts the TLB lookup and reads data from all 4 (or 8, or whatever it is) locations simultaneously. It also simultaneously reads the tag fieds for those locations which tells us what physical address they're for. Finally, after both those 4-8 data reads and the TLB access are complete, we know the right physical address; we check which of the 4-8 tags match that address, if any. If we loaded from the right spot in our set, we use that. Otherwise we report a cache miss. This is all doing a lot of extra work and is quite power-hungry but it reduces latency substantially for what turns out to be one of the most critical paths for most programs, so it's usually a good trade-off.

Only one problem with this: that doesn't work for stores. For loads, we can speculatively fetch data from 8 different locations and select the right one late. But for stores we certainly can't just start writing that data to 8 random locations, especially since _none_ of them might actually correspond to the location we wanted to write to in the first place! Stores have to wait until the address translation is done and we've actually confirmed the right location is present in the cache before we can write anything. So for stores it has to be translate address _then_ access the data array. This different timing between the two poses problems if you want to build hardware for this.

Intels older CPUs kind of brute-forced their way around this problem. For example, in the original Pentium (1993), the solution was to effectively clock the cache data array at twice the frequency (not really, it used both rising and falling edges of the same clock signal as the core, but it's functionally equivalent). The first half of each CPU cycle was reserved for the L1 read access (overlapped with TLB access), the second half (after TLB/tag access was done, which completed in the first half) was used for writes (stores).

This worked, but turned out to be a problem for hitting higher clock rates soon after. So starting with the Pentium MMX they redesigned (see https://smtnet.com/library/files/upload/pentium-microarchitecture.pdf) that part of the memory access pipeline to add.. store buffers (their somewhat clunky terminology is "cache store hit buffers"; page 3). The idea being that during the cycle scheduled for a store, we need to wait for the address translation to finish first, which is only done near the end of the cycle. But we _can_ access the cache data array, so the solution is to keep buffer space for a previous store, and while we're waiting for the result of our address translation to come up, we do the write for an earlier store from the store buffer instead! (And simultaneously put our new store into the buffer slot.) Cycles without a memory access can use the opportunity to drain the buffered store early. (At the time there was no SFENCE or similar in x86 so the semantics of when these would actually get drained were murky.) Many in-order cores do something similar, for similar reasons. The end result is that stores again end up taking delayed effect from when they happen in program order, though for very different reasons than in the out-of-order scenario.

What both example have in common is that these buffers ultimately exist to solve other problems that come with other important architectural features, and the influence they have on memory ordering is a side effect.

This got really long but I hope it clears things up.

Thanks a lot for the informative answer. Really appreciate that!