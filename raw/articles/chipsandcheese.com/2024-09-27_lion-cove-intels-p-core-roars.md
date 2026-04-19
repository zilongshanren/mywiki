---
title: 'Lion Cove: Intel’s P-Core Roars'
url: https://chipsandcheese.com/p/lion-cove-intels-p-core-roars
author: Chester Lam
published: '2024-09-27'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

Intel’s mobile CPUs have undergone massive changes over the past couple generations as Intel defends its laptop market against AMD, Qualcomm, and to a lesser extent Apple. Meteor Lake adopted aggressive chiplet design with separate compute, GPU, SOC, and IO extender tiles. Lunar Lake switches things up again, putting all compute on one tile while a second “platform controller” tile deals strictly with low speed IO.

Amidst this whirlwind of change, Intel’s performance oriented P-Cores have remained a constant. P-Cores aim to deliver maximum per-thread performance, an important metric in client designs where responsiveness is vital and many programs don’t scale across many cores. Lion Cove is Intel’s latest and greatest high performance architecture, and fills the P-Core role in Lunar Lake. While its goals have remained constant, its design has very much not. Compared to Redwood Cove P-Cores in the previous generation Meteor Lake, Lion Cove has been overhauled with both performance and energy efficiency in mind.

Here I’ll be looking at Lion Cove as implemented in the Core Ultra 7 258V.

Acknowledgments

We’d like to thank Asus for kindly sampling us with a Zenbook S 14 UX5406SA test system. Without their help, a look at Intel’s latest mobile chip wouldn’t have been possible.

System Architecture

Lion Cove cores sit on a ring bus interconnect, a familiar design that traces its roots back to Sandy Bridge in 2011. Over time though, ring bus agents have come and gone. P-Cores got to share the ring bus with E-Core clusters in 2021’s Alder Lake. Meteor Lake saw Intel kick the iGPU off the ring bus. Lunar Lake gives E-Cores the boot, leaving just the P-Cores and their associated L3 slices on the ring bus.

L3 slices on Lunar Lake continue to have 3 MB of capacity just as they did in Meteor Lake. However, Lunar Lake caps out at four cores and four L3 slices, dropping L3 capacity in half. In exchange, Intel is dealing with a smaller and simpler ring bus. Possibly because of this, Lunar Lake’s L3 latency has dramatically improved compared to Meteor Lake. It’s not as good as AMD, which had a very strong L3 design since early Zen generations. But AMD’s L3 latency advantage isn’t as drastic as it was before.

DRAM latency also improves. Lunar Lake’s new chiplet design places the memory controller and CPU cores on the same tile, so memory access no longer have to traverse a cross-die link. The LPDDR5X DRAM chips themselves have been brought on-package too.

Like Meteor Lake, Lunar Lake complicates DRAM latency measurements because the memory controller likes to stay in a low power state if there isn’t enough DRAM traffic. A plain memory latency test sees about 131.4 ns of DRAM latency. Creating some artificial bandwidth load drops latency to 112.4 ns. AMD’s Strix Point had 128 ns of DRAM latency for comparison, with margin-of-error differences under moderate bandwidth load. While DRAM latency with LPDDR5(x) will never match desktop DDR5, Lunar Lake’s DRAM latency is good for a mobile platform.

Even with on-package memory, DRAM accesses are power hungry. Lunar Lake tackles this with a 8 MB memory side cache. 8 MB is less capacity than Lion Cove’s 12 MB cache, but that’s not a huge issue because the memory side cache is aimed towards blocks like the NPU or display engine that don’t have large caches of their own. Because improving CPU performance isn’t the main goal, the memory side cache doesn’t have great latency. In fact, estimating its latency is difficult because test sizes contained within the memory side cache will inevitably see a significant number of L3 hits. In those test ranges, latency is roughly 30 ns from a P-Core.

DRAM bandwidth is quite impressive on Lunar Lake. Going to LPDDR5X-8533 brings noticeable improvements over Meteor Lake’s LPDDR5-7467. Four Lion Cove cores alone can pull more bandwidth than all of Meteor Lake’s cores.

L3 bandwidth is less impressive, though that hasn’t been Intel’s strong point for years. AMD Strix Point’s four high performance Zen 5 cores can pull over 600 GB/s from L3 with reads alone. To Intel’s credit, quad core L3 bandwidth at least doesn’t regress compared to Redwood Cove. But L3 isn’t the focus of recent Intel designs. Rather, the company uses larger L2 caches to make their cores less sensitive to L3 performance. Having a slow cache is fine if you don’t hit it often.

A Mid-Level Cache For Your Mid-Level Cache

And Intel cores have trended towards bigger L2 caches. But increasing cache capacity isn’t so simple because larger caches often come with higher latency. Intel’s L2, which the company often refers to a mid-level cache, isn’t immune.

Lion Cove counters this by adding a mid-level cache for the mid-level cache so you can avoid mid-level cache latency if you hit in the faster mid-level cache. Intel calls this new mid-level cache a L1, and renames the first level cache to L0. The new “L1” has 192 KB of capacity with 9 cycles of load-to-use latency.

I disagree with Intel’s terminology change. While first level cache latency does drop from five to four cycles, it merely matches Zen 5’s L1D in capacity and latency terms. The 192 KB “L1” has much higher latency than L1D caches in competing cores. You could really stretch things by comparing to a Cortex A72 in Graviton 1. That has 1.75 ns of L1D latency, which is in the same ballpark as the 1.88 ns of measured latency on Lion Cove’s 192 KB L1. But Cortex A72 and Lion Cove don’t have comparable design goals.

I’m going to be stubborn and call the 48 KB first level cache a “L1”, and the 192 KB cache a “L1.5” from now on. Lion Cove’s L1.5 has better bandwidth than Redwood Cove’s L2, though not with a read-only pattern. I needed a read-modify-write pattern to sustain more than 32 bytes per cycle, so I think it’s only a minor improvement. The L1.5’s bandwidth is nowhere near that of the 48 KB L1D on either Lion Cove or Redwood Cove.

That’s a lot of cache levels

But I don’t think bandwidth is Intel’s main goal with the new L1.5. Rather, it looks aimed at reducing average L1D miss latency. Catching some L1D misses and servicing them at 9 cycle latency helps of course. Beyond that, the L1.5 lets Intel make a bigger L2, reducing latency for more difficult accesses by servicing more of them within full speed core-private caches. Going from 2 MB on Redwood Cove to 2.5 MB on Lion Cove might not feel like much. However, Intel’s slides show Lion Cove can support up to 3 MB of L2 capacity. That’s as much capacity as last level caches on some old Intel dual core chips like the Core i5-3317U.

Possibly because L1.5 absorbs a good chunk of L1D miss traffic, Intel didn’t focus as much on L2 bandwidth. Lion Cove’s L2 Bandwidth tops out at 32 bytes per cycle, regardless of whether I’m using a read-only pattern or a read-modify-write one. Intel’s focus is really about giving the L2 more capacity, rather than providing higher L2 bandwidth.

If workloads spill out of L2, L3 bandwidth is quite mediocre. L3 read bandwidth from a single Lion Cove core regresses to just over 10 bytes per cycle, down from 16 bytes per cycle on Redwood Cove. Lion Cove enjoys lower L3 latency and a larger L2 miss queue (80 entries, compared to 64 on Redwood Cove). It’s a combination that should give a single core access to more L3 bandwidth, but that doesn’t show through in testing. A read-modify-write pattern achieves higher bandwidth, at 17-18 bytes per cycle.

Neither figure approaches Zen 5, which goes right to the limit of its 32 byte per cycle L2 to L3 interface. A read-modify-write pattern exercises the 32 byte per cycle link in the other direction, bringing total L3 throughput to 64 bytes per cycle. The Ryzen AI 9 HX 370 can run its Zen 5 cores at up to 5.15 GHz compared to 4.8 GHz on the Core Ultra 7 258V. AMD’s clock speed advantage further inflates its L3 bandwidth advantage.

Out-of-Order Execution Engine

One of those sweeping changes applies to the schedulers, which have been reorganized with a view towards scalability. Since the Pentium Pro from 1995, Intel has served both integer and FP/vector operations with a unified scheduler. Scaling a large unified scheduler can be difficult, so Intel split the scheduler over time. Skylake put memory address generation ops on a separate scheduler. Sunny Cove split the memory scheduler, and Golden Cove revised the memory scheduler split.

Lion Cove finally splits the unified math scheduler into separate ones for integer and floating point/vector ops. Intel also split register renaming for floating point and integer operations. That’s not visible from software, but it does suggest Intel’s core is now laid out a lot like AMD’s Zen. Both do register renaming separately for integer and vector operations, and use separate schedulers for those operations.

After the split, Lion Cove’s vector and integer schedulers each have similar capacity to Redwood Cove’s unified math scheduler. Combined integer and vector scheduling capacity is simply massive with over 200 available entries. The memory schedulers are no joke either. In every category, Lion Cove’s scheduling capacity beats Zen 5’s.

Besides big schedulers, Intel uses non-scheduling queues to let Lion Cove track more more operations waiting for an execution unit. If a scheduler fills up, the renamer can place micro-ops into an associated non-scheduling queue instead of stalling. Micro-ops sitting in a non-scheduling queue won’t be considered for execution, but can enter a scheduler later when entries become available. AMD’s Zen line and Intel’s own E-Core line have used non-scheduling queues over the years, and it’s great to see the Intel adopt it on P-Cores too.

Lion Cove’s schedulers feed a massive 18 execution ports, up from 12 in Redwood Cove. Much of that execution port count increase comes from moving FP/vector units off the integer scheduler. Execution capacity for common instruction categories hasn’t increased that much. Scalar integer adds get an extra ALU port. A third store address port helps discover memory dependencies faster, though sustained store throughput is limited two per cycle. FP/vector operations are handled by four ports instead of three.

Lion Cove’s FP/vector execution setup is curious too, because now it very closely resembles AMD’s going back to Zen 1. AMD and Intel now handle FP/vector execution with four pipes. Two deal with floating point multiplies and multiply-adds, while two others handle FP adds. Vector integer adds can go to any of the four ports. Unlike Zen 5, Lion Cove maintains single cycle vector integer add latency even when the schedulers are full and micro-ops are woken up by single cycle ops (other vector integer adds). In AMD’s favor, cores from the Zen line don’t suffer a significant penalty when a floating point multiply with normalized inputs generates a denormal output. Such an event costs 132 cycles on Lion Cove, which is worse than the 124 cycles I saw on Redwood Cove. Skymont behaves like Zen, and doesn’t suffer a significant penalty for denormal results.

Micro-ops leave the schedulers after execution units generate their speculative results. But all the way until they’re retired, micro-ops require entries in various structures like the reorder buffer, register files, and load/store queues. Those queues, buffers, and register files ensure the core can correctly produce results as if instructions were executed in program order. Lion Cove grows those structures, letting the core keep more instructions in-flight. In turn, that makes the core more resilient against long latency events like cache misses. But not every structure got equal treatment.

Lion Cove’s ROB sees a 12.5% capacity increase. It’s a noticeable improvement, if nowhere near the 45% or 40% ROB size growth that Golden Cove or Zen 5 got over their respective previous generations. However, some of Lion Cove’s supporting resources are much bigger than the corresponding ones in Golden Cove/Redwood Cove. Lion Cove can have over 40% more branches in flight. The floating point register file also sees substantial growth, likely to keep pace with increased floating point scheduling and non-scheduling queue capacity.

Since Skylake, Intel allocates both AVX-512 mask registers and MMX/x87 registers out of the same register file. I can’t test reordering capacity for mask registers because Intel stopped supporting AVX-512 on consumer chips. But testing with MMX registers shows a small increase in rename capacity over Redwood Cove. Intel may still be making AVX-512 oriented improvements, and some of those effects are visible even on client cores.

Improvements elsewhere are minor. The integer register file grew by less than a dozen entries and still doesn’t cover ROB capacity well. Intel added a few store queue entries too. As far as I can tell, the load queue either didn’t get any entries added, or even had a few removed.

Load/Store Unit

A CPU’s load/store unit often occupies plenty of die area, and is responsible for ensuring memory accesses appear to execute in program order. That feels challenging with a lot of memory accesses in-flight, because a load’s address has to be checked against all prior store addresses. If they overlap, the load has to read data from the store queue instead of the data cache.

Lion Cove maintains Golden Cove’s zero latency, two-per-cycle store forwarding capability for exact address matches. Latency slightly regresses if the load is contained within a store but addresses don’t match exactly, but that shouldn’t be common unless you’re dealing with network packets or something. Partial overlaps are handled with much higher latency, and are likely handled by blocking the load until the store commits, after which the load can get data from the L1D cache. If so, Zen 5 has a much shorter pipeline from store address generation to retirement.

Independent accesses can face delays too depending on how they interact with the underlying data cache. Tracking cached data at the byte level would be far too expensive, so caches maintain tags and state at the cache line granularity. That’s typically 64 bytes. Intel’s architectures do worse when an access crosses a 64 byte cache line boundary, taking an extra cycle for a store. Loads do a bit better probably because the data cache has more load ports and can absorb the extra bandwidth needed for a misaligned access. But misaligned loads still aren’t handled as fast as on AMD.

Address Translation

Programs operate on virtual addresses, which have to be translated to physical addresses that correspond to locations in DRAM. The load/store unit has to carry out these translations according to page tables set up by the operating system. Page tables are actually multi-level structures, so CPUs cache frequently used address translations in translation lookaside buffers (TLBs). For generations Intel has used a very complex TLB setup with separate TLBs for different page sizes and access types.

Who uses 1 GB pages anyway

Lion Cove brings the 4K page load-only DTLB’s capacity up to 128 entries, from 96 in Redwood Cove. None of the other TLB sizes have changed. That should reduce average memory access latency across a wide variety of client programs, because 4K pages are most commonly used there. However, AMD’s Zen 5 and even Zen 4 can cache far more address translations in a L2 TLB. AMD’s cores therefore have a better chance of avoiding expensive page table walks.

As on Redwood Cove, getting a translation from Lion Cove’s L2 TLB adds 7 extra cycles of latency. That penalty also matches Zen 5.

Rename and Allocate: Feeding the Backend

The rename and allocate stage allocates micro-ops into backend structures, while carrying out register renaming and other optimizations to break false dependencies. Register renaming is an inherently serial task because which physical registers correspond to an instruction’s inputs depends on how prior renames have been carried out. Probably for that reason, the renamer is often the narrowest part of a core’s pipeline. AMD and Intel’s latest cores are no exception.

Lion Cove widens the renamer to handle 8 micro-ops per cycle, up from 6 in Redwood Cove. That makes Lion Cove an 8-wide core overall, matching AMD’s Zen 5. Intel’s renamer received some impressive capabilities in Golden Cove, including the ability to execute up to 6 dependent adds with small immediates per cycle. That’s carried forward to Lion Cove, though not widened to match the renamer’s full width.

Other easier optimizations like move elimination and zeroing idiom recognition can be carried out at or near the renamer’s full width. Zen 5 is no slouch for those, but often can’t carry out those optimizations at eight per cycle. I’m not sure if it makes a big performance difference, but it does show Intel’s focus on building a very powerful rename stage.

Frontend Fetch and Decode

The frontend has to feed the rename stage by bringing instructions into the core and decoding them into micro-ops. Lion Cove’s frontend uses a similar strategy to prior P-Cores. A conventional instruction cache feeds a decoder, which both sends micro-ops downstream and fills them into a micro-op cache. Lion Cove widens the decoder to handle eight instructions per cycle, up from six in Redwood Cove. Micro-op cache capacity increases to 5250 micro-ops, up from 4096 on Redwood Cove. Bandwidth from the micro-op cache went up to, from eight to 12 micro-ops per cycle.

Unlike AMD Zen 5’s clustered decoder, all eight decode slots on Lion Cove can serve a single thread. Lion Cove can therefore sustain eight instructions per cycle as long as code fits within the 64 KB instruction cache. After that, code fetch throughput from L2 is limited to 16 bytes per cycle. L3 code fetch bandwidth is similar to data-side bandwidth, so Lion Cove’s branch predictor can run very far ahead of fetch to hide even L2 miss latency. The same doesn’t apply to Zen 5, which has lower code fetch throughput from L3.

Longer instructions can run into cache bandwidth bottlenecks. With longer 8-byte NOPs, Lion Cove can maintain 8 instructions per cycle as long as code fits within the micro-op cache. Strangely, throughput drops well before the test should spill out of the micro-op cache. The 16 KB data point for example would correspond to 2048 NOPs, which is well within the micro-op cache’s 5250 entry capacity. I saw the same behavior on Redwood Cove.

Once the test spills into the L1 instruction cache, fetch bandwidth drops to just over 32 bytes per cycle. And once it gets into L2, Lion Cove can sustain 16 instruction bytes per cycle.

Branch Predictor: Directing the Core

Instruction fetch is steered by the branch predictor, which plays an important role in improving both performance and power efficiency. Everyone tends to improve their branch predictors with every generation, and Lion Cove does so too. A single branch sees little to no penalty (evidence of a mispredicts) even when throwing a 12K long random pattern at it.

Intel definitely made some changes to direction predictor, but the scope of this change seems to be narrow. Lion Cove performance monitoring events haven’t been documented yet, but Intel does guarantee some architectural performance monitoring events will work across different generations. Events for retired branches and retired mispredicted branches are among those events.

If I look at the geometric mean of branch prediction accuracy across all SPEC CPU2017 workloads, Redwood Cove and Lion Cove differ by well under 0.1%. Lion Cove has a tweaked branch predictor for sure, but I’m not seeing it move the needle in terms of accuracy. AMD’s Zen 5 still does a bit better overall, and can gain an especially significant edge with difficult workloads like 541.leela and 541.xz. There, AMD’s latest branch predictor sees a 11.4% and 3.84% reduction in mispredicts per instruction compared to Intel’s. Within SPEC CPU2017’s floating point suite, Lion Cove struggles in 526.blender.

Branch predictor speed matters too, because the point of a branch predictor is to minimize delays from control flow dependencies. Intel continues to use a triple level branch target buffer (BTB) setup to cache frequently used branch targets, but each level has been tweaked compared to Redwood Cove. To start, both architectures can handle two taken branches per cycle likely by unrolling small loops within the micro-op queue. Lion Cove and Redwood Cove both have a 192 entry micro-op queue, but perhaps Lion Cove can’t track as many branches within it.

Next, a L1 BTB is fast enough to do zero bubble branching, which means handling taken branches with just a single cycle of latency. On Lion Cove, the L1 BTB appears to cover 2 KB of code, regardless of how many branches are in it. Redwood Cove can track up to 128 branches in its L1 BTB, mostly independently of branch spacing.

Then there’s a 6K entry BTB on both cores with 2 cycle latency, followed by a 12K entry BTB. That large last level BTB has 3-4 cycles of latency on Lion Cove, and is difficult to characterize on Redwood Cove.

Returns are predicted via a return stack, which has grown to 24 entries from 20 in Redwood Cove. Prediction latency is better when the tested call depth doesn’t exceed 12, so I suspect this is a two level structure. For comparison AMD has opted for a larger 52 entry return stack on Zen 5, which is duplicated per-thread for a total of 104 entries.

Capacity isn’t the only factor, and I have to point out how fast Intel’s return prediction is. Lion Cove and Redwood Cove can handle a call+return pair every cycle. AMD’s Zen 5 takes four cycles to do the same, or an average of two cycles per branch. Lion Cove trades some speed for a few extra return stack entries, and averages one branch per cycle up to a call depth of 24. AMD may be faster for direct branches thanks to its giant 1024 entry zero-bubble BTB. But Intel is faster for other categories of branches like calls and returns.

Core Summary

All those caches help feed Lion Cove’s core, which has huge upgrades over Redwood Cove. The pipeline is wider, structures are larger, and a reorganized out-of-order engine helps Intel achieve higher scheduling capacity.

Much like Redwood Cove, Lion Cove is a wide and high clocked out-of-order design. But it’s easily the biggest change to Intel’s performance oriented architecture since Golden Cove. After Redwood Cove’s minor changes over Raptor Cove, and Raptor Cove barely doing anything over Golden Cove, it’s great to see Lion Cove’s sweeping changes.

Intel must have put a lot of effort into Lion Cove’s design. Compared to Redwood Cove, Lion Cove posts 23.2% and 15.8% gains in SPEC CPU2017’s integer and floating point suites, respectively. Against AMD’s Strix Point, single threaded performance in SPEC is well within margin of error. It’s an notable achievement for Intel’s newest P-Core architecture because Lunar Lake feeds its P-Cores with less L3 cache than either Meteor Lake or Strix Point. A desktop CPU like the Ryzen 9 7950X3D only stays 12% and 10.8% ahead in the integer and floating point suites respectively. Getting that close to a desktop core, even a last generation one, is also a good showing.

Results here aren’t comparable to ones in the prior article because I re-ran with -O3 -mtune=native -march=native to let GCC use whatever instruction set extensions the CPU supports. They also aren’t comparable to Intel’s performance estimates, which took a variety of workloads into account at fixed frequencies.

Performance gains will vary across different workloads as SPEC CPU2017 subscores show. But there’s little doubt that Intel succeeded in delivering a generational performance uplift with Lion Cove.

Final Words

P-Cores have been Intel’s bread and butter long before the company started calling them P-Cores. Progress with Intel’s performance oriented cores hasn’t always been fast. Redwood Cove was only a slight tweak over Golden Cove. Skylake filled out five generations of Intel designs the same architecture. Going back further, Intel used the P6 architecture on the Pentium Pro, Pentium II, and Pentium III with just minor tweaks and clock speed increases in between.

Lion Cove is a much improved architecture compared to Redwood Cove, and shows Intel still has potent engineering muscle despite recent setbacks. Traditionally Intel delivered significant architecture changes during a “tock” in a tick-tock cycle. That reduces risk by separately handling process node and architecture changes. Lunar Lake not only combines a new architecture with a move to a new node, but also drops system level changes on top. At a time when Intel’s facing increased pressure from all sides, a move like Lunar Lake is a sign that Intel can adapt and survive.

Intel’s upcoming Arrow Lake desktop CPU will let Lion Cove stretch its legs with more cache and a larger power budget. Lower latency DDR5 should improve performance even further. After seeing Lion Cove perform well in a mobile form factor, I’m optimistic about what the same architecture can do on desktop. Recently Intel has been sitting on a rather unstable foundation with Raptor Lake, and Arrow Lake’s release will be a great time to put the company’s high performance chips back on stable footing.

Again, we would like to thank ASUS for sending us over a Zenbook S 14 for review and if you like our articles and journalism, and you want to support us in our endeavors, then consider heading over to our Patreon or our PayPal if you want to toss a few bucks our way. If you would like to talk with the Chips and Cheese staff and the people behind the scenes, then consider joining our Discord.

I remember there being notes here about how slow the runs of cactuBSSN were and maybe on the Skymont report as well. It seems the problem might not be compiler or hardware related but a weird regression in mmap in the Linux kernel since 2023 that was recently resolved.

It would be interesting for a follow up article about the technical reasons why the natural idea of aligning things caused a regression and more testing.

I remember there being notes here about how slow the runs of cactuBSSN were and maybe on the Skymont report as well. It seems the problem might not be compiler or hardware related but a weird regression in mmap in the Linux kernel since 2023 that was recently resolved.

https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=d4148aeab412432bf928f311eca8a2ba52bb05df

It would be interesting for a follow up article about the technical reasons why the natural idea of aligning things caused a regression and more testing.

Great review but doesn't seem like the desktop implementation is gonna perform as expected for some reason