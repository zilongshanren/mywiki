---
title: Discussing AMD’s Zen 5 at Hot Chips 2024
url: https://chipsandcheese.com/p/discussing-amds-zen-5-at-hot-chips-2024
author: Chester Lam
published: '2024-09-15'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# Discussing AMD’s Zen 5 at Hot Chips 2024

Hot Chips isn’t just a conference where companies give in-depth presentations on the architectures behind high performance chips. It’s also a place to talk to the engineers who worked on those products on the sidelines, often over coffee and pastries. I had the pleasure of chatting with some AMD folks during Hot Chips 2024 as well as attending AMD’s presentation. I’ll be discussing both, along with observations from testing and details revealed in AMD’s optimization guide for Zen 5.

Zen 5 is, of course, the latest member of AMD’s Zen line. Zen generations have each delivered substantial 1T and 2T performance gains, and Zen 5 wants to carry that forward. The 2T point gets emphasis here. AMD is well aware that Intel is planning to leave SMT out of their upcoming Lunar Lake mobile processor. Zen 5 takes the opposite approach, maintaining SMT support even in mobile products like Strix Point. AMD found that SMT let them maintain maximum 1T performance while enjoying the higher throughput enabled by running two threads in a core for multithreaded workloads. They also found SMT gave them better power efficiency in those multithreaded loads, drawing a clear contrast with Intel’s strategy.

## Frontend

AMD’s presentation starts by going through Zen 5’s pipeline from front to back. A CPU’s frontend brings instructions into the core. Zen 5 has a wider backend with more execution resources, so AMD built a new frontend to keep everything fed. Many frontend components are doubled up.

Branch prediction is the first stage in the frontend, and AMD described branch prediction as an important lever for both performance and power efficiency. Zen 5’s branch predictor gets faster, more accurate, and gets a bigger branch target cache to keep that speed up.

Dual decode clusters came up in sideline discussions. The core only uses one of its decode clusters when running a single thread, regardless of whether the sibling thread is idle or SMT is turned off. From those sideline conversations, apparently the challenge was stitching the out-of-order instructions streams back in-order at the micro-op queue. The micro-op queue is in-order because it has to serve the renamer, and register renaming is an inherently serial process. I asked if having 8-wide decode for a single thread would substantially help IPC. They acknowledged there were some cases where 8-wide decode might have performance benefits, but also noted Zen 5 aims to run a lot of code out of the micro-op cache. I also brought up Intel’s E-Cores, which can use both decode clusters for a single thread. They pointed out that Zen 5 has completely different frequency targets, and I can see their point. Something easy to do on a low performance, 3.8 GHz core like Crestmont might be harder on a high performance 5.7 GHz core like Zen 5.

Zen 5’s op cache was another discussion topic. With 6K entries, it has nominally lower capacity than Zen 4’s 6.75K entry structure. In those side conversations, AMD’s engineers clarified that Zen 5 could cache multiple micro-ops from an instruction in a single op cache entry, while Zen 4 would directly cache micro-ops (putting each in a separate entry). That’s not universally the case, as AMD’s optimization guide says microcoded instructions will limit the op cache to storing four micro-ops per line. And multiple instructions don’t necessarily take multiple entries. Adjacent instructions fused into a single micro-op can be stored in a single entry. Besides better density per entry, AMD optimized op-cache density by increasing associativity and reducing line size. The result as we’ve seen in prior articles is Zen 5 often enjoys better op cache hitrates than Zen 4, even with fewer op cache entries.

Both the fetch+decode and op cache pipelines can be active at the same time, and both feed into the in-order micro-op queue. Zen 4 could use its micro-op queue as a loop buffer, but Zen 5 does not. I asked why the loop buffer was gone in Zen 5 in side conversations. They quickly pointed out that the loop buffer wasn’t deleted. Rather, Zen 5’s frontend was a new design and the loop buffer never got added back. As to why, they said the loop buffer was primarily a power optimization. It could help IPC in some cases, but the primary goal was to let Zen 4 shut off much of the frontend in small loops. Adding any feature has an engineering cost, which has to be balanced against potential benefits. Just as with having dual decode clusters service a single thread, whether the loop buffer was worth engineer time was apparently “no”.

In those conversations, I also got the impression Zen 5’s two fetch pipelines were both active for a single thread. I spent some time trying to design a microbenchmark to verify that, but without success.

One attempt involved carving the test array into a lot of basic blocks by having the first half of the array call into cachelines in the second half. If Zen 5 could fetch those basic blocks in parallel, it should have an instruction bandwidth advantage over Zen 4. Evidently that happens to some degree when code fits in the micro-op cache.

But with larger test sizes, Zen 5 rapidly loses its advantage. As the test spills into L3, Zen 4 manages better instruction fetch bandwidth for both 1T and 2T modes. I’m really not sure what’s going on here.

Besides the fancy dual pipe stuff, Zen 5’s frontend has room for improvement with the basics. Since Zen 3, AMD has done well in achieving zero-bubble prediction for the most common direct branches. However, calls, returns, and indirect branches with changing targets still incur penalties in the frontend. When I asked about that, they said getting targets from the return stack was harder, and that getting an indirect branch’s target is more complicated. I can understand the latter – picking between several targets adds another layer of difficulty. But popping a target off the return stack seems pretty simple from my outsider view. In any case, I think Zen 5’s frontend has ample room for improvement.

## Integer Execution

Zen 5’s backend has unified schedulers for ALU and AGU pipes. AMD said symmetry in the integer execution units streamlines instruction pick from the unified schedulers and enables age-order picks throughput. That means if multiple micro-ops become ready to execute, the scheduler will pick the ones that have been waiting the longest. Doing such age-order picks can be better than a random scheduling policy if multiple micro-ops are ready. But it does require age-aware schedulers, increasing complexity.

Choosing the oldest instruction first is a known good heuristic as it is more likely that an older instruction blocks execution of later dependent operations


Qualcomm also presented their Oryon core at Hot Chips 2024, so we wound up seeing two companies advocate for different scheduler layouts in the same conference. In a separate question and answer session, Qualcomm’s Gerard Williams said a distributed scheduler made age-order picks easier. I asked about how much difference he expected age-order picks to make versus a random scheduling policy. While he didn’t directly answer the question, he did say that as a scheduler setup gets more distributed, it gets closer to oldest-first. I think he means a more distributed scheduler tends to perform closer to an age-aware one, even if the individual scheduling queues aren’t age-aware. It makes sense because splitting entries across more scheduling queues reduces the number of entries in each queue, in turn reducing the probability that multiple micro-ops suddenly become ready in one queue. Then, it’s less important which micro-op you pick.

In contrast, AMD in an [earlier interview](https://chipsandcheese.com/2024/07/15/a-video-interview-with-mike-clark-chief-architect-of-zen-at-amd/) with Cheese noted a unified scheduler could avoid “false” delays where several micro-ops become ready on one scheduling queue, but have to wait in line for that queue’s ALU port while other ALU ports on other scheduling queues potentially sit idle. From an outsider’s perspective, it’s hard to tell which method has more merit.

There’s also a question of how much it matters. Zen 5 does seem a bit less core bound than Zen 4. However, backend memory latency and frontend latency tend to be far more significant limiters than instruction execution within the core.

## Floating Point and Vector

Zen 5’s FP/vector unit has received substantial upgrades. I made a mistake in prior Zen 5 articles because I didn’t have enough independent dependency chains in my vector integer throughput test to saturate all four vector ALUs. From further testing, Zen 5 indeed has 4×512-bit vector integer execution.

Another discussion came up around two cycle latency for vector integer adds, mostly from [Mysticial (Alex) from numberworld.org](https://x.com/mysticial). Prior Zen cores could do vector integer adds with single cycle latency. AMD clarified that vector ALU operations could have single cycle latency in certain cases, specifically if the operation was woken up by a long latency instruction like a load from memory. AMD also published guidance in their instruction latency spreadsheet clarifying the situation.

The floating point schedulers have a slow region, in the oldest entries of the scheduler and only when the scheduler is full. If an operation is in the slow region and it is dependent on a 1-cycle latency operation, it will see a 1 cycle latency penalty.


There is no penalty for operations in the slow region that depend on longer latency operations or loads.Zen 5 Instruction Latencies Spreadsheet, Version 1-00


Delaying older operations feels like a weird move. Age-order picks aim to minimize latency for the oldest instructions, in order to unblock dependent ones faster. The slow region in Zen 5’s floating point schedulers would increase latency for the oldest instructions, possibly causing delays down critical dependency chains. A workload bottlenecked on execution latency would fill the scheduler, triggering the 1 cycle latency penalty.

Again there’s a question of how much this matters. I suspect it’s not a huge deal because Zen 5 isn’t particularly core bound. I did find it interesting that the two cycle latency measured from a simple microbenchmark was caused by a slow portion in the FP scheduler. That means AMD didn’t have to add a pipeline stage in the vector ALUs or vector register file read path, despite widening both to 512 bits.

## Load/Store

AMD is proud that the L1 data cache has a 50% capacity and associativity increase while maintaining a 4-cycle load-to-use latency. L2 associativity has gone up too, which should improve L2 hitrate even without a capacity change. The load/store unit within the core can keep more memory operations in-flight, thanks to larger load and store queues. Microbenchmarks indicate the core can have about 202 loads in-flight, which I previously gave as the load queue size. AMD has since published an optimization guide saying the load/store unit “can track up to 64 uncompleted loads and has no specific limit on the number of completed loads”. Since I was measuring with completed loads, my attempt to measure load queue capacity earlier likely ran into integer register file capacity limits.

The store queue has 104 entries, but a 512-bit store takes two entries just as in Zen 4. I asked about this, and AMD again felt expanding the store queue to have 512-bit wide entries would be too expensive. They said the store queue has to act a bit like a register file, because a load may need to read forwarded data from any entry in the store queue. At the same time, the retirement stage may need to read from the store queue too, in order to write store data to the cache hierarchy.

As we’ve covered before, AMD has dramatically increased L1 and L2 cache bandwidth. The L1 can service two 512-bit loads and a 512-bit store per cycle. Datapaths between L1 and L2 have been widened to 512-bits too. AMD says that’s great for HPC and AI workloads. And in a predictable move, Zen 5 has improved data prefetchers too.

While not covered in the presentation, AMD’s optimization guide indicates the load/store unit can track up to 124 outstanding L1 misses. That’s a massive increase in memory level parallelism available to a single core. For comparison, Zen 4 and Zen 3 could track 24 outstanding L1 misses. Zen 2 and Zen 1 could track 22.

Zen 5’s L3 cache has the same capacity and layout as Zen 4’s and Zen 3’s. However, AMD has managed to decrease L3 latency by 3.5 cycles. L3 latencies had been trending up as CPU makers add more pipeline stages to go after higher clock speeds, so it’s great to see L3 latency drop a bit in Zen 5.

AMD also talked about creating building blocks that can be assembled into different configurations while maintaining low latency. Core complexes and chiplets are of course a high level building block, but AMD wants to emphasize their flexibility within a core complex too. Zen 5 can scale cache capacity and core count to meet different area, performance, and power targets. Of course, that could be done with prior Zen generations too.

## Zen 5’s Performance, and SPEC2017

All of Zen 5’s changes combine to provide a substantial IPC uplift. AMD broke down contributing factors towards that IPC uplift, and noted that workloads with larger code footprints provide a larger percentage of gains.

Across a range of actual applications, AMD found that Zen 5 gave a 16% average performance per clock uplift. From endnotes, this was tested with a Ryzen 9 9950X and Ryzen 7 7700X both running at 4 GHz, fed by DDR5-6000.

Since AMD mentioned SPEC2017, I went about doing a SPEC2017 run on both a Ryzen 9 9950X sampled by AMD and my personal Ryzen 9 7950X3D. Cheese set the Ryzen 9 9950X up with DDR5-6000, while my personal system has DDR5-5600. Clock speeds were not fixed, so this isn’t a strict performance per clock comparison. I used GCC 14.2 with `-O3`

, `-mcpu=native`

, and `-fomit-frame-pointer`

flags. Compiler differences mean my results aren’t comparable to AMD’s. Scores are marked as estimates because they weren’t submitted to SPEC’s site. Submitting scores is a pretty involved process, and as Anandtech has noted, is quite over the top for a hardware enthusiast site.

With SPEC CPU2017’s integer rate test run with a single copy, the Zen 5 based Ryzen 9 9950X enjoys a 13.3% performance gain over the Zen 4 based Ryzen 9 7950X3D. Curiously, both the VCache and non-VCache cores on the 7950X3D turned in identical scores. But the same score doesn’t mean the cores have similar performance, because individual integer workloads show substantial differences between the two. Sometimes higher clock speed wins, but sometimes the extra IPC enabled by a 96 MB L3 turns out to be more important.

With similar last level cache capacity, Zen 5 generally stays ahead of Zen 4. Still, Zen 4 can surprisingly keep pace in certain workloads like 531.deepsjeng. A few other workloads give Zen 5 gains in the low single digit percentage range, showing the folly of relying on an overall IPC or performance uplift figure. The same applies when comparing Zen 5 against a VCache-enabled Zen 4 core. Again Zen 5 often comes out ahead, but swings get wilder in both directions. Zen 5 sees a massive 50% gain over VCache Zen 4 in 548.exchange2, but loses by 10.6% in 520.omnetpp.

Zen 5 does much better in SPEC CPU2017’s floating point workloads with a 29.4% or 55.9% gain over non-VCache and VCache-enabled Zen 4, respectively.

Again Zen 5’s lead varies depending on which workload you look at. But this time, Zen 5 holds a lead across all floating point subtests against both Zen 4 variants.

To me, the floating point results show the strength of Zen 5’s floating point and vector unit. Zen 5’s huge FP/vector register file, increased scheduling capacity, and larger non-scheduling queue placed before rename combine to let it shine in SPEC CPU2017’s floating point workloads. Zen 5 improves on the integer side too, though gains there aren’t so gigantic. That’s possibly because the integer register file only saw a small capacity increase, and increasing ALU port count runs into very diminishing returns because Zen 4 wasn’t particularly core-bound with only four ALU ports.

## Closing Remarks

Personally, Hot Chips 2024 was a lot of fun. A large part of that fun is being able to talk to engineers who worked on the hardware I poked around with before. Zen 5 is one of those. I’d like to thank AMD for giving a nice presentation at Hot Chips, and all of the incredible people who worked on Zen 5 for giving us insight into the motivations behind various CPU design choices.

If you like our articles and journalism, and you want to support us in our endeavors, then consider heading over to our [Patreon](https://www.patreon.com/ChipsandCheese) or our [PayPal](https://www.paypal.com/donate/?hosted_button_id=4EMPH66SBGVSQ) if you want to toss a few bucks our way. If you would like to talk with the Chips and Cheese staff and the people behind the scenes, then consider joining our [Discord](https://discord.gg/TwVnRhxgY2).