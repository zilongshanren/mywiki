---
title: 'Arm at HC35 (2023): CSS-Genesis'
url: https://chipsandcheese.com/p/arm-at-hc35-2023-css-genesis
author: Chester Lam; Joshua Gregory
published: '2023-09-13'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# Arm at HC35 (2023): CSS-Genesis

It would be a rather large understatement to say that Arm has strong popularity in general purpose CPU cores. Arm has been going forward full speed with introducing successive generations of new cores, in both the Cortex line of end-user oriented products and the highly popular Neoverse line of enterprise-grade products.

But cores alone don’t give you a functional system. Arm therefore develops a myriad of other IP blocks that integrators can use to produce a complete design. For example, their DSU-110 and CMN-700 provide interconnects to link cores with each other and other system components. Their MMU-700 handles virtual to physical address translation for peripherals. A [GIC-700](https://developer.arm.com/Processors/CoreLink%20GIC-700) can provide interrupt controller functionality.

However, customers like MediaTek and Qualcomm still have to integrate everything necessary to create a complete chip. Configuring all of those separate components, linking them together, and validating the the whole thing requires significant effort and time. In contrast, AMD and Intel create ready-made chips and control a large part of the platform design, letting customers hit the ground running. Therefore, the time to market for a typical Arm core design tends to be significantly longer than a comparable design from the x86 duopoly. A great example is the Neoverse N2 core design, which was announced by Arm in April 2021 but didn’t appear in a physical chip (to the best of our knowledge) until the launch of [the Alibaba Cloud Yitian 710, which we covered previously](https://chipsandcheese.substack.com/p/arms-neoverse-n2-cortex-a710-for-servers).

Arm has now taken a step closer to the x86 duopoly with the launch of CSS-Genesis N2, a new design service which Arm is marketing as a way to reduce development time for both general purpose processors and custom accelerators. Today, we’re taking a look at Arm’s CSS-Genesis as presented in Hot Chips 35.

## Reducing Time to Market

CSS-Genesis allows Arm customers to obtain a pre-made, validated RTL design which can be implemented into silicon much faster than the typical process for purchasing individual core designs. As part of their presentation, Arm claimed that a typical CSS-Genesis customer could see a saving of 80 engineering years (collective time spent by a team of engineers) versus a comparable IP license (where individual core designs and other components are purchased and assembled by the customer) which customers have had to use previously.

Arm’s CSS-Genesis N2 is a compute subsystem with up to 64 Neoverse N2 cores, four DDR5 memory controllers, and 64 PCIe 5.0 lanes. It utilises Arm’s CMN-700 mesh interconnect to tie all of those components together, and Cortex M7 microcontrollers (SCP and MCP) to manage clocks and voltage. An IO block is also included featuring an interrupt controller (NI-700), system MMU (MMU-700), and other address translation logic to enable CSS-Genesis customers to integrate additional on-chip accelerators and connect PCIe devices. All of this has been tested by Arm on TSMC’s N5 process to obtain area metrics and other implementation characteristics. The result is a ready-made processor block which can be implemented as a standalone chip or integrated into a larger processor with other custom accelerators, such as those for machine learning or image processing.

For a 64 core design with the maximum cache configuration, Arm quotes that cores, interconnect and last level cache (LLC) occupy an estimated 198 mm2 when implemented using TSMC’s N5 process. The CMN-700 mesh is configured with 32 core tiles, each of which occupies 6.2 mm2 and contains two N2 cores alongside two 1 MB slices of LLC. For perspective, an AMD Zen 4C core on its own occupies 2.48 mm2 of area, and a Zen 4 CCD chiplet with 8 Zen 4 cores, 32MB LLC and interconnects occupies 69.5 mm2. If we assume a 16 core Bergamo chiplet is the same size as a regular Zen 4 chiplet, then Bergamo takes around 40% more area to deliver 16 cores. Part of this is because Zen 4C is a substantially more capable core than Neoverse N2, and Bergamo has twice as much L3 cache per core. However, AMD also uses some area for cross-chiplet interfaces and microcontrollers which are an optional part for CSS-Genesis N2.

In any case, Arm’s CSS Genesis should require less silicon and thus cost less than Bergamo, making it a compelling solution for customers that can run their workloads on ARM and don’t need Bergamo’s higher performance.

### Supporting Components

To no one’s surprise, Arm has stuffed CSS-Genesis with in-house components. The MMU-700, GIC-700, NIC-450, and CMN-700 are all made by Arm. Cortex-M7 cores manage power, clocks, and voltage.

Pre-configuring and integrating all of these components will save time and engineering effort for a CSS-Genesis customer. Additionally, it provides an incentive to use Arm’s IP rather than blocks from somewhere else. This probably isn’t very important for the server market where blocks other than the CPU and interconnect play a minor role in system performance. However, a hypothetical CSS-Gensis design for mobile would be very interesting as it could let Arm gain more market share for their Mali GPUs.

### Chiplet Scaling

CSS-Genesis N2 stops at 64 core configurations, which is a bit behind Ampere Altra’s 80 cores, and significantly behind AMD’s 96 to 128 core Zen 4 parts. To enable higher core count designs, CSS-Genesis N2 can be used with a chiplet strategy similar to that of AMD’s Magny Cours (K10 server) or Interlagos (Bulldozer server). A socket can have two CSS-Genesis N2 dies, bringing per-socket core count to 128.

A dual socket configuration can provide 256 cores per node, matching AMD Bergamo’s core count. Unlike other platforms from Intel, and AMD in years past, CSS-Genesis N2 does not scale past 2 socket platforms.

128 cores is a lot, but Bergamo’s Zen 4c cores are likely to punch harder than N2, thanks to their beefy vector units and larger out of order engines. Intel’s future Sierra Forest is likely to come with 144 cores per socket, and Ampere’s Siryn scales to 192 cores.

### CSS-Genesis’s Targets

CSS-Genesis’s configurations target a wide range of markets ranging from servers to smaller applications like smart switches.

Targeting so many markets demands flexibility, so CSS-Genesis offers 24, 32, and 64 core count options. The smallest 24 core option takes up 53 mm2, and should bring down costs when high CPU throughput isn’t important. I suspect even 24 cores would be too much for something like a smart NIC, where dedicated chips or FPGAs are expected to do heavy lifting. Perhaps we’ll see even lower core count options in the future.

## Final Words on CSS Genesis

CSS-Genesis is a compelling service which will likely enable new generations of Arm core designs to reach the market in significantly less time than existing ones. It could offer a lot of value to start-ups and hyper-scalers alike, enabling them to diversify their compute infrastructure with new designs of (mostly) their own making. However what remains to be seen is how strong the demand for this service will be, with an increasingly competitive environment in this space proving to be the biggest risk looking forward. Hyper-scalers will be weighing products like AMD’s Bergamo against the CSS-Genesis offering and considering what benefits if any it may offer versus the complete platform offered by AMD. Whilst Arm did disclose they have customers for CSS-Genesis already, they did not disclose any names. Given what we know of the Yitian 710, there is certainly some merit to speculation that it was built using this service.

In discussions with Arm, there is an intention for this service to expand in the future if demand is present. Whilst they haven’t been specific in what ways this might be, we can imagine that they would likely look to expand to other Neoverse designs such as V2 or other future cores. This could certainly increase the potential market for the service, but it remains to be seen if Arm will take a larger leap and attempt to replicate this service for consumer, IoT or embedded markets. We would like to see Arm offer support for higher core counts in the future given the pace of progress in this area from Intel and AMD. If CSS-Genesis does well, we may even see Arm taking the next step and offering semi-custom finished silicon products as a service in future. In any case, CSS-Genesis increases Arm’s competitiveness within the general purpose server CPU market and brings them one step closer to matching the capability of Intel, AMD and existing partners like Qualcomm.

We’d like to thank Arm for the briefings provided to us and the presentations at Hot Chips and we look forward to seeing future designs and service offerings.

If you like our articles and journalism, and you want to support us in our endeavors, then consider heading over to our [Patreon](https://www.patreon.com/ChipsandCheese) or our [PayPal](https://www.paypal.com/donate/?hosted_button_id=4EMPH66SBGVSQ) if you want to toss a few bucks our way. If you would like to talk with the Chips and Cheese staff and the people behind the scenes, then consider joining our [Discord](https://discord.gg/TwVnRhxgY2).