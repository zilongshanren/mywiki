---
title: Running SPEC CPU2017 on Chinese CPUs, and More
url: https://chipsandcheese.com/p/running-spec-cpu2017-on-chinese-cpus
author: Chester Lam
published: '2024-10-19'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# Running SPEC CPU2017 on Chinese CPUs, and More

SPEC CPU2017 is an industry standard benchmark suite. OEMs use it to set performance expectations for their systems, and CPU make often use it to tune their designs. We've published some SPEC CPU2017 estimated results, and now it'll be interesting to go back and run SPEC CPU2017 on CPUs we've gone over in prior articles. Chinese CPUs are especially interesting because they're often not tested by more mainstream tech outlets, so it's a good place to start. Some other CPUs were tested to provide comparison data.

Results here are estimated because SPEC CPU2017 has [a long list of requirements](https://www.spec.org/cpu2017/Docs/runrules.html). We've set out to meet all the technical requirements like completing all tests in a suite from one `runcpu`

invocation and using a single file system. Differences primarily come down to documentation requirements. As before, we're using GCC 14.2.0 and running bare metal Linux. GCC 14.2.0 is either compiled from source or run through a Debian chroot if it's not available from the distribution's packages. Optimization flags are set to let the compiler perform a typical level of optimization while targeting the tested CPU's ISA extension. For example, that's `-O3 -march=native -mtune=native -fomit-frame-pointer`

for x86-64, or `-O3 -mcpu=native -fomit-frame-pointer`

for aarch64.

We'll also focus on single threaded performance with SPEC CPU2017 rate tests running a single copy. There's a small exception for evaluating SMT gains, which will be tested with two copies pinned to sibling threads on a single core.

## Loongson 3A6000

Loongson evolved from state sponsored microprocessor research efforts. While it's a separate corporation now, it's run by many of the same people that drove those research efforts at the Chinese Academy of Sciences. It's also funded by grants from the Chinese government. Current Loongson CPUs use a custom loongarch64 instruction set, which is closely related to the MIPS ISA used by older Loongson and Godson cores.

### Loongson 3A6000

The 3A6000 is the most recent Loongson CPU [we've gotten our hands on](https://chipsandcheese.com/p/loongson-3a6000-a-star-among-chinese-cpus). It's a quad core 2.5 GHz part with SMT support. Each of its LA664 cores are 6-wide with 256-bit vector execution and decent out-of-order execution capability. As of October 2024, [Loongson's site](https://www.loongson.cn/EN/product/show?id=11) continues to say the 3A6000 applies to notebooks and desktops. So, the 3A6000 will be compared against notebook and desktop CPUs. High single threaded performance is critical in those client segments because many consumer programs don't scale across a lot of cores. Unfortunately, the 3A6000 does not provide comparable single threaded performance to recent client offerings from AMD and Intel.

Loongson even falls behind against E-Cores, which sacrifice single threaded performance for better density. It's not a great sign because the point of these density optimized cores is to improve multithreaded performance by having a lot of them. Meteor Lake for example has eight Crestmont E-Cores. Loongson's 3A6000 is thus a weak quad core in an era where quad core CPUs are on their way out, even in budget PC builds.

The 3A6000 is generally uncompetitive across SPEC CPU2017’s integer workloads. Only in 520.omnetpp does Loongson get within striking distance of Crestmont, Intel’s outgoing E-Core. Floating point tests have a a couple more examples where Loongson does well. 538.imagick, 521.wrf, and 549.fotonik3d have the 3A6000 beating Crestmont. However, Crestmont manages significant wins in other floating point tests and comes off with a higher overall score.

Loongson makes up some of the difference with SMT support. Running two threads in a core gives every stage of the pipeline more explicit parallelism to work with, and often increases core utilization.

The 3A6000 turns in a decent performance with two copies pinned to a core’s SMT siblings, with over 20% gains. Gains are similar to those in AMD’s Zen 5. Zen 4 sees lower gains on FP subtests, likely because those tend to be core-bound even without a second thread in play.

Even two SMT threads however fail to provide comparable performance to a current generation AMD core running a single thread. Having SMT is better than nothing and Loongson should be commended for pulling off a decent first generation SMT implementation. But 3A6000 continues to be a slow quad core in an era where quad core CPUs are on their way out. SMT doesn’t change that, especially when Intel and AMD’s high performance cores benefit from SMT too.

Running SPEC CPU2017 on the 3A6000 was quite difficult. I had to compile SPEC CPU2017’s toolset from scratch. I also compiled GCC from scratch like with other systems that didn’t have GCC 14.2.0 available from packages, but doing so with all eight hardware threads caused the system to crash. Compilation did finish successfully when pinned to two cores, but took a very long time. After losing some sanity from dealing with the 3A6000, it only made sense to reuse the compiled toolset and compiler on a second system.

### Loongson 3A5000

Loongson’s 3A5000 is the 3A6000’s predecessor. It also runs at 2.5 GHz, but uses the 4-wide, out-of-order LA464 architecture. Loongson’s website describes the 3A5000 as a “general-purpose processor for personal computers, servers, and other IT fields”. The 3A5000’s single threaded performance in SPEC CPU2017 lands between the low power Celeron J4125 and AMD’s old Bulldozer-based FX-8150. Bulldozer beats LA464 by 19.5% and 7.3% in the integer and floating point suites, respectively, putting it about a generation ahead.

Neither 3A5000 or 3A6000 can match Intel’s E-Cores, or even the Skylake architecture from 2015. It’s a disappointing result for a chip [hyped as being competitive with AMD’s first generation Ryzen chips](https://www.techspot.com/news/90544-china-new-loongson-cpu-almost-fast-first-ryzen.html), which hit the market in 2017. Even though the i5-6600K isn’t a top end Skylake part, the 3A5000 struggles to land on the same planet.

Skylake pulls ahead by ridiculous amounts in some high IPC tests like exchange2 and x264. SPEC CPU2017’s floating point suite paints a similar picture.

### IPC, and the Loongarch64 ISA

SPEC CPU2017 is distributed in source code form, so it’s really benchmarking the compiler along with the CPU. Compiler code generation is inherently tied to the targeted ISA, and it’s interesting to see just how Loongson’s Loongarch64 instruction set stacks up against others. Generally, a lower executed instruction count points to the combination of ISA and compiler code generation more efficiently representing the workload. Loongarch64 on average requires more instructions, though in certain cases it can be competitive.

If I take the geometric mean of the difference in instructions executed, x86-64 and aarch64 are surprisingly close, with x86-64 executing ~1.17% more instructions. Loongson executes 10.6% more instructions than x86-64, a minor but still notable difference. In the floating point suite, Loongson requires 11.4% more instructions than x86-64. Interestingly, the geomean of difference in instructions executed for aarch64 and Loongarch64 is nearly the same, with Loongarch64 coming within a percent of aarch64.

549.fotonik3d and 554.roms are outliers, with Loongarch64 taking 77.1% and 78% more instructions than x86-64 to do the same work. Perhaps something is very difficult to represent in Loongarch64. Or, compiler code generation was particularly poor.

Setting instruction set aside, we can look at how well Loongson’s architectures do with the instructions they’re given. Performance monitoring events indicate Loongson’s 3A5000 and 3A6000 compete very well in terms of how many instructions they execute per cycle. However, it doesn’t translate into competitive performance because Loongson executes more instructions to complete the same work, and more importantly, cannot achieve competitive clock speeds.

I provided AMD Zen 1 results here by renting a VM.Standard.E2.4 Oracle cloud instance. Its Zen 1 configuration is unlike any other I tested because the core appears to be permanently locked into 2T mode. A single thread was only able to see half of reorder buffer and register file capacity even when its sibling thread is idle, something I didn’t observe on other cloud offerings. However, Oracle cloud supports performance monitoring events, which some other clouds don’t support. Since I don’t have a Zen 1 chip available, this is the best I can do. But figures from Zen 1 here should be taken with that in mind.

Loongson’s 3A6000 can achieve some very high IPC figures in certain SPEC CPU2017 workloads, which compensates for having to execute more instructions. Still, it’s not enough to compensate for Loongson’s clock speed disadvantage, even against a modestly clocked Skylake part. For example, the Core i5-6600K has a 94% lead against the 3A6000 in 538.imagick, even though the 3A6000 has higher IPC.

### Branch Prediction Accuracy

Branch prediction is a difficult yet highly impactful area for high performance CPU designs. Loongson’s 3A6000 has good branch prediction accuracy, and represents a strong step forward from the 3A5000. Across SPEC CPU2017’s integer suite, the 3A6000 achieves slightly better branch prediction accuracy than Skylake.

SPEC CPU2017’s floating point suite tells a similar story. Overall, Loongson’s 2024 CPU is able to achieve competitive branch prediction accuracy against Intel’s 2015 architecture. It’s far better than the 3A5000, which struggles in a surprising number of floating point workloads.

As an additional bonus, the 3A6000 suffers only a minor loss in branch prediction accuracy when the core is running two SMT threads. That suggests the core has a lot of branch predictor storage, because two threads will have a larger branch footprint.

## Zhaoxin

Zhaoxin grew out of a joint venture between VIA and the Shanghai municipal government. Unlike Loongson, Zhaoxin uses the well supported x86-64 ISA, a benefit inherited from VIA. The Zhaoxin KX-6640MA is a quad core 2.6 GHz part. Its LuiJiaZui cores use a 2-wide out-of-order architecture with low reordering capacity. Performance lands firmly in the low performance, low power segment.

The KX-6640MA is slightly outperformed by Goldmont Plus from Intel’s Atom line. In turn, the KX-6640MA ties or slightly pulls ahead of Arm’s Cortex A73. The A73 is a 2-wide core that boosts its reordering capacity with [a unique out-of-order retirement mechanism](https://chipsandcheese.com/p/cortex-a73s-not-so-infinite-reordering-capacity). Both Cortex A73 and Zhaoxin’s LuiJiaZui comfortably outpace the 2-wide in-order Cortex A55. Even a small out-of-order engine has a huge advantage over in-order execution.

A score breakdown shows Goldmont Plus often outperforming LuiJiaZui, courtesy of having a larger out-of-order engine. Cortex A73 has more reordering capacity than LuiJiaZui, even excluding Arm’s out-of-order retirement mechanism. However, Zhaoxin’s higher clock speed lets it come out ahead. The opposite is true in SPEC CPU2017’s floating point suite. There, Cortex A73 performs very well and often comes out ahead of Zhaoxin.

## Final Words

Compared to the workloads tested in our prior Loongson articles, SPEC CPU2017 provides a different perspective. Because it’s a cross-platform source code benchmark, SPEC CPU2017 excludes ISA-specific optimizations common in open source projects where performance matters. For example, 525.x264 won’t have assembly functions to accelerate video encoding as libx264 does. The SPEC CPU2017 testing done here also focuses on single threaded performance, while our prior testing covered multithreaded performance with the same number of cores in play.

However, the general performance picture is largely the same. Loongson still can’t compete with older desktop offerings like the Core i5-6600K, even if Loongson has improved performance between the 3A5000 and 3A6000. The 3A6000’s LA664 architecture can often achieve good IPC. Performance counters further showcase Loongson’s efforts to improve their branch predictor. But good IPC by itself doesn’t make a CPU competitive, just as high clock speed alone isn’t a good indicator of success. Loongson needs to keep up their pace of IPC improvements while dramatically increasing clock speeds if they hope to seriously compete with Intel and AMD.

Zhaoxin’s KX-6640MA is in an even lower performance bracket, and finds company with other low power CPUs like Arm’s Cortex A73 and Intel’s Goldmont Plus. It’s an adequate performer in that category, but Goldmont Plus can feel noticeably sluggish in everyday tasks next to a high performance CPU. SPEC CPU2017 suggests the KX-6640MA is an even worse performer, and not an ideal option for client workloads.

If you like our articles and journalism, and you want to support us in our endeavors, then consider heading over to our [Patreon](https://www.patreon.com/ChipsandCheese) or our [PayPal](https://www.paypal.com/donate/?hosted_button_id=4EMPH66SBGVSQ) if you want to toss a few bucks our way. If you would like to talk with the Chips and Cheese staff and the people behind the scenes, then consider joining our [Discord](https://discord.gg/TwVnRhxgY2).

It would be good to see a comparison between mobile GPUs, Mali vs Adreno vs PowerVR

龙芯中科已经更新了其spec2017-rata1的单核分数。你可以去loongson官网看看。GCC工具也应该是更新了，在GitHub上。单核性能提升不小。目前国内的loongson和huawei-kunpeng 920B（simc-n+1）比较有优势挑战intel。