---
title: AVX10/128 is a silly idea and should be completely removed from the specification
url: https://chipsandcheese.com/p/avx10-128-is-a-silly-idea-and-should-be-completely-removed-from-the-specification
author: Felix LeClair
published: '2023-10-11'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# AVX10/128 is a silly idea and should be completely removed from the specification

## Intro and lots of context

Intel recently unveiled the AVX10 specification as means for consolidating the vast majority of AVX-512 extensions into a single, easy-to-target specification. It aims to solve a few issues, among which is the startling array of configurations, targets, and spaghetti of AVX-512 implementations with disjointed instructions support. Lest we forget, it also primarily serves as means of bringing together all the beloved AVX-512 goodies into smaller implementations, targeted at consumer, micro-edge and embedded that can’t or won’t have the 32 512-bit registers required by AVX-512.

I’ve publicly expressed my enthusiasm for the specification since the initial publication. Relatedly, I’m giving a talk for the Easy Build/HPC communities under the title “AVX10 for HPC: a reasonable solution to the 7 levels of AVX-512 folly.” This article was originally slated to be a part of the talk, but I’m writing it out instead for the sake of reference (and because I’m already struggling to get the talk down to 90 minutes, let alone the 60 I have). **Editors note 18/10/2023: The link to public recording of the talk can be found at the end of this article**

## AVX10, what is it?

To begin, let’s break down AVX10.N/M: AVX10 is the new “foundational” SIMD/vector instruction set for x86_64. The “.N” denotes the version of AVX10 as a version modifier, allowing incremental updates. It is important to note, if you support “AVX10.N+3,” you must support all of AVX10.N, N+1 and N+2. In simpler words, users are guaranteed supersets of previous instruction sets.

What does the “/M” mean? It’s a reference to vector register implementation size of a given AVX10.N version. Specifically, it may be 512-bit, 256-bit, or the topic of this article, 128-bit wide.

128-bit registers, a.k.a XMM registers, were introduced with SSE(1) for the 32-bit only Pentium 3 in 1999. 256-bit registers were introduced with AVX1, and first implemented in the Sandy Bridge micro architecture in 2011. 512-bit registers were specified by AVX-512 and released around 2016 with Xeon Phi, but weren’t generally available until 2017 with the release of Skylake-X.

To give an idea of what each of those looks like, here’s a comparison of the “add packed single-precision floating-point values (ADDPS)” instruction, courtesy of the [officedaytime.com SIMD instruction visualizer](https://www.officedaytime.com/tips/simd.html).

## A note on naming

### From AVX, to AVX2, to AVX-512, to AVX10

After speaking with some of my favourite folks from intel, officially there aren’t “specific” reasons the name AVX10 was chosen as the successor to AVX512, beyond “marketing is going to market.”

I have an alternative theory:

The AVX-512 specification we know today started out as a much smaller VEX-encoded ISA, known as AVX3 internally, as well as some early marketing materials. AVX3 was “relatively” boring as it only expanded registers, stayed VEX and provided a more exhaustive fused multiply add, similar to what AMD attempted with the FMA4 instructions. Taking that view to the past, if you set the AVX512f extensions to be “AVX3” and then exclude the Xeon Phi-only extensions, AVX512 had ~6 groups of extension worthy of being called discrete generations. Roughly, you can categorize them into:

AVX3 F, CD, ER, PF

AVX4 VL, DQ, BW

AVX5 IFMA, VBMI

AVX6 BF16

AVX7 VPOPCNTDQ VNNI, VBMI2, BITALG

AVX8 VP2INTERSECT – deprecated

AVX9 FP16

AVX10 – the new “big one”


## Back to the good stuff

On the server and HPC side, expect all implementations to conform to the AVX10.N/512 specification. In other words, you should expect implementations to use AVX10.N with 512-bit vectors. This ensures that any existing AVX-512 code is fully supported, and continues the legacy of backward compatibility for x86_64.

On the consumer side, having a massive register file with 32 registers, each of which 512-bits is considered problematic and non-viable. However, as seen in [Zen 4](https://chipsandcheese.com/2022/11/05/amds-zen-4-part-1-frontend-and-execution-engine/), Alder Lake, [Tiger Lake](https://chipsandcheese.com/2022/07/15/caching-energy-efficiency-data-mobile-and-avx-512/) and [more](https://chipsandcheese.com/2022/03/23/via-part-4-a-deep-dive-into-centaurs-last-cpu-core-cns/), it’s rather doable. The problem is that small, “efficiency” cores, notably Intel’s recent Gracemont (in [Alder Lake](https://chipsandcheese.com/2021/12/02/popping-the-hood-on-golden-cove/) and Raptor Lake), and Crestmont (in upcoming Meteor Lake and Sierra Forest) microarchitectures, prefers to only implement 128-bit physical ALUs, relying on so-called “double pumping” (a more limited version of register pipelining from the Vector Processor days) to achieve AVX2 support. This way, they can implement the 16 x 256-bit registers of AVX2, but only need to implement 128-bit floating point and integer units. This comes with a cost: while you save on die space and power, some workloads may see significant performance regressions.

Knowing this, the fine folks at Intel designing the AVX10 spec mandated that all implementations must have 32 registers, but said registers would only need to be as wide as the given “/M”. This means AVX10/256 would have the same instruction capabilities as AVX10/512, but only require the 32 registers be 256-bits wide.

For the most part, any code written for the older AVX-512 extensions that were limited to 256-bit registers should* run fine with only a recompile. This sort of code came about as a result of the much fabled “AVX-512 down-clocking” menace that would “punish” you for using the 512-bit part of AVX-512. The good news is there’s a lot of code already designed for a “simplified” 256-bit version of AVX-512, which will either be ready or easy to migrate when the time comes.

**It’s slightly more complicated than the above, but you can get it going between a few hours and a few days.*

## But what does the Spec Say?

If you read the AVX10 specification ([Intel White paper on AVX10](https://cdrdv2-public.intel.com/784343/356368-intel-avx10-tech-paper.pdf), [full AVX10 specification](https://cdrdv2-public.intel.com/784267/355989-intel-avx10-spec.pdf)), a few things stand out.

Namely, the technical paper repeatedly uses the word “converged”. What features are converging? The answer is all the distinctive features of AVX-512 that aren’t just “big registers”. Things like IEEE-754 half precision floating points? Supported as part of AVX10. What about brain floating point 16 (BF16), a truncated version of FP32 used in the buzzword *du jour*, “AI”? Supported as a part of AVX10. What about every AVX-512 assembly programmers’ favourite dynamically reprogrammable ternary logic operator instructions? Supported as a part of AVX10. Basically, all the cool stuff assembly and compiler programmers want to use to speed up applications via smarter algorithm design are included as part of AVX10.

Another important AVX10 requirement is that all implementations must fully implement AVX2 and its 16 x 256 bit registers. In turn, you’re guaranteed support for AVX2 code on your processor. For the maths folks, you can think of it as AVX10 having the full set of AVX2 within its own set. AVX2, in turn, requires all of AVX1.

## So finally, the meat and potatoes: AVX10.N/128

I have 3 “core” problems:

Any and all implementations will be somewhat cursed.

It causes issues for the software that tries to implement the specification.

It effectively triples the per-generation development burden.



### It’s cursed

Any AVX2 implementation must have 16 x 256-bit registers. AVX10 requires 32 vector registers regardless of vector size. In the case of AVX10.N/128, that would be 32 x 128-bit registers. From the (supposed) point of view of a core design engineer/architect, the decision tree of AVX10/128 would be:

Any implementations that only supports up to AVX10/128 must support 16 256-bit YMM registers, a.k.a YMM0-15, and a secondary set of 128-bit XMM registers that span from XMM16-31. The architect is left with a few more choices.

Do you choose to have 2 different classes of SIMD vector registers with different sizes?

Do you

*alias*the upper half of ymm0-15 bits 128-255 – to be xmm16-31 bits 0-127?Do you extend xmm16-31 to be 256 bits?


The third choice is the most likely for a “clean” implementation. But then a realization will hit you: Wait! I’ve now built the same register file need for AVX10/256! If I implement a little more control logic, I have a full, proper AVX10/256 implementation and can keep my 128-bit FPUs and ALUs!

And guess what! We’ve done that before! Famously for Zen 4 and Zen4c, AMD implemented AVX512 using 256-bit FPUs. When Zen 1 adopted AVX2, they *also* double pumped a 128-bit integer unit. Previously, the Bulldozer microarchitecture implemented AVX1 with 128-bit FPUs! And it’s not just AMD! Intel does the same today with 128-bit FPUs and integer ALUs on Gracemont.

So you take a step back and realize you’ve already implemented double pumping in the first place, because you need to support the 16 x 256-bit registers for AVX1 and 2! Specifically, AVX requires logics to address, mask, load, and store both the high and low parts of a given register.

### Software implementation headaches

The next step is relatively simple: address issues for optimizing software implementations by targeting modern ISA implementations. One of the guarantees of AVX10 is that any implementation supports all smaller valid implementations. In other word, while AVX10/512 platforms support AVX10/256, AVX10/256 platforms do not support AVX10/512. By extension, AVX10/256-512 platforms support AVX10/128.

But here’s the problem. From a software targeting point of view, when AVX10 becomes ubiquitous enough to be the default x86_64 target in about a decade, AVX10/128, as the most compatible choice, ends up being a net downgrade over AVX2 for SIMD programs. If AVX10/128 is valid and makes its way to market, it becomes the *de facto* minimum target for AVX10, as it supports all server and consumer options. While it’s true that the best part of AVX-512 was not the 512 bits, it’s simultaneously true that a downgrade to 128-bit registers as a common target would be detrimental to SIMD code generation – a reminder as we moved past 128-bit registers on consumer platforms over a decade ago. Code generation has moved on. Do we really want to be stuck with a sidegrade to 128-bit registers with better instructions in a decade’s time?

### You want to make even **more** targets?!?!

**more**

My last point is that, from a software point of view, AVX10 with only 256-bit and 512-bit options effectively doubles the burden for each generation. It has already happened with consumer Golden Cove vs enterprise Golden Cove. Namely, the former only supports up to AVX2, but the latter implements all of AVX512 (to the point of being compatible with AVX10.1/512).

The “same” microarchitecture (uArch) may have different memory configurations, different amounts of Fused Multiply Add (FMA) units, different amounts of vector add units, etc.

Looking at Golden Cove, we have: consumer AVX2 with DDR4 and DDR5, workstation AVX-512 with DDR5, server AVX-512 with DDR5, server AVX-512 with HBM only, and server AVX-512 with DDR5 main memory and HBM cache.

While HPC is used to kernels (fancy name for a maths routine) with multiple versions for different sub-SKUs of an ISA, consumer software avoids doing this at all cost. You’re lucky in consumer software if the maintainers turns on anything past SSE2, let alone AVX in any of its flavours.

And I don’t blame them. From a maintenance point of view, it is unreasonable to ask every package manager to compile different versions of projects for different versions of ISAs, to tune for differently platforms, and somehow manage to always build and ship them. Now you’re going to add all of that on top of keeping up with the existing burdens of package management? I don’t think so. In HPC, you can rely on most users to recompile software for their clusters, but this simply doesn’t happen on consumer platforms. Heck, not even Arch Linux implementes that experimentally!

## Conclusion: what do I want?

My request to Intel – more specifically the evangelists, fellows, VPs, principal engineers, etc. – is simple. Page 1-2 of Intel document 355989-001US, rev 1.0, currently reads:

For Intel AVX10/256, 32-bit opmask register lengths are supported. For Intel AVX10/512, 64-bit opmask are supported. There are currently no plans to support an Intel AVX10/128 implementation.


I’d request that the above be changed to:

For Intel AVX10/256, 32-bit opmask register lengths are supported. For Intel AVX10/512, 64-bit opmask are supported. Support for an Intel AVX10/128 only implementation is not provided for within this specification. All AVX10/256 and AVX10/512 implementations shall allow for operations on scalar and 128-bit vector registers.


The specific phrasing here is meant to make sure that should intel ever want to explore an AVX10-based architecture designed for a many-core product, conceptually like Xeon Phi, they can. This way, compilers, library developers, and other software vendors aren’t in a “will they won’t they” holding pattern. It avoids needing to leave hooks in for something that’s allowed to exist per spec but won’t make it to market. The changes would still allow them to build the product eventually, but those designing for the product can bear the burden of supporting it, leaving us normal dev folks alone. The product would probably be a “simple” atom core that implements the scalar versions of AVX10, each core having its own AMX unit. But I’ll leave the rampant product speculation to a different parts of the industry

So, I humbly ask: Intel, please, please, please make AVX10/128 an illegal implementation under the current specification.

And for those interested in the history of instruction sets on x86_64, from the original x87 FPU all the way to AVX10, my talk on AVX10 for HPC is Friday the 13th of October 2023. Link here: [https://easybuild.io/tech-talks/008_avx10.html](https://easybuild.io/tech-talks/008_avx10.html)

Editors note: Link to recording of the above talk is here: [https://www.youtube.com/watch?v=hcQbZpt1V0E&t=1s](https://www.youtube.com/watch?v=hcQbZpt1V0E&t=1s)

If you like our articles and journalism, and you want to support us in our endeavors, then consider heading over to our [Patreon](https://www.patreon.com/ChipsandCheese) or our [PayPal](https://www.paypal.com/donate/?hosted_button_id=4EMPH66SBGVSQ) if you want to toss a few bucks our way. If you would like to talk with the Chips and Cheese staff and the people behind the scenes, then consider joining our [Discord](https://discord.gg/TwVnRhxgY2).