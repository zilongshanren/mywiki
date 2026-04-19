---
title: Arm’s Neoverse V2, in AWS’s Graviton 4
url: https://chipsandcheese.com/p/arms-neoverse-v2-in-awss-graviton-4
author: Chester Lam
published: '2024-07-22'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

Amazon Web Services (AWS) is the largest cloud provider, and an early Arm server adopter. AWS started investing into the Arm server ecosystem in 2018 with Graviton 1, which used 16 Cortex A72 cores. Three generations later, AWS’s Graviton 4 packs 96 Neoverse V2 cores.

Neoverse V2 is the server derivative of Arm’s Cortex X3, and is the latest member of Arm’s Neoverse V line. The Cortex X and Neoverse V series are Arm Ltd’s highest performance core line. We previously covered Neoverse V2 when Arm presented the core at Hot Chips 2023. Graviton 4 offers a chance to see a Neoverse V2 implementation in practice, and provides additional insight into Arm’s most newest and most powerful Neoverse V core.

Graviton 4 System Architecture

Graviton 4 uses Arm’s CMN-700 mesh interconnect to link 96 Neoverse V2 cores. The CMN-700 here is configured with a paltry 36 MB of shared L3 cache. Cacheline bounce latency across the CMN-700 mesh is quite good, with a latency of 30-60 ns. There’s no sharp jump like in designs that arrange cores into smaller clusters. However, latency does vary depending on where cores are located relative to the mesh stops responsible for tracking the tested address.

Core to core latency test was run with 64 core pairs in parallel because large Graviton 4 instances are expensive

To enable even larger instances, Graviton 4 is offered in a dual socket configuration to provide 192 cores and 1536 GB of DDR5. Latencies get more complicated when both sockets come into play. Crossing socket boundaries brings latency to 138.6 ns on average, which is similar to Intel’s Sapphire Rapids.

AMD’s Bergamo has to manage more cores and sees cross-socket bounce latencies exceeding 200 ns. Lower core count CPUs like Intel’s Broadwell E5-2660 v4 do better at 126 ns. Graviton therefore does well in terms of core to core latencies. It’s about on par with Graviton 2 and 3 within a socket, while providing 50% more cores. If cachelines are bounced between sockets, latencies are in line with other modern designs.

Uncontested memory accesses from one socket to another’s DRAM pool incur a heavier penalty, which isn’t great because last level cache misses are typically more common than hitting a modified line in another core’s private cache. Remote DRAM latency is north of 250 ns using 2 MB pages and pointer chasing through a 1 GB array. It’s a 142.5 ns penalty over hitting memory directly attached to the socket.

AMD’s Infinity Fabric links deliver better latency, with a 120 ns penalty for remote memory access. Older server chips have even better latency, and often enjoy better latency to directly attached memory too.

Graviton 4 has an acceptable 114.08 ns of latency for accessing directly attached memory. It’s comparable to Bergamo in a NPS1 arrangement, and worse than Genoa-X in a NPS2 setup. Graviton 3 had 120 ns of DRAM latency, so Graviton 4 at least makes progress over its predecessor.

Bandwidth is an important topic for server CPUs too, because higher core counts require more bandwidth to feed. Graviton 4 has a 12 channel, 768-bit DDR5-5600 setup with 768 GB of capacity per-chip. Bergamo also has a 12 channel memory setup, but the one we tested was set up with slower DDR5-4800 memory. Graviton 4 comes out ahead in an all-core read bandwidth test. Compared to older octa-channel setups like the one on Milan-X, Graviton 4 has a huge bandwidth advantage.

*Estimated by adding cross-socket BW from corresponding nodes, like 1->3 + 2->4

Graviton 4’s cross-socket links are less impressive, offering just over 77 GB/s when cores on one socket read from DRAM attached to the other. Zen 4’s Infinity Fabric links provide much higher bandwidth, at over 120 GB/s. It’s still a small portion of bandwidth available from directly attached DRAM, but AMD’s Bergamo and Genoa should handle better for non-NUMA aware programs.

Overall, Graviton 4 has a competent dual socket configuration. Cross-socket bandwidth and latency are a bit worse than expected, but cache coherency operations are handled well. When not crossing socket boundaries, Graviton 4’s DDR5 setup offers a combination of high bandwidth and acceptable latency.

The Neoverse V2 Core

As a member of Arm’s highest performance core line, Neoverse V2 is a large core with width and reordering capacity on par with AMD’s Zen 4. However, it stops short of being a monster like Golden Cove, Oryon, or Apple’s Firestorm. As implemented in Graviton 4, Neoverse V2 runs at up to 2.8 GHz. Clock speed is reduced to 2.7 GHz for dual socket instances. In either case, clock speed is low even compared to other server cores. For example, AMD’s density optimized Zen 4c can run at 3.1 GHz even in a dual socket, 256 core Bergamo setup. AMD’s Genoa-X, which uses Zen 4 cores with extra cache can sustain 3.7 GHz in an all-core workload.

The block diagram above was largely constructed from Arm’s Hot Chips 2023 presentation, but has been updated with estimated structure sizes from microbenchmarking.

Branch Prediction

A wide core with deep reordering capacity needs a capable branch predictor to match. Neoverse V2 uses an 8-component TAGE predictor, with larger tables than Neoverse V1. Larger tables reduce the chance of two branches clashing into the same table slot and wrecking each other’s prediction accuracy. More tables give the predictor more flexibility to use different history lengths. From abstract testing with repeating randomly generated patterns, Neoverse V2 is quite capable and looks similar to Golden Cove.

Zen 4 however can deal with longer patterns and higher branch counts. AMD has invested heavily into branch prediction over the past few Zen generations. Doing so while also increasing clock speeds past 5 GHz is a praiseworthy achievement. One small sacrifice appears to be using a two level direction predictor, where a more accurate but more deeply pipelined second level can override the first. Neoverse V2 can get by without an overriding predictor, likely because it runs at very low clocks and isn’t quite as ambitious.

Zen 4 Direction Predictor

For branch target caching, Neoverse V2 employs a triple level BTB scheme. A nano-BTB handles small loops can handle two taken branches per cycle. It appears to have 256 entries. Larger branch footprints get handled by what looks like a 8K entry BTB with single cycle latency, followed by a possibly 14K entry L2 BTB with 2-3 cycle latency.

Intel’s Golden Cove also has a large last level BTB with 12K entries. Zen 4’s 8K entry L2 BTB feels small by comparison. Neoverse V2’s ability to handle very large branch footprints with no bubbles certainly deserves praise. Arm clearly wants V2 to handle branchy spaghetti code with minimal hiccups.

Indirect branches get their target from a register instead of having it directly encoded into the instruction. The branch predictor must choose between multiple targets, creating another dimension of difficulty.

Returns are a special and common case of indirect branches, and can typically be handled with a return stack. Neoverse V2’s return stack appears to have 31 entries, much like members of AMD’s Zen line. That should be adequate for the vast majority of cases unless someone decides to use a functional programming language and misses a tail recursion case.

Impressively, Neoverse V2 handles call+return pairs in just two cycles, or likely one cycle per taken branch. Actual latency is on par with desktop Zen 4’s, which takes 4 cycles per call+return pair. Neoverse V2 also fares better when return stack capacity isn’t sufficient.

Fetch and Decode

Fetch addresses from the branch predictor are fed to downstream fetch stages via 32 entry fetch queue. To speed up instruction delivery, Neoverse V2 has a 64 KB L1 instruction cache and a 48 entry fully associative instruction TLB for address translation.

To further improve frontend performance and lower decode costs, Neoverse V2 caches decoded micro-ops in a 1536 entry micro-op cache. This micro-op cache can deliver eight micro-ops per cycle, compared to six from the conventional decoders. Throughput can further increase if the decoders fuse pairs of adjacent instructions into a single micro-op. The micro-op cache is virtually indexed and virtually addressed, so micro-op cache hits don’t require a TLB lookup. Software doesn’t need to care, because Arm has mechanisms ensuring everything stays consistent as if the micro-op cache were physically addressed.

Prior members of Arm’s Cortex X and Neoverse V line had a 3072 entry micro-op cache, so Neoverse V2’s micro-op cache is smaller than its predecessors. That’s likely because the benefit of using a micro-op cache in Neoverse V2’s scenario is limited. Throuhgput downstream is restricted by the renamer, so the micro-op cache’s benefits are restricted to lowering frontend latency and power draw. Arm has a long history of mitigating decode power with a predecode scheme, moving some decode stages to the L1i fill stage. Using that in conjunction with a micro-op cache feels like overkill, especially when Neoverse V2 is not running at high clock speeds and Intel’s Golden Cove did 6-wide decode back in 2021 at much higher clocks.

Neoverse V2 and Zen 4 fuse adjacent NOP pairs into one micro-op, inflating micro-op cache bandwidth in this test

L1i misses are tracked by a 16 entry fill buffer, which gives Neoverse V2 enough memory level parallelism to sustain 4 instructions per cycle when running code from L2. AMD and Intel enjoy better code fetch bandwidth from L3, likely because their L3 caches have better latency. Neoverse V2 still turns in a passable performance, delivering over two instructions per cycle from L3.

Rename and Allocate

Micro-ops from the frontend then pass through a rename and allocate stage, which allocates resources in the backend to track them through various stages of execution. Arm says the renamer can handle 8 micro-ops per cycle, but through testing I was only able to sustain 6 per cycle. That makes Neoverse V2 a 6-wide core overall. Arm’s slides suggest the renamer should be 8-wide, but that doesn’t line up with test results.

The renamer is also a good place to carry out various optimizations like move elimination or breaking dependencies when an operation is known to zero a register. Neoverse V2 has some move elimination capability, though it’s not as robust as on Intel and AMD’s recent CPUs. Sometimes Neoverse V2 can break dependencies between register to register MOVs, but not all the time. Independent MOVs execute at just under 4 per cycle, suggesting they still use ALU pipes. I think there are only four ALU pipes because integer additions only execute at four per cycle. To Neoverse V2’s credit, zeroing a register with an immediate value of zero works well, at 6 per cycle.

Out-of-Order Execution

In the backend, operations get sent for execution as soon as their inputs are ready, irrespective of program order. That lets the execution engine move past a stalled instruction and keep the execution units fed. How far ahead the core can move is limited by the various buffers and register files required by in-flight instructions. Neoverse V2 is a close match for Zen 4 in many respects.

Integer Cluster

Neoverse V2 should have six ALUs, up from four in Neoverse V1. I could not achieve 6 adds per cycle, so I don’t think Neoverse V2 as implemented in Graviton 4 has 6 ALUs. The next question is whether Amazon opted to delete the ALUs attached to the branch schedulers, or the two extra ALUs mentioned in Arm’s slides. Branch units are still on separate ports, because I could achieve more than 4 IPC by mixing adds with branches.

I tested scheduling capacity with 40 dependent branches followed by dependent adds. Graviton 4 doesn’t have more than 60 total entries available for such a pattern. Therefore, it’s more likely that the two extra ALUs got deleted along with their scheduling queues.

If that’s correct, Neoverse V2 has comparable scheduling capacity to Zen 4 for integer operations. Technically Zen 4 has a few more scheduler entries available, but it has to share three of its integer schedulers with memory accesses (AGU ports). Qualcomm’s Oryon looks overbuilt next to Zen 4 and Neoverse V2.

FP/Vector Execution

On the floating point and vector side, Neoverse V2 has four 128-bit pipes. All four can handle most basic FP and vector integer operations. Like prior Neoverse V/Cortex X cores and Qualcomm’s Oryon, this arrangement lets the core match Zen 4 in fused multiply-add (FMA) floating point operations per cycle even with narrower execution pipes. Zen 4 has four FP/vector execution pipes with 256-bit vector width, but they’re more specialized. AMD can have an advantage if 256-bit packed FP adds can be dispatched alongside FMAs, but Neoverse V2 can hold up better with programs that don’t use wide vectors.

FP/vector operations tend to have longer latencies, so CPUs often have a lot of scheduler entries on the FP side to hide that latency. Neoverse V2 adds a few scheduler entries compared to Cortex X2, but keeps the same scheduler arrangement. Like AMD’s Zen line, Neoverse V2 has a non-scheduling queue that can accept FP operations from the renamer if the schedulers are full. That helps delay a stall further up the pipeline and let other operations get into the backend, while being cheaper than a larger scheduler. However, Neoverse V2’s capacity to track incomplete FP/vector ops is less than Zen 4’s. It’s also less than Qualcomm Oryon’s, which takes a brute force approach to the problem with giant schedulers.

FP latences are the same for scalar FP32 and 4xFP32 packed into a 128-bit vector

Neoverse V2’s floating point execution latencies are good and in-line with the competition. 2 cycle FP addition latency is nice to see considering Neoverse V2’s low clocks, and is a strength of recent Cortex/Neoverse designs. Vector integer operations have less impressive latencies. Even simple addition of 32-bit integers packed into a 128-bit vector has two cycles of latency. Maybe Neoverse V2 has two pipeline stages for reading the vector register file, where most AMD/Intel cores are able to get by with just one.

Load/Store Unit

The load/store unit is an important component of the execution engine, and ensures memory accesses are executed quickly while making it look like those accesses went out in-order. First, memory addresses get their virtual addresses calculated by a set of three address generation units (AGUs). Two can handle both loads and stores, while one is dedicated to loads. Zen 4 similarly has a triple AGU setup, but economizes scheduler capacity by sharing entries between AGUs and ALUs.

Address Translation and TLBs

Virtual addresses are then translated to physical addresses. Translation lookaside buffers (TLBs) cache frequently used translations to speed this up. Neoverse V2 has a two level TLB setup like most cores. A 48 entry fully associative L1 DTLB handles the most commonly accessed pages, while a 2048 entry 8-way L2 TLB deals with larger memory footprints. L2 TLB accesses add 5 cycles of latency, which is reasonable even at V2’s low clocks.

Arm has opted not to change TLB capacity from Cortex X2. When AMD went from Zen 3 to Zen 4, L1 DTLB capacity increased from 64 to 72 entries, while the L2 DTLB grew from 2048 to 3072 entries. L2 DTLB access on Zen 4 adds 7 cycles, which is also reasonable considering the TLB’s larger size and ability to run above 5 GHz. In those client designs, Zen 4’s L2 DTLB actually has better latency than Neoverse V2’s. But the situation turns around in a high core count server environment, where Zen 4c has a much smaller clock speed advantage.

Memory Dependencies and Store Forwarding

Then, the load/store unit has to ensure proper ordering for memory operations. That involves checking whether a load overlaps with a prior in-flight store. If it does, the load/store unit has to forward data from the prior store instead of fetching stale data from the cache hierarchy. Neoverse V2 lacks robust detection for store forwarding opportunities, and can only forward either half of a 64-bit store to a subsequent 32-bit load. It feels a lot like Neoverse N1 from years ago. In fairness that should cover common cases, but Intel and AMD have been doing fast-path forwarding for any load contained within a prior store for quite a few generations.

Using the test described by Henry Wong, but implemented for 64-bit Arm

When fast forwarding works, Neoverse V2 carries it out with 5 cycle latency. That’s a match for Golden Cove, and is better than Zen 4’s 6-7 cycles. However, Zen 4 and Golden Cove can do zero latency forwarding with the simplest matched address case. And of course, AMD and Intel can clock their cores higher. Failed store forwarding costs 10-11 cycles on Neoverse V2, which is better than 19 or 20 cycles on Golden Cove or Zen 4.

Same test on Zen 4

L1D Access

If there are no dependencies, memory accesses hit the cache hierarchy. The L1 data cache is the first stop, and has a uniquely difficult job because programs access data at the byte granularity. Like other caches, the L1 data cache tracks data in much larger blocks. A “misaligned” access that crosses block boundaries can cause delays, because the cache has to access both blocks under the hood and merge the results.

Neoverse V2’s data cache has 64B alignment, and thus suffers misalignment penalties when an access crosses a 64B boundary. Zen 4’s data cache has 64B alignment for loads and 32B alignment for stores, making it slightly more prone to misaligned access penalties. Accesses can also cross a 4096B page boundary, meaning the TLB has to return two address translations. Neoverse V2 suffers a 11-12 cycle penalty for split-page stores. Zen 4 suffers a 33 cycle penalty in that case, while Golden Cove lands in the middle with a 24 cycle penalty. Split-page stores are handled gracefully on Neoverse V2 and Zen 2 with no penalty, while Golden Cove takes a minor 3-4 cycles for that case.

Minimum access latency is 4 cycles on V2’s data cache. Zen 4 also has 4 cycle L1D latency, but I would have liked to see 3 cycle latency considering V2’s low clock speeds. Vector access bandwidth is lower too, with 3×128-bit loads compared to 2×256-bit on Zen 4. Arm says V2 can service four scalar 64-bit loads per cycle, but because the core only has three AGUs, it’s probably a special case for LDP instructions.

Capacity-wise, V2’s data cache is good with 64 KB. It’s refreshing to see that compared to the paltry 32 KB found on Zen 4, or the mediocre 48 KB on Golden Cove. Arm has also switched from a pseudo-LRU replacement policy to RRIP (Re-Reference Interval Prediction), which can improve hitrate by making smarter decisions about what data to evict from the cache when new data is brought in.

Lower Level Caches

After L1, Neoverse V2 has a 1 or 2 MB L2 cache that insulates the core from the slower mesh interconnect. Amazon chose the 2 MB option for Graviton 4. Latency is good at 11 cycles, compared to 14 cycles for Zen 4.

Actual L2 latency is slightly worse compared to Zen 4 cores in Genoa-X, but compares favorably to the 3.1 GHz Zen 4c cores in Bergamo. Overall the L2 looks very good considering it has twice as much capacity as Zen 4’s L2.

Like Intel’s Sapphire Rapids, Neoverse V2 needs that large L2 because hitting L3 adds a lot of latency. A L3 hit takes 68 cycles, or 25 ns at the 16 MB test point. It’s better than Sapphire Rapids, but is similar to L3 latency on Intel’s Ice Lake server and worse than Bergamo’s 18 ns. AMD’s Genoa-X has even better L3 performance.

Bandwidth

A Neoverse V2 core enjoys reasonable bandwidth, though AMD and Intel’s cores have better bandwidth because they’re designed for high vector performance. That’s especially the case for Sapphire Rapids, which can do three 256-bit loads per cycle.

Arm’s Hot Chips 2023 presentation suggests Neoverse V2’s L2 can provide an incredible 128 bytes per cycle of bandwidth, using a quad bank arrangement where each bank can service a 64B cacheline request every two cycles. However, even a simple linear read-only access pattern averages just under 32 bytes per cycle. Using a read-modify-write or write-only pattern didn’t significantly change L2 bandwidth.

L3 bandwidth from a single core is poor at just over 30 GB/s. Like Intel’s Sapphire Rapids, high L3 latency likely limits achievable bandwidth. Neoverse V2 has a 96 or 92 entry transaction queue depending on whether you check the Hot Chips 2023 slides or the Technical Reference Manual. Either way, it’s a lot of entries, but not enough to hide L3 latency. AMD’s L3 provides very low latency in comparison, and L3 bandwidth from a single core is very high.

Across the whole chip, Graviton 4 has over 12 TB/s of L1 bandwidth. It’s not a match for Genoa-X’s 18 TB/s, but it’s a large jump over Graviton 3 and Milan (Zen 3 server). Total L2 bandwidth is in the multi-terabyte range as well. L3 bandwidth is difficult to evaluate because L2 capacity across the chip’s 96 cores greatly exceeds L3 capacity.

Some Light Benchmarking

Neoverse V2’s architecture and Amazon’s implementation choices have to come together to provide high performance. Here, I’m comparing an octa-core Graviton 3 instance against prior data from Bergamo. To provide a vague picture of Genoa performance, I’m downclocking my Ryzen 7950X3D to 3.42 GHz. That’s the nominal all-core boost clock for AMD’s VCache-equipped EPYC 9V33X, and roughly corresponds to the very low end of clock speeds for a Genoa part. In reality the 9V33X can sustain 3.7 GHz during heavy all-core workloads, and many other Genoa parts probably do the same.

I’ll be encoding a 4K video with libx264 and compressing a large file with 7-Zip. Software video encoding heavily exercises a CPU’s vector units and can demand significant bandwidth. 7-Zip on the other hand purely uses scalar integer operations, and can give the branch predictor a tough time.

Graviton 4 struggles in libx264. A standard Zen 4 CCD can pull ahead even without SMT. Add in SMT, and the lead grows to over 60%. V-Cache can extend that lead further. 7-Zip paints a different picture, with Graviton 4 comfortably beating an octa-core Bergamo CCX.

Performance counters indicate Arm’s efforts to optimize Neoverse V2 for low clocks has worked to some extent. Neoverse V2 averages higher IPC than Zen 4 in both workloads. However, it’s not enough to offset Zen 4’s higher clocks and SMT capability. And Zen 4 can clock much higher, which would only widen the gap.

Unfortunately there’s no way to get per-core IPC when both SMT threads are loaded

ISA can also make IPC a misleading metric because a workload might require more instructions on a different ISA. In libx264, Neoverse V2 executed 17.6% more instructions than Zen 4, partially due to differences in vector length support. 7-Zip went the other way, with Zen 4 executing 9.6% more instructions to complete the same task.

Branch prediction is one of the most challenging aspects of CPU design, and performance counters also provide insight into that. Microbenchmarking suggested Zen 4 can handle longer patterns. However, that only translates to a small advantage in practice. AMD may have overbuilt the branch predictor to improve SMT yield, since Zen 4 loses surprisingly little accuracy when a workload is allowed to use both SMT threads on a core.

Neoverse V2 doesn’t have performance counters to track renamed micro-ops, so quantifying the exact impact of mispredicts is hard. But we can at least try to normalize for branch rate by looking at mispredicts per instruction. In libx264, mispredicts have a minor impact. Prediction accuracy is just a bit better than in 7-Zip, but libx264 doesn’t execute a lot of branches compared to other instructions. The opposite is true for 7-Zip, where about 18% of instructions are branches for both x86-64 and aarch64.

AMD’s overbuilt branch predictor really proves its worth in 7-Zip, where a less than 1% difference in prediction accuracy translates to Zen 4 suffering 17.9% fewer mispredicts per instruction.

Going through the rest of the pipeline with performance counters is impractical because renting Graviton 4 instances costs money. But we can get an overview by looking at backend and frontend bound metrics. libx264 is primarily backend bound, so performance is limited by how fast the out-of-order execution engine can complete operations and how well it can hide latency.

7-Zip is both frontend and backend bound, likely because the high branch rate creates challenges for instruction delivery. Neoverse V2 likely fares better there thanks to its very large and low latency (in cycle counts) BTBs. In libx264, which has a smaller branch footprint, Neoverse V2 probably benefits from its larger L1 instruction cache.

Final Words

Arm has mastered the complexity of designing a modern out-of-order core over the past few years. Neoverse V2 is yet another demonstration of that. It takes the solid foundation provided by prior Neoverse V and Cortex X cores, and makes improvements throughout the pipeline. Compared to AMD and Intel cores, Neoverse V2 might have a leg up because its design only caters to servers and smartphones. In those applications, single-threaded performance is less critical than in laptops and desktops. For comparison, Intel’s Golden Cove and AMD’s Zen 4 have to serve across a much wider range of core power and performance targets. Deeper pipelines that are great for maximum performance at 5 GHz could lose that edge at lower clocks.

Sometimes, Neoverse V2 takes advantage of this. Call/return prediction, L2 cache latency, recovery from failed store forwarding, and split-page store handling are good examples. But sometimes, as with store forwarding, potential advantages are overcome by fancy architecture tricks on AMD and Intel’s latest cores. In other areas, V2 has no advantage over Zen 4 even in cycle count latency. L1D latency is one example, and vector integer execution latencies are another.

Neoverse V2’s area is surprisingly similar to Zen 4c’s

Therefore, Neoverse V2 isn’t really a high performance core the way Zen 4, Golden Cove, and even Qualcomm’s Oryon are. Instead, it seeks to deliver adequate single threaded performance in a power limited smartphone SoC, or a high density server CPU.

From an area perspective, Neoverse V2 implementation should have no trouble matching Bergamo’s core count. That’s especially true if an implementer decides to skimp on L3 cache, as Graviton 4 has done. But Amazon has decided they couldn’t do that with Graviton 4, which has 96 cores just like AMD’s mainstream Genoa servers. Against Bergamo, Neoverse V2 is hit or miss. But against Genoa or Genoa-X, Neoverse V2 is at a disadvantage. Its clock speed issues are just too great, considering at least one cloud provider is willing to offer 3.7 GHz Genoa instances, and Zen 4 CCDs running at 3.42 GHz already give an octa-core Graviton instance quite a challenge.

In isolation, Neoverse V2 is a good core. But with Zen 5 on the horizon, V2 could use a clock speed bump to give it a better chance against AMD’s Zen 4 from 2022. Arm has announced Cortex X4, a newer member of the Cortex X/Neoverse V line. Cortex X4 beefs up various parts of the pipeline compared to Cortex X3/Neoverse V2. Hopefully Arm pulled this off without having to run the core at very low frequency to stay within power targets. It’s all too easy to tunnel vision on clock speed or performance per clock in isolation.

Again, we would like to thank our Patreon members and Paypal donators for donating and if you like our articles and journalism then consider heading over to our Patreon or our PayPal if you want to toss a few bucks our way. If you would like to talk with the Chips and Cheese staff and the people behind the scenes, then consider joining our Discord.