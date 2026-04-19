---
title: 'The End of an Era: AMD Discontinues Pre-2016 GCN GPU Support'
url: https://chipsandcheese.com/p/the-end-of-an-era-amd-discontinues-pre-2016-gcn-gpu-support
author: Apex
published: '2021-06-23'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

A small official blog post and a driver release footnote made for an unceremonious end to one of the most loved and long-lived series of AMD GPUs ever, Hawaii, and it’s HBM-powered follow-up, Fiji. Today we try to add a small bit of ceremony back, to recognize GPUs that largely contributed to AMD’s ‘fine wine’ reputation and ask—why now?

The Hawaii chip under the hood of 2013’s Radeon R9 290X was hot and power hungry but seriously fast. Even eight years later, in today’s modern titles it consistently performs 1080p duties well. It would continue to be sold until 2015, as the R9 300 series. (Image credit: Guru3d)

Radeon driver 21.6.1 puts Hawaii and Fiji out to pasture. Why?

At the height of 2021’s continuing GPU shortages, AMD has chosen a curious time to end support for a line of GPUs that while old—the Hawaii-based Radeon R9 290X launched in 2013—still manage to maintain pace with perennial mainstream favorites the like RX 480, RX 580 and NVIDIA GeForce 1060 (Steam’s most popular GPU, ~9% of its player base); cards four years newer.

Together with the aforementioned trio, older cards like the R9 290/X, its 2015 refresh the R9 390/X and the Fury/X are still commanding prices on eBay in the multiple hundreds of dollars amid the GPU shortages, based on their usefulness as 1080p60 cards.

Product support on 21.6.1.(Source: AMD)

As of June 21st, 2021 however, the last driver update for these venerable veterans is May’s Radeon Driver 21.5.2. Crucially, the June driver fixes some UX issues that had been plaguing many users—some since purportedly as far back as 20.4.2. This exclusion will omit the 200-, 300- and Fury-series cards from receiving these and any future fixes.

So, why? And more importantly: why now? Let’s take a look.

GCN 2/3 Architecture: Too old?

It could easily be argued that, on the surface, this is needed to focus development toward newer Radeon cards and newer architectures, like RX 4/500’s Polaris GCN 4. This argument stops holding water however as soon as one realizes that many 1st generation GCN cards—rebadges in the 400 series—arestill receiving support in the 21.6.1 driver. Cards still supported are from various Oland and Cape Verde refreshes, listed below:

R5 430 (Oland Pro)

R5 435 (Oland)

R7 430 (Oland Pro)

R7 435 (Oland)

R7 450 (Cape Verde Pro)

Even worse is that the Bonaire-based Radeon RX 455 is still supported, which is a rebadge of a Radeon HD 7790. Yes, HD series. All of these GPUs are, in fact, even older architecturally than the GCN 2 Hawaii– and GCN 3 Fiji-based cards that are having support pulled.

Fiji being on newer GCN 3 is closer architecturally to GCN 4 Polaris than GCN 1′s Oland or Cape Verde, which are listed above as still supported. More telling still is the fact that GCN 2 and up is fully DirectX 12 compatible. So why, then?

Performance?

This angle was alluded to earlier in the article, however considering that the R5 430 is still supported—being little more than a display adapter—this argument doesn’t make sense either. We’ll explore the argument anyway.

For good measure, the R9 290X is roughly equal in performance to a 4GB RX 480 or RX 580, depending on title. In titles that make better use of GCN 4’s improvements the gap widens to about 10-15% advantage for Polaris. Gaps to the ever-popular GTX 1060 remain similar depending on title and scenario. At 1080p, Hawaii is certainly capable of a 60 FPS experience on almost all newer titles, as evidenced in a 2019 recap by Gamer’s Nexus.

Certainly it is faster than anything NVIDIA is currently supporting since the Kepler era, which hasn’t aged as well. As we’ll explore more down below however, the GTX 600 and 700 series based on Kepler will still end up being supported longer than Radeon 200-series of the same era.

Let’s also not forget the Radeon Fury series, a 2015 design which featured the first consumer GPU to sport HBM, which is also having support dropped.

Culling Windows 11 Support?

With rumors swirling about Microsoft announcing Windows 11’s launch on June 24, 2021 at 11AM EST, many users are speculating online that this is timing to pull support in advance for these older GPUs. Once again however, even older chips (GCN 1) are retaining architectural support in the display driver, and even more blunt is the fact that all signs point to Windows 11 being based on the same driver model as Windows 7/8/8.1/10, retaining compatibility.

Greed? FSR Support? Why is NVIDIA’s Support Longer?

Embarrassingly, a card that the R9 FuryX launched beside, NVIDIA’s 2015 Maxwell-based GeForce GTX 980 Ti, has been getting positive press for being capable of running an AMD technology, FSR. AMD’s own Fury X? Making rounds for losing driver support. (Image credit: Guru3d)

If one was a cynic, they might just arrive at the simple conclusion that AMD took FSR’s opportunity of positive press to bury the negativity around discontinuing support for cards only 6 years old. Oh, also AMD: “buy a newer card already.”

While there is no definitive way to prove this, it is either telling or just plain bad timing that the 21.6.1 driver is the first one optimized for FSR. Thankfully for affected Radeon users, FSR is implemented at the game level and does not require driver optimization. It has already been tested by users to work on these cards. The question becomes for how much longer will games work (FSR or not), and also, what FSR performance enhancements are left on the table by missing 21.6.1?

As mentioned above, there is still life left in your cards via FSR. And as many have been quick to point out, nothing is stopping your card from working today. 21.5.2 was the latest driver until two days ago, and that’s still available. Most users should be able to squeeze another 12 months or so out of these cards at playable framerates and settings which is (hopefully) enough time to try and secure a faster GPU.

The Bad: It’s All of the Above

In essence, I believe I can summarize the reasoning behind AMD’s move with one statistic:

AMD Market cap: $101B USD

NVIDIA Market cap: $471B USD

AMD (and ATI before it) have consistently played second-fiddle to NVIDIA when it comes to both mind share and market share. This balance has ebbed and flowed throughout the years, but never at one point has AMD held more than roughly one third of the dGPU market. Even during AMD’s victorious product cycles, equal or greater emphasis was typically placed on NVIDIA’s mistakes rather than AMD’s ingenuity. The R9 290X was one such competitive card. These periods of AMD strength never lasted longer than 1-2 generations at a time, though.

All of the reasons explored in the first part of this article are in some way correct. Individually they miss the mark, however hollistically they all boil down to one thing:

It’s not about power, it’s about popularity

The paragraph above provides some insight into ‘the why’, among other reasons. ‘The what’ is illustrated below by the flawed but useful Steam Hardware Survey:

At time of writing, AMD GPUs represent roughly 1/6 of the GPUs in Steam’s Hardware Survey. It must be noted that this number includes integrated GPUs, such as AMD’s Vega 8/7 and Intel’s many IGPs. The true number of Radeon dGPUs is therefore even lower. (Source: Steam)

AMD can’t continue to devote resources to card families that represent a fraction-of-a-fraction-of-a-fraction of a user base. The 200-, 300- and Fury-series cards remain in use because of their performance despite their age. The low-end 400-series cards that persist with support aren’t special; they are mostly OEM models. When all other logic fails, the 400 series is basically a ‘freebie’ optimization-wise as it’s essentially the same as the 500 series that is still sold today. AMD does have to ‘draw the line’ somewhere on support, it seems today it was 2016. I would advise Polaris users take notice today; don’t expect more than 12-24 months of driver support at this point before going through the same process. Speaking of that…

The Ugly: Zero Notice

One ugly truth that AMD continues to struggle with, frustratingly, is that PR blunders like this are entirely avoidable. Between Frank Azor’s twitter moments, Herkelmann’s over-use of the word “jebaited”, and general subversion of expectations by AMD toward their own community, the unceremonious dropping of GCN 2 and 3 support was another avoidable blunder in a history of them.

I don’t think anyone in the PC enthusiast community expects hardware to be supported forever. Some form of notice is always nice, though, and giving it costs AMD nothing. Compared to what NVIDIA did with Kepler’s move to legacy status, AMD dropping 200-, 300- and Fury-series support like a rock the day before the FSR launch can’t help but leave a bad taste in the mouth for any users holding onto these grizzled but capable cards.