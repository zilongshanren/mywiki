---
title: Why x86 Doesn’t Need to Die
url: https://chipsandcheese.com/p/why-x86-doesnt-need-to-die
author: Chester Lam
published: '2024-03-27'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

Hackaday recently published an article titled “Why x86 Needs to Die” – the latest addition in a long-running RISC vs CISC debate. Rather than x86 needing to die, I believe the RISC vs CISC debate needs to die. It should’ve died a long time ago. And by long, I mean really long.

About a decade ago, a college professor asked if I knew about the RISC vs CISC debate. I did not. When I asked further, he said RISC aimed for simpler instructions in the hope that simpler hardware implementations would run faster. While my memory of this short, ancient conversation is not perfect, I do recall that he also mentioned the whole debate had already become irrelevant by then: ISA differences were swept aside by the resources a company could put behind designing a chip. This is the fundamental reason why the RISC vs CISC debate remains irrelevant today. Architecture design and implementation matter so much more than the instruction set in play.

Some Key Terms

CISC and RISC

CISC stands for Complex Instruction Set Computer. Historically, the CISC philosophy aimed to accomplish a task with fewer, more complex instructions. In the 1970s, the x86 instruction set was designed with the CISC philosophy in mind.

In contrast, the Reduced Instruction Set Computer (RISC) philosophy wanted to use fewer and simpler instructions to make hardware design easier. Hopefully simpler hardware could run faster and be more performant. MIPS and ARM were originally designed following the RISC philosophy in the 1980s.

Superscalar

A superscalar CPU can execute more than one instruction per clock cycle, in contrast to a scalar one that can only execute one instruction at a time.

Out-of-order execution

A CPU with out-of-order execution can internally execute instructions as their dependencies become ready, irrespective of program order. It means independent instructions can begin execution ahead of a stalled one, improving execution unit utilization and mitigating the impact of cache and memory latency.

But What Are Modern CPUs Really Like?

Here are block diagrams outlining the microarchitecture of two unrelated CPUs, developed by different companies, running different instruction sets. Neither CPU core is simple, but both have a lot in common.

AMD’s Zen 4 architecture. I drew the diagram from AMD’s figures, with some details figured out through microbenchmarks.

Arm’s Cortex X2 architecture. I drew the diagram mostly from microbenchmark results to infer architectural details.

Cortex X2 and Zen 4 both use superscalar, speculative, out-of-order execution with register renaming. Beyond the core, both Cortex X2 and Zen 4 use complex, multi-level cache hierarchies and prefetchers to avoid DRAM access penalties. All of these features have everything to do with maximizing performance, especially as compute performance keeps outpacing DRAM performance. They have nothing to do with the instruction set in play.

Where the Problem Doesn’t Lie

Hackaday mentions the complexity of fetching and decoding instructions, but this isn’t a problem unique to x86. No modern, high-performance x86 or ARM/MIPS/Loongarch/RISC-V CPU directly uses instruction bits to control execution hardware like the MOS 6502 from the 1970s. Instead, they all decode instructions into an internal format understood by the out-of-order execution engine and its functional units.

Decoding is expensive for RISC architectures too, even if they used fixed length instructions. Like Intel and AMD, Arm mitigates decode costs by using a micro-op cache to hold recently used instructions in the decoded internal format. Some Arm cores go further and store instructions in a longer, intermediate format within the L1 instruction cache. That moves some decode stages to the instruction cache fill stage, taking them out of the hotter fetch+decode stages. Many Arm cores combine such a “predecode” technique with a micro-op cache. Decode is expensive for everyone, and everyone takes measures to mitigate decode costs. x86 isn’t alone in this area.

Some observed LASX vector extension instruction encodings from LoongArch, which descended from MIPS.

Hackaday further takes issue with instruction set extensions and increasing instruction count, but neither are distinctly x86 features. ARM has similarly been through numerous revisions and extensions. Where x86-64 has SSE, AVX(2), and AVX-512 vector extensions, 64-bit ARM (aarch64) has ASIMD, SVE, and SVE2 vector extensions. MIPS has a similar story with a MSA SIMD extension. MIPS didn’t get more extensions as ARM and x86 did, but that’s because no one was using it anymore. LoongArch is derived from 64-bit MIPS, but uses incompatible instruction encodings. Loongson has extended LoongArch with the LSX and LASX vector extensions.

ISAs also receive updates that have nothing to do with vectors. aarch64 got updates to accelerate atomic memory operations and speed up `memcpy`/`memset` routines. x86 sees similar updates from time to time, though in different areas. That’s because more transistor budget lets engineers do more things in hardware, and adding more instructions for specific workloads is a great way to speed them up.

mpsadbw is fine

Next, Hackaday focuses on x86’s mpsadbw instruction, noting that it’s doing “at least 19 additions but the CPU runs it in just two clock cycles.” The author should think of why that instruction exists by looking at its use cases. Video codecs strive to efficiently use bandwidth and disk space by representing most frames in terms of how they differ from previous ones, rather than storing the entire frame. Calculating the sum of absolute differences (SAD) is a good way to see how much a block has changed, and is a vital part of video encoding. ARM has similar vector instructions.

The author then suggests adding more instructions (like mpsadbw) makes register renaming and instruction scheduling more complex. That makes intuitive sense, but doesn’t match reality. Even though mpsadbw does more low-level operations, it only requires two register inputs and one destination register. The renamer therefore only needs to read two values from the register alias table to determine where to get inputs from, and allocate one free register to store the result.

The author looked at an instruction, noted that it does multiple calculations, and therefore concludes it looks scary, but let’s consider the alternative. We can perform the vector SAD calculation with RISC-like instructions (excluding the selection part of mpsadbw). Each simple RISC instruction would require the same degree of register renaming as the “complex” msadbw instruction. Each input requires a lookup in the register alias table, and a free register has to be allocated to hold each result.

Only covering the sum of absolute differences part, and not even all of that because there are already too many overlapping arrows

Contrary to the author’s claims, complex instructions actually lower register renaming and scheduling costs. Handling an equivalent sequence of simple instructions would require far more register renaming and scheduling work. A hypothetical pure RISC core would need to use some combination of higher clocks or a wider renamer to achieve comparable performance. Neither is easy. As shown above, the same register may be renamed multiple times in quick succession, so a wider renamer must cope with a longer potential dependency chain. Beyond a wider renamer, a pure RISC design would need larger register files, schedulers, and other backend buffers to mitigate the impact of having to track more instructions.

Changes Have Already Come

Of course, people designing ARM CPUs understand the importance of efficiently using fetch/decode/rename bandwidth. They also understand the importance of economizing usage of backend resources like register files and scheduler entries. That’s why ARM today has plenty of complex instructions that perform many low-level operations under the hood. Vector instructions may be the most prominent example, but it’s easy to find other examples, too. aarch64 has long supported loading a value from memory with an address generated by shifting an index register, and adding that to a base register. That’s a chain of three dependent operations under the hood, but it simplifies array addressing.

On the other side, simple instructions often make up the majority of an executed program’s instruction stream. That’s especially applicable for programs that are hard to parallelize, like file compression or web browsing. CPUs today therefore have to be good at executing simple operations quickly. At the same time, they benefit from having complex instructions to speed up specific workloads.

A page from Arm’s Cortex X2 optimization manual, showing the core doing complex operations (RSUBHN2 for example could do 16 8-bit subtractions, select the most significant half of each result, and perform rounding, all over two cycles)

Instruction sets today have changed with that reality in mind. The “CISC” and “RISC” monikers only reflect an instruction set’s distant origin. They reflect philosophical debates that were barely relevant more than three decades ago, and are completely irrelevant now. It’s time to let the CISC vs RISC debate die, forever.

Where Problems Actually Lie

Hackaday mentions x86’s real mode, leading to another important point: compatibility. When gushing over different CPUs and the performance they offer, it’s all too easy to forget what that performance is needed for: running software. If a CPU doesn’t run the software you need, it’s a tiny brick. x86-64 CPUs keep real mode around so that operating systems can keep booting in the same way. Today, you can create a single OS install drive that works on a modern Zen 4 system, a Phenom system from 15 years ago (just make sure you use MBR boot) and everything in between. That 15-year-old Phenom system can run recent operating systems like Windows 10 or Ubuntu 22.04. Of course there are limits, and you can’t run Windows 10 out of the box on a Northwood Pentium 4. But real mode support is part of what makes the same OS boot code work across so many CPUs. It’s part of the PC compatibility ecosystem that gives x86 CPUs unmatched compatibility and longevity.

Other ecosystems present a sharp contrast. Different cell phones require customized images, even if they’re from the same manufacturer and released just a few years apart. OS updates involve building and validating OS images for every device, placing a huge burden on phone makers. Therefore, ARM-based smartphones fall out of support and become e-waste long before their hardware performance becomes inadequate. Users can sometimes keep their devices up to date for a few more years if they unlock the bootloader and use community-supported images such as LineageOS, but that’s far from ideal.

The LineageOS project has over 1000 repositories, because image builds for each device have to be handled separately.

Intel and AMD correctly realized that spending extra effort on compatibility is worthwhile. Doing so streamlines software distribution, and lets users hang onto their expensive hardware for longer.

Of course, compatibility can’t be maintained forever. ISAs have to evolve. AMD and Intel probably want to save some money by reducing the validation work needed to support real mode. Intel is already planning to drop real mode. Any ISA has to receive updates as requirements change over time. But compatibility breaks should be kept to a minimum, to avoid shoving users onto an upgrade treadmill with no clear benefit.

Conclusion

The CISC vs RISC debate seems to reignite every few years, often with claims that x86 should die. That debate was most compelling in the early 1990s while I was learning to walk. Alpha’s EV5, for instance, was a four-wide core from 1994 that ran at 266 MHz. Intel’s best 1994 CPU was the two-wide, 120 MHz Pentium. But soon Intel showed they could develop high performance designs of their own, and we know what happened by the end of the decade.

The 2000s saw Intel themselves try to push x86 to the side. Itanium was designed around the principles Hackaday’s author believes so strongly in. It used a set of 128 architectural registers to avoid register renaming. It used simple, fixed-length instructions. It dropped out-of-order execution to move scheduling responsibilities to the compiler. All of those ideas failed because increasing transistor budgets allowed better branch prediction and larger out-of-order execution structures. Hardware out of order execution could adapt to changing program behavior and naturally generate more optimal instruction schedules. Since out-of-order execution was necessary for high performance anyway, there was little point in keeping Itanium around.

From Intel’s Hot Chips presentation

Toward the late 2010s, Marvell’s ThunderX3 and Qualcomm’s Centriq server CPUs tried to find a foothold in the server market. Both used aarch64, and both were terminated by the end of the decade with little to show for their efforts. That’s not to say aarch64 is a bad ISA, or that ThunderX3/Centriq were doomed by it. Rather, a CPU needs to combine high performance with a strong software ecosystem to support it.

Today, aarch64 has a stronger software ecosystem and better performing CPU cores. Ampere Altra chips are deployed across Google, Microsoft, and Oracle’s public cloud offerings. Amazon is also using Arm’s Neoverse cores in their cloud. aarch64 is in a place where it can compete head on with x86 and challenge the Intel/AMD duopoly, and that’s a good thing. But Arm, RISC-V, and MIPS/LoongArch will have to succeed through the merits of their hardware design and software ecosystems. All of those instruction sets are equal enough in areas that matter.

Going forward, I hope we’ll have more productive, well-researched discussions on the merits of various CPU designs. Of course, ISA can be part of the debate, as various ISA extensions can have a tangible impact on performance. Licensing and royalties should also be discussed, as both regularly kill all sorts of promising technologies. But utterly incorrect claims like “In RISC architectures like MIPS, ARM, or RISC-V, the implementation of instructions is all hardware” need to get thrown out. The year isn’t 1980 anymore.

If you like our articles and journalism, and you want to support us in our endeavors, then consider heading over to our Patreon or our PayPal if you want to toss a few bucks our way. If you would like to talk with the Chips and Cheese staff and the people behind the scenes, then consider joining our Discord.

Finally a detailed article countering the myths being spread in the name of tech journalism... Immensly appreciated!