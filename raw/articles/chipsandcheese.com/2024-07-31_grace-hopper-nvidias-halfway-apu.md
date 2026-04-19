---
title: Grace Hopper, Nvidia’s Halfway APU
url: https://chipsandcheese.com/p/grace-hopper-nvidias-halfway-apu
author: Chester Lam
published: '2024-07-31'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

Nvidia and AMD are the biggest players in the high performance GPU space. But while Nvidia has a huge GPU market share advantage over AMD, the latter’s CPU prowess makes it a strong competitor. AMD can sell both a CPU and GPU as one unit, and that capability has gotten the company wins in consoles and supercomputers. Oak Ridge National Laboratory’s Frontier supercomputer is one such example. There, AMD MI250X GPUs interface with a custom EPYC server CPU via Infinity Fabric.

Of course, Nvidia is not blind to this situation. They too have a high speed in-house interconnect, called NVLink. Nvidia has also dabbled with bundling CPUs alongside their GPUs. The Nintendo Switch’s Tegra X1 is a prominent example. But Tegra used relatively small CPUs and GPUs to target low power mobile applications. Grace Hopper is an attempt to get Nvidia’s CPU efforts into high performance territory. Beyond providing server-level CPU core counts and memory bandwidth, Grace Hopper comes with Nvidia’s top-of-the-line H100 datacenter GPU

GH200 rendering from Nvidia, showing the CPU on the left and GPU on the right

I’ll be looking at GH200 as hosted on Hydra. GH200 has several variants. The one I’m looking at has 480 GB of LPDDR5X memory on the CPU side, and 96 GB of HBM3 on the GPU side. I’ve already covered Neoverse V2 in Graviton 4, so I’ll focus on implementation differences rather than going over the core architecture again.

System Architecture

GH200 bundles a CPU and GPU together. The Grace CPU consists of 72 Neoverse V2 cores running at up to 3.44 GHz, supported by 114 MB of L3 cache. Cores and L3 cache sit on top of Nvidia’s Scalable Coherency Fabric (SCF). SCF is a mesh interconnect, with cores and L3 cache slices attached to mesh stops.

SCF’s responsibilities include ensuring cache coherency and proper memory ordering. From a core to core latency test, those requirements are satisfied with reasonably consistent latency across the mesh. Latency is generally comparable to Graviton 4’s, which uses Arm’s CMN-700 mesh interconnect.

Core to core latency test on Grace’s CPU

DRAM access is handled by a 480-bit LPDDR5X-6400 setup, which provides 480 GB of capacity and 384 GB/s of theoretical bandwidth. Graviton 4 opts for a 768-bit DDR5-5200 setup for 500 GB/s of theoretical bandwidth and 768 GB of capacity. Nvidia may be betting on LPDDR5X providing lower power consumption, as DRAM power can count for a significant part of a server’s power budget.

GH200’s H100 GPU sits next to the Grace CPU. Even though both are sold as a single unit, it’s not an integrated GPU setup because the two chips have separate memory pools. Opting against an integrated GPU is a sensible decision because CPUs and GPUs have different memory subsystem requirements. CPUs are sensitive to memory latency and want a lot of DRAM capacity. GPUs require high memory bandwidth, but are less latency sensitive. A memory setup that excels in all of those areas will be very costly. GH200 avoids trying to square the circle, and its H100 GPU comes with 96 GB of dedicated HBM3 memory. That’s good for 4 TB/s of theoretical bandwidth, far more than what the LPDDR5X setup can provide.

From Intel’s Hot Chips presentation

Conceptually, GH200’s design is similar to Intel’s Kaby Lake CPU with AMD’s Radeon RX Vega M graphics. That design also packages the CPU and GPU together as one unit. A 4 GB pool of HBM2 memory gives the GPU high memory bandwidth, while regular DDR4 memory gives the CPU high memory capacity and low latency. GH200 of course does this on a much larger scale on both the CPU and GPU side.

But an integrated GPU design has benefits too, mainly allowing for faster communication between the CPU and GPU. Games don’t require much bandwidth between the CPU and GPU, as long as there’s enough VRAM to handle the game in question. But compute applications are different, and can involve frequent data exchange between the CPU and GPU. Therefore, Nvidia connects the two dies with a high bandwidth proprietary interconnect called NVLink C2C. NVLink C2C offers 900 GB/s of cross-die bandwidth, or 450 GB/s in each direction. That’s an order of magnitude faster than a PCIe Gen 5 x16 link.

Besides higher bandwidth, NVLink C2C has hardware coherency support. The CPU can access HBM3 memory without explicitly copying it to LPDDR5X first, and the underlying hardware can ensure correct memory ordering without special barriers. Nvidia is confident enough in their NVLink C2C implementation that HBM3 memory is directly exposed to the CPU side as a NUMA node.

Note that remote bandwidth for Grace Hopper is for CPU-owned memory allocated through standard Linux interfaces, which uses the CPU cores for all data transfer and does not make use of CUDA Copy Engines or other acceleration

Accessing the HBM3 memory pool across NVLink C2C provides comparable bandwidth to AMD’s current generation Zen 4 servers in a dual socket configuration. It’s a good performance, if a bit short compared to the theoretical figures. Bandwidth is still significantly higher than what AWS can achieve between two Graviton 4 chips, and shows the value of Nvidia’s proprietary interconnect. Bandwidth from Grace’s local LPDDR5X pool is also solid, and on par with AMD’s Bergamo with DDR5-4800.

Latency however is poor at nearly 800 ns, even when using 2 MB pages to minimize address translation penalties. That’s a difference of 592 ns compared to accessing directly attached LPDDR5X, which itself doesn’t offer particularly good latency.

Part of this is undoubtedly because HBM isn’t a technology designed to offer good latency characteristics. But testing from the H100 GPU shows about 300 ns of DRAM latency, suggesting HBM3 latency is only a minor factor. NVLink C2C therefore appears to have much higher latency than AMD’s Infinity Fabric, or whatever Graviton 4 is using. Intel’s QPI also offers better latency.

To make things worse, the system became unresponsive during that latency test run. The first signs of trouble appeared when vi, a simple text editor, took more than several seconds to load. Even weak systems like a Cortex A73 SBC usually load vi instantly. Then, the system stopped responding to all keystrokes over SSH. When I tried to establish another SSH session, it probably got past the TCP handshake stage because it didn’t time out. But the shell never loaded, and the system remained unusable. I eventually managed to recover it by initiating a reboot through the cloud provider, but that sort of behavior is non-ideal.

Since GH200 is a discrete GPU, it’s insightful to compare link latency against other discrete GPU setups. Here, I’m using Nemes’s Vulkan uplink latency test, which uses vkMapMemory to map a portion of GPU VRAM into the test program’s address space. Latency is then measured using pointer chasing accesses, just like above.

This comparison is more reasonable, and NVLink C2C offers better latency than some discrete GPU configurations. It lands right between setups with AMD’s RX 5700 XT and HD 7950. Latency with that in mind is quite reasonable. However, CPU code will need to be careful about treating HBM3 memory simply as another NUMA node because of its high latency.

Grace’s Neoverse V2 Implementation

A CPU core architecture’s performance can vary depending on implementation. Zen 4 for example behaves very differently depending on whether it’s in a server, desktop, or mobile CPU. Neoverse V2’s situation is no different, and can vary even more because Arm wants to give implementers as much flexibility as possible.

Grace targets parallel compute applications. To that end, Nvidia opted for a large shared L3 cache and higher clock speeds. Less parallel parts of a workload can benefit from a flexible boost policy, giving individual threads more performance when power and thermal conditions allow. A large L3 might handle better when threads from the same process share data.

Graviton 4 on the other hand has to server a lot of customers while maintaining consistent performance. Neoverse V2 cores on Graviton 4 get a larger L2, helping reduce noisy neighbor effects. Low clock speeds minimize workload-dependent thermal or power throttling, Finally, a higher core count lets Amazon fit more of their smallest instances on a single server. A latency test shows the memory hierarchy differences well.

Latency in cycles is identical up to L2, because that’s part of the Neoverse V2 core design. Differences start to appear at L3, and do so in dramatic fashion. Large mesh interconnects tend to suffer high latency, and high capacity caches tend to come with a latency cost too. L3 load-to-use latency is north of 125 cycles on Grace. With such a high L2 miss cost, I would have preferred to see 2 MB of L2 cache. Graviton 4 and Intel’s Sapphire Rapids both use 2 MB of L2 cache to counter L3 latency. AMD’s Zen 4 does have a 1 MB L2, but has much lower L2 miss costs.

Higher clock speeds do hand Grace an advantage over Graviton 4 when accesses hit L1 or L2. But L3 latency is still sky-high at over 38 ns. Even Intel’s Sapphire Rapids, which also accesses a giant L3 over a giant mesh, does slightly better with 33 ns of L3 latency.

L3 cache misses head to Grace’s LPDDR5X controllers. Latency at that point is over 200 ns. Graviton 4’s DDR5 is better at 114.08 ns, putting it in the same ballpark as other server CPUs.

Bandwidth

Higher clocks mean higher bandwidth, so a Neoverse V2 core in Grace is comfortably ahead of its counterpart in Graviton 4. Cache bandwidth isn’t quite as high as AMD’s, which can be a disadvantage because Nvidia positions Grace as a CPU for highly parallel workloads. Such workloads are likely to be vectorized, and Zen 4 is very well optimized for those cases. Even when both are pulling data from large L3 caches, a Zen 4 core has more bandwidth on tap.

To Nvidia’s credit, a single Grace core can pull more bandwidth from L3 than a Graviton 4 core can. This test uses a prefetcher-friendly linear access pattern. I suspect Grace has a very aggressive prefetcher willing to queue up a ton of outstanding requests from a single core. Single core bandwidth is usually latency limited, and a L2 prefetcher can create more in-flight requests even when the core’s out-of-order execution engine reaches its reordering limits. But even the prefetcher can only go so far, and cannot cope with LPDDR5X latency. DRAM bandwidth from a single core is only 21 GB/s compared to Graviton 4’s 28 GB/s.

When all cores are loaded, Grace can achieve a cool 10.7 TB/s of L1 bandwidth. L2 bandwidth is around 5 TB/s. Both figures are lower than Graviton 4’s, which makes up for lower clock speeds by having more cores. AMD’s Genoa-X has the best of both worlds, with high per-cycle cache bandwidth, higher clock speeds, and 96 cores.

L3 bandwidth is hard to see from this test because Grace and Graviton 4 have a lot of L2 capacity compared to L3. I usually split the test array across threads because testing with a shared array tends to overestimate DRAM bandwidth. Requests from different cores to the same cacheline may get combined at some level. But testing with a shared array does help to estimate Graviton 4 and Grace’s L3 bandwidth.

Grace has over 2 TB/s of L3 bandwidth, putting it ahead of Graviton 4’s 750 GB/s. Nvidia wants Grace to serve bandwidth hungry parallel compute applications, and having that much L3 bandwidth on tap is a good thing. But AMD is still ahead. Genoa-X dodges the problem of servicing all cores from a unified cache. Instead, each octa-core cluster gets its own L3 instance. That keeps data closer to the cores, giving better L3 bandwidth scaling and lower latency. The downside is Genoa-X has more than 1 GB of last level cache, and a single core only allocates into 96 MB of it.

Some Light Benchmarking

In-depth benchmarking is best left to mainstream tech news sites with deeper budgets and full time employees. But I did dig briefly into Grace’s performance.

libx264 uses plenty of vector instructions, and can demand a lot of bandwidth. It’s the kind of thing I’d expect Grace to do well at, especially with the test locked to matching core counts. But despite clocking higher, Grace’s Neoverse V2 cores fail to beat Graviton 4’s.

7-Zip is a file compression program that only uses scalar integer instructions. The situation is no better there, and I ran the test several times despite the clock running on cloud instance time.

Despite using the same command line parameters, 7-Zip wound up executing 2.58 trillion instructions to finish compressing the test file on GH200. On Graviton 4, the same work took a mere 1.86 trillion instructions. libx264’s instruction counts were similar on both Neoverse V2 implementations, at approximately 19.8 trillion instructions. That makes the 7-Zip situation a bit suspect, so I’ll focus on libx264.

…counts cycles in which the core is unable to dispatch instructions from the front end to the back end due to a back end stall caused by a miss in the last level of cache within the core clock domain

Arm Neoverse V2 Technical Reference Manual

Neoverse V2 has a STALL_BACKEND_MEM performance monitoring event. The description for this event is clear if a bit wordy. Let’s unpack it. L2 is the last level of cache that runs at core clock. Therefore, STALL_BACKEND_MEM only considers stalls caused by L3 and DRAM latency. Dispatching instructions from the frontend to the backend is what the renamer does, and we know the renamer is the narrowest part of Neoverse V2’s pipeline. Therefore, the event is counting L2 miss latency that the out-of-order engine couldn’t absorb. And, throughput lost from those events can’t be recovered by racing ahead later elsewhere in the pipeline.

libx264 sees a massive increase in those stalls. Grace’s smaller L2 combined with worse L3 and DRAM latency isn’t a winning combination. Overall lost throughput measured at the rename stage only increased by a few percent. It’s a good demonstration of how Neoverse V2’s large backend can cope with extra latency. But it can’t cope hard enough, nullifying Grace’s clock speed advantage.

The same counters in 7-Zip don’t show such a huge discrepancy, though Grace again suffers more from L2 miss latency. Grace’s poor showing in this workload is largely due to 7-Zip somehow executing more instructions to do the same work.

7-Zip and libx264 don’t benefit from Nvidia’s implementation choices, but that doesn’t mean Grace’s design is without merit. The large 114 MB L3 cache looks great for cache blocking techniques, and higher clocks can help speed up less parallel parts of a program. Some throughput bound programs may have prefetcher-friendly sections, which can be aided by Grace’s prefetcher. Specific workloads may do better on Grace than on Graviton 4, particularly if they receive optimizations to fit Grace’s memory subsystem. But that’s beyond the scope of this brief article.

H100 On-Package GPU

The GPU on GH200 is similar to the H100 SXM variant, since 132 Streaming Multiprocessors (SMs) are enabled out of 144 on the die. VRAM capacity is 96 GB compared to the 80 GB on separately sold H100 cards, indicating that all 12 HBM controllers are enabled. Each HBM controller has a 512-bit interface, so the GH200’s GPU has a 6144-bit memory bus. Even though GH200’s GPU is connected using a higher bandwidth NVLink C2C interface, it’s exposed to software as a regular PCIe device.

nvidia-smi indicates GH200 has a 900W power limit. For comparison, H100’s SXM variant has a 700W power limit, while the H100 PCIe makes do with 350-400W. GH200 obviously has to share power between the CPU and GPU, but the GPU may have more room to breathe than its discrete counterparts when CPU load is low.

Compared to the PCIe version of the H100, GH200’s H100 runs at higher clocks, reducing cache latency. Otherwise, the H100 here looks a lot like other H100 variants. There’s large L1 cache backed by a medium capacity L2. H100 doesn’t have a gigantic last level cache like RDNA 2, CDNA 3, or Nvidia’s own Ada Lovelace client architecture. But it’s not a tiny cache either like on Ampere or other older GPUs.

VRAM latency sees a very substantial improvement, going down from 330 ns to under 300. It’s impossible to tell how much of this comes from higher clock speeds reducing time taken to traverse H100’s on-chip network, and how much comes from HBM3 offering better latency.

Bandwidth also goes up, thanks to more enabled SMs and higher clock speeds. Unfortunately, the test couldn’t get past 384 MB. That makes VRAM bandwidth difficult to determine. If things worked though, I assume GH200 would have higher GPU memory bandwidth than discrete H100 cards.

Further tests would have been interesting. I wanted to test CPU to GPU bandwidth using the GPU’s copy engine. DMA engines can queue up memory accesses independently of CPU (or GPU) cores, and are generally more latency tolerant. Nemes does have a test that uses vkCmdCopyBuffer to test exactly that. Unfortunately, that test hung and never completed.

Checking dmesg showed the kernel complaining about PCIe errors and graphics exceptions. I tried looking up some of those messages in Linux source code, but couldn’t find anything. They probably come from a closed source Nvidia kernel module. Overall, I had a frustrating experience exercising NVLink C2C. At least the Vulkan test didn’t hang the system, unlike running a plain memory latency test targeting the HBM3 memory pool. I also couldn’t use any OpenCL tests. clinfo could detect the GPU, but clpeak or any other application was unable to create an OpenCL context. I didn’t have the same frustrating experience with H100 PCIe cloud instances, where the GPU pretty much behaved as expected with Vulkan or OpenCL code. It’s a good reminder that designing and validating a custom platform like GH200 can be an incredibly difficult task.

Final Words

Nvidia’s GH200 and Grace CPU is an interesting Neoverse V2 implementation. With fewer cores and a higher power budget, Grace can clock higher than Graviton 4. But rather than providing better per-core performance as specifications might suggest, Grace is likely optimized for specific applications. General consumer workloads may not be the best fit, even well vectorized ones.

Previously I thought Arm’s Neoverse V2 had an advantage over Zen 4, because Arm can focus on a narrower range of power and performance targets. But after looking at Grace, I don’t think that captures the full picture. Rather, Arm faces a different set of challenges thanks to their business model. They don’t see chip designs through to completion like AMD and Intel. Those x86 vendors can design cores with a comparatively narrow set of platform characteristics in mind. Arm has to attract as many implementers as possible to get licensing revenue. Their engineers will have a harder time anticipating what the final platform looks like.

Arm evaluated Neoverse V2 in an emulation environment that drastically differs from Grace and Graviton 4. Slide from Arm’s Hot Chips 2023 presentation

So, Neoverse V2 can find itself having to perform in an environment that doesn’t play nice with its core architecture. Nvidia’s selection of a 1 MB L2, high latency L3, and very high latency LPDDR5X present Neoverse V2 with a spicy challenge. As covered in the Graviton 4 article, Neoverse V2 has similar reordering capacity to Zen 4. I think Zen 4 would also trip over itself with 125 cycles of L3 latency and over 200 ns of memory latency. I don’t think it’s a coincidence that every Zen 4 implementation has a fast L3. Intel is another example, Golden Cove can see 11.8 ns of L3 latency in a Core i7-12700K, or 33.3 ns in a Xeon Platinum 8480+. Golden Cove has much higher reordering capacity, making it more latency tolerant. In a server environment, Golden Cove gets a 2 MB L2 cache as well.

GH200’s GPU implementation deserves comment too. It should be the most powerful H100 variant on the market, with a fully enabled memory bus and higher power limits. NVLink C2C should provide higher bandwidth CPU to GPU communication than conventional PCIe setups too.

But it’s not perfect. NVLink C2C’s theoretical 450 GB/s is difficult to utilize because of high latency. Link errors and system hangs are a concerning problem, and point to the difficulty of validating a custom interconnect. Exposing VRAM to software as a simple NUMA node is a good north star goal, because it makes VRAM access very easy and transparent from a software point of view. But with current technology, it might be a bridge too far.

Even though it’s not an iGPU, Grace Hopper might be Nvidia’s strongest shot at competing with AMD’s iGPU prowess. Nvidia has already scored a win with Amazon and the UK’s Isambard-AI supercomputer. AMD’s MI300A is shaping up to be tough competition, with a win in Lawrence Livermore National Laboratory’s upcoming El Capitan supercomputer. MI300A uses an integrated GPU setup, which speeds up CPU to GPU communication. However, it limits memory capacity to 128 GB, a compromise that Nvidia’s discrete GPU setup doesn’t need to make. It’s good to see Nvidia and AMD competing so fiercely in the CPU/GPU integration space, and it should be exciting to see how things play out.

If you like our articles and journalism, and you want to support us in our endeavors, then consider heading over to our Patreon or our PayPal if you want to toss a few bucks our way. If you would like to talk with the Chips and Cheese staff and the people behind the scenes, then consider joining our Discord.

Previously I thought Arm’s Neoverse V2 had an advantage over Zen 4, because Arm can focus on a narrower range of power and performance targets. But after looking at Grace, I don’t think that captures the full picture. Rather, Arm faces a different set of challenges thanks to their business model. They don’t see chip designs through to completion like AMD and Intel. Those x86 vendors can design cores with a comparatively narrow set of platform characteristics in mind. Arm has to attract as many implementers as possible to get licensing revenue. Their engineers will have a harder time anticipating what the final platform looks like.

Just sharing my thoughts.

From a pure product marketing perspective, using just the x86 vendors wouldn't allow me to rebrand my products to a much higher-price point tier.

The pros of taking ARM's IP is that from their end customers perspective they can "rebrand" it as their own custom design as a selling point or sort of.

Big buzz statements like:

"Revolutionary CPU Core Design" || "industry leading power consumption"

That only works to the "untrained investors", because going deeper down you would most likely uncover that ARM CSS Gensis fingerprints all over it.

Under Final Words section:

Previously I thought Arm’s Neoverse V2 had an advantage over Zen 4, because Arm can focus on a narrower range of power and performance targets. But after looking at Grace, I don’t think that captures the full picture. Rather, Arm faces a different set of challenges thanks to their business model. They don’t see chip designs through to completion like AMD and Intel. Those x86 vendors can design cores with a comparatively narrow set of platform characteristics in mind. Arm has to attract as many implementers as possible to get licensing revenue. Their engineers will have a harder time anticipating what the final platform looks like.

Just sharing my thoughts.

From a pure product marketing perspective, using just the x86 vendors wouldn't allow me to rebrand my products to a much higher-price point tier.

The pros of taking ARM's IP is that from their end customers perspective they can "rebrand" it as their own custom design as a selling point or sort of.

Big buzz statements like:

"Revolutionary CPU Core Design" || "industry leading power consumption"

That only works to the "untrained investors", because going deeper down you would most likely uncover that ARM CSS Gensis fingerprints all over it.