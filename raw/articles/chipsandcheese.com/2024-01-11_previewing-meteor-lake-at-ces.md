---
title: Previewing Meteor Lake at CES
url: https://chipsandcheese.com/p/previewing-meteor-lake-at-ces
author: Chester Lam
published: '2024-01-11'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# Previewing Meteor Lake at CES

Intel has been using a hybrid core strategy for years in a bid to leverage their bigger engineering budget to corner AMD. Specifically, P-Cores focus on maximizing per-thread performance. E-Cores avoid pursuing diminishing returns and take less power and area. That in turn lets Intel implement more E-Cores to increase multithreaded performance.

Meteor Lake extends the hybrid core strategy by adding a third core type, the low power E-Core. Here, we’ll be taking a brief look at all three core types with some limited testing done at CES, courtesy of Cheese.

On the tested chip, the P-Cores appeared to be running at 4.7 GHz, the E-Cores at 3.77 GHz, and the low power E-Cores at 2.48 GHz. The chip may not be final.

## P-Core Cache and Memory Access

Redwood Cove largely inherits Raptor Cove’s core-private cache setup. The 48 KB L1 data cache has 5 cycle latency. Then, a 2 MB L2 cache with 16 cycle latency serves as a mid-level cache, and helps insulate the core from L3 latency. For comparison, Zen 4’s 32 KB L1D cache has 4 cycle latency. AMD then uses a 1 MB L2 with 14 cycle latency to serve as a mid-level cache.

Meteor Lake’s L3 no longer services the iGPU as it did on prior Intel designs. Instead, the iGPU sits on a separate tile and has an independent path to the memory controller. That means the iGPU doesn’t have to power up the ring bus to access memory, and the CPU’s L3 has fewer clients. However, those changes didn’t help L3 latency, which increases from 60 to 71 cycles. AMD still has a faster L3 cache, but that comes at the cost of capacity on AMD’s Phoenix APU.

Meteor Lake’s P-Core ran at similar frequencies to the Raptor Lake engineering sample Seby tested for us in 2022. Therefore, actual L1 and L2 latencies are similar. L3 latency increases from 12.5 ns to 15 ns, which is slightly disappointing.

Intel enjoys good L2 latency compared to AMD’s Phoenix. HP decided to limit the Ryzen 7 7840HS to 4.5 GHz, so Intel’s higher clock speeds partially compensate for the longer L2 access pipeline. At L1 and L3, AMD continues to enjoy a latency advantage, though again AMD’s caches are smaller.

Memory latency is always iffy to evaluate on pre-production samples. Meteor Lake here is using a LPDDR5X-7467 configuration which results in poor latency.

### Bandwidth

Again private caches show similar bandwidth characteristics. Like Golden Cove and Raptor Cove, Redwood Cove can do three 256-bit AVX loads per cycle. Combined with high clock speeds, that gives Redwood Cove a sizeable L1 bandwidth advantage over AMD’s Zen 4. Intel then has a 64 byte per cycle interface to L2 compared to AMD’s 32 byte per cycle one, which continues to put Intel ahead.

However, AMD enjoys more L2 miss bandwidth. A single Zen 4 core can pull over 120 GB/s from L3. Meteor Lake’s regresses L3 bandwidth for a single core, dropping from Raptor Lake’s 100 GB/s to 81 GB/s. It’s not a bad performance by any means, and understandable considering the L3 latency regression. However, it would have been nice to see the same level of L3 bandwidth, or even an improvement.

Single core memory bandwidth regresses too, from 30 GB/s on Raptor Lake to 25.3 GB/s on Meteor Lake. Again latency is likely a culprit. A core can only track so many cache misses, and bandwidth is probably latency limited.

## E-Core Cache and Memory Access

Like the P-Cores, Meteor Lake’s Crestmont E-Cores have similar caches to the prior generation Gracemont cores. A 32 KB L1 cache has excellent 3 cycle latency. L1 misses can be serviced by a 2 MB L2 shared by a cluster of four E-Cores. Both Meteor Lake and Raptor Lake have 20 cycle latency for their E-Core L2 caches, but Meteor Lake disappointingly only has half as much L2 capacity. Raptor Lake’s 4 MB L2 caches should provide higher performance. Meteor Lake may be prioritizing area efficiency.

L3 cache access takes a couple more cycles on Meteor Lake compared to Raptor Lake. I would have liked to see Meteor Lake’s L3 perform better considering its lower capacity. But E-Core L3 latency doesn’t regress by as much as it did on the P-Cores, so that’s something I guess.

As with Gracemont, Crestmont’s 3 cycle L1 data cache enjoys better actual access time, with the shorter pipeline more than making up for the core’s slower clock. It also beats out AMD’s Zen 4, at least when AMD’s chip is running at 4.5 GHz. Crestmont’s L2 latency is mediocre at 5.21 ns, but the slower increase in latency as the test moves through the L2 region suggests Intel has changed up L2 cache’s replacement policy.

At L3, E-Cores on both Raptor Lake and Meteor Lake see 16.6 ns of latency. It’s not great, but E-Cores are not meant to achieve maximum performance. Higher latency is understandable, particularly if multithreaded loads are more likely to be bandwidth rather than latency limited. Finally, memory latency shows similar characteristics to what we saw with the P-Cores. LPDDR5(x) is probably responsible for massively higher latency compared to desktop DDR.

### Bandwidth

Individually, E-Cores don’t have a lot of cache bandwidth. That situation persists going from Raptor Lake to Meteor Lake, but Meteor Lake takes slight regressions. Despite similar clock speeds (as evidenced by nearly identical L1 bandwidth), Meteor Lake’s E-Cores have a bit less L2 bandwidth. Intel’s smaller L2 will also reduce effective bandwidth as more accesses have to be served from L3.

In L3 sized test points, Meteor Lake again suffers a small bandwidth regression. Finally, reduced single core bandwidth from memory is likely due to higher memory latency.

## Low Power E-Core

Meteor Lake’s low power E-Core is positioned to fill the same role as A5x cores on mobile SoCs. It’s not meant to provide any extra performance or even achieve better power efficiency for long running workloads. Instead, it features very low power consumption and hopes to handle background tasks that aren’t CPU heavy without powering up the Compute Tile.

The low power E-Core are logically identical to the E-cores on the Compute Tile. The only difference between the two cores is the different physical design due to the LP E-Cores being on TSMC’s N6 node instead of on Intel’s i4 node like the compute tile. Just like the E-Core on the compute tile, there’s a 32 KB 3 cycle L1 and a shared 20 cycle 2 MB L2. However because the low power E-Cores are meant to handle tasks without powering up the Compute Tile, they’re not clients of the L3 so L2 misses go directly to memory.

Actual latency is high due to low clock speeds. L2 cache latency is nearly 8 ns. Memory latency is poor at over 200 ns. Even though the low power E-Cores are closer to the memory controller, the memory access path is probably optimized for low power rather than performance.

### Bandwidth

E-Cores are not built to be heavy hitters in throughput bound vector workloads, and that especially applies to the low power E-Cores. Bandwidth is low throughout the cache hierarchy due to both lower clocks and narrower datapaths. L1 bandwidth is jut under 80 GB/s, or around 32 bytes per cycle. A core can read 24-25 bytes per cycle from L2 as with the regular E-Cores. Lower clocks put actual L2 bandwidth just above 62 GB/s.

A single low power E-Core can achieve just under 9 GB/s of memory read bandwidth. Again this puts it behind regular E-Cores.

## Core to Core Latency

Multi-core CPUs have to maintain a coherent view of memory even though individual cores have separate caches. If a core needs to see data that another core has written to its private cache, the interconnect has to pull off a cache to cache transfer. We can time how long that takes by bouncing a cacheline between two cores using compare and swap operations.

P-Cores enjoy the lowest latency for such operations. As with Alder Lake, bouncing cachelines between E-Cores is slower. However, the E-Cores no longer appear as separate quad core clusters. Coherency is likely handled in the same manner for all E-Cores.

Low power E-Cores see very high core to core latency. Bouncing a cacheline within the low power E-Core cluster takes nearly 100 ns, and doing so between the low power E-Cores and the Compute Die takes even longer.

Intel’s prior Alder Lake hybrid architecture sees better core to core latencies in absolute terms. Even with the tested cacheline homed to a L3 slice far away from the E-Cores, worst case latency is still under 60 ns.

I wonder if Meteor Lake is running the ring interconnect at a lower clock than Alder Lake or Raptor Lake.

## Final Words

Meteor Lake’s data side cache hierarchy isn’t a dramatic improvement over Raptor Lake’s. Latency is similar or worse, and the same applies to bandwidth. Intel likely opted for a conservative approach with cores and cache while they were busy redoing their high level chip architecture. Making too many changes at once is always risky, and Intel found out years ago what would happen if the company told engineering teams to bite off more than they could chew.

I suspect Intel tried to optimize battery life in common laptop use cases like video conferencing, light web browsing, and messaging. CPU speed isn’t important in those tasks. Powering off the entire Compute Tile with its cores, cache, and ring interconnect could provide substantial power savings. Heavy tasks like video encoding, rendering, code compilation, and gaming won’t benefit from Meteor Lake’s design. Those are best left to hard hitting desktop CPUs, and Raptor Lake already fills that position.

We would like to thank Intel for letting us preview Meteor Lake as well as giving Dr. Ian Cutress a laptop that he graciously allowed us to do some more testing on.

If you like our articles and journalism, and you want to support us in our endeavors, then consider heading over to our [Patreon](https://www.patreon.com/ChipsandCheese) or our [PayPal](https://www.paypal.com/donate/?hosted_button_id=4EMPH66SBGVSQ) if you want to toss a few bucks our way. If you would like to talk with the Chips and Cheese staff and the people behind the scenes, then consider joining our [Discord](https://discord.gg/TwVnRhxgY2).