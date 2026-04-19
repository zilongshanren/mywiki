---
title: 'SiFive Completes Series F Funding Round: +$175m, $2.5b Evaluation'
url: https://chipsandcheese.com/p/sifive-completes-series-f-funding-round-175m-2-5b-evaluation
author: Dr Ian Cutress
published: '2022-03-18'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# SiFive Completes Series F Funding Round: +$175m, $2.5b Evaluation

The three main architectures currently in the ecosystem that people talk about are x86, Arm, and RISC-V. It’s that last one we’re focusing on, as the newest on the block and it is slowly becoming a de-facto option for a lot of simple compute designs as well as designers. The RISC-V model is different to the other two: the specification is open, there are no licensing fees, and any company with a core design team can build exactly the core they want with the instructions they need. There are pros and cons to this situation, but one avenue it does open up is that core microarchitecture companies can build up their designs and license them for use in other SoCs. The most well-known of the RISC-V companies that does this is SiFive, and it’s getting a cash boost injection today.

For those not in the industry, there are three main architectures for modern general purpose processors: x86, Arm, and RISC-V.

First off is x86 (and the 64-bit extensions, as well as others). Only a small number of companies have a license to build cores based on x86, and all of them use those cores to build chips which they then sell. While there has been no intention of issuing any more licenses, Intel is planning to offer its x86 cores for manufacturing in Intel’s fabs for third-party customers building new chips – this is a few years off for now, but it is coming to market.

The Arm model involves the company Arm as the arbiter of the architecture. Arm offers two main forms of license. First is a microarchitecture license, which means a company can go and design any chip they want with the instruction set, including custom instructions in some versions of this license. Second is a core license, by which Arm actually designs cores based off of the architecture, and companies can license these to build within their chips, although without modifications. Arm does the upfront work in validating designs at the fabs, allowing customers to have confidence in the base Arm designs.

RISC-V is a lot more open ended. The architecture (i.e. the instructions) are open to use for free, by anyone. This makes it very easy for everyone, from companies to research institutions, to build their own core. Then it’s up to those people to manufacture it at a fab. In the RISC-V ecosystem though, a company can build a core on that architecture, and then license it to anyone else to use in their chips, kind of like Arm’s core license. Technically the RISC-V International organization is in charge of updating the base specification and promoting the use of RISC-V, but there are no requirements to conform to the standards when in effect, everyone has a free architecture license and can design what they want. Companies like NVIDIA and Western Digital have already stated that they are building custom RISC-V cores into their products.

**SiFive on RISC-V**

So here’s where SiFive comes in. SiFive is the biggest ‘we design RISC-V cores’ company in the market, partly because the founders of SiFive created the RISC-V architecture, but also because they’ve been around the longest and had the most investment. SiFive has created a number of cores, and in our pre-briefings stated that over a billion Si-Five cores have been shipped in over 100+ products. The most powerful of their scalar ‘Performance’ cores is the P650 that was announced late last year, which SiFive reported as having a ‘performance-per-area’ advantage over the Cortex-A77 found in 3 year old smartphones. The design cycles of these cores means that we won’t actually see any in silicon until 2023, indicating just how far RISC-V still has to go.

Alongside the scalar cores, SiFive also builds vector cores called ‘Intelligence’. A customer of SiFive is Tenstorrent, a chip design company focusing on scale-out AI training and inference hardware – SiFive announced last year that its upcoming chip will use SiFive’s X280 cores, which integrate that level of vector processing.

Tenstorrent says these cores will assist machine learning tasks by providing additional mid-layer compute where needed.

SiFive was officially presented to the world in 2015, with its first Series A funding round of $5m led by Sutter Hill Ventures. Almost every year since, the company has had another investment round, building capital and simultaneously expanding both the number of employees as well as the number of cores on offer. The key investors worth mentioning here are the investment arms of other companies in the ecosystem – Qualcomm Ventures was the lead investor in the $65.4m Series D round, and SK Hynix was the lead investor in the $61M Series E round. In Series E, Qualcomm increased their investment, but also Intel Capital and Western Digital Capital got involved. In this announcement today, Samsung Ventures is also being announced as a previous investor, as well as AMD through its recent acquisition of Xilinx Ventures. **Having Intel, AMD, Qualcomm, SK Hynix, Samsung, and Western Digital onboard as investors can not be understated.**

These are technically investment firms, not research collaborations, but in my visit to the Intel Capital yearly update event a couple of years ago, investment can also come with technical collaboration, as these companies do want to see their investment succeed. For example, Intel has already enabled investment in RISC-V platform development, and will be developing the P550 core in Intel 4 (EUV) called Horse Creek. **Horse Creek is currently in production, set for customer trials by end of year, marking what is potentially Intel’s first EUV-based retail silicon.**

The latest round of funding for SiFive is being announced today, Series F, and represents a $175m investment in the company. This would bring SiFive’s total investment up to $365m. On top of this, last week SiFive sold its OpenFive business (which helped customers design ASIC silicon) for $210m cash. SiFive has stated that this extra funding will go towards hiring, core development, and the software ecosystem, building on the design wins with over 100 customers according to the press release. These cover all the major ecosystems already: embedded, automotive, client computing, datacenter, hyperscale, mobile. While they’re not being used for high-performance applications quite yet, it seems that some companies are finding these cores more versatile than microcontrollers.

In our discussions with SiFive’s CEO Patrick Little, he stated that one of the key drivers for all this in place was actually NVIDIA’s attempted acquisition of Arm. At the time, as he explains, companies invested in Arm realized that they needed an out should Arm ever go behind closed doors or get more restrictive, and as a result a surge of interest entered the RISC-V ecosystem, as well as for SiFive’s cores. Even though that deal is kaput, Patrick said that the interest didn’t wane, as these companies now have that mindset that a multi-vectored strategy is needed, and are continuing to invest in RISC-V. Patrick pointed to Intel’s recent joining of RISC-V International and the new ecosystem being put in place as a prime example.

With that in mind, we were told that a lot of the current interest in SiFive’s offerings is actually in the higher performance hardware. The vector processor line, designated by an X or the name ‘Intelligence’, is apparently where over half of the company’s spend is directed right now. That’s despite the fact that the vector cores aren’t actually in anything yet – the biggest announcement so far has been that Tenstorrent announcement, but Patrick told us that more of the SiFive teams and resources are being pumped into that area because customers are demanding it. These cores are reportedly already giving outsized returns, and even though a lot of the companies could go and build their own, Patrick says they are turning to SiFive based on the expertise and support they provide.

If we put that on a scale of funding compared to other companies in the space, here’s my AI Pure Play funding (plus select others) graph showing where SiFive is.

SiFive now has $365.5m in funding, putting it around the same area as Ampere Computing (who make the Ampere Altra CPU), Groq, and more than Nuvia from when it was acquired by Qualcomm.

A lot of people are secretly hoping that the RISC-V ecosystem gets a lot of big boosts as it allows companies in this space to be more open, and it seems there is an appetite at least for these dedicated core license vendors, like SiFive, to build cores that go into a lot of other things – even if for general high-performance there is still a few hurdles to climb.

Post by Dr. Ian Cutress

Analyst, More Than Moore

Influencer, [TechTechPotato](http://www.techtechpotato.com)

If you like our articles and journalism and you want to support us in our endeavors then consider heading over to our [Patreon](https://www.patreon.com/ChipsandCheese) or our [PayPal](https://www.paypal.com/donate/?hosted_button_id=4EMPH66SBGVSQ) if you want to toss a few bucks our way or if you would like to talk with the Chips and Cheese staff and the people behind the scenes then consider joining our [Discord](https://discord.gg/TwVnRhxgY2).