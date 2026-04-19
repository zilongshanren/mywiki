---
title: 'Comparing Crestmonts: No L3 Hurts'
url: https://chipsandcheese.com/p/comparing-crestmonts-no-l3-hurts
author: Chester Lam
published: '2024-05-21'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

Meteor Lake’s standard E-Cores share a 24 MB L3 cache with the P-Cores, while the LPE-Cores have to make do with just their private 2 MB L2. Caching is critical to performance in modern CPUs because even the latest and greatest DRAM technologies are too slow to directly handle CPU memory traffic. Since Meteor Lake implements Intel’s Crestmont architecture both with and without a L3 cache, it’s a cool opportunity to see what happens if a core sits a bit too close to DRAM.

Slide from Intel’s Tech Tour presentation

Attributing performance losses to certain factors is really hard in modern CPUs because their out-of-order execution engines and deep buffers are designed to tolerate latency. I’ll be using the top-down analysis method, which accounts for this by looking for pipeline slots lost at the CPU’s narrowest point. That’s the rename/allocate stage on nearly all modern CPUs, which handles allocating resources in the out-of-order engine to track an instruction. Slots lost at the narrowest stage can’t be compensated for by racing ahead later.

A CPU’s frontend is responsible for supplying the renamer with instructions. Slots lost because the frontend didn’t fill them are considered frontend bound. Conversely, if the renamer couldn’t send operations downstream because a required backend resource was exhausted, those slots are considered backend bound. The renamer can also lose throughput to other reasons like allocation restrictions, but those are less common. Finally, instructions can pass through the rename stage and never have their results committed. Those are considered losses due to bad speculation.

libx264 Video Encoding

libx264 is a software video encoder. Crestmont is generally backend bound in this workload, meaning it loses a lot of potential throughput because the core can’t clear out instructions fast enough.

Backend stalls happen when any register file or queue doesn’t have a free entry required by an incoming instruction. Crestmont’s load buffer is a particularly hot resource, suggesting libx264 has sequences where a lot of instructions read from memory and pile up waiting for something ahead of them to complete. The reorder buffer also fills up a lot, so the core is trying to hide a lot of latency. Next in line are the schedulers, which fill when many in-flight instructions are dependent on stalled ones.

Bigger buffers and scheduler would definitely help, but we should also look at where the latency is coming from. Crestmont’s L2 cache latency isn’t the best, but a modern out-of-order core can easily hide a couple dozen cycles of latency. Both Crestmont variants cope well with L2 latency, spending just 2-4% of cycles stalled waiting for data from L2. Meteor Lake’s high L3 latency is a bit tougher on Crestmont, which has less reordering capacity than its P-Core companions. But 6.31% still isn’t bad.

DRAM latency though is absolutely brutal. Data takes hundreds of cycles to arrive from DRAM, and Crestmont has no hope of hiding that sort of latency. Even the Redwood Cove P-Cores can only make it hurt less. Last level cache misses account for the majority of L1D miss related stalls, with low power Crestmont suffering far more than its E-Core counterpart.

To emphasize how harsh DRAM latency is, standard Crestmont saw just 0.1% of instructions load data from DRAM. Yet those 0.1% of instructions made the core stall for over 26% of cycles. Low power Crestmont suffered 2.6x more DRAM accesses per instruction, and spent 44% of cycles stalled waiting for data from DRAM. It’s a good example of how a small minority of very high latency instructions can end up heavily impacting performance.

Low power Crestmont averaged 1.17 IPC here compared to standard Crestmont’s 1.55 IPC. Meteor Lake’s L3 cache may not be the biggest or fastest around, but even a mediocre L3 is miles better than nothing at all. Despite using the same core architecture, Meteor Lake’s E-Cores achieved over 30% better IPC than the LPE-Cores. It’s a great demonstration of how important caching is for modern CPUs.

Linux Kernel Compile

Code compilation can demand a lot of CPU power, especially with parallel builds on large projects. Here I’m compiling the Linux kernel using the minimal “tinyconfig” configuration. Crestmont is still backend bound in this workload, but the frontend is now front and center in the top-down view. Compilation also sees losses from bad speculation.

Performance counters show losses to both frontend latency and bandwidth. Intel classifies instruction cache misses, branch detects, and branch resteers as latency bound. All other reasons are considered bandwidth bound.

Frontend bandwidth limitations primarily come from decoders not working efficiently. Crestmont relies on even load balancing between its two decode clusters. If one cluster gets too much work, the frontend can behave more like a 3-wide one than a 6-wide one. Crestmont usually switches decode clusters at taken branch boundaries, though the branch predictor can insert toggle points to load balance large basic blocks. Perhaps code compilation has a lot of taken branches at just the wrong intervals. Even if load balancing is good, taken branches reduce decoder throughput because decode slots after a taken branch are wasted. 21.5% of executed instructions were branches in this compilation workload, compared to just 6.1% in libx264.

Lots of branches cause frontend latency issues too. The branch predictor sometimes has to find branch targets from its larger but slower BTB levels. And sometimes, the decoders find a taken branch that the predictor wasn’t even tracking. Crestmont could benefit from a bigger BTB.

But instruction cache misses are really the elephant in the room. They’re bad on standard Crestmont, and devastating on the low power variant.

Regular Crestmont can mostly hide L2 and L3 instruction fetch latency, likely because its branch predictor can run far enough ahead of the fetch stage to exploit memory level parallelism. L3 seems to catch just about everything, because stalls due to DRAM latency are rare. Low power Crestmont isn’t so lucky. Without an L3, the core finds itself starved as instruction bytes slowly make their way from LPDDR5. The frontend spnds 12.46% of cycles doing nothing, compared to just 1.07% on regular Crestmont.

When the frontend is able to get instructions into the core fast enough, Crestmont’s backend sometimes struggles to process them fast enough. The core loses 21-23% of potential throughput this way, depending on Crestmont variant. Crestmont’s backend resources are well distributed for this workload, with reorder buffer capacity accounting for most backend related stalls. The reorder buffer filling often further suggests code compilation has plenty of instruction level parallelism available. If a lot of instructions were dependent, we’d see the schedulers fill first.

Memory loads tend to be the most common long latency instructions. Low power Crestmont again hits DRAM more and suffers. But regular Crestmont takes delays from L2 and L3 latency, so low power Crestmont only ends up stalling a bit more.

libx264 is pretty easy to understand. Instructions wanted data that had to be fetched from DRAM, forcing low power Crestmont to stall often. But kernel compilation is a good reminder that a core can stall from the other side too. Instructions themselves have to be fetched from memory, and if cache misses force the core to pull them from DRAM, it’ll probably spend a lot of time waiting to find out what to do.

A CPU’s frontend uses different coping mechanisms to deal with latency, but again there’s no getting around hundreds of cycles of latency. Regular Crestmont achieved 28.5% higher IPC using the same core architecture, again demonstrating how important caching is.

Counterexample: 7-Zip Compression

7-Zip is a free and very efficient compression program. Here I’m using it to compress a huge 2.67 GB ETL trace. 7-Zip is primarily backend bound, with bad speculation adding insult to injury. If we look past bad speculation losses, the frontend mostly does well because 7-Zip has a small instruction footprint and fits within the L1 instruction cache.

Practically all of the bad speculation losses come from branch mispredicts. Crestmont can also suffer wasted work if it has to handle memory ordering violations or guesses that a load is independent of a prior store, but the accesses end up overlapping.

That’s why CPU makers put a lot of effort into branch predictors. Crestmont’s branch predictor might not match the ones in Intel and AMD’s best high performance cores, but it’s a huge step away from the low power branch predictors found in early Atoms. Prediction accuracy in 7-Zip is decent at 95.42%, and only a bit worse than in libx264 and Linux kernel compilation.

But even an ok-ish prediction rate can be problematic if a workload has a ton of branches. 7-Zip has exactly that problem, with branches accounting for over 17% of the instruction stream. 95.42% may get you an A in class, but you probably don’t feel too great about screwing up a pile of exam questions on the way there. Similarly, Crestmont mispredicted a lot of branches and lost a lot of work to bad speculation.

Mispredicts per instruction is a better way to quantify the impact of branch mispredicts, because it takes into account how often mispredicts happen

Crestmont’s backend struggles in 7-Zip, with schedulers filling up often. Performance events can’t indicate which scheduler is filling up, but 7-Zip has almost no floating point or vector instructions. Therefore, the distributed integer schedulers are a clear culprit. A lot of 7-Zip instructions are waiting for a dependency and instruction level parallelism is hard to find, unlike with code compilation.

Unlike code compilation and video encoding, both Crestmont variants feel similar levels of pain from cache misses.

That’s because L1D hitrates are high, and most L1D misses are caught by the 2 MB L2. Anything that misses L2 likely has very poor temporal/spatial locality, and Meteor Lake’s L3 struggles to deal with them. The large 24 MB L3 only achieves 35% hitrate.

With L3 playing a minor role, regular Crestmont has just a 10.2% IPC advantage over its regular variant. 7-Zip is more heavily affected by core factors like branch prediction and probably instruction execution latency. Still, a 10% difference is enough for many reviewers to call winners and losers among competing products. The actual performance difference is more than 10% too, because low power Crestmont runs at lower clocks. If Intel tried to clock Crestmont higher without a L3, performance wouldn’t scale as DRAM accesses start costing more clock cycles.

Final Words

LPDDR5 is an amazing memory technology and gives mobile devices access to high bandwidth at low power. However, DRAM latency has always been high and memory technologies show no sign of fixing that any time soon. LPDDR technologies tend to suffer even worse latency than their non-LP counterparts. Even if a CPU only has to serve a small percentage of accesses from DRAM, those accesses end up causing a disproportionate amount of lost throughput.

Meteor Lake’s low power Crestmont cores show just how painful LPDDR5 latency can be. The core’s backend can fill up as instructions wait for data to arrive from DRAM. Or, the core can sit around waiting for the instructions themselves to arrive from DRAM. Meteor Lake’s regular E-Cores can enjoy much better performance per clock than the LPE-Cores, thanks to a large L3 cache that insulates them from LPDDR5.

Slide from Intel’s Tech Tour showing E-Cores handling a lot of lightweight tasks

On the other hand, lack of a L3 leaves a lot of LPE-Core potential on the table. Meteor Lake wants to achieve better power efficiency by having LPE-Cores handle a large range of lightweight or background tasks. Crestmont feels like the perfect core for the job. Even though it’s not as beefy as a performance oriented core, it still has a substantial out-of-order execution engine and should be more than capable of handling web browsing or messaging. But Meteor Lake’s LPE-Cores struggle whenever I pin a browser or Discord to them. YouTube playback can drop frames or see lagging audio, and Discord almost intolerably slow. That relegates the LPE-Cores to handling non-critical background tasks as if they were Cortex 5 series little cores, even though the core architecture is more comparable to a Cortex 7 series mid-core.

I wonder if Intel could give low power Crestmont a larger L2 cache, or even drop some blocks on Meteor Lake’s SoC tile to make room for a system level cache. The increased performance could let the LPE-Cores handle a lot more tasks without waking up the CPU tile, and help realize the power saving potential in Intel’s aggressive hybrid core strategy.

If you like our articles and journalism, and you want to support us in our endeavors, then consider heading over to our Patreon or our PayPal if you want to toss a few bucks our way. If you would like to talk with the Chips and Cheese staff and the people behind the scenes, then consider joining our Discord.