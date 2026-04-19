---
title: 'An EPYC Exclusive for Azure: AMD''s MI300C'
url: https://chipsandcheese.com/p/an-epyc-exclusive-for-azure-amds
author: George Cozma
published: '2024-12-02'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# An EPYC Exclusive for Azure: AMD's MI300C

### The pun was just too good to resist.

Hello you fine Internet folks,

At SC24 we stopped by the Azure Booth to check out their new HBv5 VMs powered by the AMD EPYC 9v64H CPU.

Each AMD EPYC 9v64H CPU physically have 96 Zen 4 cores along with 128GB of HBM3E.

Four of these 9v64H CPUs are then put into a HBv5 VM which has a combined 352 Zen 4 cores (88 Zen 4 cores per EPYC 9v64H CPU) with SMT disabled on the Zen 4 cores. Fun note, this is the first AMD CPU to support a quad socket configuration since the Opteron days yet the quad socket set up has double the total Infinity Fabric bandwidth compared to a standard EPYC server. Moving to the memory system and the 512GB of HBM3E delivers nearly 7TB/s of memory bandwidth across the four CPUs.

Each HBv5 VM is a single-tenant design which means that each server only has one VM running at any given time.

We can’t wait to get our hands on this VM with the EPYC 9v64H when they become generally available.

If you like our articles and journalism, and you want to support us in our endeavors, then consider heading over to our [Patreon](https://www.patreon.com/ChipsandCheese) or our [PayPal](https://www.paypal.com/donate/?hosted_button_id=4EMPH66SBGVSQ) if you want to toss a few bucks our way. If you would like to talk with the Chips and Cheese staff and the people behind the scenes, then consider joining our [Discord](https://discord.gg/TwVnRhxgY2). And if you like our video content then please subscribe to the [Chips and Cheese Youtube channel](https://www.youtube.com/@chipsandcheesecc).

No GPU? Then what is the instinct for?

4 * 96 = 384 cores. Where are the missing 32 cores since the server has ony 352 cores? Spares?