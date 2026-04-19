---
title: Latency Testing is Hard (RDNA 3 Power Saving)
url: https://chipsandcheese.com/p/latency-testing-is-hard-rdna-3-power-saving
author: Chester Lam
published: '2023-06-15'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

In a previous article, we compared Infinity Cache latency between the RX 7900 XTX, and the smaller RX 7600. After further testing, some correction is in order. AMD’s RDNA 3 architecture uses aggressive power saving techniques. Part of this seems to involve lowering the Infinity Fabric clock when there aren’t a lot of outstanding requests. Unfortunately, this power saving complicates microbenchmarking, especially attempts to measure Infinity Cache latency. This will be a short post to address the issue.

RX 7900 XTX (Navi 31)

The top end RX 7900 XTX uses the Navi 31 chip, which has a chiplet setup. Navi 31’s shader array and all caches up to L2 sit on a 5 nm Graphics Compute Die (GCD). Infinity Cache and memory controllers sit on smaller Memory Cache Dies (MCDs).

From the scalar side, our initial results measured 161 ns of Infinity Cache latency. Subsequent testing with a triple monitor setup (which forces the card into a higher power state) gives a much lower 128.4 ns of Infinity Cache latency.

We see a similar pattern with vector accesses, where measured Infinity Cache latency dropped from 199 ns to 150.3 ns with the card in a higher power state. However, caches on the shader clock domain do not see a notable latency difference. That includes the L0, L1, L2, and scalar caches.

Navi 31 likely manages power states separately for the Infinity Fabric and shader array. The shader array clocks up if it has work queued up. The Infinity Fabric also checks if it has work queued up, and adjusts its clocks without regard to whether the shader array is busy.

RX 7600 (Navi 33)

The RX 7600 features a smaller RDNA 3 implementation, built on a small monolithic 6 nm die. It has a similar power saving strategy, but the effects are very different. Infinity Cache latency barely changes, with just a 14.4% increase in latency at its lower power state. VRAM latency however takes a massive jump.

Vector accesses show similar behavior, with just a 9.5% Infinity Cache latency difference depending on whether the Infinity Fabric was in power saving state. VRAM latency meanwhile more than doubles.

RDNA 3’s power saving strategy has different effects on Navi 33 and Navi 31. Navi 33’s monolithic nature may contribute.

Big and Small RDNA 3 Compared

Previously, we noted that the 7900 XTX’s Infinity Cache was a lot slower than the RX 7600’s. With the revised data, the gap is not as large. With scalar accesses, Navi 31’s Infinity Cache is roughly 9.7% slower than Navi 33’s.

Vector accesses paint a similar picture, with a 9.3% latency difference between the two RDNA 3 implementations. That places it in line with the difference between Navi 21 (RX 6900 XT) and Navi 23 (RX 6600 XT).

Surprisingly, VRAM latencies are also very similar across small and large RDNA 3 implementations.

RDNA 3 and RDNA 2 Compared

AMD introduced its large Infinity Cache in RDNA 2, so it’s interesting to see how their second generation Infinity Cache implementation compares. A slide from AMD suggests that Infinity Cache hit latency went down from RDNA 2 to RDNA 3. Even though a chiplet interface introduces a latency penalty, AMD was able to overcome that with higher clocks.

AMD’s slide, indicating that they overcame the latency penalty of a chiplet link via higher Infinity Fabric clocks

Our updated data lines up with AMD’s claim. RDNA 3’s Infinity Cache provides roughly 13.2% lower latency than RDNA 2’s for scalar accesses, when checking the same 32 MB test size.

With vector accesses, the 64 MB test size shows a 9.67% latency reduction in favor of RDNA 3. That almost exactly lines up with AMD’s common case claim.

In VRAM, the RX 7900 XTX consistently achieves better latency than the RX 6900 XT. At the 1 GB test size, the RX 7900 XTX achieves 221.24 ns and 234.55 ns access latency for scalar and vector accesses, respectively. For comparison, the RX 6900 XT gets 260 and 283.89 ns of latency for scalar and vector accesses. AMD should be proud of their achievement, as the RX 7900 XTX achieves better VRAM latency than any other big AMD GPU I’m aware of. It also puts their VRAM access latency very close to that of the RTX 4090 and GTX 1080.

Additional testing done, with more test points after 64 MB

An unresolved question is why the latency test cannot see RDNA 3’s full Infinity Cache capacity. On the RX 6900 XT, we see an inflection point at or very close to 128 MB, its advertised cache capacity. On the RX 7900 XTX, there’s an inflection point around 64 MB. Perhaps some cache capacity is reserved for fixed function units.

Final Words

Testing is hard and a lot of things can complicate testing, including boost behavior and power saving. Also, RDNA 3’s Infinity Cache outperforms its predecessor’s in every respect except for capacity.

If you like our articles and journalism, and you want to support us in our endeavors, then consider heading over to our Patreon or our PayPal if you want to toss a few bucks our way. If you would like to talk with the Chips and Cheese staff and the people behind the scenes, then consider joining our Discord.