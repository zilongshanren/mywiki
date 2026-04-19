---
title: 'Skymont: Intel’s E-Cores reach for the Sky'
url: https://chipsandcheese.com/p/skymont-intels-e-cores-reach-for-the-sky
author: Chester Lam
published: '2024-10-03'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

The 2020s were a fun time for Intel’s Atom line, which went from an afterthought to playing a major role across Intel’s high performance client offerings. Intel’s latest mobile chip, codenamed Lunar Lake, sees Intel’s high performance P-Cores ditch SMT. With P-Cores focusing even more on single threaded performance, E-Cores will play an even more prominent role in boosting multithreaded performance. With Intel facing stronger competition than ever in the laptop scene, power efficiency is also important. Skymont is Intel’s latest E-Core architecture, and replaces Crestmont in the outgoing Meteor Lake mobile chips.

In Lunar Lake, Skymont serves both of those goals. Meteor Lake’s two levels of E-Cores have been combined into one in Lunar Lake, designed both to boost multithreaded performance and handle low priority background tasks. Meteor Lake boosted multithreaded performance with Crestmont E-Cores attached to the ring bus and L3. Two other low power Crestmont cores sat on a low power island to handle background tasks and let the higher performance cores power down more often.

Lunar Lake’s quad core Skymont cluster sits on a low power island, letting it handle light background tasks without waking the P-Cores. But it’s also on the same TSMC N3B process node as the P-Cores, and gets an improved cache hierarchy compared to Meteor Lake’s rather weak low power E-Cores. That combination lets Skymont serve both roles with a single core variant. Intel evidently decided more core levels wasn’t a good thing. They also decided just four E-Cores would be adequate, so Skymont has some big shoes to fill.

Core Overview

Skymont is a substantial step over its predecessor, Crestmont. At a high level, it’s an eight-wide out-of-order core. In many areas, it’s not far off Intel’s P-Cores or latest members of AMD’s Zen line. Skymont of course can’t run at the same clock speeds and can’t compete in absolute performance. However, it’s a good showcase of how sophisticated a density optimized core can get on a modern process node.

Keep in mind these block diagrams are an approximation. Digging into a distributed scheduler layout is a nightmare and very error prone

Digging deeper, Skymont is a clear relative of Crestmont. Both use a distributed scheduler layout with a lot of ports, and have distinguishing features like a clustered frontend. However, the scope of Skymont’s changes is pretty huge.

Impressively, Intel was able to deliver Skymont at the same time as Lion Cove, which also delivers large changes over its predecessor. Intel fighting hard to retain the laptop market that it nearly dominated a decade ago, and Lunar Lake is the result of a big company steaming ahead with all boilers lit.

Frontend: Branch Prediction

Branch prediction accuracy affects both performance and power, because wasted work costs both power and core resources downstream. When faced with crazy long random patterns, Skymont doesn’t do quite as well as Intel or AMD’s latest high performance cores. However, it’s a clear step ahead of Crestmont.

If there are a few branches in play, Skymont can deal with a longer repeating random pattern. With 512 branches each going through a different random pattern, Skymont falls apart after the random pattern is longer than 48, a good improvement over 16 on Crestmont. Perhaps Intel has given Skymont’s predictor a lot more storage for branch history.

Getting a branch’s direction right is only one part of the picture. The point of a branch predictor is to go fast and minimize delays from control flow dependencies. To do so, modern branch predictor can run far ahead of instruction fetch, queueing up cache miss requests and using memory level parallelism to mitigate L2 or even L3 latency. Caching branch targets is crucial because it lets the predictor tell where a branch goes without waiting for it to arrive at the core. Skymont can cache up to 8K branch targets in its last level branch target buffer.

Crestmont for comparison has a 6K entry last level BTB. Both E-Cores have smaller BTBs than recent high performance cores. Golden Cove has a 12K entry BTB, and AMD’s Zen 5 has a massive 24K BTB entries. Still, 8K BTB entries is nothing to scoff at. It’s more entries than older high performance cores like Sunny Cove or Zen 2.

Cache speed matters too, because taken branch latency can reduce frontend throughput. Skymont and Crestmont both have a first level 1024 entry BTB capable of zero bubble taken branches (single cycle latency). It’s faster than the 3-4 cycle latency L2 BTB, but can’t do two taken branches per cycle like Intel and AMD’s latest cores.

Returns are predicted via a return stack, because they usually go back to a corresponding call site. Skymont has a very deep 128 entry return stack, a feature inherited from Crestmont. Calls and returns have to be spaced by at least one cacheline to utilize this return stack, which complicated microbenchmarking but shouldn’t affect typical applications.

For comparison, AMD’s Zen 5 has 2×52 entry return stacks, one for each thread. Skymont’s P-Core companion, Lion Cove, has a 24 entry return stack.

In SPEC CPU2017’s workloads, Skymont posts a decent improvement in branch prediction accuracy over its predecessor. The geometric mean of branch prediction accuracy across all subtests goes up from 98.09% to 98.21%. It may seem like a minor step forward, but that’s because many of SPEC CPU2017’s workloads were easy to predict in the first place. Difficult benchmarks like 541.leela, 505.mcf, and 526.blender saw 4.83%, 5%, and 13.58% reductions in branch MPKI respectively.

Frontend: Fetch and Decode

Leapfrogging fetch and decode clusters have been a distinguishing feature of Intel’s E-Core line ever since Tremont. Skymont doubles down by adding another decode cluster, for a total of three clusters capable of decoding a total of nine instructions per cycle. Unlike AMD and Intel’s high performance cores, there is no micro-op cache or loop buffer. The fetch and decode path is the primary and only method of instruction delivery.

With 8-byte NOPs, instruction fetch bandwidth maxes out at 48 bytes per cycle. It’s a clear improvement over Crestmont, though I wonder why it’s not better on both. Each decode cluster can fetch 32 bytes per cycle, and the three decode slots in each cluster should only need 24 bytes per cycle in this test. But here, each cluster seems to cap out at 16 bytes per cycle. Lion Cove and Zen 5 can use their micro-op caches to achieve 64 bytes per cycle in this test.

4 byte NOPs more closely correspond to average instruction length in integer code, and usually moves the bottleneck to the decoders rather than instruction fetch bandwidth. Even though Skymont has 9 decode slots, sustained throughput is limited to 8 instructions per cycle by the subsequent rename stage.

For larger code footprints, Skymont and Crestmont can run code from L2 at just under 20 bytes per cycle. That’s good for 4 IPC with 4 byte instructions, which is still plenty considering IPC is often limited to far less than that by factors like backend memory latency.

Decoders feed micro-ops into queues in front of the renamer, which help absorb short duration delays. Besides a 3-wide decoder, a frontend cluster includes its own micro-op queue. Copy-pasting the cluster again brings micro-op queue capacity from 2×32 = 64 on Crestmont to 3×32 = 96 entries in Skymont. It’s nowhere near the 192 entry micro-op queue capacity on Lion Cove, but it does get close to some older cores. For reference, Zen 4 has a 144 entry micro-op queue.

Rename and Allocate

Next, the renamer stage sends micro-ops to the backend, allocating entries in all the necessary resources in the process. The renamer in Intel’s E-Cores simultaneously reads from all of the frontend clusters’s micro-op queues, putting the instruction stream back in-order for register renaming. Besides register renaming, the rename/allocate stage often performs other optimizations to break false dependenices and expose more parallelism to the backend.

Skymont can eliminate register to register MOVs and recognize zeroing idioms at full rate. That doesn’t always apply, as subtracting a register from itself no longer seems to be recognized. Compared to Crestmont, Skymont has also gained Golden Cove’s ability to do simple math completely within the renamer. Integer adds with an immediate can execute at more than one per cycle. It’s not as crazy as Golden Cove’s six dependent increments or add-immediates per cycle, but it could still speed up tiny loops by resolving the loop increment dependency chain faster.

Out-of-Order Execution Engine

It’s hard to understate the size of Skymont’s out-of-order execution engine. Its reorder buffer (ROB) has 416 entries, up from 256 in Crestmont. The ROB is an in-order list of all in-flight instructions, and an upper bound on how many micro-ops the core has in flight. For that reason, I think ROB capacity gives an idea of the reordering capacity that designers were targeting. Skymont’s ROB is larger than Sunny Cove or Zen 4’s, and not far off the 512 entry ROB in Golden Cove.

Other structures have to be sized appropriately because the rename/allocate stage is in-order, and will stall the moment it hits an instruction it can’t allocate resources for. Skymont’s register files and store queue see substantial size increases, though not by as much as ROB capacity growth.

Crestmont had generously sized register files capable of covering the majority of its ROB capacity. Intel may have decided that was overkill, and rebalanced Skymont’s backend resources to increase reordering capacity in a more efficient way.

An interesting example is Skymont’s reordering capacity for branches, which has dropped compared to Crestmont. A 96 entry branch order buffer can cover 23% of Skymont’s ROB capacity. I wonder if Intel might be cutting it a bit close here, because a couple of SPEC CPU2017 integer workloads have more frequent branches than that. But Intel’s engineers are obviously looking at more than just SPEC, and I trust they know what they’re doing.

Integer Execution

Compared to Crestmont, Skymont’s integer schedulers grow from 16 to 20 entries. There are still four schedulers, but each now has two ports instead of one, letting them feed an extra integer ALU. That doubles Skymont’s throughput for basic operations like integer adds compared to Crestmont.

Back in an interview with Cheese, AMD’s Mike Clark mentioned a unified scheduler can avoid situations where several ops become ready on one scheduling queue, but have to sit in line for that queue’s ALU port. I wonder if putting two ALU ports on each queue is a way around that. If three ALU ops suddenly become ready on one of Skymont’s schedulers, they would start execution over two cycles instead of three.

Less commonly used units like integer multipliers and shifters were not scaled up, and execution throughput for those operations remains similar to Crestmont. Skymont however has improved 64-bit integer multiplication latency, which drops from 5 to 4 cycles. It’s not as fast as Zen 5’s 3 cycles, but it’s good to see Intel find ways to cut pipeline stages here and there.

Skymont gains an extra branch port, letting it handle three not-taken branches per cycle. Throughput for taken branches is still limited to one per cycle because the branch predictor can’t go any faster.

Floating Point and Vector Execution

Floating point and vector execution has never been a strength of Intel’s E-Core line, but Skymont does get substantial upgrades. It now has a quad-pipe FPU. All four pipes can handle basic floating point and integer vector instructions, creating a setup reminiscent of Cortex X2 or Qualcomm Oryon’s. Compared to Crestmont, Intel has grown both the scheduling and non-scheduling queues by a significant amount.

As before, execution units remain 128-bits wide and 256-bit instructions execute as two micro-ops. A 256-bit vector result will also consume two 128-bit entries in the vector register file. Scheduling capacity for 256-bit operations remains mediocre despite what the numbers above would imply.

Some of the microbenchmark runs targeting Skymont’s FP/vector unit, using variations of Henry Wong’s methodology to measure structure sizes

From measurements, it feels like vaddps‘s micro-ops can’t get into the non-scheduling queue the way scalar addss ones can. So, scheduling capacity for those 256-bit packed FP adds is half of the scheduler capacity. It’s better than Crestmont, where I could get 23 vaddps instructions in flight. That measurement suggests Crestmont is using its non-scheduling queue, though not to its fullest extent.

I thought that could be a restriction with instructions that have to be broken into two micro-ops. However, cvtsi2ss (convert integer to floating point) is handled as a single micro-op and can’t use the non-scheduling queue on either architecture. Perhaps something about Intel’s non-scheduling queue prevents it from being used in certain situations.

Denormal Behavior

We previously covered Intel’s presentation on Skymont, where they discussed improved denormal handling to prevent “glass jaw” performance behavior. From testing on Skymont, there is indeed no penalty when an operation on normalized floating point numbers produces a subnormal result.

Curiously, Lion Cove has not received the same fast-path denormal handling hardware. This sort of >100 cycle penalty above can be easily avoided by disabling denormal handling via the flush-to-zero and denormals-are-zero flags. But it’s funny that Intel’s P-Cores have a “glass jaw” corner case that E-Cores now handle quite well.

Execution Latency

Skymont brings floating point execution latencies down across the board. As with Crestmont, there’s no latency penalty for using 256-bit vectors over 128-bit ones. 256-bit vector integer operations could sometimes see extra latency on Crestmont, possibly because it had an odd number of vector integer ALUs. Skymont improves there, and has no problem achieving single cycle latency for vector integer adds.

Floating point division is not pipelined and has an average latency of 2.5 cycles on Skymont. That’s a match for Zen 5, and better than 5 cycles on Crestmont.

Load/Store

Address generation gets handled by a massive seven AGUs on Skymont. Three generate load addresses, and four handle store addresses. In both areas, Skymont again gets a big upgrade over Crestmont.

Skymont’s four store AGUs may seem like overkill because the data cache can only handle two stores per cycle. However, more AGUs can help find memory dependencies faster.

As for finding those memory dependencies, Skymont behaves similarly to Crestmont. Dependencies appear to be checked at 4B granularity. Either half of a 64-bit store can be forwarded to a dependent 32-bit load. Crestmont could do zero latency forwarding for an exact address match if both the load and store are 64B aligned. Skymont expands that to cover more cases, though I don’t see any clear pattern to zero latency forwarding works. Even when it doesn’t, Skymont’s 2 cycle forwarding latency is faster than Crestmont’s 3-7 cycle latency.

Forwarding the upper half of a 64-bit store to a dependent 32-bit load takes 7-8 cycles, a bit longer than 6-7 cycles on Crestmont. Other overlap cases cause the forwarding mechanism to fail with a 14-15 cycle penalty, which is worse than Crestmont’s 11-12 cycle penalty. Just as with Crestmont, that penalty applies if a load and store access the same 4B aligned region, even if they don’t actually overlap. Intel and AMD’s high performance cores don’t suffer from that false dependency case, and generally have more flexible store forwarding mechanisms.

For example, Lion Cove and Zen 5 can do store forwarding across cacheline boundaries. Even when there are no memory dependencies, Zen 5 is notably more robust with misaligned accesses. A misaligned store executes over two cycles on Skymont, Crestmont, and Lion Cove, but can execute over a single cycle on Zen 5.

Address Translation

The load/store unit also has to translate program-visible virtual addresses to physical addresses that correspond to locations in DRAM. Operating systems set up multi-level tables to tell CPUs how they should map virtual addresses to physical ones, but accessing those tables (called a page walk) would introduce a lot of extra latency. To counter this, CPUs cache frequently used address translations in Translation Lookaside Buffers, or TLBs.

Skymont continues to have a rather small 48 entry L1 DTLB. However, L2 TLB capacity increases from 3072 to 4096 entries. The L2 TLB on Skymont is 4-way set associative, and accessing it costs an extra 9 cycles of latency jus like on Crestmont. Neither E-Core has a particularly fast L2 TLB, but getting a translation from it is far better than doing a page walk. Intel’s priority here seems to be avoiding expensive page walks rather than improving speed for TLB hits.

For context, Skymont matches AMD’s Zen 5 in L2 TLB entry count, though AMD’s 16-way set associative L2 TLB should make conflict misses less common. Skymont’s P-Core companion, Lion Cove, only has 2048 L2 TLB entries.

Cache and Memory Access

Data cache latency has regressed to four cycles on Skymont, compared to three cycles on Crestmont. Skymont’s L2 cache is more impressive, dropping latency from 20 to 19 cycles while providing twice as much capacity.

L2 misses head to a 8 MB memory side cache. Estimating memory side cache latency is difficult because testing with a 8 MB array will result in about half the accesses hitting in L2, assuming a non-LRU L2 replacement policy. At the 8 MB test size though, latency is 59.5 ns or 214 cycles. Since error from hitting L2 will only cause the test to underestimate memory side cache latency, Lunar Lake’s memory side cache has at least that much latency when accessed from the E-Core cluster.

59.5 ns is nearly as high as DRAM access latency on older systems. For example, the AMD FX-8350 has 61.7 ns of latency with a 1 GB test size and 2 MB pages. Lunar Lake’s memory side cache is very much closer to memory than CPU cores as its name suggests, and doesn’t provide comparable performance to Meteor Lake’s 24 MB L3.

As with Lunar Lake’s P-Cores, DRAM latency measurements are complicated by the memory controller staying in a low power state if there isn’t enough traffic. A simple memory latency test sees about 170 ns with a 1 GB test size, but that drops to 133 ns if another core pulls just over 8 GB/s of bandwidth. It’s better than 175 ns or 153 ns on Meteor Lake’s low power and standard Crestmont cores respectively, but nowhere near as good as desktop DDR5.

Skymont has a first level cache bandwidth advantage thanks to its additional 128-bit load port, but things are more evenly matched at lower cache levels. A single Skymont core can sustain 28-29 bytes per cycle from L2, a slight improvement over Crestmont’s 25-26 bytes per cycle. Skymont’s larger L2 is also appreciated. For larger test sizes, Crestmont benefits from Meteor Lake’s 24 MB L3. Lunar Lake’s 8 MB memory side cache really doesn’t help much. Usually memory bandwidth from a single core is latency limited, so this is another hint that latency is very high on Lunar Lake’s memory side cache.

Low power Crestmont is in a completely different class, and not in a good way. Its low clock speed and lack of a L3 cache put it far behind. Meteor Lake’s higher memory latency puts the proverbial nail in the coffin for low power Crestmont’s performance.

Multithreaded applications generally demand more bandwidth, and here Skymont posts clearer L2 bandwidth gains against its predecessor. Crestmont’s L2 could only provide 64 bytes per cycle, and that bandwidth has to be shared by all four cores in a cluster. Skymont increases L2 bandwidth to 128 bytes per cycle, doubling L2 bandwidth available to each core.

Outside the cluster, Crestmont’s L3 cache plays out against Skymont’s memory side cache. Neither has a significant advantage, and both E-Core clusters appear to be latency rather than bandwidth limited. Once the test gets out of Meteor Lake’s L3 though, the Skymont cluster can access a lot more DRAM bandwidth. However, AMD Strix Point’s Zen 5c cluster can achieve 61 GB/s from DRAM, limited only by the Infinity Fabric link.

Performance Picture

Intel compares Lunar Lake’s Skymont cores to Meteor Lake’s low power Crestmont Cores, and it’s easy to understand why. Skymont sits on a low power island just as low power Crestmont does on Meteor Lake. Both cores aim to offload background tasks, letting higher performance cores sleep.

Against low power Crestmont, Skymont benefits from better caching and better clocks courtesy of TSMC’s leading edge N3B process. Unsurprisingly, Skymont posts a huge 78.3% performance advantage in SPEC CPU2017’s integer suite. Skymont’s lead grows to a staggering 83.8% in the floating point suite.

But in my opinion, comparisons against low power Crestmont only provide half the picture. Skymont is meant to boost multithreaded performance too, like Crestmont Cores on. Meteor Lake uses Crestmont cores on the Intel 4 Compute Tile to fill that role. Therefore, a comparison against those Compute Tile Crestmont cores is also appropriate.

That comparison is less favorable to Skymont, which only manages a 0.68% performance gain in SPEC CPU2017’s integer tests. I consider that within margin of error, and even if it weren’t, no one would notice that in practice. Gains in the floating point suite are better at 15.7%, but I’d like to see double digit gains in both suites for such a large architecture change. I suspect Skymont would indeed provide double digit percentage gains given identical cache setups. However, giving Crestmont a 24 MB L3 and a 100 MHz clock speed advantage seems to be enough to cancel out Skymont’s improved architecture.

AMD’s Zen 5c is another appropriate comparison, as the Strix Point mobile chip features eight of those to improve multithreaded performance. Low clock speed on AMD’s density optimized core lets Skymont lead by a hair in SPEC CPU2017, though I still consider a 1.5% gain within margin of error. The floating point suite sees AMD’s Zen 5c pull ahead by a margin of 20.4%, partially because Zen 5c destroys Intel’s E-Cores on 503.bwaves and 549.fotonik3d.

While Skymont turns in a decent showing against its predecessor in SPEC CPU2017’s floating point suite, I feel SPEC’s reliance on compiler code generation doesn’t paint a complete picture. Software projects often use intrinsics or assembly if they require high performance. libx264 is one of them. Software video encoding offers better quality than hardware encoders by being more computationally expensive, and even the older H.264 codec is no exception.

In this workload, the Core Ultra 7 258V’s quad core Skymont cluster loses to a quad core Crestmont cluster on the Core Ultra 7 155H. Crestmont wins by just over 5%, though performance counters reported a 8.1% IPC advantage for Crestmont (1.46 IPC vs 1.35 IPC on Skymont). Skymont’s branch predictor does shine through, delivering 97.52% accuracy compared to Crestmont’s 97.35%. But it’s not enough to push Skymont ahead.

Using event 0x2E and unit masks 0x4F/0x41 for LLC references and misses

Skymont’s cache setup is a clear culprit. While Intel hasn’t documented performance counters for Skymont or Lion Cove yet, they do have a set of “architectural” performance events introduced with the Core Duo and Core Solo generation. Those are guaranteed to work on subsequent Intel CPUs, and include events for longest latency cache references and misses. What those events map to can vary of course. From testing, Skymont considers the 4 MB L2 the “longest latency cache”. And those events show Skymont sees far more misses with its 4 MB L2 than Crestmont does with its 24 MB L3.

Tested using the Broadwell binary

Y-Cruncher is a very heavily vectorized program that calculates Pi digits. Skymont really shows its advantage in this workload, posting a 1.56x speedup over its predecessor. Skymont also averaged 1.81 instructions per active core cycle, again a huge improvement over Cresmtont’s 1.22 IPC.

IPC, from performance counters. High IPC tasks tend to benefit more from a wider core, while lower IPC ones benefit from mitigating whatever the biggest bottleneck is (often backend memory access latency or frontend latency)

Performance-wise, Skymont seems to be at its best in high IPC workloads with a small cache footprint. For example Skymont beats Crestmont by 20.8% in 548.exchange2, a workload that fits in Zen 4’s 32 KB L1D cache. There, Crestmont’s already high 3.39 IPC increases to 4.21 with Skymont’s improvements. Conversely 520.omnetpp sees 10.38 MPKI on Zen 4’s 1 MB L2, and 1.42 MPKI for its 32 MB L3. On that test, Skymont drops to 0.54 IPC, while Crestmont holds up better at 0.62 IPC. However if a workload is really cache unfriendly, Skymont’s ability to pull more memory bandwidth can show through. I suspect that’s what happens in Y-Cruncher and 549.fotonik3d, as both are very memory bandwidth bound on other architectures. There, Skymont posts huge gains.

Final Words

Skymont is a huge step over Crestmont. Nearly every part of the core is beefed up in some way, and often significantly so. After seeing both P-Cores and E-Cores barely change from Alder Lake to Meteor Lake, I’m happy to see massive progress on both of Intel’s core lines. Assessing Lion Cove was straightforward because the core delivered a typical gen-on-gen improvement despite its changed cache hierarchy. Skymont’s situation is more complicated.

Certainly Lunar Lake’s Skymont cores crush low power Crestmont. But standard Crestmont already posts huge gains over its low power variant, thanks to a better cache setup and better process node. Despite massive architecture improvements, Skymont’s performance is hit or miss compared to Crestmont. Lunar Lake’s different cache hierarchy plays a large role in this, and highlights the difficulties in having one core setup play both the low power and multithreaded performance roles. It also highlights the massive role caches play in CPU performance. Even a dramatically improved core can struggle to deliver gains if the cache subsystem doesn’t keep up. That’s especially important with LPDDR5X, which has high latency and can be a handicap in low core count workloads.

Slide from Intel’s Hot Chips 2024 presentation on Lunar Lake, showing the Skymont cluster mostly containing a Teams workload

That said, Lunar Lake’s aims for better power efficiency, not necessarily for better performance. Skymont’s implementation in Lunar Lake is consistent with targeting lower power. Four Skymont cores are not going to do well against either eight standard Crestmont cores in Meteor Lake or eight Zen 5c cores in AMD’s Strix Point. But they do stand a better chance of containing low intensity workloads like videoconferencing, which are just a bit too demanding for Meteor Lake’s low power Crestmont cluster. Perhaps Lunar Lake’s Skymont cluster focuses harder on containing such workloads. Boosting multithreaded performance is a secondary concern, and landing in the same performance ballpark as Crestmont is good enough.

While the LPE-Core cluster on Meteor Lake does a comparatively poor job

When performance really matters, Lion Cove comes into play and does deliver a typical gen-on-gen improvement over Redwood Cove. Thus Lunar Cove should improve performance across a decent range of consumer applications, while also improving power efficiency in long duration, low intensity tasks. Intel designed their chip to meet those goals and I think their decisions made a lot of sense. But I was personally curious about how Skymont’s huge architecture changes would play out. Lunar Lake unfortunately isn’t the right place to evaluate that.

Again, we would like to thank ASUS for sending us over a Zenbook S 14 for review and if you like our articles and journalism, and you want to support us in our endeavors, then consider heading over to our Patreon or our PayPal if you want to toss a few bucks our way. If you would like to talk with the Chips and Cheese staff and the people behind the scenes, then consider joining our Discord.

More about the byline: I like that you're now using your actual name (or fake name, but at least it's no longer something edible). Your tests and articles are of a quality that you may as well claim get the credit with your name on it!

Nice article. There is one category of Intel chip that is missing from their portfolio since 2016: the Quark line. They also have a 2011 chip called the Claremont (a prototype which was never intended for release), which literally powered from the sky.

The Quark D2000 had around 0KB of cache and RAM. I'm waiting for a day where Intel, AMD, or ARM can release a Quark-like chip with 8MB of RAM so it can be fully solar powered and send text messages and make phone calls. That could also run Windows 95 and linux. There's an IoT - Solar GUI processor - Atom gap that has existed for the past 13 years. I am the world's leading proponent of this missing category.

More about the byline: I like that you're now using your actual name (or fake name, but at least it's no longer something edible). Your tests and articles are of a quality that you may as well claim get the credit with your name on it!

Nice article. There is one category of Intel chip that is missing from their portfolio since 2016: the Quark line. They also have a 2011 chip called the Claremont (a prototype which was never intended for release), which literally powered from the sky.

The Quark D2000 had around 0KB of cache and RAM. I'm waiting for a day where Intel, AMD, or ARM can release a Quark-like chip with 8MB of RAM so it can be fully solar powered and send text messages and make phone calls. That could also run Windows 95 and linux. There's an IoT - Solar GUI processor - Atom gap that has existed for the past 13 years. I am the world's leading proponent of this missing category.