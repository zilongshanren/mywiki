---
title: Analyzing Video Card Efficiency, Part I – Power
url: https://chipsandcheese.com/p/analyzing-video-card-efficiency-part-i-power
author: Serebit
published: '2021-09-09'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# Analyzing Video Card Efficiency, Part I – Power

While most enthusiasts chase the absolute best performance at any cost, there are a few who use efficiency as their benchmark for a card’s attractiveness. It can be argued that the efficiency of a design – how effectively it utilizes the resources available to it – is a better measure for comparing different graphics cards than pure performance, and it can offer an interesting perspective on the upsides and downsides of any given design. Though efficiency is nebulous, there are common ways to loosely measure it, chief among them being performance per watt. To that end, this piece will analyze mainstream consumer graphics cards, starting with Turing and Vega 20, to see how each card stacks up to the competition. Let’s get started.

## Methodology

The measure of efficiency used for this article is FPS per Watt, which can be simplified down to frames per Joule (or f/J), which can be thought of as the number of frames a given GPU can render on average using one Joule of energy.

The “Average FPS” metric is split between three resolutions (1080p, 1440p, and 2160p), and is a composite of two sets of results. One comes from TechPowerUp’s GPU reviews, and the other comes from the Tom’s Hardware GPU performance overview. The geometric mean of these two results is then taken for the final FPS figure for each card at each resolution.

Also, keep in mind that much of this data is using launch day drivers, because these reviews are from launch day. Thus, it is very possible that as the drivers have matured, the performance has increased for one GPU over another. However, TechPowerUp’s and Tom’s datasets are the best publicly available datasets that we have, because we do not have the resources in house to do all this testing.

The power consumption metric used is also a geometric mean, based on TechPowerUp’s GPU reviews and the Tom’s Hardware power consumption roundup. It represents the average total card power draw in a typical gaming workload. It’s worth noting that this is meant to approximate stock power draw for reference cards, or cards at or near reference clocks – cards with factory overclocks will likely see power draw higher than the numbers reported here.

In order to produce the final f/J efficiency number for each resolution, the calculated average FPS for a given card is divided by its calculated average power draw. Four cards have incomplete data, and are marked as estimates to avoid confusion.

## Gaming at 1080p

Instead of itemizing every card on this chart, we’ll go through each major architecture and discuss the interesting bits.

### Vega 20 (Radeon VII)

Starting from the bottom, the Radeon VII is horrendously inefficient at only 0.456 frames per Joule. Thankfully, things do get better as resolution increases, though the poor Radeon VII never recovers from the bottom of the chart when it comes to gaming.

### Turing (RTX 2000 and GTX 1600 series)

Moving to RTX Turing, we actually have a rather consistent set of results. The Turing RTX cards hover around 0.61 frames per Joule, with the only outliers being the RTX 2080 Super at 0.567 frames per Joule (TU104 pushed too far) and the RTX 2070 at 0.588 frames per Joule (maybe bad yields on full-die TU106?). Most of RTX Turing is so close together that it might as well be margin of error, but the RTX 2080 gets a technical victory for having the biggest number at 1080p.

Where it gets interesting, however, is GTX Turing. The GTX 1660 and GTX 1650 Super are grouped together with most of RTX Turing at around 0.63 frames per Joule, but the GTX 1660 Super and Ti are both near the top of the chart, even above the most efficient RDNA1 and least efficient RDNA2 cards. The GTX 1660 Super is identical to the GTX 1660 in all ways other than its VRAM – the base model uses GDDR5, while the Super refresh uses GDDR6. Clearly, then, the 1660 was bottlenecked by its lack of bandwidth, and merely swapping the VRAM allowed the Super model to reach 0.674 frames per Joule. The Ti model is in a similar spot, with its extra shaders and slightly lower clocks allowing it to surpass the performance per watt of the Super model at 0.701 frames per Joule. Thus, the GTX 1660 Ti is the most efficient Turing GPU at 1080p, and one of the most efficient cards overall!

### RDNA1 (RX 5000 series)

Next up is RDNA1, with results for Navi 10 and Navi 14 based cards. The RX 5500 XT does especially poorly at only 0.549 frames per Joule, which could be attributed to architectural flaws with RDNA1 not scaling down particularly well, or to the card only receiving bad bins of the Navi 14 die. The RX 5700 XT also doesn’t do very well, though this is clearly due to the card being pushed too far at stock. Interestingly, the RX 5600 XT is *not* the most efficient RDNA1 card here, though it does do rather well at 0.652 frames per Joule – the crown for RDNA1 actually goes to the RX 5700 at 0.671 frames per Joule, just behind the GTX 1660 Super. However, given the VBIOS kerfuffle with the RX 5600 XT’s launch, some variants of the card may be more efficient than others in practice. Regardless, I’ll give the 1080p RDNA1 victory to the RX 5700.

### Ampere (RTX 3000 series)

When it comes to Ampere, the chart is bisected with a clear reason: GDDR6X. The GDDR6X cards hug the bottom of the chart at 1080p, with the RTX 3080 Ti estimated to be the third least efficient card overall at only 0.566 frames per Joule, and the RTX 3080 being the most efficient GDDR6X card at 0.586 frames per Joule. Clearly, these aren’t great results, but what about the GDDR6 cards? Well, as soon as the memory type changes, the efficiency of Ampere skyrockets. The least efficient GDDR6 Ampere card at 1080p is the RTX 3060 at 0.657 frames per Joule, but the most efficient is the RTX 3070 at *0.738 *frames per Joule, the best result we’ve seen thus far (with the RTX 3060 Ti not far behind). Clearly, Ampere can be extremely competitive in efficiency if its configuration allows for it.

### RDNA2 (RX 6000 series)

Finally, we come to RDNA2, AMD’s first genuinely competitive GPU microarchitecture in years and the most efficient group on this chart. RDNA2 is a massive leap in efficiency from RDNA1 – the least efficient RDNA2 card at 1080p, the RX 6800 XT at 0.665 frames per Joule, is only slightly less efficient than the RX 5700 at the same resolution. The RX 6900 XT gets very similar efficiency in practice despite the identical TBP, and the RX 6700 XT effectively matches the most efficient Turing card at 0.702 frames per Joule. The second best RDNA2 card (and card in general) at 1080p is the RX 6800 at 0.757 frames per Joule, with access to all of Navi 21’s cache and memory bandwidth along with lower clocks and fewer compute units.

The most efficient card at 1080p, however, is the newly released RX 6600 XT. Unlike the RX 6700 XT, which has been pushed far past its most efficient clocks, the RX 6600 XT keeps its power profile low while still managing great performance, with a paramount 0.798 frames per Joule. There are a few design decisions that contribute to this, likely the reduced PCIe lanes (only x8 on Navi 23) along with the miniscule 128-bit memory bus. Let’s see if it maintains the lead at higher resolutions.

## Gaming at 1440p

At 1440p, the stack shifts somewhat, with some cards becoming bandwidth-limited and dropping to the bottom. The cards with lower bandwidth are hit the hardest; Navi 14 and TU116 based cards are sent reeling, while Navi 10, Navi 23, and the RTX 2060 all take decent blows. Generally, it seems like the more shaders a card has, the better it can handle higher resolutions (which isn’t particularly surprising). In the case of the RX 6600 XT, it would seem that its 32 MB of L3 cache isn’t quite enough to make up for its tiny memory bus at resolutions higher than 1080p, though it is still one of the top performers on the chart regardless.

Interestingly enough, as soon as resolution increases, the performance per watt of GDDR6X Ampere begins to look much more attractive. While these cards were far closer to the bottom of the stack at 1080p, GDDR6X Ampere jumps to the center of the stack at 1440p, with the RTX 3080 almost reaching the performance per watt of the diminutive RTX 3060 (though none of them reach the heights of the RTX 3070 and 3060 Ti). It seems clear to us that the GDDR6X cards are more bottlenecked by shader occupancy than anything else due to their enormous FPU count, which prevents them from reaching their full potential at lower resolutions, but allows them to shine at higher resolutions.

When it comes to RDNA2, the Navi 21 based cards do rather well at 1440p, with all three rising closer to the top of the chart. It seems that their enormous L3 cache is more than enough to keep them at near peak performance at this resolution. Meanwhile, the RX 6700 XT maintains its position, adequately fed by its 96 MB L3 cache. Due to the RX 6600 XT falling off hard and ceding its first place position, the RX 6800 shifts up one spot to become the most efficient 1440p video card listed.

## Gaming at 2160p

Finally, at 2160p (or “4K”), we see the bandwidth-limited cards drop like rocks. The GTX 1650 Super and RX 6600 XT are hit the hardest, with the latter even falling below the efficiency of the RTX 3080. The RX 5500 XT drops significantly as well, coming extremely close to taking last place on the chart – though the Radeon VII seems determined to keep its spot. Generally, like we saw at 1440p, it seems that cards with fewer shader cores are hit harder by resolution increases.

Of note is that the RX 6600 XT is the only RDNA2 card to suffer a massive hit from the jump to 2160p. The RX 6700 XT has a mostly average hit to efficiency, while the Navi 21 cards actually scale appropriately for their shader count, indicating a lack of any significant bandwidth limitation at this resolution. Given this data, it would seem that AMD chose a reasonable L3 cache size for these dies given their target resolutions. The RX 6900 XT is actually the best-scaling card on this chart, other than…

GDDR6X Ampere finally stretches its legs. Though shader occupancy was clearly an issue at previous resolutions, 2160p allows GA104 and GA102 to make full use of their bandwidth, driving the RTX 3090 and RTX 3080 Ti to the top of the chart with an impressively small 35% penalty from 1440p. Even the GA104-based RTX 3070 Ti manages to climb above the RX 5700. Now that the shader cores aren’t just sitting idle at full clocks, we see much more efficient use of power.

So, at 2160p, Ampere is far more competitive with RDNA2 in gaming power efficiency. Though this could be easily assumed given the data available from other sources, it’s pleasing to have a demonstration of how this is the case. Despite this, though, the RX 6800 still sits at the top of the chart, with two wins now under its belt.

## Conclusion

So, with all that said, what have we learned? If I could glean anything from the data I’ve collected so far, it’s that power efficiency is not as simple as one would assume. Video cards are complex creations, and each individual SKU has its own strengths and weaknesses. Efficiency changes per resolution, and it changes depending on the workload. Even the data presented here, despite my best efforts, can be regarded as an oversimplification.

Regardless, we can use this data to get a broad sense of how power efficiency manifests itself depending on the video card. For example, we can empirically validate AMD’s claims that RDNA2 is more efficient than RDNA1, and that RDNA1 is more efficient than Vega 20. Additionally, we can show that Ampere is not an inefficient architecture per se – the RTX 3070 and RTX 3060 Ti do extremely well in power efficiency, for example – but its use of GDDR6X at the high end incurs a significant penalty to efficiency at lower resolutions. These aren’t the only conclusions we can take from this data, of course, and you should feel free to draw your own.

In Part II, we’ll take a look at a different measure of efficiency, one that’s not as often discussed – *bandwidth.*

## Sources and Notes

The data used for this article has been obtained from multiple sources, including:

The power consumption measured by Tom’s Hardware for the RTX 3080 Ti seemed erroneous, only drawing slightly more than the RTX 3070 Ti, so the RTX 3080 Ti’s power consumption number for the Tom’s dataset was extrapolated based on the other cards in the Ampere lineup using the GA102 die.

The RTX 3060, RTX 3070 Ti, RTX 3080 Ti, and RX 6700 XT did not have entries in the Tom’s Hardware benchmarks roundup, so their average FPS data was extrapolated from the TechPowerUp data and the rest of the Tom’s Hardware data.

Special thanks to TechPowerUp and Tom’s Hardware for providing publicly available datasets of both average FPS and power consumption, and to the rest of the Chips and Cheese staff for contributing some additional analysis.

And a big thanks to * Fritzchens Fritz* for the banner picture and for all his hard work that he does.