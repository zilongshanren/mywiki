---
title: Loop control overhead on x86
url: https://fgiesen.wordpress.com/2011/02/17/loop-control-overhead-on-x86/
published: '2011-02-17'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Loop control overhead on x86

This is gonna be a short one. Let’s start with this simple loop to compute the dot product of two vectors vec_a, vec_b of signed 16-bit values:

; (rsi=vec_a, rdi=vec_b, rcx=N_elements/16) pxor xmm0, xmm0 pxor xmm1, xmm1 dot_loop: movdqa xmm2, [rsi] movdqa xmm3, [rsi+16] pmaddwd xmm2, [rdi] pmaddwd xmm3, [rdi+16] paddd xmm0, xmm2 paddd xmm1, xmm3 add rsi, 32 add rdi, 32 dec rcx jnz dot_loop

There’s nothing really wrong with this code, but it executes more ops per loop iteration than strictly necessary. Whether this actually costs you cycles (and how many) heavily depends on the processor you’re running on, so I’ll dodge that subject for a bit and pretend there’s no out-of-order execution to help us and every instruction costs at least one cycle.

Anyway, the key insight here is that we’re basically using three registers (`rsi`

, `rdi`

, `rcx`

) as counters, and we end up updating all of them. The key is to update less counters and shift some of the work to the magic x86 addressing modes. One way to do this is to realize that while `rsi`

and `rdi`

change every iteration, `rdi - rsi`

is loop invariant. So we can compute it once and do this:

sub rdi, rsi pxor xmm0, xmm0 pxor xmm1, xmm1 some_loop: movdqa xmm2, [rsi] movdqa xmm3, [rsi+16] pmaddwd xmm2, [rsi+rdi] pmaddwd xmm3, [rsi+rdi+16] paddd xmm0, xmm2 paddd xmm1, xmm3 add rsi, 32 dec rcx jnz some_loop

One `sub`

extra before the loop, but one less `add`

inside the loop (of course we do that work in the addressing modes now, but luckily for us, they’re basically free).

There’s a variant of this that computes `vec_a_end = rsi + rcx*32`

at the start and replaces the `dec rcx`

with a `cmp rsi, vec_a_end`

. Two more instructions at the loop head, no instructions saved inside the loop, but we get a `cmp`

/`jne`

pair which Core2 onwards can fuse into one micro-op, so that’s a plus. VC++ will often generate this style of code for simple loops.

We can still go one lower, though – there’s still two adds (or one add+one compare), after all! The trick is to use a loop count in bytes instead of elements and have it count up from `-sizeof(vec_a)`

to zero, so we can still use one `jnz`

at the end to do our conditional jump. The code looks like this:

shl rcx, 5 ; sizeof(vec_a) pxor xmm0, xmm0 pxor xmm1, xmm1 add rsi, rcx ; end of vec_a add rdi, rcx ; end of vec_b neg rcx some_loop: movdqa xmm2, [rsi+rcx] movdqa xmm3, [rsi+rcx+16] pmaddwd xmm2, [rdi+rcx] pmaddwd xmm3, [rdi+rcx+16] paddd xmm0, xmm2 paddd xmm1, xmm3 add rcx, 32 jnz some_loop

The trend should be clear at this point – a few more instrs in the loop head, but less work inside the loop. How much less depends on the processor. But the newest batch of Core i7s (Sandy Bridge) can fuse the `add`

/`jnz`

pair into one micro-op, so it’s very cheap indeed.

Careful. The complex addressing modes add at least an SIB byte to each instruction, so you can hit the 16-bytes-per-clock decode limit (i.e. you’re not going to get 4 instructions per clock). The uop cache will help hide this.

Also I believe on some processors the AGU needs extra cycles or RF ports to process the complex addressing modes. Especially as in this case you remove one “add” but add in two complex address calculations.

In practice on the big cores the above code is probably 100% dominated by inherent data latencies, so you might not see any interesting performance difference between any of the versions. The rules for the smaller cores (Atom, etc) do still tend to follow the rule that fewer instructions = better.

16 byte/clock limit: Not much of an issue in small loops (uop cache on SNB/loop buffer on Core2). Besides, at least with SIMD code, you don’t usually get the 4 instrs/clock anyway unless you have lots of scalar work inbetween – not enough execution units to complete more than 2 SIMD ops/cycle, usually (this goes for both int and float). E.g. on SNB, the example has one fused uop for the pmaddwd (unfused 1 uop port 0 for the mult + 1 uop port 2/3 for memory read) and one uop for the paddd (port 0 or 5, 0 is already taken so 5). So in this loop you can’t complete more than 2 SIMD ops/cycle, and you don’t need to decode any more (you do want to decode the loop control stuff in parallel with the rest, of course, but both are fairly small).

Reduce-style operations are something of a headache anyway since they’re basically one long dependency chain; you can get some win for associative ops by splitting into several chains and interleaving them, but at least in 32-bit mode you quickly run out of registers if you try to do that. Non-“reduce”-style operations that don’t have SIMD dependency chains spanning across loop iterations fare much better in this regard. Assuming the branch prediction doesn’t screw you (and the loop isn’t too long), OoO effectively ends up overlapping the different loop iterations which gives almost perfect pipelining even if every single instruction in the loop depends on the previous one. Did some experiments a few months ago on Core2 with code that evaluated Chebyshev polynomials using the standard recurrence; the obvious code looks like it would stall a lot, but what actually happened was that the sequence (24 instrs for degree 8 polynomials IIRC, or was it 25?) was short enough that I’d get some overlap/OoO from the outer loop (which just calculated cheb8(x) for independent x a few thousand times), so the code actually ran significantly faster than just adding up the latencies on the critical path would suggest. For a long time, unrolling has been far less effective on x86 than on other platforms (for various reasons), but it was only when I looked at that example trying to figure out what was going on that I realized just how much OoO with a long issue window really buys you.

That said, interleaving 2 independent calculations was still a good deal faster than the “one at a time” version, but it’s not as much as you’d expect. And, fun fact: In the C++ loop version, changing

`for (i=0; i < 8; i++)`

to`for (i=0; i != 8; i++)`

actually saved .5 cycles per loop iteration (on Core2, cmp+jnz can fuse but cmp+jl can’t – fixed on i7 I believe). Which I thought was cute, though it’s not something I’d worry about usually :)AGU/RF ports: On the pre-SNB cores, you have the 3 register read port limit per cycle which only counts real register file reads (ROB are cheaper). Complicated to keep track of in general, but in this case everything except for RSI/RDI is updated often enough that it’ll come from the ROB. On P4, the complex addressing modes with non-1 scale took extra cycles, but I believe the non-scaled ones were still fast.

I think Tom just tried to say that replacing ECX with EBX would save a few bytes of code, which might help.

Another trick is to move the increment to the start of loop – presuming that shorter instructions would

be still faster to fetch somehow