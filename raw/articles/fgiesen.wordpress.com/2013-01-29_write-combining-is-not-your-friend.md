---
title: Write combining is not your friend
url: https://fgiesen.wordpress.com/2013/01/29/write-combining-is-not-your-friend/
published: '2013-01-29'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Write combining is not your friend

*This post is part of a series – go here for the index.*

Most memory you deal with on a daily basis is cached; on CPUs, it’s usually write-back cached. While dealing with processor caches can be counter-intuitive, caching works well most of the time, and it’s mostly transparent to the programmer (and certainly the user). However, if we are to use the cache to service memory reads, we need to make sure to invalidate our cache entries if someone else writes to the corresponding memory locations. This is implemented using one of several mechanisms referred to as [“coherency protocols”](http://en.wikipedia.org/wiki/Cache_coherence#Coherency_protocol), which CPU cores use to synchronize their caches with each other.

That is not the subject of this post, though. Because while such mechanisms are in place for CPUs talking to each other, there is nothing equivalent for the CPU talking to other non-CPU devices, such as GPUs, storage or network devices. Generally, communication with such devices still happens via system memory (or by memory-mapping registers or device memory so they *appear* to be system memory, which doesn’t make much difference from the CPU core’s point of view), but the CPU is not going to be notified of changes in a timely fashion, so normal caching is out.

Originally, device memory used to be accessed completely without caching. That’s safe (or at least as safe as it’s going to get) but also slow, because each memory access gets turned into an individual bus transaction, which has considerable overhead. Now anything related to graphics tends to move *a lot* of data around. Before widespread hardware acceleration, it was mostly the CPU writing pixels to the frame buffer, but now there’s other graphics-related writes too. So finally we get [write combining](http://en.wikipedia.org/wiki/Write-combining), where the CPU treats reads as uncached but will buffer writes for a while in the hope of being able to combine multiple adjacent writes into a larger bus transaction. This is much faster. Common implementations have much weaker memory ordering guarantees than most memory accesses, but that’s fine too; this kind of thing tends to be used mainly for bulk transfers, where you really don’t care in which order the bytes trickle into memory. All you really want is some mechanism to make sure that all the writes are done before you pull the trigger and launch a command buffer, display a frame, trigger a texture upload, whatever.

All this is fairly straightforward and reasonable. However, the devil’s in the details, and in practice write combining is finicky. It’s really easy to make a small mistake that results in a big performance penalty. I’ve seen this twice in the last two days, on two different projects, so I’ve decided to write up some guidelines.

### Where is write combining used?

I’m only going to talk about graphics here. For all I know, write-combining might be used for lots of other things, but I would assume that even if that is true, graphics is the only mainstream application where WC memory is exposed to user-mode applications.

So the main way to get a pointer to write-combining memory is by asking a 3D or GPGPU API to map a buffer or texture into memory: that is, using GL `glMapBuffer`

, D3D9 `Lock`

, CL `clEnqueueMap*`

or D3D1x `Map`

. Not all such buffers are write-combined, but those used for rapid uploads usually are – doubly so if you’re requesting a “write-only” mapping, which all mentioned APIs support.

### What happens if you read from write-combined memory?

Sadly, the answer is not “reading from write-combined memory isn’t allowed”. This would be much simpler and less error-prone, but at least on x86, the processor doesn’t even have the notion of memory that can be written but not read.

Instead, what actually happens is that the read is treated as uncached. This means all pending write-combining buffers get flushed, and then the read is performed without any cache. Flushing write-combining buffers costs time and results in stores of partial cache lines, which is also inefficient. And of course uncached reads are really slow too.

**Don’t read from write-combining memory**, unless you have a *very* good reason to (you probably don’t). In particular, **never read values back from constant buffers, vertex buffers or index buffers you’re currently writing to**. Ever.

How bad can it possibly be? Let me show you an example. Here’s an excerpt of a VTune profile for an application I recently looked at:

As you can see, a lot of time is being spent in `CPUTModelDX11::SetRenderStates`

. Worse, as VTune helpfully highlights for us, this function runs at an absolutely appalling 9.721 clock cycles per instruction (CPI Rate)! Now it turns out that a large fraction is due to these innocent-looking lines that write to a constant buffer:

pCb = (CPUTModelConstantBuffer*)mapInfo.pData; pCb->World = world; pCb->ViewProjection = view * projection; pCb->WorldViewProjection = world * pCb->ViewProjection;

Note how `pCb->ViewProjection`

is used as an argument for a matrix multiply in the last line. Now, here’s the simple fix:

XMMATRIX viewProj = view * projection; pCb = (CPUTModelConstantBuffer*)mapInfo.pData; pCb->World = world; pCb->ViewProjection = viewProj; pCb->WorldViewProjection = world * viewProj;

And here’s the corresponding VTune profile:

Now, this profile was somewhat longer so the actual cycle counts are different, but the point stands: This simple change made the function drop from the #5 to the #12 spot, and based on the CPI rate, it now runs more than twice as fast per invocation – mind you, 4.4 cycles/instruction is still pretty bad, but it’s certainly an improvement over the 9.7 we saw earlier.

### Other things to be careful about

Okay, so not reading is an important point. What else? Well, it depends on the processor. Early x86s had fairly restrictive rules about write combining: writes had to be of certain sizes, they needed to be properly aligned, and accesses needed to be purely sequential. The first two can be dealt with, but the latter is tricky when dealing with C/C++ compilers that try to move schedule writes for optimum efficiency. For several years, it used to be that you basically had to mark all pointers to vertex buffers etc. as `volatile`

to make sure the compiler didn’t try to reorder writes and inadvertently break write-combining in the process. While not as bad as reads, this still results in a very noticeable drop in performance.

Luckily, x86 processors from about 2002 on are far more tolerant about writes arriving out of order and will generally be able to combine writes even if they’re not perfectly sequential. However, other processors (such as those found in some game consoles) aren’t as tolerant; better safe than sorry. And even if you don’t strictly need to enforce sequential accesses, it’s still a good idea to write the code that way, because of the next rule:

**Avoid holes**. If you’re writing to a memory range, write the whole range. If you’re writing a dynamic vertex buffer, write every field, *even if your shader ignores some of them*. If you map a buffer, write the whole thing – even if you (think you) know some of the contents don’t need to change. Any hole will break the sequence and turn what would otherwise be one large write into at least two smaller ones. On some processors, it has other adverse effects too. That’s why you want to write struct fields sequentially, at least in your source code – that way, it’s easier to check against the struct definition to make sure you left nothing out.

### Conclusion

Write combining is a powerful technique to accelerate writes to graphics memory, but it’s very easy to misuse in a way that causes severe performance degradation. Worse, because things only get slow but don’t crash, such problems can creep in and not be noticed for a long time. Short of profiling your code periodically, there’s little you can do to find them. Here’s the summary:

- If it’s a dynamic constant buffer, dynamic vertex buffer or dynamic texture and mapped “write-only”, it’s probably write-combined.
*Never*read from write-combined memory.*Try to keep writes sequential*. This is good style even when it’s not strictly necessary. On processors with picky write-combining logic, you might also need to use`volatile`

or some other way to cause the compiler not to reorder instructions.*Don’t leave holes*. Always write large, contiguous ranges.*Check the rules for your target architecture*. There might be additional alignment and access width limitations.

If you live by these rules, write-combining can be a powerful ally in writing high-performance graphics code. But never a friend – it *will* stab you in the back on the first opportunity. So be careful.

It’s much worse for write combining of course, but I’ve been seeing a lot of this type of code causing major unexpected performance problems :

pCb->ViewProjection = view * projection;

pCb->WorldViewProjection = world * pCb->ViewProjection;

(especially on the horrible in order platforms where it causes a LHS).

It can also be quite hidden when the memory store is a member variable. It would almost be easier if you had to call Load() and Store() manually to access memory – certainly for write combining I think I would take that hit to code time.

Nice post!

There’s a GameFest talk titled “Case Studies in VMX128 Optimization” which touches on the subject of always writing to write-combined memory sequentially, using VMX to do so. Might be interesting for others not having access to console hardware on a daily basis:

http://www.microsoft.com/en-us/download/details.aspx?id=10110

Thanks! It was a good read. Quick question:

If a vertex buffer used as “per instance” data instancing won’t be fully used, should I still fill the whole buffer contents? (DX9 hw)

Specific example:

World matrix passed through texcoords, using three float4 texcoords (encode position, rotation, scale matrix 4×3).

The vertex buffer allows up to 200 instances, then it’s 9.600 bytes

The vertex buffer isn’t using all instances (say just 3).

Should I write 144 bytes and set instance count to 3, or fill the whole 9600 bytes?

According to your suggestion “avoid holes”, I should write the whole 9600 bytes even if I wont use the extra 9.456.

However I suspect your advice might be only referring to leaving “gaps” between ranges of memory, i.e. write to memory in range [0; 1000) and then write to [1100; max_buffer) because we know in advance the range [1000; 1100) won’t be used by the GPU.

Good example about not reading from write combined memory, even though it is common sense; mistakes like this might be more common than we would like to.

Thank you!

Matias

Short version: Leaving space at the end unused (or big contiguous holes) is fine, just be sure not to drop a byte here and there.

Slightly longer version: Write combining normally happens on a cache line granularity. Once you’ve filled up a whole cache line, the processor knows it’s done and writes it to memory. And if you don’t write all bytes in a cache line, the processor will keep the write buffer around for a while, and eventually flush it (writing the partial cache line contents to memory) to make space for something else.

Unless you happen to be writing data to cache-line aligned locations and in multiples of the cache line size (64 bytes on current x86 processors, 128 bytes on some other architectures), you will generally have one partially filled cache line at the beginning and one at the end of the buffer. That’s fine. Just make sure that the bulk of your data is contiguous so you get proper write combining for everything in between.

This also tells you what the granularity is: leaving a gap can be profitable if it enables skipping at least 2 cache lines. (Technically, 1 can already be a win, but only if you actually stop and resume writing at cache line boundaries, otherwise leaving a 1-cache line gap will produce two partial cache line writes).

Thank you! That clears it up. It’s more or less what I’ve suspected. That knowledge from the “long version” is very useful.

Some arm archs are 32 bytes in cache line size btw, which is worth caring about if mobile devices keep evolving & pushing more power.

I read that a call to glMapBuffer let the driver reserve a space that can be CPU memory buffer, not GPU, and that the copy happens during unMap.

Is it the same?

It really depends on the buffer usage hint and how you’re mapping it.

If you’re mapping a newly created STATIC_DRAW buffer, you’re likely to get a pointer to system memory. The driver will later copy this to the GPU (sometime after unmap). STREAM_DRAW buffers might give you a direct pointer to write-combined memory if mapped write-only. DYNAMIC_DRAW are very likely to, at least on PC. Other buffer types (_READ and _COPY) normally won’t. Furthermore, if you’re asking for READ_ONLY or READ_WRITE access (i.e. not WRITE_ONLY), the GL implementation might well decide to copy the data to cacheable memory first before giving you a pointer. This holds for any buffer type.

And let us not forget that a simple += in a particle copier caused framerates to drop from 60 to 10 in Firestorm… Those accidental reads. :/

Another important thing that’s easy to miss is implicit alignment padding in structures. I’ve seen it break write coalescing a few times.

And why does TBB take 3.5 cycles per insn?

That’s TBB’s spin loop for idle workers. They go to sleep after a while, but it sticks around for a while in case there are more tasks forthcoming. The spin loop just executes “PAUSE” instructions which put the current hyperthread to sleep for a certain number of cycles – which gets billed as execution time by the performance counters.

The later installments in this series (“The care and feeding of worker threads” and later posts) have much lower values for this function because the thread utilization is much better.

It is true that WC is not your friend, but the MOVNTDQA instruction (introduced with SSE4) can read from it with good performance.

Nice article! Gives a good gist about write-combining. Thanks.

An excellent read.

Smallish detail. CPUTModelDX11::SetRenderStates in the first VTune profile was accidentally compared to CPUTMaterialDX11::SetRenderStates in the second one. The improvement was probably much greater (just guessing) than presented here.