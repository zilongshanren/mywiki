---
title: 'AMD’s EPYC 7J13: Zen 3 Customized'
url: https://chipsandcheese.com/p/amds-epyc-7j13-zen-3-customized
author: Chester Lam
published: '2023-06-28'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# AMD’s EPYC 7J13: Zen 3 Customized

Recently, curiosity drove me to do some microbenchmarking on Lambda Cloud’s A100 instance. That A100 instance is powered by a “AMD EPYC 7J13 64-Core Processor”. AMD’s site does not mention this SKU, nor is it listed on [Wikipedia’s Epyc page](https://en.wikipedia.org/wiki/Epyc#Third_generation_Epyc_(Milan)). lscpu claims it runs at 2.45 GHz, which is probably a base clock. Integer addition latency suggests the CPU boosts to 3.24 GHz.

The Epyc 7J13’s cores appear to be based on Zen 3, since cpuid info identifies it as family 0x19, model 0x1, and stepping 0x1. However, L2 latency is significantly higher at 20 cycles, compared to 12 cycles on typical Zen 3 cores. Increased L2 latency could be a compromise to reduce power consumption where maximum CPU performance is not required. On a GPU cloud instance, you’re paying for massive GPUs. The CPU cores are relegated to management tasks and perhaps a bit of computation not suited to GPUs. A L2 latency hit could be a worthwhile tradeoff if it lowers power consumption at a slight performance cost.

Beyond L2, we see slightly higher L3 cache latency too. However, L3 latency is probably only higher because it takes longer to check L2 on the way. Other aspects of the core are normal for a Zen 3 core. L2 bandwidth is unaffected. Instruction throughput and latencies look similar to regular Zen 3’s for basic operations.

Multithreaded bandwidth looks decent. With the 30 threads (15 cores) exposed to the VM, we see 1.7 TB/s of L3 bandwidth and 123 GB/s of memory bandwidth.

AMD is no stranger to customizing their core architecture for different applications. Zen 2 got its FPU cut down in Sony’s PS5. Zen 4 got re-implemented in a more space-efficient form in Bergamo. AMD’s Epyc 7J13 is another example of the company’s ability to customize one core architecture to fit different applications. Products like the Epyc 7J13 shows there’s a lot of room to tweak one architecture for different use cases, rather than create totally different architectures (like Golden Cove and Gracemont).

If you like our articles and journalism, and you want to support us in our endeavors, then consider heading over to our [Patreon](https://www.patreon.com/ChipsandCheese) or our [PayPal](https://www.paypal.com/donate/?hosted_button_id=4EMPH66SBGVSQ) if you want to toss a few bucks our way. If you would like to talk with the Chips and Cheese staff and the people behind the scenes, then consider joining our [Discord](https://discord.gg/TwVnRhxgY2).