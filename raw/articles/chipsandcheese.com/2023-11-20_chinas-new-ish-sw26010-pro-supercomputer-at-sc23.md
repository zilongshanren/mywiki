---
title: China’s New(ish) SW26010-Pro Supercomputer at SC23
url: https://chipsandcheese.com/p/chinas-newish-sw26010-pro-supercomputer-at-sc23
author: Chester Lam; George Cozma
published: '2023-11-20'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# China’s New(ish) SW26010-Pro Supercomputer at SC23

Computing power has emerged as a crucial national resource. Ever since the first general purpose computer, ENIAC, was used to calculate artillery and bomb ballistics, compute applications have exploded. Today, engineers use computer simulations to cheaply evaluate designs before using more resource intensive validation techniques like building scale models in wind tunnels. Scientists simulate protein interactions to find promising drug formulations before lab testing. Government agencies use supercomputers to forecast weather and climate patterns. A nation with ample computing power can more efficiently leverage its human and material capital to achieve its policy goals.

China is well aware of this and supercomputer development is high on their list of national priorities. Sunway sits front and center in China’s homegrown supercomputer effort. At Supercomputing 23, Sunway is showing off their SW20610-Pro processor which dates back to late 2020 to early 2021. It’s an improved version of the SW20610 featured in their Sunway TaihuLight. TaihuLight is [currently rank 11](https://www.top500.org/system/178764/) on the TOP500 list of most powerful supercomputers. The new Sunway supercomputer looks to take second place, landing just behind the United States Oak Ridge National Laboratory’s new Frontier supercomputer.

To that end, Sunway iterates on a design that focuses almost exclusively on compute density. SW20610-Pro takes SW20610’s basic architecture and scales it up while modernizing off-chip connectivity.

## Chip Level

Sunway’s SW20610-Pro is a many-core processor partitioned into core clusters, called Core Groups, or CGs. (Core Groups, or CGs). A CG consists of 64 Compute Processing Elements (CPEs) on a 4×4 mesh, with four CPEs sharing each mesh stop. A management processor, called a Management Processing Element (MPE), handles communication and spawning threads on the CPEs.

Sunway has no cluster or system level caches. SW20610-Pro’s chip-level organization is identical to the prior SW20610, but with six clusters instead of four.

Each cluster has its own memory controller. In SW20610-Pro, this has been upgraded to a DDR4 controller, offering increased bandwidth compared to the DDR3 setup of the prior generation. From Sunway’s presented numbers, this is likely a dual channel DDR4-3200 setup per cluster. Across all six clusters, Sunway’s SW20610-Pro has 307.2 GB/s of theoretical bandwidth. Memory capacity has been upgraded as well. SW20610-Pro’s clusters get 16 GB of DDR4 each1, compared to 8 GB of DDR3 in SW20610. In total, a chip can access 96 GB of main memory. It’s a noticeable upgrade from the SW26010’s 32 GB.

Sunway’s architecture has similarities to Fujitsu’s A64FX. Both chips offer non-uniform memory access, with each core cluster appearing as a NUMA node. They also use a dedicated management core for each cluster. A64FX’s clusters have fewer cores, but features a 8 MB L2 cache shared across all cores in a cluster. The L2 caches across A64FX can sustain 3.6 TB/s2, while the HBM2 controllers can service L2 misses with 1 TB/s of total bandwidth.

On Sunway’s performance result chart, their new supercomputer is bracketed by the United States’s Frontier and Finland’s LUMI. Both of those leverage AMD’s CDNA 2 architecture with MI250X GPUs, so that architecture will also be a useful comparison. CDNA 2 organizes Compute Units (CUs) into groups, but each group enjoys uniform memory access to the GPU’s entire 64 GB memory pool. Management functions are performed by an attached Zen 3-based Epyc CPU, which can submit commands to the GPU. Four Asynchronous Compute Engines (ACEs) on the GPU then launch threads, or wavefronts, on the shader array. If CDNA 2 works like GCN, each ACE can launch one wavefront per cycle.

All 112 Compute Units on a MI250X die share a 8 MB L2 cache capable of delivering about 3.7 TB/s. L2 misses are handled by a HBM2E setup with 1.6 TB/s of theoretical bandwidth.

## Management Core

CPEs in SW26010 could only run in user mode and don’t support interrupts3. That prevents them from running an operating system, so Sunway’s MPEs take care of launching threads and handling communication. The MPE can run code at different privilege levels and supports interrupts. Since management code is less regular than compute kernels, the MPE has out-of-order execution and a basic cache hierarchy.

SW26010-Pro’s MPEs enjoy a larger L2 cache and higher clock speeds. I wonder if Sunway’s newer chip puts the MPE on a separate clock domain from the CPEs. SW26010 ran both the CPEs and MPE at 1.45 GHz.

SW26010’s MPE has two 256-bit floating point pipes. The newer MPE likely has at least as much throughput. MPE performance isn’t very important because it only has to be fast enough to distribute work to the CPEs and hand off data to the NICs for cross-node communication.

## Compute Architecture

Sunway’s CPEs are small, lightweight cores that focus on maximum vector throughput with minimal power and area. The older SW26010 CPE had a dual pipeline setup with partial out-of-order execution3. Specifically, floating point and memory operations are issued in-order, but the two pipelines can issue instructions out-of-order with respect to each other. Execution latency is high at 7 cycles for basic floating point arithmetic. I assume these parameters are unchanged in SW26010-Pro.

We do know that Sunway increased instruction cache capacity to 32 KB. Sunway uses RISC instructions that are likely 16 bytes long. The 16 KB instruction cache thus has less capacity than a micro-op cache on recent x86 CPUs. Doubling the instruction cache capacity is a good move.

typically 1000 instructions/operations per iteration fitting into the 16 KB CPE I-Cache

Benchmarking SW26010 Many-core Processor


Sunway also doubles vector execution width to 512 bits. Clock speed increases from 1.45 to 2.25 GHz, giving the new Sunway a large increase in per-CPE performance.

Across a whole chip, SW26010-Pro more than quadruples compute throughput over its predecessor. This comes from a combination of more cores, higher clock speeds, and wider vector widths.

In theory, SW26010-Pro offers more compute throughput than Fujitsu’s A64FX. But having lots of wide execution units is one thing. Feeding them is another.

## Cache and Memory Access

Sunway’s SW26010’s CPEs lack a data cache hierarchy. Just like Sony’s Cell processor, each CPE has a 64 KB software managed scratchpad with 4 cycle access latency and 32 bytes per cycle of bandwidth. If data doesn’t fit in the scratchpad, the CPE has to access system memory via DMA commands. 64 KB is a comically small amount of storage, and lack of a proper cache hierarchy meant Sunway SW26010 was severely bottlenecked by memory bandwidth.

In an attempt to tackle the memory bandwidth problem, SW26010-Pro increases scratchpad capacity to 256 KB. Up to half of the scratchpad can be configured as cache, drawing parallels with Nvidia’s GPUs. 256 KB of local storage is better than 64 KB, and rudimentary caching is better than nothing. But next to any other modern design, SW26010-Pro is still terrifyingly memory bound.

Fujitsu’s A64FX has small core-private 64 KB L1 caches backed by a 8 MB cluster-wide L2. AMD’s CDNA 2 architecture has a software managed scratchpad and small 16 KB L1 caches. Then, a 8 MB L2 is shared across all Compute Units on the die. In both cases, a large multi-megabyte L2 cache helps reduce bandwidth demands from main memory. SW26010-Pro lacks such a cache.

## DRAM Configuration: Not Fit for Purpose

HPC workloads have high memory bandwidth demands. A paper by Zhigeng Xu, James Lin, and Satoshi Matsuoka noted that most compute kernels do 16 or fewer floating point operations per byte of memory accessed. The paper characterized SW26010 as being extremely memory-bound.

If we look at memory bandwidth to compute throughput ratios, the old SW26010 is in a poor position. More comparable many-core supercomputer chips like Fujitsu’s A64FX and Intel’s Xeon Phi have massively higher memory bandwidth per FLOP. Compute GPUs like AMD’s MI250X and Nvidia’s H100 may have more trouble feeding their execution units, but only because they’re pushing the limits of what memory technology can offer.

SW26010-Pro increases compute throughput without a corresponding upgrade in memory bandwidth. Specifically, each cluster moves from a 128-bit DDR3-2133 setup to a DDR4-3200 one. It’s a bad joke on several levels. First, it gives SW26010-Pro 0.11 bytes per FP32 FLOP. That’s half the RX 6900 XT’s bandwidth to compute ratio. The 6900 XT is a consumer GPU designed to get by with a low cost memory setup. Somehow, Sunway thought it would be fun to have more compute than a RX 6900 XT but less memory bandwidth, and without the 128 MB last level cache that makes the setup viable.

Worse, the dual channel DDR4-3200 setup attached to each SW26010-Pro core cluster is what you’d find on a last generation desktop.

## Networking Configuration

It’s not just a single chip that matters in a supercomputer, but how all the chips communicate with each other.

High speed communication sets a supercomputer apart from a pile of servers. On a supercomputer, researchers can split a problem across multiple machines (nodes) and use the high speed network to exchange data. A wimpy datacenter Ethernet network might offer 40 or 100 Gbps (5 to 12.5 GB/s) between servers. Supercomputer networks provide an order of magnitude more bandwidth.

Sunway’s SW26010-Pro has decent networking on paper. It comes closer to Fugaku and Frontier than it did when we looked at memory bandwidth. However, achieving that bandwidth is difficult. The network controller has to be fed from main memory, and Sunway’s abysmal memory subsystem strikes again.

The researcher who optimized HPL-MxP originally ran one MPI process per cluster. Each process would then mainly work with the local memory controller, maximizing memory performance. However, you want to overlap computation with network transfers. Each SW26010-Pro cluster only has 51.2 GB/s of bandwidth. Compute and network activity fight for memory bandwidth. The MPE’s caches aren’t large enough and management code ends up eating further into limited bandwidth. The result is poor network utilization.

Rongfen Lin et al5 overcame this by using a single MPI process, dividing each block into 512B sub-blocks, and distributing those sub-blocks across the NUMA nodes to achieve a pseudo-distributed mode. That spreads both compute and network bandwidth demands across SW26010-Pro’s aggregate 307 GB/s of bandwidth, eliminating partition camping issues.

I don’t know how much time this optimization took to code and test, but I can’t imagine it being trivial. I also can’t imagine such an optimization effort being necessary on Fugaku or Frontier. Fugaku has 256 GB/s of bandwidth per partition, more than enough to feed the network interfaces with bandwidth to spare. On Frontier, 100 GB/s of network bandwidth is a rounding error when a single MI250X GCD has 1.6 TB/s of bandwidth. Thus, Sunway’s memory bandwidth issues thus spill over to cross-node communication, and will require more optimization effort than other systems.

### Connecting the Supercomputer

Giving a node high network bandwidth is the first step to building a supercomputer. The next is to get all of your nodes to talk to each other with as much bandwidth as possible. To do this, Sunway retains the general organization of TaihuLight. Sunway’s new supercomputer has 41,140,224 CPEs in total, or 107,136 chips.

Each chip is a node with its own network connectivity. 256 of these nodes are connected to a fast switch, in a level called a Supernode. Sunway says this first level of connectivity provides “unblocked network bandwidth”. Each Supernode connects to a cross-supercomputer interconnect with 48 ports.

Each supernode connects to a central switching network via 48 links. We don’t know the link bandwidth or topology of the central switching network. If we assume all leaf switch ports have the same 56.25 GB/s, each supernode would have a 2.7 TB/s uplink.

Sunway TaihuLight apparently has a network bisection bandwidth of 70 TB/s and a network diameter of 74, suggesting supernodes don’t enjoy equal, unblocked bandwidth to other supernodes. The rest of TaihuLight’s topology is much like that of Sunway’s new supercomputer. It’s a tree with three levels. Thus Sunway uses a similar networking topology to older supercomputers like Summit.

RIKEN’s Fugaku takes a more sophisticated approach with a 6D torus topology. Each node’s bandwidth is divided into six ports. Pairs of ports connect to different switch levels. Bandwidth tapers off as nodes get further apart in the organization.

Fugaku can give each node 34 GB/s up to the highest level axis. For comparison, each node in Sunway’s new supercomputer can get 10.54 GB/s to the global interconnect. Sunway could have higher per-node bandwidth to the rest of the system if only a few nodes in a supernode are communicating. However if a large problem requires more than 256 nodes, you would want to put them in as few supernodes as possible to take advantage of high intra-supernode bandwidth. Thus Fugaku gives each node more than three times as much bandwidth to the global interconnect than Sunway. Large problems should have an easier time scaling across Fugaku.

ORNL’s Frontier uses a three-hop dragonfly topology, where sets of switches are fully connected at each level. I wasn’t able to find information on how much uplink bandwidth each switch has.

## Final Words

Sunway’s new supercomputer is impressive from a theoretical compute throughput standpoint. SW26010-Pro is most similar to Fugaku’s A64FX at the node level, and China’s supercomputer delivers more FP64 throughput than Japan’s while using fewer chips. However, it does so by adopting an almost singular focus on packing as much execution power into each chip as possible.

A SW26010-Pro chip has lots of wide vector execution units but does little to support them. A CPE can’t exploit thread level parallelism and has very limited ability to utilize instruction level parallelism. The memory setup is extremely weak. The result is a chip that requires a lot of optimization effort from the compiler or programmer.

Then we have the memory bandwidth problem. Putting a dual channel DDR4-3200 setup on a 64 CPE SW26010-Pro cluster is unacceptable. Even though the system dates back to 2020 to 2021 era, this memory setup is quite poor. Having over 10 times the compute as a contemporary flagship consumer CPU (Ryzen 9 3950X) with the same memory bandwidth is asking for your system to be severely memory bound in many tasks. A shift to then brand new DDR5 memory standard would still leave the system memory bound. But a 50% bandwidth increase from DDR5-4800 could increase performance by nearly that much, considering how bandwidth bound Sunway is. To truly alleviate these issues the SW26010-Pro should have had a much better cache hierarchy and a HBM setup along with cutting the number of execution units.

Sunway’s new supercomputer therefore feels like a system designed with the goal of landing high on some TOP500 lists. For that purpose, it’s perfect, providing a lot of throughput without wasting money on pesky things like cache, out-of-order execution, and high bandwidth memory. But from the perspective of solving a nation’s problems, I feel like Sunway is chasing a metric. A nation doing well in advanced technology might have a lot of supercomputer throughput, but more supercomputer throughput doesn’t necessarily mean you’ll solve technological problems faster.

At the beginning of the article, I noted that supercomputers are built to let a nation more efficiently leverage its human and material resources to achieve policy goals. There is an opportunity cost problem in using human resources on optimization time. I’m not sure how long Rongfen Lin et al spent manually interleaving HPL-MxP matrices across a node’s memory partitions, but that task would not have been necessary on Fugaku or Frontier. In one sense, I applaud the the hard work and heroic programming effort required to closely fit code to the hardware.

On the other, hardware that requires intricate optimization effort to achieve acceptable performance is not good hardware. Systems like Fugaku or Frontier don’t require as much optimization effort. Out of order execution on A64FX lets its cores dynamically come up with near-optimal instruction schedules. Frontier’s MI250X GPUs can do this in another dimension by exploiting thread-level parallelism. In both cases, simply written code is likely to perform well enough for the researcher to get on with interpreting results, rather than waste weeks iterating on code. And that’s assuming they don’t run up against Sunway’s inherent bandwidth limitations anyway.

Humans build powerful computers not for the sake of building powerful computers, but to let them solve problems faster. Stepping back from supercomputers, a lot of development in computing has been carried out to make problem solving with computers more accessible. Out-of-order execution lets programmers get better performance without manual instruction scheduling. Virtual memory lets users run several programs at once without worrying about one misbehaving program taking down the entire system. If we switch over to software, compilers let programmers keep complex programs organized without having to track what variables are stored in which registers. And garbage-collected languages like C# or Java let developers trade some performance for an easier time coding.

Higher compute performance has the same goal. More compute power lets people use simpler brute force algorithms. But a high performance system can’t just have high on-paper compute power alone. I hope Sunway’s future systems will take a more balanced approach, with more accessible computing power even at the cost of some peak throughput.

If you like our articles and journalism, and you want to support us in our endeavors, then consider heading over to our [Patreon](https://www.patreon.com/ChipsandCheese) or our [PayPal](https://www.paypal.com/donate/?hosted_button_id=4EMPH66SBGVSQ) if you want to toss a few bucks our way. If you would like to talk with the Chips and Cheese staff and the people behind the scenes, then consider joining our [Discord](https://discord.gg/TwVnRhxgY2).

## References

Yuhang Fu et al, “Towards Excascale Computation for Turbomachinery Flows”

Hatem Ltaief et al, “Meeting the Real-Time Challenges of Ground-Based Telescopes Using Low-Rank Matrix Computations”

Zhigeng Xu et al, “Benchmarking SW26010 Many-core Processor”

Jack Dongarra, “Report on the Sunway TaihuLight System”

Rongfen Lin et al, “5 ExaFlop/s HPL-MxP Benchmark with Linear Scalability on the 40-Million-Core Sunway Supercomputer”