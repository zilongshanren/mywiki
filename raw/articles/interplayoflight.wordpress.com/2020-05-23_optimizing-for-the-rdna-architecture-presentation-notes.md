---
title: 'Optimizing for the RDNA Architecture: presentation notes'
url: https://interplayoflight.wordpress.com/2020/05/23/optimizing-for-the-rdna-architecture-presentation-notes/
author: Kostas Anagnostou
published: '2020-05-23'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

AMD recently released a great presentation on RDNA, with a lot of details on the new GPU architecture and optimisation advice.

While watching it I took some notes (like you do in real conferences) and I am sharing them here in case anyone finds them useful. They can be used as a TLDR but I actively encourage you to watch the presentation as well, some parts won’t make much sense without it. I have added some extra notes of my own in brackets [] as well.

**RDNA architecture**

- RDNA introduced in July 2019 with RX 5700
- Design goals include scalability, geometry handling, cache flushing, less amount of work to feel the GPU and latency
- Compute Unit (CU) is replaced by the Work Group Processor (WGP)
- A CU on GCN has 4xSIMD16 units and 1 Scalar unit. Also has dedicated L1 cache, 64 KB LDS cache and texture units
- 4 CUs share one instruction I$ cache and one constant K$ cache
- Each SIMD16 executes 64 thread wavefronts, 16 threads per clock [The threads of a wavefront running on the same SIM16 all execute the same instruction]. A SIMD16 needs 4 clocks to complete the whole wavefront (4 clocks per instruction) [This means that an instruction has a latency of 4 cycles from start to finish. Since a CU unit has 4xSIMD16 it can be viewed as the CU executing a 64 thread wavefront per clock — they are 4 different instructions though].
- Work Group Processor
- 4 SIMD32 units and 4 Scalar units.
- It has access to 2 dedicated L0 caches (equivalent to GCN’s L1 cache), 2 Texture units and 128KB of LDS
- A WGP has its own instruction and constant caches (GCN has one per 4 CU)
- 5 WGPs share one L1 cache (not the same as GCN’s L1 cache)
- Conceptually 1 WGP ~ 2 CUs. A WGP still has more Scalar units and I$ and K$ than 2CUs [so they are not directly comparable]
- Wavefront size is now 32 threads natively. This can be executed on a SIMD32 in one clock cycle [this means that each instruction has now a latency of 1 cycle, instead of 4. Having 4 SIMD32 units a WPG can execute 4 wavefronts (instructions) per clock. It can also issue 64 thread wavefronts (dual issue) at 2 cycles per instruction].
- Geometry throughput is now 4 triangles/clock after culling [limited by the Primitive Assembler], and potentially more than 4 before culling. GCN can do 2-4 tri/clock (pre/post cull).

- Comparison example
- Latest GCN (Vega 64) has 64 CUs, a global L2 cache and HBM2 VRAM memory
- RDNA (RX 5700XT) was 20 WGPs, 4 L1 caches (1 per 5 WGPs) and global L2 cache and GDDR6 VRAM
- L1 cache is a new level of cache, doesn’t exist on GCN (4 levels of cache instead of 3)



**Optimisations**

- Texture Access
- New level of cache (L1)
- A WGP has 2 L0 caches but they are not coherent. 2 SIMD32s are tight to one L0 cache and the other 2 to the other L0 cache.
- This can have an impact if thread group more than 32 threads as each wavefront can be assigned to different SIMD32s [A thread group is a bunch of threads that will be broken down into wavefronts and assigned to various SIM32s within a WGP for execution]
- This means that if the L0 cache fetches some data for a wavefront on one SIMD32 and another wavefront needs the same data but it is on a different SIMD32 the other L0 cache may need to fetch it again. It also means that data can get out of sync if modifying it. In this case the GPU will need to update the data in L1 as well to maintain coherence.

- The L2 cache is used by all WPGs, which means less cache misses and less need to flush data to global memory
- Cache line is now 128 bytes instead of 64. This means that there may be a need to adjust memory alignment.
- Thread indices in a compute shader are organised in row major order (iterate over row elements first and then go to next row). This is equivalent to linear [non-swizzled] texture access.
- Texture access is optimised for swizzled layout (neighbouring texels are adjacent in memory) for cache coherence. We need to transform the thread indexing to approximate this (using
[Morton-like](https://en.wikipedia.org/wiki/Z-order_curve)ordering) [For another example check Bavoil’s[GDC 2019 presentation](https://www.gdcvault.com/browse/gdc-19/play/1026202)].


**Workload distribution**

- On RDNA a shader can run in wave32 or wave64 mode with dual issue. Driver will decide which mode will be used. Don’t assume a specific mode.
- We should still design our shaders for wave64 (allocate threadgroups in multiples of 64. This will also be compatible with GCN.
- Arrange threads within a threadgroup in multiples of 32
- GCN will issue a full wave64 even if some threads are only active.
- RDNA has more flexibility to skip a wave32 in a threadgroup if all its threads are inactive. This is true in wave64 mode as well by temporarily switching to wave32 mode. [in practical terms this means try to group active and inactive threads together in batches of 32, to give the WGP the opportunity to skip the inactive]


**Shader optimisations**

- We can use Local Data Share (LDS) memory to exchange data between threads in a threadgroup.
- Faster than global memory.
- Threads within a single wavefront can use Data Parallel Processing (DPP) or LDS Permute
- Also supported on GCN
- DPP can be used to exchange data between a subset of threads in a wavefront.
- Really fast
- 2 different modes on RDNA
- DPP8: instructions that operate on a group of 8 threads, supporting arbitrary swizzles (a thread can read data from any thread within that group)
- DPP16: instructions that operate on a group of 16. Support a predefined set of swizzles only.

- If we need data exchange operations on more than 16 threads we need LDS permute
- Uses LDS hardware but doesn’t read/write to LDS memory but to a temporary buffer stored in VGPRs.

- Prefer shuffle only across groups of 8 and avoid shuffles across more than 32 threads (compiler will need to resort to slow techniques)
- Use Quad Wave operations (eg QuadReadAcrossX in SM6) to implement the shuffling, they will be implemented with DPP/LDS permute instructions
- Check presentation for example


**Applied optimisations — mip chain generation**

- A texture downsampler for mipmap generation
- Classic multipass approach suffers from bottlenecks due to barriers between mips [the shader must finish writing a mip before it can be used as an input to the next pass]
- Also mip data are written and read from VRAM [which is the slowest memory available to the GPU]
- At lower mips the occupancy becomes low as well [as there is not enough work to fill the GPU].
[FidelityFX SPD sample](https://gpuopen.com/fidelityfx-spd/)uses a single pass in compute shader to generate all mips- Splits the input texture into tiles of 64×64 texels.
- Threadgroups of 256 size downsample a 64×64 tile down to 1×1
- Max texture size supported is 4Kx4k
- Uses only a single, global sync point.
- Does not use any barriers, which also allows it to overlap work from other dispatches/drawcalls in the same queue.
- Uses data exchange between mips with LDS or DPP (except for mip 6)
- Can also use Async on the compute queue to overlap other graphics work
- [More details about the technique
[here](https://github.com/GPUOpen-Effects/FidelityFX-SPD/blob/master/docs/FidelityFX_SPD.pdf)]

**Texture Access**

- Loading texture data is time consuming especially at high resolutions, so access pattern (cache efficiency) matters. This is less important for low res images that fit in the cache.
- Presenter tried different approaches for thread index remapping [check presentation]
- Morton swizzling improves perf by ~8% over row major ordering
- A Morton like, 2×2 swizzle matches standard texture layout, improves cache coherence
- Loading more than 2×2 texels per thread does not improve performance because threads are not fetching neighbouring texels any more
- 2×2 swizzle also allows quad operations.

**Workload & Data Distribution**

- Use a 64×64 tile from mip 0 [original source texture] to calculate a 32×32 mip 1 tile.
- For mip 2 each thread holds 4 output values. Use quad swizzles or LDS to move data between threads.
- The further down we go to the mip the less threads we need. We need to deactivate the unneeded threads, grouping all active threads together to allow the GPU to skip inactive wavefronts (~7% speedup)

**Shader optimisations**

- Data exchange between the mip.
- Access the values of other threads within a wavefront using wave operations
- Idea 1: Each wavefront downsamples a 32×32 patch to 1×1 using ShuffleXor.
- LDS can then be used to shuffle the 4 output values across the 4 threadgroups.
- Assumes threadgroup size of 64. Potentially not a problem.
- On Vulkan when using subgroup operations (like ShuffleXor) wavefront size is fixed to 64 (unless using an extension)
- On DX12, when using wave operations, it can still use either wave32 or wave 64

- Quad Shuffle with ShuffleXor or Quad operations
- Thread 0 can access values from threads 1-3
- Can use DPP8, very performant

- From Mip 2 to Mip 3 thread 0 can access values from threads 4,8,12 with ShuffleXor
- Can use DPP16, still performant

- Mip 3->4, Thread 0 can access values of threads 16, 32, 48
- Can’t use DPP or even LDS permute any more.
- Not performant any more
- Can be ~10% perf drop
- Also requires wavefront size of 64. Not all GPUs are running wavefront size 64.
- But it requires less LDS


- Idea 2: Encourage use of DPP/LDS permute to exchange data between threads, using only quad shuffles.
- saves one round of LDS store and load completely
- Can use DPP8, very performant.
- Average speedup ~3.5%, benefits lower resolution source textures more as they make better use of the cache.
- Quad operations are very compiler dependent
- Require less LDS and less VGPRs, better occupancy

- FP16 can also be used, especially for texture that are 16 bits per channel or less.
- On RDNA filtering of 4-channel fp16 texture is full rate [one texture read per clock]
- Writing and reading fp16 is very efficient.
- FP16 can be beneficial especially for small resolution textures. No difference measured for high resolutions
- 256×256 downsampling offers a ~40% speedup
- 1440×1400 downsampling offers a 0-2% speedup

- FP16 also requires less LDS and VGPRs

**Summary**

- Use compute shaders and recalculate thread indices using Morton-like ordering
- Keep 2×2 pattern per thread.

- Redistribute work in the shaders so as to group active thread togethers to allow the WPG to skip whole inactive wavefronts
- use subgroup operations where possible. Don’t shuffle across more than 32 threads, stick to 8 if possible
- Consider FP16 where applicable.