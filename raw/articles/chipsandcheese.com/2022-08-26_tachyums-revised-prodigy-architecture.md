---
title: Tachyum’s Revised Prodigy Architecture
url: https://chipsandcheese.com/p/tachyums-revised-prodigy-architecture
author: Chester Lam; Dr Ian Cutress
published: '2022-08-26'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

The world of semiconductor startups looking to break into the market is huge, either with some large AI training chip, or some super fast small inference device, or perhaps a HPC focused design for one particular problem the world is trying to solve. A number of these are flush with venture capital funding, many in the $100m+ range, and some with big backing above the $1b mark. In this article we are looking at Tachyum, a US/EU chip startup that first came onto our radar in 2018 with a mindblowing design covering multiple markets that no-one really believed would work, even despite a hoard of expertise behind the company with successful high-performance and high-frequency processor design. Today in 2022, they’ve revised that earlier design, and the long and short of it is that it looks more like a compute architecture that could really break the mold, assuming the bits we don’t know about do what Tachyum claim they do.

We’re talking a 128-core, 2×1024-bit vector per core, 5.7 GHz, 1 TB/sec of DRAM behemoth that on the top model pings 950W. Whoever said we were running out of thermal headroom in the datacenter was clearly wrong, and Tachyum have a point to prove. In this article, we’re going through the new design, how it compared to the old one, and what we can glean from Tachyum’s disclosures.

Tachyum Prodigy 2022

Today, Tachyum still calls their architecture ‘Prodigy’. But they’ve overhauled it in response to customer feedback. VLIW bundles are gone in favor of a more conventional ISA. Hardware scheduling is much more capable, improving performance per clock. And the cache hierarchy has seen major modifications. 2022 Prodigy’s changes are sweeping enough that much of the analysis done on 2018’s Prodigy no longer applies.

At a high level, 2022 Prodigy is still a very wide architecture with gigantic vector units:

Updated our diagram with the new information from Tachyum’s Whitepaper but we are unsure how they have 12 scheduler queues yet only 11 ports on their diagram.

And like 2018 Prodigy, 2022 Prodigy targets both extremely high clock speeds and high core counts. In fact, these goals have been pushed up, with clock speed going from 4 to 5.7 GHz, and core count doubling from 64 to 128. Let’s dive into the details.

Goodbye Bundles, Hello Sane ISA

Tachyum initially tried to simplify CPU design by tying the instruction set closely to the underlying hardware implementation. VLIW bundles allowed very simple decode and mapping logic. Scheduling was assisted by the compiler, which would set “stop bits” to mark groups of instructions that could be issued in parallel. This scheme is superficially similar to Nvidia’s use of static scheduling in Kepler and later GPU architectures, and lets the core skip dependency checking in hardware.

But tying the ISA to the hardware created a forward compatibility problem. Stop bits for example, would have to be set differently if a new architecture had different instruction latencies. Tachyum’s potential customers would not accept ISA changes between product generations. In practice, something as “simple” as adding ARM support to a complex software project could take upwards of 18 months. Supporting a new ISA had to be a one-time investment, not something that would be repeated with each CPU upgrade.

The latest Prodigy architecture addresses this by discarding the original VLIW scheme in favor of a more conventional ISA. Instructions are four or eight bytes long. Encodings no longer include a “stop bit”, meaning that Prodigy now does dependency checks in hardware instead of relying on the hardware to mark groups of independent instructions.

Frontend and Branch Prediction

Despite ditching the VLIW setup, Prodigy can still sustain eight instructions per cycle – an incredible achievement for a CPU targeting 5.7 GHz. According to Rado, this core width was necessary to achieve maximum performance in AI and HPC loads. In integer workloads, a 4-wide core would be plenty, and going up to 8-wide would only improve performance by 7-8%. However, one loop iteration in an AI or HPC program might execute two vector instructions, two loads, increment a loop counter, and conditionally branch. Bringing core width up to 8-wide would let Prodigy complete a loop iteration every cycle.

To maintain that throughput, Prodigy can pull an incredible 128 bytes per cycle from the L1 instruction cache. This is absolute overkill, considering that 64 bytes is enough to contain eight instructions. Tachyum may have opted for more fetch bandwidth to maintain high throughput around taken branches. Prodigy doesn’t have a large L0 BTB, so it’s likely to suffer more instruction fetch stalls around taken branches than Zen 3 and Golden Cove. By fetching 128B bytes at a time, the frontend can “catch up” after losing a cycle to BTB latency.

Prodigy’s branch predictor has also been improved. BTB capacity is doubled to 2048 entries, and the prediction algorithm is an improved version of the gshare one in 2018 Prodigy. But overall, Prodigy’s predictor is not in the same class as those found in the latest AMD, ARM, and Intel high performance cores. AMD’s Zen 3 has a 6656 entry main BTB. ARM’s Neoverse V1 has 8192 BTB entries, and Intel’s Golden Cove has an incredible 12K entry BTB. BTB capacity isn’t the only drawback. Prodigy continues to use a BTB tied to the instruction cache. This simplifies design because there’s no need to do a separate BTB lookup – a L1i lookup gives you both instruction bytes and branch targets. AMD’s Athlon did something similar, and ARM used this scheme into the mid 2010s. But modern cores from AMD, ARM, and Intel have moved to a decoupled BTB, allowing them to maintain high instruction bandwidth when code footprints exceed L1i capacity. With a coupled BTB, a L1i miss implies a BTB miss. And not knowing where the next branch will go greatly reduces how far you can effectively prefetch after an instruction cache miss. But Tachyum is using standard cell libraries and targeting very high clock speeds, and a decoupled BTB was considered too expensive with those standard cell libraries.

To counter this, Tachyum has increased L1i capacity to 64 KB, quadruple that of 2018 Prodigy, to make sure L1i misses are rare. Rado notes that 64 KB L1i miss rate in specint2017 is under half a percent. Our observations with Ampere Altra’s 64 KB L1i roughly align. A bigger L1i also helps with power efficiency, and minimizes contention with the data side over L2 bandwidth.

ARM has employed larger 64 KB L1i caches to great effect, and enjoys low L1i miss rates

2022 Prodigy also continues to rely on the rather dated and basic gshare prediction algorithm, while modern CPUs use more complex techniques that allow better prediction accuracy with a given storage budget. Tachyum considered building a more advanced branch predictor. But again, standard cell libraries meant that implementing a TAGE predictor would decrease clock speed by too much to make it worthwhile. A perceptron predictor was ruled out because of the high clock speed requirement – you can imagine that summing up a batch of weights is a lot to do within a clock cycle. Schemes incorporating local history were also not feasible, because the high fetch bandwidth meant multiple predictions would have to be performed per cycle. Multiple predictions with local history would require multiple history table lookups every cycle. So, Tachyum stuck with a global history based predictor, and does predictions per block of eight instructions. That keeps the branch predictor simple while letting it keep up with the prediction bandwidth demanded by Prodigy’s core width.

Intel’s Rocket Lake core, with the branch predictor storage and other frontend caches labeled. Image from Fritzchens Fritz, annotations by Clam

Rado mentioned that a future version of Prodigy could use custom cells, which would let them consider more advanced branch predictors while still targeting very high clock speeds. For comparison, Intel seems to use custom SRAM cells in the branch predictor that aren’t seen elsewhere in the core. AMD takes a different approach, using the same SRAM cells for branch predictor storage, the L1 instruction cache, and micro-op cache.

AMD’s Zen 3 core, with branch predictor storage and other frontend caches labeled. Image from Fritzchens Fritz, annotations by Clam

Zen 3 shows that it’s possible to build a state of the art branch predictor using standard cells, though perhaps not at Prodigy’s targeted 5.7 GHz speed.

Backend: Huge Vector Units, and Full OoO?

Building a wide core doesn’t mean much if you can’t keep it fed. To do that, Tachyum departed from their 2018 design and implemented deep reordering capabilities in hardware. 2022 Prodigy can track up to 256 instructions in flight, with 128 renames for integer registers and just as many for vector registers. It can reorder past all kinds of dependencies. From what we can tell with what Tachyum described, Prodigy can do full out of order execution like cores from AMD, ARM, and Intel. But instead of using a more conventional out of order engine, a check-pointing scheme is used. On instructions that could cause an exception, like a load that misses cache, Prodigy saves a checkpoint with register state. If that instruction does cause an exception, that checkpoint is used to provide precise exception handling. 2022 Prodigy can save multiple checkpoints, allowing for increased reordering capacity. This is a significant improvement over 2018 Prodigy, which could only save a single checkpoint.

As far as execution units go, Tachyum has equipped 2022 Prodigy with two gigantic 1024-bit vector units and increased vector register width to match. 2022 Prodigy thus has twice the vector width as 2018 Prodigy, and more vector throughput than any general purpose CPU around today. Even Intel’s Golden Cove only has two 512-bit vector units.

Cache Subsystem

After redesigning the Prodigy architecture to do more reordering in hardware, and thus enabling it to draw in more bandwidth for AI/HPC applications, Tachyum was faced with the challenge of keeping those cores fed. And feeding 1024-bit vector units running at insane clocks is a formidable challenge. To start, L1D data paths have been doubled in width, to match the increase in vector length. At 5.7 GHz, a Tachyum core can load data from its L1D at almost 1.5 TB/s. The L2 can deliver a full 128B cache line to the L1D per cycle, for around 730 GB/s of bandwidth. For comparison, Intel’s L1D and L2 caches have half the per-cycle load bandwidth of Prodigy’s. AMD is even further behind. Zen 2 and Zen 3 have half of Intel’s per-cycle bandwidth at L1 and L2. And of course, Prodigy clocks higher than Intel or AMD’s current CPUs, giving it a gigantic cache bandwidth advantage.

Zen 2 seems to be able to track at least 32 pending L2 misses, from uh, using count masking on undocumented performance counters

To sustain high bandwidth and hide latency, 2022 Prodigy has improved memory level parallelism (MLP). Specifically:

This is a big improvement over the 2018 version, where achievable bandwidth to L3 and memory will be limited by its low MLP. It’s in the same neighborhood as Zen 3 and Golden Cove, though likely a bit less capable in absolute terms.

2022 Prodigy also increases cache capacities to better handle loads with large memory footprints. The L1 data cache sees its capacity quadrupled from 16 to 64 KB. Per-core L2 and L3 cache capacities haven’t increased over 2018 Prodigy, but 2022 Prodigy ditches the separate L2 and L3 layout in favor of a virtual L3 setup. Idle cores will allow active ones to use their L2 as a virtual L3, increasing cache hitrates for low threaded loads. When a core evicts a line from its L2, it’ll check surrounding cores to see if their L2 can accept the evicted line. Only L2 caches belonging to inactive cores will accept these requests.

To me, this setup is not simple at all, and there’s gonna be a lot of secret sauce and tuning around how this virtual L3 is implemented. It sounds like a physical memory address can be cached in multiple virtual L3 slices, depending on which corresponding cores are idle. More slices to check means more interconnect traffic. Tachyum would also want to keep data as close to the consuming core as possible, and fewer possible locations means less flexibility on that front. Getting this virtual L3 setup right sounds like multi-dimensional optimization problem, compared to the simpler schemes used by Intel, AMD, and ARM.

Address translation performance is important too, so Tachyum has increased last level TLB size from 256 to 2048 entries. In terms of entry count, it matches Zen 2, Zen 3, and Golden Cove. To further boost TLB coverage, Prodigy does address translation at larger granularities with 64 KB page sizes, and 32 MB huge pages. A 2048 entry L2 TLB will cover 128 MB with 64 KB pages, versus 8 MB with 4K pages. ARM and x86 mostly use 4 KB pages for client applications, and 2 MB huge pages. Larger page sizes tend to waste more memory, but this isn’t a big deal on servers that typically have hundreds of gigabytes of DRAM.

Memory Bandwidth

For workloads that don’t fit in cache, DRAM bandwidth could be a problem. As we noted in our previous article, Prodigy has a higher compute to memory bandwidth ratio than current CPUs and GPUs. At first, Tachyum tried to tackle this by implementing on-package HBM. But HBM suffers from very low capacities, meaning that it wasn’t a viable option if Tachyum wanted to take on the server market. A HBM solution would be acceptable for HPC and AI applications, but Rado noted that Nvidia already owned a majority of that market, and the remaining market was tiny compared to the server market. Keeping both memory options wasn’t feasible because there wasn’t enough edge space on the chip to fit both DDR and HBM controllers.

So, Tachyum went for a very beefy DDR5-7200 setup with 16 controllers, for a total memory bus width of 1024 bits. That gives it about as much bandwidth as Nvidia’s RTX 3090 GPU. DDR5-7200 isn’t around today, but Tachyum expects that only AI and HPC customers will need the highest performing memory setup possible. These customers usually purchase entire systems instead of components, allowing integrators to bin memory modules that can hit 7200 MT/s. Server applications typically aren’t bandwidth limited, and can use slower DDR5.

But even with DDR5-7200, Prodigy’s massive vector units and high clocks mean it has a lower bandwidth to compute ratio than other CPUs and GPUs. Tachyum is hoping to close that gap by using memory compression, a bit like how GPUs do delta color compression to reduce bandwidth requirements. But unlike GPUs, Tachyum is tuning their memory compression algorithms for AI and HPC applications. Finally, Tachyum is doing ECC at a larger granularity, allowing the memory controller to use some ECC lines to transfer data instead.

Improving Emulation Performance

Tachyum’s Prodigy introduces a new ISA, and thus won’t enjoy a robust software ecosystem as x86 and ARM do. That’s a serious problem, because the best chip in the world is completely worthless if it can’t run the software a user requires. To solve this problem, Tachyum is looking to QEMU, which can emulate another architecture and allow x86 and ARM binaries to execute on Prodigy. But QEMU alone isn’t enough, because emulation performance is often very poor. For example, we ran CoreMark compiled for x86-64 under QEMU on Ampere Altra, and saw a 78% performance drop compared to running the native 64-bit ARM version.

To improve emulation performance with x86 binaries, Prodigy can be switched into “strict” memory ordering mode. This is similar to Apple’s M1, where Rosetta takes advantage of hardware total store ordering support to minimize the performance hit from binary translation. Tachyum has done software work in QEMU to improve performance too. A 30-40% performance hit is still heavy in absolute terms. But just running the required software is a higher priority than absolute performance. All the performance in the world is irrelevant if the chip can’t run the required software, so Tachyum has put effort into QEMU to ensure the hardware is at least usable on launch.

Evaluating the Architecture

Tachyum has modified Prodigy to the point that the 2018 and 2022 versions are basically different architectures. To summarize major pipeline changes:

2022 Prodigy’s changes make it a far more competitive architecture than the version presented at 2018 Hot Chips. Prodigy no longer relies heavily on the compiler, adopts a conventional ISA, and has decent hardware reordering capabilities. Those were our biggest concerns with the 2018 version, and we’re glad to see them addressed. Other weaknesses in the 2018 version, like tiny L1 caches, were corrected as well. That leaves us with a wide core with gigantic vector units, targeting unheard of clocks for high core count chips.

For HPC and AI, I expect Prodigy to be extremely competitive. It has enough reordering depth and memory level parallelism capabilities to make good use of memory bandwidth. While its memory bandwidth to compute ratio is lower than that of competing solutions, Prodigy does have a bag of tricks to alleviate that. Even without those tricks, Prodigy still has a much beefier DRAM subsystem than AMD’s Milan or Genoa. Fujitsu’s A64FX does have comparable DRAM bandwidth, but it uses HBM, which drastically limits its memory capacity.

The server market is a more difficult question. Prodigy has nice, large L1 caches, decent reordering capacity, very high clock speeds, and high core counts. But its branch predictor is far off state of the art, and last level cache capacity per core is low (especially compared to AMD). Worse, transitioning to a new ISA will be a headache for any large company. Still, I think Prodigy has a decent chance, because its clock speed advantage is so great that it could not just drown out its shortcomings, but allow it to deliver both a core count and per-core performance advantage over everyone’s else’s server offerings. Tachyum could convince people to work with their new ISA and fledgling software ecosystem to take advantage of Prodigy’s high performance.

If Prodigy gets close to its ambitious clock targets, it does have a good shot at being a “universal processor”, at least on paper. It combines GPU-like vector throughput with the per-thread performance of a CPU. The tradeoff is extremely high power consumption. 128 core Prodigy can draw up to 950W with its vector units loaded. Even the 32 core, 3.2 GHz low power SKU is spec-ed for 180W – no better than the Zen 2 based Epyc 7502P, which boosts to 3.35 GHz with a similar 180W TDP despite using a chiplet setup and inferior process nodes. In servers, integer workloads are unlikely to make Prodigy draw as much power as TDP figures would suggest. But the high TDP ratings are still a problem because cooling systems have to be designed for a worst case scenario.

About that 5.7 GHz

Personally, I’m skeptical that Prodigy will achieve its 5.7 GHz clock target. Tachyum is employing some strategies that’ll help keep power and area under control at high clocks. We can’t disclose exactly what that is at the moment, but I don’t think it’ll be enough. Pushing two 1024-bit vector units to those clocks would be an incredible feat. Pipeline length looks way too short. 2018 Prodigy had a 9 stage integer pipeline from fetch to execute. 2022 Prodigy adds one stage for hardware dependency checking, bringing the integer pipeline to 10 stages. That’s extremely short for a design targeting 5.7 GHz. For comparison, Agner Fog notes the mispredict penalty (which corresponds to pipeline length) exceeds 20 cycles on Intel’s Golden Cove. AMD’s optimization manual says Zen 3’s mispredict penalty ranges from 11-18 cycles, with a 13 cycle common case. CPUs with similar pipeline lengths to Prodigy get nowhere close to 5 GHz. Neoverse N1 has a 11 stage pipeline and does not run above 3.3 GHz. AMD’s Phenom has a 12 cycle mispredict penalty, and ran at 3.7 GHz.

If we take Tachyum’s die photo rendering and assume it occupies 500 mm2, a single Prodigy core takes well under 3 mm2, bringing hotspot issues into question

Hotspot issues have to be considered as well. AMD’s Zen 3 can clock a hair above 5 GHz, but faces cooling challenges on low threaded loads because their low core area means very high thermal density. Tachyum expects Prodigy to occupy less than 500 mm2. Die floorplan renderings published by Tachyum suggest each core takes less than 3 mm2. A Zen 3 core’s area is around 3.78 mm2 including the L2. A Prodigy core might be less complex in some areas, like the branch predictor, but it’s also more complex in others (like the vector units). I think hotspot issues will be quite likely when cores are pushed to 5.7 GHz.

As a final note, one way of considering how practical a strategy is, is seeing how often other companies settle on the same strategy. If taking a 8-wide core with 1024-bit vector units above 5 GHz was achievable for a small startup, then AMD, ARM, and Intel must have been goofing off for the past decade. Oh, and throw Nvidia into that pile too – their Kepler, Maxwell, and Pascal architectures had 32-wide FP32 ALUs, which is basically 1024-bit. Or maybe, it’s really hard to get a wide architecture to clock that high and it’s unlikely that a small startup can get there. I’m not saying 5.7 GHz is impossible for Prodigy, as AMD’s Zen 4 apparently reaches 5.85 GHz. Maybe TSMC’s 5 nm process is that magical. But achieving that kind of clock speed with giant vector units, high core count, and a relatively short pipeline looks like a bridge too far. So let’s look at how competitive Prodigy would be if it fails to hit its clock target.

HPC and AI

Even without high clocks, Prodigy has plenty of throughput thanks to giant vector units. Its floating point number crunching power is firmly in GPU territory, even at 3 GHz. Competing CPUs aren’t even in the same ballpark.

*Assumes Golden Cove gets 2×512-bit vector units in Sapphire Rapids

Funny enough, running at lower clocks also gives Prodigy a more balanced compute throughput to memory bandwidth ratio. At 5.7 GHz, Prodigy needed grab bag of tricks to reduce memory bandwidth bottlenecks. At 3 GHz, it’s still compute heavy relative to its memory bandwidth. But the ratio is less lopsided.

*Assuming SPR is using DDR5-5200

Other CPUs have more bandwidth per FLOP, but that’s mostly because they have much lower throughput. GPUs (and A64FX) owe their favorable bandwidth to compute ratio to tightly integrated memory subsystems with limited capacity. Like other server chips, Prodigy can be equipped with hundreds of gigabytes of DRAM. GPUs generally can’t.

So, Prodigy has a very good chance of being a competitive HPC or AI chip, even if it misses its clock target. Barring any show stopping flaws, throughput-bound HPC and AI applications can benefit from Prodigy’s vector units. Prodigy’s biggest weaknesses, like the software ecosystem, are less relevant because researchers and AI folks often develop for specialized systems anyway. HPC and AI code should also be regular enough that Prodigy’s weaker branch predictor won’t hold it back.

Server

Server workloads are more complicated. Prodigy has a weaker branch predictor and lower cache cache capacity than competing server chips. Without high clocks, Prodigy’s per core performance may struggle to compete. This isn’t necessarily a huge problem – ARM’s entry into the server space shows there’s room for high core count chips, even if per-core performance is not competitive (it just has to be good enough).

But there are other factors behind ARM’s foothold on the server market. ARM’s cores narrowly target low power and high density. Unlike Intel and AMD, they don’t try to cover a wide range of power and performance targets. That specialization let ARM create higher core count chips that suited cloud applications, while staying within acceptable power and cost targets. Part of that specialization involves sacrificing vector throughput and peak performance by using smaller vector units and dense designs that can’t hit high clock speeds. Prodigy has bigger vector units and higher clocks than any x86 chip, so there’s a fair chance it won’t scale down to low power quite as well as ARM cores can.

If Prodigy doesn’t hit those high clocks, I don’t see a clear way for them to grab part of the server market. They’re unlikely to outdo ARM in the high density market. Without a massive clock speed advantage, they’re unlikely to beat x86 cores in low threaded workloads. And no one’s sitting still while Tachyum works on getting Prodigy taped out. AMD is getting Zen 4 based Genoa and Bergamo ready for release. The latter will have 128 Zen 4 cores with a cut down cache setup, matching Prodigy’s core count. Ampere Computing is working on a successor to Altra that could feature more than 128 cores. Prodigy will retain a vector throughput advantage of course, but vector throughput isn’t a deciding factor in the server market like it is for HPC and AI.

Conclusion

Technology trends often go in cycles. Decades ago, servers, client systems, and supercomputers slowly converged to use similar hardware. For example, in the late 2000s, AMD’s hex-core K10 die saw service in client systems as the Phenom X6, and in servers and supercomputers as the Opteron 2435. But over the last decade, the trend has been slowly reversing. Supercomputers often employ GPU acceleration to increase throughput, and there’s increasing divergence between GPU architectures targeting HPC and those targeting client platforms. Ampere and Amazon have made specialized server chips optimized for cloud computing. Intel and AMD are still using the same architectures across all three categories, but even they are customizing chips to suit different markets. For example, Skylake in server form gets extra L2 and vector units tacked onto the core, and uses a mesh interconnect. AMD is planning to release Zen 4 in a second form, named Zen 4c, which trades cache capacity for core count and should better suit cloud computing.

Tachyum’s Prodigy represents a brave attempt to buck this trend. It combines a GPU’s vector throughput with a CPU’s per-thread performance, at the cost of high power consumption. However, we are still skeptical of how Tachyum can achieve all this with all the hurdles ahead of them. We did ask Tachyum about how they are achieving their CPU in 500mm2 and while we can’t disclose what they told us, we are still very skeptical of them achieving this on N5 due to not only having massive vector units but also having a large amount of analog circuits due to the large amount of DDR5 and PCIe 5 PHYs on the die.

Even if Prodigy hits the market as planned, it’s going to face stiff competition established players and their specialized products. Servicing different market segments with a single architecture will let Tachyum broaden their reach with the limited engineering resources they have. But that strategy doesn’t have many advantages beyond focusing engineering effort. You can’t really have a server do double duty as a HPC node just because both use the same chips. A supercomputing cluster has extremely high speed networking and distributed storage so nodes can work together on the same problem. A datacenter won’t have the same high speed networking, because responding to internet requests doesn’t require nearly as much bandwidth. Finally, Tachyum will face an uphill battle to get the software ecosystem around their ISA built up, while suffering binary translation penalties on the way. It’s a lot to handle for a small startup, and we wish them the best of luck.

Chips and Cheese also paired up with TechTechPotato to cover the architecture in video format too. Featuring both Cheese and Chips.

If you like our articles and journalism and you want to support us in our endeavors then consider heading over to our Patreon or our PayPal if you want to toss a few bucks our way or if you would like to talk with the Chips and Cheese staff and the people behind the scenes then consider joining our Discord.