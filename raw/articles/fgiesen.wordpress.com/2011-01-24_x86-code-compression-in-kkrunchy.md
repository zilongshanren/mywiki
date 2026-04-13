---
title: x86 code compression in kkrunchy
url: https://fgiesen.wordpress.com/2011/01/24/x86-code-compression-in-kkrunchy/
published: '2011-01-24'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# x86 code compression in kkrunchy

This is about the “secret ingredient” in my EXE packer kkrunchy, which was used in our (Farbrausch) 64k intros starting from “fr-030: Candytron”, and also in a lot of other 64k intros or similarly size-limited productions by other groups – including several well-known 64ks from other groups such as Conspiracy, Equinox and Fairlight, I’m happy to add.

There are two primary versions of kkrunchy. The first one was developed between 2003 and 2005 and uses a fairly simple LZ77 coder with arithmetic coding backend, designed to have good compression and a small depacker (about 300 bytes when using hand-optimized x86 code). If you’re interested in the details, a simplified C++ version of the depacker that I then used to write the ASM code from is still available [here](http://www.farbrausch.de/~fg/stuff/depacker_simple.cpp) (of the various programs I’ve written, this is still one of my favorites: it’s just nice to have something so fundamentally *simple* that’s actually useful).

The second was developed roughly between 2006 and 2008 and uses PAQ-style context mixing. To be precise, it’s a spin-off borrowing a lot of ideas from PAQ7 including its neural network mixer, but with a custom model design optimized to use a lot less memory (around 5.5mb instead of hundreds of megabytes) and run *a lot* faster. It’s still dog slow, but it managed to process >120kb/s on my then-current P4 2.4GHz instead of the roughly 5kb/s that PAQ7 managed on the same machine when targeting roughly the same compression ratio. The depacker was optimized for both size and speed (with this much computation per bit, making it 4x slower for the sake of saving a few bytes is a bad deal!), and took up a comparatively hefty 1.5k, but normally more than made up for it. For example, our 96k shooter “kkrieger” shrunk by over 10k when recompressed with the new engine (if only we’d had that before, it would’ve saved us a lot of work in the last week before release and prevented some very embarrassing bugs).

Anyway, both packing engines were competitive with the state of the art in EXE compression for the given target sizes when they were first released, but neither were in any way spectacular, and both were biased towards simplicity and tweakability, not absolutely maximum compression. That’s because unlike most other EXE packers, kkrunchy doesn’t rely solely on its backend compression engine to bring in the space savings.


### Preprocessing code for fun and profit

Especially 64k intros (the original target for kkrunchy) usually have a fairly large amount of the overall executable size devoted to code, and a much smaller amount spent on content (since 64ks are usually one-file packages, this content comes in the form of either statically initialized data or resource sections). A typical ratio for us was between 48k and 56k of the final compressed executable spent on code and overhead (you still need OS-parseable file headers and some way of importing DLLs), with the rest being data. Clearly, if you want to really make a dent on the packed size, you should concentrate on code first. This is especially true because code always comes in the same format (executable x86 opcodes) while the composition and structure of data in the executable varies a lot.

If you have a context modeling based compressor, one way to inject “domain knowledge” about x86 code into the compressor is to include models specifically designed to analyze x86 opcodes and deal with them. This is the approach taken by recent PAQ versions, and also what you’ll find in the [PPMexe paper](http://research.microsoft.com/en-us/um/people/darkok/papers/TOPLAS.pdf) (I’ll come back to this in a bit). In context coders, this is probably the most direct way to inject domain knowledge into the (de)compressor, but it has two problems: first, that domain knowledge translates to a lot of extra code you need to carry around in your decompressor, and second, you can’t do it if you’re not using a context coder! (Remember the first version of kkrunchy used a plain LZ+Ari backend).

So kkrunchy instead uses a *filter* on x86 code. The compressor first takes the original x86 code, passes it through the filter (this should better be a reversible process!), and then hands it to the main compression engine. The decompressor first undoes the actual compression, then reverse-applies the filter in a second step. This is something done by most EXE compressors, but all others (that I know of) use very simple filters, mainly intended to make jump and call offsets more compressible. kkrunchy looks deeper than that; it actually disassembles the instruction stream, albeit only very roughly. This is based on the “split-stream” algorithm in the PPMexe paper (even though the paper only appeared in a journal in 2007, an earlier version was available as a MS Research Technical Report in 2005, when I first read it).

### Split-stream encoding

Unlike most modern, RISC-influenced instruction encodings, x86 doesn’t have fixed-length instruction words, but instead uses a variable-length encoding that leads to higher code density but is full of exceptions and special cases, making instruction decoding (or even the simpler problem of just determining instruction lengths) fairly complicated. An x86 instruction can have these components:

- Zero or more
*prefixes*. A prefix is a single byte that can influence the way an operation is performed (e.g.`REP`

,`LOCK`

), the size of an operand (the*operand-size prefix*`0x66`

turns a 16-bit operation into a 32-bit operation and vice versa), the size of an addressing computation (the*address-size prefix*`0x67`

which does the same for address calculations) or the source/target of a read/write operation (via segment prefixes). There’s also a set of extra prefixes in 64-bit mode (the so-called REX byte), and finally some of the prefixes are also used to extend the opcode byte for newer instructions (e.g. SSE/SSE2). - The actual
*opcode*, which encodes the operation to be performed (duh). “Classic” x86 has one-byte and two-byte opcodes. Two-byte opcodes have 0x0f as the first byte, the rest is one-byte opcodes. (More recent instructions also have three-byte opcodes that start with either 0x0f 0x38 or 0x0f 0x3a). - A
*ModR/M byte*, which encodes either the addressing mode or registers used for an instruction. - A
*SIB byte*(scale-index-base), used to extend the ModR/M byte for more advanced 386+ addressing modes like`[esi+eax*4+0x1234]`

. - A
*displacement*(usually 8-bits or 32-bits, signed, in 32-bit code) which is just an immediate offset added to the result of an address calculation (like the “0x1234” in the example above). There’s also absolute address mode (e.g.`mov [0x01234567], 0x89abcdef`

) which is not relative to any base register. - An
*immedate operand*. Again, usually 8 or 32 bits in 32-bit code, but there are some exceptions. Some ops (like`add eax, 42`

) or (`mov [edi], 23`

) have an immediate operand. This field is separate from the displacement; both can occur in the same instruction.

What the split-stream filter does is this: It splits x86 instructions (which are an interleaved sequence of these bytes with different meanings) into separate streams based on their function. The idea is that there’s lots of similarity between values in the same stream, but very little relation between values in different streams: Especially compiler-generated code won’t use all opcodes (some are a lot more frequent than others), but 8-bit jump offsets are almost completely random. Small 32-bit immediates are a lot more common than large ones; most 32-bit displacements are positive, but stack-based references (based off either `ESP`

or `EBP`

, e.g. used to access function parameters or local variables) are often negative. SIB bytes look different from ModRM bytes (or opcode bytes), and some are a lot more common than others. And so on. kkrunchy doesn’t split all of these into distinct groups (for example, the prefix, opcode and ModR/M bytes tend to be heavily correlated, so they’re kept all in one stream) and splits some of them even further: jump offsets are special 32-bit displacements, as are call offsets, and for 8-bit displacements, it pays to have separate streams based on the “base register” field of the ModR/M byte, since offsets used off the same register – usually containing a pointer – tend to be correlated. But the basic idea is just to split instructions into their components and encode the streams separately. This is done by just keeping them in distinct regions, so we need to add a header at the beginning that tells us how long each stream is (a bit of overhead there).

One thing worth noting is that the regular (non-far, non-indirect) `JMP`

(plus conditional variants) and `CALL`

instructions use *displacements*, not absolute target addresses; i.e. they encode the distance between the target instruction and the end of the current (call/jump) instruction, not the actual target address. This is intentionally done to greatly reduce the number of *relocations* that need to be made if some piece of code needs to be moved to an address other than its preferred load address in memory. However, it also means that code that repeatedly jumps to or calls the same target address (e.g. a frequently-called function) will have a different encoding of the target address every time, since the displacement depends on the address of the call instruction! For compression purposes, we’d like calls to the same target instruction to result in the exact same encoding every time, i.e. convert the offsets into absolute addresses. This is fairly easy to do – just add the address of a call instruction to its destination address (of course, you need to undo this after decompression or the code will jump somewhere wrong). This is the one thing that most executable compressors (or general-purpose compressors that have special modes for x86 code, for that matter) will do on their own: Search for byte sequences that look like a `CALL`

or `JMP`

instruction in the byte stream, and add the current offset to the 4 bytes following it. Then do the same thing in reverse on decompression. Very simple trick, but huge effect on the compression ratio: doing this one transform before compression usually reduces the final compressed size by about 10%, both for LZ-based and context-based coders.

### Fun with calls

Function calls are special: A lot of functions will get called very often indeed. You can just rely on the relative-to-absolute offset transform and your backend encoder to handle this; but when developing kkrunchy I found that it actually pays to special-case this one a bit. So instead I keep a 255-entry LRU cache (or a FIFO for simplicity in earlier kkrunchy versions) of recent call sites. If a call is repeated, I only need to store the index; otherwise I write a “255” byte to denote a cache miss, then code the full 32-bit target address and add it to the cache. The actual call offsets aren’t correlated to the offsets, so the “cache index” and “verbatim call offset” fields are written into separate streams.

There’s two more tricks to the function call cache: First, code that follows a `RET`

instruction has a good likelihood of being the start of a new function, and second, VC++ pads the unused space between functions (for alignment reasons) with `0xcc`

bytes which correspond to the `INT3`

opcode (software breakpoint). Since `INT3`

opcodes don’t appear in most functions, any instruction following one or more `INT3`

ops is also likely to start a new function. All such potential function addresses are also speculatively added to the function address cache. A false positive will throw an address not used for at least 255 subsequent `CALL`

instructions of the cache – not a big deal. OTOH, if our guess turns out to be right and we’ve found the start of a function that gets called soon, that’s 32 bits we never need to encode now.

Typical hit rates for the function address cache are between 70 and 80 percent, and every hit saves us 3 bytes. Trust me, there’s a lot of calls in most pieces of x86 code, and this is a big deal. This is the *only* transform in the code preprocessor that results in a lower number of byte to be encoded; all other steps of the transform are either 1:1 in terms of bytes or add some overhead (headers, escape codes). Still, running the filter usually reduces the size of the file by a few percent *even before any actual compression is done*.

### Dealing with non-code bytes

The original PPMexe algorithm assumes that it’s only actually running on code, and that it knows about all basic blocks in the program (i.e. all potential jump targets are known). It will then reorder instructions to get better compression. This is not an option when dealing with arbitrary programs; for once, we don’t know where the basic blocks are (the compiler doesn’t tell us!). We also don’t want to change the program in any way (even ignoring potential performance penalties, just think about the kind of problems arbitrary reordering of instructions could introduce in lock-free code…), and finally, it’s not generally a safe assumption that the code section only contains code, or that the compressor knows about all x86 instructions (after all, there’s new ones being added every so often, and we can’t generally parse them correctly without knowing about them). Luckily, x86 disassembling is mostly self-synchronizing (even if you get a few instructions wrong, you will generally by in sync again after a few instructions unless the code was explicitly designed to be “ambiguous”), so we don’t need to sweat this too much. We do, however, need to be able to encode instruction bytes that we can’t disassemble properly.

Luckily, there’s a few one-byte opcodes that basically never occur in any real program; we can use any of them as an “escape code”. We then flag that instruction as invalid in our disassembler table; if the program actually contains that instruction, it will need to use an escape code to do so, but that’s fine. kkrunchy originally used `INTO`

(`0xce`

) as escape opcode that just means “copy the next byte verbatim”; this is supposed to trigger an interrupt if arithmetic overflow occurred in the previous flag-setting instruction. I’ve never seen this in any real program; certainly not a compiled one. Should kkrunchy ever run across it, it can still encode that instruction byte using an escape: `INTO`

turns into `0xce 0xce`

. No problem. More recent versions use the `ICEBP`

opcode (`0xf1`

) as escape, which is even more obscure. It only exists on a few x86 models, and again, I’ve never seen it actually used anywhere.

One piece of non-code that tends to occur in code sections is jump tables for switch statements. Luckily they’re fairly easy to detect with good accuracy: If we have at least 12 consecutive bytes, starting at an address divisible by 4, that look like addresses in the code (i.e. are between the “code start” and “code end” addresses which are assumed to be known), we use another escape opcode to denote “jump table with N entries follows”, where N-1 is encoded as a single-byte value. (If a jump table has more than 256 entries, we just use chain several such escapes).

Between the two tricks, unknown instructions or junk in the code section doesn’t usually cause a problem.

### A box inside a box inside a box…

Because the kkrunchy code preprocessing filter does more than most such filters, it’s also bigger (around 900 bytes of code+data combined in the last version I used). But since it runs after the main decompression phase, there’s no need to pay that cost in full: The filter code can be compressed along with the filtered data! This shaves off another few hundred bytes at the cost of one extra jump at the end of the main decompression code. All other code that runs after decompression (e.g. import processing) can also be stored in compressed format. This is a bit like the “bootstrapping” process used for some C compilers: The core part of a C compiler (syntactic analysis and a simple code generator for the target machine) is written in a very portable subset of C. This core C compiler is compiled using whatever other C compiler is currently present on the system, with optimizations disabled. The result is the stage-1 compiler. The stage-1 compiler is then used to compile a fully-featured version of our C compiler (including extensions and a fully-featured code generator with optimization), creating the stage-2 compiler. This stage-2 compiler is “feature complete”, but may be slow because it was compiled by the stage-1 compiler which doesn’t have all optimizations, so the stage-2 compiler compiles itself again (with full optimization this time!) to produce the stage-3 compiler, which is the final result (some compilers only use a stage-2 bootstrap process, and some cross compilers may use more stages, but you get the general idea). You can chain compression and filtering stages the same way; indeed, at some point I was bothered by the 1.5k spent on the context modeling depacker and considered adding a very simple pure LZ at the start of the chain (to unpack the unpacker…), but the best I managed was an overall gain of less than 100 bytes (after subtracting the “stage-0” depacker size and overhead), so I didn’t pursue that any further.

### So how much does it help?

All these techniques combined typically reduce final compressed size by about 20% compared to no preprocessing at all, with both the LZ-based and the context model coder (this is true not just with the kkrunchy backends, but also with other compressors like ZIP, RAR, LZMA or PAQ). Compare to the simpler “call offsets only” preprocessing, which typically reduces size by about 10%. That’s clearly the low-hanging fruit right there, but an extra 10% isn’t to be sneezed at, particularly since both the encoding and decoding are really quite easy and quick.

If you’re interested in the details, I made a (cleaned-up version) of the preprocessor available a while ago [here](http://farbrausch.com/~fg/code/disfilter/) (that code is placed into the public domain); there’s extra documentation with some more details in the code. The biggest lacking feature is probably x86-64 support. It shouldn’t be too hard to add, but I never got around to it since I stopped doing size-optimized stuff a while ago, and besides, even now, 64-bit x86 apps are relatively rare.

Anyway, if you have any questions or are interested in extending/using that code somewhere, just drop me a mail (or reply here). I’d certainly like to see it being useful in other contexts!

Thanks ryg, pretty cool about kkrunchy internals!

When I first saw your ppt, and before you released disfilter, I tried to split the exe streams (with an already available x86-x64 disassembler made by Dmitry Shkarin) and trying to compress it with a simple sparse 8 order context-modeling-neural-network without any success.. don’t know why, but the compression was much worse, seems that the compressor was better at recognizing a much larger set of sequence of bytes… I probably did it wrong…

Also I worked a bit on paq8, trying to extract the most efficient context-modelling method for demo exe, and I end up with the “standard” method + the sparse method (and removing all the other models, and SSE/APM stages)… without anykind of filters, the packing was 3% slightly better then kkrunchy… and the code didn’t seem to be complex… but I didn’t have the courage to make it workable for a 64Ko… I guess that there is still some improvement to do in the 64ko compression field… but you did already most the brilliant work on it!

You need to be careful about which streams to separate and which to keep as they are. For example, register numbers (appearing in ModR/M and SIB bytes or as part of the opcode) are nearly random as far as compression is concerned; you don’t want them in a separate stream. Interestingly, Prefix+Op+ModR/M groups are *not* random (and there’s quite some repetition there), so it pays to keep all of them together.

The selection of models in kkrunchy is biased towards speed. I have SSE and one APM stage (since they help and don’t take significant computation time). I also have a “long match” (LZP-like) model because it’s a fairly cheap and non-memory-thrashing way to deal with long deterministic contexts. I have some normal and sparse models (same idea as Crinkler, just use a bitmask to encode which bytes to use as context), but it’s a fairly low number (9 total) since they take a lot of computation time and memory. Also, the hash tables in kkrunchy are *very* small (total model size 5.5mb when compressing a few hundred kb of data, compare to Crinkler which uses >100mb in models to pack a few dozen kilobytes!). This size is fine for fairly redundant source data on the order of a few hundred kilobytes; on anything larger, you get tons of collisions which hurt compression badly.

3% better compared to the total executable size post-kkrunchy, or just the part that’s actually compressed data? And what kkrunchy version are you comparing to? The “a2” version linked on my homepage sucks (first context-modeling based version, had some stupid mistakes in it), newer revisions (at http://www.farbrausch.de/~fg/kkrunchy/test/) are a lot better, but I still stopped working on it in late 2007. With current machines (and current algorithms) you can certainly squeeze out a lot more. Especially if you’re less picky about memory usage. That’s actually another constraint for our 64ks; we tend to use a *lot* of virtual memory in the content generation phase at startup – often >1.2GB – so statically allocating a few hundred megabytes at startup is a no-go.

And remember that kkrunchy also includes EXE header+depackers, so that’s a bit more than 2k of overhead right there. Whenever you do this kind of comparison, you need to take the size of the decompressor into account :). It’s definitely possible to do significantly better than kkrunchy by throwing more or better models at it; what’s in there right now was constrained to keep depacking time for “fr-041: debris” in the sub-8 second range on my then-current P4 2.4GHz. That was my pain threshold between double-clicking and “something happens”. If you’re willing to make the user wait longer (or just assume he has a faster CPU), there’s a lot more you can do :)

>>> 3% better compared to the total executable size post-kkrunchy, or just the part that’s actually compressed data? And what kkrunchy version are you comparing to?

Woops, better to test with latest indeed. With a4, the difference is in favor of kkrunchy, by 0.6%.:), but still the paq8l-light was not using anykind of filters (I even didn’t turn on the simple call/jmp patch). Of course, I took into account the PE+Decompressor size… but as I said, It’s just a rough estimation, without digging into how much that would cost to implement “as-is” a paq8l lightweight version. And we would probably fight against just a couple a hundred of bytes, not enough motivating to implement such compressor! :)

But yeah, sure, kkrunchy is quite optimized in speed and well balanced with its compression ratio, compare to any paq# variants.

Such and excellent read, thanks!

Great read, thanks.

I’ll try to incorporate the methods (if not code) in coreboot, we’re already using lzma, but we’re always low on space.

Thanks for this very interesting article. I didn’t know until now any packer that optimizes anything more complex than e8/e9.

I was thinking of similar techniques to make a re-encoder of x86: a virtualizer that just embeds the same code, but re-optimized for size.

Nice article. Have you considered some of the ways a virus handles its external imports.

Some of them use Hashes to store the external DLL methods.

They load up each library name and compare it to a hash (eg Kernel32.dll might be represented by the double word 0xDEADBEEF and user32.dll might be 0x12345678 ) You save 10 bytes in not storing the string “kernel32.dll”).

The same goes for function addresses.

Normally you call GetProcAddress() with the name of the function (for late loading) but with some viruses they get the name of each function by enumatering the DLL functions, hashing and then checking if the function is a matching hash.

Let me know

I’m aware of Import by Hash, but kkrunchy doesn’t use it since Imports aren’t a big problem in the size range I was targeting and I’d rather avoid the risk of collisions entirely.

Well, the next possible step is to modify C compiler back-end to produce already “prepared” x86 code :-)

Although some may not understand and look at this statement as absurd, he does have a point. Not that any pre-processing should be done by the compiler, but that it can generate more compressible code.

The decompression stub of my product (a competitor I won’t name out of respect) actually tries to make its own code look similar to previous portions of itself. That way, its loader becomes more compressible. Therefore, you could have a new compiler optimization type of: “for compressibility”, lol.

Chris Fraser (of LCC fame) has done some interesting work in that area. Generally, you get better results compressing the compiler IR than you would compressing the original source code. Of course that’s not very interesting for an executable compressor where you pack programs individually and have to keep the overhead small, but the original research was in the context of distributing binaries across a whole system, and in that case the (late-stage) compiler backend can be shared between several programs which amortizes the overhead.

He’s got multiple interesting papers on the subject – check out his list of peer-reviewed papers.

We (farbrausch) at some point seriously considered switching to LCC with a custom size-optimizing backend to get better compression, but in the end we didn’t feel like rewriting our codebase in C98 (from C++). We even briefly considered using Forth (the advantage being that you could skip compilation completely and just use a direct threaded code interpreter), but that never got serious.

And then for .kkrieger we did end up writing and using “lekktor”, a source-level tool that performed code instrumentation to determine code coverage in a first step and then could automatically remove unused code in a second step. It was a terrible hack and a last-ditch effort (we needed to shrink the executable by 4k and didn’t have the time to do it manually), but it worked, and I should write it up sometime :)

It might be a good idea to publish the disfilter source code via GitHub (or Bitbucket, whatever) to enourage more contributors.

An older version is already on Github (as part of the fr_public repository). But so far I’ve had zero indication that anyone actually cares – I can upload it to Github, sure, but I doubt one more repository on Github is gonna suddenly create interest in the project.