---
title: 'Golden Cove’s Vector Register File: Checking with Official (SPR) Data'
url: https://chipsandcheese.com/p/golden-coves-vector-register-file-checking-with-official-spr-data
author: Chester Lam
published: '2023-01-15'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

With AVX-512 enabled on Golden Cove, we measured 210 renames for 512-bit vector registers, and 295 renames for 256-bit ones. If 32 registers are used to hold architectural state, then there should be 327 total vector registers. 242 of those would be 512 bits wide.

Our estimates land in the same ballpark. They are enough to demonstrate that only a subset of Intel’s vector registers are 512 bits wide. However, we overestimated the absolute numbers by a bit. We arrived at that estimate by taking the measured speculative register file capacity, and assuming the core would have to use 32 vector registers to hold architectural state. That’s because AVX-512 provides 32 architectural vector registers. If there’s an exception, the core has to be able to provide the correct values for all of those registers. Obviously, one way to do that is to save known-good values for all the registers in the physical register file.

Evidently, Golden Cove is able to avoid consuming 32 register file entries to hold architectural state. That lets it use those registers to keep more instructions in flight, meaning that our test sees more of the actual register file capacity than we expect. Here’s another way of looking at the data.

I’m not sure what mechanism Intel is using to achieve this. One guess is that Intel can free up a register used to hold known-good state if it knows the value is zero. It looks like the FP/vector registers are zeroed when an application is first started, and of course remain zero unless the program writes to them. Our test only writes to a subset of the architectural SSE/AVX/AVX-512 registers, meaning that quite a few of them remain zero. Specifically, it hits XMM/YMM/ZMM registers 1 through 5, inclusive.

We already found that Intel can avoid allocating a register for instructions that have to produce a result of zero. Examples include XOR-ing a register with itself, or subtracting a register with itself. Those observations applied to the speculative portion of the register file, but it’s easy to them applying to the non-speculative portion too. For example, each entry in the retired register alias table could have a bit indicating whether the register was zeroed.

Testing on server Ice Lake because I have easy access to it

While testing on server Ice Lake suggests Intel’s mechanism isn’t nearly that sophisticated. Instead, the core simply remembers whether the upper set of ZMM registers are in use. If you use any of the extra registers introduced with AVX-512 – that is, ZMM16 through 31, Ice Lake reserves another 16 registers to hold known-good state. It doesn’t matter if you touch one of them or all of them. Golden Cove is Ice Lake’s successor, and could use a similar mechanism.

Reading results is also complicated. We’re using Henry Wong’s methodology for measuring OoO structure sizes. Basically, that means putting filler instructions that use some kind of OoO resource between two pointer chasing loads that miss cache. If the CPU’s OoO structures are large enough to track all the filler instructions, the two loads can proceed in parallel. Otherwise, the rename stage stalls once the OoO resource is exhausted. That means the second load can’t overlap the first, because the second load can’t get into the OoO engine and so it can’t extract instruction level parallelism. That surfaces as a spike in the time it takes to complete both loads.

Though sometimes, the architecture in question isn’t perfect at reclaiming registers. That results in a noisy or gradual curve up, rather than a perfect spike up. We’re trying to pick the last point that we think the CPU is able to parallelize the two loads at least some of the time, but that’s not an exact science. Depending on which point we pick, we could be off by a couple entries.

What About AMD?

The existing test that used 5 ZMM registers showed 154 entries available in the speculative portion of Zen 4’s vector register file. AMD states that the register file has 192 entries, meaning 38 are used to hold non-speculative state. Therefore, Zen 4 does not employ the same register-saving optimization as Ice Lake.

On the bright side, at least modern AMD cores don’t permanently reserve vector register file entries to hold architectural state for both SMT threads, as Bulldozer did. In that respect, AMD is a match for Intel. Also, does that mean a Bulldozer article is in progress? Hmm…

What About Other Structures?

In December 2021, we published our look into Golden Cove. Based on measurements, we said that Intel did not increase the integer register file capacity from Sunny Cove. Official SPR slides said they added eight integer registers. That brings the number of integer registers from 280 to 288, for a tiny 2.8% increase in entry count.

Golden Cove’s integer register file doesn’t look any bigger than Sunny Cove’s. We also checked with instructions that don’t set flags (move immediate value, and bitwise not), and the results don’t differ.

Our measurement of speculative register file capacity didn’t detect this. What that means is that the extra registers did not allow the OoO engine to see any farther in terms of instructions that write to integer registers. Thus, the tiny increase in integer register file capacity was counteracted by having to use those registers to hold some sort of architectural state.

Sunny Cove uses 32 registers to hold architectural state. That corresponds to 16 integer registers across the two SMT threads. Eight extra registers on Golden Cove means that each SMT thread is using four integer registers to do something else. Another observation is that Sunny Cove and Golden Cove save integer register state for both SMT threads, even if one thread is active. That contrasts with their behavior for vector registers.

In any case, the original comments on Golden Cove hold. Even if the CPU could use those extra eight registers to enable higher reordering capacity, the increase is absolutely negligible. It’s not hard to find applications where more than half the instructions write to an integer register. 248 + 8 would be 256, or just half of reorder buffer capacity. We previously wrote that Golden Cove would have a good chance of running out of integer registers before running out of ROB capacity, and that still holds.

Load Queue?

Another discrepancy between microbenchmark figures and published results is the load queue. The load queue is responsible for tracking loads in flight, until the CPU can be certain their results are good and can retire them (commit their results). Intel claims the load queue has 240 entries in SPR. I assume the same applies to Golden Cove. We measured 192 entries.

I think what’s going on here is that the definition of the load buffer or load queue isn’t very clear. What we’re measuring is how many loads can be in-flight before the OoO engine has to stop accepting more instructions from the frontend. Prior to Golden Cove and Sapphire Rapids, our measurements have been consistent with Intel’s published numbers. Perhaps Intel is doing something different, and the out-of-order backend has to stall the frontend after fewer than 240 loads are in flight.

Curiously, the opposite applies to AMD’s Zen architecture. AMD’s slides claim Zen 1 has a 72 entry load queue, but measurements show Zen’s backend can track 116 in-flight loads. Subsequent Zen generations show similar behavior, with Zen 4 increasing that figure to 136. One guess is that Zen has some kind of internal load tracking structure with 72 entries, but is able to de-allocate loads from that structure before retirement.

In any case, our measurements reflect how many loads the CPU’s backend can keep in-flight before it has to tell the frontend to hold up and stop feeding it more instructions. Manufacturers might have a different definition of what a load queue is.

Final Words

AMD and Intel have been steadily increasing reordering capacity in order to cope with higher latency caches. This is especially apparent with recent Intel CPUs. Sunny Cove grew ROB size to 352 entries, while Golden Cove pushes that figure to 512. Other core structures have to grow as well to keep the core balanced. Otherwise, that ROB capacity increase won’t do much because something else will fill first. Register files are heavily used OoO structures, and Intel has obviously added more entries there.

Intel’s efforts go further, they’re making optimizations to efficiently use those entries too. AVX-512 makes that especially important, because it defines 32 architectural vector registers instead of 16. More registers let the compiler or assembly programmer keep more values in registers in case they need quick access to them later. Though they can also be a downside, because if a section of code doesn’t have a lot of “hot” values, the core ends up wasting register file entries that could have been used to let the OoO engine see further.

To compensate for that, Intel only reserves registers for the AVX-512 state when the extra registers are in use. This is a pretty coarse-grained toggle, since using even one of the upper 16 registers will cause all 16 of them to be given space in the physical register file. However, it’s a lot simpler than extending the retired register alias table to track which registers are zeroed. AMD’s setup is simpler still, with no such mode switching. On Zen 4, all 32 vector registers are apparently given space in the register file, regardless of whether they’re being used.

Finally, the main takeaway here is that estimating total register file capacity is not an exact science. CPUs can use all kinds of optimizations to reduce the number of register file entries needed to hold a known-good state. Conversely, they can be inefficient at reclaiming registers when they’re no longer needed. That would result in the test seeing less speculative renaming capacity than what the architecture should theoretically be able to provide. Finally, some register file entries can be used by microcode for temporary scratch storage, though I assume those cases are rare. We’re doing our best to determine register file capacity through testing, and our estimates should not be far off. Though they shouldn’t be seen as perfect, exact numbers. Reverse engineering hardware by looking at how it performs though software is hard. And that applies to all kinds of structures in a CPU’s backend.

When it comes to large differences like not having a split between 512-bit and 256-bit capable registers, these are easily visible. In that respect, we’re glad that our testing was able to showcase an AVX-512 optimization that Intel implemented on both Golden Cove and Sapphire Rapids.

If you like our articles and journalism and you want to support us in our endeavors then consider heading over to our Patreon or our PayPal if you want to toss a few bucks our way or if you would like to talk with the Chips and Cheese staff and the people behind the scenes then consider joining our Discord.