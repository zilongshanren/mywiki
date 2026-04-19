---
title: Dynamic Register Allocation on AMD's RDNA 4 GPU Architecture
url: https://chipsandcheese.com/p/dynamic-register-allocation-on-amds
author: Chester Lam
published: '2025-04-05'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

Modern GPUs often make a difficult tradeoff between occupancy (active thread count) and register count available to each thread. Higher occupancy provides more thread level parallelism to hide latency with, just as more SMT threads help hide latency on a CPU. But while a CPU can use all of its SMT threads regardless of what code it's running, the same doesn't apply to GPUs. GPU ISAs offer a large number of very wide vector registers. Storing all registers for all thread slots would be impractical because register files must balance capacity with speed and die area usage.

For example, RDNA 4's ISA lets instructions address up to 256 vector general purpose registers (VGPRs). Each register is 1024 bits wide in wave32 mode, and each RDNA 4 SIMD has 16 thread slots. The SIMD would need a 512 KB register file to hold 256 registers for all 16 threads. In practice register requirements vary across different GPU workloads. RDNA 4, like many other GPUs, uses a smaller register file and allocates depending on what threads require. Code that needs a lot of registers can do so at the cost of less thread-level parallelism, while code that uses fewer registers can run more active threads and be less sensitive to latency. RDNA 4 desktop GPUs have a 192 KB register file per SIMD, so a GPU kernel can use all thread slots (achieve maximum occupancy) if it uses 96 or fewer vector registers.

A bigger register file obviously improves the occupancy and register usage tradeoff situation. RDNA increased SIMD register file capacity to 128 KB, up from 64 KB on GCN. RDNA 3 introduced a 192 KB register file configuration for high end GPUs, where die area is likely less of a concern. But that strategy isn’t efficient for raytracing.

AMD notes that ray traversal and hit/miss handling have different VGPR requirements. AMD uses an inline raytracing model where all raytracing stages run within the same thread. A raytracing shader’s VGPR allocation has to be set to the maximum that any stage requires, because a thread’s register allocation remains static throughout its lifetime. Even if code that needs a lot of registers only accounts for a small part of execution time, that high VGPR allocation will limit active thread count for the duration of the workload. Raytracing is particularly latency sensitive, and AMD would like to run as many threads (rays) in parallel as possible to help absorb latency.

Dynamic Register Allocation

Therefore RDNA 4 introduces a new dynamic VGPR allocation mode. In this mode, a thread starts with a minimum VGPR allocation and changes it throughout it’s lifetime. Rather than specify how many VGPRs a shader will use, the driver tells GPU to launch it in dynamic VGPR mode. A chip-wide SQ_DYN_VGPR register directly sets active thread count per SIMD, or occupancy, rather than having that inferred from shader VGPR usage. SQ_DYN_VGPR also controls other dynamic VGPR mode parameters, like VGPR allocation block size and deadlock avoidance mode.

As defined in Linux kernel code. I couldn’t find references/usages in either Linux or LLVM, so I’m guessing what each field does

Each enabled thread slot gets a single reserved VGPR block, and a newly launched thread starts with just that VGPR block active. When the thread needs more registers, it requests a new VGPR count using a s_alloc_vgpr instruction. s_alloc_vgpr attempts to allocate more registers if called with a value higher than the current allocation, or frees registers if called with a lower value. Changing VGPR allocation affects the upper end of the usable VGPR range, just like with non-dynamic VGPR allocation. Hardware hands out VGPRs in blocks of 16 or 32, depending on how the driver sets up SQ_DYN_VGPR. A thread can allocate up to eight blocks, so the driver must select the larger block size and give up some allocation granularity if a thread needs to use more than 128 VGPRs.

Allocation requests don’t always succeed. s_alloc_vgpr sets the Scalar Condition Code (SCC) to indicate success, or clears it on failure. SCC is analogous to a flag register on CPUs, and is used for branching and add-with-carry. Shader code has to check SCC to determine if an allocation request succeeded. If an allocation request fails, a shader could in theory try to find other useful work to do while periodically retrying the allocation. But doing so would be quite complex, so in practice a shader will busy-wait until allocation succeeds.

Example of dynamic register allocation used in the DirectX procedural geometry example

Therefore dynamic VGPR mode turns the occupancy question on its head. A SIMD can have as many active threads as the driver feels like, regardless of register allocation. But theoretical occupancy doesn’t tell the whole story. Threads can still get blocked waiting on VGPR allocation. A SIMD could have all thread slots filled, but some of those threads could be busy-waiting on VGPR allocation rather than making useful progress.

Deadlock Avoidance

Busy-waiting can become more than a performance inconvenience. Dynamic VGPR allocation can lead to deadlock. AMD knows this, and describes how that can happen in RDNA 4’s ISA manual.

I think a deadlock case can be more general than what AMD describes. If every thread in a SIMD needs to allocate more registers, but hardware doesn’t have enough free registers to satisfy any request, every thread will get stuck forever. That’s a deadlock, even if there are technically registers available.

AMD mitigates some deadlock scenarios with a deadlock avoidance mode. The ISA manual is light on details, only saying it reserves just enough VGPRs for one thread to reach maximum VGPR allocation at all times. Each thread can allocate up to eight VGPR blocks, and one block comes reserved with the thread slot, so deadlock avoidance mode would reserve 7 VGPR blocks. I believe deadlock avoidance mode works by only allowing one thread to allocate registers from the reserved pool at a time. In short:

Base case: No reserved registers allocated. Any request can proceed

From (1), any combination of allocation requests from all threads will allow at least one thread (say thread A) to succeed

From (2), no other thread can allocate from the reserved pool, allowing thread A to increase its register allocation to the maximum should it need to.

Eventually A will leave its high register usage code section, or terminate completely, and thus free up registers for other threads to do the same.

Needless to say, that situation isn’t great for performance because it can serialize useful work across threads. But getting to the finish line slowly is better than not getting there at all.

Deadlock avoidance mode isn’t foolproof. If the programmer manages to meet three conditions:

Two threads need to allocate registers

The high register usage sections of both threads depend on each other, for example in a producer consumer model

No other thread can give up their registers until the two threads above make progress

Then they can run into a deadlock even with deadlock avoidance mode enabled. Programmers should probably avoid cross-thread dependencies in dynamic VGPR mode, unless they’re confident threads only wait on each other in low VGPR usage sections.

Dynamic VGPR Mode Limitations

As with many new features, dynamic VGPR mode isn’t a one-size-fits-all solution. It’s narrowly targeted to start, and can only be used with wave32 compute shaders. Graphics shaders like pixel and vertex shaders can only use the regular non-dynamic launch mode. The same goes for wave64 shaders of any type.

A workgroup of threads launched in dynamic VGPR mode will “take over” the equivalent of a GPU core. That would be a Workgroup Processor (WGP) in WGP mode, or a Compute Unit (CU) in CU mode. Thus dynamic and non-dynamic threads can’t coexist on the same GPU core.

Registers used to specify various compute program launch parameters

Dynamic VGPR mode may be less efficient at using register file capacity. Each enabled thread slot gets a reserved VGPR block, regardless of whether a thread is actually running in that slot. A workload that doesn’t have enough parallelism to fill all enabled thread slots would waste those reserved registers. Deadlock avoidance mode would set aside more registers that could have been easily allocated in non-dynamic mode. Drivers can reduce reserved register count by disabling deadlock avoidance mode or reducing thread slot count. Both of those options come with obvious downsides. In wave32 mode, non-dynamic register mode can allocate up to 256 registers in 24 entry blocksa on current RDNA 4 GPUs. That offers finer granularity than the 32 entry blocks needed to give a thread 256 registers in dynamic VGPR mode.

Nvidia’s Dynamic Register Allocation

AMD isn’t the only GPU maker that lets a thread adjust register allocation mid-execution. Nvidia introduced a setmaxnreg PTX instruction in Hopper, and that’s carried forward to Blackwell consumer GPUs. setmaxnreg superficially acts like AMD’s s_alloc_vgpr, letting the calling thread request a different register allocation. However Nvidia’s dynamic register allocation works very differently from AMD’s, and is probably better called register reassignment. Nvidia for their part never gave this mechanism a name.

Nvidia doesn’t use a separate launch mode. Kernels always launch the regular way, with a specified register allocation that also determines how many threads they can run concurrently. For example a compute shader that uses 96 registers on Blackwell will only be able to run 5 concurrent threads in each SM sub-partition. After threads launch, they can call setmaxnreg to shift registers between threads in the same workgroup. Unlike s_alloc_vgpr, setmaxnreg‘s register pool is whatever the workgroup started out with. If every thread calls setmaxnreg and requested register count across threads is greater than what the workgroup started with, they will deadlock regardless of how much free space the register file may have.

As an aside, setmaxnreg is a PTX instruction. PTX in an intermediate level programming language for Nvidia GPUs with an assembly-like syntax. It isn’t assembly, which Nvidia calls SASS. However PTX is meant to give more control over emitted instructions than a C-like high level language. Therefore PTX instructions often have similarities with SASS instructions, and can offer hints about the underlying ISA.

The semantics around setmaxnreg suggest Nvidia’s mechanism is geared towards tightly orchestrated register swapping between threads. It’s not like AMD’s free-flowing dynamic allocation behavior where different threads can be out-of-phase with each other, so to speak. Nvidia’s “warpgroup” likely refers to threads sharing the same SM sub-partition, and thus the same register file.

The same setmaxnreg instruction must be executed by all warps in a warpgroup. After executing a setmaxnreg instruction, all warps in the warpgroup must synchronize explicitly before executing subsequent setmaxnreg instructions. If a setmaxnreg instruction is not executed by all warps in the warpgroup, then the behavior is undefined

A determined developer could emulate AMD’s initial dynamic VGPR state on Nvidia by with a workgroup that allocates all register file capacity in a SM, then immediately has every thread trim its allocation down to the minimum. But after that, synchronization requirements on Nvidia would make it difficult to emulate AMD’s independent allocation behavior. setmaxnreg‘s scalar-only input makes it harder to look up a desired allocation value from memory. Of course difficult doesn’t mean impossible. A register input can be emulated with a sufficient application of conditional branches, but let’s not think about that too much.

Not Hopper or Blackwell, but have a Nvidia related image to spice things up. I’m sick of seeing AI generated images everywhere, so I’m going to start taking more pictures with my DSLR and post them

In exchange for less flexibility, Nvidia should have no problem mixing “dynamic” and regular threads on the same SM. Nvidia can also adjust register allocation with finer granularity than AMD. The latter can be especially important because Nvidia has smaller 64 KB register files, and waste from “slack” register file usage can be even more painful.

Nvidia’s register reassignment mechanism isn’t well suited for AMD’s raytracing use case. However, Nvidia’s raytracing design likely doesn’t need it. Nvidia hardware uses a DXR 1.0 raytracing model. If it works like Intel, raytracing stages execute as separate thread launches on the SMs. Regular vector register allocation that happens at each thread launch would already solve the problem AMD faces with all-in-one raytracing shaders.

And Intel?

Intel’s documentation explicitly states that raytracing stages execute as separate thread launches. But even if they didn’t, Intel would benefit less from dynamic register allocation than AMD. Intel GPUs used fixed register allocation until very recently. Each thread gets 128 registers whether it needs them or not. More recent GPUs like Battlemage add a “large GRF” mode that cuts occupancy in half to give each thread 256 registers. There’s no option in between.

Intel’s Arc B580

Therefore Intel can maintain full occupancy with a higher per-thread register count than either AMD or Nvidia. Dynamic VGPR allocation is only useful if it helps increase occupancy in the first place – that is, the GPU can’t achieve full occupancy with non-dynamic VGPR allocation. If Intel were to dynamically allocate registers, the very coarse register allocation granularity may result in a more threads getting blocked than on AMD.

Final Words

AMD’s dynamic VGPR allocation mode is an exciting new feature. It addresses a drawback with AMD’s inline raytracing technique, letting AMD keep more threads in flight without increasing register file capacity. That in turn makes RDNA 4 less latency sensitive in raytracing workloads, likely with minimal power and area cost. Raytracing shaders that use more than 96 VGPRs are attractive targets for the dynamic VGPR feature.

Profiling Quake 2 RTX under Radeon Graphics Profiler. AMD chose to use fully inlined raytracing shaders, and no dynamic VGPR allocation, despite the shader being limited to 9 threads (out of 16 slots) due to VGPR usage.

Raytracing shaders on AMD can either inline all raytracing stages, or use an “indirect” mode where different stages are executed in separate function calls. So far, I’ve only seen AMD use dynamic VGPR allocation in indirect mode. Raytracing stages all take place within the same thread in both modes, but perhaps function call sites provide a convenient place to adjust VGPR allocation. After all, a function has clearly defined entry and exit points. AMD often prefers to inline raytracing stages to avoid function call overhead. I have not seen dynamic VGPR mode used when raytracing stages are inlined, even when raytracing shader occupancy is VGPR limited.

The RX 9070 provided by AMD

Certainly s_alloc_vgpr isn’t limited to function call sites, so I wonder if future AMD drivers will be more trigger-happy with dynamic VGPR mode. Conversely, AMD uses dynamic VGPR allocation in indirect mode even when non-dynamic allocation could have achieved full occupancy. Doing so shouldn’t hurt performance, but it does suggest driver decisions aren’t so fine grained at the moment.

Setting “Disable raytracing shader inlining” using AMD’s tools makes the driver use raytracing shaders with function calls, which also use dynamic register allocation. Done here to illustrate effect on occupancy

Generic compute workloads could benefit from dynamic VGPR mode too, assuming AMD does work to expose the feature through various toolchains. Some of Nvidia’s GPGPU libraries take advantage of setmaxnreg, so there’s probably compute applications for AMD’s dynamic VGPR feature too.

At a higher level, features like dynamic VGPR allocation paint a picture where AMD’s GPU efforts are progressing at a brisk pace. It doesn’t feel like an easy feature to implement. Thread register allocation could be non-contiguous in the physical register file, complicating register addressing under the hood. Features like deadlock avoidance would demand additional work. With regards to raytracing, dynamic VGPR allocation shows there’s plenty of progress to be made within AMD’s single-shader raytracing model. Along with breaking false cross-wave memory dependencies, AMD seems determined to keep stamping out performance limiters with each generation.

If you like the content then consider heading over to the Patreon or PayPal if you want to toss a few bucks to Chips and Cheese. Also consider joining the Discord.

a. RDNA 4’s ISA manual indicates the 24 register allocation granularity only applies to devices with 1536 VGPRs per SIMD, or 192 KB register files. Other RDNA 4 devices allocate VGPRs in blocks of 16 registers, and likely have a 128 KB register file. RDNA 3 used smaller 128 KB register files in lower end devices, reserving 192 KB register files for the highest end SKUs. As RDNA 4 SKUs with non-192 KB register files do not exist at the time of writing, there is no need to discuss them in the article proper. However, such devices may launch in the future and it’s something to be aware of.

"CP is very slow on GFX12 and parsing the packet header is the main bottleneck. Using paired context regs reduce the number of packet headers and it should be more optimal.

It doesn't seem worth when only one context reg is emitted (one packet header and same number of DWORDS) or when consecutive context regs are emitted (would increase the number of DWORDS)."

Thank you very much!

It's good to see, there is someone who pays appropriate attention to analyze hardwares in depth.

Interesting observation...

"CP is very slow on GFX12 and parsing the packet header is the main bottleneck. Using paired context regs reduce the number of packet headers and it should be more optimal.

It doesn't seem worth when only one context reg is emitted (one packet header and same number of DWORDS) or when consecutive context regs are emitted (would increase the number of DWORDS)."

https://www.phoronix.com/news/AMD-RDNA4-Paired-Context-Regs