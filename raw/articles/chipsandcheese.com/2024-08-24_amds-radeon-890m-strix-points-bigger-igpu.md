---
title: 'AMD’s Radeon 890M: Strix Point’s Bigger iGPU'
url: https://chipsandcheese.com/p/amds-radeon-890m-strix-points-bigger-igpu
author: Chester Lam
published: '2024-08-24'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# AMD’s Radeon 890M: Strix Point’s Bigger iGPU

AMD’s iGPUs have seen plenty of recent success. Handheld gaming devices like Valve’s Steam Deck and Asus’s ROG Ally both use AMD integrated graphics. AMD’s last generation mobile offering, codenamed Phoenix, already did well against Intel and Qualcomm’s competing products. Strix Point, AMD’s latest mobile chip, looks to continue that strong performance. It gets an even larger GPU than before, along with a slight architecture upgrade.

We previously covered RDNA 3.5’s architecture changes in a [separate article](https://chipsandcheese.com/2024/02/04/amd-rdna-3-5s-llvm-changes/), so be sure to check that out. The Ryzen AI 9 HX 370’s Radeon 890M is designated GFX1150, which corresponds to the cut down variant of RDNA 3.5 with 128 KB vector register files.

### Acknowledgments

We would like to thank ASUS for providing a laptop for review.

## Overview

GPUs from AMD’s RDNA line are built from Workgroup Processors (WGPs), which vaguely correspond to cores from the CPU world. The Radeon 890M has eight WGPs. AMD used six WGPs in two prior generations of iGPUs, so Strix Point gets a substantial increase in GPU size.

Strix Point’s GPU side memory subsystem remains very similar to the one on Phoenix. WGPs are partitioned into two shader arrays, each with a 256 KB L1 mid-level cache. Each L1 cache instance now serves four WGPs instead of three. The entire iGPU shares a 2 MB L2 cache, and connects to the rest of the chip via four 32 byte per cycle Infinity Fabric ports. Infinity Fabric is AMD’s network-on-chip, and can run at up to 2 GHz on Strix Point. A 4x32B/cycle link may feel like overkill, but it lets Infinity Fabric run at a less aggressive 1.6 GHz while still giving the iGPU access to full LPDDR5 bandwidth. Since a large part of a chip’s power budget can be consumed doing data transfers, running the interconnect at a lower frequency could help save power during graphics workloads.

AMD continues to use a LPDDR5-capable memory controller, with support for up to LPDDR5-7500. Our test device from Asus uses exactly that, providing 120 GB/s of theoretical bandwidth. While Phoenix’s memory controller can support the same speed, the fastest Phoenix memory configuration we tested with was LPDDR5-6400 in the Ryzen Z1 Extreme. Intel’s Meteor Lake does get a similarly high bandwidth LPDDR5-7467 configuration in the Asus Zenbook 14 OLED.

## Cache and Memory Characteristics

Cache latency on Strix Point’s iGPU is almost exactly a match for its predecessor. Higher clock speeds do put AMD’s latest iGPU ahead by a hair. Compared to Intel’s Meteor Lake, AMD continues to use more cache levels than its competitors. Meteor Lake has a large and fast first level cache, backed by a L2 with twice as much capacity as AMD’s.

DRAM latency has also improved, though the difference between Strix Point and Phoenix again isn’t large. Meteor Lake suffers much higher DRAM access latency from its iGPU.

In AMD tradition, RDNA 3.5 has a scalar memory access path. Testing with scalar accesses doesn’t show any surprises. The scalar path offers lower latency, with AMD’s mid-level L1 matching Meteor Lake’s first level L1. AMD’s 16 KB scalar cache therefore acts like a L0 cache of sorts, even though AMD only applies that designation to the vector cache.

Strix Point’s memory subsystem needs to provide more bandwidth to feed its extra compute, and AMD doesn’t disappoint. First level cache bandwidth scales with WGP count, and is much higher. The mid-level L1 caches get a bit more strain because each instance now serves four WGPs instead of three, but that’s still within the capabilities of AMD’s L1 design, as AMD’s high end 7900 XTX also makes one L1 instance handle four WGPs.

L2 bandwidth continues to be impressive at 1.7 TB/s, though the increase here is minor compared to Phoenix. Meteor Lake has less cache bandwidth across the board, though its larger L2 cache does give it an advantage. Intel’s iGPU L2 has less bandwidth than AMD’s, but 1 TB/s is still nothing to sneeze at.

With LPDDR5-7500, Strix Point gets 96.11 GB/s of measured bandwidth from Vulkan. That’s somewhat better bandwidth than Meteor Lake or Phoenix, which got 87.08 and 85.58 GB/s respectively. It’s a hair behind Qualcomm’s Snapdragon X Elite, which feeds its Adreno GPU with top end LPDDR5X and achieves 97.82 GB/s. Stepping back, it’s impressive how modern iGPUs have comparable bandwidth to low end GDDR5-equipped GPUs of the past. The GTX 1050 for example got 76.26 GB/s. LPDDR has done a lot to enable faster iGPUs.

Valve’s Steam Deck is another notable comparison. Even though it launched two years ago, the Steam Deck is still a current generation product. However, the Steam Deck’s APU is sorely dated, with a small RDNA 2 GPU running at a very low 1.6 GHz clock. 1.6 GHz is well below the efficiency sweet spot on desktop RDNA 2 products.

As a result, Van Gogh has far less cache bandwidth than modern contenders. Adreno X1 is an exception, with very poor cache bandwidth for a current generation iGPU.

Besides the global memory hierarchy backed by DRAM, GPU code can explicitly keep frequently used data in on-chip local memory. Local memory is local to each workgroup in OpenCL, but in exchange offers guaranteed low latency and high bandwidth. AMD implements local memory with a 128 KB Local Data Share (LDS) in each WGP. Total LDS bandwidth is quite high for an integrated GPU, stopping just short of 5 TB/s.

LDS latency has significantly improved, and it’s not just from a slight clock speed bump. It’s a welcome change, and puts RDNA 3 well ahead of its immediate competitors.

Local memory can also be used to exchange data between a workgroup’s threads. With a thread-to-thread latency test, RDNA 3.5 acts like RDNA 3. There’s little difference between pointer chasing latency within a single thread, and data exchanges between threads. That’s a good thing, because it means RDNA 3.5’s low LDS latency benefits atomics too.

Global memory atomics are more generally applicable because they allow data exchange between any of a kernel’s threads. Latency is higher of course because transfers can’t be kept in a WGP. However, Strix Point’s iGPU manages to improve latency with global memory atomics despite its increased size.

## Compute Throughput

RDNA 3.5 inherits RDNA 3’s dual issue mechanism, which lets one wavefront start 64 FP operations per cycle. That can be done either with wave64 mode, or dual issue instructions in wave32 mode. Strix Point’s GPU is also scaled up compared to Phoenix’s. As a result, AMD has packed massive compute throughput into an iGPU. The Radeon 890M pushes past 5 TFLOPS, and past 10 TFLOPS if you count a fused multiply-add as two operations. It’s a clear improvement over Phoenix, and often on a different planet compared to the still current generation Steam Deck APU.

With special function operations like inverse square roots, Strix Point has less of a relative advantage because RDNA 3(.5)’s dual issue doesn’t apply. Still, having a bigger and much higher clocking GPU counts for a lot.

Integer operations often show up in games too, and the Radeon 890M is no slouch with those. It’s a stark contrast when compared to what we saw in Qualcomm’s Adreno X1, which generally had poor integer performance. Strix Point does well even with 64-bit integers, which are rarely used in games. GPUs typically do 64-bit integer adds with two 32-bit add-with-carry instructions, and it seems like those instructions execute at full rate here.

## CPU to GPU Bandwidth

Integrated GPUs like the one on Strix Point are more power and area constrained than their discrete desktop counterparts. But sharing a memory bus with the CPU does come with an advantage when moving data between CPU and GPU memory spaces.

With `clEnqueueWriteBuffer`

or `clEnqueueReadBuffer`

, Strix Point can use its LPDDR5 controller to get nearly 38 GB/s of copy bandwidth. It’s comfortably above the 32 GB/s that a PCIe 4.0 x16 link would offer. AMD also pulls ahead of Meteor Lake with a similarly high bandwidth LPDDR5 configuration, perhaps indicating AMD has better DMA engines.

## Compute: FluidX3D

FluidX3D simulates fluid behavior. Performance can be highly dependent on memory bandwidth, assuming the GPU in question is able to meet a baseline level of compute performance.

Strix Point’s iGPU does very well, stepping ahead of Phoenix and Meteor Lake’s iGPUs. It also moves ahead of Nvidia’s Pascal based GTX 1050 3 GB, showing the strength of LPDDR5 for latency tolerant GPU workloads. However, gains are minor because the workload is bandwidth bound.

## Cyberpunk 2077

Cyberpunk 2077 is a modern DirectX 12 game. At low settings and 1080P resolution, the Radeon 890M turns in a good performance. It clearly steps ahead of Phoenix, already had a solid iGPU.

A larger GPU needs a larger power budget to shine, and Asus’s laptop is able to give it exactly that. Battery discharge rate as measured through HWInfo was around 50W. It’s quite a bit higher than the battery discharge rate on the Meteor Lake, Phoenix, and Snapdragon X Elite laptops tested. But it’s worth it, because AMD does get more FPS per watt than the Snapdragon X Elite.

If Strix Point’s SoC power gets pulled back to 15W for 20-21W of battery draw, average FPS drops to 30 FPS. At that point, AMD’s newest GPU is able to maintain competitive performance with Intel’s Meteor Lake at lower power.

## Final Words

As the latest installment in AMD’s iGPU journey, the RDNA 3.5 iGPU in Strix Point does its job well. Performance improves compared to AMD’s already solid iGPU in Phoenix. Other than having more GPU cores running at slightly higher clock speeds, Strix Point doesn’t change a lot compared to its predecessor. RDNA 3.5’s improvements are welcome, but they’re minor as expected for a half-generation update. AMD’s GPU-side cache and memory subsystem uses the same strategy as before.

It’s a bit boring considering Intel has a larger L2 cache, and Qualcomm is playing with a 6 MB System Level Cache on their Snapdragon X Elite (of which about 2.5 MB appears usable to the iGPU). But boring might be the best answer here. Phoenix undeniably did well despite having less last level cache than its competitors. Strix Point appears to do the same, comfortably outdoing its competition. AMD is able to feed its iGPU with less caching, and without going for the most expensive LPDDR5X memory around. Making sweeping changes is always risky, as Netburst and AMD’s own Bulldozer have shown. With Strix Point, AMD is not fixing things that aren’t broken.

Strix Point’s move to RDNA 3.5 does show that AMD is focusing harder on the iGPU side than before. Not too long ago, AMD iGPUs would use hilariously out of date graphics architectures. AMD launched the Cezanne chip in 2021 with Vega graphics, which is largely similar to the original GCN architecture that launched in 2011. In 2021, AMD’s desktop discrete GPUs used the RDNA 2 architecture. Longer ago, AMD launched Trinity APUs with Terascale 3 graphics when their desktop GPUs had already moved to GCN.

With Strix Point, AMD’s mobile iGPU has a newer graphics architecture than its desktop counterparts. It’s an unprecedented situation, but not a surprising one. Since the DX11 era, AMD has never been able to take and hold the top spot in the discrete GPU market. Nvidia has been building giant chips where cost is no object for a long time, and they’re good at it. Perhaps AMD sees lower power gaming as a market segment where they can really excel. Strix Point seems to be a reflection of that.

LLVM commits also support a higher end RDNA 3.5 variant, designated GFX1151 and referred to as “Strix Halo”. Of course adding LLVM support does not mean a product is on the way. But it shows AMD is looking very seriously at what they can do with big integrated GPUs. And I look forward to seeing how AMD’s mobile graphics strategy plays out.

Again, we would like to thank ASUS for sending us over a ProArt PX13 for review and if you like our articles and journalism, and you want to support us in our endeavors, then consider heading over to our [Patreon](https://www.patreon.com/ChipsandCheese) or our [PayPal](https://www.paypal.com/donate/?hosted_button_id=4EMPH66SBGVSQ) if you want to toss a few bucks our way. If you would like to talk with the Chips and Cheese staff and the people behind the scenes, then consider joining our [Discord](https://discord.gg/TwVnRhxgY2).