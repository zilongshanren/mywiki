---
title: Little-endian vs. big-endian
url: https://fgiesen.wordpress.com/2014/10/25/little-endian-vs-big-endian/
published: '2014-10-25'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Little-endian vs. big-endian

Additional cache coherency/lock-free posts are still in the pipe, I just haven’t gotten around to writing much lately.

In the meantime, here’s a quick post on something else: little-endian (LE) vs. big-endian (BE) and some of the trade-offs involved. The whole debate comes up periodically by proponents of LE or BE with missionary zeal, and then I get annoyed, because usually what makes either endianness superior for some applications makes it inferior for others. So for what it’s worth, here’s the trade-offs I’m aware of:

### Doing math vs. indexing/sorting/searching

-
LE stores bytes in the order you do most math operations on them (if you were to do it byte by byte and not in larger chunks, that is). Additions and subtractions proceed from least-significant bit (LSB) to most-significant bit (MSB), always, because that’s the order carries (and borrows) are generated. Multiplications form partial products from smaller terms (at the limit, individual bits, though for hardware you’re more likely to use radix-4 booth recoding or similar) and add them, and the final addition likewise is LSB to MSB. Long division is the exception and works its way downwards from the most significant bits, but divisions are generally much less frequent than additions, subtractions and multiplication.

[Arbitrary-precision arithmetic](http://en.wikipedia.org/wiki/Arbitrary-precision_arithmetic)(“bignum arithmetic”) thus typically chops up numbers into segments (“legs”) matching the[word size](http://en.wikipedia.org/wiki/Word_%28computer_architecture%29)of the underlying machine, and stores these words in memory ordered from least significant to most significant – on both LE and BE architectures.All 8-bit ISAs I’m personally familiar with (Intel 8080, Zilog Z80, MOS 6502) use LE, presumably for that reason; it’s the more natural byte order for 16-bit numbers if you only have an 8-bit ALU. (That said, Motorola’s 8-bit 6800 apparently used BE). And consequently, if you’re designing a new architecture with the explicit goal of being

[source-code compatible with the 8080](http://en.wikipedia.org/wiki/Intel_8086#The_first_x86_design)(yes, x86 was already constrained by backwards-compatibility considerations even for the original 8086!) it’s going to be little-endian. - BE stores bytes in the order you compare them (assuming a lexicographic compare).
So if you want to do a lexicographic sort,

`memcmp`

does the right thing on BE but not on LE: encoding numbers in BE is an[order-preserving bijection](https://fgiesen.wordpress.com/2013/01/21/order-preserving-bijections/)(if the ordering predicate is lexicographic comparison). This is a very useful property if you’re in the business of selling your customers machines that spend a large chunk of their time sorting, searching and retrieving records, and likely one of the reasons why IBM’s architectures dating back as far as the mainframe era are big-endian. (It doesn’t make sense to speak of “endianness” before the IBM 7030, since that was the machine that introduced byte-addressable memory in the first place; machines before that point had word-based memory). It’s still common to encode numbers in BE for databases and key-value stores, even on LE architectures.

### Byte order vs. bit order

-
All LE architectures I’m aware of have the LSB as bit 0 and number both bits and bytes in order of increasing significance. Thus, bit and byte order agree: byte 0 of a number on a LE machine stores bits 0-7, byte 1 stores bits 8-15 and so forth. (Assuming 8-bit bytes, that is.)

-
BE has two schools. First, there’s “Motorola style”, which is bits numbered with LSB=0 and from then on in increasing order of significance; but at the same time, byte 0 is the most significant byte, and following bytes decrease in significance. So by these conventions, a 16-bit number would store bits 8-15 in byte 0, and bits 0-7 in byte 1. As you can see, there’s a mismatch between byte order and bit order.

-
Finally, there’s BE “IBM style”, which instead labels the

*MSB*as bit 0. As the bit number increases, they decrease in significance. In this scheme, same as in LE, byte 0 stores bits 0-7 of a number, byte 1 stores bits 8-15, and so forth; these bytes are exactly reversed compared to the LE variant, but bit and byte ordering are in agreement again.That said, referring to the MSB as bit 0 is confusing in other ways; people normally expect bit 0 to have mask

`1 << 0`

, and with MSB-first bit numbering that’s not the case.

### Memory access

-
For LE, the 8/16/32-bit prefixes of a 64-bit number all start at the same address as the number itself. This can be viewed as either an advantage (“it’s convenient!”) or a disadvantage (“it hides bugs!”).

A LE load of 8/16/32/64 bits will always put all source bits at the same position in the destination register; as you make the load wider, it will just zero-clear (or sign-extend) less of them. Flow of data through the load/store circuitry is thus essentially the same regardless of operand size; different AND masks corresponding to the load size, but that’s it.

-
For BE, prefixes start at different offsets. Again, can be viewed as either an advantage (“it prevents bugs!”) or a disadvantage (“I can’t transparently widen fields after the fact!”).

A BE load of 8/16/32/64 bits puts the source bits in different locations in the destination register; instead of a width-dependent mask, we get a width-dependent shift. In a circuit, this is a Mux of differently-shifted versions of the source operand, which is (very slightly) more complicated than the masking for LE. (Not that I actually think anyone cares about HW complexity at that level today, or has in over a decade for that matter.)


That said, the difference can be slightly interesting if you don’t have a full complement of differently-sized loads; the Cell SPUs are an example. If you don’t have narrow loads, BE is hit a bit more than LE is. A synthesized LE narrow load is `wide_unaligned_load(addr) & mask`

(where the wide unaligned load might itself consist of multiple steps, like it does on the SPUs); synthesized BE narrow load is `wide_unaligned_load(addr + offs) & mask`

. Note the extra add of a non-zero offset, which means one more instruction. You can get rid of it in principle by just having all addresses for e.g. byte-aligned data be pre-incremented by `offs`

, but that’s obnoxious too.

And that’s it for now, off the top of my head.

I think the most damning thing about little-endian is it confuses memory view windows. If you view the same block of memory as bytes, 16-bit shorts, 32-bit ints, 64-bit long long, etc., with little-endian then the views change as the granularity changes. With big-endian the grouping of bytes changes as you change the granularity but their order does not change. If you are viewing the raw memory for a struct which has different sized fields then the little-endian view adds significant cognitive load.

Big-endian also has the advantage that if you simultaneously view byte-by-byte memory and the same data loaded into a register or variable you see the same thing.

These are human factors advantages, rather than compute-efficiency factors. I would argue that if you were designing a new compute architecture now then these factors should trump the minor efficiency differences you list, and therefore BE would be the appropriate choice.

But, nobody designs a totally new compute architecture, so we are often constrained by what made sense on the 8-bit buses of thirty years ago.

All these differences are trivial, most certainly including what shows up in a debugger memory view.

The cost of having different endianness between machines is not. At this point, the dominant CPU and GPU architectures all default to LE, with even POWER recently getting serious about making LE just work and using the opportunity to clean up some ABI issues in the process. I don’t particularly care which endianness I’m on, but given that we seem to be converging on “LE everywhere”, the last thing I want is a new architecture that goes BE and prolongs the confusion by another few decades.

That is not an inherent feature of big-endiannness, though. It’s a combination of machine endianness, the fact that we dump memory with lower addresses on the left and higher on the right, and that the way we write and read numbers is big-endian. All of these are arbitrary conventions.

Hex editors and debuggers could display values right to left and that’s it. True, we usually write words the other way (oh wait, strings would appear reversed). And yes, we write down numbers big endian, probably because in “three hundreds” the hundred is just the new unit, and in “three hundreds and one” “three hundreds” is more important than “one”, both in spoken and written language.

For me the “natural” reason for little endian is : weight of digit is equal or ordered according to memory position : number = sum (digit * digit_max ^ position).

With big endian, number = sum (digit * digit_max ^ (number_of_digits – position ) ).

The article states this for bit endianness but not for byte.

In one word : small weights on small addresses.

Another thing not touched here is when network transmission comes in, everything is serialized according to some convention and some things can be done earlier if you have the first or last digit first, and some schemes store incoming data in memory in a continuous way and some others do not.

Oh well.

Although now rather historical and specialised – in a monitoring system, the least-significant part of a value is also the most volatile. Transmitting least-significant-first then provided some redundancy if the connection was lost, as the missing most-significant part could be infered from a prior value.

If I recall correctly, this was the approach taken with early Earth orbit satellite.

Having established the near-equality of BE/LE utility (and I agree that the utility difference between BE/LE is smaller than the utility difference between having both architectures co-exist vs just choosing one and staying with it) – now we can move on to the real challenge: should memory map diagrams be drawn with addresses increasing up the page (like most graphs) or down the page (like memory dumps and struct members)? :-)

At least we’ve predominantly agreed by now on 8 bit bytes, on computer words that are powers of 2, on two’s complement arithmetic, standard floating point formats and we’re closer to having convergence on character sets. I still remember 60 bit words with 10 6 bit characters, having to translate between vender-specific character sets even for digits and English letters, and one’s vs two’s complement. (I even briefly dealt with a DEC PDP-12 computer which had two CPUs sharing the same [12 bit wide IIRC] memory – a one’s complement LINK-8 and a two’s complement PDP-8 if I recall; shared data structures were extra fun).

Oh, and there were architectures with mixed endian-ness – like bytes in LE order but words in BE order (or was it vice versa?). Like ordering 2301 (or 1032?)!

It took a century or two to fully agree on which way dial clocks should rotate.

Anyway, thanks for the articles.