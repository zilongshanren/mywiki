---
title: Bit scanning equivalencies
url: https://fgiesen.wordpress.com/2013/10/18/bit-scanning-equivalencies/
published: '2013-10-18'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Bit scanning equivalencies

A lot of bit manipulation operations exist basically everywhere: AND, OR, XOR/EOR, shifts, and so forth. Some exist only on some architectures but have obvious implementations everywhere else – NAND, NOR, equivalence/XNOR and so forth.

Some exist as built-in instructions on some architectures and require fairly lengthy multi-instruction sequences when they’re not available. Some examples would be population count (number of bits set; available on recent x86s and POWER but not PowerPC), or bit reversal (available on ARMv6T2 and above).

And then there’s bit scanning operations. All of these can be done fairly efficiently on most architectures, but it’s not always obvious how.

### x86 bit scanning operations

On x86, there’s `BSF`

(bit scan forward), `BSR`

(bit scan reverse), `TZCNT`

(trailing zero count) and `LZCNT`

(leading zero count). The first two are “old” (having existed since 386), the latter are very new. `BSF`

and `TZCNT`

do basically the same thing, with one difference: `BSF`

has “undefined” results on a zero input (what is the index of the first set bit in the integer 0?), whereas the “trailing zeros” definition for `TZCNT`

provides an obvious answer: the width of the register. `BSR`

returns the index of the “last” set bit (again undefined on 0 input), `LZCNT`

returns the number of leading zero bits, so these two actually produce different results.

`x86_bsf(x) = x86_tzcnt(x)`

unless x=0 (in which case`bsf`

is undefined).`x86_bsr(x) = (reg_width - 1) - x86_lzcnt(x)`

unless x=0 (in which case`bsr`

is undefined).

In the following, I’ll only use `LZCNT`

and `TZCNT`

(use above table to convert where necessary) simply to avoid that nasty edge case at 0.

### PowerPC bit scanning operations

PPC has `cntlzw`

(Count Leading Zeros Word) and `cntlzd`

(Count Leading Zeros Double Word) but no equivalent for trailing zero bits. We can get fairly close though: there’s the old trick `x & -x`

which clears all but the lowest set bit in `x`

. As long as x is nonzero, this value has exactly one bit set, and we can determine its position using a leading zero count.

`x86_tzcnt(x) = (reg_width - 1) - ppc_cntlz(x & -x)`

unless x=0 (in which case the PPC expression returns -1).`x86_lzcnt(x) = ppc_cntlz(x)`

.

### ARM bit scanning operations

ARM also has `CLZ`

(Count Leading Zeros) but nothing for trailing zero bits. But it also offers the aforementioned `RBIT`

which reverses the bits in a word, which makes a trailing zero count easy to accomplish:

`x86_tzcnt(x) = arm_clz(arm_rbit(x))`

.`x86_lzcnt(x) = arm_clz(x)`

.

### Bonus

Finally, ARMs NEON also offers `VCLS`

(Vector Count Leading Sign Bits), which (quoting from the documentation) “counts the number of consecutive bits following the topmost bit, that are the same as the topmost bit”. Well, we can do that on all architectures I mentioned as well, using only ingredients we already have: `arm_cls(x) = x86_lzcnt(x ^ (x >> 1)) - 1`

(the shift here is an arithmetic shift). The expression `y = x ^ (x >> 1)`

gives a value that has bit `n`

set if and only if bits `n`

and `n + 1`

of x are the same. By induction, the number of leading zeros in `y`

is thus exactly the number of leading bits in `x`

that match the sign bit. This count includes the topmost (sign) bit, so it’s always at least 1, and the instruction definition I just quoted requires us to return the number of bits *following* the topmost bit that match it. So we subtract 1 to get the right result. Since we can do a fast leading zero count on all quoted platforms, we’re good.

Conclusion: bit scans / zero bit counts in either direction can be done fairly efficiently on all architectures covered, but you need to be careful when zeros are involved.

An interesting thing is that gcc and clang builtins ctz and clz (http://gcc.gnu.org/onlinedocs/gcc-4.8.1/gcc/Other-Builtins.html) follow x86 rules i.e. output is undefined when input is zero.

Given that both provide these built-ins on several architectures, including pre-LZCNT/TZCNT x86 and architectures that only provide leading zero count, this seems like a reasonable choice; any other definition would require extra tests or at the very least some branches to handle zero on a lot of targets, which is a significant overhead compared to the actual computation itself (which is usually a single-cycle operation).

That said: yet more undefined/implementation-specific behavior in C/C++ compilers. Sigh.

Probably the best thing is to provide 2 versions, one that is undefined for 0 (ctznz() maybe) and one that is defined for 0 (ctz()), which the caveat that ctznz() may be faster on some machines.

There are many times you don’t care about the 0 behavior. For example in sse2 optimized strlen(), you do this idiom:

if(x) {

int y = ctznz(x);

}

http://www.strchr.com/sse2_optimised_strlen

I’m working on a proposal to standardize these bitwise operations in C++, providing a standard abstraction over these instructions.

This post was very helpful. Here is the std proposals thread about the proposal if you’re interested. Thanks!

https://groups.google.com/a/isocpp.org/forum/#!topic/std-proposals/8WB2Z9d7A0w

One thing to watch out for is how LZCNT is executed on HW prior to Haswell:

“The encoding of lzcnt is similar enough to bsr that if lzcnt is performed on a CPU not supporting it such as Intel CPU’s prior to Haswell, it will perform the bsr operation instead of raising an invalid instruction error.”

Source: http://en.wikipedia.org/wiki/SSE4

I’ve had a failing test in my code to find out that the same LZCNT instruction is implemented correctly on my new i5-4570 Haswell whereas it is implemented as a BSR on my i7-720QM Nehalem.

Don’t ever use LZCNT without checking you’re on a CPU that supports it, period.

“The expression y = x ^ (x >> 1) gives a value that has bit n set if and only if bits n and n + 1 of x are the same.”

Did you mean to say “…has bit n _unset_ iff bits n and n+1 of x are the same” ?

Yes.

You can do slightly better with the “count sign bits” algorithm: rather than shifting right and xoring, and then having to subtract one, do a shift left and xor, so no -1 is needed. One caveat is this would return 64 for an input of zero, whereas arm would return 63… so we need to OR a 1 to fix that.

That is: arm_cls(x) = x86_lzcnt((x + x) ^ (x | 1));

Despite the OR 1, it’s still a win on x86 (among others) because we can add x to x and put the result in a different register with one instruction, which cannot be done with a shift right. See https://godbolt.org/z/5WGrY1sfv (And of course, if we know `x` isn’t zero coming into this routine, the OR 1 isn’t needed.