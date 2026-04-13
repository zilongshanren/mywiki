---
title: How many x86 instructions are there?
url: https://fgiesen.wordpress.com/2016/08/25/how-many-x86-instructions-are-there/
published: '2016-08-25'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# How many x86 instructions are there?

It’s surprisingly hard to give a good answer (the question was raised in [this article](http://pepijndevos.nl/2016/08/24/x86-instruction-distribution.html)). It depends on how you count, and the details are interesting (to me anyway).

To not leave you hanging: Intel has an official x86 encoder/decoder library called [XED](https://software.intel.com/en-us/articles/xed-x86-encoder-decoder-software-library). According to Intel’s XED, as of this writing, there are 1503 defined x86 instructions (“iclasses” in XED lingo), from `AAA`

to `XTEST`

(this includes AMD-specific extensions too, by the way). Straightforward, right?

Well, it depends on what you wanted to count. For example, as per XED, `ADD`

and `LOCK ADD`

are different “instruction classes”. Many assembly programmers would consider `LOCK`

a prefix and `LOCK ADD`

an addition with said prefix, not a distinct instruction, but XED disagrees. And in fact, for the purposes of execution, so do current x86s. An atomic add does very different things from a regular add. The prefix thing crops up elsewhere: is say `MOVSD`

(copy a single 32-bit word) a different “instruction class” from `REP MOVSD`

(block copy several 32-bit words)? XED says yes. But it doesn’t handle *all* prefixes this way in all contexts. For example, the operand-size prefix (`0x66`

) turns integer instructions operating on 32-bit registers into the equivalent instruction operating on their lower 16-bit halves, but unlike with the `REP`

or `LOCK`

prefixes, XED does not count these as separate instruction classes. If you disagree about any of these choices, your count will come out different.

### Mnemonics

It all depends on how precisely we define an instruction. Is it something with a distinct mnemonic? Let’s first look at what the article I quoted above says is by far the most common x86 instruction, at 33% of the total sample set: `MOV`

. So let’s look up MOV in the Intel Architecture manuals. And… there are 3 different top-level entries? “MOV—Move”, “MOV—Move to/from Control registers”, “MOV—Move to/from Debug Registers”. The latter are sufficiently distinct from “regular” `MOV`

to rate their own documentation pages, they have completely different instruction encodings (not even in the same encoding block as regular `MOV`

), and they’re privileged instructions, meaning lowly user-mode code isn’t even allowed to execute them. Consequently they’re also extremely rare, and are likely to account for approximately 0% of the test sample. And, sure enough, XED counts them as separate instruction classes (`MOV_CR`

and `MOV_DR`

).

So these instructions may be *called* `MOV`

, but they’re weird, special snowflakes, and from the processor’s point of view they’re entirely different instructions in a different part of the encoding space and with different rules. Calling them `MOV`

is essentially nothing but syntactic sugar in the official Intel assembly language.

And on the subject of syntactic sugar: some mnemonics are just aliases. For example, `SAL`

(shift arithmetic left) is a long-standing alias for `SHL`

(shift left). Both are just bit shifts; there is no distinction between “arithmetic” and “logical” left shifts like there is between arithmetic and logical right shifts, but the Intel manuals list `SAL`

(with an encoding that happens to be the same as `SHL`

) and all x86 assemblers I’ve ever used accept it. Hilariously, in official Intel syntax, we’re simultaneously miscounting in the other direction, since at least two mnemonics got assigned twice: we already saw the “copy” variant of `MOVSD`

(which has no explicit operands), but there’s also `MOVSD`

as in “move scalar double” (which always has two explicit operands) which is an entirely different instruction (XED calls it `MOVSD_XMM`

to disambiguate, and the same problem happens with `CMPSD`

).

There’s also SSE compares like `CMPSD`

(the two-operand one!) and `CMPPS`

. XED counts these as one instruction each. But they have an 8-bit immediate constant byte that specifies what type of comparison to perform. But disassemblers usually won’t produce the hard-to-read `CMPSD xmm0, xmm1, 2`

; they’ll disassemble that instruction as the pseudo-instruction `CMPLESD`

(compare scalar doubles for lesser-than-or-equal) instead. So is `CMPSD`

one instruction (just the base opcode with an immediate operand), is it 8 (for the 8 different standard compare modes), or something else?

This is getting messy. AT&T syntax to the rescue? Well, it solves some of our problems but also introduces new ones. For example, AT&T adds suffixes to the mnemonics to distinguish different operation widths. What Intel calls just `ADD`

turns into `ADDB`

(8-bit bytes), `ADDW`

(16-bit “words”), `ADDL`

(32-bit “long words”) and `ADDQ`

(64-bit “quadwords”) in x86-64 AT&T syntax. Do we count these as separate? As per Intel syntax, no. As per XED instruction classes, also no. But maybe we consider these distinct enough to count separately after all? Or maybe we decide that if our definition depends on the choice of assembly syntax, of which there are several, then maybe it’s not a very natural one. What does the machine do?

### Instruction bytes

Note I haven’t specified what part of the machine yet. This is thorny too. We’ll get there in a bit.

But first, instruction bytes. Let’s look at the aforementioned manual entry for real now: “MOV—Move”. If you check that page out in the current Intel Architecture Software Developer’s Manual, you’ll find it lists no less than *thirty-four encodings* (not all of them distinct; I’ll get to that). Some of these are more special, privileged operations with special encodings (namely, moves to and from segment registers). This time, XED doesn’t seem to consider segment register loads and stores to be special and lumps them into plain old `MOV`

, but I consider them distinct, and the machine considers them distinct enough to give them a special opcode byte in the encoding that’s not used for anything else, so let’s call those distinct.

That leaves us with 30 “regular” moves. Which are… somewhat irregular: 10 of them are doing their own thing and involve moves between memory and different parts of the `RAX`

(in 64-bit mode) register, all with a special absolute addressing mode (“moffs”) that shows up in these instructions and, to my knowledge, nowhere else. These instructions exist, and again, pretty much nothing uses them. They were useful on occasion in 16-bit mode but not anymore.

This specialness of the accumulator register is a recurring theme in x86. “`op`

(AL/AX/EAX/RAX), something” has its own encoding (usually smaller) and various quirks for a lot of the instructions that go back to the 8086 days. So even though an asssembly programmer might consider say `TEST ebx, 128`

and `TEST eax, 128`

the same instruction (and the XED instruction class list agrees here!), these have different opcodes and different sizes. So a lot of things that look the same in an assembly listing are actually distinct for this fairly random reason. Keep that in mind. But back to our MOV!

The remaining 20 listed MOV variants fall into four distinct categories, each of which has 5 entries. These four categories are:

- “Load-ish” – move from memory or another same-sized register to a 8/16/32/64-bit register.
- “Store-ish” – move from a 8/16/32/64-bit register to either another register of the same size, or memory.
- “Load-immediate-ish” – load an integer constant into a 8/16/32/64-bit register.
- “Store-immediate-ish” – store an integer constant to either a 8/16/32/64-bit memory location, or a register.

All processor have some equivalent of the first three (the “store immediate” exists in some CPU architectures, but there’s also many that don’t have it). Load/store architectures generally have explicit load and store instructions (hence the name), and everyone has some way to load immediates (large immediate constants often require multiple instructions, but not on x86) and to move the content of one register to another. (Though the latter is not always a dedicated instruction.) So other than the fact that our “load-ish” and “store-ish” instructions also support “storing to” and “loading from” a register (in particular, there’s two distinct ways to encode register-register MOVs), this is not that remarkable. It does explain why MOVs are so common in x86 code: “load”, “store” and “load immediate” in particular are all very common instruction, and MOV subsumes all of them, so of course you see plenty of them.

Anyway, we have four operand sizes, and four categories. So why are there *five* listed encodings per category? Okay, so this is a bit awkward. x86-64 has 16 general-purpose registers. You can access them as 16 full 64-bit registers. For all 16 registers, you can read from (or write to) their low 32-bit halves. Writing to the low 32-bit half zero-extends (i.e. it sets the high half to zero). For all 16 register, you can read from (or write to) their low 16-bit quarter. Writing to the low 16-bit quarter of a register does *not* zero-extend; the remaining bits of the register are preserved, because that’s what 32-bit code used to do and AMD decided to preserve that behavior when they specced 64-bit x86 for some reason. And for all 16 registers, you can read from (or write to) their low 8-bit eighth (the lowest byte). Writing the low byte again preserves all the higher bytes, because that’s what 32-bit mode did. With me so far? Great. Because now is when it gets weird. In 16-bit and 32-bit mode, you can also access bits 8 through 15 of the A, B, C and D registers as `AH`

, `BH`

, `CH`

and `DH`

. And x86-64 mode still lets you do that! But due to a quirk of the encoding, that works only if there’s no REX prefix (which is the prefix that is used to extend the addressable register count from 8 to 16) on the instruction.

So x86-64 actually has a total of 20 addressable 8-bit registers, in 3 disjoint sets: `AL`

through `DL`

, which can be used in any encoding. `AH`

through `DH`

, which can only be accessed if no REX prefix is present on the instruction. And the low 8 bits of the remaining 12 registers, which can only be accessed if a REX prefix is present.

This quirk is why Intel lists all 8-bit variants twice: once without REX and one with REX, because they can access slightly different parts of the register space! Alright, but surely, other than that, we must have 4 different opcodes, right? One each for move byte, word, doubleword, quadword?

Nope. Of course not. In fact, in each of these categories, there are two different opcode bytes: one used for 8-bit accesses, and one for “larger than 8-bit”. This dates back to the 8086, which was a 16-bit machine: “8-bit” and “16-bit” was all the distinction needed. Then the 386 came along and needed a way to encode 32-bit destinations, and we got the already mentioned operand size prefix byte. In 32-bit mode (handwaving here, the details are a bit more complicated), the instructions that *used* to mean 16-bit now default to 32-bit, and getting actual 16-bit instrutions requires an operand size prefix. And I already mentioned that 64-bit mode added its own set of prefixes (REX), and this REX prefix is used to upgrade the now default-32-bit “word” instructions to 64-bit width.

So even though Intel lists 5 different encodings of the instructions in each group, all of which have somewhat different semantics, there’s only 2 opcodes each associated to them: “8-bit” or “not 8-bit”. The rest is handled via prefix bytes. And as we (now) know, there’s lots of different types of MOVs that do very different things, all of which fall under the same XED “instruction class”.

Maybe instruction classes is the wrong metric to use? XED has another, finer-grained thing called “iforms” that considers the different subtypes of instructions separately. For example, for the just-discussed MOV, we get this list:

XED_IFORM_MOV_AL_MEMb=804, XED_IFORM_MOV_GPR8_GPR8_88=805, XED_IFORM_MOV_GPR8_GPR8_8A=806, XED_IFORM_MOV_GPR8_IMMb_C6r0=807, XED_IFORM_MOV_GPR8_IMMb_D0=808, XED_IFORM_MOV_GPR8_MEMb=809, XED_IFORM_MOV_GPRv_GPRv_89=810, XED_IFORM_MOV_GPRv_GPRv_8B=811, XED_IFORM_MOV_GPRv_IMMv=812, XED_IFORM_MOV_GPRv_IMMz=813, XED_IFORM_MOV_GPRv_MEMv=814, XED_IFORM_MOV_GPRv_SEG=815, XED_IFORM_MOV_MEMb_AL=816, XED_IFORM_MOV_MEMb_GPR8=817, XED_IFORM_MOV_MEMb_IMMb=818, XED_IFORM_MOV_MEMv_GPRv=819, XED_IFORM_MOV_MEMv_IMMz=820, XED_IFORM_MOV_MEMv_OrAX=821, XED_IFORM_MOV_MEMw_SEG=822, XED_IFORM_MOV_OrAX_MEMv=823, XED_IFORM_MOV_SEG_GPR16=824, XED_IFORM_MOV_SEG_MEMw=825,

As you can see, that list basically matches the way the instruction encoding works, where 8-bit anything is considered a separate instruction, but size overrides by way of prefixes are not. So that’s basically the rule for XED iforms: if it’s a separate instruction (or a separate encoding), it gets a new iform. But just modifying the size of an existing instruction (for example, widening MMX instructions to SSE, or changing the size of a MOV via prefix bytes) doesn’t.

So how many x86 instructions are there if we count distinct iforms as distinct? Turns out, an even 6000. Is that all of them? No. There are some undocumented instructions that XED doesn’t include (in addition to the several formerly undocumented instructions that Intel at some point just decided to make official). If you look at the Intel manuals, you’ll find the curious “UD2”, the defined “Undefined instruction” which is architecturally guaranteed to produce an “invalid opcode” exception. As the name suggests, it’s not the first of its kind. Its older colleague “UD1” half-exists, but not officially so. Since the semantics of UD1 are exactly the same as if it was never defined to begin with. Does a non-instruction that is non-defined and unofficially guaranteed to non-execute exactly as if it had never been in the instruction set to begin with count as an x86 instruction? For that matter, does UD2 itself, the defined undefined instruction, count as an instruction?

### Instruction decoders

But back to those iforms: 6000 instructions, huh? And these must all be handled in the decoder? That must be *terrible*.

Well, no. Not really. I mean, it’s not pleasant, but it’s not the end of the world.

First off, let’s talk about how x86 is decoded in the first place: all x86 CPUs you’re likely to interact with can decode (and execute) multiple instructions per cycle. Think about what that means: we have an (aggressively!) variable-length encoding, and we’re continually fetching instructions. These chips can decode (given the right code) 4 instructions per clock cycle. How does that work? They’re variable-length! We may know where the first instruction we’re looking at in this cycle starts, but how does the CPU know where to start decoding the second, third, and fourth instructions? That’s straightforward when your instructions are fixed-size, but for x86 they are most certainly not. And we *do* need to decide this quickly (within a single cycle), because if we take longer, we don’t know where the last instruction in our current “bundle” ends, and we don’t know where to resume decoding in the *next* cycle!

You do not have enough time in a 4GHz clock cycle (all 0.25ns of it) to fully decode 4 x86 instructions. For that matter, you don’t even have close to enough time to “fully

decode” (what exactly that means is fuzzy, and I won’t try to make it precise here) one. Two basic ways to proceed: the first is simply, don’t do that! Try to avoid it at all cost. Keep extra predecoding information (such as marking the locations where instructions start) in your instruction cache, or keep a separate decoded cache altogether, like Intels uOp caches. This works, but it doesn’t help you the first time round when you’re running code that isn’t currently cached.

Which brings us to option two: *deal with it*. And the way to do it is pretty much brute force. Keep a queue of upcoming instruction bytes (this ties in with branch target prediction and other things). As long as there’s enough space in there, you just keep fetching another 16 (or whatever) instruction bytes and throw them into the queue.

Then, *for every single byte position in that queue*, you pretend that an x86 instruction starts at that byte, and determine how long it is. Just the length. No need to know what the instruction is. No need to know what the operands are, or where the bytes denoting these operands are stored, or whether it’s an invalid encoding, or if it’s a privileged instruction that we’re not allowed to execute. None of that matters at this stage. We just want to know “supposing that this is a valid instruction, what is it’s length?”. But if we add 16 bytes per cycle to the queue, we need 16 of these predecoders in parallel to make sure that we keep up and get an instruction length for every single possible starting location. We can pipeline these predecoders over multiple cycles if necessary; we just keep fetching ahead.

Once our queue is sufficiently full and we know that size estimate for every single location in it, *then* we decide where the instruction boundaries are. That’s the stage that keeps track. It grabs 16 queue entries (or whatever) starting at the location for the current instruction, and then it just needs to “switch through”. “First instruction says size starting from there is 5 bytes, okay; that means second instruction is at byte 5, and the queue entry says that one’s 3 bytes; okay, third instruction starts at byte 8, 6 bytes”. No computation in that stage, just “table lookups” in the small size table we just spent a few cycles computing.

That’s one way to do it. As said, very much brute force, but it works. However, if you need 16 predecoders (as you do to sustain a fetch rate of 16 bytes/cycle), then you really want these to be as dumb and simple as you can possibly get away with. These things most certainly don’t care about 6000 different iforms. They just squint at the instruction *just enough* to figure out the size, and leave the rest for later.

Luckily, if you look at the actual [opcode map](http://sandpile.org/x86/opc_1.htm), you’ll see that this is not all that bad. There’s large groups of opcodes that all have basically the same size and operands, just with different operations – which we don’t care about at this stage at all.

And this kind of pattern exists pretty much everywhere. For example, look at that conspicuous, regular block of integer ALU instructions near the top of the opcode map. These all look (and work) pretty similar to the CPU. Most of them have essentially the same encodings (except for a few opcode bits that are different) and the same operand patterns. In fact, the decoder really doesn’t care whether it’s an `OR`

, an `ADD`

, a `CMP`

, or a `XOR`

. To an assembly-language programmer, a compiler, or a disassembler, these are very different instructions. To the CPU instruction decoder, these are all pretty much the same instruction: “ALU something-or-other mumble-mumble don’t care”. Which one of these gets performed will only be decided way later (and probably only after that operation make it to the ALU itself). What the decoder cares about is whether it’s an ALU instruction with an immediate operand, or if it has a memory operand, and what that memory operand looks like. And the instructions are conveniently organized in groups where the answers to these questions are always the same. With plenty of exceptions of course, because this is still x86, but evidently it can be made to work.

### Further down the pipe

Instructions really don’t get decoded all at once, in one big “switch statement”, and after that they go to disjoint parts of the chip never to meet again. That’s not how these things are built. There’s plenty of similarity between different instructions, and the “understanding” of what an instruction does is distributed, not centralized.

For example, for the purposes of most of the instruction decoder, the SSE2 instructions `ADDPS`

, `SUBPS`

, `MULSD`

and `DIVPD`

are all pretty much the same thing. They’re FP ALU instructions, they accept the same types of operands, all of which are in the same place.

Some of these instructions are so similar that they’re almost certain to never fully get “decoded”. For example, for IEEE floats, a subtraction is literally just an addition where the sign bit of the second operand is flipped. If you look at the opcode table, the difference between the encoding for ADDPS and SUBPS is precisely one flipped bit: that bit is clear for ADDPS and set for SUBPS. Literally all you need to do to support both instructions is to decode them the same, make sure to grab that one bit from the instruction, and then feed it (along with the original second operand sign bit) into a single XOR gate in front of the FP adder. That’s it. You now support both floating point addition and subtraction.

Some of these differences matter more. For example, FP multiplies go to a different functional unit than FP adds, and they have a different latency. So the data needs a different routing, and the latency for say an add and a multiply is different, which the schedulers care about. If there’s a memory load involved, then the load unit needs to know what size of access, and what part of the operand bypass network to send the results to (integer, float/SIMD?). So there’s a bunch of control signals computed eventually that express the differences between all these instructions. But a lot of it happens really late. There’s certainly no big monolithic 6000-case “switch statement” anywhere.

And then there’s further differences still. For example, MOV elimination. Many x86s can in many cases avoid real execution of register-register MOVs altogether. They just resolve it as part of their register renaming. Likewise, zeroing a register by XORing it with itself (something the author of the original article I linked to) gets resolved by renaming that register to point to a hard-wired zero register and likewise doesn’t actually take any execution resources (even though it still needs to decode).

Where does that fit in our taxonomy? `MOV rax, rbx`

will most often take 0 cycles, but sometimes take 1 cycle due to various reasons. Does the 0-cycle version, when it happens, count as a special instruction? Is `XOR rax, rax`

(which goes down the magic implicit zeroing path and takes 0 cycles to execute) a different instruction from `XOR rax, rcx`

which is encoded essentially the same way? These two instructions differ by exactly 1 bit in both the assembly-language source file and the assembled object code, yet execute in drastically different ways and with different latencies. Should that make them a separate instruction or not? The most useful answer really depends on what part of the pipeline you’re interested in. If you’re designing a CPU core, they pretty much are separate instructions. If you’re writing a disassembler, they are not.

### In conclusion…

So, is there a point to all this? I wrote it because I think it’s fun, but is there something to learn here?

I think so. It makes a wonderful example for a general phenomenon I’ve encountered in a lot of different situations: questions to which a ballpark answer is fairly easy to give, but that keeps getting gnarlier the more you try to pin it down. It’s essentially an instance of the “[coastline paradox](https://en.wikipedia.org/wiki/Coastline_paradox)“: the closer you look, the more detail you see, and the more the answer changes.

Suppose I ask you “where am I?”, and I’m okay with getting an answer that’s within about 10 meters or so. If you have a handheld GPS unit, you can just hand it to me, and if I look at the display I’ll get an answer. If I ask “where am I, down to the millimeter?”, things get a lot more complicated. Specifying the position of a person down to a meter or so makes sense, but specifying it down to a millimeter does not. Position of *what* exactly? My center of gravity? The position of my center of gravity, projected onto the ground? The position of the tip of my nose? The center point of the hangnail on my left pinky? You can’t answer that question precisely when the uncertainty inherent in the question is so much larger than the level of precision you’re aiming at.

And by the way, I used x86 as an example here, but don’t believe *for a second* the same thing doesn’t apply to, say, the ARM chip in your phone. Modern ARM chips support *multiple* encodings and also rank over 1000 instructions if you count them at the same level of granularity as XEDs “iforms”. In fact it’s pretty easy to get high instruction counts on any architecture as soon as any kind of vector/SIMD instruction set is involved, since most of them basically come in the form of “instantiate these 40 instructions for 10 different data types” (with lots of special magic that is either typeless only works on certain types, of course). And yeah, x86 has plenty of historical warts in its encoding, but so does ARM – many of them on display in the current generation of chips, where chip makers have the pleasurable task of designing 3 distinct instruction decoders: old-school 32-bit ARM or “A32”, the more compact but variable-size Thumb-2 or “T32”, and the fixed-size-again 64-bit “A64” encoding.

This was very interesting, but i want to hang on to one point.

You said movs can be implemented implicitly by register renaming. When i tried to iaca a program( on Sandy bridge, everything on fp sse henceforth), i saw that there was too much pressure on port 5 that dealt with movs, so i turned some mov instructions to xoring dest, dest and xoring(or adding) dest, src. And so, turning the one cycle on port 5 to one cycle on ports 0/1.

Can it be that keeping the movs have been a better move?

Renaming can only handle register-to-register moves (and not always!). It can’t deal with actual loads or stores (with a memory operand), nor immediate loads, nor immediate stores. Register-to-register moves are still quite common, but that’s a pretty significant restriction.

On the CPUs that implement MOV eliimination (which is Ivy Bridge and up on the Intel side, but not Sandy Bridge!) there’s generally litle reason to avoid such moves. You dont want to introduce them pointlessly (they still cost you code size and need to be decoded!) But yes, on older microarchitectures and especially on the FP/SSE paths, you can run into cases like the one I mention, where moves turn into a bottleneck because they wan to go to a heavily utilized port. That said, I wouldn’t sweat it too much: you need to be averaging well over 1 instruction per cycle for that to become a limiting factor, which is already pretty good for most code, and this is only on the older uArchs without the MOV eliimination at that! You generally run into other, worse problems (like cache misses) earlier than that.

specifically for that piece of code, everything was read sequentially so everything was clear for the cpu to prefetch into l1 cache, other parts of the code base didn’t fare so wel.

now that you say that the renaming started in ivy bridge i can relax about using iaca, so thank you, though i upgraded to a SKL and it isn’t supported by iaca yet, though they say they will do it by end of 2016 maybe.

One nice thing about SPUs, the entire instruction set fit on a single page – with brief descriptions!

Hey, I was a little surprise when you said that something “takes 0 cycles to execute”. Could you elaborate what you mean by that ?

“0 cycles latency” for a MOV means that anything that depends on the results of the MOV will issue in the same cycle as the MOV itself. (The MOV is eliminated after decoding.)

Fabian, some of the guys at Stanford just released an interesting paper that ties into this somewhat: “Stratified Synthesis: Automatically Learning the x86-64 Instruction Set”

(https://raw.githubusercontent.com/StanfordPL/stoke/develop/docs/papers/pldi16.pdf)

I like how they systematically approached identifying and testing every instruction, up to Haswell I think. They found some errors in Intel’s docs on the behavior of some instructions.

The reason they rolled up their sleeves to do this was so that they could build the STOKE superoptimizer, which is also interesting: https://github.com/StanfordPL/stoke They needed to know every possible instruction in order to generate optimal code for any given source sequence.

I hope RISC-V will save us.