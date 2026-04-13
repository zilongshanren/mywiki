---
title: More compute shaders
url: https://anteru.net/blog/2018/more-compute-shaders
published: '2018-07-14'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Last week I’ve covered [compute shaders](https://anteru.net/blog/2018/intro-to-compute-shaders), and I’ve been asked to go a bit deeper on the hardware side to cover subgroups and more. But before we get there, let’s recap briefly what a compute unit looks like and what is happening in it.

In the last post, I explained that the hardware is optimized for many items executing the same program. This resulted in the usage of very wide SIMD units (in the case of AMD’s GCN, 16-wide), hiding memory latency through task switching, and a branching model which relies on masking. I didn’t get into too much detail about those though, which we’ll do now, and after that, we’ll find out what to do with our new-found knowledge!

## SIMD execution

When it comes to executing your code, a GCN compute unit has two main building blocks you care about: Several SIMD units and a scalar unit. The SIMD units are each 16 wide, meaning they process 16 elements at a time. However, they don’t have a latency of one – they don’t finish executing an instruction in a single clock cycle. Instead, it takes four cycles to process an instruction from start to end (some take longer, but let’s pretend all take four cycles for now.) Four cycles is about the speed you’d expect for something like a fused-multiply-add, which needs to fetch three operands from the register file, do a multiply-and-add, and write the result back (highly optimized CPU designs also take four cycles, as can be seen in [Agner Fog’s instruction tables](http://www.agner.org/optimize/#manuals).)

Latency doesn’t equal throughput, though. An instruction with a latency of four can still have a throughput of one, if it’s properly pipelined. Let’s look at an example:

Which means that if we have sufficient work to do for a single SIMD, we can get 16 FMA instructions executed per clock. If we could issue a different instructions in every cycle, we’d have to deal with another problem though – some of the results may not be ready. Imagine our architecture would have a four-cycle latency on all instructions, and a single-cycle dispatch (meaning every cycle we can throw a new instruction into the pipeline.) Now, we want to execute this imaginary code:

```
v_add_f32 r0, r1, r2 ; add r1 to r2, write to r0
v_mul_f32 r3, r0, r2 ; multiply r0 with r2, write to r3
```


We have a dependency between the first and the second instruction – the second instruction cannot start before the first has finished, as it needs to wait for `r0`

to be ready. This means we’d have to stall for three cycles before we issue another instruction. The GCN architects solved this by issuing one instruction to a SIMD every *four* cycles. Additionally, instead of executing one operation on 16 elements and then switching to the next instruction, GCN runs the *same* instruction *four* times on a total of 64 elements. The only real change this requires to the hardware is to make the registers wider than the SIMD unit. Now, you *never* have to wait, as by the time the `v_mul_f32`

starts on the first 16 elements, the `v_add_f32`

just finished them:

You’ll immediately notice those *wait* cycles, and clearly that’s no good to have a unit spend most of its time waiting. To fill those up, the GCN designers use *four* SIMD units, so the real picture on the hardware is as following:

This 64-wide construct is called a “wavefront” or “wave”, and it’s the smallest unit of execution. A wave can get scheduled onto a SIMD to execute, and each thread group consists of at least one wave.

## Scalar code

Phew, that was quite a bit, and we’re unfortunately still not done. So far, we pretended everything is executed on the SIMD, but remember when I wrote there are two blocks related to execution? High time we get to this other … thing.

If you program anything remotely complex, you’ll notice that there are really two kinds of variables: *Uniform* values, which are constant across all elements, and *non-uniform* values, which differ per lane.

A non-uniform variable would be for instance the `laneId`

. We’ll pretend there’s a special register we can read – `g_laneId`

, and then we want to execute the following code:

```
if (laneId & 1) {
result += 2;
} else {
result *= 2;
}
```


In this example, we’re not going to talk about conditional moves, so this needs to get compiled to a branch. How would this look like on a GPU? As we learned, there is something called the execution mask which controls what lanes are active (also known as *divergent control flow*.) With that knowledge, this code would probably compile to something like this:

```
v_and_u32 r0, g_laneId, 1 ; r0 = laneId & 1
v_cmp_eq_u32 exec, r0, 1 ; exec[lane] = (r0[lane] == 1)
v_add_f32 r1, r1, 2 ; r1 += 2
v_invert exec ; exec[lane] = !exec[lane]
v_mul_f32 r1, r1, 2 ; r1 *= 2
v_reset exec ; exec[lane] = 1
```


Here, `exec[lane]`

is the execution mask, which varies per lane. When it’s `1`

for a particular lane, that lane will be considered active for each subsequent operation (you don’t have to manually specify the `exec`

mask a predicate, that’s implied.) The exact instructions also don’t matter, what matters is that all the values we’re looking at that are not literals are per-lane values. I.e. `g_laneId`

has a different value, as has `r1`

, for every single lane. This is a “non-uniform” value, and the default case, as each lane has its own slot in a vector register.

Now, if the control flow was looking like this, with `cb`

coming from a constant buffer:

```
if (cb == 1) {
result += 2
} else {
result *= 2;
}
```


Turning this into this straightforward code:

```
v_cmp_eq_u32 exec, cb, 1 ; exec[lane] = (cb == 1)
v_add_f32 r1, r1, 2 ; r1 += 2
v_invert exec ; exec[lane] = !exec[lane]
v_mul_f32 r1, r1, 2 ; r1 *= 2
v_reset exec ; exec[lane] = 1
```


This has suddenly a problem the previous code didn’t have – `cb`

is constant for all lanes, yet we pretend it’s not. As `cb`

is an *uniform* value, the comparison against 1 could be computed once instead of per lane. That’s how you’d do it on a CPU, where vector instructions are a new addition. You’d probably do a normal conditional jump (again, ignore conditional moves for now), and call a vector instruction in each branch. Turns out, GCN has the same concept of a “non-vector” execution, which is aptly named “scalar” as it operates on a single scalar instead of a vector. In GCN assembly, the code could compile to:

```
s_cmp_eq_u32 cb, 1 ; scc = (cb == 1)
s_cbranch_scc0 else ; jump to else if scc == 0
v_add_f32 r1, r1, 2 ; r1 += 2
s_branch end ; jump to end
else:
v_mul_f32 r1, r1, 2 ; r1 *= 2
end:
```


What does this buy us? The big advantage is that those scalar units and register are super cheap compared to vector units. Whereas a vector register is 64x32 bit in size, a scalar register is just 32 bit, so we can throw many more scalar registers on the chip than vector registers (some hardware has special predicate registers for the same reason, one bit per lane is much less storage than a full-blown vector register.) We can also add exotic bit-manipulation instructions to the scalar unit as we don’t have to instantiate it 64 times per CU. Finally, we use less power as the scalar unit has less data to move and work on.

## Putting it all together

Now, being hardware experts, let’s see how we can put our knowledge to good use finally. We’ll start with wavefront wide instructions, which are [a hot topic for GPU programmers](https://www.khronos.org/blog/vulkan-subgroup-tutorial). Wavefront wide means we do something for all lanes, instead of doing it per lane – what could that possibly be?

### Scalar optimizations

The first thing we might want to try is to play around with that execution mask. Every hardware has this present in some form, be it explicit or as a predication mask. With that, we can do some neat optimization. Let’s assume we have the following code:

```
if (distanceToCamera < 10) {
return sampleAllTerrainLayers ();
} else {
return samplePreblendedTerrain ();
}
```


Looks innocent enough, but both function calls sample memory and are thus rather expensive. As we learned, if we have divergent control flow, the GPU will execute both paths. Even worse, the compiler will likely compile this to following pseudo-code:

```
VectorRegisters<0..32> allLayerCache = loadAllTerrainLayers();
VectorRegisters<32..40> simpleCache = loadPreblendedTerrainLayers();
if (distanceToCamera < 10) {
blend (allLayerCache);
} else {
blend (sampleCache);
}
```


Basically, it will try to front-load the memory access as much as possible, so by the time we reach the `else`

path, there’s a decent chance the loads has finished. However, we – as developers – know that the all-layer variant is higher quality, so how about this approach: If *any* lane goes down the high-quality path, we send *all* lanes to the high-quality path. We’ll have slightly higher quality overall, and on top of that, we get two optimizations in return:

- The compiler can use fewer registers by not front-loading both
- The compiler can use scalar branches

There’s a bunch of functions for this, all of which operate on the execution mask (or predicate registers, from here on I’ll pretend it’s the execution mask.) The three functions you’ll hear of are:

`ballot ()`

– returns the exec mask`any ()`

– returns`exec != 0`

`all()`

– returns`~exec == 0`


Changing our code to take advantage of this is trivial:

```
if (any (distanceToCamera < 10)) {
return sampleAllTerrainLayers ();
} else {
return samplePreblendedTerrain ();
}
```


Another common optimization applies to atomics. If we want to increment a global atomic by one per lane, we could do it like this:

```
atomic<int> globalAtomic;
if (someDynamicCondition) {
++globalAtomic;
}
```


This will require up to 64 atomic increments on GCN (as GCN does not coalesce them across a full wavefront.) That’s quite expensive, we can do much better by translating this into:

```
atomic<int> globalAtomic;
var ballotResult = ballot (someDynamicCondition);
if (laneId == 0) {
globalAtomic += popcount (ballotResult);
}
```


Where `popcount`

counts the number of set bits. This cuts down the number of atomics by 64. In reality, you probably still want to have a per-lane value if you’re doing a compaction, and it turns out that case is so common that GCN has a separate opcode for it (`v_mbcnt`

) which is used automatically by the compiler when doing atomics.

Finally, one more on the scalar unit. Let’s assume we have a vertex shader which passes through some `drawId`

, and the pixel shader gets it as a normal interpolant. In this case (barring cross-stage optimization and vertex-input-layout optimization), code like this will cause problems:

```
var materialProperties = materials [drawId];
```


As the compiler does not know that `drawId`

is uniform, it will assume it can be non-uniform, and thus perform a vector load into vector registers. If we do know it’s uniform – *dynamically uniform* is the specific term here – we can tell the compiler about this. GCN has a special instruction for this which somewhat become the “standard” way to express it – `v_readfirstlane`

. Read-first-lane reads the first active lane and broadcasts its value to all other lanes. In an architecture with separate scalar registers, this means that the value can be loaded into a scalar register. The optimal code would be thus:

```
var materialProperties = materials [readFirstLane (drawId)];
```


Now, the `materialProperties`

are stored in scalar registers. This reduces the vector register pressure, and will also turn branches that reference the properties into scalar branches.

### Vector fun

So much for the scalar unit, let’s turn to the vector unit, because things get really funny here. Turns out, pixel shaders have a huge impact on compute, because they force the hardware to do something really funky – make lanes talk to each other. Everything we learned so far about GPUs said you can’t talk across lanes except through LDS, or by broadcasting something through scalar registers (or read a single lane.) Turns out, pixel shaders have a very unique requirement – they require derivatives. GPUs implement derivatives by using *quads*, i.e. 2×2 pixels, and exchange data between them in a dynamically varying way. Mind blown?

`ddx()`

, `ddy()`

instructions. Each lane processes one pixel, and within 4 lanes, a lot of exchange is required to make derivatives work. On the right side, we can see the initial packing, and how the derivatives swap data between lanes within four lanes.This is commonly referred to as *quad swizzle*, and you’ll be hard pressed to find a GPU which doesn’t do this. However, most GPUs go much further, and provide more than just simple swizzling across four lanes. GCN takes it really far since the introduction of DPP – [data parallel primitives](https://gpuopen.com/amd-gcn-assembly-cross-lane-operations/). DPP goes beyond swizzling and provides cross-lane operand sourcing. Instead of just permuting within a quad, it actually allows one lane to use another lane as the input for an instruction, so you can express something like this:

```
v_add_f32 r1, r0, r0 row_shr:1
```


What does it do? It takes the current value of `r0`

on this lane and the one to the right *on the same SIMD* (row-shift-right being set to one), adds them together, and stores it in the current lane. This is some really serious functionality which introduces new wait states, and also has various limitations as to which lanes you can broadcast to. All of this requires intimate knowledge of the implementation, and as vendors differ in how they can exchange data between lanes, the high level languages expose general wave-wide reductions like `min`

etc. which will either swizzle or use things like DPP to get to one value. With those, you can reduce values across a wavefront in very few steps, without access to memory – it’s faster and still easy to use; what’s not to like here!

## Summary

I hope I could shed some light on how things really work this time around. There’s really not much left that hasn’t been covered so far, for GCN, I can only think of separate execution ports and how waits are handled, so maybe we’ll cover that in a later post? Other than that, thanks for reading, and if you have questions, don’t hesitate to get in touch with me!