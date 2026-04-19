---
title: 'Fujitsu''s Monaka CPU: ARMv9, SVE2, and 3D Stacking'
url: https://chipsandcheese.com/p/fujitsus-monaka-cpu-armv9-sve2-and
author: George Cozma
published: '2024-12-13'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# Fujitsu's Monaka CPU: ARMv9, SVE2, and 3D Stacking

### Designed for the datacenter and due in 2027

Hello you fine Internet folks, today we are going back to SC24 with a short about Fujitsu’s upcoming Monaka CPU.

Fujitsu’s CPUs are quite prevalent in the HPC space with their prior gen A64FX CPU powering the former world’s number 1 Supercomputer, Fugaku. However, Monaka is not a direct replacement for A64FX due to Monaka not supporting HBM along with Monaka being more targeted to the general datacenter market.

Moving to the general layout of Monaka, and there is a resemblance to AMD’s EPYC series of CPUs with a central IO die and disaggregated SRAM and compute. And like AMD’s 2nd generation of V-Cache, the SRAM is below the compute in order to improve thermal management. Unlike AMD’s EPYC CPUs, the IO and the compute are placed above an interposer to allow for a higher bandwidth interconnect between the compute dies and the IO dies.

Each Monaka CPU will have up to 144 cores spread across 4 compute chiplets each with 36 cores on them and they will be fabbed on a 2nm process. The disaggregation of the SRAM and the cores means that the total 2nm area is less then 30% of the total silicon area.

As for the IO, there will be 12 channels of DDR5 which will likely provide over 600GB/s of memory bandwidth assuming Monaka supports DDR5-6400 memory. Monaka will also support PCIe 6.0 which will have CXL 3.0 support and this whole system is aimed to be air coolable.

There haven’t been any details released about the microarchitecture of the core that is going in to Monaka but hopefully it’s a custom microarchitecture as it is always interesting to see different ways different teams approach the same general task.

Hope y’all enjoy!

If you like the content then consider heading over to the [Patreon](https://www.patreon.com/ChipsandCheese) or [PayPal](https://www.paypal.com/donate/?hosted_button_id=4EMPH66SBGVSQ) if you want to toss a few bucks to Chips and Cheese. Also consider joining the [Discord](https://discord.gg/TwVnRhxgY2) and subscribing to the [Chips and Cheese Youtube channel](https://www.youtube.com/@chipsandcheesecc).


Nice overview of chip organiztion, amazing to see MCM designs have progressed from early 90s primitive stacked and wirebonded models