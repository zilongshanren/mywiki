---
title: Was Rocket Lake Power Efficient?
url: https://chipsandcheese.com/p/was-rocket-lake-power-efficient
author: Chester Lam
published: '2022-12-17'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

Compared to Golden Cove? Of course not. A newer architecture on a newer process should have a pretty huge advantage. Unsurprisingly, Golden Cove is faster at any power level.

So let’s go for more appropriate comparisons. If we level the playing field a bit by looking at CPUs implemented on the same process, Rocket Lake isn’t so bad. So in this article, we’ll take a look at Rocket Lake’s performance at different power levels. Unlike our previous article on Alder Lake, we’re going to show package power instead of core power. While core power gives us a narrow focus on the cores themselves, lots of important components are not on the core power plane on Intel’s CPUs. That includes the L3 cache, ring bus, and memory controller. Like our previous article, all tests are run with four threads active. Affinity was used to restrict workloads to four cores on CPUs that have more.

Rocket Lake vs Skylake and Kaby Lake

Rocket Lake, Skylake, and Kaby Lake are all implemented on variants of Intel’s 14nm process. That should make for a vaguely fair comparison, although Kaby Lake and Rocket Lake benefit from more optimized versions of the process node.

libx264 – 4K Video Transcode

This transcoding workload includes plenty of AVX and AVX2 instructions. It can even take advantage of AVX-512, which should make things interesting for Rocket Lake.

Rocket Lake’s high power consumption is well known, but it doesn’t do so badly at moderate power. Above 30 W, Rocket Lake’s backported Sunny Cove cores (Cypress Cove) are able to deliver higher performance than Skylake with the same power draw. Rocket Lake can also draw a lot more power to deliver higher performance, until four cores pull an incredible 147 W. Of course, going there means terrible efficiency:

The i5-6600K gets a flat line after 3.6 GHz, because maximum boost clock (measured using 1T addition latency) is plotted here. At 3.9 GHz, all core boost clock is still 3.6 GHz, and libx264 hits all four threads.

At stock clocks, Rocket Lake is 71.5% faster than Skylake, but ends up using nearly twice as much total energy to finish the task. Things are much better at moderate clock speeds. Rocket Lake’s efficiency matches Skylake’s in the mid 3 GHz range, and is best between 2.5 GHz and 3 GHz. There, it’s roughly as efficient as Kaby Lake at 3.5 GHz, Skylake at 3 GHz, or Golden Cove between 4.2 and 4.5 GHz. Rocket Lake’s biggest weakness is its inability to keep scaling down to even lower power targets. Performance takes a sharp drop below 30 W, and efficiency doesn’t improve below 2.5 GHz.

7-Zip Compression

7-Zip is very heavy on integer instructions and pretty much doesn’t hit the vector units. It’s also not as parallelizable as libx264 encoding, and often won’t fully load the four cores it’s given. Here, we’re testing 7-Zip by having it compress a 2.67 GB ETL file.

Poor i5-6600K. Not sure what happened there

With this compression workload, there’s surprisingly not too much difference between Kaby Lake, Rocket Lake, and Golden Cove. Again, Rocket Lake beats Kaby Lake above 35W, but scales poorly to lower power. Efficiency is best around 2.5 GHz, where Rocket Lake is about on par with first generation Skylake.

Would Hybrid Make Sense?

Alder Lake introduced a hybrid architecture scheme, where Golden Cove and Gracemont cores were implemented on the same chip. Golden Cove used a lot of die area and power to target maximum performance, while Gracemont took a more conservative approach and aimed to deliver power and area efficiency. Rocket Lake couldn’t have done the same thing, since Intel’s Atom cores on 14 nm didn’t even support AVX2.

At least for integer workloads, there’s a nice power range where Gracemont could offer higher performance in the same power envelope

At least for integer workloads, there’s a nice power range where Gracemont could offer higher performance in the same power envelope

But what if instruction set parity somehow wasn’t an issue? Say Goldmont Plus had microcoded AVX-512, allowing it to be used alongside Rocket Lake’s giant Cypress Cove cores. Would the power/performance curves make such a combination sensible? Unlike the previous part of the article, we’re going to use core power here. The Celeron J4125’s very low “uncore” power means that package power won’t make for a fair core to core comparison.

Rocket Lake can’t scale down to very low power levels, while Goldmont Plus can’t scale to high power. That leaves a sizeable power gap between where Goldmont Plus stops, and where Rocket Lake starts. There’s a similarly large performance gap as well. Funny enough, Skylake slots in right in between. We mostly see the same picture with 7-Zip, though Goldmont Plus does a bit better than Skylake below 5W of total core power (across four cores).

From those power/performance curves, Goldmont Plus would be a nice little core companion to Rocket Lake. It reaches power and performance levels that Willow Cove can’t. Even a triple architecture setup like that of recent mobile chips might make sense. Rocket Lake’s Willow Cove could be a “prime” core, Skylake could be a “mid” core, and Goldmont Plus could be a “little” core.

But back to reality – mismatched instruction sets were a problem with Intel’s hybrid designs. On Lakefield, Tremont didn’t support AVX, preventing software from using the AVX units on the accompanying Sunny Cove core. On Alder Lake, Gracemont didn’t support AVX-512, meaning that Golden Cove’s AVX-512 capability couldn’t be used. The same would apply here too. It’s just interesting that Goldmont Plus’s power and performance curve makes it a viable little core companion to Rocket Lake, and would cover Rocket Lake’s biggest weakness (inability to scale below 30W) in a hybrid design.

Final Words

Just like Alder Lake, Rocket Lake was criticized for its high power consumption. Both chips are inefficient at stock. Rocket Lake, by virtue of being a beefy architecture backported to an older node, is much worse. It also doesn’t scale down to low power levels as much as Alder Lake does. But it’s not all doom and gloom. In moderate desktop power levels above 30W, Rocket Lake is the most efficient 14nm design. It shows that efficiency can be gained without a new process node, by using a larger, higher IPC core running at lower clocks. Unfortunately for Rocket Lake, this efficiency advantage only applies within a small window of power targets.

If you like our articles and journalism and you want to support us in our endeavors then consider heading over to our Patreon or our PayPal if you want to toss a few bucks our way or if you would like to talk with the Chips and Cheese staff and the people behind the scenes then consider joining our Discord.