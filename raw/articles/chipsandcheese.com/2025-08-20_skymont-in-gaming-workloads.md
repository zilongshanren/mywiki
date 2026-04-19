---
title: Skymont in Gaming Workloads
url: https://chipsandcheese.com/p/skymont-in-gaming-workloads
author: Chester Lam
published: '2025-08-20'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

E-Cores are central in Intel’s CPU strategy. Their small area footprint helps Intel achieve high multithreaded performance in a low area footprint. But E-Cores don’t derive their strength from numbers alone, because they still have significant per-core performance. Skymont, the E-Cores in Intel’s latest Arrow Lake desktop platform, can reach 4.6 GHz and sustain 8 micro-ops per cycle. Workloads sensitive to per-thread performance, such as games, will still benefit from Lion Cove’s even higher clock speeds and deeper reordering capacity. Still, Skymont’s handling of gaming workloads is still interesting partially as a curiosity, and partially because it can provide playable performance across a variety of titles. Testing here was done using Intel’s Arc B580 and DDR5-6000 28-36-36-36 memory.

Top-down analysis accounts for why core width went under-utilized by looking at the rename/allocate stage. It’s the narrowest stage in the pipeline, meaning that pipeline slots lost there will bring down average throughput. Skymont is often backend-bound, which is when the renamer had micro-ops to send downstream, but the out-of-order backend couldn’t accept them. Lion Cove is in a similar situation, which isn’t surprising because both cores share a memory subsystem after L2, and backend bound losses often occur because of memory access latency.

Skymont doesn’t have events or unit masks to categorize backend bound slots into core-bound and memory bound ones. AMD suggests doing so by looking at how often instruction retirement was blocked by a load versus another instruction type. That method can be roughly replicated on Skymont, which has an event that counts cycles when retirement was blocked by a load. Setting cmask=1 and the invert bit for the retirement slot count event provides the total number of cycles with retirement stalled.

A large portion of retirement stalls are caused by memory loads, but a surprising portion are caused by other reasons. There’s some difference in this method compared to AMD’s, because retirement can be stalled for reasons other than an incomplete instruction. For example, the ROB could be empty following a costly mispredict or an exception. Still, these “core bound” slots are worth a closer look.

Backend Stalls and Core Limitations

Resource unavailability is the most common reason that the backend can’t accept incoming micro-ops. The core’s reorder buffer, register files, memory ordering queues, and other structures can fill up as micro-ops pile up ahead of a long latency one. The first structure that fills then causes the renamer to stall. Skymont has a large 416 entry reorder buffer (ROB), which in theory lets it keep nearly as many micro-ops in flight as high performance cores like Zen 5 (448) and Lion Cove (576). However, Skymont often runs into other limitations before its ROB fills up. Its mostly distributed scheduling scheme doesn’t do as well as Zen 5’s more unified one. Microbenchmarking suggests Zen 5 and Skymont have similar scheduler entry counts across broad instruction categories, but a unified scheduler is typically more efficient for a similar entry count. Zen 5 rarely runs out of scheduler entries and fills its ROB more often, showing that advantage. Skymont’s register files and memory ordering queues are adequately sized and rarely show up as a limitation. But resource stalls aren’t the only reason behind backend-bound throughput losses.

Allocation restrictions aren’t directly documented except in performance monitoring events. One theory is that the distributed schedulers have limitations on how many micro-ops they can accept from the renamer each cycle. Arm clearly documents these restrictions for their Cortex X1 core. Perhaps Skymont has similar restrictions. In any case it’s not a huge deal. Getting rid of allocation restrictions would get micro-ops into the backend faster, but the backend will inevitably run into a resource stall if long latency instructions aren’t retired quickly enough.

Finally, “serialization” refers to situations when the core can’t reorder past a certain instruction. I’m not sure how often this happens on other cores, but Zen 5’s performance counters do attribute a substantial portion of backend stalls to miscellaneous reasons. Skymont for its part can break down serialization related stalls into a few sub-categories, allowing for a closer look.

IQ_JEU_SCB refers to “an IQ [instruction queue] scoreboard that stalls allocation until a specified older uop retires or (in the case of jump scoreboard) executes. Commonly executed instructions with IQ scoreboards include LFENCE and MFENCE.” Intel’s description implies Skymont has cases where it has to block further instructions from getting into the backend until the JEU (jump execution unit?) finishes executing a jump instruction. I’m not sure what triggers this. LFENCE (load fence) and MFENCE (memory fence) are explicit software memory barriers, and require the core to serialize memory accesses. I don’t think there’s much the core can do to avoid that mandated serialization.

Other serialization cases are rare. C01_MS_SCB, not shown above, counts cases when a UMWAIT or TPAUSE instruction put the core into a light C0.1 sleep state. NON_C01_MS_SCB points to “micro-sequencer (MS) scoreboard, which stalls the front-end from issuing from the UROM until a specified older uop retires. The most commonly executed instruction with an MS scoreboard is PAUSE”. Those stalls come up a bit, so perhaps games are using spinlocks with the PAUSE instruction.

Revisiting Crestmont

Skymont is notable for massively increasing reordering capacity compared to Crestmont, its immediate predecessor. Doing a direct comparison between the two is impossible because I have Crestmont in a Meteor Lake laptop without a discrete GPU. However, running Cyberpunk 2077’s built-in benchmark to get a general picture suggests Crestmont has an easier time reaching the limit of its 256 entry reorder buffer. Other limiting factors are still significant on Crestmont, but resource stall reasons have moved around compared to Skymont. For example, Cresmont rarely runs out of memory scheduler entries, though non-memory scheduler entries still feel pressure. Allocation restrictions are more of an issue on Skymont, perhaps because an 8-wide rename/allocate group is more likely to contain more micro-ops destined for the same scheduler. Serialization remains an issue on both cores.

Data-Side Cache and Memory Access

Cache misses tend to be the most common long latency instructions, and thus contribute heavily to resource stalls. Skymont has a typical triple-level data cache hierarchy, with a 32 KB L1D, and a 4 MB L2 shared across a quad core cluster. Arrow Lake provides a 36 MB L3 that’s shared across all cores. With a larger L2, smaller L1D, and no L1.5D, Skymont leans harder on its L2 compared to the Lion Cove P-Cores. Just like Lion Cove, L2 misses have to contend with ~14 ns of L3 latency, which is high compared to AMD’s sub-9ns L3 latency.

Skymont can break down how often the core was stalled due to a L1D demand miss. “Demand” indicates an access was initiated by an instruction, as opposed to a prefetch, but does not guarantee that instruction actually retired. Intel didn’t state what criteria it uses to determine if the core is stalled. Older cores like Skylake had a similar event that, for example, would consider the core L2 bound if there’s a pending load from L2, no L2 miss in flight, and no micro-op could begin execution that cycle.

DRAM latency poses the biggest challenge for Skymont. L2-bound cycles are low, suggesting Skymont’s out-of-order engine can often keep enough instructions in flight to hide L2 latency. High L3 latency isn’t too painful, likely for two reasons. The most obvious is that Skymont’s large 4 MB L2 lets it keep many accesses off L3. For perspective, 4 MB is as large as the L3 cache on mobile and console Zen 2 variants. The second is that Skymont’s lower clock speed means it has less potential performance to begin with. An analogy is that a less streamlined aircraft might worry less about air resistance because it flies at lower speeds. It’s not technically an advantage, but it does mean the core has less to lose while waiting for data from L3.

Setting the edge bit allows counting the number of stall occurrences. Dividing stall cycle count by occurrence count provides average stall duration. Those figures are strange, because average stall durations exceed measured cache latency for L2 and L3. Perhaps a lot of blocked instructions have multiple inputs that come from the specified cache level. Or, Skymont might use different criteria than Skylake to determine when the core is memory bound. For example, it could be indicating how long the core had instructions stuck waiting on data from a specified memory hierarchy level, even if other instructions were able to execute in the meantime.

Frontend

Skymont’s frontend is rarely a limiting factor, thanks to backend-related throughput losses. However, Skymont does have interesting performance counters at the frontend, so it’s worth a look. Intel breaks down frontend related stalls into bandwidth and latency bound categories by looking at why the frontend under-fed the core. In contrast, Zen 5 and Lion Cove consider a slot frontend latency bound if the frontend delivered no micro-ops that cycle, and bandwidth-bound if it delivered some micro-ops, but not enough to fill all renamer slots. Specifically:

Skymont’s frontend-bound performance monitoring event, with unit masks written out in AMD PPR style format

Splitting up latency versus bandwidth bound slots in this way might make more sense for Skymont, because its clustered decoder is less prone to losing throughput from taken branches compared to a conventional straight-line decoder. Basically, Intel considers Skymont frontend bandwidth bound if the decoders had incoming instructions, but was unable to process them efficiently. If the frontend is under-fed because of branch predictor delays, cache misses, or TLB misses, it’s considered latency bound.

Delays from all sources are minor, though decode stalls and hitting microcode cost some throughput. I’m not sure what causes decode stalls on Skymont. Intel’s optimization guide notes that load balancing issues between the decoders or “other decode restrictions” will often be indicated by the decode stall unit mask. Microcode is often used for instructions that aren’t handled by fast-path hardware in the execution engine. Density optimized cores tend to have less area budget for rarer and more difficult operations, and may execute them with multiple micro-ops (which might come from microcode). CPU designers will try to carefully look at what instructions applications use and minimize micro-op expansion. But that task will be harder for density optimized cores like Skymont.

Skymont’s branch prediction accuracy is good enough in games. I’m not going to look too far into Palworld and Call of Duty, because I suspect the margin of error is quite high. Curiously Skymont achieved better prediction accuracy and roughly 25% fewer mispredicts per instruction in Cyberpunk 2077’s built-in benchmark.

Final Words

Skymont may not be a P-Core and does not compete for maximum performance. However, it subjectively turns in a good performance in games. I played a variety of games on the Core Ultra 9 285K with affinity set to the 16 E-Cores. All were able to achieve more than playable framerates with few stutters or other issues. It’s a good showcase of what a density optimized core can do on modern process nodes, while also highlighting the issue of diminishing returns when pushing for maximum performance. I suspect a hypothetical chip with just Skymont cores could do quite well in isolation.

That doesn’t mean all E-Core chips can go mainstream anytime soon, or that Intel’s E-Core line can displace their P-Cores. If history is anything to go off, an E-Core would need to exceed P-Core performance in a number of applications before it can wear both hats. Long long ago, Intel’s P6-based Pentium M was able to outmatch Netburst-based Pentium 4 chips in a surprisingly large variety of workloads, foreshadowing Intel’s move to ditch Netburst in favor of a beefed up P6 variant in the Core 2 series. Skymont isn’t where Pentium M was in that era, nor does Intel’s Lion Cove P-Core suffer the inefficiencies Netburst did. But there’s no ignoring that Skymont is a very capable core on its own. Intel’s E-Core team deserves credit for packing all that performance into a small area footprint.

If you like the content then consider heading over to the Patreon or PayPal if you want to toss a few bucks to Chips and Cheese. Also consider joining the Discord.

It is outrageous that you need to use the Internet Archive to link to Anandtech articles. I can't believe they pulled down the articles. What a disgrace.

It'll be very interesting if Intel would make a handheld optimized chip with just E-Cores paired with the latest Xe graphics hardware. I wonder if it would bring the balance of performance and efficiency that would greatly benefit these form factors.

It is outrageous that you need to use the Internet Archive to link to Anandtech articles. I can't believe they pulled down the articles. What a disgrace.

It'll be very interesting if Intel would make a handheld optimized chip with just E-Cores paired with the latest Xe graphics hardware. I wonder if it would bring the balance of performance and efficiency that would greatly benefit these form factors.