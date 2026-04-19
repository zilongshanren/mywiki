---
title: 'Lowering the BAR: AMD’s 6700 XT launch and the Importance of Disclosure'
url: https://chipsandcheese.com/p/lowering-the-bar-amds-6700-xt-launch-and-the-importance-of-disclosure
author: George Cozma
published: '2021-03-10'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

On March 3rd, 2021 AMD officially announced the 6700 XT to the world. Along with it came the usual first-party performance graphs, most of which showed it matching or even beating NVIDIA’s RTX 3070—which was a shock to the tech world. It would seem, however, all is not as AMD would have you believe.

AMD’s Graphs of 6700 XT Performance: 3070 Beater?

When AMD went live on March 3rd they showed the graph below:

In and of itself, this is a typical “red bar graph” first-party AMD performance slide that we have become accustomed to in their launch events. Nothing out of the ordinary here. What is unusual however, is the performance claimed on the 6700 XT. In this eight game comparison, it only loses three times, twice of which are essentially ties. This graph blew people away as few expected the 6700 XT to match the 3070 let alone beat it. An impressive showing then, as many leaks and information pre-launch had the 3070 squarely out of reach.

Not so fast. This graph is misleading.

Before we get to that, the details for this data should be referenced in the fine print. Looking at the bottom of the slide we can see:

AMD Confidential | NDA Required |Embargoed Until March 3, 2021 at 12:00pm ET. SEE ENDNOTE RX-628.

Caption on AMD’s eight-game comparison slide.

“SEE ENDNOTE RX-628” at the bottom is a reference to details about the testing that was conducted, so lets go to the end notes and see.

What about SAM?

“RX-628 – Testing done by AMD performance labs Feb 18 2020 [The date is likely an error, as I assume testing was done on Feb. 18 2021 and not Feb. 21 2020], on a RX 6700 XT (Pre-release 20.50 driver), RTX 3070 (461.40 driver), and 3060 Ti (461.40 driver), AMD Ryzen 9 5900X CPU, 16GB DDR4-3200MHz, ASRock X570 Taichi motherboard, Win10 Pro 64, Performance may Vary. RX-628″

The endnote marked RX-628 seems to be in order, however there is one glaring omission on these slides:

The RX 6700 XT was tested with Smart Access Memory (Resizable BAR) enabled.

This information, which was not publically disclosed in this launch, was later confirmed by AMD themselves in talks with Hardware Unboxed and Gamer’s Nexus.

For those unfamiliar with AMD’s Smart Access Memory or re-sizable Base Address Register, it is a feature of the PCI-Express 3.0 spec and newer that allows operating systems to access a GPU’s VRAM directly in sizes larger than (what was historically) 256MB. In the past this limitation wasn’t seen to be an issue with smaller VRAM buffers and older GPUs. With modern GPUs like AMD’s RX 6000 series coming with double-digit frame buffers, there is now more benefit to be had by giving the system direct access to multiple gigabytes of fast GDDR6.

This feature has been shown by both AMD and third party benchmarks to be good for 0-10% performance improvements, per title. This means that the performance results shown aremisleading at best and an outright lie at worst and highlights why disclosure is so important.

Why Disclosure is Important

I shouldn’t have to go over why disclosure is important—this much should be obvious—but I will. It comes down to honesty and expectations.

In these days where the global pandemic and silicon shortages have gamers and enthusiasts clamoring for any GPU they can get their hands on, a seemingly small omission like this might go unnoticed. However when consumers spend their hard-earned dollars on a product, after battling against bots and other shoppers to finally get the product they’ve been after, it better damn well perform how it is advertised.

Without full disclosure of how the testing was done then we could have tests that are skewed heavily to one side or the other and we wouldn’t know until either the consumer gets the product or an independent media site reviews it.

I remember when the tech press went after Intel for misleading marketing by using benchmarks like SYSmark and WebXPRT—which Intel helped create—and then failed to disclose the fact that they helped with their creation. Or when Nvidia tried pushing the GPP program on AIBs without disclosing what it would mean for their AIB partners’ brands and AMD GPUs.

Now, does that mean I think that AMD’s omission of SAM on a few first-party benchmarks is as bad as the examples above? No, but I do think that it is our (the tech media’s) job to hold these companies’ feet to the fire, even in fairly small cases like this, because otherwise companies may think that it OK to mislead consumers.

I hope that in the future AMD—and others—take heed and do not try to mislead consumers about their products. If they don’t, you can count on us to be here again telling you when they do.

Like the old Russian proverb says: “trust but verify.”