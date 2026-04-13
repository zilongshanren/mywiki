---
title: Papers I like (part 1)
url: https://fgiesen.wordpress.com/2017/08/12/papers-i-like-part-1/
published: '2017-08-12'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Papers I like (part 1)

This started out on [Twitter](https://twitter.com/rygorous/status/895422691963936768) and I expected having to write up maybe 50 or so, but then it made the rounds. I don’t think I have 1200+ papers that I’d recommend reading, and even if I did, I don’t think a reading list of that length is actually useful to anyone.

The original list had tweet-length comments. I have no such space limitation on this blog, so I’ll go ahead and write a few paragraphs on each paper. That does mean that we’re now back to lots of text, which means I’ll split it into parts. Such is life. In this post, I’ll do the first ten papers from my list.

One thing I noticed while writing the list is that the kind of paper I like most is those that combine solid theory with applications to concrete problems. You won’t find a lot of pure theory or pure engineering papers here. This is also emphatically not a list of “papers everyone should read” or any such nonsense. These are papers I happen to like, and if you share some of my interests, I think you’ll find a lot to like in them too. Beyond that, no guarantees.

### 1. Lamport-[“State the Problem Before Describing the Solution”](https://www.microsoft.com/en-us/research/publication/state-problem-describing-solution/#) (1978; general)

It’s a one-page memo, and yeah, the gist of it’s already in the title. Read it anyway. This applies to papers and code both.

This is not just a matter of style. If you don’t have a description of the problem independent of your proposed solution, usually the best you can say about your solution (in terms of proofs or invariants) is “it does what I think it does”. In code, the equivalent is a long, complicated process that everybody is afraid of touching and nobody is really sure what it does – just that things tend to break when you touch it.

### 2. Herlihy-[“Wait-free synchronization”](http://www.diku.dk/OLD/undervisning/2005f/dat-os/skrifter/lockfree.pdf) (1991; concurrency)

This is probably the most important single paper ever written about shared-memory multiprocessing. When it was written, such systems were nowhere near as common as they are now and each architecture had its own set of atomic synchronization primitives – chosen primarily by whatever the kernel programmers at the respective companies thought might come in handy. Pretty much everyone had a decent way to implement a basic spinlock, but beyond that, it was the wild west.

Herlihy had, in joint work with Wing, formally defined [linearizability](https://en.wikipedia.org/wiki/Linearizability) a few years earlier, in 1987 – and if it feels odd to you that we first got an “industrial-strength” definition of, effectively, atomicity a few decades after the first multi-processor supercomputers appeared, that should tell you everything you need to know about how far theory was lagging behind practice at the time.

That’s the setting for this paper. Mutual exclusion primitives exist and are well-known, but they’re *blocking*: if a thread (note: this description is anachronistic; threads weren’t yet a mainstream concept) holding a lock is delayed, say by waiting for IO, then until that thread is done, nobody else who wants to hold that lock will make any progress.

Herlihy starts by defining wait-freedom: “A wait-free implementation of a concurrent data object is one that guarantees that any process can complete any operation in a finite number of steps, regardless of the execution speeds of other processors”. (This is stronger than nonblocking aka “lock-free”, which guarantees that *some* thread will always be making progress, but can have any particular thread stuck in a retry loop for arbitrarily long).

Given that definition, he asks the question “with some atomic operations as primitives, what kinds of concurrent objects (think data structures) can we build out of them?”, and answers it definitively via consensus numbers (short version: virtually all primitives in use at the time can only solve 2-processor consensus wait-free, but compare-and-swap has a consensus number of infinity, i.e. it can be used to achieve consensus between an arbitrary number of processors wait-free).

The paper then goes on to show that, if the consensus number of available primitives is at least as high as the number of processor in a system, then in fact *any* operation can be done wait-free (*universality*). Note that this type of universal construction has high overhead and is therefore not particularly efficient, but it’s always possible.

This is a great paper and if you’re interested in concurrency, you should read it.

### 3. Cook – [“How complex systems fail”](https://www.researchgate.net/profile/Richard_Cook3/publication/228797158_How_complex_systems_fail/links/0c96053410db96a89c000000.pdf) (1998; complex systems)

This is about all kinds of complex systems, not just computer-related ones. Cook is a MD researching incidents in emergency medicine; this four-page write-up (the fifth page is bibliography) summarizes some of the most salient findings. It’s short, non-technical and relevant to everyone interacting with complex systems in their daily lives (which is, in modern society, everyone).

### 4. Moffat, Turpin – [“On the Implementation of Minimum Redundancy Prefix Codes”](https://pdfs.semanticscholar.org/bda3/442cc6b1d10e4b36b574af0a34a668492230.pdf) (1997; data compression)

My tweet-length summary was “Much has been written about Huffman coding, a lot of it wrong. Almost everything worth knowing is in this (short!) paper”. I have no space limit here, so let me explain what I mean by that: the “folk understanding” of Huffman coding is that you start by building a data structure, the Huffman tree, using Huffman’s algorithm, then you transfer a description of the tree “somehow” (imagine vigorous hand-waving here), and then the encoder produces the bit stream by encoding paths from the root to the leaves (corresponding to individual symbols) in the Huffman tree, and the decoder works by reading a bit at a time and walking down the appropriate branch of the tree, producing the right symbol and going back to the root when it hits a leaf node.

Sounds about right to you? It shouldn’t, because every single part of what I just said is either a bad idea or outright wrong in practice. Let’s start with the trees. You don’t actually want a binary tree data structure for your code – because neither encoder nor decoder should ever be working a bit at a time. In fact, the preferred approach is generally to use [canonical Huffman coding](https://en.wikipedia.org/wiki/Canonical_Huffman_code) which not only never builds a tree, but also doesn’t care about the codes assigned during the original Huffman tree-building process. All it cares about is the code *lengths*, which it uses to build an equivalent (in terms of compression ratio) encoding that is easier to decode (and also easier to transmit efficiently in the bit stream, because it has fewer redundant degrees of freedom).

You might also not want to use Huffman’s algorithm directly; actual Huffman code words for rare symbols can become really long. In practice, you want to limit them to something reasonable (I don’t know any format offhand that allows codes longer than about 20 bits; 16 bits is a typical limit) to simplify bit IO in the encoder and decoder. So to avoid over-long codes, there’s eiher some post-processing that essentially “rotates” parts of the tree (making some longer codes shorter and some shorter codes longer), or code lengths are constructed using a [different algorithm](https://en.wikipedia.org/wiki/Package-merge_algorithm) altogether.

This paper gets all these things right, and that’s why it’s the one I would recommend to anyone who wants to learn how to do Huffman coding right. As a final note, let me quote a passage from the conclusion of the paper:

In particular, we observe that explicitly tree-based decoding is an anachronism and usually best avoided, despite the attention such methods have received in textbooks, in the research literature, and in postings to the various network news groups.


It’s been 20 years; this is just as true now as it was then.

### 5. Dybvig, Hieb, Butler – [“Destination-Driven Code Generation”](https://pdfs.semanticscholar.org/dcb8/8719880e1f76ad71fb1c5aebb118e2ecfe71.pdf) (1990; compilers)

I also linked to Millikin’s [“One-pass Code Generation in V8”](http://cs.au.dk/~mis/dOvs/slides/46b-codegeneration-in-V8.pdf) as a companion piece.

Code generation for a simple stack-based virtual machine is really easy; it’s little more than a post-order traversal of the abstract syntax tree and some label management. If execution speed isn’t much of a concern, at that point you write a bytecode interpreter for said VM and call it a day.

But what if you do care about speed? Well, the next step is to generate actual machine code that still maintains the explicit stack (to get rid of the interpreter loop). Once you do that, it tends to become clear how much redundant stack manipulation and data movement you’re doing, so if you’re still not satisfied with the speed, what are you to do?

The most common answers are either to add some local smarts to the code generator, which gets messy alarmingly quickly (see the Milliken presentation for examples), or to give up and go for a “real” optimizing compiler back end, which is orders of magnitude more code and complexity (and has, not surprisingly, much higher compile times).

DDCG is a great compromise. It’s good at avoiding most of the redundant data movement and unnecessary control flow, while still fitting nicely within a simple one-pass code generator. That makes it a popular technique for JITs that need to generate passable machine code on tight deadlines.

### 6. Valmari – [“Fast brief practical DFA minimization”](http://www.cs.cmu.edu/~./cdm/pdf/Valmari12.pdf) (2012; theoretical CS/automata theory)

Take a -state

[DFA](https://en.wikipedia.org/wiki/Deterministic_finite_automaton) with transitions and an input alphabet of size

as input, and produce the corresponding minimal (by number of states) DFA – i.e. an equivalent DFA that is smaller (or at worst the same size as the input).


This is a classic automata theory problem; it’s relatively straightforward to design an algorithm that works in time (usually credited to Moore), and there’s a 1971 algorithm by Hopcroft that solves the problem in

time. So why am I linking to a 2012 paper?


Hopcroft’s algorithm is *complicated*. Textbooks tend to omit it entirely because its correctness proof and run-time analysis are considered too hard. Hopcroft’s 1971 paper was followed by a 1973 paper by Gries, “Describing an algorithm by Hopcroft”, that aims to improve the exposition. Nearly 30 years later, Knuutila wrote another follow-up paper, “Re-describing an algorithm by Hopcroft”, that still bemoans the lack of a readable exposition and gives it another go, spending 31 pages on it, and showing along the way that Hopcroft and Gries do not actually describe quite the same algorithm – and that his new algorithm is slightly different still (intentionally this time, to make it somewhat easier to analyze).

This is not what successful replication looks like, and a profoundly unsatisfying state of affairs for such a relatively fundamental (and clean) problem.

And *that’s* why I’m linking to Valmari’s 2012 paper. This paper, unlike most of the previous ones, works correctly with partial DFAs (i.e. those that don’t have transitions defined for every (state,input) pair), includes working code in the body of the paper (about 130 lines of C++, formatted for 42-char lines to fit in the two-column limit, resulting in one-letter variable names for everything; correspondingly it’s quite dense, but readable enough once you get used to the names), and takes a total of 5 pages for the algorithm description, correctness proof, and run-time analysis – the latter is ; since

, this is as good as Hopcroft’s algorithm.


The algorithm itself is rather pretty too, working by alternatingly refining a partition on the states and the transitions of the input DFA in a pleasantly symmetric way. The data structures are simple but clever.

It’s taken an extra 41 years, but I think we can actually consider this problem truly solved now.

### 7. Sarnak, Tarjan – [“Planar Point Location Using Persistent Search Trees”](http://users.cs.fiu.edu/~giri/teach/6405/s04/SarnakTarjanCACM86.pdf) (1986; computational geometry/data structures)

Planar point location (locating which polygon of a polygonal subdivision of the plane a query point falls in) is an interesting problem in its own right, but in retrospect, it’s just side dish. What this paper really does is introduce space-efficient [persistent search trees](https://en.wikipedia.org/wiki/Persistent_data_structure), using the “fat node” method. It’s a simple and very versatile idea (section 3 of the paper).

With persistent search trees, building the point location structure itself is a straightforward [sweep](https://en.wikipedia.org/wiki/Sweep_line_algorithm): do a plane sweep from left to right, keeping track of line segments of the polygonal subdivision currently intersecting the sweep line. Their relative ordering only changes at vertices. The algorithm simply keeps track of the currently active line segments in a persistent red-black tree. Once the sweep is done, the persistent tree encodes all “slabs” between line segments (and thus the polygons between them) for arbitrary x coordinates, and can be queried in logarithmic time. It’s a textbook example of good data structures making for good algorithms.

### 8. Porter, Duff – [“Compositing Digital Images”](https://keithp.com/~keithp/porterduff/p253-porter.pdf) (1984; computer graphics)

The paper that introduced, well, digital image compositing, premultiplied (also known as “associated”) alpha, and what is now known as the “Porter-Duff operators” (“over” being the most important one by far). All these concepts are fairly important in image processing; sadly the paper under-sells them a bit.

In particular, premultiplied alpha is introduced as little more than a hack that saves a fair amount of arithmetic per pixel. While true, this is one of those cases where applications were ahead of the theory.

It turns out that a much stronger argument for premultiplication isn’t that it saves a bit of arithmetic, but that it solves some important other problems: when image data is stored in pre-multiplied form, (linear) filtering and compositing operations commute – that is, filtering and compositing can be exchanged. This is not the case with non-premultiplied alpha. In particular, scaling non-premultiplied images up or down before compositing tends to introduce fringing at the edges, as color values of transparent pixels (which should not matter) bleed in. Many try to mitigate this by preprocessing say sprite data so that the color values for transparent pixels adjacent to opaque or partially translucent pixels are “close” to minimize the error, but premultiplied alpha is cheaper, simpler to implement and completely free of errors. It’s generally the representation of choice for any linear filtering/interpolation tasks. And it also turns out that compositing operations themselves (if you care about the alpha value of the result) are a lot simpler in premultiplied alpha, whereas non-premultiplied ends up with various complications and special cases.

A good read on these issues are Jim Blinn’s columns in *IEEE Computer Graphics and Applications*, specifically those on Image Compositing, which are unfortunately pay-walled so I can’t link to them . They are collected in his book “Dirty Pixels” though, which is a recommended read if you’re interested in the topic.

### 9. Brandt – [“Hard Sync Without Aliasing”](http://elthariel.free.fr/ebooks/icmc01-hardsync.pdf) (2001; DSP)

Probably the most popular class of synthesizers employs what is called “subtractive synthesis”. The idea is fairly simple: start out with an oscillator generating an “interesting” waveform (one with lots of overtones) at a specified frequency, and then proceed to shape the result using filters, which emphasize some of the overtones and de-emphasize others. It’s called subtractive synthesis because we start out with lots of overtones and then remove some of them; the converse (additive synthesis) builds up the overtone series manually by summing individual sine waves.

Typical good waveforms to use are sawtooth or pulse waves. Generating these seems really simple in code, but there’s a catch: in DSP, we generally represent waveforms by storing their values at regularly spaced discrete sample times; the original continuous signal can be recovered from these samples if and only if it is bandlimited. (This is the famous [sampling theorem](https://en.wikipedia.org/wiki/Nyquist%E2%80%93Shannon_sampling_theorem)).

Neither sawtooth waves nor pulse waves are bandlimited. To get a bandlimited (and thus representable) version of them, you have to cut off the overtone series at some point; for sampling, this is the Nyquist frequency (half the sampling rate).

If you don’t, and just sample the continuous non-bandlimited waveforms, the signal you get is similar to what a “proper” bandlimited sawtooth/pulse wave would look like, but it’s got a lot of other noisy junk in it, corresponding to frequencies above Nyquist that weren’t representable and got reflected back into the representable part of the spectrum – this is “aliasing”.

If you’re doing sound synthesis, you want clean signals without such aliasing noise. The problem is that generating them directly is hard in general. Restricted cases (perfect sawtooth or square waves where you never change the frequency or other parameters) are reasonably easy, but that doesn’t help you if you want to tweak knobs describing the shape of the waveform in real time, doing pulse-width modulation, or various other tricks.

One such other trick is “hard sync”; two oscillators, where the first oscillator resets the phase of the second whenever it wraps around. This is done in analog synthesizers and the resulting sound is harmonically quite interesting, but the resulting waveform is complex enough to defeat straightforward attempts at description using additive synthesis or similar.

It would all be much simpler if you could work with the convenient non-bandlimited saw/pulse waves, where everything is easy, and just subtract the aliasing later. Well, turns out that because sampling and everything else involved in this chain is linear, you can in fact do *exactly that*.

What this paper does is introduce what’s called “MinBLEPs” – minimum-phase BandLimited stEPs. You simply work with the convenient continuous functions, and whenever a discontinuity is introduced, you insert a corresponding MinBLEP, which cancels out the aliasing. It’s a beautiful solution to a long-standing practical problem.

### 10. Veach – [“Robust Monte Carlo Methods for Light Transport Simulation”](http://graphics.stanford.edu/papers/veach_thesis/) (1997; computer graphics)

This one’s a PhD thesis, not a paper. I’ve been active in computer graphics for a long time, but there aren’t many graphics papers linked in here. That’s partly because I have many interests outside of CG, but also due to the nature of computer graphics research, which tends to be rapid-paced and very incremental. That makes it hard to single out individual papers, for the most part.

Veach’s PhD thesis sticks out, though. When it was initially published, Veach’s research was groundbreaking. Now, nearing its 20th anniversary (it was published in December of 1997), it’s probably better summarized as “classic”, with important contributions to both theory and algorithms.

This is not light reading, but it’s definitely a must-read for anyone interested in unbiased rendering.

I enjoyed the list on Twitter; I haven’t read all of them, though. (My favorite so far is in the next batch.) A few comments:

– The paper on complex systems failure felt very familiar, but unfortunately, it didn’t say all that much about what to do about it. Perhaps a bit gloomy :-)

– The Huffman paper was sort of surprising to me, but it seems to skip over the rather common optimization of keeping the explicit tree but building LUTs for both encoders and decoders, which works with any kind of prefix code (useful if your code is somehow “weird”, e.g. if it has forbidden codes or otherwise isn’t freely choosable). I didn’t look closely enough to see if the paper’s solution ends up in the same kind of table-driven approach, but it didn’t immediately look like it.

– minBLEP is an interesting approach, but ultimately doesn’t do too well in listening tests as far as I know (if the goal is to replicate e.g. a bandlimited sawtooth). As far as (otherwise unrelated) anti-aliasing papers go, https://ccrma.stanford.edu/~dattorro/EffectDesignPart2.pdf is one of my favorites; it finally explains why linear interpolation of audio is so bad (by explaining how it corresponds to a time-varying lowpass filter).

The Huffman paper does cover LUTs (“Algorithm TABLE-LOOKUP”). There are big advantages from canonical codes in both the decoding step and the table-build step (which is not to be neglected); the ONE-SHIFT equivalent is fairly hard to beat if you have a Huffman table that’s only used for a few hundred symbols.

Re: minBLEP listening tests: citation needed! :) Many implementations are broken in subtle ways (e.g. they don’t account correctly for fractional phase), which can make a big difference.

I will readily admit that I didn’t keep listening test papers for a technique I discarded ten years or so ago. :-) So they could very well be broken.

Bookmarked the Twitter thread, Appreciate the blog post!

Just as a bit of reminiscing… Alistair Moffat’s info management class (which I took in… probably 1995; “Managing Gigabytes” was the textbook, and my copy is signed by all three authors) is one of the best I ever did. I learned more about entropy coding in 2 hours of his lectures than I would have reading a dozen textbooks.

Also Andrew Turpin is a much better Bridge player than I am.

The Herlihy link is dead, here’s one that’s active as of typing this: http://web.cs.wpi.edu/~cs3013/e11/Papers/Herlihy_WaitFreeSync.pdf

Thanks as always for taking the time to write these posts up.

Valmari, “Fast brief practical DFA minimization” (number 6 on the list) seems to be dead link now, I believe this is the piece (?), if anyone will be looking for it:

Click to access Valmari12.pdf

Thank you for assembling this list, I find these very enjoyable and the different topics keep things fresh. :) Currently aiming to learn more in-depth stuff about compression, and your and cblooms blogs are very good sources to keep me engaged.