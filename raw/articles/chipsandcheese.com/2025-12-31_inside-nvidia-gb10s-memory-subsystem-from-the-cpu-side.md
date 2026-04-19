---
title: Inside Nvidia GB10’s Memory Subsystem, from the CPU Side
url: https://chipsandcheese.com/p/inside-nvidia-gb10s-memory-subsystem
author: Chester Lam
published: '2025-12-31'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# Inside Nvidia GB10’s Memory Subsystem, from the CPU Side

GB10 is a collaboration between Nvidia and Mediatek that brings Nvidia’s Blackwell architecture into an integrated GPU. GB10’s GPU has 48 Blackwell SMs, matching the RTX 5070 in core count. The CPU side has 10 Cortex X925 and 10 Cortex A725 cores and is therefore quite powerful. Feeding all of that compute power requires a beefy memory subsystem, and can lead to difficult tradeoffs. Analyzing GB10’s memory subsystem from the CPU side will be the focus of this article. To keep article length manageable, I’ll further focus on Nvidia and Mediatek’s memory subsystems and design decisions. Core architecture and GB10’s GPU will be an exercise for another time.

# Acknowledgments

We’d like to thank Zach at ZeroOne Technology for allowing us SSH access to his DGX Spark unit for CPU testing.

# SOC Layout

CPU cores on GB10 are split into two clusters. Each cluster has five A725 cores and five X925 cores. Core numbering starts with the A725 cores within each cluster, and the two clusters come after each other. All of the A725 cores run at 2.8 GHz. X925 cores clock up to 3.9 GHz on the first cluster, and up to 4 GHz on the second.

# Cache and Memory Access

Arm’s A725 and X925 have configurable cache capacities. GB10 opts for 64 KB L1 instruction and data caches on both cores. All A725 cores get 512 KB L2 caches, and all X925 cores get 2 MB of L2. A725’s L2 is 8-way set associative and offers latency at just 9 cycles. In actual time, that comes out to 3.2 nanoseconds and is good considering the low 2.8 GHz clock speed. However, L3 latency is poor at over 21 ns, or >60 cycles.

Testing cores across both clusters indicates that the first CPU cluster has 8 MB of L3, while the second has 16 MB. I’ll refer to these as Cluster 0 and Cluster 1 respectively. Both clusters have the same L3 latency from an A725 core, despite the capacity difference. 512 KB isn’t a lot of L2 capacity when L3 latency is this high. Likely, selecting the 512 KB L2 option reduces core area and lets GB10 implement more cores. Doing so makes sense considering that A725 cores aren’t meant to individually deliver high single threaded performance. That task is best left to the X925 cores.

GB10’s X925 cores have 2 MB, 8-way set associative L2 caches with 12 cycle latency. L3 latency is surprisingly much better at ~56 cycles or ~14 ns, even though the A725 and X925 cores share the same L3. While it’s not a spectacular L3 latency result, it’s at least similar to Intel’s Arrow Lake L3 in nanosecond terms. Combined with the larger L2, that gives GB10’s X925 cores a cache setup that’s better balanced to deliver high performance.

A 16 MB system level cache (SLC) sits after L3. It’s hard to see from latency plots due to its small capacity relative to the CPU L3 caches. Latency data from cluster 0 suggests SLC latency is around 42 or 47 ns, depending on whether it’s accessed from a X925 or A725 core respectively. System level caches aren’t tightly coupled to any compute block, which typically means lower performance in exchange for being able to service many blocks across the chip. Nvidia states that the system level cache “enables power-efficient data sharing between engines” in addition to serving as the CPU’s L4 cache. Allowing data exchange between the CPU and GPU without a round trip to DRAM may well be the SLC’s most important function.

AMD’s Zen 5 in Strix Halo has smaller but faster core-private caches. GB10’s X925 and A725 cores have good cycle count latencies, but Zen 5 can clock so much higher that its caches end up being faster, if just barely so at L2. AMD’s L3 design continues to impress, delivering lower latency even though it has twice as much capacity.

DRAM latency is a bright spot for GB10. 113 ns might feel slow coming from a typical DDR5-equipped desktop, but it’s excellent for LPDDR5X. Strix Halo for comparison has over 140 ns of DRAM latency, as does Intel’s Meteor Lake. Faster LPDDR5X may play a role in GB10’s latency figures. Hot Chips slides say GB10 can run its memory bus at up to 9400 MT/s, and dmidecode reports 8533 MT/s. Placing CPU cores on the same die as the memory controllers may also contribute to lower latency.

## Bandwidth

Core-private bandwidth figures are straightforward. A725 cores can read from L1 at 48 bytes per cycle, and appear to have a 32B/cycle datapath to L2. A single A725 core can read from L3 at ~55 GB/s. X925 has more impressive bandwidth. It can read 64B/cycle from L1D, likely has a 64B/cycle path to L2, and can sustain nearly 90 GB/s of read bandwidth from L3. Single core DRAM bandwidth is also higher from a X925 core, at 38 GB/s compared to 26 GB/s from an A725 core.

A single AMD Zen 5 or Zen 4 core can pull over 50 GB/s from DRAM, or well north of 100 GB/s from L3. It’s an interesting difference that suggests AMD lets a single core queue up more memory requests, but low threaded workloads rarely demand that much bandwidth and I suspect it doesn’t make a big difference.

Shared components in the memory hierarchy face more pressure in multithreaded workloads, because having more cores active tends to multiply bandwidth demands. Normally I test multithreaded bandwidth by having each thread traverse a separate array. That prevents access combining, because no two threads will request the same address. It also shows the sum of cache capacities, because each core can keep a different part of the test data footprint in its private caches. GB10 has 15 MB of L2 across cores in each cluster, but only 8 or 16 MB of L3. Any size that fits within L3 will have a substantial part contained within L2.

Pointing all threads to the same array carries the risk of overestimating bandwidth if accesses get combined, but that seems to happen only after a shared cache. I initially validated bandwidth testing methodologies on Zen 2 and Skylake. There, shared array results generally aligned with L3 performance counter data. Using shared array results on GB10 provides another data point to evaluate L3 performance. Taken together with results using thread-private arrays, they suggest GB10 has much lower L3 bandwidth than AMD’s Strix Halo. However, it’s still respectable at north of 200 GB/s and likely to be adequate.

GB10’s two CPU clusters have asymmetrical external bandwidth, in addition to L3 capacity. Cluster 0 feels a bit like a Strix Halo CCX (Core Complex). Cluster 1 gives off AMD GMI-Wide vibes, with over 100 GB/s of read bandwidth. Switching to a 1:1 ratio of reads and writes dramatically increases measured bandwidth, suggesting the clusters have independent read and write paths with similar width. GB10’s CPU clusters are built using [Arm’s DynamIQ Shared Unit 120 ](https://developer.arm.com/documentation/102547/0201/The-DynamIQ-Shared-Unit-120/DynamIQ-Shared-Unit-120-configuration-options?lang=en)(DSU-120), which can be configured with up to four 256-bit CHI interfaces, so perhaps two clusters have different interface counts.

Much like Strix Halo, GB10’s CPU side enjoys more bandwidth than a typical client setup, but can’t fully utilize the 256-bit LPDDR5X bus. CPU workloads tend to be more latency sensitive and less bandwidth hungry. Memory subsystems in both large iGPU chips reflect that, and emphasize caching to improve CPU performance.

### A Heterogeneous Cluster Configuration?

Observations above point to Cluster 1 being performance optimized, while Cluster 0 focuses on density. Cache is one of the biggest area consumers in a modern chip so cutting L3 capacity to 8 MB is almost certainly an area concession. Cluster 0 may also have a narrower external interface as running fewer wires outside the cluster could save area as well. But Nvidia and Mediatek stop short of fully specializing each cluster.

Both Cluster 0 and Cluster 1 have the same core configuration of five X925 cores and five A725 cores. The X925 cores focus on the highest performance whereas the A725 cores focus on density. As a result the A725 cores feel out of place on a high performance cluster, especially with 512 KB of L2 in front of a L3 with over 20 ns of latency.

I wonder if going all-in on cluster specialization would be a better idea by concentrating the ten A725 cores into Cluster 0 for density and the ten X925 cores into Cluster 1 for high performance. Going from two heterogeneous clusters to two homogeneous clusters would simplify the OS scheduler as well. For example, the OS scheduler would also have an easier time containing workloads to a single cluster, letting the hardware clock or power down the second cluster.

## Latency under Bandwidth Load

Latency and bandwidth can go hand in hand. High bandwidth demands cause requests to back up in various queues throughout the memory subsystem, pushing up average request latency. Ideally, a memory subsystem can provide high bandwidth while preventing bandwidth hungry threads from starving out latency sensitive ones. Here, I’m testing latency from a X925 core with various combinations of other cores generating bandwidth load from within the same cluster.

Both clusters hit their maximum bandwidth figures with all A725 generating bandwidth load. Adding bandwidth demands from X925 cores decreases aggregate bandwidth while pushing latency up. Reversing the core load order suggests the X925 cores specifically cause contention in the memory subsystem. Latency reaches a maximum with four X925 cores asking for as much bandwidth they can get. It’s almost like the X925 cores don’t know when to slow down to avoid monopolizing memory subsystem resources. When the A725 cores come into play, GB10 seems to realize what’s going on and starts to balance bandwidth demands better. Bandwidth improves, and surprisingly, latency does too.

Cluster 1 is worse at controlling latency despite having more bandwidth on tap. It’s unexpected after testing AMD’s GMI-Wide setup, where higher off-cluster bandwidth translated to better latency control under high bandwidth load.

Loading cores across both clusters shows GB10 maintaining lower latency than Strix Halo over the achieved bandwidth range. GB10’s combination of lower baseline latency and high external bandwidth from Cluster 1 put it well ahead.

Throwing GB10’s iGPU into the mix presents an additional challenge. Increasing bandwidth demands from the iGPU drive up CPU-side latency, much like on Strix Halo. GB10 enjoys better baseline DRAM latency than Strix Halo, and maintains better latency at modest GPU bandwidth demands.

However, GB10 does let high GPU bandwidth demands squeeze out the CPU. Latency from the CPU side goes beyond 351 ns with the GPU pulling 231 GB/s.

I only generate bandwidth load from the GPU in the test above, and run a single CPU latency test thread. Mixing high CPU and GPU bandwidth demands makes the situation more complicated.

With two X925 cores on cluster 1 pulling as much bandwidth as they can get their hands on, and the GPU doing the same, latency from the highest performance X925 core goes up to nearly 400 ns. Splitting out achieved bandwidth from the CPU and GPU further shows the GPU squeezing out the CPU bandwidth test threads.

# Core to Core Latency

Memory accesses typically traverse the cache hierarchy in a vertical fashion, where cache misses at one level go through to a lower level. However, the memory subsystem may have to carry out transfers between caches at the same level in order to maintain cache coherency. Doing so can be rather complex. The memory subsystem has to determine which peer cache, if any, might have a more up-to-date copy of a line. Arm’s DSU-120 has a Snoop Control Unit, which uses snoop filters to orchestrate peer-to-peer cache transfers within a core complex. Nvidia/Mediatek’s High Performance Coherent Fabric is responsible for maintaining coherency across clusters.

GB10’s cluster boundaries are clearly visible with a coloring scheme applied across all result points. Results within each cluster are also far from uniform. Setting separate color schemes for intra-cluster and cross-cluster points highlights this. X925 cores in general give better intra-cluster latency results. Best case latencies involve transfers between X925 cores in the same cluster. Worst case latencies show up between A725 cores on different clusters, and can reach 240 ns.

Compared to Strix Halo, GB10’s core-to-core latency figures are high overall. Strix Halo manages to keep cross-cluster latencies at around 100 ns. It’s worse than what AMD achieves on desktop parts, but is substantially better than the 200 ns seen on GB10. Within clusters, AMD keeps everything below 50 ns while GB10 only manages 50-60 ns in the best case.

# Final Words

GB10’s CPU setup feels very density optimized compared to Strix Halo’s.GB10 has 20 CPU cores to Strix Halo’s 16, and gets there using a highly heterogeneous CPU configuration that’s light on cache. My initial thought is that all else being equal, I would prefer 32 MB of fast cache in a single level over 16 MB of L3 and 16 MB of slower system level cache. That said, performance is a complicated topic and I’m still working on benchmarking both Strix Halo and GB10. GB10’s memory subsystem has bright points too. Its DRAM latency is outstanding for a LPDDR5X implementation. Mediatek has also seen fit to give one cluster over 100 GB/s of external read bandwidth, which is something AMD hasn’t done on any client design to date.

CPU-side bandwidth is another interesting detail, and has a lot of common traits across both chips. CPU cores can’t access full LPDDR5X bandwidth on both GB10 and Strix Halo. The 256-bit memory bus is aimed at feeding the GPU, not the CPU. High GPU bandwidth demands can squeeze out the CPU in both memory subsystems. Perhaps Nvidia/Meditek and AMD both optimized for workloads that don’t simultaneously demand high CPU and GPU performance.

I hope to see Nvidia and AMD continue to iterate on large iGPU designs. Products like GB10 and Strix Halo allow smaller form factors, and sidestep VRAM capacity issues that plague current discrete GPUs. They’re fascinating from an enthusiast point of view. Hopefully both companies will improve their designs and make them more affordable going forward.

Again, we’d like to thank Zach at ZeroOne for providing SSH access to his Spark. If you like the content then consider heading over to the [Patreon](https://www.patreon.com/ChipsandCheese) or [PayPal](https://www.paypal.com/donate/?hosted_button_id=4EMPH66SBGVSQ) if you want to toss a few bucks to Chips and Cheese, also consider joining the [Discord](https://discord.gg/TwVnRhxgY2).

In the GB10 chip specs, both the S-dielet (CPU, memory subsystem and G-dielet (GPU) using TSMC 3nm.

Blackwell Discrete GPU cards are using TSMC N4P node and since the SM count on the G-Dielet share similarity to the RTX 5070s any chance you can test out the performance of the GPU portion?

Firstly, thanks Chester and a Happy and Healthy New Year to you and George!

Second, that makeup of the CPU reminded me of the recent large Dimensity SoCs - large X cores and the medium size A700 series cores. Maybe Mediatek figured that making the two CPU clusters larger versions of their mobile CPU was easier and quicker?

But, I can't help wonder if the area spent on the ten A cores in the Spark wouldn't have been better invested in ~ 4 additional X cores; saving a few milliwatts here and there makes sense for a smartphone SoC, but not sure it's the way to go for a ~ 200 Wh mini AI accelerator on a wall outlet.

That all being said, this is, after all, an AI box, and the key function of the CPU in those is to keep the GPU cores fed and manage traffic. A bit different from Strix Halo, which is intended to be both this and a strong general purpose computer. Strix Halo manages to be quite good at both, but it's (IMHO) a lot less specialized than the Spark. However, AFAIK, the Spark is still the way to go if AI and the Nvidia ecosystem is important; ROCm is getting better, but, from what I hear, still needs a lot more hands-on effort to make it work.

I wonder if you had a chance to test just how busy those two clusters of ARM Cores are when the Spark is used as intended - for AI? Maybe Mediatek was right about the medium size cores after all, and they'll do just fine "managing traffic"? In that case, were the X cores even necessary?

Lastly, your findings on memory and power allocation with priority for the Spark's GPU reminded me more than a little of your findings for the custom SoC for - the Steam Deck (of all things 😄). Another case of CPU cores getting starved (power and memory) so that the GPU can run at fuller tilt.

In closing, I really appreciate your tests and reviews. And, hopefully, you'll get to test a Battlematrix system from Intel soon, maybe even at or after CES (George, don't be shy asking Intel 😁) .