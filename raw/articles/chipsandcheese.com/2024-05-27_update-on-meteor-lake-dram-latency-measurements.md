---
title: Update on Meteor Lake DRAM Latency Measurements
url: https://chipsandcheese.com/p/update-on-meteor-lake-dram-latency-measurements
author: Chester Lam
published: '2024-05-27'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# Update on Meteor Lake DRAM Latency Measurements

Chip makers are always looking to save power, especially in mobile devices. Like a CPU core, Meteor Lake’s memory controller can enter lower power states with reduced clocks and voltages. I’m testing Meteor Lake in the ASUS Zenbook 14 OLED, which nominally has a 128-bit LPDDR5X-7467 setup, but memory speeds can go as low as 3200 MT/s to save power. Besides changing memory speed, the memory controller can switch from the high performance Gear 2 mode to Gear 4. Gear 2 mode means the memory controller runs at half of memory frequency, while Gear 4 cuts memory controller frequency to a quarter of memory frequency.

Apparently Intel’s heuristics determined that the memory controller should prioritize low power over high performance when my latency test runs. That makes sense, since the latency test tries to measure minimum latency with only one outstanding demand access at a time. To the memory controller, that would look like very little DRAM traffic, so going into a low power state is understandable. However, that results in higher latency measurements.

## Additional Testing

Meteor Lake’s datasheet says heuristics evaluate memory bandwidth utilization and IA (CPU core) stalls. Evidently it doesn’t care about E-Core stalls, since I see >200 ns DRAM access latency from the E-Cores and they’re spending nearly all cycles memory bound during a latency test. But Intel does take bandwidth demand into account. If I load another core with a memory bandwidth test targeting a fixed 1 GB test size, measured latency improves. Evidently memory bandwidth demands from a single E-Core or P-Core is enough to kick the memory controller into a higher performance mode, but doesn’t push queue occupancy high enough to wreck latency measurements.

From this additional testing, Meteor Lake’s memory controller appears to stay in a low power state unless the CPU tile demands a lot of extra DRAM bandwidth. Intel may be monitoring occupancy at a queue between the CPU tile and the memory controller. The memory controller will not enter a high performance state if only the LPE-Cores are generating traffic. Having one LPE-Core pull as much memory bandwidth as it can still results in >200 ns latency measurements with the other LPE-Core.

When the memory controller’s not in a low power state, the LPE-Cores see 175.3 ns of DRAM latency. DRAM latency from E-Cores was measured at about 153 ns. Meteor Lake’s P-Cores are less affected. Testing on a single P-Core already gives similar results to an E-Core with another core pulling a couple dozen GB/s of bandwidth. Adding synthetic bandwidth load only slightly improved P-Core memory latency, so maybe Intel’s heuristics might take P-Core stall reasons into account.

## Comments about Crestmont

In the [Crestmont ](https://chipsandcheese.substack.com/p/meteor-lakes-e-cores-crestmont-makes-incremental-progress)article, I wrote that Meteor Lake had high memory latency. AMD’s Van Gogh and Phoenix APUs manage to keep latency under 200 ns with 2 MB pages. They used LPDDR5, which wasn’t great compared to desktop DDR4 or DDR5. But at least they weren’t going over 200 ns.

With the memory controller in a higher power state, Crestmont can also achieve sub-200 ns memory latencies. At 153 ns, they land in the same ballpark as Zen 2 cores in AMD’s Van Gogh. Meteor Lake’s memory controller might be capable of slightly better latency too. Having another core run the bandwidth test means some requests will be queuing up at the memory controller, and queuing delays will impact latency measurements.

## Comments on the LPE-Cores

I wrote a separate article on how low power Crestmont was hamstrung by lack of a L3 cache. From the data above, Intel’s power saving strategy also has to be considered. Even high bandwidth demand from the LPE-Core cluster doesn’t bring the memory controller out of a low power state.

On one hand, I can understand Intel’s decision. LPE-Cores aim to handle tasks with minimal power draw. Keeping the memory controller in a low power state aligns with that goal. On the other, losing a high capacity cache and suffering higher memory latency is a nasty double whammy. Memory latency improves if the CPU tile is awake and generates enough traffic, but waking up the CPU tile seems to defeat the LPE-Cores’s design goals. After all, they aim to handle light tasks without waking up the CPU tile.

I still think giving the LPE-Cores more cache is the right way to go. Doubling L2 size would be a good start, because Intel’s Atoms have long been capable of supporting a 4 MB L2. A larger system level cache would be a more ambitious approach. Intel could also let the LPE-Cores kick the DRAM controller out of a a low power state. That would be a very simple move and may be possible with a firmware update. But I suspect it wouldn’t do much to improve the LPE-Core situation. 175 ns of latency is better than over 200 ns, but it’s still brutal.

## Credits

I’d like to thank Andrei F. for pointing out that Meteor Lake’s memory controllers will operate in a low P-State if processes are pinned to the LPE-Cores. That led me down a rabbit hole of testing with different combinations of loaded cores.

If you like our articles and journalism, and you want to support us in our endeavors, then consider heading over to our [Patreon](https://www.patreon.com/ChipsandCheese) or our [PayPal](https://www.paypal.com/donate/?hosted_button_id=4EMPH66SBGVSQ) if you want to toss a few bucks our way. If you would like to talk with the Chips and Cheese staff and the people behind the scenes, then consider joining our [Discord](https://discord.gg/TwVnRhxgY2).