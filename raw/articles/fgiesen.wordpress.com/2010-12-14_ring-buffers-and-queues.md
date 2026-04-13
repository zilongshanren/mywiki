---
title: Ring buffers and queues
url: https://fgiesen.wordpress.com/2010/12/14/ring-buffers-and-queues/
published: '2010-12-14'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Ring buffers and queues

The data structure is extremely simple: a bounded FIFO. One step up from plain arrays, but still, it’s very basic stuff. And if you’re doing system programming, particularly anything involving IO or directly talking to hardware (boils down to the same thing really), it’s absolutely everywhere. It’s also very useful to communicate between different threads. I have some notes on the topic than aren’t immediately obvious, so it’s time to write them up. I’m only going to talk about the single producer, single consumer (SPSC) case since that’s what you usually have when you’re dealing with hardware.

The producer produces commands/objects/whatever in some way and appends them to the queue. The consumer pops an item from the start and does its work. If the queue is full, the producer has to wait; if it’s empty, the consumer has to wait. As programmer feeding hardware (or being fed from hardware), you’re generally trying to reach a steady state that does neither. The actual data structure always looks something like this:

struct FIFO { ElemType Elem[SIZE]; uint ReadPos; uint WritePos; };

In hardware, the elements are stored in some block of memory somewhere, and `ReadPos`

/`WritePos`

usually come in the form of memory-mapped registers. In software, you normally use a slightly different layout (put one pointer before the array and the other after it and make sure it’s all in different cache lines to avoid false sharing). You can find details on this elsewhere; I’m gonna be focusing on a different, more conceptual issue.

What `Elem`

means is not really up to interpretation; it’s an array, just a block of memory where you drop your data/commands/whatever at the right position. `ReadPos`

/`WritePos`

have a bit more room for interpretation; there are two common models with slightly different tradeoffs.

### Model 1: Just array indices (or pointers)

This is what you normally have when talking to hardware. In this model, the two positions are just array indices. When adding an element, you first write the new element to memory via `Elem[WritePos] = x;`

and then compute the next write position as `WritePos = (WritePos + 1) % SIZE;`

; reading is analogous. If `ReadPos == WritePos`

, the queue is empty. Otherwise, the queue currently has `WritePos - ReadPos`

elements in it if `WritePos > ReadPos`

, and `WritePos + SIZE - ReadPos`

elements if `WritePos < ReadPos`

.

There’s an ambiguous case though: if we fill up the queue completely, we end up with `ReadPos == WritePos`

, which is then interpreted as an empty queue. (Storing `WritePos - 1`

doesn’t solve this; now the “queue empty” case becomes tricky). There’s a simple solution though: *Don’t do that*. Seriously. When adding elements to the queue, block when it contains `SIZE - 1`

elements. What you definitely shouldn’t do is get fancy and use special encodings for an empty (or full) queue and riddle the code with ifs. I’ve seen this a couple times, and it’s *bad*. It makes “lock-free” implementations hard, and when dealing with hardware, *you usually have no locks*. If you use this method, just live with the very slight memory waste.

### Model 2: Virtual stream

The intuition here is that you’re not giving the actual position in the ring buffer, but the “distance travelled” from the start. So if you’ve wrapped around the ring buffer twice, your current `WritePos`

would be `2*SIZE`

, not `0`

.

This is just a slight change, but with important consequences: writing elements is `Elem[WritePos % SIZE] = x;`

and updating the index is `WritePos++;`

(and analogous for `ReadPos`

). In other words, you delay the reduction modulo `SIZE`

. For this to be efficient, you normally want to pick a power of 2 for `SIZE`

; this makes the wrapping computation cheap and will automatically do the right thing if one of the positions ever overflows. This leads to very straightforward, efficient code. The number of items in the queue is `WritePos - ReadPos`

; no case distinction, unsigned arithmetic does the right thing. No trouble with the last element either (if the queue is full, then WritePos == ReadPos + SIZE – no problem!).

With non-pow2 SIZE, you still need to do some amount of modulo reduction on increment – always modulo `N*SIZE`

, where `N`

is some constant >1 (if you use 1, you end up with Method 1). This is more work than for method 1, so it seems like a waste. But it’s not quite that simple.

### Virtual streams are a useful model!

One advantage of virtual streams is it’s usually easier to state (and check) invariants using this model; for example, if you’re streaming data from a file (and I mean streaming in the original sense of the word, i.e. reading some amount of data sequentially and piece by piece without skipping around), it’s very convenient to use file offsets for the two pointers. This leads to very readable, straightforward logic: the two invariants for your streaming buffer are `WritePos >= ReadPos`

and `WritePos - ReadPos <= SIZE`

, and one of them (`WritePos`

– you’d pick a different name in this case) is just the current file pointer which you need to dispatch the next async read. No redundant variables, no risk of them getting out of sync. As a bonus, if you align your destination buffer address to whatever alignment requirement async reads have, it also means you can DMA data directly from the drive to your streaming buffer without any copying (the lowest bits of the file pointer and the target address need to match for this to work, and you get that almost for free out of this scheme).

This scheme is particularly useful for sound playback, where the “consumer” (the audio HW) keeps reading data whether you’re ready or not. Of course you try to produce data fast enough, but sometimes you may be too late and the audio HW forges ahead. In that case, you want to know *how far* ahead it got (at least if you’re trying to keep audio and video in sync). With a “virtual stream” type API, you have a counter for the total number of samples (or blocks, or whatever) played and can immediately answer this question. Annoyingly, almost all sound APIs only give you the current read position mod the ring buffer size, so you don’t have this information. This usually leads to a little song and dance routine in low-level sound code where you query a timer every time you ask for the current read position. Next time, you look at the time difference; if it’s longer than the total length of the ring buffer in ms minus some fudge factor, you use the secondary timer to estimate how many ms you skipped, otherwise you can use the read pointer to determine how big the skip was.

It’s not a big deal, but it *is* annoying, especially since it’s purely an API issue – the sound driver actually knows how many samples were played, even though the HW usually uses method 1, since the driver gets an interrupt whenever the audio HW is done playing a block. This is enough to disambiguate the ring buffer position. But for some reason most audio APIs don’t give you this information, so you have to guess – argh!

This is a general pattern: If you have some type of separate feedback channel, the regular ring buffer semantics are fine. But when the FIFO is really the only means of communication, the virtual stream model is more expressive and hence preferable. Particularly with pow2 sizes, where everything just works out automagically without any extra work. Finally, a nice bonus on PowerPC-based platforms is that address generation for the array access can be done with a single `rlwinm`

instruction if `SIZE`

and `sizeof(ElemType)`

are both powers of 2. This is even less work than the regular mod-after-increment variant!

Note that with Model 1 you can get away with no case distinction in calculating the number of items by just doing (WritePos – ReadPos) & (SIZE – 1) in unsigned arithmetic when SIZE is a power of two.

The real strength of Model 2 is definitely in the simpler invariants and lack of special cases. From now I’ll do all my circular FIFOs this way.

You can retain some advantages of both approaches for a circular FIFO by adding the invariant ReadPos <= WritePos < 2 * SIZE. Then you can do the modulo reduction incrementally for a non-power-of-two SIZE and easily deal with empty queues: Enforce the invariant with if (WritePos >= 2 * SIZE) { ReadPos -= SIZE; WritePos -= SIZE; } and use Elem[WritePos >= SIZE ? WritePos – SIZE : WritePos] instead of Elem[WritePos % SIZE]. Otherwise the code should be the same as for Model 2.

It looks like WordPress didn’t like my angle brackets. Here’s a paste of my original ungarbled message: https://gist.github.com/741769

There, fixed the post :)

I only have one concern with method 2. ReadPos and WritePos have a finite bit-width, and can wrap just like ReadPos/WritePos in method 1.

I’d recommend pointing this out somewhere in your post. (after all, in a streaming world, 4GB of data, if you happened to use uint32 and sizeof(ElemType)=1, is not out of the ordinary).

No offense, but I

dopoint that out in the article and explain how do deal with it for both power-of-2 and non-power-of-2 buffer sizes :). Pers comment gives another possible implementation.Your first description of model 2 is correct, but only by implication — as you say you can compute the queue size as WritePos – ReadPos, and the thing that isn’t spelled out is that as long as you make all your queue decisions based on that computation of queue size, everything will work just fine if one thing wraps.

On the other hand, the following section of the article says “This leads to very readable, straightforward logic: the two invariants for your streaming buffer are WritePos >= ReadPos and WritePos – ReadPos <= SIZE”. These invariants are not valid when one parameter has wrapped, and might be what Barbie was referring to.

Note I’m only talking about power-of-2 SIZE in that paragraph, and I declare all variable as unsigned. If and only if all these conditions are true, the invariant

`WritePos - ReadPos <= SIZE`

is always valid (even in the presence of wraparound).`WritePos >= ReadPos`

is a bit more subtle. Without wraparound, you can use it as-is. With wraparound, you need to write it as`(signed_type) (WritePos - ReadPos) >= 0`

(where you use the appropriately-sized signed type) – provided the size of your queue is less than half the range of your position variables (not an issue in practice). I should probably add that to the post.What I generally do is define a simple predicate

and then write all comparisons between queue indices in terms of

`wraparound_less`

.Hi, good artical! It happened that I need to implement an circular buffer, but I have the same question as Barbie and Sean Barrett, and after reading the discussion between you guys, I still don’t understand how to deal with this case that WritePos or ReadPos overflow for very larg data(>2^64). I just saw that you add invariants for it, but not any solution.

I wonder is there any way that re-initialize WritePos and ReadPos or do it in a way that they keep pointing to the right position in Elem[] when wraps?

I didn’t “add invariants”. I stated that the code, as given, works even in the presence of overflow, and explained why – namely, because the stated invariants hold.

“With non-pow2 SIZE, you still need to do some amount of modulo reduction on increment – always modulo N*SIZE, where N is some constant >1 (if you use 1, you end up with Method 1). This is more work than for method 1, so it seems like a waste. But it’s not quite that simple.”

Could you elaborate on this paragraph? It makes no sense to me.

Q1: What is “modulo reduction”? Is that code I need to write, or are you talking about number of CPU instructions necessary to implement modules of a larger number? Or something else? Please define “modulo reduction”… I tried to google it but with no success.

Q2: Why would you ever want to modulo something other than “SIZE”, e.g. N=1 in your “N*SIZE”? When would it make sense to modulo, say, 3*SIZE?

Q3: Re: “if you use 1, you end up with Method 1” What does this mean? Could I not use the “Virtual stream” method (storing absolute number of bytes read and written) but still do a modulus of just SIZE in my code?

Q4: Re: “This is more work than for method 1, so it seems like a waste.” What, exactly, is “more work”? Could you provide some sample code? What are you even doing that is work? Are you referring to taking the modulus?

Q5: Re: “But it’s not quite that simple.” What is not quite as simple as what? What are you even talking about here?

Q6: Could you explain why pow2 is an advantage? Is it just fewer CPU instructions, or does the C code actually look different (and if so, how)?

I enjoyed the article, and understood it, until that paragraph.

Thank You,

Derek

4 years late, so you hopefully found the answer by now, but modulo arithmetic is all about the remainder of division, and is generally denoted with a % symbol. So to compute 32 % 10 you would divide 32 by 10 first to get 3 remainder 2. We don’t care about the 3, so we just keep the 2. So 32 % 10 = 2.

Everything else is built on that.