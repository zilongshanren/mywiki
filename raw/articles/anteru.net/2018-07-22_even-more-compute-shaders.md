---
title: Even more compute shaders
url: https://anteru.net/blog/2018/even-more-compute-shaders
published: '2018-07-22'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Looks like this became a small series about GPU compute, and this week I’m going to wrap it up by discussing execution units and caches. I highly recommend reading [part one](https://anteru.net/blog/2018/intro-to-compute-shaders) and [part two](https://anteru.net/blog/2018/more-compute-shaders) first, as I’ll be referencing those regularly.

Caches and execution units, where should we start? Let’s take the execution units first.

## Issue ports

If you’re familiar with modern CPU design, you know that a CPU is not a scalar thing processing one instruction at a time. A modern CPU architecture like [Zen](https://en.wikipedia.org/wiki/Zen_(microarchitecture)) has **10** issue ports, split between integer and floating point:

GPUs also take advantage of multiple issue ports, but not in the same way as CPUs. On a CPU, instructions get executed out-of-order, and some of them speculatively at that. This is not feasible on a GPU. The whole out-of-order machinery with register renaming requires even more registers, and GPUs already have tons of registers (a Vega10 GPU has for instance a whopping 16 MiB of registers on the die.) Not to mention that speculative execution increases power usage and that’s already a heavily limiting factor for GPUs running very wide workloads. Finally, GPU programs don’t look like CPU programs to start with – out-of-order, speculation, prefetching and more is all great if you’re executing GCC, but not for ye old pixel shader.

That said, it totally makes sense to issue memory requests while the SIMD is busy working on data, or execute scalar instructions concurrently. So how can we get those advantages without going out-of-order? The advantage we have on a GPU over a CPU is that there is a ton of work in flight. Just as we take advantage for this for hiding memory latency, we can also exploit this for scheduling. On a CPU, we look ahead on a single instruction stream and try to find independent instructions. On a GPU, we already have tons of independent instruction streams. The easiest way to get instruction-level parallelism is to simply have different units for different instruction types, and issue accordingly. Turns out, that’s exactly how GCN is set up, with a few execution ports per CU:

In total, there are six distinct execution ports, and the dispatcher can send one instruction to up to five of them per cycle. There are some special-case instructions which are handled in the dispatcher directly (like no-ops – there’s no use in sending them to a unit.) At each clock cycle, the dispatcher looks at the active waves, and the next instruction that is ready. It will then send it to the next available unit. For instance, let’s assume we have code like this executing:

```
v_add_f32 r0, r1, r2
s_cmp_eq_i32 s1, s2
```


If there are two waves ready, the dispatcher will issue the first `v_add`

to the first SIMD. In the next cycle, it will issue the `s_cmp`

from the first wave, and the `v_add`

from the second wave. This way the scalar instruction overlaps with the execution of the vector instruction, and we get instruction level parallelism without any lookahead or expensive out-of-order machinery.

Let’s look at a more complete example, with multiple wavefronts executing a decent mix of scalar, vector, and memory instructions:

One last thing before we wrap this up is handling of loads and stores. On a CPU, it’s all transparent, you can write a sequence like this:

```
mov rcx,QWORD PTR [rsp+0x8]
add rdx, rcx
```


This will just work, because the CPU “knows” that the load needs to finish before the operation can start by tracking this information. On a GPU, tracking which register is written by a load would require a lot of extra hardware. The solution the GPU folks came up with is moving this problem “one level up”, into the shader compiler. The compiler has the required knowledge, and inserts the waits for loads manually. In GCN ISA, a special instruction – `s_waitcnt`

– is used to wait until a certain number of loads has finished. It’s not just waiting for everything, as this allows piping in multiple loads simultaneously and then consuming them one-by-one. The corresponding GCN ISA would look somewhat like this:

```
s_buffer_load_dword s0, s[12:15], 0x0 ; load a single dword
s_waitcnt lgkmcnt(0) ; wait for the previous
; load to finish
v_add r0, s0, r1 ; consume the loaded data
```


I think a good idea is to think of a (GCN) GPU as a CPU, running four threads per core (compute unit), and each thread can call scalar, vector and other instructions. It’s in-order, and the designers made a trade-off between hardware and software complexity. Instead of requiring expensive hardware, a GPU requires massively parallel software – not just to hide latency, but also to take advantage of all execution units. Instead of “automatic” tracking, it requires the compiler to insert extra operations, and requires the application to provide enough parallelism to fully utilize it, but at the same time, it provides massive throughput and tons of execution units. It’s a nice example how the properties of the code you’re executing can influence the design of the hardware.

## Caches

Speaking of software influencing hardware, we should also talk about caches. GPU caches are yet another – and in this series, the final – example of how a GPU was built for massively parallel workloads, and what trade offs the designer have taken compared to a CPU. We’ll also realize that CPUs are actually following the same path as GPUs along the way!

### CPUs

Let’s start by looking at how a modern CPU looks like, for example, a 32-core server CPU built on the Zen architecture:

That’s a huge CPU right there, and interestingly, the topology does matter for high performance code. Two cores sharing the same L3 can obviously exchange data right there, while going into another L3 already requires some traveling – not to mention moving across dice. That’s simply the nature of the beast, as larger and larger chips are also becoming larger in terms of die area, and traveling far distances becomes increasingly expensive in terms of power usage and latency. There’s no silver bullet around that – it’s physics at work – and except for making every core pay the worst case latency for all others, there will be always some in closer proximity.

What does this mean for the application developer? It means that the application must try to keep work “close together” – usually, the OS scheduler will take care of this. By default, all caches are *coherent* with each other, which means that if the core in the top-left corner writes something to memory, the core in the bottom right can see this. [Various protocols](https://en.wikipedia.org/wiki/Cache_coherence) have been designed to handle this; the gist of it is that any core can write some memory, and any other core will see the new data by default. No extra work required by the application – but you can imagine already that sharing data between cores will force a lot of cross-core communication.

### GPUs

Now, GPUs are much more parallel than CPUs. A Vega10 GPU is practically speaking a 64-core CPU, with a similar cache hierarchy. Let’s take a look:

The sizes are completely off, but it’s still vaguely similar. If you squint enough, you could think it’s a 64-core CPU on a single die. Obviously, the devil is hiding in the details again, because where CPUs have coherency by default, GPUs are running in a very different mode. The programming model is designed for many independent tasks, so let’s think for a moment how this would impact our cache design. Given every work item is independent, we can assume that each core works on its own data, and there is little to no sharing across cores. How could we optimize our hardware for this? First of all, we’ll get rid of coherency by default. If core A writes something, and wants core B to see it, it’s now the developer’s responsibility to do. The assumption is that this is rarely necessary, as it requires two syncs – one is memory (we need to flush the data out of the cache somehow), and the second one, it requires that the second core is actually processing the same data. As we learned, execution order is something GPUs are not usually happy to provide, and that directly impacts the cache handling. Given a developer has to synchronize already, they can do the memory barriers at the same time.

The other part is that the caches don’t manage themselves. On a CPU, things tend to just work within a single process, but on a GPU, flushing and invalidating caches is a very explicit operation. If you finish one compute shader and you want to start the next one, the GPU will typically insert a drain to make sure that all work finished, and also flush and invalidate all compute-unit local caches to make sure the next dispatch sees the data. This makes it critical to keep the data in L2 – flushing the L1 caches happens a lot, but because they’re small, it’s cheap. Compare this with a CPU where the L2 of a single core is already half the size of all L1 caches of a GPU combined!

The other interesting bit are the shared caches. In the CPU case, the only shared data is in L3. In the GPU case, where we expect a single program to execute for many compute units, the instruction cache is shared among compute units. This implies that ideally, we want to send the same program to groups of four compute units and not totally random across the GPU. Similarly, we assume that the same constants get loaded across all waves executing the same program, which results in separate constant/scalar caches. These are practically read-only (except for atomics instructions), which means that they don’t need to get flushed (no data changed), but they still require invalidation between dispatches.

You might wonder, with this default setup, how do I get coherency across caches? Surely there must be a way, as GLSL for instance has the `coherent`

modifier. Glad you’ve asked – and the solution to this is rather simple. All compute units share the same L2, so if we want to ensure coherence, we can just *bypass* L1. If you look at the [GCN ISA](https://developer.amd.com/wp-content/resources/Vega_Shader_ISA_28July2017.pdf), there’s a `GLC`

bit which says: “Force bypass of L1 cache”. By writing through to L2, and always reading from L2, we can get the impression of coherent caches, without any coherency protocol. All at the expense of basically ignoring the (tiny) L1 – again, a trade-off which makes sense for GPUs.

Finally, let’s talk once more about the sizes. Compared to a CPU, the caches are tiny, so why are they even there? On a CPU, caches are all about reuse, and as you can keep next to no data around in registers, you need large caches. The other side of the story is that CPU code tends to read memory all over the place, but typically it doesn’t read large chunks of nearby data. Think databases – the chance that you’re going to read a few entries which are next to each other is rather low.

GPUs on the other hand have to solve a different problem. Tons of threads in flight, all of them wanting to either stream through data, or access data in a spatially coherent fashion (think textures). For that use case, what you really want is a cache which helps you combine reads/writes and keeps data just around long enough that you can move it into registers. For example, you’re loading a 4-component vector component by component. Ideally, you want to have the four components “cached” until your load finishes. A tiny cache is perfect for that – it keeps the cache line around until it’s consumed, and the chance you’re going to hit it again is super small anyway as your threads are processing tons of (independent) data in general. For this series, this is the last example of how the applications and the expected usage have shaped the GPU to be very different from a CPU.

## Summary

That’s it, folks! I hope you enjoyed the series – and noticed that CPUs and GPUs are both multi-core processors, but specifically designed for different use cases and tuned for those. The other interesting bit is how the programming model influenced the hardware design and vice versa – and how we’re on some path to convergence. Modern GPU code tends to run fine on modern CPUs; it’s already well designed to take advantage of many cores, can handle non-uniform memory access, and can easily cope with little cache coherency guarantees. Where are we heading? I don’t know, but for sure, knowledge about compute shaders and GPU execution models will help prepare you for whatever future is ahead of us!