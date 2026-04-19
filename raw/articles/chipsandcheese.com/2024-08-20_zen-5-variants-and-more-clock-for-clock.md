---
title: Zen 5 Variants and More, Clock for Clock
url: https://chipsandcheese.com/p/zen-5-variants-and-more-clock-for-clock
author: Chester Lam
published: '2024-08-20'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

Zen 5 is AMD’s newest core architecture. Just a few weeks after launch, Zen 5 has already hit the market with several different cache, clock speed, and AVX-512 configurations. Here, I’m comparing Zen 5 variants along with a pile of older cores with clock speed taken out of the equation as much as possible. That means capping clock speeds on all CPUs to that of the lowest clocking chip. In this case, that’s the 3 GHz Athlon II X2 651.

One of the tested chips

Of course, other CPUs are designed with different clock speeds in mind, with their architecture optimized to deliver the best performance at those clocks. You might be asking if there’s a point to any of this from a performance perspective. The answer is no. But a better question is whether it’s fun, and in my opinion, the answer is yes. That’s because lowering clock speeds reduces the impact of memory latency. For example, 70 ns of DRAM latency is nearly 400 cycles at 5.7 GHz, but only 210 cycles at 3 GHz. Memory latency can be a huge factor in why CPUs only utilize a fraction of their core width.

Capping clock speeds to 3.5 or 4 GHz didn’t make a big difference, likely because thermal throttling prevented the four Redwood Cove cores from consistently getting to 4 GHz

Intel’s Redwood Cove (Meteor Lake’s P-Core) is one example. It’s fed by LPDDR5, which has very high latency for a client platform. IPC increases by 25.8% when dropping maximum clock speeds from 4 GHz to 1 GHz. Performance counters indicate the core loses less pipeline slots to waiting on incomplete loads (backend memory bound) as clock speeds decrease.

Tested Configurations

All CPUs were capped at 3 GHz using cpupower frequency-set --max 3000mhz. While this usually ensures the CPU runs at about 3 GHz, that’s not always the case. Depending on multiplier configuration, cores can over or undershoot that frequency target. Sometimes the error can be quite significant. Bulldozer is one example, because the two closest P-States gave 2.7 and 3.3 GHz, and cpupower used the former. Zen 2 appears to be another example.

Tests were run with affinity set to four logical cores. In CPUs with SMT or CMT capability, I used one thread per physical core. I ran three workloads, namely video encoding, file compression, and code compilation. Running tests across many systems unfortunately takes too much time, and sorting through performance metrics wouldn’t be practical if I tried to run more. Code compilation was also too much of a stretch goal, as small methodology differences could result in large differences in executed instruction counts. Therefore, performance figures for code compilation will be omitted.

Performance with 3 GHz Cap

Software video encoding with libx264 provides better quality and space tradeoffs than hardware video encoders, at the cost of being more computationally expensive. Desktop Zen 5 takes a healthy 20.8% lead over Zen 4 in the most comparable configuration. VCache gives Zen 4 96 MB of L3 cache. That shrinks Zen 5’s lead to a still significant 16.6%. With clock speeds artificially capped at 3 GHz, Zen 4 with VCache takes a lead over its vanilla counterpart. Without clock speed caps, the higher clocking Zen 4 die wins.

Mobile Zen 5 doesn’t enjoy the same lead, and performs very closely to desktop Zen 4. In its mobile variant, Zen 5 has a weaker AVX-512 implementation, less cache, and higher memory latency. Still, it’s able to stand even with Zen 4 despite those handicaps. Of course desktop Zen 4 will likely take the lead at stock speeds, but it’s cool to see how Zen 5’s architectural improvements can nullify the drawbacks of a mobile memory subsystem at 3 GHz.

Meteor lake’s E-Cores turn in a somewhat disappointing performance, and fail to enter Zen 2 or Skylake’s performance bracket. Intel slightly upgraded Crestmont’s FP/vector unit by increasing scheduler sizes compared to Gracemont, but the FP/vector unit remains weak overall compared to Zen 2 and Skylake’s. Further down the graph, Bulldozer shows off its large FP/vector unit for the time, comfortably moving past AMD’s Husky architecture.

7-Zip is a file compression program. I’m manually setting thread count to 16 and using the 24.08 binary downloaded from 7-zip.org, and compressing a 2.67 GB file. Previously, I saw the Ryzen 9 9950X easily overtaking my 7950X3D in this workload, but that was likely because the 9950X averaged higher clock speeds. With matched clock speeds, desktop Zen 5 is bracketed by Zen 4’s desktop variants. Mobile Zen 5 suffers and is no longer able to keep pace with desktop Zen 4, suggesting 7-Zip is sensitive to memory latency and cache capacity.

Further down thee graph, Intel’s Redwood Cove and AMD’s density optimized Zen 5c cores are closely matched. Skylake and Zen 2 are also neck and neck. At the bottom, the more modern Bulldozer architecture sees the Husky cores slip by. It’s funny to see because the Husky architecture traces its lineage back to the first Athlons of 1999.

For code compilation, I’m compiling the Linux kernel at commit hash 5189dafa4cf950e675f02ee04b577dfbbad0d9b1 with the tinyconfig configuration and 16 parallel jobs.

Instructions Per Cycle

CPUs provide performance monitoring events, and all of the tested cores provide comparable events for retired instructions and cycles not in halt. Dividing the former by the latter gives us IPC, or average instructions per cycle. libx264 is a moderately high IPC workload, with Zen 5 able to average over 2 IPC. Older cores still do well. Even the oldest core tested here can average over 1 IPC. Strangely, Zen 2 reports higher IPC than Skylake. Approximating clock speed by dividing cycles not in halt by 4 * runtime suggests it’s running at closer to 2.8 GHz than 3 GHz.

Desktop Zen 5 is a clear winner as expected. Intel’s Redwood Cove has very similar IPC to mobile Zen 5 and Zen 4. But unlike the Zen 2 situation, that’s not due to slight clock speed deviations. Instead, it’s because executed instruction counts differ by a non-trivial amount. In online discussions, IPC is often used as a synonym for performance per clock. But IPC doesn’t always approximate performance per clock to an acceptable degree, because a large enough difference in executed instructions can lead to a higher IPC core providing worse per-clock performance.

AMD’s slide showing instruction set support up to Zen 2

libx264 is a fun benchmark because its been around for a while and optimized for different levels of ISA extensions. Retired instruction counts fall into several bands depending on ISA extension support. Zen 4 and Zen 5 get an AVX-512 code path, letting them get the job done with fewer instructions. Skylake, Zen 2, and Meteor Lake use a AVX2 code path, which does a less efficient job of representing libx264’s work.

Bulldozer supports AVX but not AVX2, and has a few deprecated extensions (XOP, FMA4) that libx264 has code paths for. That level of ISA extension support isn’t as great as AVX2, but is a remarkable improvement over Husky’s SSE path.

With file compression, IPC closely approximates performance per clock. All CPUs here took about 1.69 trillion instructions to finish compressing the test file. Compared to libx264, 7-Zip is a lower IPC workload. Curiously, older cores like Bulldozer and Husky see a smaller IPC difference compared to newer cores like Zen 5. That’s not to say Bulldozer and Husky do well, since they both struggle and fail to average even 1 IPC.

Among Intel’s architectures, Redwood Cove only has a small lead over Skylake despite being a much bigger core. Wider cores with more reordering capacity really aren’t favored in this workload.

Code compilation is another example where executed instructions counts are largely even. There was some variation, possibly because code generation went down different paths depending on the level of ISA support, but the highest executed instruction count was 0.77 trillion, while the lowest was 0.75 trillion. It’s another case where you could say IPC while referring to performance per clock, and not be off by much.

Code compilation sees newer cores show their value again. Zen 5 outpaces Zen 4. Redwood Cove is comfortably ahead of Skylake. Crestmont also performs where Intel wants it to be, staying competitive with Skylake for performance per clock. The only exception is Bulldozer. Its more modern architecture doesn’t do much, and Husky is ahead.

While going over results, dgb was able to set up a tinyconfig kernel compilation run with the same commit hash. With a chroot Debian install, his run finished the job with 0.69 trillion instructions, with correspondingly better results. We weren’t able to get to the bottom of the difference, as methodology was largely the same except for dgb using Debian via chroot instead of a normal install. IPC results however were similar.

Branch Prediction

Performance monitoring events are closely tied to a core’s architecture, making it hard to find similar events across different cores. Besides instructions retired and unhalted cycles, retired branches and retired mispredicted branches have remained a constant in performance monitoring events through the ages. Examining those events is interesting because AMD and Intel have both put a lot of effort into improving branch prediction.

libx264’s branches aren’t completely trivial to predict, but the workload has fewer branches than code compilation or file compression. Newer CPUs tend to achieve similar accuracy, while the very old FX-8150 and Athlon II X4 651 are far behind. Bulldozer does show off its more advanced branch predictor though.

Mispredicts per instruction can quantify the impact of mispredicted branches, since it normalizes for how often branches occur in the instruction stream. Zen 2 and Redwood Cove suffer the least from mispredicted branches, since they have a decent branch predictor and have to execute more instructions to do the same work. Most of those extra instructions appear to deal with computation rather than control flow, so branches and mispredicted branches become less of a factor. The same doesn’t apply to Bulldozer and Husky. Even though their level of ISA extension support means they get the least efficient representation of work, their old branch predictors are just really bad.

File compression tends to really stress branch predictors. Prediction accuracy is still decent in an absolute sense, at over 95% in AMD and Intel’s newest cores. Zen 5 even manages to push accuracy to 96%. But over 22% of executed instructions are branches, so even 96% accuracy means the core will frequently run into a mispredicted branch. In contrast, only 6.7% of libx264’s instruction stream consists of branches on Zen 4. On Husky, that figure drops to 5.1%.

Despite Zen 5’s impressive prediction accuracy, the core still sees 8.9 branch MPKI. Zen 4 is a bit worse off at 9.3 MPKI. I suspect that’s part of why Zen 5 failed to pull a significant clock for clock lead in 7-Zip compression. 7-Zip is sensitive to cache and memory latency, as we saw with mobile Zen 5 falling well behind desktop Zen 5 and Zen 4. Out-of-order execution engines can mitigate latency by keeping more instructions in flight ahead of a long latency load from memory. But that reordering capacity gets wasted if fetched instructions keep getting flushed out due to branch mispredicts. Therefore, Zen 5 can’t make the most of its increased reordering capacity, and cores with better memory subsystems (like Zen 4 with VCache) win out.

I have the same explanation for Skylake and Redwood Cove further down the chart, though of course to a different degree. Redwood Cove’s better predictor reduces mispredicts per instruction by nearly 17.6%, but mispredicts still happen so often in an absolute sense that Redwood Cove’s giant out-of-order engine can’t stretch its legs. As a result, Redwood Cove’s lead over Skylake isn’t particularly impressive for a core that’s several generations newer.

Code compilation has similar branch frequency to file compression, with about 21.7% of the instruction stream being branches. But branches in code compilation appear easier to predict. Every core gets better prediction accuracy than with file compression. Newer branch predictors also show their worth. Zen 5 reduces mispredicts per instruction by 60.2% compared to Bulldozer, while in 7-Zip the improvement was just 33.38%.

That’s probably why newer cores do better in general. Better prediction lets larger out-of-order engines more effectively hide memory latency. The same applies to the instruction side. Newer cores have decoupled branch predictors that can act as long range prefetchers. That’s important because kernel compilation suffers a lot of L1 instruction cache misses, and accurate prefetching is required to hide L2 and L3 latency.

Larger instruction caches can mitigate this problem to some extent. Bulldozer’s 64 KB instruction cache only sees 27.82 MPKI, a 16.3% reduction in misses per instruction compared to Zen 4’s 32 KB L1i. Still, that’s a lot of misses in an absolute sense, and long distance prefetching remains important. If the branch predictor guesses wrong, prefetches will be wrong and the frontend will suffer a long stall with L2 or L3 latency in play.

Lost Pipeline Throughput

Beyond IPC and branch prediction metrics, performance monitoring events start to diverge a lot between cores. But I’m going to make an attempt to characterize how frontend or backend bound these workloads are with the best counters I can find on each architecture. They’ll no longer be directly comparable, but should give a rough general idea.

libx264 is backend bound, and that largely remains the case even when clocks are reduced to 3 GHz. Zen 2 suffers the least, likely because it’s feeding a modest 5-wide pipeline with a fast L3 cache and low latency DDR4 memory. Zen 5 loses more throughput, but that’s because it has a wider pipeline and thus more potential throughput to lose. Zen 5 is still the leader here, but that’s because of its increased reordering capacity and better frontend rather than core width.

VCache on Zen 4 cuts down data-side stalls, but doesn’t do much for the frontend, which wasn’t a huge factor to begin with. On the other hand, mobile Zen 5 becomes very backend bound with a weaker FP/vector unit and mobile memory subsystem. AMD’s old Athlon II X4 651 is even more backend bound, since it has both a weak FP/vector unit and a deficient cache subsystem. Crestmont somehow ends up being even more backend bound, suggesting its FP/vector unit is even weaker relative to the rest of the pipeline.

7-Zip loses plenty of throughput to both backend and frontend bound reasons. Desktop Zen 5 is the most frontend bound. Mobile Zen 5 is a bit less frontend bound, but only because it gets clobbered so hard by less cache and LPDDR5 latency that the frontend matters less.

7-Zip pretty much fits in the micro-op cache on CPUs that have one. Even Skylake’s 1.5K entry micro-op cache provides 93.5% of micro-ops. Zen 4’s 6.75K entry one provides 99.5% of micro-ops, and basically plays the role of the primary instruction cache in this workload. Even so, these modern cores lose a lot of throughput to the frontend not being fast enough. I guess there’s no getting around branchy code. Having wider fetch from the micro-op cache counts for less if there’s a taken branch early in the fetch group, which means subsequent fetch slots are wasted.

Crestmont’s unique out-of-order fetch and decode clusters might get around this to some extent, but it ends up being more backend bound and doesn’t win overall. Bulldozer is also curiously less frontend bound than the rest. That could be because frontend throughput tends to matter less as IPC decreases, and 7-Zip is not a high IPC workload to start with. Bulldozer has the lowest IPC of any core here.

Kernel compilation is a very frontend bound workload, providing a nice contrast to libx264. We ran the same workload on both the Ryzen 9 9950X and Ryzen 7 7950X3D in a prior article. Lowering clock speeds cuts down backend bound cycles, but doesn’t really help the frontend. Again Zen 5 loses the most potential throughput to frontend reasons, despite having arguably the most advanced frontend of all CPUs here. Feeding a 8-wide core is hard when branches are everywhere. Despite not looking so good in this graph, it’s important to remember that Zen 5 outperforms every other core architecture here, even when limited to four cores at 3 GHz.

Zen 2 and Zen 4 get absolutely hammered from the frontend side, likely because this workload seems to give their branch predictors a hard time. That prevents them from effectively prefetching to hide latency for instruction fetches that miss L1i or even L2. Zen 5 is also really frontend bound, but its better branch predictor shines and IPC increases overall. Crestmont, Husky, and Bulldozer have 64 KB L1 instruction caches and turn in a decent performance, though their small backends really suffer and hide any advantage that might bring.

Final Words

Capping a batch of CPUs to 3 GHz was a fun if time consuming exercise. Performance figures at 3 GHz have little relevance to how these CPUs will run on the vast majority of setups. But a deeper look at performance monitoring events shows surprising consistency in the challenges CPUs face even at different clock speeds across many different generations. Branchy code makes it hard for the frontend to feed the core. If you don’t have a lot of branches, cache and memory latency will take care of destroying performance.

What limits computer performance today is predictability, and the two big ones are instruction/branch predictability, and data locality.

CPU architects are no doubt aware of this. They’ve tried to mitigate those predictability challenges with better caching and better predictors. Sometimes it works out reasonably well, as in libx264 and code compilation. File compression is an example of when it doesn’t. Despite 7-Zip fitting within the micro-op cache, which is the fastest form of instruction delivery on many of the modern cores tested here, the workload still loses a lot to frontend bound reasons.

One of the tested chips

It all gets worse when branchy code starts spilling out of various cache levels, as Linux kernel compilation does. While I only dug into additional performance monitoring events on a few cores, I hope AMD will increase the L1 instruction cache’s size later on. Going to 64 KB probably isn’t enough. Apple and Qualcomm have gone for very large 192 KB L1 instruction caches, and with good reason. But even that won’t be enough to contain the instruction footprint on certain workloads.

Data-side latency is a big issue too. Tackling the memory latency problem today is arguably even harder than it was in the early 2010s. Pointer chasing through a 1 GB array with 2 MB pages gives about 76 ns of latency on the Athlon II X4 651. Do the same on the Ryzen AI 9 HX 370, and you’ll see over 128 ns of latency. Even though mobile Zen 5 has more reordering capacity and better caching than Husky, both cores often find themselves very backend bound.

A DDR3 memory module. Have fun waiting for data from this thing. Having fun? LPDDR5 is even more fun.

Despite the difficulty posed by branchy code and memory latency, CPU architects continue to do their best. I’m impressed at how good branch predictors are compared to the ones from a decade ago.

Memory latency and spaghetti code will claim your performance. Resistance is futile.

Revealed to me in a dream

Still, the fundamental limiters for CPU performance have remained the same over the past decade and more. Even giving up some performance by running at lower clock speeds does not let cores escape those challenges. I don’t expect it’ll change soon. I’ll have fun watching engineers try their best to tackle those challenges. It’s like watching a new player learn to play Dark Souls. Tragedy is inevitable. With that in mind, I wish them the best.

If you like our articles and journalism, and you want to support us in our endeavors, then consider heading over to our Patreon or our PayPal if you want to toss a few bucks our way. If you would like to talk with the Chips and Cheese staff and the people behind the scenes, then consider joining our Discord.