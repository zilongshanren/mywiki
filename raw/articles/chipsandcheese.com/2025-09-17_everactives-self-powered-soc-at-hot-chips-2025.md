---
title: Everactive’s Self-Powered SoC at Hot Chips 2025
url: https://chipsandcheese.com/p/everactives-self-powered-soc-at-hot
author: Chester Lam
published: '2025-09-17'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# Everactive’s Self-Powered SoC at Hot Chips 2025

Hot Chips 2025 was filled with presentations on high power devices. AI can demand hundreds of watts per chip, requiring sophisticated power delivery and equally complex cooling. It’s a far cry from consumer devices that must make do with standard wall outlets, or batteries for mobile devices. But if working within a wall outlet or battery’s constraints is hard, it’s nothing compared to working with, well, nothing. That’s Everactive’s focus, and the subject of their presentation at Hot Chips 2025.

Everactive makes SoCs that power themselves off energy harvested from the environment, letting them operate without a steady power source. Self-powered SoCs are well suited for large IoT deployments. Wiring power to devices or replacing batteries complicates scaling device count, especially when those IoT devices are sensors in difficult to reach places. Generating energy off the environment is also attractive from a sustainability standpoint. Reliability can benefit too, because the device won’t suffer from electrical grid failures.

But relying on energy harvesting brings its own challenges. Harvested energy is often in the milliwatt or microwatt range, depending on energy source. Power levels fluctuate depending on environmental conditions too. All that means the SoC has to run at very low power while taking measures to maximize harvested power and survive through suboptimal conditions.

# SoC Overview

Everactive’s SoC is designated PKS3000 and occupies 6.7 mm² on a 55 nm ULP process node. It’s designed around collecting and transmitting data within the tight constraints of self-powered operation. The SoC can run at 5 MHz with 12 microwatt power draw, and has a 2.19 microwatt power floor. It interfaces with a variety of sensors to gather data, and has a power-optimized Wifi/Bluetooth/5G radio for data transmission. An expansion port can connect to an external microcontroller and storage, which can also be powered off harvested energy.

On the processing side, the SoC includes an Arm Cortex M0+ microcontroller. Cortex M0+ is one Arm's lowest power cores, and comes with a simple two-stage pipeline. Its memory subsystem is similarly bare-bones, with no built-in caches and a memory port shared between instruction and data accesses. The chip includes 128 KB of SRAM and 256 KB of flash. Thus the SoC has less storage and less system memory than the original IBM PC but can clock higher which does go to show just how far silicon manufacturing has come in nearly 50 years.

# EH-PMU: Orchestrating Power Delivery

Energy harvesting is central to the chip’s goals, and is controlled by the Energy Harvesting Power Management Unit (EH-PMU). The EH-PMU uses a multiple input, single inductor, multiple output (MISIMO) topology, letting it simultaneously harvest energy from two energy sources and output power on four rails. For energy harvesting sources, Everactive gives light and temperature differences as examples because they’re often available. Light can be harvested from a photovoltaic cell (PV), and a thermoelectric generator (TEG) can do so from temperature differences. Depending on expected environmental conditions, the SoC can be set up with other energy sources like radio emissions, mechanical vibrations, or airflow.

Maximum power point tracking (MPPT) helps the EH-PMU improve energy harvesting efficiency by getting energy from each harvesting source at its optimal voltage. Because harvested energy can often be unstable despite using two sources and optimization techniques, the PKS3000 can store energy in a pair of capacitors. A supercapacitor provides deep energy storage, and aims to let the chip keep going under adverse conditions, A smaller capacitor charges faster, and can quickly collect power to speed up cold starts after brownouts. Everactive’s SoC can cold-start using the PV/TEG combo at 60 lux and 8 C, which is about equivalent to indoor lighting in a chilly room.

The EH-PMU’s powers four output rails, named 1p8, 1p2, 0p9, and adj, which can be fed off a harvesting source under good conditions. Under bad conditions, EH-PMU can feed them off stored energy in the capacitors. A set of pulse counters monitor energy flow throughout the chip. Collected energy statistics are fed to the Energy Aware Subsystem.

# Energy Aware Subsystem

The Energy Aware Subsystem (EAS) monitors energy harvesting, storage, and consumption to make power management decisions. It plays a role analogous to Intel’s Power Control Unit or AMD’s System Management Unit (SMU). Like Intel’s PCU or AMD’s SMU, the EAS manages frequency and voltage scaling with a set of different policies. Firmware can hook into the EAS to set maximum frequencies and power management policies, just as an OS would do on higher power platforms. Energy statistics can be used to decide when to enable components or perform OTA updates.

The EAS also controls a load switch that can be used to cut off external components. Everactive found that some external components have a high power floor. Shutting them off prevents them from monopolizing the chip’s very limited power budget. Components can be notified and allowed to perform a graceful shutdown. But the EAS also has the power to shut them off in a non-cooperative fashion. That gives the EAS more power than Intel’s PCU or AMD’s SMU, which can’t independently decide that some components should be shut off. But the EAS needs those powers because it has heavier responsibilities and constraints. For Everactive’s SoC, poor power management isn’t a question of slightly higher power bills or shorter battery life. Instead, it could cause frequent brownouts that prevent the SoC from providing timely sensor data updates. That’s highly non-ideal for industrial monitoring applications, where missed data could prevent operators from noticing a problem.

The EAS supports a Wait-for-Wakeup mode, which lets the device enter a low power mode where it can still respond very quickly to activity from sensors or the environment. Generally, Everactive’s SoC is geared towards trying to idle as often as possible.

# Wake-Up Radio

Idle optimizations extend to the radio. Communication is a challenge for self powered SoCs because radios can have a high power floor even if all they’re doing is staying connected to a network. Disconnecting is an option, but it’s a poor one because reconnecting introduces delays, and some access points don’t reliably handle frequent reconnects. Everactive attacks this problem with a Wake-Up Radio (WRX), which uses an always-on receiver capable of receiving a subset of messages at very low power. Compared to a conventional radio that uses duty cycling, wakeup receivers seek to reduce power wasted on idle monitoring while achieving lower latency.

Everactive’s WRX shares an antenna with an external communication transceiver, which the customer picks with their network design in mind. A RF switch lets the WRX share the antenna, and on-board matching networks pick the frequency. The passive path can operate from 300 MHz to 3 GHz, letting it support a wide range of standards with the appropriate on-board matching networks. A broadband signal is input to the wakeup receiver on the passive path, which does energy detection. Then, the WRX can do baseband gain or intermediate frequency (IF) gain depending on the protocol.

WRX power varies with configuration. Using the passive path without RF gain provides a very low baseline power of under a microwatt while providing respectable -63 dBm sensitivity for a sub-GHz application. That mode provides about 200m range, making it useful for industrial monitoring environments. Longer range applications (over 1000m) require more power, because RF boost has to get involved to increase sensitivity. To prevent high active power from becoming a problem, Everactive uses multi-stage wakeup and very fine grained duty cycling, letting the radio sample at times when it might get a bit of a wakeup message. With those techniques, the chip is able to achieve -92 dBm sensitivity while keeping power below 6 microwatts on average.

For comparison, Intel’s Wi-Fi 6 AX201 can achieve similar sensitivities, but idles at 1.6 mW in Core Power Down. Power goes up to 3.4 mW when associated with a 2.4 GHz access point. That sort of power draw is still very low in an absolute sense. But Everactive’s WRX setup pushes even lower, which is both impressive and reiterates the challenges associated with self powered operation. Everactive for their part sees standards moving in the direction of using wake-up radios. Wake-up receivers have been researched for decades, and continue to improve over time. There’s undeniably a benefit to idle power, and it’ll be interesting to see if WRX-es get more widely adopted.

# Final Words

Everactive’s PKS3000 is a showcase of extreme power saving measures. The goal of improving power efficiency is thrown around quite a lot. Datacenter GPUs strive for more FLOPS/watt. Laptop chips get power optimizations with each generation. But self powered SoCs really take things to the next level because their power budget is so limited. Many of Everactive’s optimizations shave off power on a microwatt scale, an order of magnitude below the milliwatts that mobile devices care about. PKS3000 can idle at 2.19 microwatts with some limitations, or under 4 microwatts with the wakeup receiver always on. Even under load, Everactive’s SoC draws order of magnitudes less power than the chips PC enthusiasts are familiar with, let alone the AI-oriented monster chips capable of drawing a kilowatt or more.

The PKS3000 improves over Everactive’s own PKS2001 SoC as well, reducing power while running at higher clocks and achieving better radio sensitivity. Pushing idle power down from 30 to 2.19 microwatts is impressive. Decreasing active power from 89.1 to 12 microwatts is commendable too. PKS3000 does move to a more advanced 55nm ULP node, compared to the 65nm node used by PKS2001. But a lot of improvements no doubt come from architectural techniques too.

And it’s important to not lose sight of the big picture. Neither SoC uses a cutting edge FinFET node, yet they’re able to accomplish their task with miniscule power requirements. Self powered SoCs have limitations of course, and it’s easy to see why Everactive focuses on industrial monitoring applications. But I do wonder if low power SoCs could cover a broader range of use cases as the technology develops, or if more funding lets them use modern process nodes. Everactive’s presentation was juxtaposed alongside talks on high power AI setups. Google talked about managing power swings on the megawatt scale with massive AI training deployments. Meta discussed how they increased per-rack power to 93.5 kW. Power consumption raises sustainability concerns with the current AI boom, and battery-less self-powered SoCs are so sweet from a sustainability perspective. I would love to see energy harvesting SoCs take on more tasks.

If you like the content then consider heading over to the [Patreon](https://www.patreon.com/ChipsandCheese) or [PayPal](https://www.paypal.com/donate/?hosted_button_id=4EMPH66SBGVSQ) if you want to toss a few bucks to Chips and Cheese. Also consider joining the [Discord](https://discord.gg/TwVnRhxgY2).

**References**

Cortex M0+ from Arm:

[https://developer.arm.com/Processors/Cortex-M0-Plus](https://developer.arm.com/Processors/Cortex-M0-Plus)Jesús ARGOTE-AGUILAR's thesis, "Powering Low-Power Wake-up Radios with RF Energy Harvesting":

[https://theses.hal.science/tel-05100987v1/file/ARGOTE_Jesus.pdf](https://theses.hal.science/tel-05100987v1/file/ARGOTE_Jesus.pdf)- gives an example of a wakeup receiver with 0.2 microwatt power consumption and -53 dBm sensitivity, and other examples with power going into the nanowatt range when no data is received.R. van Langevelde et al, "An Ultra-Low-Power 868/915 MHz RF Transceiver for Wireless Sensor Network Applications" at

[https://picture.iczhiku.com/resource/ieee/shkGpPyIRjUikxcX.pdf](https://picture.iczhiku.com/resource/ieee/shkGpPyIRjUikxcX.pdf)- ~1.2 microwatt sleep, 2.4 milliwatts receive, 2.7 milliwatts transmit, -89 dbM sensitivityNathan M. Pletcher et al, "A 52 μW Wake-Up Receiver With 72 dBm Sensitivity Using an Uncertain-IF Architecture" -

[https://people.eecs.berkeley.edu/~pister/290Q/Papers/Radios/Pletcher%20WakeUp%20jssc09.pdf](https://people.eecs.berkeley.edu/~pister/290Q/Papers/Radios/Pletcher%20WakeUp%20jssc09.pdf)- old WRX from 2009Jonathan K. Brown eta al, "A 65nm Energy-Harvesting ULP SoC with 256kB Cortex-M0 Enabling an 89.1µW Continuous Machine Health Monitoring Wireless Self-Powered System" - paper on Everactive's older SoC

Intel® Wi-Fi 6 AX201 (Harrison Peak 2) and Wi-Fi 6 AX101 (Harrison Peak 1) External Product Specifications (EPS)


Thanks Chester, yes, I agree, those are fascinating devices! In addition to having to manage on very little power indeed, I wonder if they mentioned anything about security, and how their designs are or can be protected. IoT devices in general have developed a poor reputation as easily exploitable, and with "always on" devices for monitoring, that must have occurred to the developers.

Fascinating!