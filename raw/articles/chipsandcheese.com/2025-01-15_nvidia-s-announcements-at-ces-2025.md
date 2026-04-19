---
title: Nvidia's Announcements at CES 2025
url: https://chipsandcheese.com/p/nvidias-announcements-at-ces-2025
author: George Cozma
published: '2025-01-15'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# Nvidia's Announcements at CES 2025

Hello you fine Internet folks,

Nvidia had a massive keynote at CES 2025 where they announced the RTX 50 series, the ConnectX-8 SuperNIC, and Project DIGITS which uses a new GB10 chip that was made in collaboration with MediaTek.

Starting with ConnectX-8, this is the newest addition to the ConnectX family of NICs which supports up to 800G line rate of InfiniBand through a single OSPF port or 400G line rate of Ethernet through 2 QSFP112 ports which allows a single ConnectX-8 SuperNIC to deliver up to 800Gb/s to the network.

What is also interesting about the ConnectX-8 SuperNIC is that it supports up to 48 lanes of PCIe Gen 6.0 using separate mezzanine cards.

Moving to the RTX 50 series and this is probably the announcement that many of you were waiting for.

Starting with the 5090 and it’s a monster of a graphics card. Based on the GB202 dies, the 5090 has 21760 CUDA cores, 2.41GHz boost clock, 32 GB of GDDR7 on a 512b memory bus that delivers nearly 1.8TB/s of memory bandwidth to the 5090. This really is a beast of a card and the 575 watt power limit shows that. Yet the Founders Edition cards are only 2 slot cards using some very clever cooling techniques. The MRSP for the 5090 Founders Edition is 1999 USD.

Moving to the 5080, and it’s basically half of a 5090. Based on the GB203 dies, the 5080 has 10752 CUDA cores, 2.62GHz boost clock, 16 GB of GDDR7 on a 256b memory bus that delivers 960GB/s of memory bandwidth. At 360 watt TDP, the 5080 doesn’t require the same cooling capability of the system that the 5080 is put into as the 5090 does. The MSRP for the 5080 Founders Edition is 999 USD.

The RTX 5070 Ti uses the same GB203 die as the 5080 but with 8960 CUDA cores, 2.45GHz boost clock, the same 16GB of GDDR7 on a 256b memory bus that delivers just under 900GB/s of memory bandwidth. The TDP for the 5070 Ti is 300 watts and the MSRP starts at 749 USD but there is no Founders Edition of the 5070 Ti.

And last but not least, the RTX 5070 uses the GB205 die and has 6144 CUDA cores, 2.51GHz boost clock, 12 GB of GDDR7 on a 192b memory bus that delivers 672GB/s of memory bandwidth. The TDP of the 5070 is 250 watts with the MSRP of the Founders Edition is 549 USD.

Now moving on to the last announcement of hardware that Nvidia announced at CES 2025, this was the one that excited me the most and that was Project DIGITS.

Project DIGITS is a very small mini PC that is powered by the brand new GB10 Grace-Blackwell chip that was a collaboration with MediaTek. The GB10 Chip has 10 ARM Cortex X925 cores and 10 ARM Cortex A725 cores that are attached to a Blackwell GPU that is capable of 1 Petaflop of FP4 compute. The GB10 is paired with 128GB of LPDDR5X memory along with a 4TB SSD and a ConnectX NIC. Project DIGITS start at 3000 USD and will be available starting in May of this year.

If you like the content then consider heading over to the [Patreon](https://www.patreon.com/ChipsandCheese) or [PayPal](https://www.paypal.com/donate/?hosted_button_id=4EMPH66SBGVSQ) if you want to toss a few bucks to Chips and Cheese. Also consider joining the [Discord](https://discord.gg/TwVnRhxgY2) and subscribing to the [Chips and Cheese Youtube channel](https://www.youtube.com/@chipsandcheesecc).

I'm a bit confused by those 48 PCIe6 lanes - doesn't an x16 PCIe6 link already do 121GB/s (net)? That's what Wikipedia says anyway. Obviously you need to allow some headroom - but even x32 would leave well over 50% of theoretical bandwidth to spare?

We need more details on the SM design - more and more details are coming out that it's all Ada silicon, which is an Ampere by itself. 0% IPC gain