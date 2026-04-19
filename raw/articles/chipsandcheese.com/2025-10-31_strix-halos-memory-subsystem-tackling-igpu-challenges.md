---
title: 'Strix Halo’s Memory Subsystem: Tackling iGPU Challenges'
url: https://chipsandcheese.com/p/strix-halos-memory-subsystem-tackling
author: Chester Lam
published: '2025-10-31'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

Editor’s Note (11/2/2025): Due to an error in moving the article over from Google Docs to Substack, the “Balancing CPU and GPU Bandwidth Demands” section was missing some Cyberpunk 2077 data. Apologizes for the mistake!

AMD’s Strix Halo aspires to deliver high CPU and GPU performance within a mobile device. Doing so presents the memory subsystem with a complicated set of demands. CPU applications are often latency sensitive with low bandwidth demands. GPU workloads are often latency tolerant and bandwidth hungry. Then, multitasking requires high memory capacity. Mobile devices need low power draw. Finally, the whole package has to fit within a price tag acceptable to consumers. Investigating how AMD dealt with those challenges should make for a good time.

Credit

ASUS has kindly sampled the ROG Flow Z13, which implements Strix Halo in a tablet form factor with 32 GB of LPDDR5X. They’ve made deep dives like this possible, and we greatly appreciate their support.

RX 7600 results were provided by Azralee from the Chips and Cheese Discord.

GPU

Strix Halo’s GPU uses a similar cache setup to AMD’s older and smaller mobile chips. As on Strix Point and Hawk Point (Zen 4 mobile), Strix Halo’s GPU is split into two Shader Arrays. Each Shader Array has 256 KB of L1 mid-level cache, and a 2 MB L2 services the entire GPU. Latencies to those GPU-private caches are in line with other RDNA3 and RDNA3.5 implementations. AMD likely kept L2 capacity at 2 MB because a 32 MB memory side cache (Infinity Cache, or MALL) takes over as the GPU’s last level cache.The L2 only has to catch enough traffic to prevent the Infinity Cache from getting overwhelmed. The resulting cache setup is similar to the one in the RX 7600, a lower midrange RDNA3 discrete card.

The Infinity Cache on Strix Halo has slightly higher latency compared to implementations in AMD’s discrete cards. DRAM latency from the GPU is higher as well. Compared to AMD’s other mobile CPUs with iGPUs though, the 32 MB Infinity Cache offers a large cache capacity increase.

Nemes’s Vulkan bandwidth test achieves just under 1 TB/s from Infinity Cache. The figures align well with performance counter data. Taken together with the chip’s 2 GHz FCLK, bandwidth test results suggest the GPU has a 512B/cycle path to the interconnect. If so, each of the GPU’s eight Infinity Fabric endpoints has a 64B/cycle link.

As a memory side cache, Infinity Cache can theoretically handle any access to physical addresses backed by DRAM. In an earlier interview with Cheese (George), AMD indicated that Infinity Cache was focused on the GPU, and that its behavior could change with firmware releases. Some of that change has happened already. When I first started testing Strix Halo just after Hot Chips 2025, results from my OpenCL microbenchmarks reflected Infinity Cache’s presence. I used that OpenCL code to figure out Data Fabric performance events. But PMU data collected from games suggested Infinity Cache wasn’t used once a game went into the background. Hardware doesn’t know whether a process is running in the foreground or background. That’s something the operating system knows, and that info would have to be communicated to hardware via drivers. Therefore, Infinity Cache policy can change on the fly from software control.

From early data collected on 9/1/2025

At that time, Nemes’s Vulkan-based code didn’t reflect Infinity Cache’s presence. PMU data showed a match between CS and UMC traffic, indicating the microbenchmark wasn’t taking advantage of Infinity Cache rather than the cache struggling with the access pattern. I was in the middle of investigating what Infinity Cache did or didn’t apply to when Windows updated. Then, foreground/background status no longer had any effect. Nemes’s Vulkan code was also able to observe the Infinity Cache.

Early observations on Infinity Cache behavior aren’t relevant today, but they do show Infinity Cache’s behavior is influenced by factors beyond a memory request’s origination point. Not all GPU requests install into the cache, and AMD can change cache policy on the fly. AMD could tune behavior with future updates too.

One early observation from OpenCL remained consistent though. Infinity Cache isn’t used for a buffer created with the CL_MEM_ALLOC_HOST_PTR flag and managed with zero-copy map/unmap APIs. CL_MEM_ALLOC_HOST_PTR requests an allocation from host-visible memory. On systems with discrete GPUs, AMD tends to handle that by allocating memory from DRAM attached to the CPU.

Intuitively, that flag shouldn’t make a difference on integrated GPUs. I’m not sure why it affects Infinity Cache behavior. Perhaps Strix Halo splits address ranges for the CPU and GPU under the hood, and the CPU’s address ranges aren’t cacheable from the Infinity Cache’s perspective.

AMD’s discrete Radeon RX 9070 shows similar behavior, with Infinity Cache not being used for host-side memory. Latency to host memory goes up to nearly a microsecond on RX 9070, while it remains unchanged on Strix Halo. Integrated GPUs have an advantage with zero-copy compute code, and it shows.

To further check zero-copy behavior, I have a test that allocates a 256 MB buffer using OpenCL’s Shared Virtual Memory APIs and only modifies a single 32-bit value. Strix Halo supports fine-grained buffer sharing like other recent AMD GPUs, meaning applications can use results generated from the GPU without calling map/unmap functions.

Strix Halo shows low latencies in line with zero-copy behavior. It’s worth noting that not all integrated GPUs can avoid a copy under the hood.

Copy APIs like clEnqueueReadBuffer and clEnqueueWriteBuffer are still relevant, because they’re the traditional way to work with discrete GPUs. Those APIs often use the copy queue and DMA engines, which handle data movement without involving general purpose compute units. Strix Halo can achieve high copy bandwidth in the CPU to GPU direction, but not the other way around.

Performance counter data suggests copies to the GPU don’t go through the Infinity Cache. During a copy, the shared memory controllers should observe both a read from CPU-side memory and a write to GPU-side memory. But there’s nowhere near 100% overhead compared to software measurements.

Bandwidth is lower in the other direction, but curiously CS-level bandwidth is similar. The memory controllers see less bandwidth, indicating some requests were handled on-chip, likely by Infinity Cache. Curiously, there’s way more than 100% overhead when comparing PMU data to software-visible copy bandwidth.

CPU

Strix Halo’s CPU side superficially resembles AMD’s flagship desktop parts, with 16 Zen 5 cores split across two Core Complex Dies (CCDs). However, these CCDs use TSMC’s InFO_oS for connectivity to the IO die rather than on-PCB traces. The CCD has 32B/cycle of bandwidth to the system in both the read and write directions.

Therefore, Strix Halo’s CCDs have more bandwidth at the die boundary than their desktop counterparts, but only in the write direction. It’s an advantage that’s likely to have minimal impact because reads often outnumber writes by a large margin.

Other CPU chiplet designs have more bandwidth at die boundaries, including the Compute Tile on Intel’s Meteor Lake and AMD’s own “GMI-Wide” configuration. GMI-Wide uses two links between the CCD and IO die to maximize cross-die bandwidth in lower core count server chips. Even though GMI-Wide doesn’t use advanced packaging, it has significantly more cross-die bandwidth than Strix Halo.

Add = adding a constant to an array, creating a read-modify-write pattern with an equal amount of reads and writes. NT Write = non-temporal writes. These bypass cache and in many CPUs trigger a special case that avoids read-for-ownership for cachelines that are entirely overwritten

In a loaded latency test with reads, a Strix Halo CCD can reach high bandwidth levels at lower latency than standard GMI-Narrow CCDs. Part of that is likely down to its high bandwidth LPDDR5X setup, which a single CCD can’t come close to saturating. But that advantage doesn’t come through until bandwidth loads pass 45-55 GB/s. Before that, LPDDR5X’s high baseline latency puts Strix Halo at a disadvantage. At very high bandwidth load, Intel Meteor Lake’s higher cross-die bandwidth keeps it ahead. AMD’s GMI-Wide setup shows what a bandwidth-focused cross-die link can do, providing excellent bandwidth at low latency.

Bringing both CCDs into play gives Strix Halo a lead over Meteor Lake. I’m starting the test by placing bandwidth load on CCD1 while running the latency test on CCD0. That gives lower latency at bandwidth loads below 60 GB/s because contention at the CCD interface is taken out of the picture. Latency does increase as I spread bandwidth load across both dies, and rises beyond 200 ns as the test approaches die-to-die bandwidth limits. However, a read-only pattern is still limited by cross-die bandwidth and falls far short of the 256 GB/s that the LPDDR5X setup is theoretically capable of.

Advanced packaging may provide latency benefits too. Regular AMD CCDs use SerDes (serializer-deserializer) blocks, which convert signals for transport over lower quality PCB traces. Zen 2’s Infinity Fabric On-Package (IFOP) SerDes for example uses 32 transmit and 40 receive lanes running at a very high clock. Forwarded clock signals per lane data bundle help tackle clock skew that comes up with high speed parallel transmission over wires of unequal lengths. CRC helps ensure data integrity.

All of that adds power and latency overhead. Strix Halo’s InFO_oS packaging doesn’t require SerDes. But any latency advantage is difficult to observe in practice. DRAM requests are the most common type of off-CCD traffic. High LPDDR5X latency masks any latency advantage when looking at DRAM requests, as shown above. Cache coherency traffic is another form of off-CCD traffic, and doesn’t involve DRAM. However, testing that with a “core to core latency” test that bounces cachelines between core pairs also doesn’t provide favorable results for Strix Halo.

A run that produced good cross-CCX latencies

AMD handles cross-CCX cache coherency at Coherent Stations (CS-es) that sit right in front of the memory controllers. Memory traffic is interleaved across memory channels and thus CS instances based on their physical address. I try hitting different physical addresses by testing with various cacheline offsets into a 4 KB page, which gives me different combinations of L3 slices and memory controller + CS pairs. Values within a single run reflect variation based on the tested core pair, while different runs display variation from different memory subsystem blocks owning the tested address.

A run on the worse end with respect to cross-CCX latencies, likely hitting a CS farther away from the CPU endpoints

Cross-CCX latencies on Strix Halo land in the 100-120 ns range depending on the location of the tested core pair, responsible L3 slice, and responsible CS. It’s significantly higher on typical desktop systems or prior mobile chips from AMD. For example, the Ryzen 9 9900X tends to have cross-CCX latencies in the 80-90 ns range, which is in line with prior Zen generations. It’s about 20 ns faster than Strix Halo.

Therefore, I don’t have a satisfactory answer about Strix Halo’s cross-die latency. Latency may indeed be lower at die boundaries. But everything past that boundary has higher latency compared to other client systems, making any advantage invisible to software.

Balancing CPU and GPU Bandwidth Demands

Sharing a memory controller across the CPU and GPU comes with advantages, like making zero-copy behavior more natural to pull off. But it comes with challenges too. CPU and GPU memory requests can contend with each other for DRAM access. Contention surfaces as higher latency. From Zen 4 onward, AMD’s L3 performance monitoring unit (PMU) can measure average latency in nanoseconds for requests external to the core cluster. PMU data isn’t directly comparable to software measurements, because it only accounts for latency after the point of a L3 miss. But it is consistent in slightly under-estimating software observed latency when running a simple latency microbenchmark. When gaming, I typically see low CPU bandwidth demands and correspondingly mild latency increases over the baseline.

The same doesn’t hold true when gaming on Strix Halo’s integrated GPU. Latency rises far above the baseline of around 140 ns. I logged average latency over 1 second intervals, and many of those intervals saw latency figures around 200 ns across several games

I wrote a microbenchmark to investigate how CPU memory latency is impacted by GPU-sde bandwidth load. As with the CPU loaded latency test, I run a latency test thread on a CPU core. But instead of using a read-only pattern, I do a standard C=A+B computation across large arrays on the GPU. To control GPU bandwidth load, I can have each OpenCL kernel invocation do more math with A and B before writing the result to C. Results show increased latency at higher GPU bandwidth demands. Other recent iGPUs show similar behavior.

In-game CPU bandwidth demands are low, but not as low as a simple latency test. I tried running a couple of read bandwidth threads on top of the test above. Strix Halo seems to let its GPU squeeze out the CPU when under extreme bandwidth demands. Latency suffers, passing 300 ns at one point.

Plotting L3 and memory controller PMU data with 1 second intervals helps capture the relationship between latency and bandwidth usage in more complex workloads. The points don’t track well with microbenchmark data collected with a single CPU-side latency test thread. Perhaps there’s enough CPU-side bandwidth demand to cause contention at both the die-to-die interface and the memory controllers. Or maybe, CPU and GPU bandwidth spikes tend to line up within those 1 second intervals. Whatever the case, PMU data highlights how Strix Halo’s CPU cores need high cache hitrates more than their desktop counterparts.

Cyberpunk 2077’s built-in benchmark is largely CPU bound when run at 1080P with medium settings and no upscaling. I used Intel’s Arc B580 on desktop systems, since it has vaguely similar compute power to Strix Halo’s iGPU. Results show a large gap between Strix Halo and AMD’s desktop platform, even though both use the same Zen 5 cores.

Memory latency under load is largely not a problem with CPU-only workloads, even when considering heavily multithreaded ones. Total bandwidth demands are much lower and actually well within the capabilities of a 128-bit DDR5 setup. That explains why AMD was able to take on quad channel HEDT parts using a desktop dual channel platform back in the Zen 2 days. Good caching likely played a role, and Strix Halo continues to have 4 MB of last level cache per core. PMU data from Cinebench, code compilation, and AV1 video encoding loosely align with microbenchmark results. Latency barely strays above the baseline. Y-Cruncher is an exception. It’s very bandwidth hungry and not cache friendly. Its bandwidth demands are several times higher, and often go beyond a dual channel DDR5-5600 setup’s capabilities. Strix Halo is a good choice for that type of workload. But in the client space, bandwidth hungry CPU applications tend to be exceptions.

Final Words: A GPU with an Integrated CPU?

Observations above suggest Strix Halo’s Infinity Fabric and DRAM setup focuses on feeding the GPU and as a result the CPU gets the short end of the stick. High Infinity Fabric endpoint count and a wide LPDDR5X bus provide high bandwidth at high latency. CPU workloads tend to be latency sensitive and contention can make that even worse.

Strix Halo shows AMD can move hundreds of gigabytes per second over Infinity Fabric within mobile power budgets. It’s impressive in that respect, but CPU-side latency is high

Other aspects of the memory subsystem de-prioritize the CPU as well. CPU accesses don’t fill into that cache, but still do a lookup likely to maintain cache coherency with the GPU. That cache lookup at the very least costs power and might add latency, even though it’ll almost never result in a hit. Lack of GMI-Wide style bandwidth is another example.

ASUS’s ROG Flow Z13 placed next to the original Surface Pro for comparison. A hypothetical larger iGPU would be difficult to accommodate in such a form factor, and would face stiff competition from discrete GPU setups

AMD’s decisions are understandable. Most client workloads have light bandwidth requirements. Strix Halo’s memory system design lets it perform well in portable gaming devices like the ROG Flow Z13. But it does make tradeoffs. And extrapolating from those tradeoffs suggests iGPU designs will face steeper challenges at higher performance tiers.

For its part, Strix Halo strikes a good balance. It enjoys iGPU advantages without being large enough for the disadvantages to hurt. I hope AMD continues to target Strix Halo’s market segment with updated designs, and look forward to seeing where they go next.

If you like the content then consider heading over to the Patreon or PayPal if you want to toss a few bucks to Chips and Cheese. Also consider joining the Discord.

I wanted to see how much the NPU XDNA2 performance differs between Halo Strix with its ample bandwidth and the Mainstream Strix-point design or even Kracken.

I wanted to see how much the NPU XDNA2 performance differs between Halo Strix with its ample bandwidth and the Mainstream Strix-point design or even Kracken.

What is SDE? Quote:

GPU-sde bandwidth load