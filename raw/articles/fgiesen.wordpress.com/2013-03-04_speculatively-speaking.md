---
title: Speculatively speaking
url: https://fgiesen.wordpress.com/2013/03/04/speculatively-speaking/
published: '2013-03-04'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Speculatively speaking

*This post is part of a series – go here for the index.*

Welcome back! Today, it’s time to take a closer look at the triangle binning code, which we’ve only seen mentioned briefly so far, and we’re going to see a few more pitfalls that all relate to [speculative execution](http://en.wikipedia.org/wiki/Speculative_execution).

### Loads blocked by what?

There’s one more micro-architectural issue this program runs into that I haven’t talked about before. Here’s the obligatory profiler screenshot:

The full column name reads “Loads Blocked by Store Forwarding”. So, what’s going on there? For this one, I’m gonna have to explain a bit first.

So let’s talk about stores in an out-of-order processor. In this series, we already saw how conditional branches and memory sharing between cores get handled on modern x86 cores: namely, with *speculative execution*. For branches, the core tries to predict which direction they will go, and automatically starts fetching and executing the corresponding instructions. Similarly, memory accesses are assumed to not conflict with what other cores are doing at the same time, and just march on ahead. But if it later turns out that the branch actually went in the other direction, that there was a memory conflict, or that some exception / hardware interrupt occurred, all the instructions that were executed in the meantime are invalid and their results must be discarded – the speculation didn’t pan out. The implicit assumption is that our speculation (branches behave as predicted, memory accesses generally don’t conflict and CPU exceptions/interrupts are rare) is right most of the time, so it generally pays off to forge ahead, and the savings are worth the occasional extra work of undoing a bunch of instructions when we turned out to be wrong.

But wait, how does the CPU “undo” instructions? Well, conceptually it takes a “snapshot” of the current machine state every time it’s about to start an operation that it might later have to undo. If that instructions makes it all the way through the pipeline without incident, it just gets retired normally, the snapshot gets thrown away and we know that our speculation was successful. But if there is a problem somewhere, the machine can just throw away all the work it did in the meantime, rewind back to the snapshot and retry.

Of course, CPUs don’t actually take full snapshots. Instead, they make use of the out-of-order machinery to do things much more efficiently: out-of-order CPUs have more registers internally than are exposed in the ISA (Instruction Set Architecture), and use a technique called “register renaming” to map the small set of architectural registers onto the larger set of physical registers. The “snapshotting” then doesn’t actually need to save register contents; it just needs to keep track of what the current register mapping at the snapshot point was, and make sure that the associated physical registers from the “before” snapshot don’t get reused until the instruction is safely retired.

This takes care of register modifications. We already know what happens with loads from memory – we just run them, and if it later turns out that the memory contents changed between the load instruction’s execution and its retirement, we need to re-run that block of code. Stores are the tricky part: we can’t easily do “memory renaming” since memory (unlike registers) is a shared resource, and also unlike registers rarely gets written in whole “accounting units” (cache lines) at a time.

The solution are *store buffers*: when a store instruction is executed, we do all the necessary groundwork – address translation, access right checking and so forth – but don’t actually write to memory just yet; rather, the target address and the associated data bits are written into a store buffer, where they just sit around for a while; the store buffers form a log of all pending writes to memory. Only after the core is sure that the store instruction will actually be executed (branch results etc. are known and no exceptions were triggered) will these values *actually* be written back to the cache.

Buffering stores this way has numerous advantages (beyond just making speculation easier), and is a technique not just used in out-of-order architectures; there’s just one problem though: what happens if I run code like this?

mov [x], eax mov ebx, [x]

Assuming no other threads writing to the same memory at the same time, you would certainly hope that at the end of this instruction sequence, `eax`

and `ebx`

contain the same value. But remember that the first instruction (the store) just writes to a store buffer, whereas the second instruction (the load) normally just references the cache. At the very least, we have to detect that this is happening – i.e., that we are trying to load from an address that currently has a write logged in a store buffer – but there’s numerous things we could do with that information.

One option is to simply stall the core and wait until the store is done before the load can start. This is fairly cheap to implement in hardware, but it does slow down the software running on it. This option was chosen by the in-order cores used in the current generation of game consoles, and the result is the dreaded “Load Hit Store” stall. It’s a way to solve the problem, but let’s just say it won’t win you many friends.

So x86 cores normally use a technique called “store to load forwarding” or just “store forwarding”, where loads can actually read data directly from the store buffers, at least under certain conditions. This is much more expensive in hardware – it adds a *lot* of wires between the load unit and the store buffers – but it is far less finicky to use on the software side.

So what are the conditions? The details depend on the core in question. Generally, if you store a value to a naturally aligned location in memory, and do a load with the same size as the store, you can expect store forwarding to work. If you do trickier stuff – span multiple cache lines, or use mismatched sizes between the loads and stores, for example – it really does depend. Some of the more recent Intel cores can also forward larger stores into smaller loads (e.g. a DWord read from a location written with `MOVDQA`

) under certain circumstances, for example. The dual case (large load overlapping with smaller stores) is substantially harder though, because it can involved multiple store buffers at the same time, and I currently know of no processor that implements this. And whenever you hit a case where the processor can’t perform store forwarding, you get the “Loads Blocked by Store Forwarding” stall above (effectively, x86’s version of a Load-Hit-Store).

### Revenge of the cycle-eaters

Which brings us back to the example at hand: what’s going on in those functions, `BinTransformedTrianglesMT`

in particular? Some investigation of the compiled code shows that the first sign of blocked loads is near these reads:

Gather(xformedPos, index, numLanes); vFxPt4 xFormedFxPtPos[3]; for(int i = 0; i < 3; i++) { xFormedFxPtPos[i].X = ftoi_round(xformedPos[i].X); xFormedFxPtPos[i].Y = ftoi_round(xformedPos[i].Y); xFormedFxPtPos[i].Z = ftoi_round(xformedPos[i].Z); xFormedFxPtPos[i].W = ftoi_round(xformedPos[i].W); }

and looking at the code for `Gather`

shows us exactly what’s going on:

void TransformedMeshSSE::Gather(vFloat4 pOut[3], UINT triId, UINT numLanes) { for(UINT l = 0; l < numLanes; l++) { for(UINT i = 0; i < 3; i++) { UINT index = mpIndices[(triId * 3) + (l * 3) + i]; pOut[i].X.lane[l] = mpXformedPos[index].m128_f32[0]; pOut[i].Y.lane[l] = mpXformedPos[index].m128_f32[1]; pOut[i].Z.lane[l] = mpXformedPos[index].m128_f32[2]; pOut[i].W.lane[l] = mpXformedPos[index].m128_f32[3]; } } }

Aha! This is the code that transforms our vertices from the AoS (array of structures) form that’s used in memory into the SoA (structure of arrays) form we use during binning (and also the two rasterizers). Note that the output vectors are written element by element; then, as soon as we try to read the whole vector into a register, we hit a forwarding stall, because the core can’t forward the results from the 4 different stores per vector to a single load. It turns out that the other two instances of forwarding stalls run into this problem for the same reason – during the gather of bounding box vertices and triangle vertices in the rasterizer, respectively.

So how do we fix it? Well, we’d really like those vectors to be written using full-width SIMD stores instead. Luckily, that’s not too hard: converting data from AoS to SoA is essentially a matrix transpose, and our typical use case happens to be 4 separate 4-vectors, i.e. a 4×4 matrix; luckily, a 4×4 matrix transpose is fairly easy to do in SSE, and Intel’s intrinsics header file even comes with a macro that implements it. So here’s the updated `Gather`

that uses a SSE transpose:

void TransformedMeshSSE::Gather(vFloat4 pOut[3], UINT triId, UINT numLanes) { const UINT *pInd0 = &mpIndices[triId * 3]; const UINT *pInd1 = pInd0 + (numLanes > 1 ? 3 : 0); const UINT *pInd2 = pInd0 + (numLanes > 2 ? 6 : 0); const UINT *pInd3 = pInd0 + (numLanes > 3 ? 9 : 0); for(UINT i = 0; i < 3; i++) { __m128 v0 = mpXformedPos[pInd0[i]]; // x0 y0 z0 w0 __m128 v1 = mpXformedPos[pInd1[i]]; // x1 y1 z1 w1 __m128 v2 = mpXformedPos[pInd2[i]]; // x2 y2 z2 w2 __m128 v3 = mpXformedPos[pInd3[i]]; // x3 y3 z3 w3 _MM_TRANSPOSE4_PS(v0, v1, v2, v3); // After transpose: pOut[i].X = VecF32(v0); // v0 = x0 x1 x2 x3 pOut[i].Y = VecF32(v1); // v1 = y0 y1 y2 y3 pOut[i].Z = VecF32(v2); // v2 = z0 z1 z2 z3 pOut[i].W = VecF32(v3); // v3 = w0 w1 w2 w3 } }

Not much to talk about here. The other two instances of this get modified in the exact same way. So how much does it help?

**Change:** Gather using SSE instructions and transpose

| Total cull time | min | 25th | med | 75th | max | mean | sdev |
|---|---|---|---|---|---|---|---|
| Initial | 3.148 | 3.208 | 3.243 | 3.305 | 4.321 | 3.271 | 0.100 |
| SSE Gather | 2.934 | 3.078 | 3.110 | 3.156 | 3.992 | 3.133 | 0.103 |

| Render depth | min | 25th | med | 75th | max | mean | sdev |
|---|---|---|---|---|---|---|---|
| Initial | 2.206 | 2.220 | 2.228 | 2.242 | 2.364 | 2.234 | 0.022 |
| SSE Gather | 2.099 | 2.119 | 2.137 | 2.156 | 2.242 | 2.141 | 0.028 |

| Depth test | min | 25th | med | 75th | max | mean | sdev |
|---|---|---|---|---|---|---|---|
| Initial | 0.813 | 0.830 | 0.839 | 0.847 | 0.886 | 0.839 | 0.013 |
| SSE Gather | 0.773 | 0.793 | 0.802 | 0.809 | 0.843 | 0.801 | 0.012 |

So we’re another 0.13ms down, about 0.04ms of which we gain in the depth testing pass and the remaining 0.09ms in the rendering pass. And a re-run with VTune confirms that the blocked loads are indeed gone:

### Vertex transformation

[Last time](https://fgiesen.wordpress.com/2013/02/28/reshaping-dataflows/), we modified the vertex transform code in the depth test rasterizer to get rid of the z-clamping and simplify the clipping logic. We also changed the logic to make better use of the regular structure of our input vertices. We don’t have any special structure we can use to make vertex transforms on regular meshes faster, but we definitely can (and should) improve the projection and near-clip logic, turning this:

mpXformedPos[i] = TransformCoords(&mpVertices[i].position, cumulativeMatrix); float oneOverW = 1.0f/max(mpXformedPos[i].m128_f32[3], 0.0000001f); mpXformedPos[i] = _mm_mul_ps(mpXformedPos[i], _mm_set1_ps(oneOverW)); mpXformedPos[i].m128_f32[3] = oneOverW;

into this:

__m128 xform = TransformCoords(&mpVertices[i].position, cumulativeMatrix); __m128 vertZ = _mm_shuffle_ps(xform, xform, 0xaa); __m128 vertW = _mm_shuffle_ps(xform, xform, 0xff); __m128 projected = _mm_div_ps(xform, vertW); // set to all-0 if near-clipped __m128 mNoNearClip = _mm_cmple_ps(vertZ, vertW); mpXformedPos[i] = _mm_and_ps(projected, mNoNearClip);

Here, near-clipped vertices are set to the (invalid) x=y=z=w=0, and the binner code can just check for `w==0`

to test whether a vertex is near-clipped instead of having to use the original w tests (which again had a hardcoded near plane value).

This change doesn’t have any significant impact on the running time, but it does get rid of the hardcoded near plane location for good, so I thought it was worth mentioning.

### Again with the memory ordering

And if we profile again, we notice there’s at least one more surprise waiting for us in the binning code:

Machine clears? We’ve seen them before, way back in “[Cores don’t like to share](https://fgiesen.wordpress.com/2013/01/31/cores-dont-like-to-share/)“. And yes, they’re again for memory ordering reasons. What did we do wrong this time? It turns out that the problematic code has been in there since the beginning, and ran just fine for quite a while, but ever since the scheduling optimizations we did in “[The care and feeding of worker threads](https://fgiesen.wordpress.com/2013/02/17/care-and-feeding-of-worker-threads-part-1/)“, we now have binning jobs running tightly packed enough to run into memory ordering issues. So what’s the problem? Here’s the code:

// Add triangle to the tiles or bins that the bounding box covers int row, col; for(row = startY; row <= endY; row++) { int offset1 = YOFFSET1_MT * row; int offset2 = YOFFSET2_MT * row; for(col = startX; col <= endX; col++) { int idx1 = offset1 + (XOFFSET1_MT * col) + taskId; int idx2 = offset2 + (XOFFSET2_MT * col) + (taskId * MAX_TRIS_IN_BIN_MT) + pNumTrisInBin[idx1]; pBin[idx2] = index + i; pBinModel[idx2] = modelId; pBinMesh[idx2] = meshId; pNumTrisInBin[idx1] += 1; } }

The problem turns out to be the array `pNumTrisInBin`

. Even though it’s accessed as 1D, it is effectively a 3D array like this:

`uint16 pNumTrisInBin[TILE_ROWS][TILE_COLS][BINNER_TASKS]`


The `TILE_ROWS`

and `TILE_COLS`

parts should be obvious. The `BINNER_TASKS`

needs some explanation though: as you hopefully remember, we try to divide the work between binning tasks so that each of them gets roughly the same amount of triangles. Now, before we start binning triangles, we don’t know which tiles they will go into – after all, that’s what the binner is there to find out.

We could have just one output buffer (bin) per tile; but then, whenever two binner tasks simultaneously end up trying to add a triangle to the same tile, they will end up getting serialized because they try to increment the same counter. And even worse, it would mean that the actual order of triangles in the bins would be different between every run, depending on when exactly each thread was running; while not fatal for depth buffers (we just end up storing the max of all triangles rendered to a pixel anyway, which is ordering-invariant) it’s still a complete pain to debug.

Hence there is one bin per tile per binning worker. We already know that the binning workers get assigned the triangles in the order they occur in the models – with the 32 binning workers we use, the first binning task gets the first 1/32 of the triangles, and second binning task gets the second 1/32, and so forth. And each binner processes triangles in order. This means that the rasterizer tasks can still process triangles in the original order they occur in the mesh – first process all triangles inserted by binner 0, then all triangles inserted by binner 1, and so forth. Since they’re in distinct memory ranges, that’s easily done. And each bin has a separate triangle counter, so they don’t interfere, right? Nothing to see here, move along.

Well, except for the bit where coherency is managed on a cache line granularity. Now, as you can see from the above declaration, the triangle counts for all the binner tasks are stored in adjacent 16-bit words; 32 of them, to be precise, one per binner task. So what was the size of a cache line again? 64 bytes, you say?

Oops.

Yep, even though it’s 32 separate counters, for the purposes of the memory subsystem it’s just the same as if it was all a single counter per tile (well, it might be slightly better than that if the initial pointer isn’t 64-byte aligned, but you get the idea).

Luckily for us, the fix is dead easy: all we have to do is shuffle the order of the array indices around.

`uint16 pNumTrisInBin[BINNER_TASKS][TILE_ROWS][TILE_COLS]`


We also happen to have 32 tiles total – which means that now, each binner task gets its own cache line by itself (again, provided we align things correctly). So again, it’s a really easy fix. The question being – how much does it help?

**Change:** Change pNumTrisInBin array indexing

| Total cull time | min | 25th | med | 75th | max | mean | sdev |
|---|---|---|---|---|---|---|---|
| Initial | 3.148 | 3.208 | 3.243 | 3.305 | 4.321 | 3.271 | 0.100 |
| SSE Gather | 2.934 | 3.078 | 3.110 | 3.156 | 3.992 | 3.133 | 0.103 |
| Change bin inds | 2.842 | 2.933 | 2.980 | 3.042 | 3.914 | 3.007 | 0.125 |

| Render depth | min | 25th | med | 75th | max | mean | sdev |
|---|---|---|---|---|---|---|---|
| Initial | 2.206 | 2.220 | 2.228 | 2.242 | 2.364 | 2.234 | 0.022 |
| SSE Gather | 2.099 | 2.119 | 2.137 | 2.156 | 2.242 | 2.141 | 0.028 |
| Change bin inds | 1.980 | 2.008 | 2.026 | 2.046 | 2.172 | 2.032 | 0.035 |

That’s right, a 0.1ms difference from *changing the memory layout of a 1024-entry, 2048-byte array*. You really need to be extremely careful with the layout of shared data when dealing with multiple cores at the same time.

### Once more, with branching

At this point, the binner is starting to look fairly good, but there’s one more thing that springs to eye:

Branch mispredictions. Now, the two rasterizers have legitimate reason to be mispredicting branches some of the time – they’re processing triangles with fairly unpredictable sizes, and the depth test rasterizer also has an early-out that’s hard to predict. But the binner has less of an excuse – sure, the triangles have very different dimensions measured *in 2×2 pixel blocks*, but the vast majority of our triangles fits inside one of our (generously sized!) 320×90 pixel tiles. So where are all these branches?

for(int i = 0; i < numLanes; i++) { // Skip triangle if area is zero if(triArea.lane[i] <= 0) continue; if(vEndX.lane[i] < vStartX.lane[i] || vEndY.lane[i] < vStartY.lane[i]) continue; float oneOverW[3]; for(int j = 0; j < 3; j++) oneOverW[j] = xformedPos[j].W.lane[i]; // Reject the triangle if any of its verts are outside the // near clip plane if(oneOverW[0] == 0.0f || oneOverW[1] == 0.0f || oneOverW[2] == 0.0f) continue; // ... }

Oh yeah, that. In particular, the first test (which checks for degenerate and back-facing triangles) will reject roughly half of all triangles and can be fairly random (as far as the CPU is concerned). Now, [last time we had an issue with branch mispredicts](https://fgiesen.wordpress.com/2013/02/16/depth-buffers-done-quick-part-2/), we simply removed the offending early-out. That’s a really bad idea in this case – any triangles we don’t reject here, we’re gonna waste even more work on later. No, these tests really should all be done here.

However, there’s no need for them to be done like this; right now, we have a whole slew of branches that are all over the map. Can’t we consolidate the branches somehow?

Of course we can. The basic idea is to do all the tests on 4 triangles at a time, while we’re still in SIMD form:

// Figure out which lanes are active VecS32 mFront = cmpgt(triArea, VecS32::zero()); VecS32 mNonemptyX = cmpgt(vEndX, vStartX); VecS32 mNonemptyY = cmpgt(vEndY, vStartY); VecF32 mAccept1 = bits2float(mFront & mNonemptyX & mNonemptyY); // All verts must be inside the near clip volume VecF32 mW0 = cmpgt(xformedPos[0].W, VecF32::zero()); VecF32 mW1 = cmpgt(xformedPos[1].W, VecF32::zero()); VecF32 mW2 = cmpgt(xformedPos[2].W, VecF32::zero()); VecF32 mAccept = and(and(mAccept1, mW0), and(mW1, mW2)); // laneMask == (1 << numLanes) - 1; - initialized earlier unsigned int triMask = _mm_movemask_ps(mAccept.simd) & laneMask;

Note I change the “is not near-clipped test” from `!(w == 0.0f)`

to `w > 0.0f`

, on account of me knowing that all legal w’s happen to not just be non-zero, they’re positive (okay, what really happened is that I forgot to add a “cmpne” when I wrote `VecF32`

and didn’t feel like adding it here). Other than that, it’s fairly straightforward. We build a mask in vector registers, then turn it into an integer mask of active lanes using `MOVMSKPS`

.

With this, we could turn all the original branches into a single test in the `i`

loop:

if((triMask & (1 << i)) == 0) continue;

However, we can do slightly better than that: it turns out we can iterate pretty much directly over the set bits in `triMask`

, which means we’re now down to one single branch in the outer loop – the loop counter itself. The modified loop looks like this:

while(triMask) { int i = FindClearLSB(&triMask); // ... }

So what does the magic `FindClearLSB`

function do? It better not contain any branches! But lucky for us, it’s quite straightforward:

// Find index of least-significant set bit in mask // and clear it (mask must be nonzero) static int FindClearLSB(unsigned int *mask) { unsigned long idx; _BitScanForward(&idx, *mask); *mask &= *mask - 1; return idx; }

all it takes is `_BitScanForward`

(the VC++ intrinsic for the x86 `BSF`

instruction) and a really old trick for clearing the least-significant set bit in a value. In other words, this compiles into about 3 integer instructions and is completely branch-free. Good enough. So does it help?

**Change:** Less branches in binner

| Total cull time | min | 25th | med | 75th | max | mean | sdev |
|---|---|---|---|---|---|---|---|
| Initial | 3.148 | 3.208 | 3.243 | 3.305 | 4.321 | 3.271 | 0.100 |
| SSE Gather | 2.934 | 3.078 | 3.110 | 3.156 | 3.992 | 3.133 | 0.103 |
| Change bin inds | 2.842 | 2.933 | 2.980 | 3.042 | 3.914 | 3.007 | 0.125 |
| Less branches | 2.786 | 2.879 | 2.915 | 2.969 | 3.706 | 2.936 | 0.092 |

| Render depth | min | 25th | med | 75th | max | mean | sdev |
|---|---|---|---|---|---|---|---|
| Initial | 2.206 | 2.220 | 2.228 | 2.242 | 2.364 | 2.234 | 0.022 |
| SSE Gather | 2.099 | 2.119 | 2.137 | 2.156 | 2.242 | 2.141 | 0.028 |
| Change bin inds | 1.980 | 2.008 | 2.026 | 2.046 | 2.172 | 2.032 | 0.035 |
| Less branches | 1.905 | 1.934 | 1.946 | 1.959 | 2.012 | 1.947 | 0.019 |

That’s another 0.07ms off the total, for about a 10% reduction in median total cull time for this post, and a 12.7% reduction in median rasterizer time. And for our customary victory lap, here’s the VTune results after this change:

The branch mispredictions aren’t gone, but we did make a notable dent. It’s more obvious if you compare the number of clock cyles with the previous image.

And with that, I’ll conclude this journey into both the triangle binner and the dark side of speculative execution. We’re also getting close to the end of this series – the next post will look again at the loading and rendering code we’ve been intentionally ignoring for most of this series :), and after that I’ll finish with a summary and wrap-up – including a list of things I didn’t cover, and why not.

Great article, I have a question relating to the store forwarding: does it apply across cores on the same physical processor? i.e core1’s store buffer contains adress 0xdeadbeef, core0’s processor performs a read from 0xdeadbeef – does the forwarding / stall happen or does core0 witness stale?

Intel’s x86_64 manual seems to indicate this happens, but won’t happen between physical processors as intra-processor forwarding doesn’t offer store ordering guarantees (implying no forwarding).

Many thanks – Stuart.

That depends on what you mean by “physical processor” – do hardware threads (hyperthreads) count? Store forwarding happens purely within a core, but a single core can run code from multiple hardware threads at the same time, and you can use store forwarding between those if you want. At the very least, you need to keep track of memory operations issued by both hardware threads and make sure the observed sequence of events matches memory ordering rules – that can be achieved using a forwarding mechanism, or simply by inserting stalls, but it needs to happen.

“Addresses” are complicated, in this context, by the way. Your program deals in virtual addresses. Most of the memory subsystem works with physical addresses, and virtual addresses permit nasty things (for the purposes of memory ordering) like synonyms where multiple different virtual addresses correspond to the same physical address. But the actual physical address for a memory access isn’t even known until several cycles after a memory operation started executing, and the “should this forward or not” decision usually needs to happen earlier than that. So CPU cores generally use conservative heuristics there that return either “definitely doesn’t need store forwarding” or “might need store forwarding”. For example, x86s usually only look at the bottom 12 bits of an address (which never change under address translation) to make that decision. If a might-need-forwarding load then later turns out not to be forwarded anyway, it needs to be canceled and re-issued down the regular path.

Between different cores (and different sockets), you use a very different type of machinery; this falls under the headline of cache coherence, and I’ve written about it elsewhere. Basically, each core can only write to cache lines it has exclusive ownership of – there can be at most one exclusive owner of any given (physical) cache line of memory at any time. That’s the invariant maintained by the cache coherency protocol, and it means that for any given byte address, all stores to it can be ordered consistently: at any given time, at most one core owns the containing cache line, and that core committed its store operations in

someorder.There’s several different mechanisms in play here that do related but different things.

Store forwarding, store buffers etc. maintain the illusion that within a single thread,

allmemory operations appear to happen in program order (from the point of view of that thread). (Out-of-order CPUs actually reorder them aggressively anyway, then use these and other mechanisms to ensure they don’t get caught.)Cache coherency protocols explicitly enforce that across

allthreads and cores, stores for each individual cache line get executed insomeorder (not necessarily one you intended, but they can always be ordered), and that if other processors cache read-only copies of a given cache line, these copies get invalidated before any core is granted exclusive write access.Between them, these two mechanisms handle the vast majority of memory ordering issues, implicitly.

However, loads, stores, atomic operations, communication between cores and certainly more complex compound operations like acquiring a lock are not infinitely fast operations that occur at one instant in time and immediately complete. All these things take time. For example, for a load operation, your copy of a given cache line might still have been valid at the time when you read out the bytes from the L1 cache data array, but it can still get invalidated (due to actions of another core) before the load is “finished” (completes the retire/commit pipeline stage).

Handling these remaining cases – when one core wants to modify a cache line while others have pending operations that read from that cache line – in a consistent, well-defined manner is where the complicated architectural memory ordering rules, memory ordering annotations, fences etc. come in.

The trick in high-performance implementations is that the full set of architectural rules is

notactively enforced most of the time. Cores speculatively run code as if there were no tricky memory ordering concerns, and most of the time on most of the code, there aren’t. However, they do keep monitoring if there are any external events that might cause the relaxed internal ordering to produce different results than the strict “official” ordering would. If so, they need to throw away all pending incomplete operations and try again. That’s the “memory ordering machine clear” (Intel lingo, but the concept applies elsewhere) I mention in this article.Hi I have a question that may seem a bit redundant but please let me know if you have addressed it anywhere or if it even makes sense:

What happens in case speculative store that was forwarding the data to the load did not succeed for some reason.

Are there any (mitigation) techniques in the modern processors to not flush the junior load to whom the data was forwarded and further junior instructions which uses that data?

The only way for stores to fail involves them (by one way or another) causing a CPU trap/fault. Which in turn causes the offending store (and anything after) to get cancelled and state to get rolled back to what it was right before the store, at which point the control flow is redirected to an exception handler. Any dependent loads get cancelled as part of the rollback.

Great article – it’s a long time since I’ve been close to the assember/hardware level, and your artciles are great for reminding me of things I knew a couple of decades ago, and informing me of what’s happened in the intervening two decades.

But one question: you write

“This option was chosen by the in-order cores used in the current generation of game consoles”.

And you go on to explain that this is *not* the approach taken in the x86 architecture.

So, what CPU were game consoles using back in 2013, then if not x86? I’m really struggling to imagine what mass-produced affordable CPUs exist *other* than x86 that have enough processing power to run modern games….

The then-current generation of game consoles at the time of writing (spring 2013) were Xbox 360/PS3. Both had custom in-order PowerPC cores for their CPUs. PS3 had one 3.2GHz in-order PPC core with 2 hardware threads (“hyperthreads” in Intel lingo) plus 8 SPUs (custom 3.2GHz in-order SIMD CPUs with their own local 256kB of SRAM and no caches, access to system RAM only via DMA transfers). Xbox 360 had 3 3.2GHz in-order PPC cores (closely related to the one in the PS3) with 2 hardware threads each, for 6 hardware threads total.

The SPUs on the PS3 were good for what they were meant for but more like DSPs; they didn’t even have instructions working on single integers for example. Everything was 128-bit vectors, and if you wanted to say write a single byte, that required a sequence of an aligned 16-byte load, multiple vector rotates and shuffles to replace a single byte in the 16-byte vector, and then an aligned 16-byte store. Between that, the relatively small memory (256k for all active code and data!), and no direct way to access RAM, the SPUs ended up being used mostly as coprocessors for batch processing or number-crunching tasks.

The Cell PPE and especially the Xbox 360 GPU (which had a lot of vector extensions) were also decent at number-crunching. Unfortunately, due to a number of unfortunate design choices, they sucked at basically everything else. In my experience, it was fairly common for random game code to take about the same (wall-clock!!) amount of time on the 3.2GHz Xenon/PS3 PPEs as it did on the ~730MHz Nintendo Wii (and I do mean Wii, not Wii U), which was also PowerPC, but using a very different core derived from the PowerPC 750CL. I talked to a couple of multi-platform game devs and I’m not the only one with that experience.