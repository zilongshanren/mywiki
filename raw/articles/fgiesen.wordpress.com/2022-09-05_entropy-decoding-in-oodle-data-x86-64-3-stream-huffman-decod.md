---
title: 'Entropy decoding in Oodle Data: x86-64 3-stream Huffman decoders'
url: https://fgiesen.wordpress.com/2022/09/05/entropy-decoding-in-oodle-data-x86-64-3-stream-huffman-decoders/
published: '2022-09-05'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Entropy decoding in Oodle Data: x86-64 3-stream Huffman decoders

The adventure continues! [Last time](https://fgiesen.wordpress.com/2022/04/04/entropy-decoding-in-oodle-data-huffman-decoding-on-the-jaguar/) I went over the core decoder loop we use on AMD Jaguar-based consoles, i.e. Xbox One and PS4. I felt that one was a good example to start with since the target hardware is fixed, behaves quite predictably, and the various features and limitations of the machine conspire to make the solution essentially canonical: the narrow CPU front-end makes it so that minimizing macro-ops issued is a significant concern, and the `BEXTR`

-based decode is a very natural fit.

This time, our hardware target is “any 64-bit x86”, used on less specialized targets like Linux, Windows and Mac 64-bit x86. We don’t have a single CPU type we’re optimizing for; it needs to run on everything, and we’d like to have good performance on anything released within the last 10 years (at the time this code was written in 2016) or so. We do get to have variants for newer ISA extensions when they help but we’d like a good baseline version for “any 64-bit x86 CPU”.

As with the previous two parts, you should read the [introduction](https://fgiesen.wordpress.com/2021/08/30/entropy-coding-in-oodle-data-huffman-coding/) to the Huffman decoders first, continue with the [“Reading bits in far too many ways”](https://fgiesen.wordpress.com/2018/02/19/reading-bits-in-far-too-many-ways-part-1/) series on this blog ([part 2](https://fgiesen.wordpress.com/2018/02/20/reading-bits-in-far-too-many-ways-part-2/), [part 3](https://fgiesen.wordpress.com/2018/09/27/reading-bits-in-far-too-many-ways-part-3/)) which is also a prerequisite, and if you can’t read and understand x86-64 assembly language this will be hard to follow.

### You know how this goes by now

I’m not going into as much detail in this post as I did in the Jaguar one, both because our target this time is somewhat fuzzier and because we’re exploring variations on a theme here. It’s interesting to cover the key ideas, not so interesting to re-do variants of the same analysis many times in a row.

Our setting, then, is the same as it was last time: we have a Huffman code stream where the code lengths are constrained to be relatively short so we can do 5 in a row between refills, we use a 4KiB table with 2048 entries covering all possible 11-bit codewords, and decoding proceeds without having to do any significant data-dependent branches. 1 We know that decoding back-to-back values from the same bitstream is limited by critical path latency, so we use multiple bitstreams.

On the AMD Jaguar, 3 independent bitstreams was sufficient to get us out of the miserable latency-bound hole and into the more desirable throughput-bound regime where we’re doing a decent job keeping the execution units busy. On the wider out-of-order cores that can sustain 4 or more instructions per cycle, 3 streams is not going to be enough for that, which is why we also have 6-stream variants that will be covered in a later part.[2](https://fgiesen.wordpress.com#fn2)

Once again, I’ll go over this from the inside out: first figure out how to decode individual bytes, then sort out the refill strategy, then deal with the remaining plumbing.

### The basic decode step

Our game plan hasn’t changed: peek ahead at the next 11 bits, do our table lookup, consume the right number of bits, emit the resulting byte. The most basic version of this, assuming we keep an explicit “remaining bits” count per stream, works out to something like this:

; peek at low 11 bits mov rcx, rBits and rcx, 2047 ; table fetch movzx ecx, word [rTablePtr + rcx*2] ; shift out consumed bits, update bit count shr rBits, cl sub rBitCount, cl ; emit decoded byte shr ecx, 8 mov [rDest + <index>], cl

So far, there should be no surprises here. 3 As given, this works out to 7 instructions per byte decoded, quite a lot more than the 3 we had in the Jaguar version, but this time we don’t have guaranteed access to BMI instructions – and even if we did, they would not be as good as they are on Jaguar.

### Two more small tweaks

Part of x86’s historical baggage is that bits 8 through 15 inclusive of the a, b, c and d registers can be accessed as their own register, and this can be used on the *emit* sequence to save an instruction, getting us down to 6:

mov [rDest + <index>], ch

Due to the way the x86-64 instruction encoding works out, `rDest`

in this code can’t be just anything. It has to be from a limited set of registers 4 but other than that, we’re still not doing anything special here.

Note that we want to be using `ECX`

as the register we load the table entry into because the variable-distance shifts in basic x86-64 all require the shift amount to live in `CL`

. 5 We don’t particularly care what register name we use for our scratch temporary; RCX/ECX is as good as any other. Nevertheless, using RCX (and only RCX) as the temporary to load table entries into is

*clearly*the right choice here, but compilers would frequently insert extra moves (sometimes more than one extra on the critical path) here, which is how we ended up hand-writing these loops in assembly to begin with.


[6](https://fgiesen.wordpress.com#fn6)The second fun wrinkle is that even though we can easily arrange for our shift count to always be in `CL`

to begin with, on Intel CPUs with BMI2 available, we always want to use the new `SHLX`

instruction instead, even when we’re shifting by the low bits of `RCX`

, because `SHLX`

takes 1 uop instead of 2 or 3 on newer Intel uArchs.[7](https://fgiesen.wordpress.com#fn7)

The final non-obvious change we do for the “real” version of the decode is that instead of the peek logic presented above, we actually do this instead:

mov ecx, 2047 and rcx, rBits

Why load the immediate first using a separate instruction and then AND with `rBits`

? Well, the important realization here is that moving an immediate value into `ecx/rcx`

has no dependencies and can execute at any time, whereas `mov rcx, rBits`

does depend on `rBits`

and thus ends up becoming a part of the critical path. Now this register-register move is generally “free” on microarchitectures that can implement reg-reg moves via renaming at an effective 0-cycle latency, which on the Intel side is Ivy Bridge and later, but there are two important caveats: first, not every machine we’re targeting (or at least were targeting at the time this code was written, 6 years ago) is Ivy Bridge and later, and second, some later microarchitectures had subtle bugs in their implementation of `MOV`

elimination and ended up disabling it later. Hence, as a general rule, the load-immediate-first version is preferable since it takes 1 cycle off the critical path for every decode when `MOV`

elimination is not performed, for whatever reason.[8](https://fgiesen.wordpress.com#fn8)

### Refill

As mentioned above, for this version we prefer the methods with explicit “remaining bits” counts, specifically what I described as variant 4 in my [write-up on bit reading](https://fgiesen.wordpress.com/2018/02/20/reading-bits-in-far-too-many-ways-part-2/).

The reason to prefer this approach here is that it keeps the load for the bit buffer refill independent of the final bit count, meaning that refill load’s latency does not necessarily end up on the critical path. Since the latency along the critical path is the primary concern for this loop, this is definitely what we want.

In the “production” version of the loop, we keep the remaining bit count for stream 0 in `al`

, the refill pointer in `r8`

, and the bit buffer for stream 0 in `r11`

. The version we use is this (with the instructions scheduled slightly differently, but that’s extremely minor):

; refill streams mov rbp, [r8] ; next0 = load(in0) movzx rcx, al ; bitc0 shl rbp, cl ; next0 << bitc0; use shlx with BMI2+! or r11, rbp ; bits0 |= next0 << bitc0 shr ecx, 3 ; 7 - bytes_consumed0 sub r8, rcx ; in0 += bytes_consumed0 - 7 or al, 56 ; bitc0 |= 56 add r8, 7 ; in0 += 7

That’s a fair number of instructions, but the dependency structure is quite favorable:

- The load of the next bits to refill only depends on
`r8`

, which is known as soon as the previous iterations’ refill is complete (all the instructions that update`r8`

are in the above code snippet!) and in particular is completely independent of the 5 table loads per stream. - Insertion of the new bits depends on the final bit count being known, but once the 3 instructions (
`MOVZX`

,`SHL`

,`OR`

, all pure int ALU) for that part of the dependency chain are done, we can start decoding the next byte. - Updating the bit count and the read pointers takes several more instructions, but neither of these are as critical because the bit count doesn’t determine any load offsets and the read pointer is only used for the next iterations’ refill.

Once again, using `SHLX`

for the shift when available is preferred. In this case, in addition to the 2 uops saved, it also lets us remove the 1 cycle for the `MOVZX`

from the critical path.

Beyond that, there’s a few more instructions in the loop to increment the destination pointer, maintain/test the “bytes to decode” count and check whether the input pointers have crossed, but all of this works the same as in the last part and is not on the critical part so I won’t spend time on it here.

### Analysis

With all that said, what’s the expected cost of this decoder? Unlike the Jaguar example which targets a single known microarchitecture, this version of the loop targets a general PC target and thus should be good for numerous uArch generations from multiple vendors over something like a 10-year window.

We have in fact done just that kind of testing, and there are some minor variants (mainly depending on whether BMI2 and thus `SHLX`

is available, as noted above), but the details here get very repetitive and tedious. I don’t particularly feel like writing all of this down, nor would it make for interesting reading.

Instead, I’m going to take a single uArch as our proxy. I’ll be using Intel’s Skylake (SKL), which Intel essentially (in progressively tweaked versions) kept re-releasing in between 2015 and 2021, meaning there’s a nearly 7-year window of Intel consumer CPUs that are all essentially SKL spin-offs. In the notebook space we saw Ice Lake in late 2019 but for desktop, 2021’s Rocket Lake (the first “real” SKL successor for desktop) was neither well-received nor sold well, and was soon replaced by Alder Lake in late 2021.

In practice, this means that at the time of this writing, the mean, median and mode Intel desktop x86 that is at least a year or so old is some SKL variant; during that time AMD made major inroads into the desktop space with their Zen cores (which, fortunately for our analysis, have quite similar performance characteristics). Notebooks are a bit more varied, but if I’m going to look at only one x86 uArch, SKL seems like a solid choice.

As mentioned multiple times throughout this post already, we’re mainly concerned about latency here. As such, I won’t go into many uArch details here and just point out that the relevant cores are a lot wider than the Jaguars we looked at last time (namely, they support 4+ instructions decoded/dispatched/retired per cycle), have 4 integer ALUs, can (under the right conditions) support 2 loads and 1 store per cycle, up to 2 branches per cycle, and in general have just more of essentially everything compared to the small Jaguar cores we looked at last time. (They also typically clock at twice the frequency, or more.)

Ironically, precisely *because* these cores are so much wider, the analysis gets a lot simpler. Here’s the gist of it: the all important critical path between iterations for a single stream starts with the final bit count for the last iteration and then goes through the refill and 5 subsequent symbols decodes until the bit count for the current iteration is known.

In the code as presented above, that means we start with the `MOVZX`

, `SHL`

and `OR`

from the refill (all basic ALU ops that are 1-cycle latency on pretty much every x86 core you can buy these days) until we know the new value of `rBits`

, for 3 cycles refill latency (can be 2 if we use SHLX).

Then we have 5 subsequent decodes where we care about the latency until we have the updated (shifted) rBits. In the version with the hoisted immediate that uses `and rcx, rBits`

, the 3 relevant instructions on that dependency chain are this AND, the table load, and then the shift by CL. The AND and shift are also 1-cycle latency. In the final iteration, we also need to know the final bit count; this is computed by another independent instruction (the `SUB`

) that depends on the table load and is likely to issue at the same time as our shift, so it doesn’t change the latency estimate. Finally, the load is the longest-latency instruction. Now SKL has 4-cycle-latency loads for certain very restricted cases, if the address itself originated on the load unit (i.e. for pointer chasing), but for our table lookup, we have a complicated addressing mode and the index register originates on the ALU not the load unit, so 5-cycle load latency is what we get.

Everything else is not critical, so for now, we’re going to ignore it. What does that leave us with? For one of our 3 streams, the latency along that critical path ends up being 3 + 5×(1 + 5 + 1) = 38 cycles.

Skylake can sustain 4+ fused-domain 9 uOps per cycle during those 38 cycles, giving us 38 × 4 = 152 issue slots. One refill takes around 8 fused-domain uOps (with SHLX), each decode step takes 6. That means one stream’s worth of decodes takes around 8 + 5×6 = 38 uops, so for 3 streams that’s 114 uops out of our budget, leaving another 38 issue slots remaining.

That leaves the work we haven’t accounted for so far: one of our streams needs to do a BSWAP (another 3 uops), we have the two pointer-crossing checks (2-4 uops depending on what macro-fusion happens), the destination pointer increment (1 uop), and the final loop condition/test (1-2 uops, again depending on macro-fusion). And that’s it. At worst, that takes another 10 uops out of our budget.

We’re left with about 124 issue slots used over 38 cycles, about 81% of what the machine can sustain. That leaves enough air in the schedule that we don’t need to be too worried about exactly what the schedulers and port load-balancing logic do; we really do expect to be mostly latency-limited still, but at least latency-limited with a decent uArch utilization. Finally, our instruction mix is balanced enough, and the machine has enough resources, that we needn’t worry too much about any particular type of resource (like say load units or shifters) getting overcrowded.

In short, the best we can expect out of the loop described above is to decode 15 bytes (5 bytes each from 3 streams) every 38 cycles, which works out to 2.53 cycles per byte. In practice, on my Skylake test machine, benchmarks hover around 41.8 cycles per 15 bytes (i.e. around 2.79 cycles/byte), both in the idealized test rig and on real-world data.

That’s approximately 10% above our rough lower-bound estimate, purely from operation latencies, assuming scheduling is perfect, there are no cache misses, and so forth. At this point, we could dig deeper and try to figure out where we’re losing these 3.8 cycles relative to our critical path estimate, and if there’s something we can do about it, but the writing’s already on the wall: with one stream, we would be utterly latency-limited with a mostly-empty machine. The 3 streams we’re using now get us to a more respectable level of uArch utilization, but while they were enough to get us into our target throughput-bound regime on Jaguar, they’re not enough, not even in a lower-bound estimate where there are never any delays due to cache misses or suboptimal uop scheduling.

### Discussion

Really, this should not be a surprise. On a machine twice as wide, with many more execution resources, instructions per cycle, and 2 cycle longer load latency, *of course* we need more streams to hide those latencies.

However, we’re starting to bump into other problems. Our bit-IO method uses 3 registers worth of state per stream: the bits, the bit count, and the refill pointer. That’s 9 registers used. We also definitely need a stack pointer, a destination buffer pointer, at least one scratch register (`rcx`

), and also a base pointer for our Huffman table and preferably also an “end-of-buffer” pointer (or, equivalently, a counter) in a register for the final loop test. That’s 14 registers spoken for, and x86-64 only has 16 GPRs.

Now, some of those registers don’t *need* to be live for most of the loop. The “end-of-buffer” pointer never changes and is only used once at the end so it’s not a big problem to leave in memory, and our refill pointers are only used during refill so we can spill some of them without wreaking havoc if we don’t mind the extra instructions to spill and reload them, but we’re getting on thin ice here.

Using more streams would be interesting, but we need to be careful not to introduce a lot of extra instructions. Potentially troublesome spills/refills introducing latency in the wrong places would suck as well. In short, we’d like a few more streams (just one extra is cutting it too close), but that in turn means 3 GPRs per stream is not going to work. We need something more compact, which leads us to a quite different design for the 6-stream decoders we added in Oodle 2.3.0. But that will have to wait for another post. Until then!

### Footnotes

[1] The “how many bytes are left” loop condition is just a counted loop and *extremely* predictable. The “did the pointers cross” check is technically data-dependent, but it is also extremely predictable (in the fast decoder loops anyway), because the decoder loops only run until our already-advanced pointers first cross, at which point we exit the fast loops and switch to the more careful variants.

[2] The trickiest part to negotiate when doing this experimentally is the transition from latency- to throughput-bound. As long as you’re latency-bound, your best move is to use strategies that minimize latency, even when doing so increases dynamic instruction count or utilization of limited execution resources. Once you have enough streams to cover the critical path latency with some slack left over, you need to worry about those bottlenecks instead, even when doing so adds latency. Options that were clearly inferior in the latency-bound regime will end up preferable in the throughput-bound regime.

[3] When writing this code in C/C++, you would probably keep the remaining bit count for the bit buffer in a 32- or 64-bit integer, not a byte, but done naively that would result in an extra instruction to extract and zero-extend the “length” field from the low 8 bits of the table entry. Using a byte register avoids the extra instruction, or alternatively, you could subtract the full 16-bit table entry from the bit count and mask the final bit count down to 8 bits (effectively reducing modulo 256) before using it. The two approaches are equivalent; for this presentation I went with the byte register variant because it’s more straightforward.

[4] x86-64 was designed to share as much of the instruction encoding (and hence the decoder logic) between the 32-bit and 64-bit versions. 32-bit x86 has 8 general-purpose registers and 3-bit register numbers; x64-64 increases this to 16 GPRs (which take 4 bits), and the high bits of the up to 3 register numbers in an instruction are grouped together in what’s called a REX prefix byte. Only some instructions have a REX prefix: if all 3 register number high bits are zero and the instruction is not 64-bit either, it’s not required. However, the register numbering for 8-bit registers worked differently than it did for the other registers: for “classic” x86 code, the 8 8-bit registers are AL, CL, DL, BL, AH, CH, DH, and BH (in that order), where those last 4 are refer to [15:8] in the corresponding 32-bit register. With the REX prefix present, every 64-bit register has its low 8 bits addressable as a corresponding “L” register, but the “H” register names are inaccessible. Thus, if you want to store `CH`

to `[rDest + immed]`

, `rDest`

needs to be one of the low 8 registers.

[5] Other (non-x86) architectures mostly don’t care about which architectural register the shift amount lives in, but almost everyone looks only at the low 5-8 bits (depending on architecture and context) of the shift count. This makes it so that arranging our (len,sym) pairs so that len is in the low byte (which for LE byte order means first byte) is almost universally the best choice.

[6] Hand-writing in ASM also made it practical to use the “store from CH” trick, which is not a huge deal in this particular version since there are other problems that we’ll get to in a minute, but this particular quirk of x86 is one that compilers generally won’t even try to use, even though it’s advantageous in cases like this one.

[7] This is one of my “favorite” x86 warts. The reason `SHL`

by CL is awkward, and often more uOps than you would expect, is because the architectural definition of this (and other variable-shift instructions) is quite strange for backwards-compatibility reasons. Namely, all the shift-by-CL instructions set different flags (and set them in different ways) depending on whether the effective shift count ends up being 0, 1, or something else. This goes back to a problem with the original 8086. The 8086 didn’t have a barrel shifter or any other way to do fast distant shifts; “`SHL AX, CL`

” existed but effectively just repeated `SHL AX, 1`

`CL`

times. This definition was presumably convenient given the *extremely* limited microcode ROM space the 8086 worked with but has the two unfortunate side effects that a) you could make shifts take a very long time on the 8086 by setting `CL`

to 255 and b) when CL is 0, no shifting takes place at all, and in particular the flags stay unchanged from before. Moreover, there’s another wrinkle in that `SHL AX, 1`

sets the overflow flag “correctly” (probably mostly by accident, because for left-shifts specifically the natural implementation of it on a 8086-like ALU data path is `ADD AX, AX`

, which does, and right-shifts can’t overflow), but when doing an iterated sequence of such shifts, the final overflow flag will indicate whether the last shift-by-1 overflowed, which is useless when the count is not 1, because for a “shift by 3” operation what you really want to know is whether there was an overflow at any point during the process, not whether the last instruction in a lengthy expansion overflowed (which is neither here nor there). The tightened definition that appears in the original 80286 manuals specifies that only the last 5 bits of the shift count matter (no doubt anticipating the coming expansion to 32-bit with the 80386) and further says that 1-bit-shifts set the overflow flag correctly but multi-bit shifts leave the overflow flags in an undefined state (not mentioned in these early manuals is that an effective shift count of 0 leaves the flags unchanged, but all x86 CPUs I’m aware of nevertheless behave this way). Long story short, the actual data portion of x86 `SHL reg, CL`

is exactly what you would expect, but which flags get updated and how is a tangled mess that, on most Intel CPUs, takes another 1 or 2 uops to resolve. Interestingly, no AMD uArchs I’m aware of, present or historical, have a problem with it.

[8] Another option available on machines with BMI1 or later is to use `ANDN`

to perform our AND operation. The idea is to put the ones’ complement of our desired mask (so `~2047`

) into a scratch register and then use `andn rcx, rInvertedMask, rBits`

to initialize `rcx`

. In short, we don’t actually care about the “not” part of the `ANDN`

, but it conveniently comes as a non-destructive 3-operand instruction that we can use to avoid the move. This does the job in one instruction, which is great, but requires us to sacrifice another register, which is not so great. In this particular code it’s not really worthwhile since we’re entirely latency-limited on sufficiently wide cores, so having a `MOV`

/`AND`

pair is not a problem as long as we don’t extend the critical path unnecessarily.

[9] I won’t go into what exactly fused-domain uOps are; it’s there for precision, but if you don’t know what that means, just ignore it, it’s way beyond the scope of what we need for this post.

Nice to see anyone coding in assembly these days :)