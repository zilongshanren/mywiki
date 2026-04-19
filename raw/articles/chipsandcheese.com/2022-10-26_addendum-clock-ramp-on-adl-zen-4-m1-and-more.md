---
title: 'Addendum: Clock Ramp on ADL, Zen 4, M1, and More'
url: https://chipsandcheese.com/p/addendum-clock-ramp-on-adl-zen-4-m1-and-more
author: Chester Lam
published: '2022-10-26'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

We recently released an article on how quickly CPUs increased their clocks from idle, and received criticism in that it didn’t include CPUs newer than Kaby Lake. That was because I just didn’t have access to such systems, but since that article, we’ve gotten test data from several people in our community. Thanks to them, we have a follow up to share.

Clock frequency ramp behavior is influenced by a variety of factors including voltage increases and operating system behavior. We’re not trying to see how fast a CPU can change clock frequency. It’s clear that a CPU can change voltage extremely quickly under special circumstances. For example, Skylake-X can clock down a couple hundred megahertz in about a tenth of a millisecond to deal with AVX-512 instructions. In that scenario, the CPU only had to make a small frequency change, was already running at full load voltage (so the voltage change is small), and isn’t reacting to a power state change command from the OS. But we’re not looking at that scenario. Rather, we’re looking at how fast a CPU gets to high clocks from idle under typical conditions.

It is a bad idea to take this graph, repost it, and claim Piledriver boosts the fastest. Because some of these results are for uh, atypical conditions

We’ll also present some results that aren’t representative of typical behavior, just because they’re fun to look at.

Intel’s Alder Lake

Alder Lake is Intel’s current flagship desktop and mobile architecture. Here, we have results from the Core i5-12600, a midrange Alder Lake SKU that only features 6 Golden Cove cores. At stock settings, Alder Lake behaves like other recent Intel CPUs with “Speed Shift” enabled. The CPU manages its own frequency with the OS out of the loop, resulting in faster response times. Like Skylake, Alder Lake reaches max boost in just over 5 ms. The i5-12600 actually boosts a hair faster than the i5-6600K, even though the former clocks almost a gigahertz higher.

If core voltage is held at a static 1.29V to enable BCLK overclocking, the CPU goes from idle clocks to over 5 GHz in around half a millisecond. Strangely, it then drops back to idle clocks for a couple milliseconds before clocking back up again.

Also, Alder Lake idles at 600 MHz, while earlier Intel client desktop CPUs tended to idle at 800 MHz. Obviously, it idles a bit higher with a BCLK overclock applied.

Intel’s Rocket Lake

In the years after Skylake, Intel failed over and over again to bring a 10nm product to desktop. The basic Skylake architecture therefore continued to serve in Intel’s flagship desktop chips until Intel backported Sunny Cove to 14nm, creating the Cypress Cove core. Rocket Lake was then launched with up to eight Cypress Cove cores in 2021, earning the distinction of being the first non-Skylake desktop chip from Intel in over five years.

With the default “balanced” power plan on Windows, Rocket Lake behaves like Skylake. That is, maximum speed is reached shortly after 5 milliseconds. If the “power saver” power plan is used, maximum clock is reached after just 3.6 ms. However, maximum clock is slightly lower with the power saver plan.

In both cases Rocket Lake boosts to extremely high clocks in a very short time.

Intel’s Tiger Lake

Tiger Lake is basically Intel’s Sunny Cove architecture implemented on an improved 10nm process, with a larger L2 cache and a non-inclusive L3. Usually, Tiger Lake appears in quad core form in a variety of laptops and ultrabooks. But here, we’re testing an 8-core Tiger Lake variant, as implemented in an Intel NUC.

The Core i9-11900KB boosts to a very high 4.9 GHz, and like other “Speed Shift” enabled Intel platforms, does so shortly after 5 ms. It doesn’t stop at any intermediate frequencies.

In power saver mode, clocks don’t spike up until about a millisecond later. Unlike Rocket Lake, Tiger Lake reaches the same high clocks in Power Saver mode.

Intel’s Cannon Lake, and Kaby Lake with Speed Shift

Cannon Lake is Intel’s 10nm shrink of Kaby Lake. Both architectures are based off the Skylake architecture. Cannon Lake notably adds AVX-512 support, though the architecture never really came to market. It only released in one dual-core SKU, with a non-functional iGPU. And that’s what we tested. We also re-tested the Kaby Lake chip, using ThrottleStop to forcibly enable “Speed Shift” even though HP’s BIOS had no option for it.

With “Speed Shift” enabled, Kaby Lake shows very similar behavior to Skylake, reaching maximum clocks a hair after 5 ms. It actually ramps frequency a bit faster than original Skylake, despite clocking 600 MHz higher.

Cannon Lake also responds very quickly, but stops just short of its maximum clock in the intial clock ramp step. It hits 2.89 GHz after 5.43 ms, then increases frequency in steps before reaching 3.2 GHz at 14.27 ms. Technically, it’s a bit slower than other “Speed Shift” enabled chips, though it should still feel pretty responsive. Most importantly, it’s much faster than responding to a power state change command from the OS.

Intel’s Broadwell

Broadwell is a 14 nm shrink of Haswell with a few minor changes to the core architecture. Unlike Haswell, Broadwell never made its presence felt on the desktop market. It released in a couple of eDRAM enabled SKUs that provided competitive performance in games, but couldn’t clock high enough to beat existing Haswell parts in most applications. Since it comes in just before Skylake, Broadwell is the last generation of Intel desktop parts before “Speed Shift” was introduced. Using Windows’s default “Balanced” power plan, Broadwell jumps to a moderate 2.1 GHz after 15 ms, then finally reaches maximum clocks after 48 ms. With the “High Performance” power plan, it goes straight to maximum clocks at 15.89 ms.

Broadwell’s behavior therefore sits right between Haswell’s and Skylake’s. Without “Speed Shift”, Broadwell can’t shoot to maximum frequency after a few milliseconds. But it can reach an intermediate frequency in half the time it takes for Haswell to do so, and can hit maximum clocks about 25% faster than Haswell too.

Haswell’s clock ramp behavior for comparison

With the “High Performance” power plan, Broadwell doesn’t exhibit the sub-millisecond boost speed that we see on Piledriver and Alder Lake. The “High Performance” plan doesn’t hold voltages high on Broadwell, so that could be a factor. But it does show that Broadwell can go straight from idle frequencies to 3.7 GHz without intermediate steps, providing better responsiveness than previous generations even if it’s not quite up to what “Speed Shift” can achieve.

AMD’s Excavator

Excavator is the last architecture in AMD’s line of cores named after heavy construction equipment. By the time Excavator showed up, AMD had given up on directly competing with Intel on the desktop market. Instead, AMD went after mobile and smaller form factor systems, by using dual module configurations equipped with relatively powerful integrated GPUs. The A12-9800 represents one of these APUs.

Out of the box, Excavator behaves a bit like Haswell, though it moves to a much higher intermediate frequency of 3.48 GHz. The core settles on its maximum 4.2 GHz after 62 ms.

With the “High Performance” power plan set, Excavator boosts faster and goes straight to its maximum 4.2 GHz in about 16 ms. In this mode, it still idles at a pretty low 0.847V, making it a good option for anyone who wants slightly better responsiveness.

AMD’s Rembrandt

AMD’s “Zen 3+” Rembrandt chip on TSMC N6 consisted of a complete redesign of the uncore that had been present on both Renoir and Cezanne, along with tweaks to the core Zen 3 design and physical layout that primarily improved power efficiency. As of writing, Rembrandt is a mobile-only design.

As a quick prescript, the following results could only be consistently reproduced on Linux. Running the same test on Windows produced significantly more variable results.

While connected to AC power, Rembrandt wastes very little time before reaching its max boost clock of 4.5 GHz, taking just under 1 ms to begin ramping from its initial clock of 1.4 GHz. On battery, it starts at the same clock and reaches the same boost clock, though it takes 1.5 ms to do so – only slightly longer. This is the fastest stock clock ramp on the chart, though the possibility exists that the cores are at a higher-than-normal voltage at idle, which can’t be ruled out without the ability to check Zen 3 core voltages on Linux.

AMD’s Zen 4

AMD’s Zen 4 is an evolution over their successful Zen 3 architecture, and takes advantage of a new process node to offer both higher clock speeds, and larger core structures that provide a performance per clock boost.

Zen 4 idles at a somewhat high 3 GHz, then boosts to its maximum clock of 5.7 GHz just after 11 ms. At first glance, this is a touch slower than older AMD chips, like the Zen 2 based Renoir. However, Zen 4’s relatively high idle clock should provide very good responsiveness right off the bat.

Apple’s M1

Apple’s M1 chip is notable for being the first laptop and small form factor desktop CPU to be implemented on TSMC’s 5 nm process. Its four Firestorm cores feature a very wide and deep architecture running at low clocks, with a heavy focus on power efficiency.

Unlike other architectures we’ve tested, Apple’s cores show a lot of run-to-run variability. Generally, the Firestorm cores start increasing their clocks after about 20 ms, and gradually increase frequency until they reach their maximum 3.2 GHz clock slightly after 100 ms. Sometimes, they’ll hit a moderate speed just above 2 GHz early on, after 20 to 30 ms.

This clock ramp behavior is somewhat reminiscent of what we saw on Snapdragon 821 when running off battery. Like Qualcomm, Apple is possibly opting for a gradual frequency to save power. But Apple does ramp clocks much faster than Qualcomm: there’s a big difference between 100 ms on Apple, and nearly 400 ms on Qualcomm.

Snapdragon 821 clock behavior from our previous article, for comparison. Qualcomm also ramps clock frequencies slowly, except on the big cores when the device is plugged in and fully charged

Still, I find this behavior a bit out of place. Unlike the Snapdragon 821 in the LG G6, the M1 in the Mac Mini will never be running off battery power. There’s no need to save every last watt if you’re plugged into the wall, so I’m surprised that we don’t see a more immediate clock ramp. For contrast, the Snapdragon 821 hits its maximum clock of 2.34 GHz after 19.6 ms when the phone is fully charged and running off AC power. Maybe Apple didn’t get a chance to implement different boosting behavior for tablets, ultrabooks, and small form factor desktops. But we don’t have other M1 implementations to test, so we can’t verify that theory.

Thanks to Dougall for testing on his M1 Mac Mini, and providing the M1 Max results below.

Apple’s M1 Max

M1 Max adds another quad core Firestorm cluster, drops the little (Icestorm) core count to two, and massively increases the GPU size. Unlike the M1, M1 Max is designed for higher power laptops and the Mac Studio.

It’s no surprise that the M1 Max boosts faster, but it still doesn’t increase clocks quite as fast as the newest AMD and Intel chips. On the best runs, it reaches 2.67 GHz in just over 10 ms. That’s not as fast as Intel’s “Speed Shift” enabled CPUs, and is slightly behind AMD’s Renoir, which boosts above 4 GHz before the 10 ms mark. But it should still be enough to offer good responsiveness, and is much better than sitting around 1 GHz after 10 ms. After that, M1 Max stays at 2.67 GHz if it’s set to “Low Power”, or slowly ramps to 3.23 GHz if “High Power” is set.

On one run, the M1 Max reached 3.23 GHz after 43 ms, which makes it slightly faster than older CPUs that relied on the OS to issue power state change commands. But on some runs, M1 Max took nearly 100 ms to reach 3.2 GHz and gradually ramped frequency like M1. With such testing variation, it’s hard to paint a clear picture of M1 Max’s frequency ramp behavior.

Apple’s power plans also behave differently from Windows and Android: clock ramp behavior doesn’t change depending on whether the device is plugged in. The only thing that matters is whether the system is set to “High Power” or “Low Power”. In “Low Power” mode, M1 Max appears to be capped to 2.67 GHz, but boosting behavior doesn’t change beyond stopping at 2.67 GHz.

Does Linux’s CPU Frequency Governor Matter?

We’ve seen before how frequency ramp behavior can be impacted by various settings. For example, setting the Windows power plan’s minimum processor state to 100% causes Piledriver to idle at a relatively high 1.3 V, resulting in incredibly fast frequency changes. When Alder Lake is given a static core voltage to enable a BCLK overclock, it also boosts very quickly and hits maximum frequency in less than a millisecond. Certain OS settings can hold CPU frequency at the maximum setting all the time, making frequency change behavior irrelevant (as no change ever occurs).

But all of those options come with drawbacks, because keeping voltage high during idle operation means the CPU is drawing extra power while doing nothing. So, what if we change the scaling governor in Linux? The scaling governor controls CPU frequency scaling, so perhaps another one would make clock speeds ramp faster. We couldn’t change it in Android without root, and it didn’t matter for Skylake and other more modern CPUs that don’t require OS commands to initiate a frequency change. So let’s have a look at the Amlogic S922X, implemented in an Odroid N2 SBC. This SoC also runs in some TV boxes, and implements two Cortex A53 cores that run at up to 1.9 GHz, and four Cortex A73 cores that run at up to 2.2 GHz.

Changing the governor around has very little effect. There are some minor differences around how fast certain clock speeds are reached, but setting a different frequency governor isn’t likely to make a noticeable difference. Technically, the “interactive” governor hits maximum clock speeds the fastest, but “ondemand” and “schedutil” are only about 10 ms behind. If we look at intermediate frequencies, “ondemand” seems to make bigger jumps early on, and maintains a clock speed advantage from 30 to 50 ms.

Another curious observation is that clock speed often appears to dip before the CPU jumps to a higher frequency. I wonder if some CPUs have to halt for a brief moment before making frequency transitions. This test infers clock speed from how long it takes to execute a known number of dependent integer additions; so a core that appears to run at 200 MHz over a 2.44 ms interval (as the A55 did just before hitting 1.9 GHz), may have been running at 1.5 GHz for a third of a millisecond, and did nothing for about 2 ms.

Final Words

For the most part, modern CPUs can clock up so fast that responsiveness isn’t a big issue. AMD and Intel have both developed mechanisms that let the OS hand power state control to the CPU, which speeds up frequency ramp because the OS isn’t part of the boost behavior control loop. Intel CPUs since Skylake can take advantage of “Speed Shift” to reach their maximum boost clocks in 5 ms or less. AMD CPUs can do the same, taking a little more or a little less time depending on whether you’re looking at Zen 2 or Zen 3. If you have one of these CPUs, there’s really no reason to run it at maximum clock all the time, or set a static voltage to make it boost faster.

CPUs without pure hardware control over speed boosting can still hit their top clocks pretty quickly if the OS is set to prioritize performance . Windows’s “High Performance” power plan probably makes it request the P-State without delay. Broadwell and Excavator both reach their highest boost clocks shortly after 15 ms in this mode, without sacrificing low idle voltages.

Apple may have hardware control over speed boosting, since M1 Max is able to hit an intermediate frequency step in just over 10 ms. Apple’s M1 (not Max) stands out by retaining a gradual boost policy, but I suspect we won’t see more of that on high performance desktop devices going forward. CPUs seem to be trending away from slow, gradual boost policies. And that’s especially true of higher power, higher performance devices.

If you like our articles and journalism and you want to support us in our endeavors then consider heading over to our Patreon or our PayPal if you want to toss a few bucks our way or if you would like to talk with the Chips and Cheese staff and the people behind the scenes then consider joining our Discord.

Credits

Thanks to cha0s for testing Broadwell, Rocket Lake, Cannon Lake, Tiger Lake, and Excavator! The tests were run on Windows 10 22H2 with most background tasks disabled. Thanks to Titanic for setting up an AMD 7950X Zen 4 system for testing along with our wonderful Chips and Cheese patrons for letting us afford a 7950X system. Thanks to davidbepo for testing and contributing the results. Alder Lake testing was done on Linux. Additional thanks to serebit for testing Rembrandt – this run was performed on EndeavourOS, using the schedutil frequency governor.