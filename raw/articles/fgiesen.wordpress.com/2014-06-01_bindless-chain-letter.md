---
title: Bindless chain letter
url: https://fgiesen.wordpress.com/2014/06/01/bindless-chain-letter/
published: '2014-06-01'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Bindless chain letter

I wanted to comment on Timothy Lottes [post on Bindless and descriptors](http://timothylottes.blogspot.com/2014/06/bindless-and-descriptors.html) (read that first!) and the comment field was too small, so here goes.

Some questions.

General: You’re implicitly assuming there’s *lots* of different types of resource tables. Why?

**UPDATE**: It seems like Timothy is talking about D3D12-esque Descriptor Tables. Well, I’m not :), so yeah, kinda talking apart here, but here’s my response anyway.

Essentially, GL bindless just means “one big resource table that contains everything”. And you could certainly implement it as such: one large resource table (multi-megabyte, potentially) that contains descriptor for absolutely everything currently live, with the handles being 32-bit offsets from the base address; nor do I see an intrinsic need for resource tables to be homogeneous in terms of either resource type or update frequency (it might be advantageous in certain cases, but I don’t see why it would be *required*).

NV GL bindless: what’s the handle values in “`TEX handle`

“? Presumably, not a 7-bit register index. I’m assuming that it boils down to a “`[bindlessTable + handle]`

” addressing mode, either explicit (i.e. this is a memory load) or implicit (HW is aware of handles and has a dedicated fetch path for them)? I couldn’t see any details in the documents you linked. Anyway, presumably there’s still resource descriptors somewhere. Where is that “somewhere”? How does do the HW know where to get them from?

NV with resource tables: why are you billing the handle table address LDC per texture sample? Unless there’s very high register pressure, you would only load the resource table pointers once per table, not once per resource access. And given my previous comment about “I don’t see why you need tons of these”, that’s really a constant per-shader cost of a few regs and a few loads; it’s not per texture sample at all.

All AMD: you can’t load the texture/sampler descriptors directly, you still need to know where to load them from (unless you use little enough resources that you can squeeze all descriptors into the 16 scalars). There’s at least one more scalar load to get a base pointer to the resource descriptors for the active draw call. Like the resource table pointer loads I just mentioned, this is amortized (just do that load once and leave the scalar reg around).

For GL bindless mode, you would presumably use a single global descriptor table that all your handles point into, and would preload the base address to that table using the 16 scalars you get to set per draw. This makes the basic model:

AMD DX “bindful”:

// sBatchDesc is one of the 16 pre-init S_LOAD_DWORD_X4 sTexDesc, sBatchDesc(16) // random offset S_LOAD_DWORD_X4 sSmpDesc, sBatchDesc(48) // ... SAMPLE ...

AMD GL “bindful”:

S_LOAD_DWORD_X8 sTexAndSmp, sBatchDesc(32) SAMPLE ...

AMD GL bindless:

// sBindlessTable also one of the 16 pre-init S_BUFFER_LOAD_DWORD sTexHandle, sConstantBuf(12) S_LOAD_DWORD_X8 sTexAndSmp, sBindlessTable(sTexHandle) SAMPLE ...

(explicit handle load here, “bindful” is cheaper on the shader side but pays that cost elsewhere by having to set up the per-batch descriptors)

and

AMD resource tables, separate tex/smp.

// let's say we have 2, sResourceTableImmutable // and sResourceTableDyn, both pre-init S_LOAD_DWORD sTexHandle, sBatchDesc(24) S_LOAD_DWORD_X4 sTexDesc, sResourceTableDyn(sTexHandle) S_LOAD_DWORD sSmpHandle, sBatchDesc(28) S_LOAD_DWORD_X4 sSmpDesc, sResourceTableImmutable(sSmpHandle) SAMPLE ...

or we could have a combined texture/sampler handle if we wanted, etc.

The big difference here is that the batch descriptors (sBatchDesc) here only hold texture *handles* (=offsets into their respective resource tables) not descriptors themselves. In the “bindful” case, there’s a conceptual global table too (the bind points), but it keeps changing between batches, which makes things tricky, and forces you to deal with multiple live versions at the same time and/or copy descriptors around. The resource table model (which bindless is a special case of!) has them stay constant and immutable over the lifetime of a command buffer which gets rid of that cost. GL bindless is similar.

Another note on the AMD resource table version: I’m loading texture/sampler handlers here separately for clarity, but that’s not at all required. A shader that references multiple contigous slots from its sBatchDesc can (and probably should) fuse them into larger pow2-sized `S_LOAD_DWORD`

s. In my example, you could just as well do:

AMD resource tables + “fusing”:

// sTexHandle = sHandles, sSmpHandle = sHandles + 1 (register IDs) S_LOAD_DWORD_X2 sHandles, sBatchDesc(24) S_LOAD_DWORD_X4 sTexDesc, sResourceTableDyn(sTexHandle) S_LOAD_DWORD_X4 sSmpDesc, sResourceTableImmutable(sSmpHandle) SAMPLE ...

So really, not all that much (cost) difference between the different “bindless-esque” approaches here that I can see.