---
title: AMD RDNA 3.5’s LLVM Changes
url: https://chipsandcheese.com/p/amd-rdna-3-5s-llvm-changes
author: Chester Lam
published: '2024-02-05'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

Integrated graphics have been a key part of AMD’s strategy ever since they bought ATI. Bringing CPU and GPU blocks together in the same chip has given AMD substantial wins, including in Microsoft’s Xbox and Sony’s Playstation. Their Van Gogh chip (found in the Steam Deck) represents yet another console success. Beyond consoles, AMD has consistently offered strong iGPUs in laptop and desktop chips. Their upcoming Strix Point parts look to continue the company’s iGPU efforts.

Here, I’ll be looking at LLVM changes made to support Strix Point. Strix Point is also referred to as GFX11.5, and represents a midpoint between GFX11 (RDNA 3) and GFX12 (RDNA 4). I’m not sure what AMD intends to call Strix Point’s architecture, but I’ll be referring to it as RDNA 3.5 for simplicity.

Strix Point Variants

LLVM changes show two Strix Point variants, gfx1150 and gfx1151. ROCm CLR code comments indicate gfx1150 is “Strix,” and gfx1151 is “Strix Halo.” Strix Halo is likely a higher end version of RDNA 3.5.

The most notable difference between the two variants is that gfx1151 (Strix Halo) has the large vector register file found in high end RDNA 3 products. That is, each SIMD has 192 KB of vector registers. gfx1150 (Strix) has a smaller 128 KB vector register file like lower end RDNA 3 parts.

With that out of the way, let’s get on to RDNA 3.5’s changes.

Single VGPR Use Hints

GPU register files need enormous read bandwidth and high capacity. To meet those requirements while keeping power and area in check, GPU register files are split into banks. The register file can service multiple reads per cycle by sending them to different banks. However, bank conflicts can reduce achievable register file bandwidth, and impact instruction issue rate. GPUs get around this with register file caches.

RDNA 3 has four single ported register file banks, and a register cache based on operand position. Up to RDNA 3, the register cache is managed entirely in hardware. RDNA 3.5 changes this by adding a single VGPR use hint instruction, s_singleuse_vdst. That instruction indicates the subsequent instruction’s inputs will not be reused, and thus caching the operands in the register cache won’t be beneficial. It’s a pretty blunt tool, and seems to apply to all operands in one go.

Nvidia similarly has a register file cache since Maxwell, which stores two registers per operand position. But unlike AMD, Nvidia has instructions opt-in to saving their inputs in the register cache. The compiler can set a reuse flag corresponding to each operand position to tell the hardware to cache the register value. Nvidia’s scheme is more flexible because caching for each operand position can be controlled separately, versus AMD’s all or nothing strategy.

However, AMD’s strategy reduces code size because they avoid specifying reuse flags with every instruction. Each Nvidia instruction since Turing, is an incredible 128 bits long. On AMD, instructions are 32 or 64 bits long, with an optional 32-bit immediate. In the worst case, an AMD instruction would be 96 bits long. Adding the 32-bit s_singleuse_vdst instruction would bring effective instruction length to 128 bits, which is only as bad as Nvidia’s typical case.

GFX12 (RDNA 4) carries this feature forward.

Scalar Floating Point Instructions

AMD’s GPUs have used a scalar unit to offload operations from the vector ALUs since the original GCN architecture launched in 2011. Scalar operations are typically used for addressing, control flow, and loading constants. AMD therefore only had an integer ALU in their scalar unit. RDNA 3.5 changes this by adding floating point operations to the scalar unit.

In summary:

AMD has implemented the most common FP operations in the scalar unit, along with a few less common ones that shouldn’t require too much hardware. More expensive special functions are absent. The scalar FPU cannot do inverse square roots (sometimes used for lighting calculations) or trigonometric functions like sine and cosine. Likely, such operations were too expensive to implement in the scalar unit. Meanwhile, AMD’s willingness to support FP16 across almost all the new FP scalar instructions shows that lower precision data types are getting first class treatment in AMD’s upcoming GPUs.

Adding a FPU to the scalar unit could help offload more work from the vector units, and possibly save some vector registers in the process. That could in turn increase occupancy and latency hiding potential, leading to better performance. The cost is additional die area and power used by the scalar units. A FPU is more expensive than an integer ALU, but improvements in process technologies may have changed the cost-benefit calculation compared to a decade ago.

RDNA 4 carries this feature forward and also has a FPU in the scalar unit. However, special functions do get limited support by adding vector ALU instructions that can write a scalar result. For example, v_s_rsq_f32 will compute the inverse square root of a value stored in a scalar register and write the result back to a scalar register. Evidently duplicating special function hardware is still too expensive even with today’s process nodes.

Two Scalar Inputs for DPP Instructions

DPP (Data Parallel Processing) instructions on RDNA 3.5 can take two scalar inputs, at operand positions src0 and src1. RDNA 3 and prior RDNA generations could only have one scalar input at src0 for DPP instruction. This was a peculiar limitation because plenty of instructions could take two scalar inputs, so the hardware was capable of handling multiple scalar inputs for one instruction.

RDNA 3.5 gets rid of this limitation, and RDNA 4 carries that forward.

Final Words

AMD’s introduction of new features in RDNA 3.5 shows the company is willing to test new features in niche products before a more widespread release. Just as PS5 introduced raytracing support before RDNA 2 launched, RDNA 3.5 debuts ISA features that show up in RDNA 4. Looking at these features in context show a few trends with AMD’s ISA development.

Single use VGPR hints continue a trend where AMD’s making increasing use of compiler-provided hints. RDNA 3 added an s_delay_alu instruction that tells hardware to delay issuing the next instruction from a thread. Likely, RDNA 3’s scheduler optimistically issues instructions and completes dependency checks in a later stage. RDNA 3.5’s single use VGPR hints are another instance of the compiler helping the hardware out with optional hints.

From an old AMD slide, showing GCN blocking a thread’s execution until an instruction completes. RDNA’s back to back issue capability requires hardware to handle RAW hazards

Even with RDNA 3.5 and RDNA 4, AMD uses compiler hints far less than Nvidia. Since Kepler, Nvidia’s hardware requires static scheduling from the compiler for correct operation.

On the scalar side, RDNA 3.5’s improvements continue to make the ISA more flexible. Again, this is part of a long running trend. GCN3 added s_cmp_eq_u64 and s_cmp_ne_u64 to let the scalar ALU compare 64-bit values. Vega added scalar atomics. Adding a FPU to the scalar unit is a logical step forward. AMD is not alone in trying to offload computations from the vector units. Nvidia introduced a uniform datapath with Turing, with similar functionality to AMD’s scalar datapath. While Nvidia has published little information on uniform datapath capabilities, I’ve observed H100 using uniform registers more often than prior generations. Examples include storing array and buffer base addresses, as well as for constant inputs to vector ops.

To close out, I wonder if hardware and software development aren’t so far apart. Branches could be forked off a main RDNA repo, given version tags, and prepared for release. While that happens, the main branch continues to evolve. RDNA 3.5 could be an example of forking a release branch at a later point in the master branch. Doing so incurs additional validation overhead, but perhaps AMD has enough engineering bandwidth to absorb the hit. Or perhaps RDNA 4 was judged too risky to use an APU product targeted for a 2024 release.

If you like our articles and journalism, and you want to support us in our endeavors, then consider heading over to our Patreon or our PayPal if you want to toss a few bucks our way. If you would like to talk with the Chips and Cheese staff and the people behind the scenes, then consider joining our Discord.