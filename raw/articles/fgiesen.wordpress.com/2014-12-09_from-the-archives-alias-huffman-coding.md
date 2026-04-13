---
title: 'From the archives: “Alias Huffman coding.”'
url: https://fgiesen.wordpress.com/2014/12/09/from-the-archives-alias-huffman-coding/
published: '2014-12-09'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# From the archives: “Alias Huffman coding.”

This is precisely what the last post was about. So nothing new. This is just my original mail on the topic with some more details that might be interesting and/or amusing to a few people. :)

Date: Wed, 05 Feb 2014 16:43:36 -0800


From: Fabian Giesen

Subject: Alias Huffman coding.

Huffman <= ANS (strict subset)

(namely, power-of-2 frequencies)

We can take any discrete probability distribution of N events and use the Alias method to construct a O(N)-entry table that allows us to sample from that distribution in O(1) time.

We can apply that same technique to e.g. rANS coding to map from (x mod M) to “what symbol is x”. We already have that.

Ergo, we can construct a Huffman-esque coder that can decode symbols using a single table lookup, where the table size only depends on N_sym and not the code lengths. (And the time to build said table given the code lengths is linear in N_sym too).

Unlike regular/canonical Huffman codes, these can have multiple unconnected ranges for the same symbol, so you still need to deal with the range remapping (the “slot_adjust” thing) you have in Alias table ANS; basically, the only difference ends up being that you have a shift instead of a multiply by the frequency.

But there’s still some advantages in that a few things simplify; for example, there’s no need (or advantage) to using a L that’s larger than M. An obvious candidate is choosing L=M=B so that your Huffman codes are length-limited to half your word size and you never do IO in smaller chunks than that.

Okay. So where does that get us? Well, something like the MSB alias rANS decoder, with a shift instead of a multiply, really:

// decoder state // suppose max_code_len = 16 U32 x; U16 const * input_ptr; U32 const m = (1 << max_code_len) - 1; U32 const bucket_shift = max_code_len - log2_nbuckets; // decode: U32 xm = x & m; U32 xm_shifted = xm >> bucket_shift; U32 bucket = xm_shifted * 2; if (xm < hufftab_divider[xm_shifted]) bucket++; x = (x & ~m) >> hufftab_shift[bucket]; x += xm - hufftab_adjust[bucket]; if (x < (1<<16)) x = (x << 16) | *input_ptr++; return hufftab_symbol[bucket];

So with a hypothetical compiler that can figure out the adc-for-bucket

thing, we’d get something like

; x in eax, input_ptr in esi movzx edx, ax ; x & m (for bucket id) shr edx, 8 ; edx = xm_shifted movzx ebx, ax ; ebx = xm cmp ax, [hufftab_divider + edx*2] adc edx, edx ; edx = bucket xor eax, ebx ; eax = x & ~m mov cl, [hufftab_shift + edx] shr eax, cl movzx ecx, word [hufftab_adjust + edx*2] add eax, ebx ; x += xm movzx edx, byte [hufftab_symbol + edx] ; symbol sub eax, ecx ; x -= adjust[bucket] cmp eax, (1<<16) jae done shl eax, 16 movzx ecx, word [esi] add esi, 2 or eax, ecx done: ; new x in eax, new input_ptr in esi ; symbol in edx

which is actually pretty damn nice considering that’s both Huffman decode and bit buffer rolled into one. Especially so since it handles all cases – there’s no extra conditions and no cases (rare though they might be) where you have to grab more bits and look into another table. Bonus points because it has an obvious variant that’s completely branch-free:

; same as before up until... sub eax, ecx ; x -= adjust[bucket] movzx ecx, word [esi] mov ebx, eax shl ebx, 16 or ebx, ecx lea edi, [esi+2] cmp eax, (1<<16) cmovb eax, ebx cmovb esi, edi

Okay, all that’s nice and everything, but for x86 it’s nothing we haven’t seen before. I have a punch line though: the same thing works on PPC – the adc thing and “sbb reg, reg” both have equivalents, so you can do branch-free computation based on some carry flag easily.

BUT, couple subtle points:

- this thing has a bunch of
`(x & foo) >> bar`

(left-shift or right-shift) kind of things, which map*really really*well to PPC because there’s rlwinm / rlwimi. -
The in-order PPCs hate variable shifts (something like 12+ cycles microcoded). Well, guess what, everything we multiply with is a small per-symbol constant, so we can just store (1 << len) per symbol and use

`mullw`

. That’s 9 cycles non-pipelined (and causes a stall after issue), but still, better than the microcode. But… wait a second.If this ends up faster than your usual Huffman, and there’s a decent chance that it might (branch-free and all), the fastest “Huffman” decoder on in-order PPC would, in fact, be a full-blown arithmetic decoder. Which amuses me no end.


# NOTE: LSB of "bucket" complemented compared to x86 # r3 = x, r4 = input ptr # r20 = &tab_divider[0] # r21 = &tab_symbol[0] # r22 = &tab_mult[0] # r23 = &tab_adjust[0] rlwinm r5, r3, 24, 23, 30 # r5 = (xm >> bucket_shift) * 2 rlwinm r6, r3, 0, 16, 31 # r6 = xm lhzx r7, r20, r5 # r7 = tab_divider[xm_shifted] srwi r8, r3, 16 # r8 = x >> log2(m) subfc r9, r7, r6 # (r9 ignored but sets carry) lhz r10, 0(r4) # *input_ptr addze r5, r5 # r5 = bucket lbzx r9, r21, r5 # r9 = symbol add r5, r5, r5 # r5 = bucket word offs lhzx r7, r22, r5 # r7 = mult li r6, 0x10000 # r6 = op for sub later lhzx r5, r23, r5 # r5 = adjust mullw r7, r7, r8 # r7 = mult * (x >> m) subf r5, r5, r6 # r5 = xm - tab_adjust[bucket] add r5, r5, r7 # r5 = new x subfc r6, r6, r5 # sets carry iff (x >= (1<<16)) rlwimi r10, r5, 16, 0, 16 # r10 = (x << 16) | *input_ptr subfe r6, r6, r6 # ~0 if (x < (1<<16)), 0 otherwise slwi r7, r6, 1 # -2 if (x < (1<<16)), 0 otherwise and r10, r10, r6 andc r5, r5, r6 subf r4, r7, r4 # input_ptr++ if (x < (1<<16)) or r5, r5, r10 # new x

That should be a complete alias rANS decoder assuming M=L=b=216.

-Fabian