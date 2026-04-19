---
title: Ryzen Z1’s Tiny iGPU
url: https://chipsandcheese.com/p/ryzen-z1s-tiny-igpu
author: Chester Lam
published: '2024-02-26'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

Editor’s Note: Just like our prior Ryzen Z1 article, the ROG Ally was kindly provided by Asus to let us test the Ryzen Z1.

ASUS ROG Ally comes in two configurations: AMD’s Ryzen Z1 Extreme and the Ryzen Z1. The Ryzen Z1 Extreme uses AMD’s high-end Zen 4 APU configuration, with eight Zen 4 cores and six RDNA 3 WGPs. Its non-extreme cousin uses a hybrid two Zen 4 + four Zen 4c CPU configuration and a much smaller iGPU with two RDNA 3 WGPs. We’ve covered the Ryzen Z1’s CPU side in a prior article. Here, we’ll be going over the iGPU.

Compared to Radeon 780M in the Ryzen Z1 Extreme, the Ryzen Z1’s Radeon 740M is much smaller. It’s also smaller than the Steam Deck’s iGPU, which uses four RDNA 2 WGPs. However, Ryzen Z1 does enjoy AMD’s newer RDNA 3 architecture. It’s also allowed to boost to very high clock speeds, while the Steam Deck’s iGPU is limited to 1.6 GHz.

Compute Throughput

WGPs, or Workgroup Processors, are the basic building blocks of AMD’s RDNA 3 graphics architecture. RDNA 3 introduces dual issue capability for a variety of common FP32 instructions, doubling the theoretical FP32 throughput. Shader programs can leverage its dual issue capability by using wave64 mode or special dual issue instructions in wave32 mode. On RDNA hardware, pixel shaders often use wave64 mode, in which 2048-bit vectors execute on the WGP’s 1024-bit execution units over 2 clock cycles, but achieve 1 instruction per cycle throughput on operations with dual issue support. Wave32 mode lets individual threads (waves) finish faster as 1 instruction per cycle throughput becomes the general case. However, taking advantage of RDNA 3’s extra FP32 units in wave32 mode requires the compiler to find dual issue pairs. That requires instruction-level parallelism within a basic block, and could be upended by register cache source port or result bus limitations.

I’ll be using Nemes’s Vulkan benchmark suite because the Steam Deck’s iGPU doesn’t support OpenCL, in which my own tests are written. AMD’s compiler uses wave64 for the instruction rate tests in this suite, making it a good showcase for RDNA 3’s increased FP32 throughput.

Even though the Radeon 740M has only two WGPs, dual issue capability and much higher clock speeds give it more FP32 throughput than the Steam Deck’s iGPU. When RDNA 3’s dual issue ability doesn’t come into play, the two chips are much closer. That applies to special functions like inverse square roots. FP16 throughputs are nearly identical as well, because both RDNA 2 and RDNA 3 can pack two FP16 values into the low and high halves of a 32-bit register and do FP16 math at double rate.

AMD’s higher-end Ryzen Z1 Extreme dramatically outpaces the Ryzen Z1’s iGPU in all categories. The Z1 Extreme enjoys the same RDNA 3 advantages as the Z1, and also runs at high clock speeds.

Games primarily use floating point operations, but integer instructions often show up in shader code too. There, RDNA 3 largely behaves like RDNA 2. The Ryzen Z1’s iGPU again uses high clock speeds to catch up with the Steam Deck’s nominally larger iGPU.

Cache and Memory Latency

GPUs use massive thread-level parallelism to hide memory latency. RDNA 2 and 3’s SIMDs are capable of 16-way SMT as long as enough vector register and local data share capacity are available. A WGP with four SIMDs can thus track up to 64 independent instruction streams. But even with thread-level parallelism and a bit of instruction-level parallelism mixed in, memory latency often limits performance.

Therefore, cache is critical for performance. RDNA uses a sophisticated triple-level cache hierarchy. Each half of a WGP gets a L0 vector cache. A set of WGPs share a L1 mid-level cache, and a L2 cache is shared across the entire GPU. Discrete RDNA 2 and RDNA 3 cards additionally have a large Infinity Cache. For example, the RX 6900 XT has 128 MB of Infinity Cache.

Higher clock speeds and RDNA 3’s larger L0/L1 sizes give the Ryzen Z1 a latency advantage over the Steam Deck. Ryzen Z1’s lead continues as the test spills into DRAM. ROG Ally’s LPDDR5 memory configuration doesn’t suffer from high latency like the Steam Deck. We saw that on the CPU side already, and testing confirms the same on the GPU side.

AMD GPUs since GCN have a separate scalar memory path to load values constant across a wavefront. The scalar path helps take load off the vector caches, and is better optimized for latency. RDNA 3 has a 16 KB first-level scalar cache just like prior AMD GPUs, but the larger 256 KB L1 still helps.

As with the vector path, the Ryzen Z1’s iGPU enjoys better scalar memory latency than the Steam Deck’s iGPU thanks to higher clocks. Compared to the Ryzen 780M in the Z1 Extreme, the Z1’s Ryzen 740M shows similar latency characteristics. However, AMD’s lower-end part does see L2 cache capacity cut from 2 MB to 1 MB. Valve’s Steam Deck also has 1 MB of L2 for the iGPU, as do older AMD iGPUs like the Vega iGPU in Renoir. The Z1 Extreme may need a larger L2 because its higher compute throughput requires more bandwidth. Higher L2 hitrate is a good way to achieve that higher bandwidth.

Cache and Memory Bandwidth

GPUs need high bandwidth to keep their wide vector execution units fed. The Ryzen Z1’s iGPU has first-level cache bandwidth similar to the Steam Deck’s iGPU, but gets there via high clocks instead of having more cache instances. As the test spills out into L1 and L2, the Radeon 740M maintains that high bandwidth because those lower level caches also run at higher clocks. In contrast, the Steam Deck’s iGPU and the Ryzen Z1 Extreme’s Radeon 780M have noticeably less L1 and L2 bandwidth per Compute Unit. Of course, the Z1 Extreme has higher bandwidth at each cache level and a larger L2 cache.

iGPUs are traditionally limited by their DRAM configuration, which has to be shared with the CPU. LPDDR4 and LPDDR5 provide a large bandwidth increase compared to the DDR4 setups of years ago, enabling larger iGPU designs and PC gaming handhelds. The non-Extreme Ryzen Z1 gets similar LPDDR5 benefits without being a large iGPU, and thus gets a very good memory bandwidth to compute ratio.

Measured bandwidth at 512 MB test size divided by measured FP32 FMA FLOPs. If we don’t consider RDNA 3’s FP dual issue capability, the 740M would have 0.06 DRAM bytes per FP32 FLOP.

In contrast, Ryzen Z1 Extreme’s very large and fast iGPU outpaces advances in memory bandwidth. DRAM bytes per FLOP is low compared to the Infinity Cache equipped RX 6900 XT, even if we factor out RDNA 3’s dual issue capability. That’s why the Radeon 780M gets a 2 MB L2 cache. The Steam Deck’s iGPU and the Ryzen Z1’s Radeon 740M in contrast make do with a 1 MB L2 because they have ample memory bandwidth relative to their compute throughput.

CPU to GPU Link Bandwidth

Integrated GPUs are often less powerful than their discrete cousins thanks to DRAM limitations. However, they do have an advantage when moving data between CPU and GPU memory spaces because they won’t be restricted by a relatively slow PCIe link.

All three AMD APUs tested here achieve similar performance, with the Steam Deck’s APU technically pulling ahead when the copy engine is in use. Achieved bandwidth is well above the 32 GB/s available with a PCIe 4.0 x16 link, so these integrated GPUs could have an advantage if the CPU and GPU need to communicate a lot. That’s unlikely to matter for gaming, but it could matter if a compute application has to process GPU-generated results on the CPU.

If we use a compute shader to move data between CPU and GPU memory, the Ryzen Z1 does fall behind a bit. That’s likely because its smaller shader array can’t keep as much work in flight to hide latency. Using a CPU-side memcpy to move data between host memory and a buffer mapped to GPU memory results in very low bandwidth. CPU cores are less latency tolerant than GPU ones, and there could be other inefficiencies when CPU cores directly access GPU memory.

Final Words

Gamers Nexus notes that ASUS’s non-Extreme ROG Ally gives up a lot of GPU performance for a $100 price drop, especially when the Ryzen Z1 Extreme’s iGPU can stretch its legs in docked mode. In that respect, it’s similar to the Steam Deck, which similarly gets outpaced by the Z1 Extreme when the latter is given enough power budget. On the flip side, the gap narrows on battery power. There, the Z1’s smaller iGPU can maintain high clocks even with a smaller power budget.

That leaves me with mixed feelings about the Ryzen Z1 as a gaming chip. Its Radeon 740M is a demonstration of how high clocks can let a small GPU go far. On the other hand, this “speed demon” advantage only works when tight power budgets prevent larger GPUs from reaching similar clocks. Performance on battery is definitely important for a portable device like the ROG Ally or Steam Deck. But those devices can spend a lot of time plugged into the wall at the airport or coffee shops. Even car and airplane seats have power outlets available, so a handheld can run in turbo mode on the go.

For those situations, the iGPU in the Ryzen Z1 feels small for a gaming first device. The two-WGP Radeon 740M is only one step up from the minimal single WGP setup in Zen 4 desktop CPUs (Raphael). For sure, the Radeon 740M has a fully fleshed out cache setup instead of Raphael’s minimal 64 KB L1 and 128 KB L2. But even Renoir from a few years ago has a wider iGPU. Meanwhile, Ryzen Z1’s CPU is very strong for a low-power chip. Two Zen 4 cores provide excellent responsiveness, while the four Zen 4c cores maintain good multi-threaded performance.

Ryzen Z1’s priorities can be seen in die area allocated for the iGPU’s WGPs versus its CPU cores. TechPowerUp states the Ryzen Z1 occupies 137 mm2. Pixel counting indicates the two WGPs occupy about 5.1 mm2 of area, while the Zen 4 and Zen 4c cores occupy 17.2 mm2 (not counting shared cache). The Van Gogh APU in Valve’s Steam Deck in contrast uses 10.9 mm2 to implement four Zen 2 cores and 17.7 mm2 for four RDNA 2 WGPs. GPU performance is often more important than the CPU side, especially in handhelds that aren’t expected to hit high frame rates. Therefore, the Ryzen Z1’s die area allocation is strange for a handheld focused chip.

However, packing six Zen 4(c) cores worth of CPU power is great if you need a very low power, very small chip for mobile device that focuses on productivity first and gaming second. Ryzen Z1 can serve in a handheld console in a pinch, and I don’t think ASUS made the wrong decision to use it in the ROG Ally. But I think Ryzen Z1 would be more at home in a small ultrabook or convertible. And it’d be cool to see AMD’s small APU shine in such a device.

If you like our articles and journalism, and you want to support us in our endeavors, then consider heading over to our Patreon or our PayPal if you want to toss a few bucks our way. If you would like to talk with the Chips and Cheese staff and the people behind the scenes, then consider joining our Discord.